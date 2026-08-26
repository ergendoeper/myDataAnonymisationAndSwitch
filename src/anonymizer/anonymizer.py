"""
Data Anonymisation Module

Uses Microsoft Presidio Analyzer + Anonymizer to redact / replace PII entities
in text before forwarding to an inference service.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DataAnonymizer:
    """
    Anonymizes text using Presidio Analyzer + Anonymizer.

    Parameters
    ----------
    language : str
        Language code for the Presidio NLP engine.
    score_threshold : float
        Minimum Presidio confidence score to anonymize an entity.
    operators : dict | None
        Custom Presidio anonymization operators per entity type.
        Defaults to replacing each entity type with a labeled placeholder,
        e.g. ``<PERSON>`` for a person's name.
    """

    def __init__(
        self,
        language: str = "en",
        score_threshold: float = 0.5,
        operators: Optional[Dict] = None,
    ) -> None:
        self.language = language
        self.score_threshold = score_threshold
        self._operators = operators
        self._analyzer = None
        self._anonymizer = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def anonymize(self, text: str) -> str:
        """Return an anonymized copy of *text*."""
        if not text or not text.strip():
            return text

        analyzer = self._get_analyzer()
        anonymizer = self._get_anonymizer()

        try:
            results = analyzer.analyze(
                text=text,
                language=self.language,
                score_threshold=self.score_threshold,
            )
        except Exception as exc:
            logger.warning("Presidio analysis failed (%s); returning original text", exc)
            return text

        if not results:
            return text

        try:
            operators = self._build_operators(results)
            anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
            return anonymized.text
        except Exception as exc:
            logger.warning("Presidio anonymization failed (%s); returning original text", exc)
            return text

    def get_entities(self, text: str) -> List[str]:
        """Return a list of detected entity types in *text*."""
        try:
            analyzer = self._get_analyzer()
            results = analyzer.analyze(
                text=text,
                language=self.language,
                score_threshold=self.score_threshold,
            )
            return [r.entity_type for r in results]
        except Exception as exc:
            logger.warning("Presidio analysis failed (%s)", exc)
            return []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_analyzer(self):
        if self._analyzer is None:
            try:
                from presidio_analyzer import AnalyzerEngine  # type: ignore
                self._analyzer = AnalyzerEngine()
            except ImportError as exc:
                raise RuntimeError(
                    "presidio-analyzer is not installed. "
                    "Install it with: pip install presidio-analyzer"
                ) from exc
        return self._analyzer

    def _get_anonymizer(self):
        if self._anonymizer is None:
            try:
                from presidio_anonymizer import AnonymizerEngine  # type: ignore
                self._anonymizer = AnonymizerEngine()
            except ImportError as exc:
                raise RuntimeError(
                    "presidio-anonymizer is not installed. "
                    "Install it with: pip install presidio-anonymizer"
                ) from exc
        return self._anonymizer

    def _build_operators(self, results) -> Dict:
        """Build per-entity operator map, using custom if provided, else replace."""
        if self._operators:
            return self._operators

        try:
            from presidio_anonymizer.entities import OperatorConfig  # type: ignore
        except ImportError:
            return {}

        operators: Dict[str, OperatorConfig] = {}
        for r in results:
            if r.entity_type not in operators:
                operators[r.entity_type] = OperatorConfig(
                    "replace", {"new_value": f"<{r.entity_type}>"}
                )
        return operators
