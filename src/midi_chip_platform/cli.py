# Bestand: cli.py
# Versienommer: 0.1.0
# Doel: Bied 'n minimale IDE-onafhanklike host-diagnosecommando.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-007
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

import argparse
import sys


class CommandLineApplication:
    def __init__(self, output=None):
        self._output = output if output is not None else sys.stdout

    def run(self, arguments=None):
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
