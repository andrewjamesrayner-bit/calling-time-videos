import re,torch,torchaudio as ta,whisper,difflib,os,json
import numpy as np
from num2words import num2words
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
lines=[l.strip() for l in open('script.txt') if l.strip()]
tts=ChatterboxTTS.from_pretrained(device='cpu');asr=whisper.load_model('small.en')
def dig(m):
    s=m.group(0).replace(',','')
    try:
        n=float(s) if '.' in s else int(s)
        if isinstance(n,int) and 1800<=n<=2030: return num2words(n,to='year')
        return num2words(n)
    except Exception: return s
def norm(s):
    s=re.sub(r'\d[\d,]*(\.\d+)?',dig,s)
    s=s.lower().replace('£',' pounds ').replace('%',' percent').replace('-',' ')
    return ''.join(re.sub(r'[^a-z]','',s).split())
PUNCH={4,5,8,10,12,15,16,17}
os.makedirs('vo2',exist_ok=True)
res=json.load(open('vo2/scores.json')) if os.path.exists('vo2/scores.json') else {}
for i,t in enumerate(lines,1):
    for a in range(2):
        key=f'{i}_{a}'
        if key in res: continue
        torch.manual_seed(977*i+a)
        ex=(0.85 if i in PUNCH else 0.72)+0.05*(a%2); cfg=0.3 if a<2 else 0.4
        w=tts.generate(t,exaggeration=ex,cfg_weight=cfg)
        p=f'vo2/r{i:02d}_{a}.wav';ta.save(p,w,tts.sr)
        h=asr.transcribe(p,language='en')['text']
        s=difflib.SequenceMatcher(None,norm(t),norm(h),autojunk=False).ratio()
        res[key]=dict(p=p,score=s,text=h); json.dump(res,open('vo2/scores.json','w'))
        print(i,a,round(s,3),h,flush=True)
print('ALLDONE',flush=True)
