# Instrumentation Design Review Template v1.0

<!--
Bestand: instrumentation_design_review_template_v1.0.md
Versienommer: 1.0.0
Doel: Definieer 'n repository-brede template vir Investigation Story instrumentasie-ontwerp.
Sprint: Sprint 3
Epic: MCP-EPIC-009 Framework Engineering
User-Story: INVESTIGATION-GOVERNANCE-001
Actienr: MCP-ACT-IDR-TEMPLATE-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / INVESTIGATION-GOVERNANCE-001
-->

## Doel

Hierdie template beskryf hoe tydelike instrumentasie vir 'n goedgekeurde Investigation Story ontwerp word voordat enige instrumentasie geïmplementeer word.

'n Instrumentation Design Review is nie kode nie, nie 'n fix nie, nie 'n refactor nie en nie 'n argitektuurvoorstel nie. Dit definieer slegs hoe observasie, meting, lokalisering en objektiewe bewys gaan plaasvind.

## Governance Workflow

```text
User Story
↓
Principal QA Review
↓
Investigation Story
↓
Instrumentation Design Review (IDR)
↓
Principal QA Review IDR
↓
Implementatie tijdelijke instrumentatie
↓
HIL metingen
↓
FIRST_DISAPPEARANCE_OF_<EVENT>
of
UNKNOWN
↓
Root Cause vastgesteld
↓
Nieuwe Fix Story
↓
Implementatie
↓
Validatie
↓
Verwijderen tijdelijke instrumentatie
```

## Harde Regels

Een IDR:

- schrijft geen code;
- maakt geen tracepoints;
- maakt geen fixes;
- maakt geen refactoring;
- maakt geen optimalisaties;
- maakt geen architectuurwijzigingen;
- definieert geen permanente API;
- definieert geen nieuw domeincontract;
- vervangt geen HIL-bewijs.

## Investigation Summary

| Veld | Waarde |
|---|---|
| Investigation Story ID | `<story-id>` |
| Titel | `<titel>` |
| Event of gedrag dat wordt gezocht | `<event>` |
| Huidige status | `<status>` |
| Root cause status | `UNKNOWN` |
| Product Owner goedkeuring | `<chat-id / datum>` |
| Principal QA pre-review | `<review-id / datum>` |

## 1. Doel Van De Investigation

Beschrijf alleen wat objectief gelokaliseerd moet worden.

Toegestaan:

- waar verdwijnt een event;
- waar verandert een timingkenmerk;
- waar stopt een signaal;
- waar ontstaat een meetbare mismatch.

Niet toegestaan:

- hoe het opgelost moet worden;
- welke code moet worden aangepast;
- welk ontwerp gekozen moet worden.

## 2. Hypotheses Die Onderzocht Worden

| ID | Hypothese | Welke observatie kan dit bevestigen? | Welke observatie kan dit falsifiëren? |
|---|---|---|---|
| H-001 | `<hypothese>` | `<observatie>` | `<observatie>` |

## 3. Hypotheses Die Niet Onderzocht Worden

| ID | Niet onderzocht | Reden |
|---|---|---|
| NH-001 | `<hypothese>` | Buiten scope van deze investigation |

## 4. Volledige Observatieketen

Beschrijf de volledige keten van bron tot eindobservatie. Elke stap krijgt een eigen stage-naam.

| Volgorde | Stage | Vraag | Mogelijke uitkomst |
|---|---|---|---|
| 1 | `<STAGE_NAME>` | `<meetvraag>` | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |

## 5. Tracepoint Definities

Voor ieder tracepoint wordt uitsluitend vastgelegd:

| Veld | Betekenis |
|---|---|
| Naam | Unieke tracepointnaam |
| Doel | Welke observatie wordt mogelijk gemaakt |
| Waarom noodzakelijk | Waarom deze stage nodig is om de verdwijnlocatie te lokaliseren |
| Verwachte observatie | Welke data zichtbaar moet worden |
| Observer-effect | Hoe het meetpunt de meting kan beïnvloeden |
| Timingrisico | Risico op timing-, buffer- of schedulingverandering |
| Bounded logging | Maximaal volume, tijd of eventcount |
| Debug-only | Hoe wordt geborgd dat dit geen productfeature is |
| Verwijderstrategie | Hoe en wanneer wordt dit verwijderd of gedeactiveerd |
| UNKNOWN-regel | Wanneer mag deze stage `UNKNOWN` rapporteren |

## 6. Observer-Effect Analyse

