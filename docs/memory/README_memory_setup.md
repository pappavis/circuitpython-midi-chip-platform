# A71C4E9B

Ja. Voor jouw script zou ik post-commit gebruiken als je wilt dat MEMORY.md na iedere succesvolle commit automatisch wordt bijgewerkt. Git voert post-commit uit nadat de commit gemaakt is; een hook moet executable zijn.  

Ga vanuit de root van je repository als volgt te werk.

# 1. Controleer eerst het script handmatig
```bash
python scripts/update_memory.py \
  --mode manual \
  --trace-id TEST-001
```
Je zou ongeveer moeten krijgen:
```
[MEMORY] MEMORY.md updated
[MEMORY] History appended: ...
[MEMORY] memory_state.json updated
```

Controleer daarna:
```bash
git status --short
```
# 2. Maak de Git-hook
```bash
mkdir -p .git/hooks
nano .git/hooks/post-commit
```

Zet hierin:
```bash
#!/bin/sh
echo "[MEMORY-HOOK] Updating repository memory..."
python3 scripts/update_memory.py \
    --mode post-commit \
    --trace-id "GIT-POST-COMMIT"
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "[MEMORY-HOOK] WARNING: memory update failed."
    exit $RESULT
fi
echo "[MEMORY-HOOK] Memory update completed."
exit 0
```
Opslaan en vervolgens executable maken:
```bash
chmod +x .git/hooks/post-commit
```
Git negeert hooks die niet executable zijn.  

3. Controleer of de hook correct staat
```bash
ls -la .git/hooks/post-commit
```
Je wilt iets als:
```bash
-rwxr-xr-x ... .git/hooks/post-commit
```
Test hem rechtstreeks:

> .git/hooks/post-commit

Daarna:
```bash
git status --short
```
Je zou wijzigingen moeten zien aan onder andere:
```md
MEMORY.md
memory_state.json
docs/memory/memory_history_....md
```

4. Test de echte Git-flow

Maak bijvoorbeeld een lege testcommit:
```bash
git commit --allow-empty -m "test memory hook"
```
Na de commit zou automatisch moeten verschijnen:
```md
[MEMORY-HOOK] Updating repository memory...
[MEMORY] MEMORY.md updated
[MEMORY] History appended: ...
[MEMORY] memory_state.json updated
[MEMORY-HOOK] Memory update completed.
```
post-commit is hiervoor geschikt omdat Git deze hook pas uitvoert nadat de commit daadwerkelijk is gemaakt.  

Maar er zit een belangrijk architectuurprobleem in deze aanpak

Na:
```md
git commit
      ↓
commit gemaakt
      ↓
post-commit
      ↓
update_memory.py
      ↓
MEMORY.md gewijzigd
memory_state.json gewijzigd
history gewijzigd
```
staan die nieuwe memory-wijzigingen niet in de commit die zojuist gemaakt is.

Je krijgt dus bijvoorbeeld:
```bash
git status
```
met:

modified: MEMORY.md
modified: memory_state.json
untracked: docs/memory/memory_history_202608181300.md
Dat kan precies zijn wat je wilt, maar als het doel is:

iedere commit moet zijn actuele MEMORY.md/state bevatten

dan hoort dit eigenlijk in pre-commit.

Dan wordt de flow:

```md
git commit
    ↓
pre-commit
    ↓
update_memory.py
    ↓
git add MEMORY.md memory_state.json docs/memory/
    ↓
commit

Git’s pre-commit wordt vóór de commit uitgevoerd en kan de commit zelfs tegenhouden wanneer de hook met een non-zero status eindigt.  

Daarvoor zou ik deze hook gebruiken:
```bash
#!/bin/sh
echo "[MEMORY-HOOK] Updating repository memory before commit..."
python3 scripts/update_memory.py \
    --mode pre-commit \
    --trace-id "GIT-PRE-COMMIT"
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "[MEMORY-HOOK] ERROR: memory update failed."
    exit $RESULT
fi
git add \
    MEMORY.md \
    memory_state.json \
    docs/memory/
echo "[MEMORY-HOOK] Memory updated and staged."
exit 0
```
Installeren:

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -e

echo "[MEMORY] Updating MEMORY.md before commit..."

python scripts/update_memory.py \
  --mode pre-commit \
  --trace-id "GIT-PRE-COMMIT" \
  --current-work-package "Commit checkpoint" \
  --last-completed-action "Preparing commit and updating operational memory" \
  --next-action "Continue from memory_state.json after commit" \
  --next-command "python -m pytest" \
  --expected-result "All tests pass or failures are captured as evidence"

git add MEMORY.md
git add memory_state.json
git add docs/memory || true

echo "[MEMORY] MEMORY.md, memory_state.json and docs/memory staged."
EOF
```
Maak hem executable:
```bash
chmod +x .git/hooks/pre-commit
```


Daarna testen:
```bash
git add scripts/update_memory.py
git commit -m "test pre-commit memory automation"
git status
git show --stat HEAD

```
Voor jouw governance/continuity-systeem zou ik pre-commit kiezen, omdat MEMORY.md, memory_state.json en de history dan onderdeel worden van dezelfde Git-snapshot waarop ze betrekking hebben.

Nog beter voor een repository die je tussen Mac/Windows/Linux wilt gebruiken: zet de hook zelf onder versiebeheer, bijvoorbeeld in .githooks/pre-commit, en configureer de repository éénmalig met:
```bash
git config core.hooksPath .githooks
```
Git ondersteunt core.hooksPath specifiek om een andere hooks-directory te gebruiken dan .git/hooks.   Daarmee kun je de hooks gewoon committen en hoef je niet op iedere machine verborgen bestanden in .git/hooks handmatig te onderhouden.


> ChatID: A71C4E9B
