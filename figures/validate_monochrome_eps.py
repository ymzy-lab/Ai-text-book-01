"""Validate that textbook EPS output is monochrome and remains vector PostScript."""
from pathlib import Path
import re

EPS_DIR = Path(__file__).resolve().parent / 'eps'
RGB_RE = re.compile(r'(?m)^\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+setrgbcolor\s*$')
FORBIDDEN_RASTER = ('colorimage', ' image\n', 'imagemask')


def main():
    files = sorted(EPS_DIR.glob('fig*.eps'))
    if len(files) != 52:
        raise RuntimeError('Expected 52 EPS files, found {}'.format(len(files)))
    errors = []
    for path in files:
        text = path.read_text(encoding='latin-1')
        if '%%MonochromePublicationStyle: true' not in text:
            errors.append('{}: missing monochrome marker'.format(path.name))
        for match in RGB_RE.finditer(text):
            r, g, b = map(float, match.groups())
            if max(r, g, b) - min(r, g, b) > 1e-6:
                errors.append('{}: chromatic RGB remains'.format(path.name))
                break
        lower = text.lower()
        for token in FORBIDDEN_RASTER:
            if token in lower:
                errors.append('{}: possible raster operator {}'.format(path.name, token.strip()))
                break
    if errors:
        raise RuntimeError('\n'.join(errors))
    print('Validated {} monochrome vector EPS figures.'.format(len(files)))


if __name__ == '__main__':
    main()
