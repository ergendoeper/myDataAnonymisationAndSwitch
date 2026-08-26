"""Tests for the DataClassifier module (no Presidio dependency required)."""

from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Minimal Presidio stubs so tests run without the full NLP install
# ---------------------------------------------------------------------------

def _make_presidio_stub(entities_by_text: dict):
    """Return a fake AnalyzerEngine that returns pre-canned results."""

    class _FakeResult:
        def __init__(self, entity_type):
            self.entity_type = entity_type

    class _FakeAnalyzer:
        def analyze(self, text, language, score_threshold=0.5):
            return [_FakeResult(e) for e in entities_by_text.get(text, [])]

    presidio_analyzer_mod = types.ModuleType("presidio_analyzer")
    presidio_analyzer_mod.AnalyzerEngine = _FakeAnalyzer
    return presidio_analyzer_mod


class TestDataClassifier(unittest.TestCase):

    def _get_classifier(self, entities_by_text: dict):
        """Return a DataClassifier backed by a stubbed Presidio analyzer."""
        stub_mod = _make_presidio_stub(entities_by_text)
        with patch.dict(sys.modules, {"presidio_analyzer": stub_mod}):
            from src.classifier.classifier import DataClassifier
            c = DataClassifier(score_threshold=0.5)
            # Inject the fake analyzer directly
            c._analyzer = stub_mod.AnalyzerEngine()
        return c

    # ------------------------------------------------------------------
    # Keyword-based classification
    # ------------------------------------------------------------------

    def test_secret_keyword_forces_secret(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        with patch.dict(sys.modules, {"presidio_analyzer": _make_presidio_stub({})}):
            c = DataClassifier.__new__(DataClassifier)
            c.score_threshold = 0.5
            c.fallback_level = ClassificationLevel.CONFIDENTIAL
            c.presidio_language = "en"
            c._analyzer = _make_presidio_stub({}).AnalyzerEngine()

        result = c.classify("This document is marked TOP SECRET")
        self.assertEqual(result, ClassificationLevel.SECRET)

    def test_confidential_keyword_forces_confidential(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({}).AnalyzerEngine()

        result = c.classify("CONFIDENTIAL - internal use only")
        self.assertEqual(result, ClassificationLevel.CONFIDENTIAL)

    def test_empty_text_returns_fallback(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({}).AnalyzerEngine()

        result = c.classify("")
        self.assertEqual(result, ClassificationLevel.CONFIDENTIAL)

    # ------------------------------------------------------------------
    # Entity-based classification
    # ------------------------------------------------------------------

    def test_pii_entity_maps_to_confidential(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        text = "Call me at 555-123-4567"
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({text: ["PHONE_NUMBER"]}).AnalyzerEngine()

        result = c.classify(text)
        self.assertEqual(result, ClassificationLevel.CONFIDENTIAL)

    def test_crypto_key_entity_maps_to_secret(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        text = "key = abc123"
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({text: ["CRYPTO_KEY"]}).AnalyzerEngine()

        result = c.classify(text)
        self.assertEqual(result, ClassificationLevel.SECRET)

    def test_location_entity_maps_to_internal(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        text = "Meet me in Berlin"
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({text: ["LOCATION"]}).AnalyzerEngine()

        result = c.classify(text)
        self.assertEqual(result, ClassificationLevel.INTERNAL)

    def test_no_entities_returns_public(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        text = "The sky is blue"
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({}).AnalyzerEngine()

        result = c.classify(text)
        self.assertEqual(result, ClassificationLevel.PUBLIC)

    def test_classify_batch(self):
        from src.classifier.classifier import DataClassifier, ClassificationLevel
        texts = ["The sky is blue", "TOP SECRET document"]
        c = DataClassifier.__new__(DataClassifier)
        c.score_threshold = 0.5
        c.fallback_level = ClassificationLevel.CONFIDENTIAL
        c.presidio_language = "en"
        c._analyzer = _make_presidio_stub({}).AnalyzerEngine()

        results = c.classify_batch(texts)
        self.assertEqual(results[0], ClassificationLevel.PUBLIC)
        self.assertEqual(results[1], ClassificationLevel.SECRET)

    # ------------------------------------------------------------------
    # ClassificationLevel ordering
    # ------------------------------------------------------------------

    def test_classification_level_ordering(self):
        from src.classifier.classifier import ClassificationLevel
        self.assertGreater(ClassificationLevel.SECRET, ClassificationLevel.CONFIDENTIAL)
        self.assertGreater(ClassificationLevel.CONFIDENTIAL, ClassificationLevel.INTERNAL)
        self.assertGreater(ClassificationLevel.INTERNAL, ClassificationLevel.PUBLIC)


if __name__ == "__main__":
    unittest.main()
