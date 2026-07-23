# Bestand: test_device_runtime.py
# Versienommer: 0.20.1
# Doel: Spesifiseer toestel-uitvoer, dependency-bewys, MIDI-routing diagnostiek, synthio-baseline en D1 fast-boot runtime-start.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-080-INV-001 Locate First Disappearance Of NoteOn
# Actienr: MCP-ACT-080-INV-001-INSTRUMENT-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-INV-001

from midi_chip_platform.device_runtime import DeviceImportSmokeCheck, DeviceRuntimeApplication
from midi_chip_platform.release import ReleaseMetadata


class TestDeviceRuntimeApplication:
    class FakeImporter:
        def __init__(self):
            self.module_names = []

        def __call__(self, module_name):
            self.module_names.append(module_name)
            return object()

    class FakeSnapshot:
        def report_lines(self):
            return (
                "CAPABILITY_DISCOVERY_STATUS=PASS",
                "BOARD_ID=lolin_s2_mini",
            )

    class FakeDiscovery:
        def __init__(self):
            self.run_count = 0

        def discover(self):
            self.run_count += 1
            return TestDeviceRuntimeApplication.FakeSnapshot()

    class FakeConfigurationSnapshot:
        def __init__(self, values=None):
            self._values = dict(values or {})

        def get(self, key, default=None):
            return self._values.get(key, default)

        def report_lines(self):
            return (
                "CONFIGURATION_STATUS=PASS",
                "CONFIG_PRIVATE_WIFI_SSID=SET",
            )

    class FakeConfigurationLoader:
        def __init__(self, values=None):
            self._values = dict(values or {})

        def load(self):
            return TestDeviceRuntimeApplication.FakeConfigurationSnapshot(self._values)

    class FakeDiagnostic:
        def __init__(self):
            self.run_count = 0

        def run(self):
            self.run_count += 1
            return True

    class FakeDiagnosticFactory:
        def __init__(self, diagnostic):
            self._diagnostic = diagnostic
            self.configuration = None

        def create_if_enabled(self, configuration):
            self.configuration = configuration
            if not configuration.get("midi.diagnostic.enabled", False):
                return None
            return self._diagnostic

    class FakeRuntime:
        def __init__(self):
            self.run_count = 0

        def run(self):
            self.run_count += 1
            return True

    class FakeRuntimeFactory:
        def __init__(self, runtime, key="synth.d1.enabled"):
            self._runtime = runtime
            self._key = str(key)
            self.configuration = None

        def create_if_enabled(self, configuration):
            self.configuration = configuration
            if not configuration.get(self._key, False):
                return None
            return self._runtime

    def test_runtime_reports_execution_proof(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.2.0",
                user_story="MCP-US-003",
                release_date="2026-07-14",
            ),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.2.0 | "
            "story=MCP-US-003 | release-date=2026-07-14",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_device_import_smoke_proof_before_ready(self) -> None:
        output = []
        importer = self.FakeImporter()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.11.1",
                user_story="MCP-US-051-IMP-001",
                release_date="2026-07-15",
            ),
            import_smoke_check=DeviceImportSmokeCheck(
                importer=importer,
                module_names=(
                    "adafruit_midi",
                    "midi_chip_platform.routing",
                ),
            ),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert importer.module_names == [
            "adafruit_midi",
            "midi_chip_platform.routing",
        ]
        assert output == [
            "circuitpython-midi-chip-platform v0.11.1 | "
            "story=MCP-US-051-IMP-001 | release-date=2026-07-15",
            "DEVICE_IMPORT_STATUS=PASS",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_injected_board_capabilities(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.4.0",
                user_story="MCP-US-004",
                release_date="2026-07-14",
            ),
            capability_discovery=self.FakeDiscovery(),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.4.0 | "
            "story=MCP-US-004 | release-date=2026-07-14",
            "CAPABILITY_DISCOVERY_STATUS=PASS",
            "BOARD_ID=lolin_s2_mini",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_reports_only_redacted_configuration_state(self) -> None:
        output = []
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.5.0",
                user_story="MCP-US-005",
                release_date="2026-07-15",
            ),
            configuration_loader=self.FakeConfigurationLoader(),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert output == [
            "circuitpython-midi-chip-platform v0.5.0 | "
            "story=MCP-US-005 | release-date=2026-07-15",
            "CONFIGURATION_STATUS=PASS",
            "CONFIG_PRIVATE_WIFI_SSID=SET",
            "DEVICE_EXECUTION_STATUS=READY",
        ]

    def test_runtime_runs_midi_diagnostic_only_when_configuration_enables_it(self) -> None:
        output = []
        diagnostic = self.FakeDiagnostic()
        factory = self.FakeDiagnosticFactory(diagnostic)
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.12.0",
                user_story="MCP-US-007",
                release_date="2026-07-15",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {"midi.diagnostic.enabled": True}
            ),
            midi_diagnostic_factory=factory,
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert diagnostic.run_count == 1
        assert factory.configuration.get("midi.diagnostic.enabled") is True
        assert output[-1] == "DEVICE_EXECUTION_STATUS=READY"

    def test_runtime_starts_d1_synth_when_configuration_enables_it(self) -> None:
        output = []
        runtime = self.FakeRuntime()
        factory = self.FakeRuntimeFactory(runtime)
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.17.0",
                user_story="MCP-US-055",
                release_date="2026-07-16",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {"synth.d1.enabled": True}
            ),
            synth_runtime_factory=factory,
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert runtime.run_count == 1
        assert factory.configuration.get("synth.d1.enabled") is True
        assert output[-1] == "DEVICE_EXECUTION_STATUS=READY"

    def test_midi_diagnostic_takes_precedence_over_d1_runtime(self) -> None:
        output = []
        diagnostic = self.FakeDiagnostic()
        runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.17.0",
                user_story="MCP-US-055",
                release_date="2026-07-16",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {"midi.diagnostic.enabled": True, "synth.d1.enabled": True}
            ),
            midi_diagnostic_factory=self.FakeDiagnosticFactory(diagnostic),
            synth_runtime_factory=self.FakeRuntimeFactory(runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert diagnostic.run_count == 1
        assert runtime.run_count == 0

    def test_midi_routing_diagnostic_takes_precedence_over_synthio_and_d1(self) -> None:
        output = []
        routing_diagnostic = self.FakeRuntime()
        synthio_baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.20.1",
                user_story="MCP-US-080-INV-001",
                release_date="2026-07-23",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "midi.routing_diagnostic.enabled": True,
                    "synthio_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": False,
                }
            ),
            midi_routing_diagnostic_factory=self.FakeRuntimeFactory(
                routing_diagnostic,
                key="midi.routing_diagnostic.enabled",
            ),
            synthio_baseline_factory=self.FakeRuntimeFactory(
                synthio_baseline,
                key="synthio_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert routing_diagnostic.run_count == 1
        assert synthio_baseline.run_count == 0
        assert d1_runtime.run_count == 0

    def test_realtime_baseline_takes_precedence_over_d1_runtime(self) -> None:
        output = []
        baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.18.1",
                user_story="MCP-US-077",
                release_date="2026-07-17",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "realtime_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": False,
                }
            ),
            realtime_baseline_factory=self.FakeRuntimeFactory(
                baseline,
                key="realtime_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert baseline.run_count == 1
        assert d1_runtime.run_count == 0

    def test_synthio_baseline_takes_precedence_over_realtime_baseline_and_d1(self) -> None:
        output = []
        synthio_baseline = self.FakeRuntime()
        realtime_baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.19.0",
                user_story="MCP-US-079",
                release_date="2026-07-19",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "synthio_baseline.enabled": True,
                    "realtime_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": False,
                }
            ),
            synthio_baseline_factory=self.FakeRuntimeFactory(
                synthio_baseline,
                key="synthio_baseline.enabled",
            ),
            realtime_baseline_factory=self.FakeRuntimeFactory(
                realtime_baseline,
                key="realtime_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert synthio_baseline.run_count == 1
        assert realtime_baseline.run_count == 0
        assert d1_runtime.run_count == 0

    def test_fast_boot_starts_d1_before_capability_and_import_smoke(self) -> None:
        output = []
        runtime = self.FakeRuntime()
        factory = self.FakeRuntimeFactory(runtime)
        importer = self.FakeImporter()
        discovery = self.FakeDiscovery()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.17.8",
                user_story="MCP-US-055",
                release_date="2026-07-16",
            ),
            capability_discovery=discovery,
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": True,
                    "midi.diagnostic.enabled": False,
                }
            ),
            import_smoke_check=DeviceImportSmokeCheck(
                importer=importer,
                module_names=("slow.module",),
            ),
            synth_runtime_factory=factory,
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert runtime.run_count == 1
        assert discovery.run_count == 0
        assert importer.module_names == []
        assert output == [
            "circuitpython-midi-chip-platform v0.17.8 | "
            "story=MCP-US-055 | release-date=2026-07-16",
            "DEVICE_FAST_BOOT_STATUS=ENABLED",
        ]

    def test_fast_boot_starts_midi_routing_diagnostic_before_synthio_and_d1(
        self,
    ) -> None:
        output = []
        routing_diagnostic = self.FakeRuntime()
        synthio_baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.20.1",
                user_story="MCP-US-080-INV-001",
                release_date="2026-07-23",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "midi.routing_diagnostic.enabled": True,
                    "synthio_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": True,
                    "midi.diagnostic.enabled": False,
                }
            ),
            midi_routing_diagnostic_factory=self.FakeRuntimeFactory(
                routing_diagnostic,
                key="midi.routing_diagnostic.enabled",
            ),
            synthio_baseline_factory=self.FakeRuntimeFactory(
                synthio_baseline,
                key="synthio_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert routing_diagnostic.run_count == 1
        assert synthio_baseline.run_count == 0
        assert d1_runtime.run_count == 0
        assert output == [
            "circuitpython-midi-chip-platform v0.20.1 | "
            "story=MCP-US-080-INV-001 | release-date=2026-07-23",
            "DEVICE_FAST_BOOT_STATUS=ENABLED",
        ]

    def test_fast_boot_starts_realtime_baseline_before_d1(self) -> None:
        output = []
        baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.18.1",
                user_story="MCP-US-077",
                release_date="2026-07-17",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "realtime_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": True,
                    "midi.diagnostic.enabled": False,
                }
            ),
            realtime_baseline_factory=self.FakeRuntimeFactory(
                baseline,
                key="realtime_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert baseline.run_count == 1
        assert d1_runtime.run_count == 0
        assert output == [
            "circuitpython-midi-chip-platform v0.18.1 | "
            "story=MCP-US-077 | release-date=2026-07-17",
            "DEVICE_FAST_BOOT_STATUS=ENABLED",
        ]

    def test_fast_boot_starts_synthio_baseline_before_realtime_baseline_and_d1(
        self,
    ) -> None:
        output = []
        synthio_baseline = self.FakeRuntime()
        realtime_baseline = self.FakeRuntime()
        d1_runtime = self.FakeRuntime()
        application = DeviceRuntimeApplication(
            release_metadata=ReleaseMetadata(
                version="0.19.0",
                user_story="MCP-US-079",
                release_date="2026-07-19",
            ),
            configuration_loader=self.FakeConfigurationLoader(
                {
                    "synthio_baseline.enabled": True,
                    "realtime_baseline.enabled": True,
                    "synth.d1.enabled": True,
                    "synth.d1.fast_boot_mode": True,
                    "midi.diagnostic.enabled": False,
                }
            ),
            synthio_baseline_factory=self.FakeRuntimeFactory(
                synthio_baseline,
                key="synthio_baseline.enabled",
            ),
            realtime_baseline_factory=self.FakeRuntimeFactory(
                realtime_baseline,
                key="realtime_baseline.enabled",
            ),
            synth_runtime_factory=self.FakeRuntimeFactory(d1_runtime),
            output=output.append,
        )

        result = application.run()

        assert result is True
        assert synthio_baseline.run_count == 1
        assert realtime_baseline.run_count == 0
        assert d1_runtime.run_count == 0
        assert output == [
            "circuitpython-midi-chip-platform v0.19.0 | "
            "story=MCP-US-079 | release-date=2026-07-19",
            "DEVICE_FAST_BOOT_STATUS=ENABLED",
        ]
