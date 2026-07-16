# Bestand: test_audio_output.py
# Versienommer: 0.13.0
# Doel: Spesifiseer blokgebaseerde PCM-formaat en host-veilige audio backends.
# Sprint: Sprint 2
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-014 AudioOutput Port And Null Backend
# Actienr: MCP-ACT-014-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-014-START

import pytest

from midi_chip_platform.audio import (
    AudioBlock,
    AudioStreamFormat,
    MemoryAudioOutput,
    NullAudioOutput,
)


class TestAudioStreamFormat:
    def test_default_format_is_bounded_mono_pcm(self) -> None:
        audio_format = AudioStreamFormat()

        assert audio_format.sample_rate == 44100
        assert audio_format.channel_count == 1
        assert audio_format.sample_width_bits == 16
        assert audio_format.frames_per_block == 128

    def test_format_rejects_unsupported_or_unbounded_values(self) -> None:
        with pytest.raises(ValueError, match="channel_count"):
            AudioStreamFormat(channel_count=3)

        with pytest.raises(ValueError, match="sample_width_bits"):
            AudioStreamFormat(sample_width_bits=24)

        with pytest.raises(ValueError, match="frames_per_block"):
            AudioStreamFormat(frames_per_block=0)


class TestAudioBlock:
    def test_block_preserves_interleaved_pcm_and_frame_count(self) -> None:
        audio_format = AudioStreamFormat(channel_count=2, frames_per_block=4)
        block = AudioBlock(audio_format, (-32768, 32767, 0, 1))

        assert block.samples == (-32768, 32767, 0, 1)
        assert block.frame_count == 2
        assert block.audio_format is audio_format

    def test_block_rejects_invalid_shape_capacity_and_range(self) -> None:
        stereo = AudioStreamFormat(channel_count=2, frames_per_block=2)

        with pytest.raises(ValueError, match="interleaved"):
            AudioBlock(stereo, (0, 1, 2))
        with pytest.raises(ValueError, match="capacity"):
            AudioBlock(stereo, (0, 0, 0, 0, 0, 0))
        with pytest.raises(ValueError, match="16-bit"):
            AudioBlock(stereo, (0, 40000))

    def test_silence_factory_is_bounded_by_the_format(self) -> None:
        audio_format = AudioStreamFormat(channel_count=2, frames_per_block=8)

        block = AudioBlock.silence(audio_format, frame_count=3)

        assert block.samples == (0, 0, 0, 0, 0, 0)
        assert block.frame_count == 3


class TestNullAudioOutput:
    def test_null_backend_counts_blocks_without_retaining_pcm(self) -> None:
        audio_format = AudioStreamFormat(frames_per_block=4)
        output = NullAudioOutput(audio_format)
        block = AudioBlock.silence(audio_format, frame_count=3)

        output.open()
        output.write_block(block)
        output.close()

        assert output.block_count == 1
        assert output.frame_count == 3
        assert output.is_open is False

    def test_backend_rejects_closed_writes_and_format_mismatch(self) -> None:
        mono = AudioStreamFormat(channel_count=1)
        stereo = AudioStreamFormat(channel_count=2)
        output = NullAudioOutput(mono)

        with pytest.raises(RuntimeError, match="closed"):
            output.write_block(AudioBlock.silence(mono, frame_count=1))

        output.open()
        with pytest.raises(ValueError, match="format"):
            output.write_block(AudioBlock.silence(stereo, frame_count=1))


class TestMemoryAudioOutput:
    def test_memory_backend_retains_blocks_for_host_assertions(self) -> None:
        audio_format = AudioStreamFormat(frames_per_block=4)
        output = MemoryAudioOutput(audio_format)
        block = AudioBlock(audio_format, (100, -100))

        output.open()
        output.write_block(block)

        assert output.blocks == (block,)
        assert output.block_count == 1
        assert output.frame_count == 2
