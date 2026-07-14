# Bestand: test_cli.py
# Versienommer: 0.1.0
# Doel: Toets die IDE-onafhanklike host-diagnose-entrypoint.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-RED-005
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

from io import StringIO

from midi_chip_platform.cli import CommandLineApplication


class TestCommandLineApplication:
    def test_diagnose_reports_import_safe_skeleton(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("diagnose",))

        assert exit_code == 0
        assert "circuitpython-midi-chip-platform" in output.getvalue()
        assert "host skeleton ready" in output.getvalue()
        assert "hardware access: disabled" in output.getvalue()
