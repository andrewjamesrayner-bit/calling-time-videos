import cairo, math, json, subprocess, sys, random
W, H, FPS = 1920, 1080, 30
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

WORDS = []
LINES = []
END = 0


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


# ================= rig =================
# Expressive stickman rig for Calling Time comedy Shorts.
# Same limb system as base.stick, but with a full face kit (eyes/pupils/brows/mouths),
# squash & stretch, and costume pieces for recurring characters.

BROWS = {   # (left inner, left outer, right inner, right outer) vertical offsets; negative = up
    "none": None,
    "neutral": (0, 0, 0, 0),
    "angry": (10, -6, 10, -6),
    "worried": (-12, 4, -12, 4),
    "raised": (-16, -14, -16, -14),
    "one": (0, 0, -14, -20),
    "sly": (6, -2, -10, -18),
}

def _eye(c, x, y, s, kind, look, col, blink):
    lx, ly = look
    if blink > 0.5 or kind == "closed":
        c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(x, y + 2 * s, 11 * s, 0.15 * math.pi, 0.85 * math.pi); c.stroke(); c.restore(); return
    if kind == "x":
        line(c, [(x - 10 * s, y - 10 * s), (x + 10 * s, y + 10 * s)], 5 * s, col)
        line(c, [(x - 10 * s, y + 10 * s), (x + 10 * s, y - 10 * s)], 5 * s, col); return
    if kind == "happy":
        c.save(); setc(c, col); c.set_line_width(5.5 * s); c.arc(x, y + 6 * s, 11 * s, 1.15 * math.pi, 1.85 * math.pi); c.stroke(); c.restore(); return
    r = {"wide": 19, "open": 14, "half": 14, "tiny": 9}.get(kind, 14) * s
    circle(c, x, y, r, fill=WHITE, stroke=col, w=4.5 * s)
    pr = (6.5 if kind != "wide" else 6) * s
    circle(c, x + lx * (r - pr - 2 * s), y + ly * (r - pr - 2 * s), pr, fill=col, stroke=None)
    if kind == "half":   # heavy lid = smug / bored
        c.save(); c.arc(x, y, r, math.pi, 2 * math.pi); c.close_path(); setc(c, WHITE); c.fill_preserve(); setc(c, col); c.set_line_width(4.5 * s); c.stroke(); c.restore()
        line(c, [(x - r, y), (x + r, y)], 5 * s, col)

def _mouth(c, x, y, s, kind, col, talk):
    if kind == "talk":
        o = 0.5 + 0.5 * math.sin(talk)
        kind = "open" if o > 0.45 else "smile"
        if kind == "open":
            c.save(); c.translate(x, y + 6 * s); c.scale(1, 0.35 + 0.65 * o); circle(c, 0, 0, 15 * s, fill=col, stroke=None); c.restore()
            c.save(); c.translate(x, y + 12 * s); c.scale(1, 0.35 * o); circle(c, 0, 0, 8 * s, fill=RED, stroke=None); c.restore(); return
    if kind == "smile":
        c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(x, y - 4 * s, 20 * s, 0.18 * math.pi, 0.82 * math.pi); c.stroke(); c.restore()
    elif kind == "grin":
        c.save(); c.new_path(); c.move_to(x - 24 * s, y); c.arc(x, y, 24 * s, 0, math.pi); c.close_path(); setc(c, col); c.fill(); c.restore()
        c.new_path(); line(c, [(x - 20 * s, y + 5 * s), (x + 20 * s, y + 5 * s)], 3.5 * s, WHITE)
    elif kind == "smirk":
        c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(x + 8 * s, y - 6 * s, 16 * s, 0.1 * math.pi, 0.55 * math.pi); c.stroke(); c.restore()
    elif kind == "frown":
        c.save(); setc(c, col); c.set_line_width(5 * s); c.arc(x, y + 22 * s, 16 * s, 1.15 * math.pi, 1.85 * math.pi); c.stroke(); c.restore()
    elif kind == "flat":
        line(c, [(x - 14 * s, y + 8 * s), (x + 14 * s, y + 8 * s)], 5 * s, col)
    elif kind == "wavy":
        pts = [(x - 20 * s + i * 5 * s, y + 8 * s + math.sin(i * 1.6) * 4 * s) for i in range(9)]
        line(c, pts, 4.5 * s, col)
    elif kind == "o":
        circle(c, x, y + 10 * s, 10 * s, fill=col, stroke=None)
    elif kind == "scream":
        c.save(); c.translate(x, y + 14 * s); c.scale(1, 1.4); circle(c, 0, 0, 17 * s, fill=col, stroke=None); c.restore()
        c.save(); c.translate(x, y + 26 * s); c.scale(1, 0.6); circle(c, 0, 0, 10 * s, fill=RED, stroke=None); c.restore()
    elif kind == "teeth":   # nervous grimace
        rrect(c, x - 24 * s, y - 2 * s, 48 * s, 22 * s, 6 * s, fill=WHITE, stroke=col, lw=4.5 * s)
        line(c, [(x - 24 * s, y + 9 * s), (x + 24 * s, y + 9 * s)], 3 * s, col)
        for k in (-12, 0, 12): line(c, [(x + k * s, y - 2 * s), (x + k * s, y + 20 * s)], 3 * s, col)

