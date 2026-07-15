# Glossary

<!--
Bestand: glossary_v0.1.0.md
Versienommer: 0.2.0
Doel: Gee een projekspesifieke betekenis vir kritieke produk-, MIDI-, audio- en governance-terme.
Sprint: Sprint 2
Epic: MCP-EPIC-009 Framework Engineering
User-Story: MVP-SCOPE-REDUCTION-001
Actienr: MCP-ACT-MVP-SCOPE-001-GLOSS-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MVP-SCOPE-REDUCTION-001
-->

| Term | Betekenis in hierdie projek |
|---|---|
| Synth | CircuitPython MIDI Chip Platform, tensy `python-d1-synth` eksplisiet genoem word |
| Synth core | Vervangbare klas wat genormaliseerde events in voices/klankgedrag omsit |
| D1-basiskern | Nuwe CircuitPython-implementering van bevestigde sine/saw/square-basiskontrakte; geen kopie van die produksierepo nie |
| Transport | USB-MIDI, BLE-MIDI of DIN/UART-adapter wat boodskappe ontvang |
| Event | Draagbare Note-, Control- of Clock-waarde sonder transportspesifieke objek |
| Port | Klasgebaseerde kontrak tussen domein en adapter |
| Capability gate | Eksplisiete ondersteund/nie-ondersteund/unknown besluit op werklike runtime-vermoë |
| Board profile | Data wat 'n bord se modules, penne en veilige backends beskryf |
| HIL | Hardware-in-the-loop toets op die werklike bord en relevante randapparaat |
| Device Connection Proof | Connection + deployment + execution; storyspesifieke stimulus volg daarna |
| Dependency closure | Bewys dat elke interne en eksterne runtime-import in die deploymanifest of device libraries bestaan |
| MVP Acceptance Set | Die bevrore lys stories wat alleen die eerste produkrelease beheer |
| MVP-Must | Direkte eindgebruikerbewys binne die MVP Acceptance Set |
| MVP-Enabler | Tegniese, veiligheids- of kwaliteitsvoorwaarde binne die MVP Acceptance Set |
| Post-MVP | Waardevolle werk wat nie die eerste D1/Logic-release blokkeer nie |
| In Review | Outomatiese werk is groen; menslike of fisiese aanvaarding is nog oop |
| Done | Kriteria, toetse/HIL, docs, Kanban, commit en aanvaarding is voltooi |
| Impediment | Bewese blokker teen die aktiewe story se kriterium, nie bloot 'n toekomstige idee nie |
| ADR | Onveranderlike rekord van 'n belangrike argitektuurbesluit en gevolge |
| Framework Engineering | Governance-laag vir visie, argitektuur, kennis, kwaliteit en agente; nie firmware nie |
| Prompt compiler | Ontwikkelproses wat 'n begrensde taakpakket uit gesaghebbende bronne saamstel; geen runtime-komponent nie |
| Context loader | Reels vir minimale relevante lêers en bewys wat voor werk gelees word |
| Instance-ID suffix | Stabiele vier-karakter, nie-geheime onderskeier in die USB-produknaam; nie 'n volledige UUID nie |
| USB identity | Manufacturer/product strings en ondersteunde USB-identifikasie wat in `boot.py` voor enumerasie gestel word |
| MIDI channel | Protokolkanaal 1-16 soos aan gebruikers gewys; adapters normaliseer biblioteekspesifieke indeksering |
| Pitch bend | Kanaalgebonde 14-bit performance control; bend range is konfigurasie |
| Slide | Deurlopende toonhoogtebeweging, dikwels per string/kanaal vanaf MIDI-kitaar |
| MIDI clock | 24 pulses per quarter note plus Start/Stop/Continue-semantiek |
| I2S | Digitale audio-bus na MAX98357 of latere stereo-DAC |
| Standalone I2S diagnostic | Onafhanklike klasgebaseerde G-C-D-toepassing sonder synth-import, gebruik om die fisiese klankpad te isoleer |
| Validated I2S profile | Pen-/formaatprofiel wat ook met die benoemde fisiese module deur HIL bewys is |
| PWM fallback | Meetbare debugsein; nie die primêre MAX98357-audio-invoer nie |
| MAX98357 | Mono I2S Class-D luidsprekerversterker; bridge-tied uitgang is nie line-level nie |
| Composition root | Enkele beheerde plek wat Application en sy ingespuite instansies konstrueer |
| Globale runtime-status | Modulevlak veranderlike diens-/toestel-/cache-/configstatus; absoluut verbode |
