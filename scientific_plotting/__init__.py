#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scientific-plotting: Publication-ready scientific plotting engine for top-tier journals.
"""

from .figure_config import (
    set_journal_profile,
    get_canvas_size,
    detect_best_fonts,
    mm_to_inches,
    TOL_MUTED,
    TOL_MUTED_LIST,
    OKABE_ITO_LIST,
    NATURE_LIST,
    CHINESE_JOURNAL_LIST,
    ALERT_RED,
    ROI_BORDER_RED,
    REF_GREY,
    ACCENT_GREEN,
    add_subplot_label,
    add_roi_box,
    add_metric_badge,
    save_publication_figure,
)

__version__ = "1.0.0"
__all__ = [
    "set_journal_profile",
    "get_canvas_size",
    "detect_best_fonts",
    "mm_to_inches",
    "TOL_MUTED",
    "TOL_MUTED_LIST",
    "OKABE_ITO_LIST",
    "NATURE_LIST",
    "CHINESE_JOURNAL_LIST",
    "ALERT_RED",
    "ROI_BORDER_RED",
    "REF_GREY",
    "ACCENT_GREEN",
    "add_subplot_label",
    "add_roi_box",
    "add_metric_badge",
    "save_publication_figure",
]

