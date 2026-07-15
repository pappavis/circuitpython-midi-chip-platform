# Artefact Taxonomy

<!--
Bestand: artefact_taxonomy_v0.1.0.md
Versienommer: 0.1.0
Doel: Klassifiseer artefakte, gesag, lewensiklus en minimum metadata.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MCP-US-065 Enterprise Meta Model, Glossary And Artefact Taxonomy
Actienr: MCP-ACT-065-TAX-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / FRAMEWORK-ENGINEERING-001
-->

## Klassifikasie

| Tipe | Voorbeeld | Besluitreg | Wysigingstrigger | Bewyswaarde |
|---|---|---|---|---|
| Vision | Enterprise Vision, MVP Scope | Product Owner | Produkdoel/scope verander | Motiveer, bewys nie implementering nie |
| Backlog | User stories, Excel Kanban | PO + Scrum Master | Status, prioriteit, nuwe requirement | Bron vir volgorde en status |
| Architecture | Architecture, meta model | CEA + Solution Architect | Grens/capability verander | Ontwerpbaseline |
| ADR | `docs/decisions/ADR-*` | Architect + PO waar scope raak | Betekenisvolle trade-off | Aanvaarde besluit en gevolge |
| Policy | AGENTS, Quality Manual | PO/CEA/QA | Kwaliteits- of veiligheidsreel verander | Verpligte hek |
| Strategy | Test Strategy, releaseplan | QA/Release/Architect | Omgewing of risikoprofiel verander | Beplan bewys |
| Playbook | Review Engine, quickstart | Proses-eienaar | Herhaalde uitvoering verbeter | Herhaalbare werkvloei |
| Specification | Prompt/Context specs | CEA/Release | Agentwerk of kennisvloei verander | Ontwikkelkontrak, nie runtime nie |
| Story review | `mcp_us_*_review` | Storyspan + PO | Story implementeer/retest | Primêre closure-bewys |
| Lessons learned | Sprint checkpoint | Scrum Master + QA | 3-4 stories of ernstige impediment | Prosesverbetering |
| Risk register | Risiko-ID's | PO + QA | Waarskynlikheid/impak/mitigasie verander | Release-inset |
| Source register | Amptelike bronverwysing | BA/Architect | Nuwe eksterne feit | Herkoms, nie plaasvervangende toets nie |

## Gesagsreels

1. 'n Story-status word in Markdown en Kanban versoen; die story review bevat detail.
2. 'n ADR is append-only in betekenis: 'n nuwe ADR vervang 'n ou besluit en skakel daarna.
3. 'n review- of lessons-learned-dokument mag nie 'n harde `AGENTS.md`-reel verslap nie.
4. 'n gegenereerde diagram is verduidelikend; teks, tests en bronkode bly normatief.
5. Eksterne QA en Copilot is adviserende bronne totdat bevindinge geklassifiseer en deur PO/Architect aanvaar is.

## Metadata

Elke beheer- of storydokument bevat bestand, versienommer, doel, sprint, epic, user story, aksienommer en ChatID. Weergawe verander wanneer betekenis verander. Datums en releaseclaims moet op werklike bewys berus.

## Retensie

- Aktiewe baselines bly onder `docs/`.
- ADR's bly onder `docs/decisions/`.
- Framework-artefakte bly onder `docs/framework_engineering/`.
- Uitvoerbare/redigeerbare bestuursartefakte bly onder `outputs/<ChatID>/`.
- Tydelike probes, private settings en toestelrugsteune word nie gecommit nie.

## Kwaliteitskontrole

Voor publikasie word skakels, metadata, story-ID's, statusversoening, geheime en Git-diff nagegaan. 'n Artefak sonder eienaar, trigger of gesag word saamgevoeg, geklassifiseer of verwyder; dokumentvolume is nie op sigself volwassenheid nie.
