# Bestand: boot.py
# Versienommer: 0.1.0
# Doel: Stel slegs die herstelbare CircuitPython USB-MIDI-profiel tydens harde boot op.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-GREEN-004
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

import supervisor
import usb_hid
import usb_midi

from midi_chip_platform.release import ReleaseMetadata
from midi_chip_platform.usb_boot import UsbBootApplication, UsbBootProfile


if __name__ == "__main__":
    UsbBootApplication(
        profile=UsbBootProfile(
            manufacturer="pappavis",
            product="CircuitPython MIDI Chip Platform",
            disable_hid=True,
        ),
        release_metadata=ReleaseMetadata(),
        supervisor_module=supervisor,
        usb_hid_module=usb_hid,
        usb_midi_module=usb_midi,
    ).run()
