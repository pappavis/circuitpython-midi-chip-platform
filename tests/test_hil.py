# Bestand: test_hil.py
# Versienommer: 0.16.0
# Doel: Spesifiseer deploy-, execution- en veilige-audio releasebewys.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-RED-006
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START

from io import StringIO
from pathlib import Path

from midi_chip_platform.hil import (
    CircuitPythonLibraryManifest,
    DeploymentDependencyInspector,
    HardwareInLoopDeployer,
    HardwareInLoopVerifier,
    HilDeploymentManifest,
    SerialHardResetProbe,
    SerialExecutionProbe,
    SerialAutoreloadSession,
)


class TestHilDeploymentManifest:
    def test_default_manifest_contains_minimal_device_release(self) -> None:
        manifest = HilDeploymentManifest.default()

        assert len(manifest.entries) == 19
        assert ("device/boot.py", "boot.py") in manifest.entries
        assert ("device/i2s_test.py", "i2s_test.py") in manifest.entries
        assert (
            "src/midi_chip_platform/d1_core.py",
            "lib/midi_chip_platform/d1_core.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/device_runtime.py",
            "lib/midi_chip_platform/device_runtime.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/platform_capabilities.py",
            "lib/midi_chip_platform/platform_capabilities.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/configuration.py",
            "lib/midi_chip_platform/configuration.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/ports.py",
            "lib/midi_chip_platform/ports.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/audio.py",
            "lib/midi_chip_platform/audio.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/core.py",
            "lib/midi_chip_platform/core.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/events.py",
            "lib/midi_chip_platform/events.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/midi_usb.py",
            "lib/midi_chip_platform/midi_usb.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/ble_midi.py",
            "lib/midi_chip_platform/ble_midi.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/routing.py",
            "lib/midi_chip_platform/routing.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/midi_semantics.py",
            "lib/midi_chip_platform/midi_semantics.py",
        ) in manifest.entries
        assert (
            "src/midi_chip_platform/midi_performance.py",
            "lib/midi_chip_platform/midi_performance.py",
        ) in manifest.entries

    def test_default_manifest_is_closed_over_internal_imports(self) -> None:
        source_root = Path(__file__).resolve().parents[1]

        missing = DeploymentDependencyInspector().find_missing(
            source_root=source_root,
            manifest=HilDeploymentManifest.default(),
        )

        assert missing == ()

    def test_inspector_reports_removed_internal_dependency(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        entries = tuple(
            entry
            for entry in HilDeploymentManifest.default().entries
            if entry[0] != "src/midi_chip_platform/ports.py"
        )

        missing = DeploymentDependencyInspector().find_missing(
            source_root=source_root,
            manifest=HilDeploymentManifest(entries),
        )

        assert (
            "src/midi_chip_platform/configuration.py",
            "src/midi_chip_platform/ports.py",
        ) in missing


class TestCircuitPythonLibraryManifest:
    def test_requirements_file_matches_default_device_libraries(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        requirement_lines = tuple(
            line.strip()
            for line in (source_root / "device" / "requirements.txt")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )

        assert requirement_lines == CircuitPythonLibraryManifest.default().library_names

    def test_missing_device_library_is_reported(self, tmp_path) -> None:
        missing = CircuitPythonLibraryManifest.default().find_missing(tmp_path)

        assert missing == ("adafruit_midi",)

    def test_directory_device_library_satisfies_manifest(self, tmp_path) -> None:
        (tmp_path / "lib" / "adafruit_midi").mkdir(parents=True)

        missing = CircuitPythonLibraryManifest.default().find_missing(tmp_path)

        assert missing == ()


class TestHardwareInLoopDeployer:
    class FakeAutoreloadSession:
        def __init__(self):
            self.calls = []

        def disable(self):
            self.calls.append("disable")

        def enable(self):
            self.calls.append("enable")

        def close(self):
            self.calls.append("close")

    class FakeAutoreloadController:
        def __init__(self, session):
            self._session = session
            self.received_port = None

        def open(self, serial_port):
            self.received_port = serial_port
            return self._session

    def test_deploy_copies_manifest_and_preserves_unrelated_files(
        self, tmp_path
    ) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest(
            (
                ("device/boot.py", "boot.py"),
                ("device/code.py", "code.py"),
            )
        )
        (source_root / "device").mkdir(parents=True)
        (source_root / "device" / "boot.py").write_text("boot", encoding="utf-8")
        (source_root / "device" / "code.py").write_text("code", encoding="utf-8")
        device_root.mkdir()
        (device_root / "keep.txt").write_text("preserve", encoding="utf-8")
        output = StringIO()

        deployed = HardwareInLoopDeployer(
            source_root=source_root,
            device_root=device_root,
            manifest=manifest,
            output=output,
        ).deploy()

        assert deployed is True
        assert (device_root / "boot.py").read_text(encoding="utf-8") == "boot"
        assert (device_root / "code.py").read_text(encoding="utf-8") == "code"
        assert (device_root / "keep.txt").read_text(encoding="utf-8") == "preserve"
        assert "HIL_DEPLOY_STATUS=PASS;files=2" in output.getvalue()
        assert str(device_root) not in output.getvalue()

    def test_deploy_refuses_missing_source_without_partial_copy(self, tmp_path) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest(
            (
                ("device/boot.py", "boot.py"),
                ("device/code.py", "code.py"),
            )
        )
        (source_root / "device").mkdir(parents=True)
        (source_root / "device" / "boot.py").write_text("boot", encoding="utf-8")
        device_root.mkdir()
        output = StringIO()

        deployed = HardwareInLoopDeployer(
            source_root=source_root,
            device_root=device_root,
            manifest=manifest,
            output=output,
        ).deploy()

        assert deployed is False
        assert not (device_root / "boot.py").exists()
        assert (
            "HIL_DEPLOY_STATUS=FAIL;reason=missing-source;files=1" in output.getvalue()
        )

    def test_deploy_refuses_manifest_with_missing_internal_import(
        self, tmp_path
    ) -> None:
        source_root = Path(__file__).resolve().parents[1]
        device_root = tmp_path / "device"
        device_root.mkdir()
        entries = tuple(
            entry
            for entry in HilDeploymentManifest.default().entries
            if entry[0] != "src/midi_chip_platform/ports.py"
        )
        output = StringIO()

        deployed = HardwareInLoopDeployer(
            source_root=source_root,
            device_root=device_root,
            manifest=HilDeploymentManifest(entries),
            output=output,
        ).deploy()

        assert deployed is False
        assert "HIL_DEPLOY_STATUS=FAIL;reason=manifest-open" in output.getvalue()

    def test_deploy_suspends_and_restores_autoreload(self, tmp_path) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest((("device/code.py", "code.py"),))
        (source_root / "device").mkdir(parents=True)
        (source_root / "device" / "code.py").write_text("code", encoding="utf-8")
        device_root.mkdir()
        session = self.FakeAutoreloadSession()
        controller = self.FakeAutoreloadController(session)

        deployed = HardwareInLoopDeployer(
            source_root=source_root,
            device_root=device_root,
            manifest=manifest,
            serial_port="private-port-id",
            autoreload_controller=controller,
        ).deploy()

        assert deployed is True
        assert controller.received_port == "private-port-id"
        assert session.calls == ["disable", "enable", "close"]


class TestSerialAutoreloadSession:
    class FakeConnection:
        def __init__(self):
            self.writes = []
            self._reads = [b"HIL_AUTORELOAD_STATUS=DISABLED\n"]

        def write(self, payload):
            self.writes.append(payload)

        def flush(self):
            return None

        def reset_input_buffer(self):
            return None

        def read(self, _size):
            if not self._reads:
                return b""
            return self._reads.pop(0)

        def close(self):
            return None

    class NoWaitSleeper:
        def sleep(self, _seconds):
            return None

    def test_disable_enters_normal_repl_before_setting_autoreload(self) -> None:
        connection = self.FakeConnection()
        session = SerialAutoreloadSession(
            connection=connection,
            sleeper=self.NoWaitSleeper(),
        )

        session.disable()

        assert connection.writes[:3] == [b"\r\n", b"\x02", b"\x03\r\n"]
        assert b"supervisor.runtime.autoreload = False" in connection.writes[3]


class TestHardwareInLoopVerifier:
    class FakeSerialProbe:
        def __init__(self, capture):
            self._capture = capture
            self.received_port = None

        def capture(self, serial_port):
            self.received_port = serial_port
            return self._capture

    def test_all_three_proof_levels_pass_without_publishing_paths(
        self, tmp_path
    ) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest.default()
        for source_relative, device_relative in manifest.entries:
            source_path = source_root / source_relative
            device_path = device_root / device_relative
            source_path.parent.mkdir(parents=True, exist_ok=True)
            device_path.parent.mkdir(parents=True, exist_ok=True)
            source_path.write_bytes(source_relative.encode("ascii"))
            device_path.write_bytes(source_relative.encode("ascii"))
        (device_root / "lib" / "adafruit_midi").mkdir(parents=True)
        (device_root / "boot_out.txt").write_text(
            "Board ID:lolin_s2_mini\n"
            "circuitpython-midi-chip-platform v0.16.0 | story=MCP-US-075 | "
            "release-date=2026-07-16\n"
            "BOOT_STATUS=PASS\n",
            encoding="utf-8",
        )
        output = StringIO()
        serial_probe = self.FakeSerialProbe(
            "circuitpython-midi-chip-platform v0.16.0 | story=MCP-US-075 | "
            "release-date=2026-07-16\nDEVICE_IMPORT_STATUS=PASS\n"
            "DEVICE_EXECUTION_STATUS=READY"
        )
        verifier = HardwareInLoopVerifier(
            source_root=source_root,
            device_root=device_root,
            serial_port="private-port-id",
            manifest=manifest,
            serial_probe=serial_probe,
            output=output,
        )

        assert verifier.run() is True
        assert serial_probe.received_port == "private-port-id"
        assert "connection: PASS" in output.getvalue()
        assert "deployment: PASS" in output.getvalue()
        assert "device-libraries: PASS" in output.getvalue()
        assert "execution: PASS" in output.getvalue()
        assert "private-port-id" not in output.getvalue()

    def test_hash_mismatch_fails_deployment_proof(self, tmp_path) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest((("device/boot.py", "boot.py"),))
        (source_root / "device").mkdir(parents=True)
        device_root.mkdir(parents=True)
        (source_root / "device" / "boot.py").write_bytes(b"approved")
        (device_root / "boot.py").write_bytes(b"different")
        (device_root / "boot_out.txt").write_text(
            "circuitpython-midi-chip-platform v0.4.0 | story=MCP-US-004 | "
            "release-date=2026-07-14\nBOOT_STATUS=PASS",
            encoding="utf-8",
        )
        verifier = HardwareInLoopVerifier(
            source_root=source_root,
            device_root=device_root,
            serial_port="redacted",
            manifest=manifest,
            serial_probe=self.FakeSerialProbe(
                "circuitpython-midi-chip-platform v0.4.0 | story=MCP-US-004 | "
                "release-date=2026-07-14\nDEVICE_EXECUTION_STATUS=READY"
            ),
            output=StringIO(),
        )

        assert verifier.run() is False

    def test_execution_without_import_marker_fails(self, tmp_path) -> None:
        source_root = tmp_path / "source"
        device_root = tmp_path / "device"
        manifest = HilDeploymentManifest((("device/boot.py", "boot.py"),))
        (source_root / "device").mkdir(parents=True)
        device_root.mkdir(parents=True)
        (source_root / "device" / "boot.py").write_bytes(b"approved")
        (device_root / "boot.py").write_bytes(b"approved")
        (device_root / "lib" / "adafruit_midi").mkdir(parents=True)
        (device_root / "boot_out.txt").write_text(
            "circuitpython-midi-chip-platform v0.16.0 | story=MCP-US-075 | "
            "release-date=2026-07-16\nBOOT_STATUS=PASS",
            encoding="utf-8",
        )
        verifier = HardwareInLoopVerifier(
            source_root=source_root,
            device_root=device_root,
            serial_port="redacted",
            manifest=manifest,
            serial_probe=self.FakeSerialProbe(
                "circuitpython-midi-chip-platform v0.16.0 | story=MCP-US-075 | "
                "release-date=2026-07-16\nDEVICE_EXECUTION_STATUS=READY"
            ),
            output=StringIO(),
        )

        assert verifier.run() is False


class TestSerialExecutionProbe:
    class FakeConnection:
        def __init__(self):
            self.writes = []
            self.closed = False
            self._reads = [b"", b"DEVICE_EXECUTION_STATUS=READY\n"]

        def write(self, payload):
            self.writes.append(payload)

        def flush(self):
            return None

        def reset_input_buffer(self):
            return None

        def read(self, size):
            if self._reads:
                return self._reads.pop(0)
            return b""

        def close(self):
            self.closed = True

    class FakeFactory:
        def __init__(self, connection):
            self._connection = connection
            self.received_port = None

        def open(self, serial_port, baudrate, timeout):
            self.received_port = serial_port
            assert baudrate == 115200
            assert timeout == 0.1
            return self._connection

    class NoSleep:
        def sleep(self, seconds):
            return None

    def test_probe_reloads_code_and_closes_connection(self) -> None:
        connection = self.FakeConnection()
        factory = self.FakeFactory(connection)
        probe = SerialExecutionProbe(
            serial_factory=factory,
            sleeper=self.NoSleep(),
            read_attempts=3,
        )

        capture = probe.capture("private-port-id")

        assert "DEVICE_EXECUTION_STATUS=READY" in capture
        assert b"\x04" in connection.writes
        assert connection.closed is True


class TestSerialHardResetProbe:
    class FakeConnection:
        def __init__(self):
            self.writes = []
            self.closed = False

        def write(self, payload):
            self.writes.append(payload)

        def flush(self):
            return None

        def close(self):
            self.closed = True

    class FakeFactory:
        def __init__(self, connection):
            self._connection = connection

        def open(self, serial_port, baudrate, timeout):
            assert serial_port == "private-port-id"
            assert baudrate == 115200
            assert timeout == 0.1
            return self._connection

    class NoSleep:
        def sleep(self, seconds):
            return None

    def test_probe_interrupts_repl_and_requests_hard_reset(self) -> None:
        connection = self.FakeConnection()
        probe = SerialHardResetProbe(
            serial_factory=self.FakeFactory(connection),
            sleeper=self.NoSleep(),
        )

        probe.reset("private-port-id")

        assert b"\x03\x03\r\n" in connection.writes
        assert (
            b"import microcontroller; microcontroller.reset()\r\n" in connection.writes
        )
        assert connection.closed is True
