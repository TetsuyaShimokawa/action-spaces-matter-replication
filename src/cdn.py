"""Cognitive difficulty number (CDN) in the Gaussian--Shannon posterior-draw model.

Notation follows the manuscript. k_a is the cognitive resource allocated to
action a, m(k) = 1 - exp(-2k) is the attention weight (eq. 11) and
f(k) = 2 exp(-2k) - exp(-4k) = 1 - m(k)^2. Conditional on the true payoff u_a,
the posterior draw is N(u_a + exp(-2k_a)(mu_a - u_a), omega_a^2 f(k_a)) (eq. 8).
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm


def m_of(k):
    """Attention weight m(k) = 1 - exp(-2k), eq. (11)."""
    return 1.0 - np.exp(-2.0 * np.asarray(k, dtype=float))


def f_of(k):
    """Variance factor f(k) = 2 exp(-2k) - exp(-4k) = 1 - m(k)^2, eq. (8)."""
    return 1.0 - m_of(k) ** 2


def cdn_closed_form(n, Delta, omega, delta=0.1):
    """Theorem 3.1, eqs. (1)/(21): K* for |S| = n, minimum gap Delta, prior scale omega."""
    z = norm.ppf(1.0 - delta)
    r = np.sqrt(2.0) * omega * z / np.sqrt(Delta ** 2 + 2.0 * omega ** 2 * z ** 2)
    return float(-0.5 * n * np.log(1.0 - r))


def accuracy_homogeneous(K, n, Delta, omega):
    """Eq. (25): pairwise accuracy under the uniform split K/n."""
    k = K / n
    return float(norm.cdf(Delta * m_of(k) / (omega * np.sqrt(2.0 * f_of(k)))))


def invert_K(sigma, n, Delta, omega):
    """Proposition 3.4(i), eq. (26): recover K from pairwise accuracy sigma in (1/2, 1)."""
    z = norm.ppf(sigma)
    r = np.sqrt(2.0) * omega * z / np.sqrt(Delta ** 2 + 2.0 * omega ** 2 * z ** 2)
    return float(-0.5 * n * np.log(1.0 - r))


def benefit_coefficients(mu, omega):
    """Eq. (13): c_a = E[(V_a - mu_a) 1{V_a = max_b V_b}] for independent N(mu_a, omega_a^2)."""
    mu = np.asarray(mu, dtype=float)
    omega = np.asarray(omega, dtype=float)
    c = np.empty(len(mu))
    for a in range(len(mu)):
        others = [b for b in range(len(mu)) if b != a]

        def integrand(x, a=a, others=others):
            p = np.prod([norm.cdf((x - mu[b]) / omega[b]) for b in others])
            return (x - mu[a]) * norm.pdf(x, mu[a], omega[a]) * p

        lo, hi = mu[a] - 10 * omega[a], mu[a] + 10 * omega[a]
        c[a] = quad(integrand, lo, hi, limit=200)[0]
    return c


def ls_allocation(c, K):
    """Eq. (14): k_a = [0.5 log(c_a / t)]_+ with sum_a k_a = K. Returns (k, t)."""
    c = np.asarray(c, dtype=float)
    if K <= 0:
        return np.zeros_like(c), float(np.max(c))
    order = np.sort(c)[::-1]
    for j in range(1, len(c) + 1):
        t = np.exp((np.sum(np.log(order[:j])) - 2.0 * K) / j)
        if j == len(c) or order[j] <= t:
            break
    return 0.5 * np.maximum(0.0, np.log(c / t)), float(t)


def comparison_margins(K, c, u, mu, omega, target, delta=0.1):
    """Lemma A.1: d_h(K) - z sqrt(v_h(K)) for every comparison h = (target, a)."""
    k, _ = ls_allocation(c, K)
    u, mu, omega = (np.asarray(x, dtype=float) for x in (u, mu, omega))
    z = norm.ppf(1.0 - delta)
    mean = u + np.exp(-2.0 * k) * (mu - u)
    var = omega ** 2 * f_of(k)
    return np.array([(mean[target] - mean[a]) - z * np.sqrt(var[target] + var[a])
                     for a in range(len(u)) if a != target])


def cdn_heterogeneous(c, u, mu, omega, target, delta=0.1, Kmax=80.0, step=0.01):
    """Lemma A.1, eq. (58): smallest K at which every comparison meets accuracy 1 - delta.

    Scans a grid and refines the first crossing by bisection. Returns (K*, upper_set),
    where upper_set reports whether the accuracy condition holds on the whole
    scanned grid above K*.
    """
    grid = np.arange(0.0, Kmax + step, step)
    ok = np.array([np.all(comparison_margins(K, c, u, mu, omega, target, delta) >= 0)
                   for K in grid])
    if not ok.any():
        return np.inf, False
    i = int(np.argmax(ok))
    if i == 0:
        return 0.0, bool(ok.all())
    lo, hi = grid[i - 1], grid[i]
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if np.all(comparison_margins(mid, c, u, mu, omega, target, delta) >= 0):
            hi = mid
        else:
            lo = mid
    return float(hi), bool(ok[i:].all())
