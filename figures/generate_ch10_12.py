"""Generate grayscale PDF/SVG textbook figures plus optional EPS side output."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch, Polygon

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
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p


def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha='left', va='top',
            fontsize=9, fontweight='bold', color=SUBTEXT)


def fig21_de_broglie_diffraction():
    fig, axs = plt.subplots(
        1, 2, figsize=(12.4, 4.8),
        gridspec_kw={'width_ratios': [0.88, 1.25]}
    )
    fig.suptitle(
        '物質も波である：ド・ブロイ波と電子回折',
        fontsize=14, fontweight='bold', color=TEXT
    )

    # (a) A moving electron has a de Broglie wavelength.
    ax = axs[0]
    panel_label(ax, '(a) 粒子に対応する波長')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    xs = np.linspace(0.8, 9.2, 400)
    wave = 3.0 + 0.65 * np.sin(2 * np.pi * xs / 2.4)
    ax.plot(xs, wave, color=PHYS, lw=2)
    for x0 in np.linspace(1.2, 8.8, 7):
        ax.plot(x0, 3.0, marker='o', linestyle='none', color=AI, ms=5)
    ax.text(5.0, 5.1, r'$\lambda=h/p$', ha='center', fontsize=15, color=TEXT)
    ax.text(
        5.0, 1.15,
        '電子は「粒」として検出されるが、\n伝播では波長を持つ',
        ha='center', fontsize=9, color=TEXT
    )

    # (b) A single row of coherently scattering atoms models one
    # direction of diffraction from a crystal.  The detection pattern
    # is calculated from the interference of all five amplitudes,
    # not drawn by hand.
    ax = axs[1]
    panel_label(ax, '(b) 原子列による電子回折：散乱波が重なる')
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 8.0)
    ax.axis('off')

    n_atoms = 5
    d = 0.72                   # lattice spacing, schematic units
    wavelength = 0.31          # de Broglie wavelength, same units
    x_atoms, x_screen = 3.10, 8.45
    y_center = 4.0
    atoms_y = y_center + np.arange(-2, 3) * d
    distance = x_screen - x_atoms

    # The Fraunhofer condition for coherent outgoing electron waves:
    # d sin(theta_m) = m lambda, m = 0, +/-1.
    theta_first = np.arcsin(wavelength / d)
    y_first = distance * np.tan(theta_first)
    bright_ys = [y_center - y_first, y_center, y_center + y_first]
    theta_null = np.arcsin(wavelength / (n_atoms * d))
    y_null = distance * np.tan(theta_null)
    dark_ys = [y_center - y_null, y_center + y_null]

    def relative_intensity(yy):
        """Normalized N-atom far-field array factor on a flat screen."""
        yy = np.atleast_1d(np.asarray(yy, dtype=float))
        theta = np.arctan2(yy - y_center, distance)
        phase = 2 * np.pi * d * np.sin(theta) / wavelength
        j = np.arange(n_atoms, dtype=float)[:, None]
        amplitude = np.exp(1j * j * phase[None, :]).sum(axis=0)
        return (np.abs(amplitude) / n_atoms)**2

    # Numerical checks tie the depicted detector peaks to interference.
    assert np.allclose(relative_intensity(bright_ys), 1.0, atol=1e-10)
    assert np.all(relative_intensity(dark_ys) < 1e-10)

    ax.text(0.35, 7.02, '入射する電子波', fontsize=9, color=TEXT)
    for yi in atoms_y:
        arrow(ax, (0.35, yi), (2.48, yi),
              color=PHYS, lw=1.2, ms=9)
    ax.plot([x_atoms, x_atoms], [2.34, 5.66], color=LIGHT, lw=1)
    for yi in atoms_y:
        ax.add_patch(Circle((x_atoms, yi), 0.12,
                            facecolor=MID, edgecolor='none', zorder=4))
    ax.text(x_atoms, 6.12, '結晶中の原子列', ha='center',
            fontsize=9, color=TEXT)
    ax.text(x_atoms + 0.20, 2.35, '間隔 d', fontsize=8.2, color=SUBTEXT)

    # Several coherent scattering contributions meet at one upper
    # diffraction peak.  Light gray lines denote contributions,
    # not classical electron trajectories.
    top_peak = bright_ys[2]
    for yi in atoms_y:
        ax.plot([x_atoms + 0.10, x_screen - 0.10],
                [yi, top_peak], color=LIGHT, lw=0.90, zorder=1)

    # Highlight the three constructive outgoing DIRECTIONS.
    for y_peak in bright_ys:
        ax.plot([x_atoms + 0.15, x_screen - 0.20],
                [y_center, y_peak], color=PHYS, lw=1.8, zorder=2)
        xx0 = x_atoms + 3.55
        xx1 = xx0 + 0.52
        yy0 = y_center + (y_peak-y_center) * (xx0-x_atoms)/distance
        yy1 = y_center + (y_peak-y_center) * (xx1-x_atoms)/distance
        arrow(ax, (xx0, yy0), (xx1, yy1),
              color=PHYS, lw=1.4, ms=9)

    ax.text(5.57, 7.40, '波の位相が揃う方向で強め合う',
            ha='center', fontsize=9, color=TEXT)
    ax.text(5.57, 6.98, r'$d\sin\theta=m\lambda$',
            ha='center', fontsize=11, color=TEXT)

    # A real detector records the squared sum of amplitudes.
    ax.plot([x_screen, x_screen], [0.67, 7.34],
            color=DARK, lw=2, zorder=3)
    ax.text(x_screen, 7.64, '検出面', ha='center',
            fontsize=9, color=TEXT)
    for yi in bright_ys:
        ax.plot(x_screen, yi, 'o', color=DARK, ms=7,
                zorder=5)
    for yi in dark_ys:
        ax.plot(x_screen, yi, 'o', color=LIGHT, ms=4.5,
                zorder=5)

    ys = np.linspace(0.67, 7.34, 900)
    intensity = relative_intensity(ys)
    x_base, profile_width = 8.95, 2.05
    ax.plot([x_base, x_base], [0.67, 7.34],
            color=LIGHT, lw=0.9)
    ax.plot(x_base + profile_width * intensity, ys,
            color=DARK, lw=2, zorder=2)
    ax.text(10.04, 7.64, '検出強度', ha='center',
            fontsize=9, color=TEXT)
    ax.text(10.10, 0.27, '山＝明るい回折ピーク',
            ha='center', fontsize=8.5, color=TEXT)

    ax.text(5.10, 0.30,
            '原子ごとの散乱波が重なる → 方向により明暗が現れる',
            ha='center', fontsize=8.7, color=TEXT)
    fig.text(0.5, 0.015,
             '右図：実際の結晶を1次元の原子列に単純化した遠方回折モデル。'
             '濃い点が強い検出方向、薄い点が打ち消し合う方向。',
             ha='center', fontsize=9, color=TEXT)

    fig.tight_layout(rect=[0, 0.070, 1, 0.90], w_pad=1.6)
    save_assets(fig, 'fig21_de_broglie_diffraction.eps')

def fig22_wavefunction_born_probability():
    fig, axs = plt.subplots(2, 1, figsize=(8.4, 6.4), sharex=True)
    fig.suptitle('波動関数から観測確率へ：Born の確率解釈', fontsize=14, fontweight='bold', color=TEXT)
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
    ax.text(0, 0.72, '測定を繰り返すと、粒子は\nこの分布に従って一点に現れる', ha='center', fontsize=9, color=TEXT)
    ax.set_xlabel('位置  x'); ax.set_ylabel('確率密度')
    ax.set_ylim(-0.1, 1.08)
    ax.grid(color=LIGHT, lw=0.5)

    fig.tight_layout(rect=[0, 0.03, 1, 0.91])
    save_assets(fig, 'fig22_wavefunction_born_probability.eps')


def fig23_uncertainty_wavepacket():
    """Show the Fourier tradeoff as wavelength-estimation intuition.

    A short wave packet contains only a few visible oscillations, so its
    wave number k (and therefore momentum p = hbar k) is poorly defined.
    A long packet contains many oscillations, so k and p are sharply defined.
    The momentum widths use the exact Gaussian minimum-uncertainty relation
    sigma_p = hbar/(2 sigma_x), with hbar = 1 in the plotted units.
    """
    fig, axs = plt.subplots(2, 2, figsize=(11.8, 7.0))
    fig.suptitle(
        '不確定性原理の直感：波長を正確に読むには、広い空間範囲が必要',
        fontsize=14, fontweight='bold', color=TEXT
    )

    # Dimensionless units with hbar = 1.
    hbar = 1.0
    k0 = 3.0
    p0 = hbar * k0
    wavelength = 2 * np.pi / k0

    x = np.linspace(-10, 10, 1800)
    p = np.linspace(0, 6, 1400)

    cases = [
        dict(
            sigma_x=0.95,
            title_x='(a) 狭い波束：見える周期が少ない',
            title_p='(b) 運動量は広くなる',
            dx_label='Δx 小',
            dp_label='Δp 大',
            note='数周期しか見えない\\n→ λ を精密に決めにくい',
        ),
        dict(
            sigma_x=3.20,
            title_x='(c) 広い波束：多くの周期を比べられる',
            title_p='(d) 運動量は鋭く決まる',
            dx_label='Δx 大',
            dp_label='Δp 小',
            note='多くの山谷を比べられる\\n→ λ を精密に決めやすい',
        ),
    ]

    for col, case in enumerate(cases):
        sigma_x = case['sigma_x']
        sigma_p = hbar / (2 * sigma_x)

        # Minimum-uncertainty Gaussian packet in position space.
        envelope = np.exp(-(x**2) / (4 * sigma_x**2))
        psi_real = envelope * np.cos(k0 * x)

        # Corresponding Gaussian momentum probability density.
        prob_p = np.exp(-((p - p0)**2) / (2 * sigma_p**2))
        prob_p /= prob_p.max()

        # -----------------------------------------------------
        # Position-space wave packet
        # -----------------------------------------------------
        ax = axs[0, col]
        panel_label(ax, case['title_x'])
        ax.plot(x, psi_real, color=PHYS, lw=1.8)
        ax.plot(x, envelope, color=LIGHT, lw=1.1, ls='--')
        ax.plot(x, -envelope, color=LIGHT, lw=1.1, ls='--')
        ax.axhline(0, color=LIGHT, lw=0.8)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-1.22, 1.22)
        ax.set_xlabel('位置  x')
        ax.set_ylabel('波の振幅')
        ax.grid(color=LIGHT, lw=0.45)

        # Mark the spatial extent over which the packet has appreciable amplitude.
        xL, xR = -2 * sigma_x, 2 * sigma_x
        yb = -1.04
        ax.plot([xL, xR], [yb, yb], color=DARK, lw=1.0)
        ax.plot([xL, xL], [yb-0.045, yb+0.045], color=DARK, lw=1.0)
        ax.plot([xR, xR], [yb-0.045, yb+0.045], color=DARK, lw=1.0)
        ax.text(0, yb-0.06, case['dx_label'],
                ha='center', va='top', fontsize=9, color=TEXT)

        # Mark one wavelength where the envelope is large.
        lam_left = -0.55 * wavelength
        lam_right = lam_left + wavelength
        ylam = 0.78
        ax.plot([lam_left, lam_right], [ylam, ylam],
                color=ACCENT, lw=1.2)
        ax.plot([lam_left, lam_left], [ylam-0.04, ylam+0.04],
                color=ACCENT, lw=1.0)
        ax.plot([lam_right, lam_right], [ylam-0.04, ylam+0.04],
                color=ACCENT, lw=1.0)
        ax.text((lam_left+lam_right)/2, ylam+0.07, 'λ',
                ha='center', fontsize=9, color=TEXT)

        ax.text(
            0, 1.07, case['note'],
            ha='center', va='top', fontsize=8.8, color=TEXT,
            bbox=dict(facecolor='white', edgecolor='none', pad=1.5)
        )

        # -----------------------------------------------------
        # Momentum-space distribution
        # -----------------------------------------------------
        ax = axs[1, col]
        panel_label(ax, case['title_p'])
        ax.plot(p, prob_p, color=AI, lw=2.1)
        ax.fill_between(p, 0, prob_p, color=PALE)
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 1.08)
        ax.set_xlabel('運動量  p')
        ax.set_ylabel('確率密度')
        ax.grid(color=LIGHT, lw=0.45)

        # Mark the 1-sigma momentum width.
        pL, pR = p0 - sigma_p, p0 + sigma_p
        yb = 0.15
        ax.plot([pL, pR], [yb, yb], color=DARK, lw=1.0)
        ax.plot([pL, pL], [yb-0.03, yb+0.03], color=DARK, lw=1.0)
        ax.plot([pR, pR], [yb-0.03, yb+0.03], color=DARK, lw=1.0)
        ax.text(p0, yb+0.055, case['dp_label'],
                ha='center', va='bottom', fontsize=9, color=TEXT)

        ax.axvline(p0, color=LIGHT, lw=0.9, ls=':')
        ax.text(
            p0, 0.86,
            'p = ħk = h/λ',
            ha='center', fontsize=9.2, color=TEXT
        )

    # Explicitly tie the intuitive picture to the Fourier uncertainty relation.
    fig.text(
        0.5, 0.045,
        '広い空間範囲に波が続くほど波長（波数 k）を正確に決められ、'
        '運動量 p=ħk も鋭く定まる。',
        ha='center', fontsize=9.6, color=TEXT
    )
    fig.text(
        0.5, 0.014,
        r'ガウス波束では $\sigma_x\sigma_p=\hbar/2$。'
        ' これは測定器の不足ではなく、波束そのもののフーリエ構造。',
        ha='center', fontsize=9.2, color=TEXT
    )

    fig.tight_layout(rect=[0, 0.085, 1, 0.91], h_pad=2.0, w_pad=1.7)
    save_assets(fig, 'fig23_uncertainty_wavepacket.eps')

def fig24_curse_dimensionality_nnqs():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.5))
    fig.suptitle('量子多体問題の「次元の呪い」とニューラル量子状態', fontsize=14, fontweight='bold', color=TEXT)

    ax = axs[0]; panel_label(ax, '(a) 状態数は指数関数的に爆発')
    N = np.arange(1, 31)
    dim = 2.0**N
    ax.semilogy(N, dim, color=AI, lw=2.2)
    ax.scatter([10, 20, 30], [2**10, 2**20, 2**30], color=AI, s=28)
    ax.text(10, 2**10*4, r'$2^{10}=1024$', ha='center', fontsize=8.5)
    ax.text(20, 2**20*4, r'$2^{20}\approx10^6$', ha='center', fontsize=8.5)
    ax.text(28, 2**30/8, '粒子を1個増やすだけで\n必要状態数が倍増', ha='right', fontsize=9, color=TEXT)
    ax.set_xlabel('2状態粒子の数  N'); ax.set_ylabel('ヒルベルト空間の次元  $2^N$')
    ax.grid(color=LIGHT, lw=0.5, which='both')

    ax = axs[1]; panel_label(ax, '(b) NNQS：巨大な波動関数を関数として圧縮')
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
    states = ['↑', '↓', '↑', '↑', '↓', '…']
    for i, s in enumerate(states):
        x0 = 0.7 + i*0.8
        ax.add_patch(Rectangle((x0, 5.1), 0.55, 0.7, facecolor=PALE, edgecolor=PHYS, lw=1.1))
        ax.text(x0+0.275, 5.45, s, ha='center', va='center', fontsize=10, color=TEXT)
    arrow(ax, (5.5, 5.45), (6.6, 5.45), color=DARK)
    box = FancyBboxPatch((6.7,4.65),2.1,1.6,boxstyle='round,pad=0.04',facecolor='white',edgecolor=AI,lw=1.6)
    ax.add_patch(box); ax.text(7.75,5.45,'Neural\nNetwork',ha='center',va='center',fontsize=10,color=TEXT)
    arrow(ax, (7.75, 4.6), (7.75, 3.45), color=AI)
    ax.add_patch(FancyBboxPatch((6.45,2.2),2.6,1.1,boxstyle='round,pad=0.04',facecolor='white',edgecolor=ACCENT,lw=1.6))
    ax.text(7.75,2.75,r'$\psi_\theta(s_1,\dots,s_N)$',ha='center',va='center',fontsize=12,color=TEXT)
    ax.text(4.8, 0.95, 'すべての振幅を表に保存せず、\n重要な相関構造をネットワークで表現', ha='center', fontsize=9, color=TEXT)

    fig.tight_layout(rect=[0, 0.03, 1, 0.90])
    save_assets(fig, 'fig24_curse_dimensionality_nnqs.eps')


def fig25_law_large_numbers():
    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.3))
    fig.suptitle('ミクロの偶然からマクロの確実性へ：大数の法則', fontsize=14, fontweight='bold', color=TEXT)
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
    ax.text(1e5, 2e-2, '粒子数が巨大になると、\nマクロな量はほとんど揺らがない', fontsize=9, color=TEXT)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_assets(fig, 'fig25_law_large_numbers.eps')


def fig26_quantum_statistics():
    """Compare MB, FD and BE statistics by their occupancy rules."""
    fig, axs = plt.subplots(1, 3, figsize=(12.2, 5.1))
    fig.suptitle(
        '三つの統計：違いは「同じ量子状態に何個入れるか」',
        fontsize=14, fontweight='bold', color=TEXT
    )

    configs = [
        {
            'title': '(a) Maxwell–Boltzmann',
            'subtitle': '古典極限：希薄なので量子効果を無視',
            'formula': r'$\langle n\rangle \simeq e^{-x}$',
            'rule1': '各状態の平均占有は小さい',
            'rule2': '高いエネルギーほど少ない',
            'example': '例：希薄な古典気体',
            'kind': 'mb',
        },
        {
            'title': '(b) Fermi–Dirac',
            'subtitle': 'フェルミ粒子：Pauli 排他原理',
            'formula': r'$\langle n\rangle = 1/(e^x+1)$',
            'rule1': '同じ量子状態には 1個まで',
            'rule2': r'$0\leq\langle n\rangle\leq1$',
            'example': '例：電子',
            'kind': 'fd',
        },
        {
            'title': '(c) Bose–Einstein',
            'subtitle': 'ボース粒子：同じ状態を共有できる',
            'formula': r'$\langle n\rangle = 1/(e^x-1)$',
            'rule1': '同じ量子状態に何個でも入れる',
            'rule2': '低エネルギー状態に集まりやすい',
            'example': '例：光子・ボース原子',
            'kind': 'be',
        },
    ]

    for ax, cfg in zip(axs, configs):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 8)
        ax.axis('off')

        panel_label(ax, cfg['title'])
        ax.text(
            3.0, 7.20, cfg['subtitle'],
            ha='center', fontsize=9.2, color=TEXT, fontweight='bold'
        )

        # Energy arrow and five single-particle quantum states.
        arrow(ax, (0.55, 1.70), (0.55, 5.95),
              color=MID, lw=1.1, ms=9)
        ax.text(0.28, 5.82, 'E', fontsize=9, color=SUBTEXT)
        levels = [2.05, 2.82, 3.59, 4.36, 5.13]
        for y in levels:
            ax.plot([1.05, 4.95], [y, y], color=LIGHT, lw=2.0)

        # Occupancy cartoons.  Every horizontal segment represents one
        # single-particle quantum state, not a degenerate energy shell.
        if cfg['kind'] == 'mb':
            # Dilute classical limit: sparse occupancy, mostly empty states.
            pts = [(1.55, levels[0]), (3.55, levels[1]), (2.55, levels[3])]
            for x0, y0 in pts:
                ax.plot(x0, y0, 'o', color=MID, ms=7, zorder=3)
            ax.text(
                3.0, 5.70, 'ほとんどの状態は空',
                ha='center', fontsize=8.5, color=SUBTEXT
            )

        elif cfg['kind'] == 'fd':
            # At most one identical fermion in one quantum state.
            pts = [(2.10, levels[0]), (3.25, levels[1]), (2.65, levels[2])]
            for x0, y0 in pts:
                ax.plot(x0, y0, 'o', color=DARK, ms=7, zorder=3)

            # Show an attempted second occupation as forbidden.
            x_forbid, y_forbid = 3.55, levels[0]
            ax.plot(x_forbid, y_forbid, 'o',
                    markerfacecolor='white', markeredgecolor=MID,
                    markeredgewidth=1.2, ms=7, zorder=3)
            ax.plot([x_forbid-0.12, x_forbid+0.12],
                    [y_forbid-0.12, y_forbid+0.12],
                    color=DARK, lw=1.2, zorder=4)
            ax.plot([x_forbid-0.12, x_forbid+0.12],
                    [y_forbid+0.12, y_forbid-0.12],
                    color=DARK, lw=1.2, zorder=4)
            ax.text(
                3.55, y_forbid+0.36, '2個目は不可',
                ha='center', fontsize=8.2, color=TEXT
            )

        else:
            # Several bosons may occupy exactly the same quantum state.
            low_y = levels[0]
            for x0 in [1.75, 2.35, 2.95, 3.55, 4.15]:
                ax.plot(x0, low_y, 'o', color=DARK, ms=7, zorder=3)
            for x0 in [2.25, 3.15]:
                ax.plot(x0, levels[1], 'o', color=MID, ms=6, zorder=3)
            ax.plot(3.15, levels[3], 'o', color=LIGHT,
                    markeredgecolor=MID, ms=5, zorder=3)
            ax.text(
                3.0, 5.70, '同じ最低状態に多数',
                ha='center', fontsize=8.5, color=SUBTEXT
            )

        # The core rule gets a dedicated box.
        box = FancyBboxPatch(
            (0.75, 0.70), 4.50, 0.76,
            boxstyle='round,pad=0.08,rounding_size=0.08',
            facecolor=PALE, edgecolor=MID, lw=1.0
        )
        ax.add_patch(box)
        ax.text(
            3.0, 1.08, cfg['rule1'],
            ha='center', va='center', fontsize=9.0,
            color=TEXT, fontweight='bold'
        )
        ax.text(
            3.0, 6.55, cfg['formula'],
            ha='center', fontsize=10.5, color=TEXT
        )
        ax.text(
            3.0, 0.36, cfg['rule2'],
            ha='center', fontsize=8.5, color=TEXT
        )
        ax.text(
            3.0, 7.72, cfg['example'],
            ha='center', fontsize=8.3, color=SUBTEXT
        )

    fig.text(
        0.5, 0.040,
        r'$x=(E-\mu)/k_BT$　　'
        '高温・低密度では量子効果が弱くなり、Fermi–Dirac と Bose–Einstein は '
        'Maxwell–Boltzmann に近づく。',
        ha='center', fontsize=9.1, color=TEXT
    )
    fig.text(
        0.5, 0.012,
        '要点：Fermi は「詰め込めない」、Bose は「同じ状態に集まれる」、'
        'Maxwell–Boltzmann はその違いが見えない希薄な古典極限。',
        ha='center', fontsize=9.3, color=TEXT
    )

    fig.tight_layout(rect=[0, 0.075, 1, 0.91], w_pad=1.1)
    save_assets(fig, 'fig26_quantum_statistics.eps')

def fig27_boltzmann_softmax():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.4))
    fig.suptitle('統計力学とAIの同型：ボルツマン分布とSoftmax', fontsize=14, fontweight='bold', color=TEXT)

    ax = axs[0]; panel_label(ax, '(a) 物理：低いエネルギーほど高確率')
    E = np.array([0.4, 1.0, 1.7, 2.4])
    w = np.exp(-E); P = w/w.sum()
    ax.bar(np.arange(4), P, edgecolor=PHYS, facecolor='white', lw=1.5)
    ax.set_xticks(np.arange(4), [r'$E_1$', r'$E_2$', r'$E_3$', r'$E_4$'])
    ax.set_ylabel('確率'); ax.set_ylim(0, 0.55)
    ax.text(1.5, 0.49, r'$P_i = e^{-E_i/k_BT}/Z$', ha='center', fontsize=11, color=TEXT)
    ax.grid(axis='y', color=LIGHT, lw=0.5)

    ax = axs[1]; panel_label(ax, '(b) AI：高いスコアほど高確率')
    score = -E
    w2 = np.exp(score); P2 = w2/w2.sum()
    ax.bar(np.arange(4), P2, edgecolor=AI, facecolor='white', lw=1.5)
    ax.set_xticks(np.arange(4), ['候補1','候補2','候補3','候補4'])
    ax.set_ylabel('Softmax確率'); ax.set_ylim(0, 0.55)
    ax.text(1.5, 0.49, r'$P_i = e^{x_i}/\sum_j e^{x_j}$', ha='center', fontsize=11, color=TEXT)
    ax.grid(axis='y', color=LIGHT, lw=0.5)
    fig.text(0.5, 0.025, r'対応：  $x_i \leftrightarrow -E_i/k_BT$     かつ     $\sum_j e^{x_j} \leftrightarrow Z$',
             ha='center', fontsize=10, color=TEXT)

    fig.tight_layout(rect=[0,0.06,1,0.90])
    save_assets(fig, 'fig27_boltzmann_softmax.eps')


def fig28_emergence_hierarchy():
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    fig.suptitle('More is different：階層ごとに新しい法則が創発する', fontsize=14, fontweight='bold', color=TEXT)
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
        ax.text(5, y+0.13, title, ha='center', va='center', fontsize=10, fontweight='bold', color=TEXT)
        ax.text(5, y-0.25, sub, ha='center', va='center', fontsize=8.5, color=SUBTEXT)
    for y in [1.75, 3.55, 5.35, 7.15]:
        arrow(ax, (4.35, y), (4.35, y+0.65), color=ACCENT, lw=1.4, ms=10)
        ax.text(3.55, y+0.25, '創発', ha='center', fontsize=8.8, color=TEXT)
    for y in [7.65, 5.85, 4.05, 2.25]:
        arrow(ax, (5.65, y), (5.65, y-0.65), color=MID, lw=1.0, ms=8)
    ax.text(7.6, 5.0, '上位の構造が下位の\n自由度を制約することもある', ha='center', fontsize=9, color=SUBTEXT)
    ax.text(7.55, 4.3, '（トップダウン因果）', ha='center', fontsize=8.5, color=SUBTEXT)

    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_assets(fig, 'fig28_emergence_hierarchy.eps')


def fig29_semiconductor_bands():
    fig, axs = plt.subplots(1, 3, figsize=(11.4, 4.5))
    fig.suptitle('バンドギャップと半導体：電子の「席」の空き方で電気伝導が決まる', fontsize=14, fontweight='bold', color=TEXT)
    labels = [('導体', 0.0), ('半導体', 1.1), ('絶縁体', 2.4)]
    for i, (title, gap) in enumerate(labels):
        ax = axs[i]; panel_label(ax, f'({chr(97+i)}) {title}')
        ax.set_xlim(0, 4); ax.set_ylim(0, 7); ax.axis('off')
        vb_top = 2.4
        cb_bot = vb_top + gap
        ax.add_patch(Rectangle((0.7,0.8),2.6,1.6,facecolor=PHYS,alpha=0.13,edgecolor=PHYS,lw=1.4))
        ax.text(2.0,1.55,'価電子帯',ha='center',fontsize=9,color=TEXT)
        if gap == 0:
            ax.add_patch(Rectangle((0.7,2.1),2.6,2.0,facecolor=AI,alpha=0.10,edgecolor=AI,lw=1.4))
            ax.text(2.0,3.25,'伝導帯と重なる',ha='center',fontsize=8.8,color=TEXT)
            arrow(ax,(2.0,2.0),(2.0,3.0),color=ACCENT,lw=1.3,ms=9)
        else:
            ax.add_patch(Rectangle((0.7,cb_bot),2.6,1.5,facecolor=AI,alpha=0.10,edgecolor=AI,lw=1.4))
            ax.text(2.0,cb_bot+0.75,'伝導帯',ha='center',fontsize=9,color=TEXT)
            ax.annotate('', xy=(3.55, cb_bot), xytext=(3.55, vb_top), arrowprops=dict(arrowstyle='<->', color=TEXT, lw=1.2))
            ax.text(3.72,(cb_bot+vb_top)/2,'gap',va='center',fontsize=8.5,color=TEXT)
            if i == 1:
                arrow(ax,(1.55,2.1),(1.55,cb_bot+0.2),color=ACCENT,lw=1.4,ms=10)
                ax.add_patch(Circle((1.55,1.95),0.08,facecolor='white',edgecolor=AI,lw=1.2))
                ax.text(2.0,5.9,'熱・光・電圧で\n励起可能',ha='center',fontsize=8.8,color=TEXT)
        ax.text(2.0,0.25,['自由に動ける','適度なギャップ','ギャップが大きい'][i],ha='center',fontsize=8.8,color=SUBTEXT)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_assets(fig, 'fig29_semiconductor_bands.eps')


def fig30_superconductivity_cooper_pair():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.5))
    fig.suptitle('超伝導：電子対が位相をそろえた巨大な量子状態', fontsize=14, fontweight='bold', color=TEXT)

    ax = axs[0]; panel_label(ax, '(a) 格子の歪みを介したクーパー対（模式図）')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    for ix in range(1,9):
        for iy in [2,3.5,5]:
            y = iy - 0.35*np.exp(-((ix-4.5)/1.3)**2)
            ax.add_patch(Circle((ix,y),0.12,facecolor=LIGHT,edgecolor=MID,lw=0.7))
    ax.add_patch(Circle((3.3,3.6),0.20,facecolor=AI,edgecolor='none'))
    ax.add_patch(Circle((6.1,3.1),0.20,facecolor=AI,edgecolor='none'))
    ax.text(3.3,4.15,'e-',ha='center',fontsize=10,color=TEXT)
    ax.text(6.1,3.65,'e-',ha='center',fontsize=10,color=TEXT)
    arrow(ax,(3.55,3.65),(5.85,3.2),color=ACCENT,lw=1.3,ms=9,style='<->')
    ax.text(4.7,2.0,'一方の電子が格子を歪ませ、\nもう一方を間接的に引き寄せる',ha='center',fontsize=9,color=TEXT)

    ax = axs[1]; panel_label(ax, '(b) 多数の対が位相をそろえて流れる')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    xs = np.linspace(0.7,9.2,400)
    for j, y0 in enumerate([2.0,3.2,4.4]):
        y = y0 + 0.22*np.sin(2.2*xs)
        ax.plot(xs,y,color=PHYS,lw=1.6)
        for x0 in np.linspace(1.2,8.8,7):
            ax.add_patch(Circle((x0, y0+0.22*np.sin(2.2*x0)),0.10,facecolor=ACCENT,edgecolor='none'))
    arrow(ax,(1.0,5.7),(8.9,5.7),color=PHYS,lw=1.8,ms=12)
    ax.text(5.0,6.05,'巨視的に同じ位相で流れる',ha='center',fontsize=9,color=TEXT)
    ax.text(5.0,0.9,'散乱が抑えられ、電気抵抗がゼロになる',ha='center',fontsize=9,color=TEXT)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_assets(fig, 'fig30_superconductivity_cooper_pair.eps')


def fig31_quantum_interference_vqe():
    fig, axs = plt.subplots(1, 2, figsize=(11.2, 4.6))
    fig.suptitle('量子計算の核心：干渉で答えを強め、VQEで古典AIと協調する', fontsize=14, fontweight='bold', color=TEXT)

    ax = axs[0]; panel_label(ax, '(a) 「全並列」ではなく振幅の干渉')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    labels = ['候補A','候補B','候補C','候補D']
    amps1 = [0.7,0.55,0.6,0.8]
    amps2 = [-0.65,-0.5,0.55,0.75]
    for i, lab in enumerate(labels):
        x0 = 1.2 + i*2.2
        ax.text(x0,6.1,lab,ha='center',fontsize=8.8,color=TEXT)
        ax.arrow(x0,3.4,0,amps1[i]*1.8,width=0.025,head_width=0.14,head_length=0.15,color=PHYS,length_includes_head=True)
        ax.arrow(x0+0.35,3.4,0,amps2[i]*1.8,width=0.025,head_width=0.14,head_length=0.15,color=AI,length_includes_head=True)
        result = amps1[i]+amps2[i]
        ax.arrow(x0+0.75,3.4,0,result*1.8,width=0.035,head_width=0.17,head_length=0.15,color=ACCENT,length_includes_head=True)
    ax.text(3.5,0.85,'誤答：山と谷を重ねて打ち消す',ha='center',fontsize=8.8,color=TEXT)
    ax.text(7.5,0.85,'正答：同符号の振幅を強める',ha='center',fontsize=8.8,color=TEXT)

    ax = axs[1]; panel_label(ax, '(b) VQE：量子–古典ハイブリッド')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    qbox = FancyBboxPatch((0.9,3.4),3.0,1.7,boxstyle='round,pad=0.04',facecolor='white',edgecolor=PHYS,lw=1.6)
    cbox = FancyBboxPatch((6.1,3.4),3.0,1.7,boxstyle='round,pad=0.04',facecolor='white',edgecolor=AI,lw=1.6)
    ax.add_patch(qbox); ax.add_patch(cbox)
    ax.text(2.4,4.25,'量子回路\n|ψ(θ)> を生成',ha='center',va='center',fontsize=9.5,color=TEXT)
    ax.text(7.6,4.25,'古典最適化\nθ を更新',ha='center',va='center',fontsize=9.5,color=TEXT)
    arrow(ax,(3.95,4.55),(6.05,4.55),color=DARK,lw=1.3,ms=10)
    ax.text(5.0,4.9,'エネルギー測定',ha='center',fontsize=8.3,color=SUBTEXT)
    arrow(ax,(6.05,3.85),(3.95,3.85),color=ACCENT,lw=1.3,ms=10)
    ax.text(5.0,3.3,'新しいパラメータ θ',ha='center',fontsize=8.3,color=TEXT)
    ax.text(5.0,1.55,'量子側：重ね合わせを作る\n古典側：損失を最小化する',ha='center',fontsize=9,color=TEXT)

    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_assets(fig, 'fig31_quantum_interference_vqe.eps')


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
    print(f'Generated 11 figures as EPS/SVG/PDF in {ROOT}')


if __name__ == '__main__':
    main()
