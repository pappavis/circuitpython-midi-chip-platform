# Bestand: code.py
# Versienommer: 0.17.6
# Doel: Start die Logic USB-MIDI fast-boot D1 na I2S runtime op die toestel.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-P0-REALTIME-BOOT-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-REALTIME-ANALYSE-001

from midi_chip_platform.configuration import CircuitPythonConfigurationFactory
from midi_chip_platform.device_runtime import DeviceImportSmokeCheck, DeviceRuntimeApplication
from midi_chip_platform.d1_runtime import D1UsbMidiI2sRuntimeFactory
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
                "midi_chip_platform.d1_runtime",
                "midi_chip_platform.events",
                "midi_chip_platform.i2s_audio",
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
        synth_runtime_factory=D1UsbMidiI2sRuntimeFactory(
            importer=__import__,
            output=print,
        ),
    ).run()
