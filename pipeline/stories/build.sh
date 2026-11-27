# usage: build.sh story.py out_sh.py
{ cat /home/claude/gen/head.py; cat "$1"; cat /home/claude/gen/mid.py /home/claude/gen/generic.py; cat /home/claude/gen/tail.py; } > "$2"
