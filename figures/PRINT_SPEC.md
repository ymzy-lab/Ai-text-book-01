# Figure asset and print specification

The textbook figures for **AI と物理学の系譜** are intended for monochrome printing.

## Asset roles

- `figures/pdf/*.pdf` — **primary LaTeX / production assets**.
  - Generated directly by Matplotlib.
  - Embedded in LuaLaTeX without an EPS conversion step.
  - `pdf.fonttype = 42` is used so TrueType/OpenType glyphs are embedded rather than intentionally converted to Type 3.
  - CI must not rewrite these PDFs through Ghostscript, because preserving text/font structure is part of the production requirement.
- `figures/svg/*.svg` — **editable vector masters**.
  - `svg.fonttype = "none"` keeps ordinary labels as SVG `<text>` wherever Matplotlib permits.
  - Intended for Illustrator/Inkscape editing and editorial corrections.
- `figures/eps/*.eps` — **optional EPS side output**.
  - Retained for compatibility, experimentation, and archival preference.
  - EPS is not used by the LaTeX manuscript build.
  - `ps.fonttype = 3` may be used here for robust PostScript rendering; EPS editability is not a production requirement.

## Mandatory monochrome and typography rule

- Production PDF and editable SVG assets must be black-and-white or grayscale only.
- **Primary text is black (`#000000`)** for print readability.
- **Secondary / auxiliary text may use dark gray (`#555555`)**.
- Lines, markers, grids, fills, and other graphical structure may use grayscale values.
- The compiled manuscript PDF must contain no chromatic cyan, magenta, or yellow ink coverage.
- Conceptual categories should be distinguished by grayscale value, line style, line weight, marker shape, hatch/pattern, or annotation rather than color alone.
- EPS side output is also normalized/validated as grayscale, but EPS must never be used as an intermediate source for the production PDF.

## CI policy

`.github/workflows/generate-figures.yml`:
- generates PDF, SVG, and EPS directly from Matplotlib;
- keeps the **native PDF** as the production asset;
- validates PDF grayscale ink coverage;
- verifies that representative PDF text survives as text;
- verifies that SVG files contain editable `<text>` elements, grayscale-only colors, and only black/dark-gray text fills;
- validates EPS separately.

`.github/workflows/compile-figured-latex.yml`:
- embeds `figures/pdf/*.pdf` directly;
- does not convert EPS to PDF;
- validates the final manuscript as monochrome.
