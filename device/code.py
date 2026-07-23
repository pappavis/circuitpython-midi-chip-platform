# Bestand: code.py
# Versienommer: 0.20.0
# Doel: Start MIDI-routing diagnose, synthio-baseline, realtime MIDI-audio baseline of D1 runtime op die toestel.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-080 USB MIDI Endpoint Routing Diagnostic
# Actienr: MCP-ACT-080-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-START

from midi_chip_platform.configuration import CircuitPythonConfigurationFactory
from midi_chip_platform.device_runtime import DeviceImportSmokeCheck, DeviceRuntimeApplication
from midi_chip_platform.d1_runtime import D1UsbMidiI2sRuntimeFactory
from midi_chip_platform.midi_routing_diagnostic import MidiRoutingDiagnosticFactory
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiDiagnosticFactory
from midi_chip_platform.platform_capabilities import CircuitPythonCapabilityFactory
from midi_chip_platform.realtime_baseline import RealtimeMidiAudioBaselineFactory
from midi_chip_platform.release import ReleaseMetadata
from midi_chip_platform.synthio_runtime import SynthioBaselineRuntimeFactory


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
                "midi_chip_platform.midi_routing_diagnostic",
                "midi_chip_platform.midi_semantics",
                "midi_chip_platform.midi_usb",
                "midi_chip_platform.ports",
                "midi_chip_platform.realtime_baseline",
                "midi_chip_platform.routing",
                "midi_chip_platform.synthio_runtime",
            ),
        ),
        midi_diagnostic_factory=CircuitPythonUsbMidiDiagnosticFactory(
            importer=__import__,
            output=print,
        ),
        midi_routing_diagnostic_factory=MidiRoutingDiagnosticFactory(
            importer=__import__,
            output=print,
        ),
        realtime_baseline_factory=RealtimeMidiAudioBaselineFactory(
            importer=__import__,
            output=print,
        ),
        synthio_baseline_factory=SynthioBaselineRuntimeFactory(
            importer=__import__,
            output=print,
        ),
        synth_runtime_factory=D1UsbMidiI2sRuntimeFactory(
            importer=__import__,
            output=print,
        ),
    ).run()
