# maze-tui (Asciiverse packaging)

Alex G. Lopez's Maze TUI, maze builders and solvers animated in the
terminal (Rust, Ratatui, crossterm), MIT; catalog title "Maze TUI", id
`maze-tui`, kind `art`. Not our code: keep changes small, list every one in
PATCHES.md, and offer fixes upstream.

- Remotes: `upstream` is github.com/agl-alexglopez/maze-tui (branch
  `main`), `origin` is github.com/theasciiverse/maze-tui.
- Branch `asciiverse` = upstream main plus our commits.
- The Cargo workspace is in `maze_tui/`; the binary is `run_tui`, shipped
  as `maze-tui`.
- Release: tag `v<version>+<upstream date>-av.<n>` (now
  `v0.1.0+20251024-av.1`) and push only that tag; the workflow runs on
  `*-av.*` tags.
- av starts it as `maze-tui` (the home screen).
- Run anything of this program under a memory cap
  (`systemd-run --user --scope -p MemoryMax=4G ...`): a 1-row window once
  made it allocate tens of gigabytes (fixed, see PATCHES.md).
- Static build, in a copy of the tree: `docker run --rm --cpus 4 --memory
  4g -v "$PWD":/src -w /src/maze_tui rust:1-alpine sh -c 'apk add musl-dev
  && cargo build --release --locked -j4'`.
- Preview: from a folder holding the binary as `maze-tui`,
  `hub/tools/castrec.py asciiverse/maze-tui.cast <folder> "w4;s-b prim -s
  bfs-hunt;w1;kenter;r7:>:0.15;w13;kesc;w2;kesc;w1" -- ./maze-tui`.
