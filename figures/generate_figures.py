"""Generate grayscale textbook figure assets for "AI と物理学の系譜".

PDF is the primary LuaLaTeX/production asset, SVG is the editable vector master,
and EPS is retained as an optional compatibility/archival side output.
Primary text is black; dark gray is reserved for secondary text and graphical
structure.
"""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch, FancyBboxPatch

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
mpl.rcParams['text.color'] = TEXT
mpl.rcParams['axes.labelcolor'] = TEXT
mpl.rcParams['axes.titlecolor'] = TEXT
mpl.rcParams['xtick.color'] = TEXT
mpl.rcParams['ytick.color'] = TEXT


def save_assets(fig, name):
    stem = Path(name).stem
    fig.savefig(OUT / f"{stem}.eps", format='eps', bbox_inches='tight', pad_inches=0.12)
    fig.savefig(SVG_OUT / f"{stem}.svg", format='svg', bbox_inches='tight', pad_inches=0.12)
    fig.savefig(PDF_OUT / f"{stem}.pdf", format='pdf', bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)


def arrow(ax, xy1, xy2, color=DARK, lw=1.4, ms=12, style='-|>'):
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p


def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha='left', va='top',
            fontsize=9, fontweight='bold', color=SUBTEXT)


def fig00_knowledge_map():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(0, 1); ax.axis('off')
    nodes = [
        (0.08, '神話・観測', '経験'), (0.19, '古典力学', '運動・最適化'),
        (0.32, '熱・統計', 'エントロピー'), (0.45, '場・波', '伝播・変換'),
        (0.58, '相対論・量子', '幾何・確率'), (0.71, '複雑系', '創発・カオス'),
        (0.84, '宇宙論', '全体像'), (0.93, 'AI', '学習・発見')]
    ax.plot([0.06, 0.93], [0.56, 0.56], color=LIGHT, lw=3, zorder=0)
    for i, (x, title, sub) in enumerate(nodes):
        color = PHYS if i < 7 else AI
        ax.add_patch(Circle((x, 0.56), 0.022, facecolor='white', edgecolor=color, lw=2, zorder=2))
        y = 0.73 if i % 2 == 0 else 0.33
        box = FancyBboxPatch((x-0.058, y-0.075), 0.116, 0.15,
                             boxstyle='round,pad=0.012,rounding_size=0.015',
                             facecolor='white', edgecolor=color, lw=1.2)
        ax.add_patch(box)
        ax.text(x, y+0.022, title, ha='center', va='center', fontsize=9, color=TEXT, fontweight='bold')
        ax.text(x, y-0.03, sub, ha='center', va='center', fontsize=7.5, color=SUBTEXT)
        ax.plot([x, x], [0.56 + (0.025 if y > 0.56 else -0.025), y + (-0.075 if y > 0.56 else 0.075)], color=LIGHT, lw=1)
    ax.text(0.5, 0.94, 'AIと物理学の系譜：複雑な世界から法則を見つける知の流れ', ha='center', va='center', fontsize=14, fontweight='bold', color=TEXT)
    ax.text(0.50, 0.08, '観測 → モデル化 → 数学的圧縮 → 予測 → 理解 → 新しい発見', ha='center', va='center', fontsize=10, color=SUBTEXT)
    save_assets(fig, 'fig00_knowledge_map.eps')