def face(c, hx, hy, s, eyes="open", look=(0, 0), brow="neutral", mouth="smile", col=INK, talk=0, blink=0, d=1):
    ex = 21 * s
    for sx in (-1, 1):
        ek = ("closed" if sx == 1 else "open") if eyes == "wink" else eyes
        _eye(c, hx + sx * ex + d * 4 * s, hy - 10 * s, s, ek, look, col, blink if eyes != "wink" else 0)
    b = BROWS.get(brow)
    if b:
        by = hy - 38 * s
        line(c, [(hx - 8 * s + d * 4 * s, by + b[0] * s), (hx - 34 * s + d * 4 * s, by + b[1] * s)], 6 * s, col)
        line(c, [(hx + 8 * s + d * 4 * s, by + b[2] * s), (hx + 34 * s + d * 4 * s, by + b[3] * s)], 6 * s, col)
    _mouth(c, hx + d * 4 * s, hy + 20 * s, s, mouth, col, talk)

def man(c, x, y, s, p, eyes="open", look=(0, 0), brow="neutral", mouth="smile", talk=0, blink=0,
        col=INK, sq=0.0, outfit=None, sweat=0, blush=0, flip=False, hold=None, extras=()):
    """x,y = hip. sq = squash(+)/stretch(-). outfit: 'landlord','racer','tycoon','mp','worker','pensioner'."""
    tt_ = extras_t[0]; ph_ = x * 0.013 + s * 3.1
    y += math.sin(tt_ * 3.2 + ph_) * 3.5 * s
    p = dict(p)
    p["la"] = (p["la"][0] + math.sin(tt_ * 2.6 + ph_) * 4, p["la"][1])
    p["ra"] = (p["ra"][0] - math.sin(tt_ * 2.6 + ph_ + 1) * 4, p["ra"][1])
    p["head"] = p.get("head", 0) + math.sin(tt_ * 1.7 + ph_) * 3
    c.save()
    c.translate(x, y + 210 * s); c.scale(1 + 0.12 * sq, 1 - 0.12 * sq); c.translate(-x, -(y + 210 * s))
    lw = 15 * s
    lean = math.radians(p["lean"])
    neck = (x + math.sin(lean) * 210 * s, y - math.cos(lean) * 210 * s)
    sh = (x + math.sin(lean) * 180 * s, y - math.cos(lean) * 180 * s)
    for (h, k) in (p["ll"], p["rl"]):
        kn = seg(x, y, 105 * s, h); ft = seg(*kn, 105 * s, h + k)
        line(c, [(x, y), kn, ft], lw, col)
    line(c, [(x, y), neck], lw, col)
    if outfit == "landlord":   # round belly, apron, bar towel on the shoulder
        bx_, by_ = (x + neck[0]) / 2 + 16 * s, (y + neck[1]) / 2 + 30 * s
        c.save(); c.translate(bx_, by_); c.scale(1.0, 1.12); circle(c, 0, 0, 70 * s, fill=(0.93, 0.93, 0.95), stroke=col, w=8 * s); c.restore()
        poly(c, [(bx_ - 52 * s, by_ - 18 * s), (bx_ + 52 * s, by_ - 18 * s), (bx_ + 64 * s, y + 40 * s), (bx_ - 64 * s, y + 40 * s)], fill=(0.16, 0.20, 0.26), stroke=col, lw=6 * s)
        rrect(c, bx_ - 22 * s, by_ + 6 * s, 44 * s, 30 * s, 6 * s, fill=None, stroke=(0.85, 0.85, 0.85), lw=4 * s)
        line(c, [(bx_ - 50 * s, by_ - 18 * s), (neck[0] - 10 * s, neck[1] + 6 * s)], 5 * s, (0.16, 0.20, 0.26))
        line(c, [(bx_ + 50 * s, by_ - 18 * s), (neck[0] + 10 * s, neck[1] + 6 * s)], 5 * s, (0.16, 0.20, 0.26))
    if outfit in ("tycoon", "mp"):
        tx, ty = neck
        poly(c, [(tx - 10 * s, ty + 4 * s), (tx + 10 * s, ty + 4 * s), (tx + 14 * s, ty + 70 * s), (tx, ty + 88 * s), (tx - 14 * s, ty + 70 * s)], fill=RED if outfit == "tycoon" else BLUE)
    hands = []
    for (u, f) in (p["la"], p["ra"]):
        el = seg(*sh, 88 * s, u); hd = seg(*el, 84 * s, u + f)
        line(c, [sh, el, hd], lw, col); hands.append(hd)
    hr = 60 * s
    hx = neck[0] + math.sin(math.radians(p["head"]) + lean) * (hr + 4 * s)
    hy = neck[1] - math.cos(math.radians(p["head"]) + lean) * (hr + 4 * s)
    circle(c, hx, hy, hr, fill=WHITE, stroke=col, w=lw)
    d = -1 if flip else 1
    if blush > 0:
        for sx in (-1, 1):
            c.save(); c.translate(hx + sx * 34 * s, hy + 14 * s); c.scale(1, 0.55); circle(c, 0, 0, 13 * s, fill=(0.95, 0.55, 0.55), stroke=None, a=0.7 * blush); c.restore()
    if outfit == "racer":
        c.save(); c.arc(hx, hy, hr + 8 * s, math.pi * 0.95, math.pi * 2.05); c.close_path(); setc(c, RED); c.fill_preserve(); setc(c, col); c.set_line_width(7 * s); c.stroke(); c.restore()
        line(c, [(hx - hr, hy - 22 * s), (hx + hr, hy - 22 * s)], 8 * s, WHITE)
    face(c, hx, hy, s, eyes, look, "none" if outfit == "racer" else brow, mouth, col, talk, blink, d)
    if outfit == "landlord":   # moustache + bald shine + towel
        poly(c, [(hx - 34 * s + d * 4 * s, hy + 12 * s), (hx + d * 4 * s, hy + 0 * s), (hx + 34 * s + d * 4 * s, hy + 12 * s), (hx + 24 * s + d * 4 * s, hy + 18 * s), (hx + d * 4 * s, hy + 10 * s), (hx - 24 * s + d * 4 * s, hy + 18 * s)], fill=col)
        c.save(); setc(c, col, 0.18); c.set_line_width(6 * s); c.arc(hx - 18 * s, hy - 20 * s, 30 * s, 1.15 * math.pi, 1.45 * math.pi); c.stroke(); c.restore()
        # tea towel over the left shoulder (drawn last so it sits on top)
        tx_, ty_ = neck[0] - 26 * s, neck[1] + 10 * s
        poly(c, [(tx_ - 26 * s, ty_ - 6 * s), (tx_ + 6 * s, ty_ - 14 * s), (tx_ + 2 * s, ty_ + 86 * s), (tx_ - 30 * s, ty_ + 92 * s)], fill=WHITE, stroke=col, lw=5 * s)
        for k in (20, 40): line(c, [(tx_ - 28 * s, ty_ + k * s), (tx_ + 4 * s, ty_ + (k - 6) * s)], 5 * s, RED)
    if outfit == "tycoon":   # shades
        for sx in (-1, 1):
            rrect(c, hx + sx * 22 * s - 20 * s + d * 4 * s, hy - 22 * s, 40 * s, 24 * s, 8 * s, fill=col)
        line(c, [(hx - 4 * s + d * 4 * s, hy - 14 * s), (hx + 4 * s + d * 4 * s, hy - 14 * s)], 4 * s, col)
    if outfit == "pensioner":
        line(c, [(hx - 46 * s, hy - 40 * s), (hx - 30 * s, hy - 52 * s), (hx - 14 * s, hy - 44 * s)], 4 * s, GREY)
        line(c, [(hx + 46 * s, hy - 40 * s), (hx + 30 * s, hy - 52 * s), (hx + 14 * s, hy - 44 * s)], 4 * s, GREY)
    if outfit == "worker":
        hx2, hy2 = hands[1]
        rrect(c, hx2 - 50 * s, hy2 - 20 * s, 100 * s, 70 * s, 6 * s, fill=(0.78, 0.62, 0.42), stroke=col, lw=6 * s)
    if sweat > 0:
        for k, (dx, dy) in enumerate(((72, -30), (-74, -10))):
            yy = hy + dy * s + 34 * s * ((sweat + k * 0.5) % 1)
            poly(c, [(hx + dx * s, yy - 18 * s), (hx + dx * s + 10 * s, yy + 4 * s), (hx + dx * s - 10 * s, yy + 4 * s)], fill=BLUE)
            circle(c, hx + dx * s, yy + 4 * s, 10 * s, fill=BLUE, stroke=None)
    if "vein" in extras:
        vx, vy = hx + 36 * s, hy - 40 * s
        for a in range(4):
            r_ = math.radians(45 + a * 90)
            line(c, [(vx + math.cos(r_) * 6 * s, vy + math.sin(r_) * 6 * s), (vx + math.cos(r_) * 16 * s, vy + math.sin(r_) * 16 * s)], 5 * s, RED)
    if "stars" in extras:
        for a in range(3):
            r_ = extras_t[0] * 4 + a * 2.09
            star(c, hx + math.cos(r_) * 80 * s, hy - 70 * s + math.sin(r_) * 18 * s, 14 * s, GOLD)
    c.restore()
    return dict(lh=hands[0], rh=hands[1], head=(hx, hy), neck=neck)

