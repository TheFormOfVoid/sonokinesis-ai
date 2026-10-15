# sonokinesis-ai

Let an AI build Just Shapes & Beats custom levels with [Sonokinesis](https://github.com/TheFormOfVoid/sonokinesis).

Plug an AI agent (Claude Code, Claude Desktop, or any client that speaks MCP) into Sonokinesis and it can
make a level the way a person does in the editor: listen to the song, lay out hazards on the beat,
write its own attacks and effects in code, check its work as pictures, and start the level in the game
for you to play. This repository holds the instructions, setup and examples for that; the tool itself
(`sonokinesis`) comes with Sonokinesis.

## What you need

- **Sonokinesis** (the release zip): the editor, the `sonokinesis` tool in `tools/`, the script library and
  the docs. Install its loader into the game with `Install-Sonokinesis.bat` if you want to play levels.
- **Just Shapes & Beats** on Steam, to play the levels (not needed to build them).
- An **AI client with MCP support**.

## Setup

1. Unzip the Sonokinesis release next to this folder (or anywhere).
2. Double-click `setup.bat` in this folder (or run `.\setup.ps1` in PowerShell). It finds
   `sonokinesis.exe` (or pass `-Sonokinesis C:\path\to\sonokinesis.exe`), writes `.mcp.json`, creates
   `levels/`, and checks the game and the loader.
3. Open your AI client here:
   - **Claude Code**: run `claude` in this folder and approve the `sonokinesis` server. Or add it yourself:
     `claude mcp add sonokinesis -- "C:\path\to\sonokinesis.exe" mcp`.
   - **Claude Desktop** and other clients: add the server from `.mcp.json` to their MCP settings
     (`"command": "C:\\path\\to\\sonokinesis.exe", "args": ["mcp"]`).
4. Start with a prompt from [prompts/make-a-level.md](prompts/make-a-level.md). The first line asks the
   agent to read [AGENTS.md](AGENTS.md), its working instructions.

Without MCP, an agent that can run commands can use the same tool from the shell:
`sonokinesis help` lists the commands (`sonokinesis new-level`, `sonokinesis render-sheet`, ...).

## What the agent can do

| | tools |
|---|---|
| read the docs | `docs` |
| start a level from a song, with tempo and beat detection | `new_level`, `analyze_song`, `beat_times` |
| see and change the level | `level_info`, `read_level`, `write_level`, `edit_level` |
| use the built-in attacks, effects and patterns | `list_scripts`, `read_script`, `place_script`, `add_pattern` |
| write its own attacks and effects | `write_script`, `check_script` |
| check the level | `validate_level` |
| look at it | `render_frames`, `render_sheet` (pictures come back to the model) |
| play it | `play_in_game`, `game_status`, `game_screenshot` |
| work with the editor open | `editor`, `editor_screenshot` |

If the Sonokinesis Editor is open on the same level, it reloads every time the agent changes it, so you
can watch the level being built and fix things by hand in between.

## Examples

[examples/neon-sprint](examples/neon-sprint) is a complete one-minute level built only with the tool:
`build.py` is the sequence of commands (what an agent sends through MCP), including a custom attack in
`scripts/closing_ring.js`. Open the folder in the editor or play it in the game.

## Docs

`docs/` has a copy of Sonokinesis's guides for agents that read files: [ai-guide](docs/ai-guide.md) (start
here), [level-format](docs/level-format.md), [scripting](docs/scripting.md), [ai-tools](docs/ai-tools.md)
and [editor-guide](docs/editor-guide.md). The `docs` tool serves the same guides from the Sonokinesis you
installed. `sync-docs.ps1` refreshes the copy from a Sonokinesis checkout
(`powershell -ExecutionPolicy Bypass -File sync-docs.ps1`).

## Good to know

- Levels the agent makes go in `levels/` (ignored by git: songs are usually not yours to publish).
- Only use songs you have the right to use, and don't copy art, sounds or levels from the game or
  from other people.
- Sonokinesis is an unofficial fan project, not affiliated with or endorsed by Berzerk Studio.

## License

GPL-3.0, like Sonokinesis ([LICENSE](LICENSE)). The example level's song is Sonokinesis's own demo track.
