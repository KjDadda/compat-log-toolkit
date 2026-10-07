#!/usr/bin/env python3
"""logsum - summarize a noisy runtime log.

Groups log lines into templates (hex addresses, numbers, paths, timestamps and
quoted strings are collapsed into placeholders), then reports the most frequent
ones. The point is to find the five lines that actually matter in a fifty
thousand line Windows-on-console compatibility log.

Usage:
    logsum.py LOG [LOG ...]          top templates (default 15)
    logsum.py --top 30 LOG           show more rows
    logsum.py --errors LOG           only error-ish lines
    logsum.py --timeline LOG         first/last timestamps + session markers
    cat LOG | logsum.py -            read stdin

Exit codes: 0 ok, 1 no input, 2 bad usage.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

# Order matters: timestamps before numbers, paths before numbers.
RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?"), "<TS>"),
    (re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"), "<UUID>"),
    (re.compile(r"\b0x[0-9a-fA-F]+\b"), "<HEX>"),
    (re.compile(r"[/\\](?:[\w.-]+[/\\])+[\w.-]+"), "<PATH>"),
    (re.compile(r'"[^"]{0,200}"'), "<STR>"),
    (re.compile(r"\b\d+(?:\.\d+)?\b"), "<N>"),
    (re.compile(r"\s+"), " "),
]

ERRORISH = re.compile(
    r"error|fail|fault|exception|crash|denied|timeout|timed out|unable|invalid|"
    r"cannot|can't|refused|abort|unhandled|not found|no such",
    re.IGNORECASE,
)

SESSIONISH = re.compile(r"session|pid=|started|exited|shutdown|WINESERVER", re.IGNORECASE)


def template(line: str) -> str:
    out = line
    for pattern, replacement in RULES:
        out = pattern.sub(replacement, out)
    return out.strip()


def read_lines(paths: list[str]) -> list[str]:
    lines: list[str] = []
    for path in paths:
        if path == "-":
            lines.extend(sys.stdin.read().splitlines())
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                lines.extend(handle.read().splitlines())
        except OSError as exc:
            print(f"logsum: {path}: {exc}", file=sys.stderr)
    return [line for line in lines if line.strip()]


def cmd_templates(lines: list[str], top: int, errors_only: bool) -> int:
    selected = [line for line in lines if ERRORISH.search(line)] if errors_only else lines
    if not selected:
        print("logsum: nothing matched", file=sys.stderr)
        return 1
    counts = Counter(template(line) for line in selected)
    examples: dict[str, str] = {}
    for line in selected:
        examples.setdefault(template(line), line.strip())
    width = len(str(counts.most_common(1)[0][1]))
    print(f"{len(selected)} lines -> {len(counts)} templates"
          f"{' (error-ish only)' if errors_only else ''}\n")
    for rank, (tmpl, count) in enumerate(counts.most_common(top), 1):
        print(f"{count:>{width}}x  {tmpl[:150]}")
        example = examples[tmpl]
        if example != tmpl and len(example) < 400:
            print(f"{'':>{width}}   e.g. {example[:150]}")
    return 0


def cmd_timeline(lines: list[str]) -> int:
    stamps = [m.group(0) for line in lines
              for m in [re.search(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}", line)] if m]
    if stamps:
        print(f"first: {stamps[0]}\nlast:  {stamps[-1]}\n")
    else:
        print("no timestamps found\n")
    markers = [(i, line.strip()) for i, line in enumerate(lines) if SESSIONISH.search(line)]
    print(f"{len(markers)} session-ish lines:")
    seen: Counter[str] = Counter()
    for _, line in markers:
        seen[template(line)] += 1
    for tmpl, count in seen.most_common(10):
        print(f"  {count:>4}x  {tmpl[:150]}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Summarize a noisy runtime log.")
    parser.add_argument("logs", nargs="+", help="log file(s), or - for stdin")
    parser.add_argument("--top", type=int, default=15, help="rows to show (default 15)")
    parser.add_argument("--errors", action="store_true", help="only error-ish lines")
    parser.add_argument("--timeline", action="store_true", help="first/last stamps + session markers")
    args = parser.parse_args(argv)

    lines = read_lines(args.logs)
    if not lines:
        print("logsum: no input", file=sys.stderr)
        return 1
    if args.timeline:
        return cmd_timeline(lines)
    return cmd_templates(lines, args.top, args.errors)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
