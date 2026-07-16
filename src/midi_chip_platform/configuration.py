# Bestand: configuration.py
# Versienommer: 0.17.8
# Doel: Laai publieke D1-runtime, fast-boot performance-verstekke en private settings.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-P0-REALTIME-FIX-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-REALTIME-ANALYSE-003

from midi_chip_platform.ports import ConfigurationPort


class ConfigurationDefaults:
    def __init__(self):
        self._values = {
            "audio.backend": "i2s-max98357a-mono",
            "audio.channel": "mono",
            "audio.i2s.bit_clock": "IO5",
            "audio.i2s.word_select": "IO3",
            "audio.i2s.data": "IO7",
            "audio.master_gain": 0.08,
            "audio.maximum_master_gain": 0.25,
            "audio.startup_muted": True,
            "audio.amplifier_gain_db": 9.0,
            "audio.gain_pin_profile": "floating-9db",
            "audio.shutdown_mode": "software-mute",
            "audio.output_load": "speaker-4-8-ohm",
            "audio.startup_test": False,
            "clock.bpm": 120,
            "synth.d1.enabled": True,
            "synth.d1.fast_boot_mode": True,
            "synth.d1.waveform": "square",
            "synth.d1.sample_rate": 16000,
            "synth.d1.frames_per_block": 128,
            "synth.d1.amplitude": 0.5,
            "synth.d1.max_blocks": 0,
            "synth.d1.idle_sleep_seconds": 0.001,
            "synth.d1.minimum_note_seconds": 0.05,
            "synth.d1.minimum_note_velocity": 64,
            "synth.d1.audition_master_gain": 0.25,
            "synth.d1.stream_active_blocks": False,
            "synth.d1.audition_tone_amplitude": 8192,
            "synth.d1.event_logging": "none",
            "synth.d1.timing_marker_enabled": True,
            "synth.d1.timing_marker_pin": "IO9",
            "midi.input.port_index": 0,
            "midi.diagnostic.enabled": False,
            "midi.diagnostic.max_events": 8,
            "midi.diagnostic.timeout_seconds": 60,
            "midi.diagnostic.poll_interval_seconds": 0.01,
            "wifi.mode": "auto",
        }

    def items(self):
        return tuple(self._values.items())


class EnvironmentSettingsSource:
    def __init__(self, getter):
        if not callable(getter):
            raise TypeError("getter must be callable")
        self._getter = getter
        self._environment_keys = {
            "audio.backend": "AUDIO_BACKEND",
            "audio.channel": "AUDIO_CHANNEL",
            "audio.i2s.bit_clock": "I2S_BIT_CLOCK",
            "audio.i2s.word_select": "I2S_WORD_SELECT",
            "audio.i2s.data": "I2S_DATA",
            "audio.master_gain": "AUDIO_MASTER_GAIN",
            "audio.maximum_master_gain": "AUDIO_MAXIMUM_MASTER_GAIN",
            "audio.startup_muted": "AUDIO_STARTUP_MUTED",
            "audio.amplifier_gain_db": "AUDIO_AMPLIFIER_GAIN_DB",
            "audio.gain_pin_profile": "AUDIO_GAIN_PIN_PROFILE",
            "audio.shutdown_mode": "AUDIO_SHUTDOWN_MODE",
            "audio.output_load": "AUDIO_OUTPUT_LOAD",
            "audio.startup_test": "AUDIO_STARTUP_TEST",
            "clock.bpm": "CLOCK_BPM",
            "synth.d1.enabled": "D1_RUNTIME_ENABLED",
            "synth.d1.fast_boot_mode": "D1_FAST_BOOT_MODE",
            "synth.d1.waveform": "D1_WAVEFORM",
            "synth.d1.sample_rate": "D1_SAMPLE_RATE",
            "synth.d1.frames_per_block": "D1_FRAMES_PER_BLOCK",
            "synth.d1.amplitude": "D1_AMPLITUDE",
            "synth.d1.max_blocks": "D1_MAX_BLOCKS",
            "synth.d1.idle_sleep_seconds": "D1_IDLE_SLEEP_SECONDS",
            "synth.d1.minimum_note_seconds": "D1_MINIMUM_NOTE_SECONDS",
            "synth.d1.minimum_note_velocity": "D1_MINIMUM_NOTE_VELOCITY",
            "synth.d1.audition_master_gain": "D1_AUDITION_MASTER_GAIN",
            "synth.d1.stream_active_blocks": "D1_STREAM_ACTIVE_BLOCKS",
            "synth.d1.audition_tone_amplitude": "D1_AUDITION_TONE_AMPLITUDE",
            "synth.d1.event_logging": "D1_EVENT_LOGGING",
            "synth.d1.timing_marker_enabled": "D1_TIMING_MARKER_ENABLED",
            "synth.d1.timing_marker_pin": "D1_TIMING_MARKER_PIN",
            "midi.input.port_index": "MIDI_INPUT_PORT_INDEX",
            "midi.diagnostic.enabled": "MIDI_DIAGNOSTIC_ENABLED",
            "midi.diagnostic.max_events": "MIDI_DIAGNOSTIC_MAX_EVENTS",
            "midi.diagnostic.timeout_seconds": "MIDI_DIAGNOSTIC_TIMEOUT_SECONDS",
            "midi.diagnostic.poll_interval_seconds": "MIDI_DIAGNOSTIC_POLL_INTERVAL_SECONDS",
            "wifi.mode": "WIFI_MODE",
            "wifi.ssid": "WIFI_SSID",
            "wifi.password": "WIFI_PASSWORD",
            "web.ap.password": "WEB_AP_PASSWORD",
        }

    def get(self, key):
        environment_key = self._environment_keys.get(str(key))
        if environment_key is None:
            return None
        value = self._getter(environment_key)
        if isinstance(value, str) and not value.strip():
            return None
        return value

    def keys(self):
        return tuple(self._environment_keys)


