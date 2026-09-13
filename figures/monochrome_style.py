from pathlib import Path
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.collections import Collection
from matplotlib.text import Text

OUT = Path(__file__).resolve().parent / 'eps'
OUT.mkdir(parents=True, exist_ok=True)

BLACK = '#111111'
DARK = '#222222'
MID = '#666666'
LIGHT = '#B8B8B8'
PALE = '#F1F1F1'
WHITE = '#FFFFFF'

OLD = {
    '#315A7D': ('PHYS', BLACK),
    '#A34E4E': ('AI', '#4A4A4A'),
    '#B07A2A': ('ACCENT', '#777777'),
    '#20252B': ('DARK', DARK),
    '#68717B': ('MID', MID),
    '#D9DEE3': ('LIGHT', LIGHT),
    '#F3F5F7': ('PALE', PALE),
}


def kind_and_gray(color):
    try:
        h = mcolors.to_hex(color, keep_alpha=False).upper()
    except Exception:
        return None, color
    if h in OLD:
        return OLD[h]
    try:
        r, g, b, a = mcolors.to_rgba(color)
        y = 0.2126*r + 0.7152*g + 0.0722*b
        if y < 0.22:
            y = 0.10
        elif y > 0.93:
            y = 1.0
        else:
            y = 0.12 + 0.80*y
        return None, (y, y, y, a)
    except Exception:
        return None, color


def configure():
    mpl.rcParams.update({
        'ps.fonttype': 3,
        'pdf.fonttype': 42,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Noto Sans CJK JP', 'Noto Sans CJK JP Regular', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        'figure.dpi': 150,
        'figure.facecolor': WHITE,
        'axes.facecolor': WHITE,
        'savefig.facecolor': WHITE,
        'text.color': BLACK,
        'axes.labelcolor': BLACK,
        'axes.edgecolor': '#555555',
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'axes.titlesize': 10,
        'axes.titleweight': 'bold',
        'axes.labelsize': 9,
        'legend.fontsize': 8,
        'lines.linewidth': 1.35,
        'patch.linewidth': 1.0,
        'hatch.linewidth': 0.55,
    })


def polish(fig):
    fig.patch.set_facecolor(WHITE)
    for ax in fig.axes:
        ax.set_facecolor(WHITE)
        ax.tick_params(colors='#333333', width=0.8, labelsize=8.5)
        for spine in ax.spines.values():
            spine.set_color('#555555')
            spine.set_linewidth(0.8)
        for gl in list(ax.get_xgridlines()) + list(ax.get_ygridlines()):
            gl.set_color('#D0D0D0')
            gl.set_linewidth(0.5)
            gl.set_linestyle(':')

    for obj in fig.findobj():
        if isinstance(obj, Line2D):
            kind, gray = kind_and_gray(obj.get_color())
            obj.set_color(gray)
            if kind == 'PHYS':
                obj.set_linestyle('-')
                obj.set_linewidth(max(1.35, obj.get_linewidth()))
            elif kind == 'AI':
                obj.set_linestyle('--')
                obj.set_linewidth(max(1.35, obj.get_linewidth()))
            elif kind == 'ACCENT':
                obj.set_linestyle('-.')
                obj.set_linewidth(max(1.55, obj.get_linewidth()))
        elif isinstance(obj, Patch):
            ek, eg = kind_and_gray(obj.get_edgecolor())
            fk, fg = kind_and_gray(obj.get_facecolor())
            obj.set_edgecolor(eg)
            obj.set_facecolor(fg)
            obj.set_alpha(1.0)
        elif isinstance(obj, Collection):
            try:
                obj.set_edgecolors([kind_and_gray(c)[1] for c in obj.get_edgecolors()])
                obj.set_facecolors([kind_and_gray(c)[1] for c in obj.get_facecolors()])
                obj.set_alpha(1.0)
            except Exception:
                pass
        elif isinstance(obj, Text):
            kind, gray = kind_and_gray(obj.get_color())
            obj.set_color(gray)
            if kind in ('AI', 'ACCENT'):
                obj.set_fontweight('bold')

    if getattr(fig, '_suptitle', None) is not None:
        fig._suptitle.set_fontsize(13)
        fig._suptitle.set_fontweight('bold')
        fig._suptitle.set_color(BLACK)


def save_eps(fig, path):
    polish(fig)
    fig.savefig(OUT / Path(path).name, format='eps', bbox_inches='tight', pad_inches=0.10, facecolor=WHITE, transparent=False)
    plt.close(fig)
