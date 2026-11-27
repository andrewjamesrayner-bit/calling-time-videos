
# ================= MAPLIN story =================
def topcard(c):
    rrect(c, 60, 150, W - 120, 210, 34, fill=WHITE, stroke=INK, lw=8)
    text(c, "MAPLIN: 217 SHOPS,", W / 2, 215, 56, INK)
    sp_ = 22
    tot = tw(c, "£235M", 76) + tw(c, "SALES... GONE", 76) + sp_
    x = W / 2 - tot / 2
    text(c, "£235M", x, 298, 76, RED, align="left"); x += tw(c, "£235M", 76) + sp_
    text(c, "SALES... GONE", x, 298, 76, INK, align="left")

HL = {"barred", "barred.", "oi", "drawer", "slumped", "dearer.", "short.", "through.", "administration.", "lights.", "unplugged."}
GOLDW = {"1972", "nineteen", "seventy-two,", "2018", "2018,", "217", "2,000", "£235", "million", "twenty-eighth", "four", "months"}
CL = 13
SPIT_LI, SPIT_WORD, SPIT_BADGE = 8, "Toys", "SAME DAY AS TOYS R US?!"
MORAL_LI, MORAL_WORD, MORAL_BADGE = 11, "unplugged", "YOU GET UNPLUGGED"
LABELS = {"smug": "GUILTY", "facepalm": "OH NO", "wince": "OOF"}
PUNCHW = [(2, "drawer"), (5, "slumped"), (6, "short"), (7, "through"), (8, "administration"), (9, "lights"), (11, "unplugged")]
MAP_BLUE = (0.10, 0.35, 0.70)

SPEC = [
    ("cat", 0, None),
    ("parts", 1, None),
    ("drawer", 2, None),
    ("shops", 3, None),
    ("sales", 4, None),
    ("pound", 5, None),
    ("insure", 6, None),
    ("talks", 7, None),
    ("admin", 8, None),
    ("spit", 8, "Toys"),
    ("lights", 9, None),
    ("fair", 10, None),
    ("moral", 11, None),
    ("bell", 12, None),
    ("cheeky", 13, None),
]

def reactions():
    return [
        (W_(2, "drawer") + 0.05, W_(2, "drawer") + 1.2, "smug", 895, 560),
        (W_(5, "dearer") - 0.1, W_(5, "dearer") + 1.0, "wince", 170, 560),
        (W_(7, "through") + 0.0, W_(7, "through") + 1.1, "facepalm", 895, 560),
    ]

