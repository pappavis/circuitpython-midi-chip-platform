# MCP-US-051/MCP-US-007 Dependency-Closed Deployment Impediment

<!--
Bestand: mcp_us_051_mcp_us_007_dependency_closed_deployment_impediment_v0.1.0.md
Versienommer: 0.2.0
Doel: Dokumenteer die ouditbevinding, herstel, toetsbewys en fisiese aanvaardingshek.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock; MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-051 Hardware-In-The-Loop Test Runner; MCP-US-007 USB MIDI Receive Loop
Actienr: MCP-ACT-051-IMP-001-DOC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051-IMP-001
-->

## Bevinding

Die vorige HIL-runner kon bewys dat verklaarde bron- en toestellêers dieselfde SHA-256 het, maar nie dat die manifest alle interne imports bevat of dat CircuitPython se eksterne biblioteke teenwoordig en invoerbaar is nie. `configuration.py` benodig `ports.py` en `routing.py` benodig `core.py`; dié twee modules was nie in die ou deploymanifest nie. `midi_usb.py` benodig ook `adafruit_midi`, maar daar was geen toestelvereiste-manifest of runtime-importhek nie.

## Herstel

- `HilDeploymentManifest` bevat nou 16 projeklêers, insluitend `ports.py` en `core.py`.
- `DeploymentDependencyInspector` ontleed die interne importgrafiek met `ast` en weier 'n oop manifest.
- `device/requirements.txt` verklaar `adafruit_midi`; die HIL-runner kontroleer die geïnstalleerde toestelbiblioteek.
- `HardwareInLoopDeployer` kopieer slegs die goedgekeurde manifest, gebruik tydelike lêers en verwyder geen bestaande toesteldata nie.
- Die deploy-CLI skakel `supervisor.runtime.autoreload` via serial REPL tydelik af, herstel dit in `finally`, en `hil-reset` lewer 'n herhaalbare harde boot.
- `DeviceImportSmokeCheck` voer die gedeployde project- en MIDI-modules in voordat `DEVICE_EXECUTION_STATUS=READY` verskyn.
- Execution-proof vereis die releasebanner, `DEVICE_IMPORT_STATUS=PASS` en `DEVICE_EXECUTION_STATUS=READY`.
- Privaat volume- en serial-identifiseerders word nie na uitvoer of Git geskryf nie.

## RED/GREEN-bewys

| Fase | Bewys |
|---|---|
| RED-1 | Toetsversameling het op ontbrekende `CircuitPythonLibraryManifest` en `DeviceImportSmokeCheck` gefaal. |
| GREEN-1 | Manifest-closure, library-manifest en import-smoke het groen geword. |
| RED-2 | Toetsversameling het op ontbrekende `HardwareInLoopDeployer` gefaal. |
| GREEN-2 | HIL/CLI/runtime-toetse, insluitend autoreload en hard reset, het geslaag. |
| Regressie | 82 pytest-toetse en Ruff het voor commit geslaag. |

## Herhaalbare deploy

Installeer eers CircuitPython-biblioteke uit die repositorymanifest met CircUp, en deploy daarna die projekmanifest:

```bash
circup --path <CIRCUITPY-PAD> install -r device/requirements.txt
python -m midi_chip_platform hil-deploy --source-root . --device-root <CIRCUITPY-PAD> --serial-port <SERIAL-POORT>
python -m midi_chip_platform hil-reset --serial-port <SERIAL-POORT>
```

CircUp se amptelike dokumentasie beskryf requirements-gebaseerde library-installering; `adafruit_midi` moet op die CircuitPython-lêerstelsel beskikbaar wees. Sien [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/) en [Adafruit MIDI](https://docs.circuitpython.org/projects/midi/en/latest/).

## Fisiese aanvaardingshek

Die Wemos S2 het op 2026-07-15 die volgende fisiese dependency-closed HIL geslaag:

1. connection via USB CDC en CIRCUITPY;
2. 'n geslote interne importgrafiek en 16 ooreenstemmende hashes;
3. `adafruit_midi` op die toestel;
4. huidige bootbanner en `BOOT_STATUS=PASS` ná harde reset;
5. `DEVICE_IMPORT_STATUS=PASS` en `DEVICE_EXECUTION_STATUS=READY` via serial.

Die eerste skryfpoging het tydens `events.py` gestop omdat auto-reload reeds ná vroeë manifestlêers begin het. Die herstel het auto-reload onder serial beheer gebring en die volledige tweede deploy plus alle HIL-hekke het geslaag. 'n Werklike USB-MIDI Note On en Note Off deur die receive-loop bly MCP-US-007 se aparte menslike stimulus.

MCP-US-051 se latere klankprobe bly afhanklik van MCP-US-014/016. Hierdie herstel begin geen audio, Wi-Fi of synth core nie.

## Hardeware-nota

Die foto toon 'n MAX98357-klas mono-I2S-versterker. Die bestaande verwysingsbedrading bly IO3 na LRC/WS, IO5 na BCLK/SCK en IO7 na DIN/SD. PCM5102 en ander I2S-backends bly 'n latere `AudioOutput`-besluit; geen versterkertipe is in hierdie deploykode vasgeskryf nie. Die MAX98357 se luidsprekeruitsette is bruggedrewe en mag nie as grondverwysde line-out of oscilloskoop-aarde behandel word nie.

## Virtuele spanbydraes

| Rol | Bydrae |
|---|---|
| Product Owner | Het die QA-aanbeveling en herstelvolgorde aanvaar. |
| Business Analyst | Het USB-MIDI-uitvoerbaarheid van blote lêergelykheid geskei. |
| Software Architect | Het manifest-closure, library boundary en import-smoke bepaal. |
| Embedded Engineer | Het die nie-destruktiewe CIRCUITPY-deploy en bordhek begrens. |
| QA Engineer | Het RED/GREEN-, regressie- en HIL-aanvaardingsbewys gedefinieer. |
| Security/Release | Het private identifiers geredigeer en destructive deploy verbied. |
| UX/Frontend | Not impacted; geen web- of UI-gedrag verander nie. |

## Status

**Dependency impediment Done.** Dependency-closed deploy, boot en serial import/execution is fisies groen. MCP-US-007 se USB-MIDI Note On/Off-stimulus het daarna op v0.12.2 geslaag en die story is aanvaar. MCP-US-051 se latere klankprobe bly binne die audio-afhanklikheid oop.
