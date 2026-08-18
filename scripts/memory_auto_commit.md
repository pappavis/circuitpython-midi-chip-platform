Update only memory_state.json using the current repository context.

Set or update these fields:

- current_work_package
- last_completed_action
- next_action
- next_command
- expected_result

Rules:

1. Do not modify production code.
2. Do not modify tests.
3. Do not modify MEMORY.md directly.
4. Do not modify docs/memory directly.
5. After saving memory_state.json, run:

python scripts/commit_with_memory.py --message "Memory checkpoint: update working state"

The commit wrapper must update MEMORY.md, append docs/memory history, update memory_state.json, stage the memory files, and create the git commit automatically.