class ConfigurationSnapshot(ConfigurationPort):
    def __init__(self, values, sources, secret_keys, override_count):
        self._values = dict(values)
        self._sources = dict(sources)
        self._secret_keys = tuple(secret_keys)
        self._override_count = int(override_count)

    def get(self, key, default=None):
        return self._values.get(str(key), default)

    def source_for(self, key):
        return self._sources.get(str(key))

    def public_items(self):
        return tuple(
            (key, value)
            for key, value in self._values.items()
            if key not in self._secret_keys
        )

    def report_lines(self):
        lines = [
            "CONFIGURATION_STATUS=PASS",
            f"CONFIG_PUBLIC_VALUES={len(self.public_items())}",
            f"CONFIG_OVERRIDE_COUNT={self._override_count}",
        ]
        for key in self._secret_keys:
            status = "SET" if self._values.get(key) not in (None, "") else "UNSET"
            lines.append(f"CONFIG_PRIVATE_{self._report_label(key)}={status}")
        return tuple(lines)

    @staticmethod
    def _report_label(key):
        return str(key).replace(".", "_").upper()


class ConfigurationLoader:
    def __init__(self, defaults, settings_source, overrides=None):
        if not isinstance(defaults, ConfigurationDefaults):
            raise TypeError("defaults must be ConfigurationDefaults")
        if not isinstance(settings_source, EnvironmentSettingsSource):
            raise TypeError("settings_source must be EnvironmentSettingsSource")
        self._defaults = defaults
        self._settings_source = settings_source
        self._overrides = dict(overrides or {})
        self._secret_keys = (
            "wifi.ssid",
            "wifi.password",
            "web.ap.password",
        )

    def load(self):
        values = {}
        sources = {}
        for key, default_value in self._defaults.items():
            values[key] = default_value
            sources[key] = "default"
        for key in self._settings_source.keys():
            settings_value = self._settings_source.get(key)
            if settings_value is not None:
                values[key] = self._coerce(settings_value, values.get(key))
                sources[key] = "private" if key in self._secret_keys else "settings"
        for key, override_value in self._overrides.items():
            values[str(key)] = override_value
            sources[str(key)] = "override"
        return ConfigurationSnapshot(
            values=values,
            sources=sources,
            secret_keys=self._secret_keys,
            override_count=len(self._overrides),
        )

    @staticmethod
    def _coerce(value, default_value):
        if isinstance(default_value, bool) and isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in ("true", "1", "yes", "on"):
                return True
            if normalized in ("false", "0", "no", "off"):
                return False
            raise ValueError("boolean setting must use true or false")
        if isinstance(default_value, int) and not isinstance(default_value, bool):
            return int(value)
        if isinstance(default_value, float):
            return float(value)
        return value


class CircuitPythonConfigurationFactory:
    def __init__(self, importer):
        self._importer = importer

    def create_loader(self, overrides=None):
        os_module = self._importer("os")
        return ConfigurationLoader(
            defaults=ConfigurationDefaults(),
            settings_source=EnvironmentSettingsSource(os_module.getenv),
            overrides=overrides,
        )
