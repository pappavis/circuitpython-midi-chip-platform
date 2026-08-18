# CircuitPython MIDI Chip Platform — Emergency Recovery Pack

## Document Control Header

| Field | Value |
|---|---|
| Document type | Single Source of Truth emergency recovery entrypoint |
| Classification | Engineering recovery and handover artifact |
| Version | 1.0 |
| Status | Recovery baseline; Product Owner review required |
| Repository | `pappavis/circuitpython-midi-chip-platform` |
| Local checkout assessed | `circuitpython-midi-chip-platform-governance` |
| Snapshot date | 2026-08-18 |
| Snapshot commit | `6485f0a` (`fix(d1): initialize mvp timing time source`) |
| Runtime metadata | `v0.21.0`, story `HIL-DIAGNOSTIC-FRAMEWORK-001`, release date `2026-07-24` |
| Host-test baseline | `183 passed` on 2026-08-18 |
| Current product blocker | `MCP-US-055` — audible Logic Pro to D1/I2S acceptance |
| Document ID | `SSOT-RECOVERY-PACK-MCP-001` |

> Recovery rule: if a fact is not supported by the current repository, tests, HIL evidence, a hardware observation or an accepted ADR, classify it as `UNKNOWN`. Do not turn an assumption into a release claim.

## 1. Emergency Executive Summary

This repository implements a class-based CircuitPython retro-synth platform. The frozen first MVP is intentionally narrow:

```text
Logic Pro
  -> USB-MIDI
  -> LOLIN/Wemos ESP32-S2 Mini
  -> portable MIDI events
  -> monophonic D1 basic core
  -> safe mono I2S
  -> MAX98357A
  -> audible output
```

The host software is recoverable and its current automated suite passes. The MVP is **not Done**. The open P0 gate is reliable, objectively evidenced, audible Logic-to-D1 playback on the reference hardware. `MCP-US-057` release work and the mandatory eight-hour burn-in may only close after that product flow is accepted.

The most recent development work added HIL timing instrumentation around MIDI receive and audio playback, a blocking first-note experiment and a fix that injects the time source before creating the MVP timing recorder. This work must not be mistaken for completed physical acceptance.

The local `main` branch was observed as `56 commits ahead` and `6 commits behind` `governance/main`. Do not pull, merge, rebase, reset, force-push or publish until the divergence is inspected and a Product Owner-approved synchronization plan exists.

## 2. First 15 Minutes

Run these read-only or host-safe checks from the repository root:

```bash
pwd
git status --short --branch
git log -12 --date=iso --pretty=format:'%h %ad %s'
git remote -v
git branch -vv
```

Read, in this order:

1. [`AGENTS.md`](AGENTS.md) — binding delivery, architecture, QA and safety rules.
2. This recovery pack.
3. [`docs/mvp_scope_v0.1.0.md`](docs/mvp_scope_v0.1.0.md) — frozen MVP acceptance set.
4. [`docs/user_stories_v0.1.0.md`](docs/user_stories_v0.1.0.md) — story status and dependencies.
5. [`docs/governance/regression_memory_v0.1.0.md`](docs/governance/regression_memory_v0.1.0.md) — protected working behavior and P0 history.
6. [`docs/decisions/MCP-US-101-FIRST-MVP-STEP.md`](docs/decisions/MCP-US-101-FIRST-MVP-STEP.md) — Product Owner choice to focus on `MCP-US-055`.
7. [`EMERGENCY_DISASTER_RECOVERY.md`](EMERGENCY_DISASTER_RECOVERY.md) — detailed but partly stale handbook; verify every mutable status value.

Then verify the host baseline with the approved local interpreter when it exists:

```bash
/Volumes/data1/michiele/venv/venv3.12/bin/python -m pytest -q
```

Expected snapshot result:

```text
183 passed
```

If that interpreter is unavailable, create a project-local Python 3.11+ environment as described below. Never use `/usr/bin/python`, Python 2.7 or an unverified bare `python` for project tests or tooling.

## 3. Stop Conditions

Stop immediately and ask the Product Owner before proceeding when any of these conditions applies:

- the requested work has no approved story plan;
- a code change has not received the mandatory pre-change Principal QA Architect review;
- the change would touch the read-only `python-d1-synth` repository;
- repository synchronization could overwrite or discard local history;
- the target CIRCUITPY volume, serial port or board identity is ambiguous;
- the action would flash UF2 firmware, erase a volume or alter a bootloader without explicit approval;
- a secret, private device identifier, local backup or credential could enter Git;
- a diagnostic reports PASS while `note_on=0` or `note_off=0` for a note-routing claim;
- a HIL result is being used to claim audible success without a human audio observation;
- the work pulls SN76489, SID, OPL, BLE, web, stereo, DSP or multi-core scope ahead of the D1/Logic MVP.

