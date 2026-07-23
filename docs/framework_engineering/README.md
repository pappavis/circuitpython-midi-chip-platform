# Framework Engineering Bootloader

<!--
Bestand: README.md
Versienommer: 0.1.0
Doel: Gee mense en agente een beheerde ingang na die projek se bestuurs- en argitektuurkonteks.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-064 tot MCP-US-067
Actienr: MCP-ACT-FWK-001-INDEX-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Doel

Hierdie gids is die **konteks-bootloader** vir Framework Engineering. Dit is nie firmware, 'n kodegenerator of 'n alternatiewe backlog nie. Die geordende user-story-katalogus bly die produkbron van waarheid; hierdie pakket verduidelik hoe visie, argitektuur, kwaliteit en kennis daarmee saamwerk.

## Minimale leesroete

1. Lees die aktiewe story in [`../user_stories_v0.1.0.md`](../user_stories_v0.1.0.md).
2. Lees [`enterprise_vision_v0.1.0.md`](enterprise_vision_v0.1.0.md) vir produkdoel en grense.
3. Lees slegs die relevante deel van [`architecture_v0.1.0.md`](architecture_v0.1.0.md).
4. Gebruik [`glossary_v0.1.0.md`](glossary_v0.1.0.md) en [`enterprise_meta_model_v0.1.0.md`](enterprise_meta_model_v0.1.0.md) om terme en verhoudings te bevestig.
5. Pas [`quality_manual_v0.1.0.md`](quality_manual_v0.1.0.md), [`test_strategy_v0.1.0.md`](test_strategy_v0.1.0.md) en [`review_engine_v0.1.0.md`](review_engine_v0.1.0.md) toe voor Done.
6. Voor enige kodewysiging, laai die permanente [`Principal QA Architect Agent`](../governance/principal_qa_architect_agent_v0.1.0.md) en die [`Regression Memory`](../governance/regression_memory_v0.1.0.md).

## Artefakkaart

| Laag | Artefak | Vraag wat dit beantwoord |
|---|---|---|
| Visie | [Enterprise Vision](enterprise_vision_v0.1.0.md) | Waarom bestaan die produk en wat is nie nou in scope nie? |
| Argitektuur | [Architecture](architecture_v0.1.0.md) | Hoe word die oplossing geskei en ontplooi? |
| Semantiek | [Enterprise Meta Model](enterprise_meta_model_v0.1.0.md) | Hoe hou stories, komponente, toetse en besluite verband? |
| Taal | [Glossary](glossary_v0.1.0.md) | Wat beteken 'n term presies in hierdie projek? |
| Beheer | [Artefact Taxonomy](artefact_taxonomy_v0.1.0.md) | Watter dokument is gesaghebbend vir watter besluit? |
| Besluite | [ADR Repository Index](adr_repository_index_v0.1.0.md) | Watter argitektuurbesluite is aanvaar of oop? |
| Kwaliteit | [Quality Manual](quality_manual_v0.1.0.md) | Watter hekke beskerm die produk? |
| Toetsing | [Test Strategy](test_strategy_v0.1.0.md) | Waar en hoe word gedrag bewys? |
| Review | [Review Engine](review_engine_v0.1.0.md) | Hoe word interne en eksterne bevindinge geklassifiseer? |
| Governance | [Principal QA Architect Agent](../governance/principal_qa_architect_agent_v0.1.0.md) | Watter harde pre-code en post-implementation QA-gate geld? |
| Governance | [Regression Memory](../governance/regression_memory_v0.1.0.md) | Watter bekende regressies mag nooit weer as PASS deurglip nie? |
| Agentwerk | [Prompt Compiler Specification](prompt_compiler_specification_v0.1.0.md) | Hoe word 'n begrensde taakpakket saamgestel? |
| Konteks | [Context Loader Specification](context_loader_specification_v0.1.0.md) | Wat moet vir 'n story gelees word? |
| Kennis | [Knowledge Base Structure](knowledge_base_structure_v0.1.0.md) | Waar hoort bevestigde kennis? |

## Gesagsvolgorde

`AGENTS.md` en menslike veiligheidsinstruksies > Principal QA Architect Gate > goedgekeurde Product Owner-besluit > user-story/backlog > ADR > argitektuur- en kwaliteitshandleidings > story-review > adviserende review. 'n Laer laag mag nooit 'n hoër laag stilweg oorskryf nie.

## Veiligheidsgrens

- Geen framework-dokument mag globale veranderlikes, import-newe-effekte of 'n runtime-LLM-afhanklikheid magtig nie.
- Geen agent mag dokumentasie as plaasvervanger vir host-, HIL- of menslike bewys gebruik nie.
- `python-d1-synth` bly leesalleen.
- Hardewarebewys gebruik ontdekte poorte en geredigeerde identiteite.
