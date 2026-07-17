# Bestand: realtime_baseline.py
# Versienommer: 0.18.1
# Doel: Bewys realtime MIDI en direkte I2S-audio met boot-audition en min logging.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-077 Realtime MIDI Audio Baseline Spike
# Actienr: MCP-ACT-077-IMP-001-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-IMPEDIMENT-001

from midi_chip_platform.events import NoteEvent
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiFactory
from midi_chip_platform.ports import ConfigurationPort, MidiInputPort


class RealtimeBaselineProfile:
    def __init__(
        self,
        sample_rate=16000,
        frequency_hz=440.0,
        amplitude=4096,
        tone_seconds=0.12,
        max_note_events=0,
        timeout_seconds=0.0,
        idle_sleep_seconds=0.0,
        event_logging="none",
        boot_audition_seconds=0.6,
    ):
        self._sample_rate = int(sample_rate)
        self._frequency_hz = float(frequency_hz)
        self._amplitude = int(amplitude)
        self._tone_seconds = float(tone_seconds)
        self._max_note_events = int(max_note_events)
        self._timeout_seconds = float(timeout_seconds)
        self._idle_sleep_seconds = float(idle_sleep_seconds)
        self._event_logging = str(event_logging).lower()
        self._boot_audition_seconds = float(boot_audition_seconds)
        self._validate()

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def frequency_hz(self):
        return self._frequency_hz

    @property
    def amplitude(self):
        return self._amplitude

    @property
    def tone_seconds(self):
        return self._tone_seconds

    @property
    def max_note_events(self):
        return self._max_note_events

    @property
    def timeout_seconds(self):
        return self._timeout_seconds

    @property
    def idle_sleep_seconds(self):
        return self._idle_sleep_seconds

    @property
    def event_logging(self):
        return self._event_logging

    @property
    def boot_audition_seconds(self):
        return self._boot_audition_seconds

    def _validate(self):
        if self._sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self._frequency_hz <= 0.0:
            raise ValueError("frequency_hz must be positive")
        if not 1 <= self._amplitude <= 32767:
            raise ValueError("amplitude must be between 1 and 32767")
        if self._tone_seconds <= 0.0:
            raise ValueError("tone_seconds must be positive")
        if self._max_note_events < 0:
            raise ValueError("max_note_events must not be negative")
        if self._timeout_seconds < 0.0:
            raise ValueError("timeout_seconds must not be negative")
        if self._idle_sleep_seconds < 0.0:
            raise ValueError("idle_sleep_seconds must not be negative")
        if self._event_logging not in ("none", "summary", "verbose"):
            raise ValueError("event_logging must be none, summary or verbose")
        if self._boot_audition_seconds < 0.0:
            raise ValueError("boot_audition_seconds must not be negative")


