from rig import *
import re

GROUND = 1120
STORE = (0.20, 0.30, 0.55)
TM = [0.0]

# ---------------- chrome ----------------
def topcard(c):
    rrect(c, 60, 150, W - 120, 210, 34, fill=WHITE, stroke=INK, lw=8)
    text(c, "COKE SOLD BRITAIN TAP WATER", W / 2, 215, 56, INK)
    sp_ = 22
    tot = tw(c, "FOR", 76) + tw(c, "95p", 76) + tw(c, "A BOTTLE", 76) + 2 * sp_
    x = W / 2 - tot / 2
    text(c, "FOR", x, 298, 76, INK, align="left"); x += tw(c, "FOR", 76) + sp_
    text(c, "95p", x, 298, 76, RED, align="left"); x += tw(c, "95p", 76) + sp_
    text(c, "A BOTTLE", x, 298, 76, INK, align="left")

HL = {"barred", "barred.", "oi", "tap", "sidcup", "sidcup.", "worse", "worse.", "bromate", "recalled", "cancelled", "none", "none.", "created", "problem", "problem."}
GOLDW = {"2004", "£7", "million", "95p", "0.03p", "3,000", "thousand", "half", "five", "weeks", "nineteenth", "march"}
for _k in range(1, len(WORDS)):
    if WORDS[_k][0].lower().startswith("barred") and WORDS[_k - 1][0].lower() == "your": WORDS[_k - 1][0] = "you're"
    if WORDS[_k][0] in ("Oh", "Oh,") and _k == len(WORDS) - 11: WORDS[_k][0] = "Oi!"
CH = []
def build_chunks():
    cur = []
    for w in WORDS:
        cur.append(w)
        if len(cur) >= 3 or re.search(r'[.,?!]$', w[0]) or (len(cur) >= 2 and w[2] - cur[0][1] > 0.9):
            CH.append(cur); cur = []
    if cur: CH.append(cur)
build_chunks()
def wkey(w): return re.sub(r'[^a-z0-9,£%\-]', '', w.lower()).strip(',')

def captions(c, tm):
    for ch in CH:
        if (ch is CH[0] and tm < ch[-1][2] + 0.12) or ch[0][1] - 0.04 <= tm < ch[-1][2] + 0.12:
            size = 108
            s = " ".join(w[0] for w in ch).upper()
            while tw(c, s, size) + size * 0.32 * len(ch) > W - 160: size -= 4
            total = sum(tw(c, w[0].upper(), size) for w in ch) + size * 0.32 * (len(ch) - 1)
            x = W / 2 - total / 2
            k = 1.0 if (ch is CH[0] and tm < ch[0][1] + 0.16) else pop(clamp((tm - ch[0][1]) / 0.16))
            c.save(); c.translate(W / 2, 1250); c.scale(k, k); c.translate(-W / 2, -1250)
            for w in ch:
                key = wkey(w[0])
                col = RED if key in HL else (GOLD if key in GOLDW or re.match(r'^[£\d]', key) else WHITE)
                said = tm >= w[1] - 0.02
                x += text(c, w[0].upper(), x, 1250, size, col if said else LGREY, align="left", stroke=INK, sw=16) + size * 0.32
            c.restore()
            return

# ---------------- helpers ----------------
def floor(c, y=GROUND): line(c, [(40, y), (W - 40, y)], 10, INK)
def hip(s): return GROUND - 210 * s
def walkpose(t, sp=12, amp=24, **kw):
    w = math.sin(t * sp) * amp
    return P(la=(18 + w * 0.6, 10), ra=(-18 - w * 0.6, -10), ll=(w, 4), rl=(-w, -4), **kw)
def badge(c, x, y, s, k, fill=GOLD, col=INK, rot=-0.06, size=76):
    sc = pop(k)
    if sc < 0.02: return
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rotate(rot)
    wd = tw(c, s, size) + 70
    rrect(c, -wd / 2, -size * 0.72, wd, size * 1.45, 16, fill=fill, stroke=INK, lw=8); text(c, s, 0, 4, size, col); c.restore()
def counter(c, x, y, pre, val, suf, k, size=150, col=RED):
    v = val * ease(k)
    s = pre + (f"{v:,.0f}") + suf
    text(c, s, x, y, size, col, stroke=INK, sw=12)
def store(c, x, base, w=440, h=470, k=0.0, t=0, name="BHS"):
    building(c, x, base, w, h, name, sign=STORE, k=k, t=t)
