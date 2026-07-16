# Snelbegin: installasie en ontwikkelomgewing

<!--
Bestand: quickstart_installation_v0.1.0.md
Versienommer: 0.14.0
Doel: Beginnerstappe vir installasie, US-055 Logic-toets, diagnose en ontwikkeling sonder IDE-afhanklikheid.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-005, MCP-US-055, MCP-US-075 en MCP-US-076
Actienr: MCP-ACT-055-HIL-READY-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-055-START
-->

## Wat hierdie weergawe doen

Hierdie weergawe bevat die host-skelet, USB-MIDI-bootprofiel, capability discovery, veilige konfigurasiegrens, draagbare events, USB/BLE-vervoergrense, kanaalroetering, note-off-semantiek, per-kanaal pitch bend/CC1-toestand, 'n draagbare D1-basiskern, 'n hoorbare lae-volume I2S-diagnose en die eerste Logic/USB-MIDI na D1 na I2S runtime. Hosttoetse bewys die klasse; `hil-deploy` kopieer 'n dependency-geslote manifest en `hil-verify` bewys verbinding, libraries, boot, clean imports en uitvoering op die bord.

## Wat jy nodig het

Installeer eers:

1. [Git](https://git-scm.com/downloads).
2. [Python 3.11 of nuwer](https://www.python.org/downloads/). Merk op Windows die opsie **Add Python to PATH** tydens installasie.
3. Opsioneel: [VS Code](https://code.visualstudio.com/) of [Thonny](https://thonny.org/). Geen IDE is verpligtend nie.

Maak daarna Terminal op macOS/Linux/Raspberry Pi, of PowerShell op Windows, oop.

## 1. Kry die projek

```bash
git clone https://github.com/pappavis/circuitpython-midi-chip-platform.git
cd circuitpython-midi-chip-platform
```

## 2. Skep 'n afsonderlike Python-omgewing

macOS, Linux en Raspberry Pi:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

Die prompt behoort nou `(.venv)` te wys. Hierdie omgewing hou projekpakkette weg van jou stelsel-Python.

Bevestig nou dat die aktiewe interpreter werklik uit `.venv` kom en Python 3.11 of nuwer is:

```bash
python -c "import sys; print(sys.executable); print(sys.version)"
```

Op Windows PowerShell gebruik jy dieselfde opdrag nadat `.venv` geaktiveer is. Stop indien die pad `/usr/bin/python` toon of die weergawe met `2.7` begin; aktiveer `.venv` weer. 'n Absolute ontwikkelaarspad hoort nooit in projekconfig of startupkode nie.

## 3. Installeer die projek en toetsgereedskap

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev,hil]"
```

## 4. Voer diagnose en toetse uit

```bash
python -m midi_chip_platform diagnose
python -m pytest
```

Die diagnose behoort onder meer te wys:

```text
circuitpython-midi-chip-platform v0.12.3 | story=MCP-US-005 | release-date=2026-07-16
circuitpython-midi-chip-platform: host skeleton ready
hardware access: disabled
runtime state: class instances only
```

Die toetsuitvoer behoort met `passed` te eindig. Hosttoetse alleen bewys nie die fisiese bord nie.

## Toets die draagbare MIDI-eventmodel

Hierdie toets benodig geen MIDI-keyboard, DAW of CircuitPython-bord nie:

```bash
python -m midi_chip_platform events-diagnose
python -m pytest -q tests/test_domain_events.py
```

Verwag `EVENT_MODEL_STATUS=PASS`, gevolg deur een note-, control-, pitch-bend- en clockreël. Die pytest-opdrag moet met `passed` eindig. Dit bewys die interne model, nie fisiese USB-MIDI-ontvangs nie.

## Toets BLE-gating en performance-controls op die host

Hierdie opdragte begin geen BLE-radio en maak geen klank nie:

```bash
python -m midi_chip_platform ble-diagnose --board-id lolin_s2_mini
python -m midi_chip_platform performance-diagnose --channel 4 --pitch-bend 12288 --modulation 127 --pitch-bend-range 2
```

Die eerste opdrag eindig doelbewus met statuskode `1` en rapporteer `board_has_no_native_ble`; dit is die korrekte veilige gedrag vir die ESP32-S2. Die tweede rapporteer `MIDI_PERFORMANCE_STATUS=PASS`, `PITCH_BEND_SEMITONES=1.000000` en `CC1_NORMALIZED=1.000000`.

## Private CircuitPython-instellings

CircuitPython lees omgewingswaardes uit `settings.toml` in die wortel van `CIRCUITPY`. Die repository se `device/settings.toml.example` bevat slegs plekhouers.

1. Maak 'n kopie met die naam `settings.toml` in die `CIRCUITPY`-wortel.
2. Vervang slegs die plekhouers wat jy benodig.
3. Moenie jou voltooide `settings.toml` na Git kopieer of commit nie.
4. Die synth rapporteer slegs of 'n private waarde `SET` of `UNSET` is.
5. 'n Leë waarde of een wat net uit spasies bestaan, word as `UNSET` behandel; gebruik aanhalingstekens vir doelbewus leë strings, byvoorbeeld `WIFI_SSID = ""`.

Prioriteit: toekomstige runtime-/commandline-overrides wen eerste, daarna `settings.toml`, daarna publieke verstekke. `settings.toml` skei geheime van bronkode maar enkripteer dit nie.

## MCP-US-003 toestelfirmware

Die repository hou deploybare lêers in `device/`. Werk steeds in die repository en nooit direk op CIRCUITPY as jou enigste bronkopie nie.

Die goedgekeurde HIL-proses:

1. Ontdek CIRCUITPY en die USB-seriële poort.
2. Maak Thonny/Serial Monitor toe sodat net een client die poort besit.
3. Neem 'n private herstelkopie buite die repository.
4. Installeer die verklaarde CircuitPython-biblioteke met CircUp.
5. Gebruik `hil-deploy` om die 16 dependency-geslote projeklêers te kopieer.
6. Wag totdat writes klaar is en voer 'n harde reset/power cycle uit sodat `boot.py` weer loop.
7. Kontroleer `boot_out.txt`, USB-MIDI-enumerasie en die runtimebanner.

Moenie 'n voorbeeldpad blind op 'n ander rekenaar gebruik nie.

## MCP-US-051 HIL-verifikasie

Maak eers Thonny, Serial Monitor en enige ander REPL-kliënt toe. Ontdek daarna die werklike volume en serial-poort vir jou rekenaar.

macOS:

```bash
ls /Volumes
ls /dev/cu.usbmodem*
```

Linux/Raspberry Pi:

```bash
ls /media/$USER
ls /dev/ttyACM*
```

Windows PowerShell:

```powershell
Get-Volume
[System.IO.Ports.SerialPort]::GetPortNames()
```

Vervang `<CIRCUITPY-PAD>` en `<SERIAL-POORT>` met die ontdekte waardes:

```bash
python -m pip install circup
circup --path <CIRCUITPY-PAD> install -r device/requirements.txt
python -m midi_chip_platform hil-deploy --source-root . --device-root <CIRCUITPY-PAD> --serial-port <SERIAL-POORT>
python -m midi_chip_platform hil-reset --serial-port <SERIAL-POORT>
python -m midi_chip_platform hil-verify --source-root . --device-root <CIRCUITPY-PAD> --serial-port <SERIAL-POORT>
```

CircUp installeer `adafruit_midi` uit `device/requirements.txt`; sien die amptelike [CircUp-dokumentasie](https://docs.circuitpython.org/projects/circup/en/latest/) en [Adafruit MIDI-dokumentasie](https://docs.circuitpython.org/projects/midi/en/latest/). Geen plaaslike volume-, toestel- of virtualenv-pad is in die kode vasgeskryf nie.

`hil-deploy` hou dieselfde serial-sessie oop om CircuitPython auto-reload tydelik af te skakel en herstel dit ook wanneer 'n kopiefout plaasvind. `hil-reset` voer daarna 'n harde boot uit sodat `boot.py` en `boot_out.txt` by die nuwe release pas.

Sukses wys `HIL_DEPLOY_STATUS=PASS;files=16`, `HIL_RESET_STATUS=REQUESTED`, gevolg deur PASS-reëls vir connection, manifest-closure, deployment, device-libraries, boot en execution, plus `private-identifiers: REDACTED`. Execution vereis `DEVICE_IMPORT_STATUS=PASS` voordat die runtime READY is. Die klankmetingsdeel van MCP-US-051 word eers bygevoeg nadat US-015/016 die fisiese PWM/MAX98357-pad lewer.

## VS Code

1. Installeer VS Code en die amptelike Microsoft **Python**-uitbreiding.
2. Kies **File > Open Folder** en open die gekloonde projeklêergids.
3. Druk `Cmd+Shift+P` op macOS of `Ctrl+Shift+P` op Windows/Linux.
4. Kies **Python: Select Interpreter** en kies die Python binne `.venv`.
5. Open **Run and Debug** en kies **MCP: Diagnose Host Skeleton**, of kies **Terminal > Run Task > MCP: Run Tests**.

Die `.vscode`-lêers verskaf gerieflike knoppies, maar roep presies dieselfde Python-opdragte as die command line aan. Die kode bevat geen VS Code-afhanklikheid nie.

## Thonny

Vir die huidige host-skelet:

1. Kies **Tools > Options > Interpreter**.
2. Kies 'n plaaslike Python 3.11+ interpreter. Indien jou Thonny-weergawe dit ondersteun, kies die `.venv`-interpreter.
3. Gebruik **View > System shell** en voer die diagnose- en toetsopdragte hierbo uit.

Vir die huidige CircuitPython-bord:

1. Kies **CircuitPython (generic)** as interpreter.
2. Kies die bord se huidige USB-seriële poort; moenie 'n poortnaam as universeel aanvaar nie.
3. Gebruik REPL om bordstatus te lees, maar maak Thonny toe voordat `hil-verify` die poort gebruik.

Thonny is dus 'n opsionele redigeerder en REPL-kliënt, nie 'n runtime-afhanklikheid nie.

## Slegs command line

Dieselfde projek werk sonder VS Code of Thonny op macOS, Windows, Linux en Raspberry Pi:

```bash
python -m midi_chip_platform diagnose
python -m pytest -q
```

Later kan 'n bord se seriële poort met bedryfstelselgereedskap ontdek word:

- macOS: `ls /dev/cu.usbmodem*`
- Linux/Raspberry Pi: `ls /dev/ttyACM*`
- Windows PowerShell: `[System.IO.Ports.SerialPort]::GetPortNames()`

Die werklike naam verskil per rekenaar, kabel, bord en aansluitvolgorde.

## Probleemoplossing

**`No module named midi_chip_platform`**

Maak seker dat jy in die projek se hooflêergids is, dat `(.venv)` sigbaar is en dat `python -m pip install -e ".[dev,hil]"` suksesvol voltooi het.

**PowerShell weier om `Activate.ps1` uit te voer**

Gebruik vir die huidige sessie:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Aktiveer daarna weer `.\.venv\Scripts\Activate.ps1`.

**VS Code gebruik die verkeerde Python**

Voer **Python: Select Interpreter** weer uit en kies `.venv`. Open daarna 'n nuwe ingeboude terminal.

**Thonny sien nie die bord nie**

Kontroleer dat CircuitPython gemonteer is, probeer 'n data-geskikte USB-kabel en kies die poort opnieuw. Geen UF2-flash of skyfuitvee is deel van hierdie story nie.

**`CIRCUITPY` is leesalleen**

Maak Thonny en serial monitors toe, ontkoppel USB, wag vyf sekondes en koppel weer sonder BOOT. Toets daarna met 'n nuwe onskadelike tekslêer. Indien dit steeds leesalleen is, stop: moenie formatteer, `storage.erase_filesystem()` gebruik of concurrent-write-beskerming afskakel nie. Deel die mount- en `boot_out.txt`-resultaat vir 'n beheerde herstelplan.

**`device-libraries: FAIL - missing: adafruit_midi`**

Maak seker dat die bord as `CIRCUITPY` gemonteer is en voer weer uit:

```bash
circup --path <CIRCUITPY-PAD> install -r device/requirements.txt
```

Moenie 'n host-Python `pip install adafruit-circuitpython-midi` as bewys gebruik nie; die library moet op die CircuitPython-volume se `lib/`-pad wees.

**`execution: FAIL` ná 'n suksesvolle deploy**

Maak Thonny en ander serial-kliënte toe, power-cycle die bord en voer `hil-verify` weer uit. Indien `DEVICE_IMPORT_STATUS=PASS` ontbreek, deel die gesaniteerde traceback; moenie READY handmatig byvoeg om die hek te omseil nie.

## Opsionele plaaslike Ollama

Ollama is nie nodig vir installasie, toetse, firmware of uitvoering nie. Dit mag later slegs vir 'n goedgekeurde klein ontwikkeltaak gebruik word. Voor gebruik moet die model met `ollama list` bevestig en met 'n klein tydbegrensde proef getoets word. Die verstek bly `default`; indien die Mac stadig word, stop die plaaslike model en gebruik die verstek-Codex/LLM-pad.

## Device Connection Proof

Lees [Device Connection Proof](device_connection_proof_v0.1.0.md). Dit onderskei:

- verbinding met 'n CircuitPython-bord;
- deploy van die bedoelde commit/hashes;
- toesteluitvoering van die verwagte weergawe en story.

Private UID-, MAC-, SSID- en geheime-data word nooit in chat of Git geplaas nie.

## US-055 Logic Pro D1-toets

Hierdie toets is die huidige menslike acceptatiehek. Gebruik net een serial tool op 'n slag: Thonny of `screen`, nie albei nie.

1. Maak Thonny en serial monitors toe.
2. Deploy die huidige firmware:

```bash
python -m midi_chip_platform hil-deploy \
  --source-root . \
  --device-root /Volumes/CIRCUITPY \
  --serial-port <jou-/dev/cu.usbmodem...-poort>
```

3. Herstart die bord of gebruik `hil-reset`.
4. Open Thonny REPL of 'n enkele serial monitor.
5. Verwag:

```text
circuitpython-midi-chip-platform v0.17.8 | story=MCP-US-055 | release-date=2026-07-16
DEVICE_FAST_BOOT_STATUS=ENABLED
D1_RUNTIME_STATUS=START;core=d1;sample_rate=16000;frames_per_block=128;max_blocks=0;minimum_note_seconds=0.05;minimum_note_velocity=64;stream_active_blocks=false;audition_tone_amplitude=8192;event_logging=none;timing_marker=IO9;master_gain=0.250
D1_MIDI_INPUT_STATUS=OPEN
D1_RUNTIME_READY;ready_ms=...
```

6. Open Logic Pro.
7. Maak `MIDI -> External MIDI`.
8. Kies die CircuitPython/Wemos bestemming, tans waarskynlik `S2 Mini`.
9. Kies MIDI Channel `All` of `1`.
10. Speel 'n noot of kort MIDI-region.

PASS:

Jy hoor D1-klank deur die MAX98357A-prototipe-opstelling. In default performance mode verskyn daar geen per-note serial output nie.

Opsioneel: meet `IO9` met die Rigol. Elke note-on gee 'n kort marker-pulse rondom die firmware/audio-startpad. `D1_REALTIME_MIDI_NOTE` verskyn net wanneer jy tydelik `D1_EVENT_LOGGING = "summary"` stel. `D1_MIDI_EVENT` en `D1_AUDIO_EVENT` verskyn net met `verbose`.

Stop met `Ctrl-C`. `D1_RUNTIME_STATUS=INTERRUPTED` is normaal wanneer jy self stop.

## Huidige pausepunt

MCP-US-005, MCP-US-007, MCP-US-008, MCP-US-009, MCP-US-014, MCP-US-016, MCP-US-063 en MCP-US-075 is Done. US-075 is met 'n eksplisiete prototipe-lasuitondering aanvaar; US-076 parkeer die gesertifiseerde hardware-cleanup. US-055 is In Review: hosttoetse is groen en die Product Owner moet nou Logic/USB-MIDI-na-hoorbare-D1/I2S op die bord toets. Die v0.17.8 hertest moet `master_gain=0.250`, `minimum_note_velocity=64`, `D1_MIDI_INPUT_STATUS=OPEN`, `event_logging=none` en `timing_marker=IO9` wys; die I2S-adapter gebruik 'n korter latched RawSample-tone sonder per-note serial backpressure.

## MAX98357A veilige toetslas

- Ontkoppel 'n direk-gekoppelde koptelefoon en moenie dit op jou ore sit tydens synthontwikkeling nie.
- Gebruik vir die MAX98357A 'n bewegende-spoel-luidspreker van 4-8 ohm met geskikte kraggradering, direk tussen `+` en `-`.
- Verbind geen uitsetterminaal aan grond, Scarlett/line-in, 'n tweede versterker of 'n geaarde scope-klem nie.
- Plaas geen gewone enkelpotmeter in of oor die bridge-tied speakeruitset nie.
- US-075 spesifiseer lae digitale master gain, startup mute en die GAIN/SD-penprofiel. 'n Toekomstige koptelefoon- of pedal-line-out gebruik 'n geskikte DAC/headphone-amp-pad.

Toets die sagtewaregrens sonder hardeware:

```bash
/Volumes/data1/michiele/venv/venv3.12/bin/python \
  -m midi_chip_platform audio-safety-diagnose \
  --master-gain 0.08 --input-peak 12000
```

`AUDIO_SAFETY_MUTED_PEAK=0`, `AUDIO_SAFETY_UNMUTED_PEAK=960` en `AUDIO_SAFETY_STATUS=PASS` bewys die digitale grens. Dit bewys nog nie die fisiese luidspreker nie.
