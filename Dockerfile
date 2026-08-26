# ── Builder ──────────────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install pinned build deps; clean up immediately to keep layer lean
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential=12.9 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Download spaCy model in the builder stage (kept out of runtime image layers)
RUN python -m spacy download en_core_web_lg

# ── Runtime ───────────────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Create non-root user/group before any COPY so chown targets exist
RUN groupadd -r -g 10001 appuser && useradd -r -u 10001 -g appuser appuser

# Copy installed Python packages and spaCy model data from builder
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser --from=builder /root/.local /home/appuser/.local

# Copy application source with correct ownership
COPY --chown=appuser:appuser src/ src/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

# Use uvicorn with 2 workers; adjust via env var UVICORN_WORKERS
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
