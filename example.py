"""
Nord Dark style — layout reference
Mirrors the structure of matplotlib's style_sheets_reference.html
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import nordmpl
nordmpl.set()

from nordmpl._palette import FROST_2, POLAR_NIGHT_1, POLAR_NIGHT_3, POLAR_NIGHT_4, CYCLE
from nordmpl._fonts import title_font

BG_FIG = POLAR_NIGHT_1
GRID   = POLAR_NIGHT_3
TICK_C = POLAR_NIGHT_4
COLORS = CYCLE

# ── Data ───────────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)
x   = np.linspace(0, 2 * np.pi, 200)

# ── Layout: 4 × 2 + 1 full-width cmap row ─────────────────────────────────
fig = plt.figure(figsize=(16, 14))
fig.suptitle(
    "Nord Dark   Matplotlib Style Reference",
    fontproperties=fm.FontProperties(family="Norwester", size=20),
    y=0.97,
)

gs = fig.add_gridspec(
    5, 2,
    height_ratios=[1, 1, 1, 1, 0.18],
    hspace=0.55, wspace=0.35,
    left=0.07, right=0.96, top=0.93, bottom=0.04,
)

# ── 1. Line plot ───────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
for i, color in enumerate(COLORS):
    ax1.plot(x, np.sin(x + i * np.pi / 4) * (1 - i * 0.08),
             color=color, label=f"series {i+1}")
ax1.set_xlabel("x")
ax1.set_ylabel("amplitude")
ax1.legend(loc="upper right", ncol=2)
nordmpl.apply(ax1, "Line plot")

# ── 2. Scatter ─────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
for i, color in enumerate(COLORS[:5]):
    ax2.scatter(rng.normal(i, 0.4, 40), rng.normal(i, 0.4, 40),
                color=color, alpha=0.75, s=25, label=f"class {i}")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.legend(loc="upper left", ncol=3)
nordmpl.apply(ax2, "Scatter plot")

# ── 3. Bar chart ───────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
values     = rng.uniform(0.3, 1.0, len(categories))
ax3.bar(categories, values, color=COLORS[:len(categories)], width=0.6)
ax3.set_ylim(0, 1.2)
ax3.set_xlabel("Month")
ax3.set_ylabel("Value")
nordmpl.apply(ax3, "Bar chart")

# ── 4. Stacked area ────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
t     = np.linspace(0, 10, 300)
waves = [np.abs(np.sin(t * (i + 1) * 0.4)) * 0.5 for i in range(4)]
ax4.stackplot(t, *waves, labels=["a", "b", "c", "d"],
              colors=COLORS[1:5], alpha=0.85)
ax4.set_xlabel("t")
ax4.set_ylabel("amplitude")
ax4.legend(loc="upper right", ncol=4)
nordmpl.apply(ax4, "Stacked area")

# ── 5. Histogram ───────────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, 0])
for i, color in enumerate(COLORS[:4]):
    ax5.hist(rng.normal(i * 0.8, 0.6, 300), bins=30,
             alpha=0.6, color=color, label=f"mean={i*0.8:.1f}")
ax5.set_xlabel("value")
ax5.set_ylabel("count")
ax5.legend(loc="upper right", ncol=2)
nordmpl.apply(ax5, "Histogram")

# ── 6. Step + confidence band ──────────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 1])
steps = np.cumsum(rng.normal(0, 1, 80))
upper = steps + rng.uniform(0.3, 1.2, 80)
lower = steps - rng.uniform(0.3, 1.2, 80)
ax6.fill_between(range(80), lower, upper, color=FROST_2, alpha=0.25)
ax6.step(range(80), steps, color=FROST_2, linewidth=1.6, where="mid")
ax6.axhline(0, color=GRID, linewidth=0.8, linestyle="--")
ax6.set_xlabel("step")
ax6.set_ylabel("value")
nordmpl.apply(ax6, "Step + confidence band")

# ── 7. Donut chart ─────────────────────────────────────────────────────────
ax7 = fig.add_subplot(gs[3, 0])
sizes = [22, 18, 15, 12, 10, 14, 9]
ax7.pie(                               # label colours handled by theme
    sizes,
    labels=["Snow", "Frost", "Red", "Orange", "Yellow", "Green", "Purple"],
    autopct="%1.0f%%",
    pctdistance=0.78,
    wedgeprops={"width": 0.55, "edgecolor": BG_FIG, "linewidth": 2},
    startangle=90,
)
nordmpl.apply(ax7, "Donut chart")

# ── 8. Heatmap (uses 'nord' cmap by default) ───────────────────────────────
ax8 = fig.add_subplot(gs[3, 1])
heat = rng.standard_normal((8, 10)).cumsum(axis=1)
im   = ax8.imshow(heat, aspect="auto", extent=(0, 10, 0, 8), origin="lower")
fig.colorbar(im, ax=ax8, pad=0.02)
ax8.set_xlabel("x")
ax8.set_ylabel("y")
nordmpl.apply(ax8, "Heatmap")

# ── 9. Colormap gradient showcase (full-width bottom row) ──────────────────
ax9 = fig.add_subplot(gs[4, :])
ax9.imshow(np.linspace(0, 1, 512).reshape(1, -1), aspect="auto")
ax9.set_axis_off()
ax9.text(-0.005, 0.5, "low",  transform=ax9.transAxes,
         ha="right", va="center", color=TICK_C)
ax9.text(1.005,  0.5, "high", transform=ax9.transAxes,
         ha="left",  va="center", color=TICK_C)
ax9.set_title("nord colormap", fontproperties=title_font(), pad=6)

plt.savefig("assets/nord-dark-reference.webp", dpi=150, bbox_inches="tight")
print("Saved: assets/nord-dark-reference.webp")
plt.show()
