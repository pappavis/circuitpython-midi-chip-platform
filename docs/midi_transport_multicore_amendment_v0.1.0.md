# MIDI Transport And Multi-Core Amendment

<!--
Bestand: midi_transport_multicore_amendment_v0.1.0.md
Versienommer: 0.1.0
Doel: Formaliseer enige-bron MIDI, standalone hostroetes, Fishman-semantiek en parallelle multi-core-risiko.
Sprint: Sprint 1
Epic: MCP-EPIC-002, MCP-EPIC-006 en MCP-EPIC-008
User-Story: MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
Actienr: MCP-ACT-MTM-AMEND-REV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
-->

## Product Owner-besluite

1. Die synth ontvang MIDI vanaf enige klas-kompatibele controller; handelsname is HIL-voorbeelde, nooit kodekonstantes nie.
2. Teenoor Logic, Windows, Linux, Raspberry Pi of 'n eksterne host tree die CircuitPython-bord as USB-MIDI device op.
3. Twee USB devices praat nie direk nie. Standalone gebruik 'n Raspberry Pi/eksterne USB-host wat na 'n geabstraheerde DIN/UART-invoer roeteer, tensy 'n latere native-host-spike die spesifieke bord bewys.
4. Fishman TriplePlay se mono-/multi-kanaalmodus behou channel state per snaar. Die synth hardkodeer geen snaar-na-kanaalvolgorde nie en sy bend range moet met die controller ooreenstem.
5. Parallelle multi-core-uitvoering is laat-MVP. Die Product Owner aanvaar CPU/RAM-risiko, maar nie stil crashes, korrupsie of onmeetbare dropout nie.

## Transportkontrak

```text
Controller -> computer/Logic/Raspberry Pi/USB host -> USB-MIDI device -> synth
Controller -> external USB host -> 5-pin DIN/UART -> MidiInputPort -> synth
```

Albei paaie normaliseer boodskappe na dieselfde klasgebaseerde eventmodel. Die synth sien by DIN/UART nie noodwendig die oorspronklike USB-toestelnaam nie; funksionele MIDI-data is die kontrak.

## Toetsprofiele

| Profiel | Minimum bewys |
|---|---|
| Algemene keyboard/controller | Note On/Off, velocity, CC1, pitch bend indien beskikbaar, All Notes Off |
| Fishman TriplePlay | Akkoord, ses-kanaal/mono-mode, onafhanklike bends, slide-variante en bend-range passing |
| Logic/DAW | External MIDI destination, kanaalrouting, note en MIDI clock; klank kom uit die fisiese pedaal |
| Standalone host | Controller, host, DIN/UART en hoorbare kern sonder DAW |
| Multi-core | Twee verskillende kerninstansies, kanaaltoewysing, heap, looplatensie, dropout en veilige resource-weiering |

## Story-impact

- US-007 en US-013 skei USB-device- en standalone DIN/UART-transporte van die eventmodel.
- US-058/059 behou Fishman- en generiese MIDI-kitaarbewys.
- US-035/036/037 word laat-MVP in plaas van Later.
- US-060 bewys die volledige standalone hostroete.
- US-061 voeg resource telemetry en veilige degradering by.

## Spanbydraerekord

| Rol | Bydrae |
|---|---|
| Product Owner | Het enige-bron MIDI, standalone werking, Fishman en parallelle kerne as produkvereistes bevestig. |
| Scrum Master | Behou die hoorbare volgorde; die amendment onderbreek nie MCP-US-003 met MIDI-runtimekode nie. |
| Business Analyst | Het USB host/device-rolle en menslike toetsprofiele eksplisiet gemaak. |
| Solution Architect | Hou alle transporte agter MidiInputPort en alle kerne agter registry/instance-grense. |
| Embedded Engineer | Native USB-host op die LOLIN S2 bly 'n onbevestigde spike; DIN/UART is die veilige standalone basislyn. |
| MIDI Engineer | Vereis per-kanaal bend-state en geen vaste snaar-kanaalkaart nie. |
| DSP/Chip Engineer | Vereis resource telemetry en deterministiese weiering voor parallelle kerne aanvaar word. |
| Web Engineer | Not impacted: geen webkode of scheduling word in hierdie amendment geïmplementeer nie. |
| QA/HIL Engineer | Het vier MIDI-profiele plus multi-core metrieke gedefinieer. |
| Release/Documentation | Sinkroniseer Markdown, Kanban, bronne, risiko's en story-ID's. |
| External Architecture Reviewer (Copilot) | Het audio-first en per-kanaal Fishman-risiko beklemtoon; codevoorstelle bly adviserend. |
| Devil's Advocate | Waarsku dat 'class compliant' nie elke controller/host-kombinasie sonder fisiese toets waarborg nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is vir hierdie amendment gebruik nie.
