"""Single entry point: reproduces every computed number in the manuscript.

Usage:  python run_all.py

Runs the scripts in scripts/ in order, writes CSV files and the console log to
output/, and compares every reproduced number with the value printed in the
manuscript (src/manuscript_values.py). The comparison is written to
output/verification.csv. The exit status is 0 if all numbers match and all
supplementary checks pass, and 1 otherwise.
"""
from __future__ import annotations

import csv
import importlib.util
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
sys.path.insert(0, str(ROOT))

from src.manuscript_values import VALUES  # noqa: E402

SCRIPTS = [
    "scripts/table1_location_scale.py",
    "scripts/grid_auction.py",
    "scripts/small_school.py",
    "scripts/da_rsd.py",
    "scripts/pigouvian_tax.py",
    "scripts/model_checks.py",
]


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for s in self.streams:
            s.write(text)
        return len(text)

    def flush(self):
        for s in self.streams:
            s.flush()


def load(rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def compare(value, reported: str):
    """Return (reproduced value formatted as in the manuscript, match flag)."""
    if reported in ("yes", "no"):
        shown = "yes" if value else "no"
        return shown, shown == reported
    if "/" in reported:
        target = Fraction(reported)
        frac = Fraction(value).limit_denominator(1000)
        return f"{value:.6f} (= {frac})", abs(value - float(target)) < 1e-12
    if "." not in reported:
        return str(int(value)), int(value) == int(reported)
    decimals = len(reported.split(".")[1])
    shown = f"{value:.{decimals}f}"
    return shown, shown == reported


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    log = open(OUTPUT / "run_all.log", "w", encoding="utf-8")
    stdout = sys.stdout
    sys.stdout = Tee(stdout, log)
    try:
        t0 = time.perf_counter()
        print("Replication package: Action Spaces Matter: Choice, Equilibrium, and")
        print("Mechanism Design under Cognitive Constraints")
        print(f"Python {platform.python_version()} on {platform.system()} {platform.release()}")
        import numpy, scipy  # noqa: E401
        print(f"numpy {numpy.__version__}, scipy {scipy.__version__}")
        print("Started", time.strftime("%Y-%m-%d %H:%M:%S"))

        results: dict = {}
        for rel in SCRIPTS:
            print()
            t = time.perf_counter()
            results.update(load(rel).run())
            print(f"[{rel} finished in {time.perf_counter() - t:.1f} s]")

        print()
        print("=" * 78)
        print("Comparison with the numbers printed in the manuscript")
        print("=" * 78)
        rows, n_bad = [], 0
        for key, loc, desc, reported in VALUES:
            shown, ok = compare(results[key], reported)
            n_bad += not ok
            rows.append({"location": loc, "quantity": desc, "manuscript": reported,
                         "reproduced": shown, "match": "yes" if ok else "NO"})
            print(f"{'ok ' if ok else 'XX '} {loc:34s} {desc:46s} {reported:>8s} {shown:>10s}")
        with open(OUTPUT / "verification.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print("written: output/verification.csv")

        checks = {k: v for k, v in results.items() if k.startswith("check_")}
        failed = [k for k, v in checks.items() if not v]
        print()
        print(f"Manuscript numbers: {len(VALUES) - n_bad} of {len(VALUES)} reproduced")
        print(f"Supplementary checks: {len(checks) - len(failed)} of {len(checks)} passed"
              + (f" (failed: {', '.join(failed)})" if failed else ""))
        print(f"Total running time: {time.perf_counter() - t0:.1f} s")
        return 0 if (n_bad == 0 and not failed) else 1
    finally:
        sys.stdout = stdout
        log.close()


if __name__ == "__main__":
    sys.exit(main())
