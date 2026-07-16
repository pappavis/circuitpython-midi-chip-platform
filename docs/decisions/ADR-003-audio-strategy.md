# ADR-003: Standalone I2S-diagnose eerste, MAX98357 as verstek

<!--
Bestand: ADR-003-audio-strategy.md
Versienommer: 0.3.0
Doel: Stel die onafhanklike vroeë I2S-diagnose, produksiegrens en latere uitbreidings vas.
Sprint: Sprint 2
Epic: MCP-EPIC-003 Audio And Chip Core
User-Story: MCP-US-016 Standalone I2S Audible Diagnostic
Actienr: MCP-ACT-MVP-SCOPE-001-ADR-003
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MVP-SCOPE-REDUCTION-001
-->

## Status

Aanvaar. Hierdie weergawe vervang die breër mono-I2S/PWM-MVP-besluit.

## Besluit

- MCP-US-016 lewer `device/i2s_test.py`: 'n klasgebaseerde, synth-onafhanklike toepassing wat G-C-D as square waves speel.
- Die lêer importeer nie `midi_chip_platform`, D1, die core registry of die normale Application-runtime nie.
- MAX98357 mono-I2S is die fisies gevalideerde verstek op BCLK IO5, WS/LRC IO3 en DATA IO7.
- Penne, sample rate, amplitude, duur en adapterprofiel word deur 'n klasinstansie besit en ingespuit; geen globale veranderlikes of modulevlak helperfunksies word gebruik nie.
- Ander standaard PCM-I2S-modules kan dieselfde profielkontrak gebruik. 'n Modulenaam word eers as fisies gevalideer gepubliseer nadat spesifieke HIL slaag.
- Die standalone toepassing en die synth-runtime gebruik die I2S-backend nooit gelyktydig nie; elke toepassing skep, gebruik en sluit die hulpbron.
- Die normale D1-kern skryf later deur die `AudioOutput`-poort en ken nie die fisiese backend nie.
- Die produksiepoort gebruik begrensde interleaved signed 16-bit PCM-blokke met eksplisiete sample rate, mono/stereo-kanaaltelling en frames-per-block; cores render blokke en nie individuele Python-samples nie.
- PWM, stereo en die geïntegreerde US-020-opstartmelodie is post-MVP werk of 'n eksplisiete impediment-contingency.

## Waarom onafhanklikheid doelbewus is

Die diagnose onderskei 'n fisiese I2S-, pen-, voeding- of versterkerprobleem van 'n fout in MIDI, D1, routing of runtime-integrasie. Die klein hoeveelheid dubbele laevlak-I2S-opstelling is aanvaarbaar omdat 'n gedeelde synth-import hierdie diagnostiese waarde sou vernietig.

Drift word beheer deur dieselfde benoemde profielvelde, AST-/importtoetse, frekwensietoetse en gepaarde HIL-dokumentasie. Geen runtime-kode word tussen die twee toepassings gedeel nie.

## Veiligheidsgrens

Die MAX98357 se luidsprekeruitgang is bridge-tied. Die twee luidsprekerterminale dryf die luidspreker direk; geen terminale word aan grond, 'n line-input of 'n tweede versterker verbind nie. Krag, luidsprekerimpedansie en bedrading word voor HIL in 'n runbook bevestig.

## Besluitmaatstawwe

- hoorbare G3-C4-D4 en gemete frekwensie/toleransie;
- veilige amplitude, geen hang en herhaalbare hulpbronvrystelling;
- geheue voor/ná die toets;
- profiel- en penversoenbaarheid;
- geen synth-import of modulevlak runtime-status;
- afsonderlike HIL-status per I2S-module.

## Gevolge

Die klankhardeware kan voor D1 onafhanklik bewys word. MAX98357 is die MVP-verwysing, maar die konstruktor-/profielgrens laat latere PCM5102- of ander standaard I2S-adapters toe sonder dat onbevestigde fisiese ondersteuning geclaim word.
