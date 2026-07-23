# MVP Build Plan Baseline

<!--
Bestand: MVP_BUILD_PLAN.md
Versienommer: 0.1.0
Doel: Leg die objektiewe MVP-bouplanbaseline vas sonder kode-, runtime- of argitektuurwysiging.
Sprint: Sprint 3
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-099 MVP Build Plan Baseline
Actienr: MCP-ACT-099-BUILD-PLAN-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-099
-->

## 1. Scope

### Goedgekeur binne MVP

Volgens `docs/mvp_scope_v0.1.0.md` is die MVP geslaag wanneer een herhaalbare vertikale vloei op die verwysingsbord bewys is:

- veilige boot en USB-MIDI Note On/Off uit Logic Pro;
- onafhanklike `device/i2s_test.py` wat G-C-D as square waves speel;
- MAX98357 mono-I2S op BCLK IO5, WS/LRC IO3 en DATA IO7;
- draagbare D1-basiskern met sine, saw en square;
- Logic Pro wat die D1-kern as bruikbare External MIDI synth hoorbaar speel;
- hosttoetse, HIL-bewys, herstelstappe, dokumentasie en release metadata;
- 8-uur geïntegreerde D1/USB-MIDI/I2S burn-in binne heap- en stabiliteitsgrense.

Volgens `docs/user_stories_v0.1.0.md` is die produkbewys USB-MIDI uit Logic Pro na 'n hoorbare D1-basiskern op die verwysingsbord met begrensde digitale volume.

### Buiten scope vir die eerste MVP

Volgens `docs/mvp_scope_v0.1.0.md`, `docs/agile_delivery_release_plan_v0.1.0.md` en `docs/user_stories_v0.1.0.md` is hierdie werk post-MVP of later:

- SN76489, SID, OPL2, OPL3 en ander synth cores;
- pitch bend, CC1-vibrato, Fishman TriplePlay bends/slides en MIDI clock;
- BLE-MIDI, DIN/UART, eksterne USB-host en DAW-vrye gebruik;
- stereo, per-stem routing, PCM5102/tweede MAX98357-HIL en PWM-fallback;
- Wi-Fi station/AP, webinterface, webklawerbord en sequencer;
- patchbestuur, MIDI-lêers, arpeggiator en akkoordprogressies;
- multi-core runtime, DSP, display, fisiese chips, pedaalhardeware en PCB;
- Windows-, tweede-bord- en unieke multi-device USB-identiteitsaanvaarding;
- gesertifiseerde speaker/headphone/pedal-uitsetcleanup.

## 2. MVP-doel

Die MVP is objektief gedefinieer as:

`Logic Pro External MIDI -> CoreMIDI/AppleMIDIUSBDriver -> USB -> CircuitPython usb_midi -> D1-basiskern -> MAX98357 mono-I2S -> hoorbare klank op die LOLIN/Wemos ESP32-S2 Mini verwysingsbord.`

## 3. Bouwvolgorde

