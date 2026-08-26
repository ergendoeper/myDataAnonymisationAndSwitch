"""
German SECO/ALK Document Fixtures

5 realistic German-language documents with embedded PII for anonymization testing.
Context: ALK (Arbeitslosenkasse) unemployment insurance and SECO processes.
"""

from __future__ import annotations

# German language documents with PII fields

DOCS_DE = [
    {
        "id": "alk_anmeldung_001",
        "title": "Anmeldung zur Arbeitslosigkeit",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ANMELDUNG ZUR ARBEITSLOSIGKEIT

Kanton: Zürich
Anmeldedatum: 01.02.2025
Arbeitsamtsstelle: Zürich Stadt

PERSONALIEN:
Name: Müller
Vorname: Hans-Peter
Geburtsdatum: 15.03.1972
AHV-Nummer: 756.1234.5678.90
Nationalität: Schweiz
Geschlecht: Männlich
Zivilstand: verheiratet

ADRESSE:
Strasse: Bahnhofstrasse 12
Postleitzahl: 8001
Ort: Zürich
Telefon Privat: +41 44 123 45 67
E-Mail: hans.mueller@example.ch

BANKVERBINDUNG (für Taggeldauszahlung):
IBAN: CH93 0076 2011 6238 5295 7
Kontoinhaber: Hans-Peter Müller
Bank: UBS AG

VERSICHERUNGSNUMMER ALK: ALK-123456

Ich melde mich hiermit ab 01.02.2025 zur Arbeitslosigkeit an und beantrage
Arbeitslosenentschädigung. Ich bestätige, dass die vorstehenden Angaben korrekt sind.""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_taggeld_001",
        "title": "Taggeld-Abrechnung",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """TAGGELD-ABRECHNUNG
Arbeitslosenversicherung ALK

Versichertennummer: ALK-234567
Name: Keller
Vorname: Maria
AHV-Nummer: 756.2345.6789.01

Abrechnungsperiode: 01.01.2025 - 31.01.2025
Anzahl Arbeitstage ohne Beschäftigung: 22
Tageggeld pro Tag: CHF 195.--

ABRECHNUNGSDETAILS:
- Brutto-Taggeld: CHF 4.290,--
- Sozialversicherungsabzüge: CHF 429,--
- Netto-Auszahlung: CHF 3.861,--

Auszahlung erfolgt auf:
IBAN: CH97 0076 2011 6238 5295 8
Adresse: Rue Principale 56, 1201 Genève

Kontaktperson bei Fragen:
Rita Schneider
Telefon: +41 31 987 65 43
E-Mail: maria.keller@example.ch

Auszahlungsdatum: 05.02.2025
Referenznummer: TG-2025-001-ALE""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_arbeitgeberbescheid_001",
        "title": "Arbeitgeberbescheinigung",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ARBEITGEBERBESCHEINIGUNG

Bescheinigt wird hiermit, dass:

ARBEITNEHMER:
Name: Schmid
Vorname: Rita
Geburtsdatum: 22.07.1985
AHV-Nummer: 756.4567.8901.23
Adresse: Schulstrasse 78, 3011 Bern

ARBEITGEBER:
Name: Technoplus AG
UID: CHE-123.456.789
Adresse: Industriestrasse 45, 8001 Zürich
Kontaktperson: Peter Schmitt
Telefon: +41 44 456 78 90
E-Mail: peter.schmitt@technoplus.ch

Anstellungsdauer:
Beginn: 01.03.2020
Ende (Kündigung): 31.01.2025

Grund der Beendigung: Betriebliche Reorganisation

LETZTE LÖHNE:
Monatliches Gehalt (letzte 3 Monate): CHF 5.800,--
Lohnausweis-Referenz: 2024-Schmid-Rita

Kontoverbindung für Rückforderungen (falls nötig):
IBAN: CH96 0076 2011 6238 5296 0

Ausgestellt am: 02.02.2025
Gültig ab: 01.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_kurzarbeitsantrag_001",
        "title": "Kurzarbeitsantrag (KAE)",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ANTRAG AUF KURZARBEITSENTSCHÄDIGUNG (KAE)

Eingereicht von:
Unternehmen: Kaufhaus Zentral GmbH
UID: CHE-234.567.890
Adresse: Bahnhofstrasse 12, 3011 Bern
Telefon: +41 31 987 65 43
Kontaktperson: Anna Schneider
E-Mail: anna@kaufhaus-zentral.ch

BETROFFENE ARBEITNEHMER:

1. Name: Moreau, Vorname: Jean-Claude
   AHV-Nummer: 756.3456.7890.12
   Adresse: Rue de la Gare 10, 1200 Genève
   Normalarbeitszeit: 40 Std/Woche
   Reduzierte Arbeitszeit: 20 Std/Woche (50%)
   Lohn: CHF 6.200,--

2. Name: Dupont, Vorname: Sophie
   AHV-Nummer: 756.8901.2345.67
   Adresse: Rue Principale 56, 1201 Genève
   Normalarbeitszeit: 40 Std/Woche
   Reduzierte Arbeitszeit: 30 Std/Woche (75%)
   Lohn: CHF 5.500,--

Grund der Kurzarbeit: COVID-19 Pandemie Folgen
Zeitraum: 01.02.2025 - 30.04.2025

Bankverbindung für KAE-Entschädigungen:
IBAN: CH57 0483 5012 3456 7800 0

Unterzeichnet: 03.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_einsprache_001",
        "title": "Einsprache gegen Einstellung der Leistungen",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """EINSPRACHE GEGEN EINSTELLUNG DER ARBEITSLOSENENTSCHÄDIGUNG

Einsprechend:
Name: Ferrari
Vorname: Andrea
Geburtsdatum: 10.11.1978
AHV-Nummer: 756.9012.3456.78
Versichertennummer ALK: ALK-901234
Adresse: Via della Stazione 20, 6900 Lugano
Telefon: +41 91 222 44 55
E-Mail: andrea.ferrari@example.ch

IBAN für Rückzahlungen: CH90 0076 2011 6238 5296 5

Eingereicht bei:
Arbeitsamt Tessin
Abteilung Einsprachen
E-Mail: einsprachen@arbeitsamt-ti.ch

GRUND DER EINSPRACHE:
Die Einstellung der Arbeitslosenentschädigung ab 15.01.2025 ist rechtswidrig,
da ich das Einkommen aus einer neuen Teilzeitbeschäftigung (15 Stunden/Woche bei
Tessin Handwerk GmbH) nicht ordnungsgemäss gemeldet hatte. Ich bestreite nicht
die Einstellung der Leistungen, bitte aber um rückwirkende Neuberechnung unter
Anrechnung dieses Einkommens.

Neuer Arbeitgeber: Tessin Handwerk GmbH
Kontakt: Marco Rossi, marco.rossi@tessin-hw.ch
Arbeitsvertrag seit: 20.01.2025

Eingereicht am: 10.02.2025
Einsprache-Referenznummer: EIN-2025-00478""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_stellenbemühungen_001",
        "title": "Nachweis der Stellenbemühungen",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """NACHWEIS DER STELLENBEMÜHUNGEN - MONAT FEBRUAR 2025

Versicherte Person:
Name: Müller
Vorname: Hans-Peter
AHV-Nummer: 756.1234.5678.90
Versichertennummer ALK: ALK-123456

Meldezeitraum: 01.02.2025 - 28.02.2025
Anzahl Bewerbungen: 8 (erforderlich: mind. 8)

BEWERBUNGSÜBERSICHT:

1. Firma: Technoplus AG, Kontakt: Peter Schmitt (peter.schmitt@technoplus.ch)
   Datum: 15.02.2025 | Art: Online-Bewerbung | Resultat: Ablehnung

2. Firma: Kaufhaus Zentral GmbH, Kontakt: Anna Schneider (anna@kaufhaus-zentral.ch)
   Datum: 18.02.2025 | Art: Schriftliche Bewerbung | Resultat: Keine Antwort

3. Firma: Logistik Services SA, Kontakt: Laurent Blanc (laurent@logistik-services.ch)
   Datum: 20.02.2025 | Art: Persönliche Bewerbung | Resultat: Bewerbungsgespräch

4. Firma: Tessin Handwerk GmbH, Kontakt: Marco Rossi (marco.rossi@tessin-hw.ch)
   Datum: 22.02.2025 | Art: Online-Bewerbung | Resultat: Ablehnung

5. Firma: Bau + Entwicklung AG, Kontakt: Thomas Keller (thomas.keller@bau-entwicklung.ch)
   Datum: 25.02.2025 | Art: Schriftliche Bewerbung | Resultat: Zu Interviews eingeladen

6. Firma: Dienstleistungen Gemeinschaft, Kontakt: Beatrice Mueller (hr@dlg-services.ch)
   Datum: 28.02.2025 | Art: Online-Bewerbung | Resultat: Ablehnung

7. Firma: IT-Solutions Europa GmbH, Kontakt: Stefan Braun (jobs@it-solutions.ch)
   Datum: 05.02.2025 | Art: Persönliche Bewerbung | Resultat: Gesprächstermin vereinbart

8. Firma: Finanz-Consulting AG, Kontakt: Dr. Rudolf Eisele (recruitment@finanz-consulting.ch)
   Datum: 10.02.2025 | Art: Online-Bewerbung | Resultat: Ablehnung

Versicherte bestätigt hiermit die Richtigkeit dieser Angaben.""",
        "pii_fields": ["name", "ahv_number", "email", "insurance_number", "contact_persons"],
    },
    {
        "id": "alk_arztzeugnis_001",
        "title": "Ärztliches Attest (Arbeitsunfähigkeitszeugnis)",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ÄRZTLICHES ATTEST FÜR ARBEITSUNFÄHIGKEIT

Patient:
Name: Keller
Vorname: Maria
Geburtsdatum: 05.06.1980
AHV-Nummer: 756.2345.6789.01

Hausarzt:
Name: Dr. Ursula Müller
GLN-Nummer: 7601002234567
Adresse: Hausarztpraxis, Hauptstrasse 75, 3011 Bern
Telefon: +41 31 345 67 89
E-Mail: ursula.mueller@arzt-bern.ch

DIAGNOSE (ICD-10):
Code: J06.9 (Akute Infektionen der Atemwege, nicht näher bezeichnet)
Befundung: Akute virale Infektionen mit Fieber, Husten, Halsweh

ZEITRAUM DER ARBEITSUNFÄHIGKEIT:
Beginn: 10.02.2025
Ende: 17.02.2025

Die o.g. Person ist in der angegebenen Zeit vollständig arbeitsunfähig.
Eine schrittweise Rückkehr zur Arbeit ist ab 18.02.2025 möglich.

Arzt Unterschrift:
Dr. U. Müller
Ausgestellt: 17.02.2025
Gültig für: ALK-Leistungen""",
        "pii_fields": ["name", "ahv_number", "doctor_name", "gln_number", "email", "phone"],
    },
    {
        "id": "alk_kuendigung_001",
        "title": "Kündigungsschreiben (Arbeitgeber)",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """KÜNDIGUNGSSCHREIBEN - ORDENTLICHE KÜNDIGUNG

Arbeitgeber:
Name: Tessin Handwerk GmbH
UID-Nummer: CHE-456.789.012
Adresse: Via della Stazione 20, 6900 Lugano
Vertreter: Marco Rossi (marco.rossi@tessin-hw.ch)

Arbeitnehmer:
Name: Schmid
Vorname: Rita
Adresse: Schulstrasse 78, 3011 Bern
AHV-Nummer: 756.4567.8901.23

---

Sehr geehrte Frau Schmid

Wir kündigen Ihr Anstellungsverhältnis ordentlich auf den 31.05.2025.

Grund der Kündigung: Betriebliche Reorganisation und Reduktion der Stellenbestände.

Ihre letzte Arbeitstag ist: 31.05.2025
Danach besteht keine Pflicht zur Arbeitsleistung mehr.

Ferienersatz und ausstehende Löhne werden mit der Schlussabrechnung verrechnet.

Kündigungsdatum: 15.02.2025
Unterschrift HR: Marco Rossi, Geschäftsführer

GEGENÜBER RECHTE:
Diese Kündigung gilt als wirksam und kann innerhalb von 5 Tagen beim Arbeitsamt
Bern angefochten werden.""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_selbstkundigung_001",
        "title": "Kündigungsschreiben (Arbeitnehmer Selbstkündigung)",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """KÜNDIGUNGSSCHREIBEN - SELBSTKÜNDIGUNG

Arbeitnehmer:
Name: Ferrari
Vorname: Andrea
Adresse: Via della Stazione 20, 6900 Lugano
AHV-Nummer: 756.9012.3456.78

Arbeitgeber:
Name: Kaufhaus Zentral GmbH
UID-Nummer: CHE-234.567.890
Adresse: Bahnhofstrasse 12, 3011 Bern
Vertreter: Anna Schneider (anna@kaufhaus-zentral.ch)

---

Sehr geehrte Damen und Herren

Hiermit kündige ich mein Anstellungsverhältnis ordentlich auf den 31.03.2025.

Grund der Selbstkündigung: Bessere berufliche Perspektiven und persönliche Entwicklung.

Mein letzter Arbeitstag ist: 31.03.2025

WICHTIG - SPERRFRIST ALK:
Diese Selbstkündigung führt automatisch zu einer Sperrfrist im Anspruch auf
Arbeitslosenentschädigung. Die ALK wird eine Sperrfrist von mindestens 1 Monat
verhängen.

Kündigungsdatum: 10.02.2025
Unterschrift: Andrea Ferrari

BESTÄTIGUNG ARBEITGEBER:
Empfangen: 10.02.2025
Unterschrift HR: Anna Schneider""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_zwischenverdienst_001",
        "title": "Abrechnung Zwischenverdienst",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ABRECHNUNG ZWISCHENVERDIENST

Versicherte Person:
Name: Dupont
Vorname: Sophie
AHV-Nummer: 756.8901.2345.67
Versichertennummer ALK: ALK-890123

Abrechnungsperiode: 01.02.2025 - 28.02.2025

ZWISCHENVERDIENST-ARBEITGEBER:
Firma: Logistik Services SA
Kontakt: Laurent Blanc (laurent@logistik-services.ch)
Tätigkeit: Teilzeitbeschäftigung (20 Stunden/Woche)

EINNAHMEN:
Bruttolohn Zwischenverdienst: CHF 2.180,--
Zwischenverdienst (nach Abzug 20%): CHF 1.744,--

BERECHNUNG ALK-LEISTUNG:
Normalleistung ALK (ohne Zwischenverdienst): CHF 3.861,--
Anrechnung Zwischenverdienst (80%): CHF 1.392,--
ALK-Differenzzahlung: CHF 2.469,--

GESAMTZAHLUNG:
Zwischenverdienst: CHF 1.744,--
ALK-Differenzzahlung: CHF 2.469,--
Gesamtnetto: CHF 4.213,--

AUSZAHLUNG ERFOLGT AUF:
IBAN für Differenzzahlung: CH91 0076 2011 6238 5296 4
Arbeitgeber veranlasst Direktzahlung Zwischenverdienst.

Kontoinhaber: Sophie Dupont
Auszahlungsdatum: 05.03.2025""",
        "pii_fields": ["name", "ahv_number", "iban", "email", "insurance_number"],
    },
    {
        "id": "alk_rav_protocol_001",
        "title": "RAV-Beratungsprotokoll",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """RAV-BERATUNGSPROTOKOLL (Regionale Arbeitsvermittlung)

RAV-Standort: RAV Zürich Stadt
Adresse: Arbeitsamt, Bahnhofplatz 10, 8001 Zürich
Datum Termin: 12.02.2025 Uhr 10:00

BERATER:
Name: Silvia Weber
E-Mail: s.weber@rav-zuerich.ch
Telefon: +41 44 123 45 00

BERATENE PERSON:
Name: Moreau
Vorname: Jean-Claude
AHV-Nummer: 756.3456.7890.12
Adresse: Rue de la Gare 10, 1200 Genève

PROTOKOLL DES BERATUNGSGESPRÄCHS:

1. AKTUELLER BERUFSSTATUS:
   - Arbeitsloser Status seit 01.02.2025
   - Letzte Beschäftigung: Technoplus AG (IT-Fachmann)
   - Gewünschte Tätigkeit: IT-Support, Projektmanagement

2. VEREINBARTE MASSNAHMEN:
   - Mindestens 8 Bewerbungen pro Monat (monatliche Kontrolle)
   - Teilnahme an "Bewerbungstechniken-Kurs" ab 24.02.2025 (RAV Zürich)
   - Spezialisierungskurs "Agile Project Management" (4 Wochen, externe Schule)
   - Aktivierung beruflicher Netzwerke (LinkedIn, Fachverbände)

3. NÄCHSTER TERMIN:
   Folgeberatung: 12.03.2025 um 10:00 Uhr

4. UNTERLAGEN:
   - Aktualisierter Lebenslauf erforderlich
   - Kurszertifikate bis nächsten Termin

Unterschrift Berater: Silvia Weber
Unterschrift Versicherte: Jean-Claude Moreau
Datum Protokoll: 12.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "counselor_name", "email", "phone"],
    },
    {
        "id": "alk_einstellung_001",
        "title": "Verfügung Einstellung im Anspruch (Sperrfrist)",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """VERFÜGUNG: EINSTELLUNG IM ANSPRUCH AUF ARBEITSLOSENENTSCHÄDIGUNG

Arbeitsamt Bern
Kornhausplatz 5, 3011 Bern

Verfügung Nr.: BEST-2025-00127
Ausgestellt am: 20.02.2025
Sachbearbeiter: Thomas Zimmer (t.zimmer@arbeitsamt-bern.ch)

BETROFFENE PERSON:
Name: Keller
Vorname: Maria
AHV-Nummer: 756.2345.6789.01
Versichertennummer ALK: ALK-234567
Adresse: Rue Principale 56, 1201 Genève

---

VERFÜGUNG:

Mit dieser Verfügung wird Ihre Anspruchsberechtigung auf Arbeitslosenentschädigung
ab 15.03.2025 für die Dauer von 30 Tagen ausgesetzt.

GRUND DER EINSTELLUNG (Selbstverschulden):
Sie haben am 10.02.2025 Ihre Beschäftigung bei Kaufhaus Zentral GmbH
freiwillig beendet (Selbstkündigung), ohne einen berechtigten Grund nach
ALV-Gesetz geltend zu machen.

SPERRFRIST-DETAILS:
- Beginn Sperrfrist: 15.03.2025
- Ende Sperrfrist: 14.04.2025
- Wiederaufnahme Leistungen: 15.04.2025

RECHTSMITTEL:
Gegen diese Verfügung können Sie innerhalb von 30 Tagen schriftlich Einsprache
erheben. Die Einsprache ist beim Arbeitsamt Bern einzureichen.

Adresse für Einsprache: Einsprachen@arbeitsamt-bern.ch

Unterschrift Sachbearbeiter: Thomas Zimmer
Stempel Arbeitsamt Bern""",
        "pii_fields": ["name", "ahv_number", "address", "email", "insurance_number", "sachbearbeiter"],
    },
    {
        "id": "alk_pendenzmeldung_001",
        "title": "Pendenzmeldung - Aufforderung fehlender Unterlagen",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """PENDENZMELDUNG - AUFFORDERUNG ZUR UNTERLAGENBESCHAFFUNG

Von: Arbeitsamt Zürich Stadt
Arbeitsamt, Bahnhofplatz 10, 8001 Zürich

An: Schmid, Rita
Schulstrasse 78, 3011 Bern
AHV-Nummer: 756.4567.8901.23
Versichertennummer ALK: ALK-456789

Datum: 18.02.2025
Referenznummer: PEND-2025-00089

BETREFF: AUFFORDERUNG ZUR UNTERLAGENBESCHAFFUNG

Sehr geehrte Frau Schmid

Bei der Überprüfung Ihrer Anspruchsberechtigung auf Arbeitslosenentschädigung
wurden folgende Unterlagen vermisst:

AUSSTEHENDE UNTERLAGEN:
1. Nachweis der Stellenbemühungen für Januar 2025 (mind. 8 Bewerbungen)
2. Ärztliches Attest für Abwesenheit 15.-20.02.2025
3. Aktualisierter Lebenslauf (bei letzter RAV-Beratung versprochen)

FRIST ZUM EINREICHEN:
Sie müssen die fehlenden Unterlagen spätestens bis 04.03.2025 (Poststempel)
beim Arbeitsamt Zürich einreichen.

KONSEQUENZEN BEI NICHTEINHALTEN:
Falls die Unterlagen nicht rechtzeitig eingereicht werden, besteht das Risiko:
- Reduktion oder Einstellung der Leistungen
- Rückzahlungsverpflichtung von zu Unrecht ausbezahlten Leistungen
- Strafen nach ALV-Gesetz

Einreichen an:
E-Mail: unterlagen@arbeitsamt-zuerich.ch
oder per Post an obenstehende Adresse

Bei Fragen: +41 44 123 45 00

Unterschrift Sachbearbeiterin: Silvia Weber
Arbeitsamt Zürich Stadt""",
        "pii_fields": ["name", "ahv_number", "address", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_insolvenzentschadigung_001",
        "title": "Antrag auf Insolvenzentschädigung",
        "language": "de",
        "classification": "CONFIDENTIAL",
        "text": """ANTRAG AUF INSOLVENZENTSCHÄDIGUNG (IEO)

Eingereicht von:
Name: Weber
Vorname: Klaus
Adresse: Hauptstrasse 45, 8005 Zürich
AHV-Nummer: 756.7890.1234.56
Versichertennummer ALK: ALK-789012
Telefon: +41 44 456 78 90

BETREIBUNGSAMT / KONKURSAMT:
Konkursbehörde: Konkursgericht Zürich
Adresse: Limmatquai 56, 8001 Zürich
Konkurs-/Betreibungsnummer: ZH-KONK-2025-07834

---

INSOLVENTER ARBEITGEBER:
Firma: IT-Solutions Europa GmbH
UID-Nummer: CHE-345.123.456
Konkursverwalter: lic.iur. Stefan Blumenstein
Telefon Konkursverwaltung: +41 44 987 65 43

BESCHÄFTIGUNGSVERHÄLTNIS:
Beschäftigungsbeginn: 01.06.2023
Beschäftigungsende: 31.01.2025 (Konkurs der Firma)
Position: Senior IT-Consultant
Bruttolohn: CHF 8.500,-- monatlich

OFFENE LOHNFORDERUNG:
Periode nicht bezahlter Löhne: 01.01.2025 - 31.01.2025 (1 Monat)
Bruttogesamtforderung: CHF 8.500,--
Abzüge (AHV/ALV): CHF 850,--
Nettoforderung: CHF 7.650,--

Beweismittel:
- Arbeitsvertrag beiliegend
- Lohnausweise 2024-2025 beiliegend
- Schreiben Konkursverwaltung bestätigend Lohnausfall

GEFORDERTE IEO-LEISTUNG:
Monatlicher Nettolohn gemäss Konkursgesuch: CHF 7.650,--

Eingereicht bei: Arbeitsamt Zürich, IEO-Abteilung
Datum Einreichung: 15.02.2025
Unterschrift: Klaus Weber""",
        "pii_fields": ["name", "ahv_number", "address", "phone", "uid_number", "betreibungsnummer", "insurance_number"],
    },
]
