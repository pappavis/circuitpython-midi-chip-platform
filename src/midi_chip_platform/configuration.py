# Bestand: configuration.py
# Versienommer: 0.1.0
# Doel: Laai publieke verstekke en private CircuitPython-settings met veilige prioriteit en redaksie.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: MCP-US-005 Configuration And Secret Boundary
# Actienr: MCP-ACT-005-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-005

from midi_chip_platform.ports import ConfigurationPort


class ConfigurationDefaults:
    def __init__(self):
        self._values = {
            "audio.backend": "i2s-max98357a-mono",
            "audio.channel": "mono",
            "audio.i2s.bit_clock": "IO5",
            "audio.i2s.word_select": "IO3",
            "audio.i2s.data": "IO7",
            "audio.startup_test": False,
            "clock.bpm": 120,
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
            "audio.startup_test": "AUDIO_STARTUP_TEST",
            "clock.bpm": "CLOCK_BPM",
            "wifi.mode": "WIFI_MODE",
            "wifi.ssid": "WIFI_SSID",
            "wifi.password": "WIFI_PASSWORD",
            "web.ap.password": "WEB_AP_PASSWORD",
        }

    def get(self, key):
        environment_key = self._environment_keys.get(str(key))
        if environment_key is None:
            return None
        return self._getter(environment_key)

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