def coin(c, x, y, r=46, spin=0.0):
    sx = abs(math.cos(spin)) * 0.85 + 0.15
    c.save(); c.translate(x, y); c.scale(sx, 1)
    circle(c, 0, 0, r, fill=GOLD, stroke=INK, w=7)
    if sx > 0.4: text(c, "£1", 0, 2, r * 0.9, INK)
    c.restore()
def note(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -48, -26, 96, 52, 8, fill=(0.55, 0.78, 0.55), stroke=INK, lw=5); text(c, "£", 0, 2, 34, INK); c.restore()
def fit(c, s_, size, maxw):
    while size > 12 and tw(c, s_, size) > maxw: size -= 2
    return size
def bottle(c, x, base, s=1.0, label="DASANI", fill=1.0):
    c.save(); c.translate(x, base); c.scale(s, s)
    poly(c, [(-70, 0), (-70, -260), (-40, -320), (-30, -380), (30, -380), (40, -320), (70, -260), (70, 0)], fill=(0.72, 0.86, 0.98), stroke=INK, lw=8)
    if fill < 1: rrect(c, -64, -260 * fill - 2, 128, 260 * fill, 6, fill=(0.55, 0.75, 0.95))
    rrect(c, -36, -420, 72, 44, 8, fill=BLUE, stroke=INK, lw=7)
    if label:
        rrect(c, -70, -200, 140, 90, 0, fill=BLUE, stroke=INK, lw=6); text(c, label, 0, -155, 30, WHITE)
    c.restore()
def cv(c, x, y, k):
    c.save(); c.translate(x, y); c.rotate(-0.04)
    rrect(c, -300, -330, 600, 660, 18, fill=WHITE, stroke=INK, lw=9)
    text(c, "CURRICULUM VITAE", 0, -270, 46, INK)
    for j, lab in enumerate(["NAME:", "RETAIL EXPERIENCE:", "SHOPS RUN:", "HOBBIES:"]):
        text(c, lab, -260, -170 + j * 120, 38, INK, align="left")
        line(c, [(-260, -130 + j * 120), (260, -130 + j * 120)], 4, GREY)
    text(c, "D. Chappell", 40, -170, 38, BLUE, align="left")
    text(c, "0", 150, 70, 40, BLUE, align="left")
    text(c, "Going fast", -40, 190, 38, BLUE, align="left")
    c.restore()
def car(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-260, 0), (-250, -60), (-60, -80), (0, -130), (120, -130), (170, -70), (270, -50), (280, 0)], fill=RED, stroke=INK, lw=9)
    rrect(c, 10, -120, 100, 45, 10, fill=(0.78, 0.88, 0.96), stroke=INK, lw=6)
    text(c, "1", -120, -40, 60, WHITE)
    for wx in (-160, 170):
        circle(c, wx, 0, 52, fill=INK, stroke=INK, w=6); circle(c, wx, 0, 20, fill=GREY, stroke=None)
    c.restore()
def calendar(c, x, y, label, k):
    c.save(); c.translate(x, y)
    rrect(c, -170, -150, 340, 300, 20, fill=WHITE, stroke=INK, lw=9)
    rrect(c, -170, -150, 340, 80, 20, fill=RED, stroke=INK, lw=9)
    text(c, label, 0, 30, 76, INK)
    c.restore()
def jar(c, x, base, fill, label="PENSION", col=GREEN, hole=False, t=0):
    rrect(c, x - 150, base - 380, 300, 380, 40, fill=(0.88, 0.94, 0.98), stroke=INK, lw=10)
    rrect(c, x - 110, base - 420, 220, 50, 12, fill=GREY, stroke=INK, lw=8)
    fh = 340 * clamp(fill)
    if fh > 4: rrect(c, x - 130, base - 20 - fh, 260, fh, 26, fill=col)
    rrect(c, x - 125, base - 260, 250, 70, 10, fill=WHITE, stroke=INK, lw=6); text(c, label, x, base - 225, 46, INK)
    if hole:
        circle(c, x + 110, base - 40, 16, fill=INK, stroke=None)
def bars(c, k):
    yb = lerp(-900, 0, ease(k))
    c.save(); c.translate(0, yb)
    rrect(c, 120, 420, W - 240, 30, 8, fill=GREY, stroke=INK, lw=8)
    for j in range(8):
        xx = 170 + j * (W - 340) / 7
        line(c, [(xx, 430), (xx, GROUND)], 22, INK); line(c, [(xx, 430), (xx, GROUND)], 10, GREY)
    c.restore()

