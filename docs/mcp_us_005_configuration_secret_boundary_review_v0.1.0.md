# MCP-US-005 Configuration And Secret Boundary Review

<!--
Bestand: mcp_us_005_configuration_secret_boundary_review_v0.1.0.md
Versienommer: 0.3.1
Doel: Dokumenteer die private settings-grens, leewaarde-herstel en finale HIL-hek.
Sprint: Sprint 1
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-005 Configuration And Secret Boundary
Actienr: MCP-ACT-005-IMP-001-DOC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005-RETEST
-->

## Status

**IN REVIEW / MENSLIKE KONFIGURASIEHEK.** Geheime-redaksie en host-regressie is groen. v0.12.3 is fisies gedeploy en connection, manifest, libraries, boot en execution slaag. Die toestel rapporteer drie private, werklik nie-leë waardes veilig as `SET`; die `UNSET`-tak bly die enigste oop sluitingshek.

## Konfigurasieprioriteit

Van hoogste na laagste:

1. Geïnjekteerde runtime-overrides.
2. `CIRCUITPY/settings.toml`, gelees deur `os.getenv()`.
3. Publieke, klasinstansie-besitte verstekke.

Die huidige publieke klankprofiel is mono MAX98357A met IO5 BCLK, IO3 WS/LRC en IO7 DATA/DIN. Geen klank- of Wi-Fi-diens word deur hierdie story begin nie.

## Geheimegrens

- `wifi.ssid`, `wifi.password` en `web.ap.password` word as private sleutels behandel.
- Diagnostiek rapporteer slegs `SET` of `UNSET`, nooit die waarde nie.
- Leë strings en waardes wat net uit whitespace bestaan, tel as `UNSET`; nie-leë geheime behou hul presiese waarde intern.
- `public_items()` sluit private sleutels en waardes uit.
- `settings.toml` bly in `.gitignore`; `device/settings.toml.example` bevat slegs plekhouers.
- Die ou prototipewagwoord bly 'n roteeraksie vir die Product Owner voordat Wi-Fi-stories begin.

## RED/GREEN-bewys

- RED: toetsinsameling het met die verwagte `ModuleNotFoundError` vir `midi_chip_platform.configuration` gefaal.
- GREEN: 40 hosttoetse slaag op `v0.5.0`; AST- en importveiligheidsreëls bly groen.
- Geheimekontrole: kunsmatige SSID- en wagwoordwaardes verskyn nie in `report_lines()` of publieke items nie.
- Toestelherbewys: CIRCUITPY/CDC, manifest, libraries, boot, config-import en execution het geslaag; private waardes is nie gepubliseer nie.
- RED 2026-07-16: twee nuwe regressietoetse het gewys dat leë en whitespace-private waardes foutief in die snapshot beland.
- GREEN 2026-07-16: die settings source normaliseer daardie waardes na `None`; 33 geteikende config/CLI/HIL-toetse en die volle stel van 91 hosttoetse slaag op v0.12.3.
- DEVICE 2026-07-16: v0.12.3 se geredigeerde HIL-verslag toon connection, manifest-closure, deployment, libraries, boot en execution as PASS. 'n Waardevrye vormkontrole het bevestig dat al drie private reëls werklik nie-leë waardes bevat; die runtime se drie `SET`-statusse is dus korrek. Geen waarde, SSID, wagwoord, UID of MAC word as aanvaardingsbewys gepubliseer nie.

## Menslike aanvaardingshek

1. Maak Thonny en enige serial monitor toe.
2. Laat die drie private waardes leeg of verwyder hul reëls; hard-reset en verwag drie keer `UNSET`.
3. Stel slegs veilige dummy-toetswaardes; hard-reset en verwag die betrokke velde as `SET`, nooit die waardes nie.
4. Verwyder die dummywaardes of maak hulle weer leeg; hard-reset en verwag weer `UNSET`.

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
