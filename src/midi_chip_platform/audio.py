# Bestand: audio.py
# Versienommer: 0.16.0
# Doel: Definieer begrensde PCM-blokke, startup mute en veilige master gain.
# Sprint: Sprint 3
# Epic: MCP-EPIC-007 DSP And Pedal Hardware
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START

from midi_chip_platform.ports import AudioOutputPort


class AudioStreamFormat:
    def __init__(
        self,
        sample_rate=44100,
        channel_count=1,
        sample_width_bits=16,
        frames_per_block=128,
    ):
        self._sample_rate = int(sample_rate)
        self._channel_count = int(channel_count)
        self._sample_width_bits = int(sample_width_bits)
        self._frames_per_block = int(frames_per_block)
        if self._sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self._channel_count not in (1, 2):
            raise ValueError("channel_count must be 1 or 2")
        if self._sample_width_bits != 16:
            raise ValueError("sample_width_bits must be 16")
        if self._frames_per_block <= 0:
            raise ValueError("frames_per_block must be positive")

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def sample_width_bits(self):
        return self._sample_width_bits

    @property
    def frames_per_block(self):
        return self._frames_per_block

    @property
    def sample_capacity(self):
        return self._frames_per_block * self._channel_count

    def is_compatible_with(self, other):
        return (
            isinstance(other, AudioStreamFormat)
            and self._sample_rate == other.sample_rate
            and self._channel_count == other.channel_count
            and self._sample_width_bits == other.sample_width_bits
            and self._frames_per_block == other.frames_per_block
        )


