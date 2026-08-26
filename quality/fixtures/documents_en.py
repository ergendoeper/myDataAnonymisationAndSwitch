"""
English SECO/ALK Document Fixtures

3 essential English-language documents for international ALK/SECO context.
Context: International contacts, SECO export risk guarantees, and cross-border employment.
"""

from __future__ import annotations

# English language documents with PII fields

DOCS_EN = [
    {
        "id": "alk_unemployment_registration_en_001",
        "title": "Application for Unemployment Benefits",
        "language": "en",
        "classification": "CONFIDENTIAL",
        "text": """APPLICATION FOR UNEMPLOYMENT BENEFITS

Canton: Zurich
Date of Application: 01.02.2025
Employment Office: Zurich City

PERSONAL INFORMATION:
Surname: Moreau
Given Name: Jean-Claude
Date of Birth: 12.05.1968
AVS Number: 756.3456.7890.12
Nationality: Switzerland
Gender: Male
Marital Status: Married

ADDRESS:
Street: Rue de la Gare 10
Postal Code: 1200
City: Genève
Home Phone: +41 22 555 33 22
Email: jean.moreau@example.ch

BANKING INFORMATION (for benefit payments):
IBAN: CH94 0076 2011 6238 5295 9
Account Holder: Jean-Claude Moreau
Bank: UBS AG

UNEMPLOYMENT INSURANCE NUMBER: ALK-345678

I hereby apply for unemployment benefits as of 01.02.2025. I declare that all
information provided above is accurate and complete.""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_short_time_work_en_001",
        "title": "Short-Time Work Compensation Request",
        "language": "en",
        "classification": "CONFIDENTIAL",
        "text": """REQUEST FOR SHORT-TIME WORK COMPENSATION (RHT)

Submitted by:
Company: Logistik Services SA
UID Number: CHE-345.678.901
Address: Hafenstrasse 78, 1200 Genève
Phone: +41 22 555 33 22
Contact Person: Laurent Blanc
Email: laurent.blanc@logistik-services.ch

AFFECTED EMPLOYEES:

1. Surname: Dupont, Given Name: Sophie
   AVS Number: 756.8901.2345.67
   Address: Rue Principale 56, 1201 Genève
   Normal Hours: 40 hours/week
   Reduced Hours: 30 hours/week (75%)
   Salary: CHF 5.500,--

2. Surname: Ferrari, Given Name: Andrea
   AVS Number: 756.9012.3456.78
   Address: Via della Stazione 20, 6900 Lugano
   Normal Hours: 40 hours/week
   Reduced Hours: 20 hours/week (50%)
   Salary: CHF 6.200,--

REASON FOR SHORT-TIME WORK: Global economic slowdown and reduced orders
PERIOD: 01.02.2025 - 30.04.2025

BANKING INFORMATION FOR COMPENSATION:
IBAN: CH95 0076 2011 6238 5296 1

Submitted: 03.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "seco_export_guarantee_en_001",
        "title": "Export Risk Guarantee (ERG) Application",
        "language": "en",
        "classification": "CONFIDENTIAL",
        "text": """EXPORT RISK GUARANTEE (ERG) APPLICATION
State Secretariat for Economic Affairs (SECO)

APPLICANT COMPANY:
Name: Bau + Entwicklung AG
UID Number: CHE-567.890.123
Address: Hauptstrasse 99, 8005 Zürich
Business Sector: Construction and Infrastructure Development

CONTACT PERSON:
Surname: Keller
Given Name: Thomas
Email: thomas.keller@bau-entwicklung.ch
Phone: +41 44 789 01 23
AVS Number: 756.7890.1234.56

EXPORT CONTRACT DETAILS:
Destination Country: Vietnam (Hanoi)
Buyer: Phuong Minh Construction Ltd.
Buyer Contact: +84 24 3825 5000
Contract Value: CHF 2,500,000
Payment Terms: L/C 90 days after shipment
Delivery Period: 2025-2026

GOODS/SERVICES:
Construction equipment, materials, and technical services for road infrastructure project

BANKING INFORMATION (for guarantee disbursements):
IBAN: CH60 0483 5012 3456 7801 3

RISK ASSESSMENT:
Requested guarantee covers commercial and political risks in the destination country.

Submitted: 10.02.2025
Application Reference: ERG-2025-CH-0847""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email", "phone", "iban"],
    },
]
