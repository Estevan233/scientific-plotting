#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Working Example 2: Grouped Bar Chart & Multi-Metric Polar Radar Chart.
Target: Elsevier / IEEE Double-Column (170mm / 6.70 in).
Features: Side-by-side (1x2) layout, Tol-muted palette, clean value labels.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from figure_config import (
    set_journal_profile,
    get_canvas_size,
    TOL_MUTED_LIST,
    add_subplot_label,
    save_publication_figure,
)

def main() -> None:
    set_journal_profile(journal="elsevier", font_style="sans-serif", base_fontsize=8.5)

    # 双栏全宽 170 mm，高宽比 0.44
    figsize = get_canvas_size(journal="elsevier", columns=2, aspect_ratio=0.42)
    fig = plt.figure(figsize=figsize)

    # 左右两个子图 (1行2列)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection="polar")

    # ── 左图：分组柱状图 ──────────────────────────────────
    metrics = ["Precision", "Recall", "F1-Score", "mIoU"]
    methods = ["Frangi", "PCEFCM", "CT-CrackSeg", "Ours"]
    scores = np.array([
        [0.72, 0.65, 0.68, 0.52],
        [0.76, 0.71, 0.73, 0.58],
        [0.85, 0.81, 0.83, 0.71],
        [0.89, 0.87, 0.88, 0.79],
    ])

    x = np.arange(len(metrics))
    n_methods = len(methods)
    bar_w = 0.18
    offsets = (np.arange(n_methods) - (n_methods - 1) / 2) * bar_w

    colors = [TOL_MUTED_LIST[0], TOL_MUTED_LIST[1], TOL_MUTED_LIST[4], "#117733"]

    for i, (m_name, c) in enumerate(zip(methods, colors)):
        is_ours = m_name == "Ours"
        edge_c = "black" if is_ours else "white"
        lw = 0.8 if is_ours else 0.5
        ax1.bar(
            x + offsets[i], scores[i],
            width=bar_w, label=m_name, color=c,
            edgecolor=edge_c, linewidth=lw, alpha=0.92,
        )

    ax1.set_ylabel("Metric Score")
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics)
    ax1.set_ylim(0.40, 1.0)
    ax1.grid(axis="y", linestyle=":", color="#CBD5E1", linewidth=0.5, alpha=0.8)
    ax1.legend(loc="upper left", framealpha=0.85, edgecolor="none", handlelength=1.4)
    add_subplot_label(ax1, "(a)", loc="upper left", pad=0.03)

    # ── 右图：雷达图 ──────────────────────────────────────
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    radar_methods = [("CT-CrackSeg", scores[2], TOL_MUTED_LIST[4]), ("Ours", scores[3], "#117733")]

    for m_name, vals, c in radar_methods:
        val_closed = np.concatenate([vals, vals[:1]])
        is_ours = m_name == "Ours"
        lw = 1.6 if is_ours else 1.2
        alpha_fill = 0.28 if is_ours else 0.15
        ax2.plot(angles, val_closed, color=c, linewidth=lw, label=m_name)
        ax2.fill(angles, val_closed, color=c, alpha=alpha_fill)

    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(metrics, fontsize=8.0)
    ax2.tick_params(axis="x", pad=6)
    ax2.set_ylim(0.4, 1.0)
    ax2.set_yticks([0.5, 0.7, 0.9])
    ax2.set_yticklabels(["0.5", "0.7", "0.9"], fontsize=7.0, color="#64748B")
    ax2.grid(color="#CBD5E1", linestyle="--", linewidth=0.5)
    ax2.legend(loc="lower right", bbox_to_anchor=(1.12, -0.05), framealpha=0.85, edgecolor="none")
    add_subplot_label(ax2, "(b)", loc="upper left", pad=0.02)

    plt.subplots_adjust(wspace=0.28, left=0.06, right=0.96, top=0.92, bottom=0.12)

    out_dir = Path(__file__).resolve().parent / "outputs"
    save_publication_figure(fig, out_dir / "fig_grouped_bar_radar", formats=("pdf", "png"), dpi=600, close=True)

if __name__ == "__main__":
    main()

