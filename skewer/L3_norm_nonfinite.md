# L3.norm-nonfinite：32 通道范数、缩放与非有限边界

<!-- beginner-r04m:start intro -->
<a id="beginner-norm"></a>
【人工概念例，非测量】(3,4)的平方和是25、长度是5；都乘1/5变(0.6,0.8)。把输入换成(6,8)，长度也成倍，整体[缩放](APPENDIX_beginner_glossary.md#g031)后仍得同一方向。这里仅用两项和理想实数说明“调一组数的大小”，不冒充实际32项与[函数表](APPENDIX_beginner_glossary.md#g074)的结果。

真实步骤只在[投影](APPENDIX_beginner_glossary.md#g038)后对Q、K各自每组32项做平方和缩放，V不做；不先减[均值](APPENDIX_beginner_glossary.md#g044)，也不在平方和上加ε，而是取规定下限。[查询](APPENDIX_beginner_glossary.md#g040)的另一尺度随后另乘，不能混成一个旋钮。[非有限](APPENDIX_beginner_glossary.md#g069)传播、精确加法树及独立[A1](APPENDIX_beginner_glossary.md#g107)分支继续留在下面。
<!-- beginner-r04m:end intro -->

[整串目录](INDEX.md) · 上层：[TIN](L2_03_tin_encoder.md)、[split16](L2_04_split16_encoder.md#qkv)、[ViT QKV](L2_05_vit.md#qkv)、[B70](L2_09_b70.md) · 相邻步骤：[attention](L3_attention_softmax.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| x₀…x₃₁ | 一个位置、一个头内32个[half](APPENDIX_beginner_glossary.md#g054)分量 |
| s、n、ε | 平方和、截下界后的统计量、下界常量 |
| r、γ | half倒数平方根、[归一化](APPENDIX_beginner_glossary.md#g043)后乘性尺度 |
| i,l,u,a | 公式内局部[归约](APPENDIX_beginner_glossary.md#g050)/取数索引，范围在各式给出 |

本页伪代码的 `T_RSQ(x)` 是 [MUFU 数值包装](L4_mufu.md#value-wrapper) 的短写，返回认证结果解码后的 F32 数值；`F32(n)` 是 half 数值的精确展开。取位型与解码不新增舍入并保留零的符号；这不要求运行时直接按 raw32 索引，B0/TIN 的 half 小表已预含该结果的 RN16，[各家族接口与接受域](#affine)仍保持。

<a id="norm-nonfinite"></a>
### L3.norm-nonfinite 每个位置、每头 32 通道的平方和归一化

- 是什么：从 QKV 投影的 half 分量计算头内长度，经 [RSQ](APPENDIX_beginner_glossary.md#g072) 与缩放后[发布](APPENDIX_beginner_glossary.md#g091) Q/K 的 [E4](APPENDIX_beginner_glossary.md#g055) 字节。
- 输入 → 输出：同一 t、同一 h 的 32 个 half → 32 个归一化 half → E4；[TIN](APPENDIX_beginner_glossary.md#g011) 为 C=32/64/128/256，[split16](APPENDIX_beginner_glossary.md#g013) 为 C=[512](APPENDIX_beginner_glossary.md#g007)，[ViT](APPENDIX_beginner_glossary.md#g014) 为 C=1024，B0/B70 为 C=32。
- 怎么算：
  ~~~text
  1. 取本位置、本头的 x[0:32]，Q 与 K 各做一次。
  2. 按本家族的固定 half 平方/融合/加法树求 s。
  3. n=max(s,ε)，ε=half(0x0410)；没有在 s 上加 ε。
  4. r=RN16(T_RSQ(F32(n)))。
  5. 每分量先 H×(x_i,r)，再按家族依次乘规定尺度。
  6. 每次 half 乘法单独发布，最后转 E4。
  ~~~
- 数值规则：统计量是平方和；没有减均值、求方差或除以 32。归约轴是头内通道，[窗口](APPENDIX_beginner_glossary.md#g015)的 64 个位置和不同头各自独立。统计量可由有限分量[上溢](APPENDIX_beginner_glossary.md#g071)为 +Inf。
- 为什么这么算：调节 Q/K 的头内长度，再由[查询尺度](APPENDIX_beginner_glossary.md#g052)控制后续分数范围；训练时的命名不能替代实际计算图。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)，[tin.cpp:114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)、[b00.hpp:25、46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L25)、[outtail.cpp:83、90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L83)，以及[数据驱动图](#map-norm)。非有限后果的原生对照与 CPU 诊断见[证据](#evidence)。
- 往下：[norm32 的树](#norm32)、[split16 / ViT](#map-norm)、[尺度与 RSQ](#affine)、[L6 到 A1](#nf-path)、[实际执行例](#worked-example)。

<a id="norm32"></a>
### L3.norm-nonfinite.norm32 TIN、B0、B70 的显式归约

- 是什么：32 个通道分成四段，每段 8 项；先局部融合平方和，再以固定配对合并。
- 输入 → 输出：一个 Q 或 K 头[向量](APPENDIX_beginner_glossary.md#g076) x → half 统计量 n。
- 怎么算：
  ~~~text
  对 i=0,…,7：
    a_i = HF(x_i,x_i,H×(x_(16+i),x_(16+i)))
    b_i = HF(x_(8+i),x_(8+i),H×(x_(24+i),x_(24+i)))
    t_i = H+(a_i,b_i)
  u_i = H+(t_i,t_(i xor 4))
  v_i = H+(u_i,u_(i xor 2))
  s   = H+(v_0,v_1)
  n   = max(s,ε)
  ~~~
- 数值规则：第 3、4 段的平方先发布 half，再作为各自融合步骤的加数；两个融合结果各发布 half，后续每个 [H+](APPENDIX_beginner_glossary.md#g063) 再发布 half。不能先在 [F32](APPENDIX_beginner_glossary.md#g056) 累加 32 个平方再转 half，也不能把两平方全部保留高精度后一次舍入。
- 下界：ε=0.00006198883056640625，[编码](APPENDIX_beginner_glossary.md#g057) 0x0410，来自代码常量。它是 s 的下限，不是模型[资源](APPENDIX_beginner_glossary.md#g079)里的待公布系数；全零组使用该下界，输出仍为零。
- 为什么这么算：固定配对规定half加法树的结合次序，改变配对可能改变逐次舍入；训练动机未知。
- 我们怎么知道：CENSUS，[tin.cpp:115–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L115)、[b00.hpp:25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L25)、[outtail.cpp:83](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L83)；Python 对应树为 [sm120_b1.py:357–371](../../../mlxdlss/sm120_b1.py#L357)。
- 往下：[RSQ 与乘性尺度](#affine)、[上溢实例](#nf-path)；half 原语的证明与边缘规则追到 [L4.half-arith](L4_half_arith.md)。

TIN 的[调用](APPENDIX_beginner_glossary.md#g080)索引为 Q 的 t·3C+32h+i，K 在此基础上加 C；V 加 2C，直接[量化](APPENDIX_beginner_glossary.md#g061)而不走本树。B0 与 B70 各只有一个 32 通道头。B70 的同一树位于[前馈](APPENDIX_beginner_glossary.md#g037)后、[注意力](APPENDIX_beginner_glossary.md#g039)分数之前；[历史](APPENDIX_beginner_glossary.md#g024)[取样](APPENDIX_beginner_glossary.md#g027)权重的归一化属于另一条 RCP 路径，不能混作 Q/K 的统计量。对应调用：[tin.cpp:119–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119)、[b00.hpp:44–46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L44)、[outtail.cpp:90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L90)；后续权重路径见 [L3.attention-softmax](L3_attention_softmax.md#window-attention)。

<a id="map-norm"></a>
### L3.norm-nonfinite.map split16 与 ViT：先解释来源表，再解释归约

- 是什么：用[冻结](APPENDIX_beginner_glossary.md#g103)图确定 32 个分量的来源、融合方向和合并次序；通用 C++ 执行器本身不规定完整 norm。
- 输入 → 输出：split16 融合 qkv 的内部 half 或 ViT QKV 的 half 部分和合并结果 → 每头 Q/K 的统计量与 E4 发布。
- 怎么算：将图中四组取数片记作 x[a,l,u]，a=0…3、l=0…3、u=0/1，恰好 32 个分量。下式使用本图的取数顺序：
  ~~~text
  pair(a,b) = HF(a,a,H×(b,b))
  t[l,u] = H+(pair(x[0,l,u],x[1,l,u]),
               pair(x[2,l,u],x[3,l,u]))
  v[l,u] = H+(t[l,u],t[l xor 2,u])
  w[l,u] = H+(v[l,u],v[l xor 1,u])
  s      = H+(w[0,0],w[0,1])
  n      = max(s,ε)
  r      = RN16(T_RSQ(F32(n)))
  ~~~
- 索引结构：a,l,u 是图内的来源坐标，不直接等于[逻辑](APPENDIX_beginner_glossary.md#g085)连续通道编号。split16 还要执行实例的窗口移位和位置选择；ViT 的 x 来自最终一段[矩阵](APPENDIX_beginner_glossary.md#g051)结果与已保存部分和的 half 合并。归约不跨 [token](APPENDIX_beginner_glossary.md#g041) 或头；不能把来源表删除后只保留张量形状。
- 叶子对应的通道：从实际消费 Q/K 的 score K32 的第 k 项反查，x[a,l,u] 的叶子就是头内通道 d。每个 RSQ 根、每个 lane 有自己的表：L27 的 node 5842/lane 0 归约 K[token0,·]，l=0,u=0 时 a=0..3 依次读 d=2、18、0、16，l=2,u=0 时读 d=10、26、8、24；下一个根 node 5843 的前四项是 d=3、19、1、17，不能照抄第一个根。按上面的 pair/XOR 树归约，不能按 d 排序后换成库 sum。全局窗口和头仍由实例来源表决定；1080 上 655,360 个归约组（含 warp 内复制）0 不一致。[F04 核对](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)
- 数值规则：split16 的冻结融合[合同](APPENDIX_beginner_glossary.md#g101)明确选 pair 的第一平方融合，第二平方先发布 half；ViT 在“两个乘积节点的加法”处采用同一方向的融合重算。所有 half 加法与 RSQ 前后转换仍是独立边界。
- 为什么这么算：片内并行分解服务于矩阵输出排列；CPU 的循环组织可优化，浮点依赖与发布次序保留。
- 我们怎么知道：CENSUS，[scalar_map.hpp:257–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L257)、[qkv_projection_impl.hpp:165–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L165)。本轮分别展开 L27 与 L61 的全部 32 个 RSQ 输入依赖，每个都含 32 个不同的标量平方；具体绑定见[附录](APPENDIX_evidence_history.md#norm-bindings)。
- 往下：[各家族尺度](#affine)、[A1 的限定改动](#a1)；矩阵部分和及原语细节见 [L3.qmma-e4m3](L3_qmma_e4m3.md)、[L4.half-arith](L4_half_arith.md)。

【CPU 重建／CENSUS】[具体图/合同、源与 SHA 绑定](APPENDIX_evidence_history.md#norm-bindings)已迁移。split16 L27 的 RSQ 属于 Q/K，RCP 属于后续 attention [分母](APPENDIX_beginner_glossary.md#g048)；其余已读的 L25/26/28/29/30/56/57 原型图没有 RSQ/RCP 节点。旧 [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) 与具名实例放行的边界仍保留，图/源一致不升级为全几何通用地图证明。

<a id="affine"></a>
### L3.norm-nonfinite.affine RSQ、下界与尺度的实际格式

- 是什么：对已经是 half 的正统计量查原生 RSQ [位型](APPENDIX_beginner_glossary.md#g057)，再在明确位置转回 half、乘尺度、转 E4。
- 输入 → 输出：n 的 half 编码 → RSQ 表项的 F32 编码 → half r → 归一化出口。
- 怎么算：
  ~~~text
  1. n=max(s,half(0x0410))；检查当前包装接受域。
  2. F32(n) 精确展开，用 n 的编码选 RSQ 表项。
  3. r=RN16(表项的 F32 值)。
  4. 先 H×(x_i,r)，再依下表完成 Q 的尺度乘法；K 不乘查询尺度。
  5. 每个 H× 发布 half，最后 E4 发布；没有归一化后的 β 加法。
  ~~~
- 数值规则：已直接核对的 split16 L27/L31 站点使用 [MUFU](APPENDIX_beginner_glossary.md#g073) RSQ 的 F32 [FTZ](APPENDIX_beginner_glossary.md#g068) 包装；其他家族按各自绑定的 RSQ 半域表取已采位型，不凭函数名补认包装形态。有限非零 half 即使为次正规数，展开成 F32 也仍为正规数；不能因此把 half 次正规数统一冲零。这里下界还进一步把 RSQ 的有限输入限制到 ≥0x0410。
- 为什么这么算：源码把倒数平方根的数值合同固定在原表；通用 sqrt/division 的近似相等不构成逐位相等。
- 我们怎么知道：CENSUS / MEASURED，[half MUFU 语义:7–19](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/SEMANTICS_ZH.md#L7)、[原表边界 JSON](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/s11-old-table-boundary.json)；表示方式及[全域](APPENDIX_beginner_glossary.md#g111)测量范围见 [L4.mufu](L4_mufu.md#representation)。
- 往下：[各包装的 +Inf 接受域](#a1)、[实际例](#worked-example)。

| 家族 | Q 的逐次发布公式 | K / V 与尺度来源 |
|---|---|---|
| TIN | Q_i=Q8(H×(H×(x_i,r),γ_h)) | γ_h 按每头 F32 存在模型资源中，读入时 [RN16](APPENDIX_beginner_glossary.md#g059)；K 为 Q8(H×(x_i,r))，V 直接 E4。源码 [tin.cpp:34–51、114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34) |
| split16 | Q_i=Q8(H×(H×(x_i,r),γ_h)) | 四字节资源尺度经 F32→half；位置/头由 map 选择；K 无此尺度。字节读取与转换：[scalar_map.hpp:252、274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L252)，实际顺序在 L27 图 |
| ViT | Q_i=Q8(H×(H×(H×(x_i,r),5.65625),γ_h)) | 5.65625 是图中固定 half 常量；γ_h 为按头读取的 F32 资源尺度，先 RN16。K 只 Q8(H×(x_i,r))；V 经布局变换直接 E4，二者没有 Q 的额外因子 |
| B0 / B70 | Q_i=Q8(H×(H×(x_i,r),γ)) | 单头 F32 资源尺度先 RN16；K 只乘 r。来源：[b00.hpp:18、46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L18)、[outtail.cpp:85、90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L85) |

尺度数值不在本文列出。γ 的存储为 F32、参与乘法时为 half；QKV 的矩阵系数则是 E4，不能把矩阵系数格式当作归一化尺度格式。上游线性变换、[旁路](APPENDIX_beginner_glossary.md#g016)和后续 attention 偏置也不充当这里的 β。

5.65625=RN16(√32)，编码0x45a8；[真实half_round实算](examples/anatomy_r04i.result.json)核对该恒等式。理想无下界/无舍入时，[L2单位向量](APPENDIX_beginner_glossary.md#g053)乘√32得到RMS为1的尺度；这里该因子只乘Q，K仍按自己的公式，不是把两份统计量都改成均方。三个half乘法各自发布，不能合并成一个F32总尺度；选择这种查询尺度的训练意图未知。

<a id="nf-path"></a>
## 正数统计量上溢与接口拒绝

【CPU 重建】有限输入的half平方/正数求和可上溢至+Inf。ε下界不消除+Inf；原TIN表支持RSQ(+Inf)=[+0](APPENDIX_beginner_glossary.md#g070)，可将有限向量吸收为带符号零。Inf×0不在这个推理内，NaN及其他原语仍各自守卫。

<a id="a1"></a>
【验证记录】默认M2的split16/ViT有限域包装拒绝该统计量；独立A1分支放行限定RSQ(+Inf)=+0及具名统计路径，仍保留[QMMA](APPENDIX_beginner_glossary.md#g065) half overflow拒绝，未更新公开M2。027/028是诊断报告中的图像样本编号，不是层号；[传播见证、分支源码与验收计数](APPENDIX_evidence_history.md#norm-propagation-detail)移至附录。

【原生行为／未知】CPU见证不证明原生网络内部也产生相同临时Inf；各分支只约束其保存的比较对象和输入域。

<a id="evidence"></a>
## 证据与未知

【验证记录】独立 RSQ(+Inf)=+0 原值、CPU 局部传播、helper 阈值控制、A1 检查点和 [FINAL](APPENDIX_beginner_glossary.md#g105) 比较是不同层次，[具名文件/分母/计数](APPENDIX_evidence_history.md#norm-evidence)已迁移。A1 的 [C8](APPENDIX_beginner_glossary.md#g109) 六纹理仍 NOT_RUN_RAW_FILES_ABSENT；旧逐 launch 有限路径不能算 A1 新门或所有输入证明。

一般 half 多操作数组合、NaN 载荷规则、未观察区间非有限次数、[GPU](APPENDIX_beginner_glossary.md#g078) 网络中间 Inf/NaN 是否可达仍 UNKNOWN；“原生内部产生 +Inf 并被吸收”仍 INFERRED。已经测到独立函数键，不代表已测网络内部实际到达它。

<a id="worked-example"></a>
### L3.norm-nonfinite.example 直接执行仓库函数的一个 32 通道组

- 是什么：执行真实参考函数，而非只在正文里列一个理论平方和。
- 输入 → 输出：人工向量 [1,−2,3,−4,0,…,0]，共 32 项；人工尺度 γ=1；得到统计量、原生 RSQ 表项与归一化 half。
- 怎么算：附录脚本从文件 AST 只抽取 _norm_squared、_rsq、normalise 三个原函数；不导入模型或其余模块，不读取权重。
- 数值规则：本组平方与融合中间值可精确表示；RSQ 与 half 乘法按原函数执行。它验证本组数值，不声称覆盖所有 FMA 输入。
- 为什么这么算：同时分清实际统计量、已发布向量的长度偏差、全零下界，以及“表有 +Inf 项但包装拒绝”的差别。
- 我们怎么知道：原写作轮实际执行附录代码，源与 RSQ 资产均核 SHA；没有新增 GPU、整网或连续链运行。
- 往下：到底了；最终 E4 编码规则见 [L4.e4m3 / K32](L4_e4m3_and_k32.md#e4m3-format)。

从仓库根目录运行，代码只需标准库和 NumPy：

[完整脚本与认证 SHA](APPENDIX_evidence_history.md#norm-example)移至附录；下方保留原执行输出，原运行范围见证据附录。

实际输出：s=n=30，half 编码 0x4f80；RSQ 的 F32 编码为 0x3e3af4ba，RN16 后 r=0.1826171875，编码 0x31d8。前四个归一化 half：

| 人工 x_i | 归一化 half | half 编码 |
|---:|---:|---|
| 1 | 0.1826171875 | 0x31d8 |
| −2 | −0.365234375 | 0xb5d8 |
| 3 | 0.5478515625 | 0x3862 |
| −4 | −0.73046875 | 0xb9d8 |

把已发布 half 的平方在实数意义下相加，得到 1.0004711151123047；half 归一化没有保证最终长度精确为 1。全零组的统计量被截到 ε。人工的 32 个 48 则使本树在最终 H+(36864,36864) 上溢为 +Inf；未改的参考 _rsq 如实拒绝它，尽管资产最后一行的 +Inf→+0 原值已经存在。A1 的放行是上文指定的新分支，例子没有悄悄修改旧守卫。
