# Bestand: midi_routing_diagnostic.py
# Versienommer: 0.20.1
# Doel: Lokaliseer tydelik waar NoteOn eerste in die MIDI-keten verdwyn.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-080-INV-001 Locate First Disappearance Of NoteOn
# Actienr: MCP-ACT-080-INV-001-INSTRUMENT-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-INV-001

from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiFactory
from midi_chip_platform.ports import MidiInputPort


class MidiInvestigationEventClassifier:
    def __init__(self):
        self._classification_count = 0

    @property
    def classification_count(self):
        return self._classification_count

    def classify_domain_event(self, event):
        self._classification_count += 1
        if event is None:
            return MidiInvestigationEventClassification("NO_EVENTS", "none")
        if isinstance(event, NoteEvent):
            if event.message_type == "note_on" and event.velocity > 0:
                return MidiInvestigationEventClassification("NOTEON_PRESENT", "note_on")
            if event.message_type == "note_on" and event.velocity == 0:
                return MidiInvestigationEventClassification(
                    "NOTEOFF_PRESENT",
                    "note_on_velocity_zero",
                )
            return MidiInvestigationEventClassification("NOTEOFF_PRESENT", "note_off")
        if isinstance(event, ControlEvent):
            if event.message_type == "pitch_bend":
                return MidiInvestigationEventClassification("CONTROL_ONLY", "pitch_bend")
            return MidiInvestigationEventClassification("CONTROL_ONLY", "control_change")
        if isinstance(event, ClockEvent):
            return MidiInvestigationEventClassification("CONTROL_ONLY", event.message_type)
        return MidiInvestigationEventClassification("UNKNOWN", "unknown_event")

    def classify_raw_message(self, message):
        self._classification_count += 1
        if message is None:
            return MidiInvestigationEventClassification("NO_EVENTS", "none")
        type_name = message.__class__.__name__.lower()
        if type_name == "noteon" or type_name.endswith(".noteon"):
            if int(getattr(message, "velocity", 0)) == 0:
                return MidiInvestigationEventClassification(
                    "NOTEOFF_PRESENT",
                    "note_on_velocity_zero",
                )
            return MidiInvestigationEventClassification("NOTEON_PRESENT", "note_on")
        if type_name == "noteoff" or type_name.endswith(".noteoff"):
            return MidiInvestigationEventClassification("NOTEOFF_PRESENT", "note_off")
        if type_name == "controlchange" or type_name.endswith(".controlchange"):
            return MidiInvestigationEventClassification("CONTROL_ONLY", "control_change")
        if type_name == "pitchbend" or type_name.endswith(".pitchbend"):
            return MidiInvestigationEventClassification("CONTROL_ONLY", "pitch_bend")
        if type_name == "programchange" or type_name.endswith(".programchange"):
            return MidiInvestigationEventClassification("CONTROL_ONLY", "program_change")
        if "clock" in type_name:
            return MidiInvestigationEventClassification("CONTROL_ONLY", "timing_clock")
        return MidiInvestigationEventClassification("UNKNOWN", type_name)


class MidiInvestigationEventClassification:
    def __init__(self, classification, event_type):
        self._classification = str(classification)
        self._event_type = str(event_type)

    @property
    def classification(self):
        return self._classification

    @property
    def event_type(self):
        return self._event_type