extras_t = [0.0]

def star(c, x, y, r, col):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    poly(c, pts, fill=col, stroke=INK, lw=3)

def blinkf(t, seed=0):
    ph_ = (t + seed * 1.37) % 3.1
    return 1.0 if ph_ < 0.12 else 0.0

def talkf(t, li):
    """mouth phase if narration words are active right now (absolute time t)."""
    for w in WORDS:
        if w[1] - 0.02 <= t <= w[2]: return t * 26
    return None

def motion_lines(c, x, y, n=4, length=140, d=1, a=1.0):
    for k in range(n):
        yy = y - 60 + k * 40
        line(c, [(x - d * 30, yy), (x - d * (30 + length * (0.6 + 0.4 * ((k * 37) % 3) / 2)), yy)], 7, INK, a)

def burst(c, x, y, r, k, col=GOLD, n=10):
    if not (0 < k < 1): return
    for j in range(n):
        a = j * 2 * math.pi / n
        line(c, [(x + math.cos(a) * r * (0.6 + 0.6 * k), y + math.sin(a) * r * (0.6 + 0.6 * k)),
                 (x + math.cos(a) * r * (0.9 + 0.9 * k), y + math.sin(a) * r * (0.9 + 0.9 * k))], 9, col, 1 - k)

def pint(c, x, y, s=1.0, level=0.8, tilt=0):
    c.save(); c.translate(x, y); c.rotate(tilt)
    poly(c, [(-34 * s, -120 * s), (34 * s, -120 * s), (26 * s, 0), (-26 * s, 0)], fill=WHITE, stroke=INK, lw=6 * s)
    top = -120 * s + 120 * s * (1 - level)
    if level > 0.02:
        poly(c, [(-34 * s + 8 * s * (1 - level), top), (34 * s - 8 * s * (1 - level), top), (26 * s, -4 * s), (-26 * s, -4 * s)], fill=GOLD)
        rrect(c, -32 * s, top - 14 * s, 64 * s, 18 * s, 8 * s, fill=WHITE)
    c.restore()

