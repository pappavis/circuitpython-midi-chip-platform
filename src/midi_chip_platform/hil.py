# Bestand: hil.py
# Versienommer: 0.21.0
# Doel: Verifieer dependency-closed deploy met MIDI-routing diagnose, synthio-baseline en HIL-diagnostics.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: HIL-DIAGNOSTIC-FRAMEWORK-001 Layered HIL Diagnostic Framework
# Actienr: MCP-ACT-HIL-DIAGNOSTIC-FRAMEWORK-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / HIL-DIAGNOSTIC-FRAMEWORK-001

import ast
import hashlib
from pathlib import Path
import shutil
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
                ("device/i2s_test.py", "i2s_test.py"),
                ("src/midi_chip_platform/__init__.py", "lib/midi_chip_platform/__init__.py"),
                ("src/midi_chip_platform/release.py", "lib/midi_chip_platform/release.py"),
                ("src/midi_chip_platform/usb_boot.py", "lib/midi_chip_platform/usb_boot.py"),
                (
                    "src/midi_chip_platform/device_runtime.py",
                    "lib/midi_chip_platform/device_runtime.py",
                ),
                (
                    "src/midi_chip_platform/platform_capabilities.py",
                    "lib/midi_chip_platform/platform_capabilities.py",
                ),
                (
                    "src/midi_chip_platform/configuration.py",
                    "lib/midi_chip_platform/configuration.py",
                ),
                (
                    "src/midi_chip_platform/ports.py",
                    "lib/midi_chip_platform/ports.py",
                ),
                (
                    "src/midi_chip_platform/audio.py",
                    "lib/midi_chip_platform/audio.py",
                ),
                (
                    "src/midi_chip_platform/d1_core.py",
                    "lib/midi_chip_platform/d1_core.py",
                ),
                (
                    "src/midi_chip_platform/d1_runtime.py",
                    "lib/midi_chip_platform/d1_runtime.py",
                ),
                (
                    "src/midi_chip_platform/i2s_audio.py",
                    "lib/midi_chip_platform/i2s_audio.py",
                ),
                (
                    "src/midi_chip_platform/realtime_baseline.py",
                    "lib/midi_chip_platform/realtime_baseline.py",
                ),
                (
                    "src/midi_chip_platform/synthio_runtime.py",
                    "lib/midi_chip_platform/synthio_runtime.py",
                ),
                (
                    "src/midi_chip_platform/core.py",
                    "lib/midi_chip_platform/core.py",
                ),
                (
                    "src/midi_chip_platform/events.py",
                    "lib/midi_chip_platform/events.py",
                ),
                (
                    "src/midi_chip_platform/midi_usb.py",
                    "lib/midi_chip_platform/midi_usb.py",
                ),
                (
                    "src/midi_chip_platform/midi_routing_diagnostic.py",
                    "lib/midi_chip_platform/midi_routing_diagnostic.py",
                ),
                (
                    "src/midi_chip_platform/ble_midi.py",
                    "lib/midi_chip_platform/ble_midi.py",
                ),
                (
                    "src/midi_chip_platform/routing.py",
                    "lib/midi_chip_platform/routing.py",
                ),
                (
                    "src/midi_chip_platform/midi_semantics.py",
                    "lib/midi_chip_platform/midi_semantics.py",
                ),
                (
                    "src/midi_chip_platform/midi_performance.py",
                    "lib/midi_chip_platform/midi_performance.py",
                ),
                (
                    "src/midi_chip_platform/hil_diagnostics.py",
                    "lib/midi_chip_platform/hil_diagnostics.py",
                ),
            )
        )

    @property
    def entries(self):
        return self._entries


