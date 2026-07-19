# Bestand: test_synthio_runtime.py
# Versienommer: 0.19.2
# Doel: Spesifiseer 'n permanente synthio audio graph met multi-port USB-MIDI scan.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-079 Persistent Synthio Audio Graph Spike
# Actienr: MCP-ACT-079-IMP-002-RED-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-079-HIL-IMPEDIMENT-002

from midi_chip_platform.events import NoteEvent
from midi_chip_platform.synthio_runtime import (
    SynthioBaselineProfile,
    SynthioBaselineRuntime,
    SynthioBaselineRuntimeFactory,
)
from midi_chip_platform.testing import MemoryConfiguration, MemoryMidiInput


class TestSynthioBaselineRuntime:
    class RecordingMidiInput(MemoryMidiInput):
        def __init__(self, events, calls):
            super().__init__(events)
            self._calls = calls

        def open(self):
            self._calls.append("midi_open")
            super().open()

        def close(self):
            self._calls.append("midi_close")
            super().close()

    class NoSleep:
        def __init__(self):
            self._now = 0.0
            self.calls = []

        def monotonic(self):
            return self._now

        def sleep(self, seconds):
            self.calls.append(float(seconds))
            self._now += float(seconds)

    class RecordingAudioGraph:
        def __init__(self):
            self.calls = []

        def open(self):
            self.calls.append("open")

        def press(self, note):
            self.calls.append(("press", int(note)))

        def release(self, note):
            self.calls.append(("release", int(note)))

        def release_all(self):
            self.calls.append("release_all")

        def close(self):
            self.calls.append("close")

    def test_profile_defaults_target_persistent_mono_realtime_audio(self) -> None:
        profile = SynthioBaselineProfile()

        assert profile.sample_rate == 16000
        assert profile.channel_count == 1
        assert profile.max_note_events == 0
        assert profile.timeout_seconds == 0.0
        assert profile.idle_sleep_seconds == 0.001
        assert profile.event_logging == "summary"
        assert profile.boot_audition_note == 69
        assert profile.boot_audition_seconds == 0.6
        assert profile.gate_seconds == 0.12
        assert profile.scan_all_midi_ports is True
        assert profile.midi_port_count == 1

    def test_runtime_presses_and_releases_notes_on_persistent_graph(self) -> None:
        output = []
        sleeper = self.NoSleep()
        graph = self.RecordingAudioGraph()
        calls = graph.calls
        runtime = SynthioBaselineRuntime(
            midi_input=self.RecordingMidiInput(
                (
                    NoteEvent.note_on(channel=1, note=60, velocity=90),
                    NoteEvent.note_off(channel=1, note=60, velocity=64),
                ),
                calls,
            ),
            audio_graph=graph,
            profile=SynthioBaselineProfile(
                max_note_events=1,
                event_logging="summary",
            ),
            output=output.append,
            sleeper=sleeper,
        )

        result = runtime.run()

        assert result is True
        assert runtime.note_on_count == 1
        assert graph.calls == [
            "open",
            ("press", 69),
            ("release", 69),
            "midi_open",
            ("press", 60),
            "release_all",
            "close",
            "midi_close",
        ]
        assert "SYNTHIO_BASELINE_AUDIO_STATUS=OPEN" in output
        assert "SYNTHIO_BASELINE_BOOT_AUDITION=START;note=69;seconds=0.600" in output
        assert "SYNTHIO_BASELINE_BOOT_AUDITION=PASS" in output
        assert (
            "SYNTHIO_BASELINE_MIDI_INPUT_STATUS=OPEN;"
            "scan_all_ports=true;port_count=1"
        ) in output
        assert "SYNTHIO_BASELINE_READY;ready_ms=600" in output
        assert any(line.startswith("SYNTHIO_BASELINE_NOTE_ON") for line in output)
        assert output[-1] == "SYNTHIO_BASELINE_STATUS=PASS;note_on=1;note_off=0;ignored=0"

    def test_runtime_releases_gate_when_no_note_off_arrives(self) -> None:
        output = []
        sleeper = self.NoSleep()
        graph = self.RecordingAudioGraph()
        runtime = SynthioBaselineRuntime(
            midi_input=MemoryMidiInput((NoteEvent.note_on(channel=1, note=64, velocity=90),)),
            audio_graph=graph,
            profile=SynthioBaselineProfile(
                max_note_events=0,
                timeout_seconds=0.2,
                idle_sleep_seconds=0.01,
                boot_audition_seconds=0.0,
                gate_seconds=0.12,
                event_logging="none",
            ),
            output=output.append,
            sleeper=sleeper,
        )

        result = runtime.run()

        assert result is True
        assert ("press", 64) in graph.calls
        assert ("release", 64) in graph.calls
        assert graph.calls[-2:] == ["release_all", "close"]

    def test_factory_is_disabled_by_default(self) -> None:
        runtime = SynthioBaselineRuntimeFactory().create_if_enabled(
            MemoryConfiguration({})
        )

        assert runtime is None

    def test_factory_creates_runtime_when_enabled(self) -> None:
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
                    return type("FakeUsbMidi", (), {"ports": (object(), object())})
                if module_name == "time":
                    return TestSynthioBaselineRuntime.NoSleep()
                raise ImportError(module_name)

        runtime = SynthioBaselineRuntimeFactory(
            importer=FakeImporter(),
            output=[].append,
        ).create_if_enabled(
            MemoryConfiguration(
                {
                    "synthio_baseline.enabled": True,
                    "synthio_baseline.sample_rate": 16000,
                    "synthio_baseline.channel_count": 1,
                    "synthio_baseline.max_note_events": 1,
                    "synthio_baseline.timeout_seconds": 0.0,
                    "synthio_baseline.idle_sleep_seconds": 0.001,
                    "synthio_baseline.event_logging": "summary",
                    "synthio_baseline.boot_audition_note": 69,
                    "synthio_baseline.boot_audition_seconds": 0.6,
                    "synthio_baseline.gate_seconds": 0.12,
                    "synthio_baseline.scan_all_midi_ports": True,
                }
            )
        )

        assert runtime is not None
