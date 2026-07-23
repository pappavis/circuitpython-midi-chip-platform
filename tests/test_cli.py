# Bestand: test_cli.py
# Versienommer: 0.21.0
# Doel: Toets hostdiagnose, HIL-diagnostics release en release-naspeurbaarheid.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: HIL-DIAGNOSTIC-FRAMEWORK-001 Layered HIL Diagnostic Framework
# Actienr: MCP-ACT-HIL-DIAGNOSTIC-FRAMEWORK-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / HIL-DIAGNOSTIC-FRAMEWORK-001

from io import StringIO
from pathlib import Path
import tomllib

from midi_chip_platform.cli import CommandLineApplication
from midi_chip_platform.release import ReleaseMetadata


class TestCommandLineApplication:
    class FakeDeployer:
        def __init__(self, passed):
            self._passed = passed

        def deploy(self):
            return self._passed

    class FakeDeployerFactory:
        def __init__(self, passed=True):
            self._passed = passed
            self.arguments = None

        def create(self, source_root, device_root, serial_port, output):
            self.arguments = (source_root, device_root, serial_port, output)
            return TestCommandLineApplication.FakeDeployer(self._passed)

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

    class FakeResetProbe:
        def __init__(self):
            self.received_port = None

        def reset(self, serial_port):
            self.received_port = serial_port

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
            "circuitpython-midi-chip-platform v0.21.0 | "
            "story=HIL-DIAGNOSTIC-FRAMEWORK-001 | release-date=2026-07-24\n"
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
        assert (
            "CONTROL_EVENT=control_change:channel=1:control=1:value=64"
            in output.getvalue()
        )
        assert "PITCH_BEND_EVENT=pitch_bend:channel=1:value=8192" in output.getvalue()
        assert "CLOCK_EVENT=timing_clock:channel=none" in output.getvalue()

    def test_d1_diagnose_reports_three_waveforms_and_note_off_silence(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(
            (
                "d1-diagnose",
                "--note",
                "69",
                "--velocity",
                "100",
                "--sample-rate",
                "16000",
                "--frames-per-block",
                "64",
            )
        )

        result = output.getvalue()
        assert exit_code == 0
        assert "D1_WAVEFORM=sine;frames=64" in result
        assert "D1_WAVEFORM=saw;frames=64" in result
        assert "D1_WAVEFORM=square;frames=64" in result
        assert "D1_CORE_STATUS=PASS;note=69;frequency_hz=440.000000" in result

    def test_audio_safety_diagnose_proves_startup_mute_and_bounded_gain(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(
            (
                "audio-safety-diagnose",
                "--master-gain",
                "0.08",
                "--input-peak",
                "12000",
            )
        )

        result = output.getvalue()
        assert exit_code == 0
        assert "AUDIO_OUTPUT_LOAD=speaker-4-8-ohm" in result
        assert "AUDIO_STARTUP_MUTED=true" in result
        assert "AUDIO_SAFETY_MUTED_PEAK=0" in result
        assert "AUDIO_SAFETY_UNMUTED_PEAK=960" in result
        assert "AUDIO_SAFETY_STATUS=PASS" in result

    def test_ble_diagnose_reports_s2_as_unsupported_without_starting_radio(
        self,
    ) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(("ble-diagnose", "--board-id", "lolin_s2_mini"))

        assert exit_code == 1
        assert "BLE_MIDI_STATUS=UNSUPPORTED" in output.getvalue()
        assert "reason=board_has_no_native_ble" in output.getvalue()

    def test_performance_diagnose_reports_normalized_bend_and_cc1(self) -> None:
        output = StringIO()
        application = CommandLineApplication(output=output)

        exit_code = application.run(
            (
                "performance-diagnose",
                "--channel",
                "4",
                "--pitch-bend",
                "12288",
                "--modulation",
                "127",
                "--pitch-bend-range",
                "2",
            )
        )

        assert exit_code == 0
        assert "MIDI_PERFORMANCE_STATUS=PASS" in output.getvalue()
        assert "CHANNEL=4" in output.getvalue()
        assert "PITCH_BEND_SEMITONES=1.000000" in output.getvalue()
        assert "CC1_NORMALIZED=1.000000" in output.getvalue()

    def test_hil_verify_delegates_paths_without_echoing_them(self) -> None:
        output = StringIO()
        factory = self.FakeVerifierFactory()
        application = CommandLineApplication(
            output=output, hil_verifier_factory=factory
        )

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
        assert factory.arguments[:3] == (
            "source-root",
            "device-root",
            "private-port-id",
        )
        assert "private-port-id" not in output.getvalue()

    def test_hil_deploy_delegates_paths_without_echoing_them(self) -> None:
        output = StringIO()
        factory = self.FakeDeployerFactory()
        application = CommandLineApplication(
            output=output, hil_deployer_factory=factory
        )

        exit_code = application.run(
            (
                "hil-deploy",
                "--source-root",
                "source-root",
                "--device-root",
                "private-device-root",
                "--serial-port",
                "private-port-id",
            )
        )

        assert exit_code == 0
        assert factory.arguments[:3] == (
            "source-root",
            "private-device-root",
            "private-port-id",
        )
        assert "private-device-root" not in output.getvalue()
        assert "private-port-id" not in output.getvalue()

    def test_hil_reset_uses_serial_without_echoing_private_port(self) -> None:
        output = StringIO()
        reset_probe = self.FakeResetProbe()
        application = CommandLineApplication(output=output, hil_reset_probe=reset_probe)

        exit_code = application.run(("hil-reset", "--serial-port", "private-port-id"))

        assert exit_code == 0
        assert reset_probe.received_port == "private-port-id"
        assert "HIL_RESET_STATUS=REQUESTED" in output.getvalue()
        assert "private-port-id" not in output.getvalue()
