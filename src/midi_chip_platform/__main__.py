# Bestand: __main__.py
# Versienommer: 0.1.0
# Doel: Delegeer python -m startup na die klasgebaseerde host-CLI.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-008
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

from midi_chip_platform.cli import CommandLineApplication


if __name__ == "__main__":
    raise SystemExit(CommandLineApplication().run())
