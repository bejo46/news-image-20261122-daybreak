# news-image-20261122 — THE DAYBREAK LEDGER

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bejo46/news-image-20261122-daybreak/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bejo46/news-image-20261122-daybreak/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A dark-broadsheet front page summing up the world's news of **Sunday 22 November 2026**:
17 stories across 7 regions, led by the tanker strikes in the Strait of Hormuz and the
collapse of the COP31 climate talks.

Built for the [make.fun](https://make.fun/bounty/news-image-20261122) bounty
**news-image-20261122** ("Sum up 22 November's world news in one image").

## What it is

- `entry.png` — the poster itself, 1024×1024 PNG.
- `render_daybreak.py` — the program that draws the poster from scratch with Pillow
  (masthead, Hormuz hero scene, a six-number strip, 12 fully illustrated story cards
  in a 3×4 grid, an ALSO TODAY strip with 4 more stories, region chips, DATE CHECK).
  Run it twice and the bytes are identical.
- `main.py` — the entry program the grader runs: standard library only, it copies the
  committed `entry.png` into `MAKEFUN_OUTPUT_DIR` (default `/output`) and verifies the
  copy by SHA-256 before reporting success.
- `stories-daybreak.md` — the story ledger: every headline, number and source on the
  poster, with the date-check notes.

## How to run

```sh
python3 render_daybreak.py   # rebuild entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # deliver out/entry.png
```

## License

MIT — see `LICENSE`.
