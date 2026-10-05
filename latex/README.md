# LaTeX manuscript source

LaTeX source for **AI と物理学の系譜**.

## Important

- `main.tex` is the base/text-only manuscript.
- `generated/main_with_figures.tex` is the ready-to-compile manuscript with all 52 figures and captions.
- `../figures/pdf/` contains the committed grayscale figure PDFs.

**Python is not required on the local PC to compile the figured manuscript.**
Python is used only by GitHub Actions / maintainers to regenerate the derived
`generated/*.tex` sources when the manuscript layout changes.

## Windows 11: build the figured manuscript

Update the branch first:

```powershell
git fetch origin
git switch figure-layout-prototype
git pull
cd latex
```

Then run:

```powershell
build_figured_windows.bat
```

or manually:

```powershell
lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
lualatex -interaction=nonstopmode -halt-on-error generated/main_with_figures.tex
```

The result is:

```text
latex\main_with_figures.pdf
```

Do not compile `main.tex` when you want the illustrated version.

## Base manuscript

To intentionally build the text-only manuscript:

```powershell
lualatex -interaction=nonstopmode -halt-on-error main.tex
lualatex -interaction=nonstopmode -halt-on-error main.tex
```

The document class is `ltjsbook`, so LuaLaTeX is required.
