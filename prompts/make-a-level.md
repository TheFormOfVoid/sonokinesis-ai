# Make a level

Copy this into your AI client, fill in the blanks, and attach or point to your song.

```
Read AGENTS.md, then make a Beatform level for my song.

Song file: C:\path\to\song.ogg
Title / artist: ...
Length: the whole song (or: the first 90 seconds)
Difficulty: medium (1 = relaxed, 5 = brutal)
Mood and ideas: ... (e.g. "lots of lasers in the chorus, a calm breakdown with a slow spinning
cross, end on a big flash")

Analyse the song first and show me a section plan with bar numbers before building. Build one
section at a time, validate it, show me a contact sheet, and start it in the game so I can play it.
```

# Add or change a section

```
In levels/<name>: bars 25-32 feel empty. Add something that builds up to the drop at bar 33,
using the snare hits. Show me renders around bar 31 before and after.
```

# Tune

```
I just played levels/<name>. The walls in bars 9-12 come too fast (I can't read the gap),
and the homing orbs at bar 18 are too easy. Fix those two things only.
```

# A new attack

```
Write a new attack script for levels/<name>: a snake of 12 squares that slithers across the
screen in a sine wave and follows the player slowly. Settings: length, speed, wave height.
Check it, place it at bar 41 for 8 beats, and render frames at bar 41, 42 and 43.
```

# A new effect

```
Write an effect that slowly tilts the camera with the music's energy and flashes the background
on every bar, and use it during the final chorus.
```
