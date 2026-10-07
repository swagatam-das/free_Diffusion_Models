# Provenance of the committed figures and results

`results/*.json` carries a timestamp for every run.  All thirteen experiments are committed at their full settings.
Figure numbers in the second column are those of the extended version for `exp01`–`exp09` and of the conference version
(Section 6, Appendix N) for `exp10`–`exp13`.

| Experiment | Figures | Committed settings |
|---|---|---|
| `exp01_forward` | 1, 2, 3 | full: N up to 800, 12 realisations per point |
| `exp02_transition` | 4 | full |
| `exp03_inequalities` | 5 | full: 6001-point grid, 60 schedule levels |
| `exp04_free_vs_classical` | 6 | full: N = 2500 (N = 3000 for the moment check) |
| `exp05_transfer` | 7 | full: N = 50, 200, 600; 400 reverse steps |
| `exp06_design_mp` | (no figure) | full: N = 400, T = 8, dt = 1e-3, 4000-point grid |
| `exp07_reverse` | 8 | full: 6e4 particles, 600 midpoint steps |
| `exp08_spiked` | 9, 10 | full: N = 600, 300 score-table levels |
| `exp09_generative` | 11 | full: N = 400, 168 000 training pairs |
| `exp10_cross_n` | Section 6, Appendix N | full: trained at N = 100 and 400, tested at N = 50 to 800 (N = 800 for the two-atom law only); 60 000 pairs, 100 epochs, 300 reverse steps; 8, 8, 4 and 3 noise draws at N = 50, 100, 200 and 400, one draw at N = 800; `--metrics` adds KS distance, moments and support endpoints for the same runs |
| `exp11_volatility` | Section 6 | full: N = 150, T = 6, dt = 2e-3, 3000-point grid |
| `exp12_designed_reverse` | Section 6, Appendix N | full: M = 800 forward particles, N = 400 generated eigenvalues, T = 5, five prior samples |
| `exp13_target_complexity` | Section 6, Appendix N | full: M = 400 particles, T = 40, snapshot interval 0.1, f = 1 |

The PNG files in `paper/` that also appear in `figures/` are byte-identical to them.

## Settings of `exp06`, `exp08` and `exp09`

`exp06` is committed at its full settings (N = 400, T = 8, dt = 1e-3, 4000-point grid).  For reference, its `--quick`
run (N = 120, T = 3, dt = 4e-3, 1200-point grid) gives:

| quantity | `--quick` | full |
|---|---|---|
| stationarity relative error, interior | 3.49e-3 | 9.39e-4 |
| edge exponents (lower / upper; theory 0.5) | 0.416 / 0.512 | 0.432 / 0.511 |
| terminal `W1` to Marchenko-Pastur | 0.0178 | 0.00353 |
| empirical support (theory [0.0858, 2.914]) | [0.0935, 2.709] | [0.0926, 2.858] |

The stationarity error and the edge exponents are properties of the analytic Marchenko-Pastur density on the
quadrature grid, so they depend on the grid size (`n_grid`), not on N; the matrix run feeds only the terminal `W1`
and the empirical support.  The full run was executed in time-boxed segments that checkpoint the matrix and the
random-number-generator state, so the result equals that of an uninterrupted run.

`exp08` and `exp09` are full runs; their JSON records the settings used (`N = 600` and `score_table_levels = 300`
for `exp08`, `N = 400` and `n_training_pairs = 168000` for `exp09`; quick mode gives 200 and 12, and 120 and 24 000).

## Notes

`exp10`, `exp11`, `exp12` and `exp13` were run in time-boxed segments (`--budget`), resuming from `results/cache/`
(git-ignored); the result for a given seed is the same as that of a single uninterrupted run.
`python experiments/exp10_cross_n.py --report-only` rebuilds the report from the cache.  In `exp10` the exact score
is the N -> infinity free score; with Euler-Maruyama steps it sometimes leaves an eigenvalue outside the support, which
raises its `W1`, so a learned score can fall below it in `W1` at finite N (the KS distance, recorded with `--metrics`,
is far less affected).

`exp08` is the slowest experiment: it solves the subordination fixed point at
every one of 300 schedule levels.  The iteration is warm-started from the
previous level (`subordination_g(..., omega0=omega, return_omega=True)`), which
cuts the iteration count by roughly an order of magnitude; without it the run is
not practical on a single core.

The checks in `reproduce/` (three-atom gap closing, real S&P 500 spectrum) are
independent of these experiments and write their logs to `reproduce/logs/`.
