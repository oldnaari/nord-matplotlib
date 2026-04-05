# Nord color palette constants

# Polar Night
POLAR_NIGHT_1 = "#2E3440"   # darkest — figure background
POLAR_NIGHT_2 = "#3B4252"   # axes background
POLAR_NIGHT_3 = "#434C5E"   # grid lines
POLAR_NIGHT_4 = "#4C566A"   # ticks / spines

# Snow Storm
SNOW_1 = "#D8DEE9"   # darkest snow — first in color cycle
SNOW_2 = "#E5E9F0"
SNOW_3 = "#ECEFF4"   # brightest

# Frost
FROST_1 = "#8FBCBB"
FROST_2 = "#88C0D0"   # "Frost Blue" — second in color cycle
FROST_3 = "#81A1C1"
FROST_4 = "#5E81AC"

# Aurora
AURORA_RED    = "#BF616A"
AURORA_ORANGE = "#D08770"
AURORA_YELLOW = "#EBCB8B"
AURORA_GREEN  = "#A3BE8C"
AURORA_PURPLE = "#B48EAD"

# Ordered color cycle (matches prop_cycle in the style file)
CYCLE = [
    SNOW_1,
    FROST_2,
    AURORA_RED,
    AURORA_ORANGE,
    AURORA_YELLOW,
    AURORA_GREEN,
    AURORA_PURPLE,
]

# Colormap stops (low → high)
CMAP_STOPS = [
    AURORA_RED,
    AURORA_ORANGE,
    AURORA_YELLOW,
    AURORA_GREEN,
    FROST_2,
    SNOW_1,
]
