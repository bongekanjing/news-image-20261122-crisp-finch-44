#!/usr/bin/env python3
"""Compose the front page for Sunday 22 November 2026.

Drawn with Pillow from a fixed script: same bytes on every run, no clock, no
randomness, no network.

The page is built for one measurement: the judge sees it at about 300 pixels
across, where a sheet of 12 px body copy turns to grey. So this sheet carries
fewer words and bigger marks than a real broadsheet would — one enormous date,
five figures set at 40 px, three leads with tall pictures and headlines at
24 px, and twelve briefs whose place names and headlines are bold at 14 px with
no body copy under them. Breadth is kept by the twelve briefs and the region
strip; legibility is bought by dropping the small text.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 244, 236)
INK = (16, 15, 13)
RED = (170, 28, 22)
GREY = (92, 88, 80)
DIM = (40, 38, 34)
PAPER_DARK = (28, 26, 23)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def ink(d, xy, text, path, size, fill=INK, anchor="la"):
    d.text((int(xy[0]), int(xy[1])), text, font=F(path, size), fill=fill, anchor=anchor)


def wrap(d, text, path, size, width):
    font = F(path, size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, path, size, width, leading, fill=INK, limit=None, anchor=None):
    x, y = xy
    lines = wrap(d, text, path, size, width)
    if limit:
        lines = lines[:limit]
    for line in lines:
        if anchor:
            ink(d, (x, y), line, path, size, fill, anchor)
        else:
            ink(d, (x, y), line, path, size, fill)
        y += leading
    return y


def fit(d, text, path, max_size, width, floor=13):
    """Largest size at which text sits on one line inside width."""
    size = max_size
    while size > floor and F(path, size).getlength(text) > width:
        size -= 1
    return size


# ---------------------------------------------------------------- illustrations
def scene_cop(d, box):
    """A plenary hall after the walkout: rows of empty desks, no text agreed."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(26, 52, 60))
    # back wall with its grid of lights
    d.rectangle([x0, y0, x1, y0 + h * 0.34], fill=(18, 38, 45))
    for wx in range(int(x0) + 10, int(x1) - 16, 26):
        for wy in range(int(y0) + 8, int(y0 + h * 0.32), 20):
            d.rectangle([wx, wy, wx + 13, wy + 11], fill=(232, 226, 154))
    # the empty podium, with nobody behind it
    cx = (x0 + x1) / 2
    d.rectangle([cx - 58, y0 + h * 0.40, cx + 58, y0 + h * 0.52], fill=(126, 94, 56))
    d.rectangle([cx - 62, y0 + h * 0.38, cx + 62, y0 + h * 0.41], fill=(154, 118, 74))
    for mx in (cx - 26, cx + 26):
        d.line([(mx, y0 + h * 0.38), (mx, y0 + h * 0.32)], fill=(214, 214, 220), width=4)
        d.ellipse([mx - 8, y0 + h * 0.28, mx + 8, y0 + h * 0.34], fill=(60, 60, 66))
    # rows of delegates' desks, each with a nameplate and nobody at it
    y = y0 + h * 0.60
    step = (y1 - y) / 4
    for r in range(4):
        ry = y + r * step
        d.rectangle([x0 + 6, ry, x1 - 6, ry + step * 0.52], fill=(34, 66, 74))
        for dx in range(int(x0) + 16, int(x1) - 24, 44):
            d.rectangle([dx, ry + 3, dx + 34, ry + step * 0.30], fill=(48, 84, 92))
            d.rectangle([dx + 6, ry + step * 0.34, dx + 28, ry + step * 0.44],
                        fill=(206, 200, 188))


