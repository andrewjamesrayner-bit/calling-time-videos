# Long-form sound design: CC0 wyzowl/sfx-kit + OGA CC0 crickets/engine + "Quirky Jazz" (CC0) bed.
import numpy as np, soundfile as sf, sys, json, subprocess, re
from scipy.signal import resample_poly
from scipy.ndimage import maximum_filter1d, uniform_filter1d
sys.argv = ['x']
import lf
import rigmod as R
SR = 48000
KIT = '/home/claude/assets/sfx-kit/'
META = {s['id']: s for s in json.load(open(KIT + 'sounds.json'))['sounds']}
v, sr0 = sf.read('vo/voiceover.wav')
if v.ndim > 1: v = v.mean(1)
if sr0 != SR: v = resample_poly(v, SR, sr0)
N = int((lf.END + 1.0) * SR)
out = np.zeros(N); out[:len(v)] += v[:N]
_cache = {}
def S_(sid):
    if sid not in _cache:
        a, sr = sf.read(KIT + META[sid]['file'])
        if a.ndim > 1: a = a.mean(1)
        if sr != SR: a = resample_poly(a, SR, sr)
        _cache[sid] = (a, META[sid]['sync']['at'])
    return _cache[sid]
def add(sid, t, g=1.0):
    a, sy = S_(sid) if isinstance(sid, str) else (sid, 0.0)
    i = int((t - sy) * SR)
    if i < 0: a = a[-i:]; i = 0
    if i >= N: return
    j = min(N, i + len(a)); out[i:j] += a[:j - i] * g

SB, LINES = lf.SB, lf.LINES
wt = R.wt
WH = ['whoosh-medium-soft', 'swish-soft', 'whoosh-fast-soft', 'swipe-medium-soft']
for i, (sc, p, txt) in enumerate(SB):
    s0 = LINES[i][0]
    shots = p.get("shots") if sc == "multi" else [(sc, p, None)]
    for j, (ss, pp, trig) in enumerate(shots):
        ts = s0 if trig is None else wt(i, trig)
        if j > 0 and trig is None: continue
        add(WH[(i + j) % 4], ts - 0.05, 0.22)
        if ss == "count": add('data-countup-short', ts + 0.1, 0.22); add('pop-medium-in', ts + 0.05, 0.25)
        elif ss == "deal": add('money-coin-drop', ts + 0.6, 0.35)
        elif ss == "flow": add('money-coins-pour', ts + 0.2, 0.25)
        elif ss == "committee": add('impact-medium-firm', ts + 0.35, 0.35)
        elif ss == "paper": add('foley-paper-slide', ts + 0.05, 0.4)
        elif ss == "jar": add('props-drip', ts + 0.3, 0.3) if pp.get("crack") or pp.get("to", 1) < pp.get("from", 0) else add('transform-fill', ts + 0.2, 0.25)
        elif ss == "storm": add('cinematic-thunder-big', ts + 0.2, 0.35)
        elif ss == "think": add('pop-small-bubble', ts + 0.3, 0.35)
        elif ss == "tycoon": add('money-register', ts + 0.3, 0.3)
        elif ss == "question": add('notification-attention-soft', ts + 0.2, 0.3)
        elif ss == "rule": add('impact-heavy-firm', ts + 0.3, 0.4)
        elif ss == "bigshop" and pp.get("rise"): add('transform-grow', ts + 0.05, 0.3)
        elif ss == "street" and pp.get("shut"): add('mechanical-shutter-heavy', ts + 0.3, 0.3)
        elif ss == "chart": add('data-chart-reveal', ts + 0.1, 0.3)
        elif ss == "scale": add('foley-wood-touch', ts + 0.4, 0.4)
        elif ss == "doha": add('shimmer-medium-soft', ts + 0.2, 0.3)
        elif ss == "board":
            fl = pp.get("flip")
            if fl is None: add('appear-flip-quick', ts + 0.1, 0.3)
            else:
                for k in range(len(pp.get("rows", [0] * 5))): add('appear-flip-quick', ts + fl + k * 0.18, 0.25)
                add('notification-failure-low', ts + fl + 0.5, 0.35)
        elif ss == "beach": add('shimmer-medium-soft', ts + 0.2, 0.25)
        elif ss == "merge": add('impact-medium-firm', ts + 1.3, 0.35)
        elif ss == "sack": add('foley-wood-touch', ts + 0.3, 0.35)
        elif ss == "banks": add('pop-small-bubble', ts + 0.1, 0.3)
        elif ss == "shops": add('appear-flip-quick', ts + pp.get("swap_at", 1.0), 0.35); add('pop-medium-in', ts + 0.1, 0.25)
    if sc == "num": add('impact-deep-firm', s0 + 0.05, 0.45); add('riser-1s-soft', s0 - 0.9, 0.25)
    elif sc == "title": add('cinematic-drum-big', s0 + 0.1, 0.5)
    elif sc == "date": add('impact-medium-hard', s0 + 0.15, 0.4)
    elif sc == "rating": add('data-progress-short', s0 + 0.3, 0.35); add('impact-heavy-hard', LINES[i][1] - 0.2, 0.45)
    elif sc == "stick" and p.get("kind") == "jail": add('cinematic-metal-big', s0 + 0.3, 0.45)
    elif sc == "stick" and p.get("kind") == "shutters": add('mechanical-shutter-heavy', s0 + 0.3, 0.45)
    elif sc == "end": add('sting-playful-short', s0 + 0.1, 0.4)
    elif sc == "pub":
        act = p["act"]
        add('foley-glass-touch', s0 + 0.2, 0.35)
        if act == "spit": tt = wt(i, p.get("trig", "Total")); add('props-splash', tt, 0.6); add('move-spring', tt + 0.08, 0.4); add('reverse-whoosh-short-strong', s0 + 0.02, 0.4)
        elif act == "intro": add('sting-warm-short', s0 + 0.05, 0.35); add('pop-medium-in', wt(i, p.get("trig", "belter")), 0.4)
        elif act == "quip": add('pop-medium-in', s0 + (LINES[i][1] - s0) * 0.45, 0.4); add('sting-playful-short', LINES[i][1] - 0.2, 0.3)
        elif act == "point": add('impact-light-firm', wt(i, p.get("trig", "why")) + 0.03, 0.55)
        elif act == "bell":
            for k in range(5): add('props-shop-bell', s0 + 0.05 + k * 0.26, 0.5)
            add('tone-ding-high', s0 + 0.05, 0.4)
        elif act == "cheeky":
            add('pop-medium-in', s0 + 0.05, 0.45)
            add('click-mouse-firm', wt(i, "subscribe"), 0.6); add('notification-success-pluck', wt(i, "subscribe") + 0.05, 0.35)
            add('click-mouse-firm', wt(i, "like"), 0.6); add('pop-large-in', wt(i, "like") + 0.05, 0.4)
            add('impact-heavy-hard', wt(i, "barred") + 0.12, 0.6); add('shimmer-short-sparkle', wt(i, "barred") + 0.9, 0.4)
