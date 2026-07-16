# Bestand: release.py
# Versienommer: 0.18.0
# Doel: Besit release-naspeurbaarheid vir die realtime MIDI-audio baseline spike.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-077 Realtime MIDI Audio Baseline Spike
# Actienr: MCP-ACT-077-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-START


class ReleaseMetadata:
    def __init__(
        self,
        version="0.18.0",
        user_story="MCP-US-077",
        release_date="2026-07-16",
    ):
        self._version = str(version)
        self._user_story = str(user_story)
        self._release_date = str(release_date)

    @property
    def version(self):
        return self._version

    @property
    def user_story(self):
        return self._user_story

    @property
    def release_date(self):
        return self._release_date

    def banner(self):
        return (
            f"circuitpython-midi-chip-platform v{self._version} | "
            f"story={self._user_story} | release-date={self._release_date}"
        )
