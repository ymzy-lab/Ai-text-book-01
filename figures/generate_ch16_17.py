"""Generate editable EPS figures for chapters 16–17 of AI と物理学の系譜."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch

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


def fig44_spin_glass_landscape():
    fig, axs = plt.subplots(1, 2, figsize=(10.8, 4.5))
    fig.suptitle('フラストレーションが作る「多谷」の地形：スピンガラスとAI',
                 fontsize=14, fontweight='bold', color=DARK)
    ax = axs[0]; panel_label(ax, '(a) 3つのスピンでも全員を満足させられない')
    ax.set_xlim(0, 8); ax.set_ylim(0, 7); ax.axis('off')
    pts = np.array([[1.5,1.5],[6.5,1.5],[4.0,5.7]])
    bonds = [(0,1,'+'),(1,2,'+'),(2,0,'−')]
    for a,b,s in bonds:
        col = PHYS if s == '+' else AI
        ax.plot([pts[a,0],pts[b,0]],[pts[a,1],pts[b,1]],color=col,lw=2)
        mid=(pts[a]+pts[b])/2
        ax.text(mid[0],mid[1],s,fontsize=13,fontweight='bold',color=col,
                bbox=dict(boxstyle='circle,pad=0.15',fc='white',ec='none'))
    spins=['↑','↑','↓']
    for (x,y),s in zip(pts,spins):
        ax.add_patch(Circle((x,y),0.35,facecolor='white',edgecolor=ACCENT,lw=1.7))
        ax.text(x,y,s,ha='center',va='center',fontsize=15,color=DARK)
    ax.text(4.0,0.45,'結合条件が競合し、単純な一意の最小配置がなくなる',ha='center',fontsize=9,color=DARK)
    ax = axs[1]; panel_label(ax, '(b) エネルギー／損失地形は多数の谷と鞍点を持つ')
    x=np.linspace(-4,4,700)
    y=0.15*x**2 + 0.38*np.sin(2.7*x) + 0.24*np.sin(5.4*x+0.5) + 1.0
    ax.plot(x,y,color=PHYS,lw=2)
    mins=[]
    for i in range(1,len(x)-1):
        if y[i] < y[i-1] and y[i] < y[i+1]: mins.append(i)
    for i in mins[::2]:
        ax.plot(x[i],y[i],'o',color=AI,ms=5)
    ax.set_xlabel('高次元パラメータ空間の断面'); ax.set_ylabel('エネルギー／損失')
    ax.grid(color=LIGHT,lw=0.5)
    ax.text(0,2.25,'局所極小・平らな谷・鞍点が共存',ha='center',fontsize=9,color=DARK)
    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig,'fig44_spin_glass_landscape.eps')


def fig45_double_descent():
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    fig.suptitle('二重降下：モデルを大きくすると、誤差が再び下がることがある',
                 fontsize=14, fontweight='bold', color=DARK)
    panel_label(ax, '(a) テスト誤差 vs モデル複雑度（模式図）')
    x=np.linspace(0.05,2.8,700)
    classic=0.9/(x+0.22)+0.16*x
    peak=1.55*np.exp(-((x-1.15)/0.18)**2)
    post=0.42/(x+0.15)
    y=0.25 + 0.22*classic + peak + 0.5*post
    ax.plot(x,y,color=PHYS,lw=2.4)
    ax.axvline(1.15,color=AI,lw=1.3,ls='--')
    ax.text(1.15,y.max()+0.06,'補間限界\n$N\\approx D$',ha='center',fontsize=9,color=AI)
    ax.text(0.45,1.0,'第1の降下',ha='center',fontsize=9,color=ACCENT)
    ax.text(2.15,0.62,'第2の降下',ha='center',fontsize=9,color=ACCENT)
    ax.annotate('古典的な「ちょうど良い複雑さ」',xy=(0.75,y[np.argmin(abs(x-0.75))]),xytext=(0.15,1.65),
                arrowprops=dict(arrowstyle='->',color=MID),fontsize=8.7,color=MID)
    ax.set_xlabel('モデル複雑度 / パラメータ数'); ax.set_ylabel('テスト誤差')
    ax.set_ylim(0.35,y.max()+0.35); ax.grid(color=LIGHT,lw=0.5)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig45_double_descent.eps')


def fig46_grokking_learning_curve():
    fig, ax = plt.subplots(figsize=(8.4,5.1))
    fig.suptitle('グロッキング：訓練データの暗記の後で、テスト性能が突然跳ね上がる',
                 fontsize=14,fontweight='bold',color=DARK)
    panel_label(ax,'(a) 正解率の時間発展（模式図）')
    t=np.linspace(0,100,600)
    train=1/(1+np.exp(-(t-12)/3.2))
    test=0.15 + 0.84/(1+np.exp(-(t-68)/3.8))
    ax.plot(t,train,color=PHYS,lw=2,label='訓練正解率')
    ax.plot(t,test,color=AI,lw=2.2,label='テスト正解率')
    ax.axvline(68,color=ACCENT,lw=1.2,ls='--')
    ax.text(68,0.52,'Grokking\n相転移的な急上昇',ha='center',fontsize=9,color=ACCENT)
    ax.text(36,0.40,'長い「暗記」期間',ha='center',fontsize=9,color=MID)
    ax.set_xlabel('学習ステップ'); ax.set_ylabel('正解率')
    ax.set_ylim(0,1.08); ax.grid(color=LIGHT,lw=0.5); ax.legend(frameon=False,fontsize=8.5,loc='lower right')
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig46_grokking_learning_curve.eps')


def fig47_ntk_infinite_width():
    fig, ax = plt.subplots(figsize=(10.5,5.2))
    fig.suptitle('NTK：ネットワークを無限幅にすると、学習ダイナミクスが解析しやすくなる',
                 fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,12); ax.set_ylim(0,7); ax.axis('off')
    ax.text(2.3,6.2,'有限幅ネットワーク',ha='center',fontsize=10,fontweight='bold',color=AI)
    layers=[0.7,2.0,3.4,4.6]
    counts=[3,6,6,2]
    positions=[]
    for x,n in zip(layers,counts):
        ys=np.linspace(2.0,5.0,n)
        positions.append([(x,y) for y in ys])
        for y in ys:
            ax.add_patch(Circle((x,y),0.10,facecolor='white',edgecolor=AI,lw=1.0))
    for L1,L2 in zip(positions[:-1],positions[1:]):
        for a in L1:
            for b in L2:
                ax.plot([a[0],b[0]],[a[1],b[1]],color=LIGHT,lw=0.35)
    ax.text(2.6,1.0,'多数の重みが非線形に連成',ha='center',fontsize=8.8,color=MID)
    arrow(ax,(5.0,3.5),(6.3,3.5),color=ACCENT,lw=1.7,ms=12)
    ax.text(5.65,4.0,r'幅 $N\to\infty$',ha='center',fontsize=10,color=ACCENT)
    box=FancyBboxPatch((6.65,2.0),4.6,3.2,boxstyle='round,pad=0.04,rounding_size=0.10',facecolor='white',edgecolor=PHYS,lw=1.6)
    ax.add_patch(box)
    ax.text(8.95,4.65,'無限幅極限',ha='center',fontsize=10,fontweight='bold',color=PHYS)
    ax.text(8.95,3.75,r'$\Theta(x,x\prime)$ が学習中ほぼ固定',ha='center',fontsize=10,color=DARK)
    ax.text(8.95,2.95,'複雑なパラメータ更新を\nカーネルによる線形化された流れとして解析',ha='center',fontsize=9,color=DARK)
    ax.text(8.95,1.15,'「巨大化すると逆に単純化する」という物理学的な極限操作',ha='center',fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig47_ntk_infinite_width.eps')


def fig48_rg_deep_learning():
    fig, axs = plt.subplots(1,2,figsize=(11.2,5.0))
    fig.suptitle('スケールを変えて本質を残す：繰り込み群と深層学習',
                 fontsize=14,fontweight='bold',color=DARK)
    ax=axs[0]; panel_label(ax,'(a) 物理：粗視化（RG）')
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    rng=np.random.default_rng(5)
    stages=[(1.2,16,0.11,'ミクロ\nスピン'),(4.5,8,0.18,'ブロック化'),(7.7,4,0.29,'マクロ\n有効自由度')]
    for x0,n,r,label in stages:
        cols=int(np.sqrt(n)); rows=int(np.ceil(n/cols))
        for k in range(n):
            cx=x0+(k%cols)*2*r*1.5; cy=2.4+(k//cols)*2*r*1.5
            ax.add_patch(Circle((cx,cy),r,facecolor=PHYS if rng.random()>0.5 else 'white',edgecolor=PHYS,lw=0.8))
        ax.text(x0+0.6,6.5,label,ha='center',fontsize=9,color=DARK)
    arrow(ax,(3.1,3.7),(4.0,3.7),color=ACCENT); arrow(ax,(6.5,3.7),(7.2,3.7),color=ACCENT)
    ax.text(5.0,0.8,'細部を捨て、スケールを上げても残る性質を抽出',ha='center',fontsize=9,color=MID)
    ax=axs[1]; panel_label(ax,'(b) AI：層を深くするほど抽象化')
    ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis('off')
    boxes=[(0.45,3.0,1.5,1.3,'pixels\n点・色'),(2.7,3.0,1.5,1.3,'edges\n線・境界'),(5.0,3.0,1.5,1.3,'parts\n目・タイヤ'),(7.3,3.0,2.0,1.3,'concept\n犬・車・意味')]
    for i,(x,y,w,h,txt) in enumerate(boxes):
        col=PHYS if i<2 else AI
        rect=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03',facecolor='white',edgecolor=col,lw=1.4)
        ax.add_patch(rect); ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=9,color=DARK)
        if i<len(boxes)-1:
            arrow(ax,(x+w+0.1,y+h/2),(boxes[i+1][0]-0.1,y+h/2),color=ACCENT,lw=1.2,ms=9)
    ax.text(5.0,6.35,'局所特徴 → 中間パーツ → 大域的な意味',ha='center',fontsize=9,color=DARK)
    ax.text(5.0,0.8,'対応は厳密な同一視ではなく、「粗視化と階層的表現」という数学的類似',ha='center',fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig,'fig48_rg_deep_learning.eps')


def fig49_five_paradigms():
    fig, ax = plt.subplots(figsize=(11.5,4.4))
    fig.suptitle('科学の5つのパラダイム：神話からAI駆動型科学へ',
                 fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    xs=[0.07,0.27,0.47,0.67,0.88]
    titles=['第1\n経験・神話','第2\n理論科学','第3\n計算科学','第4\nデータ駆動','第5\nAI駆動']
    subs=['観測・記録','方程式・演繹','シミュレーション','統計・ML','発見・推論・協働']
    examples=['ティコ','ニュートン\nマクスウェル','数値計算\nカオス','LHC\nビッグデータ','Symbolic AI\nPINNs・証明支援']
    ax.plot([xs[0],xs[-1]],[0.52,0.52],color=LIGHT,lw=4)
    for i,x in enumerate(xs):
        col=PHYS if i<3 else AI if i==4 else ACCENT
        ax.add_patch(Circle((x,0.52),0.025,facecolor='white',edgecolor=col,lw=2))
        y=0.75 if i%2==0 else 0.30
        ax.text(x,y,titles[i],ha='center',va='center',fontsize=9.2,fontweight='bold',color=DARK)
        ax.text(x,y-0.13 if y>0.5 else y+0.13,subs[i],ha='center',fontsize=8.2,color=MID)
        ax.text(x,0.08,examples[i],ha='center',fontsize=7.8,color=col)
    ax.text(0.5,0.94,'知識の作り方そのものが変化してきた',ha='center',fontsize=9,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.90])
    save_eps(fig,'fig49_five_paradigms.eps')


def fig50_prediction_vs_understanding():
    fig, ax = plt.subplots(figsize=(8.6,5.6))
    fig.suptitle('「よく当たる」と「なぜ分かる」は別の軸である',fontsize=14,fontweight='bold',color=DARK)
    panel_label(ax,'(a) 予測性能と説明可能性の概念マップ')
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.set_xlabel('人間にとっての説明可能性 / Why')
    ax.set_ylabel('予測性能 / What・How')
    ax.grid(color=LIGHT,lw=0.5)
    pts=[
        (0.25,0.88,'巨大AI\n高精度・説明困難',AI),
        (0.78,0.66,'簡潔な理論\n因果構造が明示',PHYS),
        (0.70,0.30,'単純すぎるモデル',MID),
        (0.43,0.72,'Symbolic regression\n候補式',ACCENT),
    ]
    for x,y,label,col in pts:
        ax.scatter([x],[y],s=85,color=col)
        ax.text(x+0.025,y+0.025,label,fontsize=8.5,color=DARK)
    arrow(ax,(0.33,0.86),(0.67,0.75),color=ACCENT,lw=1.3,ms=10)
    ax.text(0.52,0.91,'目標：予測を「理解可能な構造」へ翻訳',ha='center',fontsize=9,color=ACCENT)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig50_prediction_vs_understanding.eps')


def fig51_self_referential_universe():
    fig, ax = plt.subplots(figsize=(8.0,7.0))
    fig.suptitle('自己言及する宇宙：宇宙が知能を生み、知能が宇宙を理解する',
                 fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.axis('off'); ax.set_aspect('equal')
    labels=['宇宙','物質・星','生命','人間の知能','AI','新しい科学']
    angles=np.linspace(np.pi/2,np.pi/2-2*np.pi,len(labels),endpoint=False)
    pts=np.c_[0.78*np.cos(angles),0.78*np.sin(angles)]
    for i,(x,y) in enumerate(pts):
        col=PHYS if i<3 else AI if i==4 else ACCENT if i==5 else MID
        ax.add_patch(Circle((x,y),0.17,facecolor='white',edgecolor=col,lw=1.6))
        ax.text(x,y,labels[i],ha='center',va='center',fontsize=8.5,color=DARK)
        nx,ny=pts[(i+1)%len(pts)]
        vec=np.array([nx-x,ny-y]); L=np.linalg.norm(vec); u=vec/L
        arrow(ax,(x+0.19*u[0],y+0.19*u[1]),(nx-0.19*u[0],ny-0.19*u[1]),color=LIGHT,lw=1.6,ms=10)
    ax.text(0,0.08,'法則',ha='center',fontsize=15,fontweight='bold',color=DARK)
    ax.text(0,-0.13,'観測 → 理解 → 創造 → 再観測',ha='center',fontsize=9,color=MID)
    ax.text(0,-1.08,'人間が宇宙を解き明かし、その法則でAIを作り、AIが次の発見を支援する循環',ha='center',fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig51_self_referential_universe.eps')


def main():
    fig44_spin_glass_landscape()
    fig45_double_descent()
    fig46_grokking_learning_curve()
    fig47_ntk_infinite_width()
    fig48_rg_deep_learning()
    fig49_five_paradigms()
    fig50_prediction_vs_understanding()
    fig51_self_referential_universe()
    print(f'Generated 8 EPS figures in {OUT}')


if __name__ == '__main__':
    main()