def fig01_geocentric_heliocentric():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.5))
    fig.suptitle(
        '天動説と地動説：同じ観測を異なるモデルで説明する',
        fontsize=14,
        fontweight='bold',
        color=TEXT
    )

    th = np.linspace(0, 2*np.pi, 900)

    # -----------------------------
    # (a) Geocentric model
    # -----------------------------
    ax = axs[0]
    ax.set_aspect('equal')
    ax.axis('off')
    panel_label(ax, '(a) 天動説：周転円で逆行を説明')
    ax.set_xlim(-2.35, 2.35)
    ax.set_ylim(-2.05, 2.05)

    # Earth
    ax.add_patch(Circle((0, 0), 0.14, facecolor=PHYS, edgecolor='none'))
    ax.text(0, -0.32, '地球', ha='center', fontsize=9, color=TEXT)

    # Faint deferent circle
    R = 1.45
    ax.plot(R*np.cos(th), R*np.sin(th), color=LIGHT, lw=1.2)

    # Larger epicycle-like path for clearer retrograde impression
    center_angle = np.linspace(0, 2*np.pi, 900)
    Rc = 1.18
    re = 0.52
    cx = Rc * np.cos(center_angle)
    cy = Rc * np.sin(center_angle)
    ex = re * np.cos(4 * center_angle)
    ey = re * np.sin(4 * center_angle)

    path_x = cx + ex
    path_y = cy + ey

    ax.plot(path_x, path_y, color=AI, lw=1.9)

    # Planet marker
    idx = 120
    ax.add_patch(Circle((path_x[idx], path_y[idx]), 0.08, facecolor=AI, edgecolor='none'))

    ax.text(
        0, -1.82,
        '複雑な軌道を追加して観測に合わせる',
        ha='center',
        fontsize=9,
        color=SUBTEXT
    )

    # -----------------------------
    # (b) Heliocentric model
    # -----------------------------
    ax = axs[1]
    ax.set_aspect('equal')
    ax.axis('off')
    panel_label(ax, '(b) 地動説：太陽中心＋楕円軌道')
    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-2.05, 2.05)

    # Sun
    ax.add_patch(Circle((0, 0), 0.15, facecolor=ACCENT, edgecolor='none'))
    ax.text(0, -0.34, '太陽', ha='center', fontsize=9, color=TEXT)

    # Beautiful ellipses
    inner = Ellipse(
        xy=(0, 0),
        width=2.55,
        height=1.85,
        fill=False,
        edgecolor=PHYS,
        lw=1.7
    )
    outer = Ellipse(
        xy=(0, 0),
        width=4.15,
        height=2.85,
        fill=False,
        edgecolor=AI,
        lw=1.7
    )
    ax.add_patch(inner)
    ax.add_patch(outer)

    # Planet markers placed at visually balanced positions
    t1 = np.deg2rad(42)
    x1 = (2.55 / 2) * np.cos(t1)
    y1 = (1.85 / 2) * np.sin(t1)

    t2 = np.deg2rad(122)
    x2 = (4.15 / 2) * np.cos(t2)
    y2 = (2.85 / 2) * np.sin(t2)

    ax.add_patch(Circle((x1, y1), 0.07, facecolor=PHYS, edgecolor='none'))
    ax.add_patch(Circle((x2, y2), 0.08, facecolor=AI, edgecolor='none'))

    ax.text(
        0, -1.82,
        '基準系を変えると逆行は見かけの運動になる',
        ha='center',
        fontsize=9,
        color=SUBTEXT
    )

    fig.text(
        0.5, 0.03,
        'モデルの複雑さを増やすか、世界の見方そのものを変えるか',
        ha='center',
        fontsize=10,
        color=TEXT
    )

    fig.tight_layout(rect=[0, 0.06, 1, 0.91])
    save_assets(fig, 'fig01_geocentric_heliocentric.eps')



