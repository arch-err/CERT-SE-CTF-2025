#!/usr/bin/env python
binary = '1111110000011111100000111101000001111110000011111100001111110000000110001111100000011111000000011111'

print(f"Binary length: {len(binary)}")

# Try all decodings
for bits in [7, 8]:
    for offset in range(bits):
        text = ''
        for i in range(offset, len(binary) - bits, bits):
            val = int(binary[i:i+bits], 2)
            if val > 0:
                text += chr(val) if 32 <= val <= 126 else '.'

        if len(text) > 5:
            print(f"\n{bits}-bit offset {offset}: {text}")
            if 'ctf' in text.lower():
                print(f"*** FOUND FLAG ***")

# Try inverted
binary_inv = ''.join('1' if b == '0' else '0' for b in binary)
print(f"\n=== Inverted ===")
for bits in [7, 8]:
    text = ''.join(chr(int(binary_inv[i:i+bits], 2))
                   for i in range(0, len(binary_inv)-bits, bits)
                   if 0 < int(binary_inv[i:i+bits], 2) < 128)
    print(f"{bits}-bit: {text[:50]}")

# Try run-length decoding
import itertools
runs = [(k, len(list(g))) for k, g in itertools.groupby(binary)]
print(f"\nRun lengths: {runs}")

# Maybe runs encode ternary?
ternary = ''.join(str(min(length, 2)) for k, length in runs)
print(f"Ternary from runs: {ternary}")
