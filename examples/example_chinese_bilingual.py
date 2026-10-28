#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Working Example 4: Chinese Core / EI Journal Bilingual Figure (中文核心与EI期刊双语图表).
Target: 《计算机学报》《自动化学报》《电子学报》《机械工程学报》等中文顶级期刊.
Features:
- Single-column 80 mm (半栏) 1:1 physical canvas.
- Chinese font (SimSun/SimHei) + English/Numbers (Arial/Times).
- Grayscale printability: distinct line styles + markers + hatching.
- Negative sign support (unicode_minus=False).
- Bilingual caption template.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from figure_config import (
    set_journal_profile,
    get_canvas_size,
    CHINESE_JOURNAL_LIST,
    save_publication_figure,
)

def main() -> None:
    # 1. 激活中文期刊模式（自动探测宋体/黑体，配置无衬线/衬线组合与负号防乱码）
    set_journal_profile(journal="chinese_core", font_style="sans-serif", is_chinese=True, base_fontsize=9.0)

    # 2. 中文半栏（单栏）标准 80 mm，高宽比 0.72
    figsize = get_canvas_size(journal="chinese_core", columns=1, aspect_ratio=0.72)
    fig, ax = plt.subplots(figsize=figsize)

    # 3. 模拟数据（如应变-应力关系或算法信噪比曲线）
    x = np.linspace(-10, 50, 25)
    y1 = 80 / (1 + np.exp(-0.1 * (x - 15))) + 5
    y2 = 72 / (1 + np.exp(-0.08 * (x - 20))) + 3
    y3 = 90 / (1 + np.exp(-0.12 * (x - 10))) + 8

    # 4. 黑白印刷兼容：不仅依靠色彩，必须配备不同线型与标记符号
    ax.plot(
        x, y1,
        label="传统阈值法 (Otsu)",
        color=CHINESE_JOURNAL_LIST[0],
        linestyle="-",
        linewidth=1.2,
        marker="o",
        markersize=3.5,
        markevery=2,
    )
    ax.plot(
        x, y2,
        label="聚类算法 (FCM)",
        color=CHINESE_JOURNAL_LIST[1],
        linestyle="--",
        linewidth=1.2,
        marker="s",
        markersize=3.5,
        markevery=2,
    )
    ax.plot(
        x, y3,
        label="本文方法 (Ours)",
        color=CHINESE_JOURNAL_LIST[3],
        linestyle="-.",
        linewidth=1.5,
        marker="^",
        markersize=4.0,
        markevery=2,
    )

    # 5. 中英文双语坐标轴标签
    ax.set_xlabel("信噪比 / Signal-to-Noise Ratio (dB)")
    ax.set_ylabel("识别准确率 / Accuracy (%)")
    ax.set_xlim(-10, 50)
    ax.set_ylim(0, 105)

    # 辅助网格：淡虚线
    ax.grid(True, linestyle=":", color="#D1D5DB", linewidth=0.5, alpha=0.8)

    # 图例配置：无边框或浅白底
    ax.legend(loc="lower right", framealpha=0.90, edgecolor="none", handlelength=2.0)

    # 6. 保存输出
    out_dir = Path(__file__).resolve().parent / "outputs"
    save_publication_figure(fig, out_dir / "fig_chinese_bilingual", formats=("pdf", "png"), dpi=600, close=True)

    print("\n[论文排版建议图题/图注]:")
    print("图1 不同信噪比下算法识别准确率对比")
    print("Fig. 1 Comparison of recognition accuracy under different signal-to-noise ratios")

if __name__ == "__main__":
    main()

