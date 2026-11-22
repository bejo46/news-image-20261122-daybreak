#!/usr/bin/env python3
"""Render THE DAYBREAK LEDGER — @topan-kun's poster for news-image-20261122.

A dark-broadsheet one-page summary of Sunday 22 November 2026: a Hormuz
hero across the top, a six-number strip, nine illustrated story cards in
a 3x3 grid, region chips, a DATE CHECK box and a source footer. Every
fact comes from the verified ledger in stories-daybreak.md (which points
back to stories-v3.md / stories.md of the main project).

Deterministic: pure Pillow drawing, no randomness, no clock reads except
the DATE CHECK stamp constant below. Run twice -> identical bytes.
Output: entry.png next to this file (1024x1024, <= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

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

VERIFIED_STAMP = "Verified at 22:52 WIB"   # build-time constant, set at final build

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
    """Greedy word wrap; returns list of lines that each fit maxw."""
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
    """Shrink from size until the single line s fits maxw."""
    while size > floor and tw(draw, s, font(path, size)) > maxw:
        size -= 1
    return font(path, size)

def chip_number(draw, x, y, w, h, text, size=14):
    """Solid cream chip with navy bold number — never drawn over busy art."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CREAM)
    f = fit_font(draw, text, SANS_B, size, w - 8)
    draw.text((x + w / 2, y + h / 2), text, font=f, fill=INK, anchor="mm")

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, W), BG)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.line([MARGIN, 14, W - MARGIN, 14], fill=GOLD, width=2)
f_title = fit_font(d, "THE DAYBREAK LEDGER", SERIF_B, 47, CW)
d.text((W / 2, 24), "THE DAYBREAK LEDGER", font=f_title, fill=CREAM, anchor="ma")
d.line([MARGIN, 80, W - MARGIN, 80], fill=GOLD, width=2)
f_date = font(SANS_B, 28)
d.text((W / 2, 90), "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=GOLD, anchor="ma")
d.text((W - MARGIN, 96), "10 stories · 7 regions · one page",
       font=font(SANS, 13), fill=MUTED, anchor="ra")
d.text((MARGIN, 96), "Late edition — the day in one image",
       font=font(SANS_O, 13), fill=MUTED, anchor="la")

# ---------------------------------------------------------------- hero scene
HX0, HY0, HX1, HY1 = MARGIN, 128, W - MARGIN, 432
SCENE_BOT = 322                          # scene zone 128..322, text band below
# night sky bands
for i in range(10):
    t = i / 10
    col = (10 + int(10 * t), 18 + int(16 * t), 34 + int(26 * t))
    y = HY0 + (SCENE_BOT - HY0) * i // 10
    d.rectangle([HX0, y, HX1, HY0 + (SCENE_BOT - HY0) * (i + 1) // 10], fill=col)
# moon + glow
d.ellipse([838, 148, 878, 188], fill=(226, 222, 200))
d.ellipse([850, 142, 884, 176], fill=(16, 28, 48))
# sea (lower half of the scene)
d.rectangle([HX0, 252, HX1, SCENE_BOT], fill=(11, 30, 52))
for sx in range(HX0 + 30, HX1 - 40, 90):  # moonlit streaks
    d.line([sx, 292, sx + 34, 292], fill=(64, 96, 128), width=2)
# coasts: left (Arabian side) and right (Iran side) silhouettes
d.polygon([(HX0, 252), (HX0, SCENE_BOT), (210, SCENE_BOT), (258, 288), (196, 262),
           (120, 254)], fill=(6, 10, 18))
d.polygon([(HX1, 246), (HX1, SCENE_BOT), (782, SCENE_BOT), (742, 284), (806, 258),
           (884, 248)], fill=(6, 10, 18))
# radar installation on the right coast (Bahrain hint)
d.rectangle([880, 224, 932, 248], fill=(24, 34, 54))
d.line([906, 224, 906, 200], fill=(120, 132, 152), width=3)
d.arc([884, 178, 928, 222], start=200, end=340, fill=(150, 160, 178), width=3)
d.line([906, 200, 928, 186], fill=(150, 160, 178), width=3)

def tanker(cx, cy, scale, flame=False):
    """Side-view tanker silhouette centred at (cx, cy)."""
    L = int(150 * scale)
    hull_y = cy + int(16 * scale)
    d.polygon([(cx - L // 2, cy), (cx + L // 2, cy), (cx + L // 2 - int(14 * scale), hull_y),
               (cx - L // 2 + int(8 * scale), hull_y)], fill=(16, 24, 40))
    d.rectangle([cx - L // 2, hull_y, cx + L // 2 - int(14 * scale), hull_y + 3],
                fill=(120, 52, 40))
    # container stacks
    cols = [(52, 84, 96), (140, 84, 52), (70, 104, 84), (96, 74, 110)]
    bx = cx - L // 2 + int(16 * scale)
    for i, c in enumerate(cols):
        bw = int(22 * scale)
        d.rectangle([bx + i * (bw + 2), cy - int(13 * scale), bx + (i + 1) * (bw + 2) - 2, cy],
                    fill=c)
    # superstructure aft
    sx = cx + L // 2 - int(30 * scale)
    d.rectangle([sx, cy - int(22 * scale), sx + int(14 * scale), cy], fill=(196, 198, 204))
    d.rectangle([sx + int(3 * scale), cy - int(28 * scale), sx + int(8 * scale), cy - int(22 * scale)],
                fill=(150, 154, 164))
    if flame:
        fx, fy = cx - int(6 * scale), cy - int(14 * scale)
        d.polygon([(fx - 12, fy), (fx, fy - 34), (fx + 12, fy)], fill=(232, 116, 36))
        d.polygon([(fx - 6, fy), (fx, fy - 20), (fx + 6, fy)], fill=(246, 190, 60))
        for dx, dy, r, c in ((10, -44, 7, (70, 76, 90)), (20, -54, 10, (86, 92, 104)),
                             (32, -64, 13, (100, 106, 118))):   # smoke drift
            d.ellipse([fx + dx - r, fy + dy - r, fx + dx + r, fy + dy + r], fill=c)

tanker(238, 282, 0.92)
tanker(498, 272, 1.0, flame=True)
tanker(716, 290, 0.8)
# dashed gold shipping lane through the strait
for x in range(HX0 + 40, HX1 - 30, 36):
    d.line([x, 308, x + 18, 308], fill=(150, 122, 58), width=2)
d.rectangle([HX0, HY0, HX1, SCENE_BOT], outline=EDGE, width=2)

# hero text band
d.rectangle([HX0, SCENE_BOT, HX1, HY1], fill=PANEL_HI)
d.line([HX0, SCENE_BOT, HX1, SCENE_BOT], fill=GOLD, width=3)
d.text((HX0 + 18, SCENE_BOT + 10), "MIDDLE EAST · THE BIG STORY",
       font=font(SANS_B, 13), fill=GOLD, anchor="la")
f_hero = fit_font(d, "TANKERS HIT IN THE STRAIT OF HORMUZ", SERIF_B, 36, CW - 190)
d.text((HX0 + 18, SCENE_BOT + 30), "TANKERS HIT IN THE STRAIT OF HORMUZ",
       font=f_hero, fill=CREAM, anchor="la")
hero_body = ("Iran strikes US targets in Bahrain for the third time in five days; at least "
             "3 oil tankers are hit or damaged in the strait, one set ablaze. US jets "
             "answer, hitting IRGC missile-launcher sites on Qeshm Island.")
for i, line in enumerate(wrap(d, hero_body, font(SANS, 15), CW - 190)):
    d.text((HX0 + 18, SCENE_BOT + 74 + i * 19), line, font=font(SANS, 15),
           fill=(214, 220, 232), anchor="la")
d.text((HX1 - 164, SCENE_BOT + 10), "(AP · Reuters · UKMTO)",
       font=font(SANS_O, 11), fill=MUTED, anchor="ra")
# hero number chip, right of the text band
chip_number(d, HX1 - 148, SCENE_BOT + 26, 128, 62, "3", size=30)
d.text((HX1 - 84, SCENE_BOT + 96), "tankers hit", font=font(SANS_B, 11),
       fill=CREAM, anchor="ma")

# ---------------------------------------------------------------- numbers strip
SY0, SY1 = 444, 502
d.rectangle([MARGIN, SY0, W - MARGIN, SY1], fill=PANEL, outline=EDGE)
NUMBERS = [
    ("3", "tankers hit in Hormuz"),
    ("0", "fossil-fuel mentions"),
    ("39", "missing in the factory fire"),
    ("7,641", "Taiwan stocks plunge, points"),
    ("100,000", "young Europeans a year"),
    ("5,700", "Ebola deaths in DR Congo"),
]
cell_w = CW / 6
for i, (num, lab) in enumerate(NUMBERS):
    cx = MARGIN + cell_w * (i + 0.5)
    if i:
        d.line([MARGIN + cell_w * i, SY0 + 8, MARGIN + cell_w * i, SY1 - 8],
               fill=EDGE, width=1)
    d.text((cx, SY0 + 5), num, font=font(SANS_B, 23), fill=GOLD, anchor="ma")
    for j, line in enumerate(wrap(d, lab, font(SANS, 10), cell_w - 12)):
        d.text((cx, SY0 + 34 + j * 12), line, font=font(SANS, 10), fill=CREAM, anchor="ma")

# ---------------------------------------------------------------- card scenes
def scene_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 44))
    d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 16], fill=(96, 66, 40))  # table
    for i in range(4):                                                        # chairs
        cx = x + 14 + i * 22
        d.rectangle([cx, y + h - 38, cx + 13, y + h - 27], fill=(40, 58, 92))
    px, py = x + w // 2 - 13, y + 12                                          # document
    d.rectangle([px, py, px + 26, py + 34], fill=(232, 228, 216))
    d.line([px + 3, py + 3, px + 23, py + 31], fill=RED, width=3)
    d.line([px + 23, py + 3, px + 3, py + 31], fill=RED, width=3)

def scene_fire(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 22, 20))
    d.rectangle([x + 10, y + 44, x + 74, y + h - 8], fill=(24, 20, 26))       # factory
    for i in range(4):                                                        # sawtooth roof
        bx = x + 10 + i * 16
        d.polygon([(bx, y + 44), (bx + 8, y + 32), (bx + 16, y + 44)], fill=(24, 20, 26))
    d.rectangle([x + 78, y + 22, x + 88, y + h - 8], fill=(24, 20, 26))       # chimney
    for fx, fh in ((26, 30), (44, 40), (62, 26)):                             # flames
        d.polygon([(x + fx - 8, y + 46), (x + fx, y + 46 - fh), (x + fx + 8, y + 46)],
                  fill=(232, 116, 36))
        d.polygon([(x + fx - 4, y + 46), (x + fx, y + 46 - fh // 2), (x + fx + 4, y + 46)],
                  fill=(246, 190, 60))
    d.ellipse([x + 66, y + 4, x + 96, y + 22], fill=(96, 92, 96))             # smoke

def scene_chart(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 26, 44))
    for gy in range(y + 16, y + h - 10, 18):
        d.line([x + 6, gy, x + w - 6, gy], fill=(30, 46, 70), width=1)
    pts = [(x + 10, y + 22), (x + 30, y + 30), (x + 48, y + 44), (x + 66, y + 58),
           (x + 84, y + 78)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.polygon([(x + 84, y + 78), (x + 76, y + 76), (x + 83, y + 68)], fill=RED)
    d.rectangle([x + 10, y + h - 20, x + 22, y + h - 8], fill=(52, 140, 84))
    d.rectangle([x + 28, y + h - 26, x + 40, y + h - 8], fill=(52, 140, 84))

def scene_flags(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 38, 66))
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(120, 128, 110), width=2)
    for px in (x + 24, x + 66):
        d.line([px, y + 12, px, y + h - 14], fill=(180, 184, 192), width=2)
    fx, fy, fw, fh = x + 24, y + 12, 30, 19                                   # Union Jack, simplified
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(36, 54, 120))
    d.line([fx, fy, fx + fw, fy + fh], fill=(230, 230, 230), width=3)
    d.line([fx + fw, fy, fx, fy + fh], fill=(230, 230, 230), width=3)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(230, 230, 230), width=5)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(230, 230, 230), width=5)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(196, 40, 48), width=3)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(196, 40, 48), width=3)
    fx2 = x + 66                                                              # EU flag
    d.rectangle([fx2, fy, fx2 + fw, fy + fh], fill=(36, 54, 140))
    import math
    for k in range(8):
        a = 2 * math.pi * k / 8
        gx, gy = fx2 + fw // 2 + 7 * math.cos(a), fy + fh // 2 + 7 * math.sin(a)
        d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=GOLD)
    hx = x + w // 2                                                           # traveller
    d.ellipse([hx - 4, y + h - 40, hx + 4, y + h - 32], fill=CREAM)
    d.line([hx, y + h - 32, hx, y + h - 18], fill=CREAM, width=3)
    d.rectangle([hx + 4, y + h - 34, hx + 11, y + h - 22], fill=GOLD)

