# Bestand: test_i2s_audio_output.py
# Versienommer: 0.20.2
# Doel: Spesifiseer timed CircuitPython I2S playback, diagnose-gelyke tone en latched sample-lifetime.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: BUG-001-MINIMAL-FIX-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / BUG-001

from midi_chip_platform.audio import AudioBlock, AudioStreamFormat
from midi_chip_platform.i2s_audio import CircuitPythonI2sAudioOutput


class TestCircuitPythonI2sAudioOutput:
    class FakeRawSample:
        def __init__(self, buffer, sample_rate):
            self.buffer = tuple(buffer)
            self.sample_rate = sample_rate

    class FakeAudioCore:
        def RawSample(self, buffer, sample_rate):
            return TestCircuitPythonI2sAudioOutput.FakeRawSample(buffer, sample_rate)

    class FakeArrayModule:
        def array(self, typecode, values):
            assert typecode == "H"
            return tuple(values)

    class FakeI2sDevice:
        def __init__(self, bit_clock, word_select, data):
            self.pins = (bit_clock, word_select, data)
            self.played = []
            self.playing = False
            self.stop_count = 0
            self.deinit_count = 0

        def play(self, sample, loop=False):
            self.played.append((sample, loop))
            self.playing = False

        def stop(self):
            self.stop_count += 1
            self.playing = False

        def deinit(self):
            self.deinit_count += 1

    class FakeAudioBusIo:
        def __init__(self):
            self.device = None

        def I2SOut(self, bit_clock, word_select, data):
            self.device = TestCircuitPythonI2sAudioOutput.FakeI2sDevice(
                bit_clock,
                word_select,
                data,
            )
            return self.device

    class FakeBoard:
        IO5 = "IO5"
        IO3 = "IO3"
        IO7 = "IO7"

    class FakeTime:
        def __init__(self):
            self.sleep_calls = []

        def sleep(self, seconds):
            self.sleep_calls.append(seconds)

    class Importer:
        def __init__(self, modules):
            self._modules = dict(modules)

        def __call__(self, name):
            return self._modules[name]

    def test_output_converts_signed_pcm_to_unsigned_raw_sample_and_releases_i2s(
        self,
    ) -> None:
        audio_bus = self.FakeAudioBusIo()
        audio_format = AudioStreamFormat(sample_rate=16000, frames_per_block=4)
        output = CircuitPythonI2sAudioOutput(
            audio_format=audio_format,
            importer=self.Importer(
                {
                    "array": self.FakeArrayModule(),
                    "audiobusio": audio_bus,
                    "audiocore": self.FakeAudioCore(),
                    "board": self.FakeBoard(),
                    "time": self.FakeTime(),
                }
            ),
            bit_clock_pin_name="IO5",
            word_select_pin_name="IO3",
            data_pin_name="IO7",
        )
        block = AudioBlock(audio_format, (-32768, -1, 0, 32767))

        output.open()
        output.unmute()
        output.write_block(block)
        output.close()

        assert audio_bus.device.pins == ("IO5", "IO3", "IO7")
        assert len(audio_bus.device.played) == 1
        sample, loop = audio_bus.device.played[0]
        assert sample.buffer == (0, 32767, 32768, 65535)
        assert sample.sample_rate == 16000
        assert loop is True
        assert output._active_sample is None
        assert output._time_module.sleep_calls == [0.001]
        assert audio_bus.device.stop_count >= 1
        assert audio_bus.device.deinit_count == 1

    def test_output_can_play_diagnostic_style_looped_tone(self) -> None:
        audio_bus = self.FakeAudioBusIo()
        fake_time = self.FakeTime()
        audio_format = AudioStreamFormat(sample_rate=16000, frames_per_block=128)
        output = CircuitPythonI2sAudioOutput(
            audio_format=audio_format,
            importer=self.Importer(
                {
                    "array": self.FakeArrayModule(),
                    "audiobusio": audio_bus,
                    "audiocore": self.FakeAudioCore(),
                    "board": self.FakeBoard(),
                    "time": fake_time,
                }
            ),
            bit_clock_pin_name="IO5",
            word_select_pin_name="IO3",
            data_pin_name="IO7",
        )

        output.open()
        output.unmute()
        output.play_tone(frequency_hz=440.0, duration_seconds=0.35, amplitude=2048)

        assert len(audio_bus.device.played) == 1
        sample, loop = audio_bus.device.played[0]
        assert loop is True
        assert sample.sample_rate == 16000
        assert len(sample.buffer) == 36
        assert min(sample.buffer) == 32768 - 2048
        assert max(sample.buffer) == 32768 + 2048
        assert fake_time.sleep_calls == [0.35]
        assert output._active_sample is None

    def test_output_can_latch_and_stop_tone_without_sleeping(self) -> None:
        audio_bus = self.FakeAudioBusIo()
        fake_time = self.FakeTime()
        audio_format = AudioStreamFormat(sample_rate=16000, frames_per_block=128)
        output = CircuitPythonI2sAudioOutput(
            audio_format=audio_format,
            importer=self.Importer(
                {
                    "array": self.FakeArrayModule(),
                    "audiobusio": audio_bus,
                    "audiocore": self.FakeAudioCore(),
                    "board": self.FakeBoard(),
                    "time": fake_time,
                }
            ),
            bit_clock_pin_name="IO5",
            word_select_pin_name="IO3",
            data_pin_name="IO7",
        )

        output.open()
        output.unmute()
        output.start_tone(frequency_hz=440.0, amplitude=2048)

        assert len(audio_bus.device.played) == 1
        sample, loop = audio_bus.device.played[0]
        assert loop is True
        assert fake_time.sleep_calls == []
        assert output._active_sample is not None
        assert output._active_buffer is sample.buffer

        output.stop_tone()

        assert output._active_sample is None
        assert output._active_buffer is None
        assert audio_bus.device.stop_count >= 2
