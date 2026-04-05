"""
Per-axes font application.

Why this can't live in rcParams:
  matplotlib has `font.family` (global) but no per-element font-family keys
  like `axes.title.fontfamily` or `xtick.labelfamily`.  The three-font
  split (Norwester / Avenir LT Std / JetBrains Mono) must be applied
  programmatically after an axes is created.

_apply_internal(ax) is called automatically:
  - via Figure.add_axobserver (registered in nordmpl.set()) for normal axes
  - via an Axes.pie patch for pie/donut charts (labels don't exist until
    after pie() is called, so they can't be styled at axes-creation time)

Users never need to call _apply_internal directly.
apply(ax, title=...) is the public API for setting a Norwester title.
"""

from __future__ import annotations
import weakref

import numpy as np
import matplotlib.axes
from matplotlib.patches import Wedge

# Axes that have already been styled — prevents redundant work when the
# observer fires multiple times (e.g. after a colorbar is added).
_styled: weakref.WeakSet = weakref.WeakSet()


def _apply_internal(ax: matplotlib.axes.Axes) -> None:
    """
    Apply Nord fonts to axis labels and tick labels.
    For pie charts, also styles the slice labels by radial position.
    Idempotent: safe to call multiple times on the same axes.
    """
    if ax in _styled:
        return
    _styled.add(ax)

    from ._fonts import label_font, tick_font
    from ._palette import POLAR_NIGHT_1, POLAR_NIGHT_4

    ax.xaxis.label.set_fontproperties(label_font())
    ax.yaxis.label.set_fontproperties(label_font())

    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontproperties(tick_font())

    _style_pie_texts(ax)


def _style_pie_texts(ax: matplotlib.axes.Axes) -> None:
    """
    Style pie/donut chart labels by radial position.

    In matplotlib pie coords the wedge outer edge is at r = 1.0.
      r > 1  →  outer category label  →  Polar Night 4
      r < 1  →  autopct label (inside wedge)  →  Polar Night 1

    Uses radial position, not text content, so it's format-agnostic.
    Called both from _apply_internal (in case pie was drawn before the
    observer fired) and from the Axes.pie patch (the normal path).
    """
    if not any(isinstance(p, Wedge) for p in ax.patches):
        return

    from ._fonts import tick_font
    from ._palette import POLAR_NIGHT_1, POLAR_NIGHT_4

    for text in ax.texts:
        x, y = text.get_position()
        if np.hypot(x, y) > 1.0:
            text.set_color(POLAR_NIGHT_4)
            text.set_fontproperties(tick_font())
        else:
            text.set_color(POLAR_NIGHT_1)


def apply(ax: matplotlib.axes.Axes, title: str | None = None) -> None:
    """
    Public API — set a Norwester title on *ax*.

    Font styling is applied automatically when the axes is created.
    The only reason to call this is to set a title in the Norwester typeface,
    or to force-apply fonts to an axes created before nordmpl.set() was called.

    Parameters
    ----------
    ax:    Target axes.
    title: Title text rendered in Norwester.  Pass None to only ensure fonts.
    """
    _apply_internal(ax)

    if title is not None:
        from ._fonts import title_font
        from ._palette import SNOW_1
        ax.set_title(title, fontproperties=title_font(), color=SNOW_1, pad=8)
