# MCP-US-079 Persistent Synthio Audio Graph Spike Plan

<!--
Bestand: mcp_us_079_persistent_synthio_audio_graph_plan_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer die P0-plan om realtime MIDI-klank met 'n permanente synthio audio graph te bewys.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-079 Persistent Synthio Audio Graph Spike
Actienr: MCP-ACT-079-PLAN-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-078-ARCH-REVIEW-001
-->

## Probleemstelling

MCP-US-077/078 bewys drie dinge:

1. I2S en MAX98357 werk onmiddellik (`i2s_test.py` en boot-audition).
2. Logic USB-MIDI NoteOn bereik die S2 met `latency_ms=0-4`.
3. Hoorbare NoteOn-klank is nog ongeveer 20 sekondes laat.

Die fout sit dus nie primêr in MIDI receive of bedrading nie. Die huidige audio-runtime primitive is verkeerd vir performance: per-event `I2SOut.play()` en later `I2SOut.stop()`.

## Uitvoerplan

MCP-US-079 bou 'n nuwe, klein runtime langs die bestaande baseline:

- nuwe class-based module, byvoorbeeld `src/midi_chip_platform/synthio_runtime.py`;
- nuwe factory in `device/code.py`;
- nuwe config-vlagte, byvoorbeeld `SYNTHIO_BASELINE_ENABLED`, sample rate, channel count en event logging;
- I2S word een keer oopgemaak;
- `synthio.Synthesizer` word een keer geskep;
- `audio.play(synth)` word een keer by startup geroep;
- NoteOn roep net `synth.press(note)`;
- NoteOff of korte gate roep `synth.release(note)`;
- geen `I2SOut.play()` of `I2SOut.stop()` op die MIDI hot path nie.

## Aanvaardingscriteria

- Hosttoetse bewys dat die runtime NoteOn/NoteOff state mutasies uitvoer sonder per-event audio-play. Status: `PASS`, 152 hosttoetse op 2026-07-19.
- Device startup rapporteer `SYNTHIO_BASELINE_READY`.
- Boot-audition bly aan as hoorbare selftest.
- Logic Pro External MIDI na `S2 Mini` speel 20 NoteOns hoorbaar realtime.
- Doelwit: minder as 50 ms menslik waarneembare vertraging.
- Geen 12-20 sekonde audio backlog na herhaalde NoteOns.
- NoteOff of gate stop die noot.
- Geen globale veranderlikes of modulevlak runtime-status.

## Implementasiestatus

Status: `In Review / HIL Ready`

Release: `v0.19.0`

Die implementasie voeg `src/midi_chip_platform/synthio_runtime.py` by. Die nuwe runtime word net geaktiveer wanneer `SYNTHIO_BASELINE_ENABLED = "true"` in `settings.toml` staan. Dit hou die bestaande D1-runtime onaangeraak totdat die HIL-test bewys dat `synthio` die 12-20 sekonde audio backlog oplos.

## HIL Acceptatietest

1. Deploy release `v0.19.0` na `CIRCUITPY`.
2. Sit hierdie runtime flags in `settings.toml`:

```toml
SYNTHIO_BASELINE_ENABLED = "true"
REALTIME_BASELINE_ENABLED = "false"
D1_RUNTIME_ENABLED = "true"
SYNTHIO_BASELINE_EVENT_LOGGING = "summary"
SYNTHIO_BASELINE_BOOT_AUDITION_SECONDS = "0.6"
SYNTHIO_BASELINE_GATE_SECONDS = "0.12"
```

3. Herstart die S2 Mini.
4. Verwachte startup markers:

```text
circuitpython-midi-chip-platform v0.19.0 | story=MCP-US-079 | release-date=2026-07-19
DEVICE_FAST_BOOT_STATUS=ENABLED
SYNTHIO_BASELINE_AUDIO_STATUS=OPEN
SYNTHIO_BASELINE_BOOT_AUDITION=PASS
SYNTHIO_BASELINE_MIDI_INPUT_STATUS=OPEN
SYNTHIO_BASELINE_READY
```

5. Stuur ten minste 20 NoteOns vanuit Logic Pro External MIDI na `S2 Mini`.
6. Verwacht resultaat: noten zijn hoorbaar direct/realtime, zonder 12-20 sekonde naloop.

## Risiko's

- ESP32-S2 kan `synthio` beperk hanteer; eerste spike bly monofoon en een-stemmig.
- Hoer sample rates verhoog CPU en geheuedruk; begin by 16000 of 22050 Hz.
- Dynamiese allocasie op NoteOn kan latency of garbage collection veroorsaak; preallokeer waar prakties.
- `synthio` is eksperimenteel in CircuitPython; hou fallback na 'n permanente mixer graph oop.
