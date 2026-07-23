# Bestand: midi_routing_diagnostic.py
# Versienommer: 0.20.0
# Doel: Diagnoseer USB-MIDI endpoint routing en event timing sonder audio.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-080 USB MIDI Endpoint Routing Diagnostic
# Actienr: MCP-ACT-080-RED-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-080-START

from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiFactory
from midi_chip_platform.ports import MidiInputPort


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
        self._max_events = int(max_events)
        self._timeout_seconds = float(timeout_seconds)
        self._idle_sleep_seconds = float(idle_sleep_seconds)
        self._event_logging = str(event_logging)
        self._heartbeat_seconds = float(heartbeat_seconds)
        self._scan_all_midi_ports = bool(scan_all_midi_ports)
        self._midi_port_count = int(midi_port_count)

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


class MidiRoutingDiagnosticRuntime:
    def __init__(
        self,
        midi_input,
        profile,
        output=None,
        monotonic=None,
        sleeper=None,
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
        self._event_count = 0
        self._note_on_count = 0
        self._note_off_count = 0
        self._control_count = 0
        self._clock_count = 0
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
        if self._event_count > 0:
            self._output("MIDI_ROUTING_DIAGNOSTIC_STATUS=PASS;" + self._summary_fields())
            return True
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
            else:
                self._note_off_count += 1
        elif isinstance(event, ControlEvent):
            self._control_count += 1
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
        elif isinstance(event, ControlEvent):
            if event.control is not None:
                fields.append(f"control={event.control}")
            fields.append(f"value={event.value}")
        fields.append(f"event_ms={self._elapsed_ms(started_at, now)}")
        return ";".join(fields)

    def _summary_fields(self):
        return (
            f"events={self._event_count};"
            f"note_on={self._note_on_count};"
            f"note_off={self._note_off_count};"
            f"control={self._control_count};"
            f"clock={self._clock_count};"
            f"ignored={self._ignored_count}"
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
        if scan_all_ports:
            midi_input = midi_factory.create_all_inputs()
        else:
            midi_input = midi_factory.create_input(
                port_index=configuration.get("midi.input.port_index", 0)
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
            ),
            output=self._output,
            monotonic=time_module.monotonic,
            sleeper=time_module.sleep,
        )
