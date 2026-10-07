"""Generate grayscale PDF/SVG textbook figures plus optional EPS side output."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Arc

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "eps"      # optional EPS side output
SVG_OUT = ROOT / "svg"  # editable vector master
PDF_OUT = ROOT / "pdf"  # primary LaTeX / production asset
for _dir in (OUT, SVG_OUT, PDF_OUT):
    _dir.mkdir(parents=True, exist_ok=True)

mpl.rcParams['ps.fonttype'] = 3      # EPS side output: robust PostScript glyph outlines
mpl.rcParams['pdf.fonttype'] = 42     # production PDF: embedded TrueType/OpenType fonts
mpl.rcParams['svg.fonttype'] = 'none' # editable SVG: preserve ordinary text elements
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Sans CJK JP Regular', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['figure.dpi'] = 150

TEXT = '#000000'
SUBTEXT = '#555555'
PHYS = '#545454'
AI = '#606060'
ACCENT = '#808080'
DARK = '#404040'
MID = '#707070'
LIGHT = '#DDDDDD'
PALE = '#F5F5F5'
mpl.rcParams['text.color'] = TEXT
mpl.rcParams['axes.labelcolor'] = TEXT
mpl.rcParams['axes.titlecolor'] = TEXT
mpl.rcParams['xtick.color'] = TEXT
mpl.rcParams['ytick.color'] = TEXT

def save_assets(fig, name):
    stem = Path(name).stem
    fig.savefig(OUT / f"{stem}.eps", format='eps', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(SVG_OUT / f"{stem}.svg", format='svg', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(PDF_OUT / f"{stem}.pdf", format='pdf', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


def arrow(ax, xy1, xy2, color=DARK, lw=1.4, ms=12, style='-|>'):
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms, linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p

def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha='left', va='top', fontsize=9, fontweight='bold', color=SUBTEXT)

def fig06_field_div_rot():
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
    fig.suptitle('ベクトル場の直感：湧き出し（div）と渦（rot）', fontsize=14, fontweight='bold', color=TEXT)
    x = np.linspace(-1.8, 1.8, 13)
    y = np.linspace(-1.8, 1.8, 13)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2) + 1e-6
    ax = axs[0]
    panel_label(ax, '(a) div > 0：湧き出し')
    U = X / (R + 0.2); V = Y / (R + 0.2)
    ax.quiver(X, Y, U, V, color=PHYS, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=ACCENT, facecolor='none', lw=2))
    ax.text(0, -2.15, '正の発散：場が外へ広がる', ha='center', fontsize=9, color=TEXT)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    ax = axs[1]
    panel_label(ax, '(b) div < 0：吸い込み')
    U = -X / (R + 0.2); V = -Y / (R + 0.2)
    ax.quiver(X, Y, U, V, color=AI, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=ACCENT, facecolor='none', lw=2))
    ax.text(0, -2.15, '負の発散：場が内へ集まる', ha='center', fontsize=9, color=TEXT)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    ax = axs[2]
    panel_label(ax, '(c) rot ≠ 0：渦')
    U = -Y / (R + 0.35); V = X / (R + 0.35)
    ax.quiver(X, Y, U, V, color=ACCENT, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=DARK, facecolor='none', lw=2))
    arc = Arc((0, 0), 2.0, 2.0, theta1=35, theta2=320, lw=1.8, color=DARK)
    ax.add_patch(arc)
    arrow(ax, (0.45, 0.82), (0.2, 0.96), color=DARK, lw=1.2, ms=10)
    ax.text(0, -2.15, '回転成分：場がぐるぐる回る', ha='center', fontsize=9, color=TEXT)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    fig.tight_layout(rect=[0, 0.02, 1, 0.90])
    save_assets(fig, 'fig06_field_div_rot.eps')

def fig07_em_wave_attention():
    """Contrast local finite-speed wave propagation with global attention lookup."""
    fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.7), gridspec_kw={'width_ratios':[1, 1]})
    fig.suptitle('離れた場所へ情報が届く仕組み：電磁波とSelf-Attention',
                 fontsize=14, fontweight='bold', color=TEXT)

    # ---------------------------------------------------------
    # (a) Electromagnetic wave: a local field disturbance moves
    # through space at finite speed.  Three snapshots make the
    # propagation itself visually explicit.
    # ---------------------------------------------------------
    ax = axs[0]
    panel_label(ax, '(a) 物理：電磁波は空間を伝播する')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    xx = np.linspace(0.4, 9.5, 700)
    centers = [2.0, 4.5, 7.0]
    rows = [5.0, 3.45, 1.9]
    labels = [r'$t_0$', r'$t_1$', r'$t_2$']

    for center, y0, lab in zip(centers, rows, labels):
        packet = 0.62 * np.exp(-((xx-center)/0.95)**2) * np.sin(5.0*(xx-center))
        ax.plot([0.55, 9.35], [y0, y0], color=LIGHT, lw=0.9, zorder=0)
        ax.plot(xx, y0 + packet, color=PHYS, lw=2.0, zorder=2)
        ax.text(0.18, y0, lab, va='center', fontsize=9, color=TEXT)

    # Finite-speed propagation cue.
    arrow(ax, (1.25, 0.75), (8.85, 0.75), color=DARK, lw=1.6, ms=12)
    ax.text(5.05, 0.35, '局所的な場の変化が有限速度 c で右へ進む',
            ha='center', fontsize=9, color=TEXT)
    ax.text(9.05, 0.75, '空間 x', va='center', fontsize=8.5, color=SUBTEXT)

    # A fixed observation point emphasizes that the signal arrives later.
    ax.plot([8.35, 8.35], [1.25, 5.55], color=MID, lw=1.0, ls=':')
    ax.text(8.35, 5.78, '観測点', ha='center', fontsize=8.5, color=SUBTEXT)

    # ---------------------------------------------------------
    # (b) Self-Attention: one query token directly gathers
    # information from all tokens in the same layer.
    # ---------------------------------------------------------
    ax = axs[1]
    panel_label(ax, '(b) AI：Self-Attentionは全体を参照する')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    xs = np.linspace(1.0, 9.0, 6)
    words = ['The', 'universe', 'is', 'written', 'in', 'math']
    query_idx = 3
    weights = np.array([0.05, 0.27, 0.08, 0.18, 0.07, 0.35])

    # Input tokens.
    for i, (x0, word) in enumerate(zip(xs, words)):
        edge = DARK if i == query_idx else MID
        lw = 2.0 if i == query_idx else 1.2
        face = '#E8E8E8' if i == query_idx else 'white'
        rect = Rectangle((x0-0.62, 4.75), 1.24, 0.82,
                         facecolor=face, edgecolor=edge, lw=lw)
        ax.add_patch(rect)
        ax.text(x0, 5.16, word, ha='center', va='center', fontsize=8.5, color=TEXT)

    ax.text(xs[query_idx], 5.95, 'query = written',
            ha='center', fontsize=9, color=TEXT, fontweight='bold')

    # Output representation for the query token.
    out_x, out_y = xs[query_idx], 1.35
    out = Rectangle((out_x-1.05, out_y-0.42), 2.10, 0.84,
                    facecolor=PALE, edgecolor=DARK, lw=1.6)
    ax.add_patch(out)
    ax.text(out_x, out_y, 'written の\n更新後表現',
            ha='center', va='center', fontsize=8.7, color=TEXT)

    # Each token contributes to the query output; line width encodes attention weight.
    for x0, w in zip(xs, weights):
        lw = 0.8 + 4.0*w
        col = DARK if w >= 0.18 else MID
        p = FancyArrowPatch(
            (x0, 4.70), (out_x, out_y+0.48),
            arrowstyle='-|>', mutation_scale=9,
            linewidth=lw, color=col,
            connectionstyle='arc3,rad=0.0',
            shrinkA=2, shrinkB=4,
        )
        ax.add_patch(p)

    ax.text(5.0, 0.42,
            '全トークンから重み付きで情報を集める（太い線ほど強く参照）',
            ha='center', fontsize=8.6, color=TEXT)

    # Make the intended analogy and the crucial difference explicit.
    fig.text(
        0.5, 0.015,
        '共通点：離れた位置の情報が影響する　／　違い：電磁波＝局所・有限速度、Attention＝1層で全体参照',
        ha='center', fontsize=9.2, color=TEXT
    )

    fig.tight_layout(rect=[0, 0.075, 1, 0.91])
    save_assets(fig, 'fig07_em_wave_attention.eps')

def fig08_simple_harmonic_motion():
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.9))
    fig.suptitle('単振動の3つの顔：復元力・時間変化・ポテンシャル', fontsize=14, fontweight='bold', color=TEXT)
    ax = axs[0]
    panel_label(ax, '(a) バネと復元力')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
    ax.plot([0.8, 0.8], [1.0, 5.0], color=DARK, lw=3)

    # Horizontal spring with upright, evenly spaced zig-zags.
    spring_start = 0.8
    coil_start = 1.15
    coil_end = 2.70
    spring_y = 3.0
    amp = 0.38
    turns = 7

    zigx = [spring_start, coil_start]
    zigy = [spring_y, spring_y]
    dx = (coil_end - coil_start) / (2 * turns)
    for j in range(1, 2 * turns):
        zigx.append(coil_start + j * dx)
        zigy.append(spring_y + (amp if j % 2 else -amp))
    zigx.extend([coil_end, 3.0])
    zigy.extend([spring_y, spring_y])

    ax.plot(zigx, zigy, color=PHYS, lw=2)
    ax.add_patch(Rectangle((3.0, 2.2), 1.6, 1.6, facecolor=PALE, edgecolor=PHYS, lw=1.8))
    ax.text(3.8, 3.0, 'm', ha='center', va='center', fontsize=11, color=TEXT)
    ax.plot([2.6, 3.0], [3.0, 3.0], color=PHYS, lw=2)
    ax.plot([3.8, 5.6], [3.0, 3.0], color=LIGHT, lw=1.2, ls='--')
    arrow(ax, (5.0, 3.0), (4.0, 3.0), color=AI, lw=1.6, ms=12)
    ax.text(5.1, 3.2, '復元力  F = -kx', fontsize=9, color=TEXT)
    ax.text(3.85, 1.45, '平衡点から離れるほど\n元へ戻す力が働く', ha='center', fontsize=9, color=TEXT)
    ax = axs[1]
    panel_label(ax, '(b) 位置の時間変化')
    t = np.linspace(0, 4*np.pi, 400)
    x = np.cos(t)
    ax.plot(t, x, color=PHYS, lw=2)
    ax.axhline(0, color=LIGHT, lw=1)
    for xpos in [np.pi/2, 3*np.pi/2, 5*np.pi/2, 7*np.pi/2]: ax.axvline(xpos, color=LIGHT, lw=0.8, ls=':')
    ax.set_xlabel('時間  t'); ax.set_ylabel('位置  x(t)')
    ax.grid(color=LIGHT, linewidth=0.6)
    ax.text(np.pi, 1.08, '周期 T ごとに同じ運動をくり返す', ha='center', fontsize=9, color=TEXT)
    ax = axs[2]
    panel_label(ax, '(c) エネルギーの谷')
    xp = np.linspace(-2.2, 2.2, 300); V = 0.55*xp**2
    ax.plot(xp, V, color=ACCENT, lw=2)
    for p in [-1.4, 1.4]:
        ax.plot(p, 0.55*p**2, 'o', ms=6, color=PHYS)
        arrow(ax, (p, 0.55*p**2), (0.6*p, 0.55*(0.6*p)**2), color=PHYS, lw=1.2, ms=10)
    ax.set_xlabel('変位  x'); ax.set_ylabel('ポテンシャル  V(x)')
    ax.grid(color=LIGHT, linewidth=0.6)
    ax.text(0, 2.25, '谷底が安定点', ha='center', fontsize=9, color=TEXT)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_assets(fig, 'fig08_simple_harmonic_motion.eps')

def fig09_interference_standing_wave():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.0))
    fig.suptitle('重ね合わせの原理：干渉と定在波', fontsize=14, fontweight='bold', color=TEXT)
    ax = axs[0]
    panel_label(ax, '(a) 2つの波の干渉')
    x = np.linspace(0, 4*np.pi, 500)
    y1 = np.sin(x); y2 = np.sin(x + 0.7); y3 = y1 + y2
    ax.plot(x, y1, color=PHYS, lw=1.7, label='波1')
    ax.plot(x, y2, color=AI, lw=1.7, ls='--', label='波2')
    ax.plot(x, y3, color=ACCENT, lw=2.2, label='合成波')
    ax.axhline(0, color=LIGHT, lw=1)
    ax.set_xlabel('位置'); ax.set_ylabel('振幅')
    ax.grid(color=LIGHT, linewidth=0.6)
    ax.legend(frameon=False, fontsize=8, loc='upper right')
    ax.text(2.0, 1.85, '位相がそろうと強め合い，ずれると弱め合う', fontsize=9, color=TEXT)
    ax = axs[1]
    panel_label(ax, '(b) 定在波と腹・節')
    x = np.linspace(0, np.pi, 500)
    for phase in np.linspace(0, 2*np.pi, 5):
        y = 0.9*np.sin(2*x)*np.cos(phase)
        ax.plot(x, y, color=LIGHT, lw=1)
    env = 0.9*np.abs(np.sin(2*x))
    ax.plot(x, env, color=ACCENT, lw=2); ax.plot(x, -env, color=ACCENT, lw=2)
    for node in [0, np.pi/2, np.pi]:
        ax.plot(node, 0, 'o', ms=5, color=AI); ax.text(node, -1.12, '節', ha='center', fontsize=8.8, color=TEXT)
    for antinode in [np.pi/4, 3*np.pi/4]: ax.text(antinode, 1.02, '腹', ha='center', fontsize=9, color=TEXT)
    ax.axhline(0, color=LIGHT, lw=1)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel('位置'); ax.set_ylabel('振幅')
    ax.grid(color=LIGHT, linewidth=0.6)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_assets(fig, 'fig09_interference_standing_wave.eps')

def fig10_fourier_decomposition():
    fig = plt.figure(figsize=(11.8, 7.0))
    fig.suptitle(
        'フーリエ分解：複雑な波は単純な波の足し合わせ',
        fontsize=14,
        fontweight='bold',
        color=TEXT
    )

    gs = fig.add_gridspec(
        4, 2,
        width_ratios=[1.45, 1.0],
        height_ratios=[1.15, 0.8, 0.8, 0.8],
        wspace=0.28,
        hspace=0.34
    )

    ax_sum = fig.add_subplot(gs[0, 0])
    ax_c1  = fig.add_subplot(gs[1, 0], sharex=ax_sum)
    ax_c2  = fig.add_subplot(gs[2, 0], sharex=ax_sum)
    ax_c3  = fig.add_subplot(gs[3, 0], sharex=ax_sum)
    ax_sp  = fig.add_subplot(gs[:, 1])

    x = np.linspace(0, 2*np.pi, 800)

    # Fourier components
    A1, A2, A4 = 1.10, 0.55, 0.35
    p1, p2, p4 = 0.00, 0.60, -0.80

    comp1 = A1 * np.sin(x + p1)
    comp2 = A2 * np.sin(2*x + p2)
    comp3 = A4 * np.sin(4*x + p4)
    orig  = comp1 + comp2 + comp3

    # (a) Original waveform
    panel_label(ax_sum, '(a) 合成された複雑な波')
    ax_sum.plot(x, orig, color=DARK, lw=2.3)
    ax_sum.set_ylabel('振幅')
    ax_sum.grid(color=LIGHT, linewidth=0.6)
    ax_sum.text(
        np.pi, 1.65,
        '観測された信号  =  下の3成分の足し合わせ',
        ha='center',
        fontsize=9,
        color=TEXT
    )
    ax_sum.set_xlim(0, 2*np.pi)
    ax_sum.set_ylim(-1.9, 1.9)
    ax_sum.set_xticklabels([])

    # (b) Components shown separately
    panel_label(ax_c1, '(b) 単純な波への分解')

    def style_component_axis(ax, y, color, label, amp_text):
        ax.plot(x, y, color=color, lw=1.9)
        ax.axhline(0, color=LIGHT, lw=0.8)
        ax.set_ylim(-1.2, 1.2)
        ax.grid(color=LIGHT, linewidth=0.45)
        ax.set_ylabel(label, rotation=0, labelpad=18, va='center')
        ax.text(
            2*np.pi*0.985, 0.90,
            amp_text,
            ha='right',
            va='top',
            fontsize=8.5,
            color=SUBTEXT
        )

    style_component_axis(ax_c1, comp1, PHYS, 'f',  'A=1.10,  φ=0')
    style_component_axis(ax_c2, comp2, AI,   '2f', 'A=0.55,  φ=+0.60')
    style_component_axis(ax_c3, comp3, ACCENT, '4f', 'A=0.35,  φ=-0.80')

    ax_c1.set_xticklabels([])
    ax_c2.set_xticklabels([])
    ax_c3.set_xlabel('時間または位置')
    ax_c3.set_ylabel('4f', rotation=0, labelpad=18, va='center')

    ax_c1.text(
        -0.08, -0.36, '+',
        transform=ax_c1.transAxes,
        fontsize=16,
        fontweight='bold',
        color=TEXT,
        ha='center',
        va='center'
    )
    ax_c2.text(
        -0.08, -0.36, '+',
        transform=ax_c2.transAxes,
        fontsize=16,
        fontweight='bold',
        color=TEXT,
        ha='center',
        va='center'
    )

    # (c) Spectrum
    panel_label(ax_sp, '(c) 周波数スペクトル')
    freq = np.array([1, 2, 4])
    amp  = np.array([A1, A2, A4])
    phase = ['φ=0', 'φ=+0.60', 'φ=-0.80']

    ax_sp.vlines(freq, 0, amp, colors=[PHYS, AI, ACCENT], linewidth=3)
    ax_sp.plot(freq, amp, 'o', color=DARK, ms=5)
    ax_sp.set_xlim(0.5, 4.5)
    ax_sp.set_ylim(0, 1.3)
    ax_sp.set_xticks([1, 2, 3, 4])
    ax_sp.set_xlabel('周波数')
    ax_sp.set_ylabel('振幅')
    ax_sp.grid(color=LIGHT, linewidth=0.6)

    for f, a, ph in zip(freq, amp, phase):
        ax_sp.text(f, a + 0.06, ph, ha='center', fontsize=8.5, color=TEXT)

    ax_sp.text(
        2.5, 1.16,
        'どの周波数がどれだけ混ざっているかを見る',
        ha='center',
        fontsize=8.8,
        color=TEXT
    )

    fig.text(
        0.5, 0.02,
        'ポイント：波形の形は「振幅」と「位相」をもつ複数の正弦波の和で決まる',
        ha='center',
        fontsize=9.4,
        color=TEXT
    )

    fig.tight_layout(rect=[0, 0.04, 1, 0.93])
    save_assets(fig, 'fig10_fourier_decomposition.eps')

def fig11_minkowski_time_dilation():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.3))
    fig.suptitle('特殊相対論の直感：光時計とミンコフスキー図', fontsize=14, fontweight='bold', color=TEXT)
    ax = axs[0]
    panel_label(ax, '(a) 光時計')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    ax.add_patch(Rectangle((0.9, 1.2), 2.6, 4.2, facecolor=PALE, edgecolor=PHYS, lw=1.5))
    ax.plot([2.2, 2.2], [1.6, 5.0], color=PHYS, lw=1.5)
    ax.plot([1.6, 2.8], [5.0, 5.0], 'o', color=PHYS, ms=4)
    arrow(ax, (2.2, 1.8), (2.2, 4.8), color=PHYS, lw=1.3, ms=10)
    arrow(ax, (2.2, 4.8), (2.2, 1.8), color=PHYS, lw=1.3, ms=10)
    ax.text(2.2, 0.7, '静止系：光は上下に往復', ha='center', fontsize=9, color=TEXT)
    ax.add_patch(Rectangle((5.2, 1.2), 3.2, 4.2, facecolor=PALE, edgecolor=AI, lw=1.5))
    ax.plot([5.9, 7.9], [1.6, 5.0], color=AI, lw=1.5)
    ax.plot([5.9, 7.9], [5.0, 1.6], color=AI, lw=1.5)
    arrow(ax, (5.3, 5.8), (8.3, 5.8), color=DARK, lw=1.2, ms=10)
    ax.text(6.8, 6.1, '運動', fontsize=9, color=TEXT)
    ax.text(6.8, 0.7, '移動系：光の経路が斜めに長くなる', ha='center', fontsize=9, color=TEXT)
    ax = axs[1]
    panel_label(ax, '(b) ミンコフスキー図')
    ax.set_xlim(-1.2, 5.5); ax.set_ylim(-0.2, 5.5)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xlabel('空間  x'); ax.set_ylabel('時間  ct')
    ax.plot([0, 0], [0, 5.2], color=DARK, lw=1.5); ax.plot([0, 5.2], [0, 0], color=DARK, lw=1.5)
    ax.plot([0, 4.8], [0, 4.8], color=LIGHT, lw=1.4); ax.plot([0, -1.0], [0, 1.0], color=LIGHT, lw=1.4)
    ax.text(4.55, 4.95, '光', fontsize=9, color=SUBTEXT); ax.text(-0.92, 1.12, '光', fontsize=9, color=SUBTEXT)
    ax.plot([0, 0], [0, 5.0], color=PHYS, lw=2); ax.plot([0, 2.6], [0, 5.0], color=AI, lw=2)
    ax.text(0.14, 4.7, '地球の双子', color=TEXT, fontsize=9); ax.text(2.1, 4.8, '宇宙船の双子', color=TEXT, fontsize=9)
    ax.fill([0, 0.9, 1.4, 0.6], [0, 1.7, 2.7, 1.1], color=PALE, alpha=1.0)
    ax.text(2.0, 0.65, '速く動く経路ほど\n固有時間が短い', fontsize=9, color=TEXT)
    ax.grid(color=LIGHT, linewidth=0.5)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_assets(fig, 'fig11_minkowski_time_dilation.eps')

def fig12_embedding_analogy():
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    fig.suptitle('意味のベクトル：King - Man + Woman = Queen', fontsize=14, fontweight='bold', color=TEXT)
    panel_label(ax, '(a) 単語埋め込み空間の模式図')
    ax.set_xlim(-0.5, 7.2); ax.set_ylim(-0.5, 6.3)
    ax.set_xlabel('潜在次元 1'); ax.set_ylabel('潜在次元 2')
    ax.grid(color=LIGHT, linewidth=0.6)
    pts = {'man': (1.2, 1.2), 'woman': (2.0, 3.0), 'king': (4.7, 2.0), 'queen': (5.5, 3.8), 'prince': (3.6, 1.5), 'princess': (4.3, 3.3)}
    cols = {'man': PHYS, 'woman': AI, 'king': PHYS, 'queen': AI, 'prince': MID, 'princess': MID}
    for word, (x, y) in pts.items():
        ax.plot(x, y, 'o', ms=8, color=cols[word]); ax.text(x + 0.08, y + 0.10, word, fontsize=10, color=TEXT)
    arrow(ax, pts['man'], pts['king'], color=PHYS, lw=1.6, ms=12)
    arrow(ax, pts['woman'], pts['queen'], color=AI, lw=1.6, ms=12)
    arrow(ax, pts['man'], pts['woman'], color=ACCENT, lw=1.4, ms=11)
    arrow(ax, pts['king'], pts['queen'], color=ACCENT, lw=1.4, ms=11)
    ax.text(3.0, 1.35, '王らしさ', fontsize=9, color=TEXT)
    ax.text(1.35, 2.2, '性別方向', fontsize=9, color=TEXT, rotation=58)
    ax.text(4.1, 5.2, '「意味」は単語単体ではなく\n相対的な距離と方向として表現される', ha='center', fontsize=9.5, color=TEXT)
    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    save_assets(fig, 'fig12_embedding_analogy.eps')

def main():
    fig06_field_div_rot()
    fig07_em_wave_attention()
    fig08_simple_harmonic_motion()
    fig09_interference_standing_wave()
    fig10_fourier_decomposition()
    fig11_minkowski_time_dilation()
    fig12_embedding_analogy()
    print('Generated 7 EPS figures in {}'.format(OUT))

if __name__ == '__main__':
    main()
