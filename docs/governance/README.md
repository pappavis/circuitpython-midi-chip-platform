# Governance Artefacts

<!--
Bestand: README.md
Versienommer: 0.1.0
Doel: Indekseer permanente governance-artefakte wat ontwikkeling en releasebesluite beheer.
Sprint: Sprint 3
Epic: MCP-EPIC-009 Framework Engineering
User-Story: PRINCIPAL-QA-ARCHITECT-001
Actienr: MCP-ACT-QA-ARCHITECT-001-INDEX-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / PRINCIPAL-QA-ARCHITECT-001
-->

## Doel

Hierdie gids bevat permanente projekreels wat die ontwikkelproses self beheer. Dit is nie firmware nie en mag geen runtime-afhanklikheid word nie.

## Artefakte

| Artefak | Status | Wanneer laai? |
|---|---|---|
| [Principal QA Architect Agent](principal_qa_architect_agent_v0.1.0.md) | Aktief | Voor elke kodewysiging en weer na implementering |
| [Regression Memory](regression_memory_v0.1.0.md) | Aktief | Voor elke MIDI-, audio-, HIL-, runtime- of diagnostic-wysiging |

## Harde reël

Die Principal QA Architect-agent is 'n review-agent, nie 'n programmeer-agent nie. Indien die agent twyfel of bestaande funksionaliteit behoue bly, is die verdict `REJECT`.
