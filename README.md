# Replication package for "Action Spaces Matter: Choice, Equilibrium, and Mechanism Design under Cognitive Constraints"

Shinji Nakazato and Tetsuya Shimokawa (Tokyo University of Science)

## Overview

The paper is theoretical. Its numerical content consists of a small number of
closed-form evaluations, exact enumerations and illustrative examples. This
package reproduces every computed number in the main text and its appendices
(Table 1, the grid-auction table in Section 5.2, Table 2 and the DA/RSD example
in Section 7.2, and the Pigouvian-tax example in Appendix B.1). The Online
Appendix contains no numerical results. The paper contains no figures.

A single Python script, `run_all.py`, runs all programs, writes the results to
`output/`, and compares every reproduced number with the value printed in the
manuscript (`output/verification.csv`; summary in `VERIFICATION.md`). On the
machine described below the full run takes about 18 seconds.

## Data Availability and Provenance Statements

This package uses **no external data**. All inputs are model parameters stated
in the manuscript and hard-coded in the scripts. The empirical and experimental
studies cited in the paper (e.g. Chen and Sönmez 2006; Calsamiglia, Haeringer and
Klijn 2010; Rees-Jones 2018; Shorrer and Sóvágó 2023) motivate the analysis but
none of their data is used in any computation.

### Statement about rights

- [x] I certify that the authors of the manuscript have legitimate access to and permission to use the data used in this manuscript (no data are used).
- [x] I certify that the authors of the manuscript have documented permission to redistribute/publish the data contained within this replication package (no data are contained).

### License for code

The code is offered under the MIT License; see `LICENSE.txt`.

## Dataset list

None.

## Computational requirements

### Software requirements

- Python 3 (tested with Python 3.14.4)
- `numpy` 2.4.4 and `scipy` 1.17.1 (pinned in `requirements.txt`)

Only the Python standard library is used otherwise. No random number generation
affects any reported number; the supplementary Monte Carlo checks in
`scripts/model_checks.py` use a fixed seed (`20261031`).

### Controlled randomness

- [x] Random seed is set in `scripts/model_checks.py` (line `SEED = 20261031`).
- [x] No other part of the code uses pseudo-random numbers.

### Memory, runtime, storage

- Runtime: about 18 seconds in total (of which about 12 seconds for
  `scripts/grid_auction.py`, about 5 seconds for `scripts/model_checks.py`).
- Memory: under 1 GB. Storage: under 1 MB including outputs.
- Tested on: Windows 11 Enterprise, Intel Core Ultra 7 155H, 32 GB RAM,
  Python 3.14.4, numpy 2.4.4, scipy 1.17.1 (October 2026).

## Description of programs

| File | Purpose |
|---|---|
| `run_all.py` | Master script. Runs the six scripts below in order, writes `output/run_all.log`, compares reproduced and printed numbers, writes `output/verification.csv`. Exit status 0 if all numbers match and all checks pass. |
| `src/cdn.py` | Model functions: attention weight `m(k)`, variance factor `f(k)`, the closed-form cognitive difficulty number (Theorem 3.1, eq. 21), pairwise accuracy (eq. 25) and its inversion (eq. 26), benefit coefficients (eq. 13), Linear--Shannon allocation (eq. 14), heterogeneous CDN (Lemma A.1, eq. 58). |
| `src/manuscript_values.py` | The numbers printed in the manuscript, with their locations, used for the automatic comparison. |
| `src/common.py` | Output directory and CSV helper. |
| `scripts/table1_location_scale.py` | Table 1: quantiles `G^{-1}(0.9)`; Section 3.2: probit-to-logit shift `log(2.20/1.28)`. |
| `scripts/grid_auction.py` | Section 5.2 grid-auction table (`K_hom`, correct-choice probability, `Delta_excl`, `T`, `Delta_excl + T` for N = 2..6), the unconstrained optimum, cognitive feasibility at `Kbar = 2`, `eps** = 1/2`; also the additive loss convention `(N-1)T` mentioned in the text, an exact check of `Delta_excl = 1/(6N^2)`, and the sensitivity of the CDN to heterogeneous benefit coefficients (Lemma A.1). |
| `scripts/small_school.py` | Section 7.2 and Table 2: exact enumeration of the 4! priority orders; `p`, `g`, `Delta`, `K^rep` for the two local comparisons and their difference. |
| `scripts/da_rsd.py` | Section 7.2: DA versus RSD two-action example (`K*_DA`, `K*_RSD`, difference). |
| `scripts/pigouvian_tax.py` | Appendix B.1: `tau*(kappa)` for kappa = 1, 2, 3 (Proposition B.1). |
| `scripts/model_checks.py` | Supplementary checks (no printed numbers): conditional posterior draw (eq. 8), linearity of the A4 benefit (eq. 13), Theorem 3.1 at `K*` (closed form and Monte Carlo), Lemma A.1 versus Theorem 3.1, KKT conditions of eq. (14), Proposition 3.4 (inversion, derivative, Jacobian rank, eq. 28), Monte Carlo check of `Delta_excl`. |

