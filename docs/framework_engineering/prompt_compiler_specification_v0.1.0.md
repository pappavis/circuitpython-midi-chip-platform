# Prompt Compiler Specification

<!--
Bestand: prompt_compiler_specification_v0.1.0.md
Versienommer: 0.1.0
Doel: Spesifiseer hoe 'n begrensde, naspeurbare ontwikkeltaak vir 'n mens of agent saamgestel word.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-067 Prompt Compiler, Context Loader And Knowledge Base Structure
Actienr: MCP-ACT-067-PROMPT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Status en grens

Hierdie is 'n **ontwikkelprosesspesifikasie**, nie firmware of 'n verpligte LLM-program nie. “Compile” beteken dat gesaghebbende projekinvoer na 'n klein taakpakket georden word. Geen synth-runtime, webinterface of build hang van 'n LLM af nie.

## Invoer

1. Aktiewe ChatID en goedgekeurde story/impediment.
2. Harde reels uit `AGENTS.md`.
3. Storykriteria, afhanklikhede en huidige status.
4. Relevante argitektuurpoort/ADR.
5. Betrokke lêers en huidige Git-diff.
6. Bestaande tests/HIL-bewys en risiko's.
7. Menslike instruksie oor gewenste uitset en aanvaarding.

## Deterministiese samestellingsorde

`Safety -> repository identity -> scope/story -> architecture -> source evidence -> test contract -> implementation constraints -> human acceptance -> publication`.

'n Laer-prioriteit bron word weggelaat of as konflik gemerk wanneer dit 'n hoër-prioriteit reel weerspreek. Onbevestigde gesprekstekens word aannames, nie feite nie.

## Uitsetkontrak

| Veld | Vereiste |
|---|---|
| Identity | ChatID, story, aksie, repo en branch/commit |
| Objective | Een toetsbare uitkoms |
| In scope | Lêers/komponente wat mag verander |
| Out of scope | Side quests en beskermde repositories |
| Constraints | Klasse, geen globals, CircuitPython-teiken, security |
| Red | Ontbrekende/falende kontrak |
| Green | Kleinste beoogde implementering |
| Verification | Gerigte suite, regressie, HIL en menslike toets |
| Risks | Top-risiko's en rollback |
| Closure | Docs, Kanban, commit/push en volgende story |

## Validasiereels

- Presies een implementasiestory is aktief.
- Alle verwysde lêers bestaan of word eksplisiet as nuwe deliverables aangedui.
- Geen private settings, serial UID, SSID of wagwoord word ingesluit nie.
- Geen “Done” word vooraf saamgestel nie.
- 'n Hardwarestory bevat bedradings-/veiligheidsgrens, stimulus, PASS/FAIL en herstel.
- Die taakpakket mag nie self toestemming vervaardig nie; Product Owner-goedkeuring bly 'n menslike gebeurtenis tensy vooraf eksplisiet opgehef.

## Opsionele Ollama

'n Plaaslike model mag slegs 'n vooraf goedgekeurde, nie-sensitiewe klein subtaak ontvang nadat beskikbaarheid en 'n timeboxed proef bevestig is. Model, taak en uitkoms word in docs gelog. Codex/QA hersien alles. `default` bly die fallback en geen modeluitset word bron van waarheid nie.
