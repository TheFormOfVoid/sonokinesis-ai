# Instructions for AI agents

You are helping someone make a custom level for Just Shapes & Beats with **Beatform**. You have the
`beatform` MCP tools (or the `beatform` command line, same commands with dashes). With them you can
do everything the Beatform Editor does: create a level from a song, place and animate hazards, write
your own attacks and effects in JavaScript, check the level, look at it as pictures, and play it in
the game.

Before building anything, read the guides (the `docs` tool, or the files in `docs/`):

1. `ai-guide`: the workflow and what makes a level good. **Read it first.**
2. `level-format`: every field of level.json.
3. `scripting`: writing attacks, effects and patterns.
4. `ai-tools`: every tool and the edit operations.

## Rules

- **Work in a level folder.** New levels go in `levels/<name>/` in this repository unless the person
  says otherwise. Never write inside the game's folder yourself; `play_in_game` loads a level from
  wherever it is.
- **Validate after every change** (`validate_level`) and fix every error before going on. Read the
  warnings.
- **Look before you say it works.** Use `render_sheet` for a section and `render_frames` around each
  hit. Check that warnings come before hits and that there is always a safe place.
- **Time everything to the music.** Run `analyze_song` first; use `beat_times` or
  `k × 60000 / bpm` for beats. The moment an object hurts is `start + warn`: that goes on the beat.
- **Telegraph every hazard** (at least half a beat of warning, usually one beat) and **always leave a
  way out**.
- **Prefer the library** (`list_scripts`) for common attacks; write a script when nothing fits, then
  `check_script` it before placing it.
- **Share the plan, then build.** Tell the person what you're about to make (sections, bars, ideas) in
  a few lines, build one section at a time, and ask them to play it. You can't feel the level; they
  can. Change one thing at a time when tuning.
- **Only use songs the person has the right to use**, and never copy anything (art, sounds, levels)
  from the game or from other people's levels.
- If the developer console is needed (`game_screenshot`), tell the person to set `DevConsole = true`
  (and `BlockAllSaves = true` while testing) in
  `Just Shapes & Beats/BepInEx/config/dev.beatform.loader.cfg`, restart the game, and switch both back
  to `false` afterwards.

## A good first session

1. Ask for the song file, its title and artist, and what kind of level they want (length, difficulty,
   mood, favourite attack styles).
2. `new_level` into `levels/<name>`, then `analyze_song` and summarise the song's sections.
3. Propose a section plan with bar numbers and checkpoints. Wait for a yes.
4. Build the intro, validate, render, show the sheet, ask them to play it (`play_in_game`).
5. Continue section by section. Finish with a full `validate_level`, a sheet of each section, and a
   play from the start.

## When something goes wrong

- A tool returns `Error: ...`: read it, it says what to fix.
- A script error names the file and line; `read_script`, fix, `write_script` (it re-checks).
- The game doesn't answer `play_in_game`: it must be running with the Beatform loader installed, on a
  menu, and focused. `game_status` tells you what it sees.
- The person says a hit felt early or late: check its `start + warn` against `beat_times`. Felt unfair:
  lengthen the warning or widen the gap. Too easy or too busy: change density, not speed.
