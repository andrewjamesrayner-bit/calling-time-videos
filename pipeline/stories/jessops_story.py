
# ================= JESSOPS story =================
for _w in WORDS:
    if _w[0].lower().startswith("jessup"): _w[0] = _w[0].replace("Jessups", "Jessops").replace("jessups", "Jessops")
def topcard(c):
    rrect(c, 60, 150, W - 120, 210, 34, fill=WHITE, stroke=INK, lw=8)
    text(c, "JESSOPS: 187 SHOPS", W / 2, 215, 56, INK)
    sp_ = 22
    tot = tw(c, "SHUT", 76) + tw(c, "IN DAYS", 76) + sp_
    x = W / 2 - tot / 2
    text(c, "SHUT", x, 298, 76, RED, align="left"); x += tw(c, "SHUT", 76) + sp_
    text(c, "IN DAYS", x, 298, 76, INK, align="left")

HL = {"barred", "barred.", "oi", "pocket.", "cheaper.", "christmas.", "good.", "gone.", "bought.", "in."}
GOLDW = {"2013", "twenty", "thirteen.", "1935.", "nineteen", "thirty-five.", "2009,", "187", "hundred", "1,370", "thousand", "two", "months"}
CL = 15
SPIT_LI, SPIT_WORD, SPIT_BADGE = 10, "return", "NO RETURNS?!"
MORAL_LI, MORAL_WORD, MORAL_BADGE = 13, "maybe", "DON'T JUST SELL CAMERAS"
LABELS = {"smug": "UH OH", "facepalm": "OH NO", "wince": "OOF"}
PUNCHW = [(3, "pocket"), (5, "cheaper"), (7, "administrators"), (8, "good"), (9, "gone"), (10, "return"), (13, "cameras")]
JBLUE = (0.10, 0.25, 0.55)

SPEC = [
    ("flash", 0, None),
    ("shop", 1, None),
    ("proper", 2, None),
    ("pocket", 3, None),
    ("rivals", 4, None),
    ("bank", 5, None),
    ("xmas", 6, None),
    ("admin", 7, None),
    ("shut", 8, None),
    ("jobs", 9, None),
    ("returns", 10, None),
    ("spit", 10, "return"),
    ("fair", 11, None),
    ("reopen", 12, None),
    ("moral", 13, None),
    ("bell", 14, None),
    ("cheeky", 15, None),
]

def reactions():
    return [
        (W_(3, "pocket") + 0.05, W_(3, "pocket") + 1.2, "smug", 895, 560),
        (W_(6, "Christmas") + 0.05, W_(6, "Christmas") + 1.1, "facepalm", 170, 560),
        (W_(9, "gone") + 0.0, W_(9, "gone") + 1.1, "wince", 895, 560),
    ]

def camera(c, x, y, s=1.0, ang=0, flash=0.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -150, -90, 300, 190, 22, fill=INK, stroke=INK, lw=6)
    rrect(c, -100, -125, 90, 45, 10, fill=INK)
    circle(c, 10, 5, 70, fill=GREY, stroke=INK, w=10); circle(c, 10, 5, 38, fill=(0.2, 0.3, 0.45), stroke=INK, w=6)
    circle(c, 0, -8, 10, fill=WHITE, stroke=None)
    rrect(c, 90, -75, 40, 26, 6, fill=WHITE if flash > 0 else LGREY, stroke=None)
    c.restore()

def phone(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -60, -110, 120, 220, 18, fill=INK)
    rrect(c, -50, -95, 100, 180, 10, fill=(0.75, 0.85, 0.95))
    circle(c, 25, -70, 12, fill=INK, stroke=GREY, w=4)
    c.restore()

def jstore(c, x, base, w=470, h=480, k=0.0, lit=1.0, name="JESSOPS"):
    building(c, x, base, w, h, name, sign=JBLUE, k=k)
    if lit < 1:
        rrect(c, x, base - h, w, h, 10, fill=INK, a=0.6 * (1 - lit))

