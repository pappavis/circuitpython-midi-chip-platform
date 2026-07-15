# Repository Identity And Sync

<!--
Bestand: repository_identity_and_sync_v0.1.0.md
Versienommer: 0.1.0
Doel: Voorkom verwarring, drift en handmatige kopieerwerk tussen implementasie- en governance-repositories.
Sprint: Sprint 2
Epic: MCP-EPIC-008 Portability, Quality And Release
User-Story: MCP-US-007 USB MIDI Receive Loop
Actienr: MCP-ACT-007-IMP-REPO-001
ChatID: CHATOD-20260714-MCP-CP-MVP-001 / REPOSITORY-IDENTITY-IMPEDIMENT-001
-->

## Twee eksplisiete GitHub-identiteite

| Remote | Rol | Besluitreg |
|---|---|---|
| `pappavis/circuitpython-midi-chip-platform` | Kanonieke produkimplementasie, releases en toestel-deploybron | Runtime- en releasebesluite |
| `pappavis/circuitpython-midi-chip-platform-governance` | Gesinchroniseerde governance-, QA-, argitektuur- en delivery-bewysspoor | Artefak-, assurance- en prosesbesluite |

Die governance-repository bevat tans dieselfde volledige commitgeskiedenis en bronkode om end-tot-end traceability te behou. Dit maak dit **nie** 'n tweede onafhanklike produkbranch nie. Produkgedrag word deur die implementasierepo vrygestel; governancebewys verwys altyd na presies dieselfde commit-ID.

## Plaaslike checkouts

Plaaslike vouername of IDE-workspaces bepaal nooit die repository-identiteit nie. Voor enige werk moet die agent of mens die identiteit bewys met:

```bash
git status --short
git remote -v
git branch --show-current
git log -1 --oneline
```

'n Ontbrekende lêer word nie dadelik as bronkodeverlies behandel nie. Vergelyk eers die huidige commit met die kanonieke remote en gebruik 'n fast-forward pull indien die checkout skoon en agter is.

## Sinkronisasiekontrak

1. Maak en toets die verandering in een skoon werkboom.
2. Commit een keer met dieselfde traceability-ID.
3. Push dieselfde commit na implementasie `main` en governance `main`.
4. Fast-forward ander skoon plaaslike checkouts vanaf hul korrekte remote.
5. Vergelyk die commit-ID; moenie lêers handmatig tussen checkouts kopieer nie.
6. By enige dirty checkout: stop, beskerm menslike wysigings en ondersoek voor merge.

## Releasehek

'n Release of HIL-deploy is geldig wanneer:

- implementasie- en governance-remote dieselfde goedgekeurde commit bevat;
- die plaaslike implementasie-checkout nie agter die remote is nie;
- die dependency-geslote deploymanifest vanuit die implementasiecommit gebou is;
- toesteluitvoer dieselfde weergawe, story en release-datum rapporteer.

## Impedimentles

`device_runtime.py` het in 'n ou plaaslike checkout ontbreek, maar was teenwoordig in die aktiewe commit, die implementasie-remote en op `CIRCUITPY`. Die oorsaak was checkout-drift, nie 'n verlore deploydependency nie. Hierdie onderskeid word in die volgende lessons-learned-kontrolepunt hergebruik vir nuwe subtractive-, D1-, drum-machine- en FM-synthprojekte.
