# Bestand: midi_usb.py
# Versienommer: 0.19.3
# Doel: Vertaal USB-MIDI en isoleer foutiewe multi-port endpoints vir synthio diagnose.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-079 Persistent Synthio Audio Graph Spike
# Actienr: MCP-ACT-079-IMP-003-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-079-HIL-IMPEDIMENT-003

from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.ports import MidiInputPort


class MidiMessageTypes:
    def __init__(
        self,
        note_on_type,
        note_off_type,
        control_change_type=None,
        pitch_bend_type=None,
        timing_clock_type=None,
        start_type=None,
        stop_type=None,
        continue_type=None,
    ):
        self._note_on_type = note_on_type
        self._note_off_type = note_off_type
        self._control_change_type = control_change_type
        self._pitch_bend_type = pitch_bend_type
        self._timing_clock_type = timing_clock_type
        self._start_type = start_type
        self._stop_type = stop_type
        self._continue_type = continue_type

    @property
    def note_on_type(self):
        return self._note_on_type

    @property
    def note_off_type(self):
        return self._note_off_type

    @property
    def control_change_type(self):
        return self._control_change_type

    @property
    def pitch_bend_type(self):
        return self._pitch_bend_type

    @property
    def timing_clock_type(self):
        return self._timing_clock_type

    @property
    def start_type(self):
        return self._start_type

    @property
    def stop_type(self):
        return self._stop_type

    @property
    def continue_type(self):
        return self._continue_type


class MidiMessageTranslator:
    def __init__(self, message_types):
        if not isinstance(message_types, MidiMessageTypes):
            raise TypeError("message_types must be MidiMessageTypes")
        self._message_types = message_types

    def translate(self, message):
        if message is None:
            return None
        if isinstance(message, self._message_types.note_on_type):
            return NoteEvent.note_on(self._domain_channel(message), message.note, message.velocity)
        if isinstance(message, self._message_types.note_off_type):
            return NoteEvent.note_off(self._domain_channel(message), message.note, message.velocity)
        if self._matches(message, self._message_types.control_change_type):
            return ControlEvent.control_change(
                self._domain_channel(message), message.control, message.value
            )
        if self._matches(message, self._message_types.pitch_bend_type):
            return ControlEvent.pitch_bend(self._domain_channel(message), message.pitch_bend)
        if self._matches(message, self._message_types.timing_clock_type):
            return ClockEvent.timing_clock()
        if self._matches(message, self._message_types.start_type):
            return ClockEvent.start()
        if self._matches(message, self._message_types.stop_type):
            return ClockEvent.stop()
        if self._matches(message, self._message_types.continue_type):
            return ClockEvent.continue_playback()
        return None

    @staticmethod
    def _domain_channel(message):
        return int(message.channel) + 1

    @staticmethod
    def _matches(message, expected_type):
        return expected_type is not None and isinstance(message, expected_type)


class UsbMidiInputPort(MidiInputPort):
    def __init__(self, factory, translator, port_index=0):
        if not isinstance(translator, MidiMessageTranslator):
            raise TypeError("translator must be MidiMessageTranslator")
        if int(port_index) < 0:
            raise ValueError("port_index must be zero or greater")
        self._factory = factory
        self._translator = translator
        self._port_index = int(port_index)
        self._raw_midi = None

    @property
    def is_open(self):
        return self._raw_midi is not None

    def open(self):
        if not self.is_open:
            self._raw_midi = self._factory.create(self._port_index)

    def receive(self):
        if not self.is_open:
            raise RuntimeError("USB MIDI input is closed")
        return self._translator.translate(self._raw_midi.receive())

    def close(self):
        self._raw_midi = None


