# Extra animated scenes for long-form v2 (stickman-video-director B1 rules: every shot <=3s, picture changes on story beats)
FL = GROUND + 160  # floor y

def walker(c, x, s=1.0, t=0, mouth="smile", tie=False, case=False, col=INK):
    w = math.sin(t * 7) * 20
    stickman(c, x, GROUND + (1 - s) * 160 * 0 + 160 * (1 - s), s=s, la=(18 + w, 10), ra=(-18 - w, -10), ll=w, rl=-w, mouth=mouth, tie=tie, case=case, col=col)

def sc_street(c, p, t, d):
    names = p.get("names", ["SHOP"] * 4); hi = p.get("hi", -1)
    n = len(names); wdt = min(380, (W - 200) / n - 30)
    floor(c)
    for j, nm in enumerate(names):
        sc = pop(ph(t, 0.05 + j * 0.12, 0.35))
        if sc < 0.02: continue
        x = 100 + j * (wdt + 30)
        c.save(); c.translate(x + wdt / 2, FL); c.scale(1, sc); c.translate(-(x + wdt / 2), -FL)
        shopfront(c, x, FL, wdt, 430, nm, sign=RED if j == hi else GREY, shutter=p.get("shut", 0) if j == hi else 0)
        c.restore()
    for k in range(3):
        x = ((t * 120 + k * 600) % (W + 200)) - 100
        walker(c, x, 0.7, t + k, mouth="smile")
    capbox(c, p.get("cap"), t)

def sc_bigshop(c, p, t, d):
    floor(c)
    k = pop(ph(t, 0, 0.45)) if p.get("rise") else 1.0
    x0, w0 = 560, 800
    c.save(); c.translate(W / 2, FL); c.scale(1, k); c.translate(-W / 2, -FL)
    shopfront(c, x0, FL, w0, 560, p.get("name", "BHS"), sign=p.get("sign", RED), shutter=ease(ph(t, 0.3, 1.2)) * p.get("shut", 0))
    c.restore()
    if p.get("faded"):
        setc(c, BG, 0.55); c.rectangle(x0 - 10, FL - 570, w0 + 20, 580); c.fill()
    if p.get("people", True) and not p.get("faded"):
        for j in range(3):
            ph0 = (t * 0.25 + j / 3) % 1
            walker(c, lerp(200, 900, ph0), 0.75, t + j, mouth="smile", case=(j == 1))
    if p.get("solo"):
        stickman(c, 330, GROUND, la=(30, 20), ra=(-30, -20), mouth=p.get("mood", "flat"), tie=p.get("tie", False))
    sg = p.get("sign_text")
    if sg:
        s2 = pop(ph(t, p.get("sign_at", 0.5), 0.35))
        if s2 > 0.02:
            c.save(); c.translate(1300, 300); c.rotate(-0.08); c.scale(s2, s2)
            wd = tw(c, sg, 70) + 80
            rrect(c, -wd / 2, -60, wd, 120, 10, fill=p.get("sign_col", RED), stroke=INK, lw=6); text(c, sg, 0, 0, 70, INK); c.restore()
    if p.get("year"):
        s3 = pop(ph(t, 0.1, 0.35))
        yw = max(300, tw(c, p["year"], 70) + 70); c.save(); c.translate(80 + yw / 2, 230); c.scale(s3, s3); rrect(c, -yw / 2, -55, yw, 110, 12, fill=GOLD); text(c, p["year"], 0, 0, 70, BG); c.restore()
    capbox(c, p.get("cap"), t)

