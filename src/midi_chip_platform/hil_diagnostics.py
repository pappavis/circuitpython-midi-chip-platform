# Bestand: hil_diagnostics.py
# Versienommer: 0.21.0
# Doel: Lewer bounded, layered HIL-diagnostiek sonder produkgedrag te verander.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: HIL-DIAGNOSTIC-FRAMEWORK-001 Deterministic HIL Diagnostic Framework
# Actienr: HIL-DIAG-GREEN-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / HIL-DIAGNOSTIC-FRAMEWORK-001

from midi_chip_platform.audio import AudioBlock, AudioStreamFormat
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.events import NoteEvent
from midi_chip_platform.ports import ConfigurationPort
from midi_chip_platform.release import ReleaseMetadata


class HilLayerResult:
    def __init__(self, code, status, name, details=None):
        selected_status = str(status).upper()
        if selected_status not in ("PASS", "FAIL", "UNKNOWN"):
            raise ValueError("HIL layer status must be PASS, FAIL or UNKNOWN")
        self._code = str(code)
        self._status = selected_status
        self._name = str(name)
        self._details = tuple(str(detail) for detail in (details or ()))

    @property
    def code(self):
        return self._code

    @property
    def status(self):
        return self._status

    @property
    def name(self):
        return self._name

    @property
    def details(self):
        return self._details

    @property
    def is_fail(self):
        return self._status == "FAIL"

    def summary_line(self):
        return f"{self._code} {self._status} {self._name}"

    def detail_lines(self):
        return tuple(f"{self._code}_DETAIL {detail}" for detail in self._details)


class HilBootSummary:
    def __init__(self, results):
        self._results = tuple(results)

    @property
    def results(self):
        return self._results

    @property
    def first_fail(self):
        for result in self._results:
            if result.is_fail:
                return result.code
        return "NONE"

    def lines(self):
        lines = []
        for result in self._results:
            lines.append(result.summary_line())
            lines.extend(result.detail_lines())
        lines.append("")
        lines.append("Overall:")
        lines.append(f"FIRST FAIL = {self.first_fail}")
        return tuple(lines)


class SafeHilLayer:
    def __init__(self, code, name):
        self._code = str(code)
        self._name = str(name)

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    def run(self):
        try:
            return self._run()
        except Exception as error:
            return HilLayerResult(
                self._code,
                "UNKNOWN",
                self._name,
                (f"reason={error.__class__.__name__}",),
            )

    def _run(self):
        raise NotImplementedError("SafeHilLayer._run must be implemented")

    def _result(self, status, details=None):
        return HilLayerResult(self._code, status, self._name, details)


class DeploymentIntegrityLayer(SafeHilLayer):
    def __init__(
        self,
        release_metadata,
        file_reader,
        hasher,
        expected_version=None,
        expected_release_date=None,
        expected_story=None,
        expected_code_checksum=None,
        expected_boot_checksum=None,
    ):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        super().__init__("HIL-000", "Deployment")
        self._release_metadata = release_metadata
        self._file_reader = file_reader
        self._hasher = hasher
        self._expected_version = expected_version
        self._expected_release_date = expected_release_date
        self._expected_story = expected_story
        self._expected_code_checksum = expected_code_checksum
        self._expected_boot_checksum = expected_boot_checksum

    def _run(self):
        details = (
            f"release_version={self._release_metadata.version}",
            f"release_date={self._release_metadata.release_date}",
            f"git_story={self._release_metadata.user_story}",
            f"runtime_banner={self._release_metadata.banner()}",
            f"code.py={self._checksum_for('code.py')}",
            f"boot.py={self._checksum_for('boot.py')}",
        )
        mismatches = []
        self._append_mismatch(
            mismatches,
            "release_version",
            self._expected_version,
            self._release_metadata.version,
        )
        self._append_mismatch(
            mismatches,
            "release_date",
            self._expected_release_date,
            self._release_metadata.release_date,
        )
        self._append_mismatch(
            mismatches,
            "git_story",
            self._expected_story,
            self._release_metadata.user_story,
        )
        self._append_mismatch(
            mismatches,
            "code.py",
            self._expected_code_checksum,
            self._checksum_for("code.py"),
        )
        self._append_mismatch(
            mismatches,
            "boot.py",
            self._expected_boot_checksum,
            self._checksum_for("boot.py"),
        )
        if mismatches:
            return self._result("FAIL", details + tuple(mismatches))
        if self._has_expected_values():
            return self._result("PASS", details)
        return self._result("UNKNOWN", details + ("reason=expected-values-missing",))

    def _checksum_for(self, path):
        data = self._file_reader.read_bytes(path)
        return self._hasher.sha256_hex(data)

    def _has_expected_values(self):
        return all(
            value is not None
            for value in (
                self._expected_version,
                self._expected_release_date,
                self._expected_story,
                self._expected_code_checksum,
                self._expected_boot_checksum,
            )
        )

    @staticmethod
    def _append_mismatch(mismatches, label, expected, actual):
        if expected is not None and str(expected) != str(actual):
            mismatches.append(f"mismatch={label};expected={expected};actual={actual}")


