# Bestand: test_usb_midi_receive.py
# Versienommer: 0.12.1
# Doel: Bewys USB-MIDI-vertaling en begrensde Note On/Off-HIL-diagnostiek sonder hardeware.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-007 USB MIDI Receive Loop
# Actienr: MCP-ACT-007-IMP-004-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007

from midi_chip_platform.events import NoteEvent
from midi_chip_platform.midi_usb import (
    CircuitPythonUsbMidiFactory,
    MidiMessageTranslator,
    MidiMessageTypes,
    UsbMidiInputPort,
    UsbMidiReceiveDiagnostic,
)
from midi_chip_platform.testing import MemoryMidiInput


class TestUsbMidiReceive:
    class NoteOn:
        def __init__(self, note, velocity, channel=0):
            self.note = note
            self.velocity = velocity
            self.channel = channel

    class NoteOff:
        def __init__(self, note, velocity=0, channel=0):
            self.note = note
            self.velocity = velocity
            self.channel = channel

    class ControlChange:
        def __init__(self, control, value, channel=0):
            self.control = control
            self.value = value
            self.channel = channel

    class PitchBend:
        def __init__(self, pitch_bend, channel=0):
            self.pitch_bend = pitch_bend
            self.channel = channel

    class TimingClock:
        pass

    class Unknown:
        pass

    class RawMidi:
        def __init__(self, messages):
            self._messages = list(messages)

        def receive(self):
            if not self._messages:
                return None
            return self._messages.pop(0)

    class Factory:
        def __init__(self, raw_midi):
            self._raw_midi = raw_midi
            self.requested_port_index = None

        def create(self, port_index):
            self.requested_port_index = port_index
            return self._raw_midi

    class ModuleStub:
        def __init__(self, **attributes):
            for name, value in attributes.items():
                setattr(self, name, value)

    class PositionalOnlyImporter:
        def __init__(self, modules):
            self._modules = dict(modules)
            self.calls = []

        def __call__(self, *arguments):
            self.calls.append(arguments)
            module_name = arguments[0]
            if module_name not in self._modules:
                raise ImportError(module_name)
            return self._modules[module_name]

    def _translator(self):
        return MidiMessageTranslator(
            MidiMessageTypes(
                note_on_type=self.NoteOn,
                note_off_type=self.NoteOff,
                control_change_type=self.ControlChange,
                pitch_bend_type=self.PitchBend,
                timing_clock_type=self.TimingClock,
            )
        )

    def test_translates_note_and_control_messages_to_portable_events(self) -> None:
        translator = self._translator()

        note = translator.translate(self.NoteOn(note=60, velocity=99, channel=3))
        control = translator.translate(self.ControlChange(control=1, value=64, channel=0))
        bend = translator.translate(self.PitchBend(pitch_bend=12000, channel=15))
        clock = translator.translate(self.TimingClock())

        assert (note.message_type, note.channel, note.note, note.velocity) == ("note_on", 4, 60, 99)
        assert (control.message_type, control.channel, control.control, control.value) == (
            "control_change",
            1,
            1,
            64,
        )
        assert (bend.message_type, bend.channel, bend.value) == ("pitch_bend", 16, 12000)
        assert (clock.message_type, clock.channel) == ("timing_clock", None)

    def test_input_port_is_bounded_and_ignores_unknown_messages(self) -> None:
        raw_midi = self.RawMidi((self.Unknown(), self.NoteOff(note=62, velocity=7, channel=1)))
        factory = self.Factory(raw_midi)
        port = UsbMidiInputPort(factory=factory, translator=self._translator(), port_index=2)

        port.open()
        assert port.receive() is None
        event = port.receive()
        port.close()

        assert factory.requested_port_index == 2
        assert (event.message_type, event.channel, event.note, event.velocity) == (
            "note_off",
            2,
            62,
            7,
        )
        assert port.is_open is False

    def test_input_port_requires_open_before_receive(self) -> None:
        port = UsbMidiInputPort(
            factory=self.Factory(self.RawMidi(())),
            translator=self._translator(),
        )

        try:
            port.receive()
        except RuntimeError as error:
            assert str(error) == "USB MIDI input is closed"
        else:
            raise AssertionError("closed USB MIDI input must reject receive")

    def test_circuitpython_factory_uses_positional_import_arguments(self) -> None:
        midi_class = type("MidiClass", (), {})
        importer = self.PositionalOnlyImporter(
            {
                "adafruit_midi": self.ModuleStub(MIDI=midi_class),
                "usb_midi": self.ModuleStub(ports=(object(),)),
                "adafruit_midi.note_on": self.ModuleStub(NoteOn=self.NoteOn),
                "adafruit_midi.note_off": self.ModuleStub(NoteOff=self.NoteOff),
                "adafruit_midi.control_change": self.ModuleStub(
                    ControlChange=self.ControlChange
                ),
                "adafruit_midi.pitch_bend": self.ModuleStub(PitchBend=self.PitchBend),
            }
        )

        midi_input = CircuitPythonUsbMidiFactory(importer).create_input()

        assert isinstance(midi_input, UsbMidiInputPort)
        assert any(len(call) == 4 for call in importer.calls)


