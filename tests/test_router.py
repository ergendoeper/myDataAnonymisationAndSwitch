"""Tests for the InferenceRouter module."""

from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import litellm
from src.classifier.classifier import ClassificationLevel
from src.router.router import InferenceRouter, RouterConfig, SecretDataRejectedError


def _make_router():
    cfg = RouterConfig(
        url_confidential="http://svc-a/infer",
        url_internal="http://svc-b/infer",
        url_public="http://svc-c/infer",
    )
    return InferenceRouter(cfg)


class TestInferenceRouter(unittest.TestCase):
    def run_async(self, coro):
        return asyncio.run(coro)

    def test_get_target_url_confidential(self):
        r = _make_router()
        self.assertEqual(r.get_target_url(ClassificationLevel.CONFIDENTIAL), "http://svc-a/infer")

    def test_get_target_url_internal(self):
        r = _make_router()
        self.assertEqual(r.get_target_url(ClassificationLevel.INTERNAL), "http://svc-b/infer")

    def test_get_target_url_public(self):
        r = _make_router()
        self.assertEqual(r.get_target_url(ClassificationLevel.PUBLIC), "http://svc-c/infer")

    def test_get_target_url_secret_raises(self):
        r = _make_router()
        with self.assertRaises(SecretDataRejectedError):
            r.get_target_url(ClassificationLevel.SECRET)

    def test_route_secret_raises(self):
        r = _make_router()
        with self.assertRaises(SecretDataRejectedError):
            self.run_async(r.route({"messages": []}, ClassificationLevel.SECRET))

    def test_route_success(self):
        r = _make_router()
        mock_response = AsyncMock(spec=litellm.types.utils.ModelResponse)
        mock_response.model_dump.return_value = {"choices": [{"message": {"content": "ok"}}]}
        with patch("src.router.router.litellm.acompletion", new=AsyncMock(return_value=mock_response)):
            result = self.run_async(r.route({"messages": []}, ClassificationLevel.PUBLIC))

        self.assertTrue(result.success)
        self.assertEqual(result.target_url, "http://svc-c/infer")
        self.assertEqual(result.classification, ClassificationLevel.PUBLIC)
        self.assertEqual(result.request_id is not None, True)

    def test_route_auth_error(self):
        r = _make_router()
        with patch(
            "src.router.router.litellm.acompletion",
            new=AsyncMock(side_effect=litellm.exceptions.AuthenticationError("bad key", "openai", "gpt-4o")),
        ):
            result = self.run_async(r.route({"messages": []}, ClassificationLevel.INTERNAL))

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIn("bad key", result.error)

    def test_route_generic_error(self):
        r = _make_router()
        with patch("src.router.router.litellm.acompletion", new=AsyncMock(side_effect=Exception("refused"))):
            result = self.run_async(r.route({"messages": []}, ClassificationLevel.INTERNAL))

        self.assertFalse(result.success)
        self.assertEqual(result.error, "upstream inference request failed")


if __name__ == "__main__":
    unittest.main()
