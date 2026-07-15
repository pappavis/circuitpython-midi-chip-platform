# Sprint 1 Lessons Learned - Checkpoint 001

<!--
Bestand: lessons_learned_sprint_1_checkpoint_001_v0.1.0.md
Versienommer: 0.1.0
Doel: Leg leerlesse ná MCP-US-001 tot MCP-US-004 en aksies vir die volgende stories vas.
Sprint: Sprint 1
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MCP-US-005 Configuration And Secret Boundary
Actienr: MCP-ACT-005-RETRO-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / LESSONS-LEARNED-CHECKPOINT-001
-->

## Bevestigde leerlesse

| Waarneming | Bewys/oorsaak | Verbeteraksie | Eienaar | Teiken | Status |
|---|---|---|---|---|---|
| Capability-aannames is onbetroubaar | `audiopwmio` ontbreek in die werklike firmwarebou ondanks platformverwagtings | Hou runtime capability gates en negatiewe toetse verpligtend | Architect/Embedded | US-015, US-052 | Aktief |
| Programmatiese resets kan host-herenumerasie versteur | US-004 het CIRCUITPY/CDC eers ná fisiese power-cycle herstel | HIL preflight, private backup en fisiese herstelstap voor reset-afhanklike deploy | QA/HIL | US-051, US-056 | Aktief |
| USB-MIDI en massa-opberging deel 'n brose ontwikkelgrens | US-005 se volume is geldig maar media-leesalleen | Geen onbewaakte remount/erase; operateur bevestig skryfbaarheid voor deploy | Embedded/Release | US-005 | Oop |
| Dokumentasie moet runtimeclaims onderskei | Hosttoetse alleen bewys nie die gekoppelde bord nie | Gebruik altyd Connection, Deployment en Execution Proof vir fisiese claims | QA/Docs | Alle HIL-stories | Aktief |
| Geheime-skeiding is nie geheime-sekuriteit nie | `settings.toml` is leesbare plain text en ou prototipecredential was blootgestel | Roteer credentials; redigeer logs; hou private lêers uit Git | PO/Security | US-005, US-023 | Oop |

## Prosesbesluit

Die span hou stories klein, deploy slegs manifestlêers en stop by enige onbekende storage- of USB-toestand. Die volgende lessons-learned-checkpoint volg nadat nog drie of vier stories werklik `Done` is, of vroeër by 'n ernstige MIDI-/klankimpediment.

## LLM-gebruik

Geen plaaslike Ollama-model is gebruik nie.