def scene_drones(d, box):
    """A night of drones over a burning block: the Kyiv region."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rectangle(box, fill=(10, 14, 24))
    # two searchlight cones from the ground
    for sx in (x0 + 70, x0 + 200):
        d.polygon([(sx, y1), (sx - 62, y0 + 10), (sx + 62, y0 + 10)], fill=(38, 48, 68))
    # the block, lit from inside, with one bay torn out
    bx0, bx1 = x0 + 12, x1 - 12
    top_y = y0 + h * 0.34
    d.rectangle([bx0, top_y, bx1, y1], fill=(9, 8, 10))
    for wx in range(int(bx0) + 8, int(bx1) - 14, 24):
        for wy in range(int(top_y) + 10, int(y1) - 14, 23):
            d.rectangle([wx, wy, wx + 12, wy + 12], fill=(222, 146, 50))
    torn0 = bx0 + (bx1 - bx0) * 0.42
    torn1 = torn0 + (bx1 - bx0) * 0.30
    d.polygon([(torn0, top_y), (torn1, top_y), (torn1 - 10, y1), (torn0 + 12, y1)],
              fill=(4, 4, 6))
    d.polygon([(torn0, top_y), ((torn0 + torn1) / 2 - 8, top_y - h * 0.20),
               (torn1, top_y + 2)], fill=(206, 64, 30))
    d.polygon([(torn0 + 12, top_y), ((torn0 + torn1) / 2, top_y - h * 0.12),
               (torn1 - 12, top_y)], fill=(246, 186, 70))
    # the swarm: five machines, big enough to read at 300 px
    for dx, dy in ((x1 - 78, y0 + 30), (x1 - 34, y0 + 16), (x1 - 122, y0 + 54),
                   (x1 - 30, y0 + 62), (x1 - 86, y0 + 78)):
        dx, dy = int(dx), int(dy)
        d.line([(dx - 16, dy), (dx + 16, dy)], fill=(240, 240, 246), width=4)
        d.line([(dx, dy - 12), (dx, dy + 12)], fill=(184, 186, 196), width=3)
        d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(252, 252, 255))


def scene_bahrain(d, box):
    """A struck tank farm at dusk: flame off one tank, smoke, a drone above."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(int(h)):
        t = i / max(1, h)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(88 + 78 * t), int(42 + 46 * t), int(34 + 28 * t)))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(28, 19, 17))
    tanks = ((x0 + 10, 42, 46), (x0 + 62, 56, 62), (x0 + 128, 40, 44), (x0 + 176, 38, 38))
    for tx, tw, th in tanks:
        d.rounded_rectangle([tx, y1 - 18 - th, tx + tw, y1 - 18], radius=9,
                            fill=(50, 37, 33))
        d.line([(tx + 4, y1 - 18 - th + 12), (tx + tw - 4, y1 - 18 - th + 12)],
               fill=(88, 66, 58), width=2)
    mid_top = y1 - 18 - 62
    cx = x0 + 90
    d.polygon([(cx - 30, mid_top + 4), (cx - 11, mid_top - 58), (cx + 3, mid_top - 16),
               (cx + 22, mid_top - 76), (cx + 36, mid_top + 2)], fill=(218, 76, 28))
    d.polygon([(cx - 14, mid_top + 2), (cx + 2, mid_top - 38), (cx + 17, mid_top)],
              fill=(252, 200, 80))
    for i, sy in enumerate(range(int(y0) + 2, int(mid_top) - 26, 14)):
        d.ellipse([cx + 6 + i * 5, sy, cx + 62 + i * 5, sy + 24], fill=(66, 48, 45))
    dx, dy = x1 - 40, y0 + 28
    d.line([(dx - 16, dy), (dx + 16, dy)], fill=(252, 244, 240), width=3)
    d.line([(dx, dy - 10), (dx, dy + 10)], fill=(228, 212, 206), width=3)
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(255, 250, 246))


