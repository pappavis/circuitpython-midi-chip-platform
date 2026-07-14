# MCP-US-004 Board Capability Review

<!--
Bestand: mcp_us_004_board_capability_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer capability discovery, MAX98357A-penkontrole, toetse en HIL-impediment.
Sprint: Sprint 1
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-004 Board Capability Discovery
Actienr: MCP-ACT-004-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004-IN-REVIEW
-->

## Status

**DONE.** Die klasgebaseerde implementering, host-regressie, sagte toestel-capability-run, fisiese power-cycle recovery en finale connection/deployment/boot/execution-HIL is groen.

## Gelewer

- `BoardProfileRegistry` bevat 'n eksplisiete LOLIN S2 Mini-profiel; onbekende borde kry geen veronderstelde penne nie.
- `ImportModuleProbe` ontdek modules via 'n geïnjekteerde importer en begin geen diens tydens import nie.
- `MemoryProbe` rapporteer vrye en geallokeerde heap sonder globale status.
- `BoardCapabilityDiscovery` lei slegs backends af indien module én profielpenne beskikbaar is.
- Runtime-uitvoer bevat geen UID, MAC, SSID, wagwoord, objekadres of serial-poort nie.
- Startup-identiteit is `v0.4.0 | story=MCP-US-004 | release-date=2026-07-14`.

## MAX98357A-bedradingsbesluit

| LOLIN S2 Mini | I2S-rol | MAX98357A |
|---|---|---|
| IO5 | bit clock | BCLK |
| IO3 | word select | LRC/WS |
| IO7 | serial data out | DIN of SDIN |
| GND | gemeenskaplike grond | GND |
| 5 V-breadboardrail | versterkerkrag | VIN |

Belangrik: 'n pen wat letterlik `SD/MODE` gemerk is, is shutdown/kanaalseleksie en nie die I2S-data-in nie. IO7 mag slegs na `DIN`/`SDIN` gaan. Die luidspreker gaan direk tussen die bridge-tied `+` en `-` uitsette; geen luidsprekerterminaal gaan na grond of 'n line-input nie. Klankaktivering bly buite hierdie story.

## RED/GREEN en HIL-bewys

- RED: toetsinsameling het met die verwagte `ModuleNotFoundError` vir `platform_capabilities` gefaal.
- GREEN: 34 hosttoetse slaag; AST-reëls bevestig geen globale veranderlikes, modulevlak helpers of hardeware-import-newe-effekte nie.
- Fisiese preflight: `lolin_s2_mini`, `IO3=True`, `IO5=True`, `IO7=True`.
- Fisiese runtime: `audiobusio:yes`, `audiopwmio:no`, `synthio:yes`, `usb_midi:yes`, `wifi:yes`; I2S-backend is kandidaat, maar nie gestart nie.
- Private herstelkopie: buite Git geskep; geen inhoud word gepubliseer nie.

## Opgeloste impediment en herstelbewys

1. Die ESP32-S2 en versterkerkrag is veilig afgeskakel.
2. Ná vyf sekondes is USB sonder die BOOT-knoppie herkoppel.
3. Finder het `CIRCUITPY` weer gewys en CDC/REPL het teruggekeer.
4. `boot_out.txt` het `v0.4.0`, `MCP-US-004` en `BOOT_STATUS=PASS` gewys.
5. Die sewe-lêer manifest-HIL het connection, deployment, boot en execution as `PASS` gerapporteer.

Geen UF2-flash, formattering of bootloaderaksie was nodig nie.

## Virtuele spanreview

| Rol | Bydrae |
|---|---|
| Product Owner | Het MCP-US-004, die fisiese MAX98357A-opstelling en profielverstekke goedgekeur. |
| Scrum Master | Hou die werk binne capability discovery; hoorbare klank bly US-016. |
| Business Analyst | Vertaal penne, modules, geheue en backend-kandidate na toetsbare uitset. |
| Solution Architect | Vereis geïnjekteerde probes, bekende/unknown profiele en nul globale status. |
| Embedded Engineer | Bevestig IO3/5/7-aliasse en hou alle perifere aktivering uit discovery. |
| MIDI Engineer | Not impacted: hierdie story verander geen MIDI-boodskap of receive loop nie. |
| DSP/Chip Engineer | Bevestig BCLK/WS/DATA-semantiek en blokkeer klank totdat DIN/SD-MODE visueel duidelik is. |
| Web Engineer | Not impacted: capability snapshot kan later gelees word, maar geen webkode begin nou nie. |
| QA/HIL Engineer | Lewer RED/GREEN, fisiese REPL-preflight, runtime capture, privacycheck en herstelhek. |
| Release/Documentation | Sinkroniseer release-identiteit, stories, matriks, risiko's, bronne en Kanban. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe Copilot-inset is vir MCP-US-004 ontvang nie. |
| Devil's Advocate | Wys op die DIN teenoor SD/MODE-verwarring en die reset/remount-regressie. |

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
