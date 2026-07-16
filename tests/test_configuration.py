# Bestand: test_configuration.py
# Versienommer: 0.17.3
# Doel: Spesifiseer publieke D1-runtime, veilige audio en private settings.
# Sprint: Sprint 1
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-IMP-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-IMPEDIMENT-003

from midi_chip_platform.configuration import (
    ConfigurationDefaults,
    ConfigurationLoader,
    EnvironmentSettingsSource,
)
from pathlib import Path


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
        assert snapshot.get("audio.master_gain") == 0.08
        assert snapshot.get("audio.maximum_master_gain") == 0.25
        assert snapshot.get("audio.startup_muted") is True
        assert snapshot.get("audio.amplifier_gain_db") == 9.0
        assert snapshot.get("audio.gain_pin_profile") == "floating-9db"
        assert snapshot.get("audio.shutdown_mode") == "software-mute"
        assert snapshot.get("audio.output_load") == "speaker-4-8-ohm"
        assert snapshot.get("clock.bpm") == 120
        assert snapshot.get("synth.d1.enabled") is True
        assert snapshot.get("synth.d1.waveform") == "sine"
        assert snapshot.get("synth.d1.sample_rate") == 16000
        assert snapshot.get("synth.d1.frames_per_block") == 128
        assert snapshot.get("synth.d1.amplitude") == 0.5
        assert snapshot.get("synth.d1.max_blocks") == 0
        assert snapshot.get("synth.d1.idle_sleep_seconds") == 0.001
        assert snapshot.get("synth.d1.minimum_note_seconds") == 0.12
        assert snapshot.get("synth.d1.minimum_note_velocity") == 64
        assert snapshot.get("synth.d1.audition_master_gain") == 0.25
        assert snapshot.get("midi.diagnostic.enabled") is False
        assert snapshot.get("midi.diagnostic.max_events") == 8
        assert snapshot.get("midi.diagnostic.timeout_seconds") == 60

    def test_device_settings_example_quotes_non_integer_values_for_circuitpython_10(self) -> None:
        settings_example = (
            Path(__file__).parents[1] / "device" / "settings.toml.example"
        ).read_text(encoding="utf-8")

        assert 'MIDI_DIAGNOSTIC_ENABLED = "false"' in settings_example
        assert 'MIDI_DIAGNOSTIC_POLL_INTERVAL_SECONDS = "0.01"' in settings_example
        assert 'AUDIO_MASTER_GAIN = "0.08"' in settings_example
        assert 'AUDIO_MAXIMUM_MASTER_GAIN = "0.25"' in settings_example
        assert 'AUDIO_STARTUP_MUTED = "true"' in settings_example
        assert 'D1_RUNTIME_ENABLED = "true"' in settings_example
        assert 'D1_AMPLITUDE = "0.5"' in settings_example
        assert 'D1_IDLE_SLEEP_SECONDS = "0.001"' in settings_example
        assert 'D1_MINIMUM_NOTE_SECONDS = "0.12"' in settings_example
        assert "D1_MINIMUM_NOTE_VELOCITY = 64" in settings_example
        assert 'D1_AUDITION_MASTER_GAIN = "0.25"' in settings_example


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

    def test_empty_private_settings_are_treated_as_unset(self) -> None:
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(
                lambda key: "" if key in ("WIFI_SSID", "WIFI_PASSWORD") else None
            ),
        ).load()

        report = "\n".join(snapshot.report_lines())

        assert snapshot.get("wifi.ssid") is None
        assert snapshot.get("wifi.password") is None
        assert snapshot.source_for("wifi.ssid") is None
        assert "CONFIG_PRIVATE_WIFI_SSID=UNSET" in report
        assert "CONFIG_PRIVATE_WIFI_PASSWORD=UNSET" in report

    def test_whitespace_private_settings_are_treated_as_unset(self) -> None:
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(
                lambda key: "  \t " if key == "WEB_AP_PASSWORD" else None
            ),
        ).load()

        report = "\n".join(snapshot.report_lines())

        assert snapshot.get("web.ap.password") is None
        assert snapshot.source_for("web.ap.password") is None
        assert "CONFIG_PRIVATE_WEB_AP_PASSWORD=UNSET" in report

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
            "D1_RUNTIME_ENABLED": "false",
            "D1_SAMPLE_RATE": "22050",
            "D1_AMPLITUDE": "0.1",
            "MIDI_DIAGNOSTIC_ENABLED": "true",
            "MIDI_DIAGNOSTIC_MAX_EVENTS": "12",
        }
        snapshot = ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(values.get),
        ).load()

        assert snapshot.get("clock.bpm") == 96
        assert snapshot.get("audio.startup_test") is True
        assert snapshot.get("synth.d1.enabled") is False
        assert snapshot.get("synth.d1.sample_rate") == 22050
        assert snapshot.get("synth.d1.amplitude") == 0.1
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
