
def generic_shot(c, name, t, d, li, s0, tm, blink):
    if name == "spit":
        tt = max(0.15, W_(SPIT_LI, SPIT_WORD) - s0)
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
            hitshake(tm, s0 + tt, 22)
            if sp > 0.18:
                import random as _r
                rr = _r.Random(5)
                for j in range(9):
                    bx_ = 120 + rr.random() * 840; by_ = 420 + rr.random() * 700 + (sp - 0.18) * 90 * (0.5 + rr.random())
                    rad = 30 + rr.random() * 45
                    circle(c, bx_, by_, rad, fill=(0.85, 0.65, 0.2), stroke=None, a=0.55 * clamp((sp - 0.18) / 0.06))
            badge(c, W / 2, 1520, SPIT_BADGE, ph(sp, 0, 0.25), fill=RED, col=WHITE, size=fit(c, SPIT_BADGE, 96, 900))
        return True
    if name == "moral":
        tk = talkf(tm, li)
        lean = lerp(0, 8, ease(t / 0.6))
        tw_ = W_(MORAL_LI, MORAL_WORD) - s0
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
        badge(c, W / 2, 1530, MORAL_BADGE, ph(t, tw_, 0.25), fill=RED, col=WHITE, size=fit(c, MORAL_BADGE, 74, 880))
        return True
    if name == "bell":
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
        return True
    if name == "cheeky":
        pub_bg(c)
        tk = talkf(tm, li)
        t_sub = W_(CL, "subscribe") - s0; t_bar = W_(CL, "barred") - s0
        if t < t_sub - 0.15:
            pose = P(ra=(-95, -5), la=(30, 20), lean=8); eyes, brow, mouth = "open", "raised", None
        elif t < t_bar - 0.1:
            pose = P(ra=(150, 15), la=(30, 20), lean=6); eyes, brow, mouth = "open", "one", None
        elif t < t_bar + 0.9:
            pose = P(la=(155, 125), ra=(-155, -125), lean=0); eyes, brow, mouth = "half", "angry", None
        else:
            pose = P(la=(155, 125), ra=(-155, -125), lean=0); eyes, brow, mouth = "wink", "sly", "grin"
        hd = man(c, 540, 975, 1.35, pose, outfit="landlord", eyes=eyes, brow=brow,
                 mouth=("talk" if tk is not None else "smirk") if mouth is None else mouth, talk=tk or 0, blink=blink if eyes in ("open",) else 0)
        bar_front(c)
        pint(c, 880, 1000, 0.8, 0.9)
        if t < t_sub - 0.15: badge(c, 230, 600, "OI!", ph(t, 0.0, 0.2), fill=GOLD, size=110, rot=-0.1)
        if t > t_bar: stamp(c, "BARRED!", 790, 830, clamp((t - t_bar) / 0.18), size=80, rot=-0.15); hitshake(tm, s0 + t_bar + 0.1, 18)
        if t > t_bar + 0.9: star(c, hd["head"][0] + 95, hd["head"][1] - 40, 26 * pop(clamp((t - t_bar - 0.9) / 0.25)), GOLD)
        return True
    return False

def draw_shot(c, name, t, d, li, s0):
    tm = TM[0]; blink = blinkf(tm)
    if generic_shot(c, name, t, d, li, s0, tm, blink): return
    story(c, name, t, d, li, s0, tm)
