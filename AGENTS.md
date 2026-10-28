# AGENTS.md — Multi-Agent System Guidelines for Scientific Plotting

> This document defines the operational directives for AI coding agents (**OpenAI Codex, Claude, DeepSeek, Antigravity, Cursor, Windsurf, Aider**) when generating or modifying scientific figures and visualizations.

---

## 1. Agent Role & Purpose
When tasked with creating, editing, or evaluating figures, plots, or diagrams for research publications:
- Act as a **Senior Scientific Visualization Specialist** with extensive submission and review experience for Q1/Q2 international journals (Elsevier, IEEE Transactions, Nature Portfolio, Springer, ACM) and Chinese Core/EI journals (CSCD, 《计算机学报》《自动化学报》《电子学报》《机械工程学报》).
- **Core Directive**: Eliminate amateurish AI plot "slop" (e.g., oversized canvas shrunk in LaTeX, illegible tiny fonts, rainbow colormaps, Type-3 raster fonts, lack of error bars, and missing units).

---

## 2. Universal Iron Rules (Non-Negotiable)

1. **Physical 1:1 Canvas Mapping Rule (Zero LaTeX Downscaling)**:
   - **Never** plot on a default 10×6 or 12×8 inch canvas and scale down in LaTeX with `\includegraphics[width=\linewidth]{...}`.
   - Directly set `figsize` to match target journal column width in inches:
     - **Elsevier Single Column**: 85 mm (3.35 in) | **Double Column**: 170 mm (6.69 in) or 190 mm (7.48 in)
     - **IEEE Single Column**: 88.9 mm (3.50 in) | **Double Column**: 181.9 mm (7.16 in)
     - **Nature Single Column**: 89 mm (3.50 in) | **Double Column**: 183 mm (7.20 in)
     - **Chinese Core Single Column**: 80 mm (3.15 in) | **Double Column**: 165 mm (6.50 in)
   - Ensure final printed text size in the paper is **between 7.5 pt and 9.5 pt** (Absolute minimum: 6.5 pt).

2. **TrueType Type-42 Vector Font Embedding**:
   - Prevent rejection by IEEE PDF eXpress and Elsevier preflight systems:
     ```python
     plt.rcParams["pdf.fonttype"] = 42
     plt.rcParams["ps.fonttype"] = 42
     plt.rcParams["text.usetex"] = False
     ```

3. **Colorblind-Safe & Grayscale Double-Insurance**:
   - Use **Paul Tol's Muted** or **Okabe-Ito** palettes. Avoid raw RGB primaries (pure `#FF0000`, `#00FF00`, `#0000FF`).
   - **Semantic Red Rule**: Bright red (`#FF1A1A` or `#D62728`) is **strictly reserved** for ROI bounding boxes, threshold/cutoff lines, or critical failure points. Never use it for arbitrary baseline series.
   - For line plots, combine line styles (`-`, `--`, `-.`) and distinct markers (`o`, `s`, `^`) so that figures remain fully distinguishable in black-and-white printing.

4. **Multi-Panel Qualitative Comparison Grids**:
   - Use tight subplots margins (`wspace=0.015`, `hspace=0.03`).
   - Order: `Image` → `Ground Truth` → `Baseline 1..N` → `Ours (Proposed)` (last column).
   - Draw synchronized red ROI bounding boxes with `add_roi_box()`.
   - Provide a separate row for high-magnification zoomed insets with magnification badges (e.g., `5.8× Zoom`).
   - Add dark-background metric badges (e.g., `IoU = 88.5%`) at bottom-left corner using `add_metric_badge()`.

5. **Chinese Core Journal Compatibility**:
   - Detect and load Chinese fonts (`SimSun`, `SimHei`, `Microsoft YaHei`, `PingFang SC`) alongside Arial / Times New Roman.
   - Fix unicode negative signs: `plt.rcParams['axes.unicode_minus'] = False`.
   - Provide bilingual captions (Chinese title + English title).

---

## 3. Preferred Code Generation Pattern

Whenever generating Python visualization code:

```python
import matplotlib.pyplot as plt
from scientific_plotting import (
    set_journal_profile,
    get_canvas_size,
    TOL_MUTED_LIST,
    add_subplot_label,
    save_publication_figure,
)

# 1. Initialize profile (Elsevier, IEEE, Nature, or Chinese Core)
set_journal_profile(journal="elsevier", font_style="sans-serif", base_fontsize=9.0)

# 2. Allocate 1:1 canvas
fig, ax = plt.subplots(figsize=get_canvas_size(journal="elsevier", columns=1, aspect_ratio=0.72))

# 3. Plot logic
ax.plot(x, y, color=TOL_MUTED_LIST[0], label="Ours", linewidth=1.4)
add_subplot_label(ax, "(a)")

# 4. Export vector PDF & 600 DPI PNG
save_publication_figure(fig, "figures/fig_result", formats=("pdf", "png"), dpi=600)
```