| Stap | Bron | Status | Goedkeuring |
|---|---|---|---|
| 1. Veilige repository, boot, bord- en config-baseline | `docs/user_stories_v0.1.0.md`; `AGENTS.md`; ADR-001; ADR-002 | `MCP-US-001` tot `MCP-US-005`: Done volgens user-story-katalogus | Reeds in katalogus as Done gemerk |
| 2. MIDI eventmodel, USB receive, router en note semantics | `docs/user_stories_v0.1.0.md`; `docs/mcp_us_007_usb_midi_receive_review_v0.1.0.md`; `docs/mcp_us_009_note_semantics_review_v0.1.0.md` | `MCP-US-006` tot `MCP-US-009`: Done volgens user-story-katalogus | Reeds in katalogus as Done gemerk |
| 3. AudioOutput-kontrak en onafhanklike I2S-preflight | `docs/mvp_scope_v0.1.0.md`; ADR-003; `docs/mcp_us_014_audio_output_review_v0.1.0.md`; `docs/mcp_us_016_i2s_diagnostic_review_v0.1.0.md` | `MCP-US-014` en `MCP-US-016`: Done volgens user-story-katalogus | Product Owner het hoorbare G-C-D op Wemos S2 bevestig volgens katalogus |
| 4. D1-basiskern | `docs/user_stories_v0.1.0.md`; `docs/mcp_us_063_d1_core_review_v0.1.0.md` | `MCP-US-063`: Done volgens user-story-katalogus | Product Owner het v0.15.0 `d1-diagnose` aanvaar volgens katalogus |
| 5. Veilige ontwikkelvolume en prototipe-lasuitondering | `docs/user_stories_v0.1.0.md`; `docs/mcp_us_075_safe_audio_gate_review_v0.1.0.md` | `MCP-US-075`: Done met PO exception | PO exception gedokumenteer; geen produksieveiligheidsclaim |
| 6. Realtime baseline en MIDI-routeherstelpad | `docs/incidents/us_055_realtime_architecture_rebaseline_v0.1.0.md`; `docs/user_stories_v0.1.0.md` | `MCP-US-077`, `MCP-US-078`, `MCP-US-079`, `MCP-US-080`, `MCP-US-080-INV-001`: nie almal Done nie; status wissel tussen In Review en investigation | Goedgekeur as herstel-/investigation-pad volgens katalogus; finale HIL-acceptance nog oop |
| 7. Controlled native CoreMIDI route proof | `docs/evidence/mcp-us-090/final-assessment-run2.log`; `docs/evidence/mcp-us-090/live-correlation-run2.log` | `MCP-US-090`: evidence toon `LIVE_ROUTE_CONFIRMED` | Product Owner het P4N8Q2L7-akkoord gegee |
| 8. Logic Pro hoorbare D1 acceptance | `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md`; `docs/user_stories_v0.1.0.md`; `docs/mvp_scope_v0.1.0.md` | `MCP-US-055`: P0 Impediment volgens katalogus en review | UNKNOWN. Bron ontbreek vir finale aanvaarding na MCP-US-090 |
| 9. MVP release candidate en demo | `docs/user_stories_v0.1.0.md`; `docs/agile_delivery_release_plan_v0.1.0.md`; `docs/mvp_scope_v0.1.0.md` | `MCP-US-057`: MVP-Must, afhanklik van volledige acceptance set | UNKNOWN. Bron ontbreek vir uitgevoerde 8-uur burn-in en release acceptance |

## 4. Componenten

