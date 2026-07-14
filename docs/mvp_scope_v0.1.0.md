# MVP-omvang

<!--
Bestand: mvp_scope_v0.1.0.md
Versienommer: 0.3.0
Doel: Definieer die eerste toetsbare CircuitPython MIDI Chip Platform MVP.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
Actienr: MCP-ACT-MTM-AMEND-DOC-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MIDI-TRANSPORT-MULTICORE-AMENDMENT-001
-->

## Produkdefinisie

’n MIDI-beheerde, multi-kern retro-sintetiseerdermodule in pedaalvorm, met USB-MIDI, stereo-klankuitvoer, plaaslike webbeheer en uitbreibare skyfie-emulasie.

## Primêre gebruiker

’n Kitaar- of sintetiseerderentoesias wat die module in ’n musiekopstelling wil gebruik, MIDI kan roeteer maar nie noodwendig Python of ingebedde ontwikkeling ken nie.

## MVP-doel

Die MVP bewys een volledige vertikale vloei op die LOLIN/Wemos ESP32-S2 Mini:

1. Die toestel begin betroubaar en bied ’n herkenbare USB-MIDI-poort aan.
2. MIDI Note On/Off beheer ’n SN76489-agtige driestem-kern.
3. Pitch bend, CC1-modulasie en MIDI-klok word ontvang en diagnosties bewys.
4. Die eerste hoorbare vertikale sny werk mono via een MAX98357 I2S-versterker; PWM bly 'n diagnostiese fallback.
5. Elke stem kan links, regs of stereo gerouteer word.
6. ’n Opsionele G-C-D-opstartreeks laat ’n gebruiker die klankpad hoor.
7. ’n Eenvoudige plaaslike webblad kan die aktiewe kern en veilige kernparameters wys en verander.
8. Die oplossing kan vanaf ’n skoon toestel geïnstalleer, gediagnoseer en herstel word.
9. ’n Laat-MVP, geheuebegrensde delay/echo en eenvoudige reverb-spike kan omseil en beheer word sonder om MIDI te destabiliseer.
10. 'n Generiese USB-MIDI-kitaarkontroleerder kan note, akkoorde, per-kanaal bends en slides stuur; Fishman TriplePlay dien as verwysings-HIL-toestel, nie as hardgekodeerde afhanklikheid nie.
11. Die pedaal ontvang MIDI sonder DAW via 'n klas-kompatibele eksterne USB-host/Raspberry Pi-roete na 'n geabstraheerde DIN/UART-invoer.
12. Minstens twee verskillende geregistreerde kerninstansies kan laat in die MVP parallel loop met meetbare en veilige oorladinggedrag.

## Binne MVP

- Een verwysingsbord: LOLIN/Wemos ESP32-S2 Mini met CircuitPython 10.x.
- SN76489-lite is die eerste musikale kern; 'n minimale tweede kernadapter bewys laat-MVP parallelle multi-core-uitvoering voordat SID/OPL-akkuraatheid geëis word.
- USB-MIDI-invoer en MIDI-kanale 1-16.
- Note On, Note Off, velocity, pitch bend, CC1, All Notes Off en MIDI Clock/Start/Stop/Continue.
- Konfigureerbare pitch-bend range en multi-kanaal bend/slide-semantiek vir MIDI-kitaarkontroleerders.
- USB-MIDI device mode vir Logic/ander hosts plus 'n DIN/UART-transport vir 'n eksterne USB-MIDI-host soos 'n Raspberry Pi- of DOREMiDi-klas toestel.
- Interne klok teen standaard 120 BPM met eksterne MIDI-klok-oorskakeling.
- Een MAX98357 as die primêre vroeë mono-I2S-uitvoer, gevolg deur 'n hoorbare diagnostiese toetssein.
- PWM as altyd-beskikbare debug-/ossilloskoop-fallback wanneer I2S nie op 'n bord beskikbaar is nie.
- Later-MVP stereo via twee MAX98357-modules of 'n geprofileerde stereo-I2S-backend soos PCM5102; geen komponent word as universeel aanvaar nie.
- Klasgebaseerde poorte vir MIDI, kern, klok, klank en konfigurasie.
- Klein webbeheerblad op ’n vertroude plaaslike netwerk, een kliënt as ontwerpteiken.
- Laat-MVP DSP: ’n klein delay/echo en eenvoudige reverb-spike met harde geheue- en latensiegrense.
- Host-eenheidstoetse plus eksplisiete hardeware-in-die-lus-toetse.

## Buite die eerste MVP

- Oudio-invoer, pedalboard-through en verwerking van eksterne kitaarklank.
- Volledige SID-lêer-afspeel of internetstroming.
- Volledige GM MIDI-lêer-afspeel.
- Cycle-accurate OPL2/OPL3- of 6581-SID-klankakkuraatheid; dié adapters bly opvolgwerk ná die multi-core-kontrakbewys.
- ’n Volwaardige sekwenser, arpeggiator of akkoordkomponis.
- Bluetooth MIDI, DIN-MIDI-elektronika en ’n finale PCB/omhulsel.
- Ondersteuning wat beweer dat alle CircuitPython-borde identies werk.
- Raspberry Pi Zero/2/3 as dieselfde firmwarebeeld; Linux/Blinka is ’n afsonderlike adapterteiken.

## MVP-sukseskriteria

- ’n Skoon installasie vertoon ’n USB-MIDI-toestel op macOS en Windows.
- Drie gelyktydige note is hoorbaar sonder vasloop of hangende note.
- 'n Vroeë mono MAX98357-toetssein is hoorbaar voordat web-, DSP- of multi-core-werk begin.
- 'n MIDI-kitaar kan 'n enkele noot, akkoord en slide/bend speel met 'n bend range wat met die kontroleerder ooreenstem.
- Links, regs en stereo word met ’n ossilloskoop en luistertoets bevestig.
- MIDI-klok kan 120 BPM intern loop en ’n eksterne klok se tempo rapporteer.
- Die opstarttoets kan in konfigurasie aan/af geskakel word.
- Webparameterverandering onderbreek nie ’n aangehoue noot onaanvaarbaar nie.
- DSP-bypass en ten minste een hoorbare delay/reverb-proef loop binne die ooreengekome geheue- en latensiebegroting.
- Alle host-toetse is groen en die hardeware-aanvaardingstappe is gedokumenteer.
- 'n Controller kan sonder Logic via 'n eksterne USB-host/DIN-roete hoorbare MIDI aan die pedaal lewer.
- Twee kerninstansies kan parallel loop of die runtime weier 'n onveilige tweede kern deterministies met 'n duidelike resource-diagnose.
- Geen geheime of toestelspesifieke konstantes is in die openbare repository nie.

## Besluithekke

1. **Klankhek:** MAX98357 mono-I2S is die primêre vroeë pad; indien bordvermoë of stabiliteit faal, bewys PWM die debugpad en die impediment word gemeet.
2. **Webhek:** webbeheer mag nie MIDI/klanktydsberekening merkbaar benadeel nie.
3. **Kernhek:** ’n tweede kern word eers toegelaat nadat die kernpoort en SN76489-kontrakte groen is.
4. **Bordhek:** ’n nuwe bord kry eers ’n vermoënsprofiel en hardeware-toets; geen stil aannames nie.
