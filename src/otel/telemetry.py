"""
OpenTelemetry Telemetry Setup

Configures OTEL tracing, metrics, and logging for export via OTLP
(to Grafana Alloy or another OTEL collector).
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "inference-router")


def setup_telemetry(
    otlp_endpoint: Optional[str] = None,
    service_name: str = _SERVICE_NAME,
    enable_tracing: bool = True,
    enable_metrics: bool = True,
) -> None:
    """
    Initialise OTEL SDK.

    Parameters
    ----------
    otlp_endpoint : str | None
        GRPC OTLP collector endpoint, e.g. ``http://alloy:4317``.
        Falls back to the ``OTEL_EXPORTER_OTLP_ENDPOINT`` env var.
    service_name : str
        Service name reported in traces/metrics.
    enable_tracing : bool
        Whether to configure the TracerProvider.
    enable_metrics : bool
        Whether to configure the MeterProvider.
    """
    endpoint = otlp_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

    if not endpoint:
        logger.info("OTEL_EXPORTER_OTLP_ENDPOINT not set – skipping telemetry setup")
        return

    try:
        _setup_tracing(endpoint, service_name, enable_tracing)
        _setup_metrics(endpoint, service_name, enable_metrics)
    except ImportError as exc:
        logger.warning(
            "OpenTelemetry packages not fully installed (%s); telemetry disabled", exc
        )


def get_tracer(name: str = _SERVICE_NAME):
    """Return an OTEL Tracer (no-op if tracing not initialised)."""
    try:
        from opentelemetry import trace  # type: ignore
        return trace.get_tracer(name)
    except ImportError:
        return _NoOpTracer()


def get_meter(name: str = _SERVICE_NAME):
    """Return an OTEL Meter (no-op if metrics not initialised)."""
    try:
        from opentelemetry import metrics as otel_metrics  # type: ignore
        return otel_metrics.get_meter(name)
    except ImportError:
        return _NoOpMeter()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _setup_tracing(endpoint: str, service_name: str, enabled: bool) -> None:
    if not enabled:
        return
    from opentelemetry import trace  # type: ignore
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter  # type: ignore
    from opentelemetry.sdk.resources import Resource  # type: ignore

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    logger.info("OTEL tracing configured → %s", endpoint)


def _setup_metrics(endpoint: str, service_name: str, enabled: bool) -> None:
    if not enabled:
        return
    from opentelemetry import metrics as otel_metrics  # type: ignore
    from opentelemetry.sdk.metrics import MeterProvider  # type: ignore
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader  # type: ignore
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter  # type: ignore
    from opentelemetry.sdk.resources import Resource  # type: ignore

    resource = Resource.create({"service.name": service_name})
    exporter = OTLPMetricExporter(endpoint=endpoint, insecure=True)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15_000)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    otel_metrics.set_meter_provider(provider)
    logger.info("OTEL metrics configured → %s", endpoint)


# ---------------------------------------------------------------------------
# No-op fallbacks (avoids crashes when OTEL SDK not installed)
# ---------------------------------------------------------------------------

class _NoOpSpan:
    def __enter__(self): return self
    def __exit__(self, *_): pass
    def set_attribute(self, *_): pass
    def record_exception(self, *_): pass
    def set_status(self, *_): pass

class _NoOpTracer:
    def start_as_current_span(self, *_args, **_kwargs):
        return _NoOpSpan()
    def start_span(self, *_args, **_kwargs):
        return _NoOpSpan()

class _NoOpMeter:
    def create_counter(self, *_args, **_kwargs): return _NoOpCounter()
    def create_histogram(self, *_args, **_kwargs): return _NoOpCounter()

class _NoOpCounter:
    def add(self, *_args, **_kwargs): pass
    def record(self, *_args, **_kwargs): pass
