# Changes from upstream

This is the Asciiverse packaging of [Maze TUI](https://github.com/agl-alexglopez/maze-tui)
by Alex G. Lopez: maze building and solving algorithms animated in the
terminal (Rust, Ratatui and crossterm). Upstream is the `upstream` remote;
the `asciiverse` branch carries the changes below.

Built from upstream `main` at `5bf8baf` (2025-10-24). Upstream has no
tags; the crate version is 0.1.0.

## Licence

MIT, "Copyright (c) 2023 Alex G. Lopez" in LICENSE (checked 2026-11-02).
The workspace crates carry no licence field of their own. Their
dependencies (ratatui, crossterm, tui-textarea, rand, crossbeam-channel and
theirs) are MIT, or MIT and Apache-2.0 dual licensed, by `cargo metadata`;
unicode-ident adds the Unicode-DFS-2016 licence.

## Code

- **Ctrl+C quits from any screen.** In raw mode Ctrl+C arrives as a key;
  upstream ignored it during animations and typed it into the command line
  on the home screen. The event thread now sends a quit, and every screen
  leaves through the normal exit, which puts the terminal back.
- **Small windows.** Below 12x12 the home screen shows "Make the window
  bigger" instead of building its background maze: the builders panicked
  there on an empty random range. The window size minus its border now
  stops at 0; under 2 rows or columns it wrapped around, and the maze
  buffer was allocated from the wrapped size (tens of gigabytes).
- **Resizing.** The home maze is sized from the current window rather than
  the size of the last frame drawn, and the maze widgets stay inside the
  screen buffer: a frame drawn after a shrink, before the resize event
  arrived, wrote past its end and panicked.

## Packaging

- `.github/workflows/release.yml`: av archives `maze-tui-<target>` for Linux
  (static musl, x86-64 and ARM64, built in Alpine), macOS (x86-64 and
  ARM64) and Windows (x86-64 and ARM64, MSVC), with the binary (upstream's
  `run_tui`, renamed `maze-tui`), LICENSE, README and this file, plus
  SHA256SUMS. Runs on our tags only (`*-av.*`).
- `asciiverse/maze-tui.cast`, the catalog preview, recorded at 100x30 with
  hub's `tools/castrec.py`: the home screen, then `-b prim -s bfs-hunt`,
  sped up with `>`, Prim's builder and the four BFS threads hunting for the
  finish.

av starts it as `maze-tui` with no arguments: the home screen, where Enter
plays a random maze and flags choose the algorithms.

## Checked

- Linux, static musl build (Alpine, rustc 1.99.0), in tmux: Esc and Ctrl+C
  quit with status 0 from the home screen, an animation and the info popup;
  resized repeatedly between 1x1 and 120x40 at home and during animations
  without a crash; memory 5 MB at 100x30, 24 MB at 400x120, flat over 40
  mazes in a row.
- Windows and macOS: `cargo check` for x86_64-pc-windows-msvc and
  aarch64-apple-darwin passes; not run.

## Ours

- **How to play it, at the top of README.md.** A short note on installing
  and starting it with av; the original text follows unchanged.
