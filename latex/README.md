# LaTeX manuscript source

LaTeX source for **AI と物理学の系譜**.

## Structure

- `main.tex` — root document
- `chapters/preface.tex` — preface
- `chapters/chapter01.tex` ... `chapters/chapter17.tex` — chapter source files
- `chapters/references/chapter01_refs.tex` ... `chapter17_refs.tex` — chapter-end references included directly with `\input`

The manuscript does not currently use BibTeX or Biber. References are ordinary LaTeX source files.

The textbook figures are maintained separately under `../figures/eps/`. The current manuscript source is the pre-figure-insertion version.

## Build

The document class is `ltjsbook`, so compile with LuaLaTeX from this directory:

```bash
cd latex
lualatex -interaction=nonstopmode -halt-on-error main.tex
lualatex -interaction=nonstopmode -halt-on-error main.tex
```

The second pass resolves the table of contents and cross-references.

Required TeX packages include LuaTeX-ja / `ltjsbook`, `luatexja-fontspec`, `geometry`, `amsmath`, `graphicx`, `hyperref`, `bookmark`, and `enumitem`.
