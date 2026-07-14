# Agile Delivery And Release Plan

<!--
Bestand: agile_delivery_release_plan_v0.1.0.md
Versienommer: 0.2.0
Doel: Definieer die werklike Agile uitvoerings-, beheer- en releaseproses.
Sprint: Sprint 0
Epic: Alle epics
User-Story: AUDIO-PRIORITY-AMENDMENT-001
Actienr: MCP-ACT-AUDIO-AMEND-REL-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001
-->

## Doel

Hierdie projek word bestuur as 'n werklike klein produkspan. Dokumentasie is nie dekorasie nie: dit bepaal volgorde, besluitregte, bewys en release-status. Die backlog in `user_stories_v0.1.0.md` en die Excel Kanban vorm saam die delivery-baseline.

## Backloglae

| Laag | Betekenis | Toelatingsreel |
|---|---|---|
| Discovery | Ongevalideerde idee of bron | Nog geen story-belofte nie |
| Product backlog | Geordende story met waarde en afhanklikheid | BA en PO het dit verstaan |
| Ready | Plan, kriteria, risiko en toets is uitvoerbaar | DoR slaag en PO keur plan goed |
| In Progress | Presies een aktiewe implementasiestory | Afhanklikhede is Done |
| Impediment | Aktiewe story kan nie kriteria haal nie | Oorsaak, bewys en herstelplan gelog |
| In Review | Outomaties groen; mens/hardewarebewys wag | Geen nuwe funksionele story begin nie |
| Done | DoD, docs, Kanban, commit en aanvaarding voltooi | Release-status bly eerlik |
| Later/Parking Lot | Waardevol maar buite huidige volgorde/scope | Geen stil implementering nie |

## Volgorde en WIP

- Die backlogvolgorde en eksplisiete afhanklikhede is bindend.
- Maksimum een implementasiestory is `In Progress`.
- Dokumentasie-/impedimentwerk binne dieselfde story tel nie as 'n tweede story nie.
- 'n Nuwe idee word geklassifiseer en georden; dit onderbreek nie die aktiewe story nie.
- Die Scrum Master en Architect moet enige versoek stop wat 'n ongetoetste kernpad, werkende klankpad of importgrens kan breek.
- Die eerste hoorbare vertikale sny volg `MCP-US-003 -> MCP-US-004 -> MCP-US-014 -> MCP-US-016`; MAX98357 mono-I2S is primêr en PWM is fallback.
- Sonder verdere kwalifikasie beteken `synth` hierdie CircuitPython-projek; `python-d1-synth` word slegs as 'n eksplisiet benoemde leesalleen-verwysing gebruik.

## Storyritme

1. **Refinement:** BA, Architect, spesialis en QA verfyn waarde, grense, afhanklikhede en bewys.
2. **Ready review:** Scrum Master verifieer DoR; PO keur die kort plan goed.
3. **Red phase:** QA en ontwikkelaar bewys die ontbrekende gedrag met 'n falende toets.
4. **Green phase:** Die kleinste klasgebaseerde implementering maak die toets groen.
5. **Regression:** Volle relevante suite, importveiligheid en geheimekontrole slaag.
6. **HIL/review:** PO voer die gepaste MIDI-/klank-/Logic-/ossilloskooptoets uit.
7. **Closure:** docs, Kanban, rolbydraes, commit en push word voltooi.
8. **Next proposal:** net die volgende logiese story word voorgestel.

## Virtuele span-seremonies

| Seremonie | Kadens | Verpligte uitset |
|---|---|---|
| Intake/refinement | Voor elke story | Storygrense, afhanklikhede, toets en risiko |
| Story kickoff | Na PO-goedkeuring | Aktiewe plan en rolbydraes |
| Daily delivery note | Per werksessie | Vordering, blocker, nuwe feit |
| Story review | By In Review | Outomatiese en menslike bewys |
| Lessons learned checkpoint | Elke 3-4 Done stories | Nuwe lesse, aksies, eienaars en backlog-aanpassing |
| Epic review/retro | By epic-einde | Waarde, tegniek, kwaliteit, proses en besluit |
| Release readiness | Voor tag/release | Artefakmatriks, regressie, sekuriteit, installasie, rollback |

## Lessons-learned-kadens

Lessons learned word nie tot die einde van die MVP uitgestel nie.

- Verpligte checkpoint nadat stories 1-4, 5-8, 9-12 en daarna elke volgende groep van drie of vier stories `Done` word.
- 'n Vroee checkpoint gebeur ook na 'n ernstige crash, sekuriteitsbevinding, herhaalde Ctrl-C/cleanup-defek of twee verwante impediments.
- Elke checkpoint bevat: waarneming, bewys, oorsaak, proses-/kodeverbetering, eienaar, teikenstory en status.
- Die Scrum Master skeduleer dit; QA bevestig bewys; PO aanvaar backlog-/scopeveranderinge.
- Die release manager blokkeer 'n release as 'n verskuldigde checkpoint ontbreek.

### Leesalleen D1-leerlesse

Die bestaande D1 lessons-learned-dokument mag gelees word vir bevestigde patrone. Geen toekomstige D1-wysiging, dokumentasie-update, commit of push is deel van hierdie projek nie. Relevante lesse word as nuwe CircuitPython-toetse en stories herskryf, nie blind gekopieer nie.

## Releasevlakke

| Vlak | Betekenis | Minimum bewys |
|---|---|---|
| Concept | Ontwerp of spike | Geen gebruikersclaim |
| Demo | Beperkte gelukkige pad | Herhaalbare demo en bekende beperkings |
| MVP Candidate | Alle Must-stories geimplementeer | Host/HIL groen, installasie en diagnose |
| MVP Accepted | PO aanvaar produkdoel | Review, retro, bekende risiko's en release notes |
| Validated | Tweede omgewing/bord slaag | Kruisplatform- en herstelbewys |
| Production Candidate | Verspreidings- en veiligheidshekke slaag | Lisensie, USB-ID, hardwareveiligheid, rollback |

## Releasehekke

1. Geen modulevlak runtime-status, globale veranderlikes of modulevlak helperfunksies nie.
2. Import van synth-pakkette begin geen hardeware of diens nie.
3. Volle relevante toetse, AST-governance-toetse en geheime-skandering is groen.
4. Bord-/MIDI-/klankstories het 'n HIL-bewys en herstelpad.
5. Dokumentasie, Kanban, ADR's, risiko's en lessons learned is op datum.
6. Release notes onderskei Concept, Demo, MVP en Validated sonder oordrywing.
7. Git-tag wys na presies die geverifieerde commit; rollback-instruksie bestaan.
8. Elke startup toon projekweergawe, aktiewe story/amendment en release-datum; dit stem met package- en release-metadata ooreen.

## Anti-hallusinasie-maatreels

- Elke eis wys na 'n story, toets, bron, ADR of handmatige bewys.
- `Done` word nooit afgelei uit mooi dokumentasie of gegenereerde kode alleen nie.
- Onbekende bordvermoens word runtime getoets en as onbekend gerapporteer.
- Hardewaretoestelname, penne en paaie word nie uit gesprekke as universele konstantes oorgeneem nie.
- Aannames het 'n eienaar en vervaldatum/story; onbevestigde aannames bly sigbaar.
- Backlog-sanity word by elke release herhaal: unieke/opeenvolgende IDs, geldige afhanklikhede, dekking en statusversoening.
- Elke gegenereerde of gewysigde Python-lêer bevat die verpligte weergawe-, story-, aksie- en ChatID-header.