# ---------------- shot list ----------------
SPEC = [
    ("pitch", 0, None),
    ("reveal", 1, None),
    ("money", 2, None),
    ("tap", 3, None),
    ("spit", 4, None),
    ("sidcup", 5, None),
    ("price", 6, None),
    ("times", 7, None),
    ("papers", 8, None),
    ("worse", 9, None),
    ("lab", 10, None),
    ("irony", 11, None),
    ("recall", 12, None),
    ("gone", 13, None),
    ("moral", 14, None),
    ("bell", 15, None),
    ("cheeky", 16, None),
]
def build_shots():
    starts = []
    for name, li, wd in SPEC:
        st = LINES[li][0] if wd is None else wt(li, wd) - 0.04
        starts.append(max(0, st))
    starts[0] = 0.0
    out = []
    for j, (name, li, wd) in enumerate(SPEC):
        e = starts[j + 1] if j + 1 < len(SPEC) else END + 1
        out.append((name, starts[j], e, li))
    return out
SHOTS = build_shots()
def sstart(name): return [x for x in SHOTS if x[0] == name][0][1]
def W_(li, word, nth=0): return wt(li, word, nth)   # absolute time of a word

SHAKE = [0.0]
def hitshake(tabs, at, amt=18, dur=0.25):
    k = (tabs - at) / dur
    if 0 <= k < 1: SHAKE[0] = max(SHAKE[0], amt * (1 - k))

