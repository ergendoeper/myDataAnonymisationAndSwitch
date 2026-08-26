"""
Italian SECO/ALK Document Fixtures

5 realistic Italian-language documents with embedded PII for anonymization testing.
Context: Assicurazione disoccupazione ALK (Ticino - Tessin region, southern Switzerland).
"""

from __future__ import annotations

# Italian language documents with PII fields

DOCS_IT = [
    {
        "id": "alk_modulo_it_001",
        "title": "Modulo d'iscrizione alla disoccupazione",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """MODULO D'ISCRIZIONE ALL'ASSICURAZIONE CONTRO LA DISOCCUPAZIONE

Cantone: Ticino
Data d'iscrizione: 01.02.2025
Ufficio regionale: Lugano Centro

DATI PERSONALI:
Cognome: Ferrari
Nome: Andrea
Data di nascita: 10.11.1978
Numero AVS: 756.9012.3456.78
Cittadinanza: Svizzera
Sesso: Maschile
Stato civile: coniugato

INDIRIZZO:
Via: Via della Stazione 20
Codice postale: 6900
Città: Lugano
Telefono privato: +41 91 222 44 55
Indirizzo e-mail: andrea.ferrari@example.ch

COORDINATE BANCARIE (per il versamento delle prestazioni):
IBAN: CH90 0076 2011 6238 5296 5
Intestatario conto: Andrea Ferrari
Banca: UBS AG

NUMERO DELL'ASSICURAZIONE DISOCCUPAZIONE: ALK-901234

Mi iscrivo per questo mezzo all'assicurazione disoccupazione a partire dal
01.02.2025 e richiedo le prestazioni di disoccupazione. Confermo che i dati
sopra indicati sono corretti e completi.""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_conteggio_it_001",
        "title": "Conteggio indennità giornaliera",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """CONTEGGIO INDENNITÀ GIORNALIERA
Assicurazione disoccupazione ALK

Numero assicurato: ALK-123456
Cognome: Müller
Nome: Hans-Peter
Numero AVS: 756.1234.5678.90

Periodo di calcolo: 01.01.2025 - 31.01.2025
Numero di giorni senza attività professionale: 22
Indennità giornaliera: CHF 185,--

DETTAGLI DEL CONTEGGIO:
- Indennità giornaliera lorda: CHF 4.070,--
- Trattenute per assicurazioni sociali: CHF 407,--
- Importo netto versato: CHF 3.663,--

Versamento effettuato su:
IBAN: CH93 0076 2011 6238 5295 7
Indirizzo: Bahnhofstrasse 12, 8001 Zürich

Persona di contatto per domande:
Giovanni Martinelli
Telefono: +41 91 333 55 66
E-mail: hans.mueller@example.ch

Data di versamento: 05.02.2025
Numero di riferimento: IG-2025-003-ALK""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_attestato_it_001",
        "title": "Attestato del datore di lavoro",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """ATTESTATO DEL DATORE DI LAVORO

Con la presente attesto che:

DIPENDENTE:
Cognome: Keller
Nome: Maria
Data di nascita: 05.06.1980
Numero AVS: 756.2345.6789.01
Indirizzo: Rue Principale 56, 1201 Genève

DATORE DI LAVORO:
Ragione sociale: Tessin Handwerk GmbH
Numero UID: CHE-456.789.012
Indirizzo: Via della Stazione 20, 6900 Lugano
Persona di contatto: Marco Rossi
Telefono: +41 91 222 44 55
E-mail: marco.rossi@tessin-hw.ch

Periodo di lavoro:
Inizio: 10.05.2018
Fine (licenziamento): 31.01.2025

Motivo della cessazione: Ridimensionamento dell'organico

ULTIMI SALARI:
Salario mensile (ultimi 3 mesi): CHF 5.500,--
Riferimento busta paga: 2024-Keller-Maria

Coordinate bancarie per eventuali rimborsi:
IBAN: CH97 0076 2011 6238 5295 8

Redatto il: 02.02.2025
Valido dal: 01.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_lavoro_ridotto_it_001",
        "title": "Domanda per il lavoro ridotto (LR)",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """DOMANDA PER L'INDENNITÀ DI LAVORO RIDOTTO

Presentata da:
Azienda: Bianchi Costruzioni SA
Numero UID: CHE-567.890.123
Indirizzo: Viale Centrale 15, 6950 Tesserete
Telefono: +41 91 444 55 66
Persona di contatto: Davide Colombi
E-mail: davide@bianchi-costruzioni.ch

DIPENDENTI COINVOLTI:

1. Cognome: Schmid, Nome: Rita
   Numero AVS: 756.4567.8901.23
   Indirizzo: Schulstrasse 78, 3011 Bern
   Orario normale: 40 ore/settimana
   Orario ridotto: 24 ore/settimana (60%)
   Salario: CHF 5.800,--

2. Cognome: Rossi, Nome: Giuseppe
   Numero AVS: 756.5678.9012.34
   Indirizzo: Via della Stazione 20, 6900 Lugano
   Orario normale: 40 ore/settimana
   Orario ridotto: 20 ore/settimana (50%)
   Salario: CHF 6.200,--

Motivo del lavoro ridotto: Situazione economica difficile e calo ordini
Periodo: 01.02.2025 - 30.06.2025

Coordinate bancarie per l'indennità di lavoro ridotto:
IBAN: CH60 0483 5012 3456 7801 3

Firmato: 03.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_opposizione_it_001",
        "title": "Opposizione alla sospensione dei benefici",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """OPPOSIZIONE ALLA SOSPENSIONE DELLE PRESTAZIONI DI DISOCCUPAZIONE

Ricorrente:
Cognome: Bianchi
Nome: Francesca
Data di nascita: 19.03.1979
Numero AVS: 756.6789.0123.45
Numero dell'assicurazione disoccupazione: ALK-678901
Indirizzo: Via della Stazione 20, 6900 Lugano
Telefono: +41 91 333 55 66
E-mail: francesca.bianchi@example.ch

IBAN per rimborsi: CH98 0076 2011 6238 5296 2

Presentata presso:
Ufficio cantonale della disoccupazione Ticino
Dipartimento Opposizioni
E-mail: opposizioni@ufficio-disoccupazione-ti.ch

MOTIVO DELL'OPPOSIZIONE:
La sospensione dell'indennità disoccupazione dal 15.01.2025 è illegittima in
quanto non sono stata adeguatamente informata dell'obbligo di segnalare il mio
nuovo impiego. Non contesto la sospensione in sé, ma chiedo un ricalcolo
retroattivo considerando il reddito della mia attività part-time.

Nuovo datore di lavoro: Logistik Services SA
Contatto: Laurent Blanc, laurent.blanc@logistik-services.ch
Contratto dal: 18.01.2025
Orario: 18 ore/settimana

Presentata il: 10.02.2025
Numero di riferimento: OPP-2025-00612""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_ricerche_lavoro_it_001",
        "title": "Giustificativo ricerche di lavoro",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """GIUSTIFICATIVO RICERCHE DI LAVORO - FEBBRAIO 2025

Assicurato:
Cognome: Schmid
Nome: Rita
Numero AVS: 756.4567.8901.23
Numero assicurazione disoccupazione: ALK-456789

Periodo di segnalazione: 01.02.2025 - 28.02.2025
Numero candidature: 8 (obbligatorio: minimo 8)

ELENCO CANDIDATURE:

1. Ditta: Technoplus AG, Contatto: Peter Schmitt (peter.schmitt@technoplus.ch)
   Data: 15.02.2025 | Mezzo: Candidatura online | Risultato: Rifiuto

2. Ditta: Kaufhaus Zentral GmbH, Contatto: Anna Schneider (anna@kaufhaus-zentral.ch)
   Data: 18.02.2025 | Mezzo: Candidatura scritta | Risultato: Nessuna risposta

3. Ditta: Logistik Services SA, Contatto: Laurent Blanc (laurent@logistik-services.ch)
   Data: 20.02.2025 | Mezzo: Candidatura personale | Risultato: Colloquio previsto

4. Ditta: Tessin Handwerk GmbH, Contatto: Marco Rossi (marco.rossi@tessin-hw.ch)
   Data: 22.02.2025 | Mezzo: Candidatura online | Risultato: Rifiuto

5. Ditta: Bau + Entwicklung AG, Contatto: Thomas Keller (thomas.keller@bau-entwicklung.ch)
   Data: 25.02.2025 | Mezzo: Candidatura scritta | Risultato: Convocato ai colloqui

6. Ditta: Dienstleistungen Gemeinschaft, Contatto: Beatrice Mueller (hr@dlg-services.ch)
   Data: 28.02.2025 | Mezzo: Candidatura online | Risultato: Rifiuto

7. Ditta: IT-Solutions Europa GmbH, Contatto: Stefan Braun (jobs@it-solutions.ch)
   Data: 05.02.2025 | Mezzo: Candidatura personale | Risultato: Appuntamento concordato

8. Ditta: Finanz-Consulting AG, Contatto: Dr. Rudolf Eisele (recruitment@finanz-consulting.ch)
   Data: 10.02.2025 | Mezzo: Candidatura online | Risultato: Rifiuto

L'assicurato conferma l'esattezza di questi dati.""",
        "pii_fields": ["name", "ahv_number", "email", "insurance_number", "contact_persons"],
    },
    {
        "id": "alk_certificato_medico_it_001",
        "title": "Certificato medico (Incapacità di lavoro)",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """CERTIFICATO MEDICO DI INCAPACITÀ AL LAVORO

Paziente:
Cognome: Ferrari
Nome: Andrea
Data di nascita: 10.11.1978
Numero AVS: 756.9012.3456.78

Medico curante:
Nome: Dr. Laura Rossi
Numero GLN: 7601004456789
Indirizzo: Studio Medico, Via Nassa 15, 6900 Lugano
Telefono: +41 91 567 89 01
E-mail: laura.rossi@studio-medico-lugano.ch

DIAGNOSI (Codice ICD-10):
Codice: M79.3 (Panniculite, non specificata)
Osservazioni: Infiammazione dei tessuti sottocutanei con limitazione mobilità

PERIODO INCAPACITÀ DI LAVORO:
Inizio: 10.02.2025
Fine: 17.02.2025

Il paziente è totalmente incapace di lavorare nel periodo indicato.
La ripresa graduale è possibile a partire dal 18.02.2025.

Firma medico:
Dr. L. Rossi
Rilasciato: 17.02.2025
Valido per: prestazioni assicurazione disoccupazione""",
        "pii_fields": ["name", "ahv_number", "doctor_name", "gln_number", "email", "phone"],
    },
    {
        "id": "alk_licenziamento_it_001",
        "title": "Lettera di licenziamento (Datore di lavoro)",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """LETTERA DI LICENZIAMENTO - LICENZIAMENTO ORDINARIO

Datore di lavoro:
Nome: Bau + Entwicklung AG
Numero UID: CHE-567.890.123
Indirizzo: Hauptstrasse 99, 8005 Zürich
Rappresentante: Thomas Keller (thomas.keller@bau-entwicklung.ch)

Dipendente:
Cognome: Rossi
Nome: Giuseppe
Indirizzo: Via della Stazione 20, 6900 Lugano
Numero AVS: 756.5678.9012.34

---

Spett.le Signor/a Rossi

Con la presente Le comunichiamo il licenziamento del Suo rapporto di lavoro
con scadenza al 31.05.2025.

Motivo del licenziamento: Riorganizzazione aziendale e riduzione organici.

Suo ultimo giorno di lavoro: 31.05.2025
Dopo tale data non avrà alcun obbligo di prestazione lavorativa.

I saldi delle ferie e gli stipendi in sospeso saranno regolati tramite
conteggio finale.

Data licenziamento: 15.02.2025
Firma Direzione: Thomas Keller, Direttore

DIRITTI DEL DIPENDENTE:
Questo licenziamento è valido e può essere contestato entro 5 giorni presso
l'ufficio cantonale della disoccupazione Zurigo.""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_dimissioni_it_001",
        "title": "Lettera di dimissioni (Dipendente Auto-Licenziamento)",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """LETTERA DI DIMISSIONI - AUTO-LICENZIAMENTO

Dipendente:
Cognome: Dupont
Nome: Sophie
Indirizzo: Rue Principale 56, 1201 Genève
Numero AVS: 756.8901.2345.67

Datore di lavoro:
Nome: Logistik Services SA
Numero UID: CHE-345.678.901
Indirizzo: Hafenstrasse 78, 1200 Genève
Rappresentante: Laurent Blanc (laurent.blanc@logistik-services.ch)

---

Spett.le Signora, Signor Blank

Con la presente rassegno le mie dimissioni dal rapporto di lavoro con
scadenza al 31.03.2025.

Motivo delle dimissioni: Migliori prospettive professionali e sviluppo personale.

Mio ultimo giorno di lavoro: 31.03.2025

ATTENZIONE - PERIODO DI CARENZA ASSICURAZIONE DISOCCUPAZIONE:
Queste dimissioni comportano automaticamente un periodo di carenza nei miei
diritti all'indennità di disoccupazione. L'assicurazione disoccupazione
applicherà un periodo di carenza di almeno 1 mese.

Data dimissioni: 10.02.2025
Firma: Sophie Dupont

RICEVUTA DATORE DI LAVORO:
Ricevuto: 10.02.2025
Firma Direzione: Laurent Blanc""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_guadagno_intermedio_it_001",
        "title": "Conteggio reddito intermedio",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """CONTEGGIO REDDITO INTERMEDIO

Assicurato:
Cognome: Meier
Nome: Ingrid
Numero AVS: 756.0123.4567.89
Numero assicurazione disoccupazione: ALK-012345

Periodo conteggio: 01.02.2025 - 28.02.2025

DATORE DI LAVORO - REDDITO INTERMEDIO:
Ditta: Kaufhaus Zentral GmbH
Contatto: Anna Schneider (anna@kaufhaus-zentral.ch)
Attività: Lavoro part-time (20 ore/settimana)

GUADAGNI:
Salario lordo reddito intermedio: CHF 2.050,--
Reddito intermedio (detrazione 20%): CHF 1.640,--

CALCOLO INDENNITÀ DISOCCUPAZIONE:
Prestazione normale disoccupazione (senza reddito intermedio): CHF 3.564,--
Imputazione reddito intermedio (80%): CHF 1.312,--
Differenza versata da disoccupazione: CHF 2.252,--

TOTALE VERSATO:
Reddito intermedio: CHF 1.640,--
Differenza disoccupazione: CHF 2.252,--
Totale netto: CHF 3.892,--

VERSAMENTO:
IBAN per differenza disoccupazione: CH89 0076 2011 6238 5296 6
Datore di lavoro effettua pagamento diretto reddito intermedio.

Intestatario conto: Ingrid Meier
Data versamento: 05.03.2025""",
        "pii_fields": ["name", "ahv_number", "iban", "email", "insurance_number"],
    },
    {
        "id": "alk_rav_verbale_it_001",
        "title": "Verbale consultazione RAV",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """VERBALE DI CONSULTAZIONE RAV (Collocamento Regionale)

Ufficio RAV: RAV Ticino
Indirizzo: Ufficio Disoccupazione, Via della Stazione 10, 6900 Lugano
Data consultazione: 12.02.2025 ore 10:00

CONSULENTE:
Nome: Marco Rossi
E-mail: m.rossi@rav-ticino.ch
Telefono: +41 91 222 44 55

PERSONA CONSULTATA:
Cognome: Bianchi
Nome: Francesca
Numero AVS: 756.6789.0123.45
Indirizzo: Via della Stazione 20, 6900 Lugano

VERBALE CONSULTAZIONE:

1. SITUAZIONE PROFESSIONALE ATTUALE:
   - Registrato disoccupato dal: 01.02.2025
   - Ultimo impiego: Tessin Handwerk GmbH (Artigianato)
   - Settori ricercati: Gestione progettuale, amministrazione

2. MISURE CONCORDATE:
   - Minimo 8 candidature al mese (verifica mensile)
   - Partecipazione corso "Tecniche di candidatura" da 24.02.2025 (RAV Lugano)
   - Formazione specialistica "Gestione di progetti" (4 settimane, scuola esterna)
   - Attivazione rete professionale (LinkedIn, associazioni settoriali)

3. PROSSIMO APPUNTAMENTO:
   Consultazione di follow-up: 12.03.2025 ore 10:00

4. DOCUMENTI RICHIESTI:
   - CV aggiornato
   - Certificati di formazione prima del prossimo appuntamento

Firma consulente: Marco Rossi
Firma assicurato: Francesca Bianchi
Data verbale: 12.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "counselor_name", "email", "phone"],
    },
    {
        "id": "alk_sospensione_it_001",
        "title": "Decisione sospensione dei diritti",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """DECISIONE: SOSPENSIONE DEI DIRITTI ALL'INDENNITÀ DI DISOCCUPAZIONE

Ufficio cantonale della disoccupazione Lugano
Via della Stazione 10, 6900 Lugano

Decisione No: SOSP-2025-00178
Emanata: 20.02.2025
Funzionario: Marco Rossi (m.rossi@ufficio-disoccupazione-ti.ch)

PERSONA INTERESSATA:
Cognome: Ferrari
Nome: Andrea
Numero AVS: 756.9012.3456.78
Numero assicurazione disoccupazione: ALK-901234
Indirizzo: Via della Stazione 20, 6900 Lugano

---

DECISIONE:

Con la presente il Suo diritto all'indennità di disoccupazione è sospeso a
partire dal 15.03.2025 per la durata di 30 giorni.

MOTIVO DELLA SOSPENSIONE (Responsabilità personale):
Ha rescisso volontariamente il Suo rapporto di lavoro presso Bau + Entwicklung AG
il 10.02.2025 (dimissioni) senza giustificare un motivo valido secondo la legge
sull'assicurazione disoccupazione.

DETTAGLI SOSPENSIONE:
- Inizio sospensione: 15.03.2025
- Fine sospensione: 14.04.2025
- Ripresa prestazioni: 15.04.2025

RICORSO:
Ha diritto di contestare questa decisione per iscritto entro 30 giorni.
Indirizzo ricorso: Ricorsi@ufficio-disoccupazione-ti.ch

Firma funzionario: Marco Rossi
Timbro Ufficio cantonale della disoccupazione""",
        "pii_fields": ["name", "ahv_number", "address", "email", "insurance_number", "funzionario"],
    },
    {
        "id": "alk_diffida_it_001",
        "title": "Diffida - Documenti mancanti",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """DIFFIDA - COMUNICAZIONE DOCUMENTI MANCANTI

Da: Ufficio cantonale della disoccupazione Ticino
Ufficio Disoccupazione, Via della Stazione 10, 6900 Lugano

A: Keller, Maria
Rue Principale 56, 1201 Genève
Numero AVS: 756.2345.6789.01
Numero assicurazione disoccupazione: ALK-234567

Data: 18.02.2025
Riferimento: MANCANZE-2025-00089

OGGETTO: COMUNICAZIONE DOCUMENTI MANCANTI

Spett.le Signora Keller

In seguito all'esame della Sua ammissibilità all'indennità di disoccupazione,
abbiamo constatato che i seguenti documenti sono mancanti:

DOCUMENTI DA FORNIRE:
1. Giustificativo ricerche di lavoro per gennaio 2025 (minimo 8 candidature)
2. Certificato medico per assenza 15.-20.02.2025
3. CV aggiornato (promesso durante precedente consultazione RAV)

TERMINE DA RISPETTARE:
Deve trasmettere i documenti mancanti entro il 04.03.2025 (timbro postale).

CONSEGUENZE IN CASO DI MANCATO RISPETTO:
Se non fornisce questi documenti entro il termine assegnato:
- Riduzione o sospensione delle Sue prestazioni
- Obbligo di restituzione delle indennità versate indebita
- Sanzioni secondo la legge sull'assicurazione disoccupazione

TRASMISSIONE:
E-mail: documenti@ufficio-disoccupazione-ti.ch
oppure per posta all'indirizzo sopra indicato

Per domande: +41 91 567 89 01

Firma funzionario: Marco Rossi
Ufficio cantonale della disoccupazione Ticino""",
        "pii_fields": ["name", "ahv_number", "address", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_insolvibilita_it_001",
        "title": "Domanda indennità in caso di insolvibilità",
        "language": "it",
        "classification": "CONFIDENTIAL",
        "text": """DOMANDA DI INDENNITÀ IN CASO DI INSOLVIBILITÀ (IEO)

Presentata da:
Cognome: Weber
Nome: Klaus
Indirizzo: Hauptstrasse 45, 8005 Zürich
Numero AVS: 756.7890.1234.56
Numero assicurazione disoccupazione: ALK-789012
Telefono: +41 44 456 78 90

UFFICIO FALLIMENTARE:
Autorità fallimentare: Tribunale Fallimentare Zurigo
Indirizzo: Limmatquai 56, 8001 Zürich
Numero fallimento: ZH-FALL-2025-07834

---

DATORE DI LAVORO INSOLVIBILE:
Ditta: IT-Solutions Europa GmbH
Numero UID: CHE-345.123.456
Curatore fallimento: Avv. Stefan Blumenstein
Telefono amministrazione: +41 44 987 65 43

RAPPORTO DI LAVORO:
Data inizio: 01.06.2023
Data fine: 31.01.2025 (fallimento ditta)
Funzione: Senior IT-Consultant
Stipendio lordo: CHF 8.500,-- mensile

STIPENDI IMPAGATI:
Periodo non retribuito: 01.01.2025 - 31.01.2025 (1 mese)
Totale lordo rivendicato: CHF 8.500,--
Detrazione AHV/ALV: CHF 850,--
Importo netto rivendicato: CHF 7.650,--

DOCUMENTI GIUSTIFICATIVI:
- Contratto di lavoro allegato
- Buste paga 2024-2025 allegate
- Attestazione curatore confermante mancato pagamento

INDENNITÀ IEO RICHIESTA:
Stipendio mensile netto secondo domanda fallimento: CHF 7.650,--

Depositata presso: Ufficio cantonale della disoccupazione Zurigo, Servizio IEO
Data deposito: 15.02.2025
Firma: Klaus Weber""",
        "pii_fields": ["name", "ahv_number", "address", "phone", "uid_number", "numero_fallimento", "insurance_number"],
    },
]
