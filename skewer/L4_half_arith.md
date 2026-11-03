# L4.half-arith：F16 算术、两阶段 FMA 与有序发布

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。

<a id="beginner-rounding"></a>
先读[有限数点与小篮](L1_00_numbers_primer.md)；下表把“保存在哪里”分开，不把软件中间格式推为硬件内部结构。

| 操作 | 应保留的舍入位置与范围 |
|---|---|
| 普通[half](APPENDIX_beginner_glossary.md#g054)加/乘 | 当前软件先[binary64](APPENDIX_beginner_glossary.md#g056)运算再[RN16](APPENDIX_beginner_glossary.md#g059)；有限half的这两类中间运算可精确表示 |
| 软件half[融合乘加](APPENDIX_beginner_glossary.md#g063) | binary64融合结果→RN16，乘积不先单独存half；软件合同，不改成另一参考 |
| 本目标32项步 | 各项与[seed](APPENDIX_beginner_glossary.md#g042)先朝零放公共格→精确和→RN16；每步再反馈小计 |
| 16项步 | 按其独立公共格/seed规则→half；负零等边界仍未普遍关闭，不能借32项规则代替 |
| 最终颜色 | 保留各F32站点与拒绝/[冲零](APPENDIX_beginner_glossary.md#g068)，指定出口才[RZ16](APPENDIX_beginner_glossary.md#g060)；不是上面任一通用末端RN16 |
<!-- beginner-r04m:end expert -->

<a id="transpose-r04l"></a>
## 8×8 half片转置（F27.18，排名92）

输入是32个[lane](APPENDIX_beginner_glossary.md#g087)各4 B，解释为两个LE16片。对输出lane l=0..31、片b=0..1，`i=2*l+b; src=8*(i%8)+i//8`，输出两字节 `out[l,2*b+j]=in[src//2,2*(src%2)+j]` (j=0,1)。这是64个half的8×8转置，重复两次为恒等，不作舍入/数值转换。[qkv_projection_impl.hpp:185–191](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L185)。既有L61原型含32个该节点；L63原型为0，不给projection虚构此步骤。原型[MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104)保持，写出操作语义不改变原生来源准入。

[整串目录](INDEX.md) · 上层：[ViT](L2_05_vit.md)、[FFN](L3_ffn.md)、[attention](L3_attention_softmax.md) · [B0](L2_02_b0.md#channels)、[解码桥](L2_06_decoder_bridge.md#bridge)、[TIN 上采样](L2_08_tin_decoder.md#up-256) · [E4 与 K32](L4_e4m3_and_k32.md#e4m3-format) · [全链F32 / FTZ边界](L4_fp32_ftz.md#fp32-ftz)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| h,s,E,m | F16[编码](APPENDIX_beginner_glossary.md#g057)、符号、存储[指数](APPENDIX_beginner_glossary.md#g058)、尾数域 |
| v(h)、RN16/RN64 | 精确解码、各目标格式最近偶数[发布](APPENDIX_beginner_glossary.md#g091) |
| g,q,rem,n | [格距](APPENDIX_beginner_glossary.md#g066)、[缩放](APPENDIX_beginner_glossary.md#g031)商、丢弃余数、舍入后整数 |
| T0/T1、A_j | 软件浮点参考/整数替代、同址第j次half发布 |

<a id="half-arith"></a>
### L4.half-arith 一个 half 运算何时真正改变位型

- 是什么：原始编码解码后，按[调用](APPENDIX_beginner_glossary.md#g080)点规定的精度计算，再发布 F16；普通加乘、融合乘加、同址累加和格式转换各有边界。
- 输入 → 输出：F16 编码或明确的 F32/binary64 值 → F16 编码或异常；生成 [Inf](APPENDIX_beginner_glossary.md#g069) 与调用者是否接受 Inf 是两件事。

【CPU 重建】下列binary64步骤是软件复现规则；原生可观察约束来自分列的硬件比较。

- 怎么算：
  ~~~text
  1. 解码输入，保留有限值、零符号及所需的非有限分类。
  2. 普通 half 加/乘在 binary64 中运算，再由 half_round 发布。
  3. half FMA 在 binary64 中融合后舍入一次，再 half_round 舍入一次。
  4. 每次 half 加法、FMA 或转换的发布点都保留；同址贡献逐项反馈。
  5. 调用者另查其接受域；不能因 half_round 能产生 Inf 就放宽外层守卫。
  ~~~
- 数值规则：普通 half 发布为 RN-even，支持次正规；FMA 保留两个舍入阶段。F32 辅助链到显式转换处才进入 half；尾部向零发布与采样器发布另依其合同。
- 语义边界：这些是软件参考的发布接口；所列原生比较尚未唯一确定硬件内部精度和物理流水线。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)、限定 MEASURED 与 T1≡T0 软件 [PROVED](APPENDIX_beginner_glossary.md#g111) 分列如下；合成例只核对列出的软件算术。
- 往下：本主题已到底；[位格式](#format)、[舍入和加乘](#rounding)、[整数 T1](#integer-t1)、[原子加顺序](#atomic-add)、[F32 边界](#f32-boundaries)、[实际样例](#worked-examples)。

<a id="format"></a>
## 一个 F16 编码的解码与特殊值

```math
s=h\mathbin{\gg}15,\quad E=(h\mathbin{\gg}10)\mathbin{\&}31,\quad m=h\mathbin{\&}1023,
\qquad
v(h)=
\begin{cases}
(-1)^s m\,2^{-24},&E=0,\\
(-1)^s(1024+m)\,2^{E-25},&1\le E\le30.
\end{cases}
```

| 编码类别 | 当前实现 |
|---|---|
| E=0、m=0 | ±0；解码与 half_round 保留符号。RN-even 下非零[相消](APPENDIX_beginner_glossary.md#g071)为 [+0](APPENDIX_beginner_glossary.md#g070)，两项负零相加仍为 −0 |
| E=0、m≠0 | 次正规；最小正数 $2^{-24}$，最大正次正规 $1023\cdot2^{-24}$，没有统一清零 |
| E=1、m=0 | 最小正正规数 $2^{-14}$ |
| E=30、m=1023 | 最大有限幅值 65504 |
| E=31、m=0 | ±Inf；half_value 解码、half_round 接受并返回相应 Inf 编码 |
| E=31、m≠0 | NaN；half_value 生成[宿主](APPENDIX_beginner_glossary.md#g096) quiet NaN，未保存原载荷；half_round 抛出 NaN publication 异常 |

依据：[GlassBox-NR/cpp/chain_tin_optm/primitives.inc:25–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L25)。整数参考的零符号、非有限分支可逐行核对 [本项目 T1:43–73、81–95](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L43)；[证明 RESULT:9、11、14、16](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L9) 包含完整解码、零例外与非有限域处理。

这里没有“遇到非有限就全部拒绝”的统一规则：普通 half 加法的 Inf 加有限值可返回 Inf，异号 Inf 相加、Inf 乘零或 NaN 输入导致 NaN publication 拒绝；FMA 的无效组合也拒绝。非有限 T1 分支与 T0 的异常类别/消息属于软件等价证明，不能作为原生 NaN 载荷合同。min/max 还各自拒绝 NaN，比较相等时选择第二个输入编码，因此 ±0 顺序也须保留。[公开 primitives.inc:103–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L103)、[T1:55–73、81–88、105–111](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L55)。

调用者可以更窄：例如当前公开 [attention](APPENDIX_beginner_glossary.md#g039) 的 half 运算结果含 Inf 会拒绝，contract 的普通算术和同址累加也有结果守卫。不能用上述原语语义自动放行它们。[attention_impl.hpp:172–186](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172)、[ffn_contract.cpp:422–429、481–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L422)。其他[封存](APPENDIX_beginner_glossary.md#g103)版本的非有限扩展必须另绑定源码，不能借旧接受域验收升级。

<a id="rounding"></a>
## RN-even、65520 与加乘/FMA 的发布点

对有限非零 x，当前 half_round 的可执行规则是：

~~~text
取符号及幅值；幅值 ≥ 65520，直接发布带符号 Inf。
用 frexp 得到 e，使幅值位于 [2^(e−1),2^e)。
g = 2^max(e−11,−24)；q = 幅值/g；n = floor(q)；rem = q−n。
rem>1/2，或 rem=1/2 且 n 为奇数时，n 加 1。
以 n*g 编码为 half；不足最小正规数时进入次正规/零编码。
~~~

源码用二幂缩放，余数比较包含等号；符号在取幅值前保存。[primitives.inc:35–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L35)。半格不会总向上：1 与 $1+2^{-10}$ 中点取 1，而下一个半格取偶尾数的较大邻居。最小正次正规的一半取 +0，负数对应 −0；最大次正规与最小正规之间也按同一偶数规则进位，见文末运行结果。

**65520 是 RN-even 到 F16 的溢出中点。** 65504 到下一指数档的 65536 相隔 32，中点为 65520；本实现中点进到 Inf 侧。65519 发布为 65504，±65520 发布为 ±Inf，普通 half_round 本身不再抛出溢出异常；[矩阵](APPENDIX_beginner_glossary.md#g051)乘的返回守卫则另见 [QMMA发布边界](L4_e4m3_and_k32.md#publish-guards)。出处为 [primitives.inc:38–42、50–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L38)，[软件证明 RESULT:12、16](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L12) 明确保留该中点。

```math
\begin{aligned}
\mathrm{hadd}(a,b)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(a+b)),\\
\mathrm{hmul}(a,b)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(ab)),\\
\mathrm{hfma}(a,b,c)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(ab+c)).
\end{aligned}
```

公开源码是 [primitives.inc:103–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L103)。有限 half 的加法可统一到 $2^{-24}$ 整数格，乘积有效数最多 22 位，故这两种运算的 binary64 阶段精确；FMA 的精确合成则可能需要更宽整数，T1 必须显式保留先到 binary64、再到 F16 的两阶段。融合不等于先把乘积发布成 F16 再加 c，也没有在这里换成直接 exact→F16 的另一套参考。

“为了对齐原生而保留两阶段”的证据口径是：本项目沿用已经通过硬件接受域比较的软件参考，再证明替代 T1 与它相同。它不是原生内部使用 binary64 的证明，也不是一般三输入硬件全域等价证明。[窄域验收 RESULT:22–31](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L22) 中，加法/乘法对全部 raw 二输入先判实际有效性，再在接受域比输出；四个固定加数 FMA 探针也各覆盖一个 $2^{32}$ 输入域，**没有覆盖任意第三个 half 的 $2^{48}$ 硬件域**。例如加法接受 4,030,980,098 对、拒绝 263,987,198 对；接受与拒绝都不等于忽略输入，拒绝项没有 CPU 数值输出。

<a id="integer-t1"></a>
## 两阶段参考的替代实现

【CPU 重建／验证记录】冻结T1用精确整数保留先RN64、再RN16及零/非有限分支；其与T0的软件等价证明不证明[GPU](APPENDIX_beginner_glossary.md#g078)内部算法，当前公开模块仍可见std::fma。算术合同见上节；[双肢实现、证明前提与信任边界](APPENDIX_evidence_history.md#half-integer-implementation)移至附录。

<a id="atomic-add"></a>
## half 原子加为何不能任意换序

同址的每个贡献都读取前一次 half，执行加法并重新发布 half。下式中，A₀ 是按调用者合同取得的初始 half 值，tᵢ 是各项 half 贡献；π(j) 表示给定执行顺序中第 j 次使用的贡献编号，j 从1开始，直到所有贡献发布完。π 只记录这里采用的顺序，不额外证明一般 GPU 调度的全序：

```math
A_j=\mathrm{RN}_{16}\!\left(A_{j-1}+t_{\pi(j)}\right).
```

初始化必须在首项前完成，读取结果须等末项发布；改成先在 F32/binary64 求总和、最后一次 half，或把贡献分成任意[归约](APPENDIX_beginner_glossary.md#g050)树，都会改变合同。并行处理互不重叠地址不等于获准[重排](APPENDIX_beginner_glossary.md#g019)[同址贡献](APPENDIX_beginner_glossary.md#g095)。

公开 contract 先运行初始化阶段，再按两次贡献阶段，最后发布；每个二字节单元由 h_add 反馈，存在结果溢出拒绝。[ffn_contract.cpp:436–442、478–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L436)。projection 的同址循环也逐项 h_add，并检查初始化与贡献计数，[qkv_projection_impl.hpp:233–239、290–294](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L233)。L100 在映射给定的三项上明确先前两项、再第三项，[entry.cpp:64–71](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L64)。

整网涉及 [ViT](APPENDIX_beginner_glossary.md#g014) 的 8 次 contract、8 次 projection，以及 L100；[QKV](APPENDIX_beginner_glossary.md#g040) 共享执行器中的通用分支不表示 QKV 自身也有这种原子加。保存证据中，通用夹具换序为 DIFF，[step2a RESULT:15、58](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L15)；早期 projection 小单测也捕获换序 DIFF，但当时真实输入控制尚未运行，[step2b RESULT:9、16、23](../../../experiments/parity-cpp-step2b-qkv_projection-r01-20260928-codex/RESULT_ZH.md#L9)。早期 L100 换序记录明确 NOT_RUN，[entry RESULT:23、34](../../../experiments/parity-cpp-chain-entry-r01-20260930-codex-entry/RESULT_ZH.md#L23)，不改成已完成。

顺序与逐项发布在 [项目公理表:33–34](../../../experiments/parity-proof-program-r02-20261007-codex/resume12-20261009/delivery/AXIOMS_ZH.md#L33) 列为 MEASURED_AXIOM，**一般调度全序证书仍 OPEN**。有限重复一致不能证明任意到达顺序都固定，[租机 RESULT:21](../../../experiments/parity-rental-r03-addon-20261006-codex/RESULT_ZH.md#L21)。文末人工例直接演示同样三项、不同顺序分别得到 0 和 1；它是非结合性的演示，不是新增 GPU 调度测量。

<a id="f32-boundaries"></a>
## F32与half的边界

F16→F32的有限值可精确展开；F32→F16在显式转换处按RN16或该调用规定的RZ16发布。F32辅助运算不提前降成half，[纹理](APPENDIX_beginner_glossary.md#g027)half发布另有中点规则。
全链起止、FTZ和拒绝条件只在[F32站点清单](L4_fp32_ftz.md#sites)维护；本页保留half格式、融合与逐项发布算术。
NaN载荷差异及旧转换比较范围保留在[转换历史](APPENDIX_evidence_history.md#half-f32-history)，不由有限域例子升级。

<a id="worked-examples"></a>
## 人工计算例：人工编码输入到 F16 输出

全部输入为**人工构造的格式/算术例，不是模型系数**。Python 3.13 的 math.fma 执行 binary64 融合，hr 转写公开 half_round；finite_t1 用大整数演示冻结 T1 的两个舍入阶段，不代替 C++ 两肢证明。运行无需项目模块、模型数据或 GPU。

- 融合例：a=0x3c01、b=0x3bff、c=0xbc00，分别为 $1+2^{-10},1-2^{-11},-1$。精确乘加为 $2^{-11}-2^{-21}=1023/2097152$，FMA 输出 **0x0ffe**。若乘积先转 F16，它落在 $1+2^{-11}$ 中点下方而成为 1，再加 −1 得 **0x0000**。
- 半格例：0x3c00 加 0x1000 输出 **0x3c00**；0x3c01 加同一项则输出 **0x3c02**。次正规半格、负零、跨最小正规边界见 stdout。
- 同址顺序例：从 +0 开始加 2048、1、−2048，逐项 half 得 **0x0000**；改为 2048、−2048、1 则为 **0x3c00**。第一种顺序中 2048+1 恰为中点，1 被舍掉。
- 转换例：F32 编码 0x3f801000 为 half 中点，输出 **0x3c00**；相邻较大的 0x3f801001 输出 **0x3c01**。65519 与 ±65520 的结果也由脚本给出。

[完整程序、stdout与独立分数核对](APPENDIX_evidence_history.md#half-example-source)见附录；以上保留舍入位置与短结果。
