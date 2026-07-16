# Bestand: test_d1_core.py
# Versienommer: 0.15.0
# Doel: Spesifiseer die draagbare monofoniese D1-basiskern en PCM-blokgedrag.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-063 Portable D1 Baseline Synth Core
# Actienr: MCP-ACT-063-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-063-START

import pytest

from midi_chip_platform.audio import AudioStreamFormat
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.events import NoteEvent


class TestD1Patch:
    def test_default_patch_matches_verified_mono_i2s_profile(self) -> None:
        patch = D1Patch()

        assert patch.waveform == "sine"
        assert patch.audio_format.sample_rate == 16000
        assert patch.audio_format.channel_count == 1
        assert patch.audio_format.frames_per_block == 128
        assert patch.amplitude == pytest.approx(0.2)

    def test_patch_rejects_unsupported_waveform_and_unsafe_amplitude(self) -> None:
        with pytest.raises(ValueError, match="waveform"):
            D1Patch(waveform="noise")
        with pytest.raises(ValueError, match="amplitude"):
            D1Patch(amplitude=1.1)


class TestD1SynthCore:
    def _started_core(self, waveform="sine", frames_per_block=32):
        audio_format = AudioStreamFormat(
            sample_rate=16000,
            channel_count=1,
            frames_per_block=frames_per_block,
        )
        core = D1SynthCore(D1Patch(waveform=waveform, audio_format=audio_format))
        core.start()
        return core

    def test_note_on_maps_a4_to_frequency_and_velocity_scaled_pcm(self) -> None:
        core = self._started_core("sine")

        core.handle_event(NoteEvent.note_on(channel=1, note=69, velocity=127))
        loud = core.render_audio_block()
        core.handle_event(NoteEvent.note_on(channel=1, note=69, velocity=32))
        quiet = core.render_audio_block()

        assert core.active_note == 69
        assert core.active_frequency_hz == pytest.approx(440.0)
        assert max(abs(sample) for sample in loud.samples) > max(
            abs(sample) for sample in quiet.samples
        )

    @pytest.mark.parametrize("waveform", ("sine", "saw", "square"))
    def test_each_waveform_renders_bounded_non_silent_pcm(self, waveform) -> None:
        core = self._started_core(waveform, frames_per_block=128)
        core.handle_event(NoteEvent.note_on(channel=1, note=60, velocity=100))

        block = core.render_audio_block()

        assert block.frame_count == 128
        assert any(sample != 0 for sample in block.samples)
        assert min(block.samples) >= -32768
        assert max(block.samples) <= 32767
        if waveform == "square":
            assert len(set(block.samples)) == 2
        if waveform == "saw":
            assert len(set(block.samples)) > 10

    def test_phase_continues_across_bounded_blocks(self) -> None:
        core = self._started_core("sine", frames_per_block=17)
        core.handle_event(NoteEvent.note_on(channel=1, note=60, velocity=100))

        first = core.render_audio_block()
        phase_after_first = core.phase
        second = core.render_audio_block()

        assert 0.0 <= phase_after_first < 1.0
        assert first.samples != second.samples
        assert core.phase != phase_after_first

    def test_matching_note_off_and_stop_clear_voice_to_silence(self) -> None:
        core = self._started_core("square")
        core.handle_event(NoteEvent.note_on(channel=1, note=60, velocity=100))
        core.handle_event(NoteEvent.note_off(channel=1, note=60))

        silence = core.render_audio_block()

        assert core.active_note is None
        assert set(silence.samples) == {0}

        core.stop()
        assert core.is_started is False
        with pytest.raises(RuntimeError, match="stopped"):
            core.render_audio_block()

    def test_unmatched_note_off_does_not_stop_active_note(self) -> None:
        core = self._started_core()
        core.handle_event(NoteEvent.note_on(channel=1, note=60, velocity=100))

        core.handle_event(NoteEvent.note_off(channel=1, note=62))

        assert core.active_note == 60
