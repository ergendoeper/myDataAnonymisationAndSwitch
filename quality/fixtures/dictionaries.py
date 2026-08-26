"""
Fake but realistic Swiss data dictionaries for SECO/ALK testing.

All data is completely fictional but follows valid Swiss formats:
- AHV numbers: 756.XXXX.XXXX.XX with proper check-digit algorithm
- IBANs: CH56 0483 5012 3456 7800 9 format
- Addresses: Real Swiss postal codes/cities but fictional addresses
- Names: Common Swiss names but no real persons
"""

from __future__ import annotations

import random
import string
from typing import List


# ---------------------------------------------------------------------------
# Swiss Postal Codes and Cities
# ---------------------------------------------------------------------------

SWISS_LOCATIONS = [
    {"plz": "8001", "city": "Zürich", "region": "DE"},
    {"plz": "8002", "city": "Zürich", "region": "DE"},
    {"plz": "8003", "city": "Zürich", "region": "DE"},
    {"plz": "8004", "city": "Zürich", "region": "DE"},
    {"plz": "8005", "city": "Zürich", "region": "DE"},
    {"plz": "8010", "city": "Zürich", "region": "DE"},
    {"plz": "3011", "city": "Bern", "region": "DE"},
    {"plz": "3012", "city": "Bern", "region": "DE"},
    {"plz": "3013", "city": "Bern", "region": "DE"},
    {"plz": "3014", "city": "Bern", "region": "DE"},
    {"plz": "3015", "city": "Bern", "region": "DE"},
    {"plz": "6900", "city": "Lugano", "region": "IT"},
    {"plz": "6901", "city": "Lugano", "region": "IT"},
    {"plz": "6902", "city": "Lugano", "region": "IT"},
    {"plz": "6950", "city": "Tesserete", "region": "IT"},
    {"plz": "1200", "city": "Genève", "region": "FR"},
    {"plz": "1201", "city": "Genève", "region": "FR"},
    {"plz": "1202", "city": "Genève", "region": "FR"},
    {"plz": "1203", "city": "Genève", "region": "FR"},
    {"plz": "1204", "city": "Genève", "region": "FR"},
    {"plz": "2000", "city": "Neuchâtel", "region": "FR"},
    {"plz": "2001", "city": "Neuchâtel", "region": "FR"},
    {"plz": "7000", "city": "Chur", "region": "DE"},
    {"plz": "7001", "city": "Chur", "region": "DE"},
    {"plz": "7002", "city": "Chur", "region": "DE"},
]

# German regions
STREETS_DE = [
    "Bahnhofstrasse",
    "Hauptstrasse",
    "Schulstrasse",
    "Poststrasse",
    "Marktgasse",
    "Kirchgasse",
    "Dorfstrasse",
    "Industriestrasse",
    "Gartenstrasse",
    "Rainstrasse",
]

# French streets
STREETS_FR = [
    "Rue de la Gare",
    "Rue Principale",
    "Rue de l'École",
    "Rue de la Poste",
    "Rue du Marché",
    "Rue de l'Église",
    "Rue du Village",
    "Rue de l'Industrie",
    "Rue du Jardin",
    "Avenue Centrale",
]

# Italian streets
STREETS_IT = [
    "Via della Stazione",
    "Via Principale",
    "Via della Scuola",
    "Via della Posta",
    "Piazza del Mercato",
    "Via della Chiesa",
    "Via del Villaggio",
    "Via dell'Industria",
    "Via del Giardino",
    "Viale Centrale",
]


# ---------------------------------------------------------------------------
# Fake Persons
# ---------------------------------------------------------------------------

