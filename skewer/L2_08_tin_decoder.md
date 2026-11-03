# L2.08 TIN 解码：upsample 与 outview

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_08_tin_decoder.md)

[TIN](APPENDIX_beginner_glossary.md#g011) 为[窗口](APPENDIX_beginner_glossary.md#g015)块[家族](APPENDIX_beginner_glossary.md#g080)，upsample 是[上采样](APPENDIX_beginner_glossary.md#g021)过渡块，[outview](APPENDIX_beginner_glossary.md#g022) 是输出[物理](APPENDIX_beginner_glossary.md#g085)视图；[E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054)、[K32](APPENDIX_beginner_glossary.md#g065)、[RN-even](APPENDIX_beginner_glossary.md#g059)、[seed](APPENDIX_beginner_glossary.md#g042)、[skip](APPENDIX_beginner_glossary.md#g016) 与 X_r(C) 见 [记号表](INDEX.md#形状与工作区记号)。表中逻辑形状默认E4，extent依实际[params](APPENDIX_beginner_glossary.md#g083)。上采样先作2C→C[投影](APPENDIX_beginner_glossary.md#g038)；窗口[FFN](APPENDIX_beginner_glossary.md#g037)的一头/多头[矩阵](APPENDIX_beginner_glossary.md#g051)分解见[L3.ffn](L3_ffn.md#channels)，已知矩阵宽度与尚未知的独立物理布局分开。

## 解码复用的 chained

本表只导航，覆盖仍唯一归属[编码](APPENDIX_beginner_glossary.md#g009)侧共享家族。

| 本阶段调用 | 共享正文 |
|---|---|
| L134–L139 | [8h / 256 通道](L2_03_tin_encoder.md#chain-256) |
| L142–L145 | [4h / 128 通道](L2_03_tin_encoder.md#chain-128) |
| L148–L149 | [2h / 64 通道](L2_03_tin_encoder.md#chain-64) |
| L152–L153 | [1h / 32 通道](L2_03_tin_encoder.md#chain-32) |

## 两个家族的共享计算

- **upsample 是什么／输入→输出／怎么算：** 按前档 outview 解码主路并投影至目标[通道](APPENDIX_beginner_glossary.md#g007)；目标坐标取前档 floor(x/2),floor(y/2)，作最近邻两倍展开；按 [HF](APPENDIX_beginner_glossary.md#g063)([D8](APPENDIX_beginner_glossary.md#g061)(skip),s_skip,projected_main) 合并，即投影主路加[缩放](APPENDIX_beginner_glossary.md#g031)的本档编码 [full](APPENDIX_beginner_glossary.md#g018) skip；按本档 seed 规则执行首窗口块，只写声明有效范围并[发布](APPENDIX_beginner_glossary.md#g091)控制字。窗口原点只移动分窗网格，不移动最近邻源坐标。
- **outview 是什么／输入→输出／怎么算：** 读取本档内部[特征](APPENDIX_beginner_glossary.md#g008)、[权重](APPENDIX_beginner_glossary.md#g079)和窗口原点，8×8 分窗、越界补零；执行前馈、[归一化](APPENDIX_beginner_glossary.md#g043)、[注意力](APPENDIX_beginner_glossary.md#g039)与[残差](APPENDIX_beginner_glossary.md#g017)投影；在原量化点写同形 E4 视图并完成末端交接。它包含完整窗口计算，不能当成纯复制，也没有额外 pool。
- **数值规则：** 逐 K32 发布 F16；half 融合舍入及 E4 RN-even 点保持。多头先量化合并值再解码作前馈 seed，尾 seed 也取量化再解码的前馈结果；一头upsample保留未量化合并值作前馈seed；一头各块尾投影保留未量化前馈值。出口布局[重排](APPENDIX_beginner_glossary.md#g019)不再舍入。函数域/[非有限](APPENDIX_beginner_glossary.md#g069)及 QMMA [overflow](APPENDIX_beginner_glossary.md#g071) 守卫见 [非有限合同](L3_norm_nonfinite.md#norm-nonfinite)。
- **为什么：** upsample 接回本档编码旁路并恢复主路空间密度；outview 把本档结果交给下一档的读取布局，最细档交给 B70。训练/融合设计动机未知；不重复用通用理由解释每个尺度。

## 变体表

| 家族／入口 | launches / B | 逻辑形状 | 残差来源 | seed 量化 | layout | 真正差异 |
|---|---|---|---|---|---|---|
| <a id="up-256"></a>upsample 8h/256 | L133 / B48 | X₅(512) + X₄(256) skip→X₄(256) | B22/L24.full，随后本窗输入/前馈 | 合并值与尾前馈值均 E4 量化再解码 | 前档 outview→本档内部 | 首窗原点 (0,0)；权重/skip/有效范围逐配置[绑定](APPENDIX_beginner_glossary.md#g103)；1440 有效高92、窗口画布可96，仅写有效输出；只发布不等待 |
| <a id="out-256"></a>outview 8h/256 | L140 / B55 | X₄(256)→同形 | 当前窗输入与前馈结果 | 尾 seed E4 量化再解码 | 16 通道/平面，每空间位置每平面16 B，通道置换按配置 | 后继上采样读取，不额外池化 |
| <a id="up-128"></a>upsample 4h/128 | L141 / B56 | X₄(256) + X₃(128) skip→X₃(128) | B14/L16.full，随后本窗输入/前馈 | 合并值与尾前馈值均 E4 量化再解码 | 前档 outview→本档内部 | 首窗原点 (−4,0)；权重/skip/有效范围逐配置绑定 |
| <a id="out-128"></a>outview 4h/128 | L146 / B61 | X₃(128)→同形 | 当前窗输入与前馈结果 | 尾 seed E4 量化再解码 | 16 通道/平面，每空间位置每平面16 B，通道置换按配置 | 后继上采样读取，不额外池化 |
| <a id="up-64"></a>upsample 2h/64 | L147 / B62 | X₃(128) + X₂(64) skip→X₂(64) | B8/L10.full，随后本窗输入/前馈 | 合并值与尾前馈值均 E4 量化再解码 | 前档 outview→本档内部 | 首窗原点 (0,0)；权重/skip/有效范围逐配置绑定 |
| <a id="out-64"></a>outview 2h/64 | L150 / B65 | X₂(64)→同形 | 当前窗输入与前馈结果 | 尾 seed E4 量化再解码 | 16 通道/平面，每空间位置每平面16 B，通道置换按配置 | 后继上采样读取，不额外池化 |
| <a id="up-32"></a>upsample 1h/32 | L151 / B66 | X₂(64) + X₁(32) skip→X₁(32) | B4/L6.full，随后本窗输入/前馈 | 合并值与尾前馈值均未量化保留 | 前档 outview→本档内部 | 首窗原点 (0,0)；权重/skip/有效范围逐配置绑定 |
| <a id="out-32"></a>outview 1h/32 | L154 / B69 | X₁(32)→同形 | 当前窗输入与前馈结果 | 尾 seed 未量化 | [M2](APPENDIX_beginner_glossary.md#g107) 按 [outputlayout](APPENDIX_beginner_glossary.md#g088) 配置；原生独立核验 [UNKNOWN](APPENDIX_beginner_glossary.md#g104) | 后继 B70 按半分辨率坐标复用；不因共享执行器升级布局结论 |

每次均按当前配置绑定权重、残差地址、窗口原点、源物理宽高、输出布局与有效范围，不从小尺寸正方形样本推广。多头 outview 的平面布局不自动构成 B69 的独立证据。

**保留未知：** [computed-shared](APPENDIX_beginner_glossary.md#g108) 指计算得到的共享中间值之写→读来源证明（[术语](INDEX.md#项目与验证术语)），不是额外网络层。 L133 computed-shared 的符号来源层仍 NOT_ADMITTED；数值链通过不解除该状态。B69 原生独立布局仍 UNKNOWN（ARCH §4.4），最小关闭条件是：独立确定原生L154输出字节的逻辑位置/通道标签，逐项对照当前outputlayout，再核对L155按半分辨率取数的来源；两份映射一致且通过身份、范围及反例控制后方可关闭。当前没有该见证，不能只由相同CPU执行器推导。

- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（家族/布局/接线）、MEASURED（具名合并与出口）；[ARCH §4.5、§4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66)、[outview §4.4](../../../ARCHITECTURE_V3_ZH.md#44-outview-核b55--b61--b65同属-tinlayout_fused_-家族但输出不是-tin-布局)。
- 往下：[L3.tin-window：完整块交接](L3_tin_window.md#tin-window)、[已写窗口 attention](L3_attention_softmax.md#window-attention)、[half 融合舍入](L4_half_arith.md#half-arith)、[写集与布局](L3_workspace_map.md#write-sets)。

<!-- coverage: {"launches":[133],"kernels":["cc_tinlayout_fused_swin_8h_256_8_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[140],"kernels":["cc_tinlayout_fused_swin_8h_256_8_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[141],"kernels":["cc_tinlayout_fused_swin_4h_128_4_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[146],"kernels":["cc_tinlayout_fused_swin_4h_128_4_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[147],"kernels":["cc_tinlayout_fused_swin_2h_64_2_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[150],"kernels":["cc_tinlayout_fused_swin_2h_64_2_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[151],"kernels":["cc_tinlayout_fused_swin_1h_32_1_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[154],"kernels":["cc_tinlayout_fused_swin_1h_32_1_outview_wait_fp8"]} -->
