"""Pixel-art SVG toolkit matching the existing profile assets."""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = {k: tuple(v) for k, v in json.load(open(os.path.join(HERE, 'font.json'))).items()}

# ---------------------------------------------------------------- palette
GOLD        = '#f2c14e'
GOLD_HI     = '#ffe08a'
GOLD_MID    = '#d9a93c'
GOLD_DIM    = '#a8862f'
GOLD_DARK   = '#8a6a1f'
GOLD_EDGE   = '#6d5a2c'
GOLD_INNER  = '#463a1c'
GOLD_SHADE  = '#97762a'
INK         = '#dfe3ff'
INK_HI      = '#f4f6ff'
LILAC       = '#b9a3f0'
PURPLE      = '#5b41a0'
BOX_FILL    = '#1c2354'
FRAME_BLUE  = '#4a54a8'
PERI        = '#a9b6ff'
PALE        = '#cfd6ff'
CYAN        = '#7fd3ff'
WHITE       = '#e8ecff'
EMBER       = '#ff9d5c'

STAR_COLORS = [INK_HI, GOLD_HI, LILAC, PERI, PALE]

# Section-band vertical gradient (rows 4..25 of the sec-*.svg headers)
BAND_BG = ['#252c62', '#131a41', '#121940', '#12193f', '#12183f', '#11183e',
           '#11173d', '#11173c', '#10163b', '#10163a', '#101539', '#0f1539',
           '#0f1438', '#0f1437', '#0e1336', '#0e1335', '#0e1234', '#0d1233',
           '#0d1133', '#0d1132', '#0c1031', '#080b20']
# Title drop-shadow ramp, indexed by absolute row 11..24
TITLE_SHADOW = {11: '#080b1d', 12: '#070a1c', 13: '#070a1b', 14: '#070a1b',
                15: '#070a1b', 16: '#07091b', 17: '#07091a', 18: '#06091a',
                19: '#060919', 20: '#060819', 21: '#060819', 22: '#060819',
                23: '#060818', 24: '#050718'}

# Link-button interior gradient (rows 2..21)
BTN_BG = ['#413f6d', '#2a2c55', '#292b54', '#292b53', '#282a53', '#272952',
          '#262851', '#252751', '#242650', '#23254f', '#23254f', '#22244e',
          '#21234d', '#20224d', '#1f214c', '#1e204b', '#1d1f4b', '#1d1f4a',
          '#1c1e49', '#1b1d49']
BTN_CORNER = '#0b0f28'