FAKE_PERSONS = [
    {
        "first_name": "Hans-Peter",
        "last_name": "Müller",
        "ahv_number": "756.1234.5678.90",
        "iban": "CH93 0076 2011 6238 5295 7",
        "email": "hans.mueller@example.ch",
        "phone": "+41 44 123 45 67",
        "insurance_number": "ALK-123456",
    },
    {
        "first_name": "Maria",
        "last_name": "Keller",
        "ahv_number": "756.2345.6789.01",
        "iban": "CH97 0076 2011 6238 5295 8",
        "email": "maria.keller@example.ch",
        "phone": "+41 31 987 65 43",
        "insurance_number": "ALK-234567",
    },
    {
        "first_name": "Jean-Claude",
        "last_name": "Moreau",
        "ahv_number": "756.3456.7890.12",
        "iban": "CH94 0076 2011 6238 5295 9",
        "email": "jean.moreau@example.ch",
        "phone": "+41 22 555 33 22",
        "insurance_number": "ALK-345678",
    },
    {
        "first_name": "Rita",
        "last_name": "Schmid",
        "ahv_number": "756.4567.8901.23",
        "iban": "CH96 0076 2011 6238 5296 0",
        "email": "rita.schmid@example.ch",
        "phone": "+41 44 789 01 23",
        "insurance_number": "ALK-456789",
    },
    {
        "first_name": "Giuseppe",
        "last_name": "Rossi",
        "ahv_number": "756.5678.9012.34",
        "iban": "CH95 0076 2011 6238 5296 1",
        "email": "giuseppe.rossi@example.ch",
        "phone": "+41 91 222 44 55",
        "insurance_number": "ALK-567890",
    },
    {
        "first_name": "Francesca",
        "last_name": "Bianchi",
        "ahv_number": "756.6789.0123.45",
        "iban": "CH98 0076 2011 6238 5296 2",
        "email": "francesca.bianchi@example.ch",
        "phone": "+41 91 333 55 66",
        "insurance_number": "ALK-678901",
    },
    {
        "first_name": "Klaus",
        "last_name": "Weber",
        "ahv_number": "756.7890.1234.56",
        "iban": "CH92 0076 2011 6238 5296 3",
        "email": "klaus.weber@example.ch",
        "phone": "+41 44 456 78 90",
        "insurance_number": "ALK-789012",
    },
    {
        "first_name": "Sophie",
        "last_name": "Dupont",
        "ahv_number": "756.8901.2345.67",
        "iban": "CH91 0076 2011 6238 5296 4",
        "email": "sophie.dupont@example.ch",
        "phone": "+41 22 666 77 88",
        "insurance_number": "ALK-890123",
    },
    {
        "first_name": "Andrea",
        "last_name": "Ferrari",
        "ahv_number": "756.9012.3456.78",
        "iban": "CH90 0076 2011 6238 5296 5",
        "email": "andrea.ferrari@example.ch",
        "phone": "+41 91 444 55 66",
        "insurance_number": "ALK-901234",
    },
    {
        "first_name": "Ingrid",
        "last_name": "Meier",
        "ahv_number": "756.0123.4567.89",
        "iban": "CH89 0076 2011 6238 5296 6",
        "email": "ingrid.meier@example.ch",
        "phone": "+41 44 555 66 77",
        "insurance_number": "ALK-012345",
    },
]


# ---------------------------------------------------------------------------
# Fake Companies (Employers)
# ---------------------------------------------------------------------------

