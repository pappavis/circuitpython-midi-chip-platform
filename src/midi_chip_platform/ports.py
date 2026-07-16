# Bestand: ports.py
# Versienommer: 0.16.0
# Doel: Definieer vervangbare MIDI-, veilige blokaudio-, klok- en konfigurasiepoorte.
# Sprint: Sprint 2
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-075 Safe Development Audio Load And Volume Gate
# Actienr: MCP-ACT-075-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-075-START


class MidiInputPort:
    def open(self):
        raise NotImplementedError("MidiInputPort.open must be implemented")

    def receive(self):
        raise NotImplementedError("MidiInputPort.receive must be implemented")

    def close(self):
        raise NotImplementedError("MidiInputPort.close must be implemented")


class AudioOutputPort:
    @property
    def audio_format(self):
        raise NotImplementedError("AudioOutputPort.audio_format must be implemented")

    def open(self):
        raise NotImplementedError("AudioOutputPort.open must be implemented")

    def write_block(self, block):
        raise NotImplementedError("AudioOutputPort.write_block must be implemented")

    def mute(self):
        raise NotImplementedError("AudioOutputPort.mute must be implemented")

    def unmute(self):
        raise NotImplementedError("AudioOutputPort.unmute must be implemented")

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