def fig02_gradient_descent():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    fig.suptitle('谷底へ向かう運動とAIの学習：共通する「勾配」の構造', fontsize=14, fontweight='bold', color=TEXT)
    x = np.linspace(-3.2, 3.2, 500)

    def draw_offset_descent(ax, f, pts, color, offset=0.28):
        """Draw a descent trajectory toward the global minimum with arrows offset from the curve."""
        ys = [f(p) for p in pts]
        ax.plot(pts, ys, 'o', ms=6, color=color, zorder=4)
        for p, q, y, yq in zip(pts[:-1], pts[1:], ys[:-1], ys[1:]):
            ax.annotate(
                '',
                xy=(q, yq + offset),
                xytext=(p, y + offset),
                arrowprops=dict(
                    arrowstyle='-|>',
                    color=color,
                    lw=1.25,
                    mutation_scale=11,
                    shrinkA=2,
                    shrinkB=2,
                ),
                zorder=5,
            )
        ax.plot(pts[-1], ys[-1], marker='*', ms=11, color=TEXT, zorder=6)
        ax.text(pts[-1], ys[-1]-0.12, '大域最小', ha='center', va='top',
                fontsize=8.3, color=TEXT, zorder=6)

    # (a) Physical potential: descend leftward toward the true global minimum.
    Vfun = lambda t: 0.12*t**4 - 0.75*t**2 + 0.18*t + 2.1
    V = Vfun(x)
    ax = axs[0]
    panel_label(ax, '(a) 物理：ポテンシャルの谷')
    ax.plot(x, V, color=PHYS, lw=2, zorder=2)
    pts = [-0.35, -0.70, -1.05, -1.35, -1.58, -1.74, -1.82]
    draw_offset_descent(ax, Vfun, pts, ACCENT)
    ax.set_ylim(bottom=0.25)
    ax.set_xlabel('位置  x')
    ax.set_ylabel('ポテンシャル  V(x)')
    ax.grid(color=LIGHT, linewidth=0.6)

    # (b) AI loss: use the same leftward descent orientation and target the global minimum.
    Lfun = lambda t: 0.10*t**4 - 0.62*t**2 + 0.12*t + 1.8
    L = Lfun(x)
    ax = axs[1]
    panel_label(ax, '(b) AI：損失関数の谷')
    ax.plot(x, L, color=AI, lw=2, zorder=2)
    pts = [-0.35, -0.70, -1.05, -1.35, -1.58, -1.72, -1.81]
    draw_offset_descent(ax, Lfun, pts, AI)
    ax.set_ylim(bottom=0.25)
    ax.set_xlabel('パラメータ  θ')
    ax.set_ylabel('損失  L(θ)')
    ax.grid(color=LIGHT, linewidth=0.6)

    fig.text(0.5,0.02,'傾き（微分）を使って「下る方向」を決める点が共通している',ha='center',fontsize=10,color=TEXT)
    fig.tight_layout(rect=[0,0.05,1,0.90])
    save_assets(fig, 'fig02_gradient_descent.eps')


def fig03_fermat_principle():
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw={'width_ratios':[1.1,1]})
    fig.suptitle('フェルマーの原理：光は「距離」ではなく「時間」を最小にする', fontsize=14, fontweight='bold', color=TEXT)
    ax=axs[0]; panel_label(ax,'(a) 2つの媒質を通る候補経路'); ax.set_xlim(-3,3); ax.set_ylim(-2.2,2.2); ax.axis('off'); ax.axhline(0,color=DARK,lw=1)
    ax.text(-2.8,1.72,'媒質1：速い',fontsize=9,color=TEXT); ax.text(-2.8,-1.9,'媒質2：遅い',fontsize=9,color=TEXT)
    S=(-2.4,1.45); T=(2.4,-1.45); ax.plot(*S,'o',color=PHYS,ms=7); ax.text(S[0]-0.2,S[1]+0.2,'S',fontsize=10); ax.plot(*T,'o',color=AI,ms=7); ax.text(T[0]+0.1,T[1]-0.1,'T',fontsize=10)
    for xc,c,lw in [(-0.8,LIGHT,1),(0.0,LIGHT,1),(0.65,ACCENT,2.2),(1.25,LIGHT,1)]: ax.plot([S[0],xc,T[0]],[S[1],0,T[1]],color=c,lw=lw)
    ax.text(0.72,0.18,'最短時間',fontsize=9,color=TEXT,fontweight='bold')
    ax=axs[1]; panel_label(ax,'(b) 境界を横切る位置と所要時間'); xc=np.linspace(-1.6,1.8,400); v1=2.0; v2=1.0
    tt=np.sqrt((xc-S[0])**2+S[1]**2)/v1 + np.sqrt((T[0]-xc)**2+T[1]**2)/v2; im=np.argmin(tt)
    ax.plot(xc,tt,color=DARK,lw=2); ax.plot(xc[im],tt[im],'o',color=ACCENT,ms=7); ax.axvline(xc[im],color=LIGHT,lw=1); ax.text(xc[im]+0.08,tt[im]+0.05,'最小',color=TEXT,fontsize=9)
    ax.set_xlabel('境界での通過位置'); ax.set_ylabel('所要時間'); ax.grid(color=LIGHT,linewidth=0.6)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_assets(fig, 'fig03_fermat_principle.eps')


