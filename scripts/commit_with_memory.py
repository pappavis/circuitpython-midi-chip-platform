#!/usr/bin/env python3
"""
File: scripts/commit_with_memory.py
Version: 0.1.0
Purpose: Update project memory files and create a git commit automatically.

Sprint: Sprint 0
Epic: Governance / Continuity
User Story: MEMORY-AUTO-COMMIT
Action ID: MEMORY-COMMIT-001
ChatID: R6T2M9K4
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommitMemoryConfig:
    repo_root: Path
    commit_message: str
    trace_id: str
    update_mode: str


class CommandRunner:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def run(self, command: list[str], allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            command,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0 and not allow_failure:
            raise RuntimeError(
                "Command failed:\n"
                f"Command: {' '.join(command)}\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )

        return result

    def output(self, command: list[str], fallback: str = "") -> str:
        result = self.run(command, allow_failure=True)
        if result.returncode != 0:
            return fallback
        return result.stdout.strip() or fallback


class GitStatusInspector:
    def __init__(self, runner: CommandRunner) -> None:
        self.runner = runner

    def has_changes(self) -> bool:
        status = self.runner.output(["git", "status", "--short"], "")
        return bool(status.strip())

    def has_staged_changes(self) -> bool:
        staged = self.runner.output(["git", "diff", "--cached", "--name-only"], "")
        return bool(staged.strip())


class MemoryCommitApplication:
    def __init__(self, config: CommitMemoryConfig) -> None:
        self.config = config
        self.runner = CommandRunner(config.repo_root)
        self.git = GitStatusInspector(self.runner)

    def run(self) -> int:
        self.update_memory()
        self.stage_memory_files()

        if not self.git.has_staged_changes():
            print("[MEMORY-COMMIT] No staged memory changes to commit.")
            return 0

        self.create_commit()
        print("[MEMORY-COMMIT] Memory commit completed.")
        return 0

    def update_memory(self) -> None:
        print("[MEMORY-COMMIT] Updating MEMORY.md and memory_state.json...")

        self.runner.run(
            [
                "python",
                "scripts/update_memory.py",
                "--mode",
                self.config.update_mode,
                "--trace-id",
                self.config.trace_id,
            ]
        )

    def stage_memory_files(self) -> None:
        print("[MEMORY-COMMIT] Staging memory files...")

        self.runner.run(["git", "add", "memory_state.json"], allow_failure=True)
        self.runner.run(["git", "add", "MEMORY.md"], allow_failure=True)
        self.runner.run(["git", "add", "docs/memory"], allow_failure=True)
        self.runner.run(["git", "add", "docs/chatlog_copilot_codex.md"], allow_failure=True)

    def create_commit(self) -> None:
        print("[MEMORY-COMMIT] Creating git commit...")

        self.runner.run(
            [
                "git",
                "commit",
                "-m",
                self.config.commit_message,
            ]
        )


class ArgumentParserFactory:
    def build(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Update memory files and commit them automatically."
        )

        parser.add_argument(
            "--message",
            required=True,
            help="Git commit message.",
        )

        parser.add_argument(
            "--trace-id",
            default="AUTO-MEMORY-COMMIT",
            help="Trace ID written into memory update.",
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
            help="Memory update mode.",
        )

        return parser


class ConfigFactory:
    def from_args(self, args: argparse.Namespace) -> CommitMemoryConfig:
        repo_root = Path(__file__).resolve().parents[1]

        return CommitMemoryConfig(
            repo_root=repo_root,
            commit_message=args.message,
            trace_id=args.trace_id,
            update_mode=args.mode,
        )


def main() -> int:
    parser = ArgumentParserFactory().build()
    args = parser.parse_args()
    config = ConfigFactory().from_args(args)
    return MemoryCommitApplication(config).run()


if __name__ == "__main__":
    raise SystemExit(main())
