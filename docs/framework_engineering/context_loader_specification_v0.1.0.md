# Context Loader Specification

<!--
Bestand: context_loader_specification_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer minimale, relevante en veilige kontekslading per werksoort.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-067 Prompt Compiler, Context Loader And Knowledge Base Structure
Actienr: MCP-ACT-067-CONTEXT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Beginsels

Laai genoeg konteks om veilig te besluit, maar nie die hele repository uit gewoonte nie. Lees eers status en grense, daarna die kleinste bron- en toetsoppervlak. Herlees lêers onmiddellik voor wysiging wanneer die worktree kan verander het.

## Basiskonteks vir elke story

1. `AGENTS.md`.
2. Hierdie Framework Engineering `README.md`.
3. Die aktiewe ry in `docs/user_stories_v0.1.0.md`.
4. `git status`, remote-identiteit en laaste commit.
5. Die primêre story-review en gekoppelde ADR/risiko.
6. Betrokke bronlêers en gerigte tests.

## Bykomende profiele

| Werksoort | Voeg by |
|---|---|
| USB/MIDI | Eventmodel, transportadapter, MIDI glossary, Logic/HIL-runbook |
| Audio/DSP | ADR-003, board profile, safety, AudioOutput/core kontrakte, heap/latency tests |
| Wi-Fi/Web | Secret boundary, scheduler, AP/station security en recovery |
| Deploy/HIL | Repository identity, manifest, device requirements, een-serial-owner runbook |
| Release | Alle Must-statusse, risk register, installasie, lessons learned, tags/rollback |
| Framework/docs | Meta model, taxonomy, link/status sanity; geen firmwarewysiging by verstek |

## Konflikhantering

Wanneer twee checkouts of dokumente verskil: stop skryfwerk, bepaal canonical remote/commit, bewaar plaaslike wysigings, en sinkroniseer met fast-forward of 'n eksplisiete mergeplan. Wanneer latest-dokumentasie en geteikende CircuitPython verskil, geld die geteikende firmware plus fisiese probe.

## Privaatheidsfilter

Moenie die inhoud van `settings.toml`, secrets, toestelrugsteune, private serial identifiers, MAC, SSID of tokens laai in publieke logs, prompts of docs nie. Gebruik SET/UNSET, profielalias of geredigeerde suffix.

## Stale-konteksreel

Herbevestig veranderlike feite goedkoop: Git-status, toetsgetal, runtimeweergawe, device mount en poortbesit. Merk duur of nie-beskikbare feite as onbevestig; moenie vorige sukses as huidige device-state voorstel nie.

## Uitset

Die loader lewer 'n kort konteksmanifest: geleesde bronne, huidige commit, aktiewe story, oop impediments, beskermde lêers en ontbrekende menslike/HIL-invoer. Dit is werkgeheue en word slegs gecommit wanneer die story dit as artefak vereis.
