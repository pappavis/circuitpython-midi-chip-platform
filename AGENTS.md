# Project Delivery Rules

<!--
Bestand: AGENTS.md
Versienommer: 0.9.0
Doel: Afdwingbare werkreels vir mense, Codex en ander ontwikkelagente.
Sprint: Sprint 0
Epic: MCP-EPIC-001 Platform Foundation
User-Story: PRINCIPAL-QA-ARCHITECT-001
Actienr: MCP-ACT-QA-ARCHITECT-001-GOV-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / PRINCIPAL-QA-ARCHITECT-001
-->

## Harde argitektuurreels

1. **Globale veranderlikes en globale toepassingsstatus is verbode.**
2. Die `global`-sleutelwoord is verbode.
3. Modulevlak `Assign` en `AnnAssign` vir runtime-data, konfigurasie, caches, registries, toestelle of dienste is verbode.
4. Modulevlak helperfunksies is verbode. Gedrag woon in klasse as instansiemetodes, `@classmethod` of `@staticmethod`.
5. Alle veranderlike status word deur 'n klasinstansie besit en eksplisiet via constructors/dependency injection deurgegee.
6. 'n Module mag by import geen USB, MIDI, klank, Wi-Fi, webserver, pen of lêerstelsel-diens begin nie.
7. Geen modulevlak diensobjek soos `app = App()`, `midi = MidiService()` of `audio = AudioOutput()` nie.
8. Imports, klasdefinisies en docstrings is toegelaat; release-metadata word deur 'n klasinstansie besit en nie as modulevlakveranderlikes versteek nie.
9. 'n Uitvoerbare `code.py` of CLI-entrypoint mag slegs binne 'n main guard 'n topvlak `Application`-instansie skep en onmiddellik `run()` roep.
10. Die synth moet veilig as 'n biblioteek ingevoer kan word, veral deur die latere webinterface en host-simulator.
11. Sonder verdere kwalifikasie beteken `synth` in gesprekke, stories en dokumentasie hierdie CircuitPython MIDI Chip Platform; die desktop D1-projek word altyd eksplisiet as `python-d1-synth` benoem.

## Kodeweergawe en naspeurbaarheid

1. Elke gegenereerde of gewysigde `.py`-lêer bevat 'n header met bestand, kodeweergawe, doel, sprint, epic, user story, aksienommer en relevante ChatID.
2. 'n Host-CLI of toestel-runtime toon by verstek tydens startup minstens projekweergawe, aktiewe user story/amendment en release-datum.
3. Startup-metadata word deur 'n geïnjekteerde klasinstansie gelewer; geen globale metadata- of toepassingsstatus word ingestel nie.
4. `pyproject.toml`, runtime-banner, story-artefak en release-notas moet dieselfde weergawe rapporteer voordat 'n commit gepubliseer word.
5. Die argitektuurtoetse kontroleer headers en importveiligheid; 'n release-identiteitstoets kontroleer die startup-banner.

## Afdwinging

MCP-US-002 moet AST-kontraktoetse skep wat minstens die volgende as mislukkings merk:

- modulevlak runtime-toekennings;
- enige `global`-statement;
- modulevlak funksiedefinisies;
- modulevlak constructor-/start-oproepe;
- direkte bord-, netwerk- of audio-newe-effekte tydens import.

Toetse self word ook in toetsklasse georganiseer. 'n Uitsondering op hierdie reels vereis 'n goedgekeurde ADR en Product Owner-besluit; gerief is nie 'n geldige uitsondering nie.

## Story- en scope-dissipline

