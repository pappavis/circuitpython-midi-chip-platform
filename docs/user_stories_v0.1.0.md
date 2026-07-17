# User-story-katalogus

<!--
Bestand: user_stories_v0.1.0.md
Versienommer: 0.30.0
Doel: Volledige geordende backlog met US-077 realtime-baseline in review.
Sprint: Sprint 2
Epic: Alle epics
User-Story: MCP-US-055 en MCP-US-077
Actienr: MCP-ACT-077-IMP-001-GREEN-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-IMPEDIMENT-001
-->

## Statuslegende

- **Done:** artefakte en bewys is gereed vir aanvaarding.
- **In Review:** implementering en outomatiese bewys is gereed vir menslike aanvaarding.
- **Impediment:** die aktiewe story kan nie finaal sluit voordat 'n gedokumenteerde eksterne of HIL-blokker herstel is nie.
- **Next:** logiese volgende story; nog nie begin nie.
- **MVP-Must:** direkte eindgebruikerbewys binne die bevrore acceptance set.
- **MVP-Enabler:** noodsaaklike tegniese of kwaliteitsvoorwaarde binne dieselfde set.
- **Post-MVP:** waardevolle voortsetting wat nie die eerste release blokkeer nie.
- **Stretch:** slegs indien die vaste MVP stabiel en binne begroting is.
- **Later:** geprioritiseerde voortsetting ná MVP.

Die tabelvolgorde en eksplisiete afhanklikhede bepaal die implementeringsvolgorde; 'n later toegevoegde stabiele story-ID word nie hernommer om 'n kunsmatige numeriese volgorde te skep nie. `Synth` beteken in hierdie katalogus die CircuitPython MIDI Chip Platform.

## Bevrore MVP Acceptance Set

Slegs `MCP-US-001`, `US-002`, `US-003`, `US-004`, `US-005`, `US-006`, `US-007`, `US-008`, `US-009`, `US-014`, `US-016`, `US-050`, `US-051`, `US-055`, `US-057`, `US-063`, `US-075` en die P0-herstelstory `US-077` beheer MVP-aanvaarding. Die produkbewys is USB-MIDI uit Logic Pro na 'n hoorbare D1-basiskern op die verwysingsbord met begrensde digitale volume. US-077 is geen scope-uitbreiding nie; dit is die terug-na-basics realtime-baseline wat US-055 moet deblokkeer. US-075 se fisiese prototipe-las is deur 'n eksplisiete PO-uitondering aanvaar; US-076 is verpligtend voor 'n produksieveiligheidsclaim. Alle ander stories is reeds voltooide ekstra werk, governance of post-MVP voortsetting.

## MCP-EPIC-001 Platform Foundation

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-001 | Device And Source Baseline Inventory | MVP-Enabler (Done) | - | Bord, bronne, rugsteun, risiko’s en hergebruik is gedokumenteer |
| MCP-US-002 | Clean Repository And Project Skeleton | MVP-Enabler (Done) | US-001 | Klasgebaseerde poorte, host-toetse en headers bestaan; geen toestel-I/O nie |
| MCP-US-003 | Minimal Safe Boot And USB Profile | MVP-Enabler (Done) | US-002 | USB-MIDI begin vóór runtime; bord-VID/PID bly verstek; CIRCUITPY/REPL herstel en drieledige device-proof slaag |
| MCP-US-004 | Board Capability Discovery | MVP-Enabler (Done) | US-002 | Profiel, IO3/5/7, modules, geheue en I2S-backend is fisies gerapporteer; power-cycle recovery en volledige manifest-HIL slaag |
| MCP-US-005 | Configuration And Secret Boundary | Done | US-003 | Hostlektoetse plus Wemos v0.12.3 bewys `PASS`, drie leë private velde as `UNSET` en device execution as `READY` sonder waardelek |

