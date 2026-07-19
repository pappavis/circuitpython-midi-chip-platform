# Bestand: synthio_runtime.py
# Versienommer: 0.19.2
# Doel: Bewys realtime MIDI-klank met 'n permanente synthio graph en multi-port USB-MIDI scan.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-079 Persistent Synthio Audio Graph Spike
# Actienr: MCP-ACT-079-IMP-002-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-079-HIL-IMPEDIMENT-002

from midi_chip_platform.events import NoteEvent
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiFactory
from midi_chip_platform.ports import ConfigurationPort, MidiInputPort


class SynthioBaselineProfile:
    def __init__(
        self,
        sample_rate=16000,
        channel_count=1,
        max_note_events=0,
        timeout_seconds=0.0,
        idle_sleep_seconds=0.001,
        event_logging="summary",
        boot_audition_note=69,
        boot_audition_seconds=0.6,
        gate_seconds=0.12,
        scan_all_midi_ports=True,
        midi_port_count=1,
    ):
        self._sample_rate = int(sample_rate)
        self._channel_count = int(channel_count)
        self._max_note_events = int(max_note_events)
        self._timeout_seconds = float(timeout_seconds)
        self._idle_sleep_seconds = float(idle_sleep_seconds)
        self._event_logging = str(event_logging).lower()
        self._boot_audition_note = int(boot_audition_note)
        self._boot_audition_seconds = float(boot_audition_seconds)
        self._gate_seconds = float(gate_seconds)
        self._scan_all_midi_ports = bool(scan_all_midi_ports)
        self._midi_port_count = int(midi_port_count)
        self._validate()

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def channel_count(self):
        return self._channel_count

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
    def boot_audition_note(self):
        return self._boot_audition_note

    @property
    def boot_audition_seconds(self):
        return self._boot_audition_seconds

    @property
    def gate_seconds(self):
        return self._gate_seconds

    @property
    def scan_all_midi_ports(self):
        return self._scan_all_midi_ports

    @property
    def midi_port_count(self):
        return self._midi_port_count

    def _validate(self):
        if self._sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self._channel_count not in (1, 2):
            raise ValueError("channel_count must be 1 or 2")
        if self._max_note_events < 0:
            raise ValueError("max_note_events must not be negative")
        if self._timeout_seconds < 0.0:
            raise ValueError("timeout_seconds must not be negative")
        if self._idle_sleep_seconds < 0.0:
            raise ValueError("idle_sleep_seconds must not be negative")
        if self._event_logging not in ("none", "summary", "verbose"):
            raise ValueError("event_logging must be none, summary or verbose")
        if not 0 <= self._boot_audition_note <= 127:
            raise ValueError("boot_audition_note must be between 0 and 127")
        if self._boot_audition_seconds < 0.0:
            raise ValueError("boot_audition_seconds must not be negative")
        if self._gate_seconds < 0.0:
            raise ValueError("gate_seconds must not be negative")
        if self._midi_port_count < 1:
            raise ValueError("midi_port_count must be at least 1")


class CircuitPythonSynthioAudioGraph:
    def __init__(
        self,
        profile,
        importer=None,
        bit_clock_pin_name="IO5",
        word_select_pin_name="IO3",
        data_pin_name="IO7",
    ):
        if not isinstance(profile, SynthioBaselineProfile):
            raise TypeError("profile must be SynthioBaselineProfile")
        self._profile = profile
        self._importer = importer if importer is not None else __import__
        self._bit_clock_pin_name = str(bit_clock_pin_name)
        self._word_select_pin_name = str(word_select_pin_name)
        self._data_pin_name = str(data_pin_name)
        self._audio = None
        self._synth = None

    @property
    def is_open(self):
        return self._audio is not None and self._synth is not None

    def open(self):
        if self.is_open:
            return
        board_module = self._importer("board")
        audiobusio_module = self._importer("audiobusio")
        synthio_module = self._importer("synthio")
        self._audio = audiobusio_module.I2SOut(
            getattr(board_module, self._bit_clock_pin_name),
            getattr(board_module, self._word_select_pin_name),
            getattr(board_module, self._data_pin_name),
        )
        self._synth = synthio_module.Synthesizer(
            sample_rate=self._profile.sample_rate,
            channel_count=self._profile.channel_count,
        )
        self._audio.play(self._synth)

    def press(self, note):
        if not self.is_open:
            raise RuntimeError("synthio audio graph is closed")
        self._synth.press(int(note))

    def release(self, note):
        if not self.is_open:
            raise RuntimeError("synthio audio graph is closed")
        self._synth.release(int(note))

    def release_all(self):
        if not self.is_open:
            return
        self._synth.release_all()

    def close(self):
        if self._synth is not None:
            try:
                self._synth.release_all()
            except Exception:
                pass
            try:
                self._synth.deinit()
            except Exception:
                pass
            self._synth = None
        if self._audio is not None:
            try:
                self._audio.stop()
            except Exception:
                pass
            try:
                self._audio.deinit()
            except Exception:
                pass
            self._audio = None


