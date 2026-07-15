# Knowledge Base Structure

<!--
Bestand: knowledge_base_structure_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer waar bevestigde projekkennis, besluite, bewys en tydelike werk hoort.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-067 Prompt Compiler, Context Loader And Knowledge Base Structure
Actienr: MCP-ACT-067-KB-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Struktuur

```text
AGENTS.md                                  harde werk- en kodereels
README.md                                  gebruiker- en projekingang
docs/user_stories_v0.1.0.md                geordende produkbron
docs/framework_engineering/                visie, argitektuur, kwaliteit en konteks
docs/decisions/                            aanvaar/verwerp/vervangde ADR's
docs/mcp_us_*_review_v*.md                  storyspesifieke implementasie en bewys
docs/lessons_learned_*                      herbruikbare proseslesse
docs/risk_register_v*.md                    aktiewe en geslote risiko's
docs/source_register_v*.md                  eksterne bronherkoms
outputs/<ChatID>/                           redigeerbare Kanban en ander deliverables
src/ en tests/                              uitvoerbare bron van gedrag
device/                                     ontplooibare manifest en libraries
/private/tmp of private backup              tydelike probes; nooit bron van waarheid
```

## Kennisklasse

| Klas | Voorbeeld | Vertrouensvlak |
|---|---|---|
| Normatief | AGENTS, goedgekeurde story, ADR | Bindend binne gesag |
| Uitvoerbaar | Bron, tests, manifest | Bewysbaar op host/device |
| Empiries | HIL-log, hoorbare/meetresultaat | Sterk vir presiese omgewing/commit |
| Adviserend | QA-oudit, Copilot-review | Moet geklassifiseer word |
| Tydelik | Scratch probe, chatplan | Nie basis vir release sonder bevordering nie |

## Bevordering van kennis

'n Chatwaarneming word eers 'n projekfeit wanneer dit gereproduseer, geredigeer, aan 'n story/risiko gekoppel en in die gepaste review/ADR/test vasgelê is. 'n Lessons-learned-item word 'n harde reel slegs wanneer `AGENTS.md`, 'n quality gate of 'n toets dit afdwing.

## Dubbele bronvoorkoming

- Storytitel/status: user-story-katalogus en Kanban, met Markdown as mensleesbare baseline.
- Argitektuurbesluit: ADR, elders slegs skakel en opsomming.
- Detailtoetsbewys: story review, README slegs huidige status.
- Termdefinisie: glossary.
- Eksterne URL: source register of relevante ADR/review.

## Onderhoud

By elke closure kontroleer Release/Documentation skakels, metadata en stale status. By elke drie/vier stories konsolideer lessons learned. By release word verweesde artefakte, onopgeloste konflik en private data geblokkeer. Kennis word nie verwyder om 'n mislukking onsigbaar te maak nie; verouderde besluite word as superseded gemerk.