def scene_f1(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 24))
    for i, c in enumerate([(214, 84, 150), (84, 150, 214), (214, 190, 84)]):   # strip lights
        d.rectangle([x + 10 + i * 30, y + 10, x + 22 + i * 30, y + 15], fill=c)
    cy = y + h - 42
    d.polygon([(x + 4, cy + 18), (x + 24, cy + 4), (x + 60, cy - 2), (x + 88, cy + 6),
               (x + 98, cy + 18)], fill=(168, 32, 40))                        # car body
    d.rectangle([x + 2, cy - 8, x + 13, cy + 8], fill=(120, 22, 30))          # rear wing
    d.line([x + 86, cy + 2, x + 100, cy - 5], fill=(120, 22, 30), width=3)    # front wing strut
    for wx in (x + 22, x + 78):
        d.ellipse([wx - 10, cy + 12, wx + 10, cy + 32], fill=(8, 8, 10))
        d.ellipse([wx - 3, cy + 19, wx + 3, cy + 25], fill=(140, 144, 152))
    d.line([x + 4, cy + 34, x + w - 4, cy + 34], fill=(90, 96, 110), width=2)

def scene_hoop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 26, 20))
    d.line([x + 4, y + h - 12, x + w - 4, y + h - 12], fill=(120, 90, 60), width=2)
    d.rectangle([x + 58, y + 12, x + 92, y + 34], outline=(230, 230, 230), width=2)
    d.rectangle([x + 68, y + 22, x + 82, y + 34], outline=(230, 230, 230), width=1)
    d.line([x + 70, y + 36, x + 80, y + 36], fill=(232, 116, 36), width=3)    # rim
    px = x + 40                                                               # tall player
    d.ellipse([px - 5, y + 26, px + 5, y + 36], fill=CREAM)
    d.line([px, y + 36, px, y + 66], fill=CREAM, width=4)
    d.line([px, y + 42, px + 26, y + 30], fill=CREAM, width=3)                # arm up
    d.line([px, y + 66, px - 8, y + h - 14], fill=CREAM, width=3)
    d.line([px, y + 66, px + 12, y + h - 20], fill=CREAM, width=3)
    d.ellipse([px + 24, y + 18, px + 36, y + 30], fill=(232, 116, 36))        # ball

