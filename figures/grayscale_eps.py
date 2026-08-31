"""Convert Matplotlib EPS color operators to grayscale without rewriting geometry.

This preserves the original BoundingBox, Type-3 glyphs, paths, and editable vector
structure. Only explicit ``r g b setrgbcolor`` operators are replaced by
``g setgray``.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

RGB_RE = re.compile(
    r"(?P<r>(?:\d+(?:\.\d*)?|\.\d+))\s+"
    r"(?P<g>(?:\d+(?:\.\d*)?|\.\d+))\s+"
    r"(?P<b>(?:\d+(?:\.\d*)?|\.\d+))\s+setrgbcolor"
)

# Semantic palette used by the figure generators.  The chosen gray levels are
# intentionally more separated than raw luminance conversion so categories
# remain distinguishable in monochrome print.
PALETTE = {
    (0x31 / 255, 0x5A / 255, 0x7D / 255): 0.25,  # PHYS
    (0xA3 / 255, 0x4E / 255, 0x4E / 255): 0.48,  # AI
    (0xB0 / 255, 0x7A / 255, 0x2A / 255): 0.68,  # ACCENT
    (0x20 / 255, 0x25 / 255, 0x2B / 255): 0.10,  # DARK
    (0x68 / 255, 0x71 / 255, 0x7B / 255): 0.43,  # MID
    (0xD9 / 255, 0xDE / 255, 0xE3 / 255): 0.82,  # LIGHT
    (0xF3 / 255, 0xF5 / 255, 0xF7 / 255): 0.95,  # PALE
    (0xDC / 255, 0xE7 / 255, 0xF0 / 255): 0.88,  # pale blue helper
}


def nearest_palette_gray(r: float, g: float, b: float) -> float | None:
    best = None
    best_d2 = 1e9
    for (pr, pg, pb), gray in PALETTE.items():
        d2 = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d2 < best_d2:
            best_d2 = d2
            best = gray
    # Matplotlib commonly serializes RGB values to three decimals.
    return best if best_d2 <= 0.003 ** 2 * 3 else None


def to_gray(r: float, g: float, b: float) -> float:
    semantic = nearest_palette_gray(r, g, b)
    if semantic is not None:
        return semantic
    # Rec. 709 relative luminance for any colors outside the house palette.
    return max(0.0, min(1.0, 0.2126 * r + 0.7152 * g + 0.0722 * b))


def convert_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        r = float(match.group("r"))
        g = float(match.group("g"))
        b = float(match.group("b"))
        gray = to_gray(r, g, b)
        count += 1
        return f"{gray:.4f} setgray"

    return RGB_RE.sub(repl, text), count


def convert_file(path: Path) -> int:
    original = path.read_text(encoding="latin-1")
    converted, count = convert_text(original)
    path.write_text(converted, encoding="latin-1")
    return count


def main() -> None:
    eps_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "eps"
    paths = sorted(eps_dir.glob("*.eps"))
    if not paths:
        raise SystemExit(f"No EPS files found in {eps_dir}")

    total = 0
    for path in paths:
        count = convert_file(path)
        total += count
        print(f"{path.name}: converted {count} RGB operators")

    if len(paths) != 52:
        raise SystemExit(f"Expected 52 EPS figures, found {len(paths)}")
    if total == 0:
        raise SystemExit("No RGB color operators were converted")
    print(f"Converted {len(paths)} EPS files; {total} RGB operators -> grayscale")


if __name__ == "__main__":
    main()
