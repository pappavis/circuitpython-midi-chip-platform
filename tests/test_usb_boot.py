# Bestand: test_usb_boot.py
# Versienommer: 0.1.0
# Doel: Spesifiseer die veilige CircuitPython USB-bootprofiel voor implementering.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-RED-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

import pytest

from midi_chip_platform.release import ReleaseMetadata
from midi_chip_platform.usb_boot import UsbBootApplication, UsbBootProfile


class TestUsbBootApplication:
    class FakeSupervisor:
        def __init__(self, calls, fail=False):
            self._calls = calls
            self._fail = fail

        def set_usb_identification(self, **arguments):
            self._calls.append(("identity", arguments))
            if self._fail:
                raise RuntimeError("identity rejected")

    class FakeHid:
        def __init__(self, calls):
            self._calls = calls

        def disable(self):
            self._calls.append(("hid.disable", {}))

    class FakeMidi:
        def __init__(self, calls):
            self._calls = calls

        def enable(self):
            self._calls.append(("midi.enable", {}))

    def test_boot_uses_names_without_overriding_board_vid_pid(self) -> None:
        calls = []
        output = []
        application = self._application(calls, output)

        application.run()

        assert calls[0] == (
            "identity",
            {"manufacturer": "pappavis", "product": "CircuitPython MIDI Chip Platform"},
        )
        assert "vid" not in calls[0][1]
        assert "pid" not in calls[0][1]

    def test_boot_disables_hid_before_enabling_midi(self) -> None:
        calls = []
        application = self._application(calls, [])

        application.run()

        assert [name for name, _ in calls] == ["identity", "hid.disable", "midi.enable"]

    def test_boot_reports_traceability_and_success(self) -> None:
        output = []
        application = self._application([], output)

        result = application.run()

        assert result is True
        assert output[0] == (
            "circuitpython-midi-chip-platform v0.2.0 | "
            "story=MCP-US-003 | release-date=2026-07-14"
        )
        assert output[-1] == "BOOT_STATUS=PASS"

    def test_boot_does_not_hide_usb_configuration_failure(self) -> None:
        calls = []
        output = []
        application = self._application(calls, output, fail_identity=True)

        with pytest.raises(RuntimeError, match="identity rejected"):
            application.run()

        assert "BOOT_STATUS=PASS" not in output

    def _application(self, calls, output, fail_identity=False):
        return UsbBootApplication(
            profile=UsbBootProfile(
                manufacturer="pappavis",
                product="CircuitPython MIDI Chip Platform",
                disable_hid=True,
            ),
            release_metadata=ReleaseMetadata(
                version="0.2.0",
                user_story="MCP-US-003",
                release_date="2026-07-14",
            ),
            supervisor_module=self.FakeSupervisor(calls, fail=fail_identity),
            usb_hid_module=self.FakeHid(calls),
            usb_midi_module=self.FakeMidi(calls),
            output=output.append,
        )
