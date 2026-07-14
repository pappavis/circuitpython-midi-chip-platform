# Wi-Fi Runtime Fallback Amendment

<!--
Bestand: wifi_runtime_fallback_amendment_v0.1.0.md
Versienommer: 0.1.0
Doel: Formaliseer station-join, IP-ontdekking, access-point fallback en mobiele webbeheer.
Sprint: Sprint 1
Epic: MCP-EPIC-004 Local Web Control
User-Story: WIFI-RUNTIME-AMENDMENT-001
Actienr: MCP-ACT-WIFI-AMEND-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / WIFI-RUNTIME-AMENDMENT-001
-->

## Product Owner-besluite

1. Die synth kan as station by ’n gekonfigureerde Wi-Fi-netwerk aansluit en rapporteer die verkrygde IP-adres.
2. Die join-poging het ’n konfigureerbare, begrensde timeout. Geen netwerk of ’n mislukte join blokkeer nie MIDI, klank, REPL of herstel nie.
3. Ná ’n mislukte join begin die synth ’n eie beveiligde Wi-Fi access point en rapporteer die AP-IP-adres.
4. Die webinterface is mobile-first, werk in station- en AP-modus en bly binne die MVP se eenkliënt-/geheuebegroting.
5. Normale polling, note, klok en UI-verversings skryf nie elke keer ’n logreël nie. Logging is vlak-, gebeurtenis- en koersbegrens; geheime word nooit gelog nie.
6. Netwerkstatus behoort aan klasinstansies. Wi-Fi begin slegs in `code.py`-runtime ná capability/config checks en nooit in `boot.py` of tydens import nie.

## Logiese story-toewysing

| Story | Aanscherping |
|---|---|
| MCP-US-023 | Station join, timeout, station-IP, beveiligde AP-fallback, AP-IP en eksplisiete netwerktoestande |
| MCP-US-024 | Mobile-first UI, station/AP-pariteit, eenkliëntbegroting en spaarsame koersbegrensde logging |
| MCP-US-027 | Vertroude-LAN/AP-sekuriteit, private credentials, sessielimiet, afskakeling en herstel |

Geen nuwe story-ID is nodig nie: die gedrag is reeds deel van EPIC-004 se Wi-Fi-, web- en recovery-verantwoordelikhede.

## Toestandmodel

```text
OFFLINE
  -> STATION_CONNECTING
  -> STATION_READY(ip)
  -> AP_STARTING
  -> AP_READY(ip)
  -> DEGRADED_OFFLINE
```

Elke oorgang lewer hoogstens een gesanitiseerde statusgebeurtenis. ’n Herhaalde poll of reconnect-lus mag nie onbeperkte serial- of flashlogging veroorsaak nie.

## Aanvaardingsprofiele

| Profiel | Minimum bewys |
|---|---|
| Station sukses | Privaat config word gelees; join slaag binne timeout; IP verskyn een keer; mobiele browser laai statusblad |
| Station misluk | Onbereikbare toets-SSID of afgeskakelde router bereik timeout sonder hang; AP-fallback begin |
| Access point | Telefoon join die beveiligde AP; AP-IP is sigbaar; dieselfde mobiele blad en veilige parameters werk |
| Logging | Geen per-poll-/per-note-logvloed; statusveranderings verskyn; wagwoorde, SSID-geheime en kliënt-MAC’s verskyn nooit |
| Herstel | Web/verbinding kan stop of misluk sonder om USB-MIDI, REPL of volgende reboot te breek |

## Spanbydraerekord

| Rol | Bydrae |
|---|---|
| Product Owner | Het station-, AP-fallback-, mobiele UI- en spaarsame loggingvereistes bevestig. |
| Scrum Master | Plaas die gedrag binne US-023/024/027 ná scheduler en config; geen vroeë Wi-Fi side quest nie. |
| Business Analyst | Het sukses-, fallback-, IP- en recovery-toestande toetsbaar gemaak. |
| Solution Architect | Vereis ’n geïnjekteerde klasgebaseerde netwerktoestandmasjien sonder globale status. |
| Embedded Engineer | Hou Wi-Fi uit `boot.py` en begrens join/reconnect om MIDI en klank te beskerm. |
| MIDI Engineer | Vereis dat netwerkfoute geen Note/Clock-lus blokkeer nie. |
| DSP/Chip Engineer | Vereis latensie-/dropoutmeting tydens station/AP-aktiwiteit. |
| Web Engineer | Definieer mobile-first, een kliënt, klein bates en geen debugmodus in produksie nie. |
| QA/HIL Engineer | Definieer station-sukses, station-mislukking, AP, logging en herstelprofiele. |
| Release/Documentation | Sinkroniseer stories, scope, risiko’s, bronne, README en Kanban. |
| External Architecture Reviewer (Copilot) | Not impacted: geen nuwe Copilot-review is vir hierdie amendment ontvang nie. |
| Devil's Advocate | Waarsku dat ’n oop AP of onbeperkte reconnect/logging ’n sekuriteits- en real-time fout word. |

## LLM-gebruik

Geen plaaslike Ollama-model is vir hierdie amendment gebruik nie.
