from collections import defaultdict
import json
import sys

src = sys.argv[1]
dst = sys.argv[2]

f = open(src, "r")

data = json.load(f)
f.close()

out = defaultdict(lambda: [])

def translate_black_card(src):
    src["deck"] = "CAHe1"
    src["icon"] = "1"
    return src

def translate_white_card(src):
    return {
        "deck": "CAHe1",
        "icon": "1",
        "text": src,
    }

for k, v in data.iteritems():
    if k == "blackCards":
        for bc in v:
            out["black"].append(translate_black_card(bc))
    elif k == "whiteCards":
        for wc in v:
            out["white"].append(translate_white_card(wc))
    else:
        out[k] = v

fout = open(dst, "w+")
json.dump(out, fout, indent = 4)
  
fout.close()