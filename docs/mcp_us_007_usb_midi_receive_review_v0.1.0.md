# MCP-US-007 USB MIDI Receive Loop Review

<!--
Bestand: mcp_us_007_usb_midi_receive_review_v0.1.0.md
Versienommer: 0.3.1
Doel: Dokumenteer die USB-MIDI ontvangsadapter, fisiese deploy en menslike Note On/Off-hek.
Sprint: Sprint 2
Epic: MCP-EPIC-002 MIDI And Clock
User-Story: MCP-US-007 USB MIDI Receive Loop
Actienr: MCP-ACT-007-DOC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007-HIL
-->

## Gelewer

- `MidiMessageTranslator` vertaal Adafruit Note On, Note Off, CC, pitch bend en klok na die draagbare eventmodel.
- `UsbMidiInputPort` kies 'n poort volgens generiese indeks; geen vervaardiger- of toestelnaam is 'n kodekonstante nie.
- `CircuitPythonUsbMidiFactory` laai hardewaremodules eers wanneer die toesteladapter geskep word.
- `MidiReceiveLoop.poll_once()` is begrens, klasgebaseer en geskik vir 'n latere kooperatiewe scheduler.
- Onbekende boodskappe word veilig geïgnoreer.
- `UsbMidiReceiveDiagnostic` aanvaar slegs 'n ooreenstemmende Note On/Off-paar as PASS, normaliseer Note On met velocity nul na Note Off en sluit die poort altyd.
- Die diagnostiek is standaard af. `settings.toml` aktiveer dit tydelik; geen MIDI-vervaardiger, toestelnaam of private serial-pad is 'n kodekonstante nie.

## RED/GREEN-bewys

Die oorspronklike kontraktoets het tydens collection gefaal omdat `midi_chip_platform.midi_usb` nog nie bestaan het nie. Die fisiese diagnostiekkontrak het daarna RED gefaal omdat `UsbMidiReceiveDiagnostic` ontbreek het. Ná implementering slaag **86 hosttoetse**, Ruff en die dependency-closure-kontrole.

## Fisiese deploybewys

Die dependency-geslote manifest is nie-destruktief na die gekoppelde Wemos S2 gedeploy. Die volgende geredigeerde hekke is groen:

- USB CDC plus `CIRCUITPY` connection;
- interne import-closure;
- goedgekeurde SHA-256 deploypare;
- vereiste `adafruit_midi`-biblioteek;
- huidige `v0.12.0 / MCP-US-007` bootmarker;
- dependency-import en execution via serial REPL.

Geen private serial-identifiseerder, volume-inhoud of `settings.toml`-waarde is gepubliseer nie.

## Impediment MCP-US-007-IMPEDIMENT-002

Die eerste menslike her-toets het voor die receive-loop gestop met 'n CircuitPython `ValueError` oor ongeldige heelgetalsintaksis. Die oorsaak was `MIDI_DIAGNOSTIC_POLL_INTERVAL_SECONDS = 0.01`: die toestel se environment-parser het die on-gekwoteerde breukwaarde as 'n heelgetal probeer interpreteer.

Die herstel:

- voeg 'n RED-regressietoets by wat 'n CircuitPython-versoenbare stringwaarde afdwing;
- verander die voorbeeld en tydelike toestelkonfigurasie na `"0.01"`;
- laat `ConfigurationLoader` die string na die interne float omskakel;
- raak geen private of verkeerd benoemde bestaande settingslêer aan nie;
- herlaai die Wemos met 'n tien-minuut, begrensde diagnostiekvenster.

Ná die herstel slaag **87 hosttoetse** en Ruff. Die herbruikbare les word by die volgende lessons-learned-kontrolepunt ingesluit vir toekomstige subtractive-, D1-, drum-machine- en FM-synthprojekte: toets ingebedde konfigurasieparsers op die werklike firmware, nie net met desktop-TOML nie.

## Status

**In Review.** Hostgedrag, deploy, harde boot en clean-import-bewys is fisies groen. USB-MIDI Note On/Off op die Wemos S2 bly die menslike aanvaardingshek. Geen MIDI-boodskapontvangs word uit hashes of imports alleen afgelei nie.

## Menslike aanvaardingstoets

1. Maak `settings.toml` op die **CIRCUITPY-toestel** in Thonny oop. Deel of commit nooit die bestaande inhoud nie.
2. Voeg `MIDI_DIAGNOSTIC_ENABLED = true` by, of verander slegs daardie bestaande waarde na `true`.
3. Voeg indien ontbrekend `MIDI_DIAGNOSTIC_MAX_EVENTS = 8` en `MIDI_DIAGNOSTIC_TIMEOUT_SECONDS = 60` by.
4. Stoor en druk `Ctrl+D` in die Thonny REPL. Die log moet `USB_MIDI_DIAGNOSTIC_STATUS=READY` toon.
5. Maak in Logic Pro 'n **External MIDI**-track. Kies die tans gekoppelde CircuitPython/Wemos USB-MIDI-bestemming; kies MIDI-kanaal `All` of `1`.
6. Speel en los binne 60 sekondes een noot op enige gekoppelde MIDI-klawerbord of -kitaar.
7. Verwag een `USB_MIDI_EVENT=note_on` en een `USB_MIDI_EVENT=note_off`, elk met kanaal, noot en velocity, gevolg deur `USB_MIDI_DIAGNOSTIC_STATUS=PASS` en `matched_notes=1`.
8. Stel daarna `MIDI_DIAGNOSTIC_ENABLED = false`, stoor en druk weer `Ctrl+D` om normale boot te herstel.

Gebruik nooit Thonny en 'n tweede serial monitor gelyktydig nie. Logic se MIDI-roetering mag wel parallel met Thonny se REPL loop.

Hierdie story maak nog nie klank nie.
