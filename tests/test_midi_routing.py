# Bestand: test_midi_routing.py
# Versienommer: 0.1.0
# Doel: Bewys konfigureerbare kanaal-na-kern-roetering vir alle MIDI-kanale.
# Sprint: Sprint 2
# Epic: MCP-EPIC-002 MIDI And Clock
# User-Story: MCP-US-008 MIDI Channel Router
# Actienr: MCP-ACT-008-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-008

from midi_chip_platform.core import CoreRegistry
from midi_chip_platform.events import ClockEvent, NoteEvent
from midi_chip_platform.routing import MidiChannelRouter
from midi_chip_platform.testing import RecordingSynthCore


class TestMidiChannelRouter:
    def test_routes_channels_one_to_sixteen_to_configured_core_instances(self) -> None:
        registry = CoreRegistry()
        router = MidiChannelRouter(registry)
        first_core = RecordingSynthCore("d1")
        last_core = RecordingSynthCore("sn76489")

        router.configure(channel=1, core=first_core)
        router.configure(channel=16, core=last_core)

        assert router.route(NoteEvent.note_on(1, 60, 100)) is first_core
        assert router.route(NoteEvent.note_on(16, 64, 100)) is last_core
        assert router.route(NoteEvent.note_on(8, 67, 100)) is None

    def test_route_can_be_reconfigured_without_router_replacement(self) -> None:
        registry = CoreRegistry()
        router = MidiChannelRouter(registry)
        first_core = RecordingSynthCore("d1")
        replacement_core = RecordingSynthCore("sn76489")

        router.configure(4, first_core)
        router.configure(4, replacement_core)

        assert router.route(NoteEvent.note_on(4, 60, 100)) is replacement_core
        assert router.configured_channels == (4,)

    def test_channel_less_clock_is_not_sent_to_a_synth_core(self) -> None:
        router = MidiChannelRouter(CoreRegistry())

        assert router.route(ClockEvent.timing_clock()) is None
