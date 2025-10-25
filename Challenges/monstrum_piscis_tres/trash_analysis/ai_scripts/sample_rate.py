#!/usr/bin/env python
from scipy.io import wavfile
rate, audio = wavfile.read('audio.wav')
print(f"Sample rate: {rate} Hz")
print(f"Duration: {len(audio)/rate:.2f} seconds")
print(f"Channels: {audio.shape}")