## MCP-EPIC-002 MIDI And Clock

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-006 | Portable NoteEvent And ControlEvent Model | MVP-Enabler (Done) | US-002 | Product Owner het die draagbare Note/CC/bend/clock-model binne die volledige hosttoetsstel aanvaar |
| MCP-US-007 | USB MIDI Receive Loop | MVP-Enabler (Done) | US-003, US-006 | v0.12.2 ontvang fisies USB-MIDI vanaf Logic/CoreMIDI; die toestel rapporteer Note On, Note Off en 'n ooreenstemmende nootpaar as PASS |
| MCP-US-062 | BLE MIDI Transport And Capability Gate | Post-MVP (S2 negative accepted) | US-006, US-007, US-052 | S2 se veilige negatiewe gate is aanvaar; positiewe BLE-HIL wag op 'n werklike BLE-bord |
| MCP-US-008 | MIDI Channel Router | MVP-Enabler (Done) | US-007 | Kanaal 1-16 roeteer na konfigureerbare kerninstansies; clock en onbekende kanale bly veilig ongebonde |
| MCP-US-009 | Velocity And Note-Off Semantics | MVP-Enabler (Done) | US-007 | Velocity nul, Note Off, CC120 en CC123 sluit aktiewe note per kanaal deterministies |
| MCP-US-010 | Pitch Bend And CC1 Modulation | Post-MVP (host accepted) | US-007, US-063 | Per-kanaal bend/CC1-berekening is aanvaar; hoorbare bend/vibrato volg ná die D1-MVP |
| MCP-US-058 | Guitar MIDI Bend And Slide Event Semantics | Post-MVP | US-008, US-010 | Multi-kanaal note en per-kanaal bends behou onafhanklike string/slide-semantiek met konfigureerbare bend range |
| MCP-US-011 | Internal 120 BPM Clock | Post-MVP | US-002 | Interne klok lewer stabiele 24 PPQN-afgeleides en BPM-metriek |
| MCP-US-012 | External MIDI Clock Sync | Post-MVP | US-007, US-011 | USB of adapter-klok kan Start/Stop/Continue en tempo beheer |
| MCP-US-013 | Standalone DIN UART MIDI Transport | Post-MVP | US-006 | 'n Eksterne USB-host se 5-pen DIN/UART-boodskappe gebruik dieselfde MidiInputPort en eventmodel |

## MCP-EPIC-003 Audio And Chip Core

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-014 | AudioOutput Port And Null Backend | Done | US-002 | Blokgebaseerde mono/stereo signed-16 PCM-kontrak, Null/Memory-backends, application-integrasie en dependency-closed manifest slaag 99 hosttoetse sonder fisiese klankclaim |
| MCP-US-016 | Standalone I2S Audible Diagnostic (MAX98357 Default) | Done | US-004, US-014 | Product Owner het op Wemos S2 hoorbare G3-C4-D4 mono-klank bevestig; serial `PASS`, 103 hosttoetse en heap 2056512->2056192 is bewys. Lang burn-in word onder US-051/US-057 voltooi |
| MCP-US-015 | PWM Diagnostic Fallback | Post-MVP/contingency | US-004, US-014 | Gekose debugpenne lewer 'n meetbare fallback-sein wanneer I2S nie beskikbaar is nie |
| MCP-US-063 | Portable D1 Baseline Synth Core | Done | US-006, US-008, US-009, US-014, US-016 | Product Owner het v0.15.0 se sine/saw/square `d1-diagnose`, A4=440 Hz, velocity en PASS aanvaar; hoorbare Logic/I2S en lang smoke volg onder US-055/US-051 |
| MCP-US-017 | SN76489-Lite Three-Voice Core | Post-MVP | US-063, US-057 | Drie toonstemme speel onafhanklik met gedokumenteerde akkuraatheid |
| MCP-US-018 | Voice Allocation And Stealing | Post-MVP | US-017 | Vierde noot volg 'n toetsbare steal-policy sonder vasloop |
| MCP-US-020 | Optional Integrated G-C-D Startup Test | Post-MVP | US-016, US-063 | Opsionele sestiendenootreeks gebruik die D1/runtime-klankpad; dit is nie die onafhanklike US-016 hardewarediagnose nie |
| MCP-US-019 | Per-Voice Left Right Stereo Routing | Post-MVP | US-016, US-017, US-021 | Elke stem kan links, regs of stereo gemonitor word |
| MCP-US-021 | Stereo I2S Expansion Decision | Post-MVP | US-015, US-016 | HIL kies twee MAX98357-modules of 'n stereo-I2S-backend; PWM bly fallback |

## MCP-EPIC-004 Local Web Control

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-022 | Cooperative Runtime Scheduler | Post-MVP | US-007, US-014 | MIDI, klank en web-polling deel tyd sonder hoorbare blokkasie |
| MCP-US-023 | Safe Wi-Fi Station And AP Fallback Service | Post-MVP | US-005, US-022 | Startup rapporteer hostname, `station` plus station-IP, of veilige `ap-fallback` plus AP-IP; join/fallback is begrens, redigeer geheime en blokkeer nie MIDI/klank nie |
| MCP-US-024 | Mobile-Friendly Local Web Status And Parameters | Post-MVP | US-023 | Een mobiele plaaslike kliënt lees status en verander veilige parameters in station/AP-modus; polling/logging bly spaarsaam en koersbegrens |
| MCP-US-025 | Browser Virtual MIDI Keyboard | Post-MVP | US-024 | Klik/touch stuur note via dieselfde event-model |
| MCP-US-026 | Simple Step Sequencer | Post-MVP | US-011, US-024 | 'n Kort patroon kan teen interne/eksterne klok loop en stop |
| MCP-US-027 | Web Security And Recovery | Post-MVP | US-024 | Vertroude-LAN/AP-grens, private credentials, sessielimiet, netwerkafskakeling en herstelpad is getoets |

