"""Generate editable EPS figures for chapters 10–12 of AI と物理学の系譜."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch, Polygon

OUT = Path(__file__).resolve().parent / "eps"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams['ps.fonttype'] = 3
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Sans CJK JP Regular', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

PHYS = '#315A7D'
AI = '#A34E4E'
ACCENT = '#B07A2A'
DARK = '#20252B'
MID = '#68717B'
LIGHT = '#D9DEE3'
PALE = '#F3F5F7'


def save_eps(fig, name):
    fig.savefig(OUT / name, format='eps', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


def arrow(ax, xy1, xy2, color=DARK, lw=1.4, ms=12, style='-|>'):
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p


def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha='left', va='top',
            fontsize=9, fontweight='bold', color=MID)


def fig21_de_broglie_diffraction():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.4))
    fig.suptitle('物質も波である：ド・ブロイ波と電子回折', fontsize=14, fontweight='bold', color=DARK)

    ax = axs[0]; panel_label(ax, '(a) 粒子に対応する波長')
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
    xs = np.linspace(0.8, 9.2, 400)
    wave = 3.0 + 0.65*np.sin(2*np.pi*xs/2.4)
    ax.plot(xs, wave, color=PHYS, lw=2)
    for x0 in np.linspace(1.2, 8.8, 7):
        ax.plot(x0, 3.0, 'o', color=AI, ms=5)
    ax.text(5.0, 5.1, r'$\lambda = h/p$', ha='center', fontsize=15, color=DARK)
    ax.text(5.0, 1.15, '電子は「粒」として検出されるが、\n伝播では波長を持つ', ha='center', fontsize=9, color=DARK)

    ax = axs[1]; panel_label(ax, '(b) 結晶による電子回折')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    for x0 in [2.6, 3.2, 3.8]:
        for y0 in np.linspace(1.0, 6.0, 7):
            ax.add_patch(Circle((x0, y0), 0.09, facecolor=MID, edgecolor='none'))
    for y0 in np.linspace(2.4, 4.6, 6):
        arrow(ax, (0.4, y0), (2.25, y0), color=PHYS, lw=1.1, ms=8)
    for ang, c in [(-0.65, PHYS), (-0.32, LIGHT), (0, ACCENT), (0.32, LIGHT), (0.65, PHYS)]:
        x1, y1 = 4.0, 3.5
        x2 = 8.8
        y2 = y1 + np.tan(ang)*(x2-x1)
        ax.plot([x1, x2], [y1, y2], color=c, lw=2 if c != LIGHT else 1)
    ax.plot([9.0, 9.0], [0.7, 6.3], color=DARK, lw=2)
    ax.text(6.6, 6.25, '特定方向で強め合う', ha='center', fontsize=9, color=PHYS)
    ax.text(9.25, 3.5, '検出面', rotation=90, va='center', fontsize=9, color=DARK)

    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig21_de_broglie_diffraction.eps')


def fig22_wavefunction_born_probability():
    fig, axs = plt.subplots(2, 1, figsize=(8.4, 6.4), sharex=True)
    fig.suptitle('波動関数から観測確率へ：Born の確率解釈', fontsize=14, fontweight='bold', color=DARK)
    x = np.linspace(-5, 5, 800)
    envelope = np.exp(-0.5*(x/1.55)**2)
    re = envelope*np.cos(4.3*x)
    im = envelope*np.sin(4.3*x)
    prob = envelope**2

    ax = axs[0]; panel_label(ax, '(a) 複素数の確率振幅  ψ')
    ax.plot(x, re, color=PHYS, lw=1.8, label='Re ψ')
    ax.plot(x, im, color=AI, lw=1.6, ls='--', label='Im ψ')
    ax.axhline(0, color=LIGHT, lw=1)
    ax.set_ylabel('確率振幅')
    ax.grid(color=LIGHT, lw=0.5)
    ax.legend(frameon=False, fontsize=8)

    ax = axs[1]; panel_label(ax, r'(b) 観測確率  $|\psi|^2$')
    ax.fill_between(x, 0, prob, color=PHYS, alpha=0.12)
    ax.plot(x, prob, color=PHYS, lw=2.2)
    rng = np.random.default_rng(12)
    samples = rng.normal(0, 1.1, 60)
    ax.plot(samples, np.full_like(samples, -0.055), '|', ms=8, color=AI)
    ax.text(0, 0.72, '測定を繰り返すと、粒子は\nこの分布に従って一点に現れる', ha='center', fontsize=9, color=DARK)
    ax.set_xlabel('位置  x'); ax.set_ylabel('確率密度')
    ax.set_ylim(-0.1, 1.08)
    ax.grid(color=LIGHT, lw=0.5)

    fig.tight_layout(rect=[0, 0.03, 1, 0.91])
    save_eps(fig, 'fig22_wavefunction_born_probability.eps')


def fig23_uncertainty_wavepacket():
    fig, axs = plt.subplots(2, 2, figsize=(10.8, 6.2))
    fig.suptitle('不確定性原理：位置を絞るほど運動量は広がる', fontsize=14, fontweight='bold', color=DARK)

    x = np.linspace(-6, 6, 800)
    p = np.linspace(-8, 8, 800)
    sigmas = [0.65, 2.0]
    titles = [('位置が鋭い', '運動量が広い'), ('位置が広い', '運動量が鋭い')]
    for col, sigma_x in enumerate(sigmas):
        psi_x = np.exp(-(x**2)/(4*sigma_x**2))
        prob_x = psi_x**2
        sigma_p = 1/(2*sigma_x)
        prob_p = np.exp(-(p**2)/(2*sigma_p**2))
        prob_p /= prob_p.max()

        ax = axs[0, col]; panel_label(ax, f'({chr(97+2*col)}) {titles[col][0]}')
        ax.plot(x, prob_x/prob_x.max(), color=PHYS, lw=2)
        ax.fill_between(x, 0, prob_x/prob_x.max(), color=PHYS, alpha=0.10)
        ax.set_xlabel('位置 x'); ax.set_ylabel('確率密度')
        ax.grid(color=LIGHT, lw=0.5)

        ax = axs[1, col]; panel_label(ax, f'({chr(98+2*col)}) {titles[col][1]}')
        ax.plot(p, prob_p, color=AI, lw=2)
        ax.fill_between(p, 0, prob_p, color=AI, alpha=0.10)
        ax.set_xlabel('運動量 p'); ax.set_ylabel('確率密度')
        ax.grid(color=LIGHT, lw=0.5)

    fig.text(0.5, 0.015, r'$\Delta x\,\Delta p \geq \hbar/2$ ：これは測定器の性能ではなく、状態そのものの制約',
             ha='center', fontsize=10, color=DARK)
    fig.tight_layout(rect=[0, 0.05, 1, 0.91])
    save_eps(fig, 'fig23_uncertainty_wavepacket.eps')


def fig24_curse_dimensionality_nnqs():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.5))
    fig.suptitle('量子多体問題の「次元の呪い」とニューラル量子状態', fontsize=14, fontweight='bold', color=DARK)

    ax = axs[0]; panel_label(ax, '(a) 状態数は指数関数的に爆発')
    N = np.arange(1, 31)
    dim = 2.0**N
    ax.semilogy(N, dim, color=AI, lw=2.2)
    ax.scatter([10, 20, 30], [2**10, 2**20, 2**30], color=AI, s=28)
    ax.text(10, 2**10*4, r'$2^{10}=1024$', ha='center', fontsize=8.5)
    ax.text(20, 2**20*4, r'$2^{20}\approx10^6$', ha='center', fontsize=8.5)
    ax.text(28, 2**30/8, '粒子を1個増やすだけで\n必要状態数が倍増', ha='right', fontsize=9, color=DARK)
    ax.set_xlabel('2状態粒子の数  N'); ax.set_ylabel('ヒルベルト空間の次元  $2^N$')
    ax.grid(color=LIGHT, lw=0.5, which='both')

    ax = axs[1]; panel_label(ax, '(b) NNQS：巨大な波動関数を関数として圧縮')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    states = ['↑', '↓', '↑', '↑', '↓', '…']
    for i, s in enumerate(states):
        x0 = 0.7 + i*0.8
        ax.add_patch(Rectangle((x0, 5.1), 0.55, 0.7, facecolor=PALE, edgecolor=PHYS, lw=1.1))
        ax.text(x0+0.275, 5.45, s, ha='center', va='center', fontsize=10, color=DARK)
    arrow(ax, (5.5, 5.45), (6.6, 5.45), color=DARK)
    box = FancyBboxPatch((6.7,4.65),2.1,1.6,boxstyle='round,pad=0.04',facecolor='white',edgecolor=AI,lw=1.6)
    ax.add_patch(box); ax.text(7.75,5.45,'Neural\nNetwork',ha='center',va='center',fontsize=10,color=AI)
    arrow(ax, (7.75, 4.6), (7.75, 3.45), color=AI)
    ax.add_patch(FancyBboxPatch((6.45,2.2),2.6,1.1,boxstyle='round,pad=0.04',facecolor='white',edgecolor=ACCENT,lw=1.6))
    ax.text(7.75,2.75,r'$\psi_\theta(s_1,\dots,s_N)$',ha='center',va='center',fontsize=12,color=DARK)
    ax.text(4.8, 0.95, 'すべての振幅を表に保存せず、\n重要な相関構造をネットワークで表現', ha='center', fontsize=9, color=DARK)

    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_eps(fig, 'fig24_curse_dimensionality_nnqs.eps')


def fig25_law_large_numbers():
    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.3))
    fig.suptitle('ミクロの偶然からマクロの確実性へ：大数の法則', fontsize=14, fontweight='bold', color=DARK)
    rng = np.random.default_rng(3)

    ax = axs[0]; panel_label(ax, '(a) コイン投げの平均は 1/2 に収束')
    toss = rng.integers(0, 2, 5000)
    running = np.cumsum(toss)/np.arange(1, len(toss)+1)
    ax.plot(np.arange(1, len(toss)+1), running, color=PHYS, lw=1.4)
    ax.axhline(0.5, color=AI, lw=1.5, ls='--')
    ax.set_xscale('log'); ax.set_ylim(0.25, 0.75)
    ax.set_xlabel('試行回数 N'); ax.set_ylabel('表の比率')
    ax.grid(color=LIGHT, lw=0.5)

    ax = axs[1]; panel_label(ax, r'(b) 相対揺らぎ $\propto 1/\sqrt{N}$')
    N = np.logspace(0, 12, 300)
    fluct = 1/np.sqrt(N)
    ax.loglog(N, fluct, color=ACCENT, lw=2.2)
    ax.set_xlabel('粒子数 N'); ax.set_ylabel('相対的な揺らぎ')
    ax.grid(color=LIGHT, lw=0.5, which='both')
    ax.text(1e5, 2e-2, '粒子数が巨大になると、\nマクロな量はほとんど揺らがない', fontsize=9, color=DARK)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig, 'fig25_law_large_numbers.eps')


def fig26_quantum_statistics():
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    fig.suptitle('三つの統計：Maxwell–Boltzmann / Fermi–Dirac / Bose–Einstein', fontsize=14, fontweight='bold', color=DARK)
    panel_label(ax, '(a) 同じ温度での占有数の違い（模式図）')

    E = np.linspace(0.12, 6, 500)
    mu = 0.0
    T = 1.0
    mb = np.exp(-(E-mu)/T)
    fd = 1/(np.exp((E-mu)/T)+1)
    be = 1/(np.exp((E-mu)/T)-1)
    be = np.clip(be, 0, 4.5)

    ax.plot(E, mb, color=MID, lw=2, label='Maxwell–Boltzmann')
    ax.plot(E, fd, color=AI, lw=2, label='Fermi–Dirac  (+1)')
    ax.plot(E, be, color=PHYS, lw=2, label='Bose–Einstein  (−1)')
    ax.axhline(1, color=LIGHT, lw=1)
    ax.text(4.2, 1.08, 'Fermi粒子は占有数1を超えない', fontsize=8.7, color=AI)
    ax.annotate('Boson は低エネルギー状態に\n多数集まれる', xy=(0.42, 3.6), xytext=(1.6, 3.7),
                arrowprops=dict(arrowstyle='->', color=PHYS), fontsize=9, color=PHYS)
    ax.set_ylim(0, 4.6); ax.set_xlim(0, 6)
    ax.set_xlabel(r'無次元エネルギー  $(E-\mu)/k_BT$'); ax.set_ylabel('平均占有数')
    ax.grid(color=LIGHT, lw=0.5)
    ax.legend(frameon=False, fontsize=8.5, loc='upper right')

    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig, 'fig26_quantum_statistics.eps')


def fig27_boltzmann_softmax():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.4))
    fig.suptitle('統計力学とAIの同型：ボルツマン分布とSoftmax', fontsize=14, fontweight='bold', color=DARK)

    ax = axs[0]; panel_label(ax, '(a) 物理：低いエネルギーほど高確率')
    E = np.array([0.4, 1.0, 1.7, 2.4])
    w = np.exp(-E); P = w/w.sum()
    ax.bar(np.arange(4), P, edgecolor=PHYS, facecolor='white', lw=1.5)
    ax.set_xticks(np.arange(4), [r'$E_1$', r'$E_2$', r'$E_3$', r'$E_4$'])
    ax.set_ylabel('確率'); ax.set_ylim(0, 0.55)
    ax.text(1.5, 0.49, r'$P_i = e^{-E_i/k_BT}/Z$', ha='center', fontsize=11, color=DARK)
    ax.grid(axis='y', color=LIGHT, lw=0.5)

    ax = axs[1]; panel_label(ax, '(b) AI：高いスコアほど高確率')
    score = -E
    w2 = np.exp(score); P2 = w2/w2.sum()
    ax.bar(np.arange(4), P2, edgecolor=AI, facecolor='white', lw=1.5)
    ax.set_xticks(np.arange(4), ['候補1','候補2','候補3','候補4'])
    ax.set_ylabel('Softmax確率'); ax.set_ylim(0, 0.55)
    ax.text(1.5, 0.49, r'$P_i = e^{x_i}/\sum_j e^{x_j}$', ha='center', fontsize=11, color=DARK)
    ax.grid(axis='y', color=LIGHT, lw=0.5)
    fig.text(0.5, 0.025, r'対応：  $x_i \leftrightarrow -E_i/k_BT$     かつ     $\sum_j e^{x_j} \leftrightarrow Z$',
             ha='center', fontsize=10, color=ACCENT)

    fig.tight_layout(rect=[0,0.06,1,0.90])
    save_eps(fig, 'fig27_boltzmann_softmax.eps')


def fig28_emergence_hierarchy():
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    fig.suptitle('More is different：階層ごとに新しい法則が創発する', fontsize=14, fontweight='bold', color=DARK)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    levels = [
        (1.2, '素粒子・電子', '量子論・標準模型'),
        (3.0, '原子・分子・物質', '化学・多体物理'),
        (4.8, '細胞・生命', '生物学・非平衡系'),
        (6.6, '脳・認知', '神経科学・情報処理'),
        (8.4, '集団・社会', 'マクロな秩序・制度'),
    ]
    widths = [4.2, 5.0, 5.8, 6.6, 7.4]
    for (y, title, sub), w in zip(levels, widths):
        x = 5 - w/2
        rect = FancyBboxPatch((x, y-0.55), w, 1.1, boxstyle='round,pad=0.03,rounding_size=0.08',
                              facecolor='white', edgecolor=PHYS if y < 5 else AI, lw=1.4)
        ax.add_patch(rect)
        ax.text(5, y+0.13, title, ha='center', va='center', fontsize=10, fontweight='bold', color=DARK)
        ax.text(5, y-0.25, sub, ha='center', va='center', fontsize=8.5, color=MID)
    for y in [1.75, 3.55, 5.35, 7.15]:
        arrow(ax, (4.35, y), (4.35, y+0.65), color=ACCENT, lw=1.4, ms=10)
        ax.text(3.55, y+0.25, '創発', ha='center', fontsize=8.8, color=ACCENT)
    for y in [7.65, 5.85, 4.05, 2.25]:
        arrow(ax, (5.65, y), (5.65, y-0.65), color=MID, lw=1.0, ms=8)
    ax.text(7.6, 5.0, '上位の構造が下位の\n自由度を制約することもある', ha='center', fontsize=9, color=MID)
    ax.text(7.55, 4.3, '（トップダウン因果）', ha='center', fontsize=8.5, color=MID)

    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig, 'fig28_emergence_hierarchy.eps')


def fig29_semiconductor_bands():
    fig, axs = plt.subplots(1, 3, figsize=(11.4, 4.5))
    fig.suptitle('バンドギャップと半導体：電子の「席」の空き方で電気伝導が決まる', fontsize=14, fontweight='bold', color=DARK)
    labels = [('導体', 0.0), ('半導体', 1.1), ('絶縁体', 2.4)]
    for i, (title, gap) in enumerate(labels):
        ax = axs[i]; panel_label(ax, f'({chr(97+i)}) {title}')
        ax.set_xlim(0, 4); ax.set_ylim(0, 7); ax.axis('off')
        vb_top = 2.4
        cb_bot = vb_top + gap
        ax.add_patch(Rectangle((0.7,0.8),2.6,1.6,facecolor=PHYS,alpha=0.13,edgecolor=PHYS,lw=1.4))
        ax.text(2.0,1.55,'価電子帯',ha='center',fontsize=9,color=PHYS)
        if gap == 0:
            ax.add_patch(Rectangle((0.7,2.1),2.6,2.0,facecolor=AI,alpha=0.10,edgecolor=AI,lw=1.4))
            ax.text(2.0,3.25,'伝導帯と重なる',ha='center',fontsize=8.8,color=AI)
            arrow(ax,(2.0,2.0),(2.0,3.0),color=ACCENT,lw=1.3,ms=9)
        else:
            ax.add_patch(Rectangle((0.7,cb_bot),2.6,1.5,facecolor=AI,alpha=0.10,edgecolor=AI,lw=1.4))
            ax.text(2.0,cb_bot+0.75,'伝導帯',ha='center',fontsize=9,color=AI)
            ax.annotate('', xy=(3.55, cb_bot), xytext=(3.55, vb_top), arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=1.2))
            ax.text(3.72,(cb_bot+vb_top)/2,'gap',va='center',fontsize=8.5,color=ACCENT)
            if i == 1:
                arrow(ax,(1.55,2.1),(1.55,cb_bot+0.2),color=ACCENT,lw=1.4,ms=10)
                ax.add_patch(Circle((1.55,1.95),0.08,facecolor='white',edgecolor=AI,lw=1.2))
                ax.text(2.0,5.9,'熱・光・電圧で\n励起可能',ha='center',fontsize=8.8,color=DARK)
        ax.text(2.0,0.25,['自由に動ける','適度なギャップ','ギャップが大きい'][i],ha='center',fontsize=8.8,color=MID)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig, 'fig29_semiconductor_bands.eps')


def fig30_superconductivity_cooper_pair():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.5))
    fig.suptitle('超伝導：電子対が位相をそろえた巨大な量子状態', fontsize=14, fontweight='bold', color=DARK)

    ax = axs[0]; panel_label(ax, '(a) 格子の歪みを介したクーパー対（模式図）')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    for ix in range(1,9):
        for iy in [2,3.5,5]:
            y = iy - 0.35*np.exp(-((ix-4.5)/1.3)**2)
            ax.add_patch(Circle((ix,y),0.12,facecolor=LIGHT,edgecolor=MID,lw=0.7))
    ax.add_patch(Circle((3.3,3.6),0.20,facecolor=AI,edgecolor='none'))
    ax.add_patch(Circle((6.1,3.1),0.20,facecolor=AI,edgecolor='none'))
    ax.text(3.3,4.15,'e-',ha='center',fontsize=10,color=AI)
    ax.text(6.1,3.65,'e-',ha='center',fontsize=10,color=AI)
    arrow(ax,(3.55,3.65),(5.85,3.2),color=ACCENT,lw=1.3,ms=9,style='<->')
    ax.text(4.7,2.0,'一方の電子が格子を歪ませ、\nもう一方を間接的に引き寄せる',ha='center',fontsize=9,color=DARK)

    ax = axs[1]; panel_label(ax, '(b) 多数の対が位相をそろえて流れる')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    xs = np.linspace(0.7,9.2,400)
    for j, y0 in enumerate([2.0,3.2,4.4]):
        y = y0 + 0.22*np.sin(2.2*xs)
        ax.plot(xs,y,color=PHYS,lw=1.6)
        for x0 in np.linspace(1.2,8.8,7):
            ax.add_patch(Circle((x0, y0+0.22*np.sin(2.2*x0)),0.10,facecolor=ACCENT,edgecolor='none'))
    arrow(ax,(1.0,5.7),(8.9,5.7),color=PHYS,lw=1.8,ms=12)
    ax.text(5.0,6.05,'巨視的に同じ位相で流れる',ha='center',fontsize=9,color=PHYS)
    ax.text(5.0,0.9,'散乱が抑えられ、電気抵抗がゼロになる',ha='center',fontsize=9,color=DARK)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig, 'fig30_superconductivity_cooper_pair.eps')


def fig31_quantum_interference_vqe():
    fig, axs = plt.subplots(1, 2, figsize=(11.2, 4.6))
    fig.suptitle('量子計算の核心：干渉で答えを強め、VQEで古典AIと協調する', fontsize=14, fontweight='bold', color=DARK)

    ax = axs[0]; panel_label(ax, '(a) 「全並列」ではなく振幅の干渉')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    labels = ['候補A','候補B','候補C','候補D']
    amps1 = [0.7,0.55,0.6,0.8]
    amps2 = [-0.65,-0.5,0.55,0.75]
    for i, lab in enumerate(labels):
        x0 = 1.2 + i*2.2
        ax.text(x0,6.1,lab,ha='center',fontsize=8.8,color=DARK)
        ax.arrow(x0,3.4,0,amps1[i]*1.8,width=0.025,head_width=0.14,head_length=0.15,color=PHYS,length_includes_head=True)
        ax.arrow(x0+0.35,3.4,0,amps2[i]*1.8,width=0.025,head_width=0.14,head_length=0.15,color=AI,length_includes_head=True)
        result = amps1[i]+amps2[i]
        ax.arrow(x0+0.75,3.4,0,result*1.8,width=0.035,head_width=0.17,head_length=0.15,color=ACCENT,length_includes_head=True)
    ax.text(3.5,0.85,'誤答：山と谷を重ねて打ち消す',ha='center',fontsize=8.8,color=AI)
    ax.text(7.5,0.85,'正答：同符号の振幅を強める',ha='center',fontsize=8.8,color=ACCENT)

    ax = axs[1]; panel_label(ax, '(b) VQE：量子–古典ハイブリッド')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    qbox = FancyBboxPatch((0.9,3.4),3.0,1.7,boxstyle='round,pad=0.04',facecolor='white',edgecolor=PHYS,lw=1.6)
    cbox = FancyBboxPatch((6.1,3.4),3.0,1.7,boxstyle='round,pad=0.04',facecolor='white',edgecolor=AI,lw=1.6)
    ax.add_patch(qbox); ax.add_patch(cbox)
    ax.text(2.4,4.25,'量子回路\n|ψ(θ)> を生成',ha='center',va='center',fontsize=9.5,color=PHYS)
    ax.text(7.6,4.25,'古典最適化\nθ を更新',ha='center',va='center',fontsize=9.5,color=AI)
    arrow(ax,(3.95,4.55),(6.05,4.55),color=DARK,lw=1.3,ms=10)
    ax.text(5.0,4.9,'エネルギー測定',ha='center',fontsize=8.3,color=MID)
    arrow(ax,(6.05,3.85),(3.95,3.85),color=ACCENT,lw=1.3,ms=10)
    ax.text(5.0,3.3,'新しいパラメータ θ',ha='center',fontsize=8.3,color=ACCENT)
    ax.text(5.0,1.55,'量子側：重ね合わせを作る\n古典側：損失を最小化する',ha='center',fontsize=9,color=DARK)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig, 'fig31_quantum_interference_vqe.eps')


def main():
    fig21_de_broglie_diffraction()
    fig22_wavefunction_born_probability()
    fig23_uncertainty_wavepacket()
    fig24_curse_dimensionality_nnqs()
    fig25_law_large_numbers()
    fig26_quantum_statistics()
    fig27_boltzmann_softmax()
    fig28_emergence_hierarchy()
    fig29_semiconductor_bands()
    fig30_superconductivity_cooper_pair()
    fig31_quantum_interference_vqe()
    print(f'Generated 11 EPS figures in {OUT}')


if __name__ == '__main__':
    main()
