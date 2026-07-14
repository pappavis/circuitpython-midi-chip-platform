# User-story-katalogus

<!--
Bestand: user_stories_v0.1.0.md
Versienommer: 0.1.0
Doel: Volledige geordende backlog vir MVP en latere inkremente.
Sprint: Sprint 0
Epic: Alle epics
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Statuslegende

- **Done:** artefakte en bewys is gereed vir aanvaarding.
- **In Review:** implementering en outomatiese bewys is gereed vir menslike aanvaarding.
- **Next:** logiese volgende story; nog nie begin nie.
- **MVP:** nodig vir die eerste aanvaarbare produkdemonstrasie.
- **Stretch:** slegs indien die vaste MVP stabiel en binne begroting is.
- **Later:** geprioritiseerde voortsetting ná MVP.

## MCP-EPIC-001 Platform Foundation

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-001 | Device And Source Baseline Inventory | Done | - | Bord, bronne, rugsteun, risiko’s en hergebruik is gedokumenteer |
| MCP-US-002 | Clean Repository And Project Skeleton | In Review/MVP | US-001 | Klasgebaseerde poorte, host-toetse en headers bestaan; geen toestel-I/O nie |
| MCP-US-003 | Minimal Safe Boot And USB Profile | MVP | US-002 | USB-MIDI begin vóór runtime; geen netwerk of geheime in `boot.py` nie |
| MCP-US-004 | Board Capability Discovery | MVP | US-002 | Bordprofiel rapporteer penne, modules, geheue en ondersteunde klankbackends |
| MCP-US-005 | Configuration And Secret Boundary | MVP | US-003 | Publieke verstekke en private `settings.toml` werk; geheime-lektoets is groen |

## MCP-EPIC-002 MIDI And Clock

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-006 | Portable NoteEvent And ControlEvent Model | MVP | US-002 | Note, CC, bend en klokboodskappe het platform-onafhanklike klasse |
| MCP-US-007 | USB MIDI Receive Loop | MVP | US-003, US-006 | Enige klas-kompatibele USB-MIDI-bron kan Note On/Off stuur |
| MCP-US-008 | MIDI Channel Router | MVP | US-007 | Kanaal 1-16 word konfigureerbaar na ’n kerninstansie gerouteer |
| MCP-US-009 | Velocity And Note-Off Semantics | MVP | US-007 | Velocity nul sluit note; geen hangende stem ná All Notes Off nie |
| MCP-US-010 | Pitch Bend And CC1 Modulation | MVP | US-007 | Bend en vibrato word hoorbaar en diagnosties gemeet |
| MCP-US-011 | Internal 120 BPM Clock | MVP | US-002 | Interne klok lewer stabiele 24 PPQN-afgeleides en BPM-metriek |
| MCP-US-012 | External MIDI Clock Sync | MVP | US-007, US-011 | USB of adapter-klok kan Start/Stop/Continue en tempo beheer |
| MCP-US-013 | External IO MIDI Transport Spike | Later | US-007 | UART/DIN- of ander IO-adapter word deur dieselfde MIDI-poort geabstraheer |

## MCP-EPIC-003 Audio And Chip Core

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-014 | AudioOutput Port And Null Backend | MVP | US-002 | Kernlogika kan sonder fisiese klank host-getoets word |
| MCP-US-015 | Stereo PWM Diagnostic Backend | MVP | US-004, US-014 | Twee gekose penne lewer meetbare links/regs PWM-klank |
| MCP-US-016 | I2S Feasibility Spike | MVP | US-004, US-014 | Ondersteuning, penne, DAC, RAM, latensie en kwaliteit is gemeet |
| MCP-US-017 | SN76489-Lite Three-Voice Core | MVP | US-006, US-014 | Drie toonstemme speel onafhanklik met gedokumenteerde akkuraatheid |
| MCP-US-018 | Voice Allocation And Stealing | MVP | US-017 | Vierde noot volg ’n toetsbare steal-policy sonder vasloop |
| MCP-US-019 | Per-Voice Left Right Stereo Routing | MVP | US-015, US-017 | Elke stem kan links, regs of stereo gemonitor word |
| MCP-US-020 | Optional G-C-D Startup Test | MVP | US-015, US-017 | Opsionele sestiendenootreeks bewys die klankpad by start |
| MCP-US-021 | Audio Backend Decision | MVP | US-015, US-016 | ADR kies primêre uitvoer; PWM-diagnostiek bly beskikbaar |

