# US-055 Realtime Failure Copilot Review Packet

<!--
Bestand: us_055_realtime_failure_copilot_packet_v0.1.0.md
Versienommer: 0.1.0
Doel: Gee 'n eksterne reviewer 'n gefokusde pakket vir die US-055 realtime MIDI-na-audio blokker.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
Actienr: MCP-ACT-055-REVIEW-PACKET-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-REALTIME-IMPEDIMENT
-->

## Review-opdrag

Neem die rol aan van 'n onafhanklike embedded audio/MIDI architect reviewer. Hierdie pakket vra nie vir kosmetiese code review nie. Die doel is om die P0-blokker te diagnoseer wat die MVP blokkeer:

> Logic Pro stuur USB-MIDI na die Wemos S2 Mini. Die firmware ontvang soms MIDI en kan losstaande I2S-klank speel, maar die D1-runtime speel nie betroubaar en hoorbaar realtime saam met Logic nie.

Gee asseblief 'n kritiese antwoord met:

1. Waarskynlikste root cause(s).
2. Of die huidige `RawSample`/`I2SOut.play()` start/stop-benadering geskik is vir realtime synth-gebruik.
3. Of die volgende stap 'n minimale baseline spike, `synthio`, of 'n groter runtime-refactor moet wees.
4. Watter files/classes eerste verander moet word.
5. Watter HIL-test die Product Owner moet doen om te bewys dat die fix werklik werk.

## Projectcontext

| Item | Waarde |
|---|---|
| Repo | `pappavis/circuitpython-midi-chip-platform` |
| Lokale repo | `/Volumes/data1/Yandex.Disk.localized/michiele/Programmering/Python/python_normaal/github_python_normaal/circuitpython-midi-chip-platform-governance` |
| Board | Lolin/Wemos S2 Mini, ESP32-S2, CircuitPython 10.0.3 |
| Audio | MAX98357A mono I2S |
| Pins | `IO5=BCLK`, `IO3=WS/LRC`, `IO7=DIN/SD` |
| MIDI source | Logic Pro External MIDI destination `S2 Mini` |
| MVP core | D1-basiskern, monofonies, hoorbaar via I2S |
| Traceability | `CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-055` |
| Hard rule | Geen globale runtime-variables; class-based composition only |

## MVP-faalcriterium

US-055 is pas klaar wanneer:

- Logic Pro die S2 Mini as External MIDI destination kan kies.
- 'n MIDI region of live MIDI note binne menslik realtime hoorbaar uit die MAX98357A kom.
- Die runtime nie eers na 'n buffer-/timeoutagtige vertraging hoorbaar reageer nie.
- Die test met die bestaande `i2s_test.py` audio sanity check vooraf groen bly.

## Wat reeds bewezen groen is

| Area | Bewys |
|---|---|
| I2S hardware | `device/i2s_test.py` speel herhaalbaar hoorbaar G3-C4-D4 via MAX98357A |
| USB MIDI receive | MCP-US-007 het fisies `note_on`, `note_off` en `matched_notes=1` vanaf macOS/Logic/CoreMIDI ontvang |
| D1 core host | `d1-diagnose` bewys sine/saw/square PCM, A4=440 Hz, velocity, host tests groen |
| Host regression | Laaste reeks het 136 host tests groen gehad |
| Boot/config | Device start, capability/config checks pass, D1 runtime open |

Belangrik: hierdie groen bewyse is nie genoeg vir US-055 nie, want die integrasiepad `USB-MIDI -> D1 runtime -> I2S realtime audio` bly rooi.

## Wat rooi bly

Laaste HIL-test met v0.17.8:

```text
circuitpython-midi-chip-platform v0.17.8 | story=MCP-US-055 | release-date=2026-07-16
DEVICE_FAST_BOOT_STATUS=ENABLED
D1_RUNTIME_STATUS=START;core=d1;sample_rate=16000;frames_per_block=128;max_blocks=0;minimum_note_seconds=0.05;minimum_note_velocity=64;stream_active_blocks=false;audition_tone_amplitude=8192;event_logging=none;timing_marker=IO9;master_gain=0.250
D1_MIDI_INPUT_STATUS=OPEN
D1_RUNTIME_READY;ready_ms=9
```

Product Owner result:

- Logic Pro notes were not perceived as realtime.
- After several attempts, audio either came late, inconsistently, or not at all.
- `i2s_test.py` remains audible, so the MAX98357A wiring and basic I2S path are not the first suspect.
- The user reports this is the seventh failed US-055 HIL attempt and has declared it a critical MVP blocker.

## Timeline van relevante fixes

| Commit | Titel | Intent | Result |
|---|---|---|---|
| `5e77dd8` | make Logic MIDI notes audibly buffered | Try audible buffered note path | Not acceptable realtime |
| `e028a24` | stop idle i2s silence while polling midi | Avoid continuous silent I2S while waiting | Not enough |
| `cf3fd10` | raise d1 audition output for Logic hil | Raise output audibility | Still unreliable |
| `e2f0f4e` | use timed i2s playback for d1 audio | Timed playback | Still not realtime |
| `9d8a65c` | latch d1 i2s tone for Logic MIDI | Latched tone approach | Some progress, not accepted |
| `7d6ff0a` | fast boot d1 runtime for realtime MIDI | Fast boot, less startup overhead | Startup fast, playback still wrong |
| `6494086` | reduce D1 latency logging for Logic | Reduce serial logging overhead | Notes logged, perceived delay remains |
| `036f362` | add D1 GPIO timing marker | Add IO9 latency marker | Did not solve audible realtime issue |

