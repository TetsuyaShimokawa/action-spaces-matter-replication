"""Table 1 and Section 3.2: quantiles G^{-1}(0.9) of location-scale shapes.

Also computes the probit-to-logit shift of the per-comparison threshold,
log(G_logit^{-1}(0.9) / Phi^{-1}(0.9)), quoted in Section 3.2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import cauchy, logistic, norm, t as student_t, uniform

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.common import header, write_csv  # noqa: E402

Q = 0.9  # 1 - delta with delta = 0.1

SHAPES = [
    ("table1_normal", "Standard normal Phi (quasilinear / Gaussian common value)", norm()),
    ("table1_logistic", "Standard logistic", logistic()),
    ("table1_t3", "Student t with 3 degrees of freedom", student_t(3)),
    ("table1_cauchy", "Standard Cauchy", cauchy()),
    ("table1_uniform", "Uniform on [-1, 1]", uniform(loc=-1.0, scale=2.0)),
    ("table1_large_market", "Large market: limiting normal (CLT)", norm()),
]


def run() -> dict:
    header("Table 1 (Section 3.2): G^{-1}(0.9) for location-scale shapes, delta = 0.1")
    res, rows = {}, []
    for key, label, dist in SHAPES:
        q = float(dist.ppf(Q))
        res[key] = q
        rows.append({"shape": label, "G_inv_0.9": f"{q:.6f}"})
        print(f"{label:58s} {q:8.4f}")
    shift = float(np.log(logistic().ppf(Q) / norm().ppf(Q)))
    res["sec32_probit_logit_shift"] = shift
    print(f"Probit-to-logit threshold shift log(G_logit^-1(0.9)/Phi^-1(0.9)) = {shift:.4f} nats")
    write_csv("table1_location_scale.csv", ["shape", "G_inv_0.9"], rows)
    return res


if __name__ == "__main__":
    run()
