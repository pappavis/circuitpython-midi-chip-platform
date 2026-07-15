# Bestand: test_device_runtime.py
# Versienommer: 0.3.0
# Doel: Spesifiseer toestel-uitvoer- en capability-bewys sonder diensaktivering.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-RED-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005

from midi_chip_platform.device_runtime import DeviceRuntimeApplication
from midi_chip_platform.release import ReleaseMetadata


class TestDeviceRuntimeApplication:
    class FakeSnapshot:
        def report_lines(self):
            return (
                "CAPABILITY_DISCOVERY_STATUS=PASS",
                "BOARD_ID=lolin_s2_mini",
            )

    class FakeDiscovery:
        def discover(self):
            return TestDeviceRuntimeApplication.FakeSnapshot()

    class FakeConfigurationSnapshot:
        def report_lines(self):
            return (
                "CONFIGURATION_STATUS=PASS",
                "CONFIG_PRIVATE_WIFI_SSID=SET",
            )

    class FakeConfigurationLoader:
        def load(self):
            return TestDeviceRuntimeApplication.FakeConfigurationSnapshot()

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
