# Bestand: test_hil_diagnostics.py
# Versienommer: 0.21.0
# Doel: Spesifiseer elke deterministiese HIL-diagnostieklaag en boot summary.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: HIL-DIAGNOSTIC-FRAMEWORK-001 Deterministic HIL Diagnostic Framework
# Actienr: HIL-DIAG-RED-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / HIL-DIAGNOSTIC-FRAMEWORK-001

import pytest

from midi_chip_platform.hil_diagnostics import (
    AdafruitMidiParserLayer,
    AmplifierLayer,
    DeploymentIntegrityLayer,
    HardwareInLoopDiagnosticRuntime,
    HilBootSummary,
    HilLayerResult,
    HilMvp001TimingRecorder,
    I2sDmaLayer,
    PcmGeneratorLayer,
    RawUsbMidiLayer,
    SchedulerLayer,
    Sha256Hasher,
    UsbEnumerationLayer,
    VoiceAllocatorLayer,
)
from midi_chip_platform.events import NoteEvent
from midi_chip_platform.release import ReleaseMetadata


class TestHilDiagnostics:
    class FakeHashlib:
        class FakeDigest:
            def __init__(self):
                self._data = b""

            def update(self, data):
                self._data += bytes(data)

            def hexdigest(self):
                return "sha-" + self._data.decode("utf-8")

        def sha256(self):
            return TestHilDiagnostics.FakeHashlib.FakeDigest()

    class FakeReader:
        def __init__(self, values):
            self._values = dict(values)

        def read_bytes(self, path):
            return self._values[str(path)]

    class FakePortIn:
        name = "input-jack"

        def __init__(self, packets=None):
            self._packets = list(packets or [])

        def read(self, nbytes=None):
            if not self._packets:
                return None
            return self._packets.pop(0)

    class FakePortOut:
        descriptor = "output-jack"

        def write(self, buffer):
            return len(buffer)

    class FakeUsbMidi:
        def __init__(self, ports):
            self.ports = tuple(ports)

    class FakeClock:
        def __init__(self):
            self._now = 0.0
            self.sleeps = []

        def monotonic(self):
            self._now += 0.001
            return self._now

        def sleep(self, seconds):
            self.sleeps.append(seconds)
            self._now += float(seconds)

    class FakeNoteOn:
        def __init__(self, velocity=100):
            self.velocity = int(velocity)

    class FakeNoteOff:
        def __init__(self, velocity=64):
            self.velocity = int(velocity)

    class FakeMidiObject:
        def __init__(self, messages):
            self._messages = list(messages)

        def receive(self):
            if not self._messages:
                return None
            message = self._messages.pop(0)
            if isinstance(message, Exception):
                raise message
            return message

    class FakeScheduler:
        enqueue_count = 3
        dequeue_count = 2
        queue_depth = 1
        queue_overflow = 0
        oldest_event_latency = 0.003

    class FakeVoiceAllocator:
        voices_allocated = 2
        voices_released = 2
        steals = 0
        ignored_notes = 0

    class FakeDmaProbe:
        dma_writes = 5
        underruns = 0
        buffer_starvation = 0

    class StaticLayer:
        def __init__(self, result):
            self._result = result

        def run(self):
            return self._result

    @pytest.mark.smoke
    def test_layer_0_passes_when_deployment_identity_matches(self) -> None:
        layer = DeploymentIntegrityLayer(
            release_metadata=ReleaseMetadata(
                version="0.21.0",
                user_story="HIL-DIAGNOSTIC-FRAMEWORK-001",
                release_date="2026-07-24",
            ),
            file_reader=self.FakeReader({"code.py": b"code", "boot.py": b"boot"}),
            hasher=Sha256Hasher(self.FakeHashlib()),
            expected_version="0.21.0",
            expected_release_date="2026-07-24",
            expected_story="HIL-DIAGNOSTIC-FRAMEWORK-001",
            expected_code_checksum="sha-code",
            expected_boot_checksum="sha-boot",
        )

        result = layer.run()

        assert result.summary_line() == "HIL-000 PASS Deployment"
        assert "code.py=sha-code" in result.details

    def test_layer_0_fails_on_deployment_checksum_mismatch(self) -> None:
        layer = DeploymentIntegrityLayer(
            release_metadata=ReleaseMetadata(version="0.21.0"),
            file_reader=self.FakeReader({"code.py": b"code", "boot.py": b"boot"}),
            hasher=Sha256Hasher(self.FakeHashlib()),
            expected_code_checksum="different",
        )

        result = layer.run()

        assert result.status == "FAIL"
        assert any("mismatch=code.py" in detail for detail in result.details)

    @pytest.mark.smoke
    def test_layer_1_reports_usb_midi_ports_and_missing_endpoints(self) -> None:
        passing = UsbEnumerationLayer(
            self.FakeUsbMidi((self.FakePortIn(), self.FakePortOut()))
        ).run()
        failing = UsbEnumerationLayer(self.FakeUsbMidi((self.FakePortIn(),))).run()

        assert passing.summary_line() == "HIL-010 PASS USB"
        assert "inputs=1;outputs=1" in passing.details
        assert failing.summary_line() == "HIL-010 FAIL USB"

    @pytest.mark.smoke
    def test_layer_2_reports_raw_usb_midi_packets_without_decoding(self) -> None:
        clock = self.FakeClock()
        layer = RawUsbMidiLayer(
            port=self.FakePortIn((b"\x09\x90\x3c\x40", b"\x08\x80\x3c\x00")),
            monotonic=clock.monotonic,
            sleeper=clock.sleep,
            max_packets=2,
            timeout_seconds=0.1,
        )

        result = layer.run()

        assert result.summary_line() == "HIL-020 PASS Raw MIDI"
        assert "packet_count=2" in result.details
        assert "bytes_received=8" in result.details

    @pytest.mark.smoke
    def test_layer_3_reports_parser_counts_and_velocity_histogram(self) -> None:
        clock = self.FakeClock()
        layer = AdafruitMidiParserLayer(
            midi_object=self.FakeMidiObject(
                (self.FakeNoteOn(100), self.FakeNoteOff(64), object())
            ),
            note_on_type=self.FakeNoteOn,
            note_off_type=self.FakeNoteOff,
            monotonic=clock.monotonic,
            sleeper=clock.sleep,
            max_messages=3,
            timeout_seconds=0.1,
        )

        result = layer.run()

        assert result.summary_line() == "HIL-030 PASS MIDI Parser"
        assert "messages_decoded=2" in result.details
        assert "unknown_messages=1" in result.details
        assert "note_on=1" in result.details
        assert "note_off=1" in result.details
        assert "velocity_histogram=0:0,1-31:0,32-63:0,64-95:1,96-127:1" in result.details

    @pytest.mark.smoke
    def test_layer_4_reports_scheduler_metrics(self) -> None:
        result = SchedulerLayer(self.FakeScheduler()).run()

        assert result.summary_line() == "HIL-040 PASS Scheduler"
        assert "enqueue_count=3" in result.details
        assert "oldest_event_latency=0.003" in result.details

    def test_layer_5_reports_voice_allocator_metrics(self) -> None:
        result = VoiceAllocatorLayer(self.FakeVoiceAllocator()).run()

        assert result.summary_line() == "HIL-050 PASS Voices"
        assert "voices_allocated=2" in result.details
        assert "ignored_notes=0" in result.details

    def test_layer_6_reports_pcm_blocks_peak_rms_and_clipping(self) -> None:
        result = PcmGeneratorLayer().run()

        assert result.summary_line() == "HIL-060 PASS PCM"
        assert "pcm_blocks_produced=1" in result.details
        assert any(detail.startswith("peak_amplitude=") for detail in result.details)
        assert "clipping_count=0" in result.details

    def test_layer_7_reports_dma_unknown_without_probe_and_pass_with_probe(self) -> None:
        unknown = I2sDmaLayer().run()
        passing = I2sDmaLayer(self.FakeDmaProbe()).run()

        assert unknown.summary_line() == "HIL-070 UNKNOWN DMA"
        assert passing.summary_line() == "HIL-070 PASS DMA"
        assert "dma_writes=5" in passing.details

    @pytest.mark.smoke
    def test_layer_8_reports_amplifier_tone_amplitudes(self) -> None:
        result = AmplifierLayer().run()

        assert result.summary_line() == "HIL-080 PASS Audio"
        assert any("frequency=440.0" in detail for detail in result.details)
        assert any("frequency=880.0" in detail for detail in result.details)

    def test_boot_summary_identifies_first_failing_layer(self) -> None:
        results = (
            HilLayerResult("HIL-010", "PASS", "USB"),
            HilLayerResult("HIL-030", "FAIL", "MIDI Parser"),
            HilLayerResult("HIL-040", "UNKNOWN", "Scheduler"),
        )

        lines = HilBootSummary(results).lines()

        assert lines[0] == "HIL-010 PASS USB"
        assert lines[1] == "HIL-030 FAIL MIDI Parser"
        assert lines[-1] == "FIRST FAIL = HIL-030"

    @pytest.mark.smoke
    def test_hil_mvp_001_reports_timing_table_for_middle_c(self) -> None:
        clock = self.FakeClock()
        output = []
        event = NoteEvent.note_on(channel=1, note=60, velocity=100)
        recorder = HilMvp001TimingRecorder(
            monotonic=clock.monotonic,
            expected_note=60,
            expected_velocity=100,
        )

        recorder.record_raw_message(0, object())
        recorder.record_decoded_event(0, object(), event)
        recorder.record_scheduler(event)
        recorder.record_pcm(event)
        recorder.record_play_tone_entered(event)
        recorder.record_i2s_dma_write()
        recorder.record_play_tone_returned(event)
        emitted = recorder.emit_if_ready(output.append)

        assert emitted is True
        assert output[0] == "HIL-MVP-001 START"
        assert "HIL-MVP-001 TABLE=Timestamp|Layer|LatencyMs|DeltaMs|Result" in output
        assert any(line.startswith("HIL-MVP-001 ROW=T0|USB receive|0|") for line in output)
        assert any(line.startswith("HIL-MVP-001 ROW=T5|I2S first DMA write|") for line in output)
        assert any(line.startswith("HIL-MVP-001 LARGEST_DELTA=") for line in output)
        assert output[-1].startswith("HIL-MVP-001 RESULT=PASS")

    @pytest.mark.smoke
    def test_integration_hil_runtime_prints_one_summary(self) -> None:
        output = []
        layers = (
            self.StaticLayer(UsbEnumerationLayer(self.FakeUsbMidi((self.FakePortIn(), self.FakePortOut()))).run()),
            self.StaticLayer(SchedulerLayer().run()),
        )
        runtime = HardwareInLoopDiagnosticRuntime(layers=layers, output=output.append)

        result = runtime.run()

        assert result is True
        assert output.count("Overall:") == 1
        assert output[-1] == "FIRST FAIL = NONE"