## MCP-EPIC-004 Local Web Control

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-022 | Cooperative Runtime Scheduler | MVP | US-007, US-014 | MIDI, klank en web-polling deel tyd sonder hoorbare blokkasie |
| MCP-US-023 | Safe Wi-Fi Runtime Service | MVP | US-005, US-022 | Wi-Fi begin buite boot en gee ’n duidelike offline-modus |
| MCP-US-024 | Local Web Status And Parameters | MVP | US-023 | Een plaaslike kliënt kan status lees en veilige parameters verander |
| MCP-US-025 | Browser Virtual MIDI Keyboard | MVP | US-024 | Klik/touch stuur note via dieselfde event-model |
| MCP-US-026 | Simple Step Sequencer | MVP | US-011, US-024 | ’n Kort patroon kan teen interne/eksterne klok loop en stop |
| MCP-US-027 | Web Security And Recovery | MVP | US-024 | Vertroude-LAN-grens, sessielimiet en herstelpad is getoets |

## MCP-EPIC-005 Files, Harmony And Performance Tools

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-028 | Constrained MIDI File Parser | Later | US-006, US-011 | Ondersteunde formaat en gebeurtenislimiete faal veilig |
| MCP-US-029 | Chip-Aware MIDI File Playback | Later | US-017, US-028 | Oortollige note word volgens die kern se stemlimiet hanteer |
| MCP-US-030 | Local Media File Browser | Later | US-024, US-028 | Gebruiker kies ’n plaaslike MIDI-lêer sonder kodewysiging |
| MCP-US-031 | Arpeggiator | Stretch | US-011, US-017 | Up/down/random patrone volg BPM en note-off |
| MCP-US-032 | Chord Progression Generator | Stretch | US-026 | Sleutel, progressie, BPM en random seed is beheerbaar |
| MCP-US-033 | Patch Save Load And Factory Reset | MVP | US-005, US-024 | Geldige patch bly ná reboot; korrupsie val terug na veilige verstek |

## MCP-EPIC-006 Multi-Core Expansion

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-034 | SynthCore Interface And Registry | MVP | US-002, US-017 | Kern kan via registrasienaam gekies word sonder routerwysiging |
| MCP-US-035 | Core Selection By Config And Web | Later | US-024, US-034 | Kernkeuse via config/web gebruik dieselfde registry |
| MCP-US-036 | Core Selection By MIDI Channel | Later | US-008, US-034 | Kanaal-tot-kern-toewysing is dinamies en diagnosties sigbaar |
| MCP-US-037 | Concurrent Multi-Core Runtime | Later | US-035, US-036 | Minstens twee kerne loop binne ’n gemete CPU/RAM-begroting |
| MCP-US-038 | 6581 SID Core Spike | Later | US-034 | Akkuraatheidsdoel, filterbeperking en drie-stem-uitvoer is bewys |
| MCP-US-039 | SID File Local Playback | Later | US-038 | ’n begrensde SID-subset speel van plaaslike media |
| MCP-US-040 | SID File Remote Streaming | Later | US-023, US-039 | Bronlisensie, buffering, timeouts en veilige mislukking is bewys |
| MCP-US-041 | OPL2 Core Adapter | Later | US-034 | OPL2-register-/stemkontrak werk deur dieselfde router |
| MCP-US-042 | OPL3 Core Adapter | Later | US-041 | OPL3-vermoëns word sonder OPL2-regressie bygevoeg |

