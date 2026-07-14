# Bestand: test_core_registry.py
# Versienommer: 0.1.0
# Doel: Toets kanaalgebaseerde kernregistrasie sonder globale registry.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-002 Clean Repository And Project Skeleton
# Actienr: MCP-ACT-002-RED-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-002

import pytest

from midi_chip_platform.core import CoreRegistry
from midi_chip_platform.testing import RecordingSynthCore


class TestCoreRegistry:
    def test_registry_resolves_core_by_midi_channel(self) -> None:
        registry = CoreRegistry()
        core = RecordingSynthCore("sn76489-test")

        registry.register(channel=3, core=core)

        assert registry.resolve(channel=3) is core
        assert registry.resolve(channel=4) is None

    def test_registry_rejects_invalid_midi_channel(self) -> None:
        registry = CoreRegistry()

        with pytest.raises(ValueError, match="channel"):
            registry.register(channel=17, core=RecordingSynthCore("invalid"))

    def test_registry_returns_each_core_once_when_shared_across_channels(self) -> None:
        registry = CoreRegistry()
        core = RecordingSynthCore("shared")
        registry.register(channel=1, core=core)
        registry.register(channel=2, core=core)

        assert registry.cores() == (core,)