class SynthioBaselineRuntime:
    def __init__(
        self,
        midi_input,
        audio_graph,
        profile,
        output=None,
        sleeper=None,
    ):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        if not isinstance(profile, SynthioBaselineProfile):
            raise TypeError("profile must be SynthioBaselineProfile")
        self._midi_input = midi_input
        self._audio_graph = audio_graph
        self._profile = profile
        self._output = output if output is not None else print
        self._sleeper = sleeper
        self._started_at = 0.0
        self._ready_at = 0.0
        self._note_on_count = 0
        self._note_off_count = 0
        self._ignored_event_count = 0
        self._scheduled_releases = {}

    @property
    def note_on_count(self):
        return self._note_on_count

    @property
    def note_off_count(self):
        return self._note_off_count

    @property
    def ignored_event_count(self):
        return self._ignored_event_count

    def run(self):
        self._output(
            "SYNTHIO_BASELINE_STATUS=START;"
            f"sample_rate={self._profile.sample_rate};"
            f"channel_count={self._profile.channel_count};"
            f"max_note_events={self._profile.max_note_events};"
            f"timeout_seconds={self._profile.timeout_seconds:g};"
            f"event_logging={self._profile.event_logging};"
            f"boot_audition_seconds={self._profile.boot_audition_seconds:.3f};"
            f"gate_seconds={self._profile.gate_seconds:.3f};"
            f"scan_all_midi_ports={str(self._profile.scan_all_midi_ports).lower()};"
            f"midi_port_count={self._profile.midi_port_count}"
        )
        try:
            self._started_at = self._current_time()
            self._audio_graph.open()
            self._output("SYNTHIO_BASELINE_AUDIO_STATUS=OPEN")
            self._run_boot_audition()
            self._midi_input.open()
            self._output(
                "SYNTHIO_BASELINE_MIDI_INPUT_STATUS=OPEN;"
                f"scan_all_ports={str(self._profile.scan_all_midi_ports).lower()};"
                f"port_count={self._profile.midi_port_count}"
            )
            self._ready_at = self._current_time()
            self._output(
                "SYNTHIO_BASELINE_READY;"
                f"ready_ms={self._milliseconds_between(self._started_at, self._ready_at)}"
            )
            while self._should_continue():
                self._release_notes_if_due()
                event = self._midi_input.receive()
                if event is None:
                    self._sleep_when_idle()
                    continue
                if isinstance(event, NoteEvent):
                    self._handle_note_event(event)
                    continue
                self._ignored_event_count += 1
                self._log_verbose(
                    "SYNTHIO_BASELINE_IGNORED_EVENT="
                    f"{getattr(event, 'message_type', 'unknown')}"
                )
        except KeyboardInterrupt:
            self._output(
                "SYNTHIO_BASELINE_STATUS=INTERRUPTED;"
                f"note_on={self._note_on_count};note_off={self._note_off_count};"
                f"ignored={self._ignored_event_count}"
            )
            return True
        except Exception as error:
            self._output(
                "SYNTHIO_BASELINE_STATUS=FAIL;"
                f"reason={error.__class__.__name__};"
                f"note_on={self._note_on_count};note_off={self._note_off_count};"
                f"ignored={self._ignored_event_count}"
            )
            return False
        finally:
            self._shutdown()
        self._output(
            "SYNTHIO_BASELINE_STATUS=PASS;"
            f"note_on={self._note_on_count};note_off={self._note_off_count};"
            f"ignored={self._ignored_event_count}"
        )
        return True

    def _handle_note_event(self, event):
        if event.is_note_on and event.velocity > 0:
            self._press_note(event)
            return
        self._release_note(event)

    def _press_note(self, event):
        event_at = self._current_time()
        self._audio_graph.press(event.note)
        tone_started_at = self._current_time()
        self._note_on_count += 1
        if self._profile.gate_seconds > 0.0:
            self._scheduled_releases[event.note] = tone_started_at + self._profile.gate_seconds
        self._log_summary(
            "SYNTHIO_BASELINE_NOTE_ON;"
            f"channel={event.channel};note={event.note};velocity={event.velocity};"
            f"event_ms={self._milliseconds_between(self._ready_at, event_at)};"
            f"tone_start_ms={self._milliseconds_between(self._ready_at, tone_started_at)};"
            f"latency_ms={self._milliseconds_between(event_at, tone_started_at)}"
        )

    def _release_note(self, event):
        self._audio_graph.release(event.note)
        self._scheduled_releases.pop(event.note, None)
        self._note_off_count += 1
        self._log_verbose(
            "SYNTHIO_BASELINE_NOTE_OFF;"
            f"channel={event.channel};note={event.note};velocity={event.velocity}"
        )

    def _run_boot_audition(self):
        if self._profile.boot_audition_seconds <= 0.0:
            return
        if self._sleeper is None:
            return
        self._output(
            "SYNTHIO_BASELINE_BOOT_AUDITION=START;"
            f"note={self._profile.boot_audition_note};"
            f"seconds={self._profile.boot_audition_seconds:.3f}"
        )
        self._audio_graph.press(self._profile.boot_audition_note)
        self._sleeper.sleep(self._profile.boot_audition_seconds)
        self._audio_graph.release(self._profile.boot_audition_note)
        self._output("SYNTHIO_BASELINE_BOOT_AUDITION=PASS")

    def _should_continue(self):
        if (
            self._profile.max_note_events > 0
            and self._note_on_count >= self._profile.max_note_events
        ):
            return False
        if self._profile.timeout_seconds > 0.0:
            return self._current_time() - self._started_at < self._profile.timeout_seconds
        return True

    def _release_notes_if_due(self):
        if not self._scheduled_releases:
            return
        now = self._current_time()
        due_notes = tuple(
            note
            for note, release_at in self._scheduled_releases.items()
            if now >= release_at
        )
        for note in due_notes:
            self._audio_graph.release(note)
            self._scheduled_releases.pop(note, None)

    def _sleep_when_idle(self):
        if self._sleeper is not None and self._profile.idle_sleep_seconds > 0.0:
            self._sleeper.sleep(self._profile.idle_sleep_seconds)

    def _shutdown(self):
        try:
            self._audio_graph.release_all()
        except Exception:
            pass
        try:
            self._audio_graph.close()
        except Exception:
            pass
        try:
            self._midi_input.close()
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


