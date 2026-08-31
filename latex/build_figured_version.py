from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generated"
CH = ROOT / "chapters"

# (source file, EPS/PDF stem, anchor text, Japanese caption)
SPECS = [
("preface.tex","fig00_knowledge_map","この本の読み方","本書全体の見取り図。物理学の主要概念が、最適化・確率・場・波・幾何・統計・複雑系を経て現代のAIへ接続していく系譜を示す。"),
("chapter01.tex","fig01_geocentric_heliocentric","天動説","天動説と地動説の比較。複雑な周転円による記述から、より単純な太陽中心の幾何へと世界像が転換した。"),
("chapter01.tex","fig02_gradient_descent","勾配降下法","物理系がポテンシャルの低い状態へ向かう運動と、AIが損失関数を小さくする勾配降下法の対応。"),
("chapter02.tex","fig03_fermat_principle","フェルマーの原理","フェルマーの原理。光は局所的な力ではなく、経路全体の所要時間が停留する軌道を選ぶように記述できる。"),
("chapter03.tex","fig04_entropy_time_arrow","時間の矢","ミクロな可逆性とマクロな不可逆性。多数の自由度を粗視化すると、典型的な状態へ向かう流れが時間の矢として現れる。"),
("chapter03.tex","fig05_diffusion_forward_reverse","拡散モデル","拡散モデルの順方向と逆方向。情報をノイズへ崩す過程と、学習した逆過程によって構造を再生成する過程を対比する。"),
("chapter04.tex","fig06_field_div_rot","発散","ベクトル場の発散と回転の直観。場の局所構造を、湧き出し・吸い込み・渦として可視化する。"),
("chapter04.tex","fig07_em_wave_attention","Self-Attention","電磁場による情報伝播とSelf-Attentionの概念的対比。局所的な伝播と、大域的な関連付けという二つの情報伝達様式を示す。"),
("chapter05.tex","fig08_simple_harmonic_motion","単振動","単振動の三つの見方。復元力、時間波形、ポテンシャル井戸は同じ運動を異なる表現で記述する。"),
("chapter05.tex","fig09_interference_standing_wave","干渉","波の重ね合わせ、干渉、定在波。単純な波の線形結合から空間的な節と腹が生まれる。"),
("chapter05.tex","fig10_fourier_decomposition","フーリエ","複雑な時系列を単純な正弦波の重ね合わせへ分解するフーリエ解析と、その周波数スペクトル。"),
("chapter06.tex","fig11_minkowski_time_dilation","光時計","光時計とミンコフスキー図。光速度不変から時間の進み方が観測者の運動状態に依存することを幾何学的に表す。"),
("chapter06.tex","fig12_embedding_analogy","King - Man + Woman = Queen","単語埋め込み空間の幾何。語の意味関係がベクトル差として表現され、類推が空間内の平行移動として現れる。"),
("chapter07.tex","fig13_light_cone_curvature","光円錐","光円錐と曲がった時空。因果的に到達可能な領域と、重力によって時空の幾何そのものが変形するという一般相対論の見方。"),
("chapter07.tex","fig14_manifold_unfolding","多様体仮説","多様体仮説の模式図。高次元観測空間に埋め込まれた低次元構造を、学習によってほどいて扱いやすい潜在空間へ写す。"),
("chapter08.tex","fig15_blackbody_radiation","黒体放射","黒体放射の無次元スペクトル。古典論の紫外破綻と、プランクの量子仮説による高周波成分の抑制を示す。"),
("chapter08.tex","fig16_bohr_spectrum","ボーア","水素原子の離散的エネルギー準位とバルマー系列。観測される線スペクトルが準位差に対応することを示す。"),
("chapter08.tex","fig17_symbolic_regression","シンボリック回帰","シンボリック回帰。データ適合度だけでなく数式の単純さも評価し、解釈可能な法則候補を探索する。"),
("chapter09.tex","fig18_stress_strain","応力","応力―ひずみ曲線の模式図。弾性変形、塑性変形、破断という連続体の異なる応答領域を示す。"),
("chapter09.tex","fig19_chaos_lyapunov","ローレンツ","カオスの代表例であるローレンツ系。ほぼ同じ初期条件から出発した軌道が急速に離れていく初期値鋭敏性を示す。"),
("chapter09.tex","fig20_pinn_architecture","PINNs","Physics-Informed Neural Networks（PINNs）の学習構造。観測データの誤差と、微分方程式・境界条件への違反を同時に損失として最小化する。"),
("chapter10.tex","fig21_de_broglie_diffraction","ド・ブロイ","ド・ブロイ波長と電子回折。粒子として検出される電子が、伝播過程では波としての干渉性を示す。"),
("chapter10.tex","fig22_wavefunction_born_probability","ボルン","波動関数とボルン則。複素振幅そのものではなく、その絶対値の二乗が測定結果の確率密度を与える。"),
("chapter10.tex","fig23_uncertainty_wavepacket","不確定性原理","波束による位置と運動量の不確定性。位置を鋭く局在させるほど、多数の波数成分が必要となり運動量分布が広がる。"),
("chapter10.tex","fig24_curse_dimensionality_nnqs","次元の呪い","量子多体系における状態空間の指数的増大とニューラル量子状態。巨大な波動関数を構造化された関数で圧縮表現する考え方。"),
("chapter11.tex","fig25_law_large_numbers","大数の法則","大数の法則と相対揺らぎの減少。多数のミクロ要素を平均すると、マクロ量が安定した値として現れる。"),
("chapter11.tex","fig26_quantum_statistics","フェルミ","マクスウェル＝ボルツマン、フェルミ＝ディラック、ボース＝アインシュタイン統計の比較。粒子の識別可能性と量子統計が占有数を変える。"),
("chapter11.tex","fig27_boltzmann_softmax","Softmax","ボルツマン分布とSoftmaxの対応。指数関数によって相対的な重みを確率へ正規化する共通の数学構造を示す。"),
("chapter12.tex","fig28_emergence_hierarchy","創発","創発の階層構造。ミクロな自由度の集団から、上位階層でのみ意味を持つ新しい有効概念が現れる。"),
("chapter12.tex","fig29_semiconductor_bands","半導体","導体・半導体・絶縁体のバンド構造。価電子帯と伝導帯の間のエネルギーギャップが電気伝導特性を決める。"),
("chapter12.tex","fig30_superconductivity_cooper_pair","超伝導","クーパー対と超伝導状態の模式図。電子が集団的な位相秩序を形成することで、通常の散乱とは異なる巨視的量子状態が生じる。"),
("chapter12.tex","fig31_quantum_interference_vqe","VQE","量子干渉とVQEのハイブリッド最適化。量子回路で状態を生成し、古典最適化器が測定結果を用いてパラメータを更新する。"),
("chapter13.tex","fig32_reduction_hierarchy","クォーク","物質の階層。巨視的物質から分子・原子・原子核・核子を経てクォークへ至る還元的な見方を示す。"),
("chapter13.tex","fig33_standard_model_map","標準模型","標準模型の粒子地図。物質を構成するフェルミ粒子、相互作用を媒介するゲージ粒子、ヒッグス粒子を整理した。"),
("chapter13.tex","fig34_feynman_gnn","ファインマン","ファインマン図とグラフニューラルネットワークの構造的類似。粒子・頂点・相互作用をノードとエッジの関係として捉える。"),
("chapter13.tex","fig35_higgs_symmetry_breaking","ヒッグス","自発的対称性の破れを表すヒッグスポテンシャルの模式図。対称な法則から特定の真空状態が選ばれる。"),
("chapter13.tex","fig36_lhc_trigger_funnel","トリガー","LHCにおけるイベント選別の概念図。膨大な衝突事象から、トリガーが解析価値の高い少数の事象を段階的に選び出す。"),
("chapter14.tex","fig37_hubble_law","ハッブル","ハッブル＝ルメートル則の模式図。銀河までの距離と後退速度のほぼ線形な関係が宇宙膨張を示す。"),
("chapter14.tex","fig38_cosmic_timeline","インフレーション","宇宙史の時間軸。インフレーション、初期宇宙、再結合、構造形成を経て現在へ至る大域的な進化を示す。"),
("chapter14.tex","fig39_universe_composition","ダークエネルギー","現代宇宙論における宇宙のエネルギー組成。通常物質、ダークマター、ダークエネルギーの相対的な割合を示す。"),
("chapter14.tex","fig40_gravitational_chirp","重力波","連星合体に伴う重力波チャープ。合体へ近づくにつれて振幅と周波数が増大する特徴的な波形を示す。"),
("chapter14.tex","fig41_holographic_principle","ホログラフィック","ホログラフィック原理の概念図。高次元のバルクにある物理情報が、より低次元の境界上の自由度で記述できる可能性を示す。"),
("chapter15.tex","fig42_math_intuition_proof_loop","直感","数学的発見における直感・予想・証明・検証の循環。AIは候補生成と探索を加速し、人間と機械の役割分担を変える。"),
("chapter15.tex","fig43_formal_proof_pipeline","形式証明","AI支援による形式証明の流れ。自然言語の問題を形式化し、証明候補を生成して、定理証明器が機械的に検証する。"),
("chapter16.tex","fig44_spin_glass_landscape","スピングラス","スピングラスのフラストレーションと複雑なエネルギー地形。ニューラルネットワークの高次元損失地形を考えるための物理的比喩となる。"),
("chapter16.tex","fig45_double_descent","二重降下","二重降下の模式図。モデル容量を増やしたとき、補間閾値付近で一度悪化したテスト誤差が、さらに過剰パラメータ化すると再び低下する。"),
("chapter16.tex","fig46_grokking_learning_curve","グロッキング","グロッキングの学習曲線。訓練データを暗記した後も学習を続けると、ある時点で汎化性能が急激に改善する。"),
("chapter16.tex","fig47_ntk_infinite_width","NTK","ニューラル・タンジェント・カーネル（NTK）の概念図。ネットワーク幅を無限大へ近づける極限で、学習ダイナミクスをカーネル法として記述できる。"),
("chapter16.tex","fig48_rg_deep_learning","繰り込み群","繰り込み群と深層学習の階層的粗視化の類似。細かな自由度からスケールを上げながら本質的な特徴を抽出する。"),
("chapter17.tex","fig49_five_paradigms","パラダイム","科学方法論の五つのパラダイムを俯瞰する模式図。観察・理論・計算・データ集約からAI駆動科学へと研究様式が拡張してきた。"),
("chapter17.tex","fig50_prediction_vs_understanding","予測","予測性能と人間に理解可能な説明の二軸。高精度な予測と因果的・概念的理解が必ずしも同じ方向へ進むとは限らない。"),
("chapter17.tex","fig51_self_referential_universe","自己言及","宇宙から物質・生命・人間・AIが生まれ、そのAIを用いて再び宇宙を理解する自己言及的な知の循環。"),
]


