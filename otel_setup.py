"""OpenTelemetry bootstrap; no-op compatible when collector is absent."""

import logging

from opentelemetry import trace

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    provider = TracerProvider(
        resource=Resource.create({"service.name": "enterprise-rag-platform"})
    )
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
except (ImportError, RuntimeError) as exc:
    logging.getLogger(__name__).warning("OpenTelemetry setup unavailable: %s", exc)
tracer = trace.get_tracer("enterprise-rag-platform")
