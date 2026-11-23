#!/usr/bin/env python3
"""Render THE DAYBREAK LEDGER v2 — @topan-kun's poster for news-image-20261122.

Dark-broadsheet one-page summary of Sunday 22 November 2026, breadth build:
a Hormuz hero across the top, a six-detail strip, TWELVE illustrated story
cards in a 3x4 grid (scene strip on top, large headline below), an ALSO
TODAY strip with four more one-line stories, region chips, a DATE CHECK box.
17 stories, 7 regions. Every fact comes from the verified ledger in
stories-daybreak.md (pool: stories-v3.md / stories.md of the main project).

Deterministic: pure Pillow drawing, no randomness, no clock reads except
the DATE CHECK stamp constant below. Run twice -> identical bytes.
Output: entry.png next to this file (1024x1024, <= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ---------------------------------------------------------------- palette
W = 1024
MARGIN = 24
CW = W - 2 * MARGIN                     # content width = 976

BG       = (13, 20, 38)                 # deep navy sheet
PANEL    = (22, 35, 61)                 # card face
PANEL_HI = (28, 44, 74)                 # hero text band
EDGE     = (52, 72, 105)                # panel borders
CREAM    = (242, 233, 216)              # main text
MUTED    = (168, 180, 200)              # secondary text
GOLD     = (217, 164, 65)               # accents, region tags
RED      = (224, 75, 58)                # date check, alarms
INK      = (10, 16, 30)                 # text on cream chips

SERIF_B  = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_O   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"

VERIFIED_STAMP = "WIRE-CHECKED · 22 NOV 2026"   # build-time constant, set at final build

_fonts = {}
def font(path, size):
    key = (path, size)
    if key not in _fonts:
        try:
            _fonts[key] = ImageFont.truetype(path, size)
        except Exception:
            _fonts[key] = ImageFont.truetype(SANS, size)
    return _fonts[key]

def tw(draw, s, f):
    return draw.textlength(s, font=f)

def wrap(draw, s, f, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(draw, trial, f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_font(draw, s, path, size, maxw, floor=10):
    while size > floor and tw(draw, s, font(path, size)) > maxw:
        size -= 1
    return font(path, size)

def chip_number(draw, x, y, w, h, text, size=14):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CREAM)
    f = fit_font(draw, text, SANS_B, size, w - 8)
    draw.text((x + w / 2, y + h / 2), text, font=f, fill=INK, anchor="mm")

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, W), BG)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.line([MARGIN, 12, W - MARGIN, 12], fill=GOLD, width=2)
f_title = fit_font(d, "THE DAYBREAK LEDGER", SERIF_B, 44, CW)
d.text((W / 2, 20), "THE DAYBREAK LEDGER", font=f_title, fill=CREAM, anchor="ma")
d.line([MARGIN, 74, W - MARGIN, 74], fill=GOLD, width=2)
d.text((W / 2, 82), "SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 25),
       fill=GOLD, anchor="ma")
d.text((W - MARGIN, 88), "17 stories · 7 regions · one page",
       font=font(SANS, 12), fill=MUTED, anchor="ra")
d.text((MARGIN, 88), "Late edition — the day in one image",
       font=font(SANS_O, 12), fill=MUTED, anchor="la")

# ---------------------------------------------------------------- hero scene
HX0, HY0, HX1, HY1 = MARGIN, 112, W - MARGIN, 304
SCENE_BOT = 206                          # scene zone 112..206, text band below
for i in range(8):
    t = i / 8
    col = (10 + int(10 * t), 18 + int(16 * t), 34 + int(26 * t))
    y = HY0 + (SCENE_BOT - HY0) * i // 8
    d.rectangle([HX0, y, HX1, HY0 + (SCENE_BOT - HY0) * (i + 1) // 8], fill=col)
d.ellipse([848, 124, 880, 156], fill=(226, 222, 200))          # moon
d.ellipse([858, 120, 884, 146], fill=(16, 28, 48))
d.rectangle([HX0, 168, HX1, SCENE_BOT], fill=(11, 30, 52))     # sea
for sx in range(HX0 + 30, HX1 - 40, 90):
    d.line([sx, 192, sx + 34, 192], fill=(64, 96, 128), width=2)
d.polygon([(HX0, 168), (HX0, SCENE_BOT), (210, SCENE_BOT), (258, 184), (196, 172),
           (120, 168)], fill=(6, 10, 18))
d.polygon([(HX1, 164), (HX1, SCENE_BOT), (782, SCENE_BOT), (742, 182), (806, 170),
           (884, 166)], fill=(6, 10, 18))
d.rectangle([880, 146, 924, 164], fill=(24, 34, 54))           # radar site
d.line([902, 146, 902, 128], fill=(120, 132, 152), width=3)
d.arc([882, 108, 922, 148], start=200, end=340, fill=(150, 160, 178), width=3)
d.line([902, 128, 922, 116], fill=(150, 160, 178), width=3)

def tanker(cx, cy, scale, flame=False):
    L = int(150 * scale)
    hull_y = cy + int(16 * scale)
    d.polygon([(cx - L // 2, cy), (cx + L // 2, cy), (cx + L // 2 - int(14 * scale), hull_y),
               (cx - L // 2 + int(8 * scale), hull_y)], fill=(16, 24, 40))
    d.rectangle([cx - L // 2, hull_y, cx + L // 2 - int(14 * scale), hull_y + 3],
                fill=(120, 52, 40))
    cols = [(52, 84, 96), (140, 84, 52), (70, 104, 84), (96, 74, 110)]
    bx = cx - L // 2 + int(16 * scale)
    for i, c in enumerate(cols):
        bw = int(22 * scale)
        d.rectangle([bx + i * (bw + 2), cy - int(13 * scale), bx + (i + 1) * (bw + 2) - 2, cy],
                    fill=c)
    sx = cx + L // 2 - int(30 * scale)
    d.rectangle([sx, cy - int(22 * scale), sx + int(14 * scale), cy], fill=(196, 198, 204))
    d.rectangle([sx + int(3 * scale), cy - int(28 * scale), sx + int(8 * scale), cy - int(22 * scale)],
                fill=(150, 154, 164))
    if flame:
        fx, fy = cx - int(6 * scale), cy - int(14 * scale)
        d.polygon([(fx - 11, fy), (fx, fy - 30), (fx + 11, fy)], fill=(232, 116, 36))
        d.polygon([(fx - 5, fy), (fx, fy - 17), (fx + 5, fy)], fill=(246, 190, 60))
        for dx, dy, r, c in ((9, -38, 6, (70, 76, 90)), (18, -46, 9, (86, 92, 104)),
                             (28, -54, 11, (100, 106, 118))):
            d.ellipse([fx + dx - r, fy + dy - r, fx + dx + r, fy + dy + r], fill=c)

tanker(238, 184, 0.85)
tanker(498, 176, 0.95, flame=True)
tanker(716, 188, 0.75)
for x in range(HX0 + 40, HX1 - 30, 36):
    d.line([x, 200, x + 18, 200], fill=(150, 122, 58), width=2)
d.rectangle([HX0, HY0, HX1, SCENE_BOT], outline=EDGE, width=2)

# hero text band
d.rectangle([HX0, SCENE_BOT, HX1, HY1], fill=PANEL_HI)
d.line([HX0, SCENE_BOT, HX1, SCENE_BOT], fill=GOLD, width=3)
d.text((HX0 + 18, SCENE_BOT + 8), "MIDDLE EAST · THE BIG STORY",
       font=font(SANS_B, 12), fill=GOLD, anchor="la")
f_hero = fit_font(d, "TANKERS HIT IN THE STRAIT OF HORMUZ", SERIF_B, 34, CW - 190)
d.text((HX0 + 18, SCENE_BOT + 26), "TANKERS HIT IN THE STRAIT OF HORMUZ",
       font=f_hero, fill=CREAM, anchor="la")
hero_body = ("Iran strikes US targets in Bahrain for the third time in five days; at least "
             "3 oil tankers are hit or damaged in the strait, one set ablaze. US jets "
             "answer, hitting IRGC missile-launcher sites on Qeshm Island.")
for i, line in enumerate(wrap(d, hero_body, font(SANS, 14), CW - 190)):
    d.text((HX0 + 18, SCENE_BOT + 66 + i * 18), line, font=font(SANS, 14),
           fill=(214, 220, 232), anchor="la")
d.text((HX1 - 164, SCENE_BOT + 8), "(AP · Reuters · UKMTO)",
       font=font(SANS_O, 11), fill=MUTED, anchor="ra")
chip_number(d, HX1 - 148, SCENE_BOT + 22, 128, 58, "3", size=28)
d.text((HX1 - 84, SCENE_BOT + 86), "tankers hit", font=font(SANS_B, 11),
       fill=CREAM, anchor="ma")

# ---------------------------------------------------------------- numbers strip
SY0, SY1 = 312, 358
d.rectangle([MARGIN, SY0, W - MARGIN, SY1], fill=PANEL, outline=EDGE)
NUMBERS = [
    ("114–91", "Spurs beat the Pelicans"),
    ("8", "regions struck in Yemen"),
    ("2", "wounded in Bahrain"),
    ("3 DAYS", "Pugh's swim across Hormuz"),
    ("LONGEST", "COP31 summit in history"),
    ("FIRST", "pilotless air-taxi riders"),
]
cell_w = CW / 6
for i, (num, lab) in enumerate(NUMBERS):
    cx = MARGIN + cell_w * (i + 0.5)
    if i:
        d.line([MARGIN + cell_w * i, SY0 + 7, MARGIN + cell_w * i, SY1 - 7],
               fill=EDGE, width=1)
    d.text((cx, SY0 + 4), num, font=font(SANS_B, 22), fill=GOLD, anchor="ma")
    for j, line in enumerate(wrap(d, lab, font(SANS, 10), cell_w - 12)):
        d.text((cx, SY0 + 31 + j * 11), line, font=font(SANS, 10), fill=CREAM, anchor="ma")

# ---------------------------------------------------------------- card scenes (wide strips, 316x36)
def scene_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 44))
    d.rectangle([x + 30, y + h - 12, x + w - 90, y + h - 6], fill=(96, 66, 40))
    for i in range(7):
        cx = x + 44 + i * 34
        d.rectangle([cx, y + h - 22, cx + 16, y + h - 13], fill=(40, 58, 92))
    px, py = x + w - 62, y + 3
    d.rectangle([px, py, px + 24, py + 30], fill=(232, 228, 216))
    d.line([px + 3, py + 3, px + 21, py + 27], fill=RED, width=3)
    d.line([px + 21, py + 3, px + 3, py + 27], fill=RED, width=3)

def scene_fire(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 22, 20))
    d.rectangle([x + 60, y + 16, x + 200, y + h - 2], fill=(24, 20, 26))
    for i in range(5):
        bx = x + 60 + i * 28
        d.polygon([(bx, y + 16), (bx + 14, y + 6), (bx + 28, y + 16)], fill=(24, 20, 26))
    d.rectangle([x + 216, y + 4, x + 228, y + h - 2], fill=(24, 20, 26))
    for fx, fh in ((92, 22), (124, 30), (156, 20)):
        d.polygon([(x + fx - 9, y + 18), (x + fx, y + 18 - fh), (x + fx + 9, y + 18)],
                  fill=(232, 116, 36))
        d.polygon([(x + fx - 4, y + 18), (x + fx, y + 18 - fh // 2), (x + fx + 4, y + 18)],
                  fill=(246, 190, 60))
    d.ellipse([x + 226, y + 2, x + 268, y + 14], fill=(96, 92, 96))
    d.rectangle([x + 250, y + h - 12, x + 292, y + h - 3], fill=(150, 40, 36))
    d.rectangle([x + 266, y + h - 17, x + 276, y + h - 12], fill=(150, 40, 36))

def scene_chart(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 26, 44))
    for gy in (y + 10, y + 20, y + 30):
        d.line([x + 6, gy, x + w - 6, gy], fill=(30, 46, 70), width=1)
    pts = [(x + 14, y + 6), (x + 70, y + 10), (x + 126, y + 16), (x + 182, y + 22),
           (x + 238, y + 30)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.polygon([(x + 238, y + 30), (x + 230, y + 29), (x + 237, y + 21)], fill=RED)
    d.rectangle([x + 262, y + h - 14, x + 276, y + h - 3], fill=(52, 140, 84))
    d.rectangle([x + 282, y + h - 20, x + 296, y + h - 3], fill=(52, 140, 84))

def scene_flags(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 38, 66))
    d.line([x, y + h - 4, x + w, y + h - 4], fill=(120, 128, 110), width=2)
    for px in (x + 92, x + 196):
        d.line([px, y + 4, px, y + h - 4], fill=(180, 184, 192), width=2)
    fx, fy, fw, fh = x + 92, y + 4, 40, 24
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(36, 54, 120))
    d.line([fx, fy, fx + fw, fy + fh], fill=(230, 230, 230), width=3)
    d.line([fx + fw, fy, fx, fy + fh], fill=(230, 230, 230), width=3)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(230, 230, 230), width=6)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(230, 230, 230), width=6)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(196, 40, 48), width=3)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(196, 40, 48), width=3)
    fx2 = x + 196
    d.rectangle([fx2, fy, fx2 + fw, fy + fh], fill=(36, 54, 140))
    for k in range(8):
        a = 2 * math.pi * k / 8
        gx, gy = fx2 + fw // 2 + 8 * math.cos(a), fy + fh // 2 + 8 * math.sin(a)
        d.ellipse([gx - 1.8, gy - 1.8, gx + 1.8, gy + 1.8], fill=GOLD)
    hx = x + w // 2 + 62
    d.ellipse([hx - 4, y + h - 24, hx + 4, y + h - 16], fill=CREAM)
    d.line([hx, y + h - 16, hx, y + h - 5], fill=CREAM, width=3)
    d.rectangle([hx + 4, y + h - 19, hx + 12, y + h - 8], fill=GOLD)

def scene_f1(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 24))
    for i, c in enumerate([(214, 84, 150), (84, 150, 214), (214, 190, 84), (120, 220, 160)]):
        d.rectangle([x + 40 + i * 62, y + 4, x + 56 + i * 62, y + 8], fill=c)
    cy = y + h - 22
    d.polygon([(x + 88, cy + 12), (x + 116, cy + 2), (x + 168, cy - 2), (x + 212, cy + 4),
               (x + 226, cy + 12)], fill=(168, 32, 40))
    d.rectangle([x + 84, cy - 6, x + 97, cy + 10], fill=(120, 22, 30))
    d.line([x + 210, cy + 2, x + 230, cy - 4], fill=(120, 22, 30), width=3)
    for wx in (x + 118, x + 200):
        d.ellipse([wx - 9, cy + 8, wx + 9, cy + 26], fill=(8, 8, 10))
        d.ellipse([wx - 3, cy + 14, wx + 3, cy + 20], fill=(140, 144, 152))
    d.line([x + 20, cy + 26, x + w - 20, cy + 26], fill=(90, 96, 110), width=2)

def scene_hoop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 26, 20))
    d.line([x + 6, y + h - 5, x + w - 6, y + h - 5], fill=(120, 90, 60), width=2)
    d.rectangle([x + 238, y + 4, x + 282, y + 22], outline=(230, 230, 230), width=2)
    d.line([x + 252, y + 24, x + 268, y + 24], fill=(232, 116, 36), width=3)
    px = x + 108
    d.ellipse([px - 5, y + 6, px + 5, y + 16], fill=CREAM)
    d.line([px, y + 16, px, y + h - 6], fill=CREAM, width=4)
    d.line([px, y + 20, px + 30, y + 10], fill=CREAM, width=3)
    d.ellipse([px + 30, y + 2, px + 43, y + 15], fill=(232, 116, 36))
    d.line([px + 43, y + 8, x + 252, y + 16], fill=(150, 130, 110), width=1)

def scene_aid(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 50, 44))
    d.rectangle([x + 84, y + 8, x + 196, y + 30], fill=(228, 228, 224))
    d.rectangle([x + 196, y + 15, x + 226, y + 30], fill=(200, 202, 198))
    d.rectangle([x + 201, y + 18, x + 212, y + 24], fill=(70, 90, 110))
    for wx in (x + 104, x + 208):
        d.ellipse([wx - 6, y + 27, wx + 6, y + 39], fill=(16, 16, 18))
    d.rectangle([x + 133, y + 12, x + 141, y + 26], fill=RED)
    d.rectangle([x + 129, y + 16, x + 145, y + 22], fill=RED)
    for bx in (x + 30, x + 252):
        d.rectangle([bx, y + 22, bx + 20, y + 34], fill=(176, 148, 104))
        d.line([bx + 10, y + 24, bx + 10, y + 32], fill=RED, width=2)
        d.line([bx + 5, y + 28, bx + 15, y + 28], fill=RED, width=2)

def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 30))
    af = [(38, 8), (52, 6), (60, 14), (58, 24), (66, 32), (62, 44), (54, 52),
          (50, 68), (44, 84), (38, 92), (32, 80), (30, 62), (24, 52), (26, 40),
          (20, 30), (26, 18), (32, 12)]
    pts = [(x + 108 + int((px - 20) * 0.36), y + int(py * 0.36)) for px, py in af]
    d.polygon(pts, fill=(178, 146, 62))
    d.ellipse([x + 168, y + 5, x + 196, y + 33], fill=(236, 236, 232))
    d.rectangle([x + 179, y + 11, x + 185, y + 27], fill=RED)
    d.rectangle([x + 175, y + 16, x + 189, y + 22], fill=RED)
    for i in range(3):
        d.line([x + 226 + i * 26, y + 26, x + 238 + i * 26, y + 10], fill=(120, 160, 130), width=2)

def scene_yemen(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 44, 30))
    d.ellipse([x + 268, y + 4, x + 292, y + 22], fill=(240, 200, 110))
    for bx, bh in ((30, 12), (62, 17), (98, 10), (228, 14), (258, 9)):
        d.rectangle([x + bx, y + h - bh, x + bx + 24, y + h], fill=(30, 24, 18))
    jx, jy = x + 138, y + 8                                        # jet silhouette
    d.polygon([(jx, jy + 6), (jx + 16, jy), (jx + 30, jy + 5), (jx + 44, jy + 6),
               (jx + 30, jy + 10), (jx + 16, jy + 11)], fill=(14, 14, 16))
    d.polygon([(jx + 18, jy + 1), (jx + 24, jy - 5), (jx + 28, jy + 2)], fill=(14, 14, 16))
    for ex, ey in ((x + 66, y + 22), (x + 240, y + 18)):           # bursts
        for a in range(0, 360, 45):
            exx = ex + 9 * math.cos(math.radians(a)); eyy = ey + 9 * math.sin(math.radians(a))
            d.line([ex, ey, exx, eyy], fill=(246, 190, 60), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(232, 116, 36))

def scene_trade(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 58))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(11, 30, 52))
    for px in (x + 56, x + 226):
        d.line([px, y + 3, px, y + h - 8], fill=(180, 184, 192), width=2)
    fx, fy, fw, fh = x + 56, y + 3, 34, 21                          # EU flag
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(36, 54, 140))
    for k in range(8):
        a = 2 * math.pi * k / 8
        gx, gy = fx + fw // 2 + 7 * math.cos(a), fy + fh // 2 + 7 * math.sin(a)
        d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=GOLD)
    fx2 = x + 226                                                   # Indonesia flag
    d.rectangle([fx2, fy, fx2 + fw, fy + fh // 2], fill=(196, 40, 48))
    d.rectangle([fx2, fy + fh // 2, fx2 + fw, fy + fh], fill=(238, 238, 238))
    sx, sy = x + 128, y + h - 16                                    # cargo ship
    d.polygon([(sx, sy), (sx + 62, sy), (sx + 54, sy + 7), (sx + 6, sy + 7)], fill=(16, 24, 40))
    for i, c in enumerate([(52, 84, 96), (140, 84, 52), (70, 104, 84)]):
        d.rectangle([sx + 8 + i * 15, sy - 8, sx + 21 + i * 15, sy], fill=c)
    d.polygon([(x + 148, y + 6), (x + 162, y + 12), (x + 148, y + 18)], fill=GOLD)  # arrow
    d.line([x + 128, y + 12, x + 156, y + 12], fill=GOLD, width=3)

def scene_brazil(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 44))
    for rx in range(x + 14, x + w - 10, 26):                        # rain
        d.line([rx, y + 3, rx - 4, y + 13], fill=(120, 160, 200), width=2)
    d.rectangle([x + 196, y + 14, x + 252, y + h - 6], fill=(30, 26, 24))   # house
    d.polygon([(x + 190, y + 14), (x + 224, y + 4), (x + 258, y + 14)], fill=(70, 44, 30))
    d.rectangle([x + 216, y + 22, x + 232, y + h - 6], fill=(12, 10, 10))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(38, 74, 96))    # flood water
    d.line([x + 30, y + h - 5, x + 90, y + h - 5], fill=(90, 130, 160), width=2)
    d.line([x + 120, y + 24, x + 168, y + 30], fill=(120, 88, 52), width=4)  # debris log
    hx = x + 96                                                     # resident clearing
    d.ellipse([hx - 4, y + 12, hx + 4, y + 20], fill=CREAM)
    d.line([hx, y + 20, hx, y + h - 8], fill=CREAM, width=3)
    d.line([hx, y + 24, hx + 18, y + h - 10], fill=CREAM, width=2)
    d.line([hx + 18, y + h - 10, hx + 26, y + h - 16], fill=(150, 150, 150), width=3)

def scene_pugh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 34, 56))
    for wx in range(x + 10, x + w - 16, 34):                        # wave crests
        d.arc([wx, y + h - 16, wx + 22, y + h - 2], start=180, end=360,
              fill=(90, 140, 180), width=2)
    sx, sy = x + 196, y + 8                                         # distant tanker
    d.polygon([(sx, sy + 10), (sx + 84, sy + 10), (sx + 76, sy + 16), (sx + 6, sy + 16)],
              fill=(10, 16, 28))
    d.rectangle([sx + 58, sy + 2, sx + 68, sy + 10], fill=(120, 124, 132))
    for i, c in enumerate([(52, 84, 96), (140, 84, 52)]):
        d.rectangle([sx + 12 + i * 16, sy + 3, sx + 26 + i * 16, sy + 10], fill=c)
    hx, hy = x + 108, y + h - 18                                    # swimmer
    d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(232, 200, 170))
    d.line([hx, hy + 2, hx + 20, hy - 10], fill=(232, 200, 170), width=4)
    d.ellipse([hx + 20, hy - 13, hx + 26, hy - 7], fill=(232, 200, 170))
    d.arc([hx - 16, hy - 8, hx + 14, hy + 12], start=300, end=120, fill=(240, 240, 240), width=2)

# ---------------------------------------------------------------- cards
# (region, headline, source, number, scene) — 12 cards, 3 cols x 4 rows
CARDS = [
    ("GLOBAL", "COP31 TALKS COLLAPSE", "Reuters · WRI", "0 FOSSIL-FUEL MENTIONS", scene_cop31),
    ("ASIA-PACIFIC", "SERANG FACTORY FIRE", "Reuters · AP · AFP", "39 MISSING", scene_fire),
    ("ASIA-PACIFIC", "TAIWAN STOCKS PLUNGE", "wires", "7,641 PTS — WEEK", scene_chart),
    ("EUROPE", "BRITAIN OPENS TO EU YOUTH", "wires · BBC", "100,000 A YEAR", scene_flags),
    ("NORTH AMERICA", "VERSTAPPEN WINS IN VEGAS", "BBC", "34 LEAD CHANGES", scene_f1),
    ("NORTH AMERICA", "WEMBANYAMA SCORES 50", "BBC", "50 PTS", scene_hoop),
    ("MIDDLE EAST", "AID WORKERS KILLED IN GAZA", "wires", "3 KILLED", scene_aid),
    ("AFRICA", "EBOLA TOLL PASSES 5,700", "wires", "5,700 DEATHS", scene_ebola),
    ("MIDDLE EAST", "70+ RAIDS HIT YEMEN", "wires", "70+ RAIDS", scene_yemen),
    ("ASIA-PACIFIC", "EU–INDONESIA TRADE DEAL", "wires", "10 YRS OF TALKS", scene_trade),
    ("GLOBAL", "PUGH SWIMS THE STRAIT", "wires", "15 KM SWIM", scene_pugh),
    ("LATIN AMERICA", "BRAZIL TOWN DIGS OUT", "wires", "CLEAN-UP BEGINS", scene_brazil),
]
GRID_Y = 366
CARD_W, CARD_H, GAP = 318, 110, 11
SCENE_H = 36
for idx, (region, head, src, num, scene) in enumerate(CARDS):
    r, c = divmod(idx, 3)
    x = MARGIN + c * (CARD_W + GAP)
    y = GRID_Y + r * (CARD_H + GAP)
    d.rectangle([x, y, x + CARD_W, y + CARD_H], fill=PANEL, outline=EDGE)
    scene(x + 1, y + 1, CARD_W - 2, SCENE_H)
    d.line([x, y + SCENE_H + 1, x + CARD_W, y + SCENE_H + 1], fill=EDGE, width=1)
    # region tag over scene (navy backing, gold text) + source right
    f_tag = font(SANS_B, 10)
    tag_w = tw(d, region, f_tag) + 12
    d.rectangle([x + 1, y + 1, x + 1 + tag_w, y + 17], fill=(10, 16, 30))
    d.text((x + 7, y + 4), region, font=f_tag, fill=GOLD, anchor="la")
    d.rectangle([x + CARD_W - 1 - (tw(d, src, font(SANS_O, 9)) + 12), y + 1,
                 x + CARD_W - 1, y + 17], fill=(10, 16, 30))
    d.text((x + CARD_W - 7, y + 4), src, font=font(SANS_O, 9), fill=MUTED, anchor="ra")
    if num:
        chip_number(d, x + CARD_W - 164, y + SCENE_H - 21, 156, 24, num, size=12)
    # headline: largest size 28..20 whose wrap fits 2 lines in the zone below
    zone_w = CARD_W - 20
    hsize = 28
    while hsize > 20 and len(wrap(d, head, font(SANS_B, hsize), zone_w)) > 2:
        hsize -= 1
    f_head = font(SANS_B, hsize)
    lines = wrap(d, head, f_head, zone_w)
    lh = hsize + 5
    total_h = lh * len(lines) - 5
    hy = y + SCENE_H + 2 + (CARD_H - SCENE_H - 2 - total_h) // 2
    for i, line in enumerate(lines):
        d.text((x + 10, hy + i * lh), line, font=f_head, fill=CREAM, anchor="la")

# ---------------------------------------------------------------- also today
AY = 844
d.rectangle([MARGIN, AY, W - MARGIN, AY + 84], fill=PANEL, outline=EDGE)
d.text((MARGIN + 12, AY + 6), "ALSO TODAY — FOUR MORE FROM SUNDAY",
       font=font(SANS_B, 14), fill=GOLD, anchor="la")
ALSO = [
    ("TOKYO", "Pilotless air taxi carries first passengers"),
    ("MADRID", "Spain to expand bank tax for housing"),
    ("USA", "Teen gamer helps FBI rescue kidnapped girl"),
    ("EDO", "Governor to oversee kidnapper executions"),
]
f_place = font(SANS_B, 16)
f_also = font(SANS_B, 16)
col_w = (CW - 24) // 2
for i, (place, head) in enumerate(ALSO):
    r, c = divmod(i, 2)
    ax = MARGIN + 12 + c * col_w
    ay = AY + 32 + r * 27
    d.text((ax, ay), place + " — ", font=f_place, fill=GOLD, anchor="la")
    off = tw(d, place + " — ", f_place)
    d.text((ax + off, ay), head, font=f_also, fill=CREAM, anchor="la")

# ---------------------------------------------------------------- region chips
CHIP_Y = 936
labels = ["MIDDLE EAST 3", "ASIA-PACIFIC 4", "NORTH AMERICA 3", "EUROPE 2",
          "AFRICA 2", "LATIN AMERICA 1", "GLOBAL 2"]
f_chip = font(SANS_B, 12)
widths = [tw(d, s, f_chip) + 22 for s in labels]
total = sum(widths) + 8 * (len(labels) - 1)
cx = (W - total) / 2
for s, wch in zip(labels, widths):
    d.rounded_rectangle([cx, CHIP_Y, cx + wch, CHIP_Y + 24], radius=6,
                        fill=(24, 40, 70), outline=GOLD)
    d.text((cx + wch / 2, CHIP_Y + 12), s, font=f_chip, fill=CREAM, anchor="mm")
    cx += wch + 8

# ---------------------------------------------------------------- date check
DY = 968
d.rectangle([MARGIN, DY, W - MARGIN, DY + 46], outline=RED, width=2)
d.text((MARGIN + 12, DY + 5), "DATE CHECK — WHAT WE LEFT OUT",
       font=font(SANS_B, 11), fill=RED, anchor="la")
d.text((W - MARGIN - 12, DY + 5), VERIFIED_STAMP, font=font(SANS_B, 11),
       fill=RED, anchor="ra")
dc_lines = [
    "×  “El Chapo Isidro” arrested — captured Fri 20 Nov, announced Sat 21 Nov (Reuters/AP). Not 22 Nov.",
    "×  Trump–Xi–Putin Shenzhen summit — held Thu 19 Nov at APEC (WSJ, Le Monde). Not 22 Nov.",
]
for i, line in enumerate(dc_lines):
    d.text((MARGIN + 12, DY + 21 + i * 13), line, font=font(SANS, 10),
           fill=(226, 214, 200), anchor="la")

img.save("entry.png")
print("saved entry.png")
