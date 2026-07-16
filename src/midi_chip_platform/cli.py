# Bestand: cli.py
# Versienommer: 0.15.0
# Doel: Bied IDE-onafhanklike D1-, platform- en HIL-diagnostiek.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-063 Portable D1 Baseline Synth Core
# Actienr: MCP-ACT-063-GREEN-005
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-063-START

import argparse
import sys

from midi_chip_platform.audio import AudioStreamFormat
from midi_chip_platform.ble_midi import BleMidiCapabilityGate, ImportModuleProbe
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.events import ClockEvent, ControlEvent, NoteEvent
from midi_chip_platform.hil import (
    HardwareInLoopDeployerFactory,
    HardwareInLoopVerifierFactory,
    SerialHardResetProbe,
)
from midi_chip_platform.midi_performance import MidiPerformanceState
from midi_chip_platform.release import ReleaseMetadata


class CommandLineApplication:
    def __init__(
        self,
        output=None,
        release_metadata=None,
        hil_verifier_factory=None,
        hil_deployer_factory=None,
        hil_reset_probe=None,
    ):
        self._output = output if output is not None else sys.stdout
        self._release_metadata = (
            release_metadata if release_metadata is not None else ReleaseMetadata()
        )
        self._hil_verifier_factory = (
            hil_verifier_factory
            if hil_verifier_factory is not None
            else HardwareInLoopVerifierFactory()
        )
        self._hil_deployer_factory = (
            hil_deployer_factory
            if hil_deployer_factory is not None
            else HardwareInLoopDeployerFactory()
        )
        self._hil_reset_probe = (
            hil_reset_probe if hil_reset_probe is not None else SerialHardResetProbe()
        )

    def run(self, arguments=None):
        self._output.write(f"{self._release_metadata.banner()}\n")
        parser = self._build_parser()
        parsed = parser.parse_args(arguments)
        if parsed.command == "diagnose":
            return self._diagnose()
        if parsed.command == "events-diagnose":
            return self._diagnose_events()
        if parsed.command == "ble-diagnose":
            return self._diagnose_ble(parsed)
        if parsed.command == "performance-diagnose":
            return self._diagnose_performance(parsed)
        if parsed.command == "d1-diagnose":
            return self._diagnose_d1(parsed)
        if parsed.command == "hil-verify":
            return self._hil_verify(parsed)
        if parsed.command == "hil-deploy":
            return self._hil_deploy(parsed)
        if parsed.command == "hil-reset":
            return self._hil_reset(parsed)
        parser.print_help(file=self._output)
        return 2

    @classmethod
    def console_entry(cls):
        return cls().run()

    def _build_parser(self):
        parser = argparse.ArgumentParser(prog="midi-chip-platform")
        subparsers = parser.add_subparsers(dest="command")
        subparsers.add_parser("diagnose", help="verify the import-safe host skeleton")
        subparsers.add_parser(
            "events-diagnose",
            help="verify portable note, control, pitch-bend and clock events",
        )
        ble_parser = subparsers.add_parser(
            "ble-diagnose",
            help="report BLE-MIDI support without starting radio services",
        )
        ble_parser.add_argument("--board-id", required=True)
        performance_parser = subparsers.add_parser(
            "performance-diagnose",
            help="normalize pitch bend and CC1 for one MIDI channel",
        )
        performance_parser.add_argument("--channel", type=int, default=1)
        performance_parser.add_argument("--pitch-bend", type=int, default=8192)
        performance_parser.add_argument("--modulation", type=int, default=0)
        performance_parser.add_argument("--pitch-bend-range", type=float, default=2.0)
        d1_parser = subparsers.add_parser(
            "d1-diagnose",
            help="render bounded sine, saw and square D1 PCM blocks",
        )
        d1_parser.add_argument("--note", type=int, default=69)
        d1_parser.add_argument("--velocity", type=int, default=100)
        d1_parser.add_argument("--sample-rate", type=int, default=16000)
        d1_parser.add_argument("--frames-per-block", type=int, default=128)
        hil_parser = subparsers.add_parser(
            "hil-verify",
            help="verify redacted CircuitPython connection, deployment and execution proof",
        )
        hil_parser.add_argument("--source-root", default=".")
        hil_parser.add_argument("--device-root", required=True)
        hil_parser.add_argument("--serial-port", required=True)
        deploy_parser = subparsers.add_parser(
            "hil-deploy",
            help="copy the dependency-closed project manifest without deleting device files",
        )
        deploy_parser.add_argument("--source-root", default=".")
        deploy_parser.add_argument("--device-root", required=True)
        deploy_parser.add_argument("--serial-port", required=True)
        reset_parser = subparsers.add_parser(
            "hil-reset",
            help="request a CircuitPython hard reset through the serial REPL",
        )
        reset_parser.add_argument("--serial-port", required=True)
        return parser

    def _diagnose(self):
        self._output.write("circuitpython-midi-chip-platform: host skeleton ready\n")
        self._output.write("hardware access: disabled\n")
        self._output.write("runtime state: class instances only\n")
        return 0

    def _diagnose_events(self):
        note = NoteEvent.note_on(channel=1, note=60, velocity=100)
        control = ControlEvent.control_change(channel=1, control=1, value=64)
        pitch_bend = ControlEvent.pitch_bend(channel=1, value=8192)
        clock = ClockEvent.timing_clock()
        self._output.write("EVENT_MODEL_STATUS=PASS\n")
        self._output.write(
            "NOTE_EVENT="
            f"{note.message_type}:channel={note.channel}:note={note.note}:"
            f"velocity={note.velocity}\n"
        )
        self._output.write(
            "CONTROL_EVENT="
            f"{control.message_type}:channel={control.channel}:control={control.control}:"
            f"value={control.value}\n"
        )
        self._output.write(
            "PITCH_BEND_EVENT="
            f"{pitch_bend.message_type}:channel={pitch_bend.channel}:"
            f"value={pitch_bend.value}\n"
        )
        self._output.write(f"CLOCK_EVENT={clock.message_type}:channel=none\n")
        return 0

    def _hil_verify(self, parsed):
        verifier = self._hil_verifier_factory.create(
            source_root=parsed.source_root,
            device_root=parsed.device_root,
            serial_port=parsed.serial_port,
            output=self._output,
        )
        return 0 if verifier.run() else 1

    def _hil_deploy(self, parsed):
        deployer = self._hil_deployer_factory.create(
            source_root=parsed.source_root,
            device_root=parsed.device_root,
            serial_port=parsed.serial_port,
            output=self._output,
        )
        return 0 if deployer.deploy() else 1

    def _hil_reset(self, parsed):
        self._hil_reset_probe.reset(parsed.serial_port)
        self._output.write("HIL_RESET_STATUS=REQUESTED\n")
        self._output.write("private-identifiers: REDACTED\n")
        return 0

    def _diagnose_ble(self, parsed):
        capability = BleMidiCapabilityGate().evaluate(
            board_id=parsed.board_id,
            module_probe=ImportModuleProbe(),
        )
        self._output.write(f"{capability.report_line()}\n")
        return 0 if capability.is_supported else 1

    def _diagnose_performance(self, parsed):
        state = MidiPerformanceState(pitch_bend_range=parsed.pitch_bend_range)
        state.process(ControlEvent.pitch_bend(parsed.channel, parsed.pitch_bend))
        state.process(ControlEvent.control_change(parsed.channel, 1, parsed.modulation))
        channel_state = state.channel_state(parsed.channel)
        self._output.write("MIDI_PERFORMANCE_STATUS=PASS\n")
        self._output.write(
            f"CHANNEL={channel_state.channel};"
            f"PITCH_BEND_RAW={channel_state.pitch_bend_value};"
            f"PITCH_BEND_SEMITONES={channel_state.pitch_bend_semitones:.6f};"
            f"CC1_NORMALIZED={channel_state.modulation:.6f}\n"
        )
        return 0

    def _diagnose_d1(self, parsed):
        audio_format = AudioStreamFormat(
            sample_rate=parsed.sample_rate,
            channel_count=1,
            sample_width_bits=16,
            frames_per_block=parsed.frames_per_block,
        )
        frequency_hz = None
        for waveform in ("sine", "saw", "square"):
            core = D1SynthCore(D1Patch(waveform=waveform, audio_format=audio_format))
            core.start()
            core.handle_event(NoteEvent.note_on(1, parsed.note, parsed.velocity))
            block = core.render_audio_block()
            frequency_hz = core.active_frequency_hz
            self._output.write(
                f"D1_WAVEFORM={waveform};frames={block.frame_count};"
                f"minimum={min(block.samples)};maximum={max(block.samples)};"
                f"unique_samples={len(set(block.samples))}\n"
            )
            core.handle_event(NoteEvent.note_off(1, parsed.note))
            silence = core.render_audio_block()
            if any(silence.samples):
                self._output.write("D1_CORE_STATUS=FAIL;reason=note-off-not-silent\n")
                return 1
            core.stop()
        self._output.write(
            f"D1_CORE_STATUS=PASS;note={parsed.note};frequency_hz={frequency_hz:.6f};"
            f"velocity={parsed.velocity};sample_rate={audio_format.sample_rate};"
            f"waveforms=sine,saw,square\n"
        )
        return 0
