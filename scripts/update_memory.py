#!/usr/bin/env python3
"""
File: scripts/update_memory.py
Version: 0.2.0
Purpose: Update MEMORY.md, append memory history, and maintain memory_state.json.

Sprint: Sprint 0
Epic: Governance / Continuity
User Story: MEMORY-AUTO-UPDATE
Action ID: MEMORY-HOOK-001
ChatID: K9R2M7P4
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class MemoryUpdateConfig:
    repo_root: Path
    mode: str
    next_action: str
    current_work_package: str
    last_completed_action: str
    next_command: str
    expected_result: str
    trace_id: str
    chatlog_file: Path | None


class GitInspector:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def current_branch(self) -> str:
        return self._run_git(["branch", "--show-current"], "UNKNOWN")

    def last_commit(self) -> str:
        return self._run_git(["log", "-1", "--pretty=%h - %s"], "UNKNOWN")

    def modified_files(self) -> str:
        output = self._run_git(["status", "--short"], "")
        return output if output else "NONE"

    def staged_files(self) -> str:
        output = self._run_git(["diff", "--cached", "--name-only"], "")
        return output if output else "NONE"

    def _run_git(self, args: list[str], fallback: str) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            value = result.stdout.strip()
            return value if value else fallback
        except Exception:
            return fallback


class MemoryStateStore:
    def __init__(self, state_file: Path) -> None:
        self.state_file = state_file

    def load(self) -> dict[str, Any]:
        if not self.state_file.exists():
            return {}

        try:
            with self.state_file.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
                return loaded if isinstance(loaded, dict) else {}
        except Exception:
            return {}

    def save(self, state: dict[str, Any]) -> None:
        self.state_file.write_text(
            json.dumps(state, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


class ChatLogReader:
    def __init__(self, chatlog_file: Path | None) -> None:
        self.chatlog_file = chatlog_file

    def latest_excerpt(self, max_chars: int = 2500) -> str:
        if self.chatlog_file is None:
            return "No chatlog file configured."

        if not self.chatlog_file.exists():
            return f"Chatlog file not found: {self.chatlog_file}"

        content = self.chatlog_file.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            return "Chatlog file exists but is empty."

        return content[-max_chars:]


class MemoryHistoryAppender:
    def __init__(self, history_dir: Path) -> None:
        self.history_dir = history_dir

    def append_history_entry(self, entry: str, timestamp: datetime) -> Path:
        self.history_dir.mkdir(parents=True, exist_ok=True)
        filename = f"memory_history_{timestamp.strftime('%Y%m%d%H%M')}.md"
        history_file = self.history_dir / filename

        with history_file.open("a", encoding="utf-8") as handle:
            handle.write(entry)
            handle.write("\n")

        return history_file


class MemoryDocumentUpdater:
    def __init__(self, memory_file: Path) -> None:
        self.memory_file = memory_file

    def update_auto_section(self, auto_section: str) -> None:
        if not self.memory_file.exists():
            raise FileNotFoundError("MEMORY.md not found in repository root.")

        content = self.memory_file.read_text(encoding="utf-8")
        start_marker = "<!-- MEMORY_AUTO_START -->"
        end_marker = "<!-- MEMORY_AUTO_END -->"

        if start_marker in content and end_marker in content:
            before = content.split(start_marker)[0]
            after = content.split(end_marker, 1)[1]
            updated = before + auto_section + after
        else:
            updated = content.rstrip() + "\n\n" + auto_section + "\n"

        self.memory_file.write_text(updated, encoding="utf-8")


class MemoryEntryBuilder:
    def __init__(
        self,
        config: MemoryUpdateConfig,
        git: GitInspector,
        state: dict[str, Any],
        chat_excerpt: str,
        timestamp: datetime,
    ) -> None:
        self.config = config
        self.git = git
        self.state = state
        self.chat_excerpt = chat_excerpt
        self.timestamp = timestamp

    def resolved_value(self, explicit_value: str, state_key: str, fallback: str) -> str:
        if explicit_value and explicit_value != "NOT SET":
            return explicit_value
        value = self.state.get(state_key, fallback)
        return str(value) if value else fallback

    def build_memory_state(self) -> dict[str, Any]:
        return {
            "last_updated_utc": self.timestamp.isoformat(),
            "trace_id": self.config.trace_id,
            "mode": self.config.mode,
            "current_branch": self.git.current_branch(),
            "last_commit": self.git.last_commit(),
            "modified_files": self.git.modified_files(),
            "staged_files": self.git.staged_files(),
            "current_work_package": self.resolved_value(
                self.config.current_work_package,
                "current_work_package",
                "NOT SET",
            ),
            "last_completed_action": self.resolved_value(
                self.config.last_completed_action,
                "last_completed_action",
                "NOT SET",
            ),
            "next_action": self.resolved_value(
                self.config.next_action,
                "next_action",
                "NOT SET",
            ),
            "next_command": self.resolved_value(
                self.config.next_command,
                "next_command",
                "NOT SET",
            ),
            "expected_result": self.resolved_value(
                self.config.expected_result,
                "expected_result",
                "NOT SET",
            ),
        }

    def build_history_entry(self, memory_state: dict[str, Any]) -> str:
        return f"""## Session Update - {self.timestamp.strftime('%Y-%m-%d %H:%M UTC')}

