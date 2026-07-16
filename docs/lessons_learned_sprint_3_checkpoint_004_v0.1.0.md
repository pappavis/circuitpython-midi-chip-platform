# Sprint 3 Lessons Learned - Checkpoint 004

<!--
Bestand: lessons_learned_sprint_3_checkpoint_004_v0.1.0.md
Versienommer: 0.1.0
Doel: Konsolideer AudioOutput-, I2S-, D1- en fisiese uitsetveiligheidslesse.
Sprint: Sprint 3
Epic: MCP-EPIC-003, MCP-EPIC-007 en MCP-EPIC-008
User-Story: MCP-US-014, MCP-US-016, MCP-US-063 en MCP-US-075
Actienr: MCP-ACT-SPRINT-3-LESSON-004
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-063-HOST-ACCEPTED-001
-->

## Uitkoms

Die platform het drie opeenvolgende hekke geslaag: 'n begrensde AudioOutput-kontrak, hoorbare G-C-D deur die werklike Wemos S2/MAX98357A-pad en 'n draagbare D1 sine/saw/square-kern. Die Product Owner het beide die fisiese I2S-toets en die deterministiese D1-hostdiagnose aanvaar. Die volgende vertikale sny is Logic USB-MIDI na hoorbare D1, maar 'n nuwe fisiese veiligheidsfeit moet eers beheer word: die huidige toetslas is 'n goedkoop TRS-koptelefoon direk op die bridge-tied MAX98357A-uitset, sonder fisiese volumebeheer.

## Wat goed gewerk het

- Die synth-onafhanklike `i2s_test.py` het bedrading en versterker van MIDI/D1 geïsoleer.
- Serial het frekwensie, penprofiel, heap en PASS gewys; “ek hoor iets” was nie die enigste bewys nie.
- Die draagbare D1-kern het sonder NumPy, desktop-audio of bordimports 114 toetse geslaag.
- `d1-diagnose` het die Product Owner 'n eenvoudige, herhaalbare hostaanvaarding gegee.
- Die streng storyvolgorde het voorkom dat SN76489, web of multi-core die eerste hoorbare pad versteur.

## Wat verbeter moet word

| Waarneming | Risiko/oorsaak | Verbetering |
|---|---|---|
| Direkte koptelefoon was hoorbaar slegs links | Een mono BTL-uitset is aan een TRS-drywer gekoppel | Behandel dit slegs as historiese bewys; gebruik voortaan 'n 4-8 ohm luidspreker |
| Geen fisiese volumebeheer nie | MAX98357A verstek-GAIN is 9 dB; digitale amplitude was die enigste begrensing | US-075 besluit software master gain, laer GAIN-pinprofiel en veilige startup mute |
| 'n Gewone potmeter lyk na 'n maklike oplossing | BTL `+/-` is nie 'n grondverwysde analoogpad nie | Geen enkelpotmeter in die luidsprekeruitset; kies digitale beheer of 'n geskikte DAC/headphone-amp-argitektuur |
| Programmatiese hard reset het USB tydelik laat verdwyn | Her-enumerasie/herstelgedrag is nie volledig deterministies nie | Fisiese power-cycle bly in die recovery-runbook; finale HIL meet resetherstel |
| Hoorbare G-C-D het geslaag maar die banner was nog US-016 v0.14.0 | Die toestelartefak was ouer as die aktiewe US-075-repositoryweergawe | Klassifiseer klank volgens runtimebanner; deploy, hard reset en voer die volledige HIL-runner uit voor storyaanvaarding |
| Host-D1 PASS is nog nie hoorbare D1 nie | Produksie-I2S-adapter/composition root is nog nie gebou nie | US-055 bly die eerste geldige Logic-na-hoorbare-D1 claim |
| Fisiese ontwerpwerk was te generies in US-047/048 | Breadboard-, meet- en KiCad-samewerking was nie eksplisiet nie | Versterk US-047/048 met volume, veilige uitsette, testpunte, BOM, ERC/DRC en bring-up |

## Besluite en aksies

| Aksie | Eienaar | Story/hek | Status |
|---|---|---|---|
| Ontkoppel die koptelefoon voor volgehoue D1-toetse; moenie dit dra terwyl dit direk verbind is nie | Product Owner | Onmiddellik | Mensaksie |
| Verkry 'n 4-8 ohm bewegende-spoel-luidspreker met geskikte kraggradering | Product Owner/Hardware | US-076 | Later |
| Dokumenteer software amplitude ceiling, startup mute, GAIN en SD/MODE-keuses | DSP/Embedded/Hardware | US-075 | Backlog |
| Besluit afsonderlik oor speaker, headphone en pedal line-out; MAX98357 is nie al drie nie | Solution Architect/Hardware | US-047/076 | Later |
| Bou en meet 'n reproduceerbare breadboard-uitset met veilige scope-punte | Hardware/QA | US-047/076 | Later |
| Ontwerp later die KiCad-skema/PCB saam met die ervare Product Owner | Hardware/PCB/PO | US-048 | Backlog |
| Begin US-055 ná PO-aanvaarding van die begrensde prototipeprofiel; maak geen produksieveiligheidsclaim nie | Scrum/QA | US-075 -> US-055 | Voltooi met uitsondering |
| Vereis verwagte weergawe en story in elke menslike HIL-uitvoer | QA/Release | Alle HIL-stories | Beheer aktief |

## Hergebruikreël

Vir elke nuwe synth of drum-machine moet die eerste hoorbare HIL nie net penne en klank bewys nie, maar ook die **las**, impedansie, gain, maksimum amplitude, mute/herstel, veilige meetpunt en menslike luisterafstand benoem. 'n Hoorbare uitset is nie outomaties 'n veilige headphone-, line- of pedal-uitset nie.

Verder word 'n hoorbare resultaat nooit aan die aktiewe story toegeskryf sonder 'n ooreenstemmende runtimeweergawe en story-ID nie. 'n Ouer banner bewys slegs regressie van daardie ouer artefak; repository-, deployment-, boot- en execution-bewys moet eers almal groen wees.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het I2S en D1 aanvaar en die werklike TRS/full-volume toestand openbaar gemaak. |
| Scrum Master | Voeg slegs die noodsaaklike US-075 veiligheidshek voor US-055 in. |
| Business Analyst | Skei speaker-, headphone- en pedal line-out gebruikersbehoeftes. |
| Chief Enterprise Architect | Verhoed dat MAX98357 as universele AudioOutput-implementasie behandel word. |
| Solution Architect | Beplan aparte adapters/profiele vir speaker en toekomstige DAC/headphone/line-uitset. |
| Embedded Engineer | Besit GAIN-, SD/MODE-, startup mute- en digitale amplitudegedrag. |
| MIDI Engineer | Not impacted; Note On/Off-kontrak bly onveranderd. |
| DSP/Chip Engineer | Definieer begrensde master gain sonder PCM clipping. |
| Hardware/PCB Engineer | Lewer veilige breadboard, testpunte, beskerming, skema, PCB en BOM. |
| QA/HIL Engineer | Voeg las, impedansie, volume en herstel by elke hoorbare toets. |
| Release/Documentation | Hou US-055 geblokkeer totdat die veiligheidshek aanvaar is. |
| External Architecture Reviewer | Primêre datasheet/vendorbronne bly die elektriese gesag. |
| Devil's Advocate | Hoorbare sukses mag nie gehoor- of hardewareskade normaliseer nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
