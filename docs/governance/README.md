# Governance Artefacts

<!--
Bestand: README.md
Versienommer: 0.2.0
Doel: Indekseer permanente governance-artefakte wat ontwikkeling, investigation en releasebesluite beheer.
Sprint: Sprint 3
Epic: MCP-EPIC-009 Framework Engineering
User-Story: INVESTIGATION-GOVERNANCE-001
Actienr: MCP-ACT-IDR-TEMPLATE-001-INDEX-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / INVESTIGATION-GOVERNANCE-001
-->

## Doel

Hierdie gids bevat permanente projekreels wat die ontwikkelproses self beheer. Dit is nie firmware nie en mag geen runtime-afhanklikheid word nie.

## Artefakte

| Artefak | Status | Wanneer laai? |
|---|---|---|
| [Principal QA Architect Agent](principal_qa_architect_agent_v0.1.0.md) | Aktief | Voor elke kodewysiging en weer na implementering |
| [Regression Memory](regression_memory_v0.1.0.md) | Aktief | Voor elke MIDI-, audio-, HIL-, runtime- of diagnostic-wysiging |
| [Instrumentation Design Review Template](instrumentation_design_review_template_v1.0.md) | Aktief | Voor tijdelijke instrumentatie in elke goedgekeurde Investigation Story |
| [Evidence Package Template](evidence_package_template_v1.0.md) | Aktief | Voor HIL-, investigation-, release- en regressiebewys |

## Harde reël

Die Principal QA Architect-agent is 'n review-agent, nie 'n programmeer-agent nie. Indien die agent twyfel of bestaande funksionaliteit behoue bly, is die verdict `REJECT`.

## Investigation Governance Freeze

Na toevoeging van die IDR- en Evidence Package-templates word Framework Engineering vir die huidige P0-blokker bevries. Verdere governance-uitbreiding moet na Backlog/Later tensy dit direk nodig is om `MCP-US-080-INV-001` meetbaar af te rond.
