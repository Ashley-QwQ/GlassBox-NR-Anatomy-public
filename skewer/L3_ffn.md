# L3.ffn：逐通道门函数、扩张与残差接线

<!-- beginner-r04m:start intro -->
<a id="beginner-ffn"></a>
【入门简化】先让每个位置各自重组自己的数字串，经过逐项函数，再组合回原项数；这段不向别处取内容，随后[注意力](APPENDIX_beginner_glossary.md#g039)才做位置间交换。甲的2项→4项→逐项函数→2项，乙也独立走自己的线，见[人工双位置图](L1_00_one_block_primer.md#per-position)。一条[旁路](APPENDIX_beginner_glossary.md#g016)来自块入口，在收缩开始带入；另一条来自[前馈](APPENDIX_beginner_glossary.md#g037)结果，在注意力[后投影](APPENDIX_beginner_glossary.md#g038)开始带入，[完整两线图](L1_00_one_block_primer.md#two-residuals)先于下面的[家族](APPENDIX_beginner_glossary.md#g080)细表阅读。
<!-- beginner-r04m:end intro -->

<a id="contract-class-r04l"></a>
## contract模板与零源（F26.03/F26.04，排名33–34）

令P=输入字节长/4096、bands=ceil(P/128)，要求P>0且P%32=0，[CTA](APPENDIX_beginner_glossary.md#g087)数=8bands，四个[warp](APPENDIX_beginner_glossary.md#g087)全部执行。对CTA c、warp w：`class=0 if w<2 else (2 if 128*(c%bands)+64>=P else 1)`。选择名：class0→live，class1→dead，class2在 `128bands−P≥64` 时→dead_edge，否则→live；名字dead不表示不执行。[ffn_contract.cpp:224–231](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L224)、[几何与选择:301–324](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L301)。

源零谓词为 `8*(c%bands)+4*(w//2)+slot//2 >= 2*ceil(P/32)`；源map该处须为−1，其他负值不[准入](APPENDIX_beginner_glossary.md#g101)。真正edge的class2在z=0，将精确子树 `dq(part(cg(...),part_index))` 替成 `dq(sat(cat(c16(+0),c16(+0))))`；递归保持其他子树不变。只有该class/阶段允许此替换，且edge模板stores必须为空；其他模板[wiring](APPENDIX_beginner_glossary.md#g089)/stores须等于live对应图，不能由map符号猜模板。[零源校验:248–263](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L248)、[子树替换:267–281](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L267)、[应用:315–324](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L315)。此处关闭模板/零值规则；地址图仍独立标TABLE。[发布](APPENDIX_beginner_glossary.md#g091)合同见[各族发布区](L3_workspace_map.md#release-contract-r04l)。

[整串目录](INDEX.md) · 上层：[B0](L2_02_b0.md#adapter)、[TIN](L2_03_tin_encoder.md)、[split16](L2_04_split16_encoder.md#ffwd)、[ViT expand](L2_05_vit.md#expand) / [contract](L2_05_vit.md#contract)、[B70](L2_09_b70.md#b70)

## 本文件记号与对象

[E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054)、[K32](APPENDIX_beginner_glossary.md#g065)、[RN-even](APPENDIX_beginner_glossary.md#g059) 与 [seed](APPENDIX_beginner_glossary.md#g042) 沿用 [统一记号](INDEX.md#形状与工作区记号)。[Q8](APPENDIX_beginner_glossary.md#g061) 是 F16→E4 的 RN-even/[satfinite](APPENDIX_beginner_glossary.md#g062)，D8 是 E4→F16 精确[解码](APPENDIX_beginner_glossary.md#g061)；[H+](APPENDIX_beginner_glossary.md#g063)、H×、HF 分别为 half 加、乘、融合乘加。HF 的软件参考保留 [binary64](APPENDIX_beginner_glossary.md#g056) 融合结果再 RN16 的边界，见 [half 合同](L4_half_arith.md#rounding)。记 K(A,W;s) 为按实际顺序逐 K32 发布 F16、从 half seed s 起步的[矩阵](APPENDIX_beginner_glossary.md#g051)链，不是全 K 只舍入一次的实数乘法。

M×K×N 指左矩阵 M×K、右矩阵 K×N。[TIN](APPENDIX_beginner_glossary.md#g011) 的 M=64 个[窗口](APPENDIX_beginner_glossary.md#g015)位置；[split16](APPENDIX_beginner_glossary.md#g013) 的 S 是本次 X₅ [角色](APPENDIX_beginner_glossary.md#g084)的位置数（1080 为 60×36=2160），执行时的[补齐](APPENDIX_beginner_glossary.md#g085)/掩码另按 maps；[ViT](APPENDIX_beginner_glossary.md#g014) 用物理行数 P（1080 为640）。下文 [CENSUS](APPENDIX_beginner_glossary.md#g100) 描述 CPU 源/具体图，MEASURED/CONTROLLED 指具名保存记录；它们分别约束原生输出，不能证明内部[架构](APPENDIX_beginner_glossary.md#g078)唯一。设计和训练动机仍未知。

<a id="ffn"></a>
## 一个完整 FFN 子块做什么

- 是什么：先在每个位置变换[通道](APPENDIX_beginner_glossary.md#g007)，再施加单输入的[门函数](APPENDIX_beginner_glossary.md#g045)，最后经收缩/输出投影，把同一块入口的[缩放](APPENDIX_beginner_glossary.md#g031)[残差](APPENDIX_beginner_glossary.md#g017)接回主路。
- 输入 → 输出：块入口 E4（B0/B70 另保留未量化 F16 入口）→扩张 F16→门后 E4→收缩路径 F16→前馈出口 E4；未量化 F16 是否另被后续子层读取，按下表分家族处理。
- 怎么算：确定本次位置和通道；取原块入口作残差；执行本家族的预投影/扩张；逐元素执行下面的 G；按变体表完成收缩与 seed 合并；在原节点发布 F16/E4。门函数不混合两个独立隐藏[向量](APPENDIX_beginner_glossary.md#g076)，也不执行空间 attention。
- 数值规则：每个 K32 的 F16 发布、门中两次 HF 与一次 H×、中间 E4 发布、残差 H×、[部分和](APPENDIX_beginner_glossary.md#g050) H+ 均是独立边界，不能合成普通 GEMM+激活+最后一次加法。
- 为什么：扩张提供更多逐位置中间通道，输出路径把它们带回块宽；同块入口是确切的旁路来源。为何采用这些宽度、门形状或拆核方式未知；不据此补训练解释。
- 我们怎么知道：下面的行级源码、具体 DAG 与 [五类数值记录](#evidence)分列；完整 FFN 的原生输出门不等于直接观察到每个内部激活。
- 往下：[G 的算术](#gate)、[通道与变体表](#channels)、[真实 C++ 小例子](#worked-example)、[QMMA](L3_qmma_e4m3.md#qmma-e4m3)与 [E4 发布](L4_e4m3_and_k32.md#e4m3-format)。

<a id="gate"></a>
## G 是单输入的裁剪分段多项式

对输入 half x，精确的逐节点接口为：

```math
\begin{aligned}
c&=\mathrm{clamp}_{16}(x,-4,4),\\
\ell&=HF(|c|,-0.055908203125,\ 0.447265625),\\
f&=HF(c,\ell,\ 0.89453125),\\
t&=H\times(x,f),\\
G(x)&=Q8(t).
\end{aligned}
```

这里三项十进制数是函数代码中固定的**算法常数**，没有读取或披露模型系数。[clamp](APPENDIX_beginner_glossary.md#g049) 只用于因子 f，末端乘的是原来的 x；把 x 也永久裁到 ±4 会改变结果。绝对值清符号，不增加浮点舍入。两次 HF 各在融合结果后 RN16；H× 再 RN16；最后另一次 RN-even/satfinite 到 E4。该门不调用 [MUFU](APPENDIX_beginner_glossary.md#g073)、[exp](APPENDIX_beginner_glossary.md#g047)、tanh、erf、[RSQ](APPENDIX_beginner_glossary.md#g072) 或 RCP。

**它既不是 textbook [GELU](APPENDIX_beginner_glossary.md#g046)/SiLU，也不是成对通道门。** 忽略发布舍入时，其实数表达式是
```math
g_*(x)=x\left[0.89453125+c\left(0.447265625-0.055908203125|c|\right)\right].
```
在裁剪区内是分段三次式，x≤−4 的因子为0，x≥4 的因子为1.7890625。实际 finite half x=4 得 t=7.15625、E4 输出7；GELU(4) 与 SiLU(4) 均小于4，即使再按本页格式发布也不等于7，故不能当作这两者的同域等价实现。每个输出只依赖自己的 x，因子也由同一个 x 构造，没有 SwiGLU 一类的“两份独立投影→逐项相乘”，没有由 G 引起的通道减半。“近似哪类激活”的训练命名仍属【推测】，本文只使用 G。

| 家族的 G 站点 | 当前代码/图及精度差异 |
|---|---|
| B0 | [b00.hpp:24](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L24)：half clamp/abs→两次 h_fma→h_mul→sat_e4 |
| TIN | [tin.cpp:105–112](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L105)：参考式用 binary64 计算两段后各 half_round；生产可用按该函数生成的精确 unary 表，不是原生硬件查表的结论 |
| ViT expand | [ffn_expand-resume2.cpp:149–154](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L149)：两次 std::fma→half_round；入口显式拒绝 [Inf](APPENDIX_beginner_glossary.md#g069)/NaN |
| split16 ffwd | [L25 图](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json) / [L29 图](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json)：每条 G 为 min/max、abs、fma、fma、mul、Q；[执行器:254–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L254)逐节点执行 half 算术 |
| B70 | [outtail.cpp:88](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L88)：同一裁剪/两次 half FMA/half 乘法，qc 发布 E4 |

【本轮 CPU 实算】抽取原 C++ 函数，B0/TIN/ViT 三种写法的**全部63488个有限 F16 编码**得到相同 E4 输出，包括 ±0；这是这些软件函数在该域上的穷举等价，不是新 GPU 测量，也不覆盖任意非有限输入。split16 的具体 G 图与上式结构相同；未把这项软件检查升级为全图/全几何准入。链中 QMMA 的非有限 seed、E4 NaN、half [overflow](APPENDIX_beginner_glossary.md#g071) 拒绝仍按 [原语守卫](L4_e4m3_and_k32.md#publish-guards)执行；G 的 satfinite 不能用于绕过前一矩阵的拒绝。

<a id="wiring"></a>
## 一张完整残差接线图

图中的“收缩路径”按下表包含一层或多层矩阵；seed 的入口点是真实的累加接口，不是最后才附加的一条实数加法。

~~~mermaid
flowchart LR
    X["本块入口：E4；B0/B70 另保留 half"] --> PRE["预投影：split16 有；其他按变体"]
    PRE --> EX["扩张 K32 链 → F16"]
    EX --> G["单输入 G：两次 HF、一次 H× → E4"]
    G --> DOWN["收缩矩阵 / 首分片：接seed；各K32、中间E4与部分和H+按变体"]
    X --> R["原块入口解码或保留 half × 残差尺度 → half seed"]
    R --> DOWN
    DOWN --> Z["按变体合并后的前馈结果 F16"]
    Z --> Q["Q8 → 前馈出口 E4"]
    Z -. "仅具名一头路径保留未量化值" .-> L["供后续子层的独立旁路"]
~~~

<a id="channels"></a>
## 跨家族通道与变体表

所有矩阵[权重](APPENDIX_beginner_glossary.md#g079)为 E4；旁路尺度按 F16 消费，不列其值。split16 的逻辑分组由具名图的数据依赖、K32 链及权重索引覆盖推得（CENSUS / INFERRED），不把该组轴等同于16个 attention 头；[详细绑定和计数](APPENDIX_evidence_history.md#ffn-r04b)在附录。

| 家族 / 调用 | M×K×N 与扩张宽度 | G 是否拆通道 / 暂存 | 残差来源、精度与加入点 | 真正差异与定位 |
|---|---|---|---|---|
| B0 / L2 | 每窗64×32×128，再64×128×32；扩张128 | 不拆；门后128 E4 | 适配输出 a 的未量化 F16，H×(a,s_ff) 作收缩首 K32 seed；4个 K32后仍为F16，再发布E4 | 扩张输入是 xc=Q8(a)，不能从 xc 恢复残差；[b00.hpp:42–44](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L42) |
| TIN 一头 [chained](APPENDIX_beginner_glossary.md#g022) / C=32 | 64×32×128→64×128×32 | 不拆；128 E4 | H×(D8(本块入口),s_ff) 作收缩seed；收缩4步 | upsample 一头入口例外取未量化合并值 sx；不扩展[上采样](APPENDIX_beginner_glossary.md#g021)完整主题；[tin.cpp:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130) |
| TIN 多头 chained / C=64/128/256 | H=C/32；每组64×C×128，门后每组64×128×32，再64×32×C；全门宽4C | 不拆；每组128 E4，再收缩为32并Q8 | 初始化z=H×(D8(入口),s_ff)，按h原序把各32→C矩阵的half结果累加进z；每组末投影就是一个K32 | 中间32通道必须E4；不是一次普通4C→C。打包的 C×(4C+128) 包含分组branch参数区，额外128不是另一份门向量；[tin.cpp:38、63–68、133–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L63) |
| split16 ffwd / L25与L29,33,…,53；L101,105,…,129 | 预投影S×512×512→Q8；八组S×64×256→G→S×256×64→Q8；拼回S×512；全门宽2048 | 不拆；全门2048 E4为核内量，实际ffwd出口仍是512 E4/位置 | ffwd没有合入入口残差；原块入口独立交下一核 | 首块inpview与chained取数布局不同；图内三段不是把物理N_out直接当扩张宽；[L25/L29图与绑定](APPENDIX_evidence_history.md#ffn-r04b) |
| split16 ffwd_proj / L26与L30,34,…,54；L102,106,…,130 | S×512×512；接上述ffwd的512 E4 | 此核不再执行G | H×(D8(原块入口),s_ff) 作第一K32的F16 seed；随后16步，末尾Q8 | 旁路是同块入口，不是ffwd出口自身；[L26图](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json) / [L30图](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json) |
| ViT expand / L59,64,69,74,79,84,89,94 | P×1024×4096，每输出32个K32；全门宽4096 | 不拆，逐个G后4096 E4/行 | 本核不加块入口残差 | publish/chained的发布/等待不同；不改变G或宽度；[expand:267–303](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L267) |
| ViT contract / L60,65,70,75,80,85,90,95 | 逻辑P×4096×1024，但实际四个K=1024分片，各32步K32，再固定half合并 | 无G；2048 B/位置=1024个F16部分和，不是2048隐藏通道或门的一半 | H×(D8(块入口),s_ff)作分片0的seed；分片1/2/3从[+0](APPENDIX_beginner_glossary.md#g070)起；按下式H+，末尾Q8 | buffer/output/release各为独立角色；[contract:302–312、436–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L302) |
| B70 的一头FFN / L155 | 活动窗口位置×32×128→×128×32 | 不拆；128 E4 | 两路[特征](APPENDIX_beginner_glossary.md#g008)合并的未量化half merge，H×(merge,s_ff)作收缩seed | 扩张读Q8(merge)，旁路保留merge；只覆盖FFN，不展开末端头/[时域](APPENDIX_beginner_glossary.md#g024)；[outtail.cpp:85–88](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L88) |

<a id="residual"></a>
### 为何“收缩完再加残差”不够精确

B0 / TIN一头 / split16后投影 / B70 的残差先 H× 到half，再作为**矩阵第一步**的seed；每后续K32携带前步F16，不得移到整个点积后一次性相加。TIN多头的每组32→C还携带上组的half结果，组序不可任意交换。

ViT contract 的实际软件接口可写成：
```math
\begin{aligned}
r&=H\times(D8(X),s_{\rm ff}),\\
p_0&=K(H_0,W_0;r),\qquad
p_i=K(H_i,W_i;+0)\quad(i=1,2,3),\\
b_0&=p_0,\quad b_1=H+(b_0,p_1),\quad b_2=H+(b_1,p_2),\\
Y&=Q8\!\left(H+(b_2,p_3)\right).
\end{aligned}
```
H_i/W_i 表示[冻结](APPENDIX_beginner_glossary.md#g103)图分配给该分片的1024项，不额外假定内存为连续四段。分片0写half buffer，1/2依序在buffer上half累加，3与buffer相加后E4输出；[具体模板](F:/dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json)与 [执行器](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L477)共同确定该顺序。换序敏感性不等于已经证明原生并发到达顺序唯一。

这里结束于FFN出口。TIN一头后续旁路可保留未量化z，多头会使用D8(Q8(z))；完整接线见 [TIN块](L3_tin_window.md#tin-window)与 [split16融合块](L3_split16_window.md#window-attention)，各自保留attention、投影和残差接口。

<a id="worked-example"></a>
## 真实 C++ 函数的小例子：字节入、字节出

[脚本](examples/ffn_r04b.py)从当前源码逐字抽取 B0 gate、TIN gate_reference、ViT gate 及half/E4函数，编译并实际执行；K32调用原 qmma_sm120.hpp。没有导入网络、读取权重/保存网络输入/目标或使用GPU。[原输出与源身份](examples/ffn_r04b.result.json)及 [编译记录](APPENDIX_evidence_history.md#ffn-r04b)可查。

把人工half扩张结果x送G，取人工旁路E4=0x28（0.25）与half尺度0x4000（2），真实H×得到seed=0x3800（0.5）。再用一个只有第一项为1、其余为0的**人工K32收缩**，把G(x)与seed合并，最后Q8。这是小原语路径，不冒充真实128/4096通道FFN或任何模型系数。F16以四位十六进制显示编码；[小端](APPENDIX_beginner_glossary.md#g097)输入字节依次为低字节、高字节，例如0xbc00为00 bc。

| x 的F16编码（值） | G(x) E4字节 | seed F16 | 收缩结果F16 | 最终E4字节 |
|---|---|---|---|---|
| c400（−4） | 80（−0） | 3800 | 3800 | 30 |
| bc00（−1） | b0（−0.5） | 3800 | 0000 | 00 |
| 8000（−0） | 80 | 3800 | 3800 | 30 |
| 0000（+0） | 00 | 3800 | 3800 | 30 |
| 3800（0.5） | 31（0.5625） | 3800 | 3c40 | 38 |
| 3c00（1） | 3a（1.25） | 3800 | 3f00 | 3e |
| 4000（2） | 45（3.25） | 3800 | 4380 | 47 |
| 4400（4） | 4e（7） | 3800 | 4780 | 4f |
| 4500（5） | 51（9） | 3800 | 48c0 | 52 |

x=5 的输出不同于x=4，直接检验“只裁因子、不裁末端x”。同一程序另以人工half分片[2048,1,−2048,1]调用真实H+：原序得到0x3c00（1），交换中间分片得到0x4000（2）；它展示逐次half舍入的顺序敏感，不是新原生[负控](APPENDIX_beginner_glossary.md#g102)。ViT gate 对人工+Inf/−Inf/NaN均实际拒绝。完整程序还覆盖x=−5，并比较三种G写法在全部有限half输入上的输出。

<a id="evidence"></a>
## 我们怎么知道：逐调用记录与边界

| 本断言 | 直接读源 / 观察 | 比较对象与范围 | 不能证明什么 |
|---|---|---|---|
| 扩张、门和收缩节点 | 上文各家族行级源码、绑定图 | 当前CPU函数/具体图；原生输出门分列[附录](APPENDIX_evidence_history.md#ffn-gate-history) | 不把内部CPU值当原生激活观测 |
| ViT两阶段前馈 | 保存的逐调用原生/Python/C++比较 | 具名输入、output/padding/release角色各按原报告 | 旧[NOT_RUN](APPENDIX_beginner_glossary.md#g104)与MAP_CHECK_FAILED不被后来门覆盖 |
| TIN、split16、B0/B70前馈 | 保存的整launch或具名块内链比较 | 完整出口中含FFN；不是每个G单独硬件测量 | 不证明全几何、全输入或全部内部矩阵分解唯一 |

[原生行为](APPENDIX_beginner_glossary.md#g001)、CPU矩阵分解与软件G有限域等价分别保留各自证据强度；完整maps语义、任意几何/输入、非有限组合与内部值唯一仍未建立。完整图身份、K32链/权重索引计数及实算源SHA只放 [FFN证据附录](APPENDIX_evidence_history.md#ffn-r04b)；不运行或改动旧实验。