def scene_aid(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 50, 44))
    d.rectangle([x + 26, y + 30, x + 76, y + 66], fill=(228, 228, 224))       # cargo box
    d.rectangle([x + 76, y + 44, x + 94, y + 66], fill=(200, 202, 198))       # cab
    d.rectangle([x + 80, y + 48, x + 90, y + 56], fill=(70, 90, 110))
    for wx in (x + 38, x + 82):
        d.ellipse([wx - 7, y + 62, wx + 7, y + 76], fill=(16, 16, 18))
    d.rectangle([x + 46, y + 38, x + 56, y + 58], fill=RED)                   # cross on box
    d.rectangle([x + 41, y + 43, x + 61, y + 53], fill=RED)
    for bx, by in ((x + 6, y + 52), (x + 6, y + 70)):                         # aid crates
        d.rectangle([bx, by, bx + 14, by + 12], fill=(176, 148, 104))
        d.line([bx + 7, by + 2, bx + 7, by + 10], fill=RED, width=2)
        d.line([bx + 3, by + 6, bx + 11, by + 6], fill=RED, width=2)

def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 30))
    af = [(38, 8), (52, 6), (60, 14), (58, 24), (66, 32), (62, 44), (54, 52),
          (50, 68), (44, 84), (38, 92), (32, 80), (30, 62), (24, 52), (26, 40),
          (20, 30), (26, 18), (32, 12)]                                      # Africa silhouette
    d.polygon([(x + px, y + py) for px, py in af], fill=(178, 146, 62))
    d.ellipse([x + 66, y + 8, x + 90, y + 32], fill=(236, 236, 232))          # badge
    d.rectangle([x + 75, y + 13, x + 81, y + 27], fill=RED)
    d.rectangle([x + 71, y + 17, x + 85, y + 23], fill=RED)

