# Bestand: usb_boot.py
# Versienommer: 0.1.0
# Doel: Konfigureer 'n minimale, geïnjekteerde en toetsbare CircuitPython USB-profiel.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-003 Minimal Safe Boot And USB Profile
# Actienr: MCP-ACT-003-GREEN-002
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-003

from midi_chip_platform.release import ReleaseMetadata


class UsbBootProfile:
    def __init__(self, manufacturer, product, disable_hid=True):
        self._manufacturer = str(manufacturer)
        self._product = str(product)
        self._disable_hid = bool(disable_hid)

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def product(self):
        return self._product

    @property
    def disable_hid(self):
        return self._disable_hid


class UsbBootApplication:
    def __init__(
        self,
        profile,
        release_metadata,
        supervisor_module,
        usb_hid_module,
        usb_midi_module,
        output=None,
    ):
        if not isinstance(profile, UsbBootProfile):
            raise TypeError("profile must be UsbBootProfile")
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._profile = profile
        self._release_metadata = release_metadata
        self._supervisor = supervisor_module
        self._usb_hid = usb_hid_module
        self._usb_midi = usb_midi_module
        self._output = output if output is not None else print

    def run(self):
        self._output(self._release_metadata.banner())
        self._supervisor.set_usb_identification(
            manufacturer=self._profile.manufacturer,
            product=self._profile.product,
        )
        if self._profile.disable_hid:
            self._usb_hid.disable()
        self._usb_midi.enable()
        self._output("BOOT_STATUS=PASS")
        return True