Each script in `scripts/` can also be run on its own (`python scripts/<name>.py`).

## Instructions to replicators

From the root of the package:

```bash
python -m pip install -r requirements.txt
python run_all.py
```

`run_all.py` prints all results, saves the console output to
`output/run_all.log`, and writes the CSV files listed below. The final lines
report how many manuscript numbers were reproduced and how many checks passed.

## List of tables, figures and in-text numbers

| Manuscript location | Content | Program | Output file |
|---|---|---|---|
| Section 3.2, text before Table 1 | `log(2.20/1.28) = 0.54` nats | `scripts/table1_location_scale.py` | `output/run_all.log` |
| Table 1 | `G^{-1}(0.9)`: 1.28, 2.20, 1.64, 3.08, 0.80, 1.28 | `scripts/table1_location_scale.py` | `output/table1_location_scale.csv` |
| Section 5.2, grid table (unnumbered) | all entries, N = 2..6 | `scripts/grid_auction.py` | `output/table_grid_auction.csv` |
| Section 5.2, text after table | optimum near N = 4; N = 2 feasible, N = 3 infeasible at `Kbar = 2`; `eps_K* = eps** = 1/2` | `scripts/grid_auction.py` | `output/run_all.log` |
| Section 5.2, text ("The replication package reports both conventions") | additive convention `(N-1)T` | `scripts/grid_auction.py` | `output/table_grid_auction.csv` (columns `T_additive`, `excl_plus_T_additive`) |
| Section 5.2, text (sensitivity to heterogeneous coefficients, eq. 14) | CDN for `c_target/c_alt` in {1/2, 1, 2} | `scripts/grid_auction.py` | `output/table_grid_auction_heterogeneity.csv` |
| Section 7.2 text and Table 2 | `p_S = 1/4`, `p_L = 3/4`, `g = 0.20`, `Delta_S = 0.05`, `Delta_L = 0.15`, `K^rep_S = 5.47`, `K^rep_L = 3.32`, difference 2.15 | `scripts/small_school.py` | `output/table2_small_school.csv` |
| Section 7.2, DA/RSD example | `K*_DA = 1.64`, `K*_RSD = 2.79`, difference 1.15 | `scripts/da_rsd.py` | `output/da_rsd_example.csv` |
| Appendix B.1, numerical example | `tau*(1) = 1.094`, `tau*(2) = 1.035`, `tau*(3) = 1.013` | `scripts/pigouvian_tax.py` | `output/appendixB_pigouvian_tax.csv` |
| All of the above | manuscript value versus reproduced value | `run_all.py` | `output/verification.csv` |

### Notes on the grid-auction example

The manuscript table uses the representative local loss
`T(N; Kbar) = vbar [1 - Phi(N^{-1} m(Kbar/N) / (omega sqrt(2 f(Kbar/N))))]` with
`vbar = 0.06`, `omega = 0.3`, `delta = 0.1`, `Kbar = 2`. Under this convention
`Delta_excl + T` is 0.029339 at N = 4 and 0.029341 at N = 5, so the minimum over
N = 2..6 is at N = 4 (both round to 0.0293 in the table). Under the additive
convention `(N-1)T`, the unconstrained optimum over N = 2..6 is N = 3. The
cognitive constraint `K_hom <= 2` admits only N = 2 under both conventions, so
the constrained solution `eps** = 1/2` is the same. With heterogeneous benefit
coefficients (ratio 1/2 or 2) the CDN for N = 2 rises to 1.380, so N = 2 remains
feasible and N = 3 remains infeasible at `Kbar = 2`.

## References

Harris, C. R., K. J. Millman, S. J. van der Walt, et al. (2020), "Array
programming with NumPy," *Nature*, 585, 357--362.

Virtanen, P., R. Gommers, T. E. Oliphant, et al. (2020), "SciPy 1.0: Fundamental
algorithms for scientific computing in Python," *Nature Methods*, 17, 261--272.

Nakazato, S., and T. Shimokawa (2026), "Action Spaces Matter: Choice, Equilibrium, and Mechanism
Design under Cognitive Constraints," manuscript.