class CircuitPythonPrecomputedI2sToneOutput:
    def __init__(
        self,
        profile,
        importer=None,
        bit_clock_pin_name="IO5",
        word_select_pin_name="IO3",
        data_pin_name="IO7",
    ):
        if not isinstance(profile, RealtimeBaselineProfile):
            raise TypeError("profile must be RealtimeBaselineProfile")
        self._profile = profile
        self._importer = importer if importer is not None else __import__
        self._bit_clock_pin_name = str(bit_clock_pin_name)
        self._word_select_pin_name = str(word_select_pin_name)
        self._data_pin_name = str(data_pin_name)
        self._device = None
        self._raw_sample = None
        self._actual_frequency_hz = None
        self._is_playing = False

    @property
    def actual_frequency_hz(self):
        return self._actual_frequency_hz

    @property
    def is_open(self):
        return self._device is not None

    @property
    def is_playing(self):
        return self._is_playing

    def open(self):
        if self.is_open:
            return
        board_module = self._importer("board")
        audiobusio_module = self._importer("audiobusio")
        audiocore_module = self._importer("audiocore")
        array_module = self._importer("array")
        self._device = audiobusio_module.I2SOut(
            getattr(board_module, self._bit_clock_pin_name),
            getattr(board_module, self._word_select_pin_name),
            getattr(board_module, self._data_pin_name),
        )
        period_length = max(
            2,
            int(round(self._profile.sample_rate / self._profile.frequency_hz)),
        )
        half_period = max(1, period_length // 2)
        low_value = 32768 - self._profile.amplitude
        high_value = 32768 + self._profile.amplitude
        values = [
            high_value if index < half_period else low_value
            for index in range(period_length)
        ]
        self._raw_sample = audiocore_module.RawSample(
            array_module.array("H", values),
            sample_rate=self._profile.sample_rate,
        )
        self._actual_frequency_hz = self._profile.sample_rate / period_length

    def start(self):
        if not self.is_open:
            raise RuntimeError("baseline I2S output is closed")
        self._device.play(self._raw_sample, loop=True)
        self._is_playing = True

    def stop(self):
        if self._device is not None:
            self._device.stop()
        self._is_playing = False

    def play_for_duration(self, duration_seconds, sleeper):
        if not self.is_open:
            raise RuntimeError("baseline I2S output is closed")
        self.start()
        sleeper.sleep(float(duration_seconds))
        self.stop()

    def close(self):
        if self._device is None:
            return
        self.stop()
        self._device.deinit()
        self._device = None
        self._raw_sample = None


class NullBaselineTimingMarker:
    def __init__(self):
        self._begin_count = 0
        self._end_count = 0

    @property
    def begin_count(self):
        return self._begin_count

    @property
    def end_count(self):
        return self._end_count

    def open(self):
        return None

    def begin_audio_start(self):
        self._begin_count += 1

    def end_audio_start(self):
        self._end_count += 1

    def close(self):
        return None


class RealtimeMidiAudioBaselineRuntime:
    def __init__(
        self,
        midi_input,
        tone_output,
        profile,
        output=None,
        sleeper=None,
        timing_marker=None,
    ):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        if not isinstance(profile, RealtimeBaselineProfile):
            raise TypeError("profile must be RealtimeBaselineProfile")
        self._midi_input = midi_input
        self._tone_output = tone_output
        self._profile = profile
        self._output = output if output is not None else print
        self._sleeper = sleeper
        self._timing_marker = (
            timing_marker if timing_marker is not None else NullBaselineTimingMarker()
        )
        self._note_on_count = 0
        self._ignored_event_count = 0
        self._started_at = 0.0
        self._ready_at = 0.0
        self._tone_stop_at = None

    @property
    def note_on_count(self):
        return self._note_on_count

    @property
    def ignored_event_count(self):
        return self._ignored_event_count

    def run(self):
        self._output(
            "REALTIME_BASELINE_STATUS=START;"
            f"sample_rate={self._profile.sample_rate};"
            f"frequency_hz={self._profile.frequency_hz:.3f};"
            f"tone_seconds={self._profile.tone_seconds:.3f};"
            f"max_note_events={self._profile.max_note_events};"
            f"timeout_seconds={self._profile.timeout_seconds:g};"
            f"event_logging={self._profile.event_logging};"
            f"boot_audition_seconds={self._profile.boot_audition_seconds:.3f}"
        )
        try:
            self._started_at = self._current_time()
            self._timing_marker.open()
            self._midi_input.open()
            self._tone_output.open()
            self._output(
                "REALTIME_BASELINE_AUDIO_STATUS=OPEN;"
                f"actual_frequency_hz={self._tone_output.actual_frequency_hz:.3f}"
            )
            self._run_boot_audition()
            self._output("REALTIME_BASELINE_MIDI_INPUT_STATUS=OPEN")
            self._ready_at = self._current_time()
            self._output(
                "REALTIME_BASELINE_READY;"
                f"ready_ms={self._milliseconds_between(self._started_at, self._ready_at)}"
            )
            while self._should_continue():
                self._stop_tone_if_due()
                event = self._midi_input.receive()
                if event is None:
                    self._sleep_when_idle()
                    continue
                if isinstance(event, NoteEvent) and event.is_note_on and event.velocity > 0:
                    self._start_note(event)
                    continue
                self._ignored_event_count += 1
                self._log_verbose(
                    "REALTIME_BASELINE_IGNORED_EVENT="
                    f"{getattr(event, 'message_type', 'unknown')}"
                )
        except KeyboardInterrupt:
            self._output(
                "REALTIME_BASELINE_STATUS=INTERRUPTED;"
                f"note_on={self._note_on_count};ignored={self._ignored_event_count}"
            )
            return True
        except Exception as error:
            self._output(
                "REALTIME_BASELINE_STATUS=FAIL;"
                f"reason={error.__class__.__name__};"
                f"note_on={self._note_on_count};ignored={self._ignored_event_count}"
            )
            return False
        finally:
            self._shutdown()
        self._output(
            "REALTIME_BASELINE_STATUS=PASS;"
            f"note_on={self._note_on_count};ignored={self._ignored_event_count}"
        )
        return True

    def _start_note(self, event):
        event_at = self._current_time()
        self._timing_marker.begin_audio_start()
        try:
            self._tone_output.start()
        finally:
            self._timing_marker.end_audio_start()
        tone_started_at = self._current_time()
        self._tone_stop_at = tone_started_at + self._profile.tone_seconds
        self._note_on_count += 1
        self._log_summary(
            "REALTIME_BASELINE_NOTE_ON;"
            f"channel={event.channel};note={event.note};velocity={event.velocity};"
            f"event_ms={self._milliseconds_between(self._ready_at, event_at)};"
            f"tone_start_ms={self._milliseconds_between(self._ready_at, tone_started_at)};"
            f"latency_ms={self._milliseconds_between(event_at, tone_started_at)}"
        )

    def _run_boot_audition(self):
        if self._profile.boot_audition_seconds <= 0.0:
            return
        if self._sleeper is None or not hasattr(self._tone_output, "play_for_duration"):
            return
        self._output(
            "REALTIME_BASELINE_BOOT_AUDITION=START;"
            f"seconds={self._profile.boot_audition_seconds:.3f}"
        )
        self._tone_output.play_for_duration(
            self._profile.boot_audition_seconds,
            self._sleeper,
        )
        self._output("REALTIME_BASELINE_BOOT_AUDITION=PASS")

    def _should_continue(self):
        if (
            self._profile.max_note_events > 0
            and self._note_on_count >= self._profile.max_note_events
        ):
            return False
        if self._profile.timeout_seconds > 0.0:
            return self._current_time() - self._started_at < self._profile.timeout_seconds
        return True

    def _stop_tone_if_due(self):
        if self._tone_stop_at is None:
            return
        if self._current_time() >= self._tone_stop_at:
            self._tone_output.stop()
            self._tone_stop_at = None

    def _sleep_when_idle(self):
        if self._sleeper is not None and self._profile.idle_sleep_seconds > 0.0:
            self._sleeper.sleep(self._profile.idle_sleep_seconds)

    def _shutdown(self):
        try:
            self._tone_output.stop()
        except Exception:
            pass
        try:
            self._tone_output.close()
        except Exception:
            pass
        try:
            self._midi_input.close()
        except Exception:
            pass
        try:
            self._timing_marker.close()
        except Exception:
            pass

    def _current_time(self):
        if self._sleeper is not None and hasattr(self._sleeper, "monotonic"):
            return float(self._sleeper.monotonic())
        return 0.0

    @staticmethod
    def _milliseconds_between(started_at, ended_at):
        return int(round((float(ended_at) - float(started_at)) * 1000.0))

    def _log_summary(self, message):
        if self._profile.event_logging in ("summary", "verbose"):
            self._output(message)

    def _log_verbose(self, message):
        if self._profile.event_logging == "verbose":
            self._output(message)


class RealtimeMidiAudioBaselineFactory:
    def __init__(self, importer=None, output=None):
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not isinstance(configuration, ConfigurationPort):
            raise TypeError("configuration must implement ConfigurationPort")
        if not configuration.get("realtime_baseline.enabled", False):
            return None
        profile = RealtimeBaselineProfile(
            sample_rate=configuration.get("realtime_baseline.sample_rate", 16000),
            frequency_hz=configuration.get("realtime_baseline.frequency_hz", 440.0),
            amplitude=configuration.get("realtime_baseline.amplitude", 4096),
            tone_seconds=configuration.get("realtime_baseline.tone_seconds", 0.12),
            max_note_events=configuration.get("realtime_baseline.max_note_events", 0),
            timeout_seconds=configuration.get("realtime_baseline.timeout_seconds", 0.0),
            idle_sleep_seconds=configuration.get("realtime_baseline.idle_sleep_seconds", 0.0),
            event_logging=configuration.get("realtime_baseline.event_logging", "none"),
            boot_audition_seconds=configuration.get(
                "realtime_baseline.boot_audition_seconds",
                0.6,
            ),
        )
        return RealtimeMidiAudioBaselineRuntime(
            midi_input=CircuitPythonUsbMidiFactory(self._importer).create_input(
                port_index=configuration.get("midi.input.port_index", 0)
            ),
            tone_output=CircuitPythonPrecomputedI2sToneOutput(
                profile=profile,
                importer=self._importer,
                bit_clock_pin_name=configuration.get("audio.i2s.bit_clock", "IO5"),
                word_select_pin_name=configuration.get("audio.i2s.word_select", "IO3"),
                data_pin_name=configuration.get("audio.i2s.data", "IO7"),
            ),
            profile=profile,
            output=self._output,
            sleeper=self._importer("time"),
        )
