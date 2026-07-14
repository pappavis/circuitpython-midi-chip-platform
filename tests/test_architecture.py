# Bestand: test_architecture.py
# Versienommer: 0.2.0
# Doel: Dwing klasgebaseerde importveiligheid en volledige kodeheaders af.
# Sprint: Sprint 1
# Epic: MCP-EPIC-001 Platform Foundation
# User-Story: AUDIO-PRIORITY-AMENDMENT-001
# Actienr: MCP-ACT-AUDIO-AMEND-GREEN-003
# ChatID: CHATOD-20260714-MCP-CP-MVP-001 / AUDIO-PRIORITY-AMENDMENT-001

import ast
import subprocess
import sys
from pathlib import Path


class TestArchitectureRules:
    def test_source_modules_have_no_module_level_state_or_functions(self) -> None:
        source_root = Path(__file__).parents[1] / "src" / "midi_chip_platform"
        forbidden_nodes = (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.FunctionDef, ast.AsyncFunctionDef)

        for source_path in source_root.rglob("*.py"):
            syntax_tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            violations = [type(node).__name__ for node in syntax_tree.body if isinstance(node, forbidden_nodes)]
            assert violations == [], f"{source_path}: forbidden module-level nodes {violations}"

    def test_source_modules_never_use_global_statement(self) -> None:
        source_root = Path(__file__).parents[1] / "src" / "midi_chip_platform"

        for source_path in source_root.rglob("*.py"):
            syntax_tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            violations = [node.lineno for node in ast.walk(syntax_tree) if isinstance(node, ast.Global)]
            assert violations == [], f"{source_path}: global statements at lines {violations}"

    def test_host_skeleton_has_no_circuitpython_hardware_imports(self) -> None:
        source_root = Path(__file__).parents[1] / "src" / "midi_chip_platform"
        hardware_modules = {"audiobusio", "audiopwmio", "board", "pwmio", "synthio", "usb_midi", "wifi"}

        for source_path in source_root.rglob("*.py"):
            syntax_tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
            imported_names = set()
            for node in ast.walk(syntax_tree):
                if isinstance(node, ast.Import):
                    imported_names.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_names.add(node.module.split(".")[0])
            assert imported_names.isdisjoint(hardware_modules), f"{source_path}: hardware import in host skeleton"

    def test_package_import_has_no_output_or_runtime_startup(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "import midi_chip_platform"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""

    def test_python_files_contain_required_traceability_header(self) -> None:
        repository_root = Path(__file__).parents[1]
        source_paths = list((repository_root / "src").rglob("*.py")) + list((repository_root / "tests").rglob("*.py"))

        for source_path in source_paths:
            content = source_path.read_text(encoding="utf-8")
            for required_label in (
                "# Bestand:",
                "# Versienommer:",
                "# Doel:",
                "# Sprint:",
                "# Epic:",
                "# User-Story:",
                "# Actienr:",
                "# ChatID:",
            ):
                assert required_label in content, f"{source_path}: missing {required_label}"

            for required_value_label in ("Versienommer", "User-Story", "Actienr", "ChatID"):
                matching_lines = [
                    line for line in content.splitlines() if line.startswith(f"# {required_value_label}:")
                ]
                assert len(matching_lines) == 1, f"{source_path}: invalid {required_value_label} count"
                assert matching_lines[0].split(":", 1)[1].strip(), (
                    f"{source_path}: empty {required_value_label}"
                )
