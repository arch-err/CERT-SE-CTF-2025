#!/usr/bin/env python
import lz4.block
import struct

with open('sessionstore.jsonlz4', 'rb') as f:
    magic = f.read(8)  # "mozLz40\0"
    size = struct.unpack('<I', f.read(4))[0]
    compressed = f.read()

decompressed = lz4.block.decompress(compressed, uncompressed_size=size)
with open("sessionstore.json", "w") as f:
    f.write(decompressed.decode('utf-8'))
