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
        tw2 = W_(6, "ninety-five") - s0 if any(w[0].lower().startswith("95") or "ninety" in w[0].lower() for w in WORDS) else d * 0.5
        k = ease(clamp((t - max(0.2, tw2 - 0.3)) / 0.6))
        ang = -0.38 * k
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
        text(c, "UK LEGAL LIMIT: 10", 720, ybar(lim) - 30, 34, RED)
        k = ease(ph(t, 0.2, 1.0))
        v = 22 * k
        rrect(c, 420, ybar(v), 240, 1050 - ybar(v), 12, fill=RED if v > lim else GOLD, stroke=INK, lw=7)
        text(c, f"{v:.0f} ppb", 540, ybar(v) - 40, 60, RED if v > lim else INK)
        text(c, "Tested 10–22 ppb (BBC)", W / 2, 1450, 34, INK, alpha=0.6)
    elif name == "irony":
        floor(c)
        for j, (lab, val, col_) in enumerate((("SIDCUP TAP", "0", GREEN), ("DASANI", "OVER LIMIT", RED))):
            x_ = 300 + j * 480
            if j == 0:
                rrect(c, x_ - 70, GROUND - 260, 140, 260, 14, fill=(0.75, 0.88, 1.0), stroke=INK, lw=8)
            else:
                bottle(c, x_, GROUND, 0.9, "DASANI")
            text(c, lab, x_, 520, 52, INK)
            badge(c, x_, 640, "BROMATE: " + val, ph(t, 0.3 + j * 0.7, 0.25), fill=col_, col=WHITE, size=44)
        tp = W_(11, "created") - s0 if any("created" in w[0] for w in WORDS) else d * 0.7
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
        counter(c, W / 2, 470, "", 500000, " BOTTLES", ph(t, 0.1, 0.8), size=100)
    elif name == "gone":
        floor(c)
        calendar(c, 330, 700, "5 WEEKS", 1)
        rrect(c, 600, 520, 400, 360, 20, fill=(0.75, 0.86, 0.95), stroke=INK, lw=8)
        text(c, "EUROPE", 800, 600, 50, INK)
        for j in range(6):
            circle(c, 680 + (j % 3) * 120, 700 + (j // 3) * 100, 30, fill=GREEN, stroke=INK, w=5)
        tc = W_(13, "cancelled") - s0 if any("cancelled" in w[0] for w in WORDS) else d * 0.7
        if t > tc: stamp(c, "CANCELLED", 800, 720, clamp((t - tc) / 0.18), size=72, rot=-0.18); hitshake(tm, s0 + tc + 0.1, 16)
