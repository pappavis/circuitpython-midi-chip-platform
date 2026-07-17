# Bestand: test_realtime_baseline.py
# Versienommer: 0.18.1
# Doel: Spesifiseer realtime USB-MIDI en direkte I2S-audio met boot-audition.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-077 Realtime MIDI Audio Baseline Spike
# Actienr: MCP-ACT-077-IMP-001-RED-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-077-IMPEDIMENT-001

from midi_chip_platform.events import NoteEvent
from midi_chip_platform.realtime_baseline import (
    RealtimeBaselineProfile,
    RealtimeMidiAudioBaselineFactory,
    RealtimeMidiAudioBaselineRuntime,
)
from midi_chip_platform.testing import MemoryConfiguration, MemoryMidiInput


class TestRealtimeMidiAudioBaseline:
    class NoSleep:
        def __init__(self):
            self._now = 0.0
            self.calls = []

        def monotonic(self):
            return self._now

        def sleep(self, seconds):
            self.calls.append(float(seconds))
            self._now += float(seconds)

    class RecordingToneOutput:
        def __init__(self, actual_frequency_hz=440.0):
            self._actual_frequency_hz = float(actual_frequency_hz)
            self.calls = []

        @property
        def actual_frequency_hz(self):
            return self._actual_frequency_hz

        def open(self):
            self.calls.append("open")

        def start(self):
            self.calls.append("start")

        def stop(self):
            self.calls.append("stop")

        def close(self):
            self.calls.append("close")

        def play_for_duration(self, duration_seconds, sleeper):
            self.calls.append(("play_for_duration", float(duration_seconds)))
            sleeper.sleep(duration_seconds)

    def test_profile_defaults_are_small_and_realtime_focused(self) -> None:
        profile = RealtimeBaselineProfile()

        assert profile.sample_rate == 16000
        assert profile.frequency_hz == 440.0
        assert profile.amplitude == 4096
        assert profile.tone_seconds == 0.12
        assert profile.max_note_events == 0
        assert profile.timeout_seconds == 0.0
        assert profile.idle_sleep_seconds == 0.0
        assert profile.event_logging == "none"
        assert profile.boot_audition_seconds == 0.6

    def test_runtime_starts_precomputed_tone_on_note_on_without_d1_core(self) -> None:
        output = []
        tone_output = self.RecordingToneOutput(actual_frequency_hz=440.0)
        sleeper = self.NoSleep()
        runtime = RealtimeMidiAudioBaselineRuntime(
            midi_input=MemoryMidiInput(
                (
                    NoteEvent.note_on(channel=1, note=60, velocity=90),
                    NoteEvent.note_off(channel=1, note=60, velocity=64),
                )
            ),
            tone_output=tone_output,
            profile=RealtimeBaselineProfile(max_note_events=1),
            output=output.append,
            sleeper=sleeper,
        )

        result = runtime.run()

        assert result is True
        assert runtime.note_on_count == 1
        assert tone_output.calls == [
            "open",
            ("play_for_duration", 0.6),
            "start",
            "stop",
            "close",
        ]
        assert output[0].startswith("REALTIME_BASELINE_STATUS=START")
        assert "REALTIME_BASELINE_AUDIO_STATUS=OPEN;actual_frequency_hz=440.000" in output
        assert "REALTIME_BASELINE_BOOT_AUDITION=START;seconds=0.600" in output
        assert "REALTIME_BASELINE_BOOT_AUDITION=PASS" in output
        assert "REALTIME_BASELINE_MIDI_INPUT_STATUS=OPEN" in output
        assert "REALTIME_BASELINE_READY;ready_ms=600" in output
        assert not any(line.startswith("REALTIME_BASELINE_NOTE_ON") for line in output)
        assert output[-1] == "REALTIME_BASELINE_STATUS=PASS;note_on=1;ignored=0"

    def test_runtime_can_suppress_per_note_summary_logging(self) -> None:
        output = []
        runtime = RealtimeMidiAudioBaselineRuntime(
            midi_input=MemoryMidiInput((NoteEvent.note_on(1, 69, 100),)),
            tone_output=self.RecordingToneOutput(),
            profile=RealtimeBaselineProfile(max_note_events=1, event_logging="none"),
            output=output.append,
            sleeper=self.NoSleep(),
        )

        result = runtime.run()

        assert result is True
        assert not any(line.startswith("REALTIME_BASELINE_NOTE_ON") for line in output)

    def test_factory_is_disabled_by_default(self) -> None:
        runtime = RealtimeMidiAudioBaselineFactory().create_if_enabled(
            MemoryConfiguration({})
        )

        assert runtime is None

    def test_factory_creates_runtime_when_baseline_enabled(self) -> None:
        class FakeImporter:
            def __call__(self, module_name, *args):
                if module_name == "adafruit_midi":
                    class FakeMidi:
                        def __init__(self, midi_in=None, in_channel=None):
                            self.midi_in = midi_in
                            self.in_channel = in_channel

                    return type("FakeAdafruitMidi", (), {"MIDI": FakeMidi})
                if module_name == "adafruit_midi.note_on":
                    return type("FakeNoteOnModule", (), {"NoteOn": type("NoteOn", (), {})})
                if module_name == "adafruit_midi.note_off":
                    return type("FakeNoteOffModule", (), {"NoteOff": type("NoteOff", (), {})})
                if module_name == "adafruit_midi.control_change":
                    return type(
                        "FakeControlChangeModule",
                        (),
                        {"ControlChange": type("ControlChange", (), {})},
                    )
                if module_name == "adafruit_midi.pitch_bend":
                    return type(
                        "FakePitchBendModule",
                        (),
                        {"PitchBend": type("PitchBend", (), {})},
                    )
                if module_name == "usb_midi":
                    return type("FakeUsbMidi", (), {"ports": (object(),)})
                if module_name == "time":
                    return TestRealtimeMidiAudioBaseline.NoSleep()
                raise ImportError(module_name)

        runtime = RealtimeMidiAudioBaselineFactory(
            importer=FakeImporter(),
            output=[].append,
        ).create_if_enabled(
            MemoryConfiguration(
                {
                    "realtime_baseline.enabled": True,
                    "realtime_baseline.sample_rate": 16000,
                    "realtime_baseline.frequency_hz": 440.0,
                    "realtime_baseline.amplitude": 4096,
                    "realtime_baseline.tone_seconds": 0.12,
                    "realtime_baseline.max_note_events": 1,
                    "realtime_baseline.timeout_seconds": 0.0,
                    "realtime_baseline.idle_sleep_seconds": 0.0,
                    "realtime_baseline.event_logging": "summary",
                    "realtime_baseline.boot_audition_seconds": 0.6,
                }
            )
        )

        assert runtime is not None
