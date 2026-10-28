#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Working Example 3: Multi-Panel Qualitative Comparison Matrix with ROI Zoom & Metric Badges.
Target: Elsevier / IEEE Double-Column (170mm / 6.70 in).
Features:
- Standard 6-panel row: [Image, Ground Truth, Frangi, PCEFCM, DeepLearning, Ours]
- Synchronized red ROI bounding boxes.
- High-magnification detail inset row.
- Non-occluding high-contrast metric badges (e.g., IoU = 88.5%).
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from figure_config import (
    set_journal_profile,
    get_canvas_size,
    add_roi_box,
    add_metric_badge,
    save_publication_figure,
)

def synthesize_mock_patch(crack_intensity: float = 0.8, noise_level: float = 0.15) -> np.ndarray:
    """Generate synthetic crack texture array for demonstration."""
    h, w = 120, 120
    img = np.ones((h, w), dtype=np.float32) * 0.75
    # Add texture noise
    img += np.random.normal(0, noise_level, (h, w))
    # Draw curved crack line
    y_coords = np.arange(h)
    x_center = (w // 2 + 15 * np.sin(y_coords / 15.0)).astype(int)
    for y, x in zip(y_coords, x_center):
        for dx in range(-1, 2):
            if 0 <= x + dx < w:
                img[y, x + dx] -= crack_intensity * (1.0 - abs(dx) * 0.4)
    return np.clip(img, 0.0, 1.0)

def main() -> None:
    set_journal_profile(journal="elsevier", font_style="sans-serif", base_fontsize=8.0)

    # 170 mm width, 2 rows (Row 1: Overview with ROI box; Row 2: 3x Detail Inset Zoom)
    figsize = get_canvas_size(journal="elsevier", columns=2, aspect_ratio=0.38)
    fig, axes = plt.subplots(2, 6, figsize=figsize)

    headers = ["Image", "Ground Truth", "Frangi", "PCEFCM", "CT-CrackSeg", "Ours"]
    ious = [None, None, 58.4, 71.2, 81.6, 89.2]

    # Mock ROI coordinates
    roi_box = (35, 40, 45, 45)  # (x, y, w, h)
    bx, by, bw, bh = roi_box

    np.random.seed(42)
    base_img = synthesize_mock_patch(crack_intensity=0.8, noise_level=0.10)
    gt_mask = np.zeros_like(base_img)
    gt_mask[base_img < 0.45] = 1.0

    # Predictions
    pred_frangi = gt_mask * (np.random.rand(*gt_mask.shape) > 0.35)
    pred_pcefcm = gt_mask * (np.random.rand(*gt_mask.shape) > 0.20)
    pred_dl = gt_mask * (np.random.rand(*gt_mask.shape) > 0.10)
    pred_ours = gt_mask.copy()

    panels_row1 = [base_img, gt_mask, pred_frangi, pred_pcefcm, pred_dl, pred_ours]

    for c in range(6):
        ax1 = axes[0, c]
        ax2 = axes[1, c]

        # ── Row 1: Global View ──────────────────────────────
        p1 = panels_row1[c]
        if c == 0:
            ax1.imshow(p1, cmap="gray", vmin=0, vmax=1, interpolation="bilinear")
        else:
            ax1.imshow(p1, cmap="gray", vmin=0, vmax=1, interpolation="nearest")

        # Column Title
        is_ours = (headers[c] == "Ours")
        title_color = "#0B5394" if is_ours else "#1F2937"
        ax1.set_title(headers[c], fontsize=8.0, fontweight="bold", color=title_color, pad=3)

        # ROI Red box on all panels
        add_roi_box(ax1, roi_box, color="#FF1A1A", linewidth=1.0)

        # Quantitative badge on methods
        if ious[c] is not None:
            add_metric_badge(ax1, f"{ious[c]:.1f}%", is_ours=is_ours, loc="lower left", fontsize=6.8)

        # ── Row 2: Zoomed Inset ─────────────────────────────
        p2 = p1[by:by+bh, bx:bx+bw]
        if c == 0:
            ax2.imshow(p2, cmap="gray", vmin=0, vmax=1, interpolation="bilinear")
            ax2.text(0.04, 0.82, "3.0× Zoom", transform=ax2.transAxes, color="white",
                     fontsize=6.5, fontweight="bold",
                     bbox=dict(boxstyle="square,pad=0.10", facecolor="#DC2626", edgecolor="none"))
        else:
            ax2.imshow(p2, cmap="gray", vmin=0, vmax=1, interpolation="nearest")

        # Inset Red Border
        for spine in ax2.spines.values():
            spine.set_color("#DC2626")
            spine.set_linewidth(0.8)

        # Clear ticks
        for ax in (ax1, ax2):
            ax.set_xticks([])
            ax.set_yticks([])
            if ax is ax1:
                for spine in ax.spines.values():
                    spine.set_color("#D2D6DC")
                    spine.set_linewidth(0.5)

    # Row markers on left margin
    axes[0, 0].text(-0.16, 0.5, "(a)", transform=axes[0, 0].transAxes, fontsize=9.0, fontweight="bold", va="center", ha="right")
    axes[1, 0].text(-0.16, 0.5, "(b)", transform=axes[1, 0].transAxes, fontsize=9.0, fontweight="bold", va="center", ha="right")

    plt.subplots_adjust(left=0.035, right=0.995, top=0.91, bottom=0.04, wspace=0.02, hspace=0.06)

    out_dir = Path(__file__).resolve().parent / "outputs"
    save_publication_figure(fig, out_dir / "fig_multipanel_comparison", formats=("pdf", "png"), dpi=600, close=True)

if __name__ == "__main__":
    main()

