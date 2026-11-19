# Expressive stickman rig for Calling Time comedy Shorts.
# Same limb system as base.stick, but with a full face kit (eyes/pupils/brows/mouths),
# squash & stretch, and costume pieces for recurring characters.
from base import *

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
    for (lx, r_) in ((250, 330), (830, 330)):
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