## MCP-EPIC-005 Files, Harmony And Performance Tools

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-028 | Constrained MIDI File Parser | Later | US-006, US-011 | Ondersteunde formaat en gebeurtenislimiete faal veilig |
| MCP-US-029 | Chip-Aware MIDI File Playback | Later | US-017, US-028 | Oortollige note word volgens die kern se stemlimiet hanteer |
| MCP-US-030 | Local Media File Browser | Later | US-024, US-028 | Gebruiker kies ’n plaaslike MIDI-lêer sonder kodewysiging |
| MCP-US-031 | Arpeggiator | Stretch | US-011, US-017 | Up/down/random patrone volg BPM en note-off |
| MCP-US-032 | Chord Progression Generator | Stretch | US-026 | Sleutel, progressie, BPM en random seed is beheerbaar |
| MCP-US-033 | Patch Save Load And Factory Reset | Post-MVP | US-005, US-024 | Geldige patch bly ná reboot; korrupsie val terug na veilige verstek |

## MCP-EPIC-006 Multi-Core Expansion

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-034 | SynthCore Interface And Registry | Post-MVP | US-002, US-017 | Kern kan via registrasienaam gekies word sonder routerwysiging |
| MCP-US-035 | Core Selection By Config And Web | Post-MVP | US-024, US-034 | Kernkeuse via config/web gebruik dieselfde registry |
| MCP-US-036 | Core Selection By MIDI Channel | Post-MVP | US-008, US-034 | Kanaal-tot-kern-toewysing is dinamies en diagnosties sigbaar |
| MCP-US-037 | Concurrent Multi-Core Runtime | Post-MVP | US-035, US-036 | Minstens twee verskillende kerninstansies loop parallel binne 'n gemete CPU/RAM/latensiebegroting |
| MCP-US-061 | Multi-Core Resource Guard And Telemetry | Post-MVP | US-037 | Heap, looplatensie en dropout word gemeet; onveilige addisionele kern word deterministies geweier of afgeskakel |
| MCP-US-038 | 6581 SID Core Spike | Later | US-034 | Akkuraatheidsdoel, filterbeperking en drie-stem-uitvoer is bewys |
| MCP-US-039 | SID File Local Playback | Later | US-038 | ’n begrensde SID-subset speel van plaaslike media |
| MCP-US-040 | SID File Remote Streaming | Later | US-023, US-039 | Bronlisensie, buffering, timeouts en veilige mislukking is bewys |
| MCP-US-041 | OPL2 Core Adapter | Later | US-034 | OPL2-register-/stemkontrak werk deur dieselfde router |
| MCP-US-042 | OPL3 Core Adapter | Later | US-041 | OPL3-vermoëns word sonder OPL2-regressie bygevoeg |

## MCP-EPIC-007 DSP And Pedal Hardware

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-043 | DSP Budget And Bypass | Post-MVP | US-021, US-022 | Harde RAM/latensiegrens en klikvrye bypass is gemeet |
| MCP-US-044 | Lightweight Delay Echo | Post-MVP | US-043 | Beperkte delay is hoorbaar, beheerbaar en MIDI-stabiel |
| MCP-US-045 | Lightweight Reverb Spike | Post-MVP | US-043 | Eenvoudige reverb slaag die begroting of lewer 'n gedokumenteerde no-go |
| MCP-US-046 | Footswitch And Status LED | Later | US-004 | Debounce, bypass en LED-status werk sonder globale status |
| MCP-US-047 | Pedal Power, Safe Volume And Audio Protection | Later | US-021, US-075 | Krag, speaker/headphone/line-out-grense, gain/attenuasie, mute, filtering, ESD/polariteit en beskerming is op breadboard geskematiseer en met veilige testpunte gemeet |
| MCP-US-048 | KiCad Reference Pedal PCB | Later | US-047 | Die Hardware Engineer en ervare KiCad Product Owner lewer skema, PCB, footprints, testpunte en BOM; ERC/DRC, bring-up en vervaardigingsuitsette slaag |
| MCP-US-075 | Safe Development Audio Load And Volume Gate | Done (PO exception) | US-016, US-063 | v0.16.0 se `0.08` gain, `0.25` plafon, startup mute, 120 hosttoetse en hoorbare G-C-D HIL slaag; die PO aanvaar die tydelike TRS-prototiperisiko sonder produksieveiligheidsclaim |
| MCP-US-076 | Certified Speaker, Headphone And Pedal Output Cleanup | Later | US-047, US-075 | Afsonderlike speaker-, headphone- en pedal/line-out-paaie het geskikte impedansie, gain, mute, beskerming, meetpunte en HIL; geen direkte BTL-na-TRS produksiepad nie |
| MCP-US-049 | External Audio Input Architecture | Parking lot | US-047 | ADC/codec, headroom en DSP-roete het ’n goedgekeurde ADR |