class SynthioBaselineRuntimeFactory:
    def __init__(self, importer=None, output=None):
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not isinstance(configuration, ConfigurationPort):
            raise TypeError("configuration must implement ConfigurationPort")
        if not configuration.get("synthio_baseline.enabled", False):
            return None
        profile = SynthioBaselineProfile(
            sample_rate=configuration.get("synthio_baseline.sample_rate", 16000),
            channel_count=configuration.get("synthio_baseline.channel_count", 1),
            max_note_events=configuration.get("synthio_baseline.max_note_events", 0),
            timeout_seconds=configuration.get("synthio_baseline.timeout_seconds", 0.0),
            idle_sleep_seconds=configuration.get(
                "synthio_baseline.idle_sleep_seconds",
                0.001,
            ),
            event_logging=configuration.get("synthio_baseline.event_logging", "summary"),
            boot_audition_note=configuration.get(
                "synthio_baseline.boot_audition_note",
                69,
            ),
            boot_audition_seconds=configuration.get(
                "synthio_baseline.boot_audition_seconds",
                0.6,
            ),
            gate_seconds=configuration.get("synthio_baseline.gate_seconds", 0.12),
            scan_all_midi_ports=configuration.get(
                "synthio_baseline.scan_all_midi_ports",
                True,
            ),
            midi_port_count=self._midi_factory().port_count(),
        )
        midi_factory = self._midi_factory()
        if profile.scan_all_midi_ports:
            midi_input = midi_factory.create_all_inputs()
        else:
            midi_input = midi_factory.create_input(
                port_index=configuration.get("midi.input.port_index", 0)
            )
        return SynthioBaselineRuntime(
            midi_input=midi_input,
            audio_graph=CircuitPythonSynthioAudioGraph(
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

    def _midi_factory(self):
        return CircuitPythonUsbMidiFactory(self._importer)
