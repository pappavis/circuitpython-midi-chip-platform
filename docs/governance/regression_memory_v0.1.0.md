# Regression Memory

<!--
Bestand: regression_memory_v0.1.0.md
Versienommer: 0.1.0
Doel: Bewaar bekende regressies wat toekomstige reviews aktief moet teenhou.
Sprint: Sprint 3
Epic: MCP-EPIC-009 Framework Engineering
User-Story: PRINCIPAL-QA-ARCHITECT-001
Actienr: MCP-ACT-QA-ARCHITECT-001-REGRESSION-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / PRINCIPAL-QA-ARCHITECT-001
-->

## Gebruik

Hierdie lêer is 'n aktiewe regressiegeheue. Elke Principal QA Architect review vir MIDI, audio, HIL, runtime of diagnostic werk moet hierdie lêer raadpleeg voordat die verdict gegee word.

## REG-080-001: MCP-US-080 Control-Only False PASS Regression

| Veld | Waarde |
|---|---|
| Status | Aktief P0 |
| Ontdek deur | Product Owner HIL-test |
| Release | `v0.20.0` |
| Story | `MCP-US-080` |
| Datum | 2026-07-23 |
| Impak | MVP-blokker: Logic Pro note routing nie bewys nie |

### Waargenome mislukking

Die toestel het die MCP-US-080 MIDI routing diagnostic gestart, maar:

- daar was geen hoorbare audition-beep nie;
- Logic Pro note playback is nie as `NoteOn`/`NoteOff` ontvang nie;
- die S2 het slegs herhalende `Control Change` events gesien;
- die diagnostic het verkeerdelik `PASS` gerapporteer met `note_on=0` en `note_off=0`.

### Kritieke bewys

```text
circuitpython-midi-chip-platform v0.20.0 | story=MCP-US-080 | release-date=2026-07-23
MIDI_ROUTING_DIAGNOSTIC_STATUS=START;scan_all_ports=true;port_count=2;max_events=32;timeout_seconds=120;heartbeat_seconds=2
MIDI_ROUTING_DIAGNOSTIC_INPUT_STATUS=OPEN;scan_all_ports=true;port_count=2
MIDI_ROUTING_DIAGNOSTIC_READY;ready_ms=0
MIDI_ROUTING_EVENT=control_change;channel=1;control=7;value=0;event_ms=7
MIDI_ROUTING_EVENT=control_change;channel=1;control=7;value=0;event_ms=15
MIDI_ROUTING_EVENT=control_change;channel=1;control=7;value=0;event_ms=164
MIDI_ROUTING_DIAGNOSTIC_STATUS=PASS;events=32;note_on=0;note_off=0;control=32;clock=0;ignored=0
```

### Expected behavior

Wanneer 'n diagnostic bedoel is om musikale MIDI routing uit Logic Pro te bewys, mag dit nie `PASS` rapporteer sonder minstens een relevante `NoteOn` nie. Vir 'n volledige note-routing acceptatietest moet `NoteOn` en `NoteOff` aantoonbaar wees, of die diagnostic moet eksplisiet `FAIL` rapporteer met 'n rede soos `no_note_events`.

### Permanente QA kontroles

Elke toekomstige MIDI/audio/HIL review moet `REJECT` indien:

1. 'n note-routing test slegs Control Change-events sien en steeds `PASS` rapporteer;
2. `NoteOn`/`NoteOff` nie in die HIL-log verskyn waar dit deur die testdoel vereis word nie;
3. audition of audio-preflight stilweg verdwyn sonder Product Owner-besluit;
4. debugdata nie onderskei tussen control traffic en musieknote nie;
5. 'n host-toets groen is maar die HIL-bewys die musiekpad nie bewys nie;
6. 'n fix latensie, MIDI-poortkeuse of event filtering verander sonder regressietoets.

### Aanbevole toekomstige fix-rigting

- Skei diagnostic-modusse: `control-monitor`, `note-routing`, `clock-monitor` en `audio-routing`.
- Laat note-routing default `FAIL` wanneer `note_on == 0`.
- Rapporteer poortindeks en eventtype per event.
- Maak boot audition 'n eksplisiete config-keuse met duidelike startup-log.
- Voeg 'n HIL-acceptance script by wat Logic/CoreMIDI note events of 'n bekende host MIDI sender kan stuur en die toestel-log evalueer.
