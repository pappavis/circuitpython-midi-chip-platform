# MCP-US-077 Realtime MIDI Audio Baseline Spike Review

<!--
Bestand: mcp_us_077_realtime_midi_audio_baseline_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer die kleinste realtime USB-MIDI NoteOn na voorafberekende I2S-toon baseline.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-077 Realtime MIDI Audio Baseline Spike
Actienr: MCP-ACT-077-IMP-001-GREEN-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-IMPEDIMENT-001
-->

## Status

**IN REVIEW / RECEIVE PASS / AUDIO DELAYED.** `v0.18.1` voeg 'n boot-audition by die P0 realtime-baseline. Die HIL-log wys dat firmware NoteOn ontvang en `I2SOut.play()` binne `0-4 ms` aanroep, maar die Product Owner hoor die tone ongeveer 20 sekondes later. `i2s_test.py` en boot-audition is onmiddellik hoorbaar. Daarmee is die I2S-bedrading, basiese audio-start en USB-MIDI receive-loop voorlopig vrygespreek; die oorblywende P0-probleem is die per-event audio-runtime primitive.

Die doel is nie musikaliteit nie. Die doel is om hard te bewys of die Wemos S2 Mini + MAX98357A + Logic Pro pad realtime hoorbaar kan reageer voordat die D1-kern weer ingebou word.

## Implementering

| Component | Verandering |
|---|---|
| `realtime_baseline.py` | Nuwe class-based baseline-runtime met `RealtimeBaselineProfile`, `CircuitPythonPrecomputedI2sToneOutput`, `RealtimeMidiAudioBaselineRuntime` en factory |
| `configuration.py` | Nuwe `REALTIME_BASELINE_*` settings; default disabled; boot-audition default `0.6s` |
| `device_runtime.py` | Baseline-runtime kry prioriteit bo D1 wanneer `realtime_baseline.enabled` true is |
| `device/code.py` | Composition root registreer `RealtimeMidiAudioBaselineFactory` |
| `hil.py` | Deploymanifest bevat `realtime_baseline.py`; verifier herken `REALTIME_BASELINE_READY` as execution proof |
| `settings.toml.example` | Dokumenteer die P0-testvlagte |

## RED/GREEN-bewys

| Fase | Bewys |
|---|---|
| RED | Release- en HIL-contracte het gefaal toe `ReleaseMetadata` na `0.18.1/MCP-US-077` beweeg is |
| GREEN | `RealtimeMidiAudioBaselineRuntime` start voorafberekende tone op NoteOn; D1 bly uit wanneer baseline aan is |
| REGRESSION | `144 passed in 0.83s` |
| HIL | Product Owner bevestig: `i2s_test.py` slaag, boot-audition is hoorbaar by startup, en `REALTIME_BASELINE_READY;ready_ms=613` word gerapporteer |

## Waarom hierdie baseline anders is as US-055

| US-055 huidige pad | US-077 baseline |
|---|---|
| D1-kern in die runtime | Geen D1-kern |
| `SafeAudioOutput` wrapper | Direkte I2SOut |
| RawSample word per note gebou of runtime-pad herbegin | Een RawSample word by `open()` vooraf bereken |
| D1 frequency per note | Vaste 440 Hz tone vir alle NoteOn events |
| Meer bewegende dele | Kleinste primitive: USB-MIDI NoteOn -> cached I2S tone |

## HIL-teststappe

### 1. Sluit serial-konflikte

Maak Thonny toe voordat jy deploy. Na deploy mag jy Thonny weer oopmaak om die REPL/logs te sien. Gebruik nie Thonny en 'n ander serial monitor gelyktydig nie.

### 2. Stel `settings.toml`

Op `CIRCUITPY/settings.toml`, maak hierdie tijdelijke P0-testinstellings:

```toml
REALTIME_BASELINE_ENABLED = "true"
REALTIME_BASELINE_EVENT_LOGGING = "none"
REALTIME_BASELINE_BOOT_AUDITION_SECONDS = "0.6"
REALTIME_BASELINE_MAX_NOTE_EVENTS = 0
REALTIME_BASELINE_TIMEOUT_SECONDS = "0.0"
REALTIME_BASELINE_TONE_SECONDS = "0.12"
REALTIME_BASELINE_FREQUENCY_HZ = "440.0"
REALTIME_BASELINE_AMPLITUDE = 4096
MIDI_DIAGNOSTIC_ENABLED = "false"
```

Belangrik: laat `D1_RUNTIME_ENABLED = "true"` staan as dit reeds so is. Die baseline kry voorrang wanneer `REALTIME_BASELINE_ENABLED` true is.

### 3. Start die board

Verwag in Thonny:

```text
circuitpython-midi-chip-platform v0.18.1 | story=MCP-US-077 | release-date=2026-07-17
DEVICE_FAST_BOOT_STATUS=ENABLED
REALTIME_BASELINE_STATUS=START;sample_rate=16000;frequency_hz=440.000;...;event_logging=none;boot_audition_seconds=0.600
REALTIME_BASELINE_AUDIO_STATUS=OPEN;actual_frequency_hz=...
REALTIME_BASELINE_BOOT_AUDITION=START;seconds=0.600
REALTIME_BASELINE_BOOT_AUDITION=PASS
REALTIME_BASELINE_MIDI_INPUT_STATUS=OPEN
REALTIME_BASELINE_READY;ready_ms=...
```

