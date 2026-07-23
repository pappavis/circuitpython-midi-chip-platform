# MCP-US-080-INV-001 Instrumentation Design Review v0.1.0

<!--
Bestand: mcp_us_080_inv_001_instrumentation_design_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer die tydelike observasie-ontwerp vir MCP-US-080-INV-001 sonder implementasie of fixrichting.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-080-INV-001 Locate First Disappearance Of NoteOn
Actienr: MCP-ACT-080-INV-001-IDR-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-INV-001-IDR-001
Template: docs/governance/instrumentation_design_review_template_v1.0.md
-->

## Doel

Deze IDR definieert uitsluitend hoe tijdelijke observatie wordt ontworpen om vast te stellen waar `NoteOn` voor het eerst verdwijnt in de keten van Logic Pro naar de S2 synth.

Geen implementatie. Geen tracepoints. Geen fix. Geen refactor. Geen optimalisatie. Geen productarchitectuurwijziging.

## Investigation Summary

| Veld | Waarde |
|---|---|
| Investigation Story ID | `MCP-US-080-INV-001` |
| Titel | Locate First Disappearance Of NoteOn |
| Event of gedrag dat wordt gezocht | `NoteOn` |
| Huidige status | P0 Investigation / IDR |
| Root cause status | `UNKNOWN` |
| Product Owner goedkeuring | K8M4R2Q7 / B5Q8N2L7 / J6R9T2M4 |
| Principal QA pre-review | W4N8K2R6 |

## 1. Doel Van De Investigation

Lokaliseer objectief:

```text
FIRST_DISAPPEARANCE_OF_NOTEON=<meetpunt>
```

of rapporteer:

```text
UNKNOWN;reason=<objectief gemotiveerde reden>
```

## 2. Hypotheses Die Onderzocht Worden

| ID | Hypothese | Welke observatie kan dit bevestigen? | Welke observatie kan dit falsifiëren? |
|---|---|---|---|
| H-001 | Logic/CoreMIDI levert geen `NoteOn` aan de S2-route | Host/CoreMIDI-stage rapporteert `NO_EVENTS`, `CONTROL_ONLY` of `UNKNOWN` terwijl stimulus verwacht is | Host/CoreMIDI-stage rapporteert `NOTEON_PRESENT` |
| H-002 | `NoteOn` bereikt een USB-MIDI endpoint maar niet de device-decode laag | USB endpoint-stage rapporteert `NOTEON_PRESENT`, latere decode-stage niet | Decode-stage rapporteert `NOTEON_PRESENT` |
| H-003 | `NoteOn` wordt decoded maar verdwijnt vóór router/dispatcher | Decode- of receive-stage rapporteert `NOTEON_PRESENT`, latere stage rapporteert `NO_EVENTS` of `UNKNOWN` | Router/dispatcher-stage rapporteert `NOTEON_PRESENT` |
| H-004 | De investigation kan met huidige middelen niet objectief lokaliseren | Een of meer noodzakelijke stages blijven `UNKNOWN` | Alle noodzakelijke stages leveren objectieve classificaties |

## 3. Hypotheses Die Niet Onderzocht Worden

| ID | Niet onderzocht | Reden |
|---|---|---|
| NH-001 | Welke bugfix nodig is | Fixrichting is buiten scope |
| NH-002 | Welke architectuurwijziging nodig is | Productontwerp is buiten scope |
| NH-003 | Waarom audio hoorbaar vertraagt | Deze IDR lokaliseert alleen `NoteOn`-verdwijning |
| NH-004 | Of D1/synthio/I2S verbeterd moet worden | Audio- en synthwijzigingen zijn buiten scope |

## 4. Volledige Observatieketen