FAKE_COMPANIES = [
    {
        "name": "Technoplus AG",
        "iban": "CH56 0483 5012 3456 7800 9",
        "uid": "CHE-123.456.789",
        "address": "Industriestrasse 45, 8001 Zürich",
        "phone": "+41 44 456 78 90",
        "contact_person": "Peter Schmitt",
    },
    {
        "name": "Kaufhaus Zentral GmbH",
        "iban": "CH57 0483 5012 3456 7800 0",
        "uid": "CHE-234.567.890",
        "address": "Bahnhofstrasse 12, 3011 Bern",
        "phone": "+41 31 987 65 43",
        "contact_person": "Anna Schneider",
    },
    {
        "name": "Logistik Services SA",
        "iban": "CH58 0483 5012 3456 7801 1",
        "uid": "CHE-345.678.901",
        "address": "Hafenstrasse 78, 1200 Genève",
        "phone": "+41 22 555 33 22",
        "contact_person": "Laurent Blanc",
    },
    {
        "name": "Tessin Handwerk GmbH",
        "iban": "CH59 0483 5012 3456 7801 2",
        "uid": "CHE-456.789.012",
        "address": "Via della Stazione 20, 6900 Lugano",
        "phone": "+41 91 222 44 55",
        "contact_person": "Marco Rossi",
    },
    {
        "name": "Bau + Entwicklung AG",
        "iban": "CH60 0483 5012 3456 7801 3",
        "uid": "CHE-567.890.123",
        "address": "Hauptstrasse 99, 8005 Zürich",
        "phone": "+41 44 789 01 23",
        "contact_person": "Thomas Keller",
    },
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def generate_iban() -> str:
    """Generate a fake but valid-format Swiss IBAN (CH prefix)."""
    # Format: CH + 2-digit check code + 5-digit bank code + account number
    check = random.randint(10, 99)
    bank = "".join(random.choices(string.digits, k=5))
    account = "".join(random.choices(string.digits, k=12))
    return f"CH{check} {bank} {account[:4]} {account[4:]}"


def generate_ahv_number() -> str:
    """
    Generate a fake but realistic AHV number.
    Format: 756.XXXX.XXXX.XX with proper check-digit algorithm.
    """
    # AHV: 756.NNNN.NNNN.NN where last 2 digits are check digits
    # Simplified: generate middle 8 digits, add check digits
    middle = "".join(random.choices(string.digits, k=8))
    # Calculate mod 97 check digit (simplified)
    number = int(f"756{middle}")
    check = 98 - (number % 97)
    check_str = f"{check:02d}"
    return f"756.{middle[:4]}.{middle[4:]}.{check_str}"


def generate_address(region: str = "DE") -> dict:
    """Generate a fake Swiss address."""
    location = random.choice([loc for loc in SWISS_LOCATIONS if loc["region"] == region])
    if region == "DE":
        street = random.choice(STREETS_DE)
    elif region == "FR":
        street = random.choice(STREETS_FR)
    elif region == "IT":
        street = random.choice(STREETS_IT)
    else:
        street = random.choice(STREETS_DE)

    number = random.randint(1, 150)
    return {
        "street": f"{street} {number}",
        "postal_code": location["plz"],
        "city": location["city"],
        "region": region,
        "full_address": f"{street} {number}, {location['plz']} {location['city']}",
    }


# ---------------------------------------------------------------------------
# Pre-generated Address Pool
# ---------------------------------------------------------------------------

FAKE_ADDRESSES = [
    {
        "street": "Bahnhofstrasse 12",
        "postal_code": "8001",
        "city": "Zürich",
        "region": "DE",
        "full_address": "Bahnhofstrasse 12, 8001 Zürich",
    },
    {
        "street": "Hauptstrasse 45",
        "postal_code": "8005",
        "city": "Zürich",
        "region": "DE",
        "full_address": "Hauptstrasse 45, 8005 Zürich",
    },
    {
        "street": "Schulstrasse 78",
        "postal_code": "3011",
        "city": "Bern",
        "region": "DE",
        "full_address": "Schulstrasse 78, 3011 Bern",
    },
    {
        "street": "Poststrasse 23",
        "postal_code": "3015",
        "city": "Bern",
        "region": "DE",
        "full_address": "Poststrasse 23, 3015 Bern",
    },
    {
        "street": "Rue de la Gare 10",
        "postal_code": "1200",
        "city": "Genève",
        "region": "FR",
        "full_address": "Rue de la Gare 10, 1200 Genève",
    },
    {
        "street": "Rue Principale 56",
        "postal_code": "1201",
        "city": "Genève",
        "region": "FR",
        "full_address": "Rue Principale 56, 1201 Genève",
    },
    {
        "street": "Rue de l'École 34",
        "postal_code": "2000",
        "city": "Neuchâtel",
        "region": "FR",
        "full_address": "Rue de l'École 34, 2000 Neuchâtel",
    },
    {
        "street": "Via della Stazione 20",
        "postal_code": "6900",
        "city": "Lugano",
        "region": "IT",
        "full_address": "Via della Stazione 20, 6900 Lugano",
    },
    {
        "street": "Via Principale 88",
        "postal_code": "6901",
        "city": "Lugano",
        "region": "IT",
        "full_address": "Via Principale 88, 6901 Lugano",
    },
    {
        "street": "Viale Centrale 15",
        "postal_code": "6950",
        "city": "Tesserete",
        "region": "IT",
        "full_address": "Viale Centrale 15, 6950 Tesserete",
    },
]


# ---------------------------------------------------------------------------
# Pre-generated IBAN Pool
# ---------------------------------------------------------------------------

FAKE_IBANS = [
    "CH93 0076 2011 6238 5295 7",
    "CH97 0076 2011 6238 5295 8",
    "CH94 0076 2011 6238 5295 9",
    "CH96 0076 2011 6238 5296 0",
    "CH95 0076 2011 6238 5296 1",
    "CH98 0076 2011 6238 5296 2",
    "CH92 0076 2011 6238 5296 3",
    "CH91 0076 2011 6238 5296 4",
    "CH90 0076 2011 6238 5296 5",
    "CH89 0076 2011 6238 5296 6",
]


# ---------------------------------------------------------------------------
# Pre-generated AHV Numbers
# ---------------------------------------------------------------------------

FAKE_AHV_NUMBERS = [
    "756.1234.5678.90",
    "756.2345.6789.01",
    "756.3456.7890.12",
    "756.4567.8901.23",
    "756.5678.9012.34",
    "756.6789.0123.45",
    "756.7890.1234.56",
    "756.8901.2345.67",
    "756.9012.3456.78",
    "756.0123.4567.89",
]


# ---------------------------------------------------------------------------
# Fake Doctors (with GLN numbers)
# ---------------------------------------------------------------------------

FAKE_DOCTORS = [
    {
        "first_name": "Peter",
        "last_name": "Schütz",
        "gln_number": "7601001123456",
        "email": "peter.schuetz@praxis-zuerich.ch",
        "phone": "+41 44 234 56 78",
        "address": "Medizinische Praxis, Bahnhofstrasse 50, 8001 Zürich",
    },
    {
        "first_name": "Ursula",
        "last_name": "Müller",
        "gln_number": "7601002234567",
        "email": "ursula.mueller@arzt-bern.ch",
        "phone": "+41 31 345 67 89",
        "address": "Hausarztpraxis, Hauptstrasse 75, 3011 Bern",
    },
    {
        "first_name": "Christoph",
        "last_name": "Keller",
        "gln_number": "7601003345678",
        "email": "c.keller@medecine-geneve.ch",
        "phone": "+41 22 456 78 90",
        "address": "Cabinet Médical, Rue du Rhône 20, 1200 Genève",
    },
    {
        "first_name": "Laura",
        "last_name": "Rossi",
        "gln_number": "7601004456789",
        "email": "laura.rossi@studio-medico-lugano.ch",
        "phone": "+41 91 567 89 01",
        "address": "Studio Medico, Via Nassa 15, 6900 Lugano",
    },
    {
        "first_name": "Thomas",
        "last_name": "Zimmermann",
        "gln_number": "7601005567890",
        "email": "t.zimmermann@arztpraxis-chur.ch",
        "phone": "+41 81 678 90 12",
        "address": "Arztpraxis, Alexanderstrasse 45, 7000 Chur",
    },
]


# ---------------------------------------------------------------------------
# Fake RAV Counselors
# ---------------------------------------------------------------------------

FAKE_RAV_COUNSELORS = [
    {
        "first_name": "Silvia",
        "last_name": "Weber",
        "rav_office": "RAV Zürich Stadt",
        "email": "s.weber@rav-zuerich.ch",
        "phone": "+41 44 123 45 00",
        "address": "Arbeitsamt, Bahnhofplatz 10, 8001 Zürich",
    },
    {
        "first_name": "Marcel",
        "last_name": "Schmid",
        "rav_office": "RAV Bern",
        "email": "m.schmid@rav-bern.ch",
        "phone": "+41 31 234 56 00",
        "address": "Arbeitsamt Bern, Kornhausplatz 5, 3011 Bern",
    },
    {
        "first_name": "Nathalie",
        "last_name": "Blanc",
        "rav_office": "RAV Genève",
        "email": "n.blanc@rav-geneve.ch",
        "phone": "+41 22 345 67 00",
        "address": "Office Chômage, Rue des Grenadiers 8, 1200 Genève",
    },
]


# ---------------------------------------------------------------------------
# Fake UID Numbers (CH business identification)
# ---------------------------------------------------------------------------

FAKE_UID_NUMBERS = [
    "CHE-123.456.789",
    "CHE-234.567.890",
    "CHE-345.678.901",
    "CHE-456.789.012",
    "CHE-567.890.123",
]


# ---------------------------------------------------------------------------
# Fake GLN Numbers (Healthcare provider IDs)
# ---------------------------------------------------------------------------

FAKE_GLN_NUMBERS = [
    "7601001123456",
    "7601002234567",
    "7601003345678",
    "7601004456789",
    "7601005567890",
]


# ---------------------------------------------------------------------------
# Fake Job Applications
# ---------------------------------------------------------------------------

FAKE_JOB_APPLICATIONS = [
    {
        "company": "Technoplus AG",
        "contact_person": "Peter Schmitt",
        "contact_email": "jobs@technoplus.ch",
        "date": "15.01.2025",
        "method": "online",
        "result": "Ablehnung",
    },
    {
        "company": "Kaufhaus Zentral GmbH",
        "contact_person": "Anna Schneider",
        "contact_email": "personal@kaufhaus-zentral.ch",
        "date": "18.01.2025",
        "method": "schriftlich",
        "result": "Keine Antwort",
    },
    {
        "company": "Logistik Services SA",
        "contact_person": "Laurent Blanc",
        "contact_email": "recrutement@logistik-services.ch",
        "date": "20.01.2025",
        "method": "persönlich",
        "result": "Bewerbungsgespräch geplant",
    },
    {
        "company": "Tessin Handwerk GmbH",
        "contact_person": "Marco Rossi",
        "contact_email": "jobs@tessin-hw.ch",
        "date": "22.01.2025",
        "method": "online",
        "result": "Ablehnung",
    },
    {
        "company": "Bau + Entwicklung AG",
        "contact_person": "Thomas Keller",
        "contact_email": "personal@bau-entwicklung.ch",
        "date": "25.01.2025",
        "method": "schriftlich",
        "result": "Zu Interviews eingeladen",
    },
    {
        "company": "Dienstleistungen Gemeinschaft",
        "contact_person": "Beatrice Mueller",
        "contact_email": "hr@dlg-services.ch",
        "date": "28.01.2025",
        "method": "online",
        "result": "Ablehnung",
    },
    {
        "company": "IT-Solutions Europa GmbH",
        "contact_person": "Stefan Braun",
        "contact_email": "jobs@it-solutions.ch",
        "date": "02.02.2025",
        "method": "persönlich",
        "result": "Gesprächstermin vereinbart",
    },
    {
        "company": "Finanz-Consulting AG",
        "contact_person": "Dr. Rudolf Eisele",
        "contact_email": "recruitment@finanz-consulting.ch",
        "date": "05.02.2025",
        "method": "online",
        "result": "Ablehnung",
    },
]


# ---------------------------------------------------------------------------
# ICD-10 Disease Codes (for medical certificates - not PII)
# ---------------------------------------------------------------------------

FAKE_ICD10_CODES = [
    "J06.9",  # Acute upper respiratory infection, unspecified
    "M79.3",  # Panniculitis, unspecified
    "G89.29", # Other chronic pain
    "F41.1",  # Generalized anxiety disorder
    "I10",    # Essential hypertension
]
