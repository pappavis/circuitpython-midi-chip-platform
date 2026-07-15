# Bestand: events.py
# Versienommer: 0.2.0
# Doel: Definieer draagbare note-, control-, pitch-bend- en klokgebeurtenisse.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-006 Portable NoteEvent And ControlEvent Model
# Actienr: MCP-ACT-006-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-006


class MidiEvent:
    __slots__ = ("_message_type", "_channel")

    def __init__(self, message_type, channel=None):
        if channel is not None:
            self._validate_channel(channel)
            channel = int(channel)
        self._message_type = str(message_type)
        self._channel = channel

    @classmethod
    def note_on(cls, channel, note, velocity):
        return NoteEvent.note_on(channel, note, velocity)

    @classmethod
    def note_off(cls, channel, note, velocity=0):
        return NoteEvent.note_off(channel, note, velocity)

    @classmethod
    def control_change(cls, channel, control, value):
        return ControlEvent.control_change(channel, control, value)

    @classmethod
    def pitch_bend(cls, channel, value):
        return ControlEvent.pitch_bend(channel, value)

    @classmethod
    def timing_clock(cls):
        return ClockEvent.timing_clock()

    @classmethod
    def start(cls):
        return ClockEvent.start()

    @classmethod
    def stop(cls):
        return ClockEvent.stop()

    @classmethod
    def continue_playback(cls):
        return ClockEvent.continue_playback()

    @property
    def message_type(self):
        return self._message_type

    @property
    def channel(self):
        return self._channel

    @property
    def note(self):
        return None

    @property
    def velocity(self):
        return None

    @property
    def control(self):
        return None

    @property
    def value(self):
        return None

    @staticmethod
    def _validate_channel(channel):
        if not 1 <= int(channel) <= 16:
            raise ValueError("channel must be between 1 and 16")

    @staticmethod
    def _validate_midi_value(label, value):
        if not 0 <= int(value) <= 127:
            raise ValueError(f"{label} must be between 0 and 127")


class NoteEvent(MidiEvent):
    __slots__ = ("_note", "_velocity")

    def __init__(self, message_type, channel, note, velocity):
        if message_type not in ("note_on", "note_off"):
            raise ValueError("note message type must be note_on or note_off")
        self._validate_midi_value("note", note)
        self._validate_midi_value("velocity", velocity)
        super().__init__(message_type, channel)
        self._note = int(note)
        self._velocity = int(velocity)

    @classmethod
    def note_on(cls, channel, note, velocity):
        return cls("note_on", channel, note, velocity)

    @classmethod
    def note_off(cls, channel, note, velocity=0):
        return cls("note_off", channel, note, velocity)

    @property
    def note(self):
        return self._note

    @property
    def velocity(self):
        return self._velocity

    @property
    def is_note_on(self):
        return self._message_type == "note_on"


class ControlEvent(MidiEvent):
    __slots__ = ("_control", "_value")

    def __init__(self, message_type, channel, value, control=None):
        if message_type == "control_change":
            self._validate_midi_value("control", control)
            self._validate_midi_value("value", value)
        elif message_type == "pitch_bend":
            if not 0 <= int(value) <= 16383:
                raise ValueError("pitch bend value must be between 0 and 16383")
        else:
            raise ValueError("control message type must be control_change or pitch_bend")
        super().__init__(message_type, channel)
        self._control = None if control is None else int(control)
        self._value = int(value)

    @classmethod
    def control_change(cls, channel, control, value):
        return cls("control_change", channel, value=value, control=control)

    @classmethod
    def pitch_bend(cls, channel, value):
        return cls("pitch_bend", channel, value=value)

    @property
    def control(self):
        return self._control

    @property
    def value(self):
        return self._value

    @property
    def centered_value(self):
        if self._message_type != "pitch_bend":
            return None
        return self._value - 8192


class ClockEvent(MidiEvent):
    __slots__ = ()

    def __init__(self, message_type):
        if message_type not in ("timing_clock", "start", "stop", "continue"):
            raise ValueError("unsupported clock message type")
        super().__init__(message_type, channel=None)

    @classmethod
    def timing_clock(cls):
        return cls("timing_clock")

    @classmethod
    def start(cls):
        return cls("start")

    @classmethod
    def stop(cls):
        return cls("stop")

    @classmethod
    def continue_playback(cls):
        return cls("continue")
