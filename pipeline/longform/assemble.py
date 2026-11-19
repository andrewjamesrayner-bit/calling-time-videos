import subprocess, json, whisper, soundfile as sf, numpy as np
from sb import SB
SR=24000
def run(*a): subprocess.run(a,check=True)
segs=[];lines=[];t=0.0
for i,(sc,p,_) in enumerate(SB,1):
    run('ffmpeg','-loglevel','error','-y','-i',f'vo/L{i:03d}.wav','-af',
        'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,atempo=1.05',
        '-ar',str(SR),'-ac','1',f'vo/T{i:03d}.wav')
    a,_=sf.read(f'vo/T{i:03d}.wav'); d=len(a)/SR
    gap=0.75 if sc in('num','rating','date') or (i<len(SB) and SB[i][0]=='num') else (0.45 if sc=='pub' or (i<len(SB) and SB[i][0]=='pub') else 0.28)
    segs.append(a); segs.append(np.zeros(int(gap*SR)))
    lines.append([t,t+d]); t+=d+gap
full=np.concatenate([np.zeros(int(0.15*SR))]+segs); lines=[[s+0.15,e+0.15] for s,e in lines]
sf.write('vo/raw.wav',full,SR)
run('ffmpeg','-loglevel','error','-y','-i','vo/raw.wav','-af','highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=9','-ar','48000','vo/voiceover.wav')
m=whisper.load_model('small.en')
r=m.transcribe('vo/voiceover.wav',language='en',word_timestamps=True)
words=[[w['word'].strip(),w['start'],w['end']] for s in r['segments'] for w in s['words']]
json.dump(dict(lines=lines,words=words,end=t+0.15+0.6),open('vo/timing.json','w'))
print('dur',t, 'words',len(words))
