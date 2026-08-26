"""Tests for the FastAPI application endpoints."""

from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# Minimal stubs for presidio so we can import the app without NLP models
# ---------------------------------------------------------------------------

def _install_presidio_stubs():
    class _FakeResult:
        def __init__(self, entity_type):
            self.entity_type = entity_type

    class _FakeAnalyzer:
        def analyze(self, text, language, score_threshold=0.5):
            # Simulate: if text contains "secret", return CRYPTO_KEY
            if "secret" in text.lower() or "SECRET" in text:
                return [_FakeResult("CRYPTO_KEY")]
            if "@" in text:
                return [_FakeResult("EMAIL_ADDRESS")]
            return []

    class _FakeAnonymizer:
        def anonymize(self, text, analyzer_results, operators=None):
            result = MagicMock()
            result.text = "[ANONYMIZED]"
            return result

    pa_mod = types.ModuleType("presidio_analyzer")
    pa_mod.AnalyzerEngine = _FakeAnalyzer

    pan_mod = types.ModuleType("presidio_anonymizer")
    pan_mod.AnonymizerEngine = _FakeAnonymizer

    pan_entities_mod = types.ModuleType("presidio_anonymizer.entities")

    class _OpConfig:
        def __init__(self, op, params=None):
            self.op = op
            self.params = params or {}

    pan_entities_mod.OperatorConfig = _OpConfig
    pan_mod.entities = pan_entities_mod

    sys.modules["presidio_analyzer"] = pa_mod
    sys.modules["presidio_anonymizer"] = pan_mod
    sys.modules["presidio_anonymizer.entities"] = pan_entities_mod


_install_presidio_stubs()


class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        from fastapi.testclient import TestClient
        from src.config import Settings
        from src.main import create_app

        settings = Settings(
            inference_url_confidential="http://svc-a/infer",
            inference_url_internal="http://svc-b/infer",
            inference_url_public="http://svc-c/infer",
            api_keys=[],
        )
        self.app = create_app(settings=settings)
        self.client = TestClient(self.app)

    def test_healthz(self):
        r = self.client.get("/healthz")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")

    def test_classify_public(self):
        r = self.client.post("/v1/classify", json={"text": "The sky is blue"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["classification"], "PUBLIC")

    def test_classify_secret_keyword(self):
        r = self.client.post("/v1/classify", json={"text": "TOP SECRET report"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["classification"], "SECRET")

    def test_infer_secret_returns_403(self):
        r = self.client.post(
            "/v1/infer",
            json={"messages": [{"role": "user", "content": "TOP SECRET payload"}]},
        )
        self.assertEqual(r.status_code, 403)

    def test_infer_routes_public(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = {"choices": []}

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            r = self.client.post(
                "/v1/infer",
                json={"messages": [{"role": "user", "content": "The sky is blue"}]},
            )

        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["classification"], "PUBLIC")
        self.assertIn("svc-c", data["target_url"])

    def test_infer_routes_confidential_when_email_detected(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = {"choices": []}

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            r = self.client.post(
                "/v1/infer",
                json={"messages": [{"role": "user", "content": "Email me at user@example.com"}]},
            )

        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["classification"], "CONFIDENTIAL")
        self.assertIn("svc-a", data["target_url"])
        self.assertTrue(data["anonymized"])

    def test_skip_anonymization_without_role_still_anonymizes(self):
        """Callers without an authorized role cannot skip anonymisation."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            r = self.client.post(
                "/v1/infer",
                json={
                    "messages": [{"role": "user", "content": "Email user@example.com"}],
                    "skip_anonymization": True,
                },
            )
        self.assertEqual(r.status_code, 200)
        # Without a valid role, anonymisation must proceed
        self.assertTrue(r.json()["anonymized"])


class TestAppWithApiKey(unittest.TestCase):

    def setUp(self):
        from fastapi.testclient import TestClient
        from src.config import Settings
        from src.main import create_app

        settings = Settings(
            inference_url_confidential="http://svc-a/infer",
            inference_url_internal="http://svc-b/infer",
            inference_url_public="http://svc-c/infer",
            api_keys=["valid-key"],
            api_key_roles="valid-key:admin",
            anonymization_skip_allowed_roles=["admin"],
        )
        self.app = create_app(settings=settings)
        self.client = TestClient(self.app)

    def test_missing_key_returns_401(self):
        r = self.client.post("/v1/classify", json={"text": "hello"})
        self.assertEqual(r.status_code, 401)

    def test_invalid_key_returns_401(self):
        r = self.client.post(
            "/v1/classify",
            json={"text": "hello"},
            headers={"X-API-Key": "bad-key"},
        )
        self.assertEqual(r.status_code, 401)

    def test_valid_key_allows_access(self):
        r = self.client.post(
            "/v1/classify",
            json={"text": "The sky is blue"},
            headers={"X-API-Key": "valid-key"},
        )
        self.assertEqual(r.status_code, 200)

    def test_admin_can_skip_anonymization(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            r = self.client.post(
                "/v1/infer",
                json={
                    "messages": [{"role": "user", "content": "plain text"}],
                    "skip_anonymization": True,
                },
                headers={"X-API-Key": "valid-key"},
            )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()["anonymized"])


if __name__ == "__main__":
    unittest.main()
