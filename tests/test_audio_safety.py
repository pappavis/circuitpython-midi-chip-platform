# Bestand: test_audio_safety.py
# Versienommer: 0.16.0
# Doel: Spesifiseer veilige master gain, startup mute en output-profielmetadata.
# Sprint: Sprint 3
# Epic: MCP-EPIC-007 DSP And Pedal Hardware
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START

import pytest

from midi_chip_platform.audio import (
    AudioBlock,
    AudioSafetyProfile,
    AudioStreamFormat,
    MemoryAudioOutput,
    SafeAudioOutput,
)


class TestAudioSafetyProfile:
    def test_defaults_are_low_gain_speaker_only_and_start_muted(self) -> None:
        profile = AudioSafetyProfile()

        assert profile.master_gain == 0.08
        assert profile.maximum_master_gain == 0.25
        assert profile.startup_muted is True
        assert profile.amplifier_gain_db == 9.0
        assert profile.gain_pin_profile == "floating-9db"
        assert profile.shutdown_mode == "software-mute"
        assert profile.output_load == "speaker-4-8-ohm"

    def test_profile_rejects_gain_above_ceiling_or_unsafe_load_claim(self) -> None:
        with pytest.raises(ValueError, match="maximum_master_gain"):
            AudioSafetyProfile(master_gain=0.30, maximum_master_gain=0.25)
        with pytest.raises(ValueError, match="output_load"):
            AudioSafetyProfile(output_load="headphones")


class TestSafeAudioOutput:
    def test_output_is_silent_until_unmuted_then_applies_master_gain(self) -> None:
        audio_format = AudioStreamFormat(frames_per_block=4)
        delegate = MemoryAudioOutput(audio_format)
        output = SafeAudioOutput(delegate, AudioSafetyProfile(master_gain=0.08))
        block = AudioBlock(audio_format, (12000, -12000, 32767, -32768))

        output.open()
        output.write_block(block)
        output.unmute()
        output.write_block(block)
        output.close()

        assert delegate.blocks[0].samples == (0, 0, 0, 0)
        assert delegate.blocks[1].samples == (960, -960, 2621, -2621)
        assert output.is_muted is True
        assert delegate.is_open is False

    def test_unmute_requires_open_output_and_runtime_gain_stays_bounded(self) -> None:
        audio_format = AudioStreamFormat()
        output = SafeAudioOutput(MemoryAudioOutput(audio_format))

        with pytest.raises(RuntimeError, match="closed"):
            output.unmute()
        with pytest.raises(ValueError, match="maximum_master_gain"):
            output.set_master_gain(0.5)

        output.set_master_gain(0.10)
        assert output.master_gain == 0.10

    def test_profile_report_never_claims_headphone_or_line_output(self) -> None:
        report = "\n".join(AudioSafetyProfile().report_lines())

        assert "AUDIO_OUTPUT_LOAD=speaker-4-8-ohm" in report
        assert "AUDIO_MASTER_GAIN=0.080000" in report
        assert "AUDIO_STARTUP_MUTED=true" in report
        assert "AUDIO_GAIN_PIN_PROFILE=floating-9db" in report
        assert "AUDIO_SHUTDOWN_MODE=software-mute" in report
        assert "headphone" not in report.lower()
