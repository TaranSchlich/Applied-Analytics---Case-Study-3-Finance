#!/usr/bin/env python3
"""Case Study #3 (Finance) — Urban Hamster.

Insight-led findings deck for the finance team. Minimal styling: a thin
magenta accent at the top of each page and under the title only; everything
else is black text on white / light-gray panels."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PINK = RGBColor(0xE9, 0x1E, 0x8C)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x55, 0x55, 0x55)
TAB = RGBColor(0x75, 0x75, 0x75)
LIGHT = RGBColor(0xEE, 0xEE, 0xEE)
BORDER = RGBColor(0xBD, 0xBD, 0xBD)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def rect(slide, x, y, w, h, fill, line=None, line_w=1.25):
    shp = slide.shapes.add_shape(1, x, y, w, h)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space=None, line_spacing=None):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    first = True
    for txt, size, bold, color in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        if space is not None:
            p.space_after = Pt(space)
        if line_spacing is not None:
            p.line_spacing = line_spacing
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = FONT
    return tb


def content_header(slide, title, chip, chip_w=Inches(6.3)):
    rect(slide, 0, 0, SW, Inches(0.09), PINK)
    text(slide, Inches(0.5), Inches(0.17), Inches(12.3), Inches(0.62),
         [(title, 23, True, DARK)])
    rect(slide, Inches(0.5), Inches(0.85), Inches(6.5), Inches(0.04), PINK)
    rect(slide, Inches(0.5), Inches(0.97), chip_w, Inches(0.34), LIGHT)
    rect(slide, Inches(0.5), Inches(0.97), Inches(0.06), Inches(0.34), TAB)
    text(slide, Inches(0.72), Inches(1.02), chip_w - Inches(0.35), Inches(0.25),
         [(chip, 10, True, DARK)], anchor=MSO_ANCHOR.MIDDLE)


def chart_box(slide, x, y, w, h, img=None, title=None, filename=None):
    rect(slide, x, y, w, h, WHITE, BORDER, 1.25)
    if img and os.path.exists(img):
        pad = Inches(0.12)
        iw = w - 2 * pad
        ih = Emu(int(int(iw) / 1.9))
        iy = Emu(int(y) + (int(h) - int(ih)) // 2)
        slide.shapes.add_picture(img, Emu(int(x) + int(pad)), iy, iw, ih)
    else:
        cy = Emu(int(y) + int(h * 0.40))
        text(slide, x, cy, w, Inches(0.3),
             [("INSERT CHART", 12, True, GRAY)], align=PP_ALIGN.CENTER)
        if title:
            text(slide, x, Emu(int(cy) + Inches(0.32)), w, Inches(0.35),
                 [(title, 13, True, DARK)], align=PP_ALIGN.CENTER)
        if filename:
            text(slide, x, Emu(int(cy) + Inches(0.68)), w, Inches(0.3),
                 [(filename, 9, False, GRAY)], align=PP_ALIGN.CENTER)


def callout(slide, x, y, w, h, heading, runs):
    rect(slide, x, y, w, h, LIGHT)
    rect(slide, x, y, Inches(0.07), h, TAB)
    text(slide, Emu(int(x) + Inches(0.25)), Emu(int(y) + Inches(0.13)),
         w - Inches(0.4), Inches(0.32), [(heading, 13, True, DARK)])
    text(slide, Emu(int(x) + Inches(0.25)), Emu(int(y) + Inches(0.48)),
         w - Inches(0.5), h - Inches(0.55), runs, line_spacing=1.04)


def kpi_panel(slide, x, y, w, h, number, label, sub=None):
    rect(slide, x, y, w, h, WHITE, BORDER, 1.25)
    text(slide, x, Emu(int(y) + Inches(0.10)), w, Emu(int(h * 0.52)),
         [(number, 46, True, DARK)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(slide, x, Emu(int(y) + int(h * 0.58)), w, Emu(int(h * 0.24)),
         [(label, 12, True, DARK)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if sub:
        text(slide, x, Emu(int(y) + int(h * 0.82)), w, Emu(int(h * 0.16)),
             [(sub, 9.5, False, GRAY)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def bullet_block(slide, x, y, w, items, size=11, gap=7):
    """items = list of (lead_bold, rest)."""
    tb = slide.shapes.add_textbox(x, y, w, Inches(2.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    first = True
    for lead, rest in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap)
        p.line_spacing = 1.04
        r1 = p.add_run(); r1.text = lead
        r1.font.size = Pt(size); r1.font.bold = True
        r1.font.color.rgb = DARK; r1.font.name = FONT
        if rest:
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.bold = False
            r2.font.color.rgb = DARK; r2.font.name = FONT
    return tb


# ========================================================================
# COVER
# ========================================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, Inches(0.14), PINK)
rect(s, 0, Inches(7.38), SW, Inches(0.10), LIGHT)
rect(s, Inches(5.02), Inches(0.30), Inches(3.3), Inches(1.55), LIGHT)
rect(s, Inches(5.02), Inches(0.30), Inches(0.07), Inches(1.55), TAB)
text(s, Inches(5.22), Inches(0.82), Inches(3.0), Inches(0.45),
     [("CASE STUDY #3", 14, True, DARK)])
text(s, Inches(5.22), Inches(1.20), Inches(3.0), Inches(0.3),
     [("Finance — pricing & sales", 11, False, GRAY)])
text(s, Inches(0.73), Inches(2.12), Inches(12.33), Inches(1.05),
     [("URBAN  HAMSTER", 54, True, DARK)], align=PP_ALIGN.CENTER)
text(s, Inches(0.5), Inches(3.24), Inches(12.33), Inches(0.32),
     [("C L O T H I N G", 13, False, GRAY)], align=PP_ALIGN.CENTER)
rect(s, Inches(4.42), Inches(3.80), Inches(4.5), Inches(0.05), TAB)
text(s, Inches(0.61), Inches(4.04), Inches(12.33), Inches(0.7),
     [("Pricing & Sales Performance Review", 32, False, DARK)], align=PP_ALIGN.CENTER)
text(s, Inches(0.61), Inches(4.92), Inches(12.33), Inches(0.4),
     [("Where we're growing, how our margins hold, and the next move on price",
       16, False, GRAY)], align=PP_ALIGN.CENTER)
# context strip
text(s, Inches(0.61), Inches(5.66), Inches(12.33), Inches(0.32),
     [("29,120 products   ·   2,756 brands   ·   10 distribution centers   ·   5 years of orders",
       12, True, GRAY)], align=PP_ALIGN.CENTER)
text(s, Inches(0.5), Inches(6.78), Inches(12.33), Inches(0.3),
     [("T. Schlichtmann  |  GB884  |  June 2026", 12, False, GRAY)], align=PP_ALIGN.CENTER)

# ========================================================================
# SLIDE 1 — GROWTH
# ========================================================================
s = prs.slides.add_slide(BLANK)
content_header(s, "Five Years of Volume-Led Growth — Revenue Up 90.7%",
               "Revenue grew 21× since 2019, yet average order value never left ~$86",
               chip_w=Inches(7.4))

chart_box(s, Inches(0.4), Inches(1.5), Inches(6.1), Inches(3.55),
          img="revenue_by_year.png")
chart_box(s, Inches(6.85), Inches(1.5), Inches(6.1), Inches(3.55),
          img="aov_by_year.png")

callout(s, Inches(0.4), Inches(5.25), Inches(12.55), Inches(1.85), "What This Means", [
    ("Revenue climbed from $197K in 2019 to $4.16M in 2023 — about 21× — and growth "
     "re-accelerated last year, from +65.8% in 2022 to +90.7% in 2023. ", 11.5, True, DARK),
    ("But average order value held near $86 every single year, so roughly 96% of the growth "
     "came from more orders, not higher prices. We've been growing on volume and have left "
     "price untouched — a clear, untapped lever. (Revenue uses actual sale price, all orders "
     "included per the team's request.)", 11.5, False, DARK),
])

# ========================================================================
# SLIDE 2 — MARGIN & PRICING
# ========================================================================
s = prs.slides.add_slide(BLANK)
content_header(s, "Disciplined Pricing — and a Pattern in the Exceptions",
               "No loss-makers; 99.99% follow cost-plus-50%; the 4 exceptions are all two-piece sets",
               chip_w=Inches(8.6))

kpi_panel(s, Inches(0.4), Inches(1.5), Inches(2.95), Inches(1.75),
          "0", "sold below cost")
kpi_panel(s, Inches(3.55), Inches(1.5), Inches(2.95), Inches(1.75),
          "4", "below 50% markup", sub="of 29,120 — just 0.01%")

bullet_block(s, Inches(0.4), Inches(3.45), Inches(6.1), [
    ("All four are two-piece sets ", "(Orvis, N.G.U., Woman Within, Jessica London) at ~49% — a bundle-pricing quirk, not a systemic leak. A quick re-price closes it."),
    ("Margins are otherwise wide: ", "our best single item earns $594/unit (Alpha Industries Darla); premium labels like Nobis list near $830."),
    ("The catch: ", "this checks list price, not the price we actually collect."),
], size=11, gap=8)

chart_box(s, Inches(6.85), Inches(1.5), Inches(6.1), Inches(3.45),
          img="markup_vs_target.png")

callout(s, Inches(0.4), Inches(5.55), Inches(12.55), Inches(1.55), "What This Means", [
    ("On paper pricing is healthy — nothing sells below cost and the catalog follows the "
     "cost-plus-50% playbook almost perfectly. Two gaps remain: the rule prices off our "
     "costs, not the market (cost+50% may still be off vs. competitors), and it ignores "
     "checkout discounts that quietly erode margin — the “sale we never intended.” "
     "Recommend tracking realized margin (sale price vs. cost), not just list.",
     11.5, False, DARK),
])

# ========================================================================
# SLIDE 3 — COMPETITOR BENCHMARKING
# ========================================================================
s = prs.slides.add_slide(BLANK)
content_header(s, "Pricing to the Market, Not Just to Cost",
               "How to compare our prices to competitors — and where to start",
               chip_w=Inches(7.4))

text(s, Inches(0.55), Inches(1.5), Inches(5.8), Inches(0.34),
     [("What to Benchmark", 15, True, DARK)])
rect(s, Inches(0.55), Inches(1.86), Inches(1.5), Inches(0.04), PINK)
left_items = [
    ("Start Focused, Not Boundless",
     "The top 200–500 products that drive most revenue — not all 29,120."),
    ("Prioritize by Volume and Value",
     "Lead with our biggest lines (Intimates 2,363; Jeans 1,999; Tops & Tees 1,868) and "
     "highest-ticket ones (Outerwear ~$146; Suits & Sport Coats ~$127)."),
    ("Mind Brand Concentration",
     "Allegra K alone is 1,034 products (3.5% of the catalog) — a natural place to start."),
]
iy = 2.15
for t_, b_ in left_items:
    rect(s, Inches(0.52), Inches(iy), Inches(0.06), Inches(1.0), TAB)
    text(s, Inches(0.72), Inches(iy), Inches(5.7), Inches(0.3), [(t_, 13, True, DARK)])
    text(s, Inches(0.72), Inches(iy + 0.32), Inches(5.75), Inches(0.7),
         [(b_, 10.5, False, DARK)], line_spacing=1.0)
    iy += 1.18

rect(s, Inches(6.6), Inches(1.5), Inches(0.03), Inches(4.45), BORDER)

text(s, Inches(6.85), Inches(1.5), Inches(6.0), Inches(0.34),
     [("How to Run It", 15, True, DARK)])
rect(s, Inches(6.85), Inches(1.86), Inches(1.5), Inches(0.04), PINK)
right_items = [
    ("Match Cadence to Volatility",
     "Monthly baseline; weekly / near-real-time for fast-moving and seasonal items."),
    ("Compare Two Ways",
     "Industry average for context; named competitors for prices we can act on directly."),
    ("Source from Snowflake Marketplace",
     "Pull third-party pricing datasets and join them to our products table — no scraping "
     "or ETL to build."),
]
iy = 2.15
for t_, b_ in right_items:
    rect(s, Inches(6.85), Inches(iy), Inches(0.06), Inches(1.0), TAB)
    text(s, Inches(7.05), Inches(iy), Inches(5.7), Inches(0.3), [(t_, 13, True, DARK)])
    text(s, Inches(7.05), Inches(iy + 0.32), Inches(5.75), Inches(0.7),
         [(b_, 10.5, False, DARK)], line_spacing=1.0)
    iy += 1.18

callout(s, Inches(0.4), Inches(6.05), Inches(12.55), Inches(1.05), "Bottom Line", [
    ("Growth is strong and pricing is disciplined — so the next dollar of margin comes from "
     "pricing to the market, not just to cost. Stand up competitor benchmarking and "
     "realized-margin tracking, and we can align price with both our costs and the market.",
     11.5, False, DARK),
])

prs.save("Urban_Hamster_Case3_Finance_Findings.pptx")
print("saved")
