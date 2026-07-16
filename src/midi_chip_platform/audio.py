# Bestand: audio.py
# Versienommer: 0.13.0
# Doel: Definieer begrensde PCM-blokke en host-veilige audio backends.
# Sprint: Sprint 2
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-014 AudioOutput Port And Null Backend
# Actienr: MCP-ACT-014-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-014-START

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


class NullAudioOutput(AudioOutputPort):
    def __init__(self, audio_format):
        if not isinstance(audio_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        self._audio_format = audio_format
        self._is_open = False
        self._block_count = 0
        self._frame_count = 0

    @property
    def audio_format(self):
        return self._audio_format

    @property
    def is_open(self):
        return self._is_open

    @property
    def block_count(self):
        return self._block_count

    @property
    def frame_count(self):
        return self._frame_count

    def open(self):
        self._is_open = True

    def write_block(self, block):
        if not self._is_open:
            raise RuntimeError("audio output is closed")
        if not isinstance(block, AudioBlock):
            raise TypeError("block must be AudioBlock")
        if not self._audio_format.is_compatible_with(block.audio_format):
            raise ValueError("audio block format does not match output format")
        self._block_count += 1
        self._frame_count += block.frame_count

    def close(self):
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
