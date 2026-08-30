"""Generate editable EPS figures for chapters 13–15 of AI と物理学の系譜."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch, Polygon, Wedge

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


def fig32_reduction_hierarchy():
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    fig.suptitle('究極のマトリョーシカ：物質をどこまで分解できるか',
                 fontsize=14, fontweight='bold', color=DARK)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off')
    nodes = [
        (1.0, '物質', 'macroscopic'),
        (3.0, '分子', r'H$_2$O など'),
        (5.0, '原子', '原子核 + 電子'),
        (7.0, '原子核', '陽子 + 中性子'),
        (9.0, '核子', '陽子・中性子'),
        (11.0, 'クォーク', 'u, d, …'),
    ]
    radii = [0.60, 0.52, 0.46, 0.40, 0.34, 0.28]
    for i, ((x, title, sub), r) in enumerate(zip(nodes, radii)):
        col = PHYS if i < 4 else AI
        ax.add_patch(Circle((x, 3.2), r, facecolor='white', edgecolor=col, lw=2))
        ax.text(x, 3.2, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=DARK)
        ax.text(x, 2.25, sub, ha='center', fontsize=7.8, color=MID)
        if i < len(nodes)-1:
            arrow(ax, (x+r+0.12, 3.2), (nodes[i+1][0]-radii[i+1]-0.12, 3.2), color=ACCENT, lw=1.3, ms=10)
    ax.text(6.0, 4.9, '「基本粒子」を探す歴史は、発見のたびにさらに内側へ進んだ',
            ha='center', fontsize=9.5, color=DARK)
    ax.text(6.0, 0.85, '標準模型では、クォークとレプトンが物質の基本的な構成要素として整理される',
            ha='center', fontsize=9, color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.90])
    save_eps(fig, 'fig32_reduction_hierarchy.eps')


def fig33_standard_model_map():
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    fig.suptitle('標準模型：物質を作る粒子・力を伝える粒子・ヒッグス',
                 fontsize=14, fontweight='bold', color=DARK)
    ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis('off')
    ax.text(3.3, 8.25, '3世代のフェルミ粒子', ha='center', fontsize=11, fontweight='bold', color=PHYS)
    ax.text(8.85, 8.25, 'ボース粒子', ha='center', fontsize=11, fontweight='bold', color=AI)
    genx = [1.55, 3.25, 4.95]
    for j, x in enumerate(genx, start=1):
        ax.text(x, 7.55, f'第{j}世代', ha='center', fontsize=8.6, color=MID)
    fermions = [
        ('u','c','t','クォーク +2/3'),
        ('d','s','b','クォーク −1/3'),
        ('e','μ','τ','荷電レプトン'),
        ('νe','νμ','ντ','ニュートリノ'),
    ]
    ys = [6.55, 5.15, 3.35, 1.95]
    for row, (a,b,c,label) in enumerate(fermions):
        y=ys[row]
        ax.text(0.25, y, label, va='center', fontsize=8.5, color=MID)
        for x, sym in zip(genx,[a,b,c]):
            rect=FancyBboxPatch((x-0.55,y-0.45),1.1,0.9,boxstyle='round,pad=0.02',facecolor='white',edgecolor=PHYS,lw=1.4)
            ax.add_patch(rect); ax.text(x,y,sym,ha='center',va='center',fontsize=11,color=DARK)
    bosons=[('γ','電磁気力'),('g','強い力'),('W±, Z','弱い力'),('H','ヒッグス')]
    bys=[6.55,5.15,3.35,1.95]
    for y,(sym,label) in zip(bys,bosons):
        rect=FancyBboxPatch((7.15,y-0.45),1.8,0.9,boxstyle='round,pad=0.02',facecolor='white',edgecolor=AI,lw=1.4)
        ax.add_patch(rect); ax.text(8.05,y,sym,ha='center',va='center',fontsize=11,color=DARK)
        ax.text(9.25,y,label,va='center',fontsize=9,color=MID)
    ax.add_patch(FancyBboxPatch((7.0,0.45),4.1,0.75,boxstyle='round,pad=0.02',facecolor=PALE,edgecolor=MID,lw=1.1))
    ax.text(9.05,0.825,'重力は標準模型の外側',ha='center',va='center',fontsize=9,color=DARK)
    ax.text(6.0,0.05,'12種類のフェルミ粒子 + 4種類のゲージ粒子 + 1種類のヒッグス粒子 = 17種類',
            ha='center',fontsize=9.3,color=ACCENT)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig, 'fig33_standard_model_map.eps')


def fig34_feynman_gnn():
    fig, axs = plt.subplots(1,2,figsize=(10.8,4.5))
    fig.suptitle('点と線で相互作用を表す：ファインマン・ダイアグラムとGNN',
                 fontsize=14,fontweight='bold',color=DARK)
    ax=axs[0]; panel_label(ax,'(a) 物理：ファインマン・ダイアグラム')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    v1=(4.1,4.8); v2=(5.9,2.2)
    ax.plot([0.8,v1[0],9.2],[5.9,v1[1],5.4],color=PHYS,lw=2)
    ax.plot([0.8,v2[0],9.2],[1.1,v2[1],1.6],color=PHYS,lw=2)
    tt=np.linspace(0,1,180)
    xx=v1[0]+(v2[0]-v1[0])*tt
    yy=v1[1]+(v2[1]-v1[1])*tt + 0.16*np.sin(12*np.pi*tt)
    ax.plot(xx,yy,color=AI,lw=1.7)
    ax.add_patch(Circle(v1,0.10,facecolor=ACCENT,edgecolor='none'))
    ax.add_patch(Circle(v2,0.10,facecolor=ACCENT,edgecolor='none'))
    ax.text(5.65,3.75,'交換粒子（光子）',ha='center',fontsize=8.7,color=AI,rotation=-52)
    ax.text(5.0,0.45,'線＝粒子の伝播、頂点＝相互作用',ha='center',fontsize=9,color=DARK)
    ax=axs[1]; panel_label(ax,'(b) AI：グラフニューラルネットワーク')
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    pts=np.array([[1.5,1.7],[2.1,5.2],[4.1,3.6],[6.4,5.0],[7.8,2.0],[9.0,4.0]])
    edges=[(0,2),(1,2),(2,3),(2,4),(3,5),(4,5)]
    for a,b in edges:
        ax.plot([pts[a,0],pts[b,0]],[pts[a,1],pts[b,1]],color=LIGHT,lw=2)
    for i,(x,y) in enumerate(pts):
        ax.add_patch(Circle((x,y),0.25,facecolor='white',edgecolor=AI,lw=1.5))
        ax.text(x,y,str(i+1),ha='center',va='center',fontsize=8,color=DARK)
    arrow(ax,(2.8,3.95),(3.65,3.7),color=ACCENT,lw=1.3,ms=9)
    ax.text(5.0,0.45,'ノードとエッジの関係を学習する',ha='center',fontsize=9,color=DARK)
    fig.text(0.5,0.02,'同じものではないが、「複雑な関係を点と線のグラフとして扱う」という発想が共通する',
             ha='center',fontsize=9.2,color=MID)
    fig.tight_layout(rect=[0,0.06,1,0.90])
    save_eps(fig,'fig34_feynman_gnn.eps')


def fig35_higgs_symmetry_breaking():
    fig, axs = plt.subplots(1,2,figsize=(10.6,4.5))
    fig.suptitle('ヒッグス機構：対称な法則から非対称な真空が選ばれる',
                 fontsize=14,fontweight='bold',color=DARK)
    ax=axs[0]; panel_label(ax,'(a) 高温：対称な状態')
    phi=np.linspace(-2.2,2.2,400)
    Vhot=0.45*phi**2+0.12*phi**4
    ax.plot(phi,Vhot,color=PHYS,lw=2.2)
    ax.plot(0,0,'o',color=ACCENT,ms=7)
    ax.set_xlabel('場  φ'); ax.set_ylabel('ポテンシャル V(φ)')
    ax.grid(color=LIGHT,lw=0.5)
    ax.text(0,2.35,'最低点は φ=0',ha='center',fontsize=9,color=DARK)
    ax=axs[1]; panel_label(ax,'(b) 冷却後：自発的対称性の破れ')
    Vcold=0.18*phi**4-0.75*phi**2+0.80
    ax.plot(phi,Vcold,color=AI,lw=2.2)
    imin=np.argmin(Vcold[:len(phi)//2]); leftx=phi[imin]; lefty=Vcold[imin]
    ax.plot(leftx,lefty,'o',color=ACCENT,ms=7)
    ax.plot(-leftx,lefty,'o',mfc='white',mec=ACCENT,ms=7)
    ax.set_xlabel('場  φ'); ax.set_ylabel('ポテンシャル V(φ)')
    ax.grid(color=LIGHT,lw=0.5)
    ax.text(0,2.35,'法則は左右対称でも、\n真空はどちらか一方を選ぶ',ha='center',fontsize=9,color=DARK)
    fig.tight_layout(rect=[0,0.03,1,0.90])
    save_eps(fig,'fig35_higgs_symmetry_breaking.eps')


def fig36_lhc_trigger_funnel():
    fig, ax = plt.subplots(figsize=(9.0,5.4))
    fig.suptitle('LHCとAIトリガー：膨大な衝突から「残すべき事象」を選ぶ',
                 fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
    layers=[
        (1.0,8.3,8.0,1.0,r'陽子衝突：およそ $4\times10^7$ 回/秒',PHYS),
        (1.8,6.4,6.4,1.0,'超高速トリガー：粗い特徴で大幅削減',MID),
        (2.7,4.5,4.6,1.0,'高レベル解析：再構成・機械学習',AI),
        (3.7,2.6,2.6,1.0,'保存候補',ACCENT),
    ]
    for x,y,w,h,text,col in layers:
        trap=Polygon([[x,y],[x+w,y],[x+w-0.45,y-h],[x+0.45,y-h]],closed=True,facecolor='white',edgecolor=col,lw=1.6)
        ax.add_patch(trap); ax.text(x+w/2,y-h/2,text,ha='center',va='center',fontsize=9,color=DARK)
    for y1,y2 in [(7.25,6.5),(5.35,4.6),(3.45,2.7)]:
        arrow(ax,(5.0,y1),(5.0,y2),color=DARK,lw=1.2,ms=10)
    ax.text(5.0,1.3,r'概念図：原稿では最終的に約 $10^{-5}$ まで絞り込んで保存',ha='center',fontsize=9,color=MID)
    ax.text(5.0,0.65,'未知の物理を探すには「既知に似た事象だけ残す」バイアスにも注意が必要',ha='center',fontsize=9,color=AI)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig36_lhc_trigger_funnel.eps')


def fig37_hubble_law():
    fig, ax = plt.subplots(figsize=(7.8,5.0))
    fig.suptitle('膨張する宇宙：距離が遠い銀河ほど速く遠ざかる',
                 fontsize=14,fontweight='bold',color=DARK)
    panel_label(ax,'(a) ハッブル＝ルメートルの法則（模式データ）')
    rng=np.random.default_rng(7)
    d=np.linspace(20,420,28)
    H0=70.0
    v=H0*d+rng.normal(0,1800,len(d))
    ax.scatter(d,v,s=28,color=PHYS,alpha=0.85,label='銀河（模式）')
    xx=np.linspace(0,450,200)
    ax.plot(xx,H0*xx,color=AI,lw=2,label=r'$v=H_0 d$')
    ax.set_xlabel('距離 d [Mpc]'); ax.set_ylabel('後退速度 v [km/s]')
    ax.grid(color=LIGHT,lw=0.5); ax.legend(frameon=False,fontsize=8.5)
    ax.text(230,5000,r'傾き $H_0$ が現在の'+'\n'+'宇宙膨張率を表す',fontsize=9,color=DARK)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig37_hubble_law.eps')


def fig38_cosmic_timeline():
    fig, ax = plt.subplots(figsize=(11.5,3.8))
    fig.suptitle('宇宙史の見取り図：量子ゆらぎから銀河へ',fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    xs=[0.06,0.20,0.34,0.51,0.72,0.93]
    titles=['インフレーション','熱いビッグバン','元素合成','CMB\n(約38万年)','星・銀河形成','現在\n約138億年']
    subs=['急膨張','再加熱','最初の数分','宇宙の晴れ上がり','密度ゆらぎが成長','加速膨張']
    ax.plot([xs[0],xs[-1]],[0.50,0.50],color=LIGHT,lw=4)
    for i,(x,t,s) in enumerate(zip(xs,titles,subs)):
        col=ACCENT if i<2 else PHYS if i<5 else AI
        ax.add_patch(Circle((x,0.50),0.022,facecolor='white',edgecolor=col,lw=2))
        y=0.72 if i%2==0 else 0.28
        ax.text(x,y,t,ha='center',va='center',fontsize=9,fontweight='bold',color=DARK)
        ax.text(x,y-0.11 if y>0.5 else y+0.11,s,ha='center',va='center',fontsize=7.8,color=MID)
        ax.plot([x,x],[0.525 if y>0.5 else 0.475, y-0.06 if y>0.5 else y+0.06],color=LIGHT,lw=1)
    ax.text(0.5,0.93,'時間軸は概念図（縮尺は対数的な宇宙史を正確には表していない）',ha='center',fontsize=8.6,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.90])
    save_eps(fig,'fig38_cosmic_timeline.eps')


def fig39_universe_composition():
    fig, ax = plt.subplots(figsize=(7.2,5.6))
    fig.suptitle('宇宙の成分：私たちが知る通常物質は約5%',fontsize=14,fontweight='bold',color=DARK)
    sizes=[5,27,68]
    labels=['通常物質\n5%','ダークマター\n27%','ダークエネルギー\n68%']
    wedges, texts=ax.pie(sizes,labels=None,startangle=90,counterclock=False,
                         wedgeprops=dict(width=0.42,edgecolor='white'))
    angles=np.cumsum([0]+sizes)
    mids=(angles[:-1]+angles[1:])/2
    for lab,mid in zip(labels,mids):
        angle=np.deg2rad(90-3.6*mid)
        ax.text(1.18*np.cos(angle),1.18*np.sin(angle),lab,ha='center',va='center',fontsize=9,color=DARK)
    ax.text(0,0,'宇宙の\nエネルギー収支',ha='center',va='center',fontsize=10,fontweight='bold',color=DARK)
    ax.set_aspect('equal')
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig39_universe_composition.eps')


def fig40_gravitational_chirp():
    fig, axs = plt.subplots(2,1,figsize=(9.2,6.0),sharex=True)
    fig.suptitle('重力波の「チャープ」：合体直前に振幅と周波数が上がる',fontsize=14,fontweight='bold',color=DARK)
    t=np.linspace(-1.0,0,2400)
    tau=np.clip(-t,0.015,None)
    phase=48*(tau**0.42)
    amp=0.15+0.75*(1-tau)**2
    sig=amp*np.sin(phase)
    ax=axs[0]; panel_label(ax,'(a) 時系列波形')
    ax.plot(t,sig,color=PHYS,lw=1.2)
    ax.set_ylabel('ひずみ（規格化）'); ax.grid(color=LIGHT,lw=0.45)
    ax.annotate('合体',xy=(-0.02,0.7),xytext=(-0.34,1.0),arrowprops=dict(arrowstyle='->',color=AI),fontsize=9,color=AI)
    f=1/(tau**0.55)
    f=np.clip(f,0,10)
    ax=axs[1]; panel_label(ax,'(b) 周波数の上昇')
    ax.plot(t,f,color=AI,lw=2)
    ax.set_xlabel('合体までの時間'); ax.set_ylabel('周波数（規格化）'); ax.grid(color=LIGHT,lw=0.45)
    ax.text(-0.55,7.5,'CNNなどはノイズ中の\n特徴的な時間周波数パターンを探す',ha='center',fontsize=9,color=DARK)
    fig.tight_layout(rect=[0,0.03,1,0.91])
    save_eps(fig,'fig40_gravitational_chirp.eps')


def fig41_holographic_principle():
    fig, ax = plt.subplots(figsize=(9.0,5.5))
    fig.suptitle('ホログラフィック原理：内部の情報が境界面で記述されるという発想',fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    ax.add_patch(Rectangle((0.8,1.0),2.0,5.0,facecolor=PALE,edgecolor=PHYS,lw=1.6))
    for i in range(4):
        for j in range(9):
            if (i+j)%2==0:
                ax.add_patch(Circle((1.15+0.43*i,1.35+0.5*j),0.055,facecolor=PHYS,edgecolor='none'))
    ax.text(1.8,6.35,'低次元の境界',ha='center',fontsize=9,color=PHYS)
    for y in [2.0,3.4,4.8]:
        arrow(ax,(3.0,y),(4.6,y),color=ACCENT,lw=1.2,ms=9)
    theta=np.linspace(0,2*np.pi,300)
    ax.plot(7.0+2.0*np.cos(theta),3.5+2.0*np.sin(theta),color=AI,lw=1.8)
    ax.plot(7.0+1.3*np.cos(theta),3.5+1.3*np.sin(theta),color=LIGHT,lw=1.2)
    rng=np.random.default_rng(4)
    pts=rng.normal(size=(35,2)); pts=pts/np.maximum(np.linalg.norm(pts,axis=1,keepdims=True),1)*rng.uniform(0.2,1.6,(35,1))
    ax.scatter(7+pts[:,0],3.5+pts[:,1],s=14,color=MID)
    ax.text(7.0,6.35,'高次元の「バルク」',ha='center',fontsize=9,color=AI)
    ax.text(5.0,0.45,'ブラックホールではエントロピーが体積ではなく表面積に比例することが出発点',ha='center',fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig41_holographic_principle.eps')


def fig42_math_intuition_proof_loop():
    fig, ax = plt.subplots(figsize=(9.5,5.4))
    fig.suptitle('数学の二輪馬車：直感で予想し、論理で証明する',fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
    boxes=[
        (0.7,3.0,2.1,1.1,'例・データ・図形',MID),
        (3.2,4.7,2.1,1.1,'直感・AI\nパターン発見',AI),
        (6.3,4.7,2.1,1.1,'予想\nConjecture',ACCENT),
        (6.3,1.4,2.1,1.1,'厳密な証明\nProof',PHYS),
        (3.2,1.4,2.1,1.1,'定理・新しい構造',PHYS),
    ]
    for x,y,w,h,txt,col in boxes:
        r=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03,rounding_size=0.08',facecolor='white',edgecolor=col,lw=1.5)
        ax.add_patch(r); ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=9.3,color=DARK)
    arrow(ax,(2.8,3.55),(3.15,5.05),color=AI)
    arrow(ax,(5.3,5.25),(6.25,5.25),color=ACCENT)
    arrow(ax,(7.35,4.65),(7.35,2.55),color=PHYS)
    arrow(ax,(6.25,1.95),(5.35,1.95),color=PHYS)
    arrow(ax,(4.2,2.55),(2.75,3.2),color=MID)
    ax.text(5.0,6.35,'AIは「筋の良い仮説」を広い探索空間から提案できる',ha='center',fontsize=9,color=AI)
    ax.text(5.0,0.55,'人間・AI・形式証明器が役割を分担しながら循環する研究プロセス',ha='center',fontsize=9,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig42_math_intuition_proof_loop.eps')


def fig43_formal_proof_pipeline():
    fig, ax = plt.subplots(figsize=(10.5,5.0))
    fig.suptitle('形式数学：もっともらしい証明を「機械検証済みの証明」へ',fontsize=14,fontweight='bold',color=DARK)
    ax.set_xlim(0,12); ax.set_ylim(0,7); ax.axis('off')
    items=[
        (0.5,4.4,2.2,1.2,'自然言語の\n数学問題',MID),
        (3.2,4.4,2.2,1.2,'AIが候補手順・\nLeanコードを提案',AI),
        (5.9,4.4,2.2,1.2,'形式証明器が\n1ステップずつ検査',PHYS),
        (9.0,4.4,2.2,1.2,'検証済み\n証明',ACCENT),
    ]
    for x,y,w,h,txt,col in items:
        r=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03,rounding_size=0.08',facecolor='white',edgecolor=col,lw=1.5)
        ax.add_patch(r); ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=9,color=DARK)
    for x1,x2 in [(2.7,3.15),(5.4,5.85),(8.1,8.95)]:
        arrow(ax,(x1,5.0),(x2,5.0),color=DARK,lw=1.2,ms=9)
    ax.add_patch(FancyBboxPatch((5.7,1.3),2.6,1.1,boxstyle='round,pad=0.03',facecolor=PALE,edgecolor=AI,lw=1.3))
    ax.text(7.0,1.85,'論理エラー／探索行き詰まり',ha='center',va='center',fontsize=8.8,color=AI)
    arrow(ax,(7.0,4.35),(7.0,2.45),color=AI,lw=1.2,ms=9)
    arrow(ax,(5.65,1.85),(4.3,4.35),color=AI,lw=1.2,ms=9)
    ax.text(3.0,0.65,'AIの「幻覚」は証明器が拒否し、候補探索へ戻す',ha='center',fontsize=9,color=AI)
    ax.text(9.3,0.65,'正しさの検査と「人間が理解できるか」は別問題',ha='center',fontsize=9,color=MID)
    fig.tight_layout(rect=[0,0.02,1,0.92])
    save_eps(fig,'fig43_formal_proof_pipeline.eps')


def main():
    fig32_reduction_hierarchy()
    fig33_standard_model_map()
    fig34_feynman_gnn()
    fig35_higgs_symmetry_breaking()
    fig36_lhc_trigger_funnel()
    fig37_hubble_law()
    fig38_cosmic_timeline()
    fig39_universe_composition()
    fig40_gravitational_chirp()
    fig41_holographic_principle()
    fig42_math_intuition_proof_loop()
    fig43_formal_proof_pipeline()
    print(f'Generated 12 EPS figures in {OUT}')


if __name__ == '__main__':
    main()
