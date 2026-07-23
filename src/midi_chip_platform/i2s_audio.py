# Bestand: i2s_audio.py
# Versienommer: 0.20.2
# Doel: Lewer CircuitPython I2S-blokuitvoer en hou latched toonbuffers aktief.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: BUG-001-MINIMAL-FIX-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / BUG-001

from midi_chip_platform.audio import AudioBlock, AudioStreamFormat
from midi_chip_platform.ports import AudioOutputPort


class CircuitPythonI2sAudioOutput(AudioOutputPort):
    def __init__(
        self,
        audio_format,
        importer=None,
        bit_clock_pin_name="IO5",
        word_select_pin_name="IO3",
        data_pin_name="IO7",
        poll_sleep_seconds=0.001,
        timing_observer=None,
    ):
        if not isinstance(audio_format, AudioStreamFormat):
            raise TypeError("audio_format must be AudioStreamFormat")
        self._audio_format = audio_format
        self._importer = importer if importer is not None else __import__
        self._bit_clock_pin_name = str(bit_clock_pin_name)
        self._word_select_pin_name = str(word_select_pin_name)
        self._data_pin_name = str(data_pin_name)
        self._poll_sleep_seconds = float(poll_sleep_seconds)
        self._timing_observer = timing_observer
        self._array_module = None
        self._audiocore_module = None
        self._time_module = None
        self._device = None
        self._is_muted = True
        self._active_sample = None
        self._active_buffer = None

    @property
    def audio_format(self):
        return self._audio_format

    @property
    def is_open(self):
        return self._device is not None

    @property
    def is_muted(self):
        return self._is_muted

    def open(self):
        if self.is_open:
            return
        board_module = self._importer("board")
        audiobusio_module = self._importer("audiobusio")
        self._audiocore_module = self._importer("audiocore")
        self._array_module = self._importer("array")
        self._time_module = self._importer("time")
        self._device = audiobusio_module.I2SOut(
            getattr(board_module, self._bit_clock_pin_name),
            getattr(board_module, self._word_select_pin_name),
            getattr(board_module, self._data_pin_name),
        )
        self._is_muted = True

    def write_block(self, block):
        if not self.is_open:
            raise RuntimeError("I2S audio output is closed")
        if not isinstance(block, AudioBlock):
            raise TypeError("block must be AudioBlock")
        if not self._audio_format.is_compatible_with(block.audio_format):
            raise ValueError("audio block format does not match output format")
        selected_block = (
            AudioBlock.silence(self._audio_format, block.frame_count)
            if self._is_muted
            else block
        )
        if self._is_muted:
            self._sleep_for_block(selected_block)
            return
        self._active_buffer, self._active_sample = self._raw_sample_for(selected_block)
        self._record_i2s_dma_write()
        self._device.play(self._active_sample, loop=True)
        self._sleep_for_block(selected_block)
        self._device.stop()
        self._active_sample = None
        self._active_buffer = None

    def play_tone(self, frequency_hz, duration_seconds, amplitude=2048):
        if not self.is_open:
            raise RuntimeError("I2S audio output is closed")
        if self._is_muted:
            self._time_module.sleep(max(float(duration_seconds), self._poll_sleep_seconds))
            return
        selected_frequency = float(frequency_hz)
        selected_duration = float(duration_seconds)
        selected_amplitude = int(amplitude)
        if selected_frequency <= 0.0:
            raise ValueError("frequency_hz must be positive")
        if selected_duration <= 0.0:
            raise ValueError("duration_seconds must be positive")
        if not 1 <= selected_amplitude <= 32767:
            raise ValueError("amplitude must be between 1 and 32767")
        period_length = max(2, int(round(self._audio_format.sample_rate / selected_frequency)))
        half_period = max(1, period_length // 2)
        low_value = 32768 - selected_amplitude
        high_value = 32768 + selected_amplitude
        values = [
            high_value if index < half_period else low_value
            for index in range(period_length)
        ]
        self._active_buffer = self._array_module.array("H", values)
        self._active_sample = self._audiocore_module.RawSample(
            self._active_buffer,
            sample_rate=self._audio_format.sample_rate,
        )
        self._record_i2s_dma_write()
        self._device.play(self._active_sample, loop=True)
        self._time_module.sleep(max(selected_duration, self._poll_sleep_seconds))
        self._device.stop()
        self._active_sample = None
        self._active_buffer = None

    def start_tone(self, frequency_hz, amplitude=2048):
        if not self.is_open:
            raise RuntimeError("I2S audio output is closed")
        if self._is_muted:
            return
        selected_frequency = float(frequency_hz)
        selected_amplitude = int(amplitude)
        if selected_frequency <= 0.0:
            raise ValueError("frequency_hz must be positive")
        if not 1 <= selected_amplitude <= 32767:
            raise ValueError("amplitude must be between 1 and 32767")
        self.stop_tone()
        period_length = max(2, int(round(self._audio_format.sample_rate / selected_frequency)))
        half_period = max(1, period_length // 2)
        low_value = 32768 - selected_amplitude
        high_value = 32768 + selected_amplitude
        values = [
            high_value if index < half_period else low_value
            for index in range(period_length)
        ]
        self._active_buffer = self._array_module.array("H", values)
        self._active_sample = self._audiocore_module.RawSample(
            self._active_buffer,
            sample_rate=self._audio_format.sample_rate,
        )
        self._record_i2s_dma_write()
        self._device.play(self._active_sample, loop=True)

    def stop_tone(self):
        if self._device is not None:
            self._device.stop()
        self._active_sample = None
        self._active_buffer = None

    def mute(self):
        self._is_muted = True
        self.stop_tone()

    def unmute(self):
        if not self.is_open:
            raise RuntimeError("I2S audio output is closed")
        self._is_muted = False

    def close(self):
        if self._device is None:
            return
        self.mute()
        self._device.deinit()
        self._device = None

    def _raw_sample_for(self, block):
        values = []
        for sample in block.samples:
            values.append(max(0, min(65535, int(sample) + 32768)))
        buffer = self._array_module.array("H", values)
        return buffer, self._audiocore_module.RawSample(
            buffer,
            sample_rate=self._audio_format.sample_rate,
        )

    def _sleep_for_block(self, block):
        duration_seconds = block.frame_count / self._audio_format.sample_rate
        self._time_module.sleep(max(duration_seconds, self._poll_sleep_seconds))

    def _record_i2s_dma_write(self):
        if self._timing_observer is None:
            return
        record = getattr(self._timing_observer, "record_i2s_dma_write", None)
        if callable(record):
            record()