### Trace ID

{memory_state["trace_id"]}

### Update Mode

{memory_state["mode"]}

### Current Work Package

{memory_state["current_work_package"]}

### Last Completed Action

{memory_state["last_completed_action"]}

### Repository State

- Branch: `{memory_state["current_branch"]}`
- Last Commit: `{memory_state["last_commit"]}`
- Modified Files:
```text
{memory_state["modified_files"]}
```

### Staged Files

```text
{memory_state["staged_files"]}
```

### Next Action

{memory_state["next_action"]}

### Next Command

```powershell
{memory_state["next_command"]}
```

### Expected Result

{memory_state["expected_result"]}

### Latest Chatlog Excerpt

```text
{self.chat_excerpt}
```

### Notes For Next Developer

Treat MEMORY.md as operational state.
Treat Git as truth.
Treat tests as evidence.
Treat assumptions as unverified until proven.
"""

    def build_auto_section(self, memory_state: dict[str, Any], history_file: Path) -> str:
        return f"""<!-- MEMORY_AUTO_START -->

## Auto Generated Repository State

| Field | Value |
|---|---|
| Last Updated UTC | {memory_state["last_updated_utc"]} |
| Trace ID | {memory_state["trace_id"]} |
| Update Mode | {memory_state["mode"]} |
| Current Branch | {memory_state["current_branch"]} |
| Last Commit | {memory_state["last_commit"]} |
| Latest Memory History File | {history_file.as_posix()} |

### Current Work Package

```text
{memory_state["current_work_package"]}
```

### Last Completed Action

```text
{memory_state["last_completed_action"]}
```

### Next Action

```text
{memory_state["next_action"]}
```

### Next Command

```powershell
{memory_state["next_command"]}
```

### Expected Result

```text
{memory_state["expected_result"]}
```

### Modified Files

```text
{memory_state["modified_files"]}
```

<!-- MEMORY_AUTO_END -->
"""


class MemoryUpdateApplication:
    def __init__(self, config: MemoryUpdateConfig) -> None:
        self.config = config
        self.memory_file = config.repo_root / "MEMORY.md"
        self.state_file = config.repo_root / "memory_state.json"
        self.history_dir = config.repo_root / "docs" / "memory"

    def run(self) -> int:
        timestamp = datetime.now(UTC)
        git = GitInspector(self.config.repo_root)

        state_store = MemoryStateStore(self.state_file)
        existing_state = state_store.load()

        chat_reader = ChatLogReader(self.config.chatlog_file)
        chat_excerpt = chat_reader.latest_excerpt()

        builder = MemoryEntryBuilder(
            config=self.config,
            git=git,
            state=existing_state,
            chat_excerpt=chat_excerpt,
            timestamp=timestamp,
        )

        new_state = builder.build_memory_state()
        history_entry = builder.build_history_entry(new_state)

        history_appender = MemoryHistoryAppender(self.history_dir)
        history_file = history_appender.append_history_entry(history_entry, timestamp)

        auto_section = builder.build_auto_section(new_state, history_file)

        memory_updater = MemoryDocumentUpdater(self.memory_file)
        memory_updater.update_auto_section(auto_section)

        new_state["latest_memory_history_file"] = history_file.as_posix()
        state_store.save(new_state)

        print("[MEMORY] MEMORY.md updated")
        print(f"[MEMORY] History appended: {history_file}")
        print("[MEMORY] memory_state.json updated")
        return 0


class ArgumentParserFactory:
    def build(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Update MEMORY.md, docs/memory history and memory_state.json."
        )
        parser.add_argument(
            "--mode",
            default="manual",
            choices=[
                "manual",
                "pre-commit",
                "post-commit",
                "pytest",
                "release",
                "recovery",
            ],
        )
        parser.add_argument("--next-action", default="NOT SET")
        parser.add_argument("--current-work-package", default="NOT SET")
        parser.add_argument("--last-completed-action", default="NOT SET")
        parser.add_argument("--next-command", default="NOT SET")
        parser.add_argument("--expected-result", default="NOT SET")
        parser.add_argument("--trace-id", default="NOT SET")
        parser.add_argument(
            "--chatlog-file",
            default="docs/chatlog_copilot_codex.md",
        )
        return parser


class ConfigFactory:
    def from_args(self, args: argparse.Namespace) -> MemoryUpdateConfig:
        repo_root = Path(__file__).resolve().parents[1]
        chatlog_file = repo_root / args.chatlog_file if args.chatlog_file else None

        return MemoryUpdateConfig(
            repo_root=repo_root,
            mode=args.mode,
            next_action=args.next_action,
            current_work_package=args.current_work_package,
            last_completed_action=args.last_completed_action,
            next_command=args.next_command,
            expected_result=args.expected_result,
            trace_id=args.trace_id,
            chatlog_file=chatlog_file,
        )


def main() -> int:
    parser = ArgumentParserFactory().build()
    args = parser.parse_args()
    config = ConfigFactory().from_args(args)
    return MemoryUpdateApplication(config).run()


if __name__ == "__main__":
    raise SystemExit(main())
