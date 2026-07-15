# Test Strategy

<!--
Bestand: test_strategy_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer die toetsvlakke, omgewings, hardewarematriks en aanvaardingsbewys.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-066 Quality Manual, Test Strategy And Review Engine
Actienr: MCP-ACT-066-TEST-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
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
| Audio HIL | S2 + backend + meetmiddel | Hoorbaarheid, kanaal, latency, dropout | MAX98357 tone/note |
| End-to-end | Musikantopstelling | Gebruikersvloei en herstel | Controller -> pedal -> speaker |

## Omgewingsmatriks

- **Primêr host:** macOS op KodeklopperM4.
- **Sekondêr host:** Windows Spelen01 en Linux/Raspberry Pi vir geordende stories.
- **Verwysingstoestel:** LOLIN/Wemos ESP32-S2 Mini, CircuitPython 10.x.
- **Tweede MCU:** werklik BLE-geskikte CircuitPython-bord vir positiewe BLE-HIL.
- **Audio:** een MAX98357 mono eerste; PWM as meetbare fallback; stereo later.
- **MIDI-stimuli:** deterministiese host-sender, Logic Pro, generiese keyboard en later MIDI-kitaar.

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

Voor luidsprekertoets word MAX98357 se BTL-uitgang en voeding bevestig. Die eerste test gebruik veilige amplitude. Meet: sample rate, bufferduur, beginlatency, dropout, heap en cleanup. Hoorbaar is nodig vir die demo; ossilloskoop/telemetrie maak die resultaat vergelykbaar.

## Nie-funksionele toetsing

- Heap voor/na lang loop; geen onbegrensde groei.
- Looplatency en MIDI-eventverlies onder web-/multi-core-las.
- Timeout, Ctrl-C, soft reload en power-cycle herstel.
- Corrupte/ontbrekende config en capabilities faal veilig.
- Security: secret scan, AP-auth, request rate, geen private logs.

## Exit-kriteria

'n Story verlaat In Review wanneer alle eksplisiete menslike/HIL-kriteria aanvaar is. 'n Release verlaat Candidate wanneer alle Must-stories Done is, oop risiko's aanvaar is, installasie/herstel herhaal is en die tag na die geverifieerde commit wys.