1. Werk volg die geordende backlog en sy afhanklikhede.
2. Voor elke story lewer die span 'n kort uitvoerplan met lêers, rooi toets, groen implementering, risiko's en menslike aanvaarding.
3. Geen implementering begin voor Product Owner-goedkeuring van daardie story-plan nie.
4. 'n Side quest word in Backlog/Later/Parking Lot geplaas; dit verander nie die aktiewe story nie.
5. 'n Defek teen die aktiewe aanvaardingskriteria word 'n impediment binne dieselfde story.
6. Geen GUI-, web-, nuwe kern-, DSP-, PCB- of packaging-werk word vroeer ingetrek omdat dit interessant lyk nie.
7. Codex waarsku die Product Owner wanneer 'n versoek die logiese volgorde, argitektuur of werkende synth kan breek.
8. Die bevrore MVP Acceptance Set in `docs/mvp_scope_v0.1.0.md` is die enigste release-scope; post-MVP werk kan dit nie stilweg verbreed nie.
9. Die bindende oorblywende pad is `US-016 -> US-063 -> US-055 -> US-057`; US-005 en die US-014 AudioOutput-kontrak is gesluit.
10. US-016 se `device/i2s_test.py` is klasgebaseerd, het geen synth-package-import of globale status nie en besit I2S eksklusief terwyl dit loop.
11. SN76489 en elke volgende kern begin eers nadat die D1/Logic MVP aanvaar is.
12. Elke langlopende runtime-story verklaar `Burn-in: Required` of gemotiveerd `Burn-in: N/A`; die duur en heap-grense volg `docs/burn_in_heap_stability_spec_v0.1.0.md`.

## Principal QA Architect Gate

1. Voor elke kodewysiging is 'n Principal QA Architect review verpligtend volgens `docs/governance/principal_qa_architect_agent_v0.1.0.md`.
2. Die Principal QA Architect is 'n review-agent, nie 'n programmeer-agent nie; die agent skryf geen kode en implementeer geen fix nie.
3. Die implementer wys eers slegs die QA-review aan die Product Owner en wag op goedkeuring voordat enige kode verander word.
4. Na implementering word dieselfde Principal QA Architect review weer uitgevoer voordat die werk as gereed, gepubliseer of Done gemerk word.
5. By enige twyfel oor regressie, timing, MIDI-ontvangs, audio-uitset, HIL-bewys of scope is die verdict `REJECT`.
6. Die bewyslas is regressiebewys: bewys dat bestaande funksionaliteit nog werk; groen host-toetse alleen is onvoldoende.
7. Elke MIDI-, audio-, runtime-, HIL- of diagnostic-wysiging moet `docs/governance/regression_memory_v0.1.0.md` raadpleeg.
8. `REG-080-001` is 'n aktiewe P0 regressieherinnering: audition weg, geen `NoteOn`/`NoteOff`, slegs CC7, en 'n foutiewe `PASS`.
9. 'n Diagnostic wat note-routing moet bewys, mag nie slaag wanneer `note_on=0` en `note_off=0` nie.
10. Geen patch mag 'n werkende audition, I2S-preflight, USB-MIDI receive, Logic Pro routing of hoorbare audio stilweg verwyder nie.

## Produksie-repositorygrens

1. `pappavis/python-d1-synth` en elke plaaslike checkout daarvan is produksiekode en absoluut leesalleen.
2. Geen bronkode, toetse, dokumentasie, konfigurasie, backlog, Git-geskiedenis, commit of push mag daar verander word nie.
3. Die repository mag slegs gelees word vir bevestigde gedrag, kontrakte en lessons learned.
4. Hergebruik beteken dat 'n nuwe, aangepaste implementering in hierdie repository geskryf en hier getoets word; kode word nie terug in `python-d1-synth` geplaas nie.
5. Enige taak wat die grens sou oorskry, word gestop en as 'n scope- of veiligheidsimpediment gerapporteer.

## Virtuele span

Elke story bevat 'n sigbare bydraerekord van:

- Product Owner;
- Scrum Master;
- Business Analyst;
- Chief Enterprise Architect;
- Solution Architect;
- relevante Embedded/MIDI/DSP/Web-spesialis;
- QA/HIL;
- Release/Documentation;
- Devil's Advocate.

'Not impacted' is toelaatbaar, maar moet met een sin gemotiveer word. Dit verhoed denkbeeldige spanaktiwiteit en maak werklike besluitneming naspeurbaar.

Copilot kan as eksterne argitektuurreviewer inset lewer. Dié inset is adviserend: die Solution Architect en QA toets dit teen hierdie repository, amptelike bronne en Product Owner-besluite voordat enige voorstel kode of backlog word.

## Framework Engineering-konteks

