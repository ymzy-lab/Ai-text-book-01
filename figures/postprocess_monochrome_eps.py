"""Convert generated textbook EPS files to print-safe monochrome vectors.

The source generators remain unchanged and reproducible.  This post-processes only
PostScript drawing commands: RGB colours become neutral gray and the three original
semantic colours are translated to different line grammars.  No rasterization is
performed.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
EPS_DIR = ROOT / 'eps'

RGB_RE = re.compile(r'(?m)^\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+setrgbcolor\s*$')

# Rounded RGB values written by Matplotlib for the original semantic palette.
SEMANTIC = {
    (0.192, 0.353, 0.490): ('0.10 setgray', '[] 0 setdash'),       # PHYS
    (0.639, 0.306, 0.306): ('0.30 setgray', '[6 3] 0 setdash'),   # AI
    (0.690, 0.478, 0.165): ('0.48 setgray', '[7 2 1.5 2] 0 setdash'), # ACCENT
    (0.125, 0.145, 0.169): ('0.08 setgray', '[] 0 setdash'),      # DARK
    (0.408, 0.443, 0.482): ('0.38 setgray', '[] 0 setdash'),      # MID
    (0.851, 0.871, 0.890): ('0.78 setgray', '[] 0 setdash'),      # LIGHT
    (0.953, 0.961, 0.969): ('0.93 setgray', '[] 0 setdash'),      # PALE
}


def nearest_semantic(r, g, b):
    best = None
    best_d = 999.0
    for rgb, commands in SEMANTIC.items():
        d = sum((a-bb)**2 for a, bb in zip((r, g, b), rgb))
        if d < best_d:
            best_d = d
            best = commands
    return best if best_d < 0.0025 else None


def convert_match(match):
    r, g, b = map(float, match.groups())
    semantic = nearest_semantic(r, g, b)
    if semantic:
        gray_cmd, dash_cmd = semantic
        return '{}\n{}'.format(dash_cmd, gray_cmd)
    y = 0.2126*r + 0.7152*g + 0.0722*b
    if y < 0.20:
        y = 0.08
    elif y > 0.94:
        y = 1.0
    else:
        y = 0.10 + 0.82*y
    return '[] 0 setdash\n{:.3f} setgray'.format(y)


def process(path):
    text = path.read_text(encoding='latin-1')
    text = RGB_RE.sub(convert_match, text)
    # Avoid ultra-thin hairlines that disappear in print.
    text = re.sub(r'(?m)^0\.5 setlinewidth$', '0.65 setlinewidth', text)
    text = re.sub(r'(?m)^0\.6 setlinewidth$', '0.70 setlinewidth', text)
    # Explicit marker for future maintenance and validation.
    marker = '%%MonochromePublicationStyle: true\n'
    if marker not in text:
        text = text.replace('%%EndComments\n', '%%EndComments\n' + marker, 1)
    path.write_text(text, encoding='latin-1')


def main():
    files = sorted(EPS_DIR.glob('fig*.eps'))
    if len(files) != 52:
        raise RuntimeError('Expected 52 EPS files, found {}'.format(len(files)))
    for path in files:
        process(path)
    print('Post-processed {} editable EPS figures to monochrome.'.format(len(files)))


if __name__ == '__main__':
    main()