def bar(c, y=1120):
    rrect(c, 40, y - 40, W - 80, 260, 20, fill=(0.45, 0.28, 0.16), stroke=INK, lw=10)
    rrect(c, 40, y - 60, W - 80, 40, 14, fill=(0.58, 0.38, 0.22), stroke=INK, lw=8)
    for k in range(5):
        line(c, [(140 + k * 200, y + 10), (140 + k * 200, y + 190)], 5, INK, 0.25)

WOOD = (0.42, 0.26, 0.15); WOOD2 = (0.56, 0.36, 0.20); WALL = (0.30, 0.20, 0.14)
def pub_bg(c, top=370, bot=1010):
    rrect(c, 0, top, W, bot - top, 0, fill=WALL)
    # warm lamp glow
    for (lx, r_) in ((W * 0.23, 330), (W * 0.77, 330)) if W < 1500 else ((W * 0.15, 360), (W * 0.5, 360), (W * 0.85, 360)):
        g = cairo.RadialGradient(lx, top + 90, 10, lx, top + 90, r_)
        g.add_color_stop_rgba(0, 1.0, 0.82, 0.45, 0.45); g.add_color_stop_rgba(1, 1.0, 0.82, 0.45, 0.0)
        c.set_source(g); c.rectangle(0, top, W, bot - top); c.fill()
        line(c, [(lx, top), (lx, top + 60)], 4, INK)
        poly(c, [(lx - 36, top + 92), (lx - 18, top + 60), (lx + 18, top + 60), (lx + 36, top + 92)], fill=GOLD, stroke=INK, lw=5)
    # shelves with bottles
    for k, sy in enumerate((top + 250, top + 420)):
        rrect(c, 30, sy, W - 60, 22, 4, fill=WOOD2, stroke=INK, lw=5)
        r_ = random.Random(11 + k)
        x_ = 60
        while x_ < W - 90:
            bw = 34 + r_.random() * 18; bh = 90 + r_.random() * 60
            col_ = r_.choice([(0.20, 0.45, 0.25), (0.55, 0.30, 0.12), (0.75, 0.62, 0.25), (0.35, 0.18, 0.12), (0.70, 0.75, 0.78)])
            rrect(c, x_, sy - bh, bw, bh, 8, fill=col_, stroke=INK, lw=4)
            rrect(c, x_ + bw * 0.3, sy - bh - 30, bw * 0.4, 34, 4, fill=col_, stroke=INK, lw=4)
            rrect(c, x_ + 5, sy - bh * 0.6, bw - 10, bh * 0.3, 3, fill=(0.95, 0.92, 0.82))
            x_ += bw + 18 + r_.random() * 26

