# Bestand: test_i2s_diagnostic.py
# Versienommer: 0.14.0
# Doel: Spesifiseer die onafhanklike G-C-D I2S/MAX98357 diagnostiek.
# Sprint: Sprint 3
# Epic: MCP-EPIC-003 Audio And Chip Core
# User-Story: MCP-US-016 Standalone I2S Audible Diagnostic
# Actienr: MCP-ACT-016-RED-001
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-016-START

import ast
import importlib.util
from pathlib import Path


class TestStandaloneI2sDiagnosticArchitecture:
    def test_diagnostic_exists_without_synth_import_or_module_state(self) -> None:
        path = Path(__file__).parents[1] / "device" / "i2s_test.py"

        assert path.is_file()
        syntax_tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        forbidden = (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.FunctionDef, ast.AsyncFunctionDef)
        violations = [type(node).__name__ for node in syntax_tree.body if isinstance(node, forbidden)]
        imports = []
        for node in ast.walk(syntax_tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)

        assert violations == []
        assert not any(name.startswith("midi_chip_platform") for name in imports)


class TestStandaloneI2sDiagnosticBehavior:
    class FakeRawSample:
        def __init__(self, buffer, sample_rate):
            self.buffer = buffer
            self.sample_rate = sample_rate

    class FakeAudioCore:
        def RawSample(self, buffer, sample_rate):
            return TestStandaloneI2sDiagnosticBehavior.FakeRawSample(buffer, sample_rate)

    class FakeArrayModule:
        def array(self, typecode, values):
            assert typecode == "H"
            return list(values)

    class FakeI2sOutput:
        def __init__(self, bit_clock, word_select, data):
            self.pins = (bit_clock, word_select, data)
            self.played = []
            self.stop_count = 0
            self.deinit_count = 0

        def play(self, sample, loop=False):
            self.played.append((sample, loop))

        def stop(self):
            self.stop_count += 1

        def deinit(self):
            self.deinit_count += 1

    class FakeAudioBusIo:
        def __init__(self):
            self.output = None

        def I2SOut(self, bit_clock, word_select, data):
            self.output = TestStandaloneI2sDiagnosticBehavior.FakeI2sOutput(
                bit_clock,
                word_select,
                data,
            )
            return self.output

    class FakeBoard:
        IO5 = "IO5"
        IO3 = "IO3"
        IO7 = "IO7"

    class FakeTime:
        def __init__(self):
            self.sleeps = []

        def sleep(self, seconds):
            self.sleeps.append(seconds)

    class FakeGc:
        def __init__(self):
            self.collect_count = 0

        def collect(self):
            self.collect_count += 1

        def mem_free(self):
            return 2000000 - self.collect_count

    class OutputRecorder:
        def __init__(self):
            self.lines = []

        def __call__(self, value):
            self.lines.append(str(value))

    class Importer:
        def __init__(self, modules):
            self.modules = dict(modules)

        def __call__(self, name):
            return self.modules[name]

    @classmethod
    def _load_module(cls):
        path = Path(__file__).parents[1] / "device" / "i2s_test.py"
        spec = importlib.util.spec_from_file_location("standalone_i2s_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_default_profile_matches_approved_wemos_wiring(self) -> None:
        module = self._load_module()
        profile = module.I2sDiagnosticProfile()

        assert profile.bit_clock_pin_name == "IO5"
        assert profile.word_select_pin_name == "IO3"
        assert profile.data_pin_name == "IO7"
        assert profile.notes == (("G3", 196.0), ("C4", 261.63), ("D4", 293.66))

    def test_square_wave_uses_safe_unsigned_sixteen_bit_levels(self) -> None:
        module = self._load_module()
        profile = module.I2sDiagnosticProfile(sample_rate=16000, amplitude=4096)
        factory = module.SquareWaveSampleFactory(
            self.FakeArrayModule(),
            self.FakeAudioCore(),
        )

        tone = factory.create(profile, frequency=200.0)

        assert len(tone.buffer) == 80
        assert set(tone.buffer) == {32768 - 4096, 32768 + 4096}
        assert tone.raw_sample.sample_rate == 16000

    def test_application_plays_g_c_d_and_releases_i2s(self) -> None:
        module = self._load_module()
        audio_bus = self.FakeAudioBusIo()
        time_module = self.FakeTime()
        gc_module = self.FakeGc()
        output = self.OutputRecorder()
        importer = self.Importer(
            {
                "array": self.FakeArrayModule(),
                "audiobusio": audio_bus,
                "audiocore": self.FakeAudioCore(),
                "board": self.FakeBoard(),
                "gc": gc_module,
                "time": time_module,
            }
        )
        application = module.I2sDiagnosticApplication(importer=importer, output=output)

        result = application.run()

        assert result is True
        assert audio_bus.output.pins == ("IO5", "IO3", "IO7")
        assert len(audio_bus.output.played) == 3
        assert all(loop is True for _, loop in audio_bus.output.played)
        assert audio_bus.output.stop_count >= 3
        assert audio_bus.output.deinit_count == 1
        assert any("I2S_DIAGNOSTIC_STATUS=PASS" in line for line in output.lines)
