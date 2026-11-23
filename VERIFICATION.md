# Verification of manuscript numbers

Manuscript: "Action Spaces Matter: Choice, Equilibrium, and Mechanism Design under Cognitive Constraints" (main text with appendices, and Online Appendix).

Run: `python run_all.py` on Windows 11 Enterprise (Intel Core Ultra 7 155H, 32 GB RAM), Python 3.14.4, numpy 2.4.4, scipy 1.17.1, 31 October 2026. Total running time about 18 seconds. Exit status 0.

## Result

All 59 computed numbers printed in the manuscript are reproduced at the precision shown in the manuscript. No mismatch was found. All 39 supplementary checks in `scripts/model_checks.py` and `scripts/grid_auction.py` pass.

The Online Appendix contains no numerical results (only propositions and proofs), and the paper contains no figures.

Comparison rule: the reproduced value is rounded to the number of decimals printed in the manuscript and compared as text; fractions (1/4, 3/4, 1/2) are compared exactly; "yes"/"no" rows are logical statements in the text. The same table is produced automatically as `output/verification.csv`.

## Inventory and comparison

| # | Location | Quantity | Manuscript | Reproduced | Match | Program |
|---|---|---|---|---|---|---|
| 1 | Sec. 3.2, text before Table 1 | probit-to-logit shift log(2.20/1.28) (nats) | 0.54 | 0.54 | yes | `scripts/table1_location_scale.py` |
| 2 | Table 1, row 1 | G^{-1}(0.9), standard normal | 1.28 | 1.28 | yes | `scripts/table1_location_scale.py` |
| 3 | Table 1, row 3 | G^{-1}(0.9), standard logistic | 2.20 | 2.20 | yes | `scripts/table1_location_scale.py` |
| 4 | Table 1, row 4 | G^{-1}(0.9), Student t3 | 1.64 | 1.64 | yes | `scripts/table1_location_scale.py` |
| 5 | Table 1, row 5 | G^{-1}(0.9), Cauchy | 3.08 | 3.08 | yes | `scripts/table1_location_scale.py` |
| 6 | Table 1, row 6 | G^{-1}(0.9), uniform on [-1,1] | 0.80 | 0.80 | yes | `scripts/table1_location_scale.py` |
| 7 | Table 1, row 7 | G^{-1}(0.9), large market (limiting normal) | 1.28 | 1.28 | yes | `scripts/table1_location_scale.py` |
| 8 | Sec. 5.2, grid table (unnumbered) | N=2: tick size eps | 0.500 | 0.500 | yes | `scripts/grid_auction.py` |
| 9 | Sec. 5.2, grid table (unnumbered) | N=2: K*_hom | 1.332 | 1.332 | yes | `scripts/grid_auction.py` |
| 10 | Sec. 5.2, grid table (unnumbered) | N=2: correct-choice probability | 0.979 | 0.979 | yes | `scripts/grid_auction.py` |
| 11 | Sec. 5.2, grid table (unnumbered) | N=2: Delta_excl | 0.0417 | 0.0417 | yes | `scripts/grid_auction.py` |
| 12 | Sec. 5.2, grid table (unnumbered) | N=2: T | 0.0013 | 0.0013 | yes | `scripts/grid_auction.py` |
| 13 | Sec. 5.2, grid table (unnumbered) | N=2: Delta_excl + T | 0.0429 | 0.0429 | yes | `scripts/grid_auction.py` |
| 14 | Sec. 5.2, grid table (unnumbered) | N=3: tick size eps | 0.333 | 0.333 | yes | `scripts/grid_auction.py` |
| 15 | Sec. 5.2, grid table (unnumbered) | N=3: K*_hom | 2.871 | 2.871 | yes | `scripts/grid_auction.py` |
| 16 | Sec. 5.2, grid table (unnumbered) | N=3: correct-choice probability | 0.804 | 0.804 | yes | `scripts/grid_auction.py` |
| 17 | Sec. 5.2, grid table (unnumbered) | N=3: Delta_excl | 0.0185 | 0.0185 | yes | `scripts/grid_auction.py` |
| 18 | Sec. 5.2, grid table (unnumbered) | N=3: T | 0.0118 | 0.0118 | yes | `scripts/grid_auction.py` |
| 19 | Sec. 5.2, grid table (unnumbered) | N=3: Delta_excl + T | 0.0303 | 0.0303 | yes | `scripts/grid_auction.py` |
| 20 | Sec. 5.2, grid table (unnumbered) | N=4: tick size eps | 0.250 | 0.250 | yes | `scripts/grid_auction.py` |
| 21 | Sec. 5.2, grid table (unnumbered) | N=4: K*_hom | 4.784 | 4.784 | yes | `scripts/grid_auction.py` |
| 22 | Sec. 5.2, grid table (unnumbered) | N=4: correct-choice probability | 0.685 | 0.685 | yes | `scripts/grid_auction.py` |
| 23 | Sec. 5.2, grid table (unnumbered) | N=4: Delta_excl | 0.0104 | 0.0104 | yes | `scripts/grid_auction.py` |
| 24 | Sec. 5.2, grid table (unnumbered) | N=4: T | 0.0189 | 0.0189 | yes | `scripts/grid_auction.py` |
| 25 | Sec. 5.2, grid table (unnumbered) | N=4: Delta_excl + T | 0.0293 | 0.0293 | yes | `scripts/grid_auction.py` |
| 26 | Sec. 5.2, grid table (unnumbered) | N=5: tick size eps | 0.200 | 0.200 | yes | `scripts/grid_auction.py` |
| 27 | Sec. 5.2, grid table (unnumbered) | N=5: K*_hom | 6.973 | 6.973 | yes | `scripts/grid_auction.py` |
| 28 | Sec. 5.2, grid table (unnumbered) | N=5: correct-choice probability | 0.622 | 0.622 | yes | `scripts/grid_auction.py` |
| 29 | Sec. 5.2, grid table (unnumbered) | N=5: Delta_excl | 0.0067 | 0.0067 | yes | `scripts/grid_auction.py` |
| 30 | Sec. 5.2, grid table (unnumbered) | N=5: T | 0.0227 | 0.0227 | yes | `scripts/grid_auction.py` |
| 31 | Sec. 5.2, grid table (unnumbered) | N=5: Delta_excl + T | 0.0293 | 0.0293 | yes | `scripts/grid_auction.py` |
| 32 | Sec. 5.2, grid table (unnumbered) | N=6: tick size eps | 0.167 | 0.167 | yes | `scripts/grid_auction.py` |
| 33 | Sec. 5.2, grid table (unnumbered) | N=6: K*_hom | 9.377 | 9.377 | yes | `scripts/grid_auction.py` |
| 34 | Sec. 5.2, grid table (unnumbered) | N=6: correct-choice probability | 0.587 | 0.587 | yes | `scripts/grid_auction.py` |
| 35 | Sec. 5.2, grid table (unnumbered) | N=6: Delta_excl | 0.0046 | 0.0046 | yes | `scripts/grid_auction.py` |
| 36 | Sec. 5.2, grid table (unnumbered) | N=6: T | 0.0248 | 0.0248 | yes | `scripts/grid_auction.py` |
| 37 | Sec. 5.2, grid table (unnumbered) | N=6: Delta_excl + T | 0.0294 | 0.0294 | yes | `scripts/grid_auction.py` |
| 38 | Sec. 5.2, text after table | unconstrained minimiser of Delta_excl+T over N=2..6 | 4 | 4 | yes | `scripts/grid_auction.py` |
| 39 | Sec. 5.2, text after table | N=2 feasible at Kbar=2 (K_hom <= 2) | yes | yes | yes | `scripts/grid_auction.py` |
| 40 | Sec. 5.2, text after table | N=3 feasible at Kbar=2 | no | no | yes | `scripts/grid_auction.py` |
| 41 | Sec. 5.2, text after table | finest feasible grid N | 2 | 2 | yes | `scripts/grid_auction.py` |
| 42 | Sec. 5.2, text after table | constrained solution eps** | 1/2 | 0.500000 (= 1/2) | yes | `scripts/grid_auction.py` |
| 43 | Sec. 7.2 text; Table 2 row 1 | p_S | 1/4 | 0.250000 (= 1/4) | yes | `scripts/small_school.py` |
| 44 | Sec. 7.2 text; Table 2 row 1 | g_S | 0.20 | 0.20 | yes | `scripts/small_school.py` |
| 45 | Sec. 7.2 text; Table 2 row 1 | Delta_S | 0.05 | 0.05 | yes | `scripts/small_school.py` |
| 46 | Sec. 7.2 text; Table 2 row 1 | K_S^rep | 5.47 | 5.47 | yes | `scripts/small_school.py` |
| 47 | Sec. 7.2 text; Table 2 row 2 | p_L | 3/4 | 0.750000 (= 3/4) | yes | `scripts/small_school.py` |
| 48 | Sec. 7.2 text; Table 2 row 2 | g_L | 0.20 | 0.20 | yes | `scripts/small_school.py` |
| 49 | Sec. 7.2 text; Table 2 row 2 | Delta_L | 0.15 | 0.15 | yes | `scripts/small_school.py` |
| 50 | Sec. 7.2 text; Table 2 row 2 | K_L^rep | 3.32 | 3.32 | yes | `scripts/small_school.py` |
| 51 | Sec. 7.2 text | K_S^rep - K_L^rep | 2.15 | 2.15 | yes | `scripts/small_school.py` |
| 52 | Sec. 7.2, DA/RSD example | Delta_DA | 0.4 | 0.4 | yes | `scripts/da_rsd.py` |
| 53 | Sec. 7.2, DA/RSD example | Delta_RSD | 0.2 | 0.2 | yes | `scripts/da_rsd.py` |
| 54 | Sec. 7.2, DA/RSD example | K*_DA | 1.64 | 1.64 | yes | `scripts/da_rsd.py` |
| 55 | Sec. 7.2, DA/RSD example | K*_RSD | 2.79 | 2.79 | yes | `scripts/da_rsd.py` |
| 56 | Sec. 7.2, DA/RSD example | K*_RSD - K*_DA | 1.15 | 1.15 | yes | `scripts/da_rsd.py` |
| 57 | App. B.1, numerical example | tau*(1) | 1.094 | 1.094 | yes | `scripts/pigouvian_tax.py` |
| 58 | App. B.1, numerical example | tau*(2) | 1.035 | 1.035 | yes | `scripts/pigouvian_tax.py` |
| 59 | App. B.1, numerical example | tau*(3) | 1.013 | 1.013 | yes | `scripts/pigouvian_tax.py` |

