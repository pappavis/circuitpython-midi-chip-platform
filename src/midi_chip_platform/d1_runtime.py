# Bestand: d1_runtime.py
# Versienommer: 0.17.1
# Doel: Verbind USB-MIDI, D1-kern en veilige I2S-uitvoer vir die Logic MVP.
# Sprint: Sprint 3
# Epic: MCP-EPIC-008 Portability, Quality And Release
# User-Story: MCP-US-055 macOS Logic Pro Audible D1 Acceptance
# Actienr: MCP-ACT-055-IMP-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / US-055-IMPEDIMENT-001

from midi_chip_platform.audio import AudioSafetyProfile, AudioStreamFormat, SafeAudioOutput
from midi_chip_platform.d1_core import D1Patch, D1SynthCore
from midi_chip_platform.events import NoteEvent
from midi_chip_platform.i2s_audio import CircuitPythonI2sAudioOutput
from midi_chip_platform.midi_usb import CircuitPythonUsbMidiFactory
from midi_chip_platform.ports import AudioOutputPort, ConfigurationPort, MidiInputPort


class D1UsbMidiI2sRuntime:
    def __init__(
        self,
        midi_input,
        audio_output,
        core,
        output=None,
        sleeper=None,
        max_blocks=0,
        idle_sleep_seconds=0.001,
        minimum_note_seconds=0.12,
    ):
        if not isinstance(midi_input, MidiInputPort):
            raise TypeError("midi_input must implement MidiInputPort")
        if not isinstance(audio_output, AudioOutputPort):
            raise TypeError("audio_output must implement AudioOutputPort")
        if not isinstance(core, D1SynthCore):
            raise TypeError("core must be D1SynthCore")
        self._midi_input = midi_input
        self._audio_output = audio_output
        self._core = core
        self._output = output if output is not None else print
        self._sleeper = sleeper
        self._max_blocks = int(max_blocks)
        self._idle_sleep_seconds = float(idle_sleep_seconds)
        self._minimum_note_seconds = float(minimum_note_seconds)
        self._block_count = 0
        self._note_event_count = 0
        self._audible_note_count = 0

    @property
    def block_count(self):
        return self._block_count

    @property
    def note_event_count(self):
        return self._note_event_count

    @property
    def audible_note_count(self):
        return self._audible_note_count

    def run(self):
        self._output(
            "D1_RUNTIME_STATUS=START;"
            f"core={self._core.name};sample_rate={self._audio_output.audio_format.sample_rate};"
            f"frames_per_block={self._audio_output.audio_format.frames_per_block};"
            f"max_blocks={self._max_blocks};minimum_note_seconds={self._minimum_note_seconds}"
        )
        try:
            self._midi_input.open()
            self._audio_output.open()
            self._core.start()
            self._audio_output.unmute()
            while self._should_continue():
                event = self._midi_input.receive()
                if isinstance(event, NoteEvent):
                    self._core.handle_event(event)
                    self._note_event_count += 1
                    self._output(
                        f"D1_MIDI_EVENT={event.message_type};channel={event.channel};"
                        f"note={event.note};velocity={event.velocity}"
                    )
                    if event.is_note_on and event.velocity > 0:
                        self._write_minimum_audible_note(event)
                        if self._max_blocks > 0 and self._block_count >= self._max_blocks:
                            continue
                        continue
                self._write_single_runtime_block()
                if event is None and self._sleeper is not None:
                    self._sleeper.sleep(self._idle_sleep_seconds)
        except KeyboardInterrupt:
            self._output(
                "D1_RUNTIME_STATUS=INTERRUPTED;"
                f"blocks={self._block_count};note_events={self._note_event_count};"
                f"audible_notes={self._audible_note_count}"
            )
            return True
        except Exception as error:
            self._output(
                "D1_RUNTIME_STATUS=FAIL;"
                f"reason={error.__class__.__name__};blocks={self._block_count};"
                f"note_events={self._note_event_count};audible_notes={self._audible_note_count}"
            )
            return False
        finally:
            self._shutdown()
        self._output(
            "D1_RUNTIME_STATUS=PASS;"
            f"blocks={self._block_count};note_events={self._note_event_count};"
            f"audible_notes={self._audible_note_count}"
        )
        return True

    def _should_continue(self):
        return self._max_blocks <= 0 or self._block_count < self._max_blocks

    def _shutdown(self):
        try:
            self._audio_output.mute()
        except Exception:
            pass
        try:
            self._core.stop()
        except Exception:
            pass
        try:
            self._audio_output.close()
        except Exception:
            pass
        try:
            self._midi_input.close()
        except Exception:
            pass

    def _write_single_runtime_block(self):
        block = self._core.render_audio_block()
        self._audio_output.write_block(block)
        self._block_count += 1

    def _write_minimum_audible_note(self, event):
        requested_blocks = self._minimum_audible_block_count()
        if self._max_blocks > 0:
            remaining_blocks = self._max_blocks - self._block_count
            requested_blocks = max(0, min(requested_blocks, remaining_blocks))
        if requested_blocks <= 0:
            return
        for _ in range(requested_blocks):
            self._write_single_runtime_block()
        self._audible_note_count += 1
        self._output(
            "D1_AUDIO_EVENT=audible_note;"
            f"note={event.note};blocks={requested_blocks};"
            f"seconds={self._seconds_for_blocks(requested_blocks):.3f}"
        )

    def _minimum_audible_block_count(self):
        if self._minimum_note_seconds <= 0.0:
            return 1
        audio_format = self._audio_output.audio_format
        requested_frames = int(
            self._minimum_note_seconds * audio_format.sample_rate
        )
        if requested_frames <= 0:
            return 1
        return max(
            1,
            (requested_frames + audio_format.frames_per_block - 1)
            // audio_format.frames_per_block,
        )

    def _seconds_for_blocks(self, block_count):
        audio_format = self._audio_output.audio_format
        return (
            int(block_count)
            * audio_format.frames_per_block
            / audio_format.sample_rate
        )


