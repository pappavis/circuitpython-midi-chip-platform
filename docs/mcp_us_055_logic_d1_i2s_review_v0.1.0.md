# MCP-US-055 macOS Logic Pro Audible D1 Acceptance Review

<!--
Bestand: mcp_us_055_logic_d1_i2s_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die eerste Logic USB-MIDI na D1-kern na I2S-integrasie.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
Actienr: MCP-ACT-055-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-055-START
-->

## Status

**P0 IMPEDIMENT / ARCHITECTURE REBASELINE REQUIRED.** Die host-implementering is groen en dependency-closed, maar `v0.17.8` het nie die menslike Logic realtime-HIL gesluit nie. Sewe HIL-pogings het gewys dat `i2s_test.py` hoorbaar is en USB-MIDI afsonderlik werk, maar die geintegreerde pad `Logic -> USB-MIDI -> D1 runtime -> I2S` is nie betroubaar menslik realtime hoorbaar nie. Die projek stop daarom met klein US-055-patches en skuif na `MCP-US-077 Realtime MIDI Audio Baseline Spike`, gedokumenteer in `docs/incidents/us_055_realtime_architecture_rebaseline_v0.1.0.md`.

## Implementering

- `CircuitPythonI2sAudioOutput` implementeer `AudioOutputPort` en doen alle CircuitPython-imports slegs tydens `open()`.
- Signed 16-bit D1-PCM bly beskikbaar vir host/core-toetse; die US-055 HIL-pad gebruik doelbewus 'n latched RawSample-toon om die reeds bewese `i2s_test.py`-klankpad te hergebruik.
- `D1UsbMidiI2sRuntime` hou MIDI, D1 en audio as instansies. Vir Logic-aanvaarding begin `NoteOn` 'n latched tone, bly MIDI pollen, en stop die toon met `NoteOff` of shutdown.
- `D1UsbMidiI2sRuntimeFactory` bou die runtime uit `settings.toml`/defaults en hergebruik `CircuitPythonUsbMidiFactory`, `D1Patch`, `D1SynthCore`, `AudioSafetyProfile` en `SafeAudioOutput`.
- `DeviceRuntimeApplication` gee die opt-in USB-MIDI diagnostic voorrang. As `MIDI_DIAGNOSTIC_ENABLED` false is, start die D1 runtime.
- Die HIL-manifest bevat nou `d1_runtime.py` en `i2s_audio.py`.

## RED/GREEN-bewys

| Fase | Bewys |
|---|---|
| RED | Nuwe tests het met `ModuleNotFoundError` gefaal vir `midi_chip_platform.i2s_audio` en `midi_chip_platform.d1_runtime` |
| GREEN | `CircuitPythonI2sAudioOutput` pinne, signed-to-unsigned conversie, stop/deinit, latched tone start/stop en D1 Note On/Off runtime slaag |
| REGRESSION | 136 pytest-toetse slaag; architecture-toetse bevestig geen globals, geen modulefunksies en geen module-level hardeware-imports |
| HIL | Wag op Product Owner: Logic External MIDI na `S2 Mini` of bordnaam, speel Note On/Off, hoor D1 en meet opsioneel `IO9` timing-marker teenoor I2S/audio |

## Menslike HIL-aanvaarding

1. Sluit Thonny en alle serial monitors voordat jy deploy.
2. Deploy die huidige release met die HIL-runner.
3. Heropen Thonny of 'n enkele serial monitor en herstart die bord.
4. Verwag aan die begin:

```text
circuitpython-midi-chip-platform v0.17.8 | story=MCP-US-055 | release-date=2026-07-16
DEVICE_FAST_BOOT_STATUS=ENABLED
D1_RUNTIME_STATUS=START;core=d1;sample_rate=16000;frames_per_block=128;max_blocks=0;minimum_note_seconds=0.05;minimum_note_velocity=64;stream_active_blocks=false;audition_tone_amplitude=8192;event_logging=none;timing_marker=IO9;master_gain=0.250
D1_MIDI_INPUT_STATUS=OPEN
D1_RUNTIME_READY;ready_ms=...
```

