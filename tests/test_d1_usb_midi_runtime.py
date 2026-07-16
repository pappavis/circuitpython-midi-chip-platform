# Bestand: test_d1_usb_midi_runtime.py
# Versienommer: 0.17.7
# Doel: Spesifiseer die USB-MIDI na D1 na I2S fast-boot toonpad vir Logic-aanvaarding.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-P0-REALTIME-FIX-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-REALTIME-ANALYSE-002

from midi_chip_platform.audio import AudioStreamFormat, MemoryAudioOutput
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.d1_runtime import D1UsbMidiI2sRuntime, D1UsbMidiI2sRuntimeFactory
from midi_chip_platform.events import NoteEvent
from midi_chip_platform.testing import MemoryConfiguration, MemoryMidiInput


class TestD1UsbMidiI2sRuntime:
    class NoSleep:
        def __init__(self):
            self.calls = []
            self._now = 0.0

        def sleep(self, seconds):
            self.calls.append(seconds)
            self._now += float(seconds)

        def monotonic(self):
            return self._now

    class ToneMemoryAudioOutput(MemoryAudioOutput):
        def __init__(self, audio_format):
            super().__init__(audio_format)
            self._tones = []

        @property
        def tones(self):
            return tuple(self._tones)

        def play_tone(self, frequency_hz, duration_seconds, amplitude=8192):
            self._tones.append(
                ("play", float(frequency_hz), float(duration_seconds), int(amplitude))
            )

        def start_tone(self, frequency_hz, amplitude=8192):
            self._tones.append(
                ("start", float(frequency_hz), int(amplitude))
            )

        def stop_tone(self):
            self._tones.append(("stop",))

    def test_runtime_turns_note_on_and_note_off_into_audio_blocks(self) -> None:
        audio_format = AudioStreamFormat(sample_rate=16000, frames_per_block=32)
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=60, velocity=100),
                None,
                NoteEvent.note_off(channel=1, note=60, velocity=0),
                None,
            )
        )
        audio_output = MemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.2)
        )
        output = []
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=output.append,
            sleeper=self.NoSleep(),
            max_blocks=4,
            idle_sleep_seconds=0.001,
            minimum_note_seconds=0.0,
            stream_active_blocks=True,
        )

        result = runtime.run()

        assert result is True
        assert midi_input.is_open is False
        assert audio_output.is_open is False
        assert len(audio_output.blocks) == 2
        assert any(audio_output.blocks[0].samples)
        assert any(audio_output.blocks[1].samples)
        assert output[0].startswith("D1_RUNTIME_STATUS=START")
        assert "D1_MIDI_INPUT_STATUS=OPEN" in output
        assert "D1_RUNTIME_READY;ready_ms=0" in output
        assert "D1_MIDI_EVENT=note_on;channel=1;note=60;velocity=100" not in output
        assert any(line.startswith("D1_REALTIME_MIDI_NOTE=note_on") for line in output)
        assert output[-1].startswith("D1_RUNTIME_STATUS=PASS")

    def test_runtime_does_not_write_i2s_silence_while_waiting_for_midi(self) -> None:
        audio_format = AudioStreamFormat(sample_rate=16000, frames_per_block=32)
        midi_input = MemoryMidiInput((None, None, None, None))
        audio_output = MemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.2)
        )
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=[].append,
            sleeper=self.NoSleep(),
            max_blocks=4,
        )

        result = runtime.run()

        assert result is True
        assert len(audio_output.blocks) == 0
        assert runtime.block_count == 0
        assert runtime.idle_poll_count == 4

    def test_note_on_writes_minimum_audible_blocks_before_early_note_off(self) -> None:
        audio_format = AudioStreamFormat(
            sample_rate=16000,
            frames_per_block=160,
        )
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=60, velocity=100),
                NoteEvent.note_off(channel=1, note=60, velocity=0),
            )
        )
        audio_output = MemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.2)
        )
        output = []
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=output.append,
            sleeper=self.NoSleep(),
            max_blocks=13,
            minimum_note_seconds=0.05,
            event_logging="verbose",
        )

        result = runtime.run()

        assert result is True
        assert len(audio_output.blocks) == 5
        assert runtime.audible_note_count == 1
        assert runtime.block_count == 5
        assert runtime.idle_poll_count == 8
        assert any(audio_output.blocks[0].samples)
        assert any(line.startswith("D1_AUDIO_EVENT=audible_note;note=60;blocks=5") for line in output)

    def test_note_on_prefers_i2s_tone_path_when_output_supports_it(self) -> None:
        audio_format = AudioStreamFormat(
            sample_rate=16000,
            frames_per_block=160,
        )
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=69, velocity=100),
                NoteEvent.note_off(channel=1, note=69, velocity=64),
            )
        )
        audio_output = self.ToneMemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.5)
        )
        output = []
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=output.append,
            sleeper=self.NoSleep(),
            max_blocks=50,
            minimum_note_seconds=0.05,
            audition_tone_amplitude=8192,
        )

        result = runtime.run()

        assert result is True
        assert len(audio_output.blocks) == 0
        assert audio_output.tones[0] == ("start", 440.0, 8192)
        assert audio_output.tones[-1] == ("stop",)
        assert any(
            line.startswith(
                "D1_REALTIME_MIDI_NOTE=note_on;channel=1;note=69;velocity=100;"
                "frequency_hz=440.000"
            )
            and "event_ms=0;tone_start_ms=0;note_latency_ms=0" in line
            for line in output
        )
        assert any(
            line.startswith(
                "D1_AUDIO_EVENT=audible_note;mode=latched_tone;note=69;"
                "blocks=5;minimum_seconds=0.050"
            )
            for line in output
        ) is False

    def test_verbose_event_logging_keeps_diagnostic_midi_and_audio_lines(self) -> None:
        audio_format = AudioStreamFormat(
            sample_rate=16000,
            frames_per_block=160,
        )
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=69, velocity=100),
                NoteEvent.note_off(channel=1, note=69, velocity=64),
            )
        )
        audio_output = self.ToneMemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.5)
        )
        output = []
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=output.append,
            sleeper=self.NoSleep(),
            max_blocks=50,
            minimum_note_seconds=0.05,
            audition_tone_amplitude=8192,
            event_logging="verbose",
        )

        result = runtime.run()

        assert result is True
        assert "D1_MIDI_EVENT=note_on;channel=1;note=69;velocity=100" in output
        assert any(
            line.startswith(
                "D1_AUDIO_EVENT=audible_note;mode=latched_tone;note=69;"
                "blocks=5;minimum_seconds=0.050"
            )
            for line in output
        )

    def test_low_logic_velocity_is_lifted_for_hil_audibility(self) -> None:
        audio_format = AudioStreamFormat(
            sample_rate=16000,
            frames_per_block=160,
        )
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=1, note=69, velocity=32),
                NoteEvent.note_off(channel=1, note=69, velocity=64),
            )
        )
        audio_output = MemoryAudioOutput(audio_format)
        core = D1SynthCore(
            D1Patch(waveform="square", audio_format=audio_format, amplitude=0.5)
        )
        output = []
        runtime = D1UsbMidiI2sRuntime(
            midi_input=midi_input,
            audio_output=audio_output,
            core=core,
            output=output.append,
            sleeper=self.NoSleep(),
            max_blocks=13,
            minimum_note_seconds=0.05,
            minimum_note_velocity=64,
            event_logging="verbose",
        )

        result = runtime.run()

        assert result is True
        assert any(audio_output.blocks[0].samples)
        assert any(
            "D1_AUDIO_EVENT=audible_note;note=69;blocks=5;seconds=0.050;"
            "midi_velocity=32;play_velocity=64" in line
            for line in output
        )

    def test_factory_returns_none_unless_d1_runtime_is_enabled(self) -> None:
        factory = D1UsbMidiI2sRuntimeFactory()

        assert factory.create_if_enabled(MemoryConfiguration({"synth.d1.enabled": False})) is None