## MCP-EPIC-008 Portability, Quality And Release

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-050 | Host Simulator And Contract Tests | MVP-Enabler | US-002, US-006 | Kern/MIDI/klankkontrakte loop op macOS, Windows en Linux sonder bord |
| MCP-US-051 | Hardware-In-The-Loop Test Runner | MVP-Enabler (In Review) | US-003, US-016 | Autoreload-safe deploy, closure, libraries, boot en import/execution is fisies groen; die klankadapter voeg rate-limited heap/reset/dropout-burn-intelemetrie by |
| MCP-US-052 | Cross-Board Capability Profiles | Post-MVP | US-004 | 'n tweede BLE-geskikte CircuitPython-mikrobeheerder werk via 'n profiel sonder S2-regressie |
| MCP-US-053 | Raspberry Pi Linux Blinka Adapter | Later | US-014, US-050 | Pi Zero/2/3 gebruik Linux/Blinka sonder om firmwareportabiliteit te beweer |
| MCP-US-054 | Windows USB MIDI Acceptance | Post-MVP | US-003, US-007 | Toestel verskyn en ontvang note op 'n skoon Windows-rekenaar |
| MCP-US-055 | macOS Logic Pro Audible D1 Acceptance | MVP-Must (P0 Impediment) | US-003, US-007, US-009, US-014, US-016, US-063, US-075, US-077 | v0.17.8 verbind USB-MIDI, D1 en veilige I2S op host, maar sewe menslike HIL-pogings het nie betroubare realtime Logic-klank bewys nie. Closure wag op US-077 en daarna 'n Product Owner HIL-pass |
| MCP-US-077 | Realtime MIDI Audio Baseline Spike | MVP-Enabler (In Review / HIL Retest Ready) | US-007, US-016, US-075 | v0.18.1 voeg 'n boot-audition en stiller serial defaults by nadat NoteOn-start intern `0-16 ms` gemeet het maar hoorbaar 12s laat was; 144 hosttoetse slaag. Closure wag op Product Owner HIL: boot-audition en Logic NoteOn moet onmiddellik hoorbaar wees |
| MCP-US-056 | Install Recovery And Diagnostics | Post-MVP | US-005, US-051 | Beginner-runbook dek geen MIDI, geen klank, safe mode en herstel |
| MCP-US-068 | Stable USB MIDI Instance Identity | Post-MVP | US-003, US-004, US-055 | Elke toestel exposeer 'n herkenbare produknaam plus stabiele vier-karakter instance-ID; twee toestelle is onderskeibaar sonder UID/MAC-lekkasie |
| MCP-US-059 | MIDI Guitar Hardware Acceptance | Post-MVP | US-018, US-058 | 'n Generiese MIDI-kitaar en Fishman-verwysing speel note, akkoorde, bends en slides; geen toestelnaam is 'n kodekonstante nie |
| MCP-US-060 | Standalone External MIDI Host Acceptance | Post-MVP | US-013, US-017 | Controller na Raspberry Pi/eksterne USB-host na DIN/UART lewer note, bend en clock sonder DAW |
| MCP-US-057 | MVP Release Candidate And Demo | MVP-Must | US-001 tot US-009, US-014, US-016, US-050, US-051, US-055, US-063, US-075 | Tag, release notes, bekende beperkings en 'n geslaagde 8-uur burn-inverslag vergesel die herhaalbare Logic USB-MIDI na hoorbare D1-demo |

## MCP-EPIC-009 Framework Engineering

