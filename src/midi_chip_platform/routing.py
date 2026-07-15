# Bestand: routing.py
# Versienommer: 0.1.0
# Doel: Roeteer kanaalgebonde MIDI-events na konfigureerbare synth-kerninstansies.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-008 MIDI Channel Router
# Actienr: MCP-ACT-008-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-008

from midi_chip_platform.core import CoreRegistry, SynthCore


class MidiChannelRouter:
    def __init__(self, registry):
        if not isinstance(registry, CoreRegistry):
            raise TypeError("registry must be CoreRegistry")
        self._registry = registry

    @property
    def configured_channels(self):
        channels = []
        for channel in range(1, 17):
            if self._registry.resolve(channel) is not None:
                channels.append(channel)
        return tuple(channels)

    def configure(self, channel, core):
        if not isinstance(core, SynthCore):
            raise TypeError("core must implement SynthCore")
        self._registry.register(channel, core)

    def remove(self, channel):
        return self._registry.unregister(channel)

    def route(self, event):
        if event.channel is None:
            return None
        return self._registry.resolve(event.channel)
