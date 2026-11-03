# L4.mufu：特殊函数的实测位型与 CPU 表示

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · 上层：[B0 噪声](L2_02_b0.md#noise)、[ViT 归一化](L2_05_vit.md#qkv)、[ViT 注意力](L2_05_vit.md#attention)、[B70](L2_09_b70.md)、[最终显示](L2_10_output.md) · [half 发布](L4_half_arith.md#f32-boundaries)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| T_f、Domain_f | 函数f的认证[位型](APPENDIX_beginner_glossary.md#g057)映射、当前包装接受域 |
| b,s,e,m | [F32](APPENDIX_beginner_glossary.md#g056)输入[编码](APPENDIX_beginner_glossary.md#g057)、符号、存储[指数](APPENDIX_beginner_glossary.md#g058)、尾数域 |
| h₀、h | [half](APPENDIX_beginner_glossary.md#g054)小表起始编码、查询编码 |
| k、[Radius](APPENDIX_beginner_glossary.md#g073)(k) | 噪声整数键、预组合认证半径 |

<a id="mufu"></a>
### L4.mufu 一次调用不是求一个近似数学值

- 是什么：把输入位型经指定包装映射到已测输出位型；CPU 可以读原值、无损解码或执行已验收的位型变换。
- 输入 → 输出：raw32、half 编码或噪声 k → raw32/half，或域外拒绝。不同包装的输入类型和接受域不合并。
- 怎么算：
  ~~~text
  1. 确定函数、包装版本、输入格式、舍入/FTZ 和表身份。
  2. 检查当前接口的域成员，不能只检查“数值有限”。
  3. 原值表按 raw32 索引；紧凑表先重建原始整数位型。
  4. 只有已验收的缩放/修正分支可由代码计算；失败段读认证原值或拒绝。
  5. 按调用图在明确节点转回 half，再交后续运算。
  ~~~
- 数值规则：目标是 $T_f(b)$ 的编码，不是数学函数的正确舍入近似；一般[调用](APPENDIX_beginner_glossary.md#g080)只声称在 $Domain_f$ 上匹配。已采[全域](APPENDIX_beginner_glossary.md#g111)、已验压缩和网络所有站点已[绑定](APPENDIX_beginner_glossary.md#g103)是不同事实。
- 为什么这么算：保存测量包含 [libm](APPENDIX_beginner_glossary.md#g074) 和朴素约简不能重现的位型；不能从这些观察推导 [GPU](APPENDIX_beginner_glossary.md#g078) 内部唯一实现。
- 我们怎么知道：[V2-02-006](../../arch-v2/02.03_mufu.md#v2-02-006) 为范围入口；下文分别引用当前公开代码、原测量和软件表示验收。
- 往下：本主题已到底；[变体与调用者](#variants)、[表与编码](#representation)、[测量范围](#evidence)、[边缘语义](#edges)、[可运行例](#worked-examples)。

<a id="variants"></a>
## 七个函数族分别在哪里用

下表的 L3 名称是 [INDEX 中的算子步骤入口](INDEX.md)。数学名称只提示用途，不定义逐位结果。

| 函数 | L2 家族 → L3 步骤 | CPU 路径和源码 path:line |
|---|---|---|
| rsq | L2.02 B0、L2.03/08 [TIN](APPENDIX_beginner_glossary.md#g011)、L2.04/07 [split16](APPENDIX_beginner_glossary.md#g013) 的[归一化](APPENDIX_beginner_glossary.md#g043)步骤、L2.05.qkv、L2.09 B70 → L3.tin-norm 的查询/键范数倒数平方根 | half 小表或 F32 表值后转 half：[GlassBox-NR/cpp/chain_entry_optm/b00.hpp:25、46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L46)、[tin.cpp:114–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)、[scalar_map.hpp:272–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272)、[qkv_projection_impl.hpp:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192)、[outtail.cpp:58、90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L90) |
| rcp | B0/TIN/split16 [窗口](APPENDIX_beginner_glossary.md#g015)与 [ViT](APPENDIX_beginner_glossary.md#g014) [attention](APPENDIX_beginner_glossary.md#g039) → L3.attention-[softmax](APPENDIX_beginner_glossary.md#g047) 的[分母](APPENDIX_beginner_glossary.md#g048)归一化；B70 → L3.temporal-sampling；L157 → L3.postprocess 的颜色辅助倒数 | half/F32 表及尾部尾数表[缩放](APPENDIX_beginner_glossary.md#g031)：[b00.hpp:49](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L49)、[tin.cpp:124–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L124)、[scalar_map.hpp:272](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272)、[attention_impl.hpp:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212)、[b70_temporal.hpp:27–49](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L27)、[outtail.cpp:53、73](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53) |
| ex2 | 非 [reset](APPENDIX_beginner_glossary.md#g032) B70 → L3.output-temporal 的置信混合；L157 → L3.postprocess 的颜色变换 | 尾数基表、指数位变换、失败段原值及限定输入稀疏表：[b70_temporal.hpp:45–46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L45)、[outtail.cpp:55–57、71–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55)、[stage_codec.inc:70–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L70) |
| lg2 | B0 → L3.noise 的半径链；L157 → L3.postprocess 的颜色变换 | B0 的运行路径已预组合进半径表；L157 用 [E1](APPENDIX_beginner_glossary.md#g110) 解码/原值回退：[noise_online_optd.hpp:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L23)、[lg2_decoder.hpp:17–35](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/lg2_decoder.hpp#L17)、[outtail.cpp:54、74–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L54) |
| sqrt | B0 → L3.noise 的两路半径 | sqrt_k_exact.dnc 按 k 保存完整预组合半径，运行时不调用通用 sqrt：[noise_exports_optd.inc:16](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L16)、[noise_online_optd.hpp:26](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L26) |
| sin / cos | B0 → L3.noise 的三个角度因子 | 两份按 k 无损编码的实测组合表：[noise_exports_optd.inc:17–18](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L17)、[noise_online_optd.hpp:27–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L27) |

不能因“attention scores”这个名称就给注意力插入 ex2：公开 B0/TIN 的分数路是 F32 [仿射](APPENDIX_beginner_glossary.md#g049)、half clamp 与编码变换，再按有序分母使用 rcp，[tin.cpp:108–109、122–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108)。原生清单补全为七族见 [09-12 探针 RESULT:15–22、57–80](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L15)；[矩阵](APPENDIX_beginner_glossary.md#g051)辅助[张量](APPENDIX_beginner_glossary.md#g076)名字中的 sin/cos 也不代表调用三角函数，该报告另核对了其消费者。

<a id="representation"></a>
## 全域映射、尾数小表和接受域

【CPU 重建】完整 raw32 映射可以按块保存，不要求全表常驻；只读已注册且认证的成员，未注册返回缺成员。注册时核实际读取的SHA，缓存未命中、换入映射时核fd身份并拒绝所检测的变化；缓存命中复用已映射页，不保证逐查询重新检测外部文件变化。检查顺序见[full_raw_registry.hpp:28–39、53–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L28)，分块、两槽映射容量与读取布局见 [CPU 存储附录](APPENDIX_cpu_storage.md#raw-registry)；存储容量不证明一般网络可达性。

小表也保留身份：Python Sm120Tables 读实测 native_half_bits、校验 SHA、设为只读，缺表没有数学公式回退，[mlxdlss/sm120_b1.py:155–196](../../../mlxdlss/sm120_b1.py#L155)。half 路的基本公式为 $T(h-h_0)$，但必须先核对具体端点范围；ViT 先精确转 F32 查表，在显式节点 RN 到 half，[qkv_projection_impl.hpp:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192)、[attention_impl.hpp:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212)。[RCP](APPENDIX_beginner_glossary.md#g072)/RSQ 的数学倒数和平方根不在此处重新求值。

### rcp：实测尾数 + 整数指数调整

对[正规](APPENDIX_beginner_glossary.md#g068) F32 输入，取输入尾数 m 查 $r=T_{\mathrm{rcp},e=127}[m]$，把其输出存储指数减去 e−127，保留实测尾数和输入符号；调整后指数≤0 时[发布](APPENDIX_beginner_glossary.md#g091)[有符号零](APPENDIX_beginner_glossary.md#g070)，≥255 时发布有符号 [Inf](APPENDIX_beginner_glossary.md#g069)。零/次正规与非有限输入走独立认证原值分支。[outtail.cpp:53](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)。

这里的精确是“相对于已测 r 与已验收包装的位型变换”，并非宣称 r 等于正确舍入的 $1/x$。历史约简也曾因输出未冲零而失败，补齐输出 FTZ 后才在正常输入块成立，[探针 RESULT:271–285](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L271)。

### lg2 / ex2：认证基表上的位级重建

这里操作的是已测输出位型；base、raw126、level均须认证，结果不是数学库的正确舍入近似。

~~~text
LG2：正号输入的指数E=127直接读base[m]，E=126直接读raw126[m]。
E=111..125时，v=RZ32(base[m]−(127−E))；先用整数对齐有效数，再截掉24位有效数以外的低位。
每尾数取3-bit level；E分组111..118/119..122/123..124/125对应group=0/1/2/3。
输出位型=bits32(v)−[level≤group]；范围外只读已认证原值成员或拒绝。
EX2正参数：n=floor(x)，j=floor((x−n)×2^23)，delta=n−1；j夹到0..2^23−1。
EX2负正规参数：从有效数/指数形成v=trunc(|x|×2^23)，n=v>>23，t=v&(2^23−1)。
t=0时j=0、delta=−n−1；否则j=2^23−1−t、delta=−n−2。
predicted=base_EX2[j]+delta×2^23；先查输入成员，再查32-bit输出范围。
只有已验收codec分支返回predicted；指定失败段改读认证原值。
零、FTZ与非有限值沿具体包装分支；不以外推公式替代缺成员/NaN拒绝。
~~~

实际位运算见[LG2 decoder](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/lg2_decoder.hpp#L17)与[EX2包装](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55)；基表容量、原值例外及旧验收留在[CPU存储账](APPENDIX_cpu_storage.md#mufu-ex2-codec)。

### 函数行为、组合半径与接受边界

<a id="value-wrapper"></a>
为把位型查询接到浮点乘法，先区分原始位型映射 $T_f$ 与数值包装 $\widehat{T}_f$：

```math
\widehat{T}_f(x)=\mathrm{value}_{32}\!\left(T_f(\mathrm{bits}_{32}(x))\right).
```

$\mathrm{bits}_{32}$ 取一个 F32 的原始编码，$\mathrm{value}_{32}$ 将编码解释回 F32 值；两者只转换表示，不增加舍入，并保留零的符号。$c_{\ln2}$ 是 F32 编码 `0x3f317218` 表示的算法常数，见 [B0 噪声常数](L3_b0_input.md#noise)。下式的 Radius(k) 表示解码后的 F32 半径值；资产保存的是它的原始编码。

B0 组合半径仍是
```math
Radius(k)=\widehat{T}_{\mathrm{sqrt}}\!\left(\mathrm{RN}_{32}\left(\mathrm{RN}_{32}(\widehat{T}_{\mathrm{lg2}}(k2^{-24})c_{\ln2})\cdot(-2)\right)\right),\qquad 1\le k\le2^{24}.
```
不是 sqrt(k·2⁻²⁴)。冻结域的这两次乘法没有非零 F32 次正规，原 FTZ 不改变这些非零值；不外推到任意 sqrt 输入。sin/cos 表已包含角度预缩放/[向零](APPENDIX_beginner_glossary.md#g060)归约，在线不得再归约；两次半径/三次三角查询后，三次 F32 乘法才 RN 到 half，u=1 的半径保留 −0。

成员认证、表域与调用域须同时满足；跨[通道](APPENDIX_beginner_glossary.md#g007)颜色分支不因单half站点已验而扩域。零/次正规及非有限处理仍按 [具体包装](#edges)，存储裁剪见 [附录](APPENDIX_cpu_storage.md#mufu-domain-storage)。

<a id="s157-reach-r2c"></a>
## 调用站点与函数成员

每个S157站点先核对控制元组及输入位型属于已认证成员，再查实测表或译码；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。认证表的覆盖范围与调用者可达域分别约束入口，不能由单half域推导跨通道颜色全域。

<a id="evidence"></a>
<a id="lookup-contract-r04l"></a>
## 逐家族查表合同（排名7起的函数规格项）

下列步骤全部为 **TABLE_DRIVEN_DESCRIBED**。表身份、索引与包装已写全，不把原值函数改判为[闭式](APPENDIX_beginner_glossary.md#g020)。

| 消费者 | 函数输入端点与输出包装 | 表身份与索引 |
|---|---|---|
| B0 | RSQ：half编码闭区间[0x0410,0x7c00]；RCP：分母闭区间[0x1c00,0x60e0] | 原[NPZ](APPENDIX_beginner_glossary.md#g097)的 `native_half_bits[h-0x0410]`，直接返回half；RSQ长30705，RCP长30704 |
| TIN，含输入/上[下采样](APPENDIX_beginner_glossary.md#g021)/出口变体 | 共用lookup要求0x0410≤h≤0x7c00且索引小于实装长度；RSQ可取+Inf端点；RCP调用前还检查[0x1c00,0x60e0] | `rsq.u16` / `rcp.u16` 按LE16读，直接half；长度分别30705/30704，后者不能读+Inf索引 |
| split16 | 0x0410≤h<0x7c00；类别无效依赖在查询时用0x3c00占位，不能令无效值进入矩阵 | 原NPZ的 `native_float_bits[:30704]`，索引h−0x0410，返回raw32；仅在[DAG](APPENDIX_beginner_glossary.md#g089)显式rne16节点[RN16](APPENDIX_beginner_glossary.md#g059) |
| ViT QKV | F32必须精确等于转换回来的half，0x0410≤h<0x7c00，索引不得越界 | 同一RSQ raw32表；后续f16of节点RN16，非有限发布拒绝 |
| ViT attention | 同上检查half可表示性和开右端点 | 同一RCP raw32表；后续显式f16of RN16，乘常量节点还拒绝非零F32次正规 |
| B70 | RSQ闭区间[0x0410,0x7c00]，raw32表长30705，返回RN16；分母RCP为raw32函数 | RSQ索引h−0x0410；RCP按尾数表/认证原值分支，不能套用TIN分母域 |

源NPZ身份：`rsq-domain.npz` SHA-256 `06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62`；`rcp-domain.npz` SHA-256 `055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59`。TIN导出LE16表分别为 `73f5c18f6c853ce7ba071d2dca44afe4441606a046fd0d73386596b4474af874`、`0f7803de239ba07f109bead85e726cf414af35101a9d41ba58cc5c4a17a6ecfc`；这些是不同表示的身份，不可互换。[原绑定](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/s00-bindings.json)，[入口认证与字段选择:15–40](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/entry_assets.py#L15)，[TIN绑定认证:99–105](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/backend_abi.py#L99)。

端点代码：[B0:46、49、62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L46)，[TIN lookup:87](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L87)及[分母:126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L126)，[split16:272–274、322](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272)，[QKV:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192)，[attention:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212)，[B70:53–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)。TIN lookup本身只检查下界和实装长度，表中上界由具名表长度给出，不是额外硬编码守卫。0x7c00是正Inf输入端点；NaN、负编码不在这些具名表域。特殊输入不得绕过调用者的非有限守卫。

<a id="tail-dispatch-r04l"></a>
### 尾部的稀疏、codec与原值选择（排名84–86、218–222、225）

精确调度顺序为：L155 EX2先按无符号raw32键二分查 `ex2_sparse`，命中直接读raw32；未命中要求L155 temporal_tables或L157且基表长2^23。e=0返回1（含正负次正规），+Inf返回+Inf，−Inf返回+0；其余才进上文EX2译码。正数要求e≤133且expos[bits>>23]；负数要求exneg、认证codec块或原值块之一准入，指数移位<40，预测整数必须在[0,2^32−1]。负数不属于exneg但有原值成员时，原值优先于预测；缺成员及NaN不能凭预测强行接受。[outtail.cpp:55–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55)。

LG2只在L157装载：E127基表和E126原值各2^23个LE32，3-bit level表3145728 B；指数块111..127，其他正有限正规输入只有原值成员可回退。e=0先返回−Inf；负正规、Inf/NaN拒绝。RCP要求2^23项尾数表，e=0查认证正零块后并入符号，e=255查完整raw32成员，其他指数使用上文整数缩放。[outtail.cpp:53–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)。

身份合同为 `(stage,函数,表示,字节长,SHA-256,成员集合)`：尾部descriptor用manifest中sources的extracted_sha256与bytes认证RCP/RSQ/EX2；E1 manifest自身SHA固定为 `4255d067e6a618342182a86f44fbf2feceb92a7d148e0dcdfaabe304f8c72138`，little endian，三成员的字节长和SHA逐项继承其files字段。全raw registry的块成员须按[认证读取规则](#representation)装载。禁止用相同文件名替代身份核验。[tail_runtime.py:14–40](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/tail_runtime.py#L14)。L157四站点还先检查reach，再调用这些相同backing函数；函数接受域不等于RGB联合支路可达域，后者仍[UNKNOWN](APPENDIX_beginner_glossary.md#g104)。

| 尾部具名导出表示 | 字节长 | SHA-256 |
|---|---:|---|
| RCP E127 raw32基表 | 33554432 | c408381446132e07fa5581e930dc33fb790bea7ec4276ef3621e322df2492a55 |
| EX2 block127 raw32基表 | 33554432 | cce5df10202dbfcde720ca547d147edb3e2a406a5fed189323f419177a72a1a5 |
| B70 RSQ raw32半域表 | 122820 | 5f50d80e6793405891045b4c8f747b46bc86551dee11b7d2cbef84f154088107 |

身份来自[既有尾部manifest](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/dlssnr-biggeom/r01-20261006-codex/assets-chain/mirror/E/dlssnr-cpp-work/chain-outtail-r01-codex/tables/manifest.json)。实际加载先核字节数、整除元素宽度、读满与实际读取SHA；不在本轮重新生成这些表。[stage_codec.inc:30–56](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L30)。L155 temporal还要求非空184 B参数profile集合；稀疏输入/输出均为认证LE32数组，等长且1..65536项，输入有限、按无符号键排序并拒绝重复，输出按对应raw32读取。L156不装函数表；L157不装RSQ/half[量化](APPENDIX_beginner_glossary.md#g061)表。加载失败清空所有表及raw registry，不能沿用上一阶段缓存。[stage_codec.inc:58–87](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L58)。

<a id="noise-spec-r04l"></a>
### 噪声表的组合输入（排名72–73）

`NoiseAssets` 的显式输入是三个认证DNOISE01成员 Radius/Cos/Sin，不是三个libm函数。四键各在[1,2^24]，依次取 `r0=Radius(k0),r1=Radius(k1)` 和 `c3=Cos(k3),s3=Sin(k3),c2=Cos(k2)`；三个结果为 `RN32(r1*c3), RN32(r1*s3), RN32(r0*c2)`，随后调用者逐项RN16。Radius含预组合LG2/乘法/SQRT，Cos/Sin含角度变换；在线不再做这些变换。块解码、原值SHA和末项−0沿用[现有自足例](APPENDIX_cpu_storage.md#mufu-example)，非法k拒绝。[noise_online_optd.hpp:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L23)。本轮补的是精确数据合同，两个审计行仍为TABLE。

## 观测域与调用域

【验证记录】保存的七族 FTZ/非 FTZ 探针、跨架构摘要、十月原值 bank 与生产成员组合核对分别列于 [完整测量账](APPENDIX_evidence_history.md#mufu-evidence)。全域原值采集、软件 codec 接受域一致和网络调用者全域绑定是不同断言；不能把两次设备/驱动收据合成一次测量。

固定包装的保存摘要相同不证明加载机器码相同；两项旧形状未覆盖，不推广到未来驱动或未测包装。SIN/COS 的成员组合含预缩放，不是每子步骤独立全域证明；域外无输出。扩域候选保留原有效性，LG2/EX2 仅接受域匹配，失败段回退原值，不能写成所有公式全 raw32 通过。旧 NOT_RUN、跨通道域未闭合及逐调用者绑定条件继续有效。

<a id="edges"></a>
## ±0、次正规、Inf/NaN 与 FTZ

以下是保存的 **FTZ 探针包装**，不是 CPU 每个接口的接受承诺；数据来自 [edge-cases.json](../../../experiments/parity-mufu-probe-20260912/edge-cases.json) 的完整特殊指数块分类。

| 函数 | +0 / −0 | 同号次正规输入 | +Inf / −Inf | NaN |
|---|---|---|---|---|
| rcp | +Inf / −Inf | 当作对应零；大正规数的微小输出也可冲成有符号零 | +0 / −0 | 规范为 0x7fffffff |
| rsq | +Inf / −Inf | 当作对应零；负正规数输出 NaN | +0 / NaN | 同上 |
| sqrt | +0 / −0 | 当作对应零；负正规数输出 NaN | +Inf / NaN | 同上 |
| lg2 | −Inf / −Inf | 当作对应零；负正规数输出 NaN | +Inf / NaN | 同上 |
| ex2 | 1 / 1 | 当作对应零，输出 1 | +Inf / +0 | 同上 |

公开尾部包装也显式编码部分边界：lg2 的 e=0 返回 −Inf，但负正规数、Inf/NaN 等未准入输入拒绝；ex2 对 e=0 返回 1，对 ±Inf 分别返回 Inf/0，NaN 与越界有限数仍可能拒绝；rcp 的非有限结果来自认证原值。[outtail.cpp:53–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)。**“表里测到 NaN”不等于“网络调用者允许 NaN 传播”。**

half 次正规转 F32 后仍是 F32 正规数，不能因为包装有 FTZ 就一律清掉 half 次正规。half 小表常见接受域是 $h_0\le h<0x7c00$，[sm120_b1.py:374–378、415–420](../../../mlxdlss/sm120_b1.py#L374)。部分当前 C++ 包装允许0x7c00端点，[outtail.cpp:58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L58)；r04l核对上述源NPZ身份、字段长度与RSQ末项：RSQ的30705项含该输入，输出half为+0；RCP仅30704项，不含该输入。各消费者实际能否使用仍由[逐家族合同](#lookup-contract-r04l)决定。

sin/cos 的生产成员绑定针对有限归约前角度；紧凑在线接口接收合法 k，范围外即拒绝，[compact_noise_optd.hpp:79–80](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L79)。它不提供任意 NaN/Inf 三角输入的生产合同，不能凭数学恒等式补齐。半径链在 u=1 时会保留 −0，文末读取的末项验证了这一点；三路最终 F32 乘法后才转 half，[噪声证明 RESULT:9–11](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L9)。

## 为什么不能改用libm

最小正正规输入的LG2保存结果不是数学整数−126；朴素的指数缩放及三角对称约简也存在位差。函数包装须保留认证原值、修正与接受域，而不能只给宽松误差界。[具体反例、原登记与测量范围](APPENDIX_evidence_history.md#mufu-counterexample-identifiers)集中在附录。

<a id="worked-examples"></a>
## 实际读取紧凑表：k=43 到 F32/half

【验证记录】人工合法键 k=43 查询到预组合半径 raw32=0x40a260c8，F32 约 5.07431411743，RN16 为 0x4513；它不是直接 sqrt(43·2⁻²⁴)。末项 k=2²⁴ 的半径为 −0（raw32=0x80000000，half=0x8000），零符号保留。

同一原实算例还读出最小正正规输入的 LG2=0xc2fbffff，而 libm 转 F32 为 0xc2fc0000；不能用数学库替代测量表。[完整脚本与认证 SHA](APPENDIX_cpu_storage.md#mufu-example)、[解码中间整数与原 stdout](APPENDIX_cpu_storage.md#mufu-example-output)在附录。原运行范围见证据附录。

这核对了选定表项、解码转写、half 发布及一个 libm 反例，没有重新验全部压缩项或全 raw32 数据。
