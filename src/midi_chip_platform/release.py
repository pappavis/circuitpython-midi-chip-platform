# Bestand: release.py
# Versienommer: 0.1.0
# Doel: Besit en formateer runtime-release- en storynaspeurbaarheid.
# Sprint: Sprint 0
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: AUDIO-PRIORITY-AMENDMENT-001
# Actienr: MCP-ACT-AUDIO-AMEND-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001


class ReleaseMetadata:
    def __init__(
        self,
        version="0.1.1",
        user_story="AUDIO-PRIORITY-AMENDMENT-001",
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
