#!/usr/bin/env python ./solve.py ../index_modified.html #
# crop_upscale_only.py
import re, sys
from pathlib import Path
from PIL import Image, ImageOps

src = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
m = re.search(r"(span:nth-of-type\([^)]+\)(?:\s*,\s*span:nth-of-type\([^)]+\))*\s*\{[^}]*lightgreen[^}]*\})", src, re.S)
block = m.group(1) if m else src
idx = sorted(set(map(int, re.findall(r"nth-of-type\((\d+)\)", block))))

W, N = 64, 4096
bits = [1 if (i in idx) else 0 for i in range(1, N + 1)]

def img_from_bits(bits):
    H = N // W
    im = Image.new("1", (W, H))
    im.putdata(bits)
    return im

def auto_crop(im):
    im = ImageOps.invert(im.convert("L"))  # black modules as 0
    w, h = im.size
    # rows/cols that contain any black
    rows = [any(im.getpixel((x, y)) == 0 for x in range(w)) for y in range(h)]
    cols = [any(im.getpixel((x, y)) == 0 for y in range(h)) for x in range(w)]
    top = next((i for i,v in enumerate(rows) if v), 0)
    bot = h-1 - next((i for i,v in enumerate(reversed(rows)) if v), 0)
    left = next((i for i,v in enumerate(cols) if v), 0)
    right = w-1 - next((i for i,v in enumerate(reversed(cols)) if v), 0)
    return im.crop((left, top, right+1, bot+1))

for inv in [False, True]:
    data = bits if not inv else [1-b for b in bits]
    im = img_from_bits(data)
    cr = auto_crop(im)
    up = cr.resize((cr.width*12, cr.height*12), Image.NEAREST)
    fname = f"bar_inv{int(inv)}.png"
    up.save(fname)
    print("saved", fname)
