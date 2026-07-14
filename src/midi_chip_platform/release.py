# Bestand: release.py
# Versienommer: 0.2.0
# Doel: Besit en formateer gedeelde host- en toestel-release-naspeurbaarheid.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003


class ReleaseMetadata:
    def __init__(
        self,
        version="0.2.0",
        user_story="MCP-US-003",
        release_date="2026-07-14",
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
