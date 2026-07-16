# BLE MIDI And Synth Core Priority Amendment

<!--
Bestand: ble_midi_core_priority_amendment_v0.1.0.md
Versienommer: 0.1.0
Doel: Formaliseer BLE-MIDI as MVP-vereiste en die goedgekeurde synth-corevolgorde.
Sprint: Sprint 1
Epic: MCP-EPIC-002, MCP-EPIC-003 en MCP-EPIC-008
User-Story: SCOPE-AMENDMENT-002
Actienr: MCP-ACT-SCOPE-AMEND-002
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / SCOPE-AMENDMENT-002
-->

## Product Owner-besluite

1. BLE-MIDI is `Must have` vir die MVP en gebruik dieselfde klasgebaseerde eventmodel as USB-MIDI en DIN/UART.
2. Die huidige LOLIN/Wemos ESP32-S2 Mini bly die primêre vroeë USB-MIDI- en klankbord.
3. ESP32-S2 het geen native BLE-ondersteuning in CircuitPython nie. Dit moet deterministies as ’n nie-ondersteunde vermoë rapporteer sonder om USB-MIDI, klank of recovery te ontwrig.
4. MCP-US-052 kies en profileer ’n tweede BLE-geskikte CircuitPython-bord; MCP-US-062 lewer daarop die fisiese BLE-MIDI-aanvaarding.
5. Die goedgekeurde kernvolgorde is D1-basiskern, SN76489, 6581 SID, OPL2 en daarna OPL3.
6. `pappavis/python-d1-synth` bly absoluut leesalleen. D1-hergebruik beteken draagbare gedrag en kontrakte wat nuut in hierdie repository geïmplementeer en getoets word, nooit desktop-backends of wysigings aan die produksierepo nie.

## Huidige kernstatus

MCP-US-063 is nou die eerste draagbare musikale kern in implementering nadat bordvermoëns, die klankpoort, MAX98357-diagnose en die eventmodel gereed geword het. SN76489 begin eers ná die D1/Logic-MVP.

## Logiese uitvoervolgorde

```text
MCP-US-004 Board Capability Discovery
  -> MCP-US-014 AudioOutput Port And Null Backend
  -> MCP-US-016 MAX98357 Mono I2S Audible Diagnostic
  -> MCP-US-006 Portable NoteEvent And ControlEvent Model
  -> MCP-US-063 Portable D1 Baseline Synth Core
  -> MCP-US-017 SN76489-Lite Three-Voice Core
  -> MCP-US-038 6581 SID Core Spike
  -> MCP-US-041 OPL2 Core Adapter
  -> MCP-US-042 OPL3 Core Adapter
```

BLE loop parallel ná die USB-basislyn:

```text
MCP-US-004 Board Capability Discovery
  -> MCP-US-052 Cross-Board Capability Profiles
  -> MCP-US-062 BLE MIDI Transport And Capability Gate
```

## Wi-Fi-identiteitsreël

’n Sigbare `ESP_*`-netwerknaam is slegs ’n waarneming. Dit bewys nie watter fisiese bord die access point aanbied nie. Identiteit word eers aanvaar ná ’n beheerde power-cycle of ’n eksplisiete toestel-/REPL-logkorrelasie. Plaaslike SSID’s, MAC-adresse en geheime word nie in openbare konfigurasie of HIL-verslae gepubliseer nie.

## Spanbydraerekord

| Rol | Bydrae |
|---|---|
| Product Owner | Het BLE-MIDI as Must en die kernvolgorde D1, SN76489, SID, OPL2 bevestig. |
| Scrum Master | Hou BLE en kernwerk agter hul afhanklikhede; die huidige HIL-story word nie onderbreek nie. |
| Business Analyst | Het die S2-beperking, tweede-bord-aanvaarding en Wi-Fi-identiteitsreël eksplisiet gemaak. |
| Solution Architect | Behou een eventmodel en geïnjekteerde transport-/kernpoorte sonder globale status. |
| Embedded Engineer | Vereis capability discovery voordat BLE-modules of bordspesifieke penne gebruik word. |
| MIDI Engineer | Laat BLE Note On/Off, CC en pitch bend deur dieselfde eventkontrakte vloei. |
| DSP/Chip Engineer | Definieer die draagbare D1-basiskern voor skyfie-emulasie. |
| Web Engineer | Not impacted: geen web-runtime word in hierdie amendment geïmplementeer nie. |
| QA/HIL Engineer | Vereis veilige S2-negatiewe toets plus positiewe BLE-HIL op ’n geskikte tweede bord. |
| Release/Documentation | Sinkroniseer Markdown, README, Kanban, bronne, risiko’s en story-ID’s. |
| External Architecture Reviewer (Copilot) | Bly ’n kritiese, adviserende reviewer; klasgebaseerde ontwerp en die verbod op globale veranderlikes bly bindend. |
| Devil's Advocate | Waarsku dat ’n SSID nie bordidentiteit bewys nie en dat BLE-biblioteekbeskikbaarheid nie ’n HIL-bewys vervang nie. |

## LLM-gebruik

Geen plaaslike Ollama-model is vir hierdie amendment gebruik nie.