1. `docs/framework_engineering/README.md` is die beheerde konteksingang vir visie, argitektuur, kwaliteit en kennis.
2. Agente laai slegs die aktiewe story, relevante argitektuur/ADR, betrokke bron en toetse; hulle behandel ou chat- of reviewteks nie outomaties as huidige feite nie.
3. Die glossary en enterprise meta model bepaal projekterme en naspeurbaarheidsverhoudings; die user-story-katalogus bly die bron van produkvolgorde en status.
4. Die quality manual, test strategy en review engine word voor Done toegepas. Dokumentasie alleen kan nooit host-, HIL- of menslike bewys vervang nie.
5. Prompt compiler-, context loader- en knowledge-base-spesifikasies beheer ontwikkelwerk; hulle is nie firmware-, synth-runtime- of LLM-afhanklikhede nie.
6. Framework Engineering mag nie WIP-limiete, afhanklikhede, Product Owner-goedkeuring, hardewareveiligheid of die leesalleen D1-grens omseil nie.

## Kwaliteits- en releasehekke

- Red-toets voor groen implementering.
- Alle host-toetse groen voor toestelontplooiing.
- Hardeware-aanvaarding vir enige fisiese MIDI-, klank-, klok- of penverandering.
- Vroeë HIL-stories toon in die chat 'n drieledige Device Connection Proof: verbinding, gedeployde artefak en werklike toesteluitvoering. Ná eksplisiete Product Owner-vertroue mag dit vir host-only werk opsioneel word, maar nooit vir HIL-, herstel- of releasebewys nie.
- Seriële poorte, volume-name en toestel-ID's word ontdek en nie as universele konstantes gestoor nie; private UID-, MAC-, netwerk- en geheime-data word uit logs en Git gehou.
- Headers bevat bestand, weergawe, doel, sprint, epic, story, aksie en ChatID.
- Backlog, dokumentasie en Kanban word saam bygewerk.
- Lessons learned word na elke groep van drie of vier voltooide stories bygewerk, en ook by elke epic-/releasegrens of ernstige impedimentgroep.
- 'n Toepaslike story kan nie Done word sonder sy burn-in/heap-verslag nie; dokumentasie- en suiwer hostkontrakstories mag dit gemotiveerd `N/A` merk.
- Geen commit/push indien geheime, private rugsteune, plaaslike toestel-ID's of onbevestigde release-aansprake teenwoordig is nie.

## Python-interpretergrens

1. `/usr/bin/python`, Python 2.7 en 'n onbevestigde kaal `python` word nooit vir projektoetse, builds, deploys of hulpmiddels gebruik nie.
2. Codex-ontwikkelopdragte op KodeklopperM4 gebruik eksplisiet `/Volumes/data1/michiele/venv/venv3.12/bin/python`; `~/venv/venv` is 'n toegelate alternatief nadat sy Python 3.11+-weergawe bevestig is.
3. Eindgebruikers skep en aktiveer hul eie projeklokale `.venv`; dokumentasie verifieer daarna `sys.executable` en Python-weergawe voordat `python -m ...` gebruik word.
4. Geen absolute virtualenv-pad word in runtimekode, publieke config of kruisplatform-startup vasgeskryf nie.

## Opsionele plaaslike LLM-beleid

1. Ollama is slegs 'n opsionele ontwikkelhulpmiddel en nooit 'n firmware-, synth-runtime-, bou- of IDE-afhanklikheid nie.
2. Gebruik vereis 'n goedgekeurde, benoemde taak en voorafkontrole met `ollama list` plus 'n klein tydbegrensde proefaanroep.
3. Geen geheime, toestelrugsteune, privaat data of produksiekode word na 'n modelprompt gestuur nie.
4. Die verstekverskaffer is `default`; enige toekomstige host-hulpmiddel moet ook `--llm-provider default` aanvaar om Ollama eksplisiet af te skakel.
5. Indien die rekenaar stadiger word, word die plaaslike versoek gestop en die taak gaan met die verstek-Codex/LLM-pad voort.
6. Codex hersien alle plaaslike modeluitset en gewone toetse en menslike aanvaarding bly verpligtend.
