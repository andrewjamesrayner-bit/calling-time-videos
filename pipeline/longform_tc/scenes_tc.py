# Thomas Cook long-form scenes (exec'd inside lf.py after scenes4.py)
SEA = (0.16, 0.38, 0.55)
SAND = (0.80, 0.68, 0.42)

def _palm(c, px, base, h=380):
    line(c, [(px, base), (px + 20, base - h)], 18, (0.55, 0.4, 0.25))
    for j in range(5):
        a = -math.pi / 2 + (j - 2) * 0.55
        line(c, [(px + 20, base - h), (px + 20 + math.cos(a) * 140, base - h + math.sin(a) * 90 + 60)], 14, (0.3, 0.6, 0.3))

def sc_beach(c, p, t, d):
    night = p.get("night", False)
    # sea + sand
    rrect(c, 0, GROUND - 40, W, 120, 0, fill=SEA, a=0.55 if night else 0.9)
    for k in range(6):
        x0 = ((t * 60 + k * 340) % (W + 300)) - 150
        line(c, [(x0, GROUND - 10), (x0 + 120, GROUND - 10)], 5, INK, 0.25)
    rrect(c, 0, GROUND + 80, W, H - GROUND - 80, 0, fill=SAND, a=0.35 if night else 0.75)
    if night:
        circle(c, 1650, 170, 60, fill=INK, stroke=None, a=0.9)
        circle(c, 1675, 155, 55, fill=BG, stroke=None)
        for k in range(14):
            circle(c, (k * 263) % W, 60 + (k * 97) % 300, 3, fill=INK, stroke=None, a=0.5 + 0.5 * math.sin(t * 3 + k))
    else:
        circle(c, 1650, 170, 70, fill=GOLD, stroke=None)
    _palm(c, 160, GROUND + 90); _palm(c, W - 240, GROUND + 90, 330)
    n = p.get("n", 5)
    for j in range(n):
        x = 420 + j * 230
        if night:
            # asleep on sunloungers
            rrect(c, x - 90, GROUND + 120, 180, 22, 8, fill=GOLD if j % 2 else RED)
            circle(c, x - 70, GROUND + 100, 24, fill=BG, stroke=INK, w=7)
            line(c, [(x - 46, GROUND + 112), (x + 80, GROUND + 112)], 9, INK)
            text(c, "z", x - 40 + 10 * math.sin(t * 2 + j), GROUND + 40 - (t * 30 + j * 20) % 60, 36, INK, alpha=0.7)
        else:
            mood = p.get("mood", "smile")
            stickman(c, x, GROUND + 140 + math.sin(t * 2 + j) * 3, s=0.7, la=(20, 10), ra=(-20, -10),
                     mouth=mood if mood != "mix" else ["sad", "o", "flat"][j % 3], case=p.get("cases", False))
    if p.get("plane"):
        plane(c, lerp(-300, W + 300, ph(t, 0, max(d, 1.5))), 230, 0.7, INK, -0.05)
    capbox(c, p.get("cap"), t, y=110)

def sc_board(c, p, t, d):
    rows = p.get("rows", ["MALAGA", "PALMA", "TENERIFE", "CANCUN", "DALAMAN"])
    st = p.get("status", "ON TIME"); flip = p.get("flip", None)
    x, y, w = 360, 210, 1200
    rrect(c, x, y, w, 90 + 72 * len(rows), 14, fill=(0.07, 0.07, 0.09), stroke=INK, lw=6)
    text(c, "DEPARTURES", x + 40, y + 48, 44, GOLD, align="left", spacing=4)
    text(c, "THOMAS COOK", x + w - 40, y + 48, 34, INK, align="right", spacing=2)
    for k, r in enumerate(rows):
        yy = y + 125 + k * 72
        a = 1.0 if p.get('instant') else ease(ph(t, 0.05 + k * 0.08, 0.25))
        text(c, r, x + 40, yy, 42, INK, align="left", alpha=a)
        text(c, f"TC{1200 + k * 37}", x + 520, yy, 36, GREY, align="left", alpha=a)
        if flip is not None and t >= flip + k * 0.18:
            on = int((t - flip) * 4) % 2 == 0 or t > flip + 1.6
            text(c, "CANCELLED", x + w - 40, yy, 42, RED, align="right", alpha=1 if on else 0.3)
        else:
            text(c, st, x + w - 40, yy, 42, (0.35, 0.75, 0.4), align="right", alpha=a)
    capbox(c, p.get("cap"), t, y=120)

