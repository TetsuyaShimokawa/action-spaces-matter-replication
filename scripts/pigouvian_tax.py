"""Appendix B.1: numerical example for Proposition B.1 (Pigouvian tax with a
reliability constraint): tau*(kappa) = eta + omega_eta Phi^{-1}(1 - delta) exp(-kappa)
with eta = 1, omega_eta = 0.2, delta = 0.1.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.common import header, write_csv  # noqa: E402

ETA, OMEGA_ETA, DELTA = 1.0, 0.2, 0.1


def run() -> dict:
    header("Appendix B.1: Pigouvian tax tau*(kappa), eta=1, omega_eta=0.2, delta=0.1")
    z = norm.ppf(1 - DELTA)
    res, rows = {}, []
    for kappa in (1, 2, 3):
        tau = ETA + OMEGA_ETA * z * math.exp(-kappa)
        res[f"pigou_tau_{kappa}"] = tau
        rows.append({"kappa": kappa, "tau_star": f"{tau:.6f}"})
        print(f"kappa = {kappa}: tau* = {tau:.4f}")
    write_csv("appendixB_pigouvian_tax.csv", ["kappa", "tau_star"], rows)
    return res


if __name__ == "__main__":
    run()