| Volgorde | Stage | Vraag | Mogelijke uitkomst |
|---|---|---|---|
| 1 | `LOGIC_PRO_STIMULUS` | Is er een bekende note-stimulus gestart? | `NOTEON_PRESENT / NO_EVENTS / UNKNOWN` |
| 2 | `COREMIDI_HOST_SEND` | Is vóór de device-grens een `NoteOn` meetbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 3 | `USB_HOST_DESTINATION` | Is de S2-destination/poort objectief bekend? | `NOTEON_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 4 | `USB_ENDPOINT_PORT_0` | Ziet endpoint/port 0 note-events, control-only of niets? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 5 | `USB_ENDPOINT_PORT_1` | Ziet endpoint/port 1 note-events, control-only of niets? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 6 | `CIRCUITPY_USB_STACK` | Zijn events op de CircuitPython USB-laag observeerbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 7 | `ADAFRUIT_MIDI_DECODE` | Is decoded `NoteOn` observeerbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 8 | `MIDI_RECEIVE_LOOP` | Ziet de applicatie-receive-loop `NoteOn`? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 9 | `ROUTER_OBSERVATION` | Is `NoteOn` vóór of in router-observatie zichtbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 10 | `SYNTH_DISPATCH_OBSERVATION` | Is `NoteOn` vóór synth-dispatch zichtbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 11 | `D1_TRIGGER_OBSERVATION` | Is een D1-triggerobservatie mogelijk zonder gedrag te wijzigen? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 12 | `I2S_OBSERVATION` | Is een audio-startobservatie mogelijk zonder audio te wijzigen? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| 13 | `SPEAKER_OBSERVATION` | Is het resultaat menselijk of met meter observeerbaar? | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |

## 5. Tracepoint Definities

| Naam | Doel | Waarom noodzakelijk | Verwachte observatie | Observer-effect | Timingrisico | Bounded logging | Debug-only | Verwijderstrategie | UNKNOWN-regel |
|---|---|---|---|---|---|---|---|---|---|
| `LOGIC_PRO_STIMULUS` | Vastleggen welke stimulus de tester uitvoert | Zonder stimuluscontext is device-output niet interpreteerbaar | Testscenario en verwachte note(s) | Geen firmware-effect | Geen device timingrisico | Eén HIL-run record | Documentatie-only | N.v.t. | Wanneer stimulus niet reproduceerbaar is |
| `COREMIDI_HOST_SEND` | Observeren of hostlaag een note richting S2 verstuurt | Scheidt hostlaag van device-laag | `NOTEON_PRESENT`, `NOTEOFF_PRESENT`, `CONTROL_ONLY`, `NO_EVENTS` of `UNKNOWN` | Hosttooling kan routing beïnvloeden | Laag tot middel | Beperkte host-output | Debug-only HIL-bewijs | Hosttooling stoppen/verwijderen | Wanneer geen objectieve hostprobe beschikbaar is |
| `USB_HOST_DESTINATION` | Vastleggen welke destination/poort gekozen is | Zonder poortcontext blijft endpointanalyse ambigu | Destination/poortstatus of `UNKNOWN` | Geen firmware-effect | Geen device timingrisico | Eén runrecord | Documentatie-only | N.v.t. | Wanneer host geen eenduidige poort toont |
| `USB_ENDPOINT_PORT_0` | Observeren welke eventklasse port 0 levert | Endpointverwisseling uitsluiten of bevestigen | Classificatie per eventtype | Serial logging kan polling beïnvloeden | Middel | Max events/tijd begrensd | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer port niet meetbaar is |
| `USB_ENDPOINT_PORT_1` | Observeren welke eventklasse port 1 levert | Endpointverwisseling uitsluiten of bevestigen | Classificatie per eventtype | Serial logging kan polling beïnvloeden | Middel | Max events/tijd begrensd | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer port niet meetbaar is |
| `CIRCUITPY_USB_STACK` | Observeren of CircuitPython events beschikbaar stelt | Lokaliseert vóór/na USB stack-grens | Classificatie per eventtype | Extra observeerwerk kan scheduling beïnvloeden | Middel | Max events/tijd begrensd | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer stack niet apart observeerbaar is |
| `ADAFRUIT_MIDI_DECODE` | Observeren of decoded eventtypes bestaan | Lokaliseert vóór/na decode | Classificatie per decoded eventtype | Extra decode-observatie kan loop vertragen | Middel | Max events/tijd begrensd | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer decode niet apart observeerbaar is |
| `MIDI_RECEIVE_LOOP` | Observeren of applicatie-receive-loop note-events ziet | Lokaliseert vóór/na receive-loop | Classificatie per received event | Logging in loop kan timing veranderen | Hoog | Samenvatting of beperkte events | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer loop niet betrouwbaar observeerbaar is |
| `ROUTER_OBSERVATION` | Observeren of event vóór routergrens zichtbaar blijft | Lokaliseert vóór/na routing | Classificatie vóór routerbesluit | Logging kan routing timing raken | Middel | Samenvatting of beperkte events | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer router niet actief is in gekozen diagnostic |
| `SYNTH_DISPATCH_OBSERVATION` | Observeren of event vóór dispatchgrens zichtbaar blijft | Lokaliseert vóór/na dispatch | Classificatie vóór dispatch | Logging kan dispatch timing raken | Middel | Samenvatting of beperkte events | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer dispatch niet actief is in gekozen diagnostic |
| `D1_TRIGGER_OBSERVATION` | Observeren of D1-triggergrens bereikt wordt | Lokaliseert of NoteOn de synthgrens haalt | Classificatie zonder synthgedrag te wijzigen | Instrumentatie kan synthloop verstoren | Hoog | Alleen bounded summary | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer D1-pad niet actief is in investigation |
| `I2S_OBSERVATION` | Observeren of audio-startgrens relevant is | Scheidt note-disappearance van latere audio-observatie | Classificatie of `UNKNOWN` | Audio-observatie kan timing verstoren | Hoog | Alleen bounded summary | Debug-only | Tracepoint verwijderen/deactiveren | Wanneer audio buiten gekozen measurement path blijft |
| `SPEAKER_OBSERVATION` | Menselijke/meterobservatie vastleggen | Eindobservatie scheiden van firmwareclaim | Hoorbaar/meetbaar bewijs als Evidence Package-data | Geen firmware-effect | Geen device timingrisico | Eén HIL-run record | Documentatie-only | N.v.t. | Wanneer geen mens/meterobservatie beschikbaar is |

## 6. Observer-Effect Analyse

| Tracepoint | Mogelijk observer-effect | Mitigatie | Resterend risico |
|---|---|---|---|
| Host/CoreMIDI observatie | Hosttool kan routing of timing beïnvloeden | Alleen naast Logic-run gebruiken en als aparte run registreren | Middel |
| USB endpoint observatie | Extra serial output kan MIDI polling vertragen | Bounded eventcount, korte regels, summary waar mogelijk | Middel |
| Receive-loop observatie | Logging in hot path kan timing wijzigen | Minimale output, deactiveerbaar, run apart van productmodus | Hoog |
| Router/dispatch observatie | Observatie kan stagevolgorde beïnvloeden als te invasief | Alleen grensobservatie; geen beslislogica wijzigen | Middel |
| D1/I2S observatie | Kan audio timing beïnvloeden | Alleen gebruiken wanneer eerdere stages NoteOn bewijzen en latere stage nodig is | Hoog |

## 7. Risicoanalyse

| Risico | Impact | Kans | Beheersing |
|---|---|---|---|
| Tracepoints veranderen timing | Hoog | Middel | Bounded, debug-only, minimale output |
| Tracepoints worden productgedrag | Hoog | Laag | Verwijderstrategie en post-investigation QA |
| Hostlaag blijft `UNKNOWN` | Middel | Middel | Evidence Package registreert `UNKNOWN` met reden |
| CC7 wordt opnieuw als note-bewijs gelezen | Hoog | Middel | Alleen classificatie `CONTROL_ONLY`; nooit PASS voor NoteOn |

## 8. Meetmatrix

| Stage | Meetpunt | Verwachte invoer | Verwachte uitvoer | Mogelijke uitkomst |
|---|---|---|---|---|
| `LOGIC_PRO_STIMULUS` | Tester-runrecord | C4/E4/G4 stimulus | Stimulus vastgelegd of ontbrekend | `NOTEON_PRESENT / NO_EVENTS / UNKNOWN` |
| `COREMIDI_HOST_SEND` | Hostobservatie | Logic/CoreMIDI output | Eventklasse vóór device | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `USB_HOST_DESTINATION` | Destinationrecord | S2 MIDI destination | Destinationstatus | `NOTEON_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `USB_ENDPOINT_PORT_0` | Portobservatie | USB-MIDI port 0 | Eventklasse per port | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `USB_ENDPOINT_PORT_1` | Portobservatie | USB-MIDI port 1 | Eventklasse per port | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `CIRCUITPY_USB_STACK` | Stackobservatie | CircuitPython USB events | Eventklasse | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `ADAFRUIT_MIDI_DECODE` | Decodeobservatie | Decoded MIDI message | Eventklasse | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `MIDI_RECEIVE_LOOP` | Receiveobservatie | Applicatie receive | Eventklasse | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `ROUTER_OBSERVATION` | Routergrens | Received event | Eventklasse vóór/na grens | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `SYNTH_DISPATCH_OBSERVATION` | Dispatchgrens | Routed event | Eventklasse vóór/na grens | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `D1_TRIGGER_OBSERVATION` | D1-grens | Dispatch event | Triggerobservatie of onbekend | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `I2S_OBSERVATION` | Audio-startgrens | Synth trigger | Audio-startobservatie of onbekend | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |
| `SPEAKER_OBSERVATION` | Mens/meter | Audio-uitvoer | Hoorbaar/meetbaar record of onbekend | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |

