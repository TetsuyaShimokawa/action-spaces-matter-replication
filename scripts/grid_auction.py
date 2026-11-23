"""Section 5.2: grid-auction numerical example (unnumbered table).

Parameters: bbar = 1, delta = 0.1, omega = 0.3, target capacity Kbar = 2,
representative gap Delta = eps = 1/N, comprehension-loss scale vbar = 0.06.

Columns of the manuscript table:
  K_hom(N)   = Theorem 3.1 with n = N, Delta = 1/N
  accuracy   = Phi(N^{-1} m(Kbar/N) / (omega sqrt(2 f(Kbar/N))))   (eq. 25)
  Delta_excl = 1/(6 N^2)
  T          = vbar (1 - accuracy)  (representative local loss)

Also reported:
  * the additive loss convention (N - 1) T mentioned in the text;
  * an exact numerical check of Delta_excl(N) = 1/(6 N^2) for two i.i.d. U[0,1]
    values (loss |v1 - v2|/2 when both values fall in the same cell and the
    object is assigned by a fair tie-break);
  * sensitivity of the CDN to heterogeneous benefit coefficients
    c_target / c_alt in {1/2, 1, 2} via Lemma A.1 (ratio 1 reproduces K_hom).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdn import accuracy_homogeneous, cdn_closed_form, cdn_heterogeneous  # noqa: E402
from src.common import header, write_csv  # noqa: E402

DELTA, OMEGA, KBAR, VBAR = 0.1, 0.3, 2.0, 0.06
NS = range(2, 7)          # tabulated range in the manuscript
RATIOS = (0.5, 1.0, 2.0)  # c_target / c_alt for the sensitivity block


def excl_exact(N: int) -> float:
    """E[ |v1 - v2| / 2 ; v1, v2 in the same cell ] for v1, v2 ~ i.i.d. U[0,1]."""
    eps = 1.0 / N
    # By symmetry, integrate over y < x within one cell and double it.
    half, _ = dblquad(lambda y, x: 0.5 * (x - y), 0.0, eps, 0.0, lambda x: x,
                      epsabs=1e-14, epsrel=1e-12)
    return N * 2.0 * half


def hetero_K(N: int, ratio: float):
    """N bids, target is index 0 with gap 1/N to every alternative; common prior
    mean equal to the average true payoff; c = (ratio, 1, ..., 1)."""
    u = np.array([1.0 / N] + [0.0] * (N - 1))
    mu = np.full(N, u.mean())
    om = np.full(N, OMEGA)
    c = np.array([ratio] + [1.0] * (N - 1))
    return cdn_heterogeneous(c, u, mu, om, target=0, delta=DELTA)


def run() -> dict:
    header("Section 5.2: grid auction (delta=0.1, omega=0.3, Kbar=2, vbar=0.06)")
    print(f"{'N':>2} {'eps':>6} {'K_hom':>7} {'accuracy':>9} {'D_excl':>8} {'T':>7} "
          f"{'D_excl+T':>9} {'(N-1)T':>7} {'D_excl+(N-1)T':>14}")
    res, rows = {}, []
    for N in NS:
        Kh = cdn_closed_form(N, 1.0 / N, OMEGA, DELTA)
        acc = accuracy_homogeneous(KBAR, N, 1.0 / N, OMEGA)
        dex = 1.0 / (6 * N ** 2)
        T = VBAR * (1.0 - acc)
        Tadd = (N - 1) * T
        res.update({f"grid_N{N}_eps": 1.0 / N, f"grid_N{N}_Khom": Kh, f"grid_N{N}_acc": acc,
                    f"grid_N{N}_excl": dex, f"grid_N{N}_T": T, f"grid_N{N}_sum": dex + T})
        rows.append(dict(N=N, eps=1.0 / N, K_hom=Kh, accuracy=acc, Delta_excl=dex,
                         T_local=T, excl_plus_T_local=dex + T,
                         T_additive=Tadd, excl_plus_T_additive=dex + Tadd))
        print(f"{N:>2} {1 / N:6.3f} {Kh:7.3f} {acc:9.3f} {dex:8.4f} {T:7.4f} "
              f"{dex + T:9.6f} {Tadd:7.4f} {dex + Tadd:14.6f}")

    n_local = min(rows, key=lambda r: r["excl_plus_T_local"])["N"]
    n_add = min(rows, key=lambda r: r["excl_plus_T_additive"])["N"]
    feasible = [r["N"] for r in rows if r["K_hom"] <= KBAR]
    n_feas = max(feasible)
    res.update({"grid_opt_local": n_local, "grid_N2_feasible": float(2 in feasible),
                "grid_N3_feasible": float(3 in feasible), "grid_finest_feasible": n_feas,
                # Proposition 5.1: eps** = max(eps_W*, eps_K*)
                "grid_eps_starstar": max(1.0 / n_local, 1.0 / n_feas)})
    print("-" * 78)
    print(f"unconstrained optimum, local loss T        : N = {n_local}")
    print(f"unconstrained optimum, additive (N-1)T     : N = {n_add}")
    print(f"feasible grids with K_hom <= Kbar = 2      : N in {feasible}")
    print(f"finest feasible grid N = {n_feas}, eps_K* = 1/{n_feas}; "
          f"constrained solution eps** = {res['grid_eps_starstar']:.3f}")

    print("\nExact check of Delta_excl(N) = 1/(6 N^2):")
    for N in NS:
        ex = excl_exact(N)
        res[f"check_excl_N{N}"] = abs(ex - 1.0 / (6 * N ** 2)) < 1e-10
        print(f"  N={N}: integral {ex:.8f}  formula {1 / (6 * N ** 2):.8f}")

    print("\nSensitivity: CDN with heterogeneous benefit coefficients (Lemma A.1)")
    print(f"{'N':>2}" + "".join(f"{'ratio=' + format(r, 'g'):>12}" for r in RATIOS) + f"{'K_hom':>9}")
    sens_rows = []
    for r in rows:
        N = r["N"]
        vals = []
        for ratio in RATIOS:
            K, upper = hetero_K(N, ratio)
            if not upper:
                print(f"  warning: accuracy set is not an upper set (N={N}, ratio={ratio:g})")
            vals.append(K)
        res[f"check_hetero_ratio1_N{N}"] = abs(vals[1] - r["K_hom"]) < 1e-8
        sens_rows.append({"N": N, **{f"K_ratio_{x:g}": f"{v:.6f}" for x, v in zip(RATIOS, vals)},
                          "K_hom": f"{r['K_hom']:.6f}"})
        print(f"{N:>2}" + "".join(f"{v:12.3f}" for v in vals) + f"{r['K_hom']:9.3f}")
    res["grid_sens_N2_feasible_all"] = float(all(float(sens_rows[0][f"K_ratio_{x:g}"]) <= KBAR for x in RATIOS))
    res["grid_sens_N3_infeasible_all"] = float(all(float(sens_rows[1][f"K_ratio_{x:g}"]) > KBAR for x in RATIOS))

    fmt = lambda d: {k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in d.items()}  # noqa: E731
    write_csv("table_grid_auction.csv", list(rows[0].keys()), [fmt(r) for r in rows])
    write_csv("table_grid_auction_heterogeneity.csv", list(sens_rows[0].keys()), sens_rows)
    return res


if __name__ == "__main__":
    run()
