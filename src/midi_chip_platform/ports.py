# Bestand: ports.py
# Versienommer: 0.1.0
# Doel: Definieer vervangbare MIDI-, audio-, klok- en konfigurasiepoorte.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002


class MidiInputPort:
    def open(self):
        raise NotImplementedError("MidiInputPort.open must be implemented")

    def receive(self):
        raise NotImplementedError("MidiInputPort.receive must be implemented")

    def close(self):
        raise NotImplementedError("MidiInputPort.close must be implemented")


class AudioOutputPort:
    def open(self):
        raise NotImplementedError("AudioOutputPort.open must be implemented")

    def write(self, frame):
        raise NotImplementedError("AudioOutputPort.write must be implemented")

    def close(self):
        raise NotImplementedError("AudioOutputPort.close must be implemented")


class ClockPort:
    def tick(self):
        raise NotImplementedError("ClockPort.tick must be implemented")

    def now_seconds(self):
        raise NotImplementedError("ClockPort.now_seconds must be implemented")


class ConfigurationPort:
    def get(self, key, default=None):
        raise NotImplementedError("ConfigurationPort.get must be implemented")
