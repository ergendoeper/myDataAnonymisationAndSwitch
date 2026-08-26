"""
French SECO/ALK Document Fixtures

5 realistic French-language documents with embedded PII for anonymization testing.
Context: Chômage (ALK) unemployment insurance and SECO processes (Romandie region).
"""

from __future__ import annotations

# French language documents with PII fields

DOCS_FR = [
    {
        "id": "alk_formulaire_fr_001",
        "title": "Formulaire d'inscription au chômage",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """FORMULAIRE D'INSCRIPTION AU CHÔMAGE

Canton: Genève
Date d'inscription: 01.02.2025
Office du chômage: Genève Ville

DONNÉES PERSONNELLES:
Nom: Moreau
Prénom: Jean-Claude
Date de naissance: 12.05.1968
Numéro AVS: 756.3456.7890.12
Nationalité: Suisse
Sexe: Masculin
État civil: marié

ADRESSE POSTALE:
Rue: Rue de la Gare 10
Code postal: 1200
Localité: Genève
Téléphone domicile: +41 22 555 33 22
Adresse e-mail: jean.moreau@example.ch

COORDONNÉES BANCAIRES (pour le versement des allocations):
IBAN: CH94 0076 2011 6238 5295 9
Titulaire du compte: Jean-Claude Moreau
Banque: Crédit Suisse

NUMÉRO D'ASSURANCE-CHÔMAGE: ALK-345678

Je m'inscris par la présente au chômage à partir du 01.02.2025 et demande
les prestations d'assurance-chômage. Je confirme que les informations ci-dessus
sont correctes et complètes.""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_decompte_fr_001",
        "title": "Décompte indemnité journalière",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """DÉCOMPTE INDEMNITÉ JOURNALIÈRE
Assurance-chômage ALK

Numéro d'assuré: ALK-567890
Nom: Rossi
Prénom: Giuseppe
Numéro AVS: 756.5678.9012.34

Période de calcul: 01.01.2025 - 31.01.2025
Nombre de jours sans activité professionnelle: 22
Indemnité journalière: CHF 180,--

DÉTAILS DU DÉCOMPTE:
- Indemnité journalière brute: CHF 3.960,--
- Retenues aux assurances sociales: CHF 396,--
- Montant net versé: CHF 3.564,--

Versement effectué sur:
IBAN: CH95 0076 2011 6238 5296 1
Adresse: Via della Stazione 20, 6900 Lugano

Personne de contact en cas de questions:
Monica Ferrari
Téléphone: +41 91 222 44 55
E-mail: giuseppe.rossi@example.ch

Date de versement: 05.02.2025
Numéro de référence: DJ-2025-002-CHO""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_attestation_fr_001",
        "title": "Attestation de l'employeur",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """ATTESTATION DE L'EMPLOYEUR

Par la présente, j'atteste que:

EMPLOYÉ:
Nom: Dupont
Prénom: Sophie
Date de naissance: 08.09.1982
Numéro AVS: 756.8901.2345.67
Adresse: Rue Principale 56, 1201 Genève

EMPLOYEUR:
Raison sociale: Logistik Services SA
Numéro UID: CHE-345.678.901
Adresse: Hafenstrasse 78, 1200 Genève
Personne de contact: Laurent Blanc
Téléphone: +41 22 555 33 22
E-mail: laurent.blanc@logistik-services.ch

Période d'emploi:
Début: 15.06.2019
Fin (licenciement): 31.01.2025

Motif de fin de relation: Restructuration organisationnelle

DERNIERS SALAIRES:
Salaire mensuel (3 derniers mois): CHF 6.200,--
Référence bulletin de salaire: 2024-Dupont-Sophie

Données bancaires pour remboursements éventuels:
IBAN: CH91 0076 2011 6238 5296 4

Établi le: 02.02.2025
Valide à partir de: 01.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_rht_fr_001",
        "title": "Demande de Réduction de l'horaire de travail (RHT)",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """DEMANDE D'INDEMNITÉ POUR RÉDUCTION DE L'HORAIRE DE TRAVAIL

Introduite par:
Entreprise: Bau + Entwicklung AG
Numéro UID: CHE-567.890.123
Adresse: Hauptstrasse 99, 8005 Zürich
Téléphone: +41 44 789 01 23
Personne de contact: Thomas Keller
E-mail: thomas.keller@bau-entwicklung.ch

EMPLOYÉS CONCERNÉS:

1. Nom: Bianchi, Prénom: Francesca
   Numéro AVS: 756.6789.0123.45
   Adresse: Via della Stazione 20, 6900 Lugano
   Horaire normal: 40 heures/semaine
   Horaire réduit: 25 heures/semaine (62,5%)
   Salaire: CHF 5.800,--

2. Nom: Weber, Prénom: Klaus
   Numéro AVS: 756.7890.1234.56
   Adresse: Hauptstrasse 45, 8005 Zürich
   Horaire normal: 40 heures/semaine
   Horaire réduit: 20 heures/semaine (50%)
   Salaire: CHF 6.100,--

Motif de la RHT: Crise économique et baisse des commandes
Période: 01.02.2025 - 31.05.2025

Coordonnées bancaires pour les indemnités RHT:
IBAN: CH60 0483 5012 3456 7801 3

Signé: 03.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone"],
    },
    {
        "id": "alk_opposition_fr_001",
        "title": "Opposition à la suspension des prestations",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """OPPOSITION À LA SUSPENSION DES PRESTATIONS D'ASSURANCE-CHÔMAGE

Opposant:
Nom: Meier
Prénom: Ingrid
Date de naissance: 25.12.1975
Numéro AVS: 756.0123.4567.89
Numéro d'assurance-chômage: ALK-012345
Adresse: Bahnhofstrasse 12, 8001 Zürich
Téléphone: +41 44 555 66 77
E-mail: ingrid.meier@example.ch

IBAN pour remboursements: CH89 0076 2011 6238 5296 6

Présentée auprès de:
Office cantonal du chômage Zurich
Département Oppositions
E-mail: oppositions@oacc-zi.ch

MOTIF DE L'OPPOSITION:
La suspension de l'allocation chômage du 20.01.2025 est illégale car je n'ai pas
été dûment informée de l'obligation de signaler mon nouvel emploi. Je conteste
pas la suspension elle-même, mais demande un recalcul rétroactif en tenant compte
du revenu de mon activité partielle.

Nouvel employeur: Kaufhaus Zentral GmbH
Contact: Anna Schneider, anna@kaufhaus-zentral.ch
Contrat depuis: 15.01.2025
Horaire: 20 heures/semaine

Présentée le: 10.02.2025
Numéro de référence: OPP-2025-00502""",
        "pii_fields": ["name", "ahv_number", "address", "iban", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_recherches_emploi_fr_001",
        "title": "Justificatif des recherches d'emploi",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """JUSTIFICATIF DES RECHERCHES D'EMPLOI - FÉVRIER 2025

Assuré(e):
Nom: Rossi
Prénom: Giuseppe
Numéro AVS: 756.5678.9012.34
Numéro d'assurance-chômage: ALK-567890

Période de déclaration: 01.02.2025 - 28.02.2025
Nombre de candidatures: 8 (obligatoire: min. 8)

LISTE DES CANDIDATURES:

1. Entreprise: Technoplus AG, Contact: Peter Schmitt (peter.schmitt@technoplus.ch)
   Date: 15.02.2025 | Moyen: Candidature en ligne | Résultat: Rejet

2. Entreprise: Kaufhaus Zentral GmbH, Contact: Anna Schneider (anna@kaufhaus-zentral.ch)
   Date: 18.02.2025 | Moyen: Candidature écrite | Résultat: Sans réponse

3. Entreprise: Logistik Services SA, Contact: Laurent Blanc (laurent@logistik-services.ch)
   Date: 20.02.2025 | Moyen: Candidature personnelle | Résultat: Entretien convenu

4. Entreprise: Tessin Handwerk GmbH, Contact: Marco Rossi (marco.rossi@tessin-hw.ch)
   Date: 22.02.2025 | Moyen: Candidature en ligne | Résultat: Rejet

5. Entreprise: Bau + Entwicklung AG, Contact: Thomas Keller (thomas.keller@bau-entwicklung.ch)
   Date: 25.02.2025 | Moyen: Candidature écrite | Résultat: Convoqué(e) aux entretiens

6. Entreprise: Dienstleistungen Gemeinschaft, Contact: Beatrice Mueller (hr@dlg-services.ch)
   Date: 28.02.2025 | Moyen: Candidature en ligne | Résultat: Rejet

7. Entreprise: IT-Solutions Europa GmbH, Contact: Stefan Braun (jobs@it-solutions.ch)
   Date: 05.02.2025 | Moyen: Candidature personnelle | Résultat: Rendez-vous convenu

8. Entreprise: Finanz-Consulting AG, Contact: Dr. Rudolf Eisele (recruitment@finanz-consulting.ch)
   Date: 10.02.2025 | Moyen: Candidature en ligne | Résultat: Rejet

L'assuré(e) confirme par la présente l'exactitude de ces données.""",
        "pii_fields": ["name", "ahv_number", "email", "insurance_number", "contact_persons"],
    },
    {
        "id": "alk_certificat_medical_fr_001",
        "title": "Certificat médical (Incapacité de travail)",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """CERTIFICAT MÉDICAL D'INCAPACITÉ DE TRAVAIL

Patient:
Nom: Bianchi
Prénom: Francesca
Date de naissance: 19.03.1979
Numéro AVS: 756.6789.0123.45

Médecin traitant:
Nom: Dr. Christoph Keller
Numéro GLN: 7601003345678
Adresse: Cabinet Médical, Rue du Rhône 20, 1200 Genève
Téléphone: +41 22 456 78 90
E-mail: c.keller@medecine-geneve.ch

DIAGNOSTIC (Code ICD-10):
Code: F41.1 (Trouble anxieux généralisé)
Observations: État d'anxiété avec symptômes somatiques importants

PÉRIODE D'INCAPACITÉ DE TRAVAIL:
Début: 12.02.2025
Fin: 26.02.2025

L'assuré(e) est totalement incapable de travailler pendant la période indiquée.
La reprise progressive du travail est envisageable à partir du 27.02.2025.

Signature médecin:
Dr. C. Keller
Délivré: 26.02.2025
Valide pour: prestations assurance-chômage""",
        "pii_fields": ["name", "ahv_number", "doctor_name", "gln_number", "email", "phone"],
    },
    {
        "id": "alk_resiliation_fr_001",
        "title": "Lettre de résiliation (Employeur)",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """LETTRE DE RÉSILIATION - CONGÉ ORDINAIRE

Employeur:
Nom: Bau + Entwicklung AG
Numéro UID: CHE-567.890.123
Adresse: Hauptstrasse 99, 8005 Zürich
Représentant: Thomas Keller (thomas.keller@bau-entwicklung.ch)

Employé:
Nom: Weber
Prénom: Klaus
Adresse: Hauptstrasse 45, 8005 Zürich
Numéro AVS: 756.7890.1234.56

---

Chère Madame, Cher Monsieur Weber

Nous vous donnons par la présente congé de votre relation de travail avec effet
au 31.05.2025.

Motif du congé: Restructuration organisationnelle et réduction d'effectifs.

Votre dernier jour de travail: 31.05.2025
À partir de cette date, vous n'êtes plus tenu(e) de fournir du travail.

Les soldes de vacances et les salaires en attente seront régularisés par un
décompte final.

Date du congé: 15.02.2025
Signature Direction: Thomas Keller, Gérant

DROITS DE L'EMPLOYÉ:
Ce congé est valable et peut être contesté dans les 5 jours auprès de l'office
cantonal du chômage Zurich.""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_auto_resiliation_fr_001",
        "title": "Lettre de résiliation (Employé Auto-Congé)",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """LETTRE DE RÉSILIATION - AUTO-CONGÉ

Employé:
Nom: Dupont
Prénom: Sophie
Adresse: Rue Principale 56, 1201 Genève
Numéro AVS: 756.8901.2345.67

Employeur:
Nom: Logistik Services SA
Numéro UID: CHE-345.678.901
Adresse: Hafenstrasse 78, 1200 Genève
Représentant: Laurent Blanc (laurent.blanc@logistik-services.ch)

---

Madame, Monsieur

Par la présente, je donne congé de ma relation de travail avec effet au 31.03.2025.

Motif du congé: Meilleures perspectives professionnelles et développement personnel.

Mon dernier jour de travail: 31.03.2025

ATTENTION - DÉLAI DE CARENCE ASSURANCE-CHÔMAGE:
Ce congé donné par moi-même entraîne automatiquement un délai de carence dans
mes droits à l'indemnité de chômage. L'assurance-chômage prononcera un délai
de carence d'au moins 1 mois.

Date du congé: 10.02.2025
Signature: Sophie Dupont

ACCUSÉ DE RÉCEPTION EMPLOYEUR:
Reçu: 10.02.2025
Signature Direction: Laurent Blanc""",
        "pii_fields": ["name", "ahv_number", "address", "uid_number", "email"],
    },
    {
        "id": "alk_revenu_intermediate_fr_001",
        "title": "Décompte de revenu intermédiaire",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """DÉCOMPTE DE REVENU INTERMÉDIAIRE

Assuré(e):
Nom: Ferrari
Prénom: Andrea
Numéro AVS: 756.9012.3456.78
Numéro d'assurance-chômage: ALK-901234

Période de décompte: 01.02.2025 - 28.02.2025

EMPLOYEUR - REVENU INTERMÉDIAIRE:
Entreprise: Kaufhaus Zentral GmbH
Contact: Anna Schneider (anna@kaufhaus-zentral.ch)
Activité: Emploi partiel (20 heures/semaine)

REVENUS:
Salaire brut revenu intermédiaire: CHF 2.100,--
Revenu intermédiaire (déduction 20%): CHF 1.680,--

CALCUL INDEMNITÉ CHÔMAGE:
Prestation normale chômage (sans revenu intermédiaire): CHF 3.564,--
Imputation revenu intermédiaire (80%): CHF 1.344,--
Différence versée par chômage: CHF 2.220,--

TOTAL VERSÉ:
Revenu intermédiaire: CHF 1.680,--
Différence chômage: CHF 2.220,--
Total net: CHF 3.900,--

VERSEMENT:
IBAN pour différence chômage: CH90 0076 2011 6238 5296 5
Employeur effectue paiement direct revenu intermédiaire.

Titulaire compte: Andrea Ferrari
Date de versement: 05.03.2025""",
        "pii_fields": ["name", "ahv_number", "iban", "email", "insurance_number"],
    },
    {
        "id": "alk_rav_protocole_fr_001",
        "title": "Protocole de consultation RAV",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """PROTOCOLE DE CONSULTATION RAV (Placement Régional)

Bureau RAV: RAV Genève
Adresse: Office Chômage, Rue des Grenadiers 8, 1200 Genève
Date consultation: 12.02.2025 à 10h00

CONSEILLER:
Nom: Nathalie Blanc
E-mail: n.blanc@rav-geneve.ch
Téléphone: +41 22 345 67 00

PERSONNE CONSULTÉE:
Nom: Schmid
Prénom: Rita
Numéro AVS: 756.4567.8901.23
Adresse: Schulstrasse 78, 3011 Bern

PROTOCOLE DE CONSULTATION:

1. SITUATION PROFESSIONNELLE ACTUELLE:
   - Inscrit(e) au chômage depuis: 01.02.2025
   - Dernier emploi: Tessin Handwerk GmbH (Artisanat)
   - Domaines recherchés: Gestion de projet, administration

2. MESURES CONVENUES:
   - Minimum 8 candidatures par mois (contrôle mensuel)
   - Participation à cours "Techniques de candidature" dès 24.02.2025 (RAV Genève)
   - Formation spécialisée "Gestion de projet" (4 semaines, école externe)
   - Activation du réseau professionnel (LinkedIn, associations sectorielles)

3. RENDEZ-VOUS SUIVANT:
   Consultation de suivi: 12.03.2025 à 10h00

4. DOCUMENTS REQUIS:
   - CV à jour
   - Certificats de formation avant prochain rendez-vous

Signature conseiller: Nathalie Blanc
Signature assuré(e): Rita Schmid
Date protocole: 12.02.2025""",
        "pii_fields": ["name", "ahv_number", "address", "counselor_name", "email", "phone"],
    },
    {
        "id": "alk_suspension_fr_001",
        "title": "Décision de suspension des droits",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """DÉCISION: SUSPENSION DES DROITS À L'INDEMNITÉ DE CHÔMAGE

Office cantonal du chômage Bern
Kornhausplatz 5, 3011 Bern

Décision No: SUSP-2025-00214
Établie: 20.02.2025
Agent: Marcel Schmid (m.schmid@rav-bern.ch)

PERSONNE CONCERNÉE:
Nom: Meier
Prénom: Ingrid
Numéro AVS: 756.0123.4567.89
Numéro d'assurance-chômage: ALK-012345
Adresse: Bahnhofstrasse 12, 8001 Zürich

---

DÉCISION:

Par la présente, votre droit à l'indemnité de chômage est suspendu à partir du
15.03.2025 pour une durée de 30 jours.

MOTIF DE LA SUSPENSION (Responsabilité personnelle):
Vous avez mis fin volontairement à votre emploi chez Bau + Entwicklung AG le
10.02.2025 (auto-congé) sans justifier d'un motif valide selon la loi sur
l'assurance-chômage.

DÉTAILS SUSPENSION:
- Début suspension: 15.03.2025
- Fin suspension: 14.04.2025
- Reprise prestations: 15.04.2025

RECOURS:
Vous avez le droit de contester cette décision par écrit dans les 30 jours.
Adresse recours: Recours@arbeitsamt-bern.ch

Signature agent: Marcel Schmid
Cachet Office cantonal du chômage""",
        "pii_fields": ["name", "ahv_number", "address", "email", "insurance_number", "agent"],
    },
    {
        "id": "alk_mise_en_demeure_fr_001",
        "title": "Mise en demeure - Documents manquants",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """MISE EN DEMEURE - AVIS DE DOCUMENTS MANQUANTS

De: Office cantonal du chômage Genève
Office Chômage, Rue des Grenadiers 8, 1200 Genève

À: Moreau, Jean-Claude
Rue de la Gare 10, 1200 Genève
Numéro AVS: 756.3456.7890.12
Numéro d'assurance-chômage: ALK-345678

Date: 18.02.2025
Référence: RAPP-2025-00156

OBJET: AVIS DE DOCUMENTS MANQUANTS

Madame, Monsieur Moreau

Lors de l'examen de votre admissibilité à l'indemnité de chômage, nous avons
constaté que les documents suivants sont manquants:

DOCUMENTS À FOURNIR:
1. Justificatif des recherches d'emploi pour janvier 2025 (min. 8 candidatures)
2. Certificat médical pour absence 15.-20.02.2025
3. CV à jour (promis lors de consultation RAV précédente)

DÉLAI À RESPECTER:
Vous devez transmettre les documents manquants avant le 04.03.2025 (cachet postal).

CONSÉQUENCES EN CAS DE NON-RESPECT:
Si vous ne fournissez pas ces documents dans le délai imparti:
- Réduction ou suspension de vos prestations
- Obligation de remboursement des indemnités versées indûment
- Pénalités selon la loi sur l'assurance-chômage

TRANSMISSION:
E-mail: documents@oacc-geneve.ch
ou par poste à l'adresse ci-dessus

Pour questions: +41 22 345 67 00

Signature agent: Nathalie Blanc
Office cantonal du chômage Genève""",
        "pii_fields": ["name", "ahv_number", "address", "email", "phone", "insurance_number"],
    },
    {
        "id": "alk_insolvabilite_fr_001",
        "title": "Demande d'indemnité en cas d'insolvabilité",
        "language": "fr",
        "classification": "CONFIDENTIAL",
        "text": """DEMANDE D'INDEMNITÉ EN CAS D'INSOLVABILITÉ (IEO)

Présentée par:
Nom: Keller
Prénom: Maria
Adresse: Rue Principale 56, 1201 Genève
Numéro AVS: 756.2345.6789.01
Numéro d'assurance-chômage: ALK-234567
Téléphone: +41 31 987 65 43

OFFICE DE POURSUITE / FAILLITE:
Autorité de faillite: Tribunal de Faillite Genève
Adresse: Rue de la Justice 12, 1200 Genève
Numéro de faillite: GE-FAIL-2025-05678

---

EMPLOYEUR INSOLVABLE:
Entreprise: Logistik Services SA
Numéro UID: CHE-345.678.901
Administrateur faillite: Me Claire Dubois
Téléphone administration: +41 22 555 33 22

CONTRAT DE TRAVAIL:
Date début: 15.07.2022
Date fin: 31.01.2025 (faillite entreprise)
Fonction: Responsable logistique
Salaire brut: CHF 7.200,-- mensuel

SALAIRES IMPAYÉS:
Période non rémunérée: 01.01.2025 - 31.01.2025 (1 mois)
Total brut réclamé: CHF 7.200,--
Déduction AHV/ALV: CHF 720,--
Montant net réclamé: CHF 6.480,--

PIÈCES JUSTIFICATIVES:
- Contrat de travail joint
- Bulletins de salaire 2024-2025 joints
- Attestation administration faillite confirmant non-paiement

INDEMNITÉ IEO DEMANDÉE:
Salaire mensuel net selon demande de faillite: CHF 6.480,--

Déposée auprès de: Office cantonal du chômage Genève, Service IEO
Date dépôt: 15.02.2025
Signature: Maria Keller""",
        "pii_fields": ["name", "ahv_number", "address", "phone", "uid_number", "numero_faillite", "insurance_number"],
    },
]
