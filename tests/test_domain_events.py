# Bestand: test_domain_events.py
# Versienommer: 0.1.0
# Doel: Toets die draagbare MIDI-gebeurteniskontrak.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

import pytest

from midi_chip_platform.events import MidiEvent


class TestMidiEvent:
    def test_note_on_factory_preserves_channel_note_and_velocity(self) -> None:
        event = MidiEvent.note_on(channel=3, note=60, velocity=96)

        assert event.message_type == "note_on"
        assert event.channel == 3
        assert event.note == 60
        assert event.velocity == 96

    def test_channel_must_use_musician_facing_range(self) -> None:
        with pytest.raises(ValueError, match="channel"):
            MidiEvent.note_on(channel=0, note=60, velocity=96)

    def test_note_and_velocity_must_fit_midi_range(self) -> None:
        with pytest.raises(ValueError, match="note"):
            MidiEvent.note_on(channel=1, note=128, velocity=96)

        with pytest.raises(ValueError, match="velocity"):
            MidiEvent.note_on(channel=1, note=60, velocity=-1)