Hierdie epic beheer hoe mense en agente projekkennis laai, besluite neem en bewys lewer. Dit is governance, nie 'n tweede firmware-runtime nie.

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-064 | Enterprise Vision And Architecture Baseline | Done | US-001, US-002 | Enterprise-visie, framework-, solution- en deployment-argitektuur vorm een gekruisverwysde baseline |
| MCP-US-065 | Enterprise Meta Model, Glossary And Artefact Taxonomy | Done | US-064 | Rolle, stories, komponente, toetse, risiko's en besluite het benoemde verhoudings en eienaars |
| MCP-US-066 | Quality Manual, Test Strategy And Review Engine | Done | US-064, US-065 | Definition of Done verwys na herhaalbare quality-, test- en reviewhekke sonder dokumentasie-as-bewys |
| MCP-US-067 | Prompt Compiler, Context Loader And Knowledge Base Structure | Done | US-065, US-066 | Agente laai minimale bronkonteks, behou instruksieprioriteit en lewer naspeurbare story-pakkette; geen runtime-LLM-afhanklikheid nie |

## MCP-EPIC-010 Physical Chip And Display Expansion

Hierdie epic is doelbewus **ná MVP**. Dit verander nie die huidige hoorbare volgorde `US-014 -> US-016 -> US-063 -> US-075 -> US-055 -> US-057` nie en maak geen elektriese aanspraak voordat die betrokke fisiese chip en breakout gemeet is nie.

| ID | User story | Fase | Afhanklikheid | Kern-aanvaardingsbewys |
|---|---|---|---|---|
| MCP-US-069 | External I2C Status Display Adapter | Later | US-004, US-022 | Capability-gated SSD1306/soortgelyke adapter toon beperkte status en debugdata koersbegrens; afwesige display verander nie synthgedrag nie |
| MCP-US-070 | Physical Chip Transport And Capability Abstraction | Later | US-004, US-034 | Klasgebaseerde transportpoorte dek direkte GPIO, I2C-expander en SPI sonder chip-/penkonstantes; ontdekking is veilig, geïnjekteer en toetsbaar |
| MCP-US-071 | Physical SN76489 Hardware Adapter | Later | US-017, US-070 | Bevestigde chip-identiteit, vlakke, klok en bussekwensies stuur note na die fisiese chip; mislukking val terug na emulasie |
| MCP-US-072 | Physical SID6581 Feasibility And Adapter | Later | US-038, US-070 | Chip Engineer keur voeding, vlakke, klok, registerbus en analooguitvoer goed voor implementering; ondersteunde pad faal veilig terug na emulasie |
| MCP-US-073 | ArduinoOPL2 SPI Hardware Adapter | Later | US-041, US-070 | Die DhrBaksteen-bord se SPI-kontrak word teen sy bron en werklike HIL gevalideer sonder om emulatorlogika aan die buslaag te bind |
| MCP-US-074 | Emulated Or Physical Core Backend Selection And Fallback | Later | US-034, US-070, een fisiese chipadapter | Config/web kies per kern `emulated` of `physical`; emulasie is altyd verstek en fallback, en fisiese modus render nie ’n tweede plaaslike kopie nie |

## Definition of Ready

- Gebruikerwaarde, afhanklikhede en nie-doelwitte is duidelik.
- Aanvaardingsbewys kan op host, bord of albei uitgevoer word.
- Benodigde hardeware en veiligheidsrisiko’s is bekend.
- Elke ESP32-HIL-plan beskryf bedradings-/kragvoorwaardes, deploy, stimulus, verwagte REPL/LED/klank/meetuitvoer, pass/fail en herstelstappe.
- Die voorafgaande stories in die afhanklikheidsketting is `Done` of 'n uitsondering is eksplisiet deur die Product Owner aanvaar.
- Die ontwerp wys watter klas elke stuk runtime-status besit en hoe afhanklikhede ingespuit word.
- Die plan bevat 'n rooi AST-/importtoets wanneer nuwe Python-modules geskep word.
- Elke virtuele spanrol het 'n bydrae of gemotiveerde `Not impacted`-inskrywing.
- Hostopdragte gebruik 'n bevestigde Python 3.11+ virtual environment; `/usr/bin/python` en kaal onbevestigde `python` is nie projekgereedskap nie.
- Product Owner het die ongeveer 50-woord uitvoerplan aanvaar.
- Die story verklaar `Burn-in: Required` met profiel of `Burn-in: N/A` met 'n gemotiveerde rede.

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
- Vereiste burn-in en heap-lek-aanvaarding is geslaag en aan die story review gekoppel.
- MVP-aanvaarding word slegs teen die bevrore Acceptance Set beoordeel; 'n historiese `Must`-etiket of voltooide ekstra funksie verbreed dit nie.
