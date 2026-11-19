import cairo, math, json, subprocess, sys, re
from sb import SB
W, H, FPS = 1920, 1080, 30
BG = (0.051, 0.051, 0.059)        # #0D0D0F
INK = (0.96, 0.96, 0.96)          # #F5F5F5
GOLD = (0.788, 0.635, 0.153)      # #C9A227
RED = (0.784, 0.208, 0.180)       # #C8352E
GREY = (0.45, 0.45, 0.48)
DARK = (0.12, 0.12, 0.14)
PAPER = (0.93, 0.91, 0.86)
BLACK = (0.05, 0.05, 0.05)
COL = {"red": RED, "gold": GOLD, "white": INK}
FONT = "Inter"

T = json.load(open('vo/timing.json'))
LINES = T['lines']; WORDS = T['words']; END = T['end']
_FIX = {"Boy,": "Oi!", "Boy": "Oi!", "hold": "hole", "numbers": "members", "spaced": "faced", "bard.": "barred.", "Chabal": "Chappell", "Chapel": "Chappell", "Advisors": "Advisers", "Schapel,": "Chappell,", "Schapel": "Chappell", "Woolworth's.": "Woolworths.", "Advisors": "Advisers", "store's": "stores'"}
_fx = []
for _w in WORDS:
    _w = list(_w)
    if _fx and (_w[0][:1] in (",", ".", "-") and _w[0][1:2].isalnum()):
        _fx[-1] = [_fx[-1][0] + _w[0], _fx[-1][1], _w[2]]; continue
    _w[0] = _FIX.get(_w[0], _w[0])
    if _fx and _fx[-1][0] == "British" and _w[0] == "home": _w[0] = "Home"
    if _fx and _fx[-1][0] == "Home" and _w[0].lower().startswith("store"): _w[0] = "Stores" + _w[0][len("stores"):] if _w[0].lower().startswith("stores") else _w[0]
    _fx.append(_w)
WORDS = _fx
_F2 = {"Mike's": "life", "Schapel's": "Chappell's", "Woolworth's": "Woolworths", "costs": "cost", "whole": "hole", "arrivals": "rivals", "pension's": "Pensions", "In": "in", "From": "from", "On": "on", "By": "by"}
for _k in range(len(WORDS)):
    _w = WORDS[_k]; _p = WORDS[_k - 1][0] if _k else ""
    if _w[0] in ("In", "From", "On", "By") and not re.search(r"[.?!]$", _p) and _k: _w[0] = _F2[_w[0]]
    elif _w[0] in _F2 and _w[0] not in ("In", "From", "On", "By"): _w[0] = _F2[_w[0]]
    if _w[0] == "rivals" and _p == "cheap": WORDS[_k - 1][0] = "cheaper"
    if _w[0] == "Care" and _p == "Mother": WORDS[_k - 1][0] = "Mothercare"; _w[0] = ""
    if _w[0] == "Shop" and _p == "Top": WORDS[_k - 1][0] = "Topshop,"; _w[0] = ""
    if _w[0] == "regulator," and _p == "Pensions": _w[0] = "Regulator,"
    if _w[0] == "Green" and _p == "the" and WORDS[_k + 1][0] == "must": WORDS[_k - 1][0] = "that"
    if _w[0] == "chain" and _p == "the" and WORDS[_k - 2][0] == "When": WORDS[_k - 1][0] = "a"
WORDS = [w for w in WORDS if w[0]]
for _k in range(len(WORDS) - 1):
    if WORDS[_k][0] == "whole" and WORDS[_k + 1][0] == "of": WORDS[_k][0] = "hole"
    if WORDS[_k][0].lower() == "calling" and WORDS[_k + 1][0].lower().startswith("time") and WORDS[_k - 1][0] == "to":
        WORDS[_k][0] = "Calling"; WORDS[_k + 1][0] = "Time" + WORDS[_k + 1][0][4:]
NF = int(math.ceil(END * FPS))

# which entry number each line belongs to (for the corner badge)
ENTRY = []
cur = None
for s, p, _ in SB:
    if s == "num": cur = p["n"]
    if s in ("recap", "end"): cur = None
    ENTRY.append(cur)

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def pop(x):
    x = clamp(x); c = 1.70158 * 1.3
    return max(0.001, 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2)
def lerp(a, b, k): return a + (b - a) * k
def ph(t, a, d=0.45): return clamp((t - a) / d)

def setc(c, col, a=1): c.set_source_rgba(col[0], col[1], col[2], a)

