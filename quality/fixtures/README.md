# Quality Fixtures: SECO/ALK Multilingual Test Data

This directory contains comprehensive fake but realistic Swiss test data for the SECO/ALK anonymization router system.

## Overview

The fixtures provide multilingual documents with embedded personally identifiable information (PII) to test:

- **Anonymization**: Presidio-based PII detection and replacement
- **Classification**: Document sensitivity classification (PUBLIC, INTERNAL, CONFIDENTIAL, SECRET)
- **De-anonymization**: Roundtrip token mapping and reconstruction
- **Multilingual coverage**: German (DE), French (FR), Italian (IT), Rumantsch Grischun (RM), English (EN)

## Files

### Core Data

- **`dictionaries.py`** — Reusable fake Swiss data pools:
  - `FAKE_PERSONS`: 10 individuals with names, AHV numbers, IBANs, addresses, emails, insurance numbers
  - `FAKE_COMPANIES`: 5 employers with names, UIDs, addresses, contact persons
  - `FAKE_ADDRESSES`: 10 Swiss addresses (DE/FR/IT regions)
  - `FAKE_IBANS`: 10 valid-format IBANs
  - `FAKE_AHV_NUMBERS`: 10 AHV numbers with proper format (756.XXXX.XXXX.XX)
  - `FAKE_DOCTORS`: 5 doctors with GLN healthcare provider IDs
  - `FAKE_RAV_COUNSELORS`: 3 RAV employment counselors
  - `FAKE_UID_NUMBERS`: 5 Swiss company UIDs (CHE format)
  - `FAKE_GLN_NUMBERS`: 5 healthcare provider IDs
  - `FAKE_JOB_APPLICATIONS`: 8 realistic job applications (contact, date, method, result)
  - `FAKE_ICD10_CODES`: 5 ICD-10 disease codes (NOT PII - for testing non-anonymization)

### Documents by Language

Each language module contains realistic ALK/SECO documents:

#### `documents_de.py` (German - 14 documents)
1. Anmeldung zur Arbeitslosigkeit (Unemployment registration)
2. Taggeld-Abrechnung (Daily allowance statement)
3. Arbeitgeberbescheinigung (Employer certificate)
4. Kurzarbeitsantrag (Short-time work request)
5. Einsprache gegen Einstellung (Appeal against suspension)
6. Stellenbemühungen (Job search proof)
7. Ärztliches Attest (Medical certificate)
8. Kündigungsschreiben - Arbeitgeber (Termination by employer)
9. Kündigungsschreiben - Selbstkündigung (Self-termination)
10. Zwischenverdienst-Abrechnung (Interim income statement)
11. RAV-Beratungsprotokoll (Employment counseling protocol)
12. Verfügung Einstellung (Benefit suspension decision)
13. Pendenzmeldung (Reminder letter)
14. Antrag Insolvenzentschädigung (Insolvency compensation)

#### `documents_fr.py` (French - 14 documents)
French equivalents of German documents:
- Formulaire d'inscription au chômage
- Décompte indemnité journalière
- Attestation de l'employeur
- Demande RHT (Short-time work)
- Opposition à la suspension
- Justificatif des recherches d'emploi
- Certificat médical
- Lettre de résiliation (Employeur)
- Lettre de résiliation (Auto-Congé)
- Décompte revenu intermédiaire
- Protocole de consultation RAV
- Décision de suspension
- Mise en demeure
- Demande d'indemnité en cas d'insolvabilité

#### `documents_it.py` (Italian - 14 documents)
Italian equivalents for Ticino context:
- Modulo d'iscrizione alla disoccupazione
- Conteggio indennità giornaliera
- Attestato del datore di lavoro
- Domanda lavoro ridotto
- Opposizione alla sospensione
- Giustificativo ricerche di lavoro
- Certificato medico
- Lettera di licenziamento
- Lettera di dimissioni
- Conteggio reddito intermedio
- Verbale consultazione RAV
- Decisione sospensione
- Diffida (Reminder)
- Domanda indemnità insolvibilità

#### `documents_rm.py` (Rumantsch Grischun - 3 documents)
Essential documents in standardized Rumantsch (RM-CH):
- Annunzia tar la schanza (Unemployment registration)
- Quint da indemnisaziun (Benefit statement)
- Attest dal emprendider (Employer certificate)

#### `documents_en.py` (English - 3 documents)
International context:
- Application for Unemployment Benefits
- Short-Time Work Compensation Request
- Export Risk Guarantee (ERG) Application (SECO)

## PII Types Covered

Each document contains realistic PII fields for testing anonymization:

