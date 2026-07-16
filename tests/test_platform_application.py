# Bestand: test_platform_application.py
# Versienommer: 0.16.0
# Doel: Toets dependency injection, deurlopende blokaudio en veilige mute-lifecycle.
# Sprint: Sprint 2
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START

from midi_chip_platform.audio import AudioStreamFormat
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
        audio_format = AudioStreamFormat()
        audio_output = MemoryAudioOutput(audio_format)
        clock = ManualClock()
        configuration = MemoryConfiguration({"audio.channel": "stereo"})
        registry = CoreRegistry()
        core = RecordingSynthCore("d1-test", audio_format)
        registry.register(channel=3, core=core)
        application = PlatformApplication(
            midi_input, audio_output, clock, configuration, registry
        )

        application.start()
        assert audio_output.is_muted is False
        processed = application.step()
        application.stop()

        assert processed is True
        assert core.events == (event,)
        assert len(audio_output.blocks) == 1
        assert audio_output.blocks[0].samples == (0,)
        assert clock.tick_count == 1
        assert midi_input.is_open is False
        assert audio_output.is_open is False
        assert audio_output.is_muted is True

    def test_application_can_be_constructed_without_starting_dependencies(self) -> None:
        midi_input = MemoryMidiInput()
        audio_output = MemoryAudioOutput(AudioStreamFormat())
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

    def test_application_keeps_rendering_active_core_without_new_midi_event(
        self,
    ) -> None:
        event = MidiEvent.note_on(channel=1, note=60, velocity=100)
        midi_input = MemoryMidiInput((event,))
        audio_format = AudioStreamFormat(frames_per_block=4)
        audio_output = MemoryAudioOutput(audio_format)
        registry = CoreRegistry()
        core = RecordingSynthCore("d1-test", audio_format)
        registry.register(channel=1, core=core)
        application = PlatformApplication(
            midi_input,
            audio_output,
            ManualClock(),
            MemoryConfiguration(),
            registry,
        )

        application.start()
        assert application.step() is True
        assert application.step() is True
        application.stop()

        assert len(audio_output.blocks) == 2
        assert core.render_count == 2
