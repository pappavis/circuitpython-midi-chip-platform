# Evidence Package Template v1.0

<!--
Bestand: evidence_package_template_v1.0.md
Versienommer: 1.0.0
Doel: Definieer 'n repository-brede evidence package vir HIL-, investigation- en releasebewys.
Sprint: Sprint 3
Epic: MCP-EPIC-009 Framework Engineering
User-Story: INVESTIGATION-GOVERNANCE-001
Actienr: MCP-ACT-EVIDENCE-TEMPLATE-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / INVESTIGATION-GOVERNANCE-001
-->

## Doel

Een Evidence Package legt meetbewijs vast zonder interpretatie te vermengen met oplossing of implementatiekeuze. Het is bruikbaar voor investigations, HIL-runs, releasechecks en regressie-analyse.

## Harde Regels

- Bewijs is brondata, niet marketing.
- Onbekende feiten worden `UNKNOWN`.
- Menselijke observatie wordt als menselijke observatie gelabeld.
- Host-testresultaten vervangen geen HIL-bewijs.
- Een Evidence Package mag geen fixadvies als conclusie vereisen.
- Secrets, UID, MAC, SSID, tokens en private device identifiers worden geredigeerd.

## Metadata

| Veld | Waarde |
|---|---|
| Evidence Package ID | `<id>` |
| Story ID | `<story-id>` |
| Doel | `<waarvoor dient dit bewijs>` |
| Firmware versie | `<firmware-versie>` |
| Release versie | `<release-versie>` |
| Git commit | `<commit>` |
| Datum/tijd | `<YYYY-MM-DD HH:MM TZ>` |
| Tester | `<naam>` |
| Reviewer | `<naam / rol>` |
| Hardware | `<bord / module / meetopstelling>` |
| Host | `<hostnaam / OS>` |
| Tooling | `<Logic / Thonny / CLI / oscilloscope / UNKNOWN>` |

## Testcontext

| Veld | Waarde |
|---|---|
| MIDI host | `<Logic Pro / CoreMIDI sender / hardware host / UNKNOWN>` |
| Logic versie | `<versie / N/A / UNKNOWN>` |
| macOS versie | `<versie / N/A / UNKNOWN>` |
| USB poort | `<poort / hub / UNKNOWN>` |
| MIDI kanaal | `<kanaal / All / UNKNOWN>` |
| Audio backend | `<I2S / PWM / N/A / UNKNOWN>` |
| Meetinstrument | `<serial / DHO804 / gehoor / UNKNOWN>` |

## Testscenario

| Stap | Stimulus | Verwachte observatie | Werkelijke observatie | Status |
|---|---|---|---|---|
| 1 | `<stimulus>` | `<verwachting>` | `<observatie>` | `PASS / FAIL / UNKNOWN` |

## Ruwe Observaties

Plak ruwe logs of meetwaarden ongewijzigd, behalve voor redactie van private gegevens.

```text
<raw output>
```

## Meetclassificaties

Gebruik voor investigation-runs de classificaties uit de bijbehorende IDR.

| Stage | Classificatie | Bewijsregel / bron | Opmerking |
|---|---|---|---|
| `<stage>` | `<classificatie>` | `<logregel / meting>` | `<opmerking>` |

## Conclusie

Voor Investigation Stories eindigt de conclusie uitsluitend met een meetuitkomst:

```text
FIRST_DISAPPEARANCE_OF_<EVENT>=<meetpunt>
```

of:

```text
UNKNOWN;reason=<objectief gemotiveerde reden>
```

Voor release- of fixstories mag een aparte Product Owner acceptatiezin worden toegevoegd, maar alleen nadat het relevante HIL-bewijs aanwezig is.

## Open Vragen

| ID | Vraag | Impact | Eigenaar |
|---|---|---|---|
| Q-001 | `<vraag>` | `<impact>` | `<eigenaar>` |

## Bijlagen

| Bestand / bron | Doel | Redactie nodig? |
|---|---|---|
| `<pad of beschrijving>` | `<doel>` | `ja/nee` |
