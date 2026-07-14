# Bestand: hil.py
# Versienommer: 0.1.0
# Doel: Verifieer geredigeerde CircuitPython connection-, deploy-, boot- en execution-bewys.
# Sprint: Sprint 1
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-051 Hardware-In-The-Loop Test Runner
# Actienr: MCP-ACT-051-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051

import hashlib
from pathlib import Path
import time

from midi_chip_platform.release import ReleaseMetadata


class HilDeploymentManifest:
    def __init__(self, entries):
        normalized_entries = []
        for source_relative, device_relative in entries:
            normalized_entries.append((str(source_relative), str(device_relative)))
        if not normalized_entries:
            raise ValueError("HIL deployment manifest must contain at least one entry")
        self._entries = tuple(normalized_entries)

    @classmethod
    def default(cls):
        return cls(
            (
                ("device/boot.py", "boot.py"),
                ("device/code.py", "code.py"),
                ("src/midi_chip_platform/__init__.py", "lib/midi_chip_platform/__init__.py"),
                ("src/midi_chip_platform/release.py", "lib/midi_chip_platform/release.py"),
                ("src/midi_chip_platform/usb_boot.py", "lib/midi_chip_platform/usb_boot.py"),
                (
                    "src/midi_chip_platform/device_runtime.py",
                    "lib/midi_chip_platform/device_runtime.py",
                ),
            )
        )

    @property
    def entries(self):
        return self._entries


class HilCheckResult:
    def __init__(self, name, passed, evidence):
        self._name = str(name)
        self._passed = bool(passed)
        self._evidence = str(evidence)

    @property
    def passed(self):
        return self._passed

    def safe_line(self):
        status = "PASS" if self._passed else "FAIL"
        return f"{self._name}: {status} - {self._evidence}"


class PySerialConnectionFactory:
    def open(self, serial_port, baudrate, timeout):
        import serial

        return serial.Serial(serial_port, baudrate, timeout=timeout)


class SerialExecutionProbe:
    def __init__(
        self,
        serial_factory=None,
        sleeper=None,
        read_attempts=80,
        read_pause_seconds=0.05,
    ):
        self._serial_factory = (
            serial_factory if serial_factory is not None else PySerialConnectionFactory()
        )
        self._sleeper = sleeper if sleeper is not None else time
        self._read_attempts = int(read_attempts)
        self._read_pause_seconds = float(read_pause_seconds)

    def capture(self, serial_port):
        connection = self._serial_factory.open(serial_port, 115200, 0.1)
        try:
            self._sleeper.sleep(1.2)
            connection.write(b"\r\n")
            connection.flush()
            self._sleeper.sleep(0.2)
            connection.write(b"\x02")
            connection.flush()
            self._sleeper.sleep(0.2)
            connection.write(b"\x03\r\n")
            connection.flush()
            self._sleeper.sleep(0.4)
            connection.reset_input_buffer()
            connection.write(b"\x04")
            connection.flush()
            chunks = []
            for _ in range(self._read_attempts):
                chunk = connection.read(4096)
                if chunk:
                    chunks.append(chunk)
                    if b"DEVICE_EXECUTION_STATUS=READY" in b"".join(chunks):
                        break
                self._sleeper.sleep(self._read_pause_seconds)
            return b"".join(chunks).decode("utf-8", "replace")
        finally:
            connection.close()


class HardwareInLoopVerifier:
    def __init__(
        self,
        source_root,
        device_root,
        serial_port,
        manifest=None,
        serial_probe=None,
        output=None,
        release_metadata=None,
    ):
        self._source_root = Path(source_root)
        self._device_root = Path(device_root)
        self._serial_port = str(serial_port)
        self._manifest = manifest if manifest is not None else HilDeploymentManifest.default()
        self._serial_probe = serial_probe if serial_probe is not None else SerialExecutionProbe()
        self._output = output
        self._release_metadata = (
            release_metadata if release_metadata is not None else ReleaseMetadata()
        )

    def run(self):
        results = (
            self._verify_connection(),
            self._verify_deployment(),
            self._verify_boot(),
            self._verify_execution(),
        )
        self._write("DEVICE CONNECTION PROOF\n")
        for result in results:
            self._write(f"{result.safe_line()}\n")
        self._write("private-identifiers: REDACTED\n")
        return all(result.passed for result in results)

    def _verify_connection(self):
        passed = self._device_root.is_dir() and (self._device_root / "boot_out.txt").is_file()
        return HilCheckResult("connection", passed, "USB CDC + CIRCUITPY")

    def _verify_deployment(self):
        passed = True
        for source_relative, device_relative in self._manifest.entries:
            source_path = self._source_root / source_relative
            device_path = self._device_root / device_relative
            if not source_path.is_file() or not device_path.is_file():
                passed = False
                continue
            if self._digest(source_path) != self._digest(device_path):
                passed = False
        return HilCheckResult("deployment", passed, "approved manifest SHA-256 pairs")

    def _verify_boot(self):
        boot_output_path = self._device_root / "boot_out.txt"
        boot_output = ""
        if boot_output_path.is_file():
            boot_output = boot_output_path.read_text(encoding="utf-8", errors="replace")
        passed = (
            "BOOT_STATUS=PASS" in boot_output
            and self._release_metadata.banner() in boot_output
        )
        return HilCheckResult("boot", passed, "current release and USB-MIDI boot marker")

    def _verify_execution(self):
        capture = ""
        try:
            capture = self._serial_probe.capture(self._serial_port)
        except Exception:
            capture = ""
        passed = (
            "DEVICE_EXECUTION_STATUS=READY" in capture
            and self._release_metadata.banner() in capture
        )
        return HilCheckResult("execution", passed, "current release marker via serial REPL")

    def _digest(self, path):
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for block in iter(lambda: source.read(65536), b""):
                digest.update(block)
        return digest.hexdigest()

    def _write(self, text):
        if self._output is not None:
            self._output.write(text)


class HardwareInLoopVerifierFactory:
    def create(self, source_root, device_root, serial_port, output):
        return HardwareInLoopVerifier(
            source_root=source_root,
            device_root=device_root,
            serial_port=serial_port,
            output=output,
        )