for a, b, kind, lab in lf.RT:
    add('pop-medium-in', a, 0.4); add('pop-small-out', b - 0.15, 0.3)
    add({'facepalm': 'impact-light-soft', 'wince': 'notification-failure-low', 'smug': 'notification-success-pluck', 'jaw': 'notification-failure-wobble'}[kind], a + 0.2, 0.4)

# ---- music bed: ducked under voice, dipped for the collapse chapter ----
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/home/claude/assets/music/quirky_jazz.mp3', '-ac', '1', '-ar', str(SR), '/tmp/mus.wav'], check=True)
m, _ = sf.read('/tmp/mus.wav')
while len(m) < N: m = np.concatenate([m, m])
m = m[:N]; m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * 0.045
e = np.abs(np.concatenate([v, np.zeros(max(0, N - len(v)))]))[:N]
e = uniform_filter1d(maximum_filter1d(e, int(0.1 * SR)), int(0.15 * SR))
duck = 1 - 0.6 * np.clip(e / 0.12, 0, 1)
lvl = np.ones(N)
c5 = [i for i, (s, p, t) in enumerate(SB) if s == "num" and p.get("n") == 5][0]
c6 = [i for i, (s, p, t) in enumerate(SB) if s == "num" and p.get("n") == 6][0]
a_, b_ = int(LINES[c5][0] * SR), int(LINES[c6][0] * SR)
ramp = int(1.5 * SR)
lvl[a_:b_] = 0.35; lvl[a_:a_ + ramp] = np.linspace(1, 0.35, ramp); lvl[b_ - ramp:b_] = np.linspace(0.35, 1, ramp)
fade = np.ones(N); fi = int(1.0 * SR); fade[:fi] = np.linspace(0, 1, fi); fo = int(2.0 * SR); fade[-fo:] = np.linspace(1, 0, fo)
out += m * duck * lvl * fade
sf.write('vo/mix.wav', out / np.max(np.abs(out)) * 0.89, SR)
print('ok', N / SR)
