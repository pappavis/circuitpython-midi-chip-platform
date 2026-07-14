# Bordvermoënsmatriks

<!--
Bestand: board_capability_matrix_v0.1.0.md
Versienommer: 0.6.0
Doel: Skeiding tussen bevestigde verwysingsbord en toekomstige adapterteikens.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-004 Board Capability Discovery
Actienr: MCP-ACT-004-CAP-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004
-->

| Teiken | Runtime | USB-MIDI | BLE-MIDI | Wi-Fi/web | PWM stereo | I2S | Status |
|---|---|---|---|---|---|---|---|
| LOLIN/Wemos ESP32-S2 Mini | CircuitPython 10.0.3 fisies bewys | MCP-US-003 USB CDC, CIRCUITPY, AudioControl, MIDIStreaming, PortIn en PortOut bewys | Nie native ondersteun nie; veilige negatiewe capability-toets | `wifi:yes`; runtime-fallback-HIL nog nodig; verbode in `boot.py` | `audiopwmio:no` in huidige bou; aparte fallbackbesluit nodig | `audiobusio:yes`; IO5 BCLK, IO3 WS, IO7 DATA/DIN en manifest-HIL fisies bevestig | Primêre MVP; US-004 Done |
| Generiese ESP32-S2 | CircuitPython | Bordprofiel-afhanklik | Nie native ondersteun nie | Station/AP capability- en firmwarebou-afhanklik | Pen/module-afhanklik | Firmware/bord-afhanklik | Later profiel |
| ESP32-S3 | CircuitPython | Tipies beskikbaar | Native `_bleio`-kandidaat; BLE-MIDI-HIL nodig | Beskikbaar | Profiel nodig | Sterk kandidaat | Tweede MVP-kandidaat |
| RP2040-mikrobeheerder | CircuitPython | Bordafhanklik | Slegs BLE-bord/eksterne coprocessor indien amptelik ondersteun | Slegs Wi-Fi-variante/eksterne netwerk | Profiel nodig | Bordafhanklik | Later profiel |
| Raspberry Pi Zero/Zero 2/3 | Raspberry Pi OS + Python/Blinka | Linux USB/MIDI-adapter | Linux BLE-adapterpad, nie dieselfde firmware nie | Linux-netwerk | Nie dieselfde firmwarepad nie | Linux-driverpad | Afsonderlike adapter |

## Geen universele bordaannames

- Die runtime ontdek modules soos `usb_midi`, `pwmio`, `audiopwmio`, `audiobusio`, `synthio`, `wifi` en geheue-inligting.
- Penne kom uit ’n bordprofiel of gebruikerconfig, nooit uit ’n verborge universele konstante nie.
- ’n onbekende bord begin in diagnostiese/geen-klank-modus en druk ’n herstelbare fout.
- “CircuitPython device” beteken hier mikrobeheerderfirmware; Raspberry Pi Linux-rekenaars gebruik ’n verenigbare host-adapter, nie dieselfde `code.py`-beeld nie.
- ’n Sigbare `ESP_*`-SSID bewys nie bordidentiteit nie; bevestig dit met ’n beheerde power-cycle of eksplisiete toestel-/REPL-log voordat dit vir toetsing gebruik word.
- Station- en AP-IP’s word tydens runtime ontdek en gesanitiseerd gerapporteer; geen IP, SSID, credential of kliënt-MAC word ’n kodekonstante nie.
- `IO7 -> DATA` beteken die MAX98357A se `DIN`/`SDIN`. Dit beteken nooit die aparte `SD/MODE` shutdown-/kanaalseleksiepen nie.
