
# ================= COMET story =================
def topcard(c):
    rrect(c, 60, 150, W - 120, 210, 34, fill=WHITE, stroke=INK, lw=8)
    text(c, "COMET WAS SOLD FOR", W / 2, 215, 56, INK)
    sp_ = 22
    tot = tw(c, "£2", 76) + tw(c, "...THEN IT DIED", 76) + sp_
    x = W / 2 - tot / 2
    text(c, "£2", x, 298, 76, RED, align="left"); x += tw(c, "£2", 76) + sp_
    text(c, "...THEN IT DIED", x, 298, 76, INK, align="left")

HL = {"barred", "barred.", "oi", "quid!", "quid", "paid", "buyer.", "wallet.", "administration.", "why.", "penny", "shut"}
GOLDW = {"£2", "two", "pounds.", "£50", "fifty", "million", "236", "6,900", "£49", "forty-nine", "79", "seventy-nine", "2011", "2012", "eighteenth", "december."}
CL = 14
SPIT_LI, SPIT_WORD, SPIT_BADGE = 2, "paid", "THE SELLER PAID?!"
MORAL_LI, MORAL_WORD, MORAL_BADGE = 12, "why", "ASK WHY"
LABELS = {"facepalm": "OH NO", "jaw": "£49M?!", "smug": "TOLD YOU"}
PUNCHW = [(1, "quid"), (2, "paid"), (4, "wallet"), (6, "administration"), (8, "forty"), (9, "penny"), (11, "shut"), (12, "why")]
COMET_BLUE = (0.16, 0.30, 0.62)

SPEC = [
    ("sold", 0, None),
    ("quid", 1, None),
    ("spit", 2, None),
    ("dowry", 3, None),
    ("car", 4, None),
    ("opcap", 5, None),
    ("admin", 6, None),
    ("jobs", 7, None),
    ("tax", 8, None),
    ("penny", 9, None),
    ("fair", 10, None),
    ("shut", 11, None),
    ("moral", 12, None),
    ("bell", 13, None),
    ("cheeky", 14, None),
]

def reactions():
    return [
        (W_(4, "wallet") + 0.05, W_(4, "wallet") + 1.2, "facepalm", 895, 560),
        (W_(8, "forty") - 0.05, W_(8, "forty") + 1.2, "jaw", 170, 560),
        (W_(10, "inquiry") - 0.6, W_(10, "inquiry") + 0.6, "smug", 895, 560),
    ]

def coin2(c, x, y, r=46, spin=0.0):
    sx = abs(math.cos(spin)) * 0.85 + 0.15
    c.save(); c.translate(x, y); c.scale(sx, 1)
    circle(c, 0, 0, r, fill=GOLD, stroke=INK, w=7)
    if sx > 0.4: text(c, "£2", 0, 2, r * 0.9, INK)
    c.restore()

def tagp(c, x, y, s, ang=0.1):
    c.save(); c.translate(x, y); c.rotate(ang)
    wd = tw(c, s, 60) + 60
    poly(c, [(-wd / 2 - 40, 0), (-wd / 2, -50), (wd / 2, -50), (wd / 2, 50), (-wd / 2, 50)], fill=WHITE, stroke=INK, lw=7)
    circle(c, -wd / 2 - 10, 0, 9, fill=INK, stroke=None)
    text(c, s, 10, 2, 60, RED); c.restore()

def wallet(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -90, -60, 180, 120, 16, fill=(0.45, 0.28, 0.15), stroke=INK, lw=7)
    note(c, 0, -60, 0.9, 0.1)
    c.restore()

