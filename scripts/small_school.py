"""Section 7.2 and Table 2: small-school-bias illustration.

Four students rank S > L > O. Capacities: S = 1, L = 3, O unlimited (outside
option). Focal student's utilities: u(S) = 1.0, u(L) = 0.8, u(O) = 0.6.
Under a common random priority order, student-proposing DA coincides with
serial dictatorship, so all 4! = 24 priority orders are enumerated exactly.

For each local deviation (swap S and L, or swap L and O) the script computes
  p = probability that the swap changes the focal student's assignment,
  g = conditional utility loss when it does,
  Delta = p * g,
  K_rep = Theorem 3.1 with |S| = 2, omega = 0.3, delta = 0.1.
"""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdn import cdn_closed_form  # noqa: E402
from src.common import header, write_csv  # noqa: E402

STUDENTS = (0, 1, 2, 3)
FOCAL = 0
CAPACITY = {"S": 1, "L": 3, "O": len(STUDENTS)}
UTILITY = {"S": Fraction(10, 10), "L": Fraction(8, 10), "O": Fraction(6, 10)}
TRUTH = ("S", "L", "O")
OMEGA, DELTA = 0.3, 0.1


def serial_dictatorship(priority, prefs):
    seats = dict(CAPACITY)
    out = {}
    for s in priority:
        for school in prefs[s]:
            if seats[school] > 0:
                seats[school] -= 1
                out[s] = school
                break
    return out


def local_gap(deviation):
    orders = list(itertools.permutations(STUDENTS))
    changed, loss = 0, Fraction(0)
    for order in orders:
        truthful = {s: TRUTH for s in STUDENTS}
        a = serial_dictatorship(order, truthful)[FOCAL]
        dev = dict(truthful)
        dev[FOCAL] = deviation
        b = serial_dictatorship(order, dev)[FOCAL]
        if a != b:
            changed += 1
            loss += UTILITY[a] - UTILITY[b]
    p = Fraction(changed, len(orders))
    g = loss / changed if changed else Fraction(0)
    return p, g, p * g


def run() -> dict:
    header("Section 7.2 / Table 2: small-school bias (exact enumeration of 4! orders)")
    cases = [("S", "Small S vs. Large L", ("L", "S", "O")),
             ("L", "Large L vs. Outside O", ("S", "O", "L"))]
    res, rows = {}, []
    for tag, label, dev in cases:
        p, g, gap = local_gap(dev)
        K = cdn_closed_form(2, float(gap), OMEGA, DELTA)
        res.update({f"ss_p_{tag}": float(p), f"ss_g_{tag}": float(g),
                    f"ss_Delta_{tag}": float(gap), f"ss_Krep_{tag}": K})
        rows.append({"comparison": label, "p": str(p), "g": f"{float(g):.6f}",
                     "Delta": f"{float(gap):.6f}", "K_rep": f"{K:.6f}"})
        print(f"{label:24s} p = {str(p):4s} g = {float(g):.2f}  Delta = {float(gap):.2f}  K_rep = {K:.4f}")
    res["ss_Krep_diff"] = res["ss_Krep_S"] - res["ss_Krep_L"]
    print(f"K_rep(S) - K_rep(L) = {res['ss_Krep_diff']:.4f}")
    write_csv("table2_small_school.csv", ["comparison", "p", "g", "Delta", "K_rep"], rows)
    return res


if __name__ == "__main__":
    run()
