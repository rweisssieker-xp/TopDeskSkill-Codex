# Localization Guide

Primary locale: `en-US`.

The TOPdesk Skill Suite keeps the canonical skill instructions and operational documentation in `en-US`. Users can request output in any supported European locale by naming the locale in the prompt, for example:

```text
Use de-DE and create a TOPdesk migration plan.
Use fr-FR and review TOPdesk OData/API mapping.
Use nl-NL and create a Power BI reporting backlog.
```

## Language Behavior

- Default to `en-US` when the user does not specify a language.
- Match the user's language when it is clear from the prompt.
- Keep TOPdesk product names, API paths, script names, field names, DAX, Power Query, SQL, and PowerShell commands unchanged.
- Translate business explanations, checklists, acceptance criteria, user-facing summaries, and stakeholder messages.
- Prefer locale-specific terminology for service management, privacy, security, and reporting, but do not invent TOPdesk feature names.
- When a term is ambiguous, write the local term first and keep the English source term in parentheses.

## Marketplace Summary

`en-US`: TOPdesk-focused Codex skills for implementation, OData/API mapping, Power BI reporting, migration, operations, security, testing, AI governance, proof-of-value, and enablement.

`de-DE`: Codex-Skills fuer TOPdesk-Implementierung, OData/API-Mapping, Power-BI-Reporting, Migration, Betrieb, Sicherheit, Tests, KI-Governance, Proof of Value und Enablement.

`fr-FR`: Competences Codex pour TOPdesk couvrant implementation, mapping OData/API, reporting Power BI, migration, operations, securite, tests, gouvernance IA, preuve de valeur et accompagnement.

`es-ES`: Skills de Codex para TOPdesk: implantacion, mapeo OData/API, informes Power BI, migracion, operaciones, seguridad, pruebas, gobierno de IA, prueba de valor y capacitacion.

`it-IT`: Skill Codex per TOPdesk: implementazione, mapping OData/API, reporting Power BI, migrazione, operations, sicurezza, test, governance AI, proof of value e abilitazione.

`nl-NL`: Codex-skills voor TOPdesk-implementatie, OData/API-mapping, Power BI-rapportage, migratie, beheer, security, testen, AI-governance, proof-of-value en enablement.

`pl-PL`: Umiejetnosci Codex dla TOPdesk: wdrozenia, mapowanie OData/API, raportowanie Power BI, migracje, operacje, bezpieczenstwo, testy, nadzor AI, proof of value i enablement.

## Supported European Locale Starters

| Locale | Language | Prompt starter |
| --- | --- | --- |
| `en-US` | English (primary) | Plan a TOPdesk migration. |
| `en-GB` | English (UK) | Prepare a TOPdesk service management rollout. |
| `de-DE` | German | Plane eine TOPdesk Migration. |
| `fr-FR` | French | Planifie une migration TOPdesk. |
| `es-ES` | Spanish | Planifica una migracion TOPdesk. |
| `it-IT` | Italian | Pianifica una migrazione TOPdesk. |
| `nl-NL` | Dutch | Plan een TOPdesk-migratie. |
| `nl-BE` | Dutch (Belgium) | Plan een TOPdesk-implementatie. |
| `fr-BE` | French (Belgium) | Prepare un deploiement TOPdesk. |
| `pt-PT` | Portuguese | Planeia uma migracao TOPdesk. |
| `pl-PL` | Polish | Zaplanuj migracje TOPdesk. |
| `cs-CZ` | Czech | Naplanuj migraci TOPdesk. |
| `sk-SK` | Slovak | Naplanuj migraciu TOPdesk. |
| `sl-SI` | Slovenian | Nacrtuj migracijo TOPdesk. |
| `hr-HR` | Croatian | Isplaniraj TOPdesk migraciju. |
| `bs-BA` | Bosnian | Isplaniraj TOPdesk migraciju. |
| `sr-Latn-RS` | Serbian (Latin) | Isplaniraj TOPdesk migraciju. |
| `sq-AL` | Albanian | Planifiko nje migrim TOPdesk. |
| `mk-MK` | Macedonian | Isplaniraj TOPdesk migracija. |
| `el-GR` | Greek | Schediase mia metanastefsi TOPdesk. |
| `bg-BG` | Bulgarian | Planiray migratsiya na TOPdesk. |
| `ro-RO` | Romanian | Planifica o migrare TOPdesk. |
| `hu-HU` | Hungarian | Tervezz TOPdesk migraciot. |
| `et-EE` | Estonian | Planeeri TOPdesk migratsioon. |
| `lv-LV` | Latvian | Izplano TOPdesk migraciju. |
| `lt-LT` | Lithuanian | Suplanuok TOPdesk migracija. |
| `da-DK` | Danish | Planlaeg en TOPdesk-migrering. |
| `sv-SE` | Swedish | Planera en TOPdesk-migrering. |
| `nb-NO` | Norwegian Bokmal | Planlegg en TOPdesk-migrering. |
| `fi-FI` | Finnish | Suunnittele TOPdesk-migraatio. |
| `is-IS` | Icelandic | Skipuleggdu TOPdesk-flutning. |
| `ga-IE` | Irish | Pleanaigh imirce TOPdesk. |
| `mt-MT` | Maltese | Ippjana migrazzjoni TOPdesk. |
| `cy-GB` | Welsh | Cynlluniwch fudo TOPdesk. |
| `ca-ES` | Catalan | Planifica una migracio TOPdesk. |
| `eu-ES` | Basque | Planifikatu TOPdesk migrazio bat. |
| `gl-ES` | Galician | Planifica unha migracion TOPdesk. |
| `lb-LU` | Luxembourgish | Plang eng TOPdesk-Migratioun. |
| `uk-UA` | Ukrainian | Zaplanuj migratsiyu TOPdesk. |
| `tr-TR` | Turkish | Bir TOPdesk gecisi planla. |

## Localized Task Families

Use the same task families in every locale:

- Migration and rollout planning.
- OData/API discovery and mapping.
- Power BI semantic modelling, DAX, Power Query, reporting, and reconciliation.
- AI feature design, prompt/eval governance, RAG/search, and AI monitoring.
- Security, privacy, PII review, and operational runbooks.
- Proof-of-value, ROI, business cases, USPs, and battlecards.

## Translation Quality Rules

- Keep generated files actionable and concise.
- Avoid literal translation when local ITSM terminology is well established.
- Preserve legal, security, and privacy caveats in full.
- Do not translate code identifiers, JSON keys, API route names, file names, or command examples.
- Ask for the target locale only when the output will be customer-facing and the user's language is unclear.