def sc_merge(c, p, t, d):
    floor(c)
    m = ease_io(ph(t, 0.3, 1.0))
    a, b = p["a"], p["b"]
    building(c, lerp(200, 520, m), FL, 420, 330, a)
    building(c, lerp(1300, 980, m), FL, 420, 330, b)
    sc = pop(ph(t, 1.3, 0.4))
    if sc > 0.02:
        lab = p.get("label", "MERGED")
        c.save(); c.translate(W / 2, 250); c.scale(sc, sc)
        wd = tw(c, lab, 72) + 80
        rrect(c, -wd / 2, -60, wd, 120, 14, fill=GOLD); text(c, lab, 0, 0, 72, BG); c.restore()
    capbox(c, p.get("cap"), t, y=120)

def sc_sack(c, p, t, d):
    floor(c)
    x = lerp(1300, 900, ease_io(ph(t, 0, max(d, 1.0))))
    st = math.sin(t * 5) * 16
    stickman(c, x, GROUND, la=(150, 100), ra=(130, 90), ll=st, rl=-st, mouth="sad", tie=p.get("tie", False))
    r = p.get("r", 170)
    sx = x + 250 + r * 0.4
    line(c, [(x + 120, GROUND - 120), (sx - r * 0.6, FL - r * 1.2)], 7, INK)
    circle(c, sx, FL - r * 0.95, r, fill=(0.35, 0.3, 0.25), stroke=INK, w=8)
    poly(c, [(sx - 30, FL - r * 1.9), (sx + 30, FL - r * 1.9), (sx + 50, FL - r * 2.1), (sx - 50, FL - r * 2.1)], fill=(0.35, 0.3, 0.25), stroke=INK, lw=6)
    text(c, p.get("label", "DEBT"), sx, FL - r * 0.95, fit(c, p.get("label", "DEBT"), 80, r * 1.6), RED)
    for k in range(4):
        circle(c, x - 140 - k * 40, FL - 10 - k * 6, 10 + k * 5, fill=INK, stroke=None, a=0.15)
    if p.get("v"):
        pre, xx, suf, comma, dec = parse_val(p["v"])
        s_ = fmt(pre, xx * ease(ph(t, 0.1, min(1.0, d * 0.5))), suf, comma, dec)
        text(c, s_, 520, 300, 150, RED)
    capbox(c, p.get("cap"), t, y=120)

def sc_banks(c, p, t, d):
    floor(c)
    n = p.get("n", 17)
    for j in range(n):
        sc = pop(ph(t, j * 0.05, 0.25))
        if sc < 0.02: continue
        row = 0 if j < 9 else 1
        col_ = j if row == 0 else j - 9
        x = 120 + col_ * 190 + row * 95; y = FL if row == 0 else FL - 300
        c.save(); c.translate(x + 75, y); c.scale(sc, sc); c.translate(-(x + 75), -y)
        building(c, x, y, 150, 200, None, cols=True)
        c.restore()
    if p.get("v"):
        text(c, p["v"], W / 2, 250, 140, GOLD)
    capbox(c, p.get("cap"), t, y=110)

def sc_shops(c, p, t, d):
    # rows of little shopfronts that swap sign name at a trigger
    floor(c)
    sw = p.get("swap_at", None)
    for j in range(8):
        x = 110 + j * 215
        nm = p.get("b", "HAYS") if (sw is not None and t >= sw + j * 0.08) else p.get("a", "THOMAS COOK")
        shopfront(c, x, FL, 190, 300, nm, sign=GOLD if nm == p.get("b", "HAYS") else RED)
    if p.get("v"):
        text(c, p["v"], W / 2, 300, 150, GOLD)
    capbox(c, p.get("cap"), t, y=120)

SCN.update(beach=sc_beach, board=sc_board, merge=sc_merge, sack=sc_sack, banks=sc_banks, shops=sc_shops)
