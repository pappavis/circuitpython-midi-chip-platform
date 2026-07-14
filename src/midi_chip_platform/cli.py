# Bestand: cli.py
# Versienommer: 0.3.0
# Doel: Bied IDE-onafhanklike diagnose en geredigeerde HIL-verifikasie.
# Sprint: Sprint 1
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-051 Hardware-In-The-Loop Test Runner
# Actienr: MCP-ACT-051-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-051

import argparse
import sys

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

    def _hil_verify(self, parsed):
        verifier = self._hil_verifier_factory.create(
            source_root=parsed.source_root,
            device_root=parsed.device_root,
            serial_port=parsed.serial_port,
            output=self._output,
        )
        return 0 if verifier.run() else 1