class MidiInvestigationStageCounter:
    def __init__(self, stage, port_index=None):
        self._stage = str(stage)
        self._port_index = port_index
        self._note_on_count = 0
        self._note_off_count = 0
        self._note_on_velocity_zero_count = 0
        self._control_count = 0
        self._cc7_count = 0
        self._clock_count = 0
        self._pitch_bend_count = 0
        self._program_change_count = 0
        self._unknown_count = 0
        self._event_count = 0

    @property
    def stage(self):
        return self._stage

    @property
    def event_count(self):
        return self._event_count

    @property
    def note_on_count(self):
        return self._note_on_count

    @property
    def note_off_count(self):
        return self._note_off_count

    @property
    def classification(self):
        if self._note_on_count > 0:
            return "NOTEON_PRESENT"
        if self._note_off_count > 0 or self._note_on_velocity_zero_count > 0:
            return "NOTEOFF_PRESENT"
        if (
            self._control_count > 0
            or self._clock_count > 0
            or self._pitch_bend_count > 0
            or self._program_change_count > 0
        ):
            return "CONTROL_ONLY"
        if self._unknown_count > 0:
            return "UNKNOWN"
        return "NO_EVENTS"

    def record(self, classification, event_type, event):
        if classification == "NO_EVENTS":
            return
        self._event_count += 1
        if event_type == "note_on":
            self._note_on_count += 1
        elif event_type == "note_on_velocity_zero":
            self._note_on_velocity_zero_count += 1
        elif event_type == "note_off":
            self._note_off_count += 1
        elif event_type == "control_change":
            self._control_count += 1
            if int(getattr(event, "control", -1)) == 7:
                self._cc7_count += 1
        elif event_type == "timing_clock":
            self._clock_count += 1
        elif event_type == "pitch_bend":
            self._pitch_bend_count += 1
        elif event_type == "program_change":
            self._program_change_count += 1
        else:
            self._unknown_count += 1

    def summary_line(self):
        return (
            f"TRACE_SUMMARY;stage={self._stage};"
            f"port_index={self._port_text()};"
            f"classification={self.classification};"
            f"events={self._event_count};"
            f"note_on={self._note_on_count};"
            f"note_off={self._note_off_count};"
            f"note_on_velocity_zero={self._note_on_velocity_zero_count};"
            f"control={self._control_count};"
            f"cc7={self._cc7_count};"
            f"clock={self._clock_count};"
            f"pitch_bend={self._pitch_bend_count};"
            f"program_change={self._program_change_count};"
            f"unknown={self._unknown_count}"
        )

    def _port_text(self):
        if self._port_index is None:
            return "UNKNOWN"
        return str(self._port_index)


class MidiInvestigationTraceObserver:
    def __init__(self, output=None, event_logging="summary", max_trace_lines=96):
        if not callable(output if output is not None else print):
            raise TypeError("output must be callable")
        self._output = output if output is not None else print
        self._event_logging = str(event_logging)
        self._max_trace_lines = max(0, int(max_trace_lines))
        self._trace_line_count = 0
        self._classifier = MidiInvestigationEventClassifier()
        self._counters = {}

    @property
    def trace_line_count(self):
        return self._trace_line_count

    def record_raw_message(self, port_index, message):
        self._record(
            stage=f"USB_ENDPOINT_PORT_{int(port_index)}",
            port_index=int(port_index),
            classification=self._classifier.classify_raw_message(message),
            event=message,
        )

    def record_decoded_event(self, port_index, message, event):
        if message is None:
            self._ensure_counter("ADAFRUIT_MIDI_DECODE", int(port_index))
            return
        if event is None:
            self._record(
                stage="ADAFRUIT_MIDI_DECODE",
                port_index=int(port_index),
                classification=MidiInvestigationEventClassification(
                    "UNKNOWN",
                    "unknown_event",
                ),
                event=message,
            )
            return
        self._record(
            stage="ADAFRUIT_MIDI_DECODE",
            port_index=int(port_index),
            classification=self._classifier.classify_domain_event(event),
            event=event,
        )

    def record_receive_loop_event(self, event):
        self._record(
            stage="MIDI_RECEIVE_LOOP",
            port_index=None,
            classification=self._classifier.classify_domain_event(event),
            event=event,
        )

    def summary_lines(self, port_count):
        for port_index in range(int(port_count)):
            self._ensure_counter(f"USB_ENDPOINT_PORT_{port_index}", port_index)
            self._ensure_counter("ADAFRUIT_MIDI_DECODE", port_index)
        self._ensure_counter("MIDI_RECEIVE_LOOP", None)
        lines = [
            self._counters[key].summary_line()
            for key in sorted(self._counters)
        ]
        lines.extend(
            (
                "TRACE_SUMMARY;stage=ROUTER_INPUT;classification=UNKNOWN;"
                "reason=routing_not_active_in_midi_routing_diagnostic",
                "TRACE_SUMMARY;stage=ROUTER_OUTPUT;classification=UNKNOWN;"
                "reason=routing_not_active_in_midi_routing_diagnostic",
                "TRACE_SUMMARY;stage=SYNTH_DISPATCH;classification=UNKNOWN;"
                "reason=synth_dispatch_not_active_in_midi_routing_diagnostic",
                "TRACE_SUMMARY;stage=D1_NOTE_TRIGGER;classification=UNKNOWN;"
                "reason=d1_not_active_in_midi_routing_diagnostic",
            )
        )
        return tuple(lines)

    def _record(self, stage, port_index, classification, event):
        if classification.classification == "NO_EVENTS":
            self._ensure_counter(stage, port_index)
            return
        counter = self._ensure_counter(stage, port_index)
        counter.record(classification.classification, classification.event_type, event)
        if self._event_logging == "none":
            return
        if self._trace_line_count >= self._max_trace_lines:
            return
        self._trace_line_count += 1
        self._output(
            "TRACE_STAGE="
            f"{stage};port_index={self._port_text(port_index)};"
            f"eventtype={classification.event_type};"
            f"classification={classification.classification};"
            + self._event_fields(event)
            + f";trace_count={self._trace_line_count}"
        )

    def _ensure_counter(self, stage, port_index):
        key = f"{stage}:{self._port_text(port_index)}"
        if key not in self._counters:
            self._counters[key] = MidiInvestigationStageCounter(stage, port_index)
        return self._counters[key]

    def _event_fields(self, event):
        if event is None:
            return "event=none"
        fields = []
        if hasattr(event, "channel") and event.channel is not None:
            fields.append(f"channel={self._domain_channel(event.channel)}")
        if hasattr(event, "note") and event.note is not None:
            fields.append(f"note={event.note}")
        if hasattr(event, "velocity") and event.velocity is not None:
            fields.append(f"velocity={event.velocity}")
        if hasattr(event, "control") and event.control is not None:
            fields.append(f"control={event.control}")
            fields.append(f"cc7={self._bool_text(int(event.control) == 7)}")
        if hasattr(event, "value") and event.value is not None:
            fields.append(f"value={event.value}")
        if hasattr(event, "pitch_bend") and event.pitch_bend is not None:
            fields.append(f"pitch_bend={event.pitch_bend}")
        if not fields:
            fields.append(f"raw_type={event.__class__.__name__}")
        return ";".join(fields)

    @staticmethod
    def _domain_channel(channel):
        if channel is None:
            return "UNKNOWN"
        value = int(channel)
        if value == 0:
            return 1
        return value

    @staticmethod
    def _port_text(port_index):
        if port_index is None:
            return "UNKNOWN"
        return str(port_index)

    @staticmethod
    def _bool_text(value):
        return "true" if bool(value) else "false"


