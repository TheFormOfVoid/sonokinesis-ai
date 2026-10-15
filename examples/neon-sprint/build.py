"""Builds the Neon Sprint example with the sonokinesis tool, the way an AI agent does it through MCP.

Run from this folder:  python build.py  [path to sonokinesis]
It starts from the level created by `sonokinesis new-level` (level.json + song.ogg) and the custom script
in scripts/, removes everything else, and lays the level out section by section.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SONOKINESIS = sys.argv[1] if len(sys.argv) > 1 else "sonokinesis"
BEAT = 60000 / 128          # 468.75 ms: the song is 128 BPM with its first beat at 0
BAR = BEAT * 4


def b(bar, beat=0.0):
    """Song time of a bar (1-based) and a beat within it (0-based)."""
    return round((bar - 1) * BAR + beat * BEAT, 3)


def run(cmd, *args, **opts):
    argv = [SONOKINESIS, cmd, HERE, *args]
    for k, v in opts.items():
        argv += ["--" + k, v if isinstance(v, str) else json.dumps(v)]
    out = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0 and cmd != "validate-level":
        sys.exit(f"{cmd} failed: {out.stderr or out.stdout}")
    return json.loads(out.stdout) if out.stdout.strip().startswith("{") else out.stdout


def edit(*ops):
    return run("edit-level", ops=list(ops))


def obj(name, shape, start, end, warn=0, outro=0, **tracks):
    o = {"name": name, "shape": shape if isinstance(shape, dict) else {"type": shape},
         "start": round(start, 3), "end": round(end, 3), "warn": round(warn, 3), "outro": outro,
         "tracks": {k: (v if isinstance(v, list) else [[0, v]]) for k, v in tracks.items()}}
    return o


# Start clean (keeps meta, theme and the song).
edit({"op": "remove", "from": -1e9, "to": 1e9}, {"op": "removeEvents"},
     {"op": "checkpoints", "set": [b(9), b(17), b(25), b(29)]},
     {"op": "meta", "set": {"author": "Sonokinesis example", "difficulty": 2,
                            "description": "An example level built entirely with the sonokinesis tool."}})

# ---- Bars 1-8: intro. A title, decorative pulses, then rain on the off-beats. ----
edit({"op": "add", "objects": [
    {**obj("title", {"type": "text", "text": "NEON SPRINT"}, 0, b(3), outro=400,
           x=0, y=-40, h=[[0, 76], [b(3), 82]]), "hitbox": False, "color": "#ffffff"},
    {**obj("subtitle", {"type": "text", "text": "a sonokinesis example", "bold": False}, b(1, 1), b(3), outro=400,
           x=0, y=40, h=26), "hitbox": False, "color": "#33e5ff"},
]})
run("add-pattern", "pulse", at=str(b(1)), params={"beats": 16, "size": 300, "color": "#33e5ff"})
run("add-pattern", "rain", at=str(b(3)), params={"count": 8, "interval": 1, "size": 40, "seed": 3})
run("add-pattern", "rain", at=str(b(5, 0.5)), params={"count": 8, "interval": 1, "size": 40, "seed": 7, "shape": "circle"})

# Bars 5-8: walls sweep through, alternating sides, with the camera punching on the beat.
for i, bar in enumerate([5, 6, 7, 8]):
    run("add-pattern", "wall", at=str(b(bar)), params={
        "dir": "left → right" if i % 2 == 0 else "right → left", "gap": [-180, 160, -40, 220][i],
        "gapSize": 190, "beats": 3, "warnBeats": 1})
run("place-script", "zoom_pulse", at=str(b(5)), beats="16", params={"amount": 1.04, "every": 1})

# ---- Bars 9-16: the drop. Bullet rings, sweeping lasers, bursts on the bar. ----
edit({"op": "addEvents", "events": [
    {"t": b(9), "type": "flash", "duration": 400, "color": "#ffffff", "opacity": 0.6},
    {"t": b(9), "type": "shake", "duration": 350, "intensity": 12},
    {"t": b(9), "type": "background", "duration": 600, "color": "#140a1c", "ease": "outQuad"},
    {"t": b(9), "type": "sway", "rotation": 1.2, "x": 6, "y": 4, "period": BAR * 2, "duration": BAR},
]})
run("place-script", "bullet_ring", at=str(b(9)), beats="8", x="0", y="0",
    params={"volleys": 7, "every": 1, "count": 14, "speed": 280, "turn": 12})
run("place-script", "laser_sweep", at=str(b(11)), beats="6", x="-640", y="-360",
    params={"from": 0, "to": 90, "beats": 4, "warnBeats": 1.5, "width": 34})
run("place-script", "laser_sweep", at=str(b(13)), beats="6", x="640", y="360",
    params={"from": 180, "to": 270, "beats": 4, "warnBeats": 1.5, "width": 34})
run("add-pattern", "bouncer", at=str(b(11)), params={"dir": "right", "bounces": 6, "beatsPer": 1, "size": 80})
for bar, (x, y) in zip([13, 14, 15, 16], [(-380, -150), (380, 150), (-380, 150), (380, -150)]):
    run("add-pattern", "burst", at=str(b(bar)), x=str(x), y=str(y), params={"count": 10, "speed": 460, "spin": bar * 9})
run("place-script", "camera_kick", at=str(b(13)), beats="1", params={"kickX": 0, "kickY": -18})

# ---- Bars 17-24: chasers and a spinner. ----
run("add-pattern", "spinner", at=str(b(17)), params={"arms": 3, "length": 360, "speed": 90, "beats": 14, "warnBeats": 2})
run("place-script", "homing_orb", at=str(b(18)), x="560", y="-280", params={"speed": 230, "chase": 5, "shards": 8})
run("place-script", "homing_orb", at=str(b(20)), x="-560", y="280", params={"speed": 230, "chase": 5, "shards": 8})
run("add-pattern", "shockwave", at=str(b(22)), params={"max": 1100, "duration": 1600})
run("add-pattern", "shockwave", at=str(b(23)), params={"max": 1100, "duration": 1600})
run("add-pattern", "spiral", at=str(b(23)), params={"count": 32, "interval": BEAT / 4, "turn": 17, "arms": 2, "speed": 380})

# ---- Bars 25-28: breakdown. Calm, darker, the ring closes in on the player each bar. ----
edit({"op": "addEvents", "events": [
    {"t": b(25), "type": "background", "duration": 900, "color": "#050608", "ease": "inOutSine"},
    {"t": b(25), "type": "sway", "rotation": 0, "x": 0, "y": 0, "period": 2000, "duration": BAR},
    {"t": b(25), "type": "zoom", "scale": 1.08, "focus": "@player", "duration": BAR * 2, "ease": "inOutSine"},
    {"t": b(29), "type": "zoom", "scale": 1, "duration": 300, "ease": "outQuad"},
]})
for bar in [25, 26, 27, 28]:
    run("place-script", "closing_ring", at=str(b(bar) - BEAT), beats="4", params={"dots": 16 + (bar - 25) * 2, "radius": 300})

# ---- Bars 29-32: final drop. Bouncing balls, lasers on the back beats. ----
edit({"op": "addEvents", "events": [
    {"t": b(29), "type": "flash", "duration": 500, "color": "#ff2a6d", "opacity": 0.5},
    {"t": b(29), "type": "shake", "duration": 400, "intensity": 14},
    {"t": b(29), "type": "background", "duration": 400, "color": "#1a0712"},
]})
run("place-script", "bouncing_balls", at=str(b(29)), beats="8", x="0", y="-200", params={"count": 5, "bounces": 4})
for i, bar in enumerate([30, 31, 32]):
    for beat in (1, 3):
        run("add-pattern", "laser", at=str(b(bar, beat)), y=str([-220, 220, 0][i] * (1 if beat == 1 else -1)),
            params={"dir": "horizontal", "thickness": 60, "beats": 1, "warnBeats": 1})
run("place-script", "beat_flash", at=str(b(29)), beats="16", params={"alpha": 0.12, "every": 1})

# ---- The end. ----
edit({"op": "addEvents", "events": [
    {"t": b(33), "type": "flash", "duration": 1200, "color": "#ffffff", "opacity": 0.9},
    {"t": b(33), "type": "background", "duration": 1200, "color": "#0b0d12"},
]}, {"op": "add", "objects": [
    {**obj("end", {"type": "text", "text": "NICE!"}, b(33), b(33) + 1400, outro=500, x=0, y=0, h=80),
     "hitbox": False, "color": "#ffffff"},
]})

report = run("validate-level")
print(json.dumps({k: report[k] for k in ("ok", "errors", "warnings", "objects", "scriptedObjects", "events")}, indent=1))