def figure_block(stem: str, caption: str) -> str:
    return f'''\n\n\\begin{{figure}}[tbp]\n  \\centering\n  \\includegraphics[width=0.92\\textwidth,height=0.58\\textheight,keepaspectratio]{{generated/figures/{stem}.pdf}}\n  \\caption{{{caption}}}\n  \\label{{fig:{stem}}}\n\\end{{figure}}\n'''


def insert_after_anchor(text: str, anchor: str, block: str) -> tuple[str, bool]:
    body_start = text.find('\\section{')
    if body_start < 0:
        body_start = 0
    idx = text.find(anchor, body_start)
    if idx < 0:
        marker = text.find('\\input{chapters/references/', body_start)
        if marker < 0:
            marker = len(text)
        return text[:marker] + block + '\n' + text[marker:], False
    para_end = text.find('\n\n', idx)
    if para_end < 0:
        para_end = idx + len(anchor)
    return text[:para_end] + block + text[para_end:], True


def main() -> None:
    if GEN.exists():
        shutil.rmtree(GEN)
    (GEN / 'chapters').mkdir(parents=True)
    (GEN / 'figures').mkdir(parents=True)

    by_file: dict[str, list[tuple[str, str, str]]] = {}
    for filename, stem, anchor, caption in SPECS:
        by_file.setdefault(filename, []).append((stem, anchor, caption))

    report = []
    source_files = ['preface.tex'] + [f'chapter{i:02d}.tex' for i in range(1, 18)]
    for filename in source_files:
        text = (CH / filename).read_text(encoding='utf-8')
        hits = 0
        for stem, anchor, caption in by_file.get(filename, []):
            text, found = insert_after_anchor(text, anchor, figure_block(stem, caption))
            hits += int(found)
            report.append(f'{filename}: {stem}: anchor={anchor!r}: ' + ('OK' if found else 'FALLBACK'))
        (GEN / 'chapters' / filename).write_text(text, encoding='utf-8')

    main_tex = (ROOT / 'main.tex').read_text(encoding='utf-8')
    main_tex = main_tex.replace('\\include{chapters/', '\\include{generated/chapters/')
    main_tex = main_tex.replace('\\usepackage{graphicx}', '\\usepackage{graphicx}\n\\graphicspath{{generated/figures/}}')
    (GEN / 'main_with_figures.tex').write_text(main_tex, encoding='utf-8')
    (GEN / 'insertion-report.txt').write_text('\n'.join(report) + '\n', encoding='utf-8')

    print(f'Prepared figure-layout manuscript with {len(SPECS)} figures.')
    print(f'Anchors matched: {sum("OK" in x for x in report)}/{len(SPECS)}')


if __name__ == '__main__':
    main()
