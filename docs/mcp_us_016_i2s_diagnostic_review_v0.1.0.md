# MCP-US-016 Standalone I2S Audible Diagnostic Review

<!--
Bestand: mcp_us_016_i2s_diagnostic_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die standalone G-C-D/MAX98357 diagnostiek en menslike HIL-hek.
Sprint: Sprint 3
Epic: MCP-EPIC-003 Audio And Chip Core
User-Story: MCP-US-016 Standalone I2S Audible Diagnostic
Actienr: MCP-ACT-016-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-016-START
-->

## Status

**IN REVIEW / HOORBARE HIL BENODIG.** Hostgedrag, argitektuur en deploymanifest is groen. Slegs 'n mens kan bevestig dat G3-C4-D4 deur die werklike MAX98357 en luidspreker hoorbaar is.

## Implementering

- `device/i2s_test.py` is 'n selfstandige klasgebaseerde toepassing sonder `midi_chip_platform`, D1, MIDI, web of normale `code.py` runtime.
- Verstekprofiel: BCLK IO5, WS/LRC IO3, DATA/DIN IO7, 16000 Hz, mono unsigned 16-bit `RawSample` en lae amplitude.
- Die toepassing speel G3, C4 en D4 as kort square waves, stop tussen note en roep altyd `deinit()` aan.
- Serial-uitset bevat weergawe/story/datum, penprofiel, gevraagde/werklike frekwensie, heap voor/ná en `PASS` of `FAIL`.
- Die 18-lêer HIL-manifest deploy `i2s_test.py` as 'n aparte lêer en vervang nie die normale runtime nie.

## RED/GREEN-bewys

| Fase | Bewys |
|---|---|
| RED | Vier toetse het gefaal omdat `device/i2s_test.py` nie bestaan het nie |
| GREEN | Profiel, sample-range, drie note, stop/deinit en onafhanklikheid slaag |
| REGRESSION | 103 hosttoetse en Ruff slaag; class/no-globals en geen synth-import bly groen |
| HIL | Oop totdat die Product Owner die drie note hoor en die serial PASS-uitset deel |

## Veiligheid voor toets

1. MAX98357 `VIN` gaan na die bedoelde voedingsrail en `GND` deel grond met die Wemos.
2. `BCLK -> IO5`, `LRC/WS -> IO3` en `DIN/SD -> IO7`.
3. Die luidspreker sit slegs tussen die MAX98357 `+` en `-` terminale. Geen luidsprekerterminaal gaan na grond, Scarlett line-in of 'n geaarde ossilloskoopklem nie.
4. Begin met die luidspreker weg van jou ore. Die diagnostiek gebruik 'n lae digitale amplitude.
5. Net een serial client gebruik die toestel tydens deploy/run.

## Menslike aanvaarding

Ná dependency-closed deploy:

1. Open `i2s_test.py` vanaf die CIRCUITPY-volume in Thonny.
2. Kies **Run current script**. Dit laat die normale `code.py` op die volume staan.
3. Verwag drie duidelike tone in volgorde: laer G, hoër C, nog hoër D.
4. Verwag serial `I2S_DIAGNOSTIC_STATUS=PASS;notes=3;...`.
5. Druk `Ctrl-D` om die normale `code.py` daarna weer te begin.

US-016 word eers `Done` wanneer hoorbaarheid, PASS-uitset en herbegin bevestig is. Die 30-minute smoke volg ná die eerste kort hoorbare bewys.

## Burn-in

`Burn-in: Required`. Eerste aanvaarding gebruik een kort siklus. Daarna herhaal die HIL-profiel G-C-D vir 30 minute en beoordeel reset, permanente stilte, I2S-herbruikbaarheid en heap volgens die burn-in-spesifikasie.

## Bronne

- CircuitPython `audiobusio.I2SOut` en `deinit`: https://docs.circuitpython.org/en/latest/shared-bindings/audiobusio/
- CircuitPython `audiocore.RawSample`: https://docs.circuitpython.org/en/latest/shared-bindings/audiocore/
- Adafruit MAX98357 CircuitPython wiring/test: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/circuitpython-wiring-test

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Prioritiseer eerste hoorbare klank en lewer finale menslike aanvaarding. |
| Scrum Master | Hou D1 en alle side quests agter die US-016 hoorbare hek. |
| Business Analyst | Skei kort hoorbare bewys van die daaropvolgende 30-minute smoke. |
| Chief Enterprise Architect | Behou diagnostiek as onafhanklike capability probe, nie 'n tweede runtime nie. |
| Framework Engineer | Bevestig artefakgesag en traceability. |
| Solution Architect | Hou profielvelde semanties versoenbaar met produksie-AudioOutput sonder runtime-import. |
| Embedded Engineer | Kies `I2SOut`, `RawSample`, veilige cleanup en geïnjekteerde penprofiel. |
| MIDI Engineer | Not impacted: hierdie toets ontvang geen MIDI nie. |
| DSP/Chip Engineer | Genereer begrensde square waves en rapporteer kwantisering van werklike frekwensie. |
| Web Engineer | Not impacted: Wi-Fi en web bly af. |
| QA/HIL Engineer | Lewer RED/GREEN, AST, fake-device lifecycle en menslike toetsprosedure. |
| Release/Documentation | Merk v0.14.0 eerlik as In Review totdat klank gehoor is. |
| External Architecture Reviewer (Copilot) | Burn-in- en heap-aanbevelings is aan die story gekoppel. |
| Devil's Advocate | Waarsku dat serial PASS sonder hoorbare luidsprekerklank nie genoeg is nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
