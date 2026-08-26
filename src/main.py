"""
Inference-as-a-Service URL Switching Gateway
============================================

Classifies incoming data, optionally anonymises it via Presidio,
and routes the request to the appropriate inference service:

  SECRET       → 403 Rejected
  CONFIDENTIAL → Inference Service URL A
  INTERNAL     → Inference Service URL B
  PUBLIC       → Inference Service URL C
"""

from __future__ import annotations

import logging
import os
import time
import uuid
from typing import Annotated, Any, Dict, List, Optional

from fastapi import Body, Depends, FastAPI, Header, HTTPException, status
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.anonymizer import DataAnonymizer
from src.classifier import ClassificationLevel, DataClassifier
from src.config import Settings, get_settings
from src.otel import get_meter, get_tracer, setup_telemetry
from src.router import InferenceRouter
from src.router.router import RouterConfig, SecretDataRejectedError
import structlog

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger(__name__)
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger(__name__)


class RequestTooLargeError(Exception):
    pass

# ---------------------------------------------------------------------------
# Request / Response models (defined at module level so FastAPI resolves them)
# ---------------------------------------------------------------------------


class Message(BaseModel):
    role: str = Field(..., examples=["user"])
    content: str = Field(..., examples=["Hello, world!"])


class InferenceRequest(BaseModel):
    messages: List[Message] = Field(
        ..., description="Chat messages to send to the inference service."
    )
    model: Optional[str] = Field(
        default=None, description="Model identifier (forwarded as-is)."
    )
    skip_anonymization: bool = Field(
        default=False,
        description=(
            "When true and the requester has the appropriate role, "
            "skip PII anonymisation."
        ),
    )
    extra: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional parameters forwarded verbatim to the inference service.",
    )


class InferenceResponse(BaseModel):
    classification: str
    target_url: str
    anonymized: bool
    upstream_status: Optional[int] = None
    upstream_body: Optional[Any] = None
    error: Optional[str] = None


class ClassifyRequest(BaseModel):
    text: str = Field(..., description="Text to classify.")


