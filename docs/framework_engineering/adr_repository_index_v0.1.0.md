# ADR Repository Index

<!--
Bestand: adr_repository_index_v0.1.0.md
Versienommer: 0.1.0
Doel: Indekseer argitektuurbesluite en definieer ADR-governance.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-066 Quality Manual, Test Strategy And Review Engine
Actienr: MCP-ACT-066-ADR-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Register

| ADR | Status | Besluit | Primêre fitness-bewys |
|---|---|---|---|
| [ADR-001](../decisions/ADR-001-repository-strategy.md) | Aanvaar | Skoon repository met beheerde hergebruik | Leesalleen D1-grens, reuse matrix, Git history |
| [ADR-002](../decisions/ADR-002-reference-platform.md) | Aanvaar | Wemos S2 as verwysingsbord; portabiliteit deur profiele | Capability discovery en tweede-bordstory |
| [ADR-003](../decisions/ADR-003-audio-strategy.md) | Aanvaar | MAX98357 mono-I2S eerste; PWM fallback | MCP-US-016 hoorbare HIL en US-021 stereo-besluit |

## Wanneer 'n ADR nodig is

'n ADR is verpligtend vir verandering aan 'n publieke poort, repositorygrens, verwysingsplatform, USB-identiteitstrategie, audio-backendstrategie, security boundary, data-/geheime-eienaarskap of 'n onomkeerbare releaseclaim. Gewone interne implementasiedetail bly in die story review.

## Lewensiklus

`Proposed -> Accepted/Rejected -> Superseded`.

Die ADR beskryf konteks, opsies, besluit, gevolge, fitness tests en rollback. 'n Aanvaarde ADR word nie stilweg herskryf om 'n nuwe besluit te laat lyk asof dit altyd gegeld het nie; 'n nuwe ADR vervang dit eksplisiet.

## Oop ADR-kandidate

- Stabiele USB-instance-identiteit en privaatheidsgrens vir MCP-US-068.
- Stereo-backendkeuse: twee MAX98357's teenoor 'n PCM5102-klas stereo-DAC.
- Multi-core resource admission/eviction vir MCP-US-061.
- Wi-Fi station/AP security en recovery vir MCP-US-027.
