# Bestand: testing.py
# Versienommer: 0.1.0
# Doel: Verskaf host-fakes vir kontraktoetse sonder fisiese hardeware.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-006
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

from midi_chip_platform.core import SynthCore
from midi_chip_platform.ports import AudioOutputPort, ClockPort, ConfigurationPort, MidiInputPort


class MemoryMidiInput(MidiInputPort):
    def __init__(self, events=()):
        self._events = list(events)
        self._is_open = False

    @property
    def is_open(self):
        return self._is_open

    def open(self):
        self._is_open = True

    def receive(self):
        if not self._is_open:
            raise RuntimeError("MIDI input is closed")
        if not self._events:
            return None
        return self._events.pop(0)

    def close(self):
        self._is_open = False


class MemoryAudioOutput(AudioOutputPort):
    def __init__(self):
        self._frames = []
        self._is_open = False

    @property
    def frames(self):
        return tuple(self._frames)

    @property
    def is_open(self):
        return self._is_open

    def open(self):
        self._is_open = True

    def write(self, frame):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        self._frames.append(frame)

    def close(self):
        self._is_open = False


class ManualClock(ClockPort):
    def __init__(self, step_seconds=0.001):
        self._step_seconds = float(step_seconds)
        self._now_seconds = 0.0
        self._tick_count = 0

    @property
    def tick_count(self):
        return self._tick_count

    def tick(self):
        self._tick_count += 1
        self._now_seconds += self._step_seconds

    def now_seconds(self):
        return self._now_seconds


class MemoryConfiguration(ConfigurationPort):
    def __init__(self, values=None):
        self._values = dict(values or {})

    def get(self, key, default=None):
        return self._values.get(key, default)


class RecordingSynthCore(SynthCore):
    def __init__(self, name):
        self._name = str(name)
        self._events = []
        self._is_started = False

    @property
    def name(self):
        return self._name

    @property
    def events(self):
        return tuple(self._events)

    @property
    def is_started(self):
        return self._is_started

    def start(self):
        self._is_started = True

    def handle_event(self, event):
        if not self._is_started:
            raise RuntimeError("synth core is stopped")
        self._events.append(event)

    def render_frame(self):
        return (0.0, 0.0)

    def stop(self):
        self._is_started = False
