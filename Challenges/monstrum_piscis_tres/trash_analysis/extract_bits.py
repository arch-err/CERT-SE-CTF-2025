#!/usr/bin/env python
import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt

data = np.fromfile('audio.raw', dtype=np.int16).astype(float)
fs = 8000

# Get amplitude envelope
analytic_signal = hilbert(data)
envelope = np.abs(analytic_signal)

# Downsample envelope for easier analysis
downsample = 100
env_down = envelope[::downsample]
time = np.arange(len(env_down)) * downsample / fs

plt.figure(figsize=(20,4))
plt.plot(time, env_down)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.savefig('envelope.png')

# Threshold to get bits
threshold = np.median(envelope)
bits = (envelope > threshold).astype(int)
print(f"Total bits: {len(bits)}")
print(f"First 200 bits: {''.join(map(str, bits[:200]))}")

with open("./bits.txt", "w") as filp:
    filp.write(''.join(map(str, bits)))
