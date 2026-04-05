"""Font registration and FontProperties factories."""

from pathlib import Path
import matplotlib.font_manager as fm

_DATA = Path(__file__).parent / "data"

_FONT_FILES = [
    _DATA / "Norwester.ttf",
    _DATA / "AvenirLTStd-Regular.otf",
    _DATA / "AvenirLTStd-Heavy.otf",
    _DATA / "JetBrainsMonoLight.ttf",
]

_registered = False


def register():
    """Register bundled fonts with matplotlib's font manager (idempotent)."""
    global _registered
    if _registered:
        return
    for path in _FONT_FILES:
        fm.fontManager.addfont(str(path))
    _registered = True


def title_font(size=14) -> fm.FontProperties:
    return fm.FontProperties(family="Norwester", size=size)


def label_font(size=11) -> fm.FontProperties:
    return fm.FontProperties(family="Avenir LT Std", size=size)


def tick_font(size=9) -> fm.FontProperties:
    return fm.FontProperties(family="JetBrains Mono", weight=300, size=size)