def fig04_entropy_time_arrow():
    rng=np.random.default_rng(7); fig, axs=plt.subplots(1,4,figsize=(11,3.1))
    fig.suptitle('時間の矢：粒子は「特別な状態」から「ありふれた状態」へ広がる',fontsize=14,fontweight='bold',color=TEXT)
    for i,ax in enumerate(axs):
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_color(MID)
        n=90; frac=i/3; left_n=int(n*(1-frac)*0.95+n*frac*0.5); right_n=n-left_n
        x=np.concatenate([rng.uniform(0.06,0.46,left_n),rng.uniform(0.54,0.94,right_n)])
        y=np.concatenate([rng.uniform(0.06,0.94,left_n),rng.uniform(0.06,0.94,right_n)])
        ax.scatter(x,y,s=9,color=PHYS,edgecolors='none'); ax.axvline(0.5,color=LIGHT,lw=0.8,ls='--')
        ax.set_title(['低エントロピー','拡散開始','ほぼ均一','高エントロピー'][i],fontsize=9)
    fig.text(0.5,0.02,'ミクロな運動は可逆でも、マクロには「均一化する向き」が圧倒的に起こりやすい',ha='center',fontsize=10,color=TEXT)
    fig.tight_layout(rect=[0,0.07,1,0.88],w_pad=1.3); save_assets(fig, 'fig04_entropy_time_arrow.eps')


def fig05_diffusion_forward_reverse():
    rng=np.random.default_rng(12); base=np.zeros((10,10),dtype=int)
    for r,c in [(1,4),(1,5),(2,3),(2,6),(3,2),(3,7),(4,1),(4,8),(5,1),(5,8),(6,2),(6,7),(7,3),(7,6),(8,4),(8,5),(4,4),(4,5),(5,4),(5,5)]: base[r,c]=1
    levels=[0.0,0.15,0.35,0.50]; fig,axs=plt.subplots(2,4,figsize=(10.8,5.0))
    fig.suptitle('拡散モデル：秩序をノイズへ壊し、その過程を逆向きに学習する',fontsize=14,fontweight='bold',color=TEXT)
    def draw_grid(ax,arr):
        ax.set_xlim(0,10); ax.set_ylim(0,10); ax.set_aspect('equal'); ax.axis('off')
        for r in range(10):
            for c in range(10): ax.add_patch(Rectangle((c,9-r),1,1,facecolor=(DARK if arr[r,c] else 'white'),edgecolor=LIGHT,lw=0.25))
    arrays=[]
    for lv in levels:
        a=base.copy()
        if lv>0:
            mask=rng.random((10,10))<lv; noise=rng.integers(0,2,(10,10)); a=np.where(mask,noise,a)
        arrays.append(a)
    for i,a in enumerate(arrays): draw_grid(axs[0,i],a); axs[0,i].set_title(['$x_0$ データ','$x_{t_1}$','$x_{t_2}$','$x_T$ ノイズ'][i],fontsize=9)
    for j,i in enumerate([3,2,1,0]): draw_grid(axs[1,j],arrays[i]); axs[1,j].set_title(['$x_T$ ノイズ','$x_{t_2}$','$x_{t_1}$','$x_0$ 生成'][j],fontsize=9)
    fig.text(0.02,0.73,'Forward\nnoise',ha='left',va='center',fontsize=9,color=TEXT,fontweight='bold'); fig.text(0.02,0.29,'Reverse\ndenoise',ha='left',va='center',fontsize=9,color=TEXT,fontweight='bold')
    fig.text(0.5,0.02,'学習対象は「完成画像」そのものではなく、各段階でノイズを取り除く方向',ha='center',fontsize=10,color=TEXT)
    fig.tight_layout(rect=[0.06,0.06,1,0.90],h_pad=1.2,w_pad=1.0); save_assets(fig, 'fig05_diffusion_forward_reverse.eps')


def main():
    fig00_knowledge_map(); fig01_geocentric_heliocentric(); fig02_gradient_descent()
    fig03_fermat_principle(); fig04_entropy_time_arrow(); fig05_diffusion_forward_reverse()
    print(f'Generated 6 figures as EPS/SVG/PDF in {ROOT}')

if __name__ == '__main__':
    main()
