# MCP-US-080-INV-001 Locate First Disappearance Of NoteOn

<!--
Bestand: mcp_us_080_inv_001_locate_first_disappearance_of_noteon_v0.1.0.md
Versienommer: 0.2.0
Doel: Definieer die P0 investigation story wat deur observasie en meting bepaal waar NoteOn eerste in die MIDI-keten verdwyn.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-080-INV-001 Locate First Disappearance Of NoteOn
Actienr: MCP-ACT-080-INV-001-STORY-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-INV-001
-->

## Story

As Product Owner wil ek objektief vasstel waar in die volledige Logic Pro na S2 synth-keten die eerste `NoteOn` verdwyn, sodat die volgende stap op meetdata gebaseer is en nie op spekulasie nie.

## Story Type

`INVESTIGATION STORY`

Hierdie story is geen implementasie-, bugfix-, refactor-, cleanup- of performance-story nie.

## Agtergrond

Die huidige HIL-bewys toon:

- USB MIDI kommunikasie bestaan;
- MCP-US-080 ontvang slegs `Control Change 7 value 0`;
- geen `NoteOn` events is gesien nie;
- geen `NoteOff` events is gesien nie;
- Logic Pro speel geen hoorbare note op die S2 nie;
- 'n vroeëre implementering het wel hoorbare note gespeel;
- `REG-080-001` verklaar hierdie toestand as aktiewe P0-regressie.

Die root cause is `UNKNOWN`. Enige fix op hierdie punt is spekulasie.

## Doel

Bepaal presies:

1. waar die laaste korrekte `NoteOn` objektief gesien word;
2. waar die eerste ontbrekende `NoteOn` objektief vasgestel word.

Daardie punt heet:

```text
FIRST_DISAPPEARANCE_OF_NOTEON
```

## Nie-Doelwitte

Hierdie story mag nie:

- fixes uitvoer nie;
- refactoring uitvoer nie;
- optimaliseer nie;
- bestaande funksionaliteit verander nie;
- D1 audio verbeter nie;
- synthio/I2S gedrag verander nie;
- Logic Pro workaround-code byvoeg nie;
- host-toetse groen maak deur hardewaregedrag weg te steek nie.
- fixadvies, argitektuurvoorstel of implementasiekeuse as Done-uitset lewer nie.

## Toegestane Werk

Slegs die volgende is toegelaat:

- logging;
- tracing;
- diagnostiek;
- meetpunte;
- observasie;
- dokumentasie;
- HIL-instrumentasie;
- tydelike debug-uitvoer.

Alle instrumentasie moet begrens, identifiseerbaar en tydelik wees. Instrumentasie is alleen toelaatbaar wanneer dit nodig is om te observeer, te meet, te lokaliseer of objektief te bewys waar `NoteOn` eerste verdwyn.

## Onderzoeksketen

| Stap | Meetlocatie | Vraag | Mogelijke conclusie |
|---|---|---|---|
| 1 | Logic Pro region/track | Wordt `NoteOn` uit Logic verwacht? | `NOTE_EXPECTED` of `UNKNOWN` |
| 2 | macOS CoreMIDI sender | Ziet macOS een uitgaande `NoteOn` naar S2? | `NOTEON_PRESENT`, `NOTEON_ABSENT` of `UNKNOWN` |
| 3 | USB MIDI Host routing | Gaat de host naar de juiste S2-destination/endpoint? | `ROUTE_MATCH`, `ROUTE_MISMATCH` of `UNKNOWN` |
| 4 | USB Endpoint 0 | Komt raw/decoded MIDI op endpoint 0 aan? | `NOTEON_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS` of `UNKNOWN` |
| 5 | USB Endpoint 1 | Komt raw/decoded MIDI op endpoint 1 aan? | `NOTEON_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS` of `UNKNOWN` |
| 6 | CircuitPython USB stack | Levert `usb_midi.ports` events aan runtime? | `NOTEON_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS` of `UNKNOWN` |
| 7 | `adafruit_midi` | Decodeert de library `NoteOn` correct? | `NOTEON_PRESENT`, `CONTROL_ONLY`, `DECODE_FAIL` of `UNKNOWN` |
| 8 | MIDI receive loop | Ziet de applicatieloop `NoteOn`? | `NOTEON_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS` of `UNKNOWN` |
| 9 | Router | Ontvangt de router `NoteOn`? | `NOTEON_PRESENT`, `FILTERED`, `NO_EVENTS` of `UNKNOWN` |
| 10 | Synth dispatcher | Wordt `NoteOn` naar D1 dispatch gestuurd? | `DISPATCHED`, `DROPPED`, `NO_EVENTS` of `UNKNOWN` |
| 11 | D1 Synth | Ontvangt de D1-kern een note trigger? | `TRIGGER_PRESENT`, `TRIGGER_ABSENT` of `UNKNOWN` |
| 12 | I2S | Wordt audio gestart voor die note? | `AUDIO_STARTED`, `AUDIO_ABSENT` of `UNKNOWN` |
| 13 | Speaker/load | Is het resultaat hoorbaar of meetbaar? | `AUDIBLE`, `MEASURABLE_ONLY`, `SILENT` of `UNKNOWN` |

