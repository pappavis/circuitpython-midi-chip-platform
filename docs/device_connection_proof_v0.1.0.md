# Device Connection Proof

<!--
Bestand: device_connection_proof_v0.1.0.md
Versienommer: 0.1.0
Doel: Definieer veilige, herhaalbare bewys dat die bedoelde CircuitPython-kode op die fisiese bord loop.
Sprint: Sprint 1
Epic: MCP-EPIC-001 en MCP-EPIC-008
User-Story: MCP-US-003 en MCP-US-051
Actienr: MCP-ACT-003-HIL-GOV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / DEVICE-CONNECTION-PROOF-001
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
