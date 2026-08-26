"""
SECO/ALK Quality Test Fixtures

Multilingual document fixtures for testing anonymization, classification, and de-anonymization
of Swiss unemployment (ALK) and business support (SECO) documents.

All data is completely fictional but follows valid Swiss formats.
"""

from .documents_de import DOCS_DE
from .documents_en import DOCS_EN
from .documents_fr import DOCS_FR
from .documents_it import DOCS_IT
from .documents_rm import DOCS_RM

# All documents combined for bulk testing
ALL_DOCS = DOCS_DE + DOCS_FR + DOCS_IT + DOCS_RM + DOCS_EN

# Language-specific groupings
DOCS_BY_LANGUAGE = {
    "de": DOCS_DE,
    "fr": DOCS_FR,
    "it": DOCS_IT,
    "rm": DOCS_RM,
    "en": DOCS_EN,
}

__all__ = [
    "DOCS_DE",
    "DOCS_FR",
    "DOCS_IT",
    "DOCS_RM",
    "DOCS_EN",
    "ALL_DOCS",
    "DOCS_BY_LANGUAGE",
]
