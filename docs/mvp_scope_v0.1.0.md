# MVP-omvang

<!--
Bestand: mvp_scope_v0.1.0.md
Versienommer: 0.11.0
Doel: Definieer die verkleinde eerste toetsbare CircuitPython MIDI Chip Platform MVP.
Sprint: Sprint 2
Epic: MCP-EPIC-001, MCP-EPIC-002, MCP-EPIC-003 en MCP-EPIC-008
User-Story: MCP-US-055, MCP-US-075 en MCP-US-076
Actienr: MCP-ACT-055-IN-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-055-START
-->

## Langtermyn-produkdefinisie

'n MIDI-beheerde, multi-kern retro-sintetiseerdermodule in pedaalvorm, met USB-MIDI, stereo-klankuitvoer, plaaslike webbeheer en uitbreibare chip-emulasie. Hierdie visie bly staan; dit is nie alles deel van die eerste MVP nie.

## Primêre MVP-gebruiker

'n Logic Pro-gebruiker wat die LOLIN/Wemos ESP32-S2 Mini as External MIDI destination kan kies en die D1-basiskern deur 'n gekoppelde I2S-klankmodule wil hoor.

## MVP-produkhek

Die MVP is geslaag wanneer een herhaalbare vertikale vloei op die verwysingsbord bewys is:

1. Die bord begin veilig en ontvang USB-MIDI Note On/Off uit Logic Pro.
2. 'n Onafhanklike `device/i2s_test.py` speel G-C-D as square waves sonder enige import uit die synth-runtime.
3. MAX98357 mono-I2S op BCLK IO5, WS/LRC IO3 en DATA IO7 is die verstek en fisies hoorbaar gevalideer.
4. Die draagbare D1-basiskern speel sine, saw en square via die geverifieerde AudioOutput-pad.
5. Logic Pro kan die D1-kern as 'n bruikbare External MIDI synth speel en hoor.
6. Hosttoetse, HIL-bewys, herstelstappe, dokumentasie en release metadata is op datum.
7. Die geïntegreerde D1/USB-MIDI/I2S-pad voltooi 'n 8-uur burn-in binne die meetbare heap- en stabiliteitsgrense.

## Bevrore MVP Acceptance Set

Slegs hierdie stories beheer MVP-aanvaarding:

`MCP-US-001`, `MCP-US-002`, `MCP-US-003`, `MCP-US-004`, `MCP-US-005`, `MCP-US-006`, `MCP-US-007`, `MCP-US-008`, `MCP-US-009`, `MCP-US-014`, `MCP-US-016`, `MCP-US-050`, `MCP-US-051`, `MCP-US-055`, `MCP-US-057`, `MCP-US-063` en die veiligheidshek `MCP-US-075`.

`MVP-Enabler`-stories bou die veilige kontrakte. `MVP-Must`-stories lewer die eindgebruiker se direkte hoorbare bewys. Reeds voltooide werk buite hierdie lys bly waardevol, maar verbreed nie die releasehek nie.

## Standalone I2S-diagnose

MCP-US-016 besit die gevraagde eenvoudige toets en word nie gedupliseer nie.

- Die lêer is `device/i2s_test.py` en het geen afhanklikheid op `midi_chip_platform`, D1 of enige ander synth core nie.
- Alle veranderlike status behoort aan klasse; daar is geen globale veranderlikes, `global`-statements of modulevlak helperfunksies nie.
- Die toepassing genereer veilige square waves vir G3, C4 en D4, speel hulle opeenvolgend en stel I2S daarna vry.
- MAX98357 is die verstekprofiel. Penne, sample rate, amplitude, nootduur en 'n standaard PCM-I2S-adapterprofiel word deur constructor/config ingespuit.
- Ander standaard I2S-modules soos PCM5102 kan dieselfde profielgrens gebruik, maar word eers as fisies ondersteun aangedui nadat hulle eie HIL slaag.
- Die diagnose loop nie gelyktydig met die normale synth-runtime nie; albei besit dieselfde fisiese I2S-hulpbron eksklusief.

