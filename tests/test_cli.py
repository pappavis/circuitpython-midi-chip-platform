# Bestand: test_cli.py
# Versienommer: 0.9.0
# Doel: Toets host-diagnose, HIL-CLI en gedeelde release-naspeurbaarheid.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-062 BLE MIDI Transport And Capability Gate
# Actienr: MCP-ACT-062-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-062

from io import StringIO
from pathlib import Path
import tomllib

from midi_chip_platform.cli import CommandLineApplication
from midi_chip_platform.release import ReleaseMetadata


class TestCommandLineApplication:
    class FakeVerifier:
        def __init__(self, passed):
            self._passed = passed

        def run(self):
            return self._passed

    class FakeVerifierFactory:
        def __init__(self, passed=True):
            self._passed = passed
            self.arguments = None

        def create(self, source_root, device_root, serial_port, output):
            self.arguments = (source_root, device_root, serial_port, output)
            return TestCommandLineApplication.FakeVerifier(self._passed)

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
            "circuitpython-midi-chip-platform v0.8.0 | "
            "story=MCP-US-062 | release-date=2026-07-15\n"
        )

    def test_diagnose_reports_import_safe_skeleton(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("diagnose",))

        assert exit_code == 0
        assert "circuitpython-midi-chip-platform" in output.getvalue()
        assert "host skeleton ready" in output.getvalue()
        assert "hardware access: disabled" in output.getvalue()

    def test_event_model_diagnose_reports_all_portable_event_families(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("events-diagnose",))

        assert exit_code == 0
        assert "EVENT_MODEL_STATUS=PASS" in output.getvalue()
        assert "NOTE_EVENT=note_on:channel=1:note=60:velocity=100" in output.getvalue()
        assert "CONTROL_EVENT=control_change:channel=1:control=1:value=64" in output.getvalue()
        assert "PITCH_BEND_EVENT=pitch_bend:channel=1:value=8192" in output.getvalue()
        assert "CLOCK_EVENT=timing_clock:channel=none" in output.getvalue()

    def test_ble_diagnose_reports_s2_as_unsupported_without_starting_radio(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("ble-diagnose", "--board-id", "lolin_s2_mini"))

        assert exit_code == 1
        assert "BLE_MIDI_STATUS=UNSUPPORTED" in output.getvalue()
        assert "reason=board_has_no_native_ble" in output.getvalue()

    def test_hil_verify_delegates_paths_without_echoing_them(self) -> None:
        output = StringIO()
        factory = self.FakeVerifierFactory()
        application = CommandLineApplication(output=output, hil_verifier_factory=factory)

        exit_code = application.run(
            (
                "hil-verify",
                "--source-root",
                "source-root",
                "--device-root",
                "device-root",
                "--serial-port",
                "private-port-id",
            )
        )

        assert exit_code == 0
        assert factory.arguments[:3] == ("source-root", "device-root", "private-port-id")
        assert "private-port-id" not in output.getvalue()
