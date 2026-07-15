# Risiko-register

<!--
Bestand: risk_register_v0.1.0.md
Versienommer: 0.10.0
Doel: Tegniese, produk-, veiligheids- en afleweringsrisiko’s vir die MVP.
Sprint: Sprint 0
Epic: Alle epics
User-Story: MVP-SCOPE-REDUCTION-001 en MCP-US-016
Actienr: MCP-ACT-MVP-SCOPE-001-RISK-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MVP-SCOPE-REDUCTION-001
-->

| ID | Risiko | Waarskynlikheid | Impak | Eienaar | Beheer/mitigering | Status |
|---|---|---:|---:|---|---|---|
| R-001 | Wi-Fi-geheim was in prototipebron | Hoog | Kritiek | Security/PO | Roteer wagwoord; private `settings.toml`; geheime-skandering | Oop - mensaksie |
| R-002 | Te veel USB-endpoints plaas ESP32-S2 in safe mode | Medium | Hoog | Embedded | Minimale `boot.py`; skakel onnodige HID/CDC doelbewus; herstelrunbook | Oop |
| R-003 | Onbehoorlike VID/PID veroorsaak konflik of verspreidingsprobleem | Medium | Hoog | Release/Architect | Gebruik ontwikkelverstekke; besluit geldige produkidentiteit voor release | Oop |
| R-004 | Busy-wait PWM blokkeer MIDI, web en REPL | Hoog | Hoog | DSP/Embedded | Koöperatiewe scheduler; buffer-/I2S-spike; jittermeting | Oop |
| R-005 | I2S-ondersteuning of penkombinasie verskil per bord | Medium | Hoog | Embedded | US-004 profiel/runtime-diagnose bevestig S2 IO5/IO3/IO7 en `audiobusio`; MAX98357 klank-HIL volg in US-016 | Beheer aktief |
| R-006 | Webserver gebruik te veel RAM/sokke | Hoog | Hoog | Web/QA | Een kliënt; klein statiese bates; pollingbegroting; geheuemeting | Oop |
| R-007 | “Alle CircuitPython-borde” word verkeerd as identies aangebied | Hoog | Hoog | Architect/Docs | Profielkontrak; ondersteuningsmatriks; geen onbevestigde eis nie | Beheer aktief |
| R-008 | Raspberry Pi Linux en mikrobeheerderfirmware word vermeng | Medium | Medium | Architect | Afsonderlike Blinka/host-adapter en toetsbaan | Beheer aktief |
| R-009 | Meer kerne oorskry CPU/RAM en beïnvloed klank | Hoog | Hoog | DSP/Architect | Sluit eers enkelkern-D1 MVP; meet elke post-MVP multi-core-uitbreiding en weier onveilige kapasiteit deterministies | Post-MVP - risiko aanvaar |
| R-010 | SID/OPL-emulasie skep lisensie- of akkuraatheidsaansprake | Medium | Hoog | PO/Release | Bronlisensie-register; akkuraatheidsvlakke; geen “cycle accurate” sonder bewys | Oop |
| R-011 | MIDI clock (24 PPQN) oorlaai ontvangslus | Medium | Hoog | MIDI | Prioriteitsry, geen onnodige logging, klok-jittertoetse | Oop |
| R-012 | Dedupe-logika verwyder geldige note of clock | Medium | Hoog | MIDI/QA | Boodskapspesifieke dedupe; nooit blind op clock toepas nie | Oop |
| R-013 | MAX98357 bridge-tied uitset word geaard of as line-out gebruik | Medium | Kritiek | Hardware | Bedradingsdiagram; luidspreker direk tussen + en -; geen grond/line-input; HIL-kontrolelys | Oop |
| R-014 | DSP delay/reverb oorskry geheue en latensie | Hoog | Hoog | DSP | Harde bufferbegroting; bypass; no-go aanvaarbaar vir reverb-spike | Oop |
| R-015 | Outomatiese toestelkopie beskadig werkende prototipe | Laag | Kritiek | Release/QA | Rugsteun, manifest, dry-run, staging en eksplisiete deploy-story | Beheer aktief |
| R-016 | Side quests breek logiese storyvolgorde | Hoog | Medium | Scrum Master | Now/Next/Later/Parking Lot; uitvoerplan-goedkeuring per story | Beheer aktief |
| R-017 | Plaaslike LLM lewer onbetroubare kode of lek konteks | Medium | Medium | Architect/QA | Slegs klein nie-geheime take ná overleg; Codex-review en toetse verpligtend | Oop |
| R-018 | Privaat toestelrugsteun word per ongeluk gepubliseer | Laag | Kritiek | Release | Buite repo; beperkte regte; `.gitignore`; pre-commit inhoudkontrole | Beheer aktief |
| R-019 | MIDI-kitaar se bend range/kanaalmodus verskil van die synth en maak slides vals | Hoog | Hoog | MIDI/QA | Konfigureerbare bend range; per-kanaal bend-state; Fishman plus generiese HIL; diagnose wys modus | Oop |
| R-020 | Twee USB-device-endpoints word sonder 'n USB-host verbind en geen MIDI vloei nie | Hoog | Hoog | MIDI/Docs | Dokumenteer host/device-rolle; gebruik rekenaar, Raspberry Pi of eksterne USB-host; DIN/UART HIL | Oop |
| R-021 | Device-proof publiseer UID, MAC, SSID of ander plaaslike data | Medium | Kritiek | QA/Release | Redigeer uitvoer; publiseer slegs poorttipe, bord-ID, firmwareweergawe, commit/hash en status | Beheer aktief |
| R-022 | Eksterne USB-host ondersteun nie die betrokke controller of bend/clock-boodskap nie | Medium | Hoog | MIDI/QA | Klas-kompatibiliteitsmatriks; generiese plus Fishman HIL; geen handelsnaamwaarborg sonder toets nie | Oop |
| R-023 | Die primêre ESP32-S2 het geen native BLE-ondersteuning nie | Hoog | Medium | Architect/Embedded | BLE is post-MVP; capability gate hou USB stabiel; kies later 'n BLE-geskikte tweede bord in US-052/062 | Beheer aktief |
| R-024 | Herhaalde macOS host-MIDI-scan abort in `python-rtmidi`/CoreMIDI | Hoog | Medium | QA/Tooling | Moenie dieselfde in-proses scan herhaal nie; isoleer toekomstige host-scan in ’n subprocess; firmware-HIL steun op USB descriptors en device logs | Oop - hostimpediment |
| R-025 | MIDI-HIL hang of faal deur ’n poortkonflik met Thonny of ’n serial monitor | Medium | Hoog | QA/HIL | Preflight poorte; presies een REPL-kliënt; timeout, cleanup en herstelpad | Oop |
| R-026 | Fallback access point is oop, voorspelbaar of lek credentials/kliëntidentiteit | Medium | Kritiek | Security/Web | Beveiligde AP as verstek; credentials uit private config of veilige provisioning; geen geheime, MAC’s of unieke ID’s in logs/repo nie | Oop |
| R-027 | Onbegrensde join/reconnect, HTTP polling of debuglogging veroorsaak dropout, RAM-druk of flashslytasie | Hoog | Hoog | Embedded/Web/QA | Timeout en backoff; koöperatiewe poll; een kliënt; debug af in produksie; gebeurtenis-/koersbegrensde serial logging en geen normale flashlog nie | Oop |
| R-028 | Programmatiese harde reset laat USB-toestel soms sonder CIRCUITPY/CDC-herenumerasie | Medium | Hoog | Embedded/QA | Fisiese power-cycle het volume/REPL herstel; recovery-runbook en finale manifest-HIL is bewys | Beheer aktief |
| R-029 | CIRCUITPY-media word geldig maar leesalleen aan die host aangebied | Medium | Hoog | Embedded/Release | Stop deploy; verifieer FAT nie-destruktief; fisiese power-cycle en skryfbaarheidstoets; geen formattering of concurrent-write-omseiling nie | Beheers - skryfbare HIL op 2026-07-15 |
| R-030 | USB-produkname bots of verander tussen boots | Medium | Hoog | Embedded/Release | Stabiele nie-geheime vier-karakter instance-ID, gedokumenteerde collision fallback en twee-toestel DAW-aanvaarding in MCP-US-068 | Backlog - MCP-US-068 |
| R-031 | Verkeerde voeding, vlakke, klok of bussekwensie beskadig 'n skaars fisiese retrochip | Medium | Kritiek | DSP/Chip/Hardware | Datasheet- en meethek voor bedrading; current-limited bench supply; level shifting; geen universele expander-aanname | Later - MCP-US-070 tot US-073 |
| R-032 | Fisiese backend word vals opgespoor, hang die runtime of speel saam met emulasie | Medium | Hoog | Architect/Embedded/QA | Capability probe, timeout, fault injection, veilige oorskakelgrens en emulasie as verstek/fallback | Later - MCP-US-074 |
| R-033 | Die onafhanklike I2S-toets dryf weg van produksie se AudioOutput-profiel | Medium | Hoog | Architect/QA/HIL | Behou dieselfde profielveldname; AST/import- en frekwensietoetse; gepaarde MAX98357-HIL; geen gedeelde synth-runtime-import nie | Beheer in MCP-US-016 |

## Hoogste onmiddellike aksies

1. **Roteer die blootgestelde Wi-Fi-wagwoord.** Dit kan nie deur kode alleen herstel word nie.
2. Hou MCP-US-003 se `boot.py` minimaal en herstelbaar.
3. Sluit US-005, bou US-014 en bewys daarna die onafhanklike US-016 G-C-D/MAX98357-pad voor D1.
4. Publiseer geen toestelrugsteun, unieke USB-ID of plaaslike netwerkdetail nie.
5. Behandel ’n sigbare `ESP_*`-SSID as onbevestig totdat ’n beheerde power-cycle of device-log die fisiese bord korreleer.
6. Hou SN76489, web, BLE, stereo, PWM, DSP, multi-core en USB-instance-polish post-MVP totdat Logic na hoorbare D1 aanvaar is.