class UsbEnumerationLayer(SafeHilLayer):
    def __init__(self, usb_midi_module):
        super().__init__("HIL-010", "USB")
        self._usb_midi_module = usb_midi_module

    def _run(self):
        ports = tuple(getattr(self._usb_midi_module, "ports", ()))
        details = [f"port_count={len(ports)}"]
        input_count = 0
        output_count = 0
        for index, port in enumerate(ports):
            direction = self._direction_for(port)
            if direction == "input":
                input_count += 1
            if direction == "output":
                output_count += 1
            details.append(
                f"port={index};direction={direction};descriptor={self._descriptor_for(port)};"
                f"endpoint_available={str(direction != 'unknown').lower()}"
            )
        if input_count <= 0 or output_count <= 0:
            return self._result(
                "FAIL",
                tuple(details)
                + (f"inputs={input_count};outputs={output_count};reason=missing-endpoint",),
            )
        return self._result(
            "PASS",
            tuple(details) + (f"inputs={input_count};outputs={output_count}",),
        )

    @staticmethod
    def _direction_for(port):
        type_name = type(port).__name__
        if "PortIn" in type_name or callable(getattr(port, "read", None)):
            return "input"
        if "PortOut" in type_name or callable(getattr(port, "write", None)):
            return "output"
        return "unknown"

    @staticmethod
    def _descriptor_for(port):
        for attribute_name in ("name", "descriptor", "label"):
            value = getattr(port, attribute_name, None)
            if value is not None:
                return str(value)
        return type(port).__name__


class RawUsbMidiLayer(SafeHilLayer):
    def __init__(
        self,
        port,
        monotonic,
        sleeper,
        max_packets=8,
        timeout_seconds=0.25,
        read_size=4,
    ):
        super().__init__("HIL-020", "Raw MIDI")
        self._port = port
        self._monotonic = monotonic
        self._sleeper = sleeper
        self._max_packets = int(max_packets)
        self._timeout_seconds = float(timeout_seconds)
        self._read_size = int(read_size)

    def _run(self):
        packet_count = 0
        byte_count = 0
        first_packet_at = None
        started_at = self._monotonic()
        while packet_count < self._max_packets:
            now = self._monotonic()
            if now - started_at >= self._timeout_seconds:
                break
            packet = self._port.read(self._read_size)
            if packet:
                packet_count += 1
                byte_count += len(packet)
                if first_packet_at is None:
                    first_packet_at = now
            else:
                self._sleeper(0.001)
        elapsed = max(self._monotonic() - started_at, 0.000001)
        details = (
            f"first_packet_timestamp={self._timestamp_label(first_packet_at)}",
            f"packet_count={packet_count}",
            f"bytes_received={byte_count}",
            f"packet_rate={packet_count / elapsed:.3f}",
        )
        if packet_count <= 0:
            return self._result("UNKNOWN", details + ("reason=no-raw-packets",))
        return self._result("PASS", details)

    @staticmethod
    def _timestamp_label(value):
        if value is None:
            return "none"
        return f"{float(value):.6f}"


