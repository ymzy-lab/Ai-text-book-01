"""Generate chapter 4-6 editable EPS figures for AI と物理学の系譜."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Arc

OUT = Path(__file__).resolve().parent / "eps"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams['ps.fonttype'] = 3
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Sans CJK JP Regular', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['figure.dpi'] = 150

PHYS = '#315A7D'
AI = '#A34E4E'
ACCENT = '#B07A2A'
DARK = '#20252B'
MID = '#68717B'
LIGHT = '#D9DEE3'
PALE = '#F3F5F7'

def save_eps(fig, path):
    fig.savefig(OUT / Path(path).name, format='eps', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)

def arrow(ax, xy1, xy2, color=DARK, lw=1.4, ms=12, style='-|>'):
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms, linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p

def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha='left', va='top', fontsize=9, fontweight='bold', color=MID)

def fig06_field_div_rot():
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
    fig.suptitle('ベクトル場の直感：湧き出し（div）と渦（rot）', fontsize=14, fontweight='bold', color=DARK)
    x = np.linspace(-1.8, 1.8, 13)
    y = np.linspace(-1.8, 1.8, 13)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2) + 1e-6
    ax = axs[0]
    panel_label(ax, '(a) div > 0：湧き出し')
    U = X / (R + 0.2); V = Y / (R + 0.2)
    ax.quiver(X, Y, U, V, color=PHYS, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=ACCENT, facecolor='none', lw=2))
    ax.text(0, -2.15, '正の発散：場が外へ広がる', ha='center', fontsize=9, color=DARK)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    ax = axs[1]
    panel_label(ax, '(b) div < 0：吸い込み')
    U = -X / (R + 0.2); V = -Y / (R + 0.2)
    ax.quiver(X, Y, U, V, color=AI, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=ACCENT, facecolor='none', lw=2))
    ax.text(0, -2.15, '負の発散：場が内へ集まる', ha='center', fontsize=9, color=DARK)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    ax = axs[2]
    panel_label(ax, '(c) rot ≠ 0：渦')
    U = -Y / (R + 0.35); V = X / (R + 0.35)
    ax.quiver(X, Y, U, V, color=ACCENT, angles='xy', scale_units='xy', scale=4.8, width=0.006)
    ax.add_patch(Circle((0, 0), 0.18, edgecolor=DARK, facecolor='none', lw=2))
    arc = Arc((0, 0), 2.0, 2.0, theta1=35, theta2=320, lw=1.8, color=DARK)
    ax.add_patch(arc)
    arrow(ax, (0.45, 0.82), (0.2, 0.96), color=DARK, lw=1.2, ms=10)
    ax.text(0, -2.15, '回転成分：場がぐるぐる回る', ha='center', fontsize=9, color=DARK)
    ax.set_aspect('equal'); ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.25, 2.1); ax.axis('off')
    fig.tight_layout(rect=[0, 0.02, 1, 0.90])
    save_eps(fig, 'fig06_field_div_rot.eps')

def fig07_em_wave_attention():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={'width_ratios':[1.05, 1]})
    fig.suptitle('場と情報の伝播：電磁波からSelf-Attentionへ', fontsize=14, fontweight='bold', color=DARK)
    ax = axs[0]
    panel_label(ax, '(a) 物理：電磁波')
    ax.set_xlim(0, 10); ax.set_ylim(-1.8, 2.3); ax.axis('off')
    xx = np.linspace(0.4, 9.2, 400)
    Ey = 1.0*np.sin(1.5*xx); Bz = 0.7*np.sin(1.5*xx)
    ax.plot(xx, Ey + 1.0, color=PHYS, lw=2, label='E場')
    ax.plot(xx, Bz - 0.9, color=AI, lw=2, ls='--', label='B場')
    arrow(ax, (0.8, 0), (9.2, 0), color=DARK, lw=1.4, ms=12)
    ax.text(9.35, 0, '伝播方向', va='center', fontsize=9, color=DARK)
    for xpos in [1.3, 3.4, 5.5, 7.6]:
        yE = 1.0*np.sin(1.5*xpos) + 1.0
        yB = 0.7*np.sin(1.5*xpos) - 0.9
        arrow(ax, (xpos, 0), (xpos, yE), color=PHYS, lw=1.2, ms=9)
        arrow(ax, (xpos, 0), (xpos, yB), color=AI, lw=1.2, ms=9)
    ax.text(0.55, 2.0, 'E場', color=PHYS, fontsize=10, fontweight='bold')
    ax.text(0.55, -1.55, 'B場', color=AI, fontsize=10, fontweight='bold')
    ax.text(5.0, -1.72, '互いに直交する場が空間を伝わる', ha='center', fontsize=9, color=DARK)
    ax = axs[1]
    panel_label(ax, '(b) AI：Self-Attention')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    xs = np.linspace(1.3, 7.9, 6)
    labels = ['The', 'universe', 'is', 'written', 'in', 'math']
    query_idx = 3
    for i, (x0, lab) in enumerate(zip(xs, labels)):
        face = PALE if i != query_idx else '#F2E2E2'
        edge = MID if i != query_idx else AI
        rect = Rectangle((x0-0.6, 4.8), 1.2, 0.8, facecolor=face, edgecolor=edge, lw=1.4)
        ax.add_patch(rect)
        ax.text(x0, 5.2, lab, ha='center', va='center', fontsize=8.8, color=DARK)
    for i, x0 in enumerate(xs):
        lw = 2.0 if i in [1, 5] else 1.0
        col = AI if i in [1, 5] else LIGHT
        arrow(ax, (xs[query_idx], 4.75), (x0, 2.0), color=col, lw=lw, ms=10)
        circ = Circle((x0, 1.6), 0.18, edgecolor=col if i in [1, 5] else MID, facecolor='white', lw=1.1)
        ax.add_patch(circ)
        ax.text(x0, 1.15, f'w{i+1}', ha='center', fontsize=8, color=MID)
    ax.text(xs[query_idx], 6.1, 'query token', ha='center', fontsize=9, color=AI)
    ax.text(5.0, 0.55, '1つのトークンが全体との関係を動的に参照する', ha='center', fontsize=8.6, color=DARK)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig07_em_wave_attention.eps')

def fig08_simple_harmonic_motion():
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.9))
    fig.suptitle('単振動の3つの顔：復元力・時間変化・ポテンシャル', fontsize=14, fontweight='bold', color=DARK)
    ax = axs[0]
    panel_label(ax, '(a) バネと復元力')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
    ax.plot([0.8, 0.8], [1.0, 5.0], color=DARK, lw=3)
    zigx = [0.8, 1.3, 1.0, 1.6, 1.2, 1.8, 1.4, 2.0, 1.6, 2.2, 1.8, 2.4, 2.0, 2.7, 2.3, 3.0]
    zigy = [3.0, 3.0, 3.4, 2.6, 3.4, 2.6, 3.4, 2.6, 3.4, 2.6, 3.4, 2.6, 3.4, 2.6, 3.0, 3.0]
    ax.plot(zigx, zigy, color=PHYS, lw=2)
    ax.add_patch(Rectangle((3.0, 2.2), 1.6, 1.6, facecolor=PALE, edgecolor=PHYS, lw=1.8))
    ax.text(3.8, 3.0, 'm', ha='center', va='center', fontsize=11, color=DARK)
    ax.plot([2.6, 3.0], [3.0, 3.0], color=PHYS, lw=2)
    ax.plot([3.8, 5.6], [3.0, 3.0], color=LIGHT, lw=1.2, ls='--')
    arrow(ax, (5.0, 3.0), (4.0, 3.0), color=AI, lw=1.6, ms=12)
    ax.text(5.1, 3.2, '復元力  F = -kx', fontsize=9, color=AI)
    ax.text(3.85, 1.45, '平衡点から離れるほど\n元へ戻す力が働く', ha='center', fontsize=9, color=DARK)
    ax = axs[1]
    panel_label(ax, '(b) 位置の時間変化')
    t = np.linspace(0, 4*np.pi, 400)
    x = np.cos(t)
    ax.plot(t, x, color=PHYS, lw=2)
    ax.axhline(0, color=LIGHT, lw=1)
    for xpos in [np.pi/2, 3*np.pi/2, 5*np.pi/2, 7*np.pi/2]: ax.axvline(xpos, color=LIGHT, lw=0.8, ls=':')
    ax.set_xlabel('時間  t'); ax.set_ylabel('位置  x(t)')
    ax.grid(color=LIGHT, linewidth=0.6)
    ax.text(np.pi, 1.08, '周期 T ごとに同じ運動をくり返す', ha='center', fontsize=9, color=DARK)
    ax = axs[2]
    panel_label(ax, '(c) エネルギーの谷')
    xp = np.linspace(-2.2, 2.2, 300); V = 0.55*xp**2
    ax.plot(xp, V, color=ACCENT, lw=2)
    for p in [-1.4, 1.4]:
        ax.plot(p, 0.55*p**2, 'o', ms=6, color=PHYS)
        arrow(ax, (p, 0.55*p**2), (0.6*p, 0.55*(0.6*p)**2), color=PHYS, lw=1.2, ms=10)
    ax.set_xlabel('変位  x'); ax.set_ylabel('ポテンシャル  V(x)')
    ax.grid(color=LIGHT, linewidth=0.6)
    ax.text(0, 2.25, '谷底が安定点', ha='center', fontsize=9, color=DARK)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig08_simple_harmonic_motion.eps')

def fig09_interference_standing_wave():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.0))
    fig.suptitle('重ね合わせの原理：干渉と定在波', fontsize=14, fontweight='bold', color=DARK)
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
    ax.text(2.0, 1.85, '位相がそろうと強め合い，ずれると弱め合う', fontsize=9, color=DARK)
    ax = axs[1]
    panel_label(ax, '(b) 定在波と腹・節')
    x = np.linspace(0, np.pi, 500)
    for phase in np.linspace(0, 2*np.pi, 5):
        y = 0.9*np.sin(2*x)*np.cos(phase)
        ax.plot(x, y, color=LIGHT, lw=1)
    env = 0.9*np.abs(np.sin(2*x))
    ax.plot(x, env, color=ACCENT, lw=2); ax.plot(x, -env, color=ACCENT, lw=2)
    for node in [0, np.pi/2, np.pi]:
        ax.plot(node, 0, 'o', ms=5, color=AI); ax.text(node, -1.12, '節', ha='center', fontsize=8.8, color=AI)
    for antinode in [np.pi/4, 3*np.pi/4]: ax.text(antinode, 1.02, '腹', ha='center', fontsize=9, color=PHYS)
    ax.axhline(0, color=LIGHT, lw=1)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel('位置'); ax.set_ylabel('振幅')
    ax.grid(color=LIGHT, linewidth=0.6)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig09_interference_standing_wave.eps')

def fig10_fourier_decomposition():
    fig = plt.figure(figsize=(11.5, 6.2))
    fig.suptitle('フーリエの魔法：複雑な波は単純な波の足し合わせ', fontsize=14, fontweight='bold', color=DARK)
    ax1 = plt.subplot2grid((2, 2), (0, 0)); ax2 = plt.subplot2grid((2, 2), (1, 0)); ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    x = np.linspace(0, 2*np.pi, 800)
    orig = 1.1*np.sin(x) + 0.55*np.sin(2*x + 0.6) + 0.35*np.sin(4*x - 0.8)
    comp1 = 1.1*np.sin(x); comp2 = 0.55*np.sin(2*x + 0.6); comp3 = 0.35*np.sin(4*x - 0.8)
    panel_label(ax1, '(a) 複雑な波形')
    ax1.plot(x, orig, color=DARK, lw=2.2)
    ax1.set_ylabel('振幅'); ax1.set_xticklabels([]); ax1.grid(color=LIGHT, linewidth=0.6)
    ax1.text(np.pi, 1.65, '観測された信号', ha='center', fontsize=9, color=DARK)
    panel_label(ax2, '(b) 単純な波への分解')
    ax2.plot(x, comp1, color=PHYS, lw=1.7, label='基本波  f')
    ax2.plot(x, comp2, color=AI, lw=1.7, label='2f')
    ax2.plot(x, comp3, color=ACCENT, lw=1.7, label='4f')
    ax2.set_xlabel('時間または位置'); ax2.set_ylabel('振幅'); ax2.grid(color=LIGHT, linewidth=0.6)
    ax2.legend(frameon=False, fontsize=8, loc='upper right')
    panel_label(ax3, '(c) 周波数スペクトル')
    freq = np.array([1, 2, 3, 4, 5]); amp = np.array([1.1, 0.55, 0.0, 0.35, 0.0])
    ax3.vlines(freq, 0, amp, colors=[PHYS, AI, LIGHT, ACCENT, LIGHT], linewidth=3)
    ax3.plot(freq, amp, 'o', color=DARK, ms=5)
    ax3.set_xlim(0.5, 5.5); ax3.set_ylim(0, 1.3)
    ax3.set_xlabel('周波数'); ax3.set_ylabel('強さ'); ax3.grid(color=LIGHT, linewidth=0.6)
    ax3.text(2.7, 1.07, '各周波数成分の強さを読む', ha='center', fontsize=8.8, color=DARK)
    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    save_eps(fig, 'fig10_fourier_decomposition.eps')

def fig11_minkowski_time_dilation():
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.3))
    fig.suptitle('特殊相対論の直感：光時計とミンコフスキー図', fontsize=14, fontweight='bold', color=DARK)
    ax = axs[0]
    panel_label(ax, '(a) 光時計')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    ax.add_patch(Rectangle((0.9, 1.2), 2.6, 4.2, facecolor=PALE, edgecolor=PHYS, lw=1.5))
    ax.plot([2.2, 2.2], [1.6, 5.0], color=PHYS, lw=1.5)
    ax.plot([1.6, 2.8], [5.0, 5.0], 'o', color=PHYS, ms=4)
    arrow(ax, (2.2, 1.8), (2.2, 4.8), color=PHYS, lw=1.3, ms=10)
    arrow(ax, (2.2, 4.8), (2.2, 1.8), color=PHYS, lw=1.3, ms=10)
    ax.text(2.2, 0.7, '静止系：光は上下に往復', ha='center', fontsize=9, color=PHYS)
    ax.add_patch(Rectangle((5.2, 1.2), 3.2, 4.2, facecolor=PALE, edgecolor=AI, lw=1.5))
    ax.plot([5.9, 7.9], [1.6, 5.0], color=AI, lw=1.5)
    ax.plot([5.9, 7.9], [5.0, 1.6], color=AI, lw=1.5)
    arrow(ax, (5.3, 5.8), (8.3, 5.8), color=DARK, lw=1.2, ms=10)
    ax.text(6.8, 6.1, '運動', fontsize=9, color=DARK)
    ax.text(6.8, 0.7, '移動系：光の経路が斜めに長くなる', ha='center', fontsize=9, color=AI)
    ax = axs[1]
    panel_label(ax, '(b) ミンコフスキー図')
    ax.set_xlim(-1.2, 5.5); ax.set_ylim(-0.2, 5.5)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xlabel('空間  x'); ax.set_ylabel('時間  ct')
    ax.plot([0, 0], [0, 5.2], color=DARK, lw=1.5); ax.plot([0, 5.2], [0, 0], color=DARK, lw=1.5)
    ax.plot([0, 4.8], [0, 4.8], color=LIGHT, lw=1.4); ax.plot([0, -1.0], [0, 1.0], color=LIGHT, lw=1.4)
    ax.text(4.55, 4.95, '光', fontsize=9, color=MID); ax.text(-0.92, 1.12, '光', fontsize=9, color=MID)
    ax.plot([0, 0], [0, 5.0], color=PHYS, lw=2); ax.plot([0, 2.6], [0, 5.0], color=AI, lw=2)
    ax.text(0.14, 4.7, '地球の双子', color=PHYS, fontsize=9); ax.text(2.1, 4.8, '宇宙船の双子', color=AI, fontsize=9)
    ax.fill([0, 0.9, 1.4, 0.6], [0, 1.7, 2.7, 1.1], color=PALE, alpha=1.0)
    ax.text(2.0, 0.65, '速く動く経路ほど\n固有時間が短い', fontsize=9, color=DARK)
    ax.grid(color=LIGHT, linewidth=0.5)
    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig11_minkowski_time_dilation.eps')

def fig12_embedding_analogy():
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    fig.suptitle('意味のベクトル：King - Man + Woman = Queen', fontsize=14, fontweight='bold', color=DARK)
    panel_label(ax, '(a) 単語埋め込み空間の模式図')
    ax.set_xlim(-0.5, 7.2); ax.set_ylim(-0.5, 6.3)
    ax.set_xlabel('潜在次元 1'); ax.set_ylabel('潜在次元 2')
    ax.grid(color=LIGHT, linewidth=0.6)
    pts = {'man': (1.2, 1.2), 'woman': (2.0, 3.0), 'king': (4.7, 2.0), 'queen': (5.5, 3.8), 'prince': (3.6, 1.5), 'princess': (4.3, 3.3)}
    cols = {'man': PHYS, 'woman': AI, 'king': PHYS, 'queen': AI, 'prince': MID, 'princess': MID}
    for word, (x, y) in pts.items():
        ax.plot(x, y, 'o', ms=8, color=cols[word]); ax.text(x + 0.08, y + 0.10, word, fontsize=10, color=DARK)
    arrow(ax, pts['man'], pts['king'], color=PHYS, lw=1.6, ms=12)
    arrow(ax, pts['woman'], pts['queen'], color=AI, lw=1.6, ms=12)
    arrow(ax, pts['man'], pts['woman'], color=ACCENT, lw=1.4, ms=11)
    arrow(ax, pts['king'], pts['queen'], color=ACCENT, lw=1.4, ms=11)
    ax.text(3.0, 1.35, '王らしさ', fontsize=9, color=PHYS)
    ax.text(1.35, 2.2, '性別方向', fontsize=9, color=ACCENT, rotation=58)
    ax.text(4.1, 5.2, '「意味」は単語単体ではなく\n相対的な距離と方向として表現される', ha='center', fontsize=9.5, color=DARK)
    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    save_eps(fig, 'fig12_embedding_analogy.eps')

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
