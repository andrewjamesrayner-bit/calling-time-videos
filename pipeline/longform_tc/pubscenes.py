# Landlord host scenes + reaction bubbles for the long-form (exec'd inside lf.py)
import rigmod as R
R.LINES = LINES; R.WORDS = WORDS
PW, PH = W, H
def _badge(c, x, y, s, k, fill=R.GOLD, col=R.INK, rot=-0.06, size=64):
    sc = R.pop(k)
    if sc < 0.02: return
    if len(s) > 18: size = int(size * 0.8)
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rotate(rot)
    wd = R.tw(c, s, size) + 60
    x = min(x, W - wd / 2 * sc - 40); x = max(x, wd / 2 * sc + 40)
    c.restore(); c.save(); c.translate(x, y); c.scale(sc, sc); c.rotate(rot)
    R.rrect(c, -wd / 2, -size * 0.72, wd, size * 1.45, 14, fill=fill, stroke=R.INK, lw=7); R.text(c, s, 0, 4, size, col); c.restore()
def _wl(word):   # absolute time of a word in the current line
    return R.wt(CUR[0], word)
PSHAKE = [0.0]
def scene_pub(c, p, t, d):
    tm = LINES[CUR[0]][0] + t if t >= 0 else 0
    tm = max(tm, 0)
    li = CUR[0]; s0 = LINES[li][0]
    tm = s0 + t
    R.extras_t[0] = tm
    act = p.get("act")
    R.pub_bg(c, top=0, bot=800)
    tk = R.talkf(tm, li)
    blink = R.blinkf(tm)
    X, Y, S = W / 2 - 80, 805, 1.9
    mouth_talk = ("talk" if tk is not None else None)
    if act == "spit":
        tt = _wl(p.get("trig", "Total")) - s0; sp = t - tt
        tilt = -0.9 if sp < 0 else R.lerp(-0.9, 0.0, R.ease(sp / 0.15))
        hd = R.man(c, X, Y, S, R.P(ra=(-160 if sp < 0 else -120, -40), la=(30, 20)), outfit="landlord",
                   eyes="half" if sp < 0 else "wide", brow="neutral" if sp < 0 else "raised", mouth="flat" if sp < 0 else "o", blink=blink if sp < 0 else 0)
        hx, hy = hd["rh"]; R.pint(c, hx, hy + 40, 1.1, 0.7, tilt)
        R.bar_front(c, top=800, bot=1100)
        if sp > 0:
            R.droplets(c, hd["head"][0] + 40, hd["head"][1] + 30, sp, n=40, d=1)
            R.droplets(c, hd["head"][0] - 40, hd["head"][1] + 30, sp, n=24, d=-1, seed=8)
            if sp > 0.18:
                import random as _r
                rr = _r.Random(5)
                for j in range(12):
                    bx_ = 100 + rr.random() * (W - 200); by_ = 120 + rr.random() * 650 + (sp - 0.18) * 90 * (0.5 + rr.random())
                    rad = 30 + rr.random() * 50; a_ = 0.55 * R.clamp((sp - 0.18) / 0.06)
                    R.circle(c, bx_, by_, rad, fill=(0.85, 0.65, 0.2), stroke=None, a=a_)
                    R.circle(c, bx_ - rad * 0.3, by_ - rad * 0.3, rad * 0.25, fill=R.WHITE, stroke=None, a=a_)
            _badge(c, W - 360, 300, p.get("badge", "TOTAL."), R.ph(sp, 0, 0.25), fill=R.RED, col=R.WHITE, size=90)
        else:
            _badge(c, W - 360, 300, "NOT PER SHOP", R.ph(t, 0.05, 0.25), size=60)
    elif act == "intro":
        cir = t * 9
        tb = _wl(p.get("trig", "belter")) - s0
        if t < tb:
            pose = R.P(la=(70, 60), ra=(-55 + math.sin(cir) * 12, -80 + math.cos(cir) * 12), lean=4)
        else:
            pose = R.P(la=(30, 20), ra=(120, 28), lean=0)
        hd = R.man(c, X, Y, S, pose, outfit="landlord", mouth=mouth_talk or "grin", talk=tk or 0, brow="raised" if t > tb else "neutral", blink=blink)
        if t < tb:
            lx, ly = hd["lh"]; R.pint(c, lx, ly + 60, 0.9, 0.0)
            rx, ry = hd["rh"]; R.rrect(c, rx - 40, ry - 30, 80, 60, 12, fill=R.WHITE, stroke=R.INK, lw=6)
        R.bar_front(c, top=800, bot=1100)
        R.pint(c, W / 2 + 330, 800, 0.9, 0.85)
        _badge(c, W - 380, 300, p.get("badge", "THIS ONE'S A BELTER"), R.ph(t, tb, 0.25), size=56)
    elif act == "quip":
        mood = p.get("mood", "sly")
        look = (0, 1) if p.get("look") == "down" else (0, 0)
        ex = dict(flat=("half", "neutral", "flat"), sly=("half", "sly", "smirk"), raised=("wide", "raised", "o"))[mood]
        lean = R.lerp(0, 8, R.ease(t / 0.5))
        pose = R.P(la=(155, 125), ra=(-155, -125), lean=lean) if mood != "raised" else R.P(la=(60, 60), ra=(-60, -60), lean=lean)
        if p.get("look") == "down": pose = R.P(la=(30, 20), ra=(150, 15), lean=6)
        hd = R.man(c, X, Y, S, pose, outfit="landlord", eyes=ex[0], look=look, brow=ex[1], mouth=mouth_talk or ex[2], talk=tk or 0, blink=blink if ex[0] == "open" else 0)
        R.bar_front(c, top=800, bot=1100)
        R.pint(c, W / 2 + 330, 800, 0.9, 0.5)
        _badge(c, W - 380, 300, p.get("badge", ""), R.ph(t, d * 0.45, 0.25), size=54, rot=0.05)
    elif act == "point":
        tw_ = _wl(p.get("trig", "why")) - s0
        cir = t * 9
        pose = R.P(la=(70, 60), ra=(-55 + math.sin(cir) * 12, -80 + math.cos(cir) * 12), lean=4) if t < tw_ else R.P(la=(30, 20), ra=(-95, -5), lean=10)
        hd = R.man(c, X, Y, S, pose, outfit="landlord", mouth=mouth_talk or "smirk", talk=tk or 0, brow="one", eyes="half" if t < tw_ else "open", blink=blink)
        if t < tw_:
            lx, ly = hd["lh"]; R.pint(c, lx, ly + 60, 0.9, 0.0)
            rx, ry = hd["rh"]; R.rrect(c, rx - 40, ry - 30, 80, 60, 12, fill=R.WHITE, stroke=R.INK, lw=6)
        R.bar_front(c, top=800, bot=1100)
        R.pint(c, W / 2 + 330, 800, 0.9, 0.5)
        _badge(c, W - 380, 330, p.get("badge", "ASK WHY."), R.ph(t, tw_, 0.25), fill=R.RED, col=R.WHITE, size=100)
    elif act == "bell":
        sw = math.sin(t * 20) * R.clamp(1.6 - t * 0.45)
        hd = R.man(c, X, Y, S, R.P(ra=(122 + sw * 14, 26 + sw * 8), la=(35, 35)), outfit="landlord", mouth=mouth_talk or "grin", talk=tk or 0, brow="raised", blink=blink)
        rx, ry = hd["rh"]
        R.handbell(c, rx, ry, 1.1, -0.75 + sw * 0.45)
        for j in range(3):
            k = ((t * 2.5 + j / 3) % 1)
            c.save(); R.setc(c, R.GOLD, 1 - k); c.set_line_width(8); c.arc(rx + 130, ry + 80, 110 + k * 150, -1.2, 0.8); c.stroke(); c.restore()
        R.bar_front(c, top=800, bot=1100)
        R.pint(c, W / 2 + 330, 800, 0.9, 0.9)
        _badge(c, 330, 330, "TIME!", R.ph(t, 0.1, 0.25), size=110, rot=-0.12)
    elif act == "cheeky":
        t_sub = _wl("subscribe") - s0; t_like = _wl("like") - s0; t_bar = _wl("barred") - s0
        if t < t_sub - 0.15: pose = R.P(ra=(-95, -5), la=(30, 20), lean=8); e_, b_, m_ = "open", "raised", None
        elif t < t_bar - 0.1: pose = R.P(ra=(150, 15), la=(30, 20), lean=6); e_, b_, m_ = "open", "one", None
        elif t < t_bar + 0.9: pose = R.P(la=(155, 125), ra=(-155, -125)); e_, b_, m_ = "half", "angry", None
        else: pose = R.P(la=(155, 125), ra=(-155, -125)); e_, b_, m_ = "wink", "sly", "grin"
        hd = R.man(c, X, Y, S, pose, outfit="landlord", eyes=e_, brow=b_, mouth=(mouth_talk or "smirk") if m_ is None else m_, talk=tk or 0, blink=blink if e_ == "open" else 0)
        R.bar_front(c, top=800, bot=1100)
        R.pint(c, W / 2 + 330, 800, 0.9, 0.9)
        if t < t_sub - 0.15: _badge(c, 330, 330, "OI!", R.ph(t, 0.0, 0.2), size=120, rot=-0.1)
        if t > t_bar: R.stamp(c, "BARRED!", W - 420, 560, R.clamp((t - t_bar) / 0.18), size=110, rot=-0.15)
        if t > t_bar + 0.9: R.star(c, hd["head"][0] + 120, hd["head"][1] - 50, 30 * R.pop(R.clamp((t - t_bar - 0.9) / 0.25)), R.GOLD)
        # subscribe + like buttons react to the words
        tm_sub, tm_like = s0 + t_sub, s0 + t_like
        cx, cy = W - 470, 690
        k = R.pop(R.ph(t, 0, 0.3))
        if k > 0.02:
            subbed = tm >= tm_sub; liked = tm >= tm_like
            c.save(); c.translate(cx, cy); c.scale(k, k)
            R.rrect(c, -210, -50, 380, 100, 50, fill=R.GREY if subbed else R.RED, stroke=R.INK, lw=7)
            R.text(c, "SUBSCRIBED" if subbed else "SUBSCRIBE", -20, 2, 44, R.WHITE)
            z = 1 + 0.25 * math.sin(R.clamp((tm - tm_like) / 0.15) * math.pi)
            c.save(); c.translate(260, 0); c.scale(z, z); R.circle(c, 0, 0, 60, fill=R.WHITE, stroke=R.INK, w=7)
            _thumb(c, -4, -6, 0.52, liked); c.restore()
            c.restore()
            for kk, px in ((R.clamp((tm - tm_sub) / 0.4), cx - 20), (R.clamp((tm - tm_like) / 0.4), cx + 260)):
                R.burst(c, px, cy, 70, kk)

