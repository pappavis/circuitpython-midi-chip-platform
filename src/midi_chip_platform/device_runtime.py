# Bestand: device_runtime.py
# Versienommer: 0.1.0
# Doel: Lewer 'n minimale toestel-uitvoerbewys sonder MIDI-, klank- of netwerkstart.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

from midi_chip_platform.release import ReleaseMetadata


class DeviceRuntimeApplication:
    def __init__(self, release_metadata, output=None):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._release_metadata = release_metadata
        self._output = output if output is not None else print

    def run(self):
        self._output(self._release_metadata.banner())
        self._output("DEVICE_EXECUTION_STATUS=READY")
        return True