class AdafruitMidiParserLayer(SafeHilLayer):
    def __init__(
        self,
        midi_object,
        note_on_type,
        note_off_type,
        monotonic,
        sleeper,
        max_messages=8,
        timeout_seconds=0.25,
    ):
        super().__init__("HIL-030", "MIDI Parser")
        self._midi_object = midi_object
        self._note_on_type = note_on_type
        self._note_off_type = note_off_type
        self._monotonic = monotonic
        self._sleeper = sleeper
        self._max_messages = int(max_messages)
        self._timeout_seconds = float(timeout_seconds)

    def _run(self):
        decoded = 0
        unknown = 0
        parser_errors = 0
        note_on = 0
        note_off = 0
        histogram = VelocityHistogram()
        started_at = self._monotonic()
        while decoded + unknown + parser_errors < self._max_messages:
            if self._monotonic() - started_at >= self._timeout_seconds:
                break
            try:
                message = self._midi_object.receive()
            except Exception:
                parser_errors += 1
                continue
            if message is None:
                self._sleeper(0.001)
                continue
            if isinstance(message, self._note_on_type):
                decoded += 1
                note_on += 1
                histogram.record(getattr(message, "velocity", 0))
                continue
            if isinstance(message, self._note_off_type):
                decoded += 1
                note_off += 1
                histogram.record(getattr(message, "velocity", 0))
                continue
            unknown += 1
        details = (
            f"messages_decoded={decoded}",
            f"unknown_messages={unknown}",
            f"parser_errors={parser_errors}",
            f"note_on={note_on}",
            f"note_off={note_off}",
            f"velocity_histogram={histogram.label()}",
        )
        if parser_errors > 0:
            return self._result("FAIL", details)
        if decoded + unknown <= 0:
            return self._result("UNKNOWN", details + ("reason=no-parser-messages",))
        return self._result("PASS", details)


class VelocityHistogram:
    def __init__(self):
        self._buckets = {
            "0": 0,
            "1-31": 0,
            "32-63": 0,
            "64-95": 0,
            "96-127": 0,
        }

    def record(self, velocity):
        selected_velocity = int(velocity)
        if selected_velocity <= 0:
            self._buckets["0"] += 1
        elif selected_velocity <= 31:
            self._buckets["1-31"] += 1
        elif selected_velocity <= 63:
            self._buckets["32-63"] += 1
        elif selected_velocity <= 95:
            self._buckets["64-95"] += 1
        else:
            self._buckets["96-127"] += 1

    def label(self):
        return ",".join(f"{key}:{value}" for key, value in self._buckets.items())


class SchedulerLayer(SafeHilLayer):
    def __init__(self, scheduler=None):
        super().__init__("HIL-040", "Scheduler")
        self._scheduler = scheduler

    def _run(self):
        if self._scheduler is None:
            return self._result("UNKNOWN", ("reason=no-scheduler-probe",))
        details = (
            f"enqueue_count={self._value('enqueue_count')}",
            f"dequeue_count={self._value('dequeue_count')}",
            f"queue_depth={self._value('queue_depth')}",
            f"queue_overflow={self._value('queue_overflow')}",
            f"oldest_event_latency={self._value('oldest_event_latency')}",
        )
        if int(self._value("queue_overflow", 0)) > 0:
            return self._result("FAIL", details)
        return self._result("PASS", details)

    def _value(self, name, default=0):
        return getattr(self._scheduler, name, default)


class VoiceAllocatorLayer(SafeHilLayer):
    def __init__(self, allocator=None):
        super().__init__("HIL-050", "Voices")
        self._allocator = allocator

    def _run(self):
        if self._allocator is None:
            return self._result("UNKNOWN", ("reason=no-voice-allocator-probe",))
        details = (
            f"voices_allocated={self._value('voices_allocated')}",
            f"voices_released={self._value('voices_released')}",
            f"steals={self._value('steals')}",
            f"ignored_notes={self._value('ignored_notes')}",
        )
        if int(self._value("ignored_notes", 0)) > 0:
            return self._result("FAIL", details)
        return self._result("PASS", details)

    def _value(self, name, default=0):
        return getattr(self._allocator, name, default)


class PcmGeneratorLayer(SafeHilLayer):
    def __init__(self, core=None):
        super().__init__("HIL-060", "PCM")
        self._core = core

    def _run(self):
        selected_core = self._core
        if selected_core is None:
            selected_core = D1SynthCore(
                D1Patch(
                    waveform="square",
                    audio_format=AudioStreamFormat(sample_rate=16000, frames_per_block=128),
                    amplitude=0.2,
                )
            )
        selected_core.start()
        selected_core.handle_event(NoteEvent.note_on(1, 69, 100))
        block = selected_core.render_audio_block()
        selected_core.stop()
        peak = max(abs(sample) for sample in block.samples)
        rms = self._rms_for(block)
        clipping = sum(1 for sample in block.samples if abs(sample) >= 32767)
        details = (
            "pcm_blocks_produced=1",
            f"peak_amplitude={peak}",
            f"rms={rms:.3f}",
            f"clipping_count={clipping}",
        )
        if peak <= 0:
            return self._result("FAIL", details)
        return self._result("PASS", details)

    @staticmethod
    def _rms_for(block):
        total = sum(sample * sample for sample in block.samples)
        return (total / len(block.samples)) ** 0.5


