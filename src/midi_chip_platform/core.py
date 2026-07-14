# Bestand: core.py
# Versienommer: 0.1.0
# Doel: Definieer die synth-kernkontrak en instansie-besitte kanaalregistry.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-004
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002


class SynthCore:
    @property
    def name(self):
        raise NotImplementedError("SynthCore.name must be implemented")

    def start(self):
        raise NotImplementedError("SynthCore.start must be implemented")

    def handle_event(self, event):
        raise NotImplementedError("SynthCore.handle_event must be implemented")

    def render_frame(self):
        raise NotImplementedError("SynthCore.render_frame must be implemented")

    def stop(self):
        raise NotImplementedError("SynthCore.stop must be implemented")


class CoreRegistry:
    def __init__(self):
        self._cores_by_channel = {}

    def register(self, channel, core):
        self._validate_channel(channel)
        if not isinstance(core, SynthCore):
            raise TypeError("core must implement SynthCore")
        self._cores_by_channel[int(channel)] = core

    def unregister(self, channel):
        self._validate_channel(channel)
        return self._cores_by_channel.pop(int(channel), None)

    def resolve(self, channel):
        self._validate_channel(channel)
        return self._cores_by_channel.get(int(channel))

    def cores(self):
        unique_cores = []
        for core in self._cores_by_channel.values():
            if core not in unique_cores:
                unique_cores.append(core)
        return tuple(unique_cores)

    @staticmethod
    def _validate_channel(channel):
        if not 1 <= int(channel) <= 16:
            raise ValueError("channel must be between 1 and 16")