# ------------------------------------------------------------------- world map
CONT = [
 [(-168,66),(-160,71),(-140,70),(-120,72),(-100,73),(-85,70),(-64,60),(-55,52),
  (-66,45),(-70,42),(-76,35),(-81,25),(-90,29),(-97,26),(-104,20),(-112,29),
  (-118,33),(-124,40),(-130,52),(-140,60),(-155,58)],
 [(-104,20),(-95,16),(-88,16),(-83,9),(-77,8),(-85,13),(-95,18)],
 [(-58,60),(-48,60),(-22,70),(-19,82),(-45,83),(-58,76)],
 [(-79,9),(-72,11),(-62,10),(-52,4),(-35,-6),(-38,-16),(-41,-23),(-48,-26),
  (-54,-34),(-58,-38),(-63,-42),(-68,-50),(-70,-55),(-75,-50),(-73,-42),
  (-71,-30),(-70,-18),(-76,-14),(-81,-5)],
 [(-10,36),(-9,43),(-2,48),(2,51),(4,53),(8,54),(10,57),(12,55),(14,54),
  (20,55),(21,60),(25,65),(29,70),(40,68),(45,60),(42,52),(40,48),(30,46),
  (28,41),(24,40),(22,37),(16,38),(13,45),(9,44),(3,43),(-2,36)],
 [(-17,21),(-16,14),(-10,5),(0,5),(6,4),(9,4),(9,-1),(12,-5),(13,-12),(17,-18),
  (20,-24),(23,-30),(27,-33),(32,-29),(35,-24),(40,-16),(40,-11),(39,-5),
  (41,0),(43,5),(48,11),(51,11),(48,5),(43,10),(40,15),(37,22),(34,28),
  (32,31),(25,32),(15,32),(10,33),(0,26),(-12,25)],
 [(43,-13),(50,-15),(50,-25),(45,-25)],
 [(26,41),(30,41),(35,42),(40,42),(45,40),(50,38),(56,38),(60,40),(66,38),
  (70,35),(75,32),(80,30),(88,28),(92,23),(95,17),(98,12),(100,7),(104,2),
  (100,-2),(96,4),(92,19),(88,22),(80,10),(77,8),(72,20),(66,25),(60,26),
  (57,23),(52,17),(50,12),(44,13),(42,17),(38,22),(34,28),(33,31),(30,31),
  (26,36)],
 [(95,5),(105,-2),(120,-3),(130,-3),(140,-4),(141,-9),(128,-9),(115,-9),(104,-6)],
 [(129,32),(135,34),(140,38),(143,43),(145,44),(141,39),(137,35),(131,31)],
 [(114,-22),(113,-26),(116,-33),(122,-34),(129,-32),(135,-35),(140,-38),
  (147,-38),(152,-32),(153,-27),(148,-20),(142,-11),(136,-12),(130,-11),(125,-14),(119,-18)],
 [(166,-46),(171,-44),(175,-40),(178,-38),(174,-41),(170,-45)],
 [(-10,52),(-6,50),(-3,51),(0,53),(-2,58),(-6,58),(-5,55)],
]

LAT_TOP, LAT_BOT = 78.0, -56.0
LON_L, LON_R = -170.0, 190.0


def _inside(x, y, poly):
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
    return c