class DeploymentDependencyInspector:
    def __init__(self, package_name="midi_chip_platform"):
        self._package_name = str(package_name)

    def find_missing(self, source_root, manifest):
        root = Path(source_root)
        deployed_sources = {source_relative for source_relative, _ in manifest.entries}
        missing = set()
        for source_relative, _ in manifest.entries:
            source_path = root / source_relative
            if not self._is_package_source(source_relative) or not source_path.is_file():
                continue
            syntax_tree = ast.parse(
                source_path.read_text(encoding="utf-8"),
                filename=str(source_path),
            )
            for module_name in self._internal_imports(syntax_tree):
                required_source = self._source_relative(root, module_name)
                if required_source is not None and required_source not in deployed_sources:
                    missing.add((source_relative, required_source))
        return tuple(sorted(missing))

    def _is_package_source(self, source_relative):
        prefix = f"src/{self._package_name}/"
        return str(source_relative).startswith(prefix) and str(source_relative).endswith(
            ".py"
        )

    def _internal_imports(self, syntax_tree):
        module_names = set()
        package_prefix = f"{self._package_name}."
        for node in ast.walk(syntax_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == self._package_name or alias.name.startswith(
                        package_prefix
                    ):
                        module_names.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                if node.module == self._package_name or node.module.startswith(
                    package_prefix
                ):
                    module_names.add(node.module)
        return tuple(sorted(module_names))

    def _source_relative(self, source_root, module_name):
        module_path = module_name.replace(".", "/")
        source_candidate = Path("src") / f"{module_path}.py"
        if (source_root / source_candidate).is_file():
            return source_candidate.as_posix()
        package_candidate = Path("src") / module_path / "__init__.py"
        if (source_root / package_candidate).is_file():
            return package_candidate.as_posix()
        return source_candidate.as_posix()


class CircuitPythonLibraryManifest:
    def __init__(self, entries):
        normalized_entries = []
        for library_name, candidate_paths in entries:
            paths = tuple(str(path) for path in candidate_paths)
            if not paths:
                raise ValueError("CircuitPython library requires a device path")
            normalized_entries.append((str(library_name), paths))
        if not normalized_entries:
            raise ValueError("CircuitPython library manifest must not be empty")
        self._entries = tuple(normalized_entries)

    @classmethod
    def default(cls):
        return cls(
            (
                (
                    "adafruit_midi",
                    (
                        "lib/adafruit_midi",
                        "lib/adafruit_midi.py",
                        "lib/adafruit_midi.mpy",
                    ),
                ),
            )
        )

    @property
    def library_names(self):
        return tuple(library_name for library_name, _ in self._entries)

    def find_missing(self, device_root):
        root = Path(device_root)
        missing = []
        for library_name, candidate_paths in self._entries:
            if not any((root / candidate_path).exists() for candidate_path in candidate_paths):
                missing.append(library_name)
        return tuple(missing)


class HardwareInLoopDeployer:
    def __init__(
        self,
        source_root,
        device_root,
        manifest=None,
        dependency_inspector=None,
        serial_port=None,
        autoreload_controller=None,
        output=None,
    ):
        self._source_root = Path(source_root)
        self._device_root = Path(device_root)
        self._manifest = manifest if manifest is not None else HilDeploymentManifest.default()
        self._dependency_inspector = (
            dependency_inspector
            if dependency_inspector is not None
            else DeploymentDependencyInspector()
        )
        self._serial_port = None if serial_port is None else str(serial_port)
        self._autoreload_controller = (
            autoreload_controller
            if autoreload_controller is not None
            else SerialAutoreloadController()
        )
        self._output = output

    def deploy(self):
        missing_sources = tuple(
            source_relative
            for source_relative, _ in self._manifest.entries
            if not (self._source_root / source_relative).is_file()
        )
        if missing_sources:
            self._write(
                "HIL_DEPLOY_STATUS=FAIL;reason=missing-source;"
                f"files={len(missing_sources)}\n"
            )
            return False
        missing_dependencies = self._dependency_inspector.find_missing(
            source_root=self._source_root,
            manifest=self._manifest,
        )
        if missing_dependencies:
            self._write(
                "HIL_DEPLOY_STATUS=FAIL;reason=manifest-open;"
                f"edges={len(missing_dependencies)}\n"
            )
            return False
        if not self._device_root.is_dir():
            self._write("HIL_DEPLOY_STATUS=FAIL;reason=device-unavailable\n")
            return False
        session = None
        copied = False
        recovered = True
        failure_reason = "autoreload-open"
        try:
            if self._serial_port is not None:
                session = self._autoreload_controller.open(self._serial_port)
                failure_reason = "autoreload-disable"
                session.disable()
            failure_reason = "copy"
            for source_relative, device_relative in self._manifest.entries:
                source_path = self._source_root / source_relative
                device_path = self._device_root / device_relative
                device_path.parent.mkdir(parents=True, exist_ok=True)
                temporary_path = device_path.with_name(
                    f"__mcp_deploy_{device_path.name}.tmp"
                )
                shutil.copyfile(source_path, temporary_path)
                temporary_path.replace(device_path)
            copied = True
        except Exception:
            copied = False
        finally:
            if session is not None:
                try:
                    session.enable()
                except Exception:
                    recovered = False
                finally:
                    session.close()
        if not copied:
            self._write(f"HIL_DEPLOY_STATUS=FAIL;reason={failure_reason}\n")
            return False
        if not recovered:
            self._write("HIL_DEPLOY_STATUS=FAIL;reason=autoreload-recovery\n")
            return False
        self._write(f"HIL_DEPLOY_STATUS=PASS;files={len(self._manifest.entries)}\n")
        self._write("private-identifiers: REDACTED\n")
        return True

    def _write(self, text):
        if self._output is not None:
            self._output.write(text)


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


class SerialHardResetProbe:
    def __init__(self, serial_factory=None, sleeper=None):
        self._serial_factory = (
            serial_factory if serial_factory is not None else PySerialConnectionFactory()
        )
        self._sleeper = sleeper if sleeper is not None else time

    def reset(self, serial_port):
        connection = self._serial_factory.open(serial_port, 115200, 0.1)
        try:
            connection.write(b"\x03\x03\r\n")
            connection.flush()
            self._sleeper.sleep(0.5)
            connection.write(b"import microcontroller; microcontroller.reset()\r\n")
            connection.flush()
            self._sleeper.sleep(0.5)
        finally:
            connection.close()


class SerialAutoreloadSession:
    def __init__(self, connection, sleeper=None, read_attempts=60):
        self._connection = connection
        self._sleeper = sleeper if sleeper is not None else time
        self._read_attempts = int(read_attempts)

    def disable(self):
        self._connection.write(b"\r\n")
        self._connection.flush()
        self._sleeper.sleep(0.2)
        self._connection.write(b"\x02")
        self._connection.flush()
        self._sleeper.sleep(0.2)
        self._connection.write(b"\x03\r\n")
        self._connection.flush()
        self._sleeper.sleep(0.5)
        self._connection.reset_input_buffer()
        self._connection.write(
            b"import supervisor; supervisor.runtime.autoreload = False; "
            b"print('HIL_AUTORELOAD_STATUS=DISABLED')\r\n"
        )
        self._connection.flush()
        self._require_marker("HIL_AUTORELOAD_STATUS=DISABLED")

    def enable(self):
        self._connection.write(
            b"print('HIL_AUTORELOAD_STATUS=ENABLED'); "
            b"supervisor.runtime.autoreload = True\r\n"
        )
        self._connection.flush()
        self._require_marker("HIL_AUTORELOAD_STATUS=ENABLED")

    def close(self):
        self._connection.close()

    def _require_marker(self, marker):
        captured = bytearray()
        encoded_marker = marker.encode("ascii")
        for _ in range(self._read_attempts):
            chunk = self._connection.read(4096)
            if chunk:
                captured.extend(chunk)
                if encoded_marker in captured:
                    return
            self._sleeper.sleep(0.05)
        raise RuntimeError("CircuitPython autoreload marker was not received")


class SerialAutoreloadController:
    def __init__(self, serial_factory=None, sleeper=None):
        self._serial_factory = (
            serial_factory if serial_factory is not None else PySerialConnectionFactory()
        )
        self._sleeper = sleeper if sleeper is not None else time

    def open(self, serial_port):
        connection = self._serial_factory.open(serial_port, 115200, 0.1)
        return SerialAutoreloadSession(connection=connection, sleeper=self._sleeper)


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
                    captured = b"".join(chunks)
                    if (
                        b"DEVICE_EXECUTION_STATUS=READY" in captured
                        or b"D1_RUNTIME_READY" in captured
                        or b"REALTIME_BASELINE_READY" in captured
                    ):
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
        dependency_inspector=None,
        library_manifest=None,
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
        self._dependency_inspector = (
            dependency_inspector
            if dependency_inspector is not None
            else DeploymentDependencyInspector()
        )
        self._library_manifest = (
            library_manifest
            if library_manifest is not None
            else CircuitPythonLibraryManifest.default()
        )

    def run(self):
        results = (
            self._verify_connection(),
            self._verify_manifest_closure(),
            self._verify_deployment(),
            self._verify_device_libraries(),
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

    def _verify_manifest_closure(self):
        try:
            missing = self._dependency_inspector.find_missing(
                source_root=self._source_root,
                manifest=self._manifest,
            )
        except (OSError, SyntaxError):
            missing = (("unreadable", "dependency"),)
        evidence = "all internal imports are deployed"
        if missing:
            evidence = f"{len(missing)} internal import edge(s) missing"
        return HilCheckResult("manifest-closure", not missing, evidence)

    def _verify_device_libraries(self):
        missing = self._library_manifest.find_missing(self._device_root)
        evidence = "required CircuitPython libraries present"
        if missing:
            evidence = f"missing: {','.join(missing)}"
        return HilCheckResult("device-libraries", not missing, evidence)

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
        import_smoke_passed = (
            "DEVICE_EXECUTION_STATUS=READY" in capture
            and "DEVICE_IMPORT_STATUS=PASS" in capture
            and self._release_metadata.banner() in capture
        )
        fast_boot_passed = (
            "DEVICE_FAST_BOOT_STATUS=ENABLED" in capture
            and "D1_MIDI_INPUT_STATUS=OPEN" in capture
            and "D1_RUNTIME_READY" in capture
            and self._release_metadata.banner() in capture
        )
        realtime_baseline_passed = (
            "DEVICE_FAST_BOOT_STATUS=ENABLED" in capture
            and "REALTIME_BASELINE_MIDI_INPUT_STATUS=OPEN" in capture
            and "REALTIME_BASELINE_READY" in capture
            and self._release_metadata.banner() in capture
        )
        synthio_baseline_passed = (
            "DEVICE_FAST_BOOT_STATUS=ENABLED" in capture
            and "SYNTHIO_BASELINE_MIDI_INPUT_STATUS=OPEN" in capture
            and "SYNTHIO_BASELINE_READY" in capture
            and self._release_metadata.banner() in capture
        )
        midi_routing_passed = (
            "DEVICE_FAST_BOOT_STATUS=ENABLED" in capture
            and "MIDI_ROUTING_DIAGNOSTIC_INPUT_STATUS=OPEN" in capture
            and "MIDI_ROUTING_DIAGNOSTIC_READY" in capture
            and self._release_metadata.banner() in capture
        )
        passed = (
            import_smoke_passed
            or fast_boot_passed
            or realtime_baseline_passed
            or synthio_baseline_passed
            or midi_routing_passed
        )
        evidence = "current release and dependency-import markers via serial REPL"
        if fast_boot_passed:
            evidence = "current release and D1 fast-boot runtime markers via serial REPL"
        if realtime_baseline_passed:
            evidence = "current release and realtime-baseline markers via serial REPL"
        if synthio_baseline_passed:
            evidence = "current release and synthio-baseline markers via serial REPL"
        if midi_routing_passed:
            evidence = "current release and MIDI-routing diagnostic markers via serial REPL"
        return HilCheckResult(
            "execution",
            passed,
            evidence,
        )

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


class HardwareInLoopDeployerFactory:
    def create(self, source_root, device_root, serial_port, output):
        return HardwareInLoopDeployer(
            source_root=source_root,
            device_root=device_root,
            serial_port=serial_port,
            output=output,
        )
