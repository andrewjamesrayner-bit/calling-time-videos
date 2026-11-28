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
        lab = LABELS.get(kind, "OOF")
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
    t0 = LINES[CL][0]; ts = W_(CL, "subscribe"); tl = W_(CL, "like")
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
PUNCHT = [W_(li_, w_) for li_, w_ in PUNCHW]
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
