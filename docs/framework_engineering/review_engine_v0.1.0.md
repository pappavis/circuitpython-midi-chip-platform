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

1. **Reproduceer:** lees die werklike kode/docs en voer bestaande bewys uit.
2. **Classificeer erns:** P0 veiligheid/data/brick; P1 kernfunksie; P2 maintainability; P3 polish.
3. **Kontroleer scope:** defek in aktiewe story of nuwe requirement?
4. **Kontroleer argitektuur:** poorte, eienaarskap, capability, ADR en herstelpad.
5. **Ontwerp falsifiseerbare toets:** host, HIL of albei.
6. **Besluit:** CEA/Solution Architect en QA adviseer; PO aanvaar scope/prioriteit.
7. **Sluit:** bewys, docs, backlog, lessons learned en commit.

## Stopreels

- Stop wanneer 'n voorstel globale runtime-status, import-newe-effekte of 'n secret in Git vereis.
- Stop firmwarewerk wanneer die verkeerde checkout/remote/manifest aktief is.
- Stop HIL-deploy wanneer Thonny of 'n ander proses die serialpoort besit.
- Stop side quests wat die hoorbare vertikale sny vooruitloop.
- Stop 'n releaseclaim wat slegs op dokumentasie of hostfakes berus.

## Devil's Advocate-vrae

- Wat sou hierdie PASS vals positief maak?
- Watter bord-, firmware- of hostaanname is verborge?
- Kan die gebruiker herstel sonder ons ontwikkelmasjien?
- Wat gebeur met twee toestelle, twee cores, vol heap of verlore Note Off?
- Watter private data kan in logs beland?

## Uitsettemplate

Elke reviewuitset bevat: bron, bevinding, bewys, erns, klassifikasie, story/risiko, eienaar, besluit, toets en status. Lang menings sonder hierdie velde is discovery-invoer, nie 'n change request nie.