def scene_nfl(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 36, 24))
    d.arc([x + 2, y + 26, x + w - 2, y + 96], start=180, end=360, fill=(200, 204, 210), width=3)
    d.line([x + 8, y + 60, x + w - 8, y + 60], fill=(200, 204, 210), width=2)
    gx = x + w // 2                                                           # goalpost
    d.line([gx, y + 96, gx, y + 62], fill=GOLD, width=3)
    d.line([gx - 12, y + 62, gx + 12, y + 62], fill=GOLD, width=3)
    d.line([gx - 12, y + 62, gx - 12, y + 46], fill=GOLD, width=3)
    d.line([gx + 12, y + 62, gx + 12, y + 46], fill=GOLD, width=3)
    d.ellipse([x + 16, y + 78, x + 34, y + 90], fill=(140, 84, 44))           # ball
    d.line([x + 21, y + 84, x + 29, y + 84], fill=(240, 240, 240), width=2)

# ---------------------------------------------------------------- cards
CARDS = [
    ("GLOBAL", "COP31 COLLAPSE: NO DEAL",
     "The longest climate summit ever ends with nothing adopted.",
     "Reuters · WRI", "0", scene_cop31),
    ("ASIA-PACIFIC", "INDONESIA FACTORY FIRE",
     "3 dead at the Serang candy plant; rescue teams still search the ruins for the missing.",
     "Reuters · AP · AFP", "39", scene_fire),
    ("ASIA-PACIFIC", "TAIWAN STOCKS PLUNGE",
     "Stocks fell 7,641 points last week; the state fund steps in and short-selling is curbed.",
     "wires", "7,641", scene_chart),
    ("EUROPE", "UK–EU YOUTH DEAL GOES AHEAD",
     "Post-Brexit deal confirmed: Britain opens to 100,000 young Europeans a year.",
     "wires · BBC", "100,000", scene_flags),
    ("NORTH AMERICA", "VERSTAPPEN WINS LAS VEGAS GP",
     "Red Bull wins a thriller with 34 lead changes; the two Ferraris collide again.",
     "BBC", "34", scene_f1),
    ("NORTH AMERICA", "WEMBANYAMA SCORES 50",
     "San Antonio beat New Orleans 114–91 behind their star's 50-point night.",
     "BBC", "50", scene_hoop),
    ("MIDDLE EAST", "GAZA AID WORKERS KILLED",
     "Israeli troops kill 3 Palestinians handing out supplies, witnesses say.",
     "wires", "3", scene_aid),
    ("AFRICA", "EBOLA TOLL PASSES 5,700",
     "The death toll in DR Congo's Ebola outbreak passes 5,700.",
     "wires", "5,700", scene_ebola),
    ("LATIN AMERICA", "NFL IN MEXICO CITY TONIGHT",
     "49ers host the Vikings in Mexico's first Sunday Night Football, 7,352 ft up.",
     "NFL · wires", "7,352", scene_nfl),
]
GRID_Y = 514
CARD_W, CARD_H, GAP = 318, 114, 11
for idx, (region, head, body, src, num, scene) in enumerate(CARDS):
    r, c = divmod(idx, 3)
    x = MARGIN + c * (CARD_W + GAP)
    y = GRID_Y + r * (CARD_H + GAP)
    d.rectangle([x, y, x + CARD_W, y + CARD_H], fill=PANEL, outline=EDGE)
    scene(x + 1, y + 1, 100, CARD_H - 2)
    d.line([x + 101, y, x + 101, y + CARD_H], fill=EDGE, width=1)
    chip_number(d, x + 8, y + CARD_H - 27, 56, 20, num, size=13)
    tx = x + 112
    d.text((tx, y + 8), region, font=font(SANS_B, 10), fill=GOLD, anchor="la")
    d.text((x + CARD_W - 8, y + 9), f"({src})", font=font(SANS_O, 9),
           fill=MUTED, anchor="ra")
    hsize = 17
    while hsize > 14 and len(wrap(d, head, font(SANS_B, hsize), CARD_W - 122)) > 2:
        hsize -= 1
    f_head = font(SANS_B, hsize)
    for i, line in enumerate(wrap(d, head, f_head, CARD_W - 122)):
        d.text((tx, y + 23 + i * 20), line, font=f_head, fill=CREAM, anchor="la")
    for i, line in enumerate(wrap(d, body, font(SANS, 11), CARD_W - 122)):
        d.text((tx, y + 66 + i * 13), line, font=font(SANS, 11),
               fill=(205, 212, 226), anchor="la")

