
# ================= HOOVER free flights story =================
def topcard(c):
    rrect(c, 60, 150, W - 120, 210, 34, fill=WHITE, stroke=INK, lw=8)
    text(c, "FREE FLIGHTS THAT COST", W / 2, 215, 56, INK)
    sp_ = 22
    tot = tw(c, "£48M", 76) + tw(c, "...OOPS", 76) + sp_
    x = W / 2 - tot / 2
    text(c, "£48M", x, 298, 76, RED, align="left"); x += tw(c, "£48M", 76) + sp_
    text(c, "...OOPS", x, 298, 76, INK, align="left")

HL = {"barred", "barred.", "oi", "free", "mad.", "hostage.", "seats.", "miscalculated.", "plane.", "jobs."}
GOLDW = {"1992", "nineteen", "ninety-two,", "£100", "hundred", "pounds", "two", "220,000", "thousand", "six", "years.", "£48", "forty-eight", "million"}
CL = 15
SPIT_LI, SPIT_WORD, SPIT_BADGE = 12, "forty", "£48 MILLION?!"
MORAL_LI, MORAL_WORD, MORAL_BADGE = 13, "plane", "COUNT THE SEATS FIRST"
LABELS = {"jaw": "FREE?!", "facepalm": "OH NO", "wince": "OOF", "smug": "TOLD YOU"}
PUNCHW = [(3, "hoover"), (5, "mad"), (6, "seats"), (7, "hostage"), (9, "jobs"), (12, "forty"), (13, "plane")]
HOOV = (0.15, 0.32, 0.62)

SPEC = [
    ("warehouse", 0, None),
    ("offer", 1, None),
    ("map", 2, None),
    ("ny", 3, None),
    ("rush", 4, None),
    ("mad", 5, None),
    ("seats", 6, None),
    ("van", 7, None),
    ("tv", 8, None),
    ("fired", 9, None),
    ("fair", 10, None),
    ("flew", 11, None),
    ("bill", 12, None),
    ("spit", 12, "forty"),
    ("moral", 13, None),
    ("bell", 14, None),
    ("cheeky", 15, None),
]

def reactions():
    return [
        (W_(3, "hoover") + 0.05, W_(3, "hoover") + 1.2, "jaw", 895, 560),
        (W_(6, "seats") + 0.05, W_(6, "seats") + 1.1, "facepalm", 170, 560),
        (W_(9, "jobs") + 0.0, W_(9, "jobs") + 1.1, "wince", 180, 1440),
    ]

def ticket(c, x, y, s=1.0, ang=0, label="FREE FLIGHT"):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -130, -55, 260, 110, 12, fill=WHITE, stroke=INK, lw=6)
    rrect(c, -130, -55, 60, 110, 12, fill=RED, stroke=INK, lw=6)
    text(c, label, 30, 6, 30, INK)
    c.restore()

def crowd_man(c, x, t, j, carry=True, s=0.75):
    man(c, x, hip(s), s, walkpose(t + j * 0.3, sp=16, amp=30), mouth="grin", brow="raised",
        outfit=[None, "pensioner", "worker"][j % 3])
    if carry: vacuum(c, x + 60 * s, GROUND, 0.55 * s / 0.75)

