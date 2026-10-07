# Beyond the Semicircle — reference implementation

Companion code for the anonymous submission **Beyond the Semicircle: Free Diffusion Models with
Prescribed Equilibria** and for its extended version. Section and theorem numbers in this README
(Section 10, Theorem 8.11, Remark 7.3, …) refer to the extended version; for instance, Theorem 8.11, the
design theorem, is Theorem 4.2 of the conference version. The experiments `exp10`–`exp13` belong to
Section 6 and Appendix N of the conference version.

Every figure and every number reported in the experiments sections of the two papers is produced by
a script in `experiments/`. The modules in `freeddpm/` implement the objects the
paper defines: Cauchy transforms and the subordination fixed point, the forward
free Ornstein–Uhlenbeck flow and its marginals, the finite-`N` Hermitian matrix
model and its Dyson system, the reverse-time dynamics of Theorem 7.1 and
Corollary 7.4, the free entropy and Fisher functionals of Section 4, the
designed equilibria of Theorem 8.11, and free denoising score matching.

The only dependencies are NumPy, SciPy and Matplotlib. The denoiser is a small
tanh network implemented directly in NumPy with analytic gradients, so there is
no deep-learning dependency and no GPU is required.

---

## Quick start

```bash
# from the unpacked repository directory
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make test          # 29 tests, about 15 seconds
make quick         # all thirteen experiments in reduced configuration, a few minutes
make figures       # all thirteen experiments at the settings used in the paper
```

Figures are written to `figures/`, and each script also writes a JSON record of
its numerical output to `results/`, so every number quoted in the paper is
traceable to a file.

---

## Layout

```
freeddpm/
  cauchy.py        Cauchy transforms; the cubic (9.5); the subordination fixed point (10.1)
  forward.py       noise schedule; forward marginals; the two-atom benchmark; the transition
  matrix.py        GUE; Hermitian OU diffusion (3.10); the Dyson system (3.11); designed drift;
                   sandwich-volatility matrix integrator (sandwich_path)
  particles.py     noise-free particle (quantile) form of the free flow, and its probability-flow reversal
  reverse.py       probability flow (Cor. 7.4); reverse matrix SDE (Alg. 1); the sign check
  functionals.py   logarithmic energy; free Fisher information; W1/W2; inequality ratios
  design.py        the design drift of Theorem 8.11; Marchenko–Pastur; edge diagnostics
  learn.py         free denoising score matching; NumPy MLP denoiser; gradient check
  plotting.py      shared figure style
experiments/       exp01 … exp13, one script per experiment
tests/             29 tests, each checking a stated identity
figures/           output (figures/PROVENANCE.md: the settings each committed result was produced with)
results/           output (JSON), one file per experiment
reproduce/         two self-contained checks that experiments/ does not cover (three-atom gap closing, real S&P 500 spectrum)
  make_figures/    scripts for the schematic figures of the conference version (Figures 1 to 3) and the real-data figure
paper/             LaTeX source of the conference version in plain single-column format (appendix included) + figures
```

## Which script produces which figure