class I2sDmaLayer(SafeHilLayer):
    def __init__(self, dma_probe=None):
        super().__init__("HIL-070", "DMA")
        self._dma_probe = dma_probe

    def _run(self):
        if self._dma_probe is None:
            return self._result("UNKNOWN", ("reason=no-dma-probe",))
        details = (
            f"dma_writes={self._value('dma_writes')}",
            f"underruns={self._value('underruns')}",
            f"buffer_starvation={self._value('buffer_starvation')}",
        )
        if int(self._value("underruns", 0)) > 0 or int(self._value("buffer_starvation", 0)) > 0:
            return self._result("FAIL", details)
        return self._result("PASS", details)

    def _value(self, name, default=0):
        return getattr(self._dma_probe, name, default)


class AmplifierLayer(SafeHilLayer):
    def __init__(self, audio_format=None, amplitude=2048, duration_seconds=0.05):
        super().__init__("HIL-080", "Audio")
        self._audio_format = (
            audio_format
            if audio_format is not None
            else AudioStreamFormat(sample_rate=16000, frames_per_block=128)
        )
        self._amplitude = int(amplitude)
        self._duration_seconds = float(duration_seconds)

    def _run(self):
        details = []
        for frequency in (440.0, 880.0):
            block = self._block_for(frequency)
            peak = max(abs(sample) for sample in block.samples)
            duration = block.frame_count / self._audio_format.sample_rate
            details.append(
                f"frequency={frequency:.1f};duration={duration:.6f};pcm_amplitude={peak}"
            )
            if peak <= 0:
                return self._result("FAIL", tuple(details))
        return self._result("PASS", tuple(details))

    def _block_for(self, frequency):
        period_length = max(2, int(round(self._audio_format.sample_rate / float(frequency))))
        half_period = max(1, period_length // 2)
        samples = []
        while len(samples) < self._audio_format.frames_per_block:
            position = len(samples) % period_length
            samples.append(self._amplitude if position < half_period else -self._amplitude)
        return AudioBlock(self._audio_format, samples)


class HardwareInLoopDiagnosticRuntime:
    def __init__(self, layers, output=None):
        self._layers = tuple(layers)
        self._output = output if output is not None else print

    def run(self):
        results = []
        for layer in self._layers:
            result = layer.run()
            results.append(result)
            if result.code == "HIL-000" and result.is_fail:
                break
        summary = HilBootSummary(results)
        for line in summary.lines():
            self._output(line)
        return summary.first_fail == "NONE"


class HilMvp001TimingRecorder:
    def __init__(
        self,
        monotonic,
        expected_note=60,
        expected_velocity=100,
        average_limit_ms=25,
        maximum_limit_ms=100,
        single_event_limit_ms=250,
        fail_limit_ms=1000,
        critical_limit_ms=10000,
    ):
        self._monotonic = monotonic
        self._expected_note = int(expected_note)
        self._expected_velocity = int(expected_velocity)
        self._average_limit_ms = int(average_limit_ms)
        self._maximum_limit_ms = int(maximum_limit_ms)
        self._single_event_limit_ms = int(single_event_limit_ms)
        self._fail_limit_ms = int(fail_limit_ms)
        self._critical_limit_ms = int(critical_limit_ms)
        self._timestamps = {}
        self._event = None
        self._emitted = False

    @property
    def is_emitted(self):
        return self._emitted

    def record_raw_message(self, port_index, message):
        if self._emitted or message is None:
            return
        self._record_once("USB receive")

    def record_decoded_event(self, port_index, message, event):
        if self._emitted or not isinstance(event, NoteEvent):
            return
        if not event.is_note_on or event.velocity <= 0:
            return
        if event.note != self._expected_note:
            return
        self._event = event
        self._record_once("Parser")

    def record_scheduler(self, event):
        if self._matches(event):
            self._record_once("Scheduler")

    def record_pcm(self, event):
        if self._matches(event):
            self._record_once("PCM")

    def record_play_tone_entered(self, event):
        if self._matches(event):
            self._record_once("play_tone entered")

    def record_play_tone_returned(self, event):
        if self._matches(event):
            self._record_once("play_tone returned")

    def record_i2s_dma_write(self):
        if self._emitted or self._event is None:
            return
        self._record_once("I2S first DMA write")

    def emit_if_ready(self, output):
        if self._emitted or "play_tone returned" not in self._timestamps:
            return False
        for line in self._lines():
            output(line)
        self._emitted = True
        return True

    def _matches(self, event):
        return (
            isinstance(event, NoteEvent)
            and event.is_note_on
            and event.velocity > 0
            and event.note == self._expected_note
        )

    def _record_once(self, layer):
        if layer not in self._timestamps:
            self._timestamps[layer] = self._monotonic()

    def _lines(self):
        lines = [
            "HIL-MVP-001 START",
            "HIL-MVP-001 EXPECTED="
            f"note={self._expected_note};velocity={self._expected_velocity}",
            "HIL-MVP-001 TABLE=Timestamp|Layer|LatencyMs|DeltaMs|Result",
        ]
        latencies = []
        previous_latency = None
        for marker, layer in (
            ("T0", "USB receive"),
            ("T1", "Parser"),
            ("T2", "Scheduler"),
            ("T3", "play_tone entered"),
            ("T4", "play_tone returned"),
            ("T5", "I2S first DMA write"),
        ):
            latency = self._latency_ms(layer)
            delta = self._delta_ms(previous_latency, latency)
            result = self._result_for(latency)
            if latency is not None:
                latencies.append(latency)
                previous_latency = latency
            lines.append(
                f"HIL-MVP-001 ROW={marker}|{layer}|"
                f"{self._latency_label(latency)}|{self._latency_label(delta)}|{result}"
            )
        lines.append(f"HIL-MVP-001 LARGEST_DELTA={self._largest_delta_line()}")
        lines.append(f"HIL-MVP-001 RESULT={self._overall_result(latencies)}")
        return tuple(lines)

    def _latency_ms(self, layer):
        if "USB receive" not in self._timestamps or layer not in self._timestamps:
            return None
        return int(
            round(
                (self._timestamps[layer] - self._timestamps["USB receive"])
                * 1000.0
            )
        )

    @staticmethod
    def _latency_label(latency):
        if latency is None:
            return "UNKNOWN"
        return str(int(latency))

    @staticmethod
    def _delta_ms(previous_latency, current_latency):
        if previous_latency is None or current_latency is None:
            return None
        return int(current_latency) - int(previous_latency)

    def _largest_delta_line(self):
        largest = None
        previous_latency = None
        previous_layer = None
        for layer in (
            "USB receive",
            "Parser",
            "Scheduler",
            "play_tone entered",
            "play_tone returned",
            "I2S first DMA write",
        ):
            latency = self._latency_ms(layer)
            if latency is None:
                previous_layer = layer
                previous_latency = latency
                continue
            if previous_latency is not None:
                delta = int(latency) - int(previous_latency)
                if largest is None or delta > largest[2]:
                    largest = (previous_layer, layer, delta)
            previous_layer = layer
            previous_latency = latency
        if largest is None:
            return "UNKNOWN"
        return f"{largest[0]}->{largest[1]};delta_ms={largest[2]}"

    def _result_for(self, latency):
        if latency is None:
            return "UNKNOWN"
        if latency > self._critical_limit_ms:
            return "CRITICAL_BLOCKER"
        if latency > self._fail_limit_ms:
            return "FAIL"
        if latency > self._single_event_limit_ms:
            return "FAIL"
        if latency > self._maximum_limit_ms:
            return "FAIL"
        return "PASS"

    def _overall_result(self, latencies):
        if len(latencies) < 6:
            return "FAIL;reason=missing-layer-timestamp"
        worst = max(latencies)
        average = sum(latencies) / len(latencies)
        if worst > self._critical_limit_ms:
            return f"CRITICAL_BLOCKER;average_ms={average:.3f};worst_ms={worst}"
        if worst > self._fail_limit_ms:
            return f"FAIL;average_ms={average:.3f};worst_ms={worst}"
        if worst > self._single_event_limit_ms:
            return f"FAIL;average_ms={average:.3f};worst_ms={worst}"
        if average >= self._average_limit_ms or worst >= self._maximum_limit_ms:
            return f"FAIL;average_ms={average:.3f};worst_ms={worst}"
        return f"PASS;average_ms={average:.3f};worst_ms={worst}"


class NullHilMvp001TimingRecorder:
    def __init__(self):
        self._record_count = 0

    @property
    def record_count(self):
        return self._record_count

    def record_raw_message(self, port_index, message):
        self._record_count += 1

    def record_decoded_event(self, port_index, message, event):
        self._record_count += 1

    def record_scheduler(self, event):
        self._record_count += 1

    def record_pcm(self, event):
        self._record_count += 1

    def record_play_tone_entered(self, event):
        self._record_count += 1

    def record_play_tone_returned(self, event):
        self._record_count += 1

    def record_i2s_dma_write(self):
        self._record_count += 1

    def emit_if_ready(self, output):
        self._record_count += 1
        return False


class CircuitPythonFileReader:
    def __init__(self, root=""):
        self._root = str(root)

    def read_bytes(self, path):
        selected_path = self._path_for(path)
        with open(selected_path, "rb") as handle:
            return handle.read()

    def _path_for(self, path):
        if not self._root:
            return str(path)
        return self._root.rstrip("/") + "/" + str(path).lstrip("/")


class Sha256Hasher:
    def __init__(self, hashlib_module):
        self._hashlib_module = hashlib_module

    def sha256_hex(self, data):
        digest = self._hashlib_module.sha256()
        digest.update(data)
        return digest.hexdigest()


class CircuitPythonHilDiagnosticFactory:
    def __init__(self, release_metadata, importer=None, output=None):
        if not isinstance(release_metadata, ReleaseMetadata):
            raise TypeError("release_metadata must be ReleaseMetadata")
        self._release_metadata = release_metadata
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not isinstance(configuration, ConfigurationPort):
            raise TypeError("configuration must implement ConfigurationPort")
        if not configuration.get("hil.diagnostic.enabled", False):
            return None
        time_module = self._importer("time")
        usb_midi_module = self._importer("usb_midi")
        hashlib_module = self._importer("hashlib")
        layers = self._layers_for(configuration, time_module, usb_midi_module, hashlib_module)
        return HardwareInLoopDiagnosticRuntime(layers=layers, output=self._output)

    def _layers_for(self, configuration, time_module, usb_midi_module, hashlib_module):
        return (
            DeploymentIntegrityLayer(
                release_metadata=self._release_metadata,
                file_reader=CircuitPythonFileReader(),
                hasher=Sha256Hasher(hashlib_module),
                expected_version=configuration.get("hil.deployment.expected_version"),
                expected_release_date=configuration.get("hil.deployment.expected_release_date"),
                expected_story=configuration.get("hil.deployment.expected_story"),
                expected_code_checksum=configuration.get("hil.deployment.expected_code_checksum"),
                expected_boot_checksum=configuration.get("hil.deployment.expected_boot_checksum"),
            ),
            UsbEnumerationLayer(usb_midi_module),
            RawUsbMidiLayer(
                port=self._first_input_port(usb_midi_module),
                monotonic=time_module.monotonic,
                sleeper=time_module.sleep,
                max_packets=configuration.get("hil.raw_midi.max_packets", 8),
                timeout_seconds=configuration.get("hil.raw_midi.timeout_seconds", 0.25),
            ),
            self._parser_layer(configuration, time_module, usb_midi_module),
            SchedulerLayer(),
            VoiceAllocatorLayer(),
            PcmGeneratorLayer(),
            I2sDmaLayer(),
            AmplifierLayer(),
        )

    def _parser_layer(self, configuration, time_module, usb_midi_module):
        adafruit_midi = self._importer("adafruit_midi", None, None, ("MIDI",))
        note_on_module = self._importer("adafruit_midi.note_on", None, None, ("NoteOn",))
        note_off_module = self._importer("adafruit_midi.note_off", None, None, ("NoteOff",))
        return AdafruitMidiParserLayer(
            midi_object=adafruit_midi.MIDI(
                midi_in=self._first_input_port(usb_midi_module),
                in_channel=None,
            ),
            note_on_type=note_on_module.NoteOn,
            note_off_type=note_off_module.NoteOff,
            monotonic=time_module.monotonic,
            sleeper=time_module.sleep,
            max_messages=configuration.get("hil.parser.max_messages", 8),
            timeout_seconds=configuration.get("hil.parser.timeout_seconds", 0.25),
        )

    @staticmethod
    def _first_input_port(usb_midi_module):
        for port in tuple(getattr(usb_midi_module, "ports", ())):
            if callable(getattr(port, "read", None)):
                return port
        return MissingUsbMidiInputPort()


class MissingUsbMidiInputPort:
    def read(self, nbytes=None):
        return None