## 4. Current Verified Snapshot

| Item | Status | Evidence |
|---|---|---|
| Package version | `0.21.0` | `pyproject.toml` |
| Runtime banner version | `0.21.0` | `src/midi_chip_platform/release.py` |
| Last local commit | `6485f0a` | local Git history |
| Worktree | Clean at assessment | `git status --short --branch` on 2026-08-18 |
| Branch divergence | Ahead 56, behind 6 vs `governance/main` | local Git tracking status |
| Host tests | 183 passed | full `pytest -q` run on 2026-08-18 |
| Reference device | LOLIN/Wemos ESP32-S2 Mini, CircuitPython 10.x | ADR-002 and HIL evidence |
| Default physical audio | MAX98357A mono I2S | MVP scope and ADR-003 |
| Primary product gate | `MCP-US-055` P0 impediment | user-story catalogue |
| Release gate | `MCP-US-057` open | user-story catalogue |
| Burn-in | Eight-hour MVP run still required | burn-in specification |

Mutable facts in README files or older recovery documents may lag behind source metadata and Git history. Resolve discrepancies using the following authority order:

1. accepted Product Owner decision and binding `AGENTS.md` rules;
2. current code plus executable tests;
3. current HIL evidence and human acceptance records;
4. accepted ADRs and frozen MVP scope;
5. story catalogue and review documents;
6. README, generated artifacts and historical handbooks.

Never silently edit conflicting sources into agreement. Record the discrepancy and update them together under an approved work package.

## 5. Current Work Package and Safe Continuation

The last factual implementation sequence was:

| Commit | Work |
|---|---|
| `2f24dcd` | Add MVP timing smoke experiment |
| `ca83630` | Force blocking tone for first-note experiment |
| `64ae465` | Measure MVP note-latency stages |
| `6485f0a` | Initialize the MVP timing time source correctly |

The Product Owner decision in `MCP-US-101` selected reopening `MCP-US-055`: objectively prove that an end user can produce audible D1/MAX98357 output from Logic Pro through the existing runtime. That decision explicitly forbids unplanned architecture or refactoring inside the acceptance story. If acceptance fails, create and approve a separate fix story before changing runtime behavior.

Safe continuation order:

1. Preserve and inspect the current Git state.
2. Re-run all host tests.
3. Confirm that release metadata, settings and deployed device files describe the same experiment.
4. Obtain the required Principal QA Architect pre-change verdict for any code change.
5. Run only the approved, bounded HIL procedure.
6. Capture host, serial, configuration and human-observation evidence in one correlated evidence package.
7. Classify the first observable failure without inventing a root cause.
8. If the product flow passes, complete the post-change QA review and Product Owner acceptance.
9. Only then prepare `MCP-US-057`, the eight-hour burn-in and release candidate evidence.

## 6. MVP Scope Boundary

### In scope for the first MVP

- safe CircuitPython boot and USB-MIDI enumeration;
- portable MIDI Note On/Off event handling;
- bounded routing into the D1 basic core;
- independent MAX98357A/I2S preflight;
- safe digital gain and mono output;
- Logic Pro external MIDI to audible D1 acceptance;
- regression evidence, HIL evidence and eight-hour stability proof.

### Outside the first MVP

- SN76489, SID 6581, OPL2 and OPL3 cores;
- BLE-MIDI positive support on the ESP32-S2;
- DIN/UART expansion;
- web control and Wi-Fi product features;
- stereo, DSP and multi-core execution;
- physical retro-chip backends;
- production enclosure, PCB and certified speaker/headphone output;
- USB identity polish.

Post-MVP code already present remains valuable, but it does not broaden the frozen release gate.

## 7. Repository Map

```text
circuitpython-midi-chip-platform-governance/
├── 00_Start_HERE_Emergency_recovery_pack.md
├── AGENTS.md
├── EMERGENCY_DISASTER_RECOVERY.md
├── README.md
├── pyproject.toml
├── src/midi_chip_platform/     host-safe package and device runtime classes
├── device/                     deployable CircuitPython entrypoints/config template
├── tests/                      host, architecture and HIL-tooling tests
├── docs/                       scope, stories, reviews, risks and evidence
│   ├── decisions/              ADRs and Product Owner decisions
│   ├── governance/             QA, regression and evidence rules
│   ├── evidence/               HIL and investigation evidence packages
│   ├── framework_engineering/  controlled architecture/quality context
│   └── incidents/              P0 incident history
└── outputs/                    generated Kanban and audit artifacts
```

