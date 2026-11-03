# L3.attention-softmax：分数、分母归约与值汇合

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-attention"></a>
【入门简化】当前位置用Q与候选位置的K比较，再按[份额](APPENDIX_beginner_glossary.md#g048)取它们的V内容；Q/K/V都由内部数生成。先用[三位置故事与并排分数表](L1_00_one_block_primer.md#qkv-story)理解谁比较、谁被取回。普通[softmax](APPENDIX_beginner_glossary.md#g047)先取[指数](APPENDIX_beginner_glossary.md#g047)再除总量；本链先按规定改[编码](APPENDIX_beginner_glossary.md#g057)生成正[权重](APPENDIX_beginner_glossary.md#g048)，训练意图未定。[窗口](APPENDIX_beginner_glossary.md#g015)“除总量→转粗格式→组合V”，全局“转粗格式→组合V→除总量”，[两条四格线](L1_00_one_block_primer.md#quantisation-position)把转换标出；这不是可随意交换的实数平均。
<!-- beginner-r04m:end intro -->

[整串目录](INDEX.md) · 上层：[ViT 全局 attention](L2_05_vit.md#attention)、[split16 qkv / proj](L2_04_split16_encoder.md#qkv)、[TIN 编码](L2_03_tin_encoder.md)、[TIN 解码](L2_08_tin_decoder.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| φ、w、p | 分数正核、未[归一化](APPENDIX_beginner_glossary.md#g048)[half](APPENDIX_beginner_glossary.md#g054)权重、归一化half权重 |
| Den、r、accAV | half分母、half倒数、值汇合half[累加器](APPENDIX_beginner_glossary.md#g064) |
| b,l,u | 每轮列分块、分块内键对、对内位置 |
| N,n | 64键轮数、最后一轮补足键数 |

<a id="attention-softmax"></a>
### L3.attention-softmax 三类 attention 的共同接口与不同发布位置

- 是什么：以每头 32 [通道](APPENDIX_beginner_glossary.md#g007)的 Q/K 分数生成正权重，再按固定次序汇合 V。
- 输入 → 输出：[ViT](APPENDIX_beginner_glossary.md#g014) 为三份 P×1024 B 的 [E4](APPENDIX_beginner_glossary.md#g055)；[split16](APPENDIX_beginner_glossary.md#g013) 为 16 头、512 通道窗口块的内部[角色](APPENDIX_beginner_glossary.md#g084)；[TIN](APPENDIX_beginner_glossary.md#g011) 为 1/2/4/8 头、32/64/128/256 通道窗口块的内部角色。后两者每窗 64 个位置。
- 怎么算：
  ~~~text
  1. 从各自地址图/窗口布局取 Q、K、V，保留上游缩放和 E4 发布。
  2. Q32(Q_i, K_j, seed) → half 分数；ViT seed=+0，窗口 seed=本头偏置。
  3. 对分数作指定仿射、half clamp、编码变换 → half 权重 w。
  4. 用固定 half 加法树求 Den，经实测 RCP 和 RN16 得到 r。
  5. ViT：Q32(Q8(w), V, 前步accAV) → accAV；Q8(H×(accAV,r)) → 出口。
  6. TIN / split16：Q8(H×(w,r)) → 权重；Q32(权重,V,前步accAV) → accAV → Q8(accAV)。
  7. 按本家族写回、零覆盖及完成标记合同发布。
  ~~~
- 数值规则：三条路径都不能替成一次 [F32](APPENDIX_beginner_glossary.md#g056) [矩阵](APPENDIX_beginner_glossary.md#g051)乘加库 softmax；ViT 的 E4 权重在除分母之前形成，窗口的 E4 权重在除分母之后形成。
- 为什么这么算：编码变换把受限half分数映射为正权重，再[归约](APPENDIX_beginner_glossary.md#g050)分母并与V汇合；训练命名与硬件内部实现不由这些接口确定。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)，[attention_impl.hpp:172–238、243–270](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172)、[tin.cpp:108–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108)、[scalar_map.hpp:261–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L261)；具体图[绑定](APPENDIX_beginner_glossary.md#g103)与原生门见[证据](#evidence)。
- 往下：[布局](#layout)、[ViT 分数与归约](#vit-score)、[窗口路径](#window-attention)、[值汇合与发布](#publish)、[实际计算例](#worked-example)；原语分别追到 [QMMA](L3_qmma_e4m3.md#qmma-e4m3)、[half](L4_half_arith.md#half-arith)、[RCP](L4_mufu.md#representation)。

<a id="layout"></a>
### L3.attention-softmax.layout 逻辑矩阵与物理字节

- 是什么：先把[逻辑](APPENDIX_beginner_glossary.md#g085)的“某头、某位置、某通道”翻译为指定角色的[字节偏移](APPENDIX_beginner_glossary.md#g083)。
- 输入 → 输出：ViT 的 Q/K/V 均为 E4，但三者的块内排列不同；每头逻辑 Q/K/V 是 T×32，[注意力](APPENDIX_beginner_glossary.md#g039)分数是 T×T。分数矩阵按块生成，不要求完整落盘。
- 怎么算：对已核对的 ViT 布局，以下偏移以角色起点为零，全部单位为 B：
  ~~~text
  Q(t,h,d) =
    16384⌊t/16⌋ + 512h + 64(t mod 8) + 16⌊(d mod 16)/4⌋
    + 8⌊d/16⌋ + 4⌊(t mod 16)/8⌋ + (d mod 4)
  K(t,h,d) =
    16384⌊t/16⌋ + 512h + 64(t mod 8) + 16⌊(d mod 16)/4⌋
    + 8⌊(t mod 16)/8⌋ + 4⌊d/16⌋ + (d mod 4)
  V(t,h,d) =
    32768⌊t/32⌋ + 1024h + 512⌊d/16⌋ + 64(d mod 8)
    + 8⌊(d mod 16)/8⌋ + 16⌊(t mod 16)/4⌋
    + 4⌊(t mod 32)/16⌋ + (t mod 4)
  ~~~
- 索引结构：Q/K 以 16 位置×32 通道为头内块；V 以 32 位置×32 通道为头内块。Q 与 K 的两个高位轴互换，V 另按值矩阵的读取方向排列。参数指针顺序是 Q、K、V、output；已测[工作区](APPENDIX_beginner_glossary.md#g082)物理顺序是 Q、V、K、output，不能把指针顺序当成布局。
- 数值规则：地址翻译不改变 E4 编码；负地址来源按图解释成零。P=32⌈T/32⌉，N=⌈T/64⌉；P、64N、有效 T 分别约束角色长度、分块读入和逻辑有效域。
- 为什么这么算：偏移分别按两次矩阵乘的取数方向定义；普通连续T×1024 reshape会混淆[token](APPENDIX_beginner_glossary.md#g041)与通道。
- 我们怎么知道：CENSUS，[attention_impl.hpp:139–156、248–257](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L139) 定义取数与矩阵坐标；[ARCH 0.7:347](../../../ARCHITECTURE_V3_ZH.md#L347) 绑定角色顺序；本轮用[冻结 T640 绑定](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json)核 SHA 后，对三个分块的 Q/K/V 读取逐项验证上述公式，16,384,000 项通过。这是软件地址一致性复核，没有新增原生测量。
- 往下：[全局循环与尾轮](#vit-score)、[零覆盖](#padding)；窗口按下面独立[合同](APPENDIX_beginner_glossary.md#g101)解释。

| ViT 已测几何 | T | P | N | n |
|---|---:|---:|---:|---:|
| 1080 | 640 | 640 | 10 | 0 |
| 1440 | 960 | 960 | 15 | 0 |
| 4K | 2160 | 2176 | 34 | 16 |

窗口侧不能套这三个 ViT 公式。TIN 的 C++ 临时逻辑布局为 qkv[i,类型,头内通道]：索引 i·3C+类型·C+32h+d；归一化后每头 Q/K/V 各为 64×32，8×8 窗内 i=8y+x。输入画布边界外先补零，窗口原点由实例绑定；这不等于给这些键补一个负无穷分数。split16 的 [QKV](APPENDIX_beginner_glossary.md#g040) 和注意力融合在 qkv [家族](APPENDIX_beginner_glossary.md#g080)内，16 头的来源、跨位置选择、移位和写回仍由 map 决定，[proj](APPENDIX_beginner_glossary.md#g038) 家族消费其出口。源码：[tin.cpp:119–127、143–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119)、[scalar_map.hpp:250–261、319–327](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L250)；[L27/L28 图](#graph-bindings)给出具体算术，不把融合 qkv 简化成三份连续矩阵。

<a id="layout-example"></a>
### 一个点的真实取数代入

取t=9,h=0,d=4。Q式为64×1+16×1+4×1=**84 B**，K式为64×1+16×1+8×1=**88 B**；差别来自t的第3位与d的第4位互换。V式为64×4+16×2+1=**289 B**。Q偏移84=0b01010100的非零段是64/16/4，K偏移88=0b01011000是64/16/8；V偏移289=0b100100001是256/32/1。

【真实代码/地图核对】[脚本](examples/substitutions_r04g.py)按实际attention矩阵取数的row/col/K坐标选择操作数字节，读取已钉SHA的Q/K/V来源地图，结果分别为84、88、289，与[闭式](APPENDIX_beginner_glossary.md#g020)代入相同。[结果及源身份](examples/substitutions_r04g.result.json)保留参数。只算地址，不读取网络[激活](APPENDIX_beginner_glossary.md#g045)；这不是对任意地图的新准入。

<a id="vit-score"></a>
### L3.attention-softmax.vit-score 全局分数、half 分母与尾轮修正（L62/67/72/77/82/87/92/97）

- 是什么：32 头共享同一运算家族，每个查询扫描全部 64 键轮次。
- 输入 → 输出：L61/66/71/76/81/86/91/96 的已[发布](APPENDIX_beginner_glossary.md#g091) E4 Q/K/V → half 分数、half 权重与每查询 half 倒数；本 attention 没有权重矩阵操作数，也没有额外的 attention_scalar 算术操作数（见[权重页](L2_weights_layout.md)）；不要在下面步骤 2 的 HF 前后再乘它。
- 怎么算：
  ~~~text
  1. score_ij = Q32(Q_i, K_j, +0)，头维 K=32。
  2. c_ij = min(max(HF(score_ij, 0.08953857421875, 1.708984375),
                    1.439453125), 1.9775390625)。
  3. φ(score_ij) = half(((bits(c_ij) << 4) + 0x4000) mod 65536)。
  4. 各轮按下列 half 树归约，Den_0=+0，Den_(e+1)=H+(Den_e,S_e)。
  5. 若 n>0：补足项 = RN16(RN32(F32(φ(0)) × F32(n)))；
                Den_N = H−(Den_N,补足项)。
  6. Den=max(Den_N,h₀)；r=RN16(RCP32(Den))。
  ~~~
- 数值规则：步骤 2 是 half [FMA](APPENDIX_beginner_glossary.md#g063)，再 half [clamp](APPENDIX_beginner_glossary.md#g049)；步骤 3 是编码上的整数变换。原图对两 half 的打包字作变换；上述单 half 公式只在指定 clamp 区间化简成立。步骤 5 的乘法是 F32，转 half 后才从 half 总和扣除；不能把它挪进每项归约。
- h₀ 的取值：half 0x0410（6.198883056640625e-05）。它是冻结图里的常量节点 c16 6.198883056640625e-05（T640 图 node 6787、H2160 图 node 22590，图与 SHA 见 [绑定](#graph-bindings)），先拼成两个 half，再进 32 个 max(Den,·) 节点，每个 max 的两半各经 tof32 → RCP。它与 RCP 测量表的起点 0x0410 数值相同，但这里按图节点绑定，不由表起点推出。
- [缩放](APPENDIX_beginner_glossary.md#g031)位置：本核没有另乘 1/√32，也没有 log₂(e) 缩放。上游 QKV 的范数/模型尺度已进入 E4 输入；此处可见的固定分数斜率就是步骤 2 的算法常量。[QK](APPENDIX_beginner_glossary.md#g077) 分数和 AV 都经 [QMMA](APPENDIX_beginner_glossary.md#g065)，不能按 HMMA 或一次精确实数点积代算。
- 为什么这么算：补足零键仍得到φ(0)>0，尾轮明确从half分母扣掉其贡献。V 补足为零时不产生相应的值分子。
- 我们怎么知道：CENSUS，[attention_impl.hpp:172–195、206–238、243–270](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172)、[同 SHA 的冻结参考:68–97、119–152](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/external-F/src-base/kern_attention_epochfix.py#L68)，以及[具体图绑定](#graph-bindings)；T2160 图的尾轮 F32 乘数实际为 16。
- 往下：[归约树](#sum-order)、[值汇合](#publish)、[RCP 位型和域](L4_mufu.md#representation)。

【CPU 重建／位域解释】两个clamp区间都在[1,2)内，因此half符号恒为0、存储指数恒为15，编码为0x3c00+m（0≤m<1024）。在本页两个变换中，固定指数项和偏置在模65536后恰好消去，分别留下m<<4与m<<5作为**新的half编码**；原尾数的高位进入新指数域，低位成为新尾数。这样在每个指数档内线性变化、跨档按二幂变尺度，呈现指数形状；它不是对数值c直接乘16或32，更不是精确exp。

例如人工c=1.5，编码0x3e00、m=512；ViT变换得到0x2000，即0.0078125，窗口变换得到0x4000，即2。clamp使这个位域化简和正有限范围成立，换区间不能原样套用。此处解释[位型](APPENDIX_beginner_glossary.md#g057)机制，不借外部算法名称推定训练设计；完整数值用途仍由各自仿射和归约定义。

<a id="sum-order"></a>
这里把每轮 64 键按该轮 QK 的八个连续 8 列分块写作 w[b,l,u]，即键 j=64e+8b+2l+u，0≤b<8、0≤l<4、u∈{0,1}。下面的每个 H+ 都立即发布 half：

~~~text
L(l,u) = H+( H+( H+( H+(w[0,l,u],w[1,l,u]),
                         H+(w[2,l,u],w[3,l,u])),
                    H+(w[4,l,u],w[5,l,u])),
               H+(w[6,l,u],w[7,l,u]))
B(u)   = H+(H+(H+(L(0,u),L(1,u)),L(2,u)),L(3,u))
S_e    = H+(B(0),B(1))
Den_0    = +0
Den_(e+1)= H+(Den_e,S_e)，按 e=0,1,…,N−1 顺序
~~~

这棵树累加 φ 的 **half 原值**，不是 E4 解码后的权重。轮次依赖参与最终分母，地址图里的交换来源也带实际轮次；不能把最后一轮的来源复制到前面。本轮核对冻结 T640 图的全部 64 个倒数输入表达式，运算树与上式逐项相同；T2160 为同树的 34 轮，再扣尾轮补足项。原图的 [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) 状态仍保留，软件展开本身不升级地图准入；实际字节门另列于[证据](#evidence)。

**与教科书 softmax 的差别明确到步骤：**没有“每行减最大分数”，没有 ex2 或 exp 调用，也没有 log₂(e) 乘法。score 上的 max/min 是固定上下界 clamp，倒数前的 max 是分母下界 h₀。φ 通过 half 编码变换产生；它不具有数学 exp 的精确平移不变性。half 分母、实测 [RCP](APPENDIX_beginner_glossary.md#g072)、[RN16](APPENDIX_beginner_glossary.md#g059)、E4 和 AV 发布还会继续引入指定舍入。上述是代码行为；“意在近似 softmax”只是【推测】。

<a id="window-attention"></a>
### L3.attention-softmax.window 64 键窗口：TIN 与 split16 的不同仿射精度

- 是什么：TIN 的 [chained](APPENDIX_beginner_glossary.md#g022) 等窗口块确实含 attention；split16 的 qkv 家族融合生成 Q/K/V 和 attention，proj 是后续输出投影。
- 输入 → 输出：每头 Q/K/V 各 64×32；Q 与 K 分别按自己的 32 通道范数归一化，Q 再乘本头尺度，转 E4；V 从 QKV half 结果转 E4。Q 的模型尺度不在本文列数值。
- 怎么算：
  ~~~text
  1. Q=Q8(H×(归一化后的 Q, RN16(本头 F32 尺度)))；K=Q8(归一化后的 K)。
  2. score_ij=Q32(Q_i,K_j,本头/本位置 half 偏置)。
  3. TIN：c=RN16(RN32(RN32(F32(score)×0.044921875)+1.30078125))。
  4. split16：c=HF(score,0.044921875,1.30078125)。
  5. c=min(max(c,1.03125),1.5693359375)；
     w=half(((bits(c)<<5)+0x8000) mod 65536)。
  6. 各自按指定 half 树求 Den；r=RN16(RCP32(Den))。
  7. p_j=H×(w_j,r)；权重字节=Q8(p_j)；两次 K32 汇合 V。
  ~~~
- 数值规则：TIN 的 F32 乘法、F32 加法分别发布；split16 的图使用 half FMA。不能因算法常量相同而互换。TIN 分母还检查 half 编码在 [0x1c00,0x60e0]；split16 图在归约后先 max(Den,h₀)，再查 RCP。
- 为什么这么算：窗口限制交互范围，Q 的尺度与[位置偏置](APPENDIX_beginner_glossary.md#g052)调节正核的分布；边界补零、移位、偏置索引是接口事实，不能自动替成通用带掩码 softmax。
- 我们怎么知道：CENSUS，[tin.cpp:34–51、108–127、135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108)、[sm120_b1.py:381–421](../../../mlxdlss/sm120_b1.py#L381)；split16 的 half FMA / RCP 语义为 [scalar_map.hpp:261–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L261)，调用顺序取[已钉 SHA 的 L27 图](#graph-bindings)。
- 往下：[两种窗口归约坐标](#window-sum)、[发布](#publish)；范数内部的平方和另见 [L3.norm-nonfinite（头内平方和）](L3_norm_nonfinite.md#norm32)。

<a id="window-sum"></a>
TIN 在逻辑 8×8 窗口坐标下，令每个查询的 w[j] 有 64 项，完整树为：

~~~text
L(b) = H+( H+( H+( H+(w[b],w[b+16]), H+(w[b+4],w[b+20])),
                   H+(w[b+32],w[b+48])),
              H+(w[b+36],w[b+52]))
Den    = H+( H+(H+(H+(L(0),L(2)),L(8)),L(10)),
           H+(H+(H+(L(1),L(3)),L(9)),L(11)))
r    = RN16(RCP32(Den))
~~~

对应 [tin.cpp:124–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L124)。split16 用自己的片内列分块坐标：把同一查询在八个 QK 列分块上的已变换分数叫 w[b,l,u]，按[上面的 L(l,u)、B(u)、S](#sum-order)求出 S，再 Den=max(S,h₀)。这里的列顺序必须先按它的跨位置 map 选择，**不把 b,l,u 直接认成 TIN 的逻辑栅格 j**；后者正是另一个归约坐标。L27 图有两组这样的查询子片，实际来源选择各自绑定，不能固定使用第一个位置的交换源。解释器逐图执行这些选择见 [scalar_map.hpp:257–259、266–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L257)。所以不能只写“sum(w)”而让库自行决定 half/F32 和结合次序。

【CPU 重建／整数表实读】冻结的 L27 先执行各实例的 PS/SI，之后树里的 w[b,l,u] 就是局部 QK key j=8b+2l+u。用人工标签 W[q,j]：L(0,0) 读 j=0、8、16、24、32、40、48、56，L(1,0) 读 j=2、10、18、26、34、42、50、58。不同查询各有自己的绑定（root 7035/lane 0 是 q=0，root 8194/lane 0 是 q=32）。1080 的全部选择域和 4K 的全部 SI/PS 都核对过，0 不一致。j 是 QK 列标签，不能直接当作图像的 8y+x；packed word 另一半的依赖也不能删。[F04 核对](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)

<a id="publish"></a>
### L3.attention-softmax.publish 值汇合、投影边界与写回

- 是什么：把权重和值的 E4 乘积逐 K32 发布 half，最后形成出口 E4。
- 输入 → 输出：ViT 的 [Q8](APPENDIX_beginner_glossary.md#g061)(w) 或窗口的 Q8(p)，以及 E4 V → half accAV → E4 注意力出口；随后通道投影属于 L63 等或 split16 proj / TIN window 后段。
- 怎么算：
  ~~~text
  ViT：accAV_0=+0
       按轮次和每轮两个 K32：accAV_(k+1)=Q32(Q8(w)[本32键],V[本32键],accAV_k)
       共 2N 步；out=Q8(H×(accAV_(2N),r))。
  窗口：accAV_0=+0
       accAV_1=Q32(Q8(p)[本图前32键],V[本图前32键],accAV_0)
       accAV_2=Q32(Q8(p)[本图后32键],V[本图后32键],accAV_1)
       av=Q8(accAV_2)，再交自己的通道投影和残差。
  写回：按独占计算写回表 → 本实例显式零覆盖（若有）→ 完成标记。
  ~~~
- 数值规则：每一步 Q32 的种子是前一步 half，不允许把所有键一次高精度求和再转 half。ViT r 对同一查询的全部输出通道广播；r 没有提前并入 Q8(w)。TIN 的两段是逻辑键 0–31 后 32–63；split16 使用其图中绑定的键排列。ViT 当前包装拒绝[非有限](APPENDIX_beginner_glossary.md#g069) half 运算结果、非有限发布和 RCP 域外；窗口按各自原语与分母域守卫处理，不套用 ViT 的全部拒绝条件。溢出和[次正规](APPENDIX_beginner_glossary.md#g068)合同沿用 [L3.qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3)、[L4.half-arith](L4_half_arith.md#half-arith)，不因分母为正而消失。
- 原子/归约边界：这些 attention 的分母树是固定 half 加法，AV 是固定种子链；没有 half [原子加](APPENDIX_beginner_glossary.md#g095)来任意合并 attention 数值。split16 计算出口逐字节验证唯一写入者；ViT 的计算出口也逐字节 [exact-once](APPENDIX_beginner_glossary.md#g094)，随后的零覆盖是单列的合法重写。C++ 的任务计数器原子不是网络数值原子。后续 ViT projection 的同址 half 部分和属于 [有序half合并](L4_half_arith.md#half-arith)，不能反过来给 attention 换序。
- 为什么这么算：把数值累加限制在固定低精度接口内；独立输出任务的调度可变化，单条依赖链的舍入顺序不变。
- 我们怎么知道：CENSUS，[attention_impl.hpp:243–270、292–334](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L243)、[tin.cpp:127、135、157–161](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L127)、[scalar_map.hpp:303–329](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L303)；MEASURED 的范围见下表。
- 往下：[4K L62 写零](#padding)、[E4 / K32](L4_e4m3_and_k32.md)、[half 发布](L4_half_arith.md)、[RCP 表](L4_mufu.md#representation)。

<a id="padding"></a>
### L3.attention-softmax.padding 4K L62 的 16×1024 B 是发布合同

- 是什么：计算[向量](APPENDIX_beginner_glossary.md#g076)全部写完后，把 16 个物理补齐 token 的出口显式覆盖为零，再发布完成状态。
- 输入 → 输出：T=2160、P=2176 的完整计算出口 → 局部字节 [2211840,2228224) 的 16,384 B 置零；其他实例必须查自己的绑定。
- 怎么算：
  ~~~text
  1. 先完成整份 output 的计算写回。
  2. 核对 params、角色、边界及阶段身份。
  3. 执行 4096 个独立 4 B 零覆盖，覆盖这 16 KiB 恰好一次。
  4. 完成零覆盖后才发布 release63。
  5. L63 按自己的读表消费已发布出口，包含这段补齐区。
  ~~~
- 数值规则：这是计算之后的覆盖，不是给分数加 [mask](APPENDIX_beginner_glossary.md#g006)，也不是只把新分配的 CPU 缓冲预清零；普通计算会再次写这段位置。尾轮分母扣除补足键与出口零覆盖是两件事。
- 为什么这么算：L63 的已重建精确读集读取全部 16 KiB，每字节被读取 16 次；保留计算出的非零补齐值会进入后续投影。不能把它视为死空间。
- 我们怎么知道：MEASURED / CONTROLLED，[diag-L062/RESULT_ZH.md:5–15](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/diag-L062/RESULT_ZH.md#L5)；CENSUS，[vit_adapter_geometry_padded_zstore.py:166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166) 明确计算输出→零覆盖→完成标记；关闭[负控](APPENDIX_beginner_glossary.md#g102)见 [c12/RESULT_ZH.md:7](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7)。
- 往下：本片只解释 attention 发布所需部分；完整读写[生命周期](APPENDIX_beginner_glossary.md#g092)仍留在 [L3.workspace-map](L3_workspace_map.md#write-sets)。

早期事件数与当前零覆盖项的对应见[padding历史](APPENDIX_evidence_history.md#padding-bug)。

<a id="graph-bindings"></a>
## 行为解释与冻结图的绑定

【CPU 重建／CENSUS】通用执行器定义原语，具体 [DAG](APPENDIX_beginner_glossary.md#g089) 定义顺序；ViT 的 half 仿射、编码变换、分母轮次/尾扣及 AV 后缩放，split16 的仿射/归约/RCP/权重发布与后投影，分别由具名图核对。[图与绑定文件、完整 SHA](APPENDIX_evidence_history.md#attention-bindings)已迁移；不声称新的全几何符号准入或完整 [ROLE](APPENDIX_beginner_glossary.md#g105) 生命周期证明。

<a id="evidence"></a>
## 保存验证的范围

【验证记录】各门按比较对象分列，旧失败及未测不被后来链结果覆盖：

| 本断言 | 直接观察 / 读源 | 比较对象与范围 | 不能证明什么 |
|---|---|---|---|
| attention执行图对应具名输出 | 原生/Python/C++逐调用比较与已绑定算术图 | ViT、split16、TIN各按登记调用和几何；[明细](APPENDIX_evidence_history.md#attention-evidence) | 不补测旧NOT_RUN，不关闭一般地图证明 |
| L62零覆盖不可省略 | 关闭负控得到workspace差异，但六[纹理](APPENDIX_beginner_glossary.md#g027)相同 | 已登记4K L62及其后继读集 | 六POST不能替代FULL，快照零值不能证明发生零写 |
| 后来链结果与旧门并存 | 固定构建、自有检查点和原生输出对照 | [旧1 B差异、地图状态及构建边界](APPENDIX_evidence_history.md#attention-scope-detail) | 不把保存链一致升级为内部时序唯一或全输入定理 |

没有可按原登记引用的“[libm](APPENDIX_beginner_glossary.md#g074) softmax替代”专名负控；下方人工例说明实际算法，不冒充这种硬件负控。

<a id="worked-example"></a>
### L3.attention-softmax.example 实际运行的一行 64 分数

- 是什么：只演算 TIN 的分数→分母→half 归一化→E4；输入全部人工构造，不读模型权重或网络目标。
- 输入 → 输出：[-8,-4,-2,-1,0,1,2,8] 重复八次，构成一个 64 键的合成 half 分数行。
- 怎么算：从仓库根目录执行附录 Python；只使用标准库和 NumPy 读取已采 RCP 小表，不导入模型。
- 数值规则：按上面的 TIN 顺序；本组输入的仿射中间值可精确表示，也验证其分数变换与 split16 路径相同；这不证明两种仿射对任意 half 输入相同。
- 为什么这么算：同时展示 clamp、正权重、half 分母、实测 RCP 与 E4 [下溢](APPENDIX_beginner_glossary.md#g071)；教科书比较仅用于说明差异。
- 我们怎么知道：原写作轮实际执行附录代码；资产 SHA 固定，下面的数字为执行输出，不是 [GPU](APPENDIX_beginner_glossary.md#g078) 或整条 attention 的新验收。
- 往下：到底了；QMMA 本身的可运行例在 [L4.e4m3 / K32](L4_e4m3_and_k32.md)。

[完整脚本与认证 SHA](APPENDIX_evidence_history.md#attention-example)移至附录；下方保留原执行输出，原运行范围见证据附录。

得到 Den=80.375，编码 0x5506；RCP 的 F32 编码为 0x3c4bd830，转 half 得 r=0.01244354248046875，编码 0x225f。每种合成分数出现八次：

| 合成 score | w | p=H×(w,r) | Q8(p) 编码 |
|---:|---:|---:|---:|
| −8 | 0.00006103515625 | 0.0000007748603820800781 | 0x00 |
| −4 | 0.000457763671875 | 0.0000057220458984375 | 0x00 |
| −2 | 0.00341796875 | 0.000042557716369628906 | 0x00 |
| −1 | 0.00927734375 | 0.00011545419692993164 | 0x00 |
| 0 | 0.025390625 | 0.0003159046173095703 | 0x00 |
| 1 | 0.06640625 | 0.0008263587951660156 | 0x00 |
| 2 | 0.1875 | 0.0023326873779296875 | 0x01 |
| 8 | 9.75 | 0.121337890625 | 0x20 |

在普通实数意义下把 64 个已发布 p 相加，得到 0.9998188018798828，不是精确的 1；实际代码也没有再做一次强制归一化。相同 score 的标准 softmax 中，score=8 的每项为约 0.12451424958522991，与此路径的 half 结果相差约 0.00317636。这个差异来自明确的算法和舍入，不用于归因任意原生失配。

<a id="parallel-av-example"></a>
## 同一组人工分数和值：ViT 与窗口并排算到 AV

【CPU 重建／实际执行】[脚本](examples/attention_av_r04f.py)采用相同64项分数行，值向量为[1,−1,2,−2,4,−4,8,−8]重复八次，仅展示一个输出通道；它直接执行源码half/E4函数与真实QMMA K32函数，RCP读取已认证函数表。这里从人工score开始，不运行QK、模型或整个attention调用；64键ViT只是一轮原语演示，不作为已准入的网络几何。

| 路径 | 分母D / 倒数r的F16编码 | 真正送AV的前八个E4权重 | 两次K32后F16 | 出口E4 |
|---|---|---|---|---|
| ViT：E4(w)×V后乘r | 4d32 / 2a29 | 02 02 06 0f 1b 26 32 3d | d448 | c5（−3.25）；先H×(AV,r)，再Q8 |
| TIN窗口：先H×(w,r)再E4×V | 5506 / 225f | 00 00 00 00 00 00 01 20 | c7e0 | d0（−8）；AV后直接Q8 |

两条路径各用自己的φ和half归约树，因而分母也不同；不能把最终差异全部归给量化位置。该例把每个真实位置标出来，供沿ViT路径阅读者核对“先E4(w)、后乘r”。[原stdout、源/函数表SHA和严格编译参数](examples/attention_av_r04f.result.json)保存完整身份；它不升级任何旧NOT_RUN或地图准入状态。