| Component | Bronbestand | Implementatiebestand | Testbestand | Evidencelocatie |
|---|---|---|---|---|
| Safe boot en USB-profiel | `docs/mcp_us_003_safe_boot_review_v0.1.0.md`; ADR-002 | `device/boot.py`; `src/midi_chip_platform/usb_boot.py` | `tests/test_usb_boot.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| Board capability discovery | `docs/mcp_us_004_board_capability_review_v0.1.0.md`; `docs/board_capability_matrix_v0.1.0.md` | `src/midi_chip_platform/platform_capabilities.py` | `tests/test_platform_capabilities.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| Configuration boundary | `docs/mcp_us_005_configuration_secret_boundary_review_v0.1.0.md` | `src/midi_chip_platform/configuration.py`; `device/settings.toml.example` | `tests/test_configuration.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| MIDI eventmodel | `docs/mcp_us_006_portable_event_model_review_v0.1.0.md` | `src/midi_chip_platform/events.py`; `src/midi_chip_platform/midi_semantics.py` | `tests/test_domain_events.py`; `tests/test_midi_semantics.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| USB MIDI receive | `docs/mcp_us_007_usb_midi_receive_review_v0.1.0.md`; `docs/evidence/mcp-us-090/live-device-capture-run2.log` | `src/midi_chip_platform/midi_usb.py` | `tests/test_usb_midi_receive.py` | `docs/evidence/mcp-us-090/` vir controlled route proof |
| MIDI router | `docs/mcp_us_008_midi_channel_router_review_v0.1.0.md` | `src/midi_chip_platform/routing.py` | `tests/test_midi_routing.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| AudioOutput en safety | `docs/mcp_us_014_audio_output_review_v0.1.0.md`; `docs/mcp_us_075_safe_audio_gate_review_v0.1.0.md`; ADR-003 | `src/midi_chip_platform/audio.py` | `tests/test_audio_output.py`; `tests/test_audio_safety.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| Standalone I2S diagnose | `docs/mvp_scope_v0.1.0.md`; ADR-003 | `device/i2s_test.py` | `tests/test_i2s_diagnostic.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| I2S runtime output | `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md` | `src/midi_chip_platform/i2s_audio.py` | `tests/test_i2s_audio_output.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| D1 core | `docs/mcp_us_063_d1_core_review_v0.1.0.md` | `src/midi_chip_platform/d1_core.py`; `src/midi_chip_platform/core.py` | `tests/test_d1_core.py`; `tests/test_core_registry.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |
| D1 USB-MIDI runtime | `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md`; `docs/incidents/us_055_realtime_architecture_rebaseline_v0.1.0.md` | `src/midi_chip_platform/d1_runtime.py`; `src/midi_chip_platform/device_runtime.py`; `device/code.py` | `tests/test_d1_usb_midi_runtime.py`; `tests/test_device_runtime.py` | UNKNOWN. Bron ontbreek vir post-MCP-US-090 acceptance evidence |
| Realtime baseline | `docs/incidents/us_055_realtime_architecture_rebaseline_v0.1.0.md` | `src/midi_chip_platform/realtime_baseline.py` | `tests/test_realtime_baseline.py` | UNKNOWN. Bron ontbreek vir closed acceptance evidence |
| Persistent synthio baseline | `docs/mcp_us_079_persistent_synthio_audio_graph_plan_v0.1.0.md`; ADR-004 | `src/midi_chip_platform/synthio_runtime.py` | `tests/test_synthio_runtime.py` | UNKNOWN. Bron ontbreek vir HIL PASS evidence |
| MIDI routing diagnostic | `docs/mcp_us_080_usb_midi_routing_diagnostic_review_v0.1.0.md`; `docs/mcp_us_080_inv_001_instrumentation_design_review_v0.1.0.md` | `src/midi_chip_platform/midi_routing_diagnostic.py` | `tests/test_midi_routing_diagnostic.py` | `docs/evidence/mcp-us-080-inv-001/`; `docs/evidence/mcp-us-080-inv-002/`; `docs/evidence/mcp-us-080-inv-003/` |
| Native CoreMIDI route proof helper | `docs/evidence/mcp-us-090/final-assessment-run2.log` | `tools/investigation/mcp_us_090_live_route_probe.swift` | UNKNOWN. Bron ontbreek vir unit-testbestand; helper evidence is live-run gebaseer | `docs/evidence/mcp-us-090/` |
| HIL runner | `docs/mcp_us_051_hil_runner_review_v0.1.0.md`; `docs/agile_delivery_release_plan_v0.1.0.md` | `src/midi_chip_platform/hil.py`; `src/midi_chip_platform/cli.py` | `tests/test_hil.py`; `tests/test_cli.py` | UNKNOWN. Bron ontbreek vir huidige per-step evidencepad |

## 5. Acceptance

| Stap | RED-test | GREEN-implementatie | HIL-acceptatie |
|---|---|---|---|
| Safe boot en USB-profiel | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-003` Done volgens katalogus | Device proof volgens `docs/mcp_us_003_safe_boot_review_v0.1.0.md` |
| Board capability discovery | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-004` Done volgens katalogus | Wemos S2 rapporteer profiel, IO3/5/7, modules en geheue volgens katalogus |
| Config boundary | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-005` Done volgens katalogus | v0.12.3 rapporteer private velde `UNSET` en execution `READY` volgens katalogus |
| USB MIDI receive | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-007` Done volgens katalogus | v0.12.2 ontvang Note On, Note Off en ooreenstemmende nootpaar as PASS volgens katalogus |
| I2S preflight | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `device/i2s_test.py` volgens ADR-003 en `MCP-US-016` | Product Owner het G3-C4-D4 hoorbaar bevestig volgens katalogus |
| D1 core | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-063` Done volgens katalogus | Host `d1-diagnose` PASS; hoorbare Logic/I2S volg onder US-055/US-051 volgens katalogus |
| Safe audio gate | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | `MCP-US-075` Done met PO exception | v0.16.0 hoorbare G-C-D HIL en prototipe-lasuitondering volgens katalogus |
| CoreMIDI route proof | UNKNOWN. Bron ontbreek in hierdie baseline vir RED-stap | Swift CoreMIDI helper in `tools/investigation/mcp_us_090_live_route_probe.swift` | `docs/evidence/mcp-us-090/live-correlation-run2.log` toon `LIVE_ROUTE_CONFIRMED` |
| Persistent realtime audio graph | `docs/mcp_us_079_persistent_synthio_audio_graph_plan_v0.1.0.md` meld hosttests bewys geen per-event audio-play | `src/midi_chip_platform/synthio_runtime.py` bestaan; `MCP-US-079` is In Review / HIL Ready volgens katalogus | UNKNOWN. Bron ontbreek vir HIL PASS; plan vereis 20 Logic NoteOns hoorbaar realtime |
| Logic Pro hoorbare D1 acceptance | UNKNOWN. Bron ontbreek vir post-MCP-US-090 RED-test | UNKNOWN. Bron ontbreek vir goedgekeurde post-MCP-US-090 implementasiestap | UNKNOWN. Bron ontbreek vir PO-aanvaarde hoorbare Logic -> D1 -> MAX98357 demo |
| MVP release candidate | UNKNOWN. Bron ontbreek vir RED-test | UNKNOWN. Bron ontbreek vir release implementation step | UNKNOWN. Bron ontbreek vir 8-uur burn-in en release acceptance |

