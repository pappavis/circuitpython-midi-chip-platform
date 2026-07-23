# MCP-US-101 First MVP Implementation Step Decision

<!--
Bestand: MCP-US-101-FIRST-MVP-STEP.md
Versienommer: 0.1.0
Doel: Som objektief bestaande kandidaatpaden op sodat die Product Owner die eerste MCP-US-100 implementatiestap kan kies.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-101 Resolve First MVP Implementation Step
Actienr: MCP-ACT-101-FIRST-MVP-STEP-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-101
-->

## 1. Probleemstelling

MCP-US-100 kan nog nie met runtime-code begin nie omdat `docs/mvp/MVP_BUILD_PLAN.md` die post-MCP-US-090 implementatiestap as `UNKNOWN` merk.

Die bestaande dokumentasie bewys wel:

- `MCP-US-090` het die native CoreMIDI-route na destination UniqueID `2064399636` bevestig met `LIVE_ROUTE_CONFIRMED`;
- `MCP-US-055` bly as P0 impediment oop;
- die MVP-doel bly Logic Pro External MIDI na hoorbare D1 deur MAX98357 mono-I2S;
- `MCP-US-057` kan eers ná die volledige MVP acceptance set en burn-in sluit.

Die Product Owner moet dus een bestaande kandidaatpad kies voordat MCP-US-100 in 'n concrete implementatiestory opgesplits kan word.

## 2. Kandidaten

| Optie | Bron | Doel | Vereist code? | Past binnen MVP? |
|---|---|---|---|---|
| A. Sluit `MCP-US-079` HIL af: Persistent Synthio Audio Graph Spike | `docs/mcp_us_079_persistent_synthio_audio_graph_plan_v0.1.0.md`; `docs/decisions/ADR-004-persistent-realtime-audio-graph.md`; `docs/user_stories_v0.1.0.md` | Bewys dat 20 Logic NoteOns hoorbaar realtime speel sonder 12-20s backlog met bestaande `synthio_runtime.py` | Nee indien slegs HIL/acceptance; ja indien HIL faal en later 'n aparte fixstory nodig is | Ja volgens user-story-katalogus as MVP-Enabler |
| B. Heropen `MCP-US-055`: macOS Logic Pro Audible D1 Acceptance | `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md`; `docs/mvp/MVP_BUILD_PLAN.md`; `docs/user_stories_v0.1.0.md` | Bewys die volledige Logic Pro -> USB-MIDI -> D1 runtime -> I2S hoorbare productflow | Ja indien huidige runtime nie aan acceptance voldoen nie | Ja volgens MVP-Must |
| C. Berei `MCP-US-057`: MVP Release Candidate And Demo voor | `docs/user_stories_v0.1.0.md`; `docs/agile_delivery_release_plan_v0.1.0.md`; `docs/mvp_scope_v0.1.0.md` | Tag, release notes, bekende beperkings en 8-uur burn-in by 'n herhaalbare Logic USB-MIDI na hoorbare D1-demo voeg | Ja of nee, afhangend van ontbrekende release artefakte; bron is nie spesifiek nie | Ja volgens MVP-Must, maar afhanklik van US-055 |
| D. Bevestig `MCP-US-090` as bronbewys vir die host-route binne MCP-US-100 evidence | `docs/evidence/mcp-us-090/final-assessment-run2.log`; `docs/evidence/mcp-us-090/live-correlation-run2.log`; `docs/mvp/MVP_BUILD_PLAN.md` | Gebruik controlled CoreMIDI route proof as vaste evidence dat host -> S2 endpoint werk voordat productflow getest word | Nee indien alleen evidence-koppeling; ja indien nieuwe automation/story wordt gevraagd | Ja als ondersteunend bewijs; niet als volledige MVP-demo |

## 3. Effectanalyse

### Optie A. Sluit `MCP-US-079` HIL af

- Voordelen:
  - Volgt direct uit het bestaande `MCP-US-079` plan.
  - Richt zich op de bekende 12-20s audio-backlog.
  - Vereist mogelijk eerst alleen HIL en geen runtime-code.
- Risico's:
  - ADR-004 staat nog op `Proposed`.
  - `MCP-US-079` is een spike/enabler, niet de volledige D1 productacceptance.
  - HIL kan alsnog falen en dan is een aparte fixstory nodig.
- Afhankelijkheden:
  - `MCP-US-016`, `MCP-US-077`, `MCP-US-078` en ADR-004 volgens user-story-katalogus.

### Optie B. Heropen `MCP-US-055`

- Voordelen:
  - Sluit direct aan op het MVP-Must doel.
  - Test de volledige eindgebruikersflow.
  - `MCP-US-090` heeft het host-route risico verkleind.
- Risico's:
  - `MCP-US-055` staat nog als P0 impediment gedocumenteerd.
  - Zonder gekozen runtime primitive kan implementatie opnieuw impliciet ontwerp worden.
  - HIL-failure kan terugvallen op `MCP-US-079` of een nieuwe expliciete fixstory vereisen.
- Afhankelijkheden:
  - `MCP-US-003`, `MCP-US-007`, `MCP-US-009`, `MCP-US-014`, `MCP-US-016`, `MCP-US-063`, `MCP-US-075`, `MCP-US-077`, `MCP-US-078`, `MCP-US-079`, `MCP-US-080`, `MCP-US-080-INV-001` volgens user-story-katalogus.

### Optie C. Berei `MCP-US-057` voor

- Voordelen:
  - Richt zich op de uiteindelijke MVP release candidate.
  - Maakt burn-in, release notes en demo-evidence zichtbaar.
  - Sluit aan op releaseplan en Definition of Done.
- Risico's:
  - `MCP-US-057` hangt volgens katalogus af van `MCP-US-055`.
  - Zonder hoorbare Logic -> D1 acceptance kan dit geen MVP Accepted opleveren.
  - Kan release-documentatie vóór productacceptance naar voren trekken.
- Afhankelijkheden:
  - Volledige MVP Acceptance Set en `MCP-US-055`.

### Optie D. Bevestig `MCP-US-090` als bronbewys binnen MCP-US-100 evidence

- Voordelen:
  - Gebaseerd op recente PASS-evidence.
  - Maakt duidelijk dat host CoreMIDI -> S2 endpoint niet meer het primaire onbekende punt is.
  - Vereist geen runtime-code indien uitsluitend evidence-baseline.
- Risico's:
  - Bewijst niet Logic Pro External MIDI als gebruikerspad.
  - Bewijst niet D1 of I2S audio.
  - Kan niet als volledige MVP implementatiestap gelden.
- Afhankelijkheden:
  - `docs/evidence/mcp-us-090/*run2.log`.

## 4. Product Owner Decision

SELECTED OPTION:
_____

Product Owner naam:
_____

Datum:
_____

Besluitnotitie:
_____

## 5. Gevolg

Na selectie van één optie kan MCP-US-100 worden opgesplitst in een concrete implementatiestory met:

- exacte bron;
- exacte files;
- RED-test;
- GREEN-implementatie;
- HIL-acceptatie;
- evidencepad onder `docs/evidence/mcp-us-100/`;
- één kleine commit per logisch onderdeel.
