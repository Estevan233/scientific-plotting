#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scientific Plotting Universal Configuration Engine — Top-Tier Journal Standard.
Supports Elsevier, IEEE, Nature, Springer, ACM, and Chinese Core/EI Journals.

Features:
- Physical 1:1 canvas mapping (80mm - 190mm) without LaTeX scaling distortion.
- Typography hierarchy with strict Arial / Times / SimSun cross-platform font fallback.
- TrueType Type-42 embedding (zero Type-3 raster warnings on IEEE / Elsevier eXpress).
- Colorblind-safe palettes: Tol-muted, Okabe-Ito, Nature, Chinese academic.
- Subplot labeling `(a)`, ROI bounding box, zoom inset, and quantitative badge helpers.
- Vector PDF + 600 DPI PNG + SVG unified exporter.
"""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Sequence, Mapping, Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np


# ══════════════════════════════════════════════════════════════
# 1. 物理尺寸标准对照 (mm 换算至 inches)
# ══════════════════════════════════════════════════════════════

JOURNAL_WIDTHS_MM: dict[str, dict[str, float]] = {
    "elsevier": {
        "single": 85.0,        # 3.35 in
        "1.5col": 120.0,       # 4.72 in
        "double": 170.0,       # 6.69 in (部分刊物支持 190mm / 7.48 in)
        "double_wide": 190.0,  # 7.48 in
    },
    "ieee": {
        "single": 88.9,        # 3.50 in (IEEE Standard 1-col)
        "double": 181.9,       # 7.16 in (IEEE Standard 2-col)
    },
    "nature": {
        "single": 89.0,        # 3.50 in
        "double": 183.0,       # 7.20 in
    },
    "springer": {
        "single": 84.0,        # 3.31 in
        "double": 174.0,       # 6.85 in
    },
    "chinese_core": {
        "single": 80.0,        # 3.15 in (计算机学报、自动化学报、机械工程学报等)
        "double": 165.0,       # 6.50 in
    },
}


def mm_to_inches(mm: float) -> float:
    """Millimeters to inches conversion."""
    return mm / 25.4


def get_canvas_size(
    journal: str = "elsevier",
    columns: int | str = 1,
    aspect_ratio: float = 0.72,
    custom_height: float | None = None,
) -> tuple[float, float]:
    """
    Get 1:1 physical canvas size (width, height) in inches.

    Parameters
    ----------
    journal : 'elsevier' | 'ieee' | 'nature' | 'springer' | 'chinese_core'
    columns : 1 (single), 2 (double), '1.5col', or 'double_wide'
    aspect_ratio : height / width ratio (used if custom_height is None)
    custom_height : explicit height in inches (optional)
    """
    j_key = journal.lower()
    if j_key not in JOURNAL_WIDTHS_MM:
        j_key = "elsevier"

    widths = JOURNAL_WIDTHS_MM[j_key]
    if columns == 1 or columns == "1" or columns == "single":
        w_mm = widths.get("single", 85.0)
    elif columns == 2 or columns == "2" or columns == "double":
        w_mm = widths.get("double", 170.0)
    elif columns in ("1.5", "1.5col"):
        w_mm = widths.get("1.5col", 120.0)
    elif columns in ("wide", "double_wide"):
        w_mm = widths.get("double_wide", 190.0)
    else:
        w_mm = widths.get("single", 85.0)

    w_in = mm_to_inches(w_mm)
    h_in = custom_height if custom_height is not None else w_in * aspect_ratio
    return (round(w_in, 3), round(h_in, 3))


# ══════════════════════════════════════════════════════════════
# 2. 顶级期刊与色盲安全调色板 (Color Palettes)
# ══════════════════════════════════════════════════════════════

# Paul Tol's muted scheme (色盲安全 + 灰度可明显区分，顶刊首选)
TOL_MUTED: dict[str, str] = {
    "indigo":  "#332288",
    "rose":    "#CC6677",
    "sand":    "#DDCC77",
    "green":   "#117733",
    "cyan":    "#88CCEE",
    "wine":    "#882255",
    "teal":    "#44AA99",
    "purple":  "#AA4499",
    "grey":    "#DDDDDD",
}

TOL_MUTED_LIST: list[str] = [
    "#332288",  # indigo
    "#CC6677",  # rose
    "#DDCC77",  # sand
    "#117733",  # green
    "#88CCEE",  # cyan
    "#882255",  # wine
    "#44AA99",  # teal
    "#AA4499",  # purple
]

# Okabe-Ito Palette (国际权威色盲友好规范)
OKABE_ITO_LIST: list[str] = [
    "#0072B2",  # blue
    "#D55E00",  # vermilion
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#56B4E9",  # sky blue
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#000000",  # black
]

# Nature / Science 高对比度学术风格色板
NATURE_LIST: list[str] = [
    "#2E86AB",  # Deep Steel Blue
    "#A23B72",  # Ruby Plum
    "#F18F01",  # Amber Orange
    "#C73E1D",  # Russet Red
    "#95C623",  # Olive Leaf
    "#5B5F97",  # Slate Purple
]

# 中文核心学术期刊色板（端庄典雅，高对比度，黑白印刷区分度极高）
CHINESE_JOURNAL_LIST: list[str] = [
    "#1D3557",  # 深海军蓝
    "#E63946",  # 砖红
    "#457B9D",  # 中蓝
    "#2A9D8F",  # 墨绿
    "#E76F51",  # 暖橙
    "#6C757D",  # 石墨灰
]

# 强语义警示 / 截断 / ROI 标红专色（绝对严禁滥用于大面积背景或普通曲线）
ALERT_RED = "#D62728"
ROI_BORDER_RED = "#FF1A1A"
REF_GREY = "#94A3B8"
ACCENT_GREEN = "#2ECC71"


# ══════════════════════════════════════════════════════════════
# 3. 跨平台字体探测与环境配置
# ══════════════════════════════════════════════════════════════

def detect_best_fonts(is_chinese: bool = False) -> tuple[list[str], str]:
    """
    Detect optimal font family based on OS platform and language requirement.
    Returns: (font_list, font_family_name)
    """
    system = platform.system()
    
    if is_chinese:
        # 中英混排候选列表
        if system == "Windows":
            return ["SimSun", "SimHei", "Microsoft YaHei", "Arial", "Times New Roman"], "sans-serif"
        elif system == "Darwin":  # macOS
            return ["PingFang SC", "STHeiti", "Arial", "Times New Roman"], "sans-serif"
        else:  # Linux
            return ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "SimSun", "DejaVu Sans"], "sans-serif"
    else:
        # 英文顶刊（默认 Arial，兼容 Times New Roman）
        if system == "Windows":
            return ["Arial", "Helvetica", "DejaVu Sans"], "sans-serif"
        elif system == "Darwin":
            return ["Arial", "Helvetica", "Nimbus Sans"], "sans-serif"
        else:
            return ["Arial", "DejaVu Sans", "Liberation Sans"], "sans-serif"


def set_journal_profile(
    journal: str = "elsevier",
    font_style: str = "sans-serif",    # 'sans-serif' (Arial) or 'serif' (Times)
    is_chinese: bool = False,
    base_fontsize: float = 9.0,
) -> None:
    """
    Configure matplotlib rcParams to strictly match top journal standards.

    Parameters
    ----------
    journal : 'elsevier' | 'ieee' | 'nature' | 'springer' | 'chinese_core'
    font_style : 'sans-serif' (Arial, recommended) or 'serif' (Times New Roman)
    is_chinese : True if generating Chinese or bilingual labels
    base_fontsize : base typographic scale in points (default: 9.0 pt)
    """
    fonts, fallback_family = detect_best_fonts(is_chinese=is_chinese)

    if font_style == "serif" and not is_chinese:
        fonts = ["Times New Roman", "DejaVu Serif", "Liberation Serif"]
        fallback_family = "serif"

    rc = {
        # ── 字体与渲染 ──────────────────────────────────────
        "font.family": fallback_family,
        f"font.{fallback_family}": fonts,
        "axes.unicode_minus": False,         # 解决负号显示为乱码方块问题
        "text.usetex": False,                 # 避免调用外部 TeX 导致跨机字体混乱
        "mathtext.fontset": "custom",
        "mathtext.rm": fonts[0],
        "mathtext.it": f"{fonts[0]}:italic",
        "mathtext.bf": f"{fonts[0]}:bold",
        "mathtext.default": "regular",

        # ── 字号体系 (严格符合 7 - 10 pt 印刷规约) ──────────
        "font.size": base_fontsize,
        "axes.labelsize": base_fontsize + 0.5,
        "axes.titlesize": base_fontsize + 0.5,
        "legend.fontsize": base_fontsize - 0.5,
        "xtick.labelsize": base_fontsize - 0.5,
        "ytick.labelsize": base_fontsize - 0.5,

        # ── 坐标轴与刻度线 ──────────────────────────────────
        "axes.linewidth": 0.6,               # 符合期刊 >=0.25 pt 印刷下限
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.minor.width": 0.35,
        "ytick.minor.width": 0.35,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.minor.size": 2.0,
        "ytick.minor.size": 2.0,
        "xtick.direction": "in",             # 刻度朝内，保持工程/物理学术紧凑感
        "ytick.direction": "in",
        "xtick.top": True,                   # 四方闭合刻度
        "ytick.right": True,

        # ── 图例规约 ────────────────────────────────────────
        "legend.framealpha": 0.88,
        "legend.edgecolor": "none",
        "legend.fancybox": False,
        "legend.borderpad": 0.35,
        "legend.handlelength": 1.6,

        # ── 矢量保存与嵌入防封杀 (TrueType Type 42) ──────────
        "savefig.dpi": 600,                  # 高清点阵图默认 600 DPI
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
        "savefig.pad_inches": 0.04,
        "pdf.fonttype": 42,                  # TrueType 嵌入，杜绝 Type 3 报错
        "ps.fonttype": 42,
    }

    plt.rcParams.update(rc)


# ══════════════════════════════════════════════════════════════
# 4. 专业图表构件辅助函数 (Helper Utilities)
# ══════════════════════════════════════════════════════════════

def add_subplot_label(
    ax: Axes,
    label: str,
    *,
    loc: str = "upper left",
    fontsize: float = 9.5,
    fontweight: str = "bold",
    pad: float = 0.03,
) -> None:
    """
    在子图边缘添加标准 (a), (b), (c) 标识，附带半透明纯白衬底。
    """
    x_map = {"left": pad, "right": 1 - pad}
    y_map = {"upper": 1 - pad, "lower": pad}
    ha_map = {"left": "left", "right": "right"}
    va_map = {"upper": "top", "lower": "bottom"}

    parts = loc.split()
    vert, horiz = parts[0], parts[1]

    ax.text(
        x_map[horiz], y_map[vert], label,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight=fontweight,
        ha=ha_map[horiz],
        va=va_map[vert],
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.82,
            pad=1.8,
        ),
        zorder=20,
    )


def add_roi_box(
    ax: Axes,
    xywh: tuple[float, float, float, float],
    *,
    color: str = ROI_BORDER_RED,
    linewidth: float = 1.1,
    linestyle: str = "-",
) -> mpl.patches.Rectangle:
    """
    在子图上绘制感兴趣区域 (ROI) 红框。
    xywh: (x, y, width, height) in data coordinates.
    """
    x, y, w, h = xywh
    rect = plt.Rectangle(
        (x, y), w, h,
        linewidth=linewidth,
        edgecolor=color,
        facecolor="none",
        linestyle=linestyle,
        zorder=15,
    )
    ax.add_patch(rect)
    return rect


def add_metric_badge(
    ax: Axes,
    text: str,
    *,
    is_ours: bool = False,
    loc: str = "lower left",
    fontsize: float = 7.5,
    pad: float = 0.04,
) -> None:
    """
    在算法对比图的子图角标添加量化指标标牌（如 IoU = 85.2%）。
    """
    txt_color = ACCENT_GREEN if is_ours else "#A3E635"
    x = pad if "left" in loc else 1.0 - pad
    y = pad if "lower" in loc else 1.0 - pad
    ha = "left" if "left" in loc else "right"
    va = "bottom" if "lower" in loc else "top"

    ax.text(
        x, y, text,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight="bold",
        color=txt_color,
        ha=ha, va=va,
        bbox=dict(
            boxstyle="square,pad=0.15",
            facecolor="black",
            edgecolor="none",
            alpha=0.82,
        ),
        zorder=25,
    )


def save_publication_figure(
    fig: Figure,
    base_path: Path | str,
    *,
    formats: Sequence[str] = ("pdf", "png", "svg"),
    dpi: int = 600,
    close: bool = False,
) -> list[Path]:
    """
    一键输出顶刊级矢量 PDF (Type 42)、高清 PNG 与矢量 SVG。
    """
    base = Path(base_path)
    base.parent.mkdir(parents=True, exist_ok=True)
    saved_paths: list[Path] = []

    for ext in formats:
        out = base.with_suffix(f".{ext}")
        fig.savefig(
            str(out),
            dpi=dpi,
            bbox_inches="tight",
            facecolor="white",
        )
        saved_paths.append(out)
        print(f"  [Saved] {out}")

    if close:
        plt.close(fig)

    return saved_paths

