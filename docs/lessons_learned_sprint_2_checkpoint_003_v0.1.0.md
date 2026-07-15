# Sprint 2 Lessons Learned - Checkpoint 003

<!--
Bestand: lessons_learned_sprint_2_checkpoint_003_v0.1.0.md
Versienommer: 0.1.0
Doel: Konsolideer die MCP-US-007 USB-MIDI- en repository-/HIL-impedimentlesse vir toekomstige synthprojekte.
Sprint: Sprint 2
Epic: MCP-EPIC-002 en MCP-EPIC-008
User-Story: MCP-US-007 USB MIDI Receive Loop
Actienr: MCP-ACT-007-LESSON-003
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007-ACCEPTANCE
-->

## Uitkoms

MCP-US-007 is fisies aanvaar: Logic/CoreMIDI het USB-MIDI gestuur en die Wemos S2 het Note On, Note Off en 'n ooreenstemmende nootpaar gerapporteer. Die pad na hierdie PASS het verskeie herbruikbare swakplekke gevind wat toekomstige subtractive-, D1-, drum-machine- en FM-synthprojekte vroeg moet toets.

## Wat goed gewerk het

- Die ontvangsdiagnostiek het semantiese events gewys in plaas van slegs “poort oop”.
- Positional-only en firmware-spesifieke fakes het desktop-valsgroen gedrag in regressietoetse vasgevang.
- Dependency closure, atomiese deploy en REPL-handdruk het herstelbaarheid behou.
- 'n Deterministiese CoreMIDI-sender het firmware van Logic-roetering geïsoleer.
- Die Product Owner het die finale werklike DAW-stimulus gelewer.

## Wat verbeter moes word

| Waarneming | Oorsaak | Verbetering |
|---|---|---|
| `settings.toml` float/boolean het as integer gefaal | Latest docs is op 'n ouer 10.0.x-parser toegepas | Pin firmwarekontrak en toets letterlike device settings |
| Keyword-argumente na `__import__` het net op device gefaal | CPython-fake was te ruim | Gebruik 'n positional-only compatibility fake |
| `device_runtime.py` het in een checkout ontbreek | Twee lokale identities/remotes was nie eksplisiet nie | Canonical implementasie plus gedokumenteerde governance mirror |
| Deploy het met Thonny/diagnostiek gebots | Meer as een serial-eienaar | Een-monitor-reel en preflight-poortbesit |
| Autoreload-marker is gemis | REPL was in “code done”-toestand | Handdruk `Enter -> Ctrl-B -> Ctrl-C` as toestandmasjien toets |
| Logic het aanvanklik geen bewys gelewer | DAW-routing en firmware was gelyktydig onseker | Eers deterministiese CoreMIDI-isolasie, daarna Logic |
| Twee Note On-events vir een toetsnoot | Moontlike Logic echo/routing; nog nie volledig ontleed nie | Log as waarneming; behandel later binne korrekte routing/dedupe-scope |

## Aksies

| Aksie | Eienaar | Teiken/hek | Status |
|---|---|---|---|
| Hou CircuitPython 10.x settings-kontrak in tests | Embedded/QA | Configuration regression | Done |
| Behou positional-only importfake | Embedded/QA | Host suite | Done |
| Sinkroniseer implementasie en governance teen dieselfde commit | Release | Elke publikasie | Aktief |
| Gebruik een serial owner en fase-spesifieke deployfoute | HIL/Release | Elke device deploy | Aktief |
| Voeg DAW-isolasieprosedure by transporttoetse | MIDI/QA | US-054/055 | Planned |
| Ontwerp stabiele vier-karakter USB-instance-identiteit sonder privacy leak | CEA/Embedded | MCP-US-068 | Backlog |
| Ondersoek duplicates slegs wanneer die toepaslike storykriterium dit vereis | MIDI/Scrum | Routing/performance | Deferred |

## Hergebruikreel

Vir 'n nuwe synth begin hardewareontwikkeling met: geteikende firmwareparser, import-compatibility, repository identity, een serial owner, dependency-closed deploy, deterministiese transportstimulus en eers daarna DAW-/menslike integrasie. Dit verklein die kans dat musikale gedrag op 'n onbewese transport- of deploylaag gebou word.
