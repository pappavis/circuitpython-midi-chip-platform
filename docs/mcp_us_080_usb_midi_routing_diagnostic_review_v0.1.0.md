# MCP-US-080 USB MIDI Endpoint Routing Diagnostic Review

Versienommer: 0.1.0  
Release: v0.20.0  
Datum: 2026-07-23  
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-START  
Sprint: Sprint 3  
Epic: MCP-EPIC-008 Portability, Quality And Release  

## Doel

MCP-US-080 is 'n P0-isolasiestory vir die Logic Pro latency-impediment. Die story toets USB-MIDI routing en event timing sonder D1-core, synthio audio graph, `I2SOut.play()` of hoorbare tone.

Die vraag wat hierdie story moet beantwoord:

> Kom Logic/CoreMIDI NoteOn events laat by die S2 aan, of kom dit onmiddellik aan en ontstaan die hoorbare vertraging eers in die audio-pad?

## Wat v0.20.0 byvoeg

- `midi_chip_platform.midi_routing_diagnostic.MidiRoutingDiagnosticRuntime`
- `MIDI_ROUTING_DIAGNOSTIC_ENABLED`
- multi-port USB-MIDI scan via die bestaande `CircuitPythonUsbMidiFactory`
- serial markers:
  - `MIDI_ROUTING_DIAGNOSTIC_STATUS=START`
  - `MIDI_ROUTING_DIAGNOSTIC_INPUT_STATUS=OPEN`
  - `MIDI_ROUTING_DIAGNOSTIC_READY`
  - `MIDI_ROUTING_EVENT=...;event_ms=...`
  - `MIDI_ROUTING_HEARTBEAT`
  - finale `PASS`, `TIMEOUT`, `INTERRUPTED` of `FAIL`

## Nie Deel Van Hierdie Story Nie

- Geen boot-audition.
- Geen hoorbare audio.
- Geen D1-core rendering.
- Geen synthio note press/release.
- Geen latency-fix in die audio-pad.

## HIL-Acceptasietoets

1. Deploy v0.20.0 na `CIRCUITPY`.
2. Stel in `settings.toml`:

```toml
MIDI_ROUTING_DIAGNOSTIC_ENABLED = "true"
MIDI_ROUTING_DIAGNOSTIC_SCAN_ALL_PORTS = "true"
MIDI_ROUTING_DIAGNOSTIC_MAX_EVENTS = 32
MIDI_ROUTING_DIAGNOSTIC_TIMEOUT_SECONDS = "120.0"
MIDI_ROUTING_DIAGNOSTIC_IDLE_SLEEP_SECONDS = "0.001"
MIDI_ROUTING_DIAGNOSTIC_EVENT_LOGGING = "summary"
MIDI_ROUTING_DIAGNOSTIC_HEARTBEAT_SECONDS = "2.0"

MIDI_DIAGNOSTIC_ENABLED = "false"
SYNTHIO_BASELINE_ENABLED = "false"
REALTIME_BASELINE_ENABLED = "false"
```

3. Soft restart die S2.
4. Wag vir:

```text
circuitpython-midi-chip-platform v0.20.0 | story=MCP-US-080 | release-date=2026-07-23
DEVICE_FAST_BOOT_STATUS=ENABLED
MIDI_ROUTING_DIAGNOSTIC_INPUT_STATUS=OPEN
MIDI_ROUTING_DIAGNOSTIC_READY
```

5. Speel vyf los note live in Logic Pro na die S2 external MIDI destination.
6. Speel daarna dieselfde Logic MIDI region.
7. Plak die volledige serial output in die chat.

## Interpretasie

| Waarneming | Betekenis | Volgende stap |
|---|---|---|
| `MIDI_ROUTING_EVENT` verskyn onmiddellik ná jy speel | USB-MIDI receive is waarskynlik reg; audio-pad bly verdag | Heropen MCP-US-079/US-055 audio graph, moontlik met kleiner synthio test of ander I2S strategy |
| `MIDI_ROUTING_EVENT` verskyn eers 10-12s later | Logic/CoreMIDI routing of USB endpoint selection is die primêre verdagte | Ontleed Logic external MIDI routing, port identity, duplicate endpoints en CoreMIDI queueing |
| Geen `MIDI_ROUTING_EVENT`, maar wel heartbeats | S2 runtime loop leef, maar MIDI kom nie in nie | Herhaal MCP-US-007 route test en vergelyk Logic destination met Audio MIDI Setup |
| `FAIL;reason=...` | Runtime of endpoint exception | Fix exception voor verdere audio-werk |

## Status

Hosttoetse en HIL-deploybewys is deel van v0.20.0. Menslike HIL-output op 2026-07-23 het `REG-080-001` bevestig: slegs CC7, geen `NoteOn`/`NoteOff`, en 'n foutiewe `PASS`.

Hierdie story bly `REJECTED / P0 Impediment`. Die opvolg is `MCP-US-080-INV-001 Locate First Disappearance Of NoteOn`, 'n investigation-only story wat geen fix of refactor mag uitvoer nie.