MCP-US-020 bly 'n aparte post-MVP-story vir 'n geïntegreerde, opsionele G-C-D-opstartmelodie deur die D1-runtime.

## Binne MVP

- Een verwysingsbord: LOLIN/Wemos ESP32-S2 Mini met CircuitPython 10.x.
- Veilige boot, capability discovery en private configuration boundary.
- USB-MIDI device mode en Note On/Off/velocity-semantiek wat in Logic bewys is.
- AudioOutput-poort, Null backend en die onafhanklike I2S-diagnose.
- D1 sine-, saw- en square-wave basiskern.
- MAX98357 mono-I2S as fisies gevalideerde verstek.
- Host-eenheid-/kontraktoetse, HIL-runner, herstelrunbook en eerlike release metadata.

## Ná MVP

- SN76489-lite as tweede kern; daarna 6581 SID, OPL2 en OPL3.
- Pitch bend, CC1-modulasie, Fishman TriplePlay bends/slides en MIDI clock.
- BLE-MIDI, DIN/UART, eksterne USB-host en DAW-vrye gebruik.
- Stereo, per-stem routing, PCM5102/tweede MAX98357-HIL en PWM-fallback.
- Wi-Fi station/AP fallback, webinterface, webklawerbord en sekwenser.
- Patchbestuur, MIDI-lêers, arpeggiator en akkoordprogressies.
- Multi-core runtime, resource guard, DSP, display, fisiese chips, pedaalhardeware en PCB.
- Windows-, tweede-bord- en unieke multi-device USB-identiteitsaanvaarding.

## MVP-sukseskriteria

- `device/i2s_test.py` speel G-C-D hoorbaar deur die MAX98357 en kan herhaalbaar herstart word.
- Die standalone toets het geen synth-package-imports en slaag die class/no-globals AST-kontrak.
- Logic Pro stuur ten minste een ooreenstemmende Note On/Off-paar na die verwysingsbord.
- D1 sine, saw en square is hoorbaar; Note Off stop die stem sonder hangende noot.
- Die klanktoets en D1-pad gebruik dieselfde gedokumenteerde pen-/profielwaardes sonder runtime-koppeling.
- Alle MVP Acceptance Set-stories is Done en die PO aanvaar die hoorbare Logic-demo.
- Die 8-uur MVP burn-in het geen reset, hang, permanente stilte of onverklaarde USB-ontkoppeling nie; heap bly binne die grens in `burn_in_heap_stability_spec_v0.1.0.md`.
- Geen geheime, rou toestelidentifiseerders of plaaslike hardeware-name is in die openbare repository nie.

## Geordende pad

`MCP-US-016 -> MCP-US-063 -> MCP-US-075 -> MCP-US-055 -> MCP-US-057`

MCP-US-005, MCP-US-014, MCP-US-016, MCP-US-063 en MCP-US-075 is gesluit. US-075 se v0.16.0 softwarehek en hoorbare HIL is met 'n eksplisiete prototipe-lasuitondering aanvaar; US-076 parkeer gesertifiseerde uitsetcleanup ná MVP. US-055 is v0.17.3 In Review: USB-MIDI, D1 en veilige I2S is op host groen, idle stuur nie meer deurgaande silence na I2S nie, kort Logic-notes kry 'n minimum hoorbare buffer, lae Logic velocities kry HIL audition gain, en die story wag op Logic/HIL-hoorbaarheid.

## Besluithekke

1. **Configuration-hek:** MCP-US-005 se SET/UNSET-bewys is fisies gesluit.
2. **Diagnose-hek:** die onafhanklike G-C-D-toets moet hoorbaar wees voordat D1 begin.
3. **D1-hek:** SN76489 en elke volgende kern begin eers ná die aanvaarbare D1/Logic MVP.
4. **Profiel-hek:** 'n nuwe I2S-module kry eers 'n profiel en fisiese HIL voordat dokumentasie dit as gevalideer beskryf.
5. **Scope-hek:** web, BLE, stereo, DSP, multi-core en ander uitbreidings kan nie stilweg die bevrore MVP verbreed nie.
