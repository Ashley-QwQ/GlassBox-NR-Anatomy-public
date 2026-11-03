# L4.hmma：F16 乘积、K16 公共格与逐步发布

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · 上层：[B0 适配](L3_b0_input.md#adapter)、[B70 末端头](L3_b70_history_output.md#b70-network) · 对照：[E4 QMMA](L4_e4m3_and_k32.md#qmma-k32-accumulation)、[F16 格式与舍入](L4_half_arith.md#format)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

<a id="hmma"></a>
## 对象、记号与适用域

【CPU 重建】本页首先解释当前源码的[标量](APPENDIX_beginner_glossary.md#g076) [K16](APPENDIX_beginner_glossary.md#g065) 复现规则；它不是硬件[全域](APPENDIX_beginner_glossary.md#g111)定理。A、B 是各16个 [F16](APPENDIX_beginner_glossary.md#g054) [编码](APPENDIX_beginner_glossary.md#g057)，C 是一个 F16 [seed](APPENDIX_beginner_glossary.md#g042)，输出也是 F16。B0 的 hmma_cached / hmma_dot 隐含 C=[+0](APPENDIX_beginner_glossary.md#g070)；B70 的 hmma_seed 显式接收 C。缓存精确解码值不增加舍入。

F16为1位符号、5位[指数](APPENDIX_beginner_glossary.md#g058)、10位尾数域；有限范围至±65504，最小正[次正规](APPENDIX_beginner_glossary.md#g068)为2⁻²⁴。操作数的[Inf](APPENDIX_beginner_glossary.md#g069)/NaN不在这些函数的接受域，±0与非零次正规不能一律清除；完整编码见上链。

【原生行为／验证记录】[sm_120](APPENDIX_beginner_glossary.md#g078) 的保存探针支持下面公共格候选的大量有限案例，同时已发现其负零预测反例；负零修订仍待裁定。跨架构与候选状态见 [硬件边界](#hardware)，不能把当前 CPU 源码描述升级为所有原生输入的规则。

| 记号 | 本页含义 |
|---|---|
| v(h)、E_h | F16 精确值、编码中的5位存储指数；格式见上链 |
| η(h) | 正规数为 E_h−15；非零次正规固定取−14，属于字段指数，非实际 log₂ 幅值 |
| e_C | 非零 seed 的 ⌊log₂\|v(C)\|⌋；C=0 时不参与最大值 |
| E、g、RZ_g | 本次公共指数、二幂[格距](APPENDIX_beginner_glossary.md#g066)、[向零](APPENDIX_beginner_glossary.md#g060)截到该格 |
| [RN16](APPENDIX_beginner_glossary.md#g059) / K16 | 最近偶数[发布](APPENDIX_beginner_glossary.md#g091) F16 / 一步16个乘积；不是执行线程形状 |

<a id="grid"></a>
## 一步的公共格、精度与顺序

对有限输入，当前软件规则为：

```math
\begin{aligned}
E&=\max\bigl(-21,\ e_C,\ \{\eta(a_k)+\eta(b_k):v(a_k)v(b_k)\ne0\}\bigr),\\
g&=2^{E-25},\qquad RZ_g(x)=\mathrm{trunc}(x/g)\,g,\\
Y&=\mathrm{RN}_{16}\!\left(RZ_g(v(C))+
             \sum_{k=0}^{15}RZ_g(v(a_k)v(b_k))\right).
\end{aligned}
```

1. 用原 F16 指数域选择公共格；乘积为零的项不参与 E。B0 全零乘积直接返回 +0。
2. 有限 F16 乘积最多22位有效数，可在 [binary64](APPENDIX_beginner_glossary.md#g056) 中精确表示；此处**没有乘积先转 F16**。
3. seed 和每个乘积各自除以 g、向零取整数；带符号整数从 k=0 到15求和。接受域内这些整数及总和精确，不能插入每项 F16 舍入。
4. 整数总和乘回 g，再由 half_round 作一次 RN16。F16 次正规保留，不套 F32 FTZ。
5. 后继 K16 若存在，携带这个已发布的 F16；跨步不能先求实数总和再只舍入一次。软件的整数循环不证明 GPU 物理加法树。

“25”指公共格相对字段指数的位置，不能理解为浮点[累加器](APPENDIX_beginner_glossary.md#g064)统一有25位尾数，也不能把 products 与 seed 先全精确求和后才截断。

源码：[mapexec_base.hpp:157–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp#L157)、[decode_reuse.inc:71–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/decode_reuse.inc#L71)、[outtail.cpp:60–61](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L60)。末端 RN16 见 [primitives.hpp:12–36](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/primitives.hpp#L12)。

<a id="callers"></a>
## B0 与 B70 各自接在哪里

| [调用](APPENDIX_beginner_glossary.md#g080) | 输入与 K 分组 | seed / 发布 / 拒绝 |
|---|---|---|
| B0 [16→32](APPENDIX_beginner_glossary.md#g007) 适配 | 每个位置的 feat[16] 与每输出通道的16个 F16 [资源](APPENDIX_beginner_glossary.md#g079)项；每输出一个 K16 | C=+0；先得到32个 F16，再 [Q8](APPENDIX_beginner_glossary.md#g061) 供[前馈](APPENDIX_beginner_glossary.md#g037)主路；适配 F16 另留作前馈[残差](APPENDIX_beginner_glossary.md#g017)。源拒绝非有限操作数及单项[缩放](APPENDIX_beginner_glossary.md#g031)超界；这个函数没有与 B70 相同的末端有限守卫 |
| B70 末端头 | [窗口](APPENDIX_beginner_glossary.md#g015)出口32个 F16 按固定通道置换分成两组16；两组分别使用自己的 F16 头参数 | 第一步 C=+0，第二步 C=第一步 F16。无[历史](APPENDIX_beginner_glossary.md#g024)时3个 RGB 头，有历史时另算置信头；拒绝非有限输入/seed、整数总和范围≥2⁵²及末端 half [overflow](APPENDIX_beginner_glossary.md#g071) |

调用点：[b00.hpp:16、42–44](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L42)、[outtail.cpp:94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L94)。不披露资源系数；后续颜色/历史混合见 [B70](L3_b70_history_output.md#b70-mix)。函数能发布 Inf 与调用者是否接受它须分别看。

<a id="qmma-difference"></a>
## 与 sm_120 E4 QMMA 的差别

| 项 | 本页 HMMA CPU 规则 | 本串 [E4](APPENDIX_beginner_glossary.md#g055) QMMA 规则 |
|---|---|---|
| A/B、一步项数 | F16、16项 | E4、32项 |
| 非零次正规字段指数 | −14 | −6 |
| seed / 出口 | F16；B0隐含零、B70显式携带 | F16 seed，每 K32 再发布 F16 |
| 公共格 | 本页含 −21 下界、E−25；使用 F16 字段 | 按 E4 字段及 half seed 定格；见独立算术叶 |
| 证据 | 旧候选存在480个有效有符号零反例 | 另一组独立候选、控制及保存案例；不能借来关闭 HMMA 零规则 |

操作数格式、分组、守卫和证据各自[绑定](APPENDIX_beginner_glossary.md#g103)。两页都出现 E−25，不使它们可以互换；也不能把旧 sm_75/sm_86 的 E4 解码后 F16 执行当成原生 E4 QMMA。

<a id="hardware"></a>
## 跨架构：哪些是旧硬件观测，哪些仍开放

【验证记录】下表只转述具名保存记录，没有新增设备运行；候选存活仅限该实验用例。

| 架构 | 保存观测支持的候选 | 范围与限制 |
|---|---|---|
| sm_75 / RTX 2060 | K8 的字段 F24、整 K8 发布候选 | [原报告:56–71](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#L56)；K8 结果不能外推本页 K16 |
| sm_86 / RTX A2000 Laptop | K16 分两个 K8，每组按 F24 截断/发布候选；65/65辨别例与3748/3748真实片段 | [Ampere 报告:9–24](../../../experiments/parity-claude-ampere-probe-r01-20260921/RESULT_ZH.md#L9)；全 K16 F25 候选在此失败 |
| sm_89 / RTX 4090 D | 回传验收中的 HMMA 候选与 sm_86 一致 | [Ada 判读](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#L24)；设备、载荷身份与双遍条件绑定原回传，不是此次实测 |
| sm_120 | 旧 K16 整组 F25 候选；后续1,380,992例中1,380,512一致、480例 CPU −0 / GPU +0 | [后续扫描:25–31](../../../experiments/parity-proof-gpu-sweeps-r01-20261007-codex/RESULT_ZH.md#L25)正式证伪旧组合规则，不能忽略零符号 |

【原生行为／未知】480例差异不能孤立归因于乘积截断、内部累加或最终发布。把旧输出 −0 改为 +0 的候选虽然可匹配该批保存例，仍为 [OPEN](APPENDIX_beginner_glossary.md#g104)。这项规范化曾在隔离候选 `63ff1ff6` 实现并合入历史封存 `49a98a0b`，但发布线 M/M2 未带上，所以公开 v2.0.0-preview 源码（GlassBox-NR `e4a9b42`）的 hmma_seed/hmma_dot/hmma_cached 仍发布 −0；v2.0.1-preview（`636b321`）在这三处末端补回了 +0 规范化（sm_120 保存扫描单元门 0 不一致，1080p f0 端到端 158/158），本文其余代码引用与行号仍按 v2.0.0 源码；它是对齐这批保存例的实现选择，不把候选升级为已证规则。不在文档修订中改算术。仅 C 输入的63,488个有限 half 通过记录也不覆盖一般 A/B/C 组合：[窄域验收:22–31](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L22)。架构总裁定见 [ARCH §7.2.2–7.2.3](../../../ARCHITECTURE_V3_ZH.md#L865)。

闭合路径（NOT_RUN）：固定有限接受域，先分别扫描只有带符号零乘积、只有±0 seed、以及非零乘积精确相消三组；随后保持操作数多重集不变，只交换K8分组/项序，并分别记录每步原生输出[位型](APPENDIX_beginner_glossary.md#g057)。对照能排除乘积零符号、分组相消或末端零规范化的候选规则，但单一出口仍不能唯一证明内部流水线；本轮不运行新硬件探针，也不规范化旧反例。

<a id="worked-example"></a>
## 真实 C++ 小例：乘积舍入与跨 K16 舍入

【CPU 重建／实际执行】[脚本](examples/hmma_r04f.py)抽取上述三个原函数及原 half 辅助函数，在[严格浮点编译](APPENDIX_beginner_glossary.md#g098)参数下执行人工输入；不编译网络模块。[源 SHA、编译器、参数与输出](examples/hmma_r04f.result.json)可复核，完整程序放在 examples 中。

例一：其余14项为零，A=[0x3c01,0xbc00]，B=[0x3c01,0x3c02]，C=0。精确乘积和为
$(1+2^{-10})^2-(1+2^{-9})=2^{-20}$；E=0、g=2⁻²⁵，结果发布为 F16 **0x0010**。若把每个乘积先转 F16，首乘积的小项被舍掉，相消结果为 **0x0000**。

例二：第一 K16 只有1024与0.5两个非零乘积，RN16半格取偶得到1024；第二 K16 只有−1024与0.5，携带前一步1024得到0.5。若取消中途 F16 发布，四项实数和为1。

~~~text
dot 0010
cached 0010
seeded 0010
product_half_control 0000
first_K16 6400
two_K16 3800
single_final_round_control 3c00
nonfinite_operand_refused
~~~

这两例检验当前软件的格式、舍入位置与一个拒绝分支，不是模型系数、原生新测或完整接受域证明；硬件负零与一般有限 K16 规则仍按上节保留开放。
