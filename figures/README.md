# Textbook figures

Editable vector figures for **AI と物理学の系譜**.

## Policy

- Final textbook assets: `figures/eps/*.eps`
- Reproducible source: `figures/generate_figures.py`
- EPS is generated with Matplotlib's PostScript backend.
- Japanese glyphs use Type-3 vector fonts for broad EPS compatibility.
- Randomized illustrations use fixed RNG seeds for reproducibility.
- For substantial text or geometry edits, change the Python source and regenerate the EPS.

## Current batch

| File | Suggested insertion | Purpose |
|---|---|---|
| `fig00_knowledge_map.eps` | Preface / 「この本の読み方」 | Entire-book knowledge map |
| `fig01_geocentric_heliocentric.eps` | 1.2 | Geocentric vs heliocentric model comparison |
| `fig02_gradient_descent.eps` | 1.4 | Potential minimum vs AI loss minimization |
| `fig03_fermat_principle.eps` | 2.1 | Fermat principle and minimum travel time |
| `fig04_entropy_time_arrow.eps` | 3.1–3.3 | Entropy and macroscopic arrow of time |
| `fig05_diffusion_forward_reverse.eps` | 3.5 | Forward diffusion and reverse denoising |

## Local regeneration

```bash
python -m pip install numpy matplotlib
python figures/generate_figures.py
```

On GitHub, `.github/workflows/generate-figures.yml` regenerates and validates the EPS files whenever the generator is changed.
