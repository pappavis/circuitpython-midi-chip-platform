# Bestand: device_runtime.py
# Versienommer: 0.12.0
# Doel: Lewer toestelbewys en aktiveer begrensde USB-MIDI-diagnostiek slegs via konfigurasie.
# Sprint: Sprint 2
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-007 USB MIDI Receive Loop
# Actienr: MCP-ACT-007-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007

from midi_chip_platform.release import ReleaseMetadata


class DeviceImportSmokeCheck:
    def __init__(self, importer, module_names):
        normalized_names = tuple(str(module_name) for module_name in module_names)
        if not normalized_names:
            raise ValueError("device import smoke check requires module names")
        self._importer = importer
        self._module_names = normalized_names

    def run(self):
        for module_name in self._module_names:
            self._importer(module_name)
        return True


class DeviceRuntimeApplication:
    def __init__(
        self,
        release_metadata,
        capability_discovery=None,
        configuration_loader=None,
        import_smoke_check=None,
        midi_diagnostic_factory=None,
        output=None,
    ):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._release_metadata = release_metadata
        self._capability_discovery = capability_discovery
        self._configuration_loader = configuration_loader
        self._import_smoke_check = import_smoke_check
        self._midi_diagnostic_factory = midi_diagnostic_factory
        self._output = output if output is not None else print

    def run(self):
        configuration = None
        self._output(self._release_metadata.banner())
        if self._capability_discovery is not None:
            snapshot = self._capability_discovery.discover()
            for line in snapshot.report_lines():
                self._output(line)
        if self._configuration_loader is not None:
            configuration = self._configuration_loader.load()
            for line in configuration.report_lines():
                self._output(line)
        if self._import_smoke_check is not None:
            self._import_smoke_check.run()
            self._output("DEVICE_IMPORT_STATUS=PASS")
        self._output("DEVICE_EXECUTION_STATUS=READY")
        if self._midi_diagnostic_factory is not None and configuration is not None:
            diagnostic = self._midi_diagnostic_factory.create_if_enabled(configuration)
            if diagnostic is not None:
                return bool(diagnostic.run())
        return True