def story(c, name, t, d, li, s0, tm):
    if name == "sold":
        floor(c)
        # action hook: £2 coin flips into the tycoon's hand as SOLD slams on the store
        building(c, 540, GROUND, 470, 480, "COMET", sign=COMET_BLUE)
        kf = clamp(t / 0.45)
        cx = lerp(980, 280, kf); cy = lerp(420, 690, kf) - math.sin(kf * math.pi) * 260
        man(c, 260, hip(0.95), 0.95, P(ra=(-110, -40), la=(30, 20)), outfit="tycoon", mouth="grin" if kf >= 1 else "o", brow="raised")
        coin2(c, cx, cy, 60, t * 14)
        stamp(c, "SOLD", 775, 820, clamp((t - 0.45) / 0.18), size=110, rot=-0.2); hitshake(tm, s0 + 0.5, 20)
        badge(c, 200, 470, "2011", ph(t, 0.1, 0.25), size=70)
    elif name == "quid":
        floor(c)
        for j in range(8):
            xx = 90 + (j % 4) * 240; yy = 760 + (j // 4) * 330
            rrect(c, xx, yy - 230, 200, 230, 8, fill=WHITE, stroke=INK, lw=7)
            rrect(c, xx + 10, yy - 220, 180, 50, 6, fill=COMET_BLUE, stroke=INK, lw=5)
        c.save(); c.translate(W / 2, 620); s_ = pop(ph(t, 0.1, 0.35)); c.scale(s_ * 2.4, s_ * 2.4); coin2(c, 0, 0, 70, 0); c.restore()
        badge(c, W / 2, 1500, "FOR HUNDREDS OF SHOPS", ph(t, 0.5, 0.25), fill=RED, col=WHITE, size=60)
    elif name == "dowry":
        floor(c)
        k = ease(clamp(t / max(0.8, d * 0.8)))
        bx = lerp(260, 700, k)
        man(c, bx - 170, hip(0.9), 0.9, P(ra=(-80, -60), la=(80, 60), ll=(math.sin(t*12)*24*(k<1), 4), rl=(-math.sin(t*12)*24*(k<1), -4)), outfit="tycoon", mouth="grin", brow="raised")
        circle(c, bx, GROUND - 130, 130, fill=(0.6, 0.45, 0.25), stroke=INK, w=9)
        text(c, "£50M", bx, GROUND - 120, 66, WHITE, stroke=INK, sw=8)
        man(c, 930, hip(0.9), 0.9, P(ra=(-60, 60), la=(60, 60)), outfit="tycoon", mouth="smirk", brow="sly")
        text(c, "KESA", bx - 170, 520, 46, INK); text(c, "BUYER", 930, 520, 46, INK)
        counter(c, W / 2, 440, "£", 50, "M DOWRY", ph(t, 0.1, 0.8), size=110, col=GOLD)
    elif name == "car":
        floor(c)
        car(c, 420, GROUND - 52, 1.3)
        tagp(c, 420, 760, "£2", -0.08)
        tw_ = W_(4, "wallet") - s0
        if t > tw_ - 0.4:
            k = clamp((t - tw_ + 0.4) / 0.5)
            wallet(c, lerp(1000, 440, k), lerp(500, 920, k) - math.sin(k * math.pi) * 200, 1.2, k * 6)
        man(c, 880, hip(0.95), 0.95, P(ra=(-130, -60), la=(30, 20)), outfit=None, mouth="o" if t > tw_ else "smile", brow="raised")
    elif name == "opcap":
        floor(c)
        man(c, 420, hip(1.0), 1.0, P(ra=(-90, -70), la=(60, 40)), outfit="tycoon", mouth="grin", brow="one")
        rrect(c, 560, 520, 420, 260, 16, fill=WHITE, stroke=INK, lw=9)
        text(c, "TURNAROUND", 770, 600, 52, INK); text(c, "SPECIALISTS", 770, 680, 52, INK)
        for j in range(3):
            a_ = t * 4 + j * 2.1
            c.save(); c.translate(770, 920); c.rotate(a_)
            line(c, [(110, 0), (110, 40)], 12, GREEN); poly(c, [(90, 40), (130, 40), (110, 70)], fill=GREEN, stroke=None)
            c.restore()
        badge(c, W / 2, 1500, "OPCAPITA", ph(t, 0.2, 0.25), fill=WHITE, size=70)
    elif name == "admin":
        floor(c)
        calendar(c, 270, 560, "NOV '12", 1)
        ta = W_(6, "administration") - s0
        k = clamp((t - ta) / 0.8) if t > ta else 0
        building(c, 480, GROUND, 500, 500, "COMET", sign=COMET_BLUE, k=k * 0.5)
        if t > ta: stamp(c, "ADMINISTRATION", W / 2, 1450, clamp((t - ta) / 0.18), size=70, rot=-0.1); hitshake(tm, s0 + ta + 0.1, 18)
        badge(c, 290, 800, "9 MONTHS LATER", ph(t, 0.1, 0.25), size=44)
    elif name == "jobs":
        floor(c)
        badge(c, W / 2, 480, "236 STORES", ph(t, 0.05, 0.25), fill=COMET_BLUE, col=WHITE, size=80)
        n = int(18 * ease(ph(t, 0.4, 1.0)))
        for j in range(n):
            x_ = 120 + (j % 6) * 168; y_ = 930 + (j // 6) * 90
            stick(c, x_, y_, 0.32, P(), face="frown")
        counter(c, W / 2, 680, "", 6900, " JOBS", ph(t, 0.6, 0.9), size=120)
    elif name == "tax":
        floor(c)
        jar(c, W / 2, GROUND, 1 - 0.85 * ease(ph(t, 0.3, max(0.8, d - 0.4))), label="TAXPAYER", col=GREEN, hole=True)
        for j in range(8):
            k = ((t * 1.6 + j / 8) % 1)
            note(c, W / 2 + 120 + k * 380, GROUND - 40 - math.sin(k * math.pi) * 120 + k * 60, 0.7, k * 4)
        counter(c, W / 2, 520, "-£", 49, "M", ph(t, 0.2, 0.9), size=140)
        text(c, "redundancy pay + unpaid tax (BBC)", W / 2, 1450, 34, INK, alpha=0.6)
    elif name == "penny":
        floor(c)
        man(c, 300, hip(0.95), 0.95, P(ra=(-120, -60), la=(30, 20)), outfit="worker", mouth="frown", brow="worried")
        c.save(); c.translate(720, 760); c.scale(1.8, 1.8)
        circle(c, 0, 0, 80, fill=(0.75, 0.45, 0.25), stroke=INK, w=8); text(c, "1p", 0, 4, 70, INK)
        if t > 0.6: line(c, [(-20, -78), (10, -20), (-15, 20), (15, 78)], 6, INK)
        c.restore()
        badge(c, W / 2, 1500, "LESS THAN 1p IN THE £", ph(t, 0.3, 0.25), fill=RED, col=WHITE, size=64)
    elif name == "fair":
        floor(c)
        badge(c, W / 2, 480, "IN FAIRNESS...", ph(t, 0.05, 0.25), fill=WHITE, size=80)
        for j, (ox, r_) in enumerate(((-110, 80), (0, 105), (110, 85))):
            circle(c, 320 + ox, 700, r_, fill=(0.35, 0.37, 0.42), stroke=INK, w=7)
        text(c, "RECESSION", 320, 860, 46, INK)
        rrect(c, 640, 620, 320, 200, 12, fill=(0.78, 0.88, 0.96), stroke=INK, lw=8)
        poly(c, [(600, 820), (1000, 820), (1030, 870), (570, 870)], fill=GREY, stroke=INK, lw=7)
        text(c, "ONLINE", 800, 720, 54, BLUE)
        badge(c, W / 2, 1050, "\"WE WILL ASSIST FULLY\"", ph(t, d * 0.55, 0.25), fill=GOLD, size=52)
    elif name == "shut":
        floor(c)
        building(c, 300, GROUND, 480, 520, "COMET", sign=COMET_BLUE)
        k = ease(clamp(t / max(0.8, d * 0.6)))
        rrect(c, 312, GROUND - 400, 456, 400 * k, 4, fill=GREY, stroke=INK, lw=7)
        for j in range(int(10 * k)):
            line(c, [(320, GROUND - 400 + j * 40), (760, GROUND - 400 + j * 40)], 4, INK)
        badge(c, 800, 520, "79 YEARS", ph(t, 0.1, 0.25), size=58, rot=0.08)
        td = W_(11, "December") - s0
        if t > td: stamp(c, "CLOSED", 540, 900, clamp((t - td) / 0.18), size=110); hitshake(tm, s0 + td + 0.1, 18)
