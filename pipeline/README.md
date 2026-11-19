# Calling Time production pipeline

Landlord-style stickman Shorts (1080x1920) and long-form (1920x1080), rendered with pycairo.

## Setup (fresh workspace)
pip install --break-system-packages chatterbox-tts openai-whisper num2words pycairo soundfile scipy
git clone --depth 1 https://github.com/wyzowl/sfx-kit /home/claude/assets/sfx-kit
mkdir -p /home/claude/assets/music && curl -s -o /home/claude/assets/music/quirky_jazz.mp3 https://opengameart.org/sites/default/files/quirky_jazz_0.mp3   # CC0
Voice: Chatterbox stock voice, exaggeration 0.7-0.85, cfg 0.3 ("Voice 2" chosen by Andy). Never use Andy's voice.

## Short workflow (pipeline/short, copy to a work dir e.g. /home/claude/cN)
1. script.txt: one TTS line per row, numbers written as words. Last 3 lines: moral (landlord), "Time, gentlemen, please!", "Oi! Before you go... hit subscribe, smash that like... or you're barred."
2. Edit gen2.py PUNCH set (punchline line numbers, 1-based). Run gen2.py in a retry loop (OOM-safe): until grep -q ALLDONE gen2.log; do python3 gen2.py >> gen2.log 2>&1; done
3. python3 select_takes.py   (picks most expressive passing take per line)
4. python3 asm.py            (vo/voice.wav + vo/timing.json via whisper)
5. Edit sh.py: topcard(), HL/GOLDW caption colours, SPEC (shot, line_idx, trigger), story shots in draw_shot (see story.py for examples), reactions(), PUNCHT. Keep spit/moral/bell/cheeky shots.
6. python3 sh.py shots -> check stills; python3 sfx2.py 20; python3 sh.py video -> final.mp4 (-14 LUFS)
Never run TTS at the same time as whisper or rendering (8GB RAM).

## Publish
Copy final.mp4 into shorts/ in this repo, push, then vidIQ: vidiq_video_upload(url=raw.githubusercontent.com/.../shorts/<file>.mp4) -> vidiq_social_post_draft_create (YouTube, platformAccountId UCtqwK95hVOYOhGnRVSzC3vw, privacyStatus public, publishAt) -> show Andy -> vidiq_social_post_publish ONLY after he approves.
