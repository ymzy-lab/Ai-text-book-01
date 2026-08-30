"""Generate editable EPS figures for chapters 7–9 of AI と物理学の系譜."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "eps"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams["ps.fonttype"] = 3
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Noto Sans CJK JP Regular", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

PHYS = "#315A7D"; AI = "#A34E4E"; ACCENT = "#B07A2A"
DARK = "#20252B"; MID = "#68717B"; LIGHT = "#D9DEE3"; PALE = "#F3F5F7"

def save_eps(fig, name):
    fig.savefig(OUT / name, format="eps", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)

def arrow(ax, xy1, xy2, color=DARK, lw=1.4, ms=12, style="-|>"):
    p = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=color, shrinkA=0, shrinkB=0)
    ax.add_patch(p); return p

def panel_label(ax, text):
    ax.text(0.02, 0.98, text, transform=ax.transAxes, ha="left", va="top",
            fontsize=9, fontweight="bold", color=MID)

def fig13_light_cone_curvature():
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.5))
    fig.suptitle("光円錐と曲がった時空：因果律を幾何学で見る", fontsize=14, fontweight="bold", color=DARK)
    ax = axs[0]; panel_label(ax, "(a) 平らな時空：光円錐")
    ax.set_xlim(-4, 4); ax.set_ylim(-0.5, 5.5); ax.spines[["top","right"]].set_visible(False)
    ax.set_xlabel("空間  x"); ax.set_ylabel("時間  ct")
    ax.plot([-4,4],[0,0],color=DARK,lw=1); ax.plot([0,0],[0,5.2],color=DARK,lw=1)
    ax.plot([0,4.2],[0,4.2],color=PHYS,lw=2); ax.plot([0,-4.2],[0,4.2],color=PHYS,lw=2)
    ax.fill_between([-3.7,0,3.7],[3.7,0,3.7],[5.2,5.2,5.2],color=PALE)
    ax.text(0,4.65,"未来光円錐",ha="center",fontsize=9,color=PHYS)
    ax.text(0,2.0,"因果的に\n到達可能",ha="center",fontsize=9,color=DARK)
    ax.text(3.0,2.0,"Elsewhere",ha="center",fontsize=8.5,color=MID); ax.text(-3.0,2.0,"Elsewhere",ha="center",fontsize=8.5,color=MID)
    ax.grid(color=LIGHT,lw=0.5)
    ax = axs[1]; panel_label(ax, "(b) 強い重力：光円錐が内側へ傾く")
    ax.set_xlim(-1,8); ax.set_ylim(-0.5,5.5); ax.axis("off")
    ax.add_patch(Circle((6.6,0.7),0.65,facecolor=DARK,edgecolor=DARK)); ax.text(6.6,-0.15,"強い重力源",ha="center",fontsize=9)
    for x0,tilt in zip([1.1,2.5,3.9,5.1],[0.0,0.18,0.42,0.75]):
        y0=1.0; ax.plot([x0,x0],[y0,y0+3.6],color=LIGHT,lw=0.8)
        ax.plot([x0,x0+1.15+tilt],[y0,y0+2.4],color=PHYS,lw=1.8)
        ax.plot([x0,x0-1.15+tilt],[y0,y0+2.4],color=PHYS,lw=1.8)
    xs=np.linspace(0.8,6.0,300); ys=3.7-0.08*(xs-0.8)**2
    ax.plot(xs,ys,color=ACCENT,lw=2.2); arrow(ax,(5.4,3.0),(6.05,2.6),color=ACCENT,lw=1.3,ms=10)
    ax.text(3.5,4.65,"光は局所的には光円錐に沿うが、\n時空そのものが曲がっている",ha="center",fontsize=9)
    ax.text(5.0,1.1,"重力源へ近づくほど\n未来方向が内側へ傾く",ha="center",fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig13_light_cone_curvature.eps")

def fig14_manifold_unfolding():
    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.2))
    fig.suptitle("多様体仮説と『アイロンがけ』：曲がったデータ空間をほどく", fontsize=14, fontweight="bold", color=DARK)
    ax=axs[0]; panel_label(ax,"(a) 高次元空間に埋め込まれた低次元多様体"); ax.set_xlim(-0.5,10.5); ax.set_ylim(-1,6.5); ax.axis("off")
    t=np.linspace(0,1,300); x=1+8*t; y=2.8+1.8*np.sin(2*np.pi*t)
    ax.plot(x,y,color="#DCE7F0",lw=8); ax.plot(x,y,color=PHYS,lw=2)
    A=(x[30],y[30]); B=(x[265],y[265]); ax.plot(*A,"o",color=ACCENT,ms=7); ax.text(A[0]-0.25,A[1]+0.35,"A",fontsize=10)
    ax.plot(*B,"o",color=AI,ms=7); ax.text(B[0]+0.12,B[1]+0.25,"B",fontsize=10)
    ax.plot([A[0],B[0]],[A[1],B[1]],color=AI,lw=1.4,ls="--"); ax.plot(x[30:266],y[30:266],color=ACCENT,lw=2.8)
    ax.text(5.0,0.2,"直線距離はシートの外へ飛び出す",ha="center",fontsize=9,color=AI)
    ax.text(5.0,5.55,"意味のあるデータは\n薄い曲がったシート上に集まる",ha="center",fontsize=9)
    ax=axs[1]; panel_label(ax,"(b) 深層表現：多様体を平らにして距離を測る"); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis("off")
    for i,y0 in enumerate([4.8,3.7,2.6]):
        xs=np.linspace(0.8,5.0,150); yy=y0+(0.55-0.18*i)*np.sin(1.5*xs+0.5*i); ax.plot(xs,yy,color=LIGHT if i<2 else PHYS,lw=2)
    for i in range(3): arrow(ax,(5.4,4.4-i*0.9),(6.6,4.4-i*0.9),color=MID,lw=1.1,ms=9)
    ax.plot([7.0,9.2],[3.0,3.0],color="#DCE7F0",lw=6); ax.plot([7.0,9.2],[3.0,3.0],color=PHYS,lw=2)
    ax.plot(7.25,3.0,"o",color=ACCENT,ms=7); ax.plot(8.95,3.0,"o",color=AI,ms=7); arrow(ax,(7.3,3.0),(8.9,3.0),color=ACCENT,lw=1.6,ms=11)
    ax.text(3.0,5.55,"層ごとに少しずつ変形",ha="center",fontsize=9); ax.text(8.1,4.1,"潜在空間では\n意味の距離が単純になる",ha="center",fontsize=9)
    ax.text(8.1,1.6,"A → B の補間が\nシート上の道に対応",ha="center",fontsize=8.8,color=MID)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig14_manifold_unfolding.eps")

def fig15_blackbody_radiation():
    fig, ax = plt.subplots(figsize=(7.8,5.0)); fig.suptitle("黒体放射：古典論の紫外破綻とプランク分布",fontsize=14,fontweight="bold",color=DARK)
    panel_label(ax,"(a) 無次元振動数  x = hν/kBT で比較")
    x=np.linspace(0.05,8.0,500); planck=x**3/(np.exp(x)-1); wien=x**3*np.exp(-x); rj=x**2
    ax.plot(x,planck,color=DARK,lw=2.4,label="プランク分布"); ax.plot(x,wien,color=PHYS,lw=1.8,ls="--",label="ヴィーン近似"); ax.plot(x,rj,color=AI,lw=1.8,ls=":",label="レイリー・ジーンズ")
    ax.set_ylim(0,5.0); ax.set_xlabel("無次元振動数  x = hν/kBT"); ax.set_ylabel("規格化したスペクトル強度"); ax.grid(color=LIGHT,lw=0.6); ax.legend(frameon=False,fontsize=9)
    ax.annotate("低振動数では\n古典論と一致",xy=(0.7,0.6),xytext=(1.4,3.8),arrowprops=dict(arrowstyle="->",color=PHYS),fontsize=9,color=PHYS)
    ax.annotate("古典論は高振動数で発散\n（紫外破綻）",xy=(2.15,4.6),xytext=(4.4,4.25),arrowprops=dict(arrowstyle="->",color=AI),fontsize=9,color=AI)
    ax.annotate("量子化により\n高振動数が抑制",xy=(4.5,1.05),xytext=(5.4,2.1),arrowprops=dict(arrowstyle="->",color=ACCENT),fontsize=9,color=ACCENT)
    fig.tight_layout(rect=[0,0.02,1,0.92]); save_eps(fig,"fig15_blackbody_radiation.eps")

def fig16_bohr_spectrum():
    fig, axs=plt.subplots(1,2,figsize=(10.8,4.7),gridspec_kw={"width_ratios":[1.05,1]}); fig.suptitle("水素スペクトルとボーア模型：飛び飛びの線は準位差から生まれる",fontsize=14,fontweight="bold",color=DARK)
    ax=axs[0]; panel_label(ax,"(a) 水素のエネルギー準位"); nvals=np.arange(1,7); E=-13.6/nvals**2
    ax.set_xlim(0,4.5); ax.set_ylim(-14.3,0.8); ax.set_xticks([]); ax.set_ylabel("エネルギー  E_n  [eV]"); ax.grid(axis="y",color=LIGHT,lw=0.5)
    for n,e in zip(nvals,E): ax.hlines(e,0.7,3.8,color=PHYS,lw=1.5); ax.text(0.45,e,f"n={n}",ha="right",va="center",fontsize=8.5,color=MID)
    for n,x0 in zip([3,4,5,6],[1.2,1.9,2.6,3.3]): arrow(ax,(x0,-13.6/n**2),(x0,-13.6/4+0.18),color=ACCENT,lw=1.3,ms=10)
    ax.text(2.25,-2.3,"上の準位 → n=2 への遷移",ha="center",fontsize=9,color=ACCENT); ax.text(2.25,-12.8,r"$E_n \propto -1/n^2$",ha="center",fontsize=10)
    ax=axs[1]; panel_label(ax,"(b) バルマー系列の可視スペクトル"); R=1.0973731568508e7; ns=np.array([3,4,5,6]); wl=1e9/(R*(1/2**2-1/ns**2))
    for i,(n,lam) in enumerate(zip(ns,wl)):
        ax.vlines(lam,0,1.0-0.13*i,color=AI if n==3 else PHYS,lw=3); ax.text(lam,1.05-0.13*i,f"{lam:.0f} nm",rotation=90,va="bottom",ha="center",fontsize=8.2)
    ax.set_xlim(400,700); ax.set_ylim(0,1.45); ax.set_xlabel("波長  λ [nm]"); ax.set_yticks([]); ax.grid(axis="x",color=LIGHT,lw=0.6)
    ax.text(550,0.32,"整数 n が\n飛び飛びの線位置を決める",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig16_bohr_spectrum.eps")

def fig17_symbolic_regression():
    fig, axs=plt.subplots(1,2,figsize=(10.8,4.4)); fig.suptitle("シンボリック回帰：データから『読める数式』を探す",fontsize=14,fontweight="bold",color=DARK)
    ax=axs[0]; panel_label(ax,"(a) データ → 候補数式"); rng=np.random.default_rng(4); x=np.linspace(-2.2,2.2,28); y0=x**2+0.5*x+1; y=y0+rng.normal(0,0.22,len(x))
    ax.scatter(x,y,s=24,color=MID,label="観測データ（模式）"); xx=np.linspace(-2.3,2.3,250); ax.plot(xx,xx**2+0.5*xx+1,color=PHYS,lw=2,label=r"$x^2+0.5x+1$"); ax.plot(xx,1.2*xx+2,color=LIGHT,lw=1.4,ls="--",label="単純すぎる候補")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(color=LIGHT,lw=0.6); ax.legend(frameon=False,fontsize=8); ax.text(0,6.3,"記号を組み合わせ、\nデータへの適合を評価",ha="center",fontsize=9)
    ax=axs[1]; panel_label(ax,"(b) 精度と数式の単純さのトレードオフ"); comp=np.arange(2,11); err=np.array([1.05,0.66,0.39,0.22,0.16,0.12,0.105,0.098,0.095])
    ax.scatter(comp,err,s=45,color=MID); ax.plot(comp[:6],err[:6],color=ACCENT,lw=2); ax.plot(5,0.22,"o",ms=8,color=AI); ax.text(5.15,0.28,"精度と単純さの\nバランスが良い候補",fontsize=8.8,color=AI)
    ax.annotate("複雑化しても\n改善が小さい",xy=(9,0.098),xytext=(7.2,0.55),arrowprops=dict(arrowstyle="->",color=MID),fontsize=8.8,color=MID)
    ax.set_xlabel("数式の複雑さ（記号数）"); ax.set_ylabel("データ誤差"); ax.grid(color=LIGHT,lw=0.6)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig17_symbolic_regression.eps")

def fig18_stress_strain():
    fig, ax=plt.subplots(figsize=(7.8,4.9)); fig.suptitle("応力–ひずみ曲線：弾性変形から塑性・破断へ",fontsize=14,fontweight="bold",color=DARK); panel_label(ax,"(a) 連続体が壊れるまで")
    strain=np.array([0,0.01,0.02,0.035,0.055,0.08,0.11,0.14,0.17,0.20]); stress=np.array([0,0.7,1.4,2.45,2.8,3.05,3.18,3.12,2.85,2.35])
    ax.plot(strain,stress,color=PHYS,lw=2.4); ax.axvline(0.035,color=LIGHT,lw=1); ax.axvline(0.17,color=LIGHT,lw=1); ax.fill_between([0,0.035],[0,0],[3.5,3.5],color="#E7EEF4"); ax.fill_between([0.035,0.17],[0,0],[3.5,3.5],color="#F5EBDD"); ax.plot(0.20,2.35,"o",color=AI,ms=7)
    ax.text(0.017,3.28,"弾性域\n力を抜くと戻る",ha="center",fontsize=9,color=PHYS); ax.text(0.095,3.28,"塑性域\n永久変形が残る",ha="center",fontsize=9,color=ACCENT); ax.text(0.188,2.55,"破断",ha="center",fontsize=9,color=AI)
    ax.set_xlim(0,0.215); ax.set_ylim(0,3.55); ax.set_xlabel("ひずみ  ε"); ax.set_ylabel("応力  σ"); ax.grid(color=LIGHT,lw=0.6); fig.tight_layout(rect=[0,0.02,1,0.92]); save_eps(fig,"fig18_stress_strain.eps")

def _lorenz(sigma=10.0,rho=28.0,beta=8/3,dt=0.005,steps=5000,x0=(1,1,1)):
    xyz=np.zeros((steps,3)); xyz[0]=x0
    for i in range(steps-1):
        x,y,z=xyz[i]; xyz[i+1]=xyz[i]+dt*np.array([sigma*(y-x),x*(rho-z)-y,x*y-beta*z])
    return xyz

def fig19_chaos_lyapunov():
    fig, axs=plt.subplots(1,2,figsize=(10.8,4.5)); fig.suptitle("カオス：ほぼ同じ初期値が指数関数的に離れていく",fontsize=14,fontweight="bold",color=DARK)
    a=_lorenz(x0=(1,1,1)); b=_lorenz(x0=(1.0001,1,1))
    ax=axs[0]; panel_label(ax,"(a) ローレンツ・アトラクタ"); ax.plot(a[600:,0],a[600:,2],color=PHYS,lw=0.75); ax.set_xlabel("x"); ax.set_ylabel("z"); ax.grid(color=LIGHT,lw=0.4); ax.text(0,48,"決定論的な方程式でも\n軌道は非周期的になる",ha="center",fontsize=9)
    ax=axs[1]; panel_label(ax,"(b) 初期値誤差の増幅"); d=np.maximum(np.linalg.norm(a-b,axis=1),1e-10); t=np.arange(len(d))*0.005; ax.semilogy(t,d,color=AI,lw=1.8); ax.set_xlim(0,18); ax.set_ylim(1e-5,1e2); ax.set_xlabel("時間  t"); ax.set_ylabel(r"$|\delta x(t)|$"); ax.grid(color=LIGHT,lw=0.5,which="both"); ax.text(8.5,2e-4,r"$|\delta x(t)| \sim |\delta x_0|e^{\lambda t}$",ha="center",fontsize=10)
    ax.annotate("小さな差が急速に拡大",xy=(13,1.0),xytext=(5.0,15),arrowprops=dict(arrowstyle="->",color=AI),fontsize=9,color=AI)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig19_chaos_lyapunov.eps")

def fig20_pinn_architecture():
    fig, axs=plt.subplots(1,2,figsize=(11.5,4.8),gridspec_kw={"width_ratios":[1.25,1]}); fig.suptitle("PINNs：データ誤差だけでなく『物理法則違反』も罰する",fontsize=14,fontweight="bold",color=DARK)
    ax=axs[0]; panel_label(ax,"(a) PINN の学習ループ"); ax.set_xlim(0,12); ax.set_ylim(0,8); ax.axis("off")
    boxes=[(0.6,5.3,2.1,1.1,"入力\n(x, t)",PHYS),(3.5,5.0,2.6,1.7,"ニューラル\nネットワーク",AI),(7.1,5.3,2.2,1.1,"予測\nu(x,t), p(x,t)",PHYS),(7.0,2.3,2.5,1.2,"自動微分\n∂u/∂t, ∇u, …",ACCENT),(3.2,1.0,3.0,1.3,"PDE残差\n+ 保存則 + 境界条件",ACCENT)]
    for x,y,w,h,txt,col in boxes:
        r=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",facecolor="white",edgecolor=col,lw=1.7); ax.add_patch(r); ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=9)
    arrow(ax,(2.7,5.85),(3.45,5.85)); arrow(ax,(6.1,5.85),(7.05,5.85)); arrow(ax,(8.2,5.25),(8.2,3.55),color=ACCENT); arrow(ax,(7.0,2.9),(6.2,1.7),color=ACCENT)
    ax.add_patch(Rectangle((0.8,1.2),1.6,1.1,facecolor=PALE,edgecolor=PHYS,lw=1.3)); ax.text(1.6,1.75,"観測・境界\nデータ",ha="center",va="center",fontsize=9); arrow(ax,(2.4,1.75),(3.15,1.65),color=PHYS)
    ax.text(4.75,0.35,"総損失 = データ損失 + 物理損失",ha="center",fontsize=9.5); arrow(ax,(4.7,1.0),(4.7,4.95),color=AI,lw=1.2,ms=10); ax.text(5.05,3.65,"誤差逆伝播",fontsize=8.5,color=AI,rotation=90)
    ax=axs[1]; panel_label(ax,"(b) 順問題と逆問題"); ax.set_xlim(0,10); ax.set_ylim(0,8); ax.axis("off")
    ax.text(5,6.7,"順問題",ha="center",fontsize=10,fontweight="bold",color=PHYS)
    for (x,y,txt,col) in [(0.9,5.2,"原因・初期条件",PHYS),(6.7,5.2,"未来の場・流れ",PHYS),(0.9,1.45,"限られた観測",AI),(6.7,1.45,"見えない物理量\n・パラメータ",AI)]:
        r=FancyBboxPatch((x,y),2.4,1.0,boxstyle="round,pad=0.02",facecolor="white",edgecolor=col,lw=1.5); ax.add_patch(r); ax.text(x+1.2,y+0.5,txt,ha="center",va="center",fontsize=9)
    arrow(ax,(3.3,5.7),(6.65,5.7),color=PHYS,lw=1.6,ms=11); ax.text(5,4.55,"既知の方程式",ha="center",fontsize=8.7,color=MID)
    ax.text(5,2.95,"逆問題",ha="center",fontsize=10,fontweight="bold",color=AI); arrow(ax,(3.3,1.95),(6.65,1.95),color=AI,lw=1.6,ms=11); ax.text(5,0.75,"観測と物理法則を同時に満たす原因を探索",ha="center",fontsize=8.7,color=MID)
    fig.tight_layout(rect=[0,0.03,1,0.90]); save_eps(fig,"fig20_pinn_architecture.eps")

def main():
    fig13_light_cone_curvature(); fig14_manifold_unfolding(); fig15_blackbody_radiation(); fig16_bohr_spectrum(); fig17_symbolic_regression(); fig18_stress_strain(); fig19_chaos_lyapunov(); fig20_pinn_architecture(); print(f"Generated 8 EPS figures in {OUT}")

if __name__ == "__main__": main()
