# Bronregister

<!--
Bestand: source_register_v0.1.0.md
Versienommer: 0.3.0
Doel: Registreer primêre tegniese en plaaslike bronne met gebruiksgrense.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
Actienr: MCP-ACT-MTM-AMEND-SRC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
-->

## Primêre tegniese bronne

| Bron | Gebruik | Vertroue/beperking |
|---|---|---|
| [CircuitPython `usb_midi`](https://docs.circuitpython.org/en/latest/shared-bindings/usb_midi/) | USB-MIDI enable/disable, poorte, name en ESP32-S2 endpointwaarskuwing | Primêre amptelike API; firmwareweergawe moet tydens implementering bevestig word |
| [CircuitPython `supervisor`](https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/) | USB-identiteit, run reason, safe-mode-rede en runtime-status | Omitted VID/PID behou bordverstekke; USB-wysiging gebeur slegs in `boot.py` |
| [CircuitPython USB customization](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython?view=all) | Bootvolgorde, `boot_out.txt`, endpointbegroting en recovery | ESP32-S2 het 'n beperkte endpointbegroting; HIL bly verpligtend |
| [CircuitPython `audiobusio.I2SOut`](https://docs.circuitpython.org/en/stable/shared-bindings/audiobusio/) | I2S-penkontrak en sample-uitvoer | Primêre amptelike API; beskikbaarheid is bordbou-afhanklik |
| [Adafruit MAX98357 overview](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview) | Mono-I2S-versterker, sample rates, mono-meng en geen MCLK | Amptelike produkhandleiding; werklike bord/HIL bly verpligtend |
| [Adafruit MAX98357 pinouts](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts) | BCLK/LRC/DIN, bridge-tied luidsprekeruitgang, krag en gain/mode | Primêre veiligheids- en bedradingbron |
| [CircuitPython `synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/) | Eksperimentele synth, panning, envelope en bend-spike | Primêre API, maar eksplisiet eksperimenteel; nie ons enigste kernbasis nie |
| [Adafruit MIDI Library](https://docs.circuitpython.org/projects/midi/en/latest/) | Note On/Off, CC, pitch bend, clock, start/stop/continue | Amptelike biblioteek; bundelweergawe moet vasgepen word |
| [Adafruit MIDI API](https://docs.circuitpython.org/projects/midi/en/latest/api.html) | 14-bit bend, 7-bit CC en 24 PPQN timing clock | Primêre boodskapsemantiek |
| [Adafruit HTTP Server](https://docs.circuitpython.org/projects/httpserver/en/stable/) | Plaaslike HTTP, routing, WebSocket en SSE | Geheue-/sokbeperkings vereis eenkliënt-MVP |
| [HTTP server polling examples](https://docs.circuitpython.org/projects/httpserver/en/stable/examples.html) | Koöperatiewe polling en asyncio-opsies | Voorbeeld is nie ’n real-time klankwaarborg nie |
| [CircuitPython `settings.toml`](https://learn.adafruit.com/networking-in-circuitpython/network-settings) | Moderne private netwerkconfig | Geen geheime in Git nie |
| [Raspberry Pi OS documentation](https://www.raspberrypi.com/documentation/computers/os.html) | Skeiding van Linux/Python-teikens van mikrobeheerderfirmware | Pi Zero/3 kry ’n adapter, nie dieselfde firmwareclaim nie |
| [Fishman TriplePlay Support](https://fishman.com/tripleplay-support/) | USB-MIDI-kitaar, polyfonie en individuele string bends | Amptelike produkondersteuning; TriplePlay is 'n HIL-verwysing, nie 'n kodekonstante nie |
| [Fishman TriplePlay Utility User Guide](https://a11.fishman.com/wp-content/uploads/2024/12/TriplePlayUtility-UserGuide.pdf) | Trigger/Auto/Smooth/Step bend- en slide-semantiek | Amptelike handleiding; synth bend range moet konfigureerbaar en ooreenstemmend wees |
| [DOREMiDi UMH-10](https://www.doremidi.cn/h-pd-2.html) | Voorbeeld van klas-kompatibele USB-MIDI-host na 5-pen DIN | Verwysingstoestel; presiese model/controller-kombinasie vereis eie HIL |
| [RaspiMIDIHub](https://raspimidihub.com/) | Raspberry Pi USB-MIDI ontdekking en roetering sonder DAW | Eksterne projek; integrasie word as transport-HIL getoets, nie as firmware-afhanklikheid nie |

## Plaaslike en projekbronne

| Bron | Gebruik | Publikasiebeleid |
|---|---|---|
| `pappavis/python-d1-synth` | Getoetste MIDI-, voice-, pitch-, CC-, ADSR- en routingkontrakte | Verwys na openbare repo; port gedrag, nie desktop-backends nie |
| `pappavis/midi-chip-platform` | Domeindokumentasie, governance en gearchiveerde modulêre grense | Hergebruik slegs ná onafhanklike toets/portering |
| Verwysingsbord se huidige CIRCUITPY-volume | PWM/SN76489-prototipe en werklike biblioteekinventaris | Privaat rugsteun; geen geheime, UID of volledige kopie in Git nie |
| Gebruiker se Rigol DHO804 en meettoerusting | Frekwensie, duty cycle, jitter en stereokanaalbewys | Resultate word as HIL-verslag gepubliseer, nie persoonlike toesteldata nie |
| YouTube-verwysing oor ESP32/I2S | Oriëntering en praktiese demonstrasie | Sekondêre bron; argitektuurbesluite steun op amptelike API en eie metings |

## Bronreël

Dokumentasie of video bewys nie dat ’n spesifieke bordbou ’n module bevat of dat real-time klank stabiel is nie. Elke kritieke eis kry ’n runtime-vermoënscheck en, waar toepaslik, ’n ossilloskoop-/luistertoets.
