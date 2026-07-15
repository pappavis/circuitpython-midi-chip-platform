# MCP-US-005 Configuration And Secret Boundary Review

<!--
Bestand: mcp_us_005_configuration_secret_boundary_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die publieke konfigurasie, private settings-grens, toetse en HIL-hek.
Sprint: Sprint 1
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-005 Configuration And Secret Boundary
Actienr: MCP-ACT-005-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005-IN-REVIEW
-->

## Status

**IN REVIEW / HIL-HEK.** Die klasgebaseerde implementering, geheime-redaksie en host-regressie is groen. Toesteldeploy is veilig gestop omdat die fisiese `CIRCUITPY`-media leesalleen aangebied word. `diskutil verifyVolume` het geen FAT-fout gevind nie; geen reset, remount, herstel of formattering is onbewaak uitgevoer nie.

## Konfigurasieprioriteit

Van hoogste na laagste:

1. Geïnjekteerde runtime-overrides.
2. `CIRCUITPY/settings.toml`, gelees deur `os.getenv()`.
3. Publieke, klasinstansie-besitte verstekke.

Die huidige publieke klankprofiel is mono MAX98357A met IO5 BCLK, IO3 WS/LRC en IO7 DATA/DIN. Geen klank- of Wi-Fi-diens word deur hierdie story begin nie.

## Geheimegrens

- `wifi.ssid`, `wifi.password` en `web.ap.password` word as private sleutels behandel.
- Diagnostiek rapporteer slegs `SET` of `UNSET`, nooit die waarde nie.
- `public_items()` sluit private sleutels en waardes uit.
- `settings.toml` bly in `.gitignore`; `device/settings.toml.example` bevat slegs plekhouers.
- Die ou prototipewagwoord bly 'n roteeraksie vir die Product Owner voordat Wi-Fi-stories begin.

## RED/GREEN-bewys

- RED: toetsinsameling het met die verwagte `ModuleNotFoundError` vir `midi_chip_platform.configuration` gefaal.
- GREEN: 40 hosttoetse slaag op `v0.5.0`; AST- en importveiligheidsreëls bly groen.
- Geheimekontrole: kunsmatige SSID- en wagwoordwaardes verskyn nie in `report_lines()` of publieke items nie.
- Toestelpreflight: `CIRCUITPY` en CDC bestaan; die volume rapporteer media-leesalleen en die deploy het voor enige verandering gefaal.

## Menslike aanvaardingshek

1. Maak Thonny en enige serial monitor toe.
2. Ontkoppel die bord se USB-kabel, wag vyf sekondes en koppel dit weer sonder BOOT.
3. Bevestig dat Finder na `CIRCUITPY` kan skryf deur 'n onskadelike nuwe tekslêer te skep en weer te verwyder.
4. Indien die volume steeds leesalleen is, stop en deel die resultaat; moenie formatteer of `storage.erase_filesystem()` uitvoer nie.
5. Ná 'n skryfbare mount deploy die US-005-manifest en bevestig `CONFIGURATION_STATUS=PASS` plus private `SET`/`UNSET`-status sonder waardes.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het US-005 en US-006 vooraf goedgekeur en menslike toetsing vir ná werk beplan. |
| Scrum Master | Hou Wi-Fi-verbinding en klankaktivering buite US-005; log die leesalleen-HIL-hek. |
| Business Analyst | Definieer override, private settings en publieke verstekke as drie eksplisiete lae. |
| Solution Architect | Vereis `ConfigurationPort`, dependency injection en geen import-newe-effekte. |
| Embedded Engineer | Gebruik CircuitPython `os.getenv()` en raak nie die bestaande private `settings.toml` aan nie. |
| MIDI Engineer | Not impacted: geen MIDI-boodskap word in US-005 ontvang of verander nie. |
| DSP/Chip Engineer | Behou die goedgekeurde MAX98357A-penprofiel maar aktiveer geen audio nie. |
| Web Engineer | Bevestig dat latere station/AP-credentials deur dieselfde private grens kom. |
| QA/HIL Engineer | Lewer RED/GREEN, lektoetse, FAT-verifikasie en 'n nie-destruktiewe menslike herstelhek. |
| Release/Documentation | Sinkroniseer weergawe, quickstart, bronne, risiko, lessons learned en Kanban. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe reviewer-inset is vir US-005 ontvang nie. |
| Devil's Advocate | Waarsku dat `settings.toml` skeiding bied, maar nie enkripsie of credential-rotasie vervang nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
