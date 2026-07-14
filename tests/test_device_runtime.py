# Bestand: test_device_runtime.py
# Versienommer: 0.1.0
# Doel: Spesifiseer die toestel-uitvoerbewys sonder hardeware-newe-effekte.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-RED-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

from midi_chip_platform.device_runtime import DeviceRuntimeApplication
from midi_chip_platform.release import ReleaseMetadata


class TestDeviceRuntimeApplication:
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
