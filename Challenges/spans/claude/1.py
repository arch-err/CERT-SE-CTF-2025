#!/usr/bin/env python
import re

# Extract all nth-of-type positions
css = open('index.html').read()
positions = [int(x) for x in re.findall(r':nth-of-type\((\d+)\)', css)]

# Try interpreting positions as:
# 1. ASCII characters
print(''.join(chr(p % 256) for p in positions if p < 256))

# 2. Look for patterns in differences
diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
print(''.join(chr(d) for d in diffs if 32 <= d < 127))

# 3. Positions as indices into a string
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'
print(''.join(alphabet[p % len(alphabet)] for p in positions))

# 4. Check if positions encode coordinates
for p in positions[:20]:
    row, col = divmod(p-1, 64)
    print(f"{p}: ({row}, {col})")