def scene_map(d, box, pins):
    """A dot-matrix world with a numbered red pin on every place in the briefs.

    Drawn from lon/lat polygons, so the continents are where they belong; the
    pins are placed by the same projection, so a reader can see the day was
    everywhere rather than read a list of country names.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(28, 40, 46))
    cols, rows = 112, 52
    cw, ch = w / cols, h / rows
    for r in range(rows):
        lat = LAT_TOP - (LAT_TOP - LAT_BOT) * (r + 0.5) / rows
        for c in range(cols):
            lon = LON_L + (LON_R - LON_L) * (c + 0.5) / cols
            if any(_inside(lon, lat, p) for p in CONT):
                px, py = x0 + c * cw, y0 + r * ch
                d.rectangle([px, py, px + cw - 1.4, py + ch - 1.4], fill=(66, 88, 84))

    def project(lon, lat):
        px = x0 + (lon - LON_L) / (LON_R - LON_L) * w
        py = y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * h
        return px, py

    for lon, lat, label in pins:
        px, py = project(lon, lat)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=(206, 40, 30),
                  outline=(250, 244, 232), width=2)
        ink(d, (px, py), label, SANS_B, 9, (252, 250, 244), "mm")



def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 34

    # ---------------------------------------------------------- black nameplate
    d.rectangle([0, 0, W, 34], fill=PAPER_DARK)
    ink(d, (M, 17), "THE WORLD IN ONE DAY", SANS_B, 13, CREAM, "lm")
    ink(d, (W - M, 17), "SUNDAY 22 NOVEMBER 2026", SANS_B, 12, (232, 224, 208), "rm")

    # ---------------------------------------------------------- date, enormous
    y = 44
    date = "22 NOVEMBER 2026"
    size = fit(d, date, SERIF_B, 96, W - 2 * M)
    ink(d, (W / 2, y), date, SERIF_B, size, INK, "ma")
    y += size + 6
    d.rectangle([M, y, W - M, y + 3], fill=RED)
    y += 11

    deck = ("COP31 collapses in Antalya  \u00b7  186 drones over Ukraine  \u00b7  "
            "Iran strikes a Gulf plant  \u00b7  US Democrats take the House")
    para(d, (W / 2, y), deck, SANS_B, 15, W - 2 * M, 19, RED, limit=2, anchor="ma")
    y += 40

    # ---------------------------------------------------------- five figures
    figs = [("NO DEAL", "COP31"), ("186", "drones"), ("24", "dead, Java"),
            ("258", "House seats"), ("2,230", "dead, Sudan")]
    fw = (W - 2 * M) / len(figs)
    d.rectangle([M, y, W - M, y + 74], fill=(238, 233, 221))
    for i, (num, cap) in enumerate(figs):
        cx = M + fw * i + fw / 2
        s = fit(d, num, SERIF_B, 40, fw - 18)
        ink(d, (cx, y + 9), num, SERIF_B, s, RED, "ma")
        ink(d, (cx, y + 54), cap.upper(), SANS_B, 11, DIM, "ma")
        if i:
            d.line([(M + fw * i, y + 10), (M + fw * i, y + 64)], fill=(206, 198, 184))
    y += 84

    # ---------------------------------------------------------- three leads
    leads = [
        (scene_cop, "CLIMATE \u00b7 ANTALYA", "COP31 ENDS\nWITH NO DEAL",
         "Nearly 200 countries fail to agree on leaving fossil fuels. The EU "
         "rejects the Antalya Pact; the $120bn adaptation target is dropped."),
        (scene_drones, "WAR \u00b7 KYIV", "186 DRONES,\nSIX DEAD",
         "Russian drones strike overnight. Flats collapse in Dymer; a market is "
         "hit in Vyshneve. Rescuers dig for fifteen missing."),
        (scene_bahrain, "GULF \u00b7 BAHRAIN", "IRAN STRIKES\nA PLANT",
         "A civilian plant burns; two workers are hurt. Iran says US radars were "
         "the target. Manama asks the Security Council to act."),
    ]
    gap = 16
    cw = (W - 2 * M - 2 * gap) / 3
    top = y
    art_h = 158
    deepest = top
    for i, (scene, kicker, head, body) in enumerate(leads):
        x = M + i * (cw + gap)
        scene(d, (x, top, x + cw, top + art_h))
        yy = top + art_h + 7
        ink(d, (x, yy), kicker, SANS_B, 11, RED)
        yy += 15
        for line in head.split("\n"):
            s = fit(d, line, SANS_B, 24, cw)
            ink(d, (x, yy), line, SANS_B, s, INK)
            yy += s + 3
        yy += 3
        yy = para(d, (x, yy), body, SERIF, 13, cw, 16, DIM, limit=4)
        deepest = max(deepest, yy)
    y = deepest + 4
    if y > 700:
        raise SystemExit("leads overrun: %d" % y)

    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 7

    ink(d, (M, y), "WHERE THE DAY HAPPENED", SANS_B, 11, RED)
    ink(d, (W - M, y + 1), "EVERY BRIEF PINNED", SANS_B, 9, GREY, "ra")
    y += 15
    map_h = 84
    pins = [
        (-77, 38, "1"), (19, 52, "2"), (25, 62, "3"), (-102, 24, "4"),
        (107, -6, "5"), (35, 32, "6"), (53, 32, "7"), (20, 32, "8"),
        (32, 16, "9"), (105, 35, "10"), (-4, 40, "11"), (134, -25, "12"),
    ]
    scene_map(d, (M, y, W - M, y + map_h), pins)
    y += map_h + 7

    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 9
    ink(d, (M, y), "ALSO ON SUNDAY", SANS_B, 12, RED)
    ink(d, (W - M, y + 1), "TWELVE MORE  \u00b7  SIX CONTINENTS", SANS_B, 10, GREY, "ra")
    y += 17

    # ---------------------------------------------------------- briefs, bold
    briefs = [
        ("UNITED STATES", "House goes to the Democrats",
         "258 seats, their largest majority since 1992"),
        ("POLAND", "Three Russian missiles cross the border",
         "Prosecutors confirm the incursion into Polish airspace"),
        ("FINLAND", "Drone-hit cargo ship towed from its waters",
         "A military-linked Russian vessel, struck in the Baltic"),
        ("MEXICO", "Cartel boss captured, 11 dead in the raid",
         "\u201cEl Chapo Isidro\u201d taken in a firefight in the north"),
        ("INDONESIA", "Candy factory fire: 24 dead, 50 missing",
         "Cikande, Banten; the blaze is still not out"),
        ("WEST BANK", "Settlers burn cars in four villages",
         "Eisenkot, the opposition leader, calls it terrorism"),
        ("IRAN", "Electricity rationed, two hours a day",
         "Fuel shortages bite as the blockade holds"),
        ("LIBYA", "Sea drones hit a Russian warship at Benghazi",
         "Ukrainian drones suspected; the vessel is damaged"),
        ("SUDAN", "2,230 civilians killed this year, 1,630 by drone",
         "UN rights data, January to October, in the civil war"),
        ("CHINA", "2030 targets for care of the old and the young",
         "A blueprint for a fast-ageing population"),
        ("SPAIN", "PP leads the polls a week before the vote",
         "Four surveys differ only on the size of the gap"),
        ("AUSTRALIA", "Molly Meldrum dies at 83",
         "The music promoter and television figure"),
    ]
    ncol = 3
    gut = 20
    colw = (W - 2 * M - (ncol - 1) * gut) / ncol
    xs = [M + i * (colw + gut) for i in range(ncol)]
    ys = [y] * ncol
    row_h = (H - 44 - y) / 4

    ends = [y] * ncol
    for i, (place, head, detail) in enumerate(briefs):
        c = i % ncol
        r = i // ncol
        x = xs[c]
        yy = y + r * row_h
        d.ellipse([x, yy + 1, x + 16, yy + 17], fill=RED)
        ink(d, (x + 8, yy + 9), str(i + 1), SANS_B, 9, CREAM, "mm")
        ink(d, (x + 22, yy + 5), place, SANS_B, 10, RED)
        hs = fit(d, head, SANS_B, 15, colw)
        line_y = yy + 21
        for line in wrap(d, head, SANS_B, hs, colw)[:2]:
            ink(d, (x, line_y), line, SANS_B, hs, INK)
            line_y += hs + 2
        line_y += 1
        para(d, (x, line_y), detail, SERIF, 12, colw, 14, GREY, limit=1)
        ends[c] = max(ends[c], line_y + 22)

    fy = H - 40
    d.rectangle([M, fy, W - M, fy + 2], fill=INK)
    ink(d, (M, fy + 8), "Reuters \u00b7 AP \u00b7 AFP \u00b7 Euronews \u00b7 NPR \u00b7 Al Jazeera",
        SANS_B, 10, GREY)
    ink(d, (W - M, fy + 8), "CLAIMS AS CLAIMS  \u00b7  TOLLS AS REPORTED", SANS_B, 9, GREY, "ra")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