def text(c, s, x, y, size, col=INK, align="center", stroke=None, sw=0, alpha=1, weight="black", spacing=0):
    c.save()
    c.select_font_face(FONT + (" Black" if weight == "black" else ""), cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    if spacing:
        # manual letter spacing
        widths = [c.text_extents(ch).x_advance for ch in s]
        tw = sum(widths) + spacing * (len(s) - 1)
        x0 = x - tw / 2 if align == "center" else (x if align == "left" else x - tw)
        ext = c.text_extents(s)
        y0 = y - (ext.height / 2 + ext.y_bearing)
        for ch, wd in zip(s, widths):
            c.move_to(x0, y0); c.text_path(ch); x0 += wd + spacing
        setc(c, col, alpha); c.fill(); c.restore(); return tw
    ext = c.text_extents(s)
    if align == "center": x0 = x - (ext.width / 2 + ext.x_bearing)
    elif align == "left": x0 = x - ext.x_bearing
    else: x0 = x - ext.width - ext.x_bearing
    y0 = y - (ext.height / 2 + ext.y_bearing)
    c.move_to(x0, y0); c.text_path(s)
    if stroke:
        setc(c, stroke, alpha); c.set_line_width(sw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    setc(c, col, alpha); c.fill(); c.restore()
    return ext.width

def tw(c, s, size):
    c.save(); c.select_font_face(FONT + " Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    w = c.text_extents(s).x_advance; c.restore(); return w

def fit(c, s, size, maxw):
    while size > 20 and tw(c, s, size) > maxw: size -= 4
    return size

def line(c, pts, w=10, col=INK, a=1):
    c.save(); setc(c, col, a); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.stroke(); c.restore()

def circle(c, x, y, r, fill=None, stroke=INK, w=10, a=1):
    c.save(); c.arc(x, y, r, 0, 2 * math.pi)
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(w); c.stroke()
    c.new_path(); c.restore()

def rrect(c, x, y, w, h, r, fill=None, stroke=None, lw=8, a=1):
    r = min(r, w / 2, h / 2)
    c.save(); c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(lw); c.stroke()
    c.new_path(); c.restore()

def poly(c, pts, fill=None, stroke=None, lw=8, a=1):
    c.save(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path()
    if fill: setc(c, fill, a); c.fill_preserve()
    if stroke: setc(c, stroke, a); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.new_path(); c.restore()

def limb(x, y, L, ang):
    r = math.radians(ang); return (x + L * math.sin(r), y + L * math.cos(r))

def stickman(c, x, y, s=1.0, la=(25, 15), ra=(-25, -15), ll=12, rl=-12, tie=False, col=INK, mouth=None,
             helmet=False, sit=False, hat=False, case=False):
    w = 11 * s
    neck = (x, y - 160 * s); hr = 38 * s
    head = (x, neck[1] - hr - 5 * s)
    line(c, [(x, y), neck], w, col)
    if sit:
        k = (x + 70 * s, y + 5 * s); f = (x + 120 * s, y + 20 * s)
        line(c, [(x, y), k, f], w, col)
    else:
        for a in (ll, rl):
            k = limb(x, y, 80 * s, a); f = limb(*k, 80 * s, a * 0.6)
            line(c, [(x, y), k, f], w, col)
    sh = (x, y - 140 * s)
    hands = []
    for (ua, fa) in (la, ra):
        e = limb(*sh, 68 * s, ua); h = limb(*e, 64 * s, fa)
        line(c, [sh, e, h], w, col); hands.append(h)
    circle(c, head[0], head[1], hr, fill=BG, stroke=col, w=w)
    for dx in (-13, 13):
        circle(c, head[0] + dx * s, head[1] - 5 * s, 4.5 * s, fill=col, stroke=None)
    if mouth == "smile":
        c.save(); setc(c, col); c.set_line_width(4.5 * s); c.arc(head[0], head[1] + 5 * s, 15 * s, 0.15 * math.pi, 0.85 * math.pi); c.stroke(); c.restore()
    elif mouth == "o":
        circle(c, head[0], head[1] + 15 * s, 8 * s, fill=col, stroke=None)
    elif mouth == "flat":
        line(c, [(head[0] - 12 * s, head[1] + 17 * s), (head[0] + 12 * s, head[1] + 17 * s)], 4.5 * s, col)
    elif mouth == "sad":
        c.save(); setc(c, col); c.set_line_width(4.5 * s); c.arc(head[0], head[1] + 28 * s, 13 * s, 1.15 * math.pi, 1.85 * math.pi); c.stroke(); c.restore()
    if tie:
        tx, ty = neck[0], neck[1] + 3 * s
        poly(c, [(tx - 8 * s, ty), (tx + 8 * s, ty), (tx + 11 * s, ty + 58 * s), (tx, ty + 72 * s), (tx - 11 * s, ty + 58 * s)], fill=RED)
    if helmet:
        c.save(); setc(c, RED); c.arc(head[0], head[1], hr + 6 * s, math.pi, 2 * math.pi); c.close_path(); c.fill(); c.restore()
        line(c, [(head[0] - hr - 6 * s, head[1]), (head[0] + hr + 6 * s, head[1])], 6 * s, GOLD)
    if hat:
        rrect(c, head[0] - 32 * s, head[1] - hr - 46 * s, 64 * s, 40 * s, 4, fill=INK)
        line(c, [(head[0] - 52 * s, head[1] - hr - 6 * s), (head[0] + 52 * s, head[1] - hr - 6 * s)], 8 * s, INK)
    if case:
        hx, hy = hands[1]
        rrect(c, hx - 40 * s, hy, 80 * s, 60 * s, 8, fill=GOLD, stroke=None)
    return head, hands

def walk(t, sp=6, amp=22):
    a = math.sin(t * sp) * amp
    return a, -a

# ---------------- background + chrome ----------------
def background(c, f):
    setc(c, BG); c.paint()
    # faint grid
    c.save(); setc(c, INK, 0.035); c.set_line_width(1)
    off = (f * 0.4) % 80
    for x in range(-80, W + 80, 80):
        c.move_to(x + off, 0); c.line_to(x + off, H)
    for y in range(0, H, 80):
        c.move_to(0, y); c.line_to(W, y)
    c.stroke(); c.restore()
    # vignette
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.55)
    c.set_source(g); c.paint()

def chrome(c, i):
    text(c, "CALLING TIME", 60, 52, 26, GOLD, align="left", spacing=4)
    n = ENTRY[i]
    if n:
        rrect(c, W - 150, 26, 96, 54, 10, fill=RED)
        text(c, f"#{n}", W - 102, 53, 34, INK)

def capbox(c, s, t, x=W / 2, y=150, col=GOLD):
    if not s: return
    k = ease(ph(t, 0.1, 0.35))
    if k <= 0.01: return
    size = 46
    wdt = tw(c, s, size) + 60
    c.save(); c.translate(x, y); c.scale(1, k)
    rrect(c, -wdt / 2, -38, wdt, 76, 10, fill=col)
    text(c, s, 0, 0, size, BG)
    c.restore()

# ---------------- props ----------------
def vacuum(c, x, y, s=1):
    line(c, [(x, y - 260 * s), (x + 40 * s, y - 40 * s)], 12 * s, INK)
    rrect(c, x + 10 * s, y - 160 * s, 70 * s, 130 * s, 18 * s, fill=RED, stroke=INK, lw=6 * s)
    rrect(c, x - 10 * s, y - 40 * s, 140 * s, 40 * s, 12 * s, fill=GREY, stroke=INK, lw=6 * s)
    circle(c, x + 10 * s, y + 4 * s, 10 * s, fill=INK, stroke=None); circle(c, x + 110 * s, y + 4 * s, 10 * s, fill=INK, stroke=None)

def plane(c, x, y, s=1, col=INK, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -150, -22, 300, 44, 22, fill=col)
    poly(c, [(-20, 0), (60, 0), (-40, -110), (-80, -110)], fill=col)
    poly(c, [(-20, 0), (60, 0), (-40, 110), (-80, 110)], fill=col)
    poly(c, [(-150, -10), (-110, -10), (-140, -70), (-165, -70)], fill=col)
    for k in range(5): circle(c, 40 + k * -32, -4, 6, fill=BG, stroke=None)
    c.restore()

def bottle(c, x, y, s=1, label="PURE", water=1.0):
    # body
    bw, bh = 170 * s, 380 * s
    rrect(c, x - bw / 2, y - bh, bw, bh, 30 * s, fill=(0.2, 0.35, 0.5), stroke=INK, lw=7 * s)
    if water < 1:
        rrect(c, x - bw / 2 + 6, y - bh + 6, bw - 12, (bh - 12) * (1 - water), 26 * s, fill=BG)
    rrect(c, x - 40 * s, y - bh - 70 * s, 80 * s, 80 * s, 10 * s, fill=(0.2, 0.35, 0.5), stroke=INK, lw=7 * s)
    rrect(c, x - 46 * s, y - bh - 100 * s, 92 * s, 36 * s, 8 * s, fill=INK)
    rrect(c, x - bw / 2 - 4, y - bh * 0.62, bw + 8, 110 * s, 6, fill=INK)
    text(c, label, x, y - bh * 0.62 + 55 * s, fit(c, label, 44 * s, bw - 20), BG)

def tap(c, x, y, s=1, drip_t=0):
    rrect(c, x - 140 * s, y - 30 * s, 160 * s, 50 * s, 12, fill=GREY, stroke=INK, lw=6)
    rrect(c, x, y - 30 * s, 50 * s, 110 * s, 12, fill=GREY, stroke=INK, lw=6)
    rrect(c, x - 90 * s, y - 70 * s, 60 * s, 40 * s, 8, fill=GREY, stroke=INK, lw=6)
    for k in range(3):
        dy = ((drip_t * 1.2 + k / 3) % 1) * 220 * s
        circle(c, x + 25 * s, y + 95 * s + dy, 9 * s, fill=(0.4, 0.65, 0.95), stroke=None)

def building(c, x, y, w, h, label=None, col=INK, fill=DARK, cols=True):
    poly(c, [(x - 20, y - h), (x + w / 2, y - h - 110), (x + w + 20, y - h)], fill=fill, stroke=col, lw=7)
    rrect(c, x, y - h, w, h, 4, fill=fill, stroke=col, lw=7)
    if cols:
        n = 5
        for k in range(n):
            cx = x + w * (k + 0.5) / n
            line(c, [(cx, y - h + 40), (cx, y - 20)], 14, col, 0.8)
    if label: text(c, label, x + w / 2, y - h - 150, fit(c, label, 44, w + 100), GOLD)

def shopfront(c, x, y, w, h, name, sign=RED, shutter=0.0, a=1):
    rrect(c, x, y - h, w, h, 8, fill=DARK, stroke=INK, lw=6, a=a)
    rrect(c, x + 8, y - h + 8, w - 16, 70, 6, fill=sign, a=a)
    text(c, name, x + w / 2, y - h + 43, fit(c, name, 44, w - 40), INK, alpha=a)
    # window + door
    rrect(c, x + 20, y - h + 100, w * 0.5, h - 130, 6, fill=(0.2, 0.3, 0.38), stroke=INK, lw=4, a=a)
    rrect(c, x + w * 0.62, y - h + 100, w * 0.3, h - 100, 6, fill=(0.25, 0.2, 0.15), stroke=INK, lw=4, a=a)
    if shutter > 0:
        sh = (h - 80) * shutter
        rrect(c, x + 6, y - h + 80, w - 12, sh, 2, fill=GREY, a=a)
        c.save(); setc(c, BG, 0.5); c.set_line_width(3)
        yy = y - h + 80 + 14
        while yy < y - h + 80 + sh:
            c.move_to(x + 8, yy); c.line_to(x + w - 8, yy); yy += 18
        c.stroke(); c.restore()

def note(c, x, y, s=1, ang=0, col=(0.35, 0.6, 0.35)):
    c.save(); c.translate(x, y); c.rotate(ang)
    rrect(c, -60 * s, -32 * s, 120 * s, 64 * s, 6, fill=col, stroke=INK, lw=3)
    text(c, "£", 0, 0, 40 * s, INK)
    c.restore()

def coin(c, x, y, r=40, lab="£"):
    circle(c, x, y, r, fill=GOLD, stroke=INK, w=5)
    text(c, lab, x, y, r * 1.1, BG)

def suitcase(c, x, y, s=1, col=GOLD):
    rrect(c, x - 38 * s, y - 56 * s, 76 * s, 56 * s, 8, fill=col, stroke=INK, lw=4)
    line(c, [(x - 14 * s, y - 56 * s), (x - 14 * s, y - 70 * s), (x + 14 * s, y - 70 * s), (x + 14 * s, y - 56 * s)], 5, INK)

def board(c, x, y, w, rows, t):
    rrect(c, x, y, w, 70 + 60 * len(rows), 10, fill=(0.08, 0.08, 0.1), stroke=INK, lw=5)
    text(c, "DEPARTURES", x + w / 2, y + 38, 36, GOLD, spacing=3)
    for k, r in enumerate(rows):
        yy = y + 100 + k * 60
        text(c, r, x + 30, yy, 32, INK, align="left")
        if ph(t, 0.5 + k * 0.35, 0.2) > 0:
            on = int(t * 3) % 2 == 0 or t > 2.5
            text(c, "CANCELLED", x + w - 30, yy, 32, RED, align="right", alpha=1 if on else 0.35)

def train(c, x, y, s=1):
    rrect(c, x, y - 150 * s, 260 * s, 150 * s, 10, fill=DARK, stroke=INK, lw=6)
    rrect(c, x + 180 * s, y - 230 * s, 80 * s, 80 * s, 6, fill=DARK, stroke=INK, lw=6)
    rrect(c, x + 20 * s, y - 220 * s, 50 * s, 70 * s, 4, fill=GREY, stroke=INK, lw=5)
    for k in range(3): circle(c, x + (50 + k * 80) * s, y + 10 * s, 30 * s, fill=BG, stroke=INK, w=6)
    for car in range(2):
        cx = x - (300 + car * 300) * s
        rrect(c, cx, y - 140 * s, 280 * s, 140 * s, 10, fill=RED if car == 0 else GOLD, stroke=INK, lw=6)
        for k in range(3): rrect(c, cx + (25 + k * 85) * s, y - 115 * s, 60 * s, 50 * s, 4, fill=BG)
        for k in (60, 220): circle(c, cx + k * s, y + 10 * s, 26 * s, fill=BG, stroke=INK, w=6)
        line(c, [(cx + 280 * s, y - 40 * s), (cx + 300 * s, y - 40 * s)], 8, INK)

def dome(c, x, y, r, lit=False, t=0):
    if lit:
        for k in range(6):
            a = math.pi * (1.15 + 0.7 * k / 5)
            ln = r * (1.5 + 0.15 * math.sin(t * 4 + k))
            line(c, [(x, y - r * 0.9), (x + math.cos(a) * ln, y + math.sin(a) * ln)], 18, [RED, GOLD, INK][k % 3], 0.25)
    c.save(); c.arc(x, y, r, math.pi, 2 * math.pi); c.close_path()
    setc(c, (0.92, 0.92, 0.9) if not lit else (0.25, 0.22, 0.3)); c.fill_preserve(); setc(c, INK); c.set_line_width(6); c.stroke(); c.restore()
    for k in range(12):
        a = math.pi + math.pi * (k + 0.5) / 12
        px, py = x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82
        line(c, [(px, py + 30), (px + math.cos(a) * 140, py + math.sin(a) * 140 - 40)], 7, GOLD)

# ---------------- stick scenes ----------------
GROUND = 720

def floor(c):
    line(c, [(120, GROUND + 160), (W - 120, GROUND + 160)], 5, INK, 0.25)

def scene_stick(c, p, t, d):
    k = p["kind"]; bob = math.sin(t * 3) * 4
    G = GROUND
    if k == "vacuum":
        vx = 760 + 20 * math.sin(t * 2.5)
        stickman(c, vx - 110, G + bob, la=(40, 60), ra=(55, 70), mouth="smile")
        vacuum(c, vx, G + 160)
        px = -300 + (W + 600) * ease_io(ph(t, 0.3, max(1.0, d - 0.5)))
        c.save(); setc(c, INK, 0.3); c.set_dash([18, 18]); c.set_line_width(5)
        c.move_to(-200, 420); c.line_to(px, 420 - (px + 200) * 0.12); c.stroke(); c.restore()
        plane(c, px, 420 - (px + 200) * 0.12, 0.9, GOLD, -0.12)
    elif k == "bottle":
        bottle(c, W / 2 + 160, G + 140, 1.0, "PURE?")
        tap(c, W / 2 + 160, 360, 1.0, t)
        stickman(c, 600, G + bob, la=(30, 20), ra=(-150, -170), mouth="o")
        sc = pop(ph(t, 0.6, 0.4))
        if sc > 0.02:
            c.save(); c.translate(560, 470); c.scale(sc, sc); text(c, "?", 0, 0, 140, GOLD); c.restore()
    elif k == "stranded":
        board(c, 1060, 230, 700, ["MALAGA", "PALMA", "ORLANDO", "LANZAROTE"], t)
        for j in range(5):
            x = 230 + j * 150
            stickman(c, x, G + 20 + math.sin(t * 2 + j) * 3, s=0.8, la=(15, 10), ra=(-15, -10), mouth="sad", case=True)
    elif k == "present":
        # spotlight
        c.save(); setc(c, GOLD, 0.08); c.move_to(W / 2 - 60, 0); c.line_to(W / 2 + 60, 0); c.line_to(W / 2 + 330, G + 160); c.line_to(W / 2 - 330, G + 160); c.close_path(); c.fill(); c.restore()
        wave = 20 * math.sin(t * 3)
        stickman(c, W / 2, G - 20 + bob, la=(30, 20), ra=(-110 + wave, -150 + wave), tie=True, mouth="smile")
        poly(c, [(W / 2 - 120, G + 20), (W / 2 + 120, G + 20), (W / 2 + 95, G + 160), (W / 2 - 95, G + 160)], fill=(0.3, 0.2, 0.12), stroke=INK, lw=5)
        text(c, p.get("label", ""), W / 2, G + 90, 44, GOLD)
        for j in range(14):
            hx = 140 + j * 130
            circle(c, hx, G + 205 + (j % 2) * 10, 34, fill=DARK, stroke=INK, w=5, a=0.9)
    elif k == "c5":
        x = -250 + 1400 * ease(ph(t, 0.0, d * 0.8))
        # lorry bumper on right
        rrect(c, 1450, 360, 520, 520, 10, fill=(0.2, 0.2, 0.23), stroke=INK, lw=6)
        rrect(c, 1430, 760, 540, 70, 6, fill=GREY, stroke=INK, lw=6)
        circle(c, 1600, 880, 110, fill=BG, stroke=INK, w=12); circle(c, 1600, 880, 40, fill=GREY, stroke=None)
        text(c, "LORRY", 1710, 560, 60, INK, alpha=0.5)
        # C5 body
        cx, cy = x, G + 120
        poly(c, [(cx - 170, cy + 20), (cx + 150, cy + 20), (cx + 170, cy - 30), (cx - 60, cy - 70), (cx - 170, cy - 20)], fill=INK, stroke=INK, lw=4)
        circle(c, cx - 120, cy + 40, 32, fill=BG, stroke=INK, w=8); circle(c, cx + 120, cy + 40, 32, fill=BG, stroke=INK, w=8)
        stickman(c, cx - 60, cy - 50, s=0.75, la=(-60, -80), ra=(-60, -80), sit=True, mouth="o")
        for j in range(3): line(c, [(cx - 220 - j * 40, cy - 40 + j * 25), (cx - 300 - j * 40, cy - 40 + j * 25)], 6, GOLD, 0.6)
    elif k == "computer":
        rrect(c, 820, 430, 620, 380, 16, fill=DARK, stroke=INK, lw=8)
        rrect(c, 850, 460, 560, 320, 8, fill=(0.15, 0.17, 0.22))
        # globe
        gx, gy = 1130, 600
        circle(c, gx, gy, 110, fill=None, stroke=GOLD, w=6)
        c.save(); setc(c, GOLD); c.set_line_width(5); c.save(); c.translate(gx, gy); c.scale(0.45 + 0.4 * abs(math.sin(t)), 1); c.arc(0, 0, 110, 0, 2 * math.pi); c.restore(); c.stroke(); c.restore()
        line(c, [(gx - 110, gy), (gx + 110, gy)], 5, GOLD)
        rrect(c, 760, 810, 740, 30, 10, fill=GREY, stroke=INK, lw=5)
        stickman(c, 560, G + bob, la=(-40, -70), ra=(-60, -80), tie=True, mouth="smile")
        for j in range(4):
            b = pop(ph(t, 0.5 + j * 0.4, 0.35))
            if b > 0.02:
                c.save(); c.translate(1560 + (j % 2) * 150, 380 + (j // 2) * 220); c.scale(b, b)
                rrect(c, -55, -50, 110, 100, 10, fill=[RED, GOLD][j % 2], stroke=INK, lw=4)
                line(c, [(-25, -50), (-25, -75), (25, -75), (25, -50)], 6, INK); c.restore()
    elif k == "money":
        stickman(c, W / 2, G + bob, la=(-130 + 20 * math.sin(t * 6), -160), ra=(130 - 20 * math.sin(t * 6), 160), tie=True, mouth="smile")
        for j in range(16):
            ph0 = (t * 0.7 + j / 16) % 1
            ang = (j * 137.5) % 360
            r = 80 + 700 * ph0
            x = W / 2 + math.cos(math.radians(ang)) * r
            y = G - 250 + math.sin(math.radians(ang)) * r * 0.55 + 300 * ph0 ** 2
            note(c, x, y, 0.9, ph0 * 6 + j)
    elif k == "loading":
        rrect(c, 760, 300, 760, 460, 16, fill=DARK, stroke=INK, lw=8)
        text(c, "LOADING…", 1140, 440, 64, INK)
        prog = 0.04 + 0.12 * ph(t, 0, d)
        rrect(c, 840, 540, 600, 50, 25, fill=None, stroke=INK, lw=5)
        rrect(c, 846, 546, 588 * prog, 38, 19, fill=RED)
        text(c, "56K MODEM", 1140, 680, 40, GOLD, spacing=3)
        foot = 12 * abs(math.sin(t * 5))
        stickman(c, 480, G + bob, la=(30, 60), ra=(-30, -60), ll=12 + foot, mouth="flat")
        # clock
        circle(c, 300, 330, 90, fill=DARK, stroke=INK, w=8)
        a = t * 2.5
        line(c, [(300, 330), (300 + math.sin(a) * 70, 330 - math.cos(a) * 70)], 7, RED)
        line(c, [(300, 330), (300 + math.sin(a / 12) * 45, 330 - math.cos(a / 12) * 45)], 9, INK)
    elif k == "markup":
        tap(c, 420, 380, 0.9, t)
        text(c, "TAP", 420, 720, 60, INK)
        a1 = ease(ph(t, 0.4, 0.5))
        line(c, [(600, 560), (600 + 260 * a1, 560)], 12, GOLD)
        if a1 > 0.95: poly(c, [(870, 560), (840, 535), (840, 585)], fill=GOLD)
        if ph(t, 0.8, 0.3) > 0:
            bottle(c, 1080, G + 120, 0.85, "PURE?")
        a2 = ease(ph(t, 1.4, 0.5))
        if a2 > 0:
            line(c, [(1240, 560), (1240 + 240 * a2, 560)], 12, GOLD)
        sc = pop(ph(t, 1.9, 0.4))
        if sc > 0.02:
            c.save(); c.translate(1640, 560); c.scale(sc, sc); c.rotate(-0.1)
            rrect(c, -150, -80, 300, 160, 14, fill=RED, stroke=INK, lw=6)
            text(c, "£££", 0, 0, 90, INK); c.restore()
    elif k == "factory":
        rrect(c, 520, 380, 640, 420, 12, fill=DARK, stroke=INK, lw=8)
        for j in range(3):
            g = (t * 2 + j * 2.1)
            cx_, cy_ = 640 + j * 200, 520
            circle(c, cx_, cy_, 60, fill=None, stroke=GOLD, w=8)
            line(c, [(cx_, cy_), (cx_ + math.cos(g) * 60, cy_ + math.sin(g) * 60)], 8, GOLD)
        text(c, "PURIFICATION", 840, 700, 48, INK, spacing=2)
        line(c, [(1160, 760), (1800, 760)], 10, GREY)
        bx = 1220 + ((t * 120) % 500)
        bottle(c, bx, 740, 0.45, "")
        sc = pop(ph(t, 0.8, 0.4))
        if sc > 0.02:
            c.save(); c.translate(1560, 420); c.scale(sc, sc)
            poly(c, [(0, -120), (120, 90), (-120, 90)], fill=GOLD, stroke=INK, lw=8)
            text(c, "!", 0, 20, 130, BG); c.restore()
            text(c, "BROMATE", 1560, 580, 52, RED, alpha=ease(ph(t, 1.0, 0.4)))
    elif k == "vacpile":
        n = int(min(9, 1 + t * 3))
        for j in range(n):
            col_, row = j % 3, j // 3
            x = 1100 + col_ * 190; y = G + 160 - (row + 1) * 150
            rrect(c, x, y, 180, 140, 6, fill=(0.45, 0.32, 0.18), stroke=INK, lw=5)
            text(c, "VACUUM", x + 90, y + 70, 30, INK)
        stickman(c, 650, G + bob, la=(-70, -90), ra=(-70, -90), mouth="smile")
        rrect(c, 700, G - 240, 180, 140, 6, fill=(0.45, 0.32, 0.18), stroke=INK, lw=5)
        sc = pop(ph(t, 0.6, 0.4))
        if sc > 0.02:
            c.save(); c.translate(420, 380); c.scale(sc, sc); c.rotate(-0.15)
            rrect(c, -150, -60, 300, 120, 10, fill=GOLD, stroke=INK, lw=5)
            text(c, "2 x TICKETS", 0, 0, 38, BG); c.restore()
    elif k == "court":
        rrect(c, 700, 420, 520, 260, 8, fill=(0.3, 0.2, 0.12), stroke=INK, lw=6)
        stickman(c, 960, 520, s=0.8, la=(30, 20), ra=(-100, -130 + 40 * abs(math.sin(t * 4))), mouth="flat")
        rrect(c, 790, 640, 340, 100, 8, fill=(0.3, 0.2, 0.12), stroke=INK, lw=6)
        for j, x in enumerate([260, 420, 1500, 1660]):
            stickman(c, x, G + bob * (1 if j % 2 else -1), s=0.85, la=(-120, -150) if j == 1 else (25, 10), ra=(-25, -10), mouth="flat")
    elif k == "dome":
        dome(c, W / 2, G + 120, 520)
        for j in range(4):
            stickman(c, 300 + j * 90, G + 140, s=0.45, la=(20, 10), ra=(-20, -10))
    elif k == "arena":
        dome(c, W / 2, G + 120, 520, lit=True, t=t)
        for j in range(7):
            nx = 400 + j * 190; ny = 300 - ((t * 60 + j * 40) % 200)
            circle(c, nx, ny, 18, fill=[GOLD, RED, INK][j % 3], stroke=None); line(c, [(nx + 16, ny), (nx + 16, ny - 70), (nx + 46, ny - 50)], 6, [GOLD, RED, INK][j % 3])
    elif k == "shops":
        names = p.get("names", ["SHOP"] * 4)
        for j in range(4):
            sc = pop(ph(t, 0.15 + j * 0.25, 0.4))
            if sc <= 0.02: continue
            x = 180 + j * 410
            c.save(); c.translate(x + 180, G + 160); c.scale(sc, sc); c.translate(-(x + 180), -(G + 160))
            shopfront(c, x, G + 160, 360, 460, names[j], sign=RED if names[j] == "BHS" else GREY)
            c.restore()
    elif k == "sandwich":
        # scale
        ang = -0.25 * ease(ph(t, 0.6, 0.8))
        cx_, cy_ = W / 2, 520
        poly(c, [(cx_ - 50, G + 160), (cx_ + 50, G + 160), (cx_, cy_)], fill=GREY, stroke=INK, lw=5)
        dx, dy = math.cos(ang) * 420, math.sin(ang) * 420
        line(c, [(cx_ - dx, cy_ - dy), (cx_ + dx, cy_ + dy)], 12, INK)
        for side, lab in ((-1, "EARRINGS"), (1, "PRAWN SANDWICH")):
            px, py = cx_ + side * dx, cy_ + side * dy
            line(c, [(px, py), (px - 90, py + 160)], 4, INK); line(c, [(px, py), (px + 90, py + 160)], 4, INK)
            line(c, [(px - 120, py + 160), (px + 120, py + 160)], 10, INK)
            if side < 0:
                for e in (-30, 30):
                    circle(c, px + e, py + 115, 22, fill=GOLD, stroke=INK, w=4)
            else:
                poly(c, [(px - 80, py + 150), (px + 80, py + 150), (px - 80, py + 60)], fill=PAPER, stroke=INK, lw=5)
                line(c, [(px - 70, py + 75), (px + 50, py + 140)], 10, (0.95, 0.55, 0.45))
            text(c, lab, px, py + 220, 40, GOLD)
    elif k == "bank":
        building(c, 760, G + 160, 400, 380, "BANK")
        for j in range(3):
            ph0 = (t * 0.6 + j / 3) % 1
            coin(c, 380 + 360 * ph0, G - 80, 30)
            hx = 1200 + 420 * ph0
            poly(c, [(hx - 40, G), (hx + 40, G), (hx + 40, G - 60), (hx, G - 100), (hx - 40, G - 60)], fill=GOLD, stroke=INK, lw=4)
        text(c, "SAVERS' DEPOSITS", 470, G + 60, 36, INK)
        text(c, "MORTGAGES", 1500, G + 60, 36, INK)
    elif k == "wholesale":
        building(c, 760, G + 160, 400, 380, "NORTHERN ROCK")
        # cloud
        for (ox, oy, r) in ((-90, 0, 90), (0, -50, 110), (100, 0, 90), (0, 30, 90)):
            circle(c, 380 + ox, 330 + oy, r, fill=DARK, stroke=None)
        text(c, "MONEY MARKETS", 380, 340, 40, GOLD)
        for j in range(4):
            ph0 = (t * 0.8 + j / 4) % 1
            note(c, 480 + 360 * ph0, 400 + 200 * ph0, 0.7, 0)
        for j in range(3):
            ph0 = (t * 0.6 + j / 3) % 1
            hx = 1200 + 420 * ph0
            poly(c, [(hx - 40, G), (hx + 40, G), (hx + 40, G - 60), (hx, G - 100), (hx - 40, G - 60)], fill=GOLD, stroke=INK, lw=4)
    elif k == "queue":
        building(c, 1350, G + 160, 420, 400, "NORTHERN ROCK")
        n = 11
        for j in range(n):
            x = 1290 - j * 105
            stickman(c, x, G + 30 + math.sin(t * 3 + j) * 3, s=0.72, la=(20, 10), ra=(-20, -10), mouth=["flat", "o", "sad"][j % 3])
    elif k == "shop":
        shopfront(c, 660, G + 160, 600, 560, p.get("name", "SHOP"), sign=RED)
        for j in range(3):
            stickman(c, 380 + j * 1100 / 2 * (j > 0) + (j > 1) * 50, G + bob, s=0.8, mouth="smile", la=(20, 10), ra=(-20, -10))
    elif k == "leaseback":
        shopfront(c, 560, G + 160, 520, 520, p.get("name", "SHOP"), sign=RED)
        s1 = pop(ph(t, 0.4, 0.4))
        if s1 > 0.02:
            c.save(); c.translate(1500, 300); c.scale(s1, s1); c.rotate(-0.08)
            rrect(c, -170, -55, 340, 110, 8, fill=RED, stroke=INK, lw=5); text(c, "SOLD", 0, 0, 70, INK); c.restore()
        s2 = pop(ph(t, 1.6, 0.4))
        if s2 > 0.02:
            c.save(); c.translate(1500, 450); c.scale(s2, s2); c.rotate(0.06)
            rrect(c, -200, -50, 400, 100, 8, fill=GOLD, stroke=INK, lw=5); text(c, "RENT DUE", 0, 0, 60, BG); c.restore()
        bx = 1300 + 450 * ease_io(ph(t, 0.8, 1.6))
        circle(c, bx, G + 60, 100, fill=GOLD, stroke=INK, w=6); text(c, "£", bx, G + 70, 110, BG)
    elif k == "shutters":
        for j in range(3):
            x = 170 + j * 540
            shopfront(c, x, G + 160, 500, 520, p.get("name", "SHOP"), sign=RED, shutter=ease(ph(t, 0.3 + j * 0.5, 0.9)))
        sc = pop(ph(t, 1.8, 0.4))
        if sc > 0.02:
            c.save(); c.translate(W / 2, 560); c.scale(sc, sc); c.rotate(-0.06)
            rrect(c, -380, -70, 760, 140, 10, fill=RED, stroke=INK, lw=6); text(c, "CLOSING DOWN", 0, 0, 80, INK); c.restore()
    elif k == "racer":
        stickman(c, 800, G + bob, la=(30, 20), ra=(-120, -160), helmet=True, mouth="smile")
        # chequered flag
        fx, fy = 1000, 300
        line(c, [(fx - 140, fy + 300), (fx - 140, fy - 20)], 8, INK)
        wv = math.sin(t * 5) * 10
        for r in range(4):
            for q in range(6):
                col_ = INK if (r + q) % 2 == 0 else BG
                rrect(c, fx - 140 + q * 40, fy + r * 40 + wv * (q / 6), 40, 40, 0, fill=col_)
        sc = pop(ph(t, 0.6, 0.4))
        if sc > 0.02:
            c.save(); c.translate(1350, 600); c.scale(sc, sc); coin(c, 0, 0, 110, "£1"); c.restore()
    elif k == "train":
        x = -200 + (W - 200) * ease(ph(t, 0, d * 0.9))
        line(c, [(0, G + 70), (W, G + 70)], 8, GREY)
        train(c, x, G + 30, 1.0)
        for j in range(4):
            r = 30 + j * 25 + ((t * 40) % 40)
            circle(c, x + 220 - j * 60, G - 260 - j * 50, r, fill=INK, stroke=None, a=0.25)
    elif k == "merge2":
        m = ease_io(ph(t, 0.3, 1.2))
        for j, (nm, x0) in enumerate(((p["a"], 160), (p["b"], 760), (p["c"], 1360))):
            x = lerp(x0, 760, m * 0.0) + (760 - x0) * m * 0.35
            building(c, x, G + 160, 400, 340, nm, cols=True)
        if m >= 0.99:
            sc = pop(ph(t, 1.5, 0.4))
            if sc > 0.02:
                c.save(); c.translate(W / 2, 300); c.scale(sc, sc)
                rrect(c, -300, -60, 600, 120, 14, fill=GOLD); text(c, "STOREHOUSE", 0, 0, 72, BG); c.restore()
    elif k == "pension":
        lev = p.get("level", 0.5)
        x0, y0 = 760, G + 160
        rrect(c, x0 - 10, y0 - 560, 420, 560, 50, fill=DARK, stroke=INK, lw=8)
        rrect(c, x0 + 50, y0 - 610, 300, 60, 14, fill=GREY, stroke=INK, lw=6)
        cur = lev
        if p.get("cap", "").startswith("THE PENSION HOLE"): cur = lerp(0.8, lev, ease(ph(t, 0.2, max(0.5, d - 0.6))))
        if p.get("cap", "").startswith("THE SETTLEMENT"): cur = lerp(0.15, lev, ease(ph(t, 0.4, max(0.5, d - 0.8))))
        fh = 500 * cur
        rrect(c, x0 + 15, y0 - 25 - fh, 370, fh, 30, fill=(0.25, 0.6, 0.35))
        rrect(c, x0 + 40, y0 - 360, 320, 90, 10, fill=PAPER, stroke=INK, lw=5); text(c, "PENSION", x0 + 200, y0 - 315, 56, BG)
        stickman(c, 480, G + bob, s=0.9, la=(25, 15), ra=(-25, -15), mouth="smile" if cur > 0.6 else "sad")
        stickman(c, 1430, G + bob, s=0.9, la=(25, 15), ra=(-25, -15), mouth="smile" if cur > 0.6 else "sad")
    elif k == "sale":
        k1 = ease(ph(t, 0.2, 0.6))
        stickman(c, 620, G + bob, la=(30, 20), ra=(-85 + 20 * (1 - k1), -10), tie=True, mouth="smile")
        stickman(c, 1300, G + bob, la=(85 - 20 * (1 - k1), 10), ra=(-30, -20), mouth="smile", helmet=True)
        sc = pop(ph(t, 0.7, 0.4))
        if sc > 0.02:
            c.save(); c.translate(W / 2, 400); c.scale(sc, sc); coin(c, 0, 0, 130, "£1"); c.restore()
        shopfront(c, 60, G + 160, 300, 380, "BHS", sign=RED)
    elif k == "jail":
        stickman(c, W / 2, G + bob, la=(40, 30), ra=(-40, -30), mouth="sad", helmet=True)
        kk = ease(ph(t, 0.2, 0.5))
        top = lerp(-200, 260, kk)
        rrect(c, W / 2 - 360, top, 720, G + 160 - top, 10, fill=None, stroke=GREY, lw=12)
        for j in range(9): line(c, [(W / 2 - 320 + j * 80, top), (W / 2 - 320 + j * 80, G + 160)], 12, GREY)
        sc = pop(ph(t, 0.9, 0.4))
        if sc > 0.02:
            c.save(); c.translate(W / 2 + 520, 360); c.scale(sc, sc); c.rotate(-0.08)
            rrect(c, -190, -60, 380, 120, 10, fill=RED); text(c, "6 YEARS", 0, 0, 72, INK); c.restore()
    elif k == "merge":
        m = ease_io(ph(t, 0.3, 1.2))
        building(c, 300 + 260 * m, G + 160, 360, 340, "THOMAS COOK", cols=True)
        building(c, 1260 - 260 * m, G + 160, 360, 340, "MYTRAVEL", cols=True)
        if m >= 0.99:
            sc = pop(ph(t, 1.6, 0.4))
            if sc > 0.02:
                c.save(); c.translate(W / 2, 330); c.scale(sc, sc)
                circle(c, 0, 0, 120, fill=DARK, stroke=RED, w=10); text(c, "DEBT", 0, 0, 64, RED); c.restore()
                line(c, [(W / 2, 450), (W / 2, 560)], 8, RED)
    elif k == "planes":
        for j in range(4):
            ph0 = (t * 0.25 + j / 4) % 1
            plane(c, -300 + (W + 600) * ph0, 260 + j * 110, 0.55, [GOLD, INK, RED, INK][j], -0.06)
        for j in range(8):
            stickman(c, 260 + j * 200, G + 60 + math.sin(t * 2 + j) * 3, s=0.6, la=(20, 10), ra=(-20, -10), case=True)
    capbox(c, p.get("cap"), t)

ENTRY_NOW = [None]

# ---------------- other scene templates ----------------
def parse_val(v):
    m = re.match(r'^([£$\-]*)([\d,]*\.?\d+)(.*)$', v)
    if not m: return None
    pre, num, suf = m.groups()
    dec = len(num.split('.')[1]) if '.' in num else 0
    return pre, float(num.replace(',', '')), suf, (',' in num), dec

def fmt(pre, x, suf, comma, dec):
    s = f"{x:,.{dec}f}" if comma else f"{x:.{dec}f}"
    return f"{pre}{s}{suf}"

def scene_stat(c, p, t, d):
    col = COL[p.get("col", "gold")]
    v = p["v"]; pv = parse_val(v)
    k = ease(ph(t, 0.05, 0.9))
    if pv and not (pv[1] >= 1800 and pv[1] <= 2030 and not pv[0] and not pv[2]):
        pre, num, suf, comma, dec = pv
        shown = fmt(pre, num * k if k < 1 else num, suf, comma, dec)
    else:
        shown = v
    sc = pop(ph(t, 0.0, 0.45))
    size = fit(c, v, 300, W - 240)
    c.save(); c.translate(W / 2, 470); c.scale(sc, sc)
    text(c, shown, 0, 0, size, col)
    c.restore()
    a = ease(ph(t, 0.35, 0.4))
    lab = p.get("label", "")
    ls = fit(c, lab, 50, W - 260)
    text(c, lab, W / 2, 720, ls, INK, alpha=a, spacing=2)
    line(c, [(W / 2 - 300 * a, 790), (W / 2 + 300 * a, 790)], 6, col, a)

def scene_vs(c, p, t, d):
    (la, va), (lb, vb) = p["a"], p["b"]
    mx = max(va, vb)
    for j, (lab, val, col) in enumerate(((la, va, GREY), (lb, vb, RED))):
        y = 360 + j * 250
        g = ease_io(ph(t, 0.15 + j * 0.6, 0.9))
        text(c, lab, 200, y - 70, 44, INK, align="left", spacing=2)
        rrect(c, 200, y - 30, 1300, 110, 12, fill=DARK)
        wbar = max(1, 1300 * (val / mx) * g)
        rrect(c, 200, y - 30, wbar, 110, 12, fill=col)
        dec = 1 if (val != int(val)) else 0
        num = f"{val * g:,.{dec}f}" if not p.get("plain") else f"{val * g:,.0f}"
        text(c, num, min(200 + wbar + 30, 1540), y + 25, 76, INK if g > 0 else BG, align="left")
    if p.get("note"):
        text(c, p["note"], W / 2, 860, 30, GREY, weight="regular")

def scene_head(c, p, t, d):
    sc = pop(ph(t, 0.0, 0.45)); rot = (1 - ease(ph(t, 0, 0.45))) * -0.5 - 0.03
    c.save(); c.translate(W / 2, 520); c.rotate(rot); c.scale(sc, sc)
    rrect(c, -760, -330, 1520, 640, 6, fill=PAPER)
    text(c, "THE BUSINESS PAGES", 0, -260, 54, BLACK, spacing=6)
    line(c, [(-700, -210), (700, -210)], 4, BLACK)
    line(c, [(-700, -200), (700, -200)], 2, BLACK)
    hs = fit(c, p["h"], 120, 1360)
    words = p["h"]
    if hs < 80 and len(words) > 22:
        sp = words.split(" "); half = len(sp) // 2
        l1, l2 = " ".join(sp[:half]), " ".join(sp[half:])
        hs = min(fit(c, l1, 120, 1360), fit(c, l2, 120, 1360))
        text(c, l1, 0, -80, hs, BLACK); text(c, l2, 0, 40, hs, BLACK)
    else:
        text(c, words, 0, -30, hs, BLACK)
    text(c, p.get("sub", ""), 0, 150, 44, RED, weight="regular")
    for j in range(3):
        line(c, [(-700, 220 + j * 30), (700 - j * 200, 220 + j * 30)], 10, GREY, 0.6)
    c.restore()

def scene_date(c, p, t, d):
    sc = pop(ph(t, 0.0, 0.45))
    c.save(); c.translate(W / 2, 470); c.scale(sc, sc)
    rrect(c, -520, -200, 1040, 400, 20, fill=DARK, stroke=INK, lw=6)
    rrect(c, -520, -200, 1040, 90, 20, fill=RED)
    for x in (-350, 350): circle(c, x, -200, 22, fill=BG, stroke=INK, w=6)
    ds = fit(c, p["d"], 150, 960)
    text(c, p["d"], 0, 50, ds, GOLD)
    c.restore()
    s2 = ease(ph(t, 0.55, 0.25))
    if s2 > 0:
        st = 2.2 - 1.2 * s2
        c.save(); c.translate(W / 2 + 260, 770); c.rotate(-0.12); c.scale(st, st)
        ws = fit(c, p["w"], 70, 700)
        wd = tw(c, p["w"], ws) + 60
        rrect(c, -wd / 2, -55, wd, 110, 8, fill=None, stroke=RED, lw=8, a=s2)
        text(c, p["w"], 0, 0, ws, RED, alpha=s2)
        c.restore()

def scene_text(c, p, t, d):
    col = COL[p.get("col", "white")]
    sc = pop(ph(t, 0.0, 0.45))
    s = p["t"]; size = fit(c, s, 200, W - 240)
    c.save(); c.translate(W / 2, 460); c.scale(sc, sc); text(c, s, 0, 0, size, col); c.restore()
    if p.get("sub"):
        a = ease(ph(t, 0.4, 0.4))
        text(c, p["sub"], W / 2, 680, fit(c, p["sub"], 54, W - 260), INK, alpha=a, spacing=2)

def meter(c, n, t, y=560, start=0.3):
    segw, gap = 140, 14
    x0 = W / 2 - (10 * segw + 9 * gap) / 2
    for j in range(10):
        x = x0 + j * (segw + gap)
        rrect(c, x, y - 50, segw, 100, 10, fill=DARK, stroke=GREY, lw=3)
        on = ph(t, start + j * 0.09, 0.12)
        if j < n and on > 0:
            col = GOLD if j < 6 else RED
            rrect(c, x, y - 50, segw, 100, 10, fill=col, a=on)

def scene_rating(c, p, t, d):
    text(c, "FATAL DECISION RATING", W / 2, 230, 64, INK, spacing=6, alpha=ease(ph(t, 0, 0.3)))
    meter(c, p["n"], t, 420)
    end = 0.3 + p["n"] * 0.09 + 0.2
    sc = pop(ph(t, end, 0.45))
    if sc > 0.02:
        c.save(); c.translate(W / 2, 640); c.scale(sc, sc)
        text(c, f"{p['n']}/10", 0, 0, 190, RED if p["n"] >= 8 else GOLD); c.restore()
    a = ease(ph(t, end + 0.5, 0.4))
    text(c, p["v"], W / 2, 830, fit(c, p["v"], 64, W - 300), INK, alpha=a, spacing=2)

def scene_rating_intro(c, p, t, d):
    text(c, "FATAL DECISION RATING", W / 2, 330, 84, GOLD, spacing=6, alpha=ease(ph(t, 0, 0.3)))
    n = 1 + int(9 * ease_io(ph(t, 0.4, max(0.5, d - 0.8))))
    meter(c, n, 99, 560)
    text(c, f"?/10", W / 2, 780, 120, RED, alpha=ease(ph(t, 0.5, 0.4)))

def scene_num(c, p, t, d):
    n = p["n"]
    text(c, str(n), W / 2 + 420, 560, 900, INK, alpha=0.04)
    sc = pop(ph(t, 0.0, 0.5))
    c.save(); c.translate(560, 520); c.scale(sc, sc); text(c, f"#{n}", 0, 0, 380, RED); c.restore()
    a = ease(ph(t, 0.3, 0.4))
    nm = p["name"]
    nx = 560 + tw(c, f"#{n}", 380) / 2 + 50
    ns = fit(c, nm, 110, W - nx - 100)
    c.save(); c.translate(-60 * (1 - a), 0)
    text(c, nm, nx, 470, ns, GOLD, align="left", alpha=a)
    text(c, p["year"], nx, 600, 80, INK, align="left", alpha=ease(ph(t, 0.55, 0.4)))
    c.restore()
    line(c, [(nx, 680), (nx + 700 * ease(ph(t, 0.5, 0.6)), 680)], 8, RED)

def scene_title(c, p, t, d):
    a = ease(ph(t, 0.0, 0.4))
    text(c, p["a"], W / 2, 330, fit(c, p["a"], 130, W - 200), INK, alpha=a)
    sc = pop(ph(t, 0.35, 0.5))
    c.save(); c.translate(W / 2, 540); c.scale(sc, sc); text(c, p["b"], 0, 0, 240, RED); c.restore()
    text(c, p.get("c", "THAT SHOCKED THE NATION"), W / 2, 760, 60, GOLD, spacing=6, alpha=ease(ph(t, 0.9, 0.4)))

RECAP = ["SINCLAIR C5", "BOO.COM", "DASANI", "HOOVER", "MILLENNIUM DOME", "RATNERS", "NORTHERN ROCK", "WOOLWORTHS", "BHS", "THOMAS COOK"]
def scene_recap(c, p, t, d):
    for j, nm in enumerate(RECAP):
        a = ease(ph(t, j * (max(0.6, d - 0.6) / 10), 0.25))
        col_, row = j % 2, j // 2
        x = 260 + col_ * 760; y = 200 + row * 150
        rrect(c, x, y - 55, 640, 110, 12, fill=DARK, stroke=RED if j == 9 else GREY, lw=4, a=a)
        text(c, f"#{10 - j}", x + 70, y, 54, RED, alpha=a)
        text(c, nm, x + 150, y, fit(c, nm, 54, 470), INK, align="left", alpha=a)

def scene_end(c, p, t, d):
    sc = pop(ph(t, 0.0, 0.5))
    c.save(); c.translate(W / 2, 430); c.scale(sc, sc)
    text(c, "CALLING TIME", 0, 0, 170, GOLD, spacing=10); c.restore()
    text(c, "FAMOUS COMPANIES. ONE FATAL DECISION.", W / 2, 590, 50, INK, spacing=3, alpha=ease(ph(t, 0.4, 0.4)))
    s2 = pop(ph(t, 0.9, 0.45))
    if s2 > 0.02:
        c.save(); c.translate(W / 2, 760); c.scale(s2, s2)
        rrect(c, -260, -60, 520, 120, 60, fill=RED); text(c, "SUBSCRIBE", 0, 0, 64, INK); c.restore()

SCN = dict(stick=scene_stick, stat=scene_stat, vs=scene_vs, head=scene_head, date=scene_date, text=scene_text,
           rating=scene_rating, rating_intro=scene_rating_intro, num=scene_num, title=scene_title, recap=scene_recap, end=scene_end)

exec(open('scenes4.py').read())
from sb import REACT
exec(open('pubscenes.py').read())

# ---------------- captions ----------------
def clean(w):
    return w
HL = set()
CHUNKS = []
def build_chunks():
    cur = []
    for w in WORDS:
        cur.append(w)
        n = len(cur)
        if n >= 4 or (n >= 2 and re.search(r'[.,?!:]$', w[0])) or re.search(r'[.?!]$', w[0]):
            CHUNKS.append(cur); cur = []
    if cur: CHUNKS.append(cur)
build_chunks()

KEYW = re.compile(r'^(£|\$)?[\d,.]+(m|bn|%)?$|million|billion|percent|pound|bankrupt|collapsed|gone|stranded|recalled|receivership|nationalised|crap|disaster|worst|one$', re.I)
def captions(c, tm):
    for ch in CHUNKS:
        if ch[0][1] - 0.05 <= tm < ch[-1][2] + 0.15:
            # don't hold caption across a long gap
            words = [w[0] for w in ch]
            s = " ".join(words)
            size = 54
            total = tw(c, s, size)
            if total > W - 300: size = int(size * (W - 300) / total); total = tw(c, s, size)
            x = W / 2 - total / 2
            k = clamp((tm - ch[0][1]) / 0.12)
            c.save()
            rrect(c, x - 30, 1010 - 42, total + 60, 84, 12, fill=BG, a=0.72 * k)
            for w in ch:
                wd = tw(c, w[0] + " ", size)
                said = tm >= w[1]
                col = RED if KEYW.search(re.sub(r'[^\w£$%.,]', '', w[0])) else (INK if said else GREY)
                text(c, w[0], x, 1010, size, col, align="left", alpha=k)
                x += wd
            c.restore()
            return

# ---------------- frame ----------------
def find_line(tm):
    for i, (s, e) in enumerate(LINES):
        nxt = LINES[i + 1][0] if i + 1 < len(LINES) else END + 1
        if tm < nxt: return i, s, nxt
    return len(LINES) - 1, LINES[-1][0], END

def frame(f, surf=None):
    tm = f / FPS
    surf = surf or cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    background(c, f)
    i, s, nxt = find_line(tm)
    i = max(0, i); s = s if tm >= s else 0
    sc, p, _ = SB[i]
    CUR[0] = i
    ENTRY_NOW[0] = ENTRY[i]
    t = tm - s; d = nxt - s
    z = 1 + 0.035 * clamp(t / max(d, 0.1))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    SCN[sc](c, p, t, d)
    c.restore()
    reaction_overlay(c, tm)
    if SB[i][0] != 'pub': chrome(c, i)
    captions(c, tm)
    return surf

if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for a in sys.argv[2:]:
            f = int(float(a) * FPS); frame(f).write_to_png(f"still_{float(a):07.2f}.png")
    elif sys.argv[1] == "lines":
        # one still per line at 70% through: quick check
        for a in sys.argv[2:]:
            i = int(a); s = LINES[i][0]; nxt = LINES[i + 1][0] if i + 1 < len(LINES) else END
            tm = s + 0.75 * (nxt - s); frame(int(tm * FPS)).write_to_png(f"ln_{i:03d}.png")
    elif sys.argv[1] == "video":
        a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, NF)
        out = sys.argv[4] if len(sys.argv) > 4 else "out.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for f in range(a, min(b, NF)):
            frame(f, surf); surf.flush(); pr.stdin.write(bytes(surf.get_data()))
        pr.stdin.close(); pr.wait()
