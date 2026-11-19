import cairo, math, json, subprocess, sys, random
W, H, FPS = 1080, 1920, 30
BG = (0.965, 0.945, 0.905)
INK = (0.07, 0.07, 0.08)
RED = (0.80, 0.18, 0.16)
GOLD = (0.86, 0.66, 0.15)
GREEN = (0.20, 0.62, 0.32)
GREY = (0.62, 0.62, 0.64)
LGREY = (0.85, 0.84, 0.82)
WHITE = (1, 1, 1)
BLUE = (0.30, 0.55, 0.85)
FONT = "Inter Black"

T = json.load(open('vo/timing.json'))
LINES, WORDS, END = T['lines'], T['words'], T['end']
END += 1.3
_fx = []
for w in WORDS:
    if _fx and w[0].startswith(',000'):
        _fx[-1] = [_fx[-1][0] + ',000', _fx[-1][1], w[2]]; continue
    if _fx and _fx[-1][0] == 'Warehouse' and w[0] == 'is':
        _fx[-1] = ['Warehouses', _fx[-1][1], w[2]]; continue
    if _fx and w[0].startswith('-') and len(w[0]) > 1:
        _fx[-1] = [_fx[-1][0] + w[0], _fx[-1][1], w[2]]; continue
    w = list(w)
    w[0] = {'Per': 'For', 'bard.': 'barred.', 'bard!': 'barred!', 'bard': 'barred', 'Jail': 'Jailed', 'Chabal,': 'Chappell,', 'Chabal': 'Chappell', 'Chapel.': 'Chappell.', 'Chapel': 'Chappell'}.get(w[0], w[0])
    _fx.append(w)
WORDS = _fx
NF = int(math.ceil(END * FPS))

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def pop(x):
    x = clamp(x); c = 2.2
    return max(0.001, 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2)
def ph(t, a, d=0.35): return clamp((t - a) / d)
def lerp(a, b, k): return a + (b - a) * k

def wt(li, word, nth=0):
    s, e = LINES[li]
    hits = [w for w in WORDS if s - 0.15 <= w[1] <= e + 0.1 and word.lower() in w[0].lower()]
    return hits[min(nth, len(hits) - 1)][1] if hits else s

def setc(c, col, a=1): c.set_source_rgba(col[0], col[1], col[2], a)

