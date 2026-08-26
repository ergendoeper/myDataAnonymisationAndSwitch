"""
Inference Router

Routes a request to the correct inference service URL based on the
data classification level.

  SECRET       → Rejected (raises SecretDataRejectedError)
  CONFIDENTIAL → Inference Service URL A
  INTERNAL     → Inference Service URL B
  PUBLIC       → Inference Service URL C
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

import litellm
import structlog
from litellm.types.utils import ModelResponse

from src.classifier import ClassificationLevel

logger = logging.getLogger(__name__)
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger(__name__)


class SecretDataRejectedError(Exception):
    """Raised when data classified as SECRET is submitted."""


@dataclass
class RouterConfig:
    """Backend/model configuration for the three inference endpoints."""

    url_confidential: str
    url_internal: str
    url_public: str
    model_confidential: str = "openai/gpt-4o"
    model_internal: str = "openai/gpt-4o-mini"
    model_public: str = "openai/gpt-3.5-turbo"
    enable_fallbacks: bool = True
    max_retries: int = 3
    timeout_seconds: float = 60.0
    verify_ssl: bool = True


@dataclass
class RoutingResult:
    """Result of a routing + inference call."""

    classification: ClassificationLevel
    target_url: str
    payload: Dict[str, Any]
    anonymized: bool
    request_id: str
    response: Optional[ModelResponse] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.response is not None and self.error is None


class InferenceRouter:
    """
    Routes inference requests to the correct backend URL.

    Parameters
    ----------
    config : RouterConfig
        Holds the three inference endpoint URLs and connection settings.
    """

    def __init__(self, config: RouterConfig) -> None:
        self.config = config
        litellm.set_verbose = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_target_url(self, level: ClassificationLevel) -> str:
        """Return the target URL for a given classification level.

        Raises SecretDataRejectedError for SECRET data.
        """
        if level == ClassificationLevel.SECRET:
            raise SecretDataRejectedError(
                "Data classified as SECRET cannot be forwarded to any inference service."
            )
        mapping = {
            ClassificationLevel.CONFIDENTIAL: self.config.url_confidential,
            ClassificationLevel.INTERNAL: self.config.url_internal,
            ClassificationLevel.PUBLIC: self.config.url_public,
        }
        return mapping[level]

    def get_target_model(self, level: ClassificationLevel) -> str:
        """Return the configured LiteLLM model alias for a classification level."""
        if level == ClassificationLevel.SECRET:
            raise SecretDataRejectedError(
                "Data classified as SECRET cannot be forwarded to any inference service."
            )
        mapping = {
            ClassificationLevel.CONFIDENTIAL: self.config.model_confidential,
            ClassificationLevel.INTERNAL: self.config.model_internal,
            ClassificationLevel.PUBLIC: self.config.model_public,
        }
        return mapping[level]

    async def route(
        self,
        payload: Dict[str, Any],
        level: ClassificationLevel,
        anonymized: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
        request_id: Optional[str] = None,
    ) -> RoutingResult:
        """
        Forward *payload* to the appropriate inference endpoint.

        Parameters
        ----------
        payload : dict
            The JSON body to send to the inference service.
        level : ClassificationLevel
            Pre-computed data classification level.
        anonymized : bool
            Whether the payload has already been anonymized.
        extra_headers : dict | None
            Additional HTTP headers to include in the request.
        """
        try:
            target_url = self.get_target_url(level)
        except SecretDataRejectedError:
            raise

        target_model = self.get_target_model(level)

        result = RoutingResult(
            classification=level,
            target_url=target_url,
            payload=payload,
            anonymized=anonymized,
            request_id=request_id or str(uuid.uuid4()),
        )

        acompletion_kwargs: Dict[str, Any] = {
            "model": target_model,
            "api_base": target_url,
            "messages": payload["messages"],
            "num_retries": self.config.max_retries,
            "request_timeout": self.config.timeout_seconds,
            "ssl_verify": self.config.verify_ssl,
        }
        if extra_headers:
            acompletion_kwargs["extra_headers"] = extra_headers
        if self.config.enable_fallbacks:
            acompletion_kwargs["fallbacks"] = [
                self.config.model_confidential,
                self.config.model_internal,
                self.config.model_public,
            ]
        if "model" in payload:
            acompletion_kwargs["model"] = payload["model"]
        for key, value in payload.items():
            if key not in {"messages", "model"}:
                acompletion_kwargs[key] = value

        try:
            response = await litellm.acompletion(**acompletion_kwargs)
            result.response = response
            log.info(
                "litellm_route_success",
                request_id=result.request_id,
                classification_level=level.value,
                target_model=acompletion_kwargs["model"],
                anonymized=anonymized,
                duration_ms=None,
                status_code=200,
            )
        except litellm.exceptions.AuthenticationError as exc:
            result.error = str(exc)
            log.error(
                "litellm_route_auth_error",
                request_id=result.request_id,
                classification_level=level.value,
                target_model=target_model,
                anonymized=anonymized,
                duration_ms=None,
                status_code=502,
            )
        except Exception:
            result.error = "upstream inference request failed"
            log.error(
                "litellm_route_error",
                request_id=result.request_id,
                classification_level=level.value,
                target_model=target_model,
                anonymized=anonymized,
                duration_ms=None,
                status_code=500,
            )

        return result