- **Names**: Swiss given names and surnames (Müller, Keller, Rossi, etc.)
- **AHV Numbers**: Swiss social insurance numbers (756 prefix, 13-digit)
- **IBANs**: Swiss bank account identifiers (CHxx format)
- **Addresses**: Real Swiss postal codes/cities + fictional street addresses
- **Email Addresses**: Realistic format (.ch domain)
- **Phone Numbers**: Swiss phone format (+41 XX ...)
- **Insurance Numbers**: ALK versicherungsnummern (ALK-XXXXXX)
- **UID Numbers**: Swiss company UIDs (CHE-XXX.XXX.XXX)
- **GLN Numbers**: Healthcare provider IDs (7-digit)
- **Betreibungsnummern**: Bankruptcy/debt collection reference numbers

## Non-PII Data (NOT Anonymized)

- **ICD-10 Codes**: Medical diagnosis codes (e.g., J06.9) - considered non-PII per Swiss privacy law
- **Locations**: City and canton names (public information)
- **Dates**: Employment periods, document dates

## How to Use

### Import All Documents
```python
from quality.fixtures import ALL_DOCS, DOCS_BY_LANGUAGE
```

### Import Language-Specific Documents
```python
from quality.fixtures import DOCS_DE, DOCS_FR, DOCS_IT, DOCS_RM, DOCS_EN
```

### Import Data Dictionaries
```python
from quality.fixtures.dictionaries import (
    FAKE_PERSONS, FAKE_COMPANIES, FAKE_ADDRESSES, FAKE_IBANS,
    FAKE_AHV_NUMBERS, FAKE_DOCTORS, FAKE_RAV_COUNSELORS,
    FAKE_UID_NUMBERS, FAKE_GLN_NUMBERS, FAKE_JOB_APPLICATIONS,
    FAKE_ICD10_CODES
)
```

### Use in Tests
```python
import pytest
from quality.fixtures import DOCS_DE

@pytest.mark.parametrize("doc", DOCS_DE)
def test_anonymization(doc):
    from src.anonymizer.anonymizer import DataAnonymizer
    anon = DataAnonymizer(language="de")
    anonymized = anon.anonymize(doc["text"])
    # Assert PII fields are replaced
    for pii_value in extract_pii_from_doc(doc):
        assert pii_value not in anonymized
```

## Adding New Fixtures

1. **Add data to `dictionaries.py`** if new PII pools are needed
2. **Create document in language-specific file** following the structure:
   ```python
   {
       "id": "unique_identifier",
       "title": "Document Title",
       "language": "de|fr|it|rm|en",
       "classification": "CONFIDENTIAL",  # or PUBLIC/INTERNAL/SECRET
       "text": """Full document text with PII fields embedded...""",
       "pii_fields": ["name", "ahv_number", "email", ...]
   }
   ```
3. **Update `__init__.py`** if adding a new language module

## Data Quality Notes

- **All data is completely fictional** - no real persons, companies, or accounts
- **Swiss format compliance**: AHV numbers, IBANs, UIDs follow correct formats with fake values
- **Regional authenticity**: Document types, terminology, and processes match actual ALK/SECO systems
- **Language quality**: Native-level German, French, Italian; Rumantsch uses standardized RM-CH (not regional variants like Sursilvan)

## Anonymization Testing Strategy

### Completeness Test
Verify all PII fields in `pii_fields` array are successfully anonymized.

### False-Positive Test
Ensure generic texts (without PII) remain unchanged after anonymization.

### Roundtrip Test
Anonymize → replace with tokens → de-anonymize → verify original reconstruction.

### Multilingual Coverage
Test Presidio detection across all 5 languages; document known limitations (e.g., Rumantsch support).

## Known Limitations

1. **Presidio Rumantsch Support**: Microsoft Presidio has limited support for Rumantsch Grischun.
   Expected: Lower detection rates for RM documents; may require custom patterns.
2. **Regional Dialects**: Fixtures use standardized languages (de_DE, fr_FR, it_IT, rm_CH, en_US).
3. **ICD-10 Codes**: Not anonymized per Swiss privacy regulations.

## Dependencies

- `presidio-analyzer` — PII entity detection
- `presidio-anonymizer` — PII replacement
- `ragas` — Quality evaluation (optional, for qua lity tests)
- `datasets` — Data handling for RAGAS

## References

- Swiss AHV number format: https://www.bsv.admin.ch/bsv/en/home/insurance/ahv/faq.html
- IBAN validation: https://www.iban.com/
- UID (UIDs) Switzerland: https://www.uid.admin.ch/
- SECO: https://www.seco.admin.ch/
- ALK (Unemployment Insurance): https://www.kav.admin.ch/
