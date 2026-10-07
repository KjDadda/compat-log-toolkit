#!/usr/bin/env python3
"""Write a synthetic Windows-on-console style log, so logsum.py can be smoke-tested
without shipping anyone's real run output.

    python3 tests/make_sample_log.py > /tmp/sample.log
    ./tools/logsum.py /tmp/sample.log
"""
import random
import sys

random.seed(7)
out = []


def ts(sec: int) -> str:
    return f"2026-10-01T00:00:{sec:02d}"


for sec in range(0, 5):
    out.append(f"{ts(sec)} session started pid={100 + sec} app_id=0x00006018")
for _ in range(3):
    out.append("WINESERVER: starting wineserver as pid 214")
for _ in range(400):
    out.append(f"err:module:import_dll Library example-runtime-1-0.dll ({hex(random.getrandbits(32))}) not found")
for _ in range(120):
    out.append(f"warn:seh:dispatch_exception code={hex(random.getrandbits(32))} flags=0x0 addr={hex(random.getrandbits(48))}")
for i in range(30):
    out.append(f"{ts(4)} fault_top pc=0x1413adfee count={i}")
for i in range(10):
    out.append(f"{ts(4)} frames_put={i} shown=0 vk_shown=3 audio={21000 + i}")
out.append(f"{ts(4)} session exited pid=100 code=0x00000000")

sys.stdout.write("\n".join(out) + "\n")