## 9. Verwachte Classificaties

| Classificatie | Betekenis binnen MCP-US-080-INV-001 |
|---|---|
| `NOTEON_PRESENT` | Het meetpunt ziet objectief `NoteOn` |
| `NOTEOFF_PRESENT` | Het meetpunt ziet objectief `NoteOff` |
| `CONTROL_ONLY` | Het meetpunt ziet control-verkeer, maar geen note-events |
| `NO_EVENTS` | Het meetpunt ziet geen events |
| `UNKNOWN` | Het meetpunt is niet objectief meetbaar of bewijs ontbreekt |

## 10. HIL-Run Template

| Veld | Waarde |
|---|---|
| Story ID | `MCP-US-080-INV-001` |
| Firmware versie | `<firmware-versie>` |
| Git commit | `<commit>` |
| Release versie | `<release-versie>` |
| Datum/tijd | `<YYYY-MM-DD HH:MM TZ>` |
| Tester | `<naam>` |
| Hardware | `<S2 / MAX98357 / overige>` |
| Host | `<hostnaam / macOS>` |
| Logic versie | `<versie / UNKNOWN>` |
| macOS versie | `<versie / UNKNOWN>` |
| USB poort | `<poort / hub / UNKNOWN>` |
| MIDI kanaal | `<All / 1 / ander / UNKNOWN>` |
| Testscenario | `Live C4/E4/G4 en MIDI-region C4/E4/G4` |
| Verwachte observatie | `NoteOn zichtbaar of UNKNOWN met reden` |
| Werkelijke observatie | `<observatie>` |

## 11. Reproduceerbaarheid

De run is reproduceerbaar wanneer de Evidence Package Template is ingevuld en ruwe logs of meetobservaties zijn opgenomen. Elk ontbrekend feit wordt `UNKNOWN`, niet ingevuld op basis van aanname.

## 12. Verwijderstrategie

De toekomstige instrumentatie moet na deze investigation:

- verwijderd of standaard gedeactiveerd worden;
- geen productgedrag achterlaten;
- geen nieuwe API of domeincontract achterlaten;
- door post-investigation QA worden gecontroleerd;
- in een Evidence Package aantonen welke tijdelijke observatie actief was.

## Done Definitie

Deze IDR is Done wanneer:

- alle meetpunten ontworpen zijn;
- observer-effecten en timingrisico's beschreven zijn;
- HIL-run reproduceerbaar is via de template;
- verwijderstrategie vastligt;
- geen fixadvies of implementatiekeuze is opgenomen.
