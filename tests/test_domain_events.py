# Bestand: test_domain_events.py
# Versienommer: 0.2.0
# Doel: Toets draagbare note-, control-, bend- en klokgebeurtenisse.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-006 Portable NoteEvent And ControlEvent Model
# Actienr: MCP-ACT-006-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-006

import pytest

from midi_chip_platform.events import ClockEvent, ControlEvent, MidiEvent, NoteEvent


class TestMidiEvent:
    def test_note_on_factory_preserves_channel_note_and_velocity(self) -> None:
        event = MidiEvent.note_on(channel=3, note=60, velocity=96)

        assert event.message_type == "note_on"
        assert event.channel == 3
        assert event.note == 60
        assert event.velocity == 96
        assert isinstance(event, NoteEvent)

    def test_channel_must_use_musician_facing_range(self) -> None:
        with pytest.raises(ValueError, match="channel"):
            MidiEvent.note_on(channel=0, note=60, velocity=96)

    def test_note_and_velocity_must_fit_midi_range(self) -> None:
        with pytest.raises(ValueError, match="note"):
            MidiEvent.note_on(channel=1, note=128, velocity=96)

        with pytest.raises(ValueError, match="velocity"):
            MidiEvent.note_on(channel=1, note=60, velocity=-1)


class TestNoteEvent:
    def test_explicit_note_off_preserves_release_velocity(self) -> None:
        event = NoteEvent.note_off(channel=16, note=127, velocity=32)

        assert event.message_type == "note_off"
        assert event.channel == 16
        assert event.note == 127
        assert event.velocity == 32
        assert event.is_note_on is False


class TestControlEvent:
    def test_control_change_uses_separate_controller_and_value(self) -> None:
        event = ControlEvent.control_change(channel=2, control=1, value=96)

        assert event.message_type == "control_change"
        assert event.channel == 2
        assert event.control == 1
        assert event.value == 96

    def test_pitch_bend_preserves_full_fourteen_bit_value(self) -> None:
        event = ControlEvent.pitch_bend(channel=4, value=16383)

        assert event.message_type == "pitch_bend"
        assert event.channel == 4
        assert event.value == 16383
        assert event.centered_value == 8191

    def test_control_and_pitch_bend_ranges_are_validated(self) -> None:
        with pytest.raises(ValueError, match="control"):
            ControlEvent.control_change(channel=1, control=128, value=0)

        with pytest.raises(ValueError, match="pitch bend"):
            ControlEvent.pitch_bend(channel=1, value=16384)


class TestClockEvent:
    @pytest.mark.parametrize(
        ("factory_name", "message_type"),
        (
            ("timing_clock", "timing_clock"),
            ("start", "start"),
            ("stop", "stop"),
            ("continue_playback", "continue"),
        ),
    )
    def test_system_realtime_events_are_channel_independent(
        self, factory_name, message_type
    ) -> None:
        event = getattr(ClockEvent, factory_name)()

        assert event.message_type == message_type
        assert event.channel is None