class D1UsbMidiI2sRuntimeFactory:
    def __init__(self, importer=None, output=None):
        self._importer = importer if importer is not None else __import__
        self._output = output if output is not None else print

    def create_if_enabled(self, configuration):
        if not isinstance(configuration, ConfigurationPort):
            raise TypeError("configuration must implement ConfigurationPort")
        if not configuration.get("synth.d1.enabled", True):
            return None
        audio_format = AudioStreamFormat(
            sample_rate=configuration.get("synth.d1.sample_rate", 16000),
            channel_count=1,
            sample_width_bits=16,
            frames_per_block=configuration.get("synth.d1.frames_per_block", 128),
        )
        i2s_output = CircuitPythonI2sAudioOutput(
            audio_format=audio_format,
            importer=self._importer,
            bit_clock_pin_name=configuration.get("audio.i2s.bit_clock", "IO5"),
            word_select_pin_name=configuration.get("audio.i2s.word_select", "IO3"),
            data_pin_name=configuration.get("audio.i2s.data", "IO7"),
        )
        safe_output = SafeAudioOutput(
            i2s_output,
            AudioSafetyProfile(
                master_gain=configuration.get("audio.master_gain", 0.08),
                maximum_master_gain=configuration.get("audio.maximum_master_gain", 0.25),
                startup_muted=configuration.get("audio.startup_muted", True),
                amplifier_gain_db=configuration.get("audio.amplifier_gain_db", 9.0),
                gain_pin_profile=configuration.get("audio.gain_pin_profile", "floating-9db"),
                shutdown_mode=configuration.get("audio.shutdown_mode", "software-mute"),
                output_load=configuration.get("audio.output_load", "speaker-4-8-ohm"),
            ),
        )
        core = D1SynthCore(
            D1Patch(
                waveform=configuration.get("synth.d1.waveform", "sine"),
                audio_format=audio_format,
                amplitude=configuration.get("synth.d1.amplitude", 0.2),
            )
        )
        time_module = self._importer("time")
        return D1UsbMidiI2sRuntime(
            midi_input=CircuitPythonUsbMidiFactory(self._importer).create_input(
                port_index=configuration.get("midi.input.port_index", 0)
            ),
            audio_output=safe_output,
            core=core,
            output=self._output,
            sleeper=time_module,
            max_blocks=configuration.get("synth.d1.max_blocks", 0),
            idle_sleep_seconds=configuration.get("synth.d1.idle_sleep_seconds", 0.001),
            minimum_note_seconds=configuration.get("synth.d1.minimum_note_seconds", 0.12),
        )