def bar_front(c, top=1000, bot=1430, pumps=True):
    if pumps:
        for px, cl in ((120, RED), (210, GOLD)):
            rrect(c, px - 22, top - 80, 44, 80, 8, fill=(0.75, 0.62, 0.35), stroke=INK, lw=5)
            rrect(c, px - 14, top - 230, 28, 150, 12, fill=(0.98, 0.95, 0.88), stroke=INK, lw=5)
            rrect(c, px - 22, top - 200, 44, 60, 6, fill=cl, stroke=INK, lw=4)
    rrect(c, 0, top + 20, W, bot - top - 20, 0, fill=WOOD, stroke=INK, lw=10)
    rrect(c, -10, top - 8, W + 20, 40, 10, fill=WOOD2, stroke=INK, lw=8)
    for k in range(4):
        rrect(c, 40 + k * 260, top + 70, 220, bot - top - 130, 14, fill=None, stroke=(0.30, 0.18, 0.10), lw=6)
    line(c, [(20, bot - 30), (W - 20, bot - 30)], 14, GOLD)
    text(c, "THE CALLING TIME · FREE HOUSE", W / 2, top + 75, 34, GOLD, alpha=0.9)

def handbell(c, hx, hy, s=1.0, ang=0):
    c.save(); c.translate(hx, hy); c.rotate(ang)
    rrect(c, -14 * s, -20 * s, 28 * s, 70 * s, 12 * s, fill=WOOD2, stroke=INK, lw=6 * s)
    c.translate(0, 120 * s)
    poly(c, [(-60 * s, 50 * s), (-40 * s, -50 * s), (40 * s, -50 * s), (60 * s, 50 * s)], fill=GOLD, stroke=INK, lw=7 * s)
    rrect(c, -74 * s, 44 * s, 148 * s, 20 * s, 9 * s, fill=GOLD, stroke=INK, lw=6 * s)
    circle(c, math.sin(ang * 4) * 24 * s, 74 * s, 13 * s, fill=INK, stroke=None)
    c.restore()

def bell(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang)
    line(c, [(0, -90 * s), (0, -40 * s)], 8 * s, INK)
    poly(c, [(-50 * s, 40 * s), (-34 * s, -40 * s), (34 * s, -40 * s), (50 * s, 40 * s)], fill=GOLD, stroke=INK, lw=7 * s)
    rrect(c, -62 * s, 34 * s, 124 * s, 18 * s, 8 * s, fill=GOLD, stroke=INK, lw=6 * s)
    circle(c, math.sin(ang * 3) * 20 * s, 60 * s, 12 * s, fill=INK, stroke=None)
    c.restore()

def droplets(c, x, y, t, n=26, spread=1.0, col=(0.75, 0.55, 0.12), d=1, seed=3):
    r = random.Random(seed)
    for j in range(n):
        vx = d * (500 + r.random() * 900) * spread; vy = -350 + r.random() * 420
        xx = x + vx * t; yy = y + vy * t + 900 * t * t
        circle(c, xx, yy, 7 + r.random() * 9, fill=col, stroke=None, a=clamp(1.4 - t * 1.5))
