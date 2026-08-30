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

## Verification plan

A dedicated GitHub Actions workflow will install a Japanese-capable TeX Live environment, compile `latex/main.tex` twice with LuaLaTeX, and upload `main.pdf` and `main.log` as build artifacts.
