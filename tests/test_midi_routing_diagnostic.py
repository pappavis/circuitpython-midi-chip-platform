# Bestand: test_midi_routing_diagnostic.py
# Versienommer: 0.20.0
# Doel: Spesifiseer USB-MIDI routing diagnose sonder audio as P0 latency-isolasie.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-080 USB MIDI Endpoint Routing Diagnostic
# Actienr: MCP-ACT-080-RED-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-START

from midi_chip_platform.events import ControlEvent, NoteEvent
from midi_chip_platform.midi_routing_diagnostic import (
    MidiRoutingDiagnosticFactory,
    MidiRoutingDiagnosticProfile,
    MidiRoutingDiagnosticRuntime,
)
from midi_chip_platform.testing import MemoryConfiguration, MemoryMidiInput


class TestMidiRoutingDiagnosticRuntime:
    class ManualTime:
        def __init__(self):
            self._seconds = 0.0

        def monotonic(self):
            return self._seconds

        def sleep(self, seconds):
            self._seconds += float(seconds)

    def test_profile_defaults_target_midi_only_routing_measurement(self) -> None:
        profile = MidiRoutingDiagnosticProfile()

        assert profile.max_events == 16
        assert profile.timeout_seconds == 60.0
        assert profile.idle_sleep_seconds == 0.001
        assert profile.event_logging == "summary"
        assert profile.heartbeat_seconds == 2.0
        assert profile.scan_all_midi_ports is True
        assert profile.midi_port_count == 1

    def test_runtime_logs_note_events_without_audio_path(self) -> None:
        output = []
        clock = self.ManualTime()
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=69, velocity=99),
                NoteEvent.note_off(channel=1, note=69, velocity=64),
                ControlEvent.control_change(channel=1, control=1, value=127),
            )
        )
        runtime = MidiRoutingDiagnosticRuntime(
            midi_input=midi_input,
            profile=MidiRoutingDiagnosticProfile(
                max_events=3,
                timeout_seconds=1.0,
                idle_sleep_seconds=0.001,
                event_logging="summary",
                heartbeat_seconds=0.0,
                scan_all_midi_ports=True,
                midi_port_count=2,
            ),
            output=output.append,
            monotonic=clock.monotonic,
            sleeper=clock.sleep,
        )

        result = runtime.run()

        assert result is True
        assert midi_input.is_open is False
        assert output[0] == (
            "MIDI_ROUTING_DIAGNOSTIC_STATUS=START;"
            "scan_all_ports=true;port_count=2;max_events=3;"
            "timeout_seconds=1;heartbeat_seconds=0"
        )
        assert "MIDI_ROUTING_DIAGNOSTIC_READY;ready_ms=0" in output
        assert (
            "MIDI_ROUTING_EVENT=note_on;channel=1;note=69;velocity=99;event_ms=0"
            in output
        )
        assert (
            "MIDI_ROUTING_EVENT=note_off;channel=1;note=69;velocity=64;event_ms=0"
            in output
        )
        assert "MIDI_ROUTING_EVENT=control_change;channel=1;control=1;value=127;event_ms=0" in output
        assert output[-1] == (
            "MIDI_ROUTING_DIAGNOSTIC_STATUS=PASS;events=3;note_on=1;"
            "note_off=1;control=1;clock=0;ignored=0"
        )

    def test_runtime_heartbeats_when_no_midi_arrives(self) -> None:
        output = []
        clock = self.ManualTime()
        runtime = MidiRoutingDiagnosticRuntime(
            midi_input=MemoryMidiInput(()),
            profile=MidiRoutingDiagnosticProfile(
                max_events=1,
                timeout_seconds=0.003,
                idle_sleep_seconds=0.001,
                event_logging="summary",
                heartbeat_seconds=0.001,
            ),
            output=output.append,
            monotonic=clock.monotonic,
            sleeper=clock.sleep,
        )

        result = runtime.run()

        assert result is False
        assert any(line.startswith("MIDI_ROUTING_HEARTBEAT") for line in output)
        assert output[-1] == (
            "MIDI_ROUTING_DIAGNOSTIC_STATUS=TIMEOUT;events=0;note_on=0;"
            "note_off=0;control=0;clock=0;ignored=0"
        )


class TestMidiRoutingDiagnosticFactory:
    class FakeMidi:
        def __init__(self, midi_in=None, in_channel=None):
            self.midi_in = midi_in
            self.in_channel = in_channel

        def receive(self):
            return None

    class ModuleStub:
        def __init__(self, **attributes):
            for name, value in attributes.items():
                setattr(self, name, value)

    class ManualTime:
        def __init__(self):
            self._seconds = 0.0

        def monotonic(self):
            return self._seconds

        def sleep(self, seconds):
            self._seconds += float(seconds)

    class FakeImporter:
        def __init__(self):
            self.time = TestMidiRoutingDiagnosticFactory.ManualTime()

        def __call__(self, module_name, *args):
            if module_name == "adafruit_midi":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    MIDI=TestMidiRoutingDiagnosticFactory.FakeMidi
                )
            if module_name == "usb_midi":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    ports=(object(), object())
                )
            if module_name == "adafruit_midi.note_on":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    NoteOn=type("NoteOn", (), {})
                )
            if module_name == "adafruit_midi.note_off":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    NoteOff=type("NoteOff", (), {})
                )
            if module_name == "adafruit_midi.control_change":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    ControlChange=type("ControlChange", (), {})
                )
            if module_name == "adafruit_midi.pitch_bend":
                return TestMidiRoutingDiagnosticFactory.ModuleStub(
                    PitchBend=type("PitchBend", (), {})
                )
            if module_name == "time":
                return self.time
            raise ImportError(module_name)

    def test_factory_is_disabled_by_default(self) -> None:
        runtime = MidiRoutingDiagnosticFactory().create_if_enabled(
            MemoryConfiguration({})
        )

        assert runtime is None

    def test_factory_creates_multi_port_runtime_when_enabled(self) -> None:
        output = []
        runtime = MidiRoutingDiagnosticFactory(
            importer=self.FakeImporter(),
            output=output.append,
        ).create_if_enabled(
            MemoryConfiguration(
                {
                    "midi.routing_diagnostic.enabled": True,
                    "midi.routing_diagnostic.scan_all_ports": True,
                    "midi.routing_diagnostic.max_events": 1,
                    "midi.routing_diagnostic.timeout_seconds": 0.002,
                    "midi.routing_diagnostic.idle_sleep_seconds": 0.001,
                    "midi.routing_diagnostic.event_logging": "summary",
                    "midi.routing_diagnostic.heartbeat_seconds": 0.0,
                }
            )
        )

        assert runtime is not None
        assert runtime.run() is False
        assert any("port_count=2" in line for line in output)
