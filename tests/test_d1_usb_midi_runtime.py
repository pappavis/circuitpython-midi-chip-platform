# Bestand: test_d1_usb_midi_runtime.py
# Versienommer: 0.17.0
# Doel: Spesifiseer die USB-MIDI na D1 na I2S runtime-lus vir Logic-aanvaarding.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-055-START

from midi_chip_platform.audio import AudioStreamFormat, MemoryAudioOutput
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.d1_runtime import D1UsbMidiI2sRuntime, D1UsbMidiI2sRuntimeFactory
from midi_chip_platform.events import NoteEvent
from midi_chip_platform.testing import MemoryConfiguration, MemoryMidiInput


class TestD1UsbMidiI2sRuntime:
    class NoSleep:
        def __init__(self):
            self.calls = []

        def sleep(self, seconds):
            self.calls.append(seconds)

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
        )

        result = runtime.run()

        assert result is True
        assert midi_input.is_open is False
        assert audio_output.is_open is False
        assert len(audio_output.blocks) == 4
        assert any(audio_output.blocks[0].samples)
        assert any(audio_output.blocks[1].samples)
        assert set(audio_output.blocks[2].samples) == {0}
        assert output[0].startswith("D1_RUNTIME_STATUS=START")
        assert "D1_MIDI_EVENT=note_on;channel=1;note=60;velocity=100" in output
        assert output[-1].startswith("D1_RUNTIME_STATUS=PASS")

    def test_factory_returns_none_unless_d1_runtime_is_enabled(self) -> None:
        factory = D1UsbMidiI2sRuntimeFactory()

        assert factory.create_if_enabled(MemoryConfiguration({"synth.d1.enabled": False})) is None
