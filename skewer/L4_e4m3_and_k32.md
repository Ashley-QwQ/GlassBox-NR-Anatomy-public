# L4：E4M3 字节与 sm_120 K32 累加

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[返回 L3 矩阵链](L3_qmma_e4m3.md#qmma-e4m3) · [整串](INDEX.md)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| b,s,e,m | [E4](APPENDIX_beginner_glossary.md#g055)[编码](APPENDIX_beginner_glossary.md#g057)、符号、存储[指数](APPENDIX_beginner_glossary.md#g058)、尾数域 |
| u(b)、C | 2⁻⁹整数单位的E4解码、[half](APPENDIX_beginner_glossary.md#g054) [seed](APPENDIX_beginner_glossary.md#g042) |
| e_f,E,g | 字段指数、公共[对齐指数](APPENDIX_beginner_glossary.md#g066)、格距，按上下文区分存储指数 |
| L,S_min,S_exact | 大[动态范围](APPENDIX_beginner_glossary.md#g071)相消守卫的最大项/最小非零乘积/未放置和 |
| Q_g、[RNE16](APPENDIX_beginner_glossary.md#g059) | 格点[向零](APPENDIX_beginner_glossary.md#g060)放置、最近偶数half[发布](APPENDIX_beginner_glossary.md#g091) |

<a id="e4m3-format"></a>
### L4.e4m3-format 存的一个字节究竟表示什么

- 是什么：1 位符号、4 位指数、3 位尾数；最高指数域没有沿用 IEEE 小格式的 [Inf](APPENDIX_beginner_glossary.md#g069) 编码。
- 输入 → 输出：一个字节 b → 有限值或 NaN 标志；F16 [激活](APPENDIX_beginner_glossary.md#g045)反向[量化](APPENDIX_beginner_glossary.md#g061)为 E4 字节。[矩阵](APPENDIX_beginner_glossary.md#g051)段采用该编码，辅助[尺度](APPENDIX_beginner_glossary.md#g031)/偏置与暂存仍按各自类型读取。
- 怎么算：
  ~~~text
  s = b >> 7；e = (b >> 3) & 15；m = b & 7
  若 e=15 且 m=7：NaN 编码，本 QMMA 输入拒绝
  若 e=0：u = (−1)^s × m
  否则：u = (−1)^s × (8+m) × 2^(e−1)
  实际值 = u × 2^−9；两种零编码另保留存储符号
  ~~~
- 数值规则：解码为精确整数/二幂变换，有限 E4 可精确转 F16。反向 $Q8$ 选最近码、平局取偶码；±Inf 饱和到 ±448，NaN 拒绝。E4 没有 Inf 编码，0x78 仍为有限数。
- 为什么这么算：位域决定可表示集合；短编码减少矩阵/激活的存储与搬运，设计目的未由本轮证明。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED（转换接受域）；[半域原语 RESULT:43–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md)。
- 往下：本主题位格式已到底；[K32 累加](#qmma-k32-accumulation)。

```math
\mathrm{value}(b)=
\begin{cases}
(-1)^s m\,2^{-9}, & e=0,\\
(-1)^s(8+m)\,2^{e-10}, & e>0,\ (e,m)\ne(15,7).
\end{cases}
```

| 编码类别 | 数值/处理 | 边界 |
|---|---|---|
| 0x00 / 0x80 | [+0](APPENDIX_beginner_glossary.md#g070) / −0 | 整数 u 都是 0；直接转 F16 的辅助函数保留零符号 |
| e=0、m=1..7 | [次正规](APPENDIX_beginner_glossary.md#g068) | 最小正数 $2^{-9}$，最大正次正规 $7\cdot2^{-9}$ |
| e=1、m=0 | 最小正正规数 | $2^{-6}$ |
| e=15、m=0..6 | 仍有限 | 0x78 为 256，0x7e 为 448；负数翻转符号位 |
| 0x7f / 0xff | NaN | 两个码，无 ±Inf 编码 |
| 全部有限码 | 含两种零 | 共 254 码；本轮脚本枚举分类同此计数 |

$Q8$ 的可手算定义：取符号，在正 E4 码 0..126 中选与输入幅值距离最小者，平局选最低位为 0 的码，再恢复符号；幅值达到 448 或为 Inf 时饱和。生产查表优化保存同一函数结果，不新增舍入。

| 格式断言 | 当前公开源码 path:line | 实验/裁决 |
|---|---|---|
| 位域、整数单位、NaN 拒绝 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:22–25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L22)、[primitives.inc:61–67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L61) | [半域原语 RESULT:43](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md)：成对解包 64,516 接受、1,020 含 NaN 组合排除；不是独立单字节码计数 |
| E4→F16 保留 ±0，[QMMA](APPENDIX_beginner_glossary.md#g065) 整数解码不保留零号 | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L67)、[qmma_sm120.hpp:25、38](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L38) | [EQUIVALENCE:5、7、13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md)；一般硬件 signed-zero 合同未建立 |
| F16→E4 [satfinite](APPENDIX_beginner_glossary.md#g062)、平局取偶 | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68)、[同文件:85–100](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L85) | [半域 RESULT:44–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md)：各 63,490 接受、2,046 NaN 拒绝，接受域零差；[非有限诊断:103](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md) 明记 ±Inf 饱和 |
| 预解码表保存数值/NaN 标志，消费时才报错 | [GlassBox-NR/cpp/chain_tin_optm/decode_reuse.inc:2–13](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/decode_reuse.inc#L2)、[qmma_sm120.hpp:72–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L72) | [移植 RESULT:15–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| 数值转换不同于位复制 | [GlassBox-NR/cpp/chain_tin_optm/portable_bits.hpp:5–8](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/portable_bits.hpp#L5) | CENSUS：只复制同宽对象字节；不能当成[量化](APPENDIX_beginner_glossary.md#g061)，转换接受域依前述实验 |

<a id="qmma-k32-accumulation"></a>
### L4.qmma-k32-accumulation 公共格点与整 K32 精确和

- 是什么：32 个精确 E4 乘积和一个 F16 seed 分别放置到共同格点，再只发布一次 F16。
- 输入 → 输出：32 对有限 E4 与有限 C →一个 F16；分析模型可形成 Inf，默认生产包装在返回前拒绝。
- 怎么算：
  ~~~text
  1. 先解码/检查 seed，再依次检查被消费的 E4，形成精确乘积 p_i。
  2. E 取非零乘积的两操作数 e_f 之和与非零 C 的 e_C 的最大值。
  3. g = 2^(E−25)；分别算 Q_g(C) 与每项 Q_g(p_i)。
  4. 从 Q_g(C) 开始，依 i=0..31 精确加 Q_g(p_i)。
  5. 最终一次 RNE16，再按生产守卫接受/拒绝；没有 K8/K16 分组或逐乘积 half 发布。
  ~~~
- 数值规则：正规 E4 的 $e_f=e-7$，次正规固定 −6；F16 次正规 seed 的 $e_C$ 仍取实际指数。放置为 RZ，末端才 RN-even；支持次正规 F16 输出。当前软件模型把零和规范成 +0。
- 为什么这么算：field、F25、C 进对齐最大值并截断、整 K32 发布，是[冻结](APPENDIX_beginner_glossary.md#g103)候选经硬件判别选中的行为；不能据此证明内部唯一加法树。
- 我们怎么知道：MEASURED / CENSUS（范围分开）；[RULE:17–29](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star)。
- 往下：本主题算术已到底；[发布/守卫](#publish-guards)、[可执行例子](#worked-examples)。

```math
e_f(x)=
\begin{cases}
e(x)-7,&x\text{ 为正规 E4},\\
-6,&x\text{ 为非零次正规 E4},
\end{cases}
\quad
E=\max\!\left(\{e_f(a_i)+e_f(b_i):p_i\ne0\}\cup\{e_C:C\ne0\}\right).
```

```math
g=2^{E-25},\quad
Q_g(x)=\mathrm{sgn}(x)\left\lfloor |x|/g\right\rfloor g,\quad
\mathrm{out}=\mathrm{RNE}_{16}\!\left(Q_g(C)+\sum_{i=0}^{31}Q_g(p_i)\right).
```

全零乘积时非零 C 的值保持；C 也为零时当前实现返回 +0。比如 E4 0x01 的实际指数为 −9，但 $e_f$ 是 −6；换成实际乘积 floor-log 最大值会得到另一个被排除的模型。

整数对应为 $c=C2^{24}$、$t_i=p_i2^{24}$、$\mathrm{shift}=\max(E-1,0)$。源码把两操作数各按 $2^{-9}$ 单位解码成整数，再相乘并乘 64，恰得到 $t_i$。对 c 与各 $t_i$ 的绝对值先右移再左移 shift 位，最后恢复符号，才是负数的向零放置；不能直接用负数算术右移代替。z 先取放置后的 c，再逐项加放置后的 $t_i$。shift 原式为负时，格点细于 $2^{-24}$，各项已在整数单位格上，所以取 0 不改变结果。

| 对应关系 | 当前公开源码 path:line | 实验/软件记录 |
|---|---|---|
| E4 单位 $2^{-9}$，seed 单位 $2^{-24}$ | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:22–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L22) | [EQUIVALENCE:5–7](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| field、C 实际指数、C 进 max | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:33、50–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L33) | [RULE:19–24](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star)；batch3 排除 [value](APPENDIX_beginner_glossary.md#g067)/renorm 类 |
| 乘积不预舍入成 half，整数乘 64 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:54–55](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L54) | [EQUIVALENCE:7、11](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md)、[移植 RESULT:15–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| RZ 放置，先 C 再 32 项精确和，末端一次发布 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:34–46、58–65](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L34) | [RULE:21–22](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star)、[EQUIVALENCE:9–13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |

有限输入下，任意整数[部分和](APPENDIX_beginner_glossary.md#g050)幅值不超过
$(32\cdot448^2+65504)2^{24}=108851114278912<2^{47}$。
截断不增幅，所以 int64 加法精确；能[重排](APPENDIX_beginner_glossary.md#g019)的是这些整数，不是跨 K32 的 F16 或网络[浮点](APPENDIX_beginner_glossary.md#g056)归约。本轮脚本计算此界；软件依据是 EQUIVALENCE:11 与 qmma_sm120.hpp:54–60。

<a id="publish-guards"></a>
## 一次发布在哪里舍入，65520 在哪里被拒绝

对 z 取幅值最高位 top，保留 11 位有效数，其余为 r。r 大于 tie 时进位，等于 tie 且 q 为奇数时进位；进位到 2048 时调整指数；次正规分支返回对应尾数。当前整数模型没有 binary64 中间舍入，乘积也没有预先 F16 舍入。

| 阶段 | 行为 | 当前公开源码 path:line / 证据 |
|---|---|---|
| 接收 seed | 指数域 31 的 NaN/Inf 先拒绝 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:27–31、50–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L27)；[移植 RESULT:15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| 放置/和 | RZ 后精确求和，另检查幅值达到 $2^{52}$ 的范围错误 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:34–35、58–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L58)；[EQUIVALENCE:9–13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| [D27](APPENDIX_beginner_glossary.md#g109) 限域 | 保留旧消去/动态范围拒绝条件，有限模型可算不等于生产接受 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:61–64](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L61)；[移植 RESULT:9、15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#实现与定位) |
| F16 发布 | 一次整数 RN-even；零为 +0，溢出生成带符号 Inf [位型](APPENDIX_beginner_glossary.md#g057) | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:37–46、65](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L37)；[EQUIVALENCE:13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| 生产返回前 | model=false 时结果指数域 31 触发 QMMA half overflow，不返回 Inf | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:66、69–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L66)；[非有限诊断:23、104–105](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md) |
| 随后 E4 量化 | 再作 RN-even/satfinite，可能出现二次格式舍入差异 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L104)、[primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68)；本轮例 C |

D27 可按整数算：$L=\max(|c|,\max_i|t_i|)$、$S_{\min}=\min_{t_i\ne0}|t_i|$、$S_{\rm exact}=c+\sum t_i$。当 L 和非零乘积存在，若
$\lfloor\log_2 L\rfloor-24\ge12$、
$\lfloor\log_2 L\rfloor-\lfloor\log_2 S_{\min}\rfloor\ge20$、
$\lfloor\log_2 L\rfloor-\lfloor\log_2|S_{\rm exact}|\rfloor\ge2$
同时成立，生产拒绝；精确和为 0 时最后一个量用 99。最小项只从乘积取，最大项包括 seed。这是域守卫，不是本轮证明的硬件分界。

**65520 是格点放置后总和的 F16 溢出中点。** 最大正有限值 65504，再往上间距 32，中点 65520；平局进位到溢出侧。本模型对幅值低于 65520 的邻近值可发布 65504，对幅值达到 65520 的值形成 Inf 再拒绝。须先做格点放置，不能只拿未截断数学点积套阈值。另见 [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:35–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L35)，42 行明确包含等号。软件阈值不证明硬件完整混合非有限/溢出合同。

<a id="build-selection-r04l"></a>
## 编译时选择的合同（审计 V07.01，排名2）

`QMMA_TARGET_SM120 == 1` 才进入本页 field/F25 核；未定义或其他值进入保留的旧 value/D27 分支。不能按[宿主](APPENDIX_beginner_glossary.md#g096)[GPU](APPENDIX_beginner_glossary.md#g078)或头文件存在推定选择。具名隔离构建同时记录 `-DQMMA_TARGET_SM120=1` 与强制包含共用头文件，归属以该构建清单及其源码身份为准；它不自动证明任意下游二进制用了相同选项。[build_manifest_v3.json:13–15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/build_manifest_v3.json#L13)，[选择入口:107–110](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L107)。

旧分支的完整替代式为：以 $2^{-24}$ 为单位，`c=F16(seed)*2^24`、`t[i]=u(a[i])*u(b[i])*64`，`L=max(abs(c),max(abs(t)))`，`shift=max(floor(log2(L))+1-27,0)`（L=0时内部log取−99）。`place(v)=sign(v)*((abs(v)>>shift)<<shift)`，从 `place(c)` 起按0..31加 `place(t[i])`；这是幅值右移后恢复符号，负数不作算术右移。若和幅值≥2^52则拒绝，再应用前述D27三个条件；最终一次 RN16(sum*2^-24)，指数全1拒绝。此旧分支与field/F25不可混称。[ffn_contract.cpp:111–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L111)，[TIN同式:129–153](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L129)。

<a id="worked-examples"></a>
## 合成例：输入字节到 F16 输出

左右输入均人工构造，**未读取或列出模型系数**。下列字节按十六进制列前三项，余项补正零到 32 对；初始 seed=0x0000，除非另写。脚本实际执行，并以独立 Fraction 精确分数及 Python F16 转换核对可比较舍入。

### A：同一 K32 内只在最后舍入

左 [38,01,01]、右 [38,28,01]，乘积为 $1,2^{-11},2^{-18}$。E=0，$g=2^{-25}$，均不丢位。
整数项为 16777216、8192、64，和 16785472，实际值 $262273/262144$。
它在 F16 半格 $1+2^{-11}$ 上方，输出 **0x3c01**，即 $1+2^{-10}$。

若前两对放第一步、第三对另放下一 K32：第一步 $2049/2048$ 恰为中点，偶数规则取 0x3c00；第二步以它为 seed，加 $2^{-18}$ 后仍为 **0x3c00**。这展示整 K32 与分组发布的差别；本[算子](APPENDIX_beginner_glossary.md#g035)不会因只有三个非零项而额外分组。

### B：格点放置不能省略

左 [78,f8,01]、右 [38,38,01]，乘积 $256,-256,2^{-18}$。
E=8，$g=2^{-17}$，最后一项 RZ 变 0，输出 **0x0000**。
忽略格点直接把精确总和 $2^{-18}$ 转 F16，会得 **0x0040**。
前两项幅值未达到大动态范围相消守卫的top条件，此生产例被接受。

### C：F16 后再 E4 的二次格式舍入

左右均为 [38,28,01]，精确结果 $1+2^{-4}+2^{-18}=278529/262144$。
先到 F16 得 **0x3c40**，值为 $17/16$；随后在 E4 的 1 与 $9/8$ 中点，偶码取 **0x38**。
直接从未舍入精确值转 E4 则略高于中点，取 **0x39**。
这是两次不同目标格式的发布，不是 K32 内多一次 binary64→F16 舍入。

### D：65520 与默认生产守卫

| 左前三字节 | 右前三字节 | 放置后总和 | 默认生产结果 |
|---|---|---:|---|
| [78,c8,b8] | [78,48,38] | 65519 | 0x7bff，即 65504 |
| [78,c8,00] | [78,48,00] | 65520 | QMMA half overflow；分析发布位型 0x7c00 |
| 将上一行左输入翻转符号 | 同上一行 | −65520 | QMMA half overflow；分析发布位型 0xfc00 |

E=16、$g=2^{-9}$，列出值均能精确放置。分析模式仅展示被拒绝前的模型位型，不能算生产返回或硬件测量。

### 实际执行脚本

中间整数单位为 $2^{-24}$。e4_from_units 只用于本例有限值的最近码比较；完整 NaN/Inf 转换合同在格式片已列。无需项目模块、[权重](APPENDIX_beginner_glossary.md#g079)、数学[函数表](APPENDIX_beginner_glossary.md#g074)或 GPU：

[完整程序与原输出](APPENDIX_evidence_history.md#e4-example-source)见附录；上方保留格式与K32算术例。