def text(c, s, x, y, size, col=INK, align="center", stroke=None, sw=0, alpha=1):
    c.save(); c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    e = c.text_extents(s)
    x0 = x - (e.width / 2 + e.x_bearing) if align == "center" else (x - e.x_bearing if align == "left" else x - e.width - e.x_bearing)
    y0 = y - (e.height / 2 + e.y_bearing)
    c.move_to(x0, y0); c.text_path(s)
    if stroke:
        setc(c, stroke, alpha); c.set_line_width(sw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    setc(c, col, alpha); c.fill(); c.restore(); return e.x_advance

def tw(c, s, size):
    c.save(); c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = c.text_extents(s).x_advance; c.restore(); return w

def line(c, pts, w=14, col=INK, a=1):
    c.save(); setc(c, col, a); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.stroke(); c.restore()

def circle(c, x, y, r, fill=None, stroke=INK, w=12, a=1):
    c.save(); c.arc(x, y, r, 0, 2 * math.pi)
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(w); c.stroke()
    c.new_path(); c.restore()

def rrect(c, x, y, w, h, r, fill=None, stroke=None, lw=10, a=1):
    r = max(0.1, min(r, w / 2, h / 2))
    c.save(); c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.new_path(); c.restore()

def poly(c, pts, fill=None, stroke=None, lw=10, a=1):
    c.save(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path()
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.new_path(); c.restore()

# ---------------- stickman rig ----------------
# angles in degrees from straight down; positive swings to screen-right
BASE = dict(lean=0, head=0, la=(20, 10), ra=(-20, -10), ll=(10, 4), rl=(-10, -4))

def P(**k):
    d = dict(BASE); d.update(k); return d

def lp(a, b, k):
    out = {}
    for key in a:
        va, vb = a[key], b.get(key, a[key])
        out[key] = tuple(lerp(x, y, k) for x, y in zip(va, vb)) if isinstance(va, tuple) else lerp(va, vb, k)
    return out

def seg(x, y, L, ang):
    r = math.radians(ang); return (x + L * math.sin(r), y + L * math.cos(r))

def stick(c, x, y, s, p, face="smile", tie=False, col=INK, lw=None, hat=None, sweat=0, case=False, flip=False):
    """x,y = hip. Returns dict of hand points."""
    lw = lw or 15 * s
    lean = math.radians(p["lean"])
    neck = (x + math.sin(lean) * 210 * s, y - math.cos(lean) * 210 * s)
    sh = (x + math.sin(lean) * 180 * s, y - math.cos(lean) * 180 * s)
    for (h, k) in (p["ll"], p["rl"]):
        kn = seg(x, y, 105 * s, h); ft = seg(*kn, 105 * s, h + k)
        line(c, [(x, y), kn, ft], lw, col)
    line(c, [(x, y), neck], lw, col)
    hands = []
    for (u, f) in (p["la"], p["ra"]):
        el = seg(*sh, 88 * s, u); hd = seg(*el, 84 * s, u + f)
        line(c, [sh, el, hd], lw, col); hands.append(hd)
    hr = 58 * s
    hx = neck[0] + math.sin(math.radians(p["head"]) + lean) * (hr + 4 * s)
    hy = neck[1] - math.cos(math.radians(p["head"]) + lean) * (hr + 4 * s)
    if tie:
        tx, ty = neck
        poly(c, [(tx - 10 * s, ty + 4 * s), (tx + 10 * s, ty + 4 * s), (tx + 14 * s, ty + 70 * s), (tx, ty + 88 * s), (tx - 14 * s, ty + 70 * s)], fill=RED)
    circle(c, hx, hy, hr, fill=WHITE, stroke=col, w=lw)
    d = -1 if flip else 1
    ex = 20 * s
    if face in ("o", "panic"):
        for sx in (-1, 1):
            circle(c, hx + sx * ex + d * 4 * s, hy - 10 * s, 12 * s, fill=WHITE, stroke=col, w=4.5 * s)
            circle(c, hx + sx * ex + d * 4 * s, hy - 10 * s, 5 * s, fill=col, stroke=None)
        circle(c, hx + d * 4 * s, hy + 26 * s, 13 * s if face == "panic" else 9 * s, fill=col, stroke=None)
        line(c, [(hx - 32 * s, hy - 36 * s), (hx - 12 * s, hy - 42 * s)], 5 * s, col)
        line(c, [(hx + 12 * s, hy - 42 * s), (hx + 32 * s, hy - 36 * s)], 5 * s, col)
    else:
        for sx in (-1, 1):
            circle(c, hx + sx * ex + d * 5 * s, hy - 8 * s, 6.5 * s, fill=col, stroke=None)
        if face == "smile":
            c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(hx + d * 5 * s, hy + 8 * s, 20 * s, 0.18 * math.pi, 0.82 * math.pi); c.stroke(); c.restore()
        elif face == "grin":
            c.save(); setc(c, col); c.move_to(hx - 22 * s + d * 5 * s, hy + 10 * s); c.arc(hx + d * 5 * s, hy + 10 * s, 22 * s, 0, math.pi); c.close_path(); c.fill(); c.restore()
        elif face == "smug":
            c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(hx + d * 12 * s, hy + 10 * s, 16 * s, 0.1 * math.pi, 0.6 * math.pi); c.stroke(); c.restore()
            line(c, [(hx - 30 * s, hy - 26 * s), (hx - 10 * s, hy - 22 * s)], 5 * s, col)
            line(c, [(hx + 10 * s, hy - 22 * s), (hx + 30 * s, hy - 26 * s)], 5 * s, col)
        elif face == "sad":
            c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(hx + d * 4 * s, hy + 34 * s, 16 * s, 1.15 * math.pi, 1.85 * math.pi); c.stroke(); c.restore()
            line(c, [(hx - 32 * s, hy - 24 * s), (hx - 12 * s, hy - 32 * s)], 5 * s, col)
            line(c, [(hx + 12 * s, hy - 32 * s), (hx + 32 * s, hy - 24 * s)], 5 * s, col)
        elif face == "flat":
            line(c, [(hx - 14 * s, hy + 22 * s), (hx + 16 * s, hy + 22 * s)], 5 * s, col)
    if sweat > 0:
        for k, (dx, dy) in enumerate(((70, -30), (-72, -10))):
            yy = hy + dy * s + 30 * s * ((sweat + k * 0.5) % 1)
            poly(c, [(hx + dx * s, yy - 18 * s), (hx + dx * s + 10 * s, yy + 4 * s), (hx + dx * s - 10 * s, yy + 4 * s)], fill=BLUE)
            circle(c, hx + dx * s, yy + 4 * s, 10 * s, fill=BLUE, stroke=None)
    if hat == "cap":
        c.save(); setc(c, RED); c.arc(hx, hy - 6 * s, hr + 2 * s, math.pi, 2 * math.pi); c.close_path(); c.fill(); c.restore()
        line(c, [(hx, hy - 8 * s), (hx + d * 95 * s, hy - 8 * s)], 12 * s, RED)
    if case:
        hx2, hy2 = hands[1]
        rrect(c, hx2 - 55 * s, hy2 - 4 * s, 110 * s, 80 * s, 10 * s, fill=GOLD, stroke=col, lw=6 * s)
        line(c, [(hx2 - 20 * s, hy2 - 4 * s), (hx2 - 20 * s, hy2 - 18 * s), (hx2 + 20 * s, hy2 - 18 * s), (hx2 + 20 * s, hy2 - 4 * s)], 6 * s, col)
    return dict(lh=hands[0], rh=hands[1], head=(hx, hy))

# ---------------- props ----------------
def building(c, x, base, w, h, name, sign=RED, k=0.0, t=0):
    """k = collapse 0..1"""
    c.save()
    sink = h * 0.85 * eio(k)
    tilt = 0.18 * eio(k) * (1 if hash(name) % 2 else -1)
    c.rectangle(x - 60, 0, w + 120, base + 2); c.clip()
    c.translate(x + w / 2, base); c.rotate(tilt); c.translate(-(x + w / 2), -base + sink)
    rrect(c, x, base - h, w, h, 10, fill=WHITE, stroke=INK, lw=11)
    rrect(c, x + 14, base - h + 16, w - 28, 100, 8, fill=sign, stroke=INK, lw=7)
    parts = name.split("|")
    for j, pn in enumerate(parts):
        fs = 50 if len(parts) == 1 else 38
        while tw(c, pn, fs) > w - 50: fs -= 2
        text(c, pn, x + w / 2, base - h + 66 + (j - (len(parts) - 1) / 2) * 42, fs, WHITE)
    for r in range(3):
        for q in range(2):
            rrect(c, x + 30 + q * (w - 30) / 2, base - h + 150 + r * 105, (w - 90) / 2, 70, 6, fill=(0.78, 0.88, 0.96), stroke=INK, lw=7)
    if k > 0.05:
        random.seed(hash(name) % 1000)
        for _ in range(4):
            px = x + random.random() * w; py = base - h + random.random() * h
            line(c, [(px, py), (px + 30, py + 40), (px + 5, py + 80), (px + 35, py + 120)], 7, INK, min(1, k * 3))
    c.restore()
    if 0.05 < k < 0.999:
        for j in range(7):
            r = 40 + 70 * eio(k) + (j % 3) * 15
            circle(c, x + w * (j / 6), base - 10 - 30 * math.sin(j), r, fill=LGREY, stroke=None, a=0.85 * (1 - k * 0.6))

def stamp(c, s, x, y, k, col=RED, size=120, rot=-0.15):
    if k <= 0: return
    sc = 2.6 - 1.6 * ease(k)
    a = clamp(k * 3)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    wd = tw(c, s, size) + 70
    rrect(c, -wd / 2, -size * 0.75, wd, size * 1.5, 18, fill=None, stroke=col, lw=14, a=a)
    text(c, s, 0, 0, size, col, alpha=a)
    c.restore()

def vacuum(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    line(c, [(0, -330), (40, -60)], 16, INK)
    rrect(c, -40, -380, 90, 40, 14, fill=INK)
    rrect(c, 10, -220, 110, 190, 30, fill=RED, stroke=INK, lw=10)
    rrect(c, -40, -50, 200, 55, 18, fill=GREY, stroke=INK, lw=10)
    circle(c, -5, 12, 18, fill=INK, stroke=None); circle(c, 120, 12, 18, fill=INK, stroke=None)
    c.restore()

def box(c, x, y, w, h, label="VACUUM"):
    rrect(c, x, y, w, h, 6, fill=(0.80, 0.62, 0.40), stroke=INK, lw=8)
    line(c, [(x + w / 2, y), (x + w / 2, y + 22)], 6, INK)
    fs = 34
    while tw(c, label, fs) > w - 24: fs -= 2
    text(c, label, x + w / 2, y + h / 2 + 8, fs, INK)

def board(c, x, y, w, rows, flip):
    rrect(c, x, y, w, 110 + 86 * len(rows), 18, fill=(0.12, 0.12, 0.15), stroke=INK, lw=10)
    text(c, "DEPARTURES", x + w / 2, y + 58, 48, GOLD)
    for j, (dest, st) in enumerate(rows):
        yy = y + 140 + j * 86
        text(c, dest, x + 40, yy, 46, WHITE, align="left")
        k = flip[j] if isinstance(flip, (list, tuple)) else flip
        if k < 0.5:
            text(c, "ON TIME", x + w - 40, yy, 44, (0.45, 0.85, 0.5), align="right", alpha=1 - k * 2)
        else:
            text(c, "CANCELLED", x + w - 40, yy, 44, (1, 0.35, 0.3), align="right", alpha=(k - 0.5) * 2)

def plane(c, x, y, s=1.0, col=INK, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -170, -28, 340, 56, 28, fill=WHITE, stroke=col, lw=9)
    poly(c, [(-30, 0), (60, 0), (-50, -130), (-95, -130)], fill=WHITE, stroke=col, lw=9)
    poly(c, [(-30, 10), (60, 10), (-50, 120), (-95, 120)], fill=WHITE, stroke=col, lw=9)
    poly(c, [(-170, -10), (-120, -10), (-155, -95), (-185, -95)], fill=RED, stroke=col, lw=9)
    for k in range(6): circle(c, 100 - k * 38, -6, 8, fill=BLUE, stroke=None)
    c.restore()

