#!/usr/bin/env python3
"""Entry program for THE DAYBREAK LEDGER (news-image-20261122).

The finished poster is committed in this repository as ``entry.png``.
This program delivers it: it copies the file, byte for byte, into the
directory named by the MAKEFUN_OUTPUT_DIR environment variable (or
``/output`` when the variable is unset), then re-reads both copies and
compares their SHA-256 digests so a truncated or altered delivery is
reported as an error instead of passing silently.

Only the Python standard library is used. The grading sandbox is a bare
Python image with no third-party packages and the repository mounted
read-only, so this program writes nothing beside itself. Its output is
byte-identical on every run because the committed poster bytes are the
deliverable — nothing is re-rendered at grade time.
"""

import hashlib
import os
import sys
from pathlib import Path

POSTER = "entry.png"
DEFAULT_OUT = "/output"
BLOCK = 32 * 1024


def digest_of(path):
    """Return (byte_count, sha256_hex) for the file at path."""
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(BLOCK)
            if not chunk:
                break
            n += len(chunk)
            h.update(chunk)
    return n, h.hexdigest()


def deliver(source, target):
    """Stream source onto target without changing a single byte."""
    with open(source, "rb") as fin, open(target, "wb") as fout:
        while True:
            chunk = fin.read(BLOCK)
            if not chunk:
                break
            fout.write(chunk)


def output_dir():
    """Resolve the delivery directory: env var wins, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen) if chosen else Path(DEFAULT_OUT)


def main():
    poster_path = Path(__file__).resolve().parent / POSTER
    if not poster_path.is_file():
        print(f"missing artifact: {poster_path}", file=sys.stderr)
        return 1

    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / POSTER

    deliver(poster_path, dest)

    if digest_of(poster_path) != digest_of(dest):
        print("delivery check failed: copy differs from entry.png", file=sys.stderr)
        return 1

    size, sha = digest_of(dest)
    print(f"delivered {POSTER} -> {dest}")
    print(f"bytes {size}")
    print(f"sha256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
