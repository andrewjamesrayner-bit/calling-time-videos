import json, numpy as np, torch, torchaudio as ta, torchaudio.functional as F, subprocess
res = json.load(open('vo2/scores.json'))
lines = [l.strip() for l in open('script.txt') if l.strip()]
def feats(p):
    w, sr = ta.load(p); w = w.mean(0)
    f0 = F.detect_pitch_frequency(w.unsqueeze(0), sr, freq_low=70, freq_high=350)[0].numpy()
    # energy per 20ms frame
    hop = int(sr * 0.02); fr = w[: len(w) // hop * hop].reshape(-1, hop).numpy()
    rms = np.sqrt((fr ** 2).mean(1)); voiced = rms > rms.max() * 0.12
    f0v = f0[: len(voiced)][voiced[: len(f0)]] if len(f0) else f0
    f0v = f0v[(f0v > 70) & (f0v < 350)]
    pv = np.std(np.log(f0v)) if len(f0v) > 10 else 0
    ed = np.std(20 * np.log10(rms[voiced] + 1e-6)) if voiced.sum() > 5 else 0
    return pv, ed, len(w) / sr
pick = {}
for i, t in enumerate(lines, 1):
    cands = [(k, v) for k, v in res.items() if k.split('_')[0] == str(i)]
    rows = []
    for k, v in cands:
        pv, ed, du = feats(v['p'])
        rows.append((k, v['score'], pv, ed, du, v['p'], v['text']))
    good = [r for r in rows if r[1] >= 0.92] or sorted(rows, key=lambda r: -r[1])[:1]
    dmin = min(r[4] for r in good)
    best = max(good, key=lambda r: r[2] * 4 + r[3] * 0.05 - 0.6 * (r[4] / dmin - 1) + 0.5 * r[1])
    pick[i] = best[5]
    print(i, ' | '.join(f"{r[0]} s={r[1]:.2f} pv={r[2]:.3f} ed={r[3]:.1f} d={r[4]:.1f}" for r in rows), '=>', best[0])
    subprocess.run(['cp', best[5], f'vo/L{i:02d}.wav'])
json.dump(pick, open('vo2/pick.json', 'w'), indent=1)