**Eerste acceptatievraag:** hoor je die boot-audition direct tijdens de startup? Als dit al 12 seconden later klinkt, ligt het probleem onder Logic/MIDI en moeten we het I2S/audio-startpad of hardwarepad onderzoeken.

**Antwoord 2026-07-17:** ja, boot-audition is hoorbaar by startup. Dit beteken dat die 12-sekonde vertraging nie in die basiese I2S-audio-startpad sit nie.

**Logic retest 2026-07-17:** met `event_logging=none` was daar na `REALTIME_BASELINE_READY` geen hoorbare Logic NoteOn-klank en geen MIDI-gerelateerde debugoutput. Omdat `none` per-note logging doelbewus uitskakel, is die volgende P0-story `MCP-US-078`: herhaal dieselfde Logic-test met `REALTIME_BASELINE_EVENT_LOGGING=summary` en bewys eers of NoteOn events die S2 ná ready bereik.

**MCP-US-078 retest 2026-07-19:** met `REALTIME_BASELINE_EVENT_LOGGING=summary` bereik Logic Pro NoteOn events die S2 ná `REALTIME_BASELINE_READY`. Die Product Owner-log bevat 17 `REALTIME_BASELINE_NOTE_ON` events op channel 1 met `latency_ms=0-4`. Daarmee is die post-ready USB-MIDI receive-loop voorlopig vrygespreek. Die Product Owner bevestig daarna dat NoteOn-tone wel hoorbaar is, maar steeds ongeveer 20 sekondes laat. Die probleem bly dus in die audio-runtime primitive, nie in I2S wiring of USB-MIDI receive nie.

### 4. Logic Pro test

1. Open Logic Pro.
2. Kies `MIDI -> External MIDI`.
3. MIDI Destination: `S2 Mini`.
4. MIDI Channel: `All` of `1`.
5. Speel een noot live of speel 'n korte MIDI-region.

### 5. Verwacht resultaat

Elke NoteOn moet onmiddellik 'n korte vaste toon hoorbaar maken via de MAX98357A. De toon is altijd ongeveer A4/440 Hz; dit is expres, omdat US-077 alleen realtime triggerbaarheid test.

Standaard is per-note logging in `v0.18.1` uitgeschakeld om serial flood als timingfactor uit te sluiten. Als je toch tijdelijk logging nodig hebt, zet:

```toml
REALTIME_BASELINE_EVENT_LOGGING = "summary"
```

Dan zie je per noot iets zoals:

```text
REALTIME_BASELINE_NOTE_ON;channel=1;note=60;velocity=90;event_ms=...;tone_start_ms=...;latency_ms=...
```

## Pass/Fail

| Resultaat | Betekenis |
|---|---|
| Hoorbare directe tone per Logic NoteOn | US-077 HIL PASS; daarna D1 opnieuw op deze primitive bouwen |
| Boot-audition klinkt 12 seconden laat | Logic/MIDI is vrijgesproken; onderzoek I2SOut/startup audio path of hardwarewaarneming |
| Boot-audition klinkt direct, Logic NoteOn klinkt 12 seconden laat | Onderzoek MIDI-event queue, Logic routing of post-ready runtime-loop |
| Logs tonen NoteOn maar geen hoorbare tone | Audio-start/I2S path blijft verdacht; vergelijk direct met `i2s_test.py` |
| Geen NoteOn logs | Logic/CoreMIDI routing of USB-MIDI receive opnieuw testen met MCP-US-007 diagnostic |
| Tone pas veel later hoorbaar | MIDI/audio-loop scheduling nog fout; test zonder serial summary logging |
| Board crasht of hangt | Baseline-runtime blijft te zwaar of imports/config/deploy missen dependency |

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Verklaar US-055 as P0-blokker en vra 'n terug-na-basics spike. |
| Scrum Master | Hou scope beperk tot realtime primitive; geen SN76489/web/DSP-sidequest. |
| Business Analyst | Verduidelik dat vaste A4-tone aanvaarbaar is omdat die story triggerbaarheid bewys. |
| Chief Enterprise Architect | Behou D1 en baseline as aparte runtimes met 'n composition-root-keuse. |
| Solution Architect | Plaas baseline voor D1 wanneer enabled, sonder bestaande D1 code te verwyder. |
| Embedded Engineer | Verwyder per-note allocation uit die HIL-kritieke baselinepad. |
| MIDI Engineer | Hergebruik die reeds geslaagde USB-MIDI translator en NoteEvent-model. |
| DSP/Chip Engineer | Gebruik square tone as meetbare, hoorbare primitive in plaas van synthkwaliteit. |
| QA/HIL Engineer | Voeg host-contracte, HIL-manifest closure en menslike teststappe by. |
| External Reviewer | Kan hierdie baseline gebruik om te bepaal of US-055 se fout onder D1 of onder MIDI/I2S lê. |

## Volgende stap na HIL

Omdat die boot-audition nou slaag, is die logiese volgende actie:

1. Aanvaar ADR-004 as rigting: realtime MIDI-performance gebruik 'n permanente audio graph.
2. Implementeer MCP-US-079 met `synthio.Synthesizer`: `audio.play(synth)` by startup en `synth.press/release` op MIDI events.
3. Bewys met HIL dat 20 Logic NoteOns binne menslik hoorbare realtime klink sonder 12-20s backlog.
4. Eers daarna US-055 refactor: herbou D1-runtime op die bewezen persistent-audio primitive.
5. Voeg eers daarna pitch/velocity/musikaliteit terug.

As US-077 faal, stop D1-werk en diagnoseer USB-MIDI/I2S primitive met scope markers.
