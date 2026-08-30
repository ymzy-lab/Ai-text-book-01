# Textbook figures

Editable vector figures for **AI と物理学の系譜**.

## Policy

- Final textbook assets: `figures/eps/*.eps`
- Reproducible sources: `figures/generate_figures.py`, `figures/generate_new_figures.py`, `figures/generate_ch07_09.py`, `figures/generate_ch10_12.py`, and `figures/generate_ch13_15.py`
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
| `fig06_field_div_rot.eps` | 4.3 | Vector field intuition for divergence and curl |
| `fig07_em_wave_attention.eps` | 4.5–4.7 | Electromagnetic propagation vs Self-Attention |
| `fig08_simple_harmonic_motion.eps` | 5.1 | Restoring force, harmonic motion, and potential |
| `fig09_interference_standing_wave.eps` | 5.2 | Superposition, interference, and standing waves |
| `fig10_fourier_decomposition.eps` | 5.3–5.4 | Fourier decomposition and frequency spectrum |
| `fig11_minkowski_time_dilation.eps` | 6.3 | Light clock and Minkowski diagram |
| `fig12_embedding_analogy.eps` | 6.5–6.6 | Word-vector analogy geometry |
| `fig13_light_cone_curvature.eps` | 7.1–7.4 | Light cone, causal region, and curved spacetime |
| `fig14_manifold_unfolding.eps` | 7.5–7.6 | Manifold hypothesis and deep representation flattening |
| `fig15_blackbody_radiation.eps` | 8.2–8.4 | Blackbody radiation, ultraviolet catastrophe, and Planck distribution |
| `fig16_bohr_spectrum.eps` | 8.6–8.7 | Hydrogen energy levels and Balmer spectrum |
| `fig17_symbolic_regression.eps` | 8.8 | Symbolic regression and accuracy-complexity tradeoff |
| `fig18_stress_strain.eps` | 9.2 | Elastic, plastic, and fracture regimes |
| `fig19_chaos_lyapunov.eps` | 9.4 | Lorenz attractor and exponential separation of nearby trajectories |
| `fig20_pinn_architecture.eps` | 9.5 | PINN training loop, physics loss, forward and inverse problems |
| `fig21_de_broglie_diffraction.eps` | 10.1 | de Broglie wavelength and electron diffraction |
| `fig22_wavefunction_born_probability.eps` | 10.4 | Complex wavefunction and Born probability density |
| `fig23_uncertainty_wavepacket.eps` | 10.3 | Position-momentum uncertainty using wave packets |
| `fig24_curse_dimensionality_nnqs.eps` | 10.5–10.6 | Exponential Hilbert-space growth and neural quantum states |
| `fig25_law_large_numbers.eps` | 11.1 | Law of large numbers and vanishing relative fluctuations |
| `fig26_quantum_statistics.eps` | 11.3–11.4 | Maxwell-Boltzmann, Fermi-Dirac, and Bose-Einstein statistics |
| `fig27_boltzmann_softmax.eps` | 11.5 | Boltzmann distribution and Softmax correspondence |
| `fig28_emergence_hierarchy.eps` | 12.1 | Hierarchy, emergence, and top-down constraints |
| `fig29_semiconductor_bands.eps` | 12.2 | Conductor, semiconductor, and insulator band gaps |
| `fig30_superconductivity_cooper_pair.eps` | 12.3 | Cooper pairing and coherent superconducting state |
| `fig31_quantum_interference_vqe.eps` | 12.4 | Quantum interference and VQE hybrid optimization |
| `fig32_reduction_hierarchy.eps` | 13.1 | Matter hierarchy from macroscopic matter to quarks |
| `fig33_standard_model_map.eps` | 13.5–13.7 | Standard Model fermions, gauge bosons, and Higgs |
| `fig34_feynman_gnn.eps` | 13.4 | Feynman diagram and GNN structural analogy |
| `fig35_higgs_symmetry_breaking.eps` | 13.7 | Spontaneous symmetry breaking and vacuum selection |
| `fig36_lhc_trigger_funnel.eps` | 13.9 | LHC event filtering and AI trigger funnel |
| `fig37_hubble_law.eps` | 14.1 | Hubble–Lemaître law with schematic galaxy data |
| `fig38_cosmic_timeline.eps` | 14.2–14.3 | Inflation-to-present cosmic timeline |
| `fig39_universe_composition.eps` | 14.4 | Ordinary matter, dark matter, and dark energy fractions |
| `fig40_gravitational_chirp.eps` | 14.5 | Gravitational-wave chirp waveform and rising frequency |
| `fig41_holographic_principle.eps` | 14.9 | Boundary information and bulk description |
| `fig42_math_intuition_proof_loop.eps` | 15.1–15.3 | Intuition, conjecture, proof, and discovery loop |
| `fig43_formal_proof_pipeline.eps` | 15.4 | AI-assisted formal proof and machine verification pipeline |

## Local regeneration

```bash
python -m pip install numpy matplotlib
python figures/generate_figures.py
python figures/generate_new_figures.py
python figures/generate_ch07_09.py
python figures/generate_ch10_12.py
python figures/generate_ch13_15.py
```

On GitHub, `.github/workflows/generate-figures.yml` regenerates and validates all EPS files whenever a generator is changed.
