# Virtuele span en RACI

<!--
Bestand: team_raci_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer spanrolle, bydraes, besluitregte en samewerkingsritme.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-001 Device And Source Baseline Inventory
Actienr: MCP-ACT-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001
-->

## Spanrolle

| Rol | Verantwoordelikheid | Verpligte inset per story |
|---|---|---|
| Sales/Discovery | Gebruik, waarde, begroting en verwagtingsbestuur | Waardehipotese en demo-uitkoms |
| Business Analyst | Gebruikersvloei, omvang, aannames en meetbaarheid | Story/aanvaardingskriteria en nie-doelwitte |
| Product Owner | Prioriteit, waarde en formele aanvaarding | Ready/accept/reject-besluit |
| Scrum Master | Volgorde, afhanklikhede, impediments en Kanban-higiëne | Now/Next/Later, blokkasies en volgende stap |
| Solution Architect | Poorte, runtime-grense, ADR’s en portabiliteit | Ontwerpresensie en trade-offs |
| Embedded Engineer | CircuitPython, boot, penne, geheue en ontplooiing | Bordimpak en herstelpad |
| MIDI Engineer | MIDI-protokol, kanale, klok en kontroleboodskappe | Message-kontrakte en randgevalle |
| DSP/Chip Engineer | Kernemulasie, voice allocation, klank en effekte | CPU/RAM/latensie- en akkuraatheidsbegroting |
| Web Engineer | Plaaslike UI, protokol en samewerkende scheduling | UI-stroom en sok/geheue-impak |
| QA/HIL Engineer | Rooi/groen, simulators, meettoerusting en hardeware-aanvaarding | Toetsmatriks en objektiewe bewys |
| Release/Documentation | Git, weergawe, installasie, sekuriteit en naspeurbaarheid | Publikasiehek en gebruikersdokumentasie |
| Devil’s Advocate | Kritiese teenargumente, mislukkingmodusse en scope creep | Ten minste een risiko of falsifiseerbare vraag |

## RACI per werkstroom

Legenda: **A** aanspreeklik, **R** uitvoerend verantwoordelik, **C** geraadpleeg, **I** ingelig.

| Werkstroom | PO | Scrum | Architect | Embedded | MIDI | DSP | Web | QA | Release |
|---|---|---|---|---|---|---|---|---|---|
| MVP-omvang | A | R | C | C | C | C | C | C | I |
| Repository/poorte | I | C | A/R | C | C | C | C | C | R |
| Boot en bordprofiel | I | C | C | A/R | C | C | I | R | C |
| MIDI en klok | I | C | C | C | A/R | C | I | R | I |
| Kern en klank | I | C | C | R | C | A/R | I | R | I |
| Plaaslike webbeheer | I | C | C | C | C | C | A/R | R | I |
| HIL en release | A | C | C | C | C | C | C | R | A/R |

## Storyritme

1. Product Owner bevestig die logiese volgende story.
2. Die span lewer ’n ongeveer 50-woord uitvoerplan met lêers, rooi/groen-toets en menslike aanvaarding.
3. Geen implementering begin voor eksplisiete goedkeuring nie, behalwe wanneer die gebruiker daardie spesifieke hek vooraf ophef.
4. Architect, spesialis-ingenieur, QA en Release gee altyd ’n sigbare inset.
   Elke ander spanrol gee ook 'n bydrae of 'n gemotiveerde `Not impacted`; die span word nie bloot as 'n etiket gebruik nie.
5. Die Scrum Master hou side quests in Later/Parking Lot en verander nie stilweg die huidige sprint nie.
6. Na groen host-toetse volg hardeware-aanvaarding indien fisiese gedrag geraak word.
7. Dokumentasie, Kanban, commit en push sluit die story af.
8. Na elke drie of vier voltooide stories fasiliteer die Scrum Master 'n lessons-learned-checkpoint voor die volgende releasebesluit.

## Plaaslike Ollama-beleid

- Delegering gebeur slegs ná overleg met die gebruiker vir ’n benoemde klein taak.
- Voor enige gebruik word die model se beskikbaarheid met `ollama list` bevestig en 'n klein tydbegrensde proefaanroep uitgevoer.
- Geskikte take: taalversorging, tabelnormalisering, toetsnaamvoorstelle en nie-sensitiewe opsommings.
- Ongeskikte take: geheime, toestelrugsteune, argitektuurbesluite, veiligheidskritieke kode en finale Git-publikasie.
- Codex hersien altyd die uitset; gewone toetse en menslike aanvaarding bly verpligtend.
- Ollama is nooit deel van die firmware, synth-runtime of verpligte ontwikkelketting nie.
- Die verstek is `default`; 'n toekomstige host-hulpmiddel moet `--llm-provider default` bied om plaaslike modelgebruik af te skakel.
- Fallback is altyd die verstek-Codex/LLM-pad wanneer Ollama stadig, onbeskikbaar of onseker is.

## Huidige gebruikstatus

MCP-US-002 het geen plaaslike model gebruik nie. Ollama-integrasie bly buite die synth-runtime en vereis 'n afsonderlik goedgekeurde ontwikkelhulpmiddel-story.
