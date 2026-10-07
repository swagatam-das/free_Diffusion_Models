# `paper/`

`main.tex` is the conference version, *Beyond the Semicircle: Free Diffusion Models with Prescribed Equilibria*, in plain
single-column format with the appendix included. The conference submission uses the same text in the conference style.

```bash
cd paper
pdflatex main.tex && pdflatex main.tex && pdflatex main.tex     # no BibTeX: the bibliography is inline
```

All figures it includes are in this directory. The experiment figures are the files in `../figures/`, produced by
`../experiments/`; Figures 1 to 3 are produced by `../reproduce/make_figures/`.