class MultiUsbMidiInputPort(MidiInputPort):
    def __init__(self, midi_inputs):
        self._midi_inputs = tuple(midi_inputs)
        if not self._midi_inputs:
            raise ValueError("multi USB MIDI input requires at least one port")
        self._is_open = False
        self._next_index = 0
        self._disabled_indexes = set()

    @property
    def is_open(self):
        return self._is_open

    @property
    def port_count(self):
        return len(self._midi_inputs)

    @property
    def active_port_count(self):
        return len(self._midi_inputs) - len(self._disabled_indexes)

    def open(self):
        if self._is_open:
            return
        self._disabled_indexes.clear()
        for index, midi_input in enumerate(self._midi_inputs):
            try:
                midi_input.open()
            except (AttributeError, ValueError, OSError, RuntimeError):
                self._disabled_indexes.add(index)
        self._is_open = True

    def receive(self):
        if not self._is_open:
            raise RuntimeError("USB MIDI input is closed")
        for offset in range(len(self._midi_inputs)):
            index = (self._next_index + offset) % len(self._midi_inputs)
            if index in self._disabled_indexes:
                continue
            try:
                event = self._midi_inputs[index].receive()
            except (AttributeError, ValueError, OSError, RuntimeError):
                self._disabled_indexes.add(index)
                continue
            if event is not None:
                self._next_index = (index + 1) % len(self._midi_inputs)
                return event
        return None

    def close(self):
        for index, midi_input in enumerate(self._midi_inputs):
            if index in self._disabled_indexes:
                continue
            midi_input.close()
        self._is_open = False


class AdafruitMidiObjectFactory:
    def __init__(self, midi_class, usb_midi_module):
        self._midi_class = midi_class
        self._usb_midi_module = usb_midi_module

    def create(self, port_index):
        ports = self._usb_midi_module.ports
        if int(port_index) >= len(ports):
            raise ValueError("USB MIDI input port index is unavailable")
        return self._midi_class(midi_in=ports[int(port_index)], in_channel=None)


class CircuitPythonUsbMidiFactory:
    def __init__(self, importer=None):
        self._importer = importer if importer is not None else __import__

    def create_input(self, port_index=0):
        adafruit_midi = self._importer("adafruit_midi", None, None, ("MIDI",))
        usb_midi = self._importer("usb_midi")
        message_types = self._create_message_types()
        return UsbMidiInputPort(
            factory=AdafruitMidiObjectFactory(adafruit_midi.MIDI, usb_midi),
            translator=MidiMessageTranslator(message_types),
            port_index=port_index,
        )

    def create_all_inputs(self):
        adafruit_midi = self._importer("adafruit_midi", None, None, ("MIDI",))
        usb_midi = self._importer("usb_midi")
        message_types = self._create_message_types()
        midi_inputs = tuple(
            UsbMidiInputPort(
                factory=AdafruitMidiObjectFactory(adafruit_midi.MIDI, usb_midi),
                translator=MidiMessageTranslator(message_types),
                port_index=port_index,
            )
            for port_index in range(len(usb_midi.ports))
        )
        return MultiUsbMidiInputPort(midi_inputs)

    def port_count(self):
        return len(self._importer("usb_midi").ports)

    def _create_message_types(self):
        return MidiMessageTypes(
            note_on_type=self._message_type("adafruit_midi.note_on", "NoteOn"),
            note_off_type=self._message_type("adafruit_midi.note_off", "NoteOff"),
            control_change_type=self._message_type(
                "adafruit_midi.control_change", "ControlChange"
            ),
            pitch_bend_type=self._message_type("adafruit_midi.pitch_bend", "PitchBend"),
            timing_clock_type=self._optional_message_type(
                "adafruit_midi.timing_clock", "TimingClock"
            ),
            start_type=self._optional_message_type("adafruit_midi.start", "Start"),
            stop_type=self._optional_message_type("adafruit_midi.stop", "Stop"),
            continue_type=self._optional_message_type(
                "adafruit_midi.midi_continue", "Continue"
            ),
        )

    def _message_type(self, module_name, class_name):
        module = self._importer(module_name, None, None, (class_name,))
        return getattr(module, class_name)

    def _optional_message_type(self, module_name, class_name):
        try:
            return self._message_type(module_name, class_name)
        except (ImportError, AttributeError):
            return None


