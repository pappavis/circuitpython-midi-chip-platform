# Bestand: test_cli.py
# Versienommer: 0.2.0
# Doel: Toets die IDE-onafhanklike host-diagnose en startup-naspeurbaarheid.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: AUDIO-PRIORITY-AMENDMENT-001
# Actienr: MCP-ACT-AUDIO-AMEND-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001

from io import StringIO
from pathlib import Path
import tomllib

from midi_chip_platform.cli import CommandLineApplication
from midi_chip_platform.release import ReleaseMetadata


class TestCommandLineApplication:
    def test_runtime_version_matches_package_version(self) -> None:
        project_path = Path(__file__).parents[1] / "pyproject.toml"
        project_data = tomllib.loads(project_path.read_text(encoding="utf-8"))

        assert ReleaseMetadata().version == project_data["project"]["version"]

    def test_startup_reports_release_traceability(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("diagnose",))

        assert exit_code == 0
        assert output.getvalue().startswith(
            "circuitpython-midi-chip-platform v0.1.1 | "
            "story=AUDIO-PRIORITY-AMENDMENT-001 | release-date=2026-07-14\n"
        )

    def test_diagnose_reports_import_safe_skeleton(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("diagnose",))

        assert exit_code == 0
        assert "circuitpython-midi-chip-platform" in output.getvalue()
        assert "host skeleton ready" in output.getvalue()
        assert "hardware access: disabled" in output.getvalue()
