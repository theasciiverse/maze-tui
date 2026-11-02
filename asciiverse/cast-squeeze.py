#!/usr/bin/env python3
"""Shortens the still stretches of an asciicast v3 recording.

maze-tui holds a finished maze on screen and keeps redrawing it unchanged,
and how long a random maze takes to build and solve differs from run to
run, so a scripted recording cannot cut at the right moment. This replays
the cast in a terminal emulator (pyte) and caps every stretch in which the
screen does not change at LIMIT seconds; everything that moves keeps its
timing.

Usage: cast-squeeze.py <in.cast> <out.cast> [LIMIT, default 0.8]
"""
import json, sys

import pyte

src, dst = sys.argv[1], sys.argv[2]
limit = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8

with open(src) as f:
    lines = f.read().splitlines()
head = json.loads(lines[0])
if head.get("version") != 3:
    sys.exit("asciicast v3 only")
screen = pyte.Screen(head["term"]["cols"], head["term"]["rows"])
stream = pyte.Stream(screen)


def snapshot():
    return [[(c.data, c.fg, c.bg, c.bold, c.reverse)
             for c in (screen.buffer[y][x] for x in range(screen.columns))]
            for y in range(screen.lines)]


out = [lines[0]]
before = snapshot()
still = 0.0          # seconds the screen has not changed, at original pace
total_in = total_out = 0.0
for line in lines[1:]:
    if not line.strip():
        continue
    delay, kind, data = json.loads(line)
    # the screen was unchanged during this delay; keep only what the cap allows
    kept = min(delay, max(0.0, limit - still))
    still += delay
    total_in += delay
    total_out += kept
    if kind == "o":
        stream.feed(data)
        now = snapshot()
        if now != before:
            still = 0.0
            before = now
    out.append(json.dumps([round(kept, 6), kind, data], ensure_ascii=False))

with open(dst, "w") as f:
    f.write("\n".join(out) + "\n")
print(f"{dst}: {total_in:.1f} s -> {total_out:.1f} s", file=sys.stderr)