class MidiReceiveLoop:
    def __init__(self, midi_input, event_consumer, event_processor=None):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        self._midi_input = midi_input
        self._event_consumer = event_consumer
        self._event_processor = event_processor
        self._received_count = 0

    @property
    def received_count(self):
        return self._received_count

    def poll_once(self):
        event = self._midi_input.receive()
        if event is None:
            return False
        events = (event,)
        if self._event_processor is not None:
            events = self._event_processor.process(event)
        for processed_event in events:
            self._event_consumer(processed_event)
        self._received_count += 1
        return True


class UsbMidiReceiveDiagnostic:
    def __init__(
        self,
        midi_input,
        output=None,
        monotonic=None,
        sleeper=None,
        max_events=8,
        timeout_seconds=60.0,
        poll_interval_seconds=0.01,
    ):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        if not callable(output if output is not None else print):
            raise TypeError("output must be callable")
        if not callable(monotonic):
            raise TypeError("monotonic must be callable")
        if not callable(sleeper):
            raise TypeError("sleeper must be callable")
        if int(max_events) < 2:
            raise ValueError("max_events must be at least 2")
        if float(timeout_seconds) <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if float(poll_interval_seconds) <= 0:
            raise ValueError("poll_interval_seconds must be greater than zero")
        self._midi_input = midi_input
        self._output = output if output is not None else print
        self._monotonic = monotonic
        self._sleeper = sleeper
        self._max_events = int(max_events)
        self._timeout_seconds = float(timeout_seconds)
        self._poll_interval_seconds = float(poll_interval_seconds)

    def run(self):
        event_count = 0
        note_on_count = 0
        note_off_count = 0
        matched_note_count = 0
        active_notes = set()
        started_at = self._monotonic()
        self._output(
            "USB_MIDI_DIAGNOSTIC_STATUS=READY;"
            f"max_events={self._max_events};timeout_seconds={self._timeout_seconds:g}"
        )
        try:
            self._midi_input.open()
            while event_count < self._max_events:
                if self._monotonic() - started_at >= self._timeout_seconds:
                    break
                event = self._midi_input.receive()
                if not isinstance(event, NoteEvent):
                    self._sleeper(self._poll_interval_seconds)
                    continue
                message_type = self._normalized_message_type(event)
                key = (event.channel, event.note)
                event_count += 1
                if message_type == "note_on":
                    note_on_count += 1
                    active_notes.add(key)
                else:
                    note_off_count += 1
                    if key in active_notes:
                        active_notes.remove(key)
                        matched_note_count += 1
                self._output(
                    f"USB_MIDI_EVENT={message_type};channel={event.channel};"
                    f"note={event.note};velocity={event.velocity}"
                )
                if matched_note_count > 0:
                    break
        except Exception:
            self._output("USB_MIDI_DIAGNOSTIC_STATUS=FAIL;reason=input-error")
            return False
        finally:
            self._midi_input.close()
        summary = (
            f"events={event_count};note_on={note_on_count};"
            f"note_off={note_off_count};matched_notes={matched_note_count}"
        )
        if matched_note_count > 0:
            self._output(f"USB_MIDI_DIAGNOSTIC_STATUS=PASS;{summary}")
            return True
        self._output(
            "USB_MIDI_DIAGNOSTIC_STATUS=FAIL;reason=incomplete-note-pair;"
            f"{summary}"
        )
        return False

    @staticmethod
    def _normalized_message_type(event):
        if event.message_type == "note_on" and event.velocity == 0:
            return "note_off"
        return event.message_type


class CircuitPythonUsbMidiDiagnosticFactory:
    def __init__(self, importer=None, output=None):
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not configuration.get("midi.diagnostic.enabled", False):
            return None
        time_module = self._importer("time")
        midi_input = CircuitPythonUsbMidiFactory(self._importer).create_input(
            port_index=configuration.get("midi.input.port_index", 0)
        )
        return UsbMidiReceiveDiagnostic(
            midi_input=midi_input,
            output=self._output,
            monotonic=time_module.monotonic,
            sleeper=time_module.sleep,
            max_events=configuration.get("midi.diagnostic.max_events", 8),
            timeout_seconds=configuration.get("midi.diagnostic.timeout_seconds", 60),
            poll_interval_seconds=configuration.get(
                "midi.diagnostic.poll_interval_seconds", 0.01
            ),
        )