def story(c, name, t, d, li, s0, tm):
    if name == "flash":
        floor(c)
        # action hook: camera slams in and fires a blinding flash
        k = clamp(t / 0.25)
        camera(c, W / 2, lerp(300, 760, ease(k)), 1.6, -0.2 * (1 - k), flash=1 if t > 0.3 else 0)
        if k >= 1: hitshake(tm, s0 + 0.25, 20)
        if 0.3 < t < 0.75:
            setc(c, WHITE, 1 - (t - 0.3) / 0.45); c.paint()
        badge(c, 220, 470, "JAN 2013", ph(t, 0.5, 0.25), size=64)
        tl = W_(0, "last") - s0
        if t > tl: badge(c, W / 2, 1500, "SAY CHEESE...", ph(t, tl, 0.25), fill=GOLD, size=70)
    elif name == "shop":
        floor(c)
        jstore(c, 300, GROUND, 480, 520, k=0)
        badge(c, 200, 520, "1935", ph(t, W_(1, "nineteen") - s0, 0.25), size=70)
        badge(c, 880, 560, "LEICESTER", ph(t, W_(1, "Leicester") - s0, 0.25), fill=WHITE, size=46, rot=0.06)
        man(c, 160, hip(0.8), 0.8, P(ra=(-130, -60), la=(30, 20)), outfit="pensioner", mouth="grin", brow="raised")
    elif name == "proper":
        floor(c)
        man(c, 420, hip(1.0), 1.0, P(ra=(-80, -60), la=(80, 60)), mouth="grin", brow="raised")
        camera(c, 420, 780, 0.9, math.sin(t * 4) * 0.05, flash=(t * 2) % 1 < 0.15)
        for j in range(3):
            circle(c, 800, 700 + j * 120, 60 - j * 8, fill=GREY, stroke=INK, w=7)
        text(c, "LENSES", 800, 1040, 44, INK)
        badge(c, W / 2, 1500, "PROPER CAMERAS", ph(t, 0.2, 0.25), fill=GOLD, size=70)
    elif name == "pocket":
        floor(c)
        man(c, 540, hip(1.1), 1.1, P(ra=(-30, -20), la=(30, 20)), mouth="smirk", brow="sly")
        tp = W_(3, "pocket") - s0
        k = ease(clamp((t - tp + 0.2) / 0.4))
        phone(c, 640, lerp(950, 620, k), 1.0, 0.1 * k)
        if t > tp:
            for j in range(4):
                burst(c, 640, 620, 120, clamp((t - tp) * 2))
            badge(c, W / 2, 1500, "CAMERA PHONES", ph(t, tp, 0.25), fill=RED, col=WHITE, size=70)
    elif name == "rivals":
        floor(c)
        ts_ = [W_(4, "Phones") - s0, W_(4, "Supermarkets") - s0, W_(4, "internet") - s0]
        k0 = pop(ph(t, ts_[0], 0.3)); k1 = pop(ph(t, ts_[1], 0.3)); k2 = pop(ph(t, ts_[2], 0.3))
        if k0 > 0: phone(c, 220, 760, k0)
        if k1 > 0:
            c.save(); c.translate(540, 820); c.scale(k1, k1)
            rrect(c, -110, -120, 220, 130, 10, fill=GREY, stroke=INK, lw=8); line(c, [(-140, -150), (-110, -120)], 10, INK)
            circle(c, -70, 40, 24, fill=INK, stroke=None); circle(c, 70, 40, 24, fill=INK, stroke=None); c.restore()
        if k2 > 0:
            c.save(); c.translate(860, 760); c.scale(k2, k2)
            rrect(c, -130, -90, 260, 170, 12, fill=(0.78, 0.88, 0.96), stroke=INK, lw=8)
            poly(c, [(-160, 80), (160, 80), (190, 130), (-190, 130)], fill=GREY, stroke=INK, lw=7)
            text(c, "£ LESS", 0, 0, 44, RED); c.restore()
        man(c, 540, hip(0.6) + 0, 0.6, P(ra=(-150, -120), la=(150, 120)), outfit="worker", mouth="scream", brow="worried")
    elif name == "bank":
        floor(c)
        k = ease(clamp((t - 0.4) / 0.8))
        c.save(); c.translate(380, 760)
        setc(c, JBLUE); c.move_to(0, 0); c.arc(0, 0, 220, -math.pi / 2 + 1.6 * k, 1.5 * math.pi); c.close_path(); c.fill()
        c.arc(0, 0, 220, 0, 2 * math.pi); setc(c, INK); c.set_line_width(9); c.stroke(); c.restore()
        c.save(); c.translate(380 + 360 * k, 760 - 60 * k)
        setc(c, GOLD); c.move_to(0, 0); c.arc(0, 0, 220, -math.pi / 2, -math.pi / 2 + 1.6); c.close_path(); c.fill(); c.restore()
        building(c, 720, GROUND, 300, 260, "BANK", sign=GREEN)
        badge(c, 200, 470, "2009", ph(t, 0.1, 0.25), size=70)
        badge(c, W / 2, 1500, "DEBT FOR SHARES", ph(t, d * 0.5, 0.25), fill=WHITE, size=64)
    elif name == "xmas":
        floor(c)
        tc = W_(6, "Christmas") - s0
        droop = ease(clamp((t - tc) / 0.6)) if t > tc else 0
        c.save(); c.translate(320, GROUND); c.rotate(0.35 * droop)
        for j in range(3):
            poly(c, [(-170 + j * 40, -100 - j * 150), (170 - j * 40, -100 - j * 150), (0, -300 - j * 150)], fill=GREEN, stroke=INK, lw=8)
        rrect(c, -30, -100, 60, 100, 4, fill=WOOD, stroke=INK, lw=6)
        star(c, 0, -620, 40, GOLD); c.restore()
        pts = [(600 + j * 45, 600 + (j * j) * 6 * droop + math.sin(j) * 20) for j in range(10)]
        line(c, pts, 12, RED)
        text(c, "SALES", 800, 560, 50, INK)
    elif name == "admin":
        floor(c)
        ta = W_(7, "administrators") - s0
        jstore(c, 300, GROUND, 480, 520, k=0)
        man(c, 160, hip(0.85), 0.85, P(ra=(-40, -20), la=(40, 20)), outfit="tycoon", mouth="frown", brow="worried")
        if t < ta: badge(c, W / 2, 520, "SUPPLIERS: NO", ph(t, 0.1, 0.25), fill=RED, col=WHITE, size=64)
        if t > ta: stamp(c, "ADMINISTRATION", W / 2, 1450, clamp((t - ta) / 0.18), size=70, rot=-0.1); hitshake(tm, s0 + ta + 0.1, 18)
    elif name == "shut":
        floor(c)
        tg = W_(8, "good") - s0
        for j in range(12):
            xx = 70 + (j % 4) * 245; yy = 760 + (j // 4) * 180
            off = t > tg - 0.6 + j * 0.05
            rrect(c, xx, yy - 150, 210, 150, 8, fill=(0.3, 0.3, 0.32) if off else WHITE, stroke=INK, lw=6)
            rrect(c, xx + 8, yy - 142, 194, 40, 5, fill=JBLUE, stroke=INK, lw=4)
        counter(c, W / 2, 530, "", 187, " SHOPS", ph(t, 0.05, 0.8), size=96, col=JBLUE)
        if t > tg: stamp(c, "SHUT", W / 2, 1450, clamp((t - tg) / 0.18), size=120); hitshake(tm, s0 + tg + 0.1, 16)
    elif name == "jobs":
        floor(c)
        counter(c, 420, 560, "", 1370, "", ph(t, 0.05, 0.8), size=150, col=RED)
        badge(c, 420, 700, "JOBS", ph(t, 0.4, 0.25), fill=WHITE, size=60)
        for j in range(5):
            x_ = 140 + j * 200
            man(c, x_, hip(0.6), 0.6, P(ra=(-30, -20), la=(30, 20), lean=-4), outfit="worker", mouth="frown", brow="worried")
            box(c, x_ - 60, hip(0.6) - 40, 120, 70, "")
    elif name == "returns":
        floor(c)
        rrect(c, 300, 560, 480, 300, 14, fill=WHITE, stroke=INK, lw=9)
        text(c, "RETURNS", W / 2, 650, 64, INK)
        line(c, [(330, 590), (750, 830)], 18, RED); line(c, [(750, 590), (330, 830)], 18, RED)
        man(c, 220, hip(0.9), 0.9, P(ra=(-100, -40), la=(30, 20)), mouth="o", brow="worried")
        box(c, 250, 820, 150, 110, "")
    elif name == "fair":
        floor(c)
        badge(c, W / 2, 480, "IN FAIRNESS...", ph(t, 0.05, 0.25), fill=WHITE, size=80)
        k = clamp(t / max(0.8, d * 0.7))
        pts = [(180 + j * 75, 650 + (j ** 1.6) * 18 * k) for j in range(10)]
        line(c, [(160, 620), (160, 1060), (920, 1060)], 8, INK)
        line(c, pts, 14, RED)
        text(c, "CAMERA SALES", 540, 1110, 40, INK)
        badge(c, W / 2, 1500, "WHOLE MARKET SHRINKING", ph(t, d * 0.4, 0.25), fill=GOLD, size=56)
    elif name == "reopen":
        floor(c)
        tr = W_(12, "reopened") - s0
        lit = 0.0 if t < tr else clamp((t - tr) / 0.3)
        jstore(c, 300, GROUND, 480, 520, lit=lit)
        man(c, 160, hip(0.85), 0.85, P(ra=(-140, -110) if t > tr else (-40, -20), la=(30, 20)), outfit="tycoon", mouth="grin", brow="raised")
        badge(c, 880, 560, "NEW OWNER", ph(t, 0.3, 0.25), fill=WHITE, size=46, rot=0.06)
        if t > tr:
            for j in range(6): star(c, 300 + j * 90, 560 + math.sin(t * 6 + j) * 30, 20, GOLD)
            badge(c, W / 2, 1500, "2 MONTHS LATER", ph(t, tr, 0.25), fill=GREEN, col=WHITE, size=66)
