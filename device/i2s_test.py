# Bestand: i2s_test.py
# Versienommer: 0.14.0
# Doel: Speel 'n onafhanklike G3-C4-D4 square-wave I2S hardewarediagnose.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-016 Standalone I2S Audible Diagnostic
# Actienr: MCP-ACT-016-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-016-START


class I2sDiagnosticProfile:
    def __init__(
        self,
        bit_clock_pin_name="IO5",
        word_select_pin_name="IO3",
        data_pin_name="IO7",
        sample_rate=16000,
        amplitude=4096,
        note_duration_seconds=0.35,
        gap_duration_seconds=0.08,
        notes=None,
    ):
        self._bit_clock_pin_name = str(bit_clock_pin_name)
        self._word_select_pin_name = str(word_select_pin_name)
        self._data_pin_name = str(data_pin_name)
        self._sample_rate = int(sample_rate)
        self._amplitude = int(amplitude)
        self._note_duration_seconds = float(note_duration_seconds)
        self._gap_duration_seconds = float(gap_duration_seconds)
        self._notes = tuple(
            notes
            if notes is not None
            else (("G3", 196.0), ("C4", 261.63), ("D4", 293.66))
        )
        self._validate()

    @property
    def bit_clock_pin_name(self):
        return self._bit_clock_pin_name

    @property
    def word_select_pin_name(self):
        return self._word_select_pin_name

    @property
    def data_pin_name(self):
        return self._data_pin_name

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def amplitude(self):
        return self._amplitude

    @property
    def note_duration_seconds(self):
        return self._note_duration_seconds

    @property
    def gap_duration_seconds(self):
        return self._gap_duration_seconds

    @property
    def notes(self):
        return self._notes

    def _validate(self):
        if self._sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if not 1 <= self._amplitude <= 8191:
            raise ValueError("amplitude must be between 1 and 8191")
        if self._note_duration_seconds <= 0:
            raise ValueError("note_duration_seconds must be positive")
        if self._gap_duration_seconds < 0:
            raise ValueError("gap_duration_seconds must not be negative")
        if not self._notes:
            raise ValueError("notes must not be empty")


class SquareWaveTone:
    def __init__(self, buffer, raw_sample, actual_frequency):
        self._buffer = buffer
        self._raw_sample = raw_sample
        self._actual_frequency = float(actual_frequency)

    @property
    def buffer(self):
        return self._buffer

    @property
    def raw_sample(self):
        return self._raw_sample

    @property
    def actual_frequency(self):
        return self._actual_frequency


class SquareWaveSampleFactory:
    def __init__(self, array_module, audio_core_module):
        self._array_module = array_module
        self._audio_core_module = audio_core_module

    def create(self, profile, frequency):
        if not isinstance(profile, I2sDiagnosticProfile):
            raise TypeError("profile must be I2sDiagnosticProfile")
        selected_frequency = float(frequency)
        if selected_frequency <= 0:
            raise ValueError("frequency must be positive")
        period_length = max(2, int(round(profile.sample_rate / selected_frequency)))
        low_value = 32768 - profile.amplitude
        high_value = 32768 + profile.amplitude
        half_period = period_length // 2
        values = [high_value if index < half_period else low_value for index in range(period_length)]
        buffer = self._array_module.array("H", values)
        raw_sample = self._audio_core_module.RawSample(
            buffer,
            sample_rate=profile.sample_rate,
        )
        return SquareWaveTone(
            buffer=buffer,
            raw_sample=raw_sample,
            actual_frequency=profile.sample_rate / period_length,
        )


class I2sDiagnosticApplication:
    def __init__(self, profile=None, importer=None, output=None):
        self._profile = profile if profile is not None else I2sDiagnosticProfile()
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def run(self):
        audio_output = None
        gc_module = None
        heap_before = None
        try:
            modules = self._load_modules()
            gc_module = modules[4]
            gc_module.collect()
            heap_before = gc_module.mem_free()
            self._write_start(heap_before)
            board_module = modules[3]
            audio_output = modules[1].I2SOut(
                getattr(board_module, self._profile.bit_clock_pin_name),
                getattr(board_module, self._profile.word_select_pin_name),
                getattr(board_module, self._profile.data_pin_name),
            )
            factory = SquareWaveSampleFactory(modules[0], modules[2])
            time_module = modules[5]
            for note_name, frequency in self._profile.notes:
                tone = factory.create(self._profile, frequency)
                self._output(
                    "I2S_NOTE="
                    + str(note_name)
                    + ";requested_hz="
                    + str(frequency)
                    + ";actual_hz="
                    + str(tone.actual_frequency)
                )
                audio_output.play(tone.raw_sample, loop=True)
                time_module.sleep(self._profile.note_duration_seconds)
                audio_output.stop()
                time_module.sleep(self._profile.gap_duration_seconds)
            gc_module.collect()
            heap_after = gc_module.mem_free()
            self._output(
                "I2S_DIAGNOSTIC_STATUS=PASS;notes="
                + str(len(self._profile.notes))
                + ";heap_before="
                + str(heap_before)
                + ";heap_after="
                + str(heap_after)
            )
            return True
        except Exception as error:
            self._output(
                "I2S_DIAGNOSTIC_STATUS=FAIL;error="
                + type(error).__name__
                + ";message="
                + str(error)
            )
            return False
        finally:
            if audio_output is not None:
                try:
                    audio_output.stop()
                except Exception:
                    pass
                audio_output.deinit()
            if gc_module is not None:
                gc_module.collect()

    def _load_modules(self):
        return (
            self._importer("array"),
            self._importer("audiobusio"),
            self._importer("audiocore"),
            self._importer("board"),
            self._importer("gc"),
            self._importer("time"),
        )

    def _write_start(self, heap_before):
        self._output(
            "circuitpython-midi-chip-platform v0.14.0 | "
            "story=MCP-US-016 | release-date=2026-07-16"
        )
        self._output(
            "I2S_DIAGNOSTIC_STATUS=START;backend=max98357a-mono;"
            "bclk="
            + self._profile.bit_clock_pin_name
            + ";ws="
            + self._profile.word_select_pin_name
            + ";data="
            + self._profile.data_pin_name
            + ";sample_rate="
            + str(self._profile.sample_rate)
            + ";heap_before="
            + str(heap_before)
        )


if __name__ == "__main__":
    I2sDiagnosticApplication().run()
