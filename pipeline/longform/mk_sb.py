from sb_old import SB as OLD, GOLD, RED, M
import pprint
SB = list(OLD)
def idx(sub):
    for i, (_, _, t) in enumerate(SB):
        if sub in t: return i
    raise KeyError(sub)
def after(sub, entry): SB.insert(idx(sub) + 1, entry)
def replace(sub, entry): SB[idx(sub)] = entry
# cold open spit-take
after("For one pound.", ("pub", dict(act="spit", trig="Total", badge="TOTAL."), "Not one pound per shop. One pound. Total."))
# host intro after the title card
after("This is the story of British Home Stores.", ("pub", dict(act="intro"), "Evening, and welcome to Calling Time. Pull up a stool, because this one's a belter."))
# chapter quips
after("It was seen as cheap, and dowdy.", ("pub", dict(act="quip", look="down", badge="CHEAP & DOWDY?", mood="flat"), "Cheap and dowdy. Bit like my carpet."))
after("significantly more money left the company", ("pub", dict(act="quip", mood="sly", badge="I KNOW HOW THIS ENDS"), "Money going out faster than it comes in? I've run a pub. I know how that ends."))
after("MPs called that an insult", ("pub", dict(act="quip", mood="raised", badge="THAT'S A LOT OF DRIPS"), "A drip in the ocean. Two point six million pounds. That's a lot of drips."))
# ending: landlord delivers the rule, bell, cheeky CTA
replace("So here's the one question", ("pub", dict(act="point", trig="why", badge="ASK WHY."), "So here's the one question that could have saved eleven thousand jobs. When a chain with more than a hundred and sixty stores is worth one pound... ask why."))
after("Tell me in the comments.", ("pub", dict(act="bell"), "Time, gentlemen, please!"))
after("Time, gentlemen, please!", ("pub", dict(act="cheeky"), "Oi! Before you go... hit subscribe, smash that like... or you're barred."))
replace("watch this video next", ("end", dict(), "And for nine more British business disasters, watch this one next."))
REACT = [  # (line text substring, trigger word, kind, label)
    ("More than double", "double", "jaw", "MORE THAN DOUBLE?!"),
    ("three hundred and fifty-four million", "fifty-four", "wince", "OOF"),
    ("declared bankrupt twice", "Twice", "facepalm", "OH NO"),
    ("The sale went ahead anyway", "anyway", "facepalm", "WHY?!"),
    ("jailed for six years", "jailed", "smug", "TOLD YOU"),
]
with open('sb.py', 'w') as f:
    f.write("GOLD = (0.788, 0.635, 0.153)\nRED = (0.784, 0.208, 0.180)\n")
    f.write("SB = " + pprint.pformat(SB, width=220) + "\n")
    f.write("REACT = " + pprint.pformat(REACT, width=220) + "\n")
print(len(SB))
