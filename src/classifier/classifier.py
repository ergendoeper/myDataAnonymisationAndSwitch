"""
Data Classification Module

Uses Microsoft Presidio to detect sensitive entities in text and assigns
a classification level: SECRET, CONFIDENTIAL, INTERNAL, or PUBLIC.

Classification rules (conservative – falls back to CONFIDENTIAL when uncertain):
- SECRET     : Detected entities that are typically government/military grade
               (e.g., CRYPTO_KEY, NRP, IN_AADHAAR) OR explicit SECRET keyword
               present in the text with high confidence.
- CONFIDENTIAL: PII detected (PERSON, EMAIL, PHONE, CREDIT_CARD, IBAN_CODE, etc.)
               or the system cannot determine a lower classification.
- INTERNAL   : Low-severity entity types detected (LOCATION, DATE_TIME, ORG)
               without any PII or secret indicators.
- PUBLIC     : No entities detected and no secret/internal indicators.
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Classification levels (ordered by sensitivity – higher value = more sensitive)
# ---------------------------------------------------------------------------

class ClassificationLevel(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"

    @property
    def sensitivity(self) -> int:
        _order = {
            ClassificationLevel.PUBLIC: 0,
            ClassificationLevel.INTERNAL: 1,
            ClassificationLevel.CONFIDENTIAL: 2,
            ClassificationLevel.SECRET: 3,
        }
        return _order[self]

    def __ge__(self, other: "ClassificationLevel") -> bool:  # type: ignore[override]
        return self.sensitivity >= other.sensitivity

    def __gt__(self, other: "ClassificationLevel") -> bool:  # type: ignore[override]
        return self.sensitivity > other.sensitivity


# ---------------------------------------------------------------------------
# Entity type mappings
# ---------------------------------------------------------------------------

# Entities that immediately escalate to SECRET
_SECRET_ENTITIES = {
    "CRYPTO_KEY",
    "NRP",          # National Registration numbers – often state-secret-adjacent
    "IN_AADHAAR",
    "US_SSN",       # Sometimes treated as SECRET in defence contexts; conservative
    "UK_NHS",       # Can be secret in some contexts
    "MEDICAL_LICENSE",
    "PASSPORT",     # Passport numbers considered SECRET by some policies
}

# Entities that map to CONFIDENTIAL (PII)
_CONFIDENTIAL_ENTITIES = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "IBAN_CODE",
    "IP_ADDRESS",
    "DATE_TIME",   # Can be INTERNAL but keep conservative: treat as CONFIDENTIAL
    "URL",
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "US_PASSPORT",
    "AU_ABN",
    "AU_ACN",
    "AU_TFN",
    "SG_NRIC_FIN",
    "IN_PAN",
    "ES_NIF",
    "IT_FISCAL_CODE",
    "PL_PESEL",
    "FI_PERSONAL_IDENTITY_CODE",
    "NO_BAN_ID",
}

# Entities that map to INTERNAL
_INTERNAL_ENTITIES = {
    "LOCATION",
    "ORG",
    "ORGANIZATION",
}

# Keyword patterns that force SECRET classification regardless of NLP result
_SECRET_KEYWORDS_PATTERN = re.compile(
    r"\b(SECRET|TOP\s*SECRET|CLASSIFIED|GEHEIM|STRENG\s*GEHEIM|TS/SCI)\b",
    re.IGNORECASE,
)

# Keyword patterns that force CONFIDENTIAL classification
_CONFIDENTIAL_KEYWORDS_PATTERN = re.compile(
    r"\b(CONFIDENTIAL|VERTRAULICH|INTERN|PROPRIETARY|RESTRICTED)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class DataClassifier:
    """
    Classifies text as SECRET / CONFIDENTIAL / INTERNAL / PUBLIC.

    Parameters
    ----------
    score_threshold : float
        Minimum Presidio confidence score to consider an entity match.
    fallback_level : ClassificationLevel
        Level to assign when no entities are found and no keyword matches.
        Defaults to CONFIDENTIAL (conservative).
    presidio_language : str
        Language code for the Presidio NLP engine.
    """

    def __init__(
        self,
        score_threshold: float = 0.5,
        fallback_level: ClassificationLevel = ClassificationLevel.CONFIDENTIAL,
        presidio_language: str = "en",
    ) -> None:
        self.score_threshold = score_threshold
        self.fallback_level = fallback_level
        self.presidio_language = presidio_language
        self._analyzer = self._build_analyzer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(self, text: str) -> ClassificationLevel:
        """Return the classification level for the given text."""
        if not text or not text.strip():
            return self.fallback_level

        # 1. Keyword-based shortcuts (fast, deterministic)
        if _SECRET_KEYWORDS_PATTERN.search(text):
            logger.debug("SECRET keyword detected – classifying as SECRET")
            return ClassificationLevel.SECRET

        if _CONFIDENTIAL_KEYWORDS_PATTERN.search(text):
            logger.debug("CONFIDENTIAL keyword detected – classifying as CONFIDENTIAL")
            return ClassificationLevel.CONFIDENTIAL

        # 2. NLP-based entity detection via Presidio
        try:
            results = self._analyzer.analyze(
                text=text,
                language=self.presidio_language,
                score_threshold=self.score_threshold,
            )
        except Exception as exc:
            logger.warning(
                "Presidio analysis failed (%s); falling back to %s",
                exc,
                self.fallback_level,
            )
            return self.fallback_level

        if not results:
            return ClassificationLevel.PUBLIC

        return self._level_from_entities([r.entity_type for r in results])

    def classify_batch(self, texts: List[str]) -> List[ClassificationLevel]:
        """Classify multiple texts and return the list of classification levels."""
        return [self.classify(t) for t in texts]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_analyzer():
        """Lazily import and build the Presidio AnalyzerEngine."""
        try:
            from presidio_analyzer import AnalyzerEngine  # type: ignore
            return AnalyzerEngine()
        except ImportError as exc:
            raise RuntimeError(
                "presidio-analyzer is not installed. "
                "Install it with: pip install presidio-analyzer"
            ) from exc

    def _level_from_entities(
        self, entity_types: List[str]
    ) -> ClassificationLevel:
        """Map a list of entity type strings to a classification level."""
        level = ClassificationLevel.INTERNAL  # At minimum INTERNAL if entities found

        for entity_type in entity_types:
            if entity_type in _SECRET_ENTITIES:
                return ClassificationLevel.SECRET  # Escalate immediately
            if entity_type in _CONFIDENTIAL_ENTITIES:
                level = ClassificationLevel.CONFIDENTIAL
            elif entity_type in _INTERNAL_ENTITIES:
                if level < ClassificationLevel.CONFIDENTIAL:  # type: ignore[operator]
                    level = ClassificationLevel.INTERNAL

        # If we found entities but none matched our lists, fall back conservatively
        return level