class TestUsbMidiReceiveDiagnostic:
    class ManualTime:
        def __init__(self):
            self._seconds = 0.0

        def monotonic(self):
            return self._seconds

        def sleep(self, seconds):
            self._seconds += float(seconds)

    def test_matching_note_on_and_note_off_produce_pass_and_close_port(self) -> None:
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=4, note=60, velocity=99),
                NoteEvent.note_off(channel=4, note=60, velocity=31),
            )
        )
        manual_time = self.ManualTime()
        output = []
        diagnostic = UsbMidiReceiveDiagnostic(
            midi_input=midi_input,
            output=output.append,
            monotonic=manual_time.monotonic,
            sleeper=manual_time.sleep,
            max_events=4,
            timeout_seconds=1.0,
            poll_interval_seconds=0.01,
        )

        result = diagnostic.run()

        assert result is True
        assert midi_input.is_open is False
        assert "USB_MIDI_EVENT=note_on;channel=4;note=60;velocity=99" in output
        assert "USB_MIDI_EVENT=note_off;channel=4;note=60;velocity=31" in output
        assert output[-1] == (
            "USB_MIDI_DIAGNOSTIC_STATUS=PASS;events=2;note_on=1;"
            "note_off=1;matched_notes=1"
        )

    def test_timeout_without_complete_note_pair_fails_and_closes_port(self) -> None:
        midi_input = MemoryMidiInput((NoteEvent.note_on(channel=1, note=64, velocity=80),))
        manual_time = self.ManualTime()
        output = []
        diagnostic = UsbMidiReceiveDiagnostic(
            midi_input=midi_input,
            output=output.append,
            monotonic=manual_time.monotonic,
            sleeper=manual_time.sleep,
            max_events=4,
            timeout_seconds=0.03,
            poll_interval_seconds=0.01,
        )

        result = diagnostic.run()

        assert result is False
        assert midi_input.is_open is False
        assert output[-1] == (
            "USB_MIDI_DIAGNOSTIC_STATUS=FAIL;reason=incomplete-note-pair;"
            "events=1;note_on=1;note_off=0;matched_notes=0"
        )

    def test_note_on_with_zero_velocity_is_normalized_to_note_off(self) -> None:
        midi_input = MemoryMidiInput(
            (
                NoteEvent.note_on(channel=2, note=67, velocity=100),
                NoteEvent.note_on(channel=2, note=67, velocity=0),
            )
        )
        manual_time = self.ManualTime()
        output = []
        diagnostic = UsbMidiReceiveDiagnostic(
            midi_input=midi_input,
            output=output.append,
            monotonic=manual_time.monotonic,
            sleeper=manual_time.sleep,
        )

        assert diagnostic.run() is True
        assert "USB_MIDI_EVENT=note_off;channel=2;note=67;velocity=0" in output
