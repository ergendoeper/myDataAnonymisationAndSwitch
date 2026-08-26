# myDataAnonymisationAndSwitch

**Inference-as-a-Service URL Switching Gateway** — classifies incoming data using
[Microsoft Presidio](https://microsoft.github.io/presidio/), anonymises PII, and
routes requests to the appropriate inference endpoint based on the data
classification level.

---

## Architecture Overview

```
Client
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│              Inference Router (FastAPI)                  │
│                                                          │
│  1. Classify text          (Presidio Analyzer)           │
│     SECRET  → 403 Rejected                              │
│     CONFIDENTIAL → URL A                                │
│     INTERNAL     → URL B                                │
│     PUBLIC       → URL C                                │
│                                                          │
│  2. Anonymise PII          (Presidio Anonymizer)         │
│     (skippable by authorised roles)                      │
│                                                          │
│  3. Forward to upstream inference service                │
└─────────────────────────────────────────────────────────┘
  │                │                │
  ▼                ▼                ▼
URL A          URL B            URL C
(CONFIDENTIAL) (INTERNAL)       (PUBLIC)

Observability: OTEL → Grafana Alloy → Prometheus / Loki / Grafana
Quality:       RAGAS evaluation script
```

---

## Classification Rules

| Level | Trigger |
|---|---|
| **SECRET** | Keyword: `SECRET`, `TOP SECRET`, `CLASSIFIED`, `GEHEIM`, `TS/SCI` _or_ Presidio entity: `CRYPTO_KEY`, `PASSPORT`, `NRP`, `US_SSN`, `IN_AADHAAR`, … |
| **CONFIDENTIAL** | Keyword: `CONFIDENTIAL`, `VERTRAULICH`, `PROPRIETARY` _or_ PII entity: `PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `CREDIT_CARD`, `IBAN_CODE`, … |
| **INTERNAL** | Entity: `LOCATION`, `ORG`, `ORGANIZATION` without any higher-classification signal |
| **PUBLIC** | No entities detected and no keyword match |

When uncertain and no indication of SECRET is present, the system falls back to
**CONFIDENTIAL** (conservative default).

---

## Quick Start (Docker Compose)

```bash
# 1. Copy and edit the environment variables
cp .env.example .env   # create a .env file with your inference URLs and API keys

# 2. Start all services (router + Alloy + Prometheus + Loki + Grafana)
docker compose up -d

# 3. Test the API
curl -X POST http://localhost:8000/v1/classify \
     -H "Content-Type: application/json" \
     -d '{"text": "My email is user@example.com"}'
# → {"classification":"CONFIDENTIAL","text_length":34}

curl -X POST http://localhost:8000/v1/infer \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-key" \
     -d '{"messages":[{"role":"user","content":"What is the weather today?"}]}'
```

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `INFERENCE_URL_CONFIDENTIAL` | `http://inference-service-a/v1/chat/completions` | URL A for CONFIDENTIAL data |
| `INFERENCE_URL_INTERNAL` | `http://inference-service-b/v1/chat/completions` | URL B for INTERNAL data |
| `INFERENCE_URL_PUBLIC` | `http://inference-service-c/v1/chat/completions` | URL C for PUBLIC data |
| `INFERENCE_TIMEOUT_SECONDS` | `60.0` | HTTP timeout for upstream calls |
| `INFERENCE_VERIFY_SSL` | `true` | Verify TLS certs on upstream calls |
| `LITELLM_MODEL_CONFIDENTIAL` | `openai/gpt-4o` | LiteLLM model alias for CONFIDENTIAL routing |
| `LITELLM_MODEL_INTERNAL` | `openai/gpt-4o-mini` | LiteLLM model alias for INTERNAL routing |
| `LITELLM_MODEL_PUBLIC` | `openai/gpt-3.5-turbo` | LiteLLM model alias for PUBLIC routing |
| `LITELLM_ENABLE_FALLBACKS` | `true` | Enable LiteLLM fallback chain |
| `LITELLM_MAX_RETRIES` | `3` | Max LiteLLM retry attempts |
| `API_KEYS` | _(empty – auth disabled)_ | Comma-separated list of API keys |
| `API_KEY_ROLES` | _(empty)_ | Key→role mapping, e.g. `key1:admin,key2:trusted` |
| `ANONYMIZER_ENABLED` | `true` | Enable anonymisation by default |
| `ANONYMIZATION_SKIP_ALLOWED_ROLES` | `["admin","trusted"]` | JSON list of roles that may skip anonymisation |
| `CLASSIFIER_SCORE_THRESHOLD` | `0.5` | Presidio minimum confidence score |
| `CLASSIFIER_LANGUAGE` | `en` | NLP language for Presidio |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | _(empty – OTEL disabled)_ | OTLP gRPC endpoint, e.g. `http://alloy:4317` |
| `OTEL_SERVICE_NAME` | `inference-router` | Service name in traces/metrics |
| `LOG_LEVEL` | `INFO` | Python log level |

### LiteLLM routing backend

Routing to URL A/B/C now uses `litellm.acompletion()` instead of direct `httpx` POST calls.
Each classification level maps to a configurable LiteLLM model alias while keeping the
same URL-based backend split via `api_base`:

- `CONFIDENTIAL` → `INFERENCE_URL_CONFIDENTIAL` + `LITELLM_MODEL_CONFIDENTIAL`
- `INTERNAL` → `INFERENCE_URL_INTERNAL` + `LITELLM_MODEL_INTERNAL`
- `PUBLIC` → `INFERENCE_URL_PUBLIC` + `LITELLM_MODEL_PUBLIC`

Structured JSON logs include `request_id`, `classification_level`, `target_model`,
`anonymized`, `duration_ms`, and `status_code`.

---

## API Endpoints

### `POST /v1/classify`
Classify text without routing or anonymisation.

**Request**
```json
{ "text": "My name is John Doe, call me at 555-1234." }
```
**Response**
```json
{ "classification": "CONFIDENTIAL", "text_length": 42 }
```

### `POST /v1/infer`
Classify → anonymise → route to the appropriate inference service.

**Request**
```json
{
  "messages": [{"role": "user", "content": "What is the capital of Germany?"}],
  "model": "gpt-4o",
  "skip_anonymization": false
}
```
**Response**
```json
{
  "classification": "PUBLIC",
  "target_url": "http://inference-service-c/v1/chat/completions",
  "anonymized": true,
  "upstream_status": 200,
  "upstream_body": { "choices": [...] },
  "error": null
}
```

`skip_anonymization: true` is silently ignored unless the caller's API key maps to
a role listed in `ANONYMIZATION_SKIP_ALLOWED_ROLES`.

### `GET /healthz` / `GET /readyz`
Liveness and readiness probes.

---

## Kubernetes Deployment

```bash
# 1. Create namespace and deploy Alloy
kubectl apply -f k8s/alloy.yaml

# 2. Edit k8s/inference-router.yaml – update image, URLs, and secrets
kubectl apply -f k8s/inference-router.yaml

# 3. Verify
kubectl -n inference-router get pods
kubectl -n inference-router port-forward svc/inference-router 8000:80
```

The manifest includes a `Deployment`, `Service`, `ConfigMap`, `Secret`,
`HorizontalPodAutoscaler`, and `Ingress`. Adjust the `Ingress` host and TLS
settings to match your cluster.

---

## Observability (OTEL → Alloy → Prometheus / Loki / Grafana)

The router exports:

| Signal | Name | Description |
|---|---|---|
| Counter | `inference_router.requests` | Total requests, labelled by `classification` |
| Counter | `inference_router.classifications` | Requests per `level` |
| Histogram | `inference_router.latency_ms` | End-to-end latency |

Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4317` to enable.

Grafana is available at http://localhost:3000 (compose) with Prometheus and Loki
pre-configured as data sources.

---

## Quality Evaluation (RAGAS)

```bash
# Run the evaluation script against a live router
python quality/ragas_eval.py \
  --endpoint http://localhost:8000 \
  --api-key your-key \
  --output quality/ragas_results.csv

# Dry-run mode (no LLM calls; uses ground-truth answers for CI)
python quality/ragas_eval.py --dry-run
```

RAGAS evaluates **faithfulness** and **answer_relevancy** out of the box.
Add more samples to `EVAL_SAMPLES` in `quality/ragas_eval.py`.

---

## Development

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install the spaCy model used by Presidio
python -m spacy download en_core_web_lg

# Install dev/test dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Run the server locally
uvicorn src.main:app --reload
```

---

## Security Notes

- **SECRET data is rejected** with HTTP 403 before it reaches any inference backend.
- **Anonymisation is on by default**; only callers with an authorised role can skip it.
- API keys are passed via `X-API-Key` header; TLS should be enforced in production
  (use cert-manager + Let's Encrypt in the supplied Ingress manifest).
- The container runs as a **non-root user** with `readOnlyRootFilesystem: true` and
  all Linux capabilities dropped.

---

## License

See [LICENSE](LICENSE).