class AudioBlock:
    def __init__(self, audio_format, samples):
        if not isinstance(audio_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        self._audio_format = audio_format
        self._samples = tuple(samples)
        if not self._samples:
            raise ValueError("audio block must contain at least one frame")
        if len(self._samples) % audio_format.channel_count != 0:
            raise ValueError("samples must contain complete interleaved frames")
        if len(self._samples) > audio_format.sample_capacity:
            raise ValueError("samples exceed audio block capacity")
        for sample in self._samples:
            if isinstance(sample, bool) or not isinstance(sample, int):
                raise TypeError("PCM samples must be integers")
            if not -32768 <= sample <= 32767:
                raise ValueError("PCM samples must fit signed 16-bit range")

    @property
    def audio_format(self):
        return self._audio_format

    @property
    def samples(self):
        return self._samples

    @property
    def frame_count(self):
        return len(self._samples) // self._audio_format.channel_count

    @classmethod
    def silence(cls, audio_format, frame_count=None):
        if not isinstance(audio_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        selected_frame_count = (
            audio_format.frames_per_block if frame_count is None else int(frame_count)
        )
        if not 1 <= selected_frame_count <= audio_format.frames_per_block:
            raise ValueError("frame_count must fit audio block capacity")
        sample_count = selected_frame_count * audio_format.channel_count
        return cls(audio_format, (0,) * sample_count)


class AudioSafetyProfile:
    def __init__(
        self,
        master_gain=0.08,
        maximum_master_gain=0.25,
        startup_muted=True,
        amplifier_gain_db=9.0,
        gain_pin_profile="floating-9db",
        shutdown_mode="software-mute",
        output_load="speaker-4-8-ohm",
    ):
        self._master_gain = float(master_gain)
        self._maximum_master_gain = float(maximum_master_gain)
        self._startup_muted = bool(startup_muted)
        self._amplifier_gain_db = float(amplifier_gain_db)
        self._gain_pin_profile = str(gain_pin_profile)
        self._shutdown_mode = str(shutdown_mode)
        self._output_load = str(output_load)
        if not 0.0 < self._maximum_master_gain <= 1.0:
            raise ValueError("maximum_master_gain must be greater than 0.0 and at most 1.0")
        if not 0.0 <= self._master_gain <= self._maximum_master_gain:
            raise ValueError("master_gain must not exceed maximum_master_gain")
        if not self._gain_pin_profile:
            raise ValueError("gain_pin_profile must not be empty")
        if self._shutdown_mode not in ("software-mute", "sd-pin"):
            raise ValueError("shutdown_mode must be software-mute or sd-pin")
        if self._output_load != "speaker-4-8-ohm":
            raise ValueError("output_load must be speaker-4-8-ohm")

    @property
    def master_gain(self):
        return self._master_gain

    @property
    def maximum_master_gain(self):
        return self._maximum_master_gain

    @property
    def startup_muted(self):
        return self._startup_muted

    @property
    def amplifier_gain_db(self):
        return self._amplifier_gain_db

    @property
    def gain_pin_profile(self):
        return self._gain_pin_profile

    @property
    def shutdown_mode(self):
        return self._shutdown_mode

    @property
    def output_load(self):
        return self._output_load

    def report_lines(self):
        return (
            f"AUDIO_OUTPUT_LOAD={self._output_load}",
            f"AUDIO_MASTER_GAIN={self._master_gain:.6f}",
            f"AUDIO_MAXIMUM_MASTER_GAIN={self._maximum_master_gain:.6f}",
            "AUDIO_STARTUP_MUTED=" + str(self._startup_muted).lower(),
            f"AUDIO_AMPLIFIER_GAIN_DB={self._amplifier_gain_db:.1f}",
            f"AUDIO_GAIN_PIN_PROFILE={self._gain_pin_profile}",
            f"AUDIO_SHUTDOWN_MODE={self._shutdown_mode}",
        )


class NullAudioOutput(AudioOutputPort):
    def __init__(self, audio_format):
        if not isinstance(audio_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        self._audio_format = audio_format
        self._is_open = False
        self._is_muted = True
        self._block_count = 0
        self._frame_count = 0

    @property
    def audio_format(self):
        return self._audio_format

    @property
    def is_open(self):
        return self._is_open

    @property
    def is_muted(self):
        return self._is_muted

    @property
    def block_count(self):
        return self._block_count

    @property
    def frame_count(self):
        return self._frame_count

    def open(self):
        self._is_open = True
        self._is_muted = True

    def write_block(self, block):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        if not isinstance(block, AudioBlock):
            raise TypeError("block must be AudioBlock")
        if not self._audio_format.is_compatible_with(block.audio_format):
            raise ValueError("audio block format does not match output format")
        self._block_count += 1
        self._frame_count += block.frame_count

    def mute(self):
        self._is_muted = True

    def unmute(self):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        self._is_muted = False

    def close(self):
        self._is_muted = True
        self._is_open = False


class MemoryAudioOutput(NullAudioOutput):
    def __init__(self, audio_format):
        super().__init__(audio_format)
        self._blocks = []

    @property
    def blocks(self):
        return tuple(self._blocks)

    def write_block(self, block):
        super().write_block(block)
        self._blocks.append(block)


class SafeAudioOutput(AudioOutputPort):
    def __init__(self, delegate, profile=None):
        if not isinstance(delegate, AudioOutputPort):
            raise TypeError("delegate must implement AudioOutputPort")
        self._delegate = delegate
        self._profile = profile if profile is not None else AudioSafetyProfile()
        if not isinstance(self._profile, AudioSafetyProfile):
            raise TypeError("profile must be AudioSafetyProfile")
        self._master_gain = self._profile.master_gain
        self._is_open = False
        self._is_muted = True

    @property
    def audio_format(self):
        return self._delegate.audio_format

    @property
    def is_open(self):
        return self._is_open

    @property
    def is_muted(self):
        return self._is_muted

    @property
    def master_gain(self):
        return self._master_gain

    @property
    def profile(self):
        return self._profile

    def open(self):
        if self._is_open:
            return
        self._delegate.open()
        self._delegate.mute()
        self._is_open = True
        self._is_muted = self._profile.startup_muted
        if not self._is_muted:
            self._delegate.unmute()

    def write_block(self, block):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        if not isinstance(block, AudioBlock):
            raise TypeError("block must be AudioBlock")
        if not self.audio_format.is_compatible_with(block.audio_format):
            raise ValueError("audio block format does not match output format")
        selected_block = (
            AudioBlock.silence(self.audio_format, block.frame_count)
            if self._is_muted
            else self._scale(block)
        )
        self._delegate.write_block(selected_block)

    def mute(self):
        self._is_muted = True
        self._delegate.mute()

    def unmute(self):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        self._delegate.unmute()
        self._is_muted = False

    def set_master_gain(self, value):
        selected_gain = float(value)
        if not 0.0 <= selected_gain <= self._profile.maximum_master_gain:
            raise ValueError("master_gain must not exceed maximum_master_gain")
        self._master_gain = selected_gain

    def close(self):
        if not self._is_open:
            return
        self.mute()
        self._delegate.close()
        self._is_open = False

    def _scale(self, block):
        samples = []
        for sample in block.samples:
            scaled = int(round(sample * self._master_gain))
            samples.append(max(-32768, min(32767, scaled)))
        return AudioBlock(block.audio_format, samples)
