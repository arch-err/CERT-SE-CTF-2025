#!/usr/bin/env python
import re

# Read the CSS selector line
css = open('challenge.html').read()

# Extract all nth-of-type numbers
pattern = r'span:nth-of-type\((\d+)\)'
positions = sorted([int(x) for x in re.findall(pattern, css)])

print(f"Total light pixels: {len(positions)}")
print(f"Range: {min(positions)} to {max(positions)}")

# Create a visual grid (adjust width based on viewport)
width = 64  # Try different widths: 32, 64, 80, etc.
max_pos = max(positions)
height = (max_pos // width) + 1

grid = [['█' for _ in range(width)] for _ in range(height)]

for pos in positions:
    row = (pos - 1) // width
    col = (pos - 1) % width
    if row < height:
        grid[row][col] = '░'

for row in grid:
    print(''.join(row))
