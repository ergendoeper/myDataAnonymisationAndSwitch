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
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from src.classifier import ClassificationLevel

logger = logging.getLogger(__name__)


class SecretDataRejectedError(Exception):
    """Raised when data classified as SECRET is submitted."""


@dataclass
class RouterConfig:
    """URL configuration for the three inference endpoints."""

    url_confidential: str
    url_internal: str
    url_public: str
    timeout_seconds: float = 60.0
    verify_ssl: bool = True


@dataclass
class RoutingResult:
    """Result of a routing + inference call."""

    classification: ClassificationLevel
    target_url: str
    payload: Dict[str, Any]
    anonymized: bool
    response: Optional[httpx.Response] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.response is not None and self.response.is_success


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

    async def route(
        self,
        payload: Dict[str, Any],
        level: ClassificationLevel,
        anonymized: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
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

        headers = {"Content-Type": "application/json"}
        if extra_headers:
            headers.update(extra_headers)

        result = RoutingResult(
            classification=level,
            target_url=target_url,
            payload=payload,
            anonymized=anonymized,
        )

        async with httpx.AsyncClient(
            timeout=self.config.timeout_seconds,
            verify=self.config.verify_ssl,
        ) as client:
            try:
                response = await client.post(
                    target_url, json=payload, headers=headers
                )
                result.response = response
                logger.info(
                    "Routed %s request to %s – status %s",
                    level.value,
                    target_url,
                    response.status_code,
                )
            except httpx.RequestError as exc:
                result.error = str(exc)
                logger.error(
                    "Failed to reach inference service at %s: %s", target_url, exc
                )

        return result
