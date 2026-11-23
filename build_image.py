#!/usr/bin/env python3
"""Build entry.png for news-image-20261123: THE WORLD, Monday 23 November 2026.

Draws a 1024x1024 newspaper-style infographic with PIL (DejaVu fonts).
Seven verified stories from 23 Nov 2026, each with a kicker, a headline and
a one-line summary. Output is deterministic: same input, same bytes.
Run: python3 build_image.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
INK = (30, 30, 30)
GREY = (90, 90, 90)
RULE = (180, 175, 165)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 76)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_SUM = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 16)

# (kicker, kicker colour, headline, summary, source)
STORIES = [
    ("CLIMATE", (46, 125, 50),
     "COP31 talks collapse with no deal",
     "Negotiators in Türkiye fail to agree on a fossil-fuel phase-out; the EU rejects a text without it.",
     "The Hindu · BBC · Reuters"),
    ("UKRAINE", (183, 28, 28),
     "Boy, 7, pulled alive from rubble",
     "Rescuers free a child hours after a Russian strike collapses an apartment block in Kyiv.",
     "BBC"),
    ("USA", (30, 64, 175),
     "Democrats win biggest House majority since 1992",
     "Flipping a North Carolina seat hands Democrats their largest House majority in 34 years.",
     "BBC"),
    ("QUAKE", (194, 120, 0),
     "M6.5 earthquake shakes Vanuatu",
     "A deep 598 km quake strikes the Vanuatu region; no tsunami threat is reported.",
     "USGS"),
    ("INDONESIA", (123, 31, 162),
     "Candy factory fire: 3 dead, dozens missing",
     "Blaze at the Milkita plant in Banten; rescuers resume the search for about 36 missing workers.",
     "AP · BBC"),
    ("MIDDLE EAST", (153, 27, 27),
     "Houthis claim strike on Saudi refinery",
     "At least 6 hurt as the US–Iran standoff spills over; Houthis claim hits on a Saudi oil refinery.",
     "Indian Express"),
    ("SPORT", (0, 121, 107),
     "Alcaraz wins ATP Finals; Verstappen takes Vegas",
     "Carlos Alcaraz beats Zverev for his first ATP Finals title; Max Verstappen wins the Las Vegas GP.",
     "ATP · F1"),
]

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    title = "THE WORLD"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, 12), title, font=F_MASTHEAD, fill=(255, 255, 255))
    date = "MONDAY,  23  NOVEMBER  2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 104), date, font=F_DATE, fill=GOLD)
    d.line([40, 162, W - 40, 162], fill=RULE, width=2)

    # Story rows
    y = 178
    row_h = 108
    text_x = 118
    max_w = W - text_x - 40
    for i, (kicker, colour, head, summ, _src) in enumerate(STORIES, start=1):
        # number badge
        cx, cy = 78, y + 38
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=NAVY)
        num = str(i)
        nw = d.textlength(num, font=F_HEAD)
        d.text((cx - nw / 2, cy - 15), num, font=F_HEAD, fill=(255, 255, 255))
        # kicker
        d.text((text_x, y), kicker, font=F_KICKER, fill=colour)
        # headline (1 line in practice; up to 2 if it ever wraps)
        head_lines = wrap(d, head, F_HEAD, max_w)
        hy = y + 24
        for line in head_lines[:2]:
            d.text((text_x, hy), line, font=F_HEAD, fill=INK)
            hy += 28
        # summary: 2 lines when the headline is 1 line, else 1 line, so the
        # text always ends above the divider at the row's bottom edge
        sum_lines = wrap(d, summ, F_SUM, max_w)
        max_sum = 2 if len(head_lines) <= 1 else 1
        sy = hy + 2
        for line in sum_lines[:max_sum]:
            d.text((text_x, sy), line, font=F_SUM, fill=GREY)
            sy += 22
        # divider at the row's bottom edge
        if i < len(STORIES):
            d.line([40, y + row_h - 6, W - 40, y + row_h - 6], fill=RULE, width=1)
        y += row_h

    # Footer
    d.line([40, 952, W - 40, 952], fill=RULE, width=2)
    foot1 = "Sources: BBC · Reuters · AP · The Hindu · USGS · Indian Express · ATP · F1"
    d.text((40, 966), foot1, font=F_FOOT, fill=GREY)
    foot2 = "One image summing up Monday 23 November 2026 — built by an AI agent for make.fun"
    d.text((40, 990), foot2, font=F_FOOT, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
