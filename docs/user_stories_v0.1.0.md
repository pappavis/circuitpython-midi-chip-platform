# User-story-katalogus

<!--
Bestand: user_stories_v0.1.0.md
Versienommer: 0.11.0
Doel: Volledige geordende backlog vir MVP en latere inkremente.
Sprint: Sprint 0
Epic: Alle epics
User-Story: MCP-US-008 MIDI Channel Router
Actienr: MCP-ACT-008-BACKLOG-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-008
-->

## Statuslegende

- **Done:** artefakte en bewys is gereed vir aanvaarding.
- **In Review:** implementering en outomatiese bewys is gereed vir menslike aanvaarding.
- **Impediment:** die aktiewe story kan nie finaal sluit voordat 'n gedokumenteerde eksterne of HIL-blokker herstel is nie.
- **Next:** logiese volgende story; nog nie begin nie.
- **MVP:** nodig vir die eerste aanvaarbare produkdemonstrasie.
- **Stretch:** slegs indien die vaste MVP stabiel en binne begroting is.
- **Later:** geprioritiseerde voortsetting ná MVP.

Die tabelvolgorde en eksplisiete afhanklikhede bepaal die implementeringsvolgorde; 'n later toegevoegde stabiele story-ID word nie hernommer om 'n kunsmatige numeriese volgorde te skep nie. `Synth` beteken in hierdie katalogus die CircuitPython MIDI Chip Platform.

## MCP-EPIC-001 Platform Foundation

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-001 | Device And Source Baseline Inventory | Done | - | Bord, bronne, rugsteun, risiko’s en hergebruik is gedokumenteer |
| MCP-US-002 | Clean Repository And Project Skeleton | Done | US-001 | Klasgebaseerde poorte, host-toetse en headers bestaan; geen toestel-I/O nie |
| MCP-US-003 | Minimal Safe Boot And USB Profile | Done | US-002 | USB-MIDI begin vóór runtime; bord-VID/PID bly verstek; CIRCUITPY/REPL herstel en drieledige device-proof slaag |
| MCP-US-004 | Board Capability Discovery | Done | US-002 | Profiel, IO3/5/7, modules, geheue en I2S-backend is fisies gerapporteer; power-cycle recovery en volledige manifest-HIL slaag |
| MCP-US-005 | Configuration And Secret Boundary | In Review | US-003 | Hostlektoetse en prioriteit is groen; fisiese deploy wag op herstel van leesalleen CIRCUITPY-media |

## MCP-EPIC-002 MIDI And Clock

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-006 | Portable NoteEvent And ControlEvent Model | In Review | US-002 | Note, CC, 14-bit bend en kanaallose clock het backend-onafhanklike klasse; 49 hosttoetse is groen |
| MCP-US-007 | USB MIDI Receive Loop | In Review | US-003, US-006 | Generiese Adafruit-vertaling en begrensde receive-loop is host-groen; fisiese Note On/Off wag op toesteltoegang |
| MCP-US-062 | BLE MIDI Transport And Capability Gate | Impediment (host ready) | US-006, US-007, US-052 | S2 se veilige negatiewe gate en gedeelde transportkontrak is groen; positiewe BLE-HIL wag op 'n werklike BLE-bord |
| MCP-US-008 | MIDI Channel Router | Done | US-007 | Kanaal 1-16 roeteer na konfigureerbare kerninstansies; clock en onbekende kanale bly veilig ongebonde |
| MCP-US-009 | Velocity And Note-Off Semantics | MVP | US-007 | Velocity nul sluit note; geen hangende stem ná All Notes Off nie |
| MCP-US-010 | Pitch Bend And CC1 Modulation | MVP | US-007 | Bend en vibrato word hoorbaar en diagnosties gemeet |
| MCP-US-058 | Guitar MIDI Bend And Slide Event Semantics | MVP | US-008, US-010 | Multi-kanaal note en per-kanaal bends behou onafhanklike string/slide-semantiek met konfigureerbare bend range |
| MCP-US-011 | Internal 120 BPM Clock | MVP | US-002 | Interne klok lewer stabiele 24 PPQN-afgeleides en BPM-metriek |
| MCP-US-012 | External MIDI Clock Sync | MVP | US-007, US-011 | USB of adapter-klok kan Start/Stop/Continue en tempo beheer |
| MCP-US-013 | Standalone DIN UART MIDI Transport | MVP | US-006 | 'n Eksterne USB-host se 5-pen DIN/UART-boodskappe gebruik dieselfde MidiInputPort en eventmodel |

## MCP-EPIC-003 Audio And Chip Core

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-014 | AudioOutput Port And Null Backend | MVP | US-002 | Kernlogika kan sonder fisiese klank host-getoets word |
| MCP-US-016 | MAX98357 Mono I2S Audible Diagnostic | MVP | US-004, US-014 | Een geprofileerde MAX98357 speel 'n veilige hoorbare toetssein; penne, RAM, latensie en dropout is gemeet |
| MCP-US-015 | PWM Diagnostic Fallback | MVP | US-004, US-014 | Gekose debugpenne lewer 'n meetbare fallback-sein wanneer I2S nie beskikbaar is nie |
| MCP-US-063 | Portable D1 Baseline Synth Core | MVP | US-006, US-014, US-016 | Nuut-geporteerde sine/saw/square D1-gedrag speel via AudioOutput met Note/CC/bend; geen desktop-backend of produksierepo-wysiging nie |
| MCP-US-017 | SN76489-Lite Three-Voice Core | MVP | US-063 | Drie toonstemme speel onafhanklik met gedokumenteerde akkuraatheid |
| MCP-US-018 | Voice Allocation And Stealing | MVP | US-017 | Vierde noot volg ’n toetsbare steal-policy sonder vasloop |
| MCP-US-020 | Optional G-C-D Startup Test | MVP | US-016, US-063 | Opsionele sestiendenootreeks bewys die mono-I2S-klankpad by start |
| MCP-US-019 | Per-Voice Left Right Stereo Routing | MVP | US-016, US-017, US-021 | Elke stem kan links, regs of stereo gemonitor word |
| MCP-US-021 | Stereo I2S Expansion Decision | MVP | US-015, US-016 | HIL kies twee MAX98357-modules of 'n stereo-I2S-backend; PWM bly fallback |

