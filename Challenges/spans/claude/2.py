#!/usr/bin/env python
import re

html = open('index.html').read()
lit_positions = set(int(x) for x in re.findall(r':nth-of-type\((\d+)\)', html))

# Create 64x64 grid (positions are 1-indexed)
grid = [[0]*64 for _ in range(64)]
for pos in lit_positions:
    row, col = divmod(pos - 1, 64)
    grid[row][col] = 1

# Try reading as bytes horizontally
result = []
for row in grid:
    for i in range(0, 64, 8):
        byte = int(''.join(str(b) for b in row[i:i+8]), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Horizontal:', ''.join(result))

# Try reading as bytes vertically
result = []
for col in range(64):
    for row_start in range(0, 64, 8):
        byte = int(''.join(str(grid[row_start+i][col]) for i in range(8)), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Vertical:', ''.join(result))

# Try LSB first (reverse bit order)
result = []
for row in grid:
    for i in range(0, 64, 8):
        byte = int(''.join(str(b) for b in row[i:i+8][::-1]), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Horizontal LSB:', ''.join(result))

# Try 7-bit ASCII or other chunk sizes
for chunk_size in [5, 6, 7, 8]:
    result = []
    bits = ''.join(str(grid[r][c]) for r in range(64) for c in range(64))
    for i in range(0, len(bits), chunk_size):
        val = int(bits[i:i+chunk_size], 2)
        if 32 <= val < 127:
            result.append(chr(val))
    print(f'{chunk_size}-bit:', ''.join(result)[:100])


# XOR each row with a repeating pattern
for pattern in [0xAA, 0x55, 0xFF, 0x00]:
    result = []
    for row in grid:
        for i in range(0, 64, 8):
            byte = int(''.join(str(b) for b in row[i:i+8]), 2)
            byte ^= pattern
            if 32 <= byte < 127:
                result.append(chr(byte))
    print(f'XOR 0x{pattern:02X}:', ''.join(result)[:80])


result = []
for i in range(63):
    xor_row = [grid[i][j] ^ grid[i+1][j] for j in range(64)]
    for k in range(0, 64, 8):
        byte = int(''.join(str(b) for b in xor_row[k:k+8]), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Row XOR:', ''.join(result))


# Checkerboard XOR (like static noise pattern)
result = []
for row in range(64):
    for col_start in range(0, 64, 8):
        byte_bits = []
        for bit_idx in range(8):
            col = col_start + bit_idx
            bit = grid[row][col]
            # XOR based on position
            if (row + col) % 2 == 0:
                bit ^= 1  # XOR with checkerboard
            byte_bits.append(str(bit))
        byte = int(''.join(byte_bits), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Checkerboard XOR:', ''.join(result))

result = []
for row in range(64):
    xor_val = 0x55 if row % 2 == 0 else 0xAA
    for i in range(0, 64, 8):
        byte = int(''.join(str(grid[row][i+j]) for j in range(8)), 2)
        byte ^= xor_val
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Alternating rows:', ''.join(result))

result = []
for row in range(64):
    for col_start in range(0, 64, 8):
        byte_bits = []
        for bit_idx in range(8):
            col = col_start + bit_idx
            bit = grid[row][col]
            # Alternate by column
            if col % 2 == 1:
                bit ^= 1
            byte_bits.append(str(bit))
        byte = int(''.join(byte_bits), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
        else:
            result.append('.')
print('Alt columns:', ''.join(result))


# XOR in checkerboard but read differently
bits = []
for r in range(64):
    for c in range(64):
        bit = grid[r][c]
        if c % 2 == 1:  # Only XOR odd columns
            bit ^= 1
        bits.append(str(bit))

# Convert to bytes
result = []
for i in range(0, len(bits), 8):
    byte = int(''.join(bits[i:i+8]), 2)
    if 32 <= byte < 127:
        result.append(chr(byte))
print('Column parity:', ''.join(result))

result = []
for row in range(64):
    for col_start in range(0, 64, 8):
        byte_bits = []
        for bit_idx in range(8):
            col = col_start + bit_idx
            bit = grid[row][col]
            # XOR odd columns AND odd rows
            if col % 2 == 1 and row % 2 == 1:
                bit ^= 1
            byte_bits.append(str(bit))
        byte = int(''.join(byte_bits), 2)
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Row+Col XOR:', ''.join(result))

result = []
for row in range(64):
    xor_pattern = 0x55 if row % 2 == 1 else 0x00
    for col_start in range(0, 64, 8):
        byte = int(''.join(str(grid[row][col_start+j]) for j in range(8)), 2)
        byte ^= xor_pattern
        if 32 <= byte < 127:
            result.append(chr(byte))
print('Odd rows XOR 0x55:', ''.join(result))


import base64

encoded = "A@;&TQ|;PN%U]8uUb#uE6D&JEOU!2ZL,&0)eSAKMyWy@HdSqdeX1,W6   MT9ytml!D1e9I0@KXhLu &T.fY8!iWL3E3&0P;AXyd;D?ya5g 0CmM'A-I,P~]mWV!*e}_}mUA SLLZ7ee1%a9%5!]/.cu\ei %MumT%n@XYNL0c5%D6\q]1sz,eFWe}^iyM\"QYY[iGms|4k (`ssteWL85W^LQ}"

# Try Base85 (ASCII85)
try:
    import base64
    print("Base85:", base64.a85decode(encoded))
except Exception as e:
    print(f"Base85 error: {e}")

# Try Base64 (with padding)
try:
    print("Base64:", base64.b64decode(encoded + '=='))
except:
    pass

# ROT47
result = []
for c in encoded:
    if 33 <= ord(c) <= 126:
        result.append(chr(33 + (ord(c) - 33 + 47) % 94))
    else:
        result.append(c)
print("ROT47:", ''.join(result))

# Check if flag is already visible
if 'ctf[' in encoded or 'ctf{' in encoded:
    print("FOUND:", encoded)


import base64
import zlib

encoded = "A@;&TQ|;PN%U]8uUb#uE6D&JEOU!2ZL,&0)eSAKMyWy@HdSqdeX1,W6   MT9ytml!D1e9I0@KXhLu &T.fY8!iWL3E3&0P;AXyd;D?ya5g 0CmM'A-I,P~]mWV!*e}_}mUA SLLZ7ee1%a9%5!]/.cu\ei %MumT%n@XYNL0c5%D6\q]1sz,eFWe}^iyM\"QYY[iGms|4k (`ssteWL85W^LQ}"
data = base64.b64decode(encoded + '==')

# Try zlib decompression
try:
    print("zlib:", zlib.decompress(data))
except:
    pass

# Try with different wbits for gzip/deflate
for wbits in [15, -15, 16+15]:
    try:
        print(f"zlib wbits={wbits}:", zlib.decompress(data, wbits))
    except:
        pass

# XOR with common single bytes
for key in range(256):
    result = bytes([b ^ key for b in data])
    if b'ctf' in result or b'flag' in result.lower():
        print(f"XOR 0x{key:02x}:", result)

# Check for magic bytes
print("First bytes (hex):", data[:16].hex())