## Verdachte architectuurkeuse

The current US-055 path tries to make individual MIDI notes audible by calling an I2S `RawSample` start/stop style tone path:

- `D1UsbMidiI2sRuntime.run()` polls USB MIDI.
- On `NoteOn`, it calls `_start_minimum_audible_tone()`.
- `_start_minimum_audible_tone()` calls `audio_output.start_tone(...)` if available.
- `CircuitPythonI2sAudioOutput.start_tone()` creates a fresh `array("H", values)`, wraps it in `audiocore.RawSample`, and calls `I2SOut.play(raw_sample, loop=True)`.
- `NoteOff` schedules or performs `stop_tone()`.

This resembles the standalone `i2s_test.py` diagnostic, but it may be a bad realtime synth architecture because it repeatedly allocates/replaces RawSamples and restarts `I2SOut.play()` inside the MIDI loop.

## Relevant files for review

| File | Waarom dit saak maak |
|---|---|
| `src/midi_chip_platform/d1_runtime.py` | Main runtime loop and NoteOn/NoteOff handling |
| `src/midi_chip_platform/i2s_audio.py` | CircuitPython I2S output, RawSample start/stop, tone generation |
| `src/midi_chip_platform/d1_core.py` | Portable D1 oscillator and PCM block rendering |
| `src/midi_chip_platform/midi_usb.py` | USB MIDI input and adafruit_midi translation |
| `src/midi_chip_platform/audio.py` | Audio ports, safety wrapper, gain/mute boundaries |
| `device/i2s_test.py` | Known-good independent I2S audible diagnostic |
| `device/code.py` | Device composition root |
| `tests/test_d1_usb_midi_runtime.py` | Host-level contract tests that currently pass but do not prove HIL realtime behavior |

## Vrae aan Copilot / externe reviewer

### Architecture

1. Is `audiocore.RawSample` plus `I2SOut.play(..., loop=True)` on each NoteOn a valid realtime synth design on CircuitPython ESP32-S2?
2. Should this project switch the MVP D1 realtime path to `synthio.Synthesizer` where available?
3. If `synthio` is used, how should the project keep class-based ports and host tests without coupling all code to CircuitPython modules?
4. Is it more correct to keep `i2s_test.py` as hardware smoke only and build a separate `RealtimeMidiAudioBaseline` before reusing `D1SynthCore`?

### MIDI

5. Could `adafruit_midi.MIDI.receive()` polling plus `time.sleep(0.001)` cause missed or delayed perceived response?
6. Should the loop drain all pending MIDI messages before touching audio?
7. Are duplicate Logic events expected, and should dedupe happen before audio triggering on-device?

### Audio

8. Does repeatedly allocating `array("H", ...)` and `RawSample(...)` in NoteOn risk heap churn, delay, or audio engine instability?
9. Should the waveform buffers be precomputed and reused per note/frequency bucket?
10. Is `SafeAudioOutput` masking/muting or gain wrapping a possible cause of inconsistent audible result?
11. Should the runtime maintain a continuously playing synth engine rather than starting/stopping I2S per note?

### Hardware/platform

12. Is ESP32-S2 likely sufficient for a monophonic D1 MVP, or should we require ESP32-S3 now?
13. Is the MAX98357A plus temporary cheap TRS headphone prototype likely to confuse perceived timing tests? It does not explain missing scope changes, but please comment.
14. Is IO9 timing-marker enough, or should there be a second marker for MIDI receive vs audio play vs I2S signal?

### Test strategy

15. What is the smallest next HIL experiment that can distinguish "MIDI is late" from "audio start is late" from "audio is not audible"?
16. Should the Product Owner test with Logic only, or should we first use a host-side CoreMIDI sender with deterministic timestamps?
17. What exact PASS/FAIL serial output should the baseline spike print?

## Aanbevole volgende stap vanuit Codex

Codex proposes **not** to keep patching v0.17.8 directly. Instead:

1. Freeze US-055 as `P0 Impediment: Architecture Rebaseline Required`.
2. Add `MCP-US-077 Realtime MIDI Audio Baseline Spike`.
3. Build a new isolated device script/runtime path:
   - USB MIDI receive only.
   - Same known-good I2S pins.
   - No D1 core.
   - No `SafeAudioOutput`.
   - No config loader.
   - No per-note serial logging by default.
   - On NoteOn, play a known-good fixed G/C/D or note-frequency tone using the simplest possible audio method.
   - Optional IO marker pulses for receive and audio-start.
4. If that baseline is realtime audible, reintroduce the D1 core.
5. If that baseline is not realtime audible, stop D1 work and solve MIDI/audio primitive first.

## Gewenste reviewer-output

Please answer in this structure:

```text
1. Executive diagnosis
2. Most likely root cause ranking
3. Architecture decision: RawSample restart vs synthio vs continuous engine
4. Minimal next experiment
5. Exact files/classes to modify
6. HIL acceptance test for Product Owner
7. Risks if ignored
```

## Non-goals

- Do not expand to SN76489, SID, OPL2, web UI or BLE.
- Do not rewrite the whole framework unless the baseline proves the current abstraction prevents realtime audio.
- Do not claim MVP pass from host tests alone.
- Do not modify `python-d1-synth`; it is a separate production repo.

