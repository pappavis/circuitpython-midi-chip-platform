# MCP-US-010 Pitch Bend And CC1 Modulation Review

<!--
Bestand: mcp_us_010_pitch_bend_cc1_review_v0.1.0.md
Versienommer: 0.1.0
Doel: Dokumenteer per-kanaal bend/modulasiestatus en die hoorbare aanvaardingshek.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-010 Pitch Bend And CC1 Modulation
Actienr: MCP-ACT-010-REVIEW-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-010-IN-REVIEW
-->

## Hostlewering

- `MidiPerformanceState` besit pitch bend en CC1 per MIDI-kanaal.
- 14-bit bend word rondom 8192 gesentreer en na 'n konfigureerbare semitone-reeks omgeskakel.
- CC1 word na `0.0..1.0` genormaliseer.
- Kanaaltoestand is geïsoleer, wat latere Fishman/MPE-agtige per-string bends moontlik maak sonder gedeelde globale status.
- `performance-diagnose` lewer meetbare, masjienleesbare waardes.

## Hosttoets

```bash
python -m midi_chip_platform performance-diagnose \
  --channel 4 \
  --pitch-bend 12288 \
  --modulation 127 \
  --pitch-bend-range 2
```

Verwag:

```text
MIDI_PERFORMANCE_STATUS=PASS
CHANNEL=4;PITCH_BEND_RAW=12288;PITCH_BEND_SEMITONES=1.000000;CC1_NORMALIZED=1.000000
```

Die volledige hoststel is **68 passed**.

## Hoorbare hek

Die oorspronklike aanvaardingskriterium vereis hoorbare bend en vibrato. MCP-US-016 se MAX98357-klankpad en MCP-US-063 se draagbare D1-kern bestaan nou, maar hulle is nog nie deur US-075/US-055 veilig en hoorbaar geïntegreer nie. US-010 bly daarom **In Review (control state ready)**. Geen hostberekening word as hoorbare hardewarebewys voorgestel nie.

Wanneer die klankpad gereed is, moet die menslike toets minstens die volgende bewys:

1. Hou een noot aan en beweeg pitch bend van middel na beide uiterstes.
2. Bevestig ongeveer die ingestelde semitone-reeks sonder onderbreking.
3. Hou 'n noot aan en beweeg CC1 van nul na maksimum.
4. Bevestig dat vibratodiepte hoorbaar verander en Note Off steeds die stem sluit.
5. Herhaal op 'n tweede MIDI-kanaal om kanaalisolasie te bewys.

Dit is die voorafbepaalde pausepunt vir die outonome batch.
