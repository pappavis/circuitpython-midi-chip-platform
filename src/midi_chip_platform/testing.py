# Bestand: testing.py
# Versienommer: 0.15.0
# Doel: Verskaf host-fakes vir MIDI-, deurlopende blokaudio- en kernkontraktoetse.
# Sprint: Sprint 2
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-063 Portable D1 Baseline Synth Core
# Actienr: MCP-ACT-063-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-063-START

from midi_chip_platform.audio import AudioBlock, AudioStreamFormat
from midi_chip_platform.audio import MemoryAudioOutput as AudioMemoryOutput
from midi_chip_platform.core import SynthCore
from midi_chip_platform.ports import ClockPort, ConfigurationPort, MidiInputPort


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


class MemoryAudioOutput(AudioMemoryOutput):
    pass


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
    def __init__(self, name, audio_format=None):
        self._name = str(name)
        self._audio_format = (
            audio_format if audio_format is not None else AudioStreamFormat()
        )
        self._events = []
        self._is_started = False
        self._render_count = 0

    @property
    def name(self):
        return self._name

    @property
    def events(self):
        return tuple(self._events)

    @property
    def is_started(self):
        return self._is_started

    @property
    def render_count(self):
        return self._render_count

    def start(self):
        self._is_started = True

    def handle_event(self, event):
        if not self._is_started:
            raise RuntimeError("synth core is stopped")
        self._events.append(event)

    def render_audio_block(self):
        self._render_count += 1
        return AudioBlock.silence(self._audio_format, frame_count=1)

    def stop(self):
        self._is_started = False
