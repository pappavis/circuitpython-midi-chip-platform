# Bestand: d1_core.py
# Versienommer: 0.15.0
# Doel: Lewer 'n draagbare monofoniese sine/saw/square D1 PCM-basiskern.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-063 Portable D1 Baseline Synth Core
# Actienr: MCP-ACT-063-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-063-START

import math

from midi_chip_platform.audio import AudioBlock, AudioStreamFormat
from midi_chip_platform.core import SynthCore
from midi_chip_platform.events import NoteEvent


class D1Patch:
    def __init__(self, waveform="sine", audio_format=None, amplitude=0.2):
        selected_waveform = str(waveform).lower()
        if selected_waveform not in ("sine", "saw", "square"):
            raise ValueError("waveform must be sine, saw or square")
        selected_format = (
            audio_format
            if audio_format is not None
            else AudioStreamFormat(
                sample_rate=16000,
                channel_count=1,
                sample_width_bits=16,
                frames_per_block=128,
            )
        )
        if not isinstance(selected_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        selected_amplitude = float(amplitude)
        if not 0.0 < selected_amplitude <= 1.0:
            raise ValueError("amplitude must be greater than 0.0 and at most 1.0")
        self._waveform = selected_waveform
        self._audio_format = selected_format
        self._amplitude = selected_amplitude

    @property
    def waveform(self):
        return self._waveform

    @property
    def audio_format(self):
        return self._audio_format

    @property
    def amplitude(self):
        return self._amplitude


class D1Oscillator:
    def __init__(self, patch):
        if not isinstance(patch, D1Patch):
            raise TypeError("patch must be D1Patch")
        self._patch = patch
        self._phase = 0.0

    @property
    def phase(self):
        return self._phase

    def reset(self):
        self._phase = 0.0

    def render(self, frequency_hz, velocity):
        selected_frequency = float(frequency_hz)
        if selected_frequency <= 0.0:
            raise ValueError("frequency_hz must be positive")
        selected_velocity = int(velocity)
        if not 0 <= selected_velocity <= 127:
            raise ValueError("velocity must be between 0 and 127")
        audio_format = self._patch.audio_format
        peak = int(round(32767 * self._patch.amplitude * selected_velocity / 127.0))
        phase_increment = selected_frequency / audio_format.sample_rate
        samples = []
        for _ in range(audio_format.frames_per_block):
            value = self._wave_sample(self._phase)
            pcm_sample = max(-32768, min(32767, int(round(value * peak))))
            for _ in range(audio_format.channel_count):
                samples.append(pcm_sample)
            self._phase += phase_increment
            self._phase -= math.floor(self._phase)
        return AudioBlock(audio_format, samples)

    def _wave_sample(self, phase):
        if self._patch.waveform == "sine":
            return math.sin(2.0 * math.pi * phase)
        if self._patch.waveform == "saw":
            return 2.0 * (phase - math.floor(phase + 0.5))
        return 1.0 if phase < 0.5 else -1.0


class D1SynthCore(SynthCore):
    def __init__(self, patch=None, name="d1"):
        self._patch = patch if patch is not None else D1Patch()
        if not isinstance(self._patch, D1Patch):
            raise TypeError("patch must be D1Patch")
        self._name = str(name)
        self._oscillator = D1Oscillator(self._patch)
        self._is_started = False
        self._active_note = None
        self._active_frequency_hz = None
        self._active_velocity = 0

    @property
    def name(self):
        return self._name

    @property
    def is_started(self):
        return self._is_started

    @property
    def active_note(self):
        return self._active_note

    @property
    def active_frequency_hz(self):
        return self._active_frequency_hz

    @property
    def phase(self):
        return self._oscillator.phase

    @property
    def audio_format(self):
        return self._patch.audio_format

    def start(self):
        if self._is_started:
            return
        self._clear_voice()
        self._is_started = True

    def handle_event(self, event):
        self._require_started()
        if not isinstance(event, NoteEvent):
            return False
        if event.is_note_on and event.velocity > 0:
            self._active_note = event.note
            self._active_frequency_hz = self._frequency_for_midi_note(event.note)
            self._active_velocity = event.velocity
            self._oscillator.reset()
            return True
        if self._active_note == event.note:
            self._clear_voice()
            return True
        return False

    def render_audio_block(self):
        self._require_started()
        if self._active_note is None:
            return AudioBlock.silence(self._patch.audio_format)
        return self._oscillator.render(
            frequency_hz=self._active_frequency_hz,
            velocity=self._active_velocity,
        )

    def stop(self):
        if not self._is_started:
            return
        self._clear_voice()
        self._is_started = False

    def _clear_voice(self):
        self._active_note = None
        self._active_frequency_hz = None
        self._active_velocity = 0
        self._oscillator.reset()

    def _require_started(self):
        if not self._is_started:
            raise RuntimeError("D1 synth core is stopped")

    @staticmethod
    def _frequency_for_midi_note(note):
        return 440.0 * math.pow(2.0, (int(note) - 69) / 12.0)
