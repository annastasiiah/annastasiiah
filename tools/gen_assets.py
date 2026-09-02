#!/usr/bin/env python3
"""Regenerate the pixel-art SVGs used by the profile README.

    python3 tools/gen_assets.py            # writes into ../assets
    python3 tools/gen_assets.py <outdir>

Existing hand-drawn pieces (hero, divider, footer, arsenal, featured-dnd,
sec-about, sec-arsenal, sec-featured, link-linkedin/github/email) are left
alone; this script only builds the ones added for the portfolio layout.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixart import *                                    # noqa: E402
from sprites import mage, python_icon                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, '..', 'assets'))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- sprites
CHEST = ["...GGGGGGGG...",
         "..GPPPPPPPPG..",
         ".GPPPPPPPPPPG.",
         "GPPPPPGGPPPPPG",
         "GGGGGGGGGGGGGG",
         "GPPPPGGGGPPPPG",
         "GPPPPGDDGPPPPG",
         "GPPPPGGGGPPPPG",
         "GPPPPPPPPPPPPG",
         "GGGGGGGGGGGGGG"]

CHART = ["..........GG..",
         "......LL..GG..",
         "......LL..GG..",
         "..LL..LL..GG..",
         "..LL..LL..GG..",
         "..LL..LL..GG..",
         "..LL..LL..GG..",
         "..LL..LL..GG..",
         "GGGGGGGGGGGGGG"]

MAIL = ["GGGGGGGGGGGGGG",
        "GWW........WWG",
        "G.WW......WW.G",
        "G..WW....WW..G",
        "G...WW..WW...G",
        "G....WWWW....G",
        "G.....WW.....G",
        "G............G",
        "GGGGGGGGGGGGGG"]

SPR = {'G': GOLD, 'P': PURPLE, 'D': BOX_FILL, 'L': LILAC, 'W': PALE}

STEAM = ["......###...",
         "....##...##.",
         "....#.....#.",
         "...#..###..#",
         "...#..###..#",
         "...#..###..#",
         "....##....#.",
         ".#####...##.",
         "#..##.###...",
         "#...#.......",
         "#...#.......",
         ".###........"]

JOYSTICK = ["...####...",
            "..#....#..",
            ".#......#.",
            ".#......#.",
            "..#....#..",
            "...####...",
            "....##....",
            "....##....",
            "....##....",
            "....##....",
            "..######..",
            ".########.",
            "##########",
            "##########"]

SHIP_ART = [".......S.......",
            "......S.S......",
            "......S.S......",
            ".....S...S.....",
            ".....S...S.....",
            "....S.....S....",
            "....S.....S....",
            "...S.......S...",
            "...S.......S...",
            "..S....S....S..",
            "..S..SS.SS..S..",
            "..S.S.....S.S..",
            "..SS.......SS..",
            "...............",
            "......F.F......",
            ".......F......."]

ROCK = [".......",
        "..RRR..",
        ".R...R.",
        "R.....R",
        "R.....R",
        ".R...R.",
        "..RRR.."]

CHIP_BORDER, CHIP_CORNER = '#3a4488', '#0b0f28'
CHIP_TOP, CHIP_BOT = '#2c335d', '#1c2451'


# ---------------------------------------------------------------- section headers
def build_headers():
    for fn, title, spr, at, seed in [
        ('sec-portfolio.svg', 'Portfolio',    CHEST, (4, 6), 7),
        ('sec-stats.svg',     'GitHub Stats', CHART, (4, 7), 11),
        ('sec-connect.svg',   'Connect',      MAIL,  (4, 7), 23),
    ]:
        cv, _, _ = header(title, spr, at, seed, sprite_colors=SPR)
        cv.save(os.path.join(OUT, fn), title)
        print('wrote', fn)


# ---------------------------------------------------------------- link button
def build_steam():
    text = 'Steam'
    w = 29 + 6 * len(text)
    cv = Canvas(w, 24)
    for i, col in enumerate(BTN_BG):
        cv.hline(1, 2 + i, w - 2, col)
    cv.hline(1, 1, w - 2, FRAME_BLUE)
    cv.hline(1, 22, w - 2, FRAME_BLUE)
    cv.vline(0, 2, 20, FRAME_BLUE)
    cv.vline(w - 1, 2, 20, FRAME_BLUE)
    for cx, cy in ((0, 1), (w - 1, 1), (0, 22), (w - 1, 22)):
        cv.set(cx, cy, BTN_CORNER)
    cv.blit(5, 5, STEAM, {'#': PERI})
    cv.text(22, 8, text, INK)
    cv.save(os.path.join(OUT, 'link-steam.svg'), 'Steam')
    print('wrote link-steam.svg')


# ---------------------------------------------------------------- about card
def framed_box(cv, x, y, w, h):
    cv.rect(x, y, w, h, BOX_FILL)
    cv.border(x, y, w, h, GOLD_DARK)
    m = w // 3
    cv.hline(x + (w - m) // 2, y, m, GOLD_MID)
    cv.hline(x + (w - m) // 2, y + h - 1, m, GOLD_MID)
    for cx, cy in ((x, y), (x + w - 1, y), (x, y + h - 1), (x + w - 1, y + h - 1)):
        cv.set(cx, cy, GOLD_DIM)


def build_about_card():
    W, H = 170, 158
    cv = panel(W, H, seed=17, stars=34)
    spr, cols = mage(ASSETS)
    bw, bh = 40, 36
    bx, by = (W - bw) // 2, 8
    framed_box(cv, bx, by, bw, bh)
    cv.blit(bx + (bw - 32) // 2, by + (bh - 26) // 2, spr, cols, scale=2)

    ry = by + bh + 6
    for x in range(14, W - 14):
        t = 1 - abs(x - W / 2) / (W / 2 - 14)
        cv.set(x, ry, mix(cv.get(x, ry), GOLD_DARK, 0.15 + 0.5 * t))

    entries = [('CLASS',    ['Backend Developer']),
               ('ORIGIN',   ['Mathematics &', 'Cybersecurity']),
               ('FOCUS',    ['Python · FastAPI']),
               ('LEARNING', ['JavaScript · React'])]
    y = ry + 8
    for label, values in entries:
        cv.set(9, y + 3, GOLD)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            cv.set(9 + dx, y + 3 + dy, GOLD_DARK)
        cv.text(14, y, label, GOLD)
        y += 9
        for v in values:
            cv.text(14, y, v, INK)
            y += 8
        y += 4
    cv.save(os.path.join(OUT, 'about-card.svg'),
            'Adventurer card — Class: Backend Developer. Origin: Mathematics & Cybersecurity. '
            'Focus: Python and FastAPI. Learning: JavaScript and React.')
    print('wrote about-card.svg')


# ---------------------------------------------------------------- CTA button
def build_cta():
    text, w, h = 'ALL REPOSITORIES →', 262, 28
    cv = Canvas(w, h)
    for y in range(1, h - 1):
        cv.hline(1, y, w - 2, mix('#1b1f4e', '#0e1130', (y - 1) / (h - 3)))
    starfield(cv, 3, 3, w - 6, h - 6, 14, 3, bright=0.2)
    cv.border(0, 0, w, h, GOLD_DARK)
    seg = 9
    cv.hline((w - seg) // 2, 0, seg, GOLD_MID)
    cv.hline((w - seg) // 2, h - 1, seg, GOLD_MID)
    cv.vline(0, (h - 6) // 2, 6, GOLD_MID)
    cv.vline(w - 1, (h - 6) // 2, 6, GOLD_MID)
    for cx, cy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        cv.set(cx, cy, GOLD_DIM)
    cv.text((w - Canvas.text_w(text, 2)) // 2, (h - 14) // 2, text, GOLD_HI, scale=2)
    cv.save(os.path.join(OUT, 'btn-repos.svg'), 'All repositories')
    print('wrote btn-repos.svg')


# ---------------------------------------------------------------- project card
def chip(cv, x, y, text, icon, icon_colors, icon_w):
    w, h = 27 + 6 * len(text), 20
    for i in range(18):
        cv.hline(x, y + 1 + i, w, mix(CHIP_TOP, CHIP_BOT, i / 17))
    cv.hline(x + 1, y, w - 2, CHIP_BORDER)
    cv.hline(x + 1, y + h - 1, w - 2, CHIP_BORDER)
    cv.vline(x, y + 1, h - 2, CHIP_BORDER)
    cv.vline(x + w - 1, y + 1, h - 2, CHIP_BORDER)
    for cx, cy in ((x, y), (x + w - 1, y), (x, y + h - 1), (x + w - 1, y + h - 1)):
        cv.set(cx, cy, CHIP_CORNER)
    cv.blit(x + 5 + (13 - icon_w) // 2, y + (h - len(icon)) // 2, icon, icon_colors)
    cv.text(x + 22, y + 6, text, INK)
    return w


def gold_button(cv, x, y, text):
    w, h = Canvas.text_w(text, 1) + 14, 18
    for i in range(h - 2):
        cv.hline(x + 1, y + 1 + i, w - 2, mix('#1d2150', '#12163a', i / (h - 3)))
    cv.border(x, y, w, h, GOLD_MID)
    for cx, cy in ((x, y), (x + w - 1, y), (x, y + h - 1), (x + w - 1, y + h - 1)):
        cv.set(cx, cy, GOLD_DARK)
    cv.text(x + 7, y + 6, text, GOLD_HI)
    return w


def build_asteroids_card():
    W, H = 320, 142
    cv = panel(W, H, seed=41, stars=52)
    ex, ey = (W - 58) // 2, 8
    cv.blit(ex, ey, SHIP_ART, {'S': INK, 'F': EMBER}, scale=2)
    cv.blit(ex - 22, ey + 4, ROCK, {'R': '#8f96be'}, scale=2)
    cv.blit(ex + 32, ey + 16, ROCK, {'R': '#6f7699'}, scale=2)

    title, ty = 'Asteroids Game', 46
    shadow = {ty + 2 + i: mix(PANEL_TOP, '#04060f', 0.75) for i in range(16)}
    cv.text((W - Canvas.text_w(title, 2)) // 2, ty, title, GOLD, scale=2,
            shadow_map=shadow, shadow_off=2)
    for i, line in enumerate(['A classic Asteroids-style arcade game',
                              'built with Python and Pygame.']):
        cv.text((W - Canvas.text_w(line)) // 2, 68 + i * 9, line, INK)

    py_rows, py_cols = python_icon(ASSETS)
    chips = [('Python', py_rows, py_cols, 13), ('Pygame', JOYSTICK, {'#': INK}, 10)]
    total = sum(27 + 6 * len(t) for t, *_ in chips) + 8 * (len(chips) - 1)
    cx = (W - total) // 2
    for t, ic, icc, iw in chips:
        cx += chip(cv, cx, 90, t, ic, icc, iw) + 8

    bw = Canvas.text_w('View Repository →', 1) + 14
    gold_button(cv, (W - bw) // 2, 116, 'View Repository →')
    cv.save(os.path.join(OUT, 'project-asteroids.svg'),
            'Asteroids Game — a classic Asteroids-style arcade game built with '
            'Python and Pygame. View repository.')
    print('wrote project-asteroids.svg')


if __name__ == '__main__':
    build_headers()
    build_steam()
    build_about_card()
    build_cta()
    build_asteroids_card()
    print('\nall assets written to', OUT)
