# LaTeX manuscript source

LaTeX source for **AI と物理学の系譜**.

## Structure

- `main.tex` — base manuscript without inserted figures
- `chapters/preface.tex` — preface
- `chapters/chapter01.tex` ... `chapters/chapter17.tex` — chapter source files
- `chapters/references/chapter01_refs.tex` ... `chapter17_refs.tex` — chapter-end references
- `build_figured_version.py` — generates a figure-inserted manuscript
- `../figures/pdf/` — committed grayscale figure PDFs used by local builds

The manuscript does not use BibTeX or Biber. References are ordinary LaTeX source files.

## Important: `main.tex` has no figures

Compiling `main.tex` directly produces the pre-figure manuscript.

For the version with all 52 figures and Japanese captions, first generate
`generated/main_with_figures.tex`, then compile that file.

## Windows 11 build

Make sure you are on the `figure-layout-prototype` branch and have the latest files:

```powershell
git switch figure-layout-prototype
git pull
cd latex
```

Then either run the batch file:

```powershell
build_figured_windows.bat
```

or run the commands manually:

```powershell
python build_figured_version.py
lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
```

The resulting PDF is:

```text
latex/main_with_figures.pdf
```

The build script copies the committed grayscale PDFs from `figures/pdf/` into
`latex/generated/figures/`, so Ghostscript is not required just to compile the
figure-inserted manuscript locally.

## Base manuscript build

To compile the text-only manuscript intentionally:

```bash
cd latex
lualatex -interaction=nonstopmode -halt-on-error main.tex
lualatex -interaction=nonstopmode -halt-on-error main.tex
```

The document class is `ltjsbook`, so LuaLaTeX is required. Required packages
include LuaTeX-ja / `ltjsbook`, `luatexja-fontspec`, `geometry`, `amsmath`,
`graphicx`, `hyperref`, `bookmark`, and `enumitem`.
