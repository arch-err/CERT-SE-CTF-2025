#!/usr/bin/env python
import re

html = open("index.html", "r", encoding="utf-8").read()
on = set(map(int, re.findall(r":nth-of-type\((\d+)\)", html)))

# 64x64 grid
g = [[0]*64 for _ in range(64)]
for p in on:
    r, c = divmod(p-1, 64)
    g[r][c] = 1
g = [list(x) for x in zip(*g[::-1])]  # rotate 90 cw
# 1) flip odd columns (dead-channel parity)
for r in range(64):
    for c in range(64):
        if c % 2 == 1:
            g[r][c] ^= 1

# 2) snake rows, 3) bytes, 4) XOR 0x55 on odd rows
out = bytearray()
for r in range(64):
    row = g[r][:]
    if r % 2 == 1:  # snake
        row.reverse()
    for i in range(0, 64, 8):
        byte = int("".join(map(str, row[i:i+8])), 2)
        if r % 2 == 1:
            byte ^= 0x55
        out.append(byte)

s = out.decode("ascii", errors="ignore")
print(s)

import re as rx
m = rx.search(r"ctf[\[{(].*?[}\])]", s, rx.I)
print("FLAG:", m.group(0) if m else "not found")
