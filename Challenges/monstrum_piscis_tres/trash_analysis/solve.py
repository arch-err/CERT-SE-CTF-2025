#!/usr/bin/env python ./solve.py audio.wav #
import numpy as np
import sys

# Read with proper encoding
data = []
with open(sys.argv[1], 'rb') as f:
    for line in f:
        line = line.decode('utf-8', errors='ignore').strip()
        if ',' in line:
            try:
                parts = line.split(',')
                if len(parts) == 2:
                    val = float(parts[1])
                    data.append(val)
            except ValueError:
                continue

data = np.array(data)
if len(data) == 0:
    print("No data parsed!")
    sys.exit(1)

print(f"Total samples: {len(data)}")
print(f"Min: {data.min()}, Max: {data.max()}")
print(f"Unique values: {len(np.unique(data))}")

# Ternary encoding (3 levels for "tres")
low, mid = np.percentile(data, [33, 66])
ternary = ''.join('0' if v < low else '1' if v < mid else '2' for v in data)

print(f"\nTernary (first 100): {ternary[:100]}")

# Try grouping as base-3
for group_size in [3, 4, 5, 6]:
    chars = []
    for i in range(0, len(ternary) - group_size, group_size):
        val = int(ternary[i:i+group_size], 3)
        if 32 <= val <= 126:
            chars.append(chr(val))
    text = ''.join(chars)
    if len(text) > 10:
        print(f"\nBase-3 grouped by {group_size}:")
        print(text[:200])

# Binary
threshold = np.median(data)
binary = ''.join('1' if v > threshold else '0' for v in data)
for bits in [7, 8]:
    text = ''.join(chr(int(binary[i:i+bits], 2))
                   for i in range(0, len(binary) - bits, bits)
                   if 0 < int(binary[i:i+bits], 2) < 128)
    printable_count = len([c for c in text[:50] if c.isprintable()])
    if printable_count > 20:
        print(f"\nBinary {bits}-bit:\n{text[:200]}")
