# Bestand: events.py
# Versienommer: 0.1.0
# Doel: Definieer draagbare MIDI-gebeurtenisse sonder backend-afhanklikheid.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002


class MidiEvent:
    __slots__ = ("_message_type", "_channel", "_note", "_velocity", "_value")

    def __init__(self, message_type, channel, note=None, velocity=None, value=None):
        self._validate_channel(channel)
        self._validate_optional_midi_value("note", note)
        self._validate_optional_midi_value("velocity", velocity)
        self._message_type = str(message_type)
        self._channel = int(channel)
        self._note = note
        self._velocity = velocity
        self._value = value

    @classmethod
    def note_on(cls, channel, note, velocity):
        return cls("note_on", channel, note=note, velocity=velocity)

    @classmethod
    def note_off(cls, channel, note, velocity=0):
        return cls("note_off", channel, note=note, velocity=velocity)

    @classmethod
    def control_change(cls, channel, control, value):
        cls._validate_optional_midi_value("control", control)
        cls._validate_optional_midi_value("value", value)
        return cls("control_change", channel, note=control, value=value)

    @classmethod
    def pitch_bend(cls, channel, value):
        if not 0 <= int(value) <= 16383:
            raise ValueError("pitch bend value must be between 0 and 16383")
        return cls("pitch_bend", channel, value=int(value))

    @property
    def message_type(self):
        return self._message_type

    @property
    def channel(self):
        return self._channel

    @property
    def note(self):
        return self._note

    @property
    def velocity(self):
        return self._velocity

    @property
    def value(self):
        return self._value

    @staticmethod
    def _validate_channel(channel):
        if not 1 <= int(channel) <= 16:
            raise ValueError("channel must be between 1 and 16")

    @staticmethod
    def _validate_optional_midi_value(label, value):
        if value is not None and not 0 <= int(value) <= 127:
            raise ValueError(f"{label} must be between 0 and 127")
