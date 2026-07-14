# MCP-US-002 Project Skeleton Review

<!--
Bestand: mcp_us_002_project_skeleton_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Storyreview, spanbydraes, toetsbewys en menslike aanvaarding vir die host-skelet.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-002 Clean Repository And Project Skeleton
Actienr: MCP-ACT-002-REV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002
-->

## Uitkoms

Die repository bevat nou 'n installeerbare Python-hostpakket met klasgebaseerde MIDI-event-, kernregister-, poort- en toepassingskontrakte. Imports begin geen hardeware of diens nie. Fakes bewys dependency injection sonder CircuitPython-biblioteke. Geen bordkode is ontplooi nie.

## Red/groen-bewys

- **Rooi:** die eerste `pytest`-loop het tydens versameling met vier `ModuleNotFoundError`-foute misluk omdat `midi_chip_platform` nog nie bestaan het nie.
- **Groen:** ná die minimale implementering slaag 14 toetse.
- Die AST-heining verwerp globale runtime-toekennings, modulevlakfunksies, `global`, hardeware-imports en import-newe-effekte.
- Die CLI-diagnose bewys 'n host-only beginpad sonder toesteltoegang.

## Veranderde oppervlak

- `src/midi_chip_platform/`: events, poorte, kernregister, toepassing, test doubles en CLI.
- `tests/`: argitektuur-, domein-, routerings-, toepassing- en CLI-kontrakte.
- `pyproject.toml`: installeerbare Python 3.11+-pakket sonder runtime-afhanklikhede.
- `.vscode/`: opsionele diagnose-, debug- en toetstake.
- `docs/`: snelbegin, bestuurreëls en hierdie review.

## Spanbydraerekord

| Rol | Bydrae |
|---|---|
| Sales/Discovery | Beginner-installasie en 'n kort diagnosepad verminder die eerste-gebruik-drempel. |
| Business Analyst | Scope is beperk tot 'n host-skelet; geen firmware, web, DSP of hoorbare kern word geëis nie. |
| Product Owner | Het MCP-US-002 en die nuwe IDE-/produksiegrense eksplisiet goedgekeur. |
| Scrum Master | Het MCP-US-003 en alle toestelwerk buite die aktiewe story gehou. |
| Solution Architect | Het dependency injection, vervangbare poorte en 'n kanaal-na-kernregister gedefinieer. |
| Embedded Engineer | Het bevestig dat host-modules geen `board`, USB-, Wi-Fi- of klankimport doen nie. |
| MIDI Engineer | Het 'n platform-onafhanklike `MidiEvent`-kontrak en kanaalgrense gelewer; volledige MIDI volg in MCP-US-006. |
| DSP/Chip Engineer | Het slegs 'n `SynthCore`-kontrak goedgekeur; geen voortydige oscillator of chip-emulasie is bygevoeg nie. |
| Web Engineer | Het bevestig dat die pakket veilig ingevoer kan word sonder om 'n runtime te begin. |
| QA/HIL Engineer | Het die rooi/groen-siklus en AST-/import-/routeringstoetse ontwerp. Geen HIL is nodig omdat geen fisiese gedrag verander nie. |
| Release/Documentation | Het verpakking, Afrikaans-snelbegin en opsionele VS Code/Thonny-paaie voorsien. |
| Devil's Advocate | Waarsku dat 'host skeleton ready' nie as werkende firmware of klank bewys mag word nie. |

## Produksie- en LLM-grense

- `python-d1-synth` is nie verander nie en bly absoluut leesalleen.
- Geen Ollama-model is vir hierdie story aangeroep nie.
- Ollama bly 'n opsionele, voorafgetoetste ontwikkelhulpmiddel met `default` as fallback; dit is nie deel van die synth nie.

## Menslike aanvaarding

Voer vanaf die repository-hooflêergids uit:

```bash
python -m pip install -e ".[dev]"
python -m midi_chip_platform diagnose
python -m pytest -q
```

Aanvaar wanneer diagnose `host skeleton ready`, `hardware access: disabled` en `runtime state: class instances only` wys, en alle toetse slaag.

## Volgende stap

Na Product Owner-aanvaarding is **MCP-US-003: Minimal Safe Boot And USB Profile** die volgende logiese story. Geen implementering daarvan begin sonder 'n nuwe kort plan en goedkeuring nie.
