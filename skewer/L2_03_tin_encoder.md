# L2.03 TIN 编码与共享 chained 家族

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_03_tin_encoder.md)

[权重组织、dtype与阶段字节账](L2_weights_layout.md)

[TIN](APPENDIX_beginner_glossary.md#g011) 是本串的[窗口](APPENDIX_beginner_glossary.md#g015)块[家族](APPENDIX_beginner_glossary.md#g080)；[inpview](APPENDIX_beginner_glossary.md#g022)、chained、ds_wait 分别为输入视图块、同档连续块、[下采样](APPENDIX_beginner_glossary.md#g021)末块。[E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054)、[K32](APPENDIX_beginner_glossary.md#g065)、[RN-even](APPENDIX_beginner_glossary.md#g059)、[full](APPENDIX_beginner_glossary.md#g018)/pool、[seed](APPENDIX_beginner_glossary.md#g042) 与 X_r(C) 见 [记号表](INDEX.md#形状与工作区记号)；本页空间形状沿用该表，[FFN](APPENDIX_beginner_glossary.md#g037) 的 [M×K×N](APPENDIX_beginner_glossary.md#g051) 与一头/多头分解见 [L3.ffn](L3_ffn.md#channels)，不由执行索引轴反推其他窗口子层。

## 三个家族的共享计算

- **inpview 是什么／输入→输出／怎么算：** 将上一档[分平面](APPENDIX_beginner_glossary.md#g088) pool 解到本档[逻辑](APPENDIX_beginner_glossary.md#g085)位置；按实际窗口位移取 8×8 窗口、越界 [token](APPENDIX_beginner_glossary.md#g041) 补零；执行前馈、Q/K [归一化](APPENDIX_beginner_glossary.md#g043)、窗口[注意力](APPENDIX_beginner_glossary.md#g039)与[残差](APPENDIX_beginner_glossary.md#g017)[投影](APPENDIX_beginner_glossary.md#g038)；[量化](APPENDIX_beginner_glossary.md#g061)后按内部布局写出并[发布](APPENDIX_beginner_glossary.md#g091)完成标记。输入输出同档同[通道](APPENDIX_beginner_glossary.md#g007)。
- **chained 是什么／输入→输出／怎么算：** 从本档内部布局取当前块输入；按当前原点分窗并补零；执行同档前馈与窗口注意力，分别保留本窗输入/前馈残差；按原量化点回写和发布。[编码](APPENDIX_beginner_glossary.md#g009)与解码共用家族，不共用数值、[权重](APPENDIX_beginner_glossary.md#g079)或残差。
- **ds_wait 是什么／输入→输出／怎么算：** 先执行本档末窗口块；未量化结果分别送两条路径：直接量化成 full 留作解码 [skip](APPENDIX_beginner_glossary.md#g016)；另对 2×2 half 按固定两行顺序求平均，平[均值](APPENDIX_beginner_glossary.md#g044)先量化，再投影到两倍通道并写下一档 pool。按实例完成补齐写和控制交接，不能从已量化 full 解码重算池化。
- **数值规则：** 输入/矩阵权重为 E4，每 K32 发布 F16；half RN-even、E4 饱和量化、融合和残差发布次序不变，补零位置仍参与注意力。残差来源与量化差异按共享核心及下表列明，half[尺度](APPENDIX_beginner_glossary.md#g031)乘法见 [完整TIN块](L3_tin_window.md#tin-window)。L6 CPU norm 正数求和可到 [Inf](APPENDIX_beginner_glossary.md#g069)，有限输入不保证内部有限；函数域和 QMMA [overflow](APPENDIX_beginner_glossary.md#g071) 拒绝按 [非有限合同](L3_norm_nonfinite.md#nf-path)保留。
- **为什么：** inpview 负责接入前档物理视图；chained 在同尺度内处理位置关系；ds_wait 同时交出细尺度旁路和较小的主路。训练动机、窗口排程选择及融合边界的硬件成因未建立；不由核名补因果。

## 变体表（输入、输出默认 E4；每行是独立覆盖入口）

| 家族／入口 | launches / B | 逻辑形状 | 残差来源 | seed 量化 | layout | 真正差异 |
|---|---|---|---|---|---|---|
| <a id="inp-32"></a>inp 1h/32 | L3 / B1 | X₁(32)→同形 | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取未量化前馈z | 分平面→本档内部 | 1 头/32 通道；本档首块，单例 |
| <a id="chain-32"></a>chain 1h/32 | L4,L5,L152,L153 / B2/B3/B67/B68 | X₁(32)→同形 | 当前窗输入与前馈结果 | 尾投影取未量化前馈结果 | 本档内部→内部 | 1 头/32 通道；编码/解码共用，窗口原点逐实例[绑定](APPENDIX_beginner_glossary.md#g103) |
| <a id="ds-32"></a>ds 1h/32 | L6 / B4 | X₁(32)→full X₁(32) + pool X₂(64) | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取未量化前馈z | 独立 full / pool [角色](APPENDIX_beginner_glossary.md#g084)；按本次配置 | 1 头/32 通道；full 交解码；主路降采样；L6 CPU norm 溢出边界保留 |
| <a id="inp-64"></a>inp 2h/64 | L7 / B5 | X₂(64)→同形 | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 分平面→本档内部 | 2 头/64 通道；本档首块，单例 |
| <a id="chain-64"></a>chain 2h/64 | L8,L9,L148,L149 / B6/B7/B63/B64 | X₂(64)→同形 | 当前窗输入与前馈结果 | 尾投影取 E4 量化再解码的前馈结果 | 本档内部→内部 | 2 头/64 通道；编码/解码共用，窗口原点逐实例绑定 |
| <a id="ds-64"></a>ds 2h/64 | L10 / B8 | X₂(64)→full X₂(64) + pool X₃(128) | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 独立 full / pool 角色；按本次配置 | 2 头/64 通道；full 交解码；主路降采样 |
| <a id="inp-128"></a>inp 4h/128 | L11 / B9 | X₃(128)→同形 | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 分平面→本档内部 | 4 头/128 通道；本档首块，单例 |
| <a id="chain-128"></a>chain 4h/128 | L12,L13,L14,L15,L142,L143,L144,L145 / B10–B13/B57–B60 | X₃(128)→同形 | 当前窗输入与前馈结果 | 尾投影取 E4 量化再解码的前馈结果 | 本档内部→内部 | 4 头/128 通道；编码/解码共用，窗口原点逐实例绑定 |
| <a id="ds-128"></a>ds 4h/128 | L16 / B14 | X₃(128)→full X₃(128) + pool X₄(256) | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 独立 full / pool 角色；按本次配置 | 4 头/128 通道；full 交解码；主路降采样 |
| <a id="inp-256"></a>inp 8h/256 | L17 / B15 | X₄(256)→同形 | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 分平面→本档内部 | 8 头/256 通道；本档首块，单例 |
| <a id="chain-256"></a>chain 8h/256 | L18,L19,L20,L21,L22,L23,L134,L135,L136,L137,L138,L139 / B16–B21/B49–B54 | X₄(256)→同形 | 当前窗输入与前馈结果 | 尾投影取 E4 量化再解码的前馈结果 | 本档内部→内部 | 8 头/256 通道；编码/解码共用，窗口原点逐实例绑定 |
| <a id="ds-256"></a>ds 8h/256 | L24 / B22 | X₄(256)→full X₄(256) + pool X₅(512) | 当前窗输入与前馈结果 | 入口E4解码作前馈seed；尾投影取E4量化再解码的前馈z | 独立 full / pool 角色；按本次配置 | 8 头/256 通道；full 交解码；主路降采样；L24 显式零写含名义 512 通道区之外的相关平面 |

各次权重、输入/输出区间、几何 extent、窗口原点和控制/发布区均从实际 [params](APPENDIX_beginner_glossary.md#g083) 绑定；不将某几何固定偏移推广到其他配置。ds 的 full 留给对应解码档，pool 的分配范围、补齐写和投影权重也逐配置取值。

- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（接线、形状、布局）、MEASURED（ARCH 具名数值实例）；[ARCH §4.1–§4.3](../../../ARCHITECTURE_V3_ZH.md#4-编码解码主干tin-swin)、[块内接口](../../../ARCHITECTURE_V3_ZH.md#43-一个-tin-块的内部)。调用集合由下面原覆盖清单逐项保留，解码侧 [L1.08](L1_08_tin_decoder.md)复用四档 chained。
- 往下：[L3.tin-window：完整窗口块接线](L3_tin_window.md#tin-window)、[窗口 attention](L3_attention_softmax.md#window-attention)、[norm](L3_norm_nonfinite.md#norm32)、[QMMA](L3_qmma_e4m3.md#qmma-e4m3)、[输入/full/pool 布局](L3_workspace_map.md#regions)。

<!-- 以下覆盖清单对应上表入口，保持单一归属。 -->
<!-- coverage: {"launches":[3],"kernels":["cc_tinlayout_fused_swin_1h_32_1_inpview_tilesync_fp8"]} -->
<!-- coverage: {"launches":[4,5,152,153],"kernels":["cc_tinlayout_fused_swin_1h_32_1_chained_fp8"]} -->
<!-- coverage: {"launches":[6],"kernels":["cc_tinlayout_fused_swin_1h_32_1_ds_wait_fp8"]} -->
<!-- coverage: {"launches":[7],"kernels":["cc_tinlayout_fused_swin_2h_64_2_inpview_tilesync_fp8"]} -->
<!-- coverage: {"launches":[8,9,148,149],"kernels":["cc_tinlayout_fused_swin_2h_64_2_chained_fp8"]} -->
<!-- coverage: {"launches":[10],"kernels":["cc_tinlayout_fused_swin_2h_64_2_ds_wait_fp8"]} -->
<!-- coverage: {"launches":[11],"kernels":["cc_tinlayout_fused_swin_4h_128_4_inpview_tilesync_fp8"]} -->
<!-- coverage: {"launches":[12,13,14,15,142,143,144,145],"kernels":["cc_tinlayout_fused_swin_4h_128_4_chained_fp8"]} -->
<!-- coverage: {"launches":[16],"kernels":["cc_tinlayout_fused_swin_4h_128_4_ds_wait_fp8"]} -->
<!-- coverage: {"launches":[17],"kernels":["cc_tinlayout_fused_swin_8h_256_8_inpview_tilesync_fp8"]} -->
<!-- coverage: {"launches":[18,19,20,21,22,23,134,135,136,137,138,139],"kernels":["cc_tinlayout_fused_swin_8h_256_8_chained_fp8"]} -->
<!-- coverage: {"launches":[24],"kernels":["cc_tinlayout_fused_swin_8h_256_8_ds_wait_fp8"]} -->