5. Open Logic Pro.
6. Maak 'n nuwe `MIDI -> External MIDI` track.
7. Kies die Wemos/S2 MIDI destination, tans waarskynlik `S2 Mini`. MIDI Channel mag `All` of `1` wees.
8. Speel eers ná `D1_RUNTIME_READY` 'n kort noot of 'n MIDI-region met C4/E4/G4.
9. Verwag hoorbare D1-klank deur die bestaande MAX98357A-prototipe-opstelling.
10. In default performance mode is daar doelbewus geen per-note serial output nie. Verwag hoorbare note en, indien jy die Rigol gebruik, 'n kort `IO9` pulse rondom die firmware/audio-startpad.

As jy serial-note-telemetrie nodig het, stel tydelik `D1_EVENT_LOGGING = "summary"` in `settings.toml` en herstart. Dan verskyn `D1_REALTIME_MIDI_NOTE=...note_latency_ms=...`. In `verbose` diagnose mode verskyn daar ook `D1_MIDI_EVENT` en `D1_AUDIO_EVENT` reëls. Skakel daarna terug na `none` vir performance.

11. Stop die runtime met `Ctrl-C`. `D1_RUNTIME_STATUS=INTERRUPTED` is aanvaarbaar vir 'n handmatige stop.

## Pass/Fail

| Uitkoms | Betekenis |
|---|---|
| Hoorbare klank uit Logic en geen serial flood | US-055 kan aanvaar word |
| `IO9` pulse maar geen klank | I2S/audio/debugpad ondersoek; herhaal eers standalone `i2s_test.py` |
| Geen `IO9` pulse by note-on | Logic/CoreMIDI routing of USB-MIDI-poort ondersoek; herhaal MCP-US-007 diagnostic of skakel `summary` logging tydelik aan |
| `summary` wys `D1_REALTIME_MIDI_NOTE` maar geen klank | D1 runtime of I2S audio-startpad ondersoek |
| Traceback in `i2s_audio.py` | I2S pins/backend of `audiocore.RawSample` conversie ondersoek |

## Beperkings

- Hierdie eerste MVP-pad is monofonies.
- Pitch bend, CC1-vibrato, polifonie en SN76489 bly post-MVP nadat die D1/Logic-pad gesluit is.
- Die Product Owner se tijdelijke TRS-koptelefoonlas bly 'n prototipe-uitzondering; US-076 is nodig voor enige produksie/headphone/line-out claim.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Hou die MVP beperk tot Logic USB-MIDI na hoorbare D1 op die verwysingsbord. |
| Scrum Master | Voorkom SN76489, web, pitch bend en fisiese chip-sidequests voor US-055 closure. |
| Business Analyst | Vertaal hoorbare Logic-gebruik na 'n toetsbare HIL-prosedure. |
| Chief Enterprise Architect | Behou poorte en instansie-eienaarskap as solution boundary. |
| Framework Engineer | Verifieer traceability, manifest closure en no-globals-regels. |
| Solution Architect | Voeg die kleinste composition-root by in plaas van 'n nuwe framework. |
| Embedded Engineer | Hou CircuitPython imports lazy en pins uit config/defaults. |
| MIDI Engineer | Hergebruik die bestaande USB-MIDI translator en note semantics. |
| DSP/Chip Engineer | Hergebruik D1 PCM-blokke en veilige output-gain. |
| QA/HIL Engineer | Lewer RED/GREEN, 135 regressietoetse en menslike HIL-instructies. |
| Release/Documentation | Berei `v0.17.8` performance-hertoets as In Review voor en hou US-057 vir finale release/burn-in. |
| External Architecture Reviewer (Copilot) | Die vertical-slice aanbeveling USB-MIDI -> D1 -> audio is nou geimplementeer. |
| Devil's Advocate | Waarsku dat hostgroen nog nie hoorbare Logic-aanvaarding is nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
