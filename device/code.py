# Bestand: code.py
# Versienommer: 0.3.0
# Doel: Rapporteer veilige toestelvermoens en geredigeerde konfigurasie sonder diensstart.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005

from midi_chip_platform.configuration import CircuitPythonConfigurationFactory
from midi_chip_platform.device_runtime import DeviceRuntimeApplication
from midi_chip_platform.platform_capabilities import CircuitPythonCapabilityFactory
from midi_chip_platform.release import ReleaseMetadata


if __name__ == "__main__":
    DeviceRuntimeApplication(
        release_metadata=ReleaseMetadata(),
        capability_discovery=CircuitPythonCapabilityFactory(__import__).create_discovery(),
        configuration_loader=CircuitPythonConfigurationFactory(__import__).create_loader(),
    ).run()
