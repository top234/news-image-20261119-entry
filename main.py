#!/usr/bin/env python3
"""Entry program for news-image-20261119.

Writes the pre-rendered front-page image to /output/entry.png.
Standard library only; deterministic: the same bytes on every run.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

MAX_BYTES = 1 * 1024 * 1024
EXPECT_W, EXPECT_H = 1024, 1024


def check_png(path):
    """Fail loudly unless path is a valid 1024x1024 PNG of at most 1 MiB."""
    if not os.path.isfile(path):
        sys.exit("entry.png missing next to main.py: %s" % path)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        sys.exit("entry.png too big: %d bytes (limit %d)" % (size, MAX_BYTES))
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a valid PNG")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (EXPECT_W, EXPECT_H):
        sys.exit("entry.png is %dx%d, expected %dx%d"
                 % (width, height, EXPECT_W, EXPECT_H))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    check_png(SRC)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
