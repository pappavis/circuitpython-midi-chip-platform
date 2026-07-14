# Audio Priority Amendment

<!--
Bestand: audio_priority_amendment_v0.1.0.md
Versienommer: 0.1.0
Doel: Formaliseer MAX98357-eerste klank, PWM-fallback, MIDI-kitaar-slides en release-naspeurbaarheid.
Sprint: Sprint 0
Epic: MCP-EPIC-001, MCP-EPIC-002 en MCP-EPIC-003
User-Story: AUDIO-PRIORITY-AMENDMENT-001
Actienr: MCP-ACT-AUDIO-AMEND-REV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001
-->

## Product Owner-besluit

1. `Synth` beteken voortaan die CircuitPython MIDI Chip Platform, tensy `python-d1-synth` eksplisiet genoem word.
2. Die eerste hoorbare uitset gebruik een MAX98357 in mono-I2S-modus.
3. PWM is 'n diagnostiese fallback; dit is nie 'n MAX98357-invoer of finale line-out nie.
4. Stereo volg later via twee MAX98357-modules of 'n geprofileerde stereo-I2S-backend soos PCM5102.
5. Generiese MIDI-kitaarondersteuning sluit akkoorde, per-kanaal bends en slides in. Fishman TriplePlay is 'n verwysings-HIL-toestel en nooit 'n hardgekodeerde toestelnaam nie.
6. Elke startup toon die projekweergawe, aktiewe story/amendment en release-datum.

## Geordende hoorbare pad

`MCP-US-003 -> MCP-US-004 -> MCP-US-014 -> MCP-US-016 -> MCP-US-015`

- US-003 lewer veilige boot en USB-identiteit.
- US-004 bewys werklike bord-, module- en penvermoëns.
- US-014 hou die klankbackend vervangbaar.
- US-016 lewer die eerste veilige, hoorbare MAX98357 mono-toetssein.
- US-015 bewys PWM wanneer I2S nie beskikbaar of stabiel is nie.

## Guitar-MIDI-verfyning

- **MCP-US-058** bou platform-onafhanklike multi-kanaal bend- en slide-semantiek met konfigureerbare bend range.
- **MCP-US-059** bewys fisiese note, akkoorde, bends en slides met 'n generiese MIDI-kitaar en Fishman TriplePlay as een verwysing.
- Fishman se Trigger, Auto, Smooth en Step bend modes word as toetsvariante behandel; die platform probeer nie Fishman-firmware naboots nie.

## Release-identiteit

Release `0.1.1` toon by host-start:

```text
circuitpython-midi-chip-platform v0.1.1 | story=AUDIO-PRIORITY-AMENDMENT-001 | release-date=2026-07-14
```

Dieselfde klasgebaseerde metadata-kontrak word later deur CircuitPython `code.py` gebruik. Metadata begin geen hardeware tydens import nie.

## Spanbydraerekord

| Rol | Bydrae |
|---|---|
| Sales/Discovery | Vroeë hoorbare klank en kitaar-ekspressie maak die produkwaarde demonstreerbaar. |
| Business Analyst | Het mono-eerste, PWM-fallback, later-stereo en slide-uitkomste van implementasiedetail geskei. |
| Product Owner | Het MAX98357, synth-betekenis, Fishman-verwysing en startup-naspeurbaarheid aanvaar. |
| Scrum Master | Het die klankprioriteit as backlog-amendment verwerk sonder om US-003 oor te slaan. |
| Solution Architect | Het die vervangbare `AudioOutputPort`, bordprofiele en metadata-instansiegrens behou. |
| Embedded Engineer | Vereis vermoënsontdekking voor I2S-pengebruik en 'n herstelbare bootpad. |
| MIDI Engineer | Het per-kanaal bend-state, konfigureerbare bend range en afsonderlike host/HIL-stories voorgestel. |
| DSP/Chip Engineer | Gebruik eers 'n begrensde toetssein; die SN76489-kern bly in sy bestaande story. |
| Web Engineer | Not impacted: geen webkode verander nie; backend-kontrakte bly invoerveilig. |
| QA/HIL Engineer | Vereis rooi/groen startup-toets, MAX98357-bedradingskontrole en latere Fishman/generiese HIL. |
| Release/Documentation | Hou pakketweergawe, banner, ChatID, backlog, ADR en Kanban versoen. |
| Devil's Advocate | Waarsku dat MAX98357 bridge-tied luidsprekeruitset nie as geaarde line-out gebruik mag word nie. |

## Bronne

- https://docs.circuitpython.org/en/stable/shared-bindings/audiobusio/
- https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview
- https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts
- https://fishman.com/tripleplay-support/
- https://a11.fishman.com/wp-content/uploads/2024/12/TriplePlayUtility-UserGuide.pdf