| Script | Section | Figures | Reports |
|---|---|---|---|
| `exp01_forward.py` | §10.1 | `fig1_forward_convergence`, `fig10_spacetime`, `fig11_rate` | snapshot `W1`; convergence exponents; noncollision |
| `exp02_transition.py` | §10.2 | `fig12_phase` | `v*` by bisection; error along `v = a²` |
| `exp03_inequalities.py` | §10.3 | `fig13_inequalities` | max LSI / Talagrand / HWI ratios; de Bruijn error |
| `exp04_free_vs_classical.py` | §10.4 | `fig5_free_vs_classical` | `W1` free vs coordinatewise; fourth-moment gap |
| `exp05_transfer.py` | §10.5 | `fig6_dimension_transfer` | `W1` at `N = 50, 200, 600` |
| `exp06_design_mp.py` | §10.6 | `fig14_design_mp` | terminal `W1`; support; stationarity identity; edge exponents |
| `exp07_reverse.py` | §10.7 | `fig4_reverse_reconstruction` | `W1` along the reverse flow; sign check |
| `exp08_spiked.py` | §10.8 | `fig7_spiked_forward`, `fig8_spiked_reverse` | forward and reverse `W1` |
| `exp09_generative.py` | §10.9 | `fig9_generative` | `W1` for the learned, oracle and coordinatewise scores |
| `exp10_cross_n.py` | Section 6 | `fig16_cross_n` | `W1` of a learned score trained at one `N` and used at others (`--budget`, `--report-only`, `--extra-draws`) |
| `exp11_volatility.py` | Section 6 | `fig15_volatility` | free OU, free Langevin, clock change, non-constant `f` on Marchenko–Pastur |
| `exp12_designed_reverse.py` | Section 6 | `fig17_designed_reverse` | forward particle flow of a designed flow and its reversal from Marchenko–Pastur noise (`freeddpm.particles`) |
| `exp13_target_complexity.py` | Section 6 | `fig18_target_complexity` | designed flow to targets with one, two, three cuts and with outlier bumps; gap-closing times of Theorem 4.8 |

§10.x refers to the extended version, Section 6 to the conference version. Each script takes `--quick` (reduced
dimensions, ensembles and grids) and `--seed`. Seeds are fixed, so results are reproducible on a given NumPy version.
`exp10`–`exp13` can also run in resumable segments (`--budget SECONDS`, then run again to continue; see `--help` for
the other options). Figures 1 to 3 of the conference version, the schematic figures, are produced by `reproduce/make_figures/`.

## Additional reproducible results (`reproduce/`)

Two results of the condensed paper have no script among `exp01`–`exp09`: the gap-closing thresholds on
a three-atom law, and the real S&P 500 correlation spectrum. `reproduce/` re-derives them with short,
self-contained scripts (NumPy, SciPy and pandas; independent of `freeddpm/`):

```bash
make reproduce                      # about a minute; logs in reproduce/logs/
make reproduce-dynamics             # also the S&P 500 matrix-diffusion run
```

See `reproduce/README.md`. The S&P 500 scripts download one public CSV (about 30 MB) into `data/`.

---

## Conventions

These matter, and getting one of them wrong changes a sign or a constant.

**Cauchy transform.** `G(z) = ∫ dμ(y)/(z−y)` maps the upper half plane to the
lower one, with `G(z) ~ 1/z` at infinity. Boundary values give
`ψ(x) = −Im G(x+i0)/π` and `ξ(x) = 2 Re G(x+i0)`.

**Sign of the score.** `ξ_μ` is the *conjugate variable*, equal to twice the
Hilbert transform and to **minus** the classical score. With this convention the
semicircular law of unit variance has `ξ_γ(x) = x`, and the reverse drift
`½βy − βξ` collapses to the forward drift `−½βy` at equilibrium. This is the
diagnostic of Remark 7.3; `reverse.stationarity_residual` implements it and
`tests/` checks it. With the opposite convention the residual is `2βy`.

**Semicircular normalisation.** `gamma_v` is supported on `[−2√v, 2√v]`, and
`matrix.gue(N)` returns a Hermitian matrix whose spectrum converges to `γ₁`,
i.e. to `[−2, 2]`.

**Time direction in the reverse flow.** `probability_flow` takes an *increasing*
sequence of `alpha` values, corresponding to decreasing `t`. The step length in
reverse time is `h = t(α_k) − t(α_{k+1}) > 0` and the drift is `(β/2)(y − ξ)` as
written in Corollary 7.4. Integrating with the opposite sign runs the flow
forwards again and collapses the ensemble onto the semicircular law; the
function raises rather than silently doing this.

