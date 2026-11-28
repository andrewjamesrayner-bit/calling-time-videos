for _k in range(1, len(WORDS)):
    if WORDS[_k][0].lower().startswith("barred") and WORDS[_k - 1][0].lower() == "your": WORDS[_k - 1][0] = "you're"
_lastst = LINES[-1][0]
for _k in range(len(WORDS)):
    if WORDS[_k][1] >= _lastst - 0.3 and WORDS[_k][0].strip(",.!").lower() in ("oh", "oi"):
        WORDS[_k][0] = "Oi!"; break
CH = []
def build_chunks():
    cur = []
    for w in WORDS:
        cur.append(w)
        if len(cur) >= 3 or re.search(r'[.,?!]$', w[0]) or (len(cur) >= 2 and w[2] - cur[0][1] > 0.9):
            CH.append(cur); cur = []
    if cur: CH.append(cur)
build_chunks()
def wkey(w): return re.sub(r'[^a-z0-9,£%\-]', '', w.lower()).strip(',')

def captions(c, tm):
    for ch in CH:
        if (ch is CH[0] and tm < ch[-1][2] + 0.12) or ch[0][1] - 0.04 <= tm < ch[-1][2] + 0.12:
            size = 108
            s = " ".join(w[0] for w in ch).upper()
            while tw(c, s, size) + size * 0.32 * len(ch) > W - 160: size -= 4
            total = sum(tw(c, w[0].upper(), size) for w in ch) + size * 0.32 * (len(ch) - 1)
            x = W / 2 - total / 2
            k = 1.0 if (ch is CH[0] and tm < ch[0][1] + 0.16) else pop(clamp((tm - ch[0][1]) / 0.16))
            c.save(); c.translate(W / 2, 1250); c.scale(k, k); c.translate(-W / 2, -1250)
            for w in ch:
                key = wkey(w[0])
                col = RED if key in HL else (GOLD if key in GOLDW or re.match(r'^[£\d]', key) else WHITE)
                said = tm >= w[1] - 0.02
                x += text(c, w[0].upper(), x, 1250, size, col if said else LGREY, align="left", stroke=INK, sw=16) + size * 0.32
            c.restore()
            return

# ---------------- helpers ----------------
def floor(c, y=GROUND): line(c, [(40, y), (W - 40, y)], 10, INK)
def hip(s): return GROUND - 210 * s
def walkpose(t, sp=12, amp=24, **kw):
    w = math.sin(t * sp) * amp
    return P(la=(18 + w * 0.6, 10), ra=(-18 - w * 0.6, -10), ll=(w, 4), rl=(-w, -4), **kw)
def badge(c, x, y, s, k, fill=GOLD, col=INK, rot=-0.06, size=76):
    sc = pop(k)
    if sc < 0.02: return
    c.save(); c.translate(x, y); c.scale(sc, sc); c.rotate(rot)
    wd = tw(c, s, size) + 70
    rrect(c, -wd / 2, -size * 0.72, wd, size * 1.45, 16, fill=fill, stroke=INK, lw=8); text(c, s, 0, 4, size, col); c.restore()
def counter(c, x, y, pre, val, suf, k, size=150, col=RED):
    v = val * ease(k)
    s = pre + (f"{v:,.0f}") + suf
    text(c, s, x, y, size, col, stroke=INK, sw=12)
def store(c, x, base, w=440, h=470, k=0.0, t=0, name="BHS"):
    building(c, x, base, w, h, name, sign=STORE, k=k, t=t)
def coin(c, x, y, r=46, spin=0.0):
    sx = abs(math.cos(spin)) * 0.85 + 0.15
    c.save(); c.translate(x, y); c.scale(sx, 1)
    circle(c, 0, 0, r, fill=GOLD, stroke=INK, w=7)
    if sx > 0.4: text(c, "£1", 0, 2, r * 0.9, INK)
    c.restore()