## Remarks (no change to the manuscript required)

1. Section 5.2: `Delta_excl + T` equals 0.029339 at N = 4 and 0.029341 at N = 5; both round to 0.0293 in the table. The minimum over N = 2..6 is at N = 4, consistent with the text ("minimized near N = 4"). The margin is small (2e-6).
2. Section 5.2: under the additive convention `(N-1)T` the unconstrained optimum over N = 2..6 is N = 3 rather than N = 4. The text states that the additive convention could change the numerical optimum and that the package reports both conventions; it does (`output/table_grid_auction.csv`). The constrained solution `eps** = 1/2` is the same under both conventions.
3. Section 5.2: with heterogeneous benefit coefficients (`c_target/c_alt` = 1/2 or 2), the CDN for N = 2 is 1.380 and for N = 3 at least 2.728, so the feasibility statement at `Kbar = 2` is unchanged (`output/table_grid_auction_heterogeneity.csv`). The text reports no numbers for this sensitivity check.
4. Section 5.2: `Delta_excl(N) = 1/(6N^2)` is confirmed by exact numerical integration (error below 1e-10) and by Monte Carlo.
5. Table 1, row 2 (quadratic loss) reports no number ("depends on shape"); nothing to verify.
6. Unrounded values: `log(2.1972/1.2816) = 0.5391`; `K^rep_S = 5.4723`, `K^rep_L = 3.3239`, difference 2.1484; `K*_DA = 1.6373`, `K*_RSD = 2.7890`, difference 1.1517; `tau* = 1.0943, 1.0347, 1.0128`. The printed differences (2.15, 1.15) agree both with the difference of unrounded values and with the difference of the rounded values.