**Sandwich coefficient.** For a constant coefficient `f ≡ c` the increment
`f dS f` equals `c² dS`, so Theorem 8.2 reduces to the constant-schedule case at
`f = β^{1/4}`, not `√β`. A constant `f` only rescales time: the spectral velocity is `c⁴` times that of `f ≡ 1`
(`tests/test_sandwich.py`).

---

## Numerical notes

**The logarithmic energy is singular on the diagonal.** For a density on a
uniform grid the diagonal cell is replaced by its exact local average
`log(h/2) − 1`; for a sample the diagonal is excluded and the sum normalised by
`n(n−1)`. See `functionals.log_energy_density`.

**`D` and `I` are differences of O(1) quantities.** Once `μ_t` is within
quadrature error of `γ`, the inequality ratios are noise. `exp03` computes the
error floor by evaluating `D` for the exact semicircular law on the same grid,
where the true value is zero, and drops points below twenty times that floor.
Without this guard the Talagrand ratio appears to exceed 1 at large `Λ`, which
is a quadrature artefact and not a violated inequality.

**The Dyson system is stiff near close eigenvalues.** The repulsion term blows
up like the reciprocal gap, so an explicit step longer than the gap divided by
the drift can push eigenvalues through one another. The eigenvalue integrators
`dyson_path` and `designed_dyson_path` therefore cap the displacement at 0.15
times the smallest gap (`matrix._safe_step`). For the Marchenko–Pastur
potential, which is singular at the origin, even the capped scheme is forced onto
steps of order `1e-8`, so `exp06` integrates the Hermitian *matrix* model instead
(`matrix.designed_matrix_path`): `V'` is applied spectrally, with the eigenvalues
clipped at 0.02 before it is evaluated, the repulsion is generated by the noise
rather than formed explicitly, and a step of `1e-3` is stable.

**Subordination near the real axis.** The fixed point
`ω ← z − v G_ρ(ω)` is iterated with damping and the imaginary part is kept
bounded below by `Im z`, using that `ω` maps `C⁺` into itself. For laws with
outliers of mass `O(1/N)` the density near an outlier is comparable to the
regularisation `ε`, which is why `exp08` reports no absorption time: any
threshold-based detection of gap closure there measures the threshold.

---

## Notes on three results

**1. The convergence exponent for the forward flow.** Comparing the empirical spectral distribution against the
**exact** free marginal gives fitted slopes of `−0.93` and `−0.97` (at `α = 0.3` and `0.6`;
`results/exp01_forward.json`): eigenvalues of a deformed GUE are rigid, so their empirical measure is far closer to
its limit than an i.i.d. sample of the same size would be. Against an **equal-size Monte Carlo sample** drawn from
`μ_t` the slopes are about `−0.5`, but what that measures is the fluctuation of the reference sample and not of the
matrix model. `exp01` produces both panels and reports both slopes (`slope_exact_*` and `slope_mc_*`).

**2. Edge regularity in Theorem 8.11.** The Plemelj–Privalov theorem gives Hölder continuity of `H(f²μ*)` on
compact subsets of the interior of the support, not up to a hard edge. For `f ≡ 1` and `ψ* ≡ ½` on `[−1,1]` — a
Hölder continuous density — one has `Hμ*(x) = ½ log|(x+1)/(x−1)|`, which diverges at both edges, so the design drift
is unbounded there. `design.flat_law_hilbert` implements this counterexample and the test suite checks it. Under
the additional hypothesis that `ψ*` vanishes at the edges at a Hölder rate the drift is bounded and Hölder on the
whole support; the Marchenko–Pastur law satisfies this, with edge exponents measured at `0.43` and `0.51` against
the theoretical `1/2`.

**3. The reduction constant in Theorem 8.2.** `f ≡ β^{1/4}`, not `f ≡ √β`; see Conventions above.

---

## Citation

See `CITATION.cff`. Please cite the paper rather than the repository.

## Licence

MIT, see `LICENSE`.
