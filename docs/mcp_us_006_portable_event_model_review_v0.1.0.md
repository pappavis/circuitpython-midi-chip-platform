# MCP-US-006 Portable NoteEvent And ControlEvent Model Review

<!--
Bestand: mcp_us_006_portable_event_model_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die transport-onafhanklike MIDI-eventmodel, toetse en menslike aanvaarding.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-006 Portable NoteEvent And ControlEvent Model
Actienr: MCP-ACT-006-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-006-IN-REVIEW
-->

## Status

**IN REVIEW.** Die hostimplementering, terugwaartse versoenbaarheid, AST-governance en regressie is groen. Hierdie story het geen fisiese MIDI- of toestel-HIL nodig nie; Product Owner-aanvaarding volg met `events-diagnose` en die eventtoetse.

## Gelewer

- `MidiEvent` bly die algemene fabriek- en basiskontrak.
- `NoteEvent` besit note-on/note-off, musikantkanaal 1-16, noot 0-127 en velocity 0-127.
- `ControlEvent` besit CC control/value 0-127 en pitch bend 0-16383; `centered_value` lewer -8192 tot 8191.
- `ClockEvent` besit Timing Clock, Start, Stop en Continue sonder MIDI-kanaal.
- Geen `adafruit_midi`, USB-, BLE-, UART-, bord- of klanktipe lek die domeinmodel binne nie.
- `MidiEvent.note_on()`, `note_off()`, `control_change()` en `pitch_bend()` lewer die nuwe spesifieke klasse.

## Bewuste nie-doelwitte

- Note On met velocity nul word eers in MCP-US-009 na Note Off genormaliseer.
- Geen USB-MIDI-byte of Adafruit-objek word in hierdie story vertaal nie; dit begin in MCP-US-007.
- Geen channel router, pitch-bend-klank, MIDI clock-scheduler of Fishman slidegedrag word vooruit geïmplementeer nie.

## RED/GREEN-bewys

- RED: import van `ClockEvent`, `ControlEvent` en `NoteEvent` het soos verwag gefaal.
- Tweede RED: `events-diagnose` was nog nie 'n geldige CLI-keuse nie.
- GREEN: 49 hosttoetse slaag op `v0.6.0`.
- CLI-bewys: `EVENT_MODEL_STATUS=PASS` plus note-, CC-, bend- en clockreëls.

## Menslike aanvaarding

Voer vanuit die repository en geaktiveerde virtuele omgewing uit:

```bash
python -m midi_chip_platform events-diagnose
python -m pytest -q tests/test_domain_events.py
```

Aanvaar indien die eerste opdrag `EVENT_MODEL_STATUS=PASS` en vier eventreëls wys, en die tweede opdrag met alle toetse `passed` eindig.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het US-006 vooraf goedgekeur en menslike hosttoetsing vir ná werk beplan. |
| Scrum Master | Beperk die story tot die eventmodel; fisiese receive loop bly US-007. |
| Business Analyst | Skeur note, controls/bend en transport-clock in toetsbare gebruikersbegrippe. |
| Solution Architect | Behou die domeinmodel los van Adafruit-, USB-, BLE- en UART-backends. |
| Embedded Engineer | Bevestig dat die klasse CircuitPython-vriendelike gewone Python gebruik. |
| MIDI Engineer | Verifieer 7-bit note/CC, 14-bit bend, kanaal 1-16 en kanaallose real-time clock. |
| DSP/Chip Engineer | Not impacted: events word nog nie na oscillators of klank gemap nie. |
| Web Engineer | Bevestig dat die latere webkeyboard dieselfde NoteEvent kan skep. |
| QA/HIL Engineer | Lewer twee RED-fases, grenswaardetoetse, regressie en CLI-aanvaarding. |
| Release/Documentation | Sinkroniseer v0.6.0, Sprint 2, review, quickstart, bronne en Kanban. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe reviewer-inset is vir US-006 ontvang nie. |
| Devil's Advocate | Blokkeer voortydige velocity-zero, MPE/slide en routingsemantiek. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