## Meetpunten

| Meetpunt | Trace marker | Noodzaak |
|---|---|---|
| Logic Pro teststimulus | `TRACE_STAGE=LOGIC_PRO_TEST_STIMULUS` | Bevestigt dat de menselijke test exact C4/E4/G4 of live notes probeert te sturen |
| CoreMIDI host sender | `TRACE_STAGE=COREMIDI_HOST_SEND` | Observeert of een `NoteOn` vóór de device-grens meetbaar is; zonder dit bewijs blijft de hostlaag `UNKNOWN` |
| USB destination mapping | `TRACE_STAGE=USB_HOST_DESTINATION` | Bevestigt welke S2 endpoint/destination door macOS/Logic wordt gebruikt |
| USB endpoint per port | `TRACE_STAGE=USB_ENDPOINT;port_index=N` | Vangt verkeerde endpointselectie en duplicate/control-only poorten af |
| CircuitPython port read | `TRACE_STAGE=CIRCUITPY_USB_STACK;port_index=N` | Bewijst of CircuitPython bytes/events per poort aanbiedt |
| `adafruit_midi` decode | `TRACE_STAGE=ADAFRUIT_MIDI_DECODE;port_index=N` | Bewijst of decoded eventtypes verdwijnen tijdens library parsing |
| Receive loop | `TRACE_STAGE=MIDI_RECEIVE;port_index=N` | Bewijst of de eigen loop de decoded notes ziet |
| Router | `TRACE_STAGE=ROUTER` | Bewijst of kanaal-/eventfiltering notes laat vallen |
| Synth dispatcher | `TRACE_STAGE=SYNTH_DISPATCH` | Bewijst of MIDI-events de synth-control laag bereiken |
| D1 trigger | `TRACE_STAGE=D1_SYNTH` | Bewijst of het D1-pad een trigger krijgt |
| I2S start | `TRACE_STAGE=I2S` | Bewijst of audio-uitvoer gestart wordt |
| Speaker/load | `TRACE_STAGE=SPEAKER` | Menselijke/meterobservatie; firmware mag dit niet zelf claimen zonder HIL |

## Instrumentatiegrens

Alle tracepoints en meetinstrumentatie zijn:

- tijdelijk;
- debug-only;
- bounded;
- eenvoudig deactiveerbaar of verwijderbaar;
- zonder wijziging van productgedrag;
- zonder wijziging van routing;
- zonder wijziging van timingstrategie;
- zonder wijziging van eventsemantiek;
- zonder wijziging van audio;
- zonder wijziging van D1-functionaliteit.

Tracepoints zijn observatiehulpmiddelen. Zij vormen geen productarchitectuur, geen nieuwe feature en geen permanente runtime-eis.

## Verwachte Output

### Logic/CoreMIDI meetpunt

```text
TRACE_STAGE=COREMIDI_HOST_SEND;destination=<redacted>;event=note_on;channel=1;note=60;velocity=80;status=NOTEON_PRESENT
TRACE_STAGE=COREMIDI_HOST_SEND;destination=<redacted>;event=note_off;channel=1;note=60;velocity=64;status=NOTEOFF_PRESENT
```

Indien niet meetbaar:

```text
TRACE_STAGE=COREMIDI_HOST_SEND;status=UNKNOWN;reason=no_host_probe_available
```

### USB endpoint meetpunt

```text
TRACE_STAGE=USB_ENDPOINT;port_index=0;note_on=1;note_off=1;cc=0;clock=0;unknown=0;status=NOTEON_PRESENT
TRACE_STAGE=USB_ENDPOINT;port_index=1;note_on=0;note_off=0;cc=32;clock=0;unknown=0;status=CONTROL_ONLY
```

### CircuitPython / `adafruit_midi` meetpunt

```text
TRACE_STAGE=ADAFRUIT_MIDI_DECODE;port_index=0;event=note_on;channel=1;note=60;velocity=80;status=NOTEON_PRESENT
```

### Receive/router/dispatcher meetpunten

