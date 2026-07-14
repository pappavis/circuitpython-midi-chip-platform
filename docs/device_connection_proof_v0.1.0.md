# Device Connection Proof

<!--
Bestand: device_connection_proof_v0.1.0.md
Versienommer: 0.3.0
Doel: Definieer veilige, herhaalbare bewys dat die bedoelde CircuitPython-kode op die fisiese bord loop.
Sprint: Sprint 1
Epic: MCP-EPIC-001 en MCP-EPIC-008
User-Story: MCP-US-003, MCP-US-004 en MCP-US-051
Actienr: MCP-ACT-004-HIL-GOV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-004
-->

## Bewysvlakke

| Vlak | Vraag | Publiseerbare bewys |
|---|---|---|
| Connection | Is Codex aan 'n CircuitPython-bord verbind? | Ontdekte poorttipe, CIRCUITPY-gemonteer, bord-ID en CircuitPython-weergawe |
| Deployment | Is die goedgekeurde repository-artefak gekopieer? | Broncommit plus SHA-256-vergelyking van deploymanifest; geen private rugsteuninhoud |
| Execution | Het die toestel daardie firmware uitgevoer? | Runtimebanner met weergawe/story en `DEVICE_EXECUTION_STATUS=READY` |

## Veiligheidsreëls

- Ontdek poorte en volumes; hardkodeer nie die huidige USB-reeksnommer of mountpad as produkgedrag nie.
- Kontroleer met `lsof` of 'n serial client die poort besit. Thonny en 'n tweede monitor mag nie gelyktydig verbind wees nie.
- Neem voor skryf 'n private herstelkopie buite Git. Moet nooit `settings.toml`, Wi-Fi-geheime, UID, MAC of netwerklyste publiseer nie.
- 'n `boot.py`-verandering vereis 'n volledige harde reset nadat alle writes voltooi is; Ctrl-D herlaai net `code.py`.
- As CIRCUITPY/REPL verdwyn, stop die story en volg safe-mode/bootloader-herstel. Geen UF2-flash of formattering gebeur sonder aparte goedkeuring nie.

## Chat-uitvoerformaat

```text
DEVICE CONNECTION PROOF
connection: PASS
transport: USB CDC + CIRCUITPY
board: lolin_s2_mini
circuitpython: 10.0.3
deployment: PASS
source-commit: <git sha>
manifest-sha256: <digest>
execution: PASS
runtime: v<version> story=<story> DEVICE_EXECUTION_STATUS=READY
private-identifiers: REDACTED
```

Die bewys is aanvanklik verpligtend. Ná 'n eksplisiete Product Owner-vertrouensbesluit mag dit vir host-only stories opsioneel word; HIL, recovery en release bly altyd verpligtend.

## MCP-US-003 fisiese bewys, 2026-07-14

| Kontrole | Resultaat | Geredigeerde bewys |
|---|---|---|
| Connection | PASS | USB CDC-poort ontdek; CIRCUITPY gemonteer; `lolin_s2_mini`; CircuitPython 10.0.3 |
| Deployment | PASS | Commit `3994f46`; ses bron-/toestelpaar-hashes was identies |
| Minimal boot | PASS | `v0.2.0`, `story=MCP-US-003`, `BOOT_STATUS=PASS` |
| USB identity | PASS | Vendor `pappavis`; produk `CircuitPython MIDI Chip Platform` |
| USB MIDI descriptors | PASS | USB AudioControl en MIDIStreaming-interface is deur macOS IOKit ontdek |
| Device MIDI runtime | PASS | `usb_midi.ports` het een `PortIn` en een `PortOut` bevat |
| Application execution | PASS | `DEVICE_EXECUTION_STATUS=READY` direk via CircuitPython REPL |
| Host RtMidi scan | IMPEDIMENT | Python/RtMidi kon nie 'n CoreMIDI client skep nie (`-10833`); Logic-aanvaarding bly MCP-US-055 |
| Private identifiers | REDACTED | Geen UID, MAC, SSID, wagwoord of private rugsteuninhoud gepubliseer nie |

Die eerste volume-kopie met `rsync` is deur CircuitPython se onmiddellike auto-reload onderbreek. Die herstelpad het gewerk: stop, bevestig mount/REPL, skakel auto-reload tydelik af, kopieer biblioteke eerste en `boot.py` laaste, vergelyk hashes, voer 'n harde reset uit en verwyder slegs die geskepte tydelike lêers.

## MCP-US-051 runnerbewys, 2026-07-14

Die herhaalbare CLI het teen dieselfde fisiese bord geslaag:

```text
circuitpython-midi-chip-platform v0.3.0 | story=MCP-US-051 | release-date=2026-07-14
DEVICE CONNECTION PROOF
connection: PASS - USB CDC + CIRCUITPY
deployment: PASS - approved manifest SHA-256 pairs
boot: PASS - current release and USB-MIDI boot marker
execution: PASS - current release marker via serial REPL
private-identifiers: REDACTED
```

Hierdie uitvoer bewys nie nog klank nie. Die runner se klankmeetadapter en menslike hoorbare aanvaarding volg nadat US-015/016 'n fisiese uitvoerpad lewer.

## MCP-US-004 capability-bewys, 2026-07-14

Die sagte runtime-run het direk vanaf die fisiese S2 Mini gerapporteer:

```text
circuitpython-midi-chip-platform v0.4.0 | story=MCP-US-004 | release-date=2026-07-14
CAPABILITY_DISCOVERY_STATUS=PASS
BOARD_ID=lolin_s2_mini
BOARD_PROFILE=KNOWN
I2S_PINS=BCLK:IO5,WS:IO3,DATA:IO7->DIN
I2S_PIN_STATUS=AVAILABLE
MODULES=audiobusio:yes,audiopwmio:no,synthio:yes,usb_midi:yes,wifi:yes
AUDIO_BACKENDS=i2s-max98357a-mono
DEVICE_EXECUTION_STATUS=READY
```

Die opvolgende programmatiese harde reset het USB-identiteit behou, maar macOS het aanvanklik nie CIRCUITPY of CDC/REPL herenumerateer nie. 'n Fisiese power-cycle het beide herstel. Die finale runner het connection, sewe manifesthashes, `v0.4.0` boot en werklike REPL-uitvoering as `PASS` gerapporteer; private identifiseerders is geredigeer.
