# MCP-US-075 Safe Development Audio Load And Volume Gate Review

<!--
Bestand: mcp_us_075_safe_audio_gate_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die veilige master-gain, startup-mute en speaker-HIL-aanvaardingshek.
Sprint: Sprint 3
Epic: MCP-EPIC-007 DSP And Pedal Hardware
User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
Actienr: MCP-ACT-075-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START
-->

## Status

**IN REVIEW.** Die klasgebaseerde veilige-audiokontrak, konfigurasie, lae-volume standalone diagnostiek en hostbewys is groen. Menslike HIL wag op 'n 4-8 ohm luidspreker; die Product Owner se aanvaarding van die direkte koptelefoonrisiko verander nie die projek se veilige toetslas of Definition of Done nie.

## Implementering

- `AudioSafetyProfile` besit `0.08` master gain, `0.25` harde plafon, startup mute en eksplisiete speaker-/GAIN-/shutdown-metadata.
- `SafeAudioOutput` dekoreer enige `AudioOutputPort`, skryf stilte voor unmute, skaal signed-16 PCM ná unmute en mute weer voor close.
- `PlatformApplication` open audio gedemp, begin kerne, unmute daarna en mute voor core shutdown.
- `ConfigurationDefaults` en `settings.toml.example` bevat draagbare veilige-audiovelde; CLI/runtime overrides bly hoër prioriteit.
- `device/i2s_test.py` bly synth-onafhanklik, begin met 0.25 s stilte en verlaag sy square-wave amplitude van 4096 na 2048.
- Die huidige fisiese profiel rapporteer eerlik `floating-9db` en `software-mute`; dit beweer nie dat 'n SD-pen of 3 dB GAIN-modifikasie reeds bedraad is nie.

## RED/GREEN-bewys

| Fase | Bewys |
|---|---|
| RED | Pytest collection faal omdat `AudioSafetyProfile` nog nie bestaan nie |
| GREEN | Startup mute, begrensde gain, lifecycle, konfigurasie, CLI en standalone I2S-profiel slaag |
| REGRESSION | 120 pytest-toetse en Ruff slaag; AST behou geen globals/modulefunksies nie |
| HOST | `AUDIO_SAFETY_MUTED_PEAK=0`, `AUDIO_SAFETY_UNMUTED_PEAK=960` en finale `PASS` |
| HIL | Wag op 4-8 ohm luidspreker en menslike G-C-D-aanvaarding |

## Hostdiagnose

```bash
/Volumes/data1/michiele/venv/venv3.12/bin/python \
  -m midi_chip_platform audio-safety-diagnose \
  --master-gain 0.08 \
  --input-peak 12000
```

Verwag:

```text
AUDIO_OUTPUT_LOAD=speaker-4-8-ohm
AUDIO_MASTER_GAIN=0.080000
AUDIO_MAXIMUM_MASTER_GAIN=0.250000
AUDIO_STARTUP_MUTED=true
AUDIO_SAFETY_MUTED_PEAK=0
AUDIO_SAFETY_UNMUTED_PEAK=960
AUDIO_SAFETY_STATUS=PASS
```

## Oorblywende menslike HIL

1. Ontkoppel die TRS-koptelefoon van die MAX98357A.
2. Verbind 'n 4-8 ohm luidspreker met gepaste wattgradering slegs tussen die versterker se `+` en `-` speakerterminale.
3. Hou BCLK=IO5, WS/LRC=IO3 en DIN=IO7; verbind geen speakerterminaal aan ground, line-in of scope-ground nie.
4. Deploy v0.16.0 en voer `i2s_test.py` uit.
5. Aanvaar slegs indien G3-C4-D4 sag maar duidelik hoorbaar is, serial `amplitude=2048`, `startup_mute_seconds=0.25`, `output_load=speaker-4-8-ohm` en finale `PASS` toon.

## Impediment MCP-US-075-HIL-IMPEDIMENT-001

Die eerste hoorbare hertoets het `v0.14.0 | story=MCP-US-016` en amplitude `4096` gerapporteer. Dit was 'n geldige US-016-regressiebewys, maar nie US-075-aanvaarding nie: die bord se `i2s_test.py` was ouer as die goedgekeurde repositoryweergawe.

Nadat Thonny gesluit is, het die beheerde herstelpad die dependency-geslote v0.16.0-manifes ontplooi, die bord hard gereset en weer geverifieer. Die finale runnerbewys was:

```text
circuitpython-midi-chip-platform v0.16.0 | story=MCP-US-075 | release-date=2026-07-16
DEVICE CONNECTION PROOF
connection: PASS - USB CDC + CIRCUITPY
manifest-closure: PASS - all internal imports are deployed
deployment: PASS - approved manifest SHA-256 pairs
device-libraries: PASS - required CircuitPython libraries present
boot: PASS - current release and USB-MIDI boot marker
execution: PASS - current release and dependency-import markers via serial REPL
private-identifiers: REDACTED
```

Die impediment is tegnies opgelos. Storyaanvaarding bly oop totdat die menslike hoorbare hertoets ook die v0.16.0 US-075-markers toon.

## Burn-in

`N/A` vir die hostprofiel. Hierdie story vereis een kort veilige speaker-HIL. Die 30-minute en 8-uur geïntegreerde USB-MIDI/D1/audio/heap-burn-in bly onderskeidelik MCP-US-051, US-055 en US-057.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het die risiko openbaar gemaak en hostimplementering goedgekeur; speaker-HIL bly oop. |
| Scrum Master | Hou US-055 geblokkeer totdat hierdie HIL aanvaar is. |
| Business Analyst | Skei speaker, headphone en pedal-line-out as verskillende produkkontrakte. |
| Chief Enterprise Architect | Behou die veiligheidslaag as dekorator om vervangbare backends. |
| Solution Architect | Maak gain en mute backend-onafhanklik; fisiese SD/GAIN bly profieldata. |
| Embedded Engineer | Behou gedempte open/start/stop-volgorde en laer standalone amplitude. |
| MIDI Engineer | Not impacted; MIDI-eventkontrak verander nie. |
| DSP/Chip Engineer | Skaal PCM simmetries binne signed-16 en 'n harde gain-plafon. |
| Hardware/PCB Engineer | Spesifiseer speaker-only BTL-toets; latere US-047/048 dek breadboard en KiCad. |
| QA/HIL Engineer | Lewer RED/GREEN/CLI-bewys en blokkeer onveilige menslike HIL. |
| Release/Documentation | Bump na v0.16.0 en merk die story eerlik In Review. |
| External Architecture Reviewer | Primêre vendorveiligheidsgrense bly gesaghebbend. |
| Devil's Advocate | Risiko-aanvaarding is nie 'n vervanging vir 'n veilige toetslas nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
