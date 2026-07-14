# CircuitPython MIDI Chip Platform

> ’n MIDI-beheerde, multi-kern retro-sintetiseerdermodule in pedaalvorm, met USB-MIDI, stereo-klankuitvoer, plaaslike webbeheer en uitbreibare skyfie-emulasie.

## Projekstatus

Die projek is in **Sprint 0: platformfondasie**. MCP-US-002 lewer 'n invoerveilige, klasgebaseerde host-skelet met poorte vir MIDI, klank, klok en konfigurasie. Daar is nog geen toestel-firmware of hoorbare chip-emulasie in hierdie repository nie; daardie werk volg volgens backlogvolgorde.

## Begin hier

Die [snelbegin- en installasiegids](docs/quickstart_installation_v0.1.0.md) neem 'n beginner stap vir stap deur Git, Python, 'n virtuele omgewing, installasie, diagnose en toetse op macOS, Windows en Raspberry Pi. VS Code en Thonny is opsionele hulpmiddels; die projek is nie van enige IDE afhanklik nie.

Nadat die installasie voltooi is:

```bash
python -m midi_chip_platform diagnose
python -m pytest
```

## MVP in een sin

Bewys op ’n LOLIN/Wemos ESP32-S2 Mini dat ’n gebruiker USB-MIDI-note kan stuur, ’n SN76489-agtige driestem-kern kan speel, links/regs/stereo-uitvoer kan kies, ’n hoorbare opstarttoets kan uitvoer en kernparameters op ’n eenvoudige plaaslike webblad kan verander.

## Hoekom ’n skoon repository?

Die bestaande `pappavis/midi-chip-platform` bevat waardevolle idees, dokumentasie en ’n ou modulêre CircuitPython-basislyn, maar ook verskillende runtime-generasies. Hierdie repository hergebruik die getoetste kontrakte en leerlesse sonder om historiese eksperimente as produksiekode te behandel.

## Lees eerste

- [MVP-omvang](docs/mvp_scope_v0.1.0.md)
- [Volledige user-story-katalogus](docs/user_stories_v0.1.0.md)
- [Toestel- en broninventaris](docs/mcp_us_001_device_source_baseline_inventory_v0.1.0.md)
- [Hergebruiksmatriks](docs/reuse_matrix_v0.1.0.md)
- [Span en RACI](docs/team_raci_v0.1.0.md)
- [Risiko-register](docs/risk_register_v0.1.0.md)
- [Bronregister](docs/source_register_v0.1.0.md)
- [Excel Kanban-backlog](outputs/CHATOD-20260714-MCP-CP-MVP-001/circuitpython_midi_chip_platform_mvp_kanban_v0.1.0.xlsx)
- [Agile delivery- en releaseplan](docs/agile_delivery_release_plan_v0.1.0.md)
- [Backlog sanity check](docs/backlog_sanity_check_v0.1.0.md)
- [Afdwingbare agent- en kodereels](AGENTS.md)
- [Snelbegin, installasie en ontwikkelomgewings](docs/quickstart_installation_v0.1.0.md)
- [MCP-US-002 review en toetsbewys](docs/mcp_us_002_project_skeleton_review_v0.1.0.md)

## Belangrike veiligheidsreëls

- Wi-Fi-wagwoorde, API-sleutels en plaaslike toestelidentifiseerders word nooit in Git gestoor nie.
- `settings.toml`, `secrets.py`, firmwarebeelde en private toestelrugsteune word deur `.gitignore` uitgesluit.
- ’n Wagwoord wat voorheen in prototipekode verskyn het, moet geroteer word voordat netwerkwerk begin.
- Geen UF2-flash, skyfuitvee of bootloader-aksie gebeur sonder ’n afsonderlike, eksplisiete goedkeuring nie.

## Ontwikkelbeginsels

- Klasgebaseerde ontwerp sonder globale toepassingsstatus.
- Geen globale veranderlikes, `global`-statements, modulevlak helperfunksies of import-newe-effekte nie.
- Alle runtime-status behoort aan klasinstansies en word via dependency injection gekoppel.
- Klein stories met rooi/groen-toetse en eksplisiete hardeware-aanvaarding.
- Bordvermoëns word ontdek; bordname, MIDI-toestelle en penne word nie as universele konstantes aanvaar nie.
- MIDI, kernlogika, klankuitvoer en webbeheer word deur duidelike poorte geskei.
- Die klankenjin bly vervangbaar: SN76489 eerste; SID, OPL2/OPL3 en ander kerne later.
- Die span volg backlogvolgorde; side quests word georden en nie stilweg geimplementeer nie.
- Lessons learned word na elke drie of vier voltooide stories en by epic-/releasegrense opgedateer.
- `python-d1-synth` is produksiekode en word uitsluitlik as 'n leesalleen-verwysing gebruik.
- Ollama is opsioneel vir goedgekeurde klein ontwikkeltake; dit is nooit nodig om die synth te bou of uit te voer nie.

## Lisensie

MIT. Sien [LICENSE](LICENSE).
