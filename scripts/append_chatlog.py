#!/usr/bin/env python3
"""
File: scripts/append_chatlog.py
Version: 0.2.0
Purpose: Append traceable Copilot/Codex/agent notes to project chatlog.

Sprint: Sprint 0
Epic: Governance / Continuity
User Story: CHATLOG-AUTO-APPEND
Action ID: CHATLOG-001
ChatID: K9R2M7P4
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class ChatLogEntry:
    trace_id: str
    source: str
    user_request: str
    assistant_output: str
    timestamp_utc: str


@dataclass
class ChatLogConfig:
    repo_root: Path
    chatlog_file: Path


class ChatLogWriter:
    def __init__(self, config: ChatLogConfig) -> None:
        self.config = config

    def append(self, entry: ChatLogEntry) -> None:
        self.config.chatlog_file.parent.mkdir(parents=True, exist_ok=True)
        text = self.format_entry(entry)

        with self.config.chatlog_file.open("a", encoding="utf-8") as handle:
            handle.write(text)

    def format_entry(self, entry: ChatLogEntry) -> str:
        return f"""
## Chat Entry - {entry.timestamp_utc}

- Trace ID: `{entry.trace_id}`
- Source: `{entry.source}`

### User Request

{entry.user_request}

### Assistant / Agent Output

{entry.assistant_output}
"""


class ArgumentParserFactory:
    def build(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Append a traceable markdown entry to the project chat log."
        )
        parser.add_argument("--trace-id", required=True)
        parser.add_argument("--source", default="copilot-chat")
        parser.add_argument("--user-request", required=True)
        parser.add_argument("--assistant-output", required=True)
        parser.add_argument(
            "--chatlog-file",
            default="docs/chatlog_copilot_codex.md",
        )
        return parser


class ConfigFactory:
    def from_args(self, args: argparse.Namespace) -> tuple[ChatLogConfig, ChatLogEntry]:
        repo_root = Path(__file__).resolve().parents[1]
        chatlog_file = repo_root / args.chatlog_file

        config = ChatLogConfig(
            repo_root=repo_root,
            chatlog_file=chatlog_file,
        )

        entry = ChatLogEntry(
            trace_id=args.trace_id,
            source=args.source,
            user_request=args.user_request,
            assistant_output=args.assistant_output,
            timestamp_utc=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
        )

        return config, entry


class ChatLogApplication:
    def run(self) -> int:
        parser = ArgumentParserFactory().build()
        args = parser.parse_args()
        config, entry = ConfigFactory().from_args(args)
        ChatLogWriter(config).append(entry)
        print(f"[CHATLOG] Appended trace {entry.trace_id} to {config.chatlog_file}")
        return 0


def main() -> int:
    return ChatLogApplication().run()


if __name__ == "__main__":
    raise SystemExit(main())
