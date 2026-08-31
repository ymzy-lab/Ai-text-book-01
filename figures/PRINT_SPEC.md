# Figure print specification

The textbook figures for **AI と物理学の系譜** are intended for monochrome printing.

## Mandatory color rule

- Final figure assets must be **black-and-white or grayscale only**.
- No RGB/CMYK chromatic color may remain in the print-ready EPS or in the compiled manuscript PDF.
- Multiple conceptual categories that were previously distinguished by color must instead be distinguished by grayscale value, line style, line weight, marker shape, hatch/pattern, or annotation.
- The editable source code may retain semantic color constants for development convenience, but the canonical `figures/eps/*.eps` assets are normalized to DeviceGray by CI before they are committed.
- The figure-inserted manuscript CI independently converts figures to DeviceGray and rejects any final PDF with nonzero cyan, magenta, or yellow ink coverage.

This specification is enforced by:

- `.github/workflows/generate-figures.yml`
- `.github/workflows/compile-figured-latex.yml`
