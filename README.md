# CircuitPython MIDI Chip Platform

> ’n MIDI-beheerde, multi-kern retro-sintetiseerdermodule in pedaalvorm, met USB-MIDI, stereo-klankuitvoer, plaaslike webbeheer en uitbreibare skyfie-emulasie.

![CircuitPython MIDI Chip Platform-argitektuur in 1985-retrostyl](assets/images/circuitpython-midi-chip-platform-architecture-v0.1.0.png)

Die seinpad bly doelbewus modulêr. Die eerste klein MVP bewys slegs **Logic USB-MIDI → D1-basiskern → MAX98357-I2S**. Daarna brei dieselfde kontrakte uit na **SN76489 → 6581 SID → OPL2 → OPL3**, ander transports en ander klankbackends.

## Projekstatus

Die projek is by **Sprint 2**, runtime **v0.13.0**. MCP-US-014 se blokgebaseerde AudioOutput plus Null/Memory-backends is host-groen; dit is nog nie 'n fisiese klankclaim nie. Die volgende story is die onafhanklike MCP-US-016 G-C-D/MAX98357 I2S-toets, gevolg deur die D1-kern en hoorbare Logic-aanvaarding.

## Begin hier

### 1. Gebruikers: installatiegids
Die [snelbegin- en installasiegids](docs/quickstart_installation_v0.1.0.md) neem 'n beginner stap vir stap deur Git, Python, 'n virtuele omgewing, installasie, diagnose en toetse op macOS, Windows en Raspberry Pi. VS Code en Thonny is opsionele hulpmiddels; die projek is nie van enige IDE afhanklik nie.

Nadat die installasie voltooi is:

```bash
python -m midi_chip_platform diagnose
python -m pytest
```

