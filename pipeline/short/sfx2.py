# Real CC0 sound design: wyzowl/sfx-kit (CC0) + "Quirky Jazz" (opengameart, CC0) music bed.
import numpy as np, soundfile as sf, sys, json, subprocess
from scipy.signal import resample_poly
from scipy.ndimage import maximum_filter1d, uniform_filter1d
sys.argv = ['x']
import sh
SR = 48000
KIT = '/home/claude/assets/sfx-kit/'
META = {s['id']: s for s in json.load(open(KIT + 'sounds.json'))['sounds']}
v, _ = sf.read('vo/voice.wav')
if v.ndim > 1: v = v.mean(1)
N = int((sh.END + 0.6) * SR)
out = np.zeros(N); out[:len(v)] += v
rng = np.random.default_rng(1)
_cache = {}
def S_(sid):
    if sid not in _cache:
        a, sr = sf.read(KIT + META[sid]['file'])
        if a.ndim > 1: a = a.mean(1)
        if sr != SR: a = resample_poly(a, SR, sr)
        _cache[sid] = (a, META[sid]['sync']['at'])
    return _cache[sid]
def add(sid, t, g=1.0):
    """place sound so its sync point lands at time t"""
    a, sy = S_(sid) if isinstance(sid, str) else (sid, 0.0)
    i = int((t - sy) * SR)
    if i < 0: a = a[-i:]; i = 0
    if i >= N: return
    j = min(N, i + len(a)); out[i:j] += a[:j - i] * g
def tone(f, d):
    n = int(d * SR); return np.sin(2 * np.pi * np.cumsum(np.full(n, f) if np.ndim(f) == 0 else f) / SR)
def cricket(d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR
    gate = (np.sin(2 * np.pi * 14 * tt) > 0.3) * ((tt % 0.42) < 0.26)
    return tone(4300, d) * gate * 0.25
def scratch():
    n = int(0.42 * SR); tt = np.arange(n) / SR
    f = 260 + 1100 * np.abs(np.sin(tt * 24))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (2 * (ph / (2 * np.pi) % 1) - 1) * 0.35 + rng.standard_normal(n) * 0.15
    from scipy.signal import lfilter
    return lfilter([0.3], [1, -0.7], x) * np.exp(-tt * 3)
def vroom(d=1.3):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 70 + 150 * (tt / d) ** 0.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (2 * (ph / (2 * np.pi) % 1) - 1) + 0.5 * np.sin(2 * ph)
    from scipy.signal import lfilter
    return lfilter([0.08], [1, -0.92], x) * np.sin(np.pi * tt / d) * 1.4

def OGA(f, dur=None):
    a, sr = sf.read('/home/claude/assets/oga/' + f)
    if a.ndim > 1: a = a.mean(1)
    if sr != SR: a = resample_poly(a, SR, sr)
    if dur:
        a = a[int(2.0 * SR): int((2.0 + dur) * SR)].copy(); n = len(a); fd = int(0.15 * SR)
        a[:fd] *= np.linspace(0, 1, fd); a[-fd:] *= np.linspace(1, 0, fd)
    return a / (np.abs(a).max() + 1e-9) * 0.8
S = sh.sstart; W_ = sh.W_
# ---- cues ----
add('shimmer-medium-soft', 0.05, 0.4); add('appear-burst', 0.25, 0.4)
add('pop-large-in', S('reveal') + 0.05, 0.5)
add('money-register', S('money') + 0.2, 0.45); add('money-notes', S('money') + 0.5, 0.35)
add('props-drip', S('tap') + 0.1, 0.5); add('notification-failure-wobble', W_(3, "tap") + 0.05, 0.4)
add('reverse-whoosh-short-strong', S('spit') + 0.02, 0.45)
add('props-splash', max(S('spit') + 0.15, W_(4, "Sidcup")), 0.7); add('move-spring', W_(4, "Sidcup") + 0.08, 0.45)
add('whoosh-medium-soft', S('sidcup') - 0.05, 0.3); add('props-drip', S('sidcup') + 0.6, 0.3)
add('foley-wood-touch', W_(6, "Dasani") + 0.3, 0.5); add('impact-medium-hard', W_(6, "Dasani") + 0.5, 0.5)
add('data-countup-medium', S('times') + 0.05, 0.35); add('impact-heavy-firm', S('times') + 0.75, 0.5)
add('foley-paper-slide', S('papers') + 0.15, 0.5); add('foley-paper-slide', S('papers') + 1.05, 0.5)
add('cinematic-thunder-big', S('worse') + 0.1, 0.45)
add('data-chart-reveal', S('lab') + 0.2, 0.35); add('notification-attention-soft', S('lab') + 1.1, 0.4)
add('impact-light-firm', W_(11, "created") + 0.05, 0.55)
add('cinematic-slam-big', S('recall') + 0.6, 0.35); add('data-countup-short', S('recall') + 0.1, 0.3)
add('time-clock-fast', S('gone') + 0.0, 0.35); add('impact-heavy-hard', W_(13, "cancelled") + 0.1, 0.6)
add('whoosh-slow-soft', S('moral') + 0.05, 0.3); add('foley-glass-touch', S('moral') + 0.6, 0.4)
add('impact-light-firm', W_(14, "tap") + 0.03, 0.6)
for k in range(5): add('props-shop-bell', S('bell') + 0.05 + k * 0.26, 0.55)
add('tone-ding-high', S('bell') + 0.05, 0.45)
ts = W_(16, "subscribe"); tl = W_(16, "like"); tb = W_(16, "barred")
add('pop-medium-in', S('cheeky') + 0.05, 0.5)
add('click-mouse-firm', ts, 0.7); add('notification-success-pluck', ts + 0.05, 0.4)
add('click-mouse-firm', tl, 0.7); add('pop-large-in', tl + 0.05, 0.45)
add('impact-heavy-hard', tb + 0.12, 0.7)
add('shimmer-short-sparkle', tb + 0.9, 0.45)
for a_, b_, kind, *_ in sh.REACT:
    add('pop-medium-in', a_, 0.45); add('pop-small-out', b_ - 0.15, 0.35)
    add({'facepalm': 'impact-light-soft', 'wince': 'notification-failure-low', 'smug': 'notification-success-pluck'}[kind], a_ + 0.2, 0.4)

# ---- music bed ----
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/home/claude/assets/music/quirky_jazz.mp3', '-ac', '1', '-ar', str(SR), '/tmp/mus.wav'], check=True)
m, _ = sf.read('/tmp/mus.wav')
OFF = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
m = m[int(OFF * SR):]
while len(m) < N: m = np.concatenate([m, m])
m = m[:N]
m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * 0.05          # normalise RMS
e = np.abs(np.concatenate([v, np.zeros(max(0, N - len(v)))]))[:N]
e = uniform_filter1d(maximum_filter1d(e, int(0.1 * SR)), int(0.15 * SR))
duck = 1 - 0.6 * np.clip(e / 0.12, 0, 1)
fade = np.ones(N); fi = int(0.4 * SR); fade[:fi] = np.linspace(0.3, 1, fi)
fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo)
out += m * duck * fade
sf.write('vo/mix.wav', out / np.max(np.abs(out)) * 0.89, SR)
print('ok')
