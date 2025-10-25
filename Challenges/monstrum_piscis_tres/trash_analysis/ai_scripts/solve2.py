#!/usr/bin/env python
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt

rate, audio = wavfile.read('audio.wav')

# Define the two bands you see in spectrogram
# Estimate from your images: ~400Hz and ~1600Hz roughly
f_low = [300, 500]   # Adjust based on your spectrogram
f_high = [1500, 1700]

# Extract each band
sos_low = signal.butter(4, f_low, 'bandpass', fs=rate, output='sos')
sos_high = signal.butter(4, f_high, 'bandpass', fs=rate, output='sos')

band_low = signal.sosfilt(sos_low, audio)
band_high = signal.sosfilt(sos_high, audio)

# Get envelopes
env_low = np.abs(signal.hilbert(band_low))
env_high = np.abs(signal.hilbert(band_high))

# Plot to verify
plt.figure(figsize=(12, 4))
plt.plot(env_low[:8000], label='Low band')
plt.plot(env_high[:8000], label='High band')
plt.legend()
plt.savefig('bands.png')
plt.show()

# Now threshold and decode as two separate bitstreams