class MidiRoutingDiagnosticProfile:
    def __init__(
        self,
        max_events=16,
        timeout_seconds=60.0,
        idle_sleep_seconds=0.001,
        event_logging="summary",
        heartbeat_seconds=2.0,
        scan_all_midi_ports=True,
        midi_port_count=1,
        max_trace_lines=96,
    ):
        if int(max_events) < 0:
            raise ValueError("max_events must be zero or greater")
        if float(timeout_seconds) < 0:
            raise ValueError("timeout_seconds must be zero or greater")
        if float(idle_sleep_seconds) < 0:
            raise ValueError("idle_sleep_seconds must be zero or greater")
        if float(heartbeat_seconds) < 0:
            raise ValueError("heartbeat_seconds must be zero or greater")
        if str(event_logging) not in ("none", "summary", "verbose"):
            raise ValueError("event_logging must be none, summary or verbose")
        if int(max_trace_lines) < 0:
            raise ValueError("max_trace_lines must be zero or greater")
        self._max_events = int(max_events)
        self._timeout_seconds = float(timeout_seconds)
        self._idle_sleep_seconds = float(idle_sleep_seconds)
        self._event_logging = str(event_logging)
        self._heartbeat_seconds = float(heartbeat_seconds)
        self._scan_all_midi_ports = bool(scan_all_midi_ports)
        self._midi_port_count = int(midi_port_count)
        self._max_trace_lines = int(max_trace_lines)

    @property
    def max_events(self):
        return self._max_events

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
    def heartbeat_seconds(self):
        return self._heartbeat_seconds

    @property
    def scan_all_midi_ports(self):
        return self._scan_all_midi_ports

    @property
    def midi_port_count(self):
        return self._midi_port_count

    @property
    def max_trace_lines(self):
        return self._max_trace_lines