def mix(a, b, t):
    """Blend two #rrggbb colors."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[None] * w for _ in range(h)]

    def set(self, x, y, c):
        if c and 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[y][x]

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def border(self, x, y, w, h, c):
        self.hline(x, y, w, c); self.hline(x, y + h - 1, w, c)
        self.vline(x, y, h, c); self.vline(x + w - 1, y, h, c)

    def blit(self, x, y, rows, colors, scale=1):
        """rows: list of strings; colors: dict char -> color ('.' skipped)."""
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch == '.':
                    continue
                col = colors.get(ch, ch)
                for sy in range(scale):
                    for sx in range(scale):
                        self.set(x + dx * scale + sx, y + dy * scale + sy, col)

    # ------------------------------------------------------------ text
    def text(self, x, y, s, color, scale=1, shadow=None, shadow_off=None,
             shadow_map=None):
        adv = 6 * scale
        if shadow or shadow_map:
            off = shadow_off if shadow_off else scale
            for i, ch in enumerate(s):
                g = FONT.get(ch, FONT[' '])
                for r in range(7):
                    for c in range(5):
                        if g[r][c] == '#':
                            for sy in range(scale):
                                for sx in range(scale):
                                    px, py = x + i * adv + c * scale + sx + off, y + r * scale + sy + off
                                    col = shadow_map.get(py) if shadow_map else shadow
                                    self.set(px, py, col)
        for i, ch in enumerate(s):
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                for c in range(5):
                    if g[r][c] == '#':
                        for sy in range(scale):
                            for sx in range(scale):
                                self.set(x + i * adv + c * scale + sx, y + r * scale + sy, color)

    @staticmethod
    def text_w(s, scale=1):
        return len(s) * 6 * scale - scale

    # ------------------------------------------------------------ output
    def svg(self, label=''):
        runs = {}
        for y in range(self.h):
            x = 0
            while x < self.w:
                c = self.px[y][x]
                if c is None:
                    x += 1; continue
                x0 = x
                while x < self.w and self.px[y][x] == c:
                    x += 1
                runs.setdefault(c, []).append((x0, y, x - x0))
        order = sorted(runs, key=lambda c: -len(runs[c]))
        parts = []
        for c in order:
            d = ''.join('M%d %dh%dv1h-%dz' % (x, y, w, w) for x, y, w in runs[c])
            parts.append('<path fill="%s" d="%s"/>' % (c, d))
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
                'shape-rendering="crispEdges" role="img" aria-label="%s">' % (self.w, self.h, label))
        return head + ''.join(parts) + '</svg>'

    def save(self, path, label=''):
        with open(path, 'w') as fh:
            fh.write(self.svg(label))
        return path


def starfield(cv, x, y, w, h, n, seed, avoid=(), bright=0.30):
    """Sprinkle sparse stars, skipping rectangles in `avoid`."""
    rng = random.Random(seed)
    placed = 0
    tries = 0
    while placed < n and tries < n * 60:
        tries += 1
        sx = rng.randrange(x, x + w)
        sy = rng.randrange(y, y + h)
        if any(ax <= sx < ax + aw and ay <= sy < ay + ah for ax, ay, aw, ah in avoid):
            continue
        if cv.get(sx, sy) is None:
            continue
        col = rng.choice(STAR_COLORS) if rng.random() < bright else mix(cv.get(sx, sy), INK_HI, 0.35)
        cv.set(sx, sy, col)
        placed += 1


PANEL_TOP = '#141942'
PANEL_BOT = '#0b0f2b'


def panel(w, h, seed=0, stars=None, top=PANEL_TOP, bot=PANEL_BOT):
    """Framed starry panel in the style of arsenal.svg / featured-dnd.svg."""
    cv = Canvas(w, h)
    # interior vertical gradient
    span = max(1, (h - 4) - 3)
    for y in range(3, h - 3):
        cv.hline(3, y, w - 6, mix(top, bot, (y - 3) / span))
    # inner hairline ring
    cv.border(2, 2, w - 4, h - 4, GOLD_INNER)
    for cx, cy in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
        cv.set(cx, cy, GOLD_DIM)
    # gap ring picks up the interior tone
    for y in range(1, h - 1):
        for x in (1, w - 2):
            if cv.get(x, y) is None:
                cv.set(x, y, mix(top, bot, min(1, max(0, (y - 3) / span))))
    for x in range(1, w - 1):
        for y in (1, h - 2):
            if cv.get(x, y) is None:
                cv.set(x, y, mix(top, bot, min(1, max(0, (y - 3) / span))))
    # outer border: bright at the corners, dim along the runs
    for x in range(w):
        c = GOLD_DIM if (x < 5 or x >= w - 5) else GOLD_EDGE
        cv.set(x, 0, c); cv.set(x, h - 1, c)
    for y in range(h):
        c = GOLD_DIM if (y < 5 or y >= h - 5) else GOLD_EDGE
        cv.set(0, y, c); cv.set(w - 1, y, c)
    # corner gems
    cv.set(1, 1, GOLD_HI); cv.set(w - 2, h - 2, GOLD_HI)
    if stars:
        starfield(cv, 4, 4, w - 8, h - 8, stars, seed)
    return cv

BOX_TOP = 'aaaaaaabbbbbbbbbaaaaaa'
BOX_ACC = 'accccccccdcbcdccccccca'
BOX_MID = 'a' + 'c' * 20 + 'a'
BOX_COLORS = {'a': GOLD_DARK, 'b': GOLD_MID, 'c': BOX_FILL, 'd': GOLD_SHADE}


def header(title, sprite, sprite_at, seed, label=None, sprite_colors=None):
    """Build a 320x30 section header in the established style."""
    cv = Canvas(320, 30)
    # band gradient, rows 4..25
    for i, col in enumerate(BAND_BG):
        cv.hline(0, 4 + i, 320, col)

    tw = Canvas.text_w(title, 2)
    group_w = 22 + 9 + tw
    box_x = 160 - group_w // 2
    text_x = box_x + 31

    starfield(cv, 0, 5, 320, 20, 26, seed,
              avoid=[(box_x - 2, 4, 26, 24), (text_x - 2, 7, tw + 6, 20),
                     (6, 13, 6, 6), (307, 13, 7, 6)])

    # connecting rules: a gradient that brightens toward the title
    bg15 = BAND_BG[15 - 4]
    lend = box_x - 9
    for x in range(11, lend + 1):
        t = 0.105 + 0.445 * (x - 11) / max(1, lend - 11)
        cv.set(x, 15, mix(bg15, GOLD_DARK, t))
    rstart = text_x + tw + 9
    for x in range(rstart, 309):
        t = 0.105 + 0.445 * (308 - x) / max(1, 308 - rstart)
        cv.set(x, 15, mix(bg15, GOLD_DARK, t))
    for nx in (8, 309):
        cv.rect(nx, 14, 3, 3, GOLD_DARK)

    # icon box
    cv.blit(box_x, 5, [BOX_TOP, BOX_ACC] + [BOX_MID] * 18 + [BOX_ACC, BOX_TOP], BOX_COLORS)
    if sprite:
        cv.blit(box_x + sprite_at[0], 5 + sprite_at[1], sprite, sprite_colors or {})

    cv.text(text_x, 9, title, GOLD, scale=2, shadow_map=TITLE_SHADOW, shadow_off=2)
    return cv, box_x, text_x
