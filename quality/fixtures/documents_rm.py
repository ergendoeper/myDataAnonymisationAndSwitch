"""
Rumantsch Grischun SECO/ALK Document Fixtures

3 essential Rumantsch Grischun (standardized RM-CH) documents for ALK unemployment insurance.
Context: Grisons region (Graubünden) - Switzerland's largest canton by area, multilingual.
"""

from __future__ import annotations

# Rumantsch Grischun language documents with PII fields

DOCS_RM = [
    {
        "id": "alk_annunzia_rm_001",
        "title": "Annunzia tar la schanza",
        "language": "rm",
        "classification": "CONFIDENTIAL",
        "text": """ANNUNZIA TAR LA SCHANZA

Chantun: Grischun
Data da l'annunzia: 01.02.2025
Uffizi regiunal: Chur

DATAS PERSUNALAS:
Nom: Müller
Prenom: Hans-Peter
Data da naschientscha: 15.03.1972
Numer AVS: 756.1234.5678.90
Naziunalitad: Svizzra
Sez: Mascul
Stat civil: marità

ADRESCHA:
Via: Bahnhofstrasse 12
Numer postal: 8001
Vschinchla: Zürich
Telefon privat: +41 44 123 45 67
E-mail: hans.mueller@example.ch

DATAS BANCARAS (per il virament da las indemnisaziuns):
IBAN: CH93 0076 2011 6238 5295 7
Titular dal conto: Hans-Peter Müller
Banca: UBS AG

NUMER DA SIGIRANZA TAR LA SCHANZA: ALK-123456

Jau m'annunzia cun questa per la schanza a partir dal 01.02.2025 e
tumond indemnisaziuns da la schanza. Jau confirmi che las infurmaziuns
da sura sun correctas e completas.""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_quint_rm_001",
        "title": "Quint da indemnisaziun",
        "language": "rm",
        "classification": "CONFIDENTIAL",
        "text": """QUINT DA INDEMNISAZIUN TAR LA SCHANZA
Sigiranza da la schanza ALK

Numer d'assegurada: ALK-234567
Nom: Keller
Prenom: Maria
Numer AVS: 756.2345.6789.01

Perioda da calculaziun: 01.01.2025 - 31.01.2025
Dumber da dis senza lavur: 22
Indemnisaziun per di: CHF 195.--

DETAGLS DA LA CALCULAZIUN:
- Indemnisaziun lorda: CHF 4.290,--
- Deducziun per sigiranzas socialas: CHF 429,--
- Virament nett: CHF 3.861,--

Virament sin:
IBAN: CH97 0076 2011 6238 5295 8
Adrescha: Rue Principale 56, 1201 Genève

Persuna da contact per dumondas:
Rita Schneider
Telefon: +41 31 987 65 43
E-mail: maria.keller@example.ch

Data da virament: 05.02.2025
Numer da referenza: QI-2025-001-ALE""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_attest_rm_001",
        "title": "Attest dal emprendider",
        "language": "rm",
        "classification": "CONFIDENTIAL",
        "text": """ATTEST DAL EMPRENDIDER

Cun questa attestesch jau che:

LAVURANTA:
Nom: Schmid
Prenom: Rita
Data da naschientscha: 22.07.1985
Numer AVS: 756.4567.8901.23
Adrescha: Schulstrasse 78, 3011 Bern

EMPRENDIDER:
Numen: Technoplus AG
Numer UID: CHE-123.456.789
Adrescha: Industriestrasse 45, 8001 Zürich
Persuna da contact: Peter Schmitt
Telefon: +41 44 456 78 90
E-mail: peter.schmitt@technoplus.ch

Perioda da lavur:
Cumenzament: 01.03.2020
Fin (rescissiun): 31.01.2025

Motivaziun da la fin: Reorganisaziun dal'interpresa

ULTIMS SALAS:
Sala mensila (ultims 3 mais): CHF 5.800,--
Referenza da la listella da salaidas: 2024-Schmid-Rita

Coordinadas bancaras per restitucziuns (sch'esser necessari):
IBAN: CH96 0076 2011 6238 5296 0

Emessa da: 02.02.2025
Valida a partir da: 01.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
]
