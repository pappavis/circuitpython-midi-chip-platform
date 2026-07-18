# ADR-004: Persistent realtime audio graph vir MIDI performance

<!--
Bestand: ADR-004-persistent-realtime-audio-graph.md
Versienommer: 0.1.0
Doel: Herbaseer realtime MIDI-klank op 'n permanente audio graph in plaas van per-event I2SOut play/stop.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-079 Persistent Synthio Audio Graph Spike
Actienr: MCP-ACT-079-ARCH-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-078-ARCH-REVIEW-001
-->

## Status

Proposed. Hierdie ADR is geskryf na MCP-US-077/078 se HIL-bewys:

- `device/i2s_test.py` is onmiddellik hoorbaar.
- `REALTIME_BASELINE_BOOT_AUDITION` is onmiddellik hoorbaar.
- Logic Pro USB-MIDI NoteOn events bereik die S2 na `REALTIME_BASELINE_READY`.
- Firmware meet `latency_ms=0-4` tussen MIDI receive en die huidige `I2SOut.play()` call.
- Die Product Owner hoor die NoteOn-klank ongeveer 20 sekondes laat.

## Konteks

Die huidige baseline en D1-runtime gebruik variasies van hierdie patroon:

1. open `audiobusio.I2SOut`;
2. maak of hergebruik 'n `audiocore.RawSample`;
3. roep `I2SOut.play(sample, loop=True)` op NoteOn;
4. roep later `I2SOut.stop()` om die noot te eindig.

Volgens CircuitPython se `audiobusio.I2SOut` dokumentasie is `play()` 'n non-blocking sample-player API vir `WaveFile`, `RawSample`, `Mixer` of soortgelyke audio samples. Dit is bruikbaar vir diagnostiese tone, maar die HIL-bewys wys dat dit nie die betroubare realtime voice-control primitive vir hierdie synth moet wees nie.

CircuitPython se `synthio.Synthesizer` bied 'n beter model vir hierdie probleem: een synthesizer-object word eenmalig aan die audio output gekoppel, waarna note met `press()`, `release()` of `change()` bestuur word. Die 10.2.x dokumentasie meld ook dat `change()` note-start en note-stop atomies met betrekking tot output generation uitvoer.

Bronne:

- https://docs.circuitpython.org/en/10.2.x/shared-bindings/audiobusio/index.html
- https://docs.circuitpython.org/en/10.2.x/shared-bindings/synthio/index.html

## Besluit

Vir realtime MIDI-performance aanvaar die projek hierdie argitektuur:

- Open `audiobusio.I2SOut` presies een keer by runtime startup.
- Skep 'n permanente audio-engine object presies een keer.
- Roep `audio.play(engine)` presies een keer by startup.
- Die MIDI-loop mag nie `I2SOut.play()` of `I2SOut.stop()` op die NoteOn/NoteOff hot path roep nie.
- MIDI NoteOn/NoteOff muteer net voice-state in die engine.
- Die eerste engine-spike gebruik `synthio.Synthesizer` met mono, lae sample rate, een stem en minimale logging.
- Indien `synthio` op ESP32-S2 nie haalbaar is nie, is die fallback 'n permanente `audiomixer.Mixer` of soortgelyke persistent graph waarin NoteOn net voice/gate/level state verander.

## Nie-besluite

- Hierdie ADR implementeer nog nie D1-klankkwaliteit, filter, envelope of pitch bend nie.
- Hierdie ADR besluit nie oor stereo, SN76489, SID, OPL2 of physical chip output nie.
- Hierdie ADR sertifiseer nie ESP32-S2 vir finale polyfonie nie.

## Fitness tests

MCP-US-079 moet hierdie bewys lewer:

- boot open I2S een keer;
- startup speel steeds 'n boot-audition selftest;
- na `READY` speel Logic NoteOn binne menslik hoorbare realtime, doelwit minder as 50 ms;
- 20 herhaalde Logic NoteOns skep geen 12-20 sekonde hoorbare backlog nie;
- firmware-log onderskei MIDI receive, voice press en voice release;
- NoteOff of 'n kort gate stop die toon betroubaar;
- host tests bewys dat die NoteOn path nie `I2SOut.play()` of `I2SOut.stop()` aanroep nie;
- implementasie bly klasgebaseerd en gebruik geen globale veranderlikes of modulevlak runtime-status nie.

## Gevolge

MCP-US-055 word nie met nog 'n per-event RawSample patch gedeblokkeer nie. Die volgende logiese story is MCP-US-079: 'n klein persistent `synthio` audio graph spike. Eers nadat daardie spike HIL-groen is, mag D1-runtime teruggebou word op die nuwe primitive.

ESP32-S2-risiko's bly eksplisiet:

- beperkte CPU/RAM;
- garbage collection op die hot path;
- te hoe sample rate;
- te veel voices;
- `synthio` API is eksperimenteel;
- latency kan terugkom as runtime allocasies tydens NoteOn plaasvind.

Die eerste spike beperk daarom scope tot mono, een stem, vooraf ingestelde waveform/envelope en geen dinamiese samplebou tydens NoteOn.
