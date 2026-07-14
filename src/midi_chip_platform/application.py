# Bestand: application.py
# Versienommer: 0.1.0
# Doel: Koordineer geinjekteerde platformpoorte sonder import-newe-effekte.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-GREEN-005
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

from midi_chip_platform.core import CoreRegistry
from midi_chip_platform.ports import AudioOutputPort, ClockPort, ConfigurationPort, MidiInputPort


class PlatformApplication:
    def __init__(self, midi_input, audio_output, clock, configuration, registry):
        self._require_type("midi_input", midi_input, MidiInputPort)
        self._require_type("audio_output", audio_output, AudioOutputPort)
        self._require_type("clock", clock, ClockPort)
        self._require_type("configuration", configuration, ConfigurationPort)
        self._require_type("registry", registry, CoreRegistry)
        self._midi_input = midi_input
        self._audio_output = audio_output
        self._clock = clock
        self._configuration = configuration
        self._registry = registry
        self._is_started = False

    @property
    def is_started(self):
        return self._is_started

    def start(self):
        if self._is_started:
            return
        self._midi_input.open()
        self._audio_output.open()
        for core in self._registry.cores():
            core.start()
        self._is_started = True

    def step(self):
        if not self._is_started:
            raise RuntimeError("application must be started before step")
        event = self._midi_input.receive()
        self._clock.tick()
        if event is None:
            return False
        core = self._registry.resolve(event.channel)
        if core is None:
            return False
        core.handle_event(event)
        frame = core.render_frame()
        if frame is not None:
            self._audio_output.write(frame)
        return True

    def stop(self):
        if not self._is_started:
            return
        for core in reversed(self._registry.cores()):
            core.stop()
        self._audio_output.close()
        self._midi_input.close()
        self._is_started = False

    @staticmethod
    def _require_type(label, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(f"{label} must implement {expected_type.__name__}")
