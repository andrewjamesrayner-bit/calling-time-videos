import json, numpy as np, torchaudio as ta, torchaudio.functional as F, shutil
from sb import SB
res = json.load(open('vo5/scores.json'))
def pv(p):
    w, sr = ta.load(p); w = w.mean(0)
    f0 = F.detect_pitch_frequency(w.unsqueeze(0), sr, freq_low=70, freq_high=350)[0].numpy()
    f0 = f0[(f0 > 70) & (f0 < 350)]
    return float(np.std(np.log(f0))) if len(f0) > 10 else 0.0
for i in range(1, len(SB) + 1):
    c = [v for k, v in res.items() if k.split('_')[0] == str(i)]
    good = [v for v in c if v['score'] >= 0.92] or sorted(c, key=lambda v: -v['score'])[:1]
    best = max(good, key=lambda v: pv(v['p']) + 0.5 * v['score']) if len(good) > 1 else good[0]
    shutil.copy(best['p'], f'vo/L{i:03d}.wav')
    if best['score'] < 0.92: print('LOW', i, round(best['score'], 3), best['text'])
print('picked')
