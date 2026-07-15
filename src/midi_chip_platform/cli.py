# Bestand: cli.py
# Versienommer: 0.5.0
# Doel: Bied IDE-onafhanklike host-, MIDI-, BLE-capability- en HIL-diagnose.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-062 BLE MIDI Transport And Capability Gate
# Actienr: MCP-ACT-062-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-062

import argparse
import sys

from midi_chip_platform.ble_midi import BleMidiCapabilityGate, ImportModuleProbe
from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.hil import HardwareInLoopVerifierFactory
from midi_chip_platform.release import ReleaseMetadata


class CommandLineApplication:
    def __init__(self, output=None, release_metadata=None, hil_verifier_factory=None):
        self._output = output if output is not None else sys.stdout
        self._release_metadata = release_metadata if release_metadata is not None else ReleaseMetadata()
        self._hil_verifier_factory = (
            hil_verifier_factory
            if hil_verifier_factory is not None
            else HardwareInLoopVerifierFactory()
        )

    def run(self, arguments=None):
        self._output.write(f"{self._release_metadata.banner()}\n")
        parser = self._build_parser()
        parsed = parser.parse_args(arguments)
        if parsed.command == "diagnose":
            return self._diagnose()
        if parsed.command == "events-diagnose":
            return self._diagnose_events()
        if parsed.command == "ble-diagnose":
            return self._diagnose_ble(parsed)
        if parsed.command == "hil-verify":
            return self._hil_verify(parsed)
        parser.print_help(file=self._output)
        return 2

    @classmethod
    def console_entry(cls):
        return cls().run()

    def _build_parser(self):
        parser = argparse.ArgumentParser(prog="midi-chip-platform")
        subparsers = parser.add_subparsers(dest="command")
        subparsers.add_parser("diagnose", help="verify the import-safe host skeleton")
        subparsers.add_parser(
            "events-diagnose",
            help="verify portable note, control, pitch-bend and clock events",
        )
        ble_parser = subparsers.add_parser(
            "ble-diagnose",
            help="report BLE-MIDI support without starting radio services",
        )
        ble_parser.add_argument("--board-id", required=True)
        hil_parser = subparsers.add_parser(
            "hil-verify",
            help="verify redacted CircuitPython connection, deployment and execution proof",
        )
        hil_parser.add_argument("--source-root", default=".")
        hil_parser.add_argument("--device-root", required=True)
        hil_parser.add_argument("--serial-port", required=True)
        return parser

    def _diagnose(self):
        self._output.write("circuitpython-midi-chip-platform: host skeleton ready\n")
        self._output.write("hardware access: disabled\n")
        self._output.write("runtime state: class instances only\n")
        return 0

    def _diagnose_events(self):
        note = NoteEvent.note_on(channel=1, note=60, velocity=100)
        control = ControlEvent.control_change(channel=1, control=1, value=64)
        pitch_bend = ControlEvent.pitch_bend(channel=1, value=8192)
        clock = ClockEvent.timing_clock()
        self._output.write("EVENT_MODEL_STATUS=PASS\n")
        self._output.write(
            "NOTE_EVENT="
            f"{note.message_type}:channel={note.channel}:note={note.note}:"
            f"velocity={note.velocity}\n"
        )
        self._output.write(
            "CONTROL_EVENT="
            f"{control.message_type}:channel={control.channel}:control={control.control}:"
            f"value={control.value}\n"
        )
        self._output.write(
            "PITCH_BEND_EVENT="
            f"{pitch_bend.message_type}:channel={pitch_bend.channel}:"
            f"value={pitch_bend.value}\n"
        )
        self._output.write(
            f"CLOCK_EVENT={clock.message_type}:channel=none\n"
        )
        return 0

    def _hil_verify(self, parsed):
        verifier = self._hil_verifier_factory.create(
            source_root=parsed.source_root,
            device_root=parsed.device_root,
            serial_port=parsed.serial_port,
            output=self._output,
        )
        return 0 if verifier.run() else 1

    def _diagnose_ble(self, parsed):
        capability = BleMidiCapabilityGate().evaluate(
            board_id=parsed.board_id,
            module_probe=ImportModuleProbe(),
        )
        self._output.write(f"{capability.report_line()}\n")
        return 0 if capability.is_supported else 1
