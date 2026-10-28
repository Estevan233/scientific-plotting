#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Working Example 1: Publication-Ready Experimental Curves with Error Bands.
Target: Elsevier / IEEE Single-Column (85mm / 3.35 in).
Features: Tol-muted color scheme, shaded error bounds, 1:1 physical canvas.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Ensure figure_config is reachable
sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from figure_config import (
    set_journal_profile,
    get_canvas_size,
    TOL_MUTED_LIST,
    save_publication_figure,
)

def main() -> None:
    # 1. 注入顶级期刊风格（Elsevier 单栏，无衬线 Arial）
    set_journal_profile(journal="elsevier", font_style="sans-serif", base_fontsize=9.0)

    # 2. 1:1 画布尺寸：单栏 85 mm，高宽比 0.75
    figsize = get_canvas_size(journal="elsevier", columns=1, aspect_ratio=0.72)
    fig, ax = plt.subplots(figsize=figsize)

    # 3. 模拟数据（如训练损失、收敛趋势）
    epochs = np.linspace(1, 100, 30)
    methods = [
        ("Baseline A", 0.45 * np.exp(-epochs / 25) + 0.12, 0.035, TOL_MUTED_LIST[0], "s", "-"),
        ("Baseline B", 0.52 * np.exp(-epochs / 18) + 0.08, 0.025, TOL_MUTED_LIST[1], "^", "--"),
        ("Ours (Proposed)", 0.60 * np.exp(-epochs / 12) + 0.03, 0.015, "#117733", "o", "-"),
    ]

    # 4. 绘制曲线与置信区间
    for name, mean_curve, std_val, color, marker, ls in methods:
        is_ours = "Ours" in name
        lw = 1.4 if is_ours else 1.1
        ms = 4.0 if is_ours else 3.2

        ax.plot(
            epochs, mean_curve,
            label=name, color=color, linestyle=ls, linewidth=lw,
            marker=marker, markersize=ms, markevery=3,
        )
        # 阴影半透明误差带
        ax.fill_between(
            epochs,
            mean_curve - std_val,
            mean_curve + std_val,
            color=color,
            alpha=0.18 if is_ours else 0.12,
            edgecolor="none",
        )

    # 5. 精细化轴线与标签
    ax.set_xlabel("Training Epochs")
    ax.set_ylabel(r"Objective Loss ($\mathcal{L}_{\mathrm{total}}$)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0.0, 0.65)

    # 网格线：极淡点状
    ax.grid(True, linestyle=":", color="#CBD5E1", linewidth=0.5, alpha=0.8)

    # 图例配置：紧凑半透明
    ax.legend(loc="upper right", framealpha=0.88, edgecolor="none", handlelength=1.6)

    # 6. 一键保存矢量 PDF 与 600 DPI PNG
    out_dir = Path(__file__).resolve().parent / "outputs"
    save_publication_figure(fig, out_dir / "fig_curve_errorbar", formats=("pdf", "png"), dpi=600, close=True)

if __name__ == "__main__":
    main()