## MCP-EPIC-007 DSP And Pedal Hardware

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-043 | DSP Budget And Bypass | MVP | US-021, US-022 | Harde RAM/latensiegrens en klikvrye bypass is gemeet |
| MCP-US-044 | Lightweight Delay Echo | MVP-late | US-043 | Beperkte delay is hoorbaar, beheerbaar en MIDI-stabiel |
| MCP-US-045 | Lightweight Reverb Spike | MVP-late | US-043 | Eenvoudige reverb slaag die begroting of lewer ’n gedokumenteerde no-go |
| MCP-US-046 | Footswitch And Status LED | Later | US-004 | Debounce, bypass en LED-status werk sonder globale status |
| MCP-US-047 | Pedal Power And Audio Protection | Later | US-021 | Krag, vlakke, filtering en beskerming is geskematiseer en gemeet |
| MCP-US-048 | KiCad Reference PCB | Later | US-047 | Skematiese, PCB en BOM slaag ERC/DRC en bring-up-runbook |
| MCP-US-049 | External Audio Input Architecture | Parking lot | US-047 | ADC/codec, headroom en DSP-roete het ’n goedgekeurde ADR |

## MCP-EPIC-008 Portability, Quality And Release

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-050 | Host Simulator And Contract Tests | MVP | US-002, US-006 | Kern/MIDI/clock-toetse loop op macOS, Windows en Linux sonder bord |
| MCP-US-051 | Hardware-In-The-Loop Test Runner | MVP | US-003, US-015 | REPL, USB-MIDI en klankmeetstappe lewer ’n naspeurbare verslag |
| MCP-US-052 | Cross-Board Capability Profiles | Later | US-004 | ’n tweede CircuitPython-mikrobeheerder werk via ’n profiel |
| MCP-US-053 | Raspberry Pi Linux Blinka Adapter | Later | US-014, US-050 | Pi Zero/2/3 gebruik Linux/Blinka sonder om firmwareportabiliteit te beweer |
| MCP-US-054 | Windows USB MIDI Acceptance | MVP | US-003, US-007 | Toestel verskyn en ontvang note op ’n skoon Windows-rekenaar |
| MCP-US-055 | macOS Logic Pro Acceptance | MVP | US-003, US-007 | Logic stuur note/clock en ontvang ’n stabiele uitvoerpad |
| MCP-US-056 | Install Recovery And Diagnostics | MVP | US-005, US-051 | Beginner-runbook dek geen MIDI, geen klank, safe mode en herstel |
| MCP-US-057 | MVP Release Candidate And Demo | MVP | Alle MVP-stories | Tag, release notes, bekende beperkings en demo is gereed |

## Definition of Ready

- Gebruikerwaarde, afhanklikhede en nie-doelwitte is duidelik.
- Aanvaardingsbewys kan op host, bord of albei uitgevoer word.
- Benodigde hardeware en veiligheidsrisiko’s is bekend.
- Die voorafgaande stories in die afhanklikheidsketting is `Done` of 'n uitsondering is eksplisiet deur die Product Owner aanvaar.
- Die ontwerp wys watter klas elke stuk runtime-status besit en hoe afhanklikhede ingespuit word.
- Die plan bevat 'n rooi AST-/importtoets wanneer nuwe Python-modules geskep word.
- Elke virtuele spanrol het 'n bydrae of gemotiveerde `Not impacted`-inskrywing.
- Product Owner het die ongeveer 50-woord uitvoerplan aanvaar.

## Definition of Done

- Rooi toets is gedemonstreer of vooraf as verwagte mislukking vasgelê.
- Groen eenheid-/kontraktoetse slaag.
- Geen globale runtime-veranderlikes, `global`-statements of modulevlak helperfunksies is teenwoordig nie.
- Alle veranderlike status behoort aan klasinstansies; import begin geen synth, MIDI, audio, Wi-Fi, web- of borddiens nie.
- Die synthmodules kan as biblioteek ingevoer word en die weblaag kan afhanklikhede instansieer sonder outomatiese startup.
- Relevante hardewaretoets is deur mens of meetinstrument aanvaar.
- Dokumentasie, headers, backlog, ChatID en story-ID is bygewerk.
- Die span het bepaal of hierdie closure 'n drie-/vier-story lessons-learned-checkpoint aktiveer en dit, indien verskuldig, voltooi.
- Geen geheime, plaaslike konstantes of onbedoelde binêre lêers is gestage nie.
- Commit en push is voltooi; demo- teenoor produksestatus is eerlik.
