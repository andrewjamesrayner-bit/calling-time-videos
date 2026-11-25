import re,torch,torchaudio as ta,whisper,difflib,os,json
from num2words import num2words
from chatterbox.tts import ChatterboxTTS
from sb import SB
torch.set_num_threads(4)
tts=ChatterboxTTS.from_pretrained(device='cpu');asr=whisper.load_model('small.en')
def dig(m):
    s=m.group(0).replace(',','')
    try:
        n=float(s) if '.' in s else int(s)
        if isinstance(n,int) and 1800<=n<=2030: return num2words(n,to='year')
        return num2words(n)
    except Exception: return s
def norm(s):
    s=re.sub(r'£\s?([\d.,]+)\s?(bn|billion|m|million)?\b',lambda m: m.group(1)+' '+({'bn':'billion','m':'million'}.get((m.group(2) or '').lower(),m.group(2) or ''))+' pounds',s,flags=re.I)
    s=re.sub(r'\d[\d,]*(\.\d+)?',dig,s)
    s=s.lower().replace('£',' pounds ').replace('%',' percent').replace('-',' ')
    return ''.join(re.sub(r'[^a-z]','',s).split())
os.makedirs('vo5',exist_ok=True)
res=json.load(open('vo5/scores.json')) if os.path.exists('vo5/scores.json') else {}
for i,(sc,p,t) in enumerate(SB,1):
    host = sc=='pub'
    need = 2 if host else 1
    a=0
    while True:
        key=f'{i}_{a}'
        if key not in res:
            torch.manual_seed(1931*i+a)
            ex=(0.85 if host else 0.7)+0.04*(a%2); cfg=0.3
            w=tts.generate(t,exaggeration=ex,cfg_weight=cfg)
            pth=f'vo5/r{i:03d}_{a}.wav';ta.save(pth,w,tts.sr)
            h=asr.transcribe(pth,language='en')['text']
            s=difflib.SequenceMatcher(None,norm(t),norm(h),autojunk=False).ratio()
            res[key]=dict(p=pth,score=s,text=h); json.dump(res,open('vo5/scores.json','w'))
            print(i,a,round(s,3),h,flush=True)
        good=[k for k in res if k.split('_')[0]==str(i) and res[k]['score']>=0.92]
        a+=1
        if (len(good)>=1 and a>=need) or a>=4: break
print('ALLDONE',flush=True)