```text
TRACE_STAGE=MIDI_RECEIVE;event=note_on;channel=1;note=60;velocity=80;status=NOTEON_PRESENT
TRACE_STAGE=ROUTER;event=note_on;channel=1;note=60;route=d1;status=FORWARDED
TRACE_STAGE=SYNTH_DISPATCH;event=note_on;core=d1;note=60;status=DISPATCHED
```

### Eerste verdwynpunt

```text
FIRST_DISAPPEARANCE_OF_NOTEON;last_seen=ADAFRUIT_MIDI_DECODE;first_missing=MIDI_RECEIVE;evidence=<short-evidence-id>
```

As die verdwynpunt nie bepaal kan word nie:

```text
FIRST_DISAPPEARANCE_OF_NOTEON;last_seen=UNKNOWN;first_missing=UNKNOWN;reason=insufficient_measurement_data
```

## HIL-Testplan

1. Bevestig dat `i2s_test.py` nog hoorbaar G-C-D kan speel; dit is net 'n audio-preflight, nie MIDI-bewys nie.
2. Start MCP-US-080-INV-001 diagnostic-modus met bounded logging.
3. In Logic Pro:
   - kies die S2 as External MIDI destination;
   - kies MIDI Channel `All` of `1`;
   - speel live C4, E4, G4;
   - speel daarna 'n MIDI-region met C4, E4, G4.
4. Voer 'n host-known-note sender uit na dezelfde CoreMIDI destination indien beskikbaar.
5. Verzamel volledige serial output.
6. Classificeer elke meetlocatie als `NOTEON_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS`, `FILTERED`, `DROPPED`, `AUDIO_ABSENT`, `AUDIBLE`, `MEASURABLE_ONLY`, `SILENT` of `UNKNOWN`.
7. Bepaal uitsluitend `FIRST_DISAPPEARANCE_OF_NOTEON`.

## Acceptatiecriteria

De story is alleen gereed wanneer:

- de volledige MIDI-keten in het onderzoeksrapport is gemapt;
- iedere meetlocatie een verwachte loggingvorm heeft;
- de HIL-test per meetlocatie objectieve data oplevert of expliciet `UNKNOWN` rapporteert;
- exact is vastgesteld waar `NoteOn` voor het eerst verdwijnt, of waarom dit nog `UNKNOWN` is;
- geen bestaande functionaliteit is gewijzigd;
- geen bugfix is uitgevoerd;
- geen refactor is uitgevoerd;
- geen optimalisatie is uitgevoerd;
- geen productarchitectuurwijziging is uitgevoerd;
- alle tracepoints en meetinstrumentatie tijdelijk, debug-only, bounded en eenvoudig deactiveerbaar of verwijderbaar zijn;
- tracepoints geen productgedrag, routing, timing, eventsemantiek, audio of D1-functionaliteit wijzigen;
- Principal QA Architect `PASS` geeft voor de investigation-resultaten.

## Done-Criterium

De investigation sluit uitsluitend met een meetrapport dat één van deze uitkomsten objectief vastlegt:

```text
FIRST_DISAPPEARANCE_OF_NOTEON=<meetpunt>
```

of:

```text
UNKNOWN;reason=<objectief gemotiveerde reden>
```

Een fixadvies, architectuurvoorstel of implementatiekeuze is geen onderdeel van Done.

## Virtuele Teaminzet

| Rol | Inzet |
|---|---|
| Product Owner | Verklaart P0 impediment en keurt investigation-only scope goed |
| Scrum Master | Bewaakt dat dit geen fix/refactor wordt |
| Business Analyst | Definieert de onderzoeksvraag als locatiebepaling, niet oorzaak/fix |
| Chief Enterprise Architect | Bewaakt ketenbrede meetbaarheid van Logic tot speaker |
| Solution Architect | Scheidt host-, USB-, decode-, router-, synth- en audio-lagen |
| Embedded/MIDI Specialist | Definieert MIDI 1.0 eventclassificatie en endpointmetingen |
| QA/HIL | Vereist echte S2/Logic HIL-output en `UNKNOWN` waar bewijs ontbreekt |
| Release/Documentation | Legt meetuitkomst en eventueel `UNKNOWN` vast zonder fixadvies |
| Devil's Advocate | Verwerpt elke conclusie zonder meetdata |

## Burn-in

`Burn-in: N/A`

Motivering: dit is 'n bounded investigation story. Langlopende stabiliteit hoort pas bij de latere fix-/release-story.

## Status

`Ready For Product Owner Review`

Nog geen code. Nog geen fix. Nog geen refactor. Nog geen productontwerp.

## Gekoppelde Artefakte

- `docs/governance/instrumentation_design_review_template_v1.0.md`
- `docs/governance/evidence_package_template_v1.0.md`
- `docs/mcp_us_080_inv_001_instrumentation_design_review_v0.1.0.md`