Critical runtime files:

| File | Responsibility |
|---|---|
| `device/boot.py` | Safe USB profile before normal runtime |
| `device/code.py` | CircuitPython composition entrypoint |
| `device/i2s_test.py` | Independent audible I2S G-C-D preflight |
| `src/midi_chip_platform/device_runtime.py` | Device composition root |
| `src/midi_chip_platform/midi_usb.py` | USB-MIDI translation and receive behavior |
| `src/midi_chip_platform/d1_core.py` | Portable D1 waveform core |
| `src/midi_chip_platform/d1_runtime.py` | D1 USB-MIDI to I2S product path and timing hooks |
| `src/midi_chip_platform/i2s_audio.py` | CircuitPython I2S output adapter |
| `src/midi_chip_platform/hil.py` | Deployment, reset and evidence-oriented HIL tooling |
| `src/midi_chip_platform/hil_diagnostics.py` | Layered diagnostic and timing observations |
| `src/midi_chip_platform/release.py` | Injected release identity and startup banner |

## 8. Architecture and Non-Negotiable Rules

The architecture is port/adaptor oriented and class-based:

```text
USB-MIDI adapter
  -> portable event model
  -> channel/semantic handling
  -> D1 synth core
  -> safe audio boundary
  -> I2S adapter
  -> physical amplifier/speaker
```

Non-negotiable rules from `AGENTS.md` include:

- no global application state and no `global` keyword;
- no module-level runtime assignments or helper functions;
- no USB, MIDI, audio, Wi-Fi, pin or filesystem service may start during import;
- mutable state belongs to injected class instances;
- executable entrypoints create an application only inside a main guard;
- every changed Python file retains its traceability header;
- version, story, release date and runtime banner must agree for publication;
- no implementation begins before story-plan approval;
- every code change requires Principal QA Architect review before and after implementation;
- working audition, I2S preflight, USB receive, Logic routing and audible audio are protected regression behavior.

## 9. Rebuild the Host Environment

Requirements:

- Python 3.11 or newer;
- pytest for host validation;
- pyserial for HIL commands;
- no host installation of `adafruit-circuitpython-midi` as substitute for the device library.

