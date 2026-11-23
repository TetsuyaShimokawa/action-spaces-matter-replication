"""Section 7.2: two-action DA versus RSD illustration.

u(A) = 1, u(B) = beta = 0.6, omega = 0.3, delta = 0.1.
Delta_DA = 1 - beta = 0.4; Delta_RSD = (1 - beta) / 2 = 0.2 (the report matters
in half of the states). K* from Theorem 3.1 with |S| = 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdn import cdn_closed_form  # noqa: E402
from src.common import header, write_csv  # noqa: E402

BETA, OMEGA, DELTA = 0.6, 0.3, 0.1


def run() -> dict:
    header("Section 7.2: DA vs. RSD two-action example (beta=0.6, omega=0.3, delta=0.1)")
    d_da, d_rsd = 1 - BETA, (1 - BETA) / 2
    k_da = cdn_closed_form(2, d_da, OMEGA, DELTA)
    k_rsd = cdn_closed_form(2, d_rsd, OMEGA, DELTA)
    print(f"Delta_DA = {d_da:.2f}  K*_DA  = {k_da:.4f}")
    print(f"Delta_RSD = {d_rsd:.2f} K*_RSD = {k_rsd:.4f}")
    print(f"K*_RSD - K*_DA = {k_rsd - k_da:.4f}")
    write_csv("da_rsd_example.csv", ["mechanism", "Delta", "K_star"],
              [{"mechanism": "DA", "Delta": f"{d_da:.6f}", "K_star": f"{k_da:.6f}"},
               {"mechanism": "RSD", "Delta": f"{d_rsd:.6f}", "K_star": f"{k_rsd:.6f}"}])
    return {"darsd_Delta_DA": d_da, "darsd_Delta_RSD": d_rsd,
            "darsd_K_DA": k_da, "darsd_K_RSD": k_rsd, "darsd_diff": k_rsd - k_da}


if __name__ == "__main__":
    run()
