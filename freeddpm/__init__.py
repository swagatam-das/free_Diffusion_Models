"""Free diffusion for spectral laws: reference implementation.

Companion code for *Beyond the Semicircle: Free Diffusion Models with Prescribed
Equilibria* and its extended version.  Every figure and every number reported in the
experiments sections of the two papers is produced by a script in ``experiments/``; the
modules here implement the objects the papers define.
"""

__version__ = "1.0.0"

from . import cauchy, design, forward, functionals, learn, matrix, reverse  # noqa: F401

__all__ = [
    "cauchy",
    "design",
    "forward",
    "functionals",
    "learn",
    "matrix",
    "reverse",
]