Cold build:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,hil]"
python -m midi_chip_platform diagnose
python -m pytest -q
```

The virtual environment is disposable and must not be committed. If dependency installation requires network access, record the versions actually installed before claiming reproducibility.

## 10. Device Recovery Preconditions

Before any deployment, identify rather than assume:

- the mounted `CIRCUITPY` volume;
- the serial device;
- the physical board and CircuitPython version;
- the presence of required device libraries;
- the MAX98357A wiring and safe speaker/load;
- the intended Logic/CoreMIDI destination;
- the exact `settings.toml` experiment flags.

Known MVP reference wiring must be verified against current docs and hardware before power-up. The repository historically uses IO5 for bit clock, IO3 for word select and IO7 for data/DIN, but board capability discovery and the current approved wiring document remain authoritative.

`settings.toml` contains local runtime choices and possibly secrets. Start from `device/settings.toml.example`; never commit the real file. Never copy a private device backup into the repository.

## 11. HIL Recovery Ladder

Use the smallest test that isolates the next boundary:

1. **Connection proof** — discover volume and serial endpoint; read board/CircuitPython identity.
2. **Dependency proof** — verify the deployed dependency closure and `adafruit_midi` on `CIRCUITPY/lib`.
3. **Safe boot proof** — confirm boot banner, USB interfaces and recoverable REPL/CIRCUITPY access.
4. **Independent audio proof** — run `device/i2s_test.py`; confirm G-C-D audibly with the synth runtime absent.
5. **USB-MIDI proof** — observe real Note On and Note Off, not only CC messages.
6. **Routing proof** — correlate the host destination and device events with timestamps.
7. **D1 runtime proof** — correlate receive, dispatch, audio start and completion timing.
8. **Human product proof** — record whether Logic-triggered D1 audio is actually audible and acceptably realtime.
9. **Stability proof** — after functional acceptance, perform the required eight-hour burn-in with heap and reset/hang monitoring.

Do not skip directly to step 8 when a lower layer is unknown. Do not call steps 1–7 a substitute for audible product acceptance.

## 12. Evidence Package Minimum

Every HIL, investigation or release claim should contain:

- repository commit and worktree status;
- package/runtime release metadata;
- host Python executable and version;
- complete host test result;
- discovered board, volume and serial endpoint without publishing private identifiers;
- CircuitPython version and deployed artifact identity;
- redacted settings relevant to the test;
- exact stimulus, including MIDI channel, note and velocity;
- timestamped host-send events;
- timestamped device receive/dispatch/audio events;
- explicit counts for Note On and Note Off;
- result per acceptance criterion;
- human audible observation when sound is claimed;
- first observable failure or `UNKNOWN`;
- cleanup/recovery result after the run.

Use [`docs/governance/evidence_package_template_v1.0.md`](docs/governance/evidence_package_template_v1.0.md). Investigation stories close with `FIRST_DISAPPEARANCE_OF_<EVENT>` or `UNKNOWN`, not with unapproved fix advice.

## 13. Git Recovery and Synchronization

Two remotes exist in the assessed checkout:

| Remote | Intended repository observed |
|---|---|
| `origin` | `pappavis/circuitpython-midi-chip-platform` |
| `governance` | `pappavis/circuitpython-midi-chip-platform-governance` |

The local branch tracks `governance/main`, not `origin/main`. This is a material recovery risk.

Safe inspection:

```bash
git status --short --branch
git remote -v
git branch -vv
git log --graph --decorate --oneline --all -40
git diff governance/main...main --stat
git diff main...governance/main --stat
```

Required before synchronization:

1. Confirm which remote is authoritative.
2. Preserve the current commit hash and untracked/modified-file inventory.
3. Fetch without merging only after network access is approved.
4. Inspect both sides of the divergence.
5. Choose merge, rebase or selective transfer explicitly with the Product Owner.
6. Run the full suite after resolution.
7. Do not force-push or rewrite published history without explicit authorization.

Never use `git reset --hard` or checkout-based discard as a recovery shortcut.

## 14. Security and Hardware Safety

- Keep `settings.toml`, `.env`, `secrets.py`, device backups, UF2/BIN images and private identifiers out of Git.
- Redact Wi-Fi credentials and rotate any historically exposed password before network work.
- Do not enable Wi-Fi from `boot.py`.
- Start with safe digital gain and a verified physical load.
- Do not infer that a MAX98357A speaker output is safe for headphones or a production enclosure.
- Do not flash firmware, erase `CIRCUITPY` or modify a bootloader without separate explicit approval and a recovery image/procedure.
- Stop on unexpected heat, noise, repeated USB resets, filesystem corruption or unstable power.

## 15. Troubleshooting Matrix

| Symptom | First checks | Do not conclude yet |
|---|---|---|
| Tests fail after clone | Python version, editable install, exact commit, missing optional dependencies | Firmware defect |
| CIRCUITPY absent | data-capable cable, USB port, board power, boot mode | Board is dead |
| Serial `Device not configured` | re-enumerate ports, inspect mount/USB events, close competing tools | Root cause is known |
| Only CC7 appears | Logic routing, destination, stimulus, Note On/Off counters | MIDI path passed |
| I2S diagnostic audible, D1 silent | event receive, dispatch, audio-start timing, active settings | Amplifier is broken |
| Audio delayed 12–20 seconds | timestamp every boundary, inspect blocking/backlog behavior | Host MIDI is necessarily late |
| First note blocks | confirm active experiment flag and evidence timestamps | Experiment is production behavior |
| Runtime banner disagrees with package version | inspect `pyproject.toml`, `release.py`, device files and deployed artifact | Release is valid |
| Different host and device evidence | correlate clocks/run IDs and repeat bounded test | Evidence packages belong together |

## 16. Release Recovery Gate

The MVP may not be called Done until all of the following are true:

- frozen MVP Acceptance Set stories are Done;
- `MCP-US-055` audible Logic-to-D1 acceptance is approved;
- all host tests pass at the release commit;
- required HIL and regression evidence is complete;
- I2S preflight, USB-MIDI Note On/Off and audible D1 behavior remain intact;
- release metadata is consistent across package, runtime banner, docs and tag;
- the eight-hour burn-in completes without reset, hang, permanent silence or unexplained USB disconnect;
- heap stability stays within the documented boundary;
- risks and known limitations are recorded and accepted;
- the tag points to the tested commit;
- no secrets, private backups or local device identifiers are included.

## 17. Recovery Checklists

### Cold-start checklist

- [ ] Confirm repository path and remotes.
- [ ] Record current commit, branch, worktree and divergence.
- [ ] Read `AGENTS.md` and the frozen MVP scope.
- [ ] Verify Python 3.11+ executable.
- [ ] Install declared host dependencies in an isolated environment.
- [ ] Run the full host suite.
- [ ] Reconcile package and runtime release identity.
- [ ] Identify the active approved story and work package.
- [ ] Review regression memory before MIDI/audio/HIL work.
- [ ] Obtain required QA and Product Owner gates before changes.

### HIL checklist

- [ ] Discover the board, volume and serial port.
- [ ] Back up only allowed local configuration outside Git.
- [ ] Verify dependency closure and deployed artifact hashes/identity.
- [ ] Confirm safe boot and recoverable REPL.
- [ ] Run independent I2S preflight.
- [ ] Confirm real Note On and Note Off events.
- [ ] Capture correlated timing evidence.
- [ ] Record human audible result.
- [ ] Restore temporary instrumentation or leave it disabled by default.
- [ ] Confirm the board remains recoverable after testing.

### Publication checklist

- [ ] Resolve remote authority and branch divergence deliberately.
- [ ] Perform post-change Principal QA Architect review.
- [ ] Obtain Product Owner acceptance.
- [ ] Run full tests on the exact publication commit.
- [ ] Complete required HIL and burn-in evidence.
- [ ] Update backlog, Kanban, docs and release metadata together.
- [ ] Scan for secrets, device backups and private identifiers.
- [ ] Commit narrowly and review the final diff.
- [ ] Push only to the confirmed remote/branch.

## 18. Known Risks and Technical Debt

| Risk/debt | Recovery impact |
|---|---|
| P0 audible realtime path remains unaccepted | Blocks MVP and release candidate |
| Local branch diverges from tracked remote | Publication can lose or duplicate work |
| README and older recovery handbook contain stale status | A new engineer may resume the wrong story/version |
| Host tests cannot prove physical sound | False-positive release risk |
| Serial capture can fail during HIL | Evidence may be incomplete or miscorrelated |
| Experimental blocking/timing behavior exists in latest commits | Active settings must be identified before HIL |
| Device identity and ports vary per host | Hardcoded endpoints make recovery fragile |
| Historical credential exposure is documented | Credentials require rotation before network work |
| No repository evidence of CI at this snapshot | Local full-suite execution remains essential |

## 19. Recovery Scenarios

### Repository exists, documentation is missing

Recover facts from `pyproject.toml`, release metadata, source headers, tests, Git history and HIL evidence. Rebuild a status ledger. Do not infer Product Owner acceptance from green tests.

### Documentation exists, code is missing

Restore from the confirmed Git remote and exact tag/commit. Treat generated artifacts and copied device volumes as evidence, not authoritative source code. Never reconstruct production code by blindly copying an old `CIRCUITPY` backup.

### Hardware exists, host checkout is missing

Do not overwrite the device. First inventory the mounted volume and preserve an authorized local backup outside Git. Restore the host repository separately, compare artifact identities and only deploy after determining which side is newer and approved.

### Only code and backlog remain

Run tests, reconstruct the story dependency chain, verify accepted ADRs, inventory runtime configuration and repeat the HIL ladder. All previous human audio acceptance becomes `UNKNOWN` unless preserved as repository evidence.

### Remote and local history disagree

Freeze writes. Record both commit graphs, identify unique commits, confirm remote authority and obtain a synchronization decision. Preserve both histories until the full suite and required HIL proof pass on the resolved branch.

## 20. Glossary

| Term | Meaning |
|---|---|
| D1 | The project's first portable monophonic basic synth core |
| HIL | Hardware-in-the-loop validation using the real board and peripherals |
| I2S | Digital audio transport used for the MAX98357A output path |
| MVP | Frozen first release proving Logic USB-MIDI to audible D1 output |
| P0 | Highest-priority product blocker |
| Product proof | Human-observed end-to-end behavior, supported by correlated evidence |
| Regression memory | Protected prior behavior that a change must not break |
| SSOT | Single Source of Truth recovery entrypoint |
| UNKNOWN | A fact not currently proven by acceptable evidence |

## 21. Final Recovery Principle

Recover the smallest proven system first. Preserve Git history, keep the physical device recoverable, validate one boundary at a time, and distinguish host correctness from hardware and human acceptance. The next legitimate milestone is not a new synth feature: it is reliable, evidenced, audible Logic Pro to D1/MAX98357 playback, followed by stability proof and the MVP release gate.

