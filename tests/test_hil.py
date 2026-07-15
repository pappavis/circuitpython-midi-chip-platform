# Bestand: test_hil.py
# Versienommer: 0.7.0
# Doel: Spesifiseer geredigeerde connection-, deploy-, boot- en execution-HIL-bewys.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-008 MIDI Channel Router
# Actienr: MCP-ACT-008-RED-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-008

from io import StringIO

from midi_chip_platform.hil import (
    HardwareInLoopVerifier,
    HilDeploymentManifest,
    SerialExecutionProbe,
)


class TestHilDeploymentManifest:
    def test_default_manifest_contains_minimal_device_release(self) -> None:
        manifest = HilDeploymentManifest.default()

        assert len(manifest.entries) == 12
        assert ("device/boot.py", "boot.py") in manifest.entries
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


class TestHardwareInLoopVerifier:
    class FakeSerialProbe:
        def __init__(self, capture):
            self._capture = capture
            self.received_port = None

        def capture(self, serial_port):
            self.received_port = serial_port
            return self._capture

    def test_all_three_proof_levels_pass_without_publishing_paths(self, tmp_path) -> None:
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
        (device_root / "boot_out.txt").write_text(
            "Board ID:lolin_s2_mini\n"
            "circuitpython-midi-chip-platform v0.9.0 | story=MCP-US-008 | "
            "release-date=2026-07-15\n"
            "BOOT_STATUS=PASS\n",
            encoding="utf-8",
        )
        output = StringIO()
        serial_probe = self.FakeSerialProbe(
            "circuitpython-midi-chip-platform v0.9.0 | story=MCP-US-008 | "
            "release-date=2026-07-15\nDEVICE_EXECUTION_STATUS=READY"
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
