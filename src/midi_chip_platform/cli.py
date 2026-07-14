# Bestand: cli.py
# Versienommer: 0.2.0
# Doel: Bied IDE-onafhanklike diagnose met verpligte release-naspeurbaarheid.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: AUDIO-PRIORITY-AMENDMENT-001
# Actienr: MCP-ACT-AUDIO-AMEND-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001

import argparse
import sys

from midi_chip_platform.release import ReleaseMetadata


class CommandLineApplication:
    def __init__(self, output=None, release_metadata=None):
        self._output = output if output is not None else sys.stdout
        self._release_metadata = release_metadata if release_metadata is not None else ReleaseMetadata()

    def run(self, arguments=None):
        self._output.write(f"{self._release_metadata.banner()}\n")
        parser = self._build_parser()
        parsed = parser.parse_args(arguments)
        if parsed.command == "diagnose":
            return self._diagnose()
        parser.print_help(file=self._output)
        return 2

    @classmethod
    def console_entry(cls):
        return cls().run()

    def _build_parser(self):
        parser = argparse.ArgumentParser(prog="midi-chip-platform")
        subparsers = parser.add_subparsers(dest="command")
        subparsers.add_parser("diagnose", help="verify the import-safe host skeleton")
        return parser

    def _diagnose(self):
        self._output.write("circuitpython-midi-chip-platform: host skeleton ready\n")
        self._output.write("hardware access: disabled\n")
        self._output.write("runtime state: class instances only\n")
        return 0
