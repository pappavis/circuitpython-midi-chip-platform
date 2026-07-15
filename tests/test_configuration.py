# Bestand: test_configuration.py
# Versienommer: 0.12.0
# Doel: Spesifiseer publieke verstekke, private settings en opt-in MIDI-diagnostiek.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-007 USB MIDI Receive Loop
# Actienr: MCP-ACT-007-RED-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-007

from midi_chip_platform.configuration import (
    ConfigurationDefaults,
    ConfigurationLoader,
    EnvironmentSettingsSource,
)


class TestConfigurationDefaults:
    def test_public_defaults_preserve_approved_mono_i2s_profile(self) -> None:
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(lambda key: None),
        ).load()

        assert snapshot.get("audio.backend") == "i2s-max98357a-mono"
        assert snapshot.get("audio.i2s.bit_clock") == "IO5"
        assert snapshot.get("audio.i2s.word_select") == "IO3"
        assert snapshot.get("audio.i2s.data") == "IO7"
        assert snapshot.get("clock.bpm") == 120
        assert snapshot.get("midi.diagnostic.enabled") is False
        assert snapshot.get("midi.diagnostic.max_events") == 8
        assert snapshot.get("midi.diagnostic.timeout_seconds") == 60


class TestConfigurationSecretBoundary:
    class RecordingGetter:
        def __init__(self, values):
            self._values = dict(values)
            self._requested = []

        @property
        def requested(self):
            return tuple(self._requested)

        def __call__(self, key):
            self._requested.append(key)
            return self._values.get(key)

    def test_private_settings_are_read_without_exposing_values(self) -> None:
        private_ssid = "private-network-value"
        private_password = "private-password-value"
        getter = self.RecordingGetter(
            {
                "WIFI_SSID": private_ssid,
                "WIFI_PASSWORD": private_password,
            }
        )
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(getter),
        ).load()

        report = "\n".join(snapshot.report_lines())

        assert snapshot.get("wifi.ssid") == private_ssid
        assert snapshot.get("wifi.password") == private_password
        assert snapshot.source_for("wifi.ssid") == "private"
        assert "WIFI_SSID" in getter.requested
        assert private_ssid not in report
        assert private_password not in report
        assert "CONFIG_PRIVATE_WIFI_SSID=SET" in report
        assert "CONFIG_PRIVATE_WIFI_PASSWORD=SET" in report

    def test_runtime_override_has_highest_priority(self) -> None:
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(
                lambda key: "private-backend" if key == "AUDIO_BACKEND" else None
            ),
            overrides={"audio.backend": "runtime-backend"},
        ).load()

        assert snapshot.get("audio.backend") == "runtime-backend"
        assert snapshot.source_for("audio.backend") == "override"

    def test_string_settings_preserve_default_integer_and_boolean_types(self) -> None:
        values = {
            "CLOCK_BPM": "96",
            "AUDIO_STARTUP_TEST": "true",
            "MIDI_DIAGNOSTIC_ENABLED": "true",
            "MIDI_DIAGNOSTIC_MAX_EVENTS": "12",
        }
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(values.get),
        ).load()

        assert snapshot.get("clock.bpm") == 96
        assert snapshot.get("audio.startup_test") is True
        assert snapshot.get("midi.diagnostic.enabled") is True
        assert snapshot.get("midi.diagnostic.max_events") == 12

    def test_public_items_exclude_private_values(self) -> None:
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(
                lambda key: "do-not-publish" if key == "WIFI_PASSWORD" else None
            ),
        ).load()

        public_items = dict(snapshot.public_items())

        assert "audio.backend" in public_items
        assert "wifi.password" not in public_items
        assert "do-not-publish" not in repr(public_items)
