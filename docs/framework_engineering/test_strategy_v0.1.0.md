# Test Strategy

<!--
Bestand: test_strategy_v0.1.0.md
Versienommer: 0.4.0
Doel: Definieer die toetsvlakke, omgewings, hardewarematriks en aanvaardingsbewys.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: QA-BURN-IN-AMENDMENT-001, MCP-US-016 en MCP-US-075
Actienr: MCP-ACT-075-TEST-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START
-->

## Toetspiramide

| Vlak | Loop waar | Fokus | Voorbeeld |
|---|---|---|---|
| AST/governance | Host | Geen globals/modulefunksies/importside-effects; headers | Architecture tests |
| Eenheid | Host | Event-, router-, config- en core-semantiek | Note On velocity nul |
| Kontrak | Host met fakes | Poorte en adaptergrense | Positional-only importer |
| Integrasie | Host | Manifest, CLI, config en simulators | Dependency closure |
| Device smoke | S2 via HIL | Boot, imports, heap, capabilities | READY markers |
| Transport HIL | S2 + DAW/controller | Werklike USB/BLE/DIN-boodskappe | Note On/Off paar |
| Standalone audio HIL | S2 + I2S backend + meetmiddel | G-C-D, penne, profiel, cleanup sonder synth | `device/i2s_test.py` -> MAX98357 |
| D1 audio HIL | S2 + D1 + backend | Waveform, Note On/Off, latency, dropout | Logic -> D1 -> MAX98357 |
| End-to-end | Logic Pro-opstelling | MVP-gebruikersvloei en herstel | Logic -> reference board -> speaker |
| Burn-in | S2 + MIDI/audio HIL | Langdurige stabiliteit, heaptrend en cleanup | 30m/8h/12h/24h profiel |

## Omgewingsmatriks

- **Primêr host:** macOS op KodeklopperM4.
- **Sekondêr host:** Windows Spelen01 en Linux/Raspberry Pi vir geordende stories.
- **Verwysingstoestel:** LOLIN/Wemos ESP32-S2 Mini, CircuitPython 10.x.
- **Tweede MCU:** post-MVP werklik BLE-geskikte CircuitPython-bord.
- **Audio:** een MAX98357 mono as MVP-verstek; ander PCM-I2S-profiele verdien afsonderlike HIL; PWM en stereo is post-MVP.
- **MIDI-stimuli:** deterministiese host-sender en Logic Pro vir MVP; generiese keyboard en MIDI-kitaar later.

Geen toestelnaam, serial-pad of audio interface word 'n universele toetskonstante nie. Die operateur kies of discovery vind dit.

## Red/Green-protokol

1. Skryf die kleinste kontrak wat die ontbrekende gedrag of vorige defek reproduseer.
2. Bewaar RED-bewys in die story review; die hoofbranch hoef nie rooi te bly nie.
3. Implementeer die kleinste klasgebaseerde verandering.
4. Loop gerigte en volledige regressie.
5. Vir fisiese gedrag: deploy presies die getoetste manifest en voer die menslike stimulus uit.

## HIL-bewysformaat

`Commit/version -> discovered connection -> deployed hashes/closure -> device startup -> stimulus -> observed events/audio -> PASS/FAIL -> recovery`.

Persoonlike UID, MAC, SSID, wagwoord en volledige serial-pad word geredigeer. 'n PASS bevat genoeg semantiese uitvoer om die kriterium te bewys, byvoorbeeld `note_on`, `note_off`, kanaal, note en `matched_notes`.

## Audio-aanvaarding

Voor luidsprekertoets word MAX98357 se BTL-uitgang, voeding en 4-8 ohm speakerlas bevestig. US-016 speel G3-C4-D4 via 'n synth-onafhanklike toepassing; US-075 verlaag amplitude, voeg startup mute by en bewys `SafeAudioOutput` se `0.08` gain/`0.25` plafon op die host. Geen direkte koptelefoon-, line-in-, grond- of potmeterverbinding tel as aanvaardingsbewys nie. Daarna bewys US-055 D1 Note On/Off deur dieselfde profielkontrak en produksie-AudioOutput-pad.

## Nie-funksionele toetsing

- Heap voor/na lang loop; geen onbegrensde groei.
- Looplatency en MIDI-eventverlies onder web-/multi-core-las.
- Timeout, Ctrl-C, soft reload en power-cycle herstel.
- Corrupte/ontbrekende config en capabilities faal veilig.
- Security: secret scan, AP-auth, request rate, geen private logs.

## Burn-in en heap-lek

`docs/burn_in_heap_stability_spec_v0.1.0.md` is normatief. Die D1-MVP vereis 'n ononderbroke 8-uur run, geen reset/hang/MemoryError nie, en finale vrye heap ná GC binne die grootste van 4096 bytes of 5% van die post-warm-up baseline. Elke toepaslike story verklaar sy profiel reeds in Definition of Ready.

## Exit-kriteria

'n Story verlaat In Review wanneer alle eksplisiete menslike/HIL-kriteria aanvaar is. 'n Release verlaat Candidate wanneer die veiligheidsgewysigde 17-story MVP Acceptance Set Done is, die Product Owner Logic-na-hoorbare-D1 aanvaar, oop risiko's aanvaar is en die tag na die geverifieerde commit wys.
