# Bestand: test_platform_application.py
# Versienommer: 0.1.0
# Doel: Toets dependency injection en die minimale platform-lifecycle.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-RED-004
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

from midi_chip_platform.application import PlatformApplication
from midi_chip_platform.core import CoreRegistry
from midi_chip_platform.events import MidiEvent
from midi_chip_platform.testing import (
    ManualClock,
    MemoryAudioOutput,
    MemoryConfiguration,
    MemoryMidiInput,
    RecordingSynthCore,
)


class TestPlatformApplication:
    def test_application_routes_one_event_through_injected_instances(self) -> None:
        event = MidiEvent.note_on(channel=3, note=60, velocity=100)
        midi_input = MemoryMidiInput((event,))
        audio_output = MemoryAudioOutput()
        clock = ManualClock()
        configuration = MemoryConfiguration({"audio.channel": "stereo"})
        registry = CoreRegistry()
        core = RecordingSynthCore("sn76489-test")
        registry.register(channel=3, core=core)
        application = PlatformApplication(midi_input, audio_output, clock, configuration, registry)

        application.start()
        processed = application.step()
        application.stop()

        assert processed is True
        assert core.events == (event,)
        assert audio_output.frames == ((0.0, 0.0),)
        assert clock.tick_count == 1
        assert midi_input.is_open is False
        assert audio_output.is_open is False

    def test_application_can_be_constructed_without_starting_dependencies(self) -> None:
        midi_input = MemoryMidiInput()
        audio_output = MemoryAudioOutput()
        application = PlatformApplication(
            midi_input,
            audio_output,
            ManualClock(),
            MemoryConfiguration(),
            CoreRegistry(),
        )

        assert application.is_started is False
        assert midi_input.is_open is False
        assert audio_output.is_open is False
