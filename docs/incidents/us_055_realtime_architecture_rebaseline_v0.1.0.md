# US-055 Realtime Architecture Rebaseline

<!--
Bestand: us_055_realtime_architecture_rebaseline_v0.1.0.md
Versienommer: 0.1.0
Doel: Merk die Logic realtime D1-integrasie as P0-blokker en definieer 'n terug-na-basics herstelpad.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance / MCP-US-077 Realtime MIDI Audio Baseline Spike
Actienr: MCP-ACT-055-REBASELINE-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-REALTIME-IMPEDIMENT
-->

## Besluit

US-055 bly 'n **P0 impediment** totdat 'n kleiner realtime-baseline bewys is. Die projek stop met klein iterasies op die huidige v0.17.8 D1-runtimepad omdat sewe menslike HIL-pogings nie tot 'n aanvaarbare realtime Logic Pro resultaat gelei het nie.

## Hoekom hierdie stap nodig is

Die projek het drie afsonderlike waarhede:

1. `i2s_test.py` speel hoorbaar deur die MAX98357A.
2. MCP-US-007 bewys USB-MIDI ontvangs vanaf macOS/Logic/CoreMIDI.
3. Die huidige integrasiepad speel nie betroubaar en menslik realtime as Logic Pro synth nie.

Daarom is die fout waarskynlik nie "geen MIDI" of "geen I2S" in isolasie nie. Die risiko is die integrasie-argitektuur self: MIDI-polling, per-note RawSample allocation/start/stop, safety wrapper, logging, sleeps en D1-core composition leef in een pad wat nie deur host tests as realtime bewys kan word nie.

## Nuwe herstelvolgorde

| Stap | Naam | Doel | Slaagkriterium |
|---|---|---|---|
| 1 | Audio-only sanity | Behou `i2s_test.py` as hardeware groen basis | G-C-D hoorbaar |
| 2 | MIDI-only sanity | Behou MCP-US-007 diagnostic | Note On/Off word gesien |
| 3 | MCP-US-077 realtime baseline | MIDI NoteOn speel onmiddellik 'n bekende I2S toon sonder D1/config/safety wrapper | Logic note is hoorbaar realtime |
| 4 | D1 reintroduction | Vervang hardcoded tone met D1-core of `synthio` engine | Logic note is hoorbaar realtime met D1 |
| 5 | US-055 closure | Volledige MVP acceptance | Product Owner aanvaar Logic -> S2 -> D1 -> MAX98357A |

## Kandidaten vir root cause

| Rang | Hypothese | Waarom waarskynlik | Hoe bewys |
|---|---|---|---|
| 1 | RawSample/I2SOut start-stop per NoteOn is nie geskik vir realtime synth nie | `i2s_test.py` werk as diagnose, maar diagnose is nie realtime MIDI performance nie | MCP-US-077 vergelyk simple tone baseline vs current runtime |
| 2 | Heap churn deur per-note buffer/RawSample allocation | NoteOn skep nuwe arrays en RawSamples | Voeg precomputed tones of synthio toe en meet latency |
| 3 | Poll/sleep/logging versteur timing | Vorige fixes het logging verminder maar nie opgelos nie | Baseline sonder logging/config/safety wrapper |
| 4 | SafeAudioOutput/gain/mute wrapper versteur start/stop | Huidige path loop deur wrapper | Baseline direk na I2SOut |
| 5 | Logic routing/perceived test issue | Minder waarskynlik omdat Logic met ander synths werk en MIDI events soms gesien word | Deterministiese host CoreMIDI sender as aanvullende test |
| 6 | ESP32-S2 performance limiet | Moontlik, maar te vroeg om te besluit | Baseline op S2; S3 eers as S2 primitive faal |

## Nieuwe story

### MCP-US-077 Realtime MIDI Audio Baseline Spike

As Product Owner wil ik een ultra-kleine realtime USB-MIDI naar I2S baseline horen, zonder D1-core en zonder framework-complexiteit, zodat wij kunnen bewijzen of de S2 Mini en MAX98357A realtime MIDI-audio kunnen leveren voordat wij de D1-runtime verder refactoren.

Aanvaardingscriteria:

- `i2s_test.py` blijft hoorbaar groen.
- USB MIDI NoteOn vanuit Logic of CoreMIDI triggert direct een hoorbare toon.
- De baseline gebruikt dezelfde fysieke I2S-pins: `IO5`, `IO3`, `IO7`.
- De baseline heeft geen globale runtime-status en blijft class-based.
- De baseline start zonder D1 core, config loader, SafeAudioOutput of web/Wi-Fi.
- Serial output is rate-limited en toont alleen startup, ready en optionele summary.
- Indien mogelijk pulseert een timing-pin bij MIDI receive en audio start.
- Product Owner bevestigt of de noot menselijk realtime hoorbaar is.

## Lessons learned item

Neem op in de volgende lessons-learned cyclus:

- HIL integration tests mogen niet vervangen worden door host-groene compositietests.
- Een diagnostische audio path (`i2s_test.py`) is niet automatisch een performance audio engine.
- Bij embedded audio moet de eerste realtime story een minimale primitive spike zijn voordat een synth core, safety wrapper en config tegelijk worden geintegreerd.
- Repeated HIL failure after three fixes should trigger architecture rebaseline, not another narrow patch.

