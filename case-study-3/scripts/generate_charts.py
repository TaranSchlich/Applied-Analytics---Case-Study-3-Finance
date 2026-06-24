#!/usr/bin/env python3
"""Generate all charts for the Case Study #3 finance deck, in one consistent
minimal style (white bg, dark line/bars, a single magenta accent)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PINK = "#E91E8C"
DARK = "#1A1A1A"
BAR = "#9E9E9E"
GRID = "#D9D9D9"
LINE = "#1F3552"  # deep navy for line series

plt.rcParams["font.family"] = "DejaVu Sans"

years = [2019, 2020, 2021, 2022, 2023]
revenue = [196829.32, 694405.70, 1315714.64, 2181671.66, 4159538.94]
orders = [2275, 8019, 15228, 25617, 47895]
aov = [r / o for r, o in zip(revenue, orders)]


def style_ax(ax):
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["left", "bottom"]:
        ax.spines[sp].set_color(GRID)
    ax.tick_params(colors=DARK, labelsize=9)


def line_chart(fname, yvals, title, ylabel, fmt, ymax, ytick_fmt=None):
    fig, ax = plt.subplots(figsize=(6.6, 3.5), dpi=200)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.plot(years, yvals, color=LINE, linewidth=2.6, zorder=3,
            marker="o", markersize=6, markerfacecolor=LINE)
    # highlight the latest year in magenta
    ax.plot(years[-1], yvals[-1], marker="o", markersize=10,
            markerfacecolor=PINK, markeredgecolor=PINK, zorder=4)
    for x, y in zip(years, yvals):
        ax.annotate(fmt(y), (x, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=9.5,
                    fontweight="bold", color=DARK)
    ax.set_ylim(0, ymax)
    ax.set_xticks(years)
    if ytick_fmt is not None:
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: ytick_fmt(v)))
    ax.set_ylabel(ylabel, fontsize=10, color=DARK)
    ax.set_title(title, fontsize=12.5, fontweight="bold", color=DARK, pad=12)
    style_ax(ax)
    plt.tight_layout()
    plt.savefig(fname, facecolor="white", bbox_inches="tight")
    plt.close()
    print("saved", fname)


# 1) Revenue by year
line_chart("revenue_by_year.png", revenue,
           "Revenue by Year (2019–2023)", "Revenue",
           lambda v: f"${v/1e6:.2f}M", 4.8e6,
           ytick_fmt=lambda v: f"${v/1e6:.0f}M" if v > 0 else "$0")

# 2) Average order value by year (the flat line — volume story)
line_chart("aov_by_year.png", aov,
           "Average Order Value by Year (2019–2023)", "Avg. order value",
           lambda v: f"${v:.0f}", 120)

# 3) Markup of the 4 off-policy products vs. 50% target
fig, ax = plt.subplots(figsize=(6.6, 3.5), dpi=200)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
labels = ["Orvis", "N.G.U.", "Woman\nWithin", "Jessica\nLondon"]
markups = [49.7, 49.5, 49.3, 49.3]
bars = ax.bar(labels, markups, color=BAR, width=0.62, zorder=3)
ax.axhline(50, color=PINK, linestyle="--", linewidth=1.8, zorder=4)
ax.text(3.45, 54.5, "50% target", color=PINK, fontsize=10,
        fontweight="bold", ha="right", va="center")
for b, m in zip(bars, markups):
    ax.text(b.get_x() + b.get_width()/2, m - 3.5, f"{m:.1f}%",
            ha="center", va="top", fontsize=10, color="white", fontweight="bold")
ax.set_ylim(0, 60)
ax.set_ylabel("Markup over cost (%)", fontsize=10, color=DARK)
ax.set_title("The 4 Off-Policy Items Are All Two-Piece Sets",
             fontsize=12.5, fontweight="bold", color=DARK, pad=12)
style_ax(ax)
plt.tight_layout()
plt.savefig("markup_vs_target.png", facecolor="white", bbox_inches="tight")
plt.close()
print("saved markup_vs_target.png")
