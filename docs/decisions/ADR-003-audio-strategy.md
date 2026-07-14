# ADR-003: MAX98357 mono-I2S eerste, PWM as fallback

<!--
Bestand: ADR-003-audio-strategy.md
Versienommer: 0.2.0
Doel: Stel die vroeë hoorbare I2S-pad, fallback en latere stereo-uitbreiding vas.
Sprint: Sprint 0
Epic: MCP-EPIC-003 Audio And Chip Core
User-Story: AUDIO-PRIORITY-AMENDMENT-001
Actienr: MCP-ACT-AUDIO-AMEND-ADR-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001
-->

## Status

Aanvaar; vervang die vorige PWM-eerste besluit. Stereo-implementasie volg 'n latere HIL-besluit.

## Besluit

- Een MAX98357 is die primêre eerste hoorbare backend en speel 'n mono-I2S diagnostiese toetssein.
- MCP-US-004 ontdek eers werklike `audiobusio.I2SOut`-ondersteuning en geldige penne; geen bordnaam of penkombinasie word universeel hardgekodeer nie.
- PWM bly 'n afsonderlike debug-/ossilloskoop-fallback en is nie die MAX98357 se invoer nie.
- Stereo volg later via twee MAX98357-modules of 'n geprofileerde stereo-I2S-toestel soos PCM5102.
- Alle kerne skryf na ’n `AudioOutput`-poort en ken nie die fisiese backend nie.

## Veiligheidsgrens

Die MAX98357 se luidsprekeruitgang is bridge-tied. Die twee luidsprekerterminale dryf die luidspreker direk; geen terminale word aan grond, 'n line-input of 'n tweede versterker verbind nie. Krag, luidsprekerimpedansie en bedrading word voor HIL in 'n runbook bevestig.

## Besluitmaatstawwe

- dropout/jitter tydens MIDI en webpolling;
- CPU- en heapverbruik;
- mono hoorbaarheid, dropout, geraas en veilige amplitude;
- latere stereo-integriteit en kanaalkeuse;
- bordportabiliteit en komponentkoste;
- herstelbaarheid in debugmodus.

## Gevolge

Hoorbare klank word vroeg bewys, maar 'n MAX98357 is 'n luidsprekerversterker en nie 'n pedaal-line-out nie. Die backend-poort hou toekomstige stereo-I2S, line-level DAC en PWM-diagnostiek vervangbaar.
