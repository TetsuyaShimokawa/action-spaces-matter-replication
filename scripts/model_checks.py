"""Supplementary numerical checks of the formulas behind the reported numbers.

These do not correspond to numbers printed in the manuscript; they verify, by
simulation or direct computation, the model equations used by the other scripts:
  * eq. (8): conditional mean and variance of the posterior draw;
  * eq. (13): linearity of the A4 benefit in the attention weights m;
  * Theorem 3.1: accuracy equals 1 - delta at K* (closed form and Monte Carlo);
  * Lemma A.1 / eq. (14): heterogeneous CDN reduces to Theorem 3.1 with common
    coefficients; KKT conditions of the Linear--Shannon allocation;
  * Proposition 3.4: inversion (26), derivative in (ii), Jacobian rank,
    and the cross-action restriction (28).
Monte Carlo checks use a fixed seed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdn import (accuracy_homogeneous, benefit_coefficients, cdn_closed_form,  # noqa: E402
                     cdn_heterogeneous, f_of, invert_K, ls_allocation, m_of)
from src.common import header  # noqa: E402

SEED = 20261031
NSIM = 2_000_000


def status(flag: bool) -> str:
    return "PASS" if flag else "FAIL"


def check_conditional_draw(rng, res):
    header("Eq. (8): posterior draw conditional on the true payoff")
    mu, om, u = 0.0, 0.3, 0.25
    for k in (0.2, 1.0, 2.5):
        m = m_of(k)
        signal = u + rng.standard_normal(NSIM) * om * np.sqrt(np.exp(-2 * k) / m)
        draw = mu + m * (signal - mu) + rng.standard_normal(NSIM) * om * np.exp(-k)
        mean_th, var_th = u + np.exp(-2 * k) * (mu - u), om ** 2 * f_of(k)
        ok = abs(draw.mean() - mean_th) < 1e-3 and abs(draw.var() / var_th - 1) < 5e-3
        res[f"check_eq8_k{k}"] = ok
        print(f"k={k}: mean {draw.mean():.5f} vs {mean_th:.5f}; "
              f"var {draw.var():.6f} vs {var_th:.6f}  {status(ok)}")


def check_linear_benefit(rng, res):
    header("Eq. (13): A4 benefit B(m) = B(0) + sum_a c_a m_a")
    mu, om = np.array([0.2, 0.0, -0.1]), np.array([0.3, 0.4, 0.3])
    c = benefit_coefficients(mu, om)
    V = mu + om * rng.standard_normal((NSIM, 3))
    B0 = mu[np.argmax(mu + om * rng.standard_normal((NSIM, 3)), axis=1)].mean()
    for i, mvec in enumerate((np.zeros(3), np.array([0.3, 0.7, 0.5]), np.array([0.9, 0.2, 0.6]))):
        Vt = mu + mvec * (V - mu) + np.sqrt(1 - mvec ** 2) * om * rng.standard_normal((NSIM, 3))
        B = V[np.arange(NSIM), np.argmax(Vt, axis=1)].mean()
        ok = abs(B - (B0 + c @ mvec)) < 3e-3
        res[f"check_eq13_case{i}"] = ok
        print(f"m={mvec}: simulated {B:.4f}, B(0)+c.m = {B0 + c @ mvec:.4f}  {status(ok)}")


def check_theorem31(rng, res):
    header("Theorem 3.1: pairwise accuracy equals 1 - delta at K*")
    for n, D in ((2, 0.05), (2, 0.4), (5, 0.2), (8, 0.125)):
        K = cdn_closed_form(n, D, 0.3, 0.1)
        acc = accuracy_homogeneous(K, n, D, 0.3)
        ok = abs(acc - 0.9) < 1e-12
        res[f"check_thm31_n{n}_D{D}"] = ok
        print(f"n={n} Delta={D}: K*={K:.4f}, accuracy {acc:.10f}  {status(ok)}")
    n, D, om = 3, 0.2, 0.3
    K = cdn_closed_form(n, D, om, 0.1)
    k = K / n
    u = np.array([D, 0.0, 0.0])
    draws = u + np.exp(-2 * k) * (0.0 - u) + om * np.sqrt(f_of(k)) * rng.standard_normal((NSIM, n))
    acc = (draws[:, 0] >= draws[:, 1]).mean()
    ok = abs(acc - 0.9) < 2e-3
    res["check_thm31_mc"] = ok
    print(f"Monte Carlo pairwise accuracy at K* (n=3, Delta=0.2): {acc:.4f}  {status(ok)}")


def check_lemma_a1(res):
    header("Lemma A.1 and eq. (14): heterogeneous CDN and Linear--Shannon allocation")
    for n, D in ((2, 0.05), (4, 0.25), (6, 1 / 6)):
        u = np.array([D] + [0.0] * (n - 1))
        K, _ = cdn_heterogeneous(np.ones(n), u, np.full(n, u.mean()), np.full(n, 0.3), 0)
        Kc = cdn_closed_form(n, D, 0.3, 0.1)
        ok = abs(K - Kc) < 1e-8
        res[f"check_lemmaA1_n{n}"] = ok
        print(f"common c, n={n}: Lemma A.1 {K:.6f} vs Theorem 3.1 {Kc:.6f}  {status(ok)}")
    c = np.array([2.0, 1.0, 0.5, 0.1])
    for K in (0.1, 0.5, 2.0):
        k, t = ls_allocation(c, K)
        act = k > 0
        ok = (np.allclose(c[act] * np.exp(-2 * k[act]), t) and np.all(c[~act] <= t + 1e-12)
              and abs(k.sum() - K) < 1e-12)
        res[f"check_kkt_K{K}"] = ok
        print(f"K={K}: k={np.round(k, 4)}, sum={k.sum():.4f}, KKT  {status(ok)}")
    k, _ = ls_allocation(c, 3.0)
    ok = abs((k[0] - k[1]) - 0.5 * np.log(c[0] / c[1])) < 1e-12
    res["check_eq28"] = ok
    print(f"Prop. 3.4(iii), eq. (28): k_a - k_b = 0.5 log(c_a/c_b)  {status(ok)}")


def check_identification(res):
    header("Proposition 3.4: identification")
    om, D = 0.3, 0.2
    for n, K in ((2, 1.0), (4, 3.0), (6, 7.5)):
        sig = accuracy_homogeneous(K, n, D, om)
        Kinv = invert_K(sig, n, D, om)
        ok = abs(Kinv - K) < 1e-8
        res[f"check_eq26_n{n}"] = ok
        print(f"(i) n={n} K={K}: sigma={sig:.6f}, inverted K={Kinv:.8f}  {status(ok)}")
    K, h = 3.0, 1e-6
    rows = []
    for n in (2, 5):
        g = lambda KK, n=n: np.log(m_of(KK / n)) - 0.5 * np.log(2 * f_of(KK / n))  # noqa: E731
        num = (g(K + h) - g(K - h)) / (2 * h)
        m = m_of(K / n)
        th = 2 / (n * m * (1 + m))
        ok = abs(num - th) < 1e-6
        res[f"check_prop34ii_n{n}"] = ok
        rows.append([th, -1.0])
        print(f"(ii) n={n}: dRHS/dK numeric {num:.6f} vs 2/[n m (1+m)] {th:.6f}  {status(ok)}")
    rank = np.linalg.matrix_rank(np.array(rows))
    res["check_prop34ii_rank"] = rank == 2
    print(f"(ii) Jacobian rank with n in {{2, 5}}: {rank}  {status(rank == 2)}")


def check_excl_mc(rng, res):
    header("Section 5.2: Monte Carlo check of Delta_excl(N) = 1/(6 N^2)")
    v = rng.random((NSIM, 2))
    for N in range(2, 7):
        cell = np.floor(v * N)
        sim = np.where(cell[:, 0] == cell[:, 1], 0.5 * np.abs(v[:, 0] - v[:, 1]), 0.0).mean()
        ok = abs(sim * 6 * N * N - 1) < 0.01
        res[f"check_excl_mc_N{N}"] = ok
        print(f"N={N}: simulated {sim:.5f} vs {1 / (6 * N * N):.5f}  {status(ok)}")


def run() -> dict:
    rng = np.random.default_rng(SEED)
    res: dict = {}
    check_conditional_draw(rng, res)
    check_linear_benefit(rng, res)
    check_theorem31(rng, res)
    check_lemma_a1(res)
    check_identification(res)
    check_excl_mc(rng, res)
    return res


if __name__ == "__main__":
    run()
