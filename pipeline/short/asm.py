import subprocess, json, whisper, soundfile as sf, numpy as np
SR=48000
def run(*a): subprocess.run(a,check=True)
segs=[];lines=[];t=0.05
n=len([l for l in open('script.txt') if l.strip()])
for i in range(1,n+1):
    run('ffmpeg','-loglevel','error','-y','-i',f"vo/L{i:02d}.wav",'-af','silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,atempo=1.07','-ar',str(SR),'-ac','1',f'vo/T{i}.wav')
    a,_=sf.read(f'vo/T{i}.wav'); d=len(a)/SR
    gap={2:0.5,3:0.4,5:0.35,9:0.3,10:0.3,14:0.4,15:0.55}.get(i,0.13)
    segs+= [a,np.zeros(int(gap*SR))]; lines.append([t,t+d]); t+=d+gap
full=np.concatenate([np.zeros(int(0.05*SR))]+segs)
sf.write('vo/raw.wav',full,SR)
run('ffmpeg','-loglevel','error','-y','-i','vo/raw.wav','-af','highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-15:TP=-1.5','-ar',str(SR),'vo/voice.wav')
m=whisper.load_model('small.en')
r=m.transcribe('vo/voice.wav',language='en',word_timestamps=True)
words=[[w['word'].strip(),w['start'],w['end']] for s in r['segments'] for w in s['words']]
json.dump(dict(lines=lines,words=words,end=t+0.4),open('vo/timing.json','w'))
print('dur',t)
