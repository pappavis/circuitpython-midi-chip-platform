# Review Engine Playbook

<!--
Bestand: review_engine_v0.1.0.md
Versienommer: 0.1.0
Doel: Maak interne, eksterne en AI-reviewbevindinge herhaalbaar en besluitbaar.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-066 Quality Manual, Test Strategy And Review Engine
Actienr: MCP-ACT-066-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Invoer

Reviews kan van Product Owner, spanlid, Copilot, Codex, eksterne QA, gebruikerstoets of meetinstrument kom. Bronstatus bepaal nie outomaties korrektheid nie. Elke bevinding moet na 'n lêer, gedrag, requirement, risiko of ontbrekende bewys wys.

## Klassifikasie

| Besluit | Betekenis | Vereiste aksie |
|---|---|---|
| Accept | Korrek, binne scope en logies georden | Voeg by aktiewe story of backlog |
| Modify | Kerninsig is geldig, voorgestelde oplossing pas nie | Herskryf kriterium/ontwerp en toets |
| Defer | Geldig maar afhanklikheid/prioriteit is later | Plaas met ID en rede in backlog |
| Reject | Verkeerd, onbewys, onveilig of teen beleid | Dokumenteer kort falsifikasie |
| Investigate | Onvoldoende data | Timeboxed spike/probe, geen produksieclaim |

## Reviewvolgorde

0. **Principal QA Gate:** voor enige kodewysiging moet `docs/governance/principal_qa_architect_agent_v0.1.0.md` en `docs/governance/regression_memory_v0.1.0.md` toegepas word. Twyfel beteken `REJECT`.
1. **Reproduceer:** lees die werklike kode/docs en voer bestaande bewys uit.
2. **Classificeer erns:** P0 veiligheid/data/brick; P1 kernfunksie; P2 maintainability; P3 polish.
3. **Kontroleer scope:** defek in aktiewe story of nuwe requirement?
4. **Kontroleer argitektuur:** poorte, eienaarskap, capability, ADR en herstelpad.
5. **Ontwerp falsifiseerbare toets:** host, HIL of albei.
6. **Besluit:** CEA/Solution Architect en QA adviseer; PO aanvaar scope/prioriteit.
7. **Sluit:** bewys, docs, backlog, lessons learned en commit.

## Investigation Story Workflow

Elke goedgekeurde Investigation Story volg hierdie vaste volgorde:

```text
User Story
↓
Principal QA Review
↓
Investigation Story
↓
Instrumentation Design Review (IDR)
↓
Principal QA Review IDR
↓
Implementatie tijdelijke instrumentatie
↓
HIL metingen
↓
FIRST_DISAPPEARANCE_OF_<EVENT>
of
UNKNOWN
↓
Root Cause vastgesteld
↓
Nieuwe Fix Story
↓
Implementatie
↓
Validatie
↓
Verwijderen tijdelijke instrumentatie
```

Die IDR gebruik `docs/governance/instrumentation_design_review_template_v1.0.md`. HIL- en meetbewys gebruik `docs/governance/evidence_package_template_v1.0.md`.

## Stopreels

- Stop kodewerk wanneer die Principal QA Architect pre-code review ontbreek, nie deur die Product Owner goedgekeur is nie, of `REJECT` gee.
- Stop investigation-implementatie wanneer 'n goedgekeurde IDR ontbreek.
- Stop HIL-aanvaarding wanneer 'n Evidence Package ontbreek of kernvelde `UNKNOWN` is sonder objektiewe rede.
- Stop MIDI/audio/HIL werk wanneer `REG-080-001` nie eksplisiet oorweeg is nie.
- Stop wanneer 'n voorstel globale runtime-status, import-newe-effekte of 'n secret in Git vereis.
- Stop firmwarewerk wanneer die verkeerde checkout/remote/manifest aktief is.
- Stop HIL-deploy wanneer Thonny of 'n ander proses die serialpoort besit.
- Stop side quests wat die hoorbare vertikale sny vooruitloop.
- Stop 'n releaseclaim wat slegs op dokumentasie of hostfakes berus.

## Devil's Advocate-vrae

- Is dit dalk weer 'n false PASS waar net Control Change-events gesien word en geen `NoteOn`/`NoteOff` nie?
- Wat sou hierdie PASS vals positief maak?
- Watter bord-, firmware- of hostaanname is verborge?
- Kan die gebruiker herstel sonder ons ontwikkelmasjien?
- Wat gebeur met twee toestelle, twee cores, vol heap of verlore Note Off?
- Watter private data kan in logs beland?

## Algemene uitsettemplate

Elke reviewuitset bevat: bron, bevinding, bewys, erns, klassifikasie, story/risiko, eienaar, besluit, toets en status. Lang menings sonder hierdie velde is discovery-invoer, nie 'n change request nie.

Vir die verpligte Principal QA Architect Gate vervang `docs/governance/principal_qa_architect_agent_v0.1.0.md` hierdie algemene template met sy presiese verdict-formaat.
