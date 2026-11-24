#!/usr/bin/env python3
"""Seventeen Syllables of Debugging - make.fun entry.

Writes one haiku about debugging (5-7-5, seventeen syllables) to
/output/entry.txt, the path the program/v1 harness grades, and prints it.
Standard library only; no network access; fully deterministic.
"""
from pathlib import Path

HAIKU = (
    "Breakpoint holds its breath\n"
    "the log swears it worked at noon\n"
    "no one touched a thing\n"
)

# Hand-counted syllables per line, checked at runtime: 5-7-5 = 17.
#   "Breakpoint(2) holds(1) its(1) breath(1)" = 5
#   "the(1) log(1) swears(1) it(1) worked(1) at(1) noon(1)" = 7
#   "no(1) one(1) touched(1) a(1) thing(1)" = 5
EXPECTED_SYLLABLES = (5, 7, 5)


def count_syllables(line: str) -> int:
    """Count syllables in one line with a small vowel-group heuristic.

    Good enough as a sanity check for this fixed text; the haiku itself
    was counted by hand and the expected counts above are authoritative.
    """
    vowels = "aeiouy"
    total = 0
    for word in line.lower().replace("-", " ").split():
        word = word.strip(".,;:!?\"'")
        if not word:
            continue
        # A final "-ed" after a consonant other than t/d is silent
        # ("worked" and "touched" are one syllable each), so drop its e
        # before counting vowel groups.
        if word.endswith("ed") and len(word) > 2 and word[-3] not in "td":
            word = word[:-2] + "d"
        groups = 0
        prev_vowel = False
        for ch in word:
            is_vowel = ch in vowels
            if is_vowel and not prev_vowel:
                groups += 1
            prev_vowel = is_vowel
        if word.endswith("e") and groups > 1:
            groups -= 1
        total += max(groups, 1)
    return total


def verify_haiku(text: str) -> None:
    """Refuse to write a haiku that is not three lines of 5-7-5."""
    lines = text.strip("\n").split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be 3 lines, got {len(lines)}")
    if len(text) > 200:
        raise ValueError(f"haiku must be at most 200 chars, got {len(text)}")
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        got = count_syllables(line)
        if got != expected:
            raise ValueError(
                f"line {line!r} has {got} syllables, expected {expected}"
            )


def main() -> None:
    verify_haiku(HAIKU)
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HAIKU, encoding="utf-8")
    print(HAIKU, end="")


if __name__ == "__main__":
    main()