## 6. Open blokkades

| Blokkade | Bron | Status |
|---|---|---|
| MCP-US-055 is steeds as P0 impediment gemerk | `docs/user_stories_v0.1.0.md`; `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md` | Oop |
| ADR-004 is `Proposed`, maar `MCP-US-079` verwys daarna as afhanklikheid | `docs/decisions/ADR-004-persistent-realtime-audio-graph.md`; `docs/user_stories_v0.1.0.md` | Oop |
| Post-MCP-US-090 implementasiestap vir MCP-US-100 ontbreek | Hierdie baseline teen bestaande docs | Oop |
| HIL PASS vir `MCP-US-079` ontbreek | `docs/mcp_us_079_persistent_synthio_audio_graph_plan_v0.1.0.md`; `docs/user_stories_v0.1.0.md` | Oop |
| US-057 8-uur burn-in en release evidence ontbreek | `docs/mvp_scope_v0.1.0.md`; `docs/agile_delivery_release_plan_v0.1.0.md`; `docs/user_stories_v0.1.0.md` | Oop |
| Sommige componenten het geen eenduidige per-step evidencepad | Componenttabel hierbo | Oop |

### Dokumentkonflikte

| Document A | Document B | Conflict |
|---|---|---|
| `docs/mvp_scope_v0.1.0.md` | `docs/user_stories_v0.1.0.md` | Die MVP Acceptance Set in `mvp_scope` lys nie `US-077`, `US-078`, `US-079`, `US-080`, `MCP-US-080-INV-001` of `MCP-US-090` as formele MVP-set items nie; `user_stories` voeg herstel-/investigation-stories by vir MVP-aanvaarding. |
| `AGENTS.md` | `docs/mvp_scope_v0.1.0.md` | `AGENTS.md` meld die bindende oorblywende pad as `US-016 -> US-063 -> US-055 -> US-057`; `mvp_scope` meld `MCP-US-016 -> MCP-US-063 -> MCP-US-075 -> MCP-US-055 -> MCP-US-057`. |
| `docs/decisions/ADR-004-persistent-realtime-audio-graph.md` | `docs/user_stories_v0.1.0.md` | ADR-004 is `Proposed`; `MCP-US-079` se afhanklikheid verwys na ADR-004. |
| `docs/mcp_us_055_logic_d1_i2s_review_v0.1.0.md` | `docs/evidence/mcp-us-090/final-assessment-run2.log` | US-055 review is nog P0 impediment; MCP-US-090 bewys slegs native CoreMIDI-route, nie die hoorbare D1/I2S productflow nie. |

## 7. Definitie van MVP

Die MVP is een klein, herhaalbare demo op die LOLIN/Wemos ESP32-S2 Mini verwysingsbord:

1. Die toestel begin veilig en herstelbaar.
2. Die gebruiker kies die bord as Logic Pro External MIDI destination.
3. Logic Pro stuur Note On/Off oor die bewese native CoreMIDI/AppleMIDIUSBDriver/USB-pad.
4. CircuitPython `usb_midi` ontvang die musikale Note On/Off events.
5. Die D1-basiskern speel hoorbare sine, saw of square deur die MAX98357 mono-I2S-uitvoer.
6. Die onafhanklike `device/i2s_test.py` bly beskikbaar as fisiese G-C-D audio-preflight.
7. Die demo het hosttoetse, HIL-bewys, evidence, dokumentasie, release metadata en 8-uur burn-in.

MVP is nog nie objektief Done volgens die bestaande dokumentasie nie, omdat `MCP-US-055` en `MCP-US-057` nog oop is en 'n post-MCP-US-090 implementasiestap ontbreek.
