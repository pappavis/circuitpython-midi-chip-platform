# Bestand: code.py
# Versienommer: 0.1.0
# Doel: Bewys veilige toesteluitvoering sonder om MIDI-, klank- of netwerkdienste te begin.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-GREEN-005
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

from midi_chip_platform.device_runtime import DeviceRuntimeApplication
from midi_chip_platform.release import ReleaseMetadata


if __name__ == "__main__":
    DeviceRuntimeApplication(release_metadata=ReleaseMetadata()).run()