# ---------------------------------------------------------------- region chips
CHIP_Y = 890
labels = ["MIDDLE EAST 2", "ASIA-PACIFIC 2", "NORTH AMERICA 2", "EUROPE 1",
          "AFRICA 1", "LATIN AMERICA 1", "GLOBAL 1"]
f_chip = font(SANS_B, 12)
widths = [tw(d, s, f_chip) + 22 for s in labels]
total = sum(widths) + 8 * (len(labels) - 1)
cx = (W - total) / 2
for s, wch in zip(labels, widths):
    d.rounded_rectangle([cx, CHIP_Y, cx + wch, CHIP_Y + 26], radius=6,
                        fill=(24, 40, 70), outline=GOLD)
    d.text((cx + wch / 2, CHIP_Y + 13), s, font=f_chip, fill=CREAM, anchor="mm")
    cx += wch + 8

# ---------------------------------------------------------------- date check + footer
DY = 928
d.rectangle([MARGIN, DY, W - MARGIN, DY + 56], outline=RED, width=2)
d.text((MARGIN + 12, DY + 7), "DATE CHECK — WHAT WE LEFT OUT",
       font=font(SANS_B, 12), fill=RED, anchor="la")
d.text((W - MARGIN - 12, DY + 7), VERIFIED_STAMP, font=font(SANS_B, 11),
       fill=RED, anchor="ra")
dc_lines = [
    "×  “El Chapo Isidro” arrested — captured Fri 20 Nov, announced Sat 21 Nov (Reuters/AP). Not 22 Nov.",
    "×  Trump–Xi–Putin Shenzhen summit — held Thu 19 Nov at APEC (WSJ, Le Monde). Not 22 Nov.",
]
for i, line in enumerate(dc_lines):
    d.text((MARGIN + 12, DY + 26 + i * 15), line, font=font(SANS, 11),
           fill=(226, 214, 200), anchor="la")
d.text((W / 2, 994), "All 10 stories happened or were first reported on Sunday 22 November 2026"
       "  ·  Sources: Reuters, AP, BBC, AFP, UKMTO and wires",
       font=font(SANS, 11), fill=MUTED, anchor="ma")

img.save("entry.png")
print("saved entry.png")