def story(c, name, t, d, li, s0, tm):
    if name == "warehouse":
        floor(c)
        # action hook: warehouse doors burst and vacuums avalanche out
        k = clamp(t / 0.25)
        rrect(c, 120, 440, 840, 680, 10, fill=(0.82, 0.82, 0.86), stroke=INK, lw=10)
        poly(c, [(100, 440), (540, 330), (980, 440)], fill=(0.65, 0.65, 0.72), stroke=INK, lw=9)
        text(c, "WAREHOUSE", W / 2, 420, 48, INK)
        dw = 320 * ease(k)
        rrect(c, 380 - dw / 2, 640, 160, 480, 4, fill=GREY, stroke=INK, lw=8)
        rrect(c, 540 + dw / 2, 640, 160, 480, 4, fill=GREY, stroke=INK, lw=8)
        if k >= 1: hitshake(tm, s0 + 0.25, 22)
        for j in range(9):
            p = clamp((t - 0.2 - j * 0.07) * 1.2)
            if p <= 0: continue
            a_ = -math.pi / 2 + (j - 4) * 0.3
            vacuum(c, W / 2 + math.cos(a_) * 480 * p, 1000 + math.sin(a_) * 500 * p + 520 * p * p, 0.45, p * 6 + j)
        badge(c, 200, 520, "1992", ph(t, 0.1, 0.25), size=70)
        tb = W_(0, "brilliant") - s0
        if t > tb: badge(c, W / 2, 1500, "A BRILLIANT IDEA", ph(t, tb, 0.25), fill=GOLD, size=70)
    elif name == "offer":
        floor(c)
        vacuum(c, 300, GROUND, 1.0, math.sin(t * 3) * 0.04)
        rrect(c, 170, 520, 230, 120, 14, fill=GOLD, stroke=INK, lw=8); text(c, "£100+", 285, 584, 58, INK)
        tf = W_(1, "two") - s0
        for j in range(2):
            k = pop(ph(t, tf + j * 0.2, 0.3))
            if k > 0: ticket(c, 760, 640 + j * 190, k * 1.2, -0.08 + j * 0.12)
        if t > tf: badge(c, W / 2, 1500, "TWO FREE FLIGHTS", ph(t, tf, 0.25), fill=RED, col=WHITE, size=72)
    elif name == "map":
        floor(c)
        ta = W_(2, "America") - s0
        am = t > ta
        k = clamp(t / max(0.5, d))
        plane(c, lerp(-200, W + 200, k), 760 - 160 * math.sin(k * math.pi), 1.1, ang=-0.15 + 0.3 * k)
        for j in range(6):
            circle(c, (j * 210 + t * 160) % (W + 200) - 100, 520 + (j % 3) * 70, 50, fill=WHITE, stroke=None, a=0.8)
        if am:
            badge(c, W / 2, 1480, "...AND AMERICA!", ph(t, ta, 0.25), fill=RED, col=WHITE, size=76, rot=0.05)
        else:
            badge(c, W / 2, 1480, "EUROPE", ph(t, 0.1, 0.25), fill=WHITE, size=76)
    elif name == "ny":
        floor(c)
        # seesaw: tiny vacuum vs giant plane ticket
        k = ease(clamp((t - 0.3) / 0.6))
        ang = 0.32 * k
        c.save(); c.translate(W / 2, 900)
        poly(c, [(-40, 220), (40, 220), (0, 0)], fill=GREY, stroke=INK, lw=8)
        c.rotate(ang); line(c, [(-420, 0), (420, 0)], 14, INK); c.restore()
        lx, ly = W / 2 - 420 * math.cos(ang), 900 - 420 * math.sin(ang)
        rx, ry = W / 2 + 420 * math.cos(ang), 900 + 420 * math.sin(ang)
        vacuum(c, lx - 30, ly - 8, 0.45)
        ticket(c, rx, ry - 70, 1.0, -ang, "NEW YORK")
        text(c, "£100ish", lx, ly - 230, 50, GOLD, stroke=INK, sw=8)
        text(c, "FLIGHTS!", rx, ry - 170, 56, RED, stroke=INK, sw=8)
    elif name == "rush":
        floor(c)
        # a stampede running in from the right toward the shop
        building(c, 60, GROUND, 360, 470, "ELECTRICALS", sign=HOOV)
        for j in range(7):
            x_ = W + 80 - ((t * 520 + j * 140) % 900)
            man(c, x_, hip(0.7), 0.7, walkpose(t + j, sp=20, amp=34), mouth="grin", brow="raised", outfit=[None, "pensioner", "worker"][j % 3], flip=True)
        motion_lines(c, 880, 900, n=5, d=-1)
        badge(c, W / 2, 1500, "UH OH...", ph(t, 0.3, 0.25), fill=GOLD, size=76)
    elif name == "mad":
        floor(c)
        for j in range(5):
            x_ = ((t * 260 + j * 230) % 1300) - 150
            crowd_man(c, x_, t, j)
        tc = W_(5, "cheapest") - s0
        if t > tc: badge(c, W / 2, 1500, "JUST FOR THE TICKETS", ph(t, tc, 0.25), fill=RED, col=WHITE, size=64)
        else: badge(c, W / 2, 560, "HOOVER MAD", ph(t, 0.1, 0.25), fill=GOLD, size=80, rot=0.05)
    elif name == "seats":
        floor(c)
        plane(c, W / 2, 720, 2.2)
        for j in range(10):
            circle(c, W / 2 + 200 - j * 44, 707, 14, fill=GOLD, stroke=INK, w=4)
        ts_ = W_(6, "seats") - s0
        for j in range(4):
            man(c, 150 + j * 250, hip(0.75), 0.75, P(ra=(-120, -60), la=(120, 60)), mouth="frown" if t > ts_ else "o", brow="worried")
        if t > ts_: stamp(c, "FULL", W / 2, 1450, clamp((t - ts_) / 0.18), size=110); hitshake(tm, s0 + ts_ + 0.1, 16)
    elif name == "van":
        floor(c)
        # Hoover-blue van with a cross customer stood on the roof
        x0 = W / 2
        rrect(c, x0 - 320, 700, 520, 330, 18, fill=HOOV, stroke=INK, lw=9)
        poly(c, [(x0 + 200, 780), (x0 + 300, 780), (x0 + 340, 900), (x0 + 340, 1030), (x0 + 200, 1030)], fill=HOOV, stroke=INK, lw=9)
        rrect(c, x0 + 220, 800, 80, 80, 8, fill=(0.78, 0.88, 0.96), stroke=INK, lw=6)
        text(c, "HOOVER", x0 - 60, 860, 70, WHITE)
        for wx in (x0 - 200, x0 + 220):
            circle(c, wx, 1050, 60, fill=INK, stroke=INK, w=6); circle(c, wx, 1050, 22, fill=GREY, stroke=None)
        th = W_(7, "hostage") - s0
        man(c, x0 - 80, 700 - 210 * 0.8, 0.8, P(ra=(-150, -120) if t > th else (-90, -40), la=(150, 120) if t > th else (40, 20)),
            mouth="scream" if t > th else "frown", brow="angry", outfit="worker")
        badge(c, 230, 520, "CUMBRIA", ph(t, 0.1, 0.25), fill=(0.1, 0.45, 0.25), col=WHITE, size=58)
        if t > th: stamp(c, "MINE NOW", W / 2, 1450, clamp((t - th) / 0.18), size=90); hitshake(tm, s0 + th + 0.1, 16)
    elif name == "tv":
        floor(c)
        rrect(c, 90, 500, 460, 340, 22, fill=INK, stroke=INK, lw=8)
        rrect(c, 115, 525, 410, 290, 12, fill=(0.75, 0.85, 0.95))
        text(c, "WATCHDOG", 320, 600, 52, RED)
        man(c, 320, 780, 0.45, P(ra=(-120, -40), la=(30, 20)), mouth="o", brow="angry", outfit="mp")
        line(c, [(220, 840), (190, 900)], 10, INK); line(c, [(420, 840), (450, 900)], 10, INK)
        tp = W_(8, "Parliament") - s0
        if t > tp:
            k = pop(ph(t, tp, 0.3))
            c.save(); c.translate(800, GROUND); c.scale(k, k)
            rrect(c, -40, -620, 80, 620, 4, fill=(0.85, 0.75, 0.5), stroke=INK, lw=8)
            circle(c, 0, -520, 34, fill=WHITE, stroke=INK, w=6)
            poly(c, [(-50, -620), (0, -720), (50, -620)], fill=(0.6, 0.5, 0.3), stroke=INK, lw=7)
            rrect(c, -220, -300, 440, 300, 4, fill=(0.85, 0.75, 0.5), stroke=INK, lw=8)
            c.restore()
            badge(c, 800, 1480, "PARLIAMENT", k, fill=WHITE, size=60)
    elif name == "fired":
        floor(c)
        tj = W_(9, "jobs") - s0
        for j in range(3):
            x_ = 240 + j * 300 + (t - tj) * 180 * (t > tj)
            man(c, x_, hip(0.85), 0.85, P(ra=(-60, -20), la=(60, 20)), outfit="tycoon", mouth="frown" if t > tj else "flat", brow="worried")
            box(c, x_ - 80, hip(0.85) - 60, 160, 90, "DESK")
        if t > tj: stamp(c, "OUT", W / 2, 1450, clamp((t - tj) / 0.18), size=120); hitshake(tm, s0 + tj + 0.1, 14)
        badge(c, W / 2, 520, "3 TOP EXECUTIVES", ph(t, 0.1, 0.25), fill=GOLD, size=64)
    elif name == "fair":
        floor(c)
        badge(c, W / 2, 480, "IN FAIRNESS...", ph(t, 0.05, 0.25), fill=WHITE, size=80)
        rrect(c, 140, 600, 800, 260, 16, fill=WHITE, stroke=INK, lw=8)
        text(c, "TRADING STANDARDS:", W / 2, 670, 46, INK)
        text(c, "\"NO INTENT TO DECEIVE\"", W / 2, 760, 50, GREEN if "GREEN" in globals() else BLUE)
        tm_ = W_(10, "miscalculated") - s0
        if t > tm_:
            badge(c, W / 2, 1000, "BUT THE MATHS...", ph(t, tm_, 0.25), fill=RED, col=WHITE, size=64)
            text(c, "1 + 1 = 7", W / 2, 1450, 90, INK, alpha=clamp((t - tm_) / 0.3))
    elif name == "flew":
        floor(c)
        counter(c, W / 2, 560, "", 220000, "", ph(t, 0.05, 0.9), size=150, col=GOLD)
        badge(c, W / 2, 700, "PEOPLE FLEW", ph(t, 0.6, 0.25), fill=WHITE, size=56)
        for j in range(3):
            plane(c, ((t * 400 + j * 420) % (W + 400)) - 200, 860 + j * 40, 0.5, ang=-0.1)
        tc = W_(11, "court") - s0
        if t > tc:
            k = clamp((t - tc) * 3)
            c.save(); c.translate(W / 2, 1060); c.rotate(-0.6 + 0.6 * abs(math.sin(t * 6)))
            rrect(c, -20, -10, 200, 30, 8, fill=WOOD, stroke=INK, lw=6); rrect(c, 140, -60, 80, 120, 10, fill=WOOD2, stroke=INK, lw=6)
            c.restore()
            badge(c, W / 2, 1480, "6 YEARS IN COURT", k, fill=RED, col=WHITE, size=64)
    elif name == "bill":
        floor(c)
        # receipt unrolling down the screen
        k = ease(clamp(t / max(0.6, d)))
        rrect(c, 280, 420, 520, 120 + 560 * k, 6, fill=WHITE, stroke=INK, lw=8)
        text(c, "THE BILL", W / 2, 490, 56, INK)
        for j in range(int(6 * k)):
            line(c, [(330, 570 + j * 80), (750 - (j * 37) % 160, 570 + j * 80)], 8, GREY)
        man(c, 900, hip(0.8), 0.8, P(ra=(-130, -90), la=(30, 20)), outfit="tycoon", mouth="teeth", brow="worried", sweat=t * 1.5)
