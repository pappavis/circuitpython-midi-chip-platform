# Snelbegin: installasie en ontwikkelomgewing

<!--
Bestand: quickstart_installation_v0.1.0.md
Versienommer: 0.4.0
Doel: Beginnerstappe vir installasie, diagnose en ontwikkeling sonder IDE-afhanklikheid.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-051 Hardware-In-The-Loop Test Runner
Actienr: MCP-ACT-051-DOC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051
-->

## Wat hierdie weergawe doen

Hierdie weergawe bevat die host-skelet, die minimale MCP-US-003 CircuitPython USB-MIDI-bootprofiel en MCP-US-051 se eerste HIL-runner. Dit maak nog geen klank en ontvang nog geen note nie. Hosttoetse bewys die klasse; `hil-verify` bewys verbinding, deploy, boot en uitvoering op die bord.

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
circuitpython-midi-chip-platform v0.3.0 | story=MCP-US-051 | release-date=2026-07-14
circuitpython-midi-chip-platform: host skeleton ready
hardware access: disabled
runtime state: class instances only
```

Die toetsuitvoer behoort met `passed` te eindig. Hosttoetse alleen bewys nie die fisiese bord nie.

## MCP-US-003 toestelfirmware

Die repository hou deploybare lêers in `device/`. Werk steeds in die repository en nooit direk op CIRCUITPY as jou enigste bronkopie nie.

Die goedgekeurde HIL-proses:

1. Ontdek CIRCUITPY en die USB-seriële poort.
2. Maak Thonny/Serial Monitor toe sodat net een client die poort besit.
3. Neem 'n private herstelkopie buite die repository.
4. Kopieer `device/boot.py` en `device/code.py` na die CIRCUITPY-wortel.
5. Kopieer slegs die vereiste package-lêers na `CIRCUITPY/lib/midi_chip_platform/`.
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
python -m midi_chip_platform hil-verify --source-root . --device-root <CIRCUITPY-PAD> --serial-port <SERIAL-POORT>
```

Sukses wys vier PASS-reëls vir connection, deployment, boot en execution, plus `private-identifiers: REDACTED`. Die runner eggo nie die private serial-poort nie. Die klankmetingsdeel van MCP-US-051 word eers bygevoeg nadat US-015/016 die fisiese PWM/MAX98357-pad lewer.

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

## Opsionele plaaslike Ollama

Ollama is nie nodig vir installasie, toetse, firmware of uitvoering nie. Dit mag later slegs vir 'n goedgekeurde klein ontwikkeltaak gebruik word. Voor gebruik moet die model met `ollama list` bevestig en met 'n klein tydbegrensde proef getoets word. Die verstek bly `default`; indien die Mac stadig word, stop die plaaslike model en gebruik die verstek-Codex/LLM-pad.

## Device Connection Proof

Lees [Device Connection Proof](device_connection_proof_v0.1.0.md). Dit onderskei:

- verbinding met 'n CircuitPython-bord;
- deploy van die bedoelde commit/hashes;
- toesteluitvoering van die verwagte weergawe en story.

Private UID-, MAC-, SSID- en geheime-data word nooit in chat of Git geplaas nie.

## Volgende logiese story

MCP-US-003 is Done. MCP-US-051 se connection/deploy/boot/execution-runner is groen; die volledige klankmeetdeel wag op US-015/016. Die volgende normale produkstory in backlogvolgorde is **MCP-US-004: Board Capability Discovery**.
