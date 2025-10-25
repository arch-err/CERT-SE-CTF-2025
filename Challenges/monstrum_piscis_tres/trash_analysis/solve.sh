#!/usr/bin/env bash
set -euo pipefail

in="${1:-input.wav}"
out_base="${2:-output}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# 1) Reverse
ffmpeg -y -i "$in" -af areverse "${out_base}_reversed.wav"

# 2) Estimate beep frequency: analyze in 0.5s windows, collect peaks
# Requires ffmpeg with astats and showfreqs; we’ll extract spectrum via ebur128+astats fallback
ffmpeg -hide_banner -i "$in" -filter_complex \
  "aformat=channel_layouts=mono,asplit[s1][s2]; \
   [s1]astats=metadata=1:reset=0,ametadata=print:file=${tmp}/astats.txt; \
   [s2]showspectrum=mode=combined:slide=1:s=1024x256:legend=0:scale=lin,format=yuv420p" -t 5 -f null - 2>/dev/null || true

# Fallback simple guess via sox freq stat if present
freq=""
if command -v sox >/dev/null 2>&1; then
  if sox "$in" -n stat -freq 2>"$tmp/freq.txt"; then
    # crude parse: pick the line after "Max"
    freq=$(awk '/Max/ {getline; print int($1+0.5)}' "$tmp/freq.txt" || true)
  fi
fi

# If no freq yet, default to 1000 Hz as a placeholder
if [[ -z "${freq}" || "${freq}" -le 0 ]]; then
  echo "WARN: Could not auto-detect beep frequency. Defaulting to 1000 Hz."
  freq=1000
fi

echo "Using notch center frequency: ${freq} Hz"

# 3) Apply a narrow notch; adjust width based on sample rate
# Use ffmpeg anotch with Q=30 (narrow). Tweak if needed.
ffmpeg -y -i "$in" -af "anotch=f=${freq}:w=30:order=2" "${out_base}_debeep.wav"

echo "Done:"
echo " - ${out_base}_reversed.wav"
echo " - ${out_base}_debeep.wav"