## MCP-EPIC-004 Local Web Control

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-022 | Cooperative Runtime Scheduler | MVP | US-007, US-014 | MIDI, klank en web-polling deel tyd sonder hoorbare blokkasie |
| MCP-US-023 | Safe Wi-Fi Station And AP Fallback Service | MVP | US-005, US-022 | Runtime join ’n gekonfigureerde netwerk binne timeout en rapporteer station-IP; by mislukking begin ’n beveiligde AP en rapporteer AP-IP sonder MIDI-/klankblokkasie |
| MCP-US-024 | Mobile-Friendly Local Web Status And Parameters | MVP | US-023 | Een mobiele plaaslike kliënt lees status en verander veilige parameters in station/AP-modus; polling/logging bly spaarsaam en koersbegrens |
| MCP-US-025 | Browser Virtual MIDI Keyboard | MVP | US-024 | Klik/touch stuur note via dieselfde event-model |
| MCP-US-026 | Simple Step Sequencer | MVP | US-011, US-024 | ’n Kort patroon kan teen interne/eksterne klok loop en stop |
| MCP-US-027 | Web Security And Recovery | MVP | US-024 | Vertroude-LAN/AP-grens, private credentials, sessielimiet, netwerkafskakeling en herstelpad is getoets |

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
| MCP-US-035 | Core Selection By Config And Web | MVP-late | US-024, US-034 | Kernkeuse via config/web gebruik dieselfde registry |
| MCP-US-036 | Core Selection By MIDI Channel | MVP-late | US-008, US-034 | Kanaal-tot-kern-toewysing is dinamies en diagnosties sigbaar |
| MCP-US-037 | Concurrent Multi-Core Runtime | MVP-late | US-035, US-036 | Minstens twee verskillende kerninstansies loop parallel binne 'n gemete CPU/RAM/latensiebegroting |
| MCP-US-061 | Multi-Core Resource Guard And Telemetry | MVP-late | US-037 | Heap, looplatensie en dropout word gemeet; onveilige addisionele kern word deterministies geweier of afgeskakel |
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
| MCP-US-051 | Hardware-In-The-Loop Test Runner | In Review | US-003, US-015 | Connection/deploy/execution-runner is groen; USB-MIDI is bewys en die klankmeetadapter volg ná US-015/016 |
| MCP-US-052 | Cross-Board Capability Profiles | MVP | US-004 | ’n tweede BLE-geskikte CircuitPython-mikrobeheerder werk via ’n profiel sonder S2-regressie |
| MCP-US-053 | Raspberry Pi Linux Blinka Adapter | Later | US-014, US-050 | Pi Zero/2/3 gebruik Linux/Blinka sonder om firmwareportabiliteit te beweer |
| MCP-US-054 | Windows USB MIDI Acceptance | MVP | US-003, US-007 | Toestel verskyn en ontvang note op ’n skoon Windows-rekenaar |
| MCP-US-055 | macOS Logic Pro Acceptance | MVP | US-003, US-007 | Logic kies die synth as External MIDI destination en stuur note/clock; fisiese pedaaluitvoer bly die klankpad |
| MCP-US-056 | Install Recovery And Diagnostics | MVP | US-005, US-051 | Beginner-runbook dek geen MIDI, geen klank, safe mode en herstel |
| MCP-US-059 | MIDI Guitar Hardware Acceptance | MVP | US-018, US-058 | 'n Generiese MIDI-kitaar en Fishman-verwysing speel note, akkoorde, bends en slides; geen toestelnaam is 'n kodekonstante nie |
| MCP-US-060 | Standalone External MIDI Host Acceptance | MVP | US-013, US-017 | Controller na Raspberry Pi/eksterne USB-host na DIN/UART lewer note, bend en clock sonder DAW |
| MCP-US-057 | MVP Release Candidate And Demo | MVP | Alle MVP-stories | Tag, release notes, bekende beperkings en demo is gereed |

## Definition of Ready

- Gebruikerwaarde, afhanklikhede en nie-doelwitte is duidelik.
- Aanvaardingsbewys kan op host, bord of albei uitgevoer word.
- Benodigde hardeware en veiligheidsrisiko’s is bekend.
- Elke ESP32-HIL-plan beskryf bedradings-/kragvoorwaardes, deploy, stimulus, verwagte REPL/LED/klank/meetuitvoer, pass/fail en herstelstappe.
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
- Fisiese werk toon, waar van toepassing, Connection, Deployment en Execution Proof sonder UID-, MAC-, SSID- of geheime-lekkasie.
- Dokumentasie, headers, backlog, ChatID en story-ID is bygewerk.
- Startup toon die huidige projekweergawe, aktiewe story/amendment en release-datum.
- Die span het bepaal of hierdie closure 'n drie-/vier-story lessons-learned-checkpoint aktiveer en dit, indien verskuldig, voltooi.
- Geen geheime, plaaslike konstantes of onbedoelde binêre lêers is gestage nie.
- Commit en push is voltooi; demo- teenoor produksestatus is eerlik.
