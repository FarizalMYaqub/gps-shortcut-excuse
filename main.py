#!/usr/bin/env python3
"""The GPS Swears It Was a Shortcut — entry program.

One original line, in the GPS's own voice: its excuse for sending
the driver down the wrong road. The program prints that excuse to
/output/entry.txt. The excuse never changes between runs — it is a
constant in this file, not a guess, not a fetch, not a roll of the
dice — so the judge always reads the same bytes.

The joke: the GPS blames the map, then lists its witnesses — the
lake, the wedding guests, the cul-de-sac — and ends by thanking the
one place that actually welcomed it. Smug, defensive, caught red
handed, exactly the voice the brief asks for.
"""

import os
import sys

EXCUSE = (
    "The map promised me a road. The lake disagreed, the wedding "
    "guests applauded, and the cul-de-sac was the only one who "
    "thanked me."
)

ENTRY_OUTPUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
MAX_CHARS = 200


def excuse_text():
    """Hand back the excuse, but only if it obeys the brief: one
    line of plain text, no more than 200 characters, nothing blank."""
    line = EXCUSE
    if not line.strip():
        raise ValueError("excuse is blank")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse must stay on one line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "excuse runs %d characters, %d over the limit"
            % (len(line), len(line) - MAX_CHARS)
        )
    line.encode("utf-8")
    return line


def write_excuse(path):
    """Put the excuse on disk where the judge looks, by way of a
    temporary file and a rename, so no one ever reads half a line.
    Read it back and compare, letter for letter."""
    line = excuse_text()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    staging = path + ".staging"
    with open(staging, "w", encoding="utf-8") as out:
        out.write(line)
    os.replace(staging, path)
    with open(path, encoding="utf-8") as back:
        landed = back.read()
    if landed != line:
        raise ValueError("what landed is not the excuse")
    return line


def run():
    """Write the excuse and say how long it is."""
    line = write_excuse(ENTRY_OUTPUT)
    sys.stdout.write(
        "Wrote %d chars to %s\n" % (len(line), ENTRY_OUTPUT)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