def resistor(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    line(c, [(-70, 0), (70, 0)], 6, GREY)
    rrect(c, -36, -16, 72, 32, 12, fill=(0.85, 0.75, 0.55), stroke=INK, lw=5)
    for j, col in enumerate((RED, INK, GOLD)):
        rrect(c, -22 + j * 16, -16, 7, 32, 0, fill=col)
    c.restore()

def iron(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -80, -16, 110, 32, 12, fill=RED, stroke=INK, lw=5)
    line(c, [(30, 0), (100, 0)], 9, GREY)
    c.restore()

def cable(c, x, y, s=1.0, ang=0, col=BLUE):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    pts = [(-90 + j * 15, math.sin(j * 0.9) * 22) for j in range(13)]
    line(c, pts, 9, col); rrect(c, 90, -14, 30, 28, 4, fill=GREY, stroke=INK, lw=4)
    c.restore()

def gadget(c, x, y, s, i, ang=0):
    [resistor, iron, cable][i % 3](c, x, y, s, ang)

def mstore(c, x, base, w=470, h=480, k=0.0, lit=1.0):
    building(c, x, base, w, h, "MAPLIN", sign=MAP_BLUE, k=k)
    if lit < 1:
        rrect(c, x, base - h, w, h, 10, fill=INK, a=0.6 * (1 - lit))

def story(c, name, t, d, li, s0, tm):
    if name == "cat":
        floor(c)
        # action hook: a catalogue slams onto the table and bursts open, parts flying out
        k = clamp(t / 0.3)
        y_ = lerp(200, 760, k * k)
        if k >= 1: hitshake(tm, s0 + 0.3, 20)
        c.save(); c.translate(W / 2, y_); c.rotate(-0.05)
        rrect(c, -300, -200, 600, 400, 14, fill=MAP_BLUE, stroke=INK, lw=9)
        text(c, "ELECTRONICS", 0, -100, 60, WHITE); text(c, "MAIL ORDER", 0, -20, 52, GOLD); text(c, "CATALOGUE", 0, 60, 52, WHITE)
        c.restore()
        if k >= 1:
            for j in range(9):
                p = clamp((t - 0.3) * 1.4)
                a_ = -math.pi / 2 + (j - 4) * 0.33
                gadget(c, W / 2 + math.cos(a_) * 520 * p, 760 + math.sin(a_) * 420 * p + 380 * p * p, 0.9, j, p * 5 + j)
        badge(c, 200, 470, "1972", ph(t, 0.1, 0.25), size=70)
        man(c, 880, hip(0.85), 0.85, P(ra=(-130, -60), la=(130, 60)), outfit=None, mouth="grin", brow="raised")
    elif name == "parts":
        floor(c)
        for j in range(16):
            yy = ((t * 600 + j * 170) % 1100) + 380
            gadget(c, 90 + (j * 131) % 900, yy, 1.0, j, t * 3 + j)
        tc = W_(1, "Cables") - s0
        lab = "CABLES YOU'D NEVER NEED" if t > tc else ("SOLDERING IRONS" if t > W_(1, "Soldering") - s0 else "RESISTORS")
        badge(c, W / 2, 1500, lab, 1, fill=WHITE, size=fit(c, lab, 64, 860))
    elif name == "drawer":
        floor(c)
        rrect(c, 300, 760, 520, 360, 10, fill=WOOD2, stroke=INK, lw=9)
        k = ease(clamp(t / 0.5))
        rrect(c, 330 - 0 * k, 800 - 0, 460 + 60 * k, 130, 8, fill=WOOD, stroke=INK, lw=8)
        circle(c, 560 + 30 * k, 865, 14, fill=GOLD, stroke=INK, w=5)
        for j in range(10):
            p = clamp((t - 0.4 - j * 0.05) * 2)
            cable(c, 420 + j * 40, 790 - p * (120 + (j % 3) * 70), 0.8, math.sin(t * 6 + j) * 0.5, col=[BLUE, RED, GREEN, GOLD][j % 4])
        man(c, 170, hip(0.95), 0.95, P(ra=(-100, -40), la=(30, 20)), outfit="pensioner", mouth="grin", brow="raised")
        badge(c, W / 2, 1500, "EVERY DAD IN BRITAIN", ph(t, 0.2, 0.25), fill=GOLD, size=64)
    elif name == "shops":
        floor(c)
        n = int(12 * ease(ph(t, 0.05, 0.9)))
        for j in range(n):
            xx = 70 + (j % 4) * 245; yy = 760 + (j // 4) * 180
            rrect(c, xx, yy - 150, 210, 150, 8, fill=WHITE, stroke=INK, lw=6)
            rrect(c, xx + 8, yy - 142, 194, 40, 5, fill=MAP_BLUE, stroke=INK, lw=4)
        counter(c, W / 2, 480, "", 217, " SHOPS", ph(t, 0.05, 0.8), size=120, col=MAP_BLUE)
        badge(c, W / 2, 1400, "2,000+ STAFF", ph(t, d * 0.55, 0.25), fill=GOLD, size=70)
    elif name == "sales":
        floor(c)
        for j in range(14):
            note(c, 80 + (j * 77) % 920, ((t * 420 + j * 140) % 700) + 520, 0.9, t * 3 + j)
        counter(c, W / 2, 620, "£", 235, "M", ph(t, 0.1, 0.8), size=200, col=GOLD)
        badge(c, W / 2, 800, "A YEAR", ph(t, 0.6, 0.25), fill=WHITE, size=60)
    elif name == "pound":
        floor(c)
        # £ coin tumbling down a falling chart while price tags shoot up
        pts = [(140 + j * 70, 520 + j * 30 + math.sin(j) * 30) for j in range(12)]
        k = clamp(t / max(0.8, d * 0.6)); m = max(2, int(12 * k))
        line(c, pts[:m], 12, RED)
        px, py = pts[m - 1]
        c.save(); c.translate(px, py - 50); c.rotate(t * 4); circle(c, 0, 0, 50, fill=GOLD, stroke=INK, w=7); text(c, "£", 0, 4, 60, INK); c.restore()
        for j in range(3):
            x_ = 260 + j * 280
            rrect(c, x_ - 90, GROUND - 150, 180, 150, 8, fill=(0.8, 0.65, 0.45), stroke=INK, lw=7); text(c, "IMPORT", x_, GROUND - 75, 34, INK)
            ty = GROUND - 200 - 160 * ease(ph(t, d * 0.55 + j * 0.15, 0.4))
            text(c, "££" if ty > GROUND - 280 else "£££", x_, ty, 60, RED, stroke=INK, sw=6)
    elif name == "insure":
        floor(c)
        for r in range(3):
            rrect(c, 120, 520 + r * 200, 520, 24, 6, fill=WOOD2, stroke=INK, lw=6)
            if r == 2 and t < 0.6:
                for j in range(3): gadget(c, 200 + j * 150, 500 + r * 200, 0.7, j)
        k = ease(ph(t, 0.2, 1.0))
        c.save(); c.translate(lerp(850, 1300, k), lerp(820, 300, k)); c.rotate(k * 3)
        poly(c, [(-150, 0), (-100, -80), (0, -110), (100, -80), (150, 0)], fill=RED, stroke=INK, lw=8)
        line(c, [(0, 0), (0, 170)], 10, INK); c.restore()
        text(c, "CREDIT INSURANCE", 800, 1000, 40, INK, alpha=1 - k)
        badge(c, W / 2, 1500, "EMPTY SHELVES", ph(t, d * 0.55, 0.25), fill=RED, col=WHITE, size=72)
    elif name == "talks":
        floor(c)
        tt = W_(7, "through") - s0
        miss = t > tt
        k = clamp(t / max(0.4, tt))
        man(c, 300, hip(0.95), 0.95, P(ra=(-60 - 30 * k, -20), la=(30, 20)), outfit="tycoon", mouth="frown" if miss else "smile", brow="worried" if miss else "raised")
        man(c, 780, hip(0.95), 0.95, P(la=(60 + 30 * k, 20) if not miss else (30, 20), ra=(-30, -20)), outfit="tycoon", mouth="flat" if miss else "smile", flip=True)
        text(c, "MAPLIN", 300, 560, 44, MAP_BLUE); text(c, "BUYER", 780, 560, 44, INK)
        rrect(c, 380, 450, 320, 90, 14, fill=WHITE, stroke=INK, lw=6); text(c, "RESCUE DEAL", 540, 496, 40, INK)
        if miss: stamp(c, "DEAL OFF", 540, 900, clamp((t - tt) / 0.18), size=100); hitshake(tm, s0 + tt + 0.1, 16)
    elif name == "admin":
        floor(c)
        calendar(c, 270, 560, "28 FEB", 1)
        ta = W_(8, "administration") - s0
        k = clamp((t - ta) / 0.8) if t > ta else 0
        mstore(c, 480, GROUND, 500, 500, k=k * 0.4)
        if t > ta: stamp(c, "ADMINISTRATION", W / 2, 1450, clamp((t - ta) / 0.18), size=70, rot=-0.1); hitshake(tm, s0 + ta + 0.1, 18)
        badge(c, 270, 800, "2018", ph(t, 0.1, 0.25), size=60)
    elif name == "lights":
        floor(c)
        tl = W_(9, "lights") - s0
        lit = 1 - clamp((t - tl) / 0.12) if t > tl else 1
        mstore(c, 300, GROUND, 480, 520, lit=lit)
        man(c, 880, hip(0.95), 0.95, P(ra=(-140, -100), la=(30, 20)), outfit="worker", mouth="frown", brow="worried")
        rrect(c, 950, 640, 50, 80, 8, fill=WHITE, stroke=INK, lw=5)
        badge(c, 540, 500, "JUNE 2018", ph(t, 0.1, 0.25), size=58, rot=0.06)
        if t > tl:
            setc(c, INK, 0.35 * (1 - lit) * 0.9); c.paint()
            stamp(c, "CLICK.", 540, 1430, clamp((t - tl) / 0.18), col=GOLD, size=90)
    elif name == "fair":
        floor(c)
        badge(c, W / 2, 480, "IN FAIRNESS...", ph(t, 0.05, 0.25), fill=WHITE, size=80)
        rrect(c, 140, 620, 360, 220, 12, fill=WHITE, stroke=INK, lw=8)
        text(c, "\"THE ECONOMY,", 320, 700, 40, INK); text(c, "NOT THE BRAND\"", 320, 770, 40, INK)
        rrect(c, 620, 620, 320, 200, 12, fill=(0.78, 0.88, 0.96), stroke=INK, lw=8)
        poly(c, [(580, 820), (980, 820), (1010, 870), (550, 870)], fill=GREY, stroke=INK, lw=7)
        text(c, "ONLINE", 780, 720, 54, BLUE)
        k = ph(t, d * 0.5, 0.3)
        if k > 0:
            cable(c, 540, 1010, 1.4, 0)
            badge(c, 540, 1120, "CHEAPER", k, fill=RED, col=WHITE, size=60)
