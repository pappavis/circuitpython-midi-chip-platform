# Bestand: release.py
# Versienommer: 0.5.0
# Doel: Besit en formateer gedeelde host- en toestel-release-naspeurbaarheid.
# Sprint: Sprint 1
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-GREEN-005
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005


class ReleaseMetadata:
    def __init__(
        self,
        version="0.5.0",
        user_story="MCP-US-005",
        release_date="2026-07-15",
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
