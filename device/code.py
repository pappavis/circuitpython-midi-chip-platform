# Bestand: code.py
# Versienommer: 0.16.0
# Doel: Rapporteer toestelgereedheid en smoke-toets veilige D1-audio-afhanklikhede.
# Sprint: Sprint 3
# Epic: MCP-EPIC-007 DSP And Pedal Hardware
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-GREEN-008
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START

from midi_chip_platform.configuration import CircuitPythonConfigurationFactory
from midi_chip_platform.device_runtime import DeviceImportSmokeCheck, DeviceRuntimeApplication
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiDiagnosticFactory
from midi_chip_platform.platform_capabilities import CircuitPythonCapabilityFactory
from midi_chip_platform.release import ReleaseMetadata


if __name__ == "__main__":
    DeviceRuntimeApplication(
        release_metadata=ReleaseMetadata(),
        capability_discovery=CircuitPythonCapabilityFactory(__import__).create_discovery(),
        configuration_loader=CircuitPythonConfigurationFactory(__import__).create_loader(),
        import_smoke_check=DeviceImportSmokeCheck(
            importer=__import__,
            module_names=(
                "adafruit_midi",
                "adafruit_midi.control_change",
                "adafruit_midi.midi_continue",
                "adafruit_midi.note_off",
                "adafruit_midi.note_on",
                "adafruit_midi.pitch_bend",
                "adafruit_midi.start",
                "adafruit_midi.stop",
                "adafruit_midi.timing_clock",
                "midi_chip_platform.ble_midi",
                "midi_chip_platform.application",
                "midi_chip_platform.audio",
                "midi_chip_platform.configuration",
                "midi_chip_platform.core",
                "midi_chip_platform.d1_core",
                "midi_chip_platform.events",
                "midi_chip_platform.midi_performance",
                "midi_chip_platform.midi_semantics",
                "midi_chip_platform.midi_usb",
                "midi_chip_platform.ports",
                "midi_chip_platform.routing",
            ),
        ),
        midi_diagnostic_factory=CircuitPythonUsbMidiDiagnosticFactory(
            importer=__import__,
            output=print,
        ),
    ).run()