def draw_shot(c, name, t, d, li, s0):
    tm = TM[0]
    floor_y = GROUND
    blink = blinkf(tm)
    if name == "pitch":
        floor(c)
        # exec unveils a giant blue bottle with sparkles
        k = ease(clamp(t / 0.5))
        man(c, 260, hip(0.95), 0.95, P(ra=(-120, -30), la=(30, 20)), outfit="tycoon", mouth="grin", brow="raised")
        c.save(); c.translate(700, GROUND); s_ = 0.4 + 0.6 * pop(clamp(t / 0.4)); c.scale(s_, s_)
        bottle(c, 0, 0, 1.6, "DASANI")
        c.restore()
        for j in range(6):
            a_ = t * 2 + j
            star(c, 700 + math.cos(a_) * 230, 600 + math.sin(a_) * 200, 18 + 8 * math.sin(t * 6 + j), GOLD)
        badge(c, 200, 470, "2004", ph(t, 0, 0.25), size=70)
    elif name == "reveal":
        floor(c)
        c.save(); c.translate(W / 2, GROUND); c.scale(1.9, 1.9); bottle(c, 0, 0, 1.0, "DASANI"); c.restore()
        badge(c, W / 2, 1520, "\"PURE\" BOTTLED WATER", ph(t, 0.2, 0.3), fill=BLUE, col=WHITE, size=62)
    elif name == "money":
        floor(c)
        for j in range(14):
            note(c, 80 + (j * 77) % 920, ((t * 420 + j * 140) % 860) + 380, 0.9, t * 3 + j)
        rrect(c, 140, 520, 800, 380, 20, fill=WHITE, stroke=INK, lw=10)
        text(c, "NEW! DASANI", W / 2, 640, 80, BLUE)
        text(c, "The UK's purest water*", W / 2, 740, 46, INK)
        text(c, "*allegedly", W / 2, 840, 30, GREY)
        line(c, [(300, 900), (300, GROUND)], 14, INK); line(c, [(780, 900), (780, GROUND)], 14, INK)
        counter(c, W / 2, 470, "£", 7, "M", ph(t, 0.1, 0.8), size=130, col=GOLD)
    elif name == "tap":
        floor(c)
        tp = W_(3, "tap") - s0
        # kitchen tap filling the bottle
        rrect(c, 520, 420, 60, 120, 10, fill=GREY, stroke=INK, lw=8)
        rrect(c, 520, 420, 260, 50, 14, fill=GREY, stroke=INK, lw=8)
        rrect(c, 730, 470, 50, 60, 8, fill=GREY, stroke=INK, lw=8)
        for j in range(6):
            yy = 540 + ((t * 900 + j * 60) % 300)
            circle(c, 755, yy, 9, fill=(0.55, 0.75, 0.95), stroke=None)
        bottle(c, 755, GROUND, 1.1, "DASANI", fill=clamp(t / max(0.5, d)))
        sneaky = t > tp
        man(c, 300, hip(0.95), 0.95, P(ra=(-60, -20), la=(30, 20), lean=-6 if sneaky else 0), outfit="tycoon",
            mouth="teeth" if sneaky else "smirk", brow="worried" if sneaky else "sly", sweat=t * 1.5 if sneaky else 0)
        if sneaky: badge(c, W / 2, 1520, "IT WAS TAP WATER", ph(t, tp, 0.25), fill=RED, col=WHITE, size=72)
        else: badge(c, W / 2, 1520, "ONE SMALL PROBLEM...", ph(t, 0.1, 0.25), size=64)
    elif name == "sidcup":
        floor(c)
        # road sign + factory with a pipe from MAINS to the bottling line
        rrect(c, 90, 430, 440, 170, 14, fill=(0.1, 0.45, 0.25), stroke=WHITE, lw=8)
        text(c, "SIDCUP", 310, 500, 70, WHITE); text(c, "KENT", 310, 565, 40, WHITE)
        line(c, [(310, 600), (310, GROUND)], 16, INK)
        rrect(c, 600, 640, 400, 480, 10, fill=(0.85, 0.85, 0.88), stroke=INK, lw=9)
        poly(c, [(600, 640), (700, 560), (800, 640), (900, 560), (1000, 640)], fill=(0.7, 0.7, 0.75), stroke=INK, lw=8)
        text(c, "FACTORY", 800, 760, 46, INK)
        line(c, [(40, 1060), (600, 1060)], 26, BLUE); text(c, "MAINS SUPPLY", 420, 1020, 34, BLUE)
        k = clamp(t / 0.8)
        circle(c, lerp(60, 590, k), 1060, 14, fill=WHITE, stroke=None)
        badge(c, W / 2, 1520, "NEVER CLAIMED SPRING WATER", ph(t, 0.3, 0.3), fill=WHITE, size=52)
    elif name == "price":
        floor(c)
        tw2 = W_(6, "Dasani") - s0
        k = ease(clamp((t - max(0.2, tw2 - 0.3)) / 0.6))
        ang = 0.30 * k
        c.save(); c.translate(W / 2, 760)
        poly(c, [(-40, 380), (40, 380), (0, 0)], fill=GREY, stroke=INK, lw=8)
        c.rotate(ang)
        line(c, [(-420, 0), (420, 0)], 14, INK)
        c.restore()
        lx, ly = W / 2 - 420 * math.cos(ang), 760 - 420 * math.sin(ang)
        rx, ry = W / 2 + 420 * math.cos(ang), 760 + 420 * math.sin(ang)
        # left: tap water glass, right: Dasani bottle (heavier = pricier)
        rrect(c, lx - 50, ly - 140, 100, 140, 10, fill=(0.75, 0.88, 1.0), stroke=INK, lw=7); text(c, "TAP", lx, ly - 170, 44, INK); text(c, "0.03p", lx, ly - 225, 54, GOLD, stroke=INK, sw=8)
        bottle(c, rx, ry, 0.8, "DASANI"); text(c, "95p", rx, ry - 330, 70, RED, stroke=INK, sw=10)
        text(c, "per half litre", W / 2, 1450, 34, INK, alpha=0.6)
    elif name == "times":
        floor(c)
        counter(c, W / 2, 640, "", 3166, "x", ph(t, 0.05, 0.7), size=200)
        badge(c, W / 2, 820, "THE PRICE OF TAP WATER", ph(t, 0.4, 0.25), fill=RED, col=WHITE, size=56)
        for j in range(5):
            bottle(c, 160 + j * 190, GROUND, 0.45 + 0.05 * math.sin(t * 8 + j), "")
    elif name == "papers":
        for j, (h, sub, ang) in enumerate([("TAP WATER FOR 95p?!", "Coke's 'pure' water is from Sidcup", -0.05), ("PECKHAM SPRING 2.0", "Papers compare Dasani to famous sitcom scam", 0.06)]):
            k = pop(ph(t, 0.15 + j * 0.9, 0.3))
            if k < 0.02: continue
            c.save(); c.translate(W / 2 + (j * 2 - 1) * 40, 620 + j * 330); c.rotate(ang); c.scale(k, k)
            rrect(c, -440, -170, 880, 340, 12, fill=(0.97, 0.96, 0.92), stroke=INK, lw=9)
            text(c, "THE DAILY GRUMBLE", 0, -120, 40, INK); line(c, [(-400, -90), (400, -90)], 5, INK)
            text(c, h, 0, -10, fit(c, h, 84, 820), RED); text(c, sub, 0, 90, fit(c, sub, 36, 800), INK)
            c.restore()
    elif name == "worse":
        floor(c)
        rrect(c, 300, 620, 480, 500, 10, fill=(0.85, 0.85, 0.88), stroke=INK, lw=9); text(c, "DASANI", 540, 760, 60, BLUE)
        cx_ = 540 + math.sin(t * 2) * 30
        for j, (ox, r_) in enumerate(((-120, 90), (0, 120), (130, 95))):
            circle(c, cx_ + ox, 450, r_, fill=(0.35, 0.37, 0.42), stroke=INK, w=7)
        if (t * 3) % 1 < 0.15:
            poly(c, [(560, 520), (500, 640), (550, 640), (480, 780), (620, 600), (560, 600), (620, 520)], fill=GOLD, stroke=INK, lw=5)
        for j in range(16):
            xx = 300 + (j * 37) % 500; yy = 540 + ((t * 700 + j * 50) % 500)
            line(c, [(xx, yy), (xx - 10, yy + 30)], 5, BLUE)
    elif name == "lab":
        floor(c)
        rrect(c, 120, 420, 840, 700, 20, fill=WHITE, stroke=INK, lw=9)
        text(c, "BROMATE TEST", W / 2, 490, 56, INK)
        lim = 10; mx = 25
        def ybar(v): return 1050 - 480 * v / mx
        line(c, [(180, ybar(lim)), (900, ybar(lim))], 8, RED)
        text(c, "UK LEGAL LIMIT: 10", 300, ybar(lim) - 30, 34, RED)
        k = ease(ph(t, 0.2, 1.0))
        v = 22 * k
        rrect(c, 420, ybar(v), 240, 1050 - ybar(v), 12, fill=RED if v > lim else GOLD, stroke=INK, lw=7)
        text(c, f"{v:.0f} ppb", 540, ybar(v) - 40, 60, RED if v > lim else INK)
        text(c, "Tested 10–22 ppb (BBC)", W / 2, 1450, 34, INK, alpha=0.6)
    elif name == "irony":
        floor(c)
        for j, (lab, val, col_) in enumerate((("SIDCUP TAP", "0", GREEN), ("DASANI", "OVER LIMIT", RED))):
            x_ = 290 + j * 500
            if j == 0:
                rrect(c, x_ - 70, GROUND - 260, 140, 260, 14, fill=(0.75, 0.88, 1.0), stroke=INK, lw=8)
            else:
                bottle(c, x_, GROUND, 0.9, "DASANI")
            text(c, lab, x_, 520, 52, INK)
            badge(c, x_, 640, "BROMATE: " + val, ph(t, 0.3 + j * 0.7, 0.25), fill=col_, col=WHITE, size=36)
        tp = W_(11, "created") - s0
        if t > tp: badge(c, W / 2, 1520, "THE PURIFYING DID IT", ph(t, tp, 0.25), fill=RED, col=WHITE, size=66)
    elif name == "recall":
        floor(c)
        # shelf of bottles swept into a skip
        rrect(c, 80, 560, 520, 30, 6, fill=WOOD2, stroke=INK, lw=6); rrect(c, 80, 820, 520, 30, 6, fill=WOOD2, stroke=INK, lw=6)
        k = clamp(t / max(0.8, d * 0.7))
        for row, sy in enumerate((560, 820)):
            for j in range(5):
                gone = k * 5 > (4 - j) + row * 0.5
                if gone:
                    ph_ = clamp(k * 5 - ((4 - j) + row * 0.5))
                    bx_ = lerp(130 + j * 100, 860, ph_); by_ = lerp(sy, 1000, ph_) - math.sin(ph_ * math.pi) * 200
                    if ph_ < 1:
                        c.save(); c.translate(bx_, by_); c.rotate(ph_ * 6); bottle(c, 0, 0, 0.32, ""); c.restore()
                else:
                    bottle(c, 130 + j * 100, sy, 0.32, "")
        poly(c, [(720, 920), (1000, 920), (970, GROUND), (750, GROUND)], fill=(0.9, 0.7, 0.1), stroke=INK, lw=8)
        text(c, "RECALL", 860, 1010, 44, INK)
        counter(c, W / 2, 500, "", 500000, " BOTTLES", ph(t, 0.1, 0.8), size=78)
    elif name == "gone":
        floor(c)
        calendar(c, 330, 700, "5 WEEKS", 1)
        rrect(c, 600, 520, 400, 360, 20, fill=(0.75, 0.86, 0.95), stroke=INK, lw=8)
        text(c, "EUROPE", 800, 600, 50, INK)
        for j in range(6):
            circle(c, 680 + (j % 3) * 120, 700 + (j // 3) * 100, 30, fill=GREEN, stroke=INK, w=5)
        tc = W_(13, "cancelled") - s0
        if t > tc: stamp(c, "CANCELLED", 800, 720, clamp((t - tc) / 0.18), size=72, rot=-0.18); hitshake(tm, s0 + tc + 0.1, 16)
    elif name == "spit":
        # cutaway: the landlord drinking, then a spit-take on "Sidcup"
        tt = max(0.15, W_(4, "Sidcup") - s0)
        sp = t - tt
        tilt = -0.9 if sp < 0 else lerp(-0.9, 0.0, ease(sp / 0.15))
        pub_bg(c)
        hd = man(c, 560, 975, 1.35, P(ra=(-160 if sp < 0 else -120, -40), la=(30, 20)), outfit="landlord",
                 eyes="half" if sp < 0 else "wide", brow="neutral" if sp < 0 else "raised", mouth="flat" if sp < 0 else "o", blink=blink if sp < 0 else 0)
        hx, hy = hd["rh"]
        pint(c, hx, hy + 40, 1.0, 0.7, tilt)
        bar_front(c)
        if sp > 0:
            droplets(c, hd["head"][0] + 40, hd["head"][1] + 30, sp, n=34, d=1)
            droplets(c, hd["head"][0] - 40, hd["head"][1] + 30, sp, n=20, d=-1, seed=8)
            hitshake(tm, tt, 22)
            if sp > 0.18:
                import random as _r
                rr = _r.Random(5)
                for j in range(9):
                    bx_ = 120 + rr.random() * 840; by_ = 420 + rr.random() * 700 + (sp - 0.18) * 90 * (0.5 + rr.random())
                    rad = 30 + rr.random() * 45
                    circle(c, bx_, by_, rad, fill=(0.85, 0.65, 0.2), stroke=None, a=0.55 * clamp((sp - 0.18) / 0.06))
                    circle(c, bx_ - rad * 0.3, by_ - rad * 0.3, rad * 0.25, fill=WHITE, stroke=None, a=0.6 * clamp((sp - 0.18) / 0.06))
            badge(c, W / 2, 1520, "FROM SIDCUP?!", ph(sp, 0, 0.25), fill=RED, col=WHITE, size=96)
        else:
            pass
    elif name == "moral":
        tk = talkf(tm, li)
        lean = lerp(0, 8, ease(t / 0.6))
        tw_ = W_(14, "tap") - s0
        if t < tw_:
            cir = t * 9
            pose = P(la=(70, 60), ra=(-55 + math.sin(cir) * 12, -80 + math.cos(cir) * 12), lean=lean)
        else:
            pose = P(la=(30, 20), ra=(-95, -5), lean=lean + 6)
        pub_bg(c)
        hd = man(c, 560, 975, 1.35, pose, outfit="landlord",
                 mouth="talk" if tk is not None else "smirk", talk=tk or 0, brow="one", eyes="half" if t < tw_ else "open", blink=blink)
        if t < tw_:
            lx, ly = hd["lh"]; pint(c, lx, ly + 60, 0.85, 0.0)
            rx, ry = hd["rh"]; rrect(c, rx - 40, ry - 30, 80, 60, 12, fill=WHITE, stroke=INK, lw=6)
        bar_front(c)
        pint(c, 880, 1000, 0.8, 0.5)
        badge(c, W / 2, 1530, "BETTER THAN THE TAP?", ph(t, tw_, 0.25), fill=RED, col=WHITE, size=74)
    elif name == "bell":
        pub_bg(c)
        sw = math.sin(t * 20) * clamp(1.6 - t * 0.45)
        tk = talkf(tm, li)
        hd = man(c, 500, 975, 1.35, P(ra=(122 + sw * 14, 26 + sw * 8), la=(35, 35)), outfit="landlord",
                 mouth="talk" if tk is not None else "grin", talk=tk or 0, brow="raised", eyes="open", blink=blink)
        rx, ry = hd["rh"]
        handbell(c, rx, ry, 1.0, -0.75 + sw * 0.45)
        for j in range(3):
            k = ((t * 2.5 + j / 3) % 1)
            c.save(); setc(c, GOLD, 1 - k); c.set_line_width(8); c.arc(rx + 120, ry + 70, 100 + k * 130, -1.2, 0.8); c.stroke(); c.restore()
        bar_front(c)
        pint(c, 880, 1000, 0.8, 0.9)
        badge(c, 190, 620, "TIME!", ph(t, 0.1, 0.25), fill=GOLD, size=100, rot=-0.12)

    elif name == "cheeky":
        pub_bg(c)
        tk = talkf(tm, li)
        t_sub = W_(16, "subscribe") - s0; t_like = W_(16, "like") - s0; t_bar = W_(16, "barred") - s0
        if t < t_sub - 0.15:          # "Oi!" — leans in, points at the viewer
            pose = P(ra=(-95, -5), la=(30, 20), lean=8); eyes, brow, mouth = "open", "raised", None
        elif t < t_bar - 0.1:         # points down at the buttons
            pose = P(ra=(150, 15), la=(30, 20), lean=6); eyes, brow, mouth = "open", "one", None
        elif t < t_bar + 0.9:         # arms folded, stern
            pose = P(la=(155, 125), ra=(-155, -125), lean=0); eyes, brow, mouth = "half", "angry", None
        else:                         # wink
            pose = P(la=(155, 125), ra=(-155, -125), lean=0); eyes, brow, mouth = "wink", "sly", "grin"
        hd = man(c, 540, 975, 1.35, pose, outfit="landlord", eyes=eyes, brow=brow,
                 mouth=("talk" if tk is not None else "smirk") if mouth is None else mouth, talk=tk or 0, blink=blink if eyes in ("open",) else 0)
        bar_front(c)
        pint(c, 880, 1000, 0.8, 0.9)
        if t < t_sub - 0.15: badge(c, 230, 600, "OI!", ph(t, 0.0, 0.2), fill=GOLD, size=110, rot=-0.1)
        if t > t_bar: stamp(c, "BARRED!", 790, 830, clamp((t - t_bar) / 0.18), size=80, rot=-0.15); hitshake(tm, s0 + t_bar + 0.1, 18)
        if t > t_bar + 0.9: star(c, hd["head"][0] + 95, hd["head"][1] - 40, 26 * pop(clamp((t - t_bar - 0.9) / 0.25)), GOLD)

# ---------------- landlord reaction bubbles ----------------
def reactions():
    return [  # (start, end, kind, x, y)
        (W_(7, "price") - 0.1, W_(7, "price") + 1.1, "jaw", 160, 500),
        (W_(9, "worse") + 0.1, W_(9, "worse") + 1.2, "facepalm", 895, 985),
        (W_(11, "created") + 0.1, W_(11, "created") + 1.2, "smug", 895, 985),
    ]
REACT = reactions()
def reaction(c, tm):
    for a, b, kind, x, y in REACT:
        if not (a <= tm < b): continue
        t = tm - a; d = b - a
        k = pop(clamp(t / 0.22)) * (1 - ease(clamp((t - (d - 0.18)) / 0.18)))
        if k < 0.02: return
        r = 105
        c.save(); c.translate(x, y); c.scale(k, k); c.rotate(math.sin(t * 5) * 0.03)
        circle(c, 0, 0, r + 9, fill=WHITE, stroke=INK, w=9)
        c.save(); c.arc(0, 0, r, 0, 2 * math.pi); c.clip()
        rrect(c, -r, -r, 2 * r, 2 * r, 0, fill=WALL)
        g = cairo.RadialGradient(0, -60, 5, 0, -60, 170); g.add_color_stop_rgba(0, 1, 0.82, 0.45, 0.5); g.add_color_stop_rgba(1, 1, 0.82, 0.45, 0)
        c.set_source(g); c.paint()
        if kind == "facepalm":
            hd = man(c, 0, 205, 0.8, P(ra=(-25, -150), la=(30, 20), head=-8), outfit="landlord", eyes="closed", brow="worried", mouth="frown")
            hx, hy = hd["head"]
            circle(c, hx + 6, hy - 6, 26, fill=WHITE, stroke=INK, w=7)   # palm over the eyes
            line(c, [(hx - 10, hy - 26), (hx + 26, hy - 32)], 5, INK)
        elif kind == "jaw":
            man(c, 0, 205, 0.8, P(la=(150, 150), ra=(-150, -150)), outfit="landlord", eyes="wide", brow="raised", mouth="scream")
        elif kind == "wince":
            man(c, 0, 205, 0.8, P(la=(150, 120), ra=(-150, -120), head=6 * math.sin(t * 30) * (t < 0.4)), outfit="landlord", eyes="closed", brow="worried", mouth="teeth")
        else:
            man(c, 0, 205, 0.8, P(la=(155, 125), ra=(-155, -125)), outfit="landlord", eyes="half", brow="sly", mouth="smirk")
        c.restore()
        c.restore()
        lab = {"facepalm": "OH NO", "wince": "OOF", "smug": "TOLD YOU", "jaw": "95p?!"}[kind]
        badge(c, x + 40, y + 140, lab, clamp((t - 0.15) / 0.25) * (1 - ease(clamp((t - (d - 0.18)) / 0.18))), fill=GOLD, size=42, rot=0.08)
        return

# ---------------- CTA ----------------
def thumb(c, x, y, s, filled):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = RED if filled else WHITE
    rrect(c, -70, -10, 40, 90, 8, fill=col, stroke=INK, lw=8)
    poly(c, [(-24, -6), (6, -70), (30, -66), (24, -14), (70, -14), (78, 0), (66, 80), (-24, 80)], fill=col, stroke=INK, lw=8)
    c.restore()

def cta(c, tm):
    t0 = LINES[16][0]; ts = W_(16, "subscribe"); tl = W_(16, "like")
    t = tm - t0
    if t < 0: return
    cy = 1530
    sc = pop(ph(t, 0, 0.3))
    click = clamp((tm - ts) / 0.15); like = clamp((tm - tl) / 0.15)
    c.save(); c.translate(W / 2, cy); c.scale(sc, sc)
    subbed = click > 0.5
    rrect(c, -300, -60, 420, 120, 60, fill=GREY if subbed else RED, stroke=INK, lw=8)
    text(c, "SUBSCRIBED" if subbed else "SUBSCRIBE", -110 if subbed else -90, 2, 52 if subbed else 56, WHITE)
    z = 1 + 0.25 * math.sin(clamp(like) * math.pi)
    c.save(); c.translate(230, 0); c.scale(z, z); circle(c, 0, 0, 72, fill=WHITE, stroke=INK, w=8); thumb(c, -4, -6, 0.62, like > 0.5); c.restore()
    c.restore()
    if sc > 0.5:
        k1 = eio(clamp((tm - (ts - 0.45)) / 0.4)); k2 = eio(clamp((tm - (tl - 0.35)) / 0.3))
        hx = lerp(W / 2 + 330, W / 2 - 90, k1); hy = lerp(cy + 220, cy + 20, k1)
        hx = lerp(hx, W / 2 + 230, k2); hy = lerp(hy, cy + 10, k2)
        press = 0.85 if (0 <= tm - ts < 0.25 or 0 <= tm - tl < 0.25) else 1.0
        c.save(); c.translate(hx, hy); c.scale(press, press)
        poly(c, [(0, 0), (0, 90), (22, 70), (40, 108), (58, 100), (40, 62), (70, 60)], fill=WHITE, stroke=INK, lw=7); c.restore()
        for kk, px in ((click, W / 2 - 90), (like, W / 2 + 230)):
            burst(c, px, cy, 70, kk)

# ---------------- frame ----------------
PUNCHT = [W_(3, "tap"), W_(4, "Sidcup"), W_(6, "Dasani"), W_(9, "worse"), W_(11, "none"), W_(12, "recalled"), W_(13, "cancelled"), W_(14, "tap")]
def punch(tm, s0):
    k = 0.0
    for pt in PUNCHT:
        if s0 - 0.01 <= pt <= tm: k = max(k, ease((tm - pt) / 0.07))
    return k

def frame(f, surf=None):
    tm = f / FPS; TM[0] = tm; extras_t[0] = tm
    surf = surf or cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    setc(c, BG); c.paint()
    SHAKE[0] = 0.0
    for name, s, e, li in SHOTS:
        if s <= tm < e:
            t, d = tm - s, max(0.3, min(e, END) - s)
            # punch-in on each cut: quick zoom settle, then slow push
            z = (1 + 0.06 * (1 - ease(t / 0.25)) + 0.035 * clamp(t / d)) * (1 + 0.11 * punch(tm, s))
            c.save(); c.translate(W / 2, 800); c.scale(z, z); c.translate(-W / 2, -800)
            # draw once to compute shake, then apply (shake computed inside draw via hitshake)
            c.push_group()
            draw_shot(c, name, t, d, li, s)
            pat = c.pop_group()
            amt = SHAKE[0]
            c.translate(math.sin(tm * 90) * amt, math.cos(tm * 77) * amt)
            c.set_source(pat); c.paint()
            c.restore()
            break
    reaction(c, tm)
    topcard(c)
    captions(c, tm)
    cta(c, tm)
    text(c, "CALLING TIME", W / 2, 100, 30, INK, alpha=0.55)
    return surf

if __name__ == "__main__":
    if sys.argv[1] == "shots":
        for name, s, e, li in SHOTS:
            for fr in (0.3, 0.8):
                tm = s + fr * (min(e, END) - s); frame(int(tm * FPS)).write_to_png(f"sh_{s:06.2f}_{name}_{int(fr*10)}.png")
    elif sys.argv[1] == "video":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-i", "vo/mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-af", "apad,loudnorm=I=-14:TP=-1.5", "-ar", "48000", "-t", f"{NF / FPS:.3f}", "-movflags", "+faststart", "final.mp4"]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for f in range(NF):
            frame(f, surf); surf.flush(); pr.stdin.write(bytes(surf.get_data()))
        pr.stdin.close(); pr.wait()
