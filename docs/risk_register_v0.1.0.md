# Risiko-register

<!--
Bestand: risk_register_v0.1.0.md
Versienommer: 0.2.0
Doel: Tegniese, produk-, veiligheids- en afleweringsrisiko’s vir die MVP.
Sprint: Sprint 0
Epic: Alle epics
User-Story: AUDIO-PRIORITY-AMENDMENT-001
Actienr: MCP-ACT-AUDIO-AMEND-RISK-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001
-->

| ID | Risiko | Waarskynlikheid | Impak | Eienaar | Beheer/mitigering | Status |
|---|---|---:|---:|---|---|---|
| R-001 | Wi-Fi-geheim was in prototipebron | Hoog | Kritiek | Security/PO | Roteer wagwoord; private `settings.toml`; geheime-skandering | Oop - mensaksie |
| R-002 | Te veel USB-endpoints plaas ESP32-S2 in safe mode | Medium | Hoog | Embedded | Minimale `boot.py`; skakel onnodige HID/CDC doelbewus; herstelrunbook | Oop |
| R-003 | Onbehoorlike VID/PID veroorsaak konflik of verspreidingsprobleem | Medium | Hoog | Release/Architect | Gebruik ontwikkelverstekke; besluit geldige produkidentiteit voor release | Oop |
| R-004 | Busy-wait PWM blokkeer MIDI, web en REPL | Hoog | Hoog | DSP/Embedded | Koöperatiewe scheduler; buffer-/I2S-spike; jittermeting | Oop |
| R-005 | I2S-ondersteuning of penkombinasie verskil per bord | Medium | Hoog | Embedded | Vermoënsprofiel; runtime-diagnose; MAX98357 HIL; PWM fallback | Oop |
| R-006 | Webserver gebruik te veel RAM/sokke | Hoog | Hoog | Web/QA | Een kliënt; klein statiese bates; pollingbegroting; geheuemeting | Oop |
| R-007 | “Alle CircuitPython-borde” word verkeerd as identies aangebied | Hoog | Hoog | Architect/Docs | Profielkontrak; ondersteuningsmatriks; geen onbevestigde eis nie | Beheer aktief |
| R-008 | Raspberry Pi Linux en mikrobeheerderfirmware word vermeng | Medium | Medium | Architect | Afsonderlike Blinka/host-adapter en toetsbaan | Beheer aktief |
| R-009 | Meer kerne oorskry CPU/RAM en beïnvloed klank | Hoog | Hoog | DSP/Architect | Een kern in eerste MVP; begroting vóór tweede kern | Oop |
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

## Hoogste onmiddellike aksies

1. **Roteer die blootgestelde Wi-Fi-wagwoord.** Dit kan nie deur kode alleen herstel word nie.
2. Hou MCP-US-003 se `boot.py` minimaal en herstelbaar.
3. Bewys 'n veilige, hoorbare MAX98357 mono-I2S-pad en hou PWM as meetbare fallback voordat webbeheer bygevoeg word.
4. Publiseer geen toestelrugsteun, unieke USB-ID of plaaslike netwerkdetail nie.
