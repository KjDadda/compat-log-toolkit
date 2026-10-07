# Compatibility report — <TITLE / IDENTIFIER>

Copy this file to `reports/<YYYY-MM-DD>-<short-name>.md` and fill it in. Write it
while the run is fresh, and never delete a failure — a documented failure is the
whole point.

---

- **Date tested:**
- **Status:** not working / boots but unusable / playable / verified working
- **Confidence:** single run / repeated (>3 runs, same result) / confirmed by another person

## Environment

- **Runtime / runtime version:**
- **Prefix type and location:** (internal storage vs external — note which, and why)
- **Title / build identifier:**
- **Runtime patches applied:** (none, or list each one and what it changes)
- **Host and storage:** (what the title is read from)

## Test

What was done, in order, so someone else can repeat it:

1.
2.
3.

## Result

What happened, as observed. Time from launch to failure, what was on screen, whether
audio played, whether it exited cleanly.

## What the log showed

Summarize with `tools/logsum.py` rather than pasting thousands of lines:

```console
$ ./tools/logsum.py run.log --errors --top 10
```

Paste the ranked output here, plus the single line that best explains the failure
and how to read it.

## Interpretation

Your best current explanation — and say plainly what you have *not* verified. Mark
guesses as guesses.

## Next step

The smallest experiment that would discriminate between the remaining explanations,
and what result would mean what.
