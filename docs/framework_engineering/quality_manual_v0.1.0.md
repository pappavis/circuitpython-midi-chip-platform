# Quality Manual

<!--
Bestand: quality_manual_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer kwaliteitseienaarskap, verpligte hekke en objektiewe vrystellingsbewys.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-066 Quality Manual, Test Strategy And Review Engine
Actienr: MCP-ACT-066-QUAL-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Kwaliteitsbeleid

Kwaliteit beteken dat die produk se beweerde gedrag herhaalbaar, herstelbaar, veilig begrens en na 'n aanvaarbare story terugspoorbaar is. Groen hosttoetse is noodsaaklik maar bewys nie fisiese USB, audio, BLE, penne of timing alleen nie.

## Verpligte hekke

| Hek | Minimum bewys | Blokkeer Done wanneer |
|---|---|---|
| Scope | Goedgekeurde story en afhanklikhede | Side quest of onduidelike kriterium |
| Architecture | Instansie-eienaarskap, poortgrens, ADR indien nodig | Globale status/import-newe-effek/ongekeurde grens |
| Red/Green | Vooraf falende of eksplisiet ontbrekende kontrak, daarna groen | Geen falsifiseerbare toets nie |
| Regression | Volle relevante pytest en lint | Regressie of statiese fout |
| Security/Privacy | Secret- en identiteitskontrole | Secret, UID, MAC of private backup in Git/log |
| Deploy | Dependency closure en atomiese/autoreload-safe kopie | Onvolledige manifest of onbekende destructive aksie |
| HIL | Connection, deployment, execution, stimulus | Fisiese claim sonder toestelbewys |
| Human acceptance | PO se hoorbare/Logic/meet-instrument resultaat | Kriterium vereis menslike waarneming en dit ontbreek |
| Traceability | Header, story review, backlog, Kanban, commit | Statusse/weergawe/ChatID verskil |
| Release | Risiko, docs, rollback, tag | Oop Must-story of onbevestigde claim |

## Defek- en impedimentbeleid

'n Defek teen die aktiewe kriterium bly in dieselfde story as `IMPEDIMENT-nnn`. Dit kry reproduksie, verwagte/werklike resultaat, oorsaak, kleinste herstel, regressietoets, HIL-retest en lessons-learned-kandidaat. 'n nuwe funksie om die defek te omseil is nie 'n fix nie.

## Kodekwaliteit

- Klasse en dependency injection; geen globale runtime-status of modulevlak helperfunksies.
- Geen hardware/network/audio startup tydens import nie.
- CircuitPython-versoenbaarheid word teen die geteikende firmwarekontrak getoets.
- Begrensde loops, buffers en logs; cleanup in sukses, timeout, fout en Ctrl-C/soft reload.
- Generiese device discovery; spesifieke verwysingstoestelle bly toetsdata/profiele.

## Dokumentkwaliteit

Artefakte bevat metadata, eienaar/gesag, huidige status en direkte skakels. Dokumentasie mag nie meer volwassenheid beweer as die kode en HIL nie. Beginnersinstruksies bevat presiese stappe, verwagte uitvoer, foutdiagnose en herstel.

## Metrieke

Die span volg: groen toetsgetal, oop impediments, story cycle time, regressies, dependency-closure, HIL pass rate, heap, audio latency/dropout, hersteltyd en statusversoeningsfoute. Metrieke verduidelik risiko; hulle vervang nie aanvaarding nie.

## Afwykings

Slegs 'n goedgekeurde ADR plus PO-besluit kan 'n verpligte hek tydelik afwyk. Die afwyking het 'n vervaldatum/story, eienaar, risiko en rollback. “Dit werk op my bord” is nie 'n afwyking nie.
