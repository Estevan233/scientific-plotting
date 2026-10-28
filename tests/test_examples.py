#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke test suite for scientific-plotting.
Verifies that all minimal working examples execute without error and generate valid PDFs and PNGs.
"""

import os
import subprocess
import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
OUTPUTS_DIR = EXAMPLES_DIR / "outputs"


class TestScientificPlottingExamples(unittest.TestCase):

    def setUp(self) -> None:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    def _run_script(self, script_name: str) -> None:
        script_path = EXAMPLES_DIR / script_name
        self.assertTrue(script_path.exists(), f"Script {script_name} does not exist.")

        env = os.environ.copy()
        # Add repo root to PYTHONPATH so package import works
        env["PYTHONPATH"] = str(REPO_ROOT)

        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            env=env,
        )
        if proc.returncode != 0:
            print(f"\n--- STDERR for {script_name} ---")
            print(proc.stderr)
            print(f"--- STDOUT for {script_name} ---")
            print(proc.stdout)
        self.assertEqual(proc.returncode, 0, f"{script_name} exited with code {proc.returncode}")

    def test_01_curve_and_errorbar(self) -> None:
        self._run_script("example_curve_and_errorbar.py")
        pdf = OUTPUTS_DIR / "fig_curve_errorbar.pdf"
        png = OUTPUTS_DIR / "fig_curve_errorbar.png"
        self.assertTrue(pdf.exists() and pdf.stat().st_size > 1000)
        self.assertTrue(png.exists() and png.stat().st_size > 1000)

    def test_02_grouped_bar_and_radar(self) -> None:
        self._run_script("example_grouped_bar_and_radar.py")
        pdf = OUTPUTS_DIR / "fig_grouped_bar_radar.pdf"
        png = OUTPUTS_DIR / "fig_grouped_bar_radar.png"
        self.assertTrue(pdf.exists() and pdf.stat().st_size > 1000)
        self.assertTrue(png.exists() and png.stat().st_size > 1000)

    def test_03_multipanel_comparison(self) -> None:
        self._run_script("example_multipanel_comparison.py")
        pdf = OUTPUTS_DIR / "fig_multipanel_comparison.pdf"
        png = OUTPUTS_DIR / "fig_multipanel_comparison.png"
        self.assertTrue(pdf.exists() and pdf.stat().st_size > 1000)
        self.assertTrue(png.exists() and png.stat().st_size > 1000)

    def test_04_chinese_bilingual(self) -> None:
        self._run_script("example_chinese_bilingual.py")
        pdf = OUTPUTS_DIR / "fig_chinese_bilingual.pdf"
        png = OUTPUTS_DIR / "fig_chinese_bilingual.png"
        self.assertTrue(pdf.exists() and pdf.stat().st_size > 1000)
        self.assertTrue(png.exists() and png.stat().st_size > 1000)


if __name__ == "__main__":
    unittest.main()

