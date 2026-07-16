# MCP-US-075 Safe Development Audio Load And Volume Gate Review

<!--
Bestand: mcp_us_075_safe_audio_gate_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die master-gain, startup-mute, hoorbare HIL en Product Owner-prototipe-lasuitondering.
Sprint: Sprint 3
Epic: MCP-EPIC-007 DSP And Pedal Hardware
User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
Actienr: MCP-ACT-075-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START
-->

## Status

**DONE WITH PRODUCT OWNER EXCEPTION.** Die klasgebaseerde veilige-audiokontrak, konfigurasie, lae-volume standalone diagnostiek, hostbewys en hoorbare v0.16.0 HIL is groen. Die Product Owner het op 2026-07-16 bevestig dat G3-C4-D4 hoorbaar was met die bestaande goedkoop TRS-koptelefoon en het die prototipe-lasrisiko voorlopig aanvaar. Hierdie closure sertifiseer slegs die software gain/startup-mute en hoorbare ontwikkelpad; dit sertifiseer nie die direkte BTL-koptelefoonlas as elektries veilig nie. MCP-US-076 parkeer die korrekte speaker/headphone/pedal-uitset-argitektuur ná MVP.

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

Die impediment is tegnies opgelos. Die menslike hertoets het daarna die v0.16.0 US-075-markers, G3-C4-D4, stabiele heap en finale `PASS` getoon.

## Product Owner-uitondering en aanvaarding

Die fisiese toets het nog die bestaande goedkoop TRS-koptelefoon gebruik. Die Product Owner aanvaar hierdie prototiperisiko en het gevra dat die strenger elektriese cleanup eers ver ná die MVP plaasvind. Daarom:

- sluit US-075 op grond van die bewese lae-volume softwarehek en hoorbare HIL;
- bly R-013 oop as 'n aanvaarde prototiperisiko;
- begin US-055 volgens die bindende D1/Logic-volgorde;
- vereis MCP-US-076 voor enige produksie-, draagbare, headphone-, line-out- of pedal-releaseclaim.

Die aanvaarde toesteluitvoer bevat `amplitude=2048`, `startup_mute_seconds=0.25`, `gain_pin_profile=floating-9db`, `shutdown_mode=software-mute`, drie note, finale `PASS` en 'n heapverskil van 320 bytes.

## Burn-in

`N/A` vir die hostprofiel. Die kort hoorbare ontwikkel-HIL is met 'n Product Owner-lasuitondering aanvaar. Die 30-minute en 8-uur geïntegreerde USB-MIDI/D1/audio/heap-burn-in bly onderskeidelik MCP-US-051, US-055 en US-057; gesertifiseerde fisiese uitsetcleanup is MCP-US-076.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het die hoorbare v0.16.0 HIL en prototipe-lasrisiko eksplisiet aanvaar; produksieveiligheid nie gesertifiseer nie. |
| Scrum Master | Sluit US-075 met uitsondering, parkeer US-076 ná MVP en open US-055. |
| Business Analyst | Skei speaker, headphone en pedal-line-out as verskillende produkkontrakte. |
| Chief Enterprise Architect | Behou die veiligheidslaag as dekorator om vervangbare backends. |
| Solution Architect | Maak gain en mute backend-onafhanklik; fisiese SD/GAIN bly profieldata. |
| Embedded Engineer | Behou gedempte open/start/stop-volgorde en laer standalone amplitude. |
| MIDI Engineer | Not impacted; MIDI-eventkontrak verander nie. |
| DSP/Chip Engineer | Skaal PCM simmetries binne signed-16 en 'n harde gain-plafon. |
| Hardware/PCB Engineer | Spesifiseer speaker-only BTL-toets; latere US-047/048 dek breadboard en KiCad. |
| QA/HIL Engineer | Lewer RED/GREEN/CLI-bewys en blokkeer onveilige menslike HIL. |
| Release/Documentation | Behou v0.16.0-bewys, dokumenteer die uitsondering en merk die story Done. |
| External Architecture Reviewer | Primêre vendorveiligheidsgrense bly gesaghebbend. |
| Devil's Advocate | Risiko-aanvaarding is nie 'n vervanging vir 'n veilige toetslas nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
