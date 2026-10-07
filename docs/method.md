# Method

How a capability is evaluated in this project. The point isn't ceremony — it's that
a result nobody can reproduce isn't a result.

## 1. One variable at a time

Change one thing per run (a runtime patch, a DLL, a config value, a network target).
If two things change and the outcome changes, you've learned nothing about which one
mattered — and if you're later tempted to keep both, you're carrying a fix you don't
understand.

## 2. Reproduce before diagnosing

A failure that happens once might be timing, caching, or a stray state file. Run it
again before explaining it. `fault_top pc=… count=0` over eleven minutes and the same
line with `count=1` followed by a crash are different results, and the difference
between them is the finding.

## 3. Summarize, don't read

Full logs go to `logsum.py`. A run that produces 50,000 lines has maybe five that
carry information; the template ranking is what makes them visible, and comparing
rankings between two runs is what makes "did it change?" objective.

## 4. Separate what was observed from what was inferred

Reports have two sections for this. "The client sent 456 bytes and the bridge journal
shows no request" is an observation. "The client rejects the reply" is an inference
and belongs in the interpretation section, marked as one.

Correcting an inference is normal and gets recorded, not quietly edited out. A wrong
hypothesis that was written down and then disproved is a useful artefact; a wrong
hypothesis that was never written down is a bug you'll re-ship.

## 5. Record the negative results

A title that doesn't work is as valuable as one that does — more, when the failure
mode is consistent, because now it's a test case. Nothing gets deleted for being a
failure.

## 6. Say what hasn't been tested

"Playable" with no qualification invites people to assume online, saves, and every
mode work. State the surface that was actually exercised, and the one that wasn't.
