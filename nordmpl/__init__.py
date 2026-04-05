"""
nordmpl — Nord Dark theme for Matplotlib.

Quickstart
----------
    import nordmpl
    nordmpl.set()

    # Use matplotlib normally — no other calls needed.
    fig, ax = plt.subplots()
    ax.plot(...)
    ax.set_xlabel("x")        # Avenir LT Std, automatic
    ax.set_title("My chart")  # for Norwester: nordmpl.apply(ax, title="...")

Public API
----------
    set()           Apply the full theme (fonts + cmap + style + auto-hook).
    apply(ax, ...)  Set a Norwester title; also ensures fonts if needed.
    cmap            The 'nord' LinearSegmentedColormap object.
    palette         Module with individual Nord colour constants.
"""

import matplotlib as mpl
import matplotlib.style
import matplotlib.figure
import matplotlib.axes
from pathlib import Path

from . import _fonts, _cmap
from ._palette import (
    POLAR_NIGHT_1, POLAR_NIGHT_2, POLAR_NIGHT_3, POLAR_NIGHT_4,
    SNOW_1, SNOW_2, SNOW_3,
    FROST_1, FROST_2, FROST_3, FROST_4,
    AURORA_RED, AURORA_ORANGE, AURORA_YELLOW, AURORA_GREEN, AURORA_PURPLE,
    CYCLE,
)
from ._apply import apply, _apply_internal, _style_pie_texts, _styled
from . import _palette as palette

_STYLE_PATH = Path(__file__).parent / "data" / "nord-dark.mplstyle"

cmap = _cmap.get()

_hooked = False


def set() -> None:                          # noqa: A001
    """
    Activate the Nord Dark theme.

    1. Register bundled fonts with fontManager.
    2. Register the 'nord' colormap.
    3. Apply the .mplstyle rcParams.
    4. Patch Figure.__init__ — registers an axobserver on every new figure
       so fonts are applied automatically when any axes is created.
    5. Patch Axes.pie — styles slice labels after pie() adds them,
       since they don't exist at axes-creation time.
    """
    global _hooked

    _fonts.register()
    _cmap.register()
    matplotlib.style.use(str(_STYLE_PATH))
    mpl.rcParams["image.cmap"] = "nord"

    if _hooked:
        return
    _hooked = True

    # ── Hook 1: auto-style axes on creation ───────────────────────────────
    def _observer(fig: matplotlib.figure.Figure) -> None:
        for ax in fig.get_axes():
            _apply_internal(ax)

    _orig_fig_init = matplotlib.figure.Figure.__init__

    def _patched_fig_init(self, *args, **kwargs):
        _orig_fig_init(self, *args, **kwargs)
        self.add_axobserver(_observer)

    matplotlib.figure.Figure.__init__ = _patched_fig_init

    # ── Hook 2: auto-style pie labels after pie() is called ───────────────
    _orig_pie = matplotlib.axes.Axes.pie

    def _patched_pie(self, *args, **kwargs):
        result = _orig_pie(self, *args, **kwargs)
        # Discard so _apply_internal re-runs and picks up the new texts
        _styled.discard(self)
        _apply_internal(self)
        return result

    matplotlib.axes.Axes.pie = _patched_pie
