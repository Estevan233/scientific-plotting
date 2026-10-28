# CLAUDE.md — Guidelines for Claude Code

This repository provides **scientific-plotting**, a publication-grade scientific visualization engine and AI assistant skill for top-tier academic journals (Elsevier, IEEE, Nature, Springer, ACM, and Chinese Core/EI).

## Commands
- **Run Smoke Tests**: `python tests/test_examples.py`
- **Install Package in Editable Mode**: `pip install -e .`
- **Run Single Example**:
  - `python examples/example_curve_and_errorbar.py`
  - `python examples/example_grouped_bar_and_radar.py`
  - `python examples/example_multipanel_comparison.py`
  - `python examples/example_chinese_bilingual.py`

## Architecture & Code Structure
- `scientific_plotting/`: The core Python package. Contains `figure_config.py` with rcParams setup, color palettes, 1:1 canvas calculator, and helper decorators.
- `scripts/figure_config.py`: Mirror script entry point for Agent Skill execution without package installation.
- `examples/`: Minimal working examples (MWE) covering curves, bar/radar, qualitative image grids with ROI zoom, bilingual charts, and TikZ.
- `references/`: Detailed specifications for journal dimensions and color accessibility.

## Code Style & Conventions
- **Physical 1:1 Sizing**: Always use `get_canvas_size(journal, columns, aspect_ratio)` instead of hardcoded oversized figsize.
- **Font Standards**: Arial or Times New Roman (Latin), SimSun or SimHei (CJK). Always set `pdf.fonttype = 42`.
- **Palette**: Use `TOL_MUTED_LIST` or `OKABE_ITO_LIST`. Never use bright primary red (`#FF0000`) except for ROI zoom boxes and threshold cutoff indicators.
- **Python**: PEP 8, typed annotations, Python 3.8+ compatible.