def _thumb(c, x, y, s, filled):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = R.RED if filled else R.WHITE
    R.rrect(c, -70, -10, 40, 90, 8, fill=col, stroke=R.INK, lw=8)
    R.poly(c, [(-24, -6), (6, -70), (30, -66), (24, -14), (70, -14), (78, 0), (66, 80), (-24, 80)], fill=col, stroke=R.INK, lw=8)
    c.restore()
SCN["pub"] = scene_pub

# ---------------- reaction bubbles ----------------
def _react_times():
    out = []
    for sub, word, kind, lab in REACT:
        li = [i for i, (_, _, t) in enumerate(SB) if sub in t][0]
        a = R.wt(li, word) - 0.05
        out.append((a, a + 1.4, kind, lab))
    return out
RT = _react_times()
def reaction_overlay(c, tm):
    for a, b, kind, lab in RT:
        if not (a <= tm < b): continue
        t = tm - a; d = b - a
        R.extras_t[0] = tm
        k = R.pop(R.clamp(t / 0.22)) * (1 - R.ease(R.clamp((t - (d - 0.18)) / 0.18)))
        if k < 0.02: return
        x, y, r = W - 190, (650 if kind == "smug" else 330), 120
        c.save(); c.translate(x, y); c.scale(k, k); c.rotate(math.sin(t * 5) * 0.03)
        R.circle(c, 0, 0, r + 10, fill=R.WHITE, stroke=R.INK, w=9)
        c.save(); c.arc(0, 0, r, 0, 2 * math.pi); c.clip()
        R.rrect(c, -r, -r, 2 * r, 2 * r, 0, fill=R.WALL)
        g = cairo.RadialGradient(0, -60, 5, 0, -60, 170); g.add_color_stop_rgba(0, 1, 0.82, 0.45, 0.5); g.add_color_stop_rgba(1, 1, 0.82, 0.45, 0)
        c.set_source(g); c.paint()
        if kind == "facepalm":
            hd = R.man(c, 0, 225, 0.85, R.P(ra=(-25, -150), la=(30, 20), head=-8), outfit="landlord", eyes="closed", brow="worried", mouth="frown")
            hx, hy = hd["head"]; R.circle(c, hx + 6, hy - 6, 28, fill=R.WHITE, stroke=R.INK, w=7)
        elif kind == "wince":
            R.man(c, 0, 225, 0.85, R.P(la=(150, 120), ra=(-150, -120), head=6 * math.sin(t * 30) * (t < 0.4)), outfit="landlord", eyes="closed", brow="worried", mouth="teeth")
        elif kind == "jaw":
            R.man(c, 0, 225, 0.85, R.P(la=(150, 150), ra=(-150, -150)), outfit="landlord", eyes="wide", brow="raised", mouth="scream")
        else:
            R.man(c, 0, 225, 0.85, R.P(la=(155, 125), ra=(-155, -125)), outfit="landlord", eyes="half", brow="sly", mouth="smirk")
        c.restore(); c.restore()
        _badge(c, x - 10, y + 150, lab, R.clamp((t - 0.15) / 0.25) * (1 - R.ease(R.clamp((t - (d - 0.18)) / 0.18))), size=36, rot=0.06)
        return