class MidiRoutingDiagnosticRuntime:
    def __init__(
        self,
        midi_input,
        profile,
        output=None,
        monotonic=None,
        sleeper=None,
        trace_observer=None,
    ):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        if not isinstance(profile, MidiRoutingDiagnosticProfile):
            raise TypeError("profile must be MidiRoutingDiagnosticProfile")
        if not callable(output if output is not None else print):
            raise TypeError("output must be callable")
        if not callable(monotonic):
            raise TypeError("monotonic must be callable")
        if not callable(sleeper):
            raise TypeError("sleeper must be callable")
        self._midi_input = midi_input
        self._profile = profile
        self._output = output if output is not None else print
        self._monotonic = monotonic
        self._sleeper = sleeper
        self._trace_observer = trace_observer
        self._event_count = 0
        self._note_on_count = 0
        self._note_off_count = 0
        self._note_on_velocity_zero_count = 0
        self._control_count = 0
        self._cc7_count = 0
        self._clock_count = 0
        self._pitch_bend_count = 0
        self._program_change_count = 0
        self._ignored_count = 0

    @property
    def event_count(self):
        return self._event_count

    @property
    def note_on_count(self):
        return self._note_on_count

    @property
    def note_off_count(self):
        return self._note_off_count

    def run(self):
        started_at = self._monotonic()
        next_heartbeat_at = started_at + self._profile.heartbeat_seconds
        self._output(
            "MIDI_ROUTING_DIAGNOSTIC_STATUS=START;"
            f"scan_all_ports={self._bool_text(self._profile.scan_all_midi_ports)};"
            f"port_count={self._profile.midi_port_count};"
            f"max_events={self._profile.max_events};"
            f"timeout_seconds={self._profile.timeout_seconds:g};"
            f"heartbeat_seconds={self._profile.heartbeat_seconds:g}"
        )
        self._output(
            "TRACE_STAGE=COREMIDI_HOST_SEND;classification=UNKNOWN;"
            "reason=no_host_probe_in_repository"
        )
        self._output(
            "TRACE_STAGE=USB_HOST_DESTINATION;classification=UNKNOWN;"
            "reason=device_firmware_cannot_verify_logic_destination"
        )
        try:
            self._midi_input.open()
            self._output(
                "MIDI_ROUTING_DIAGNOSTIC_INPUT_STATUS=OPEN;"
                f"scan_all_ports={self._bool_text(self._profile.scan_all_midi_ports)};"
                f"port_count={self._profile.midi_port_count}"
            )
            self._output("MIDI_ROUTING_DIAGNOSTIC_READY;ready_ms=0")
            while not self._is_done(started_at):
                event = self._midi_input.receive()
                now = self._monotonic()
                if event is None:
                    if self._should_heartbeat(now, next_heartbeat_at):
                        self._output(
                            "MIDI_ROUTING_HEARTBEAT;"
                            f"elapsed_ms={self._elapsed_ms(started_at, now)};"
                            f"events={self._event_count}"
                        )
                        next_heartbeat_at = now + self._profile.heartbeat_seconds
                    if self._profile.idle_sleep_seconds > 0:
                        self._sleeper(self._profile.idle_sleep_seconds)
                    continue
                if self._trace_observer is not None:
                    self._trace_observer.record_receive_loop_event(event)
                self._record_event(event)
                if self._profile.event_logging != "none":
                    self._output(self._format_event(event, started_at, now))
        except KeyboardInterrupt:
            self._output(
                "MIDI_ROUTING_DIAGNOSTIC_STATUS=INTERRUPTED;"
                + self._summary_fields()
            )
            return True
        except Exception as error:
            self._output(
                "MIDI_ROUTING_DIAGNOSTIC_STATUS=FAIL;"
                f"reason={type(error).__name__};"
                + self._summary_fields()
            )
            return False
        finally:
            self._midi_input.close()
        self._output_trace_summaries()
        self._output(self._first_disappearance_line())
        if self._note_on_count > 0:
            self._output("MIDI_ROUTING_DIAGNOSTIC_STATUS=PASS;" + self._summary_fields())
            return True
        if self._event_count > 0:
            self._output(
                "MIDI_ROUTING_DIAGNOSTIC_STATUS=FAIL;reason=no_noteon_observed;"
                + self._summary_fields()
            )
            return False
        self._output("MIDI_ROUTING_DIAGNOSTIC_STATUS=TIMEOUT;" + self._summary_fields())
        return False

    def _is_done(self, started_at):
        if self._profile.max_events > 0 and self._event_count >= self._profile.max_events:
            return True
        if self._profile.timeout_seconds <= 0:
            return False
        return self._monotonic() - started_at >= self._profile.timeout_seconds

    def _should_heartbeat(self, now, next_heartbeat_at):
        return self._profile.heartbeat_seconds > 0 and now >= next_heartbeat_at

    def _record_event(self, event):
        self._event_count += 1
        if isinstance(event, NoteEvent):
            if event.message_type == "note_on" and event.velocity > 0:
                self._note_on_count += 1
            elif event.message_type == "note_on" and event.velocity == 0:
                self._note_on_velocity_zero_count += 1
                self._note_off_count += 1
            else:
                self._note_off_count += 1
        elif isinstance(event, ControlEvent):
            if event.message_type == "pitch_bend":
                self._pitch_bend_count += 1
            else:
                self._control_count += 1
                if event.control == 7:
                    self._cc7_count += 1
        elif isinstance(event, ClockEvent):
            self._clock_count += 1
        else:
            self._ignored_count += 1

    def _format_event(self, event, started_at, now):
        fields = [
            f"MIDI_ROUTING_EVENT={event.message_type}",
        ]
        if event.channel is not None:
            fields.append(f"channel={event.channel}")
        if isinstance(event, NoteEvent):
            fields.append(f"note={event.note}")
            fields.append(f"velocity={event.velocity}")
            if event.message_type == "note_on" and event.velocity == 0:
                fields.append("velocity_semantics=note_off")
        elif isinstance(event, ControlEvent):
            if event.control is not None:
                fields.append(f"control={event.control}")
                fields.append(f"cc7={self._bool_text(event.control == 7)}")
            fields.append(f"value={event.value}")
        fields.append(f"event_ms={self._elapsed_ms(started_at, now)}")
        return ";".join(fields)

    def _summary_fields(self):
        return (
            f"events={self._event_count};"
            f"note_on={self._note_on_count};"
            f"note_off={self._note_off_count};"
            f"note_on_velocity_zero={self._note_on_velocity_zero_count};"
            f"control={self._control_count};"
            f"cc7={self._cc7_count};"
            f"clock={self._clock_count};"
            f"pitch_bend={self._pitch_bend_count};"
            f"program_change={self._program_change_count};"
            f"ignored={self._ignored_count}"
        )

    def _output_trace_summaries(self):
        if self._trace_observer is None:
            return
        for line in self._trace_observer.summary_lines(self._profile.midi_port_count):
            self._output(line)

    def _first_disappearance_line(self):
        if self._note_on_count == 0 and self._event_count > 0:
            return (
                "FIRST_DISAPPEARANCE_OF_NOTEON=UNKNOWN;"
                "reason=device_observed_no_noteon_and_host_stage_is_unknown"
            )
        if self._note_on_count == 0:
            return (
                "FIRST_DISAPPEARANCE_OF_NOTEON=UNKNOWN;"
                "reason=device_observed_no_events_and_host_stage_is_unknown"
            )
        return (
            "FIRST_DISAPPEARANCE_OF_NOTEON=UNKNOWN;"
            "reason=noteon_seen_at_midi_receive_loop_router_synth_d1_not_active"
        )

    @staticmethod
    def _elapsed_ms(started_at, now):
        return int((float(now) - float(started_at)) * 1000)

    @staticmethod
    def _bool_text(value):
        return "true" if bool(value) else "false"


