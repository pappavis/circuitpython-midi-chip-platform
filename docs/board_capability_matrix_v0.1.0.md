# Bordvermoënsmatriks

<!--
Bestand: board_capability_matrix_v0.1.0.md
Versienommer: 0.2.0
Doel: Skeiding tussen bevestigde verwysingsbord en toekomstige adapterteikens.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
Actienr: MCP-ACT-003-HIL-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003
-->

| Teiken | Runtime | USB-MIDI | Wi-Fi/web | PWM stereo | I2S | Status |
|---|---|---|---|---|---|---|
| LOLIN/Wemos ESP32-S2 Mini | CircuitPython 10.0.3 fisies ontdek | USB CDC/CIRCUITPY teenwoordig; MCP-US-003 profiel benodig finale HIL | Beskikbaar, maar verbode in `boot.py` | Bestaande prototipe bewys | Spike nodig | Primêre MVP |
| Generiese ESP32-S2 | CircuitPython | Bordprofiel-afhanklik | Gewoonlik beskikbaar | Pen/module-afhanklik | Firmware/bord-afhanklik | Later profiel |
| ESP32-S3 | CircuitPython | Tipies beskikbaar | Beskikbaar | Profiel nodig | Sterk kandidaat | Later profiel |
| RP2040-mikrobeheerder | CircuitPython | Bordafhanklik | Slegs Wi-Fi-variante/eksterne netwerk | Profiel nodig | Bordafhanklik | Later profiel |
| Raspberry Pi Zero/Zero 2/3 | Raspberry Pi OS + Python/Blinka | Linux USB/MIDI-adapter | Linux-netwerk | Nie dieselfde firmwarepad nie | Linux-driverpad | Afsonderlike adapter |

## Geen universele bordaannames

- Die runtime ontdek modules soos `usb_midi`, `pwmio`, `audiopwmio`, `audiobusio`, `synthio`, `wifi` en geheue-inligting.
- Penne kom uit ’n bordprofiel of gebruikerconfig, nooit uit ’n verborge universele konstante nie.
- ’n onbekende bord begin in diagnostiese/geen-klank-modus en druk ’n herstelbare fout.
- “CircuitPython device” beteken hier mikrobeheerderfirmware; Raspberry Pi Linux-rekenaars gebruik ’n verenigbare host-adapter, nie dieselfde `code.py`-beeld nie.
