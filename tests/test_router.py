"""Tests for the InferenceRouter module."""

from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

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
            asyncio.get_event_loop().run_until_complete(
                r.route({"messages": []}, ClassificationLevel.SECRET)
            )

    def test_route_success(self):
        r = _make_router()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_response)

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            result = asyncio.get_event_loop().run_until_complete(
                r.route({"messages": []}, ClassificationLevel.PUBLIC)
            )

        self.assertTrue(result.success)
        self.assertEqual(result.target_url, "http://svc-c/infer")
        self.assertEqual(result.classification, ClassificationLevel.PUBLIC)

    def test_route_network_error(self):
        import httpx
        r = _make_router()

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=httpx.ConnectError("refused"))

        with patch("src.router.router.httpx.AsyncClient", return_value=mock_client):
            result = asyncio.get_event_loop().run_until_complete(
                r.route({"messages": []}, ClassificationLevel.INTERNAL)
            )

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)


if __name__ == "__main__":
    unittest.main()
