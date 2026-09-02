"""Sprites lifted from the existing artwork so new panels stay on-model."""
import re


def load(path):
    """Read one of our crispEdges pixel SVGs back into a colour grid."""
    s = open(path).read()
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
    W, H = int(vb.group(1)), int(vb.group(2))
    grid = [[None] * W for _ in range(H)]
    for m in re.finditer(r'<path fill="(#[0-9a-fA-F]{6})"(?:\s+opacity="([\d.]+)")?\s+d="([^"]+)"', s):
        color, op, d = m.group(1), m.group(2), m.group(3)
        if op and float(op) < 0.5:
            continue
        for mm in re.finditer(r'M(\d+) (\d+)h(\d+)v1h-\d+z', d):
            x, y, w = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            for i in range(x, x + w):
                if 0 <= i < W and 0 <= y < H:
                    grid[y][i] = color
    return W, H, grid


def _crop(grid, x0, y0, x1, y1, drop):
    rows, colors = [], {}
    for y in range(y0, y1 + 1):
        row = ''
        for x in range(x0, x1 + 1):
            c = grid[y][x]
            if c is None or c in drop:
                row += '.'
            else:
                colors.setdefault(c, chr(ord('A') + len(colors)))
                row += colors[c]
        rows.append(row)
    return rows, {v: k for k, v in colors.items()}


def mage(assets):
    """The hooded figure from the About Me section badge."""
    import os
    _, _, g = load(os.path.join(assets, 'sec-about.svg'))
    return _crop(g, 101, 8, 116, 20, {'#8a6a1f', '#d9a93c', '#97762a', '#1c2354'})


def python_icon(assets):
    """The Python glyph used on the arsenal chips."""
    import os
    _, _, g = load(os.path.join(assets, 'arsenal.svg'))
    keep = {'#4b8bbe', '#ffd43b'}
    pts = [(x, y) for y in range(24, 52) for x in range(40, 120) if g[y][x] in keep]
    x0 = min(p[0] for p in pts); x1 = max(p[0] for p in pts)
    y0 = min(p[1] for p in pts); y1 = max(p[1] for p in pts)
    rows = [''.join({'#4b8bbe': 'B', '#ffd43b': 'Y'}.get(g[y][x], '.')
                    for x in range(x0, x1 + 1)) for y in range(y0, y1 + 1)]
    return rows, {'B': '#4b8bbe', 'Y': '#ffd43b'}
