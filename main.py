#!/usr/bin/env python3
"""Entrypoint for the news-image-20261122 submission.

The submission is a single picture: entry.png, a front page that sums up
the world news of Sunday 22 November 2026. This program's only job is to
place that bundled picture where make.fun expects it.

It uses nothing but the Python standard library, reads no network, and
writes the exact same bytes on every run, because it copies a fixed file.
"""

from pathlib import Path
import hashlib
import os
import shutil
import sys


def locate_picture() -> Path:
    """Return the path of the picture bundled next to this file."""
    here = Path(__file__).resolve().parent
    picture = here / "entry.png"
    if not picture.is_file():
        print(f"missing bundled picture: {picture}", file=sys.stderr)
        raise SystemExit(1)
    return picture


def main() -> int:
    source = locate_picture()
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / "entry.png"
    shutil.copyfile(source, destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(f"wrote {destination} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