| Tracepoint | Mogelijk observer-effect | Mitigatie | Resterend risico |
|---|---|---|---|
| `<TRACEPOINT>` | `<effect>` | `<mitigatie>` | `<risico>` |

## 7. Risicoanalyse

| Risico | Impact | Kans | Beheersing |
|---|---|---|---|
| Tijdelijke logging verandert timing | Hoog | Middel | Bounded logging, korte regels, debug-only |
| Instrumentatie wordt productgedrag | Hoog | Laag | Verwijderstrategie en QA-gate |

## 8. Meetmatrix

De meetmatrix gebruikt uitsluitend de goedgekeurde classificaties:

- `NOTEON_PRESENT`
- `NOTEOFF_PRESENT`
- `CONTROL_ONLY`
- `NO_EVENTS`
- `UNKNOWN`

Geen andere classificaties zijn toegestaan zonder expliciete Principal QA Architect goedkeuring.

| Stage | Meetpunt | Verwachte invoer | Verwachte uitvoer | Mogelijke uitkomst |
|---|---|---|---|---|
| `<STAGE>` | `<MEETPUNT>` | `<invoer>` | `<uitvoer>` | `NOTEON_PRESENT / NOTEOFF_PRESENT / CONTROL_ONLY / NO_EVENTS / UNKNOWN` |

## 9. Verwachte Classificaties

| Classificatie | Betekenis | Wanneer gebruiken |
|---|---|---|
| `NOTEON_PRESENT` | Het onderzochte meetpunt ziet objectief een NoteOn-event | Alleen bij meetbaar NoteOn-bewijs |
| `NOTEOFF_PRESENT` | Het onderzochte meetpunt ziet objectief een NoteOff-event | Alleen bij meetbaar NoteOff-bewijs |
| `CONTROL_ONLY` | Het meetpunt ziet alleen control-verkeer en geen note-events | Wanneer geen NoteOn/NoteOff zichtbaar is maar control-events wel |
| `NO_EVENTS` | Het meetpunt ziet helemaal geen events | Wanneer de stage actief is maar niets ontvangt |
| `UNKNOWN` | De stage is niet objectief meetbaar of bewijs ontbreekt | Wanneer data ontbreekt, tooling ontbreekt of de meting niet betrouwbaar is |

## 10. HIL-Run Template

Iedere HIL-run registreert minimaal:

| Veld | Waarde |
|---|---|
| Story ID | `<story-id>` |
| Firmware versie | `<firmware-versie>` |
| Git commit | `<commit>` |
| Release versie | `<release>` |
| Datum/tijd | `<YYYY-MM-DD HH:MM TZ>` |
| Tester | `<naam>` |
| Hardware | `<bord / module / meetopstelling>` |
| Host | `<hostnaam / OS>` |
| Logic versie | `<versie of N/A>` |
| macOS versie | `<versie of N/A>` |
| USB poort | `<poort / hub / UNKNOWN>` |
| MIDI kanaal | `<kanaal / All / UNKNOWN>` |
| Testscenario | `<scenario>` |
| Verwachte observatie | `<verwachting>` |
| Werkelijke observatie | `<observatie>` |

## 11. Reproduceerbaarheid

Een investigation-run is reproduceerbaar wanneer:

- de firmwareversie en git commit bekend zijn;
- de hardware-opstelling beschreven is;
- host, OS, MIDI-host en poort bekend of `UNKNOWN` zijn;
- stimulus en verwachte observatie vastliggen;
- ruwe observatie of serial output bewaard is;
- de conclusie alleen op meetdata steunt.

## 12. Verwijderstrategie

Elke IDR moet vooraf beschrijven:

- welke tijdelijke instrumentatie na de investigation weg moet;
- welke instellingen of debug-flags terug naar default moeten;
- hoe gecontroleerd wordt dat geen tijdelijke observatie productgedrag is geworden;
- welke post-investigation QA-check verwijdering bevestigt.

## Done Definitie Voor Investigation Stories

Een Investigation Story is uitsluitend gereed wanneer:

- alle meetpunten ontworpen zijn;
- alle observer-effecten beschreven zijn;
- HIL-run reproduceerbaar is;
- tijdelijke instrumentatie verwijderbaar is;
- het eindrapport uitsluitend eindigt met:

```text
FIRST_DISAPPEARANCE_OF_<EVENT>=<meetpunt>
```

of:

```text
UNKNOWN;reason=<objectief gemotiveerde reden>
```

zonder fixadvies.