class MidiRoutingDiagnosticFactory:
    def __init__(self, importer=None, output=None):
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not configuration.get("midi.routing_diagnostic.enabled", False):
            return None
        time_module = self._importer("time")
        midi_factory = CircuitPythonUsbMidiFactory(self._importer)
        scan_all_ports = configuration.get(
            "midi.routing_diagnostic.scan_all_ports", True
        )
        trace_observer = MidiInvestigationTraceObserver(
            output=self._output,
            event_logging=configuration.get(
                "midi.routing_diagnostic.event_logging",
                "summary",
            ),
            max_trace_lines=configuration.get(
                "midi.routing_diagnostic.max_trace_lines",
                96,
            ),
        )
        if scan_all_ports:
            midi_input = midi_factory.create_all_inputs(trace_observer=trace_observer)
        else:
            midi_input = midi_factory.create_input(
                port_index=configuration.get("midi.input.port_index", 0),
                trace_observer=trace_observer,
            )
        return MidiRoutingDiagnosticRuntime(
            midi_input=midi_input,
            profile=MidiRoutingDiagnosticProfile(
                max_events=configuration.get("midi.routing_diagnostic.max_events", 16),
                timeout_seconds=configuration.get(
                    "midi.routing_diagnostic.timeout_seconds", 60.0
                ),
                idle_sleep_seconds=configuration.get(
                    "midi.routing_diagnostic.idle_sleep_seconds", 0.001
                ),
                event_logging=configuration.get(
                    "midi.routing_diagnostic.event_logging", "summary"
                ),
                heartbeat_seconds=configuration.get(
                    "midi.routing_diagnostic.heartbeat_seconds", 2.0
                ),
                scan_all_midi_ports=scan_all_ports,
                midi_port_count=midi_factory.port_count(),
                max_trace_lines=configuration.get(
                    "midi.routing_diagnostic.max_trace_lines",
                    96,
                ),
            ),
            output=self._output,
            monotonic=time_module.monotonic,
            sleeper=time_module.sleep,
            trace_observer=trace_observer,
        )
