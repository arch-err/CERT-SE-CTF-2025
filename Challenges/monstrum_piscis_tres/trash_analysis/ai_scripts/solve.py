#!/usr/bin/env python
import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, audio = wavfile.read('audio.wav')
if len(audio.shape) > 1:
    audio = audio[:, 0]

# Parameters
symbol_rate = 50  # Hz, adjust based on spectrogram pattern spacing
samples_per_symbol = int(rate / symbol_rate)

# Define frequency bands (adjust based on your spectrogram)
freqs = [900, 1000, 1100]  # Three frequencies for "tres"

symbols = []
for i in range(0, len(audio) - samples_per_symbol, samples_per_symbol):
    chunk = audio[i:i + samples_per_symbol]

    # Check power in each frequency band
    powers = []
    for freq in freqs:
        # Bandpass filter around this frequency
        sos = signal.butter(4, [freq - 50, freq + 50], 'bandpass', fs=rate, output='sos')
        filtered = signal.sosfilt(sos, chunk)
        powers.append(np.sum(filtered ** 2))

    # Pick strongest frequency
    symbols.append(np.argmax(powers))

print(f"Symbols: {len(symbols)}")
print(f"Symbol sequence (first 100): {symbols[:100]}")

# Convert to ASCII
text = ''
for i in range(0, len(symbols) - 5, 5):
    val = int(''.join(str(s) for s in symbols[i:i+5]), 3)
    if 32 <= val <= 126:
        text += chr(val)

print(f"\nDecoded:\n{text[:500]}")


# Extract two separate bitstreams
band1 = signal.butter(4, [700, 900], 'bandpass', fs=rate, output='sos')
band2 = signal.butter(4, [1100, 1300], 'bandpass', fs=rate, output='sos')

sig1 = signal.sosfilt(band1, audio)
sig2 = signal.sosfilt(band2, audio)

# Threshold each
bits1 = (np.abs(signal.hilbert(sig1)) > np.median(np.abs(signal.hilbert(sig1)))).astype(int)
bits2 = (np.abs(signal.hilbert(sig2)) > np.median(np.abs(signal.hilbert(sig2)))).astype(int)

# Downsample to symbol rate
step = rate // 50
bits1 = bits1[::step]
bits2 = bits2[::step]

# Combine: 0 = both off, 1 = band1, 2 = band2
ternary = [0 if not b1 and not b2 else 1 if b1 and not b2 else 2 for b1, b2 in zip(bits1, bits2)]
print(ternary)
