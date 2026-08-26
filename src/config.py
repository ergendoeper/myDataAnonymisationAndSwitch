"""
Application configuration via Pydantic Settings.

All values can be overridden via environment variables or a .env file.
"""

from __future__ import annotations

from typing import List, Optional, Set

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Inference service URLs
    # ------------------------------------------------------------------
    inference_url_confidential: AnyHttpUrl = Field(
        default="http://inference-service-a/v1/chat/completions",
        description="Inference endpoint for CONFIDENTIAL data (URL A).",
    )
    inference_url_internal: AnyHttpUrl = Field(
        default="http://inference-service-b/v1/chat/completions",
        description="Inference endpoint for INTERNAL data (URL B).",
    )
    inference_url_public: AnyHttpUrl = Field(
        default="http://inference-service-c/v1/chat/completions",
        description="Inference endpoint for PUBLIC data (URL C).",
    )
    inference_timeout_seconds: float = Field(
        default=60.0, description="HTTP timeout for upstream inference calls."
    )
    inference_verify_ssl: bool = Field(
        default=True, description="Verify TLS certificates for upstream calls."
    )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------
    classifier_score_threshold: float = Field(
        default=0.5,
        description="Presidio minimum confidence score to treat an entity as detected.",
    )
    classifier_language: str = Field(
        default="en", description="NLP language for Presidio."
    )

    # ------------------------------------------------------------------
    # Anonymisation
    # ------------------------------------------------------------------
    anonymizer_enabled: bool = Field(
        default=True, description="Enable data anonymisation by default."
    )
    # Users (by API key name / subject claim) allowed to skip anonymisation
    anonymization_skip_allowed_roles: List[str] = Field(
        default=["admin", "trusted"],
        description="Roles/subjects permitted to set skip_anonymization=true.",
    )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    api_keys: List[str] = Field(
        default_factory=list,
        description=(
            "Comma-separated list of static API keys accepted in the "
            "X-API-Key header. Leave empty to disable static key auth."
        ),
    )
    # Roles per API key – format: "key1:role1,key2:role2"
    api_key_roles: str = Field(
        default="",
        description="Mapping of API keys to roles. Format: key:role,key2:role2",
    )

    @field_validator("api_keys", mode="before")
    @classmethod
    def _split_api_keys(cls, v):
        if isinstance(v, str):
            return [k.strip() for k in v.split(",") if k.strip()]
        return v

    def get_role_for_key(self, api_key: str) -> Optional[str]:
        """Return the role associated with an API key, or None."""
        if not self.api_key_roles:
            return None
        mapping = {}
        for pair in self.api_key_roles.split(","):
            parts = pair.strip().split(":", 1)
            if len(parts) == 2:
                mapping[parts[0].strip()] = parts[1].strip()
        return mapping.get(api_key)

    # ------------------------------------------------------------------
    # OpenTelemetry
    # ------------------------------------------------------------------
    otel_exporter_otlp_endpoint: Optional[str] = Field(
        default=None,
        description="OTLP gRPC endpoint, e.g. http://alloy:4317.",
    )
    otel_service_name: str = Field(
        default="inference-router",
        description="Service name reported to the OTEL collector.",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    log_level: str = Field(default="INFO", description="Python logging level.")
    cors_origins: List[str] = Field(
        default=["*"], description="Allowed CORS origins."
    )


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Return (and cache) the application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