def sc_count(c, p, t, d):
    pre, x, suf, comma, dec = parse_val(p["v"])
    k = ease(ph(t, 0.1, min(1.0, d * 0.5)))
    sval = fmt(pre, x * k, suf, comma, dec)
    col = COL[p.get("col", "gold")]
    icon = p.get("icon", "notes")
    if icon == "notes":
        for j in range(18):
            ph0 = (t * 0.6 + j / 18) % 1
            note(c, 120 + (j * 197) % (W - 240), -60 + ph0 * (FL + 100), 0.8, ph0 * 6 + j)
    elif icon == "people":
        n = min(40, int(40 * k) + 1)
        for j in range(n):
            xx = 160 + (j % 20) * 82; yy = 760 + (j // 20) * 120
            stickman(c, xx, yy, s=0.42, la=(15, 8), ra=(-15, -8), mouth="sad", case=True)
    elif icon == "shops":
        n = min(24, int(24 * k) + 1)
        for j in range(n):
            xx = 180 + (j % 12) * 135; yy = 720 + (j // 12) * 150
            rrect(c, xx - 55, yy - 60, 110, 110, 6, fill=DARK, stroke=INK, lw=4); rrect(c, xx - 55, yy - 60, 110, 26, 6, fill=RED)
    rrect(c, W / 2 - 560, 250, 1120, 330, 26, fill=BG, a=0.85)
    text(c, sval, W / 2, 380, fit(c, sval, 220, 1000), col)
    text(c, p.get("label", ""), W / 2, 520, fit(c, p.get("label", ""), 48, 1050), INK, alpha=ease(ph(t, 0.4, 0.4)))

def sc_flow(c, p, t, d):
    floor(c)
    shopfront(c, 140, FL, 520, 480, p.get("a", "BHS"), sign=RED)
    stickman(c, 1520, GROUND, la=(-120, -150), ra=(120, 150), tie=True, mouth="smile")
    for j in range(10):
        ph0 = (t * 0.8 + j / 10) % 1
        xx = lerp(560, 1450, ph0); yy = lerp(520, 560, ph0) - math.sin(ph0 * math.pi) * 260
        note(c, xx, yy, 0.9, ph0 * 6 + j)
    if p.get("v"):
        pre, x, suf, comma, dec = parse_val(p["v"])
        k = ease(ph(t, 0.15, min(1.0, d * 0.5)))
        s_ = fmt(pre, x * k, suf, comma, dec)
        text(c, s_, W / 2 + 120, 235, 130, COL[p.get("col", "red")])
    for j, lab in enumerate(p.get("tags", [])):
        sc = pop(ph(t, 0.3 + j * 0.45, 0.3))
        if sc < 0.02: continue
        c.save(); c.translate(1100 + (j - 1) * 260, 370); c.scale(sc, sc); c.rotate((j - 1) * 0.05)
        wd = tw(c, lab, 44) + 50; rrect(c, -wd / 2, -40, wd, 80, 10, fill=GOLD); text(c, lab, 0, 0, 44, BG); c.restore()
    capbox(c, p.get("cap"), t, y=95 if p.get("v") else 120)

def sc_jar(c, p, t, d):
    floor(c)
    a, b = p.get("from", 0.8), p.get("to", 0.8)
    cur = lerp(a, b, ease(ph(t, 0.2, max(0.5, d * 0.7))))
    x0 = 760
    rrect(c, x0 - 10, FL - 560, 420, 560, 50, fill=DARK, stroke=INK, lw=8)
    rrect(c, x0 + 50, FL - 610, 300, 60, 14, fill=GREY, stroke=INK, lw=6)
    fh = 500 * cur
    colj = (0.25, 0.6, 0.35) if cur > 0.45 else (0.75, 0.55, 0.15) if cur > 0.2 else RED
    if fh > 4: rrect(c, x0 + 15, FL - 25 - fh, 370, fh, 30, fill=colj)
    if p.get("crack"):
        line(c, [(x0 + 100, FL - 540), (x0 + 160, FL - 420), (x0 + 110, FL - 300), (x0 + 180, FL - 160)][:1 + int(4 * ph(t, 0.1, 0.6)) or 1], 8, INK)
    rrect(c, x0 + 40, FL - 360, 320, 90, 10, fill=PAPER, stroke=INK, lw=5); text(c, "PENSION", x0 + 200, FL - 315, 56, BG)
    for xx in (420, 1440):
        stickman(c, xx, GROUND, s=0.9, la=(25, 15), ra=(-25, -15), mouth="smile" if cur > 0.45 else "sad")
    if p.get("v"):
        text(c, p["v"], W / 2 + 200, 205, fit(c, p["v"], 100, 900), COL[p.get("col", "red")], alpha=ease(ph(t, 0.3, 0.4)))
    capbox(c, p.get("cap"), t, y=95 if p.get("v") else 150)

def sc_chart(c, p, t, d):
    pts = p["pts"]; k = ease(ph(t, 0.1, max(0.6, d * 0.75)))
    x0, y0, w, h = 300, 220, 1320, 560
    line(c, [(x0, y0), (x0, y0 + h), (x0 + w, y0 + h)], 6, INK, 0.6)
    n = max(2, int(len(pts) * k) + 1); use = pts[:min(len(pts), n)]
    col = COL[p.get("col", "red")]
    line(c, [(x0 + px * w, y0 + (1 - py) * h) for px, py in use], 12, col)
    lx, ly = use[-1]; circle(c, x0 + lx * w, y0 + (1 - ly) * h, 16, fill=col, stroke=INK, w=4)
    for j, lab in enumerate(p.get("xl", [])):
        text(c, lab, x0 + j * w / (len(p["xl"]) - 1), y0 + h + 50, 36, INK, alpha=0.7)
    if p.get("big"):
        text(c, p["big"], x0 + w - 200, y0 + 80, 110, col, alpha=ease(ph(t, 0.5, 0.4)))
    capbox(c, p.get("cap"), t, y=120)

def sc_paper(c, p, t, d):
    k = ph(t, 0, 0.5); sc = pop(k); rot = (1 - ease(k)) * -0.8 - 0.03
    c.save(); c.translate(W / 2, 470); c.rotate(rot); c.scale(sc, sc)
    rrect(c, -620, -330, 1240, 660, 6, fill=PAPER, stroke=INK, lw=6)
    text(c, p.get("mast", "THE DAILY STICK"), 0, -270, 54, BG)
    line(c, [(-570, -228), (570, -228)], 5, BG)
    hs = fit(c, p["h"], 110, 1120)
    text(c, p["h"], 0, -120, hs, RED)
    text(c, p.get("sub", ""), 0, -10, 44, BG)
    for j in range(4): line(c, [(-570, 80 + j * 55), (570 - (j % 2) * 260, 80 + j * 55)], 14, (0.75, 0.73, 0.68))
    c.restore()

def sc_committee(c, p, t, d):
    rrect(c, 260, 640, 1400, 120, 8, fill=(0.35, 0.22, 0.14), stroke=INK, lw=5)
    for j in range(5):
        x = 420 + j * 270
        nod = math.sin(t * 3 + j) * 4
        stickman(c, x, 640 + nod, s=0.75, la=(40, 60), ra=(-40, -60), tie=True, mouth="flat")
    rrect(c, 300, 760, 1320, 50, 4, fill=GOLD); text(c, p.get("plate", "MPs' COMMITTEE · 2016"), W / 2, 785, 34, BG)
    q = p.get("q")
    if q:
        sc = pop(ph(t, 0.3, 0.4))
        if sc > 0.02:
            c.save(); c.translate(W / 2, 250); c.scale(sc, sc)
            qs = fit(c, q, 70, 1300); wd = tw(c, q, qs) + 100
            rrect(c, -wd / 2, -80, wd, 160, 30, fill=PAPER, stroke=INK, lw=6)
            poly(c, [(-40, 78), (40, 78), (0, 150)], fill=PAPER)
            text(c, q, 0, 0, qs, RED); c.restore()

def sc_deal(c, p, t, d):
    floor(c)
    k1 = ease(ph(t, 0.15, 0.6))
    stickman(c, 700, GROUND, la=(30, 20), ra=(-85 + 25 * (1 - k1), -10), tie=True, mouth="smile")
    stickman(c, 1220, GROUND, la=(85 - 25 * (1 - k1), 10), ra=(-30, -20), mouth="smile", helmet=p.get("helmet", True))
    shopfront(c, 80, FL, 420, 460, p.get("name", "BHS"), sign=RED)
    sc = pop(ph(t, 0.55, 0.4))
    if sc > 0.02:
        c.save(); c.translate(W / 2 + 10, 330); c.scale(sc, sc); c.rotate(math.sin(t * 3) * 0.1); coin(c, 0, 0, 130, p.get("coin", "£1")); c.restore()
    capbox(c, p.get("cap"), t, y=120)

def sc_think(c, p, t, d):
    floor(c)
    stickman(c, 700, GROUND, la=(40, 120), ra=(-60, -150), mouth=p.get("mood", "flat"), tie=p.get("tie", False), helmet=p.get("helmet", False))
    for j, r in enumerate((14, 22, 32)):
        circle(c, 800 + j * 45, 420 - j * 50, r, fill=DARK, stroke=INK, w=4, a=ease(ph(t, 0.1 + j * 0.1, 0.2)))
    sc = pop(ph(t, 0.25, 0.35))
    if sc > 0.02:
        c.save(); c.translate(1250, 300); c.scale(sc, sc)
        s = p.get("bubble", "?"); fs = fit(c, s, 80, 700); wd = max(300, tw(c, s, fs) + 100)
        rrect(c, -wd / 2, -110, wd, 220, 60, fill=DARK, stroke=INK, lw=6); text(c, s, 0, 0, fs, COL[p.get("col", "gold")]); c.restore()
    capbox(c, p.get("cap"), t, y=120)

def sc_tycoon(c, p, t, d):
    floor(c)
    x = lerp(500, 900, ease_io(ph(t, 0, d)))
    w = math.sin(t * 6) * 18
    stickman(c, x, GROUND, la=(30 + w * 0.3, 10), ra=(-30, -10), ll=w, rl=-w, tie=True, mouth="smile", hat=p.get("hat", False))
    for side in (-1, 1):
        bx = x + side * 120
        circle(c, bx, GROUND + 60, 70, fill=(0.75, 0.6, 0.3), stroke=INK, w=5)
        text(c, "£", bx, GROUND + 64, 70, BG)
    if p.get("v"):
        text(c, p["v"], x, 230, 130, COL[p.get("col", "gold")], alpha=ease(ph(t, 0.2, 0.4)))
    capbox(c, p.get("cap"), t, y=120)

def sc_scale(c, p, t, d):
    (la_, av), (lb_, bv) = p["a"], p["b"]
    ang = 0.22 * ease(ph(t, 0.5, 0.8)) * (1 if bv > av else -1)
    cx, cy = W / 2, 330
    poly(c, [(cx - 50, FL), (cx + 50, FL), (cx, cy)], fill=GREY, stroke=INK, lw=5)
    floor(c)
    dx, dy = math.cos(ang) * 520, math.sin(ang) * 520
    line(c, [(cx - dx, cy - dy), (cx + dx, cy + dy)], 12, INK)
    for side, lab, v, col in ((-1, la_, av, GOLD), (1, lb_, bv, RED)):
        px, py = cx + side * dx, cy + side * dy
        line(c, [(px, py), (px - 110, py + 190)], 4, INK); line(c, [(px, py), (px + 110, py + 190)], 4, INK)
        line(c, [(px - 150, py + 190), (px + 150, py + 190)], 10, INK)
        n = max(1, int(v / max(av, bv) * 9))
        for j in range(n): note(c, px - 90 + (j % 3) * 90, py + 165 - (j // 3) * 40, 0.7)
        text(c, lab, px, py + 260, 44, col)
    capbox(c, p.get("cap"), t, y=120)

def sc_crowd(c, p, t, d):
    floor(c)
    n = min(30, int(30 * ease(ph(t, 0, min(1.2, d * 0.6)))) + 1)
    for j in range(n):
        xx = 140 + (j % 15) * 115 + (j // 15) * 55; yy = GROUND + 30 + (j // 15) * 90
        stickman(c, xx, yy, s=0.55, la=(15, 8), ra=(-15, -8), mouth="sad", case=True)
    if p.get("v"):
        pre, x, suf, comma, dec = parse_val(p["v"])
        s_ = fmt(pre, x * ease(ph(t, 0.1, min(1.0, d * 0.5))), suf, comma, dec)
        text(c, s_, W / 2, 230, 170, COL[p.get("col", "red")])
    capbox(c, p.get("cap"), t, y=380 if p.get("v") else 150)

def sc_storm(c, p, t, d):
    floor(c)
    shopfront(c, 560, FL, 800, 520, p.get("name", "BHS"), sign=RED, shutter=p.get("shut", 0))
    for (ox, r) in ((-180, 110), (-40, 150), (120, 120), (240, 90)):
        circle(c, W / 2 + ox, 150, r, fill=(0.25, 0.25, 0.28), stroke=None)
    for j in range(28):
        rx = 560 + (j * 97) % 800; ry = 220 + ((t * 700 + j * 53) % 560)
        line(c, [(rx, ry), (rx - 10, ry + 30)], 4, (0.5, 0.6, 0.8))
    if int(t * 3) % 4 == 0:
        poly(c, [(W / 2, 200), (W / 2 - 40, 330), (W / 2 + 10, 330), (W / 2 - 30, 460), (W / 2 + 60, 290), (W / 2 + 10, 290)], fill=GOLD)
    capbox(c, p.get("cap"), t, y=120)

def sc_question(c, p, t, d):
    floor(c)
    stickman(c, W / 2, GROUND, la=(150, 30), ra=(-150, -30), mouth="o")
    for j in range(5):
        a = j * 1.25 + t * 0.6
        sc = pop(ph(t, j * 0.15, 0.3))
        c.save(); c.translate(W / 2 + math.cos(a) * 330, 380 + math.sin(a) * 170); c.scale(sc, sc)
        text(c, "?", 0, 0, 120, GOLD if j % 2 else RED); c.restore()
    if p.get("q"):
        text(c, p["q"], W / 2, 150, fit(c, p["q"], 80, 1600), INK, alpha=ease(ph(t, 0.3, 0.4)))

def sc_doha(c, p, t, d):
    floor(c)
    shopfront(c, 760, FL, 560, 480, "BHS", sign=RED)
    for side in (-1, 1):
        px = 560 if side < 0 else 1500
        line(c, [(px, FL), (px + 20, FL - 380)], 18, (0.55, 0.4, 0.25))
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * 0.55
            line(c, [(px + 20, FL - 380), (px + 20 + math.cos(a) * 140, FL - 380 + math.sin(a) * 90 + 60)], 14, (0.3, 0.6, 0.3))
    circle(c, 1650, 170, 70, fill=GOLD, stroke=None)
    plane(c, lerp(-300, W + 300, ph(t, 0, d)), 200, 0.7, INK, -0.05)
    capbox(c, p.get("cap"), t)

def sc_rule(c, p, t, d):
    sc = pop(ph(t, 0, 0.5))
    c.save(); c.translate(W / 2, 440); c.scale(sc, sc)
    rrect(c, -800, -230, 1600, 460, 30, fill=DARK, stroke=GOLD, lw=8)
    text(c, p.get("top", "THE ONE RULE"), 0, -140, 56, GOLD)
    l1 = p["a"]; text(c, l1, 0, -20, fit(c, l1, 96, 1500), INK)
    l2 = p.get("b", ""); text(c, l2, 0, 110, fit(c, l2, 110, 1500), RED, alpha=ease(ph(t, 0.8, 0.4)))
    c.restore()

def scene_multi(c, p, t, d):
    shots = p["shots"]
    starts = []
    s0, e0 = LINES[CUR[0]]
    for j, (sc_, pp, trig) in enumerate(shots):
        if j == 0 or not trig: starts.append(0.0 if j == 0 else None); continue
        hit = None
        for w in WORDS:
            if s0 - 0.1 <= w[1] <= e0 + 0.1 and trig.lower() in w[0].lower():
                hit = w[1] - s0 - 0.06; break
        starts.append(hit)
    # fill missing starts evenly
    for j in range(len(starts)):
        if starts[j] is None: starts[j] = d * j / len(starts)
    for j in range(1, len(starts)): starts[j] = max(starts[j], starts[j - 1] + 0.5)
    j = 0
    for k in range(len(starts)):
        if t >= starts[k]: j = k
    st = starts[j]; en = starts[j + 1] if j + 1 < len(starts) else d
    sc_, pp, _ = shots[j]
    SCN[sc_](c, pp, t - st, max(0.4, en - st))

CUR = [0]
SCN.update(street=sc_street, bigshop=sc_bigshop, count=sc_count, flow=sc_flow, jar=sc_jar, chart=sc_chart, paper=sc_paper,
           committee=sc_committee, deal=sc_deal, think=sc_think, tycoon=sc_tycoon, scale=sc_scale, crowd=sc_crowd,
           storm=sc_storm, question=sc_question, doha=sc_doha, rule=sc_rule, multi=scene_multi)
