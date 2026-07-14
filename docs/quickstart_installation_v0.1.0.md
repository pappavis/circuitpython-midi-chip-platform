# Snelbegin: installasie en ontwikkelomgewing

<!--
Bestand: quickstart_installation_v0.1.0.md
Versienommer: 0.2.0
Doel: Beginnerstappe vir installasie, diagnose en ontwikkeling sonder IDE-afhanklikheid.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: AUDIO-PRIORITY-AMENDMENT-001
Actienr: MCP-ACT-AUDIO-AMEND-DOC-002
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001
-->

## Wat hierdie weergawe doen

Hierdie weergawe is 'n host-skelet wat die argitektuur en toetse op 'n gewone rekenaar uitvoer. Dit skryf nog niks na 'n CircuitPython-bord nie en maak nog geen klank nie. Die diagnose hieronder bevestig dat Python, die pakket en die veilige klasgebaseerde fondasie korrek werk.

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
python -m pip install -e ".[dev]"
```

## 4. Voer diagnose en toetse uit

```bash
python -m midi_chip_platform diagnose
python -m pytest
```

Die diagnose behoort onder meer te wys:

```text
circuitpython-midi-chip-platform v0.1.1 | story=AUDIO-PRIORITY-AMENDMENT-001 | release-date=2026-07-14
circuitpython-midi-chip-platform: host skeleton ready
hardware access: disabled
runtime state: class instances only
```

Die toetsuitvoer behoort met `passed` te eindig. Jy hoef nie 'n ESP32 of MIDI-toestel vir hierdie story te koppel nie.

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

Vir 'n CircuitPython-bord in 'n latere story:

1. Kies **CircuitPython (generic)** as interpreter.
2. Kies die bord se huidige USB-seriële poort; moenie 'n poortnaam as universeel aanvaar nie.
3. Gebruik REPL om bordstatus te lees. MCP-US-002 ontplooi nog geen `boot.py` of `code.py` nie.

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

Maak seker dat jy in die projek se hooflêergids is, dat `(.venv)` sigbaar is en dat `python -m pip install -e ".[dev]"` suksesvol voltooi het.

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

## Volgende logiese story

Na menslike aanvaarding van MCP-US-002 is die geordende volgende story **MCP-US-003: Minimal Safe Boot And USB Profile**. Dit sal 'n afsonderlike plan en goedkeuring vereis voordat enige toestel-I/O begin.