def note(c, x, y, s=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rrect(c, -48, -26, 96, 52, 8, fill=(0.55, 0.78, 0.55), stroke=INK, lw=5); text(c, "£", 0, 2, 34, INK); c.restore()
def fit(c, s_, size, maxw):
    while size > 12 and tw(c, s_, size) > maxw: size -= 2
    return size
def bottle(c, x, base, s=1.0, label="DASANI", fill=1.0):
    c.save(); c.translate(x, base); c.scale(s, s)
    poly(c, [(-70, 0), (-70, -260), (-40, -320), (-30, -380), (30, -380), (40, -320), (70, -260), (70, 0)], fill=(0.72, 0.86, 0.98), stroke=INK, lw=8)
    if fill < 1: rrect(c, -64, -260 * fill - 2, 128, 260 * fill, 6, fill=(0.55, 0.75, 0.95))
    rrect(c, -36, -420, 72, 44, 8, fill=BLUE, stroke=INK, lw=7)
    if label:
        rrect(c, -70, -200, 140, 90, 0, fill=BLUE, stroke=INK, lw=6); text(c, label, 0, -155, 30, WHITE)
    c.restore()
def cv(c, x, y, k):
    c.save(); c.translate(x, y); c.rotate(-0.04)
    rrect(c, -300, -330, 600, 660, 18, fill=WHITE, stroke=INK, lw=9)
    text(c, "CURRICULUM VITAE", 0, -270, 46, INK)
    for j, lab in enumerate(["NAME:", "RETAIL EXPERIENCE:", "SHOPS RUN:", "HOBBIES:"]):
        text(c, lab, -260, -170 + j * 120, 38, INK, align="left")
        line(c, [(-260, -130 + j * 120), (260, -130 + j * 120)], 4, GREY)
    text(c, "D. Chappell", 40, -170, 38, BLUE, align="left")
    text(c, "0", 150, 70, 40, BLUE, align="left")
    text(c, "Going fast", -40, 190, 38, BLUE, align="left")
    c.restore()
def car(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-260, 0), (-250, -60), (-60, -80), (0, -130), (120, -130), (170, -70), (270, -50), (280, 0)], fill=RED, stroke=INK, lw=9)
    rrect(c, 10, -120, 100, 45, 10, fill=(0.78, 0.88, 0.96), stroke=INK, lw=6)
    text(c, "1", -120, -40, 60, WHITE)
    for wx in (-160, 170):
        circle(c, wx, 0, 52, fill=INK, stroke=INK, w=6); circle(c, wx, 0, 20, fill=GREY, stroke=None)
    c.restore()
def calendar(c, x, y, label, k):
    c.save(); c.translate(x, y)
    rrect(c, -170, -150, 340, 300, 20, fill=WHITE, stroke=INK, lw=9)
    rrect(c, -170, -150, 340, 80, 20, fill=RED, stroke=INK, lw=9)
    text(c, label, 0, 30, 76, INK)
    c.restore()
def jar(c, x, base, fill, label="PENSION", col=GREEN, hole=False, t=0):
    rrect(c, x - 150, base - 380, 300, 380, 40, fill=(0.88, 0.94, 0.98), stroke=INK, lw=10)
    rrect(c, x - 110, base - 420, 220, 50, 12, fill=GREY, stroke=INK, lw=8)
    fh = 340 * clamp(fill)
    if fh > 4: rrect(c, x - 130, base - 20 - fh, 260, fh, 26, fill=col)
    rrect(c, x - 125, base - 260, 250, 70, 10, fill=WHITE, stroke=INK, lw=6); text(c, label, x, base - 225, 46, INK)
    if hole:
        circle(c, x + 110, base - 40, 16, fill=INK, stroke=None)
def bars(c, k):
    yb = lerp(-900, 0, ease(k))
    c.save(); c.translate(0, yb)
    rrect(c, 120, 420, W - 240, 30, 8, fill=GREY, stroke=INK, lw=8)
    for j in range(8):
        xx = 170 + j * (W - 340) / 7
        line(c, [(xx, 430), (xx, GROUND)], 22, INK); line(c, [(xx, 430), (xx, GROUND)], 10, GREY)
    c.restore()

def build_shots():
    starts = []
    for name, li, wd in SPEC:
        st = LINES[li][0] if wd is None else wt(li, wd) - 0.04
        starts.append(max(0, st))
    starts[0] = 0.0
    out = []
    for j, (name, li, wd) in enumerate(SPEC):
        e = starts[j + 1] if j + 1 < len(SPEC) else END + 1
        out.append((name, starts[j], e, li))
    return out
SHOTS = build_shots()
def sstart(name): return [x for x in SHOTS if x[0] == name][0][1]
def W_(li, word, nth=0): return wt(li, word, nth)   # absolute time of a word

SHAKE = [0.0]
def hitshake(tabs, at, amt=18, dur=0.25):
    k = (tabs - at) / dur
    if 0 <= k < 1: SHAKE[0] = max(SHAKE[0], amt * (1 - k))

