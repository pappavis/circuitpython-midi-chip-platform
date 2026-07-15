# Bestand: test_ble_midi.py
# Versienommer: 0.1.0
# Doel: Bewys BLE-MIDI capability gating en vervoerhergebruik sonder vals hardewarebewys.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-062 BLE MIDI Transport And Capability Gate
# Actienr: MCP-ACT-062-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-062

from midi_chip_platform.ble_midi import BleMidiCapabilityGate, BleMidiInputPort
from midi_chip_platform.midi_usb import MidiMessageTranslator, MidiMessageTypes


class TestBleMidiCapabilityGate:
    class ModuleProbe:
        def __init__(self, available_modules):
            self._available_modules = set(available_modules)

        def is_available(self, module_name):
            return module_name in self._available_modules

    def test_lolin_s2_reports_native_ble_as_unsupported(self) -> None:
        capability = BleMidiCapabilityGate().evaluate(
            board_id="lolin_s2_mini",
            module_probe=self.ModuleProbe(("adafruit_ble", "adafruit_ble_midi")),
        )

        assert capability.is_supported is False
        assert capability.reason == "board_has_no_native_ble"

    def test_ble_capable_board_requires_both_runtime_modules(self) -> None:
        gate = BleMidiCapabilityGate()

        missing_library = gate.evaluate(
            board_id="generic_ble_board",
            module_probe=self.ModuleProbe(("adafruit_ble",)),
        )
        ready = gate.evaluate(
            board_id="generic_ble_board",
            module_probe=self.ModuleProbe(("adafruit_ble", "adafruit_ble_midi")),
        )

        assert missing_library.is_supported is False
        assert missing_library.reason == "ble_midi_library_unavailable"
        assert ready.is_supported is True
        assert ready.reason == "ready"


class TestBleMidiInputPort:
    class NoteOn:
        def __init__(self):
            self.note = 64
            self.velocity = 88
            self.channel = 0

    class NoteOff:
        pass

    class Receiver:
        def __init__(self):
            self.started = False
            self.stopped = False
            self._messages = [TestBleMidiInputPort.NoteOn()]

        def start(self):
            self.started = True

        def receive(self):
            if not self._messages:
                return None
            return self._messages.pop(0)

        def stop(self):
            self.stopped = True

    def test_ble_transport_uses_the_same_portable_event_model(self) -> None:
        receiver = self.Receiver()
        translator = MidiMessageTranslator(
            MidiMessageTypes(note_on_type=self.NoteOn, note_off_type=self.NoteOff)
        )
        port = BleMidiInputPort(receiver=receiver, translator=translator)

        port.open()
        event = port.receive()
        port.close()

        assert receiver.started is True
        assert receiver.stopped is True
        assert (event.message_type, event.channel, event.note, event.velocity) == (
            "note_on",
            1,
            64,
            88,
        )