class ClassifyResponse(BaseModel):
    classification: str
    text_length: int


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    cfg = settings or get_settings()

    # Telemetry
    setup_telemetry(
        otlp_endpoint=cfg.otel_exporter_otlp_endpoint,
        service_name=cfg.otel_service_name,
    )

    tracer = get_tracer(cfg.otel_service_name)
    meter = get_meter(cfg.otel_service_name)
    request_counter = meter.create_counter(
        "inference_router.requests",
        description="Total inference requests",
    )
    latency_histogram = meter.create_histogram(
        "inference_router.latency_ms",
        description="End-to-end request latency in ms",
    )
    classification_counter = meter.create_counter(
        "inference_router.classifications",
        description="Requests per classification level",
    )

    # Singleton components
    classifier = DataClassifier(
        score_threshold=cfg.classifier_score_threshold,
        presidio_language=cfg.classifier_language,
    )
    anonymizer = DataAnonymizer(
        language=cfg.classifier_language,
        score_threshold=cfg.classifier_score_threshold,
    )
    router_config = RouterConfig(
        url_confidential=str(cfg.inference_url_confidential),
        url_internal=str(cfg.inference_url_internal),
        url_public=str(cfg.inference_url_public),
        model_confidential=cfg.litellm_model_confidential,
        model_internal=cfg.litellm_model_internal,
        model_public=cfg.litellm_model_public,
        enable_fallbacks=cfg.litellm_enable_fallbacks,
        max_retries=cfg.litellm_max_retries,
        timeout_seconds=cfg.inference_timeout_seconds,
        verify_ssl=cfg.inference_verify_ssl,
    )
    inference_router = InferenceRouter(router_config)

    app = FastAPI(
        title="Inference-as-a-Service URL Switching Gateway",
        description=(
            "Classifies incoming data, anonymises PII via Presidio, "
            "and routes requests to the appropriate inference endpoint."
        ),
        version="1.0.0",
    )
    app.state.max_body_bytes = 1024 * 1024

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # Auth dependency
    # ------------------------------------------------------------------

    def _get_api_key(x_api_key: Annotated[Optional[str], Header()] = None) -> Optional[str]:
        if not cfg.api_keys:
            return None  # Auth disabled
        if x_api_key not in cfg.api_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key",
            )
        return x_api_key

    def _get_role(api_key: Optional[str] = Depends(_get_api_key)) -> Optional[str]:
        if api_key is None:
            return None
        return cfg.get_role_for_key(api_key)

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.get("/healthz", tags=["ops"])
    async def health():
        return {"status": "ok"}

    @app.get("/readyz", tags=["ops"])
    async def ready():
        return {"status": "ok"}

    @app.post("/v1/classify", response_model=ClassifyResponse, tags=["classify"])
    async def classify_text(
        req: Annotated[ClassifyRequest, Body()],
        _key: Optional[str] = Depends(_get_api_key),
    ):
        """Classify text without routing or anonymisation."""
        level = classifier.classify(req.text)
        return ClassifyResponse(
            classification=level.value,
            text_length=len(req.text),
        )

    @app.post("/v1/infer", response_model=InferenceResponse, tags=["inference"])
    async def infer(
        request: Request,
        req: Annotated[InferenceRequest, Body()],
        role: Optional[str] = Depends(_get_role),
    ):
        """
        Main endpoint: classify → (optionally anonymise) → route → return response.
        """
        t0 = time.monotonic()
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        body = await request.body()
        if len(body) > app.state.max_body_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={"request_id": request_id},
            )

        # Concatenate all message contents for classification
        full_text = " ".join(m.content for m in req.messages)

        with tracer.start_as_current_span("classify") as span:
            level = classifier.classify(full_text)
            span.set_attribute("classification", level.value)

        request_counter.add(1, {"classification": level.value})
        classification_counter.add(1, {"level": level.value})

        # Reject SECRET data immediately
        if level == ClassificationLevel.SECRET:
            latency_histogram.record(
                (time.monotonic() - t0) * 1000, {"classification": "SECRET"}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Request rejected: data classified as SECRET cannot be "
                    "forwarded to any inference service."
                ),
            )

        # Determine whether to anonymise
        should_anonymize = cfg.anonymizer_enabled
        if req.skip_anonymization:
            allowed_roles = set(cfg.anonymization_skip_allowed_roles)
            if role in allowed_roles:
                should_anonymize = False
                logger.info("Anonymisation skipped by role=%s", role)
            else:
                logger.warning(
                    "Role %s not allowed to skip anonymisation; proceeding with anonymisation",
                    role,
                )

        # Anonymise message contents
        messages_out = []
        for msg in req.messages:
            content = msg.content
            if should_anonymize:
                with tracer.start_as_current_span("anonymize"):
                    content = anonymizer.anonymize(content)
            messages_out.append({"role": msg.role, "content": content})

        # Build upstream payload
        payload: Dict[str, Any] = {"messages": messages_out}
        if req.model:
            payload["model"] = req.model
        if req.extra:
            payload.update(req.extra)

        # Route request
        try:
            with tracer.start_as_current_span("route") as span:
                result = await inference_router.route(
                    payload=payload,
                    level=level,
                    anonymized=should_anonymize,
                    request_id=request_id,
                )
                span.set_attribute("target_url", result.target_url)
        except SecretDataRejectedError as exc:  # belt-and-suspenders
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"request_id": request_id},
            )

        latency_histogram.record(
            (time.monotonic() - t0) * 1000, {"classification": level.value}
        )
        duration_ms = (time.monotonic() - t0) * 1000

        upstream_status = 200 if result.response else None
        upstream_body = result.response.model_dump() if result.response else None
        log.info(
            "inference_request",
            request_id=request_id,
            classification_level=level.value,
            target_model=cfg.litellm_model_public,
            anonymized=should_anonymize,
            duration_ms=duration_ms,
            status_code=upstream_status,
        )

        return InferenceResponse(
            classification=level.value,
            target_url=result.target_url,
            anonymized=should_anonymize,
            upstream_status=upstream_status,
            upstream_body=upstream_body,
            error=result.error,
        )

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

app = create_app()
