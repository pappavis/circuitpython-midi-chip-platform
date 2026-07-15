# Bestand: ble_midi.py
# Versienommer: 0.1.0
# Doel: Gate BLE-MIDI per bordvermoe en hergebruik die draagbare MIDI-eventmodel.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-062 BLE MIDI Transport And Capability Gate
# Actienr: MCP-ACT-062-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-062

from midi_chip_platform.midi_usb import MidiMessageTranslator
from midi_chip_platform.ports import MidiInputPort


class BleMidiCapability:
    def __init__(self, board_id, is_supported, reason):
        self._board_id = str(board_id)
        self._is_supported = bool(is_supported)
        self._reason = str(reason)

    @property
    def board_id(self):
        return self._board_id

    @property
    def is_supported(self):
        return self._is_supported

    @property
    def reason(self):
        return self._reason

    def report_line(self):
        status = "SUPPORTED" if self._is_supported else "UNSUPPORTED"
        return f"BLE_MIDI_STATUS={status};reason={self._reason}"


class BleMidiCapabilityGate:
    def evaluate(self, board_id, module_probe):
        normalized_board_id = str(board_id).strip().lower()
        boards_without_native_ble = ("lolin_s2_mini", "esp32s2", "esp32-s2")
        if normalized_board_id in boards_without_native_ble:
            return BleMidiCapability(board_id, False, "board_has_no_native_ble")
        if not module_probe.is_available("adafruit_ble"):
            return BleMidiCapability(board_id, False, "ble_library_unavailable")
        if not module_probe.is_available("adafruit_ble_midi"):
            return BleMidiCapability(board_id, False, "ble_midi_library_unavailable")
        return BleMidiCapability(board_id, True, "ready")


class ImportModuleProbe:
    def __init__(self, importer=None):
        self._importer = importer if importer is not None else __import__

    def is_available(self, module_name):
        try:
            self._importer(str(module_name))
        except ImportError:
            return False
        return True


class BleMidiInputPort(MidiInputPort):
    def __init__(self, receiver, translator):
        if not isinstance(translator, MidiMessageTranslator):
            raise TypeError("translator must be MidiMessageTranslator")
        self._receiver = receiver
        self._translator = translator
        self._is_open = False

    @property
    def is_open(self):
        return self._is_open

    def open(self):
        if not self._is_open:
            self._receiver.start()
            self._is_open = True

    def receive(self):
        if not self._is_open:
            raise RuntimeError("BLE MIDI input is closed")
        return self._translator.translate(self._receiver.receive())

    def close(self):
        if self._is_open:
            self._receiver.stop()
            self._is_open = False
