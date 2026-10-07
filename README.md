# compat-log-toolkit

Tools for capturing and summarizing Windows-on-console runtime logs, plus the
report template we use when a title's compatibility is evaluated.

Part of [CommonFrame Labs](https://commonframelabs.stream) — independent
compatibility research.

## Why

A compatibility run produces a lot of output. The failure is usually in there, but
it's buried under tens of thousands of lines of the same repeating noise. Reading
it top to bottom doesn't scale and doesn't reproduce; summarizing it does.

## logsum

`tools/logsum.py` collapses log lines into templates — timestamps, hex addresses,
numbers, paths and quoted strings become placeholders — then ranks them by
frequency. Two runs of the same failure produce the same template, which makes
"did my change actually fix it?" a one-line diff instead of a judgement call.

```console
$ ./tools/logsum.py run.log --top 10
24810 lines -> 312 templates

  8412x  err:module:import_dll Library <STR> (<HEX>) not found
  3907x  warn:seh:dispatch_exception code=<HEX> flags=<HEX> addr=<HEX>
   612x  <TS> fault_top pc=<HEX> count=<N>
   118x  <TS> frame_put=<N> shown=<N> vk_shown=<N> audio=<N>
     14x  <TS> session started pid=<N>
```

Error-ish lines only, when the signal is drowned out:

```console
$ ./tools/logsum.py --errors run.log
```

First/last timestamps and session markers — useful for "it died eight seconds in":

```console
$ ./tools/logsum.py --timeline run.log
first: 2026-10-07T09:43:44
last:  2026-10-07T09:43:52

412 session-ish lines:
   24x  WINESERVER ...
    2x  <TS> session started pid=<N>
```

Stdin works too (`cat run.log | ./tools/logsum.py -`), so it drops into a pipeline
that's already capturing output.

No dependencies beyond Python 3.8+.

## templates/compat-report.md

The format we use to record a single title's result: environment, what was tested,
what happened, what the log actually showed, and the current status. Copy it, fill
it in, keep it — the value of compatibility work is in the record, not the anecdote.

## Status

Early and small. This is the tooling side of the research described on our site,
published because "we test things carefully" is worth nothing if nobody can see how.

## License

MIT — see [LICENSE](LICENSE).
