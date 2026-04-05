"""Nord colormap — registered as 'nord' and 'nord_r'."""

import matplotlib as mpl
import matplotlib.colors as mcolors

from ._palette import CMAP_STOPS

_registered = False


def register():
    """Register the 'nord' colormap (idempotent)."""
    global _registered
    if _registered:
        return
    nord   = mcolors.LinearSegmentedColormap.from_list("nord",   CMAP_STOPS)
    nord_r = mcolors.LinearSegmentedColormap.from_list("nord_r", CMAP_STOPS[::-1])
    for cmap in (nord, nord_r):
        try:
            mpl.colormaps.register(cmap)
        except ValueError:
            pass  # already registered
    _registered = True


def get(reverse=False) -> mcolors.LinearSegmentedColormap:
    """Return the nord colormap object without side-effects."""
    stops = CMAP_STOPS[::-1] if reverse else CMAP_STOPS
    name  = "nord_r" if reverse else "nord"
    return mcolors.LinearSegmentedColormap.from_list(name, stops)
