Write-Host "[MEMORY] Updating repository memory..."

python scripts/update_memory.py `
    --mode pre-commit `
    --trace-id "AUTO-PRECOMMIT" `
    --current-work-package "Commit checkpoint" `
    --last-completed-action "Preparing commit" `
    --next-action "Continue development after commit" `
    --next-command "python -m pytest" `
    --expected-result "All tests pass"

if ($LASTEXITCODE -ne 0)
{
    Write-Error "update_memory.py failed"
    exit 1
}

git add MEMORY.md
git add memory_state.json

if (Test-Path "docs/memory")
{
    git add docs/memory
}

Write-Host "[MEMORY] Files staged."
exit 0