### 2. Ontwikkelaars: Bootloader
Lees die [architectuur, teams en user stories](https://github.com/pappavis/circuitpython-midi-chip-platform/blob/main/docs/framework_engineering/README.md) "Bootloader".


## MVP in een sin

Bewys op 'n LOLIN/Wemos ESP32-S2 Mini dat Logic Pro USB-MIDI Note On/Off kan stuur en dat 'n draagbare D1-basiskern hoorbaar deur die MAX98357-I2S-uitvoer speel.

## Ná die eerste MVP

SN76489, SID, OPL, BLE-MIDI, DIN/UART, MIDI-kitaar-slides, stereo, multi-core, DSP en plaaslike webbeheer bly geordende post-MVP stories. Wi-Fi sal nooit in `boot.py` begin nie.

## Hoekom ’n skoon repository?

Die bestaande `pappavis/midi-chip-platform` bevat waardevolle idees, dokumentasie en ’n ou modulêre CircuitPython-basislyn, maar ook verskillende runtime-generasies. Hierdie repository hergebruik die getoetste kontrakte en leerlesse sonder om historiese eksperimente as produksiekode te behandel.

## Lees eerste

- [MVP-omvang](docs/mvp_scope_v0.1.0.md)
- [Framework Engineering: beheerde visie-, argitektuur- en kwaliteitsingang](docs/framework_engineering/README.md)
- [Enterprise Vision](docs/framework_engineering/enterprise_vision_v0.1.0.md)
- [Framework And Solution Architecture](docs/framework_engineering/architecture_v0.1.0.md)
- [Enterprise Meta Model](docs/framework_engineering/enterprise_meta_model_v0.1.0.md)
- [Quality Manual](docs/framework_engineering/quality_manual_v0.1.0.md)
- [Test Strategy](docs/framework_engineering/test_strategy_v0.1.0.md)
- [Volledige user-story-katalogus](docs/user_stories_v0.1.0.md)
- [Toestel- en broninventaris](docs/mcp_us_001_device_source_baseline_inventory_v0.1.0.md)
- [Hergebruiksmatriks](docs/reuse_matrix_v0.1.0.md)
- [Span en RACI](docs/team_raci_v0.1.0.md)
- [Risiko-register](docs/risk_register_v0.1.0.md)
- [Burn-In en heap-stabiliteitspesifikasie](docs/burn_in_heap_stability_spec_v0.1.0.md)
- [Bronregister](docs/source_register_v0.1.0.md)
- [Excel Kanban-backlog](outputs/CHATOD-20260714-MCP-CP-MVP-001/circuitpython_midi_chip_platform_mvp_kanban_v0.1.0.xlsx)
- [Agile delivery- en releaseplan](docs/agile_delivery_release_plan_v0.1.0.md)
- [Backlog sanity check](docs/backlog_sanity_check_v0.1.0.md)
- [Afdwingbare agent- en kodereels](AGENTS.md)
- [Snelbegin, installasie en ontwikkelomgewings](docs/quickstart_installation_v0.1.0.md)
- [MCP-US-002 review en toetsbewys](docs/mcp_us_002_project_skeleton_review_v0.1.0.md)
- [MCP-US-003 safe-boot review en HIL-bewys](docs/mcp_us_003_safe_boot_review_v0.1.0.md)
- [MCP-US-004 bordvermoëns-review en bedrading](docs/mcp_us_004_board_capability_review_v0.1.0.md)
- [MCP-US-005 konfigurasie- en geheimegrens-review](docs/mcp_us_005_configuration_secret_boundary_review_v0.1.0.md)
- [MCP-US-014 AudioOutput-review](docs/mcp_us_014_audio_output_review_v0.1.0.md)
- [MCP-US-006 draagbare MIDI-eventmodel-review](docs/mcp_us_006_portable_event_model_review_v0.1.0.md)
- [MCP-US-007 USB-MIDI receive-loop-review](docs/mcp_us_007_usb_midi_receive_review_v0.1.0.md)
- [MCP-US-062 BLE-MIDI capability-review](docs/mcp_us_062_ble_midi_capability_review_v0.1.0.md)
- [MCP-US-008 MIDI-kanaalrouter-review](docs/mcp_us_008_midi_channel_router_review_v0.1.0.md)
- [MCP-US-009 note-off-semantiek-review](docs/mcp_us_009_note_semantics_review_v0.1.0.md)
- [MCP-US-010 pitch bend/CC1-review](docs/mcp_us_010_pitch_bend_cc1_review_v0.1.0.md)
- [Outonome MIDI-batch hostaanvaarding en toestelverbinding](docs/autonomous_midi_batch_host_acceptance_v0.1.0.md)
- [Sprint 1 lessons learned - checkpoint 001](docs/lessons_learned_sprint_1_checkpoint_001_v0.1.0.md)
- [Sprint 2 lessons learned - checkpoint 001](docs/lessons_learned_sprint_2_checkpoint_001_v0.1.0.md)
- [Sprint 2 lessons learned - dependency-closed deployment](docs/lessons_learned_sprint_2_checkpoint_002_v0.1.0.md)
- [Sprint 2 lessons learned - USB-MIDI HIL en repository/REPL](docs/lessons_learned_sprint_2_checkpoint_003_v0.1.0.md)
- [MCP-US-051 HIL-runner review](docs/mcp_us_051_hil_runner_review_v0.1.0.md)
- [MCP-US-051/007 dependency-closed deployment-impediment](docs/mcp_us_051_mcp_us_007_dependency_closed_deployment_impediment_v0.1.0.md)
- [Audio-prioriteit en MIDI-kitaar amendment](docs/audio_priority_amendment_v0.1.0.md)
- [MIDI-transport en multi-core amendment](docs/midi_transport_multicore_amendment_v0.1.0.md)
- [BLE-MIDI en synth-core-prioriteit](docs/ble_midi_core_priority_amendment_v0.1.0.md)
- [Wi-Fi station-, access-point- en mobiele webfallback](docs/wifi_runtime_fallback_amendment_v0.1.0.md)
- [Post-MVP fisiese chip- en I2C-display-uitbreiding](docs/physical_chip_display_expansion_amendment_v0.1.0.md)
- [Device Connection Proof](docs/device_connection_proof_v0.1.0.md)
- [Repository-identiteit en sinkronisasiekontrak](docs/repository_identity_and_sync_v0.1.0.md)

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
- `device/i2s_test.py` sal as US-016 die MAX98357-pad onafhanklik met G-C-D square waves toets; dit voer geen synthpakket in nie en deel geen globale status nie.
- Die klankenjin bly vervangbaar: draagbare D1-basiskern eerste, SN76489 tweede, 6581 SID derde en OPL2/OPL3 daarna.
- Ná MVP kan dieselfde kernkontrak 'n emuleerde of fisiese chipbackend kies; emulasie bly altyd verstek en veilige fallback.
- BLE-MIDI is post-MVP en capability-gated: die ESP32-S2 rapporteer dit veilig as nie-ondersteun; 'n BLE-geskikte tweede bord lewer later die fisiese aanvaardingsbewys.
- Wi-Fi-runtime gebruik ’n eksplisiete toestandmasjien: station join, begrensde mislukking, beveiligde AP-fallback en sigbare IP; logging is spaarsaam en koersbegrens.
- Die span volg backlogvolgorde; side quests word georden en nie stilweg geimplementeer nie.
- Lessons learned word na elke drie of vier voltooide stories en by epic-/releasegrense opgedateer.
- `python-d1-synth` is produksiekode en word uitsluitlik as 'n leesalleen-verwysing gebruik.
- Ollama is opsioneel vir goedgekeurde klein ontwikkeltake; dit is nooit nodig om die synth te bou of uit te voer nie.
- Startup toon altyd projekweergawe, aktiewe story/amendment en release-datum.
- 'n Post-MVP release-polish story sal elke USB-toestel 'n herkenbare `EasyLab4Kids-midi-chip-platform XXXX`-styl naam gee, waar `XXXX` 'n stabiele, nie-geheime instance-ID is.

## Lisensie

MIT. Sien [LICENSE](LICENSE).
