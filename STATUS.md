# Repository status snapshot

Recorded: 2026-08-30 20:41 JST

## Baseline before CI verification

- Branch: `main`
- Baseline commit: `3b3c5ffe6b820b7e057a973d78298158de5e7197`
- Baseline tree: `30c729257e5353fa5ccac62e3ddacd4267908b53`
- Repository language reported by GitHub: TeX

## Manuscript

- Root source: `latex/main.tex`
- Document class: `ltjsbook`
- Intended engine: LuaLaTeX
- Front matter: `latex/chapters/preface.tex`
- Main text: `latex/chapters/chapter01.tex` through `chapter17.tex`
- Chapter references: `latex/chapters/references/chapter01_refs.tex` through `chapter17_refs.tex`
- Bibliography backend: none; references are ordinary LaTeX files included with `\input`
- Current manuscript is the pre-figure-insertion version; no `\includegraphics` references are present yet.

## Figure assets

- Editable vector assets: `figures/eps/fig00_knowledge_map.eps` through `fig51_self_referential_universe.eps`
- Figure count: 52 EPS files
- Reproducible generators are maintained under `figures/`.
- Existing figure CI: `.github/workflows/generate-figures.yml`

## LuaLaTeX dependencies used by `main.tex`

- `ltjsbook` / LuaTeX-ja
- `luatexja`
- `luatexja-fontspec`
- `geometry`
- `amsmath`
- `graphicx`
- `hyperref`
- `bookmark`
- `enumitem`

## CI verification result

- Workflow: `.github/workflows/compile-latex.yml`
- Verified commit: `441e8716f52c208982664093a01c28a6a114913a`
- GitHub Actions run: `33310298826`
- Job: `99254019961`
- Result: **success**
- Runner: Ubuntu 24.04
- Engine: LuaHBTeX 1.17.0 / TeX Live 2023 (Debian packages)
- `ltjsbook.cls`, `luatexja.sty`, and `luatexja-fontspec.sty` were found successfully.
- LuaLaTeX pass 1: success, PDF generated.
- LuaLaTeX pass 2: success, final PDF generated.
- Final output: `main.pdf`, 227 pages, 1,783,886 bytes.
- LaTeX warning scan (`LaTeX Warning`, package warnings, `Overfull`, `Underfull`): no matches in the final log.
- Build artifact: `latex-build`, artifact ID `9731792237`.
- Artifact contains `main.pdf`, `main.log`, `compile-pass1.txt`, and `compile-pass2.txt`.
- Artifact expiry: 2026-11-28.

The current pre-figure manuscript therefore compiles reproducibly on GitHub Actions with the repository contents alone plus the documented TeX Live packages.
