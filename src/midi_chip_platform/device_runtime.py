# Bestand: device_runtime.py
# Versienommer: 0.3.0
# Doel: Lewer toestel-, capability- en geredigeerde konfigurasiebewys sonder diensstart.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005

from midi_chip_platform.release import ReleaseMetadata


class DeviceRuntimeApplication:
    def __init__(
        self,
        release_metadata,
        capability_discovery=None,
        configuration_loader=None,
        output=None,
    ):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._release_metadata = release_metadata
        self._capability_discovery = capability_discovery
        self._configuration_loader = configuration_loader
        self._output = output if output is not None else print

    def run(self):
        self._output(self._release_metadata.banner())
        if self._capability_discovery is not None:
            snapshot = self._capability_discovery.discover()
            for line in snapshot.report_lines():
                self._output(line)
        if self._configuration_loader is not None:
            configuration = self._configuration_loader.load()
            for line in configuration.report_lines():
                self._output(line)
        self._output("DEVICE_EXECUTION_STATUS=READY")
        return True
