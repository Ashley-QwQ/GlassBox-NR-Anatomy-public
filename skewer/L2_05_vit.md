# L2.05 ViT：共享计算、六家族与块内接线

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [所属 L1](L1_05_vit.md) · [统一记号](INDEX.md#形状与工作区记号)

[权重组织、dtype与阶段字节账](L2_weights_layout.md)

【CPU 重建／CENSUS】L58 把二维[角色](APPENDIX_beginner_glossary.md#g084)改为序列，八个块各执行 expand→contract→qkv→[attention](APPENDIX_beginner_glossary.md#g039)→projection，L99 再改回二维。每块入口记 X，contract 出口记 Z；两条[残差](APPENDIX_beginner_glossary.md#g017)分别来自 X 与 Z。主角色为 [E4](APPENDIX_beginner_glossary.md#g055)，[矩阵](APPENDIX_beginner_glossary.md#g051)逐 [K32](APPENDIX_beginner_glossary.md#g065) [发布](APPENDIX_beginner_glossary.md#g091) [F16](APPENDIX_beginner_glossary.md#g054)，[尺度](APPENDIX_beginner_glossary.md#g031)、[归约](APPENDIX_beginner_glossary.md#g050)、partial half buffer 和 release 各有独立格式/顺序。[补齐](APPENDIX_beginner_glossary.md#g085)行、有效行和额外零写分开登记。

【原生行为／验证记录】下面的宽度与操作次序由当前源码、[绑定](APPENDIX_beginner_glossary.md#g103)图和具名输出门支持；它们不证明原生[内部结构唯一](APPENDIX_beginner_glossary.md#g111)。训练动机、先 [FFN](APPENDIX_beginner_glossary.md#g037) 后 attention 及拆核原因未知。

## 共享合同与六个变体

[调用](APPENDIX_beginner_glossary.md#g080)先按 [params](APPENDIX_beginner_glossary.md#g083) 绑定输入/输出、[权重](APPENDIX_beginner_glossary.md#g079)、几何和完成标记，再执行本家族的数值图，最后发布相应角色。相同家族复用计算结构；数值、残差和地址仍逐块绑定。全局 attention 用逻辑 T 个键；执行按物理 P 行和既定补足轮次组织，不从分配长度增加有效键。

| 家族 / 覆盖入口 | 输入→输出 | 本家族计算与[量化](APPENDIX_beginner_glossary.md#g061) | 残差、布局和真正差异 |
|---|---|---|---|
| <a id="repack"></a>[repack](APPENDIX_beginner_glossary.md#g019)；L58、L99 | X₆(1024) ↔ P×1024 B | 四字节块的[闭式](APPENDIX_beginner_glossary.md#g020)置换，无算术舍入 | L58 显式写补齐零；L99只写逻辑T行；不读取权重/残差。[映射](L3_workspace_map.md#repack) |
| <a id="expand"></a>expand；L59,64,69,74,79,84,89,94 / B31–B38 | X: P×1024→P×4096 B | 1024→4096矩阵，每输出32步K32；逐元素G后E4 | 无本核残差。首块publish与其余[chained](APPENDIX_beginner_glossary.md#g022)的等待/发布不同，G和宽度相同。[FFN](L3_ffn.md#channels) |
| <a id="contract"></a>contract；L60,65,70,75,80,85,90,95 | P×4096 B→Z: P×1024 B | 四个K=1024分片各32步K32；先依序形成half部分和，再E4 | 仅分片0接 [H×](APPENDIX_beginner_glossary.md#g063)(D8(X),s_ff) [seed](APPENDIX_beginner_glossary.md#g042)；分片1/2/3从[+0](APPENDIX_beginner_glossary.md#g070)起。buffer是每行1024个F16=2048 B，不是2048隐藏[通道](APPENDIX_beginner_glossary.md#g007)。[首分片与合并](L3_ffn.md#residual) |
| <a id="qkv"></a>qkv；L61,66,71,76,81,86,91,96 | Z→Q、K、V各P×1024 B | 三路[投影](APPENDIX_beginner_glossary.md#g038)；32头、每头32通道；Q/K头内平方和、[RSQ](APPENDIX_beginner_glossary.md#g072)及尺度后E4，V不作该[归一化](APPENDIX_beginner_glossary.md#g043) | 接收Z，无投影残差；[F32](APPENDIX_beginner_glossary.md#g056)表返回值在显式节点回half。[norm](L3_norm_nonfinite.md#norm32) |
| <a id="attention"></a>attention；L62,67,72,77,82,87,92,97 | Q/K/V→P×1024 B | 全局分数→φ→half归约与RCP；先E4(w)汇合V，后half乘r再E4 | 无外部矩阵权重/残差；补足零键需尾轮扣除。4K L62另在计算后覆盖16×1024 B为零，再发布；不复制到全部调用。[attention](L3_attention_softmax.md#attention-softmax) |
| <a id="projection"></a>projection；L63,68,73,78,83,88,93,98 | attention出口 + Z→下块P×1024 B | 输出矩阵、half部分和按冻结图合并，最后E4 | [旁路](APPENDIX_beginner_glossary.md#g016)是本块contract出口Z；有序half合并不能换成末端实数相加。L98为wait变体。分片、seed与合并顺序见 [QKV与projection部分和](L3_workspace_map.md#partial-sums-r04l)；[矩阵与发布](L3_qmma_e4m3.md#qmma-e4m3)、[half累加](L4_half_arith.md#atomic-add) |

## B31：1080 的一个完整块（T=P=640）

~~~mermaid
flowchart TD
    X["X：640×1024 E4"] --> EX["L59 expand：1024→4096；G→E4"]
    EX --> CT["L60 contract：4个K1024分片；分片0接seed；各32步K32"]
    X --> SeedFFN["D8(X) × s_ff → half seed"]
    SeedFFN --> CT
    CT --> BUF["分片0/1/2依序写half buffer：640×1024 F16 = 640×2048 B"]
    BUF --> Z["分片3与buffer作H+；Z：640×1024 E4"]
    Z --> QKV["L61：Q/K/V各640×1024 E4；32头×32通道；只归一化Q/K"]
    QKV --> AT["L62：每头640×640分数，分块执行；φ→Den→r"]
    AT --> AV["Q8(w)×V：20步K32；half乘r→640×1024 E4"]
    AV --> PR["L63 projection：矩阵与规定half部分和合并"]
    Z --> ResidualAttn["本块Z的投影残差接口"]
    ResidualAttn --> PR
    PR --> Y["B31出口：640×1024 E4 → B32"]
~~~

1080没有补足键；图中20步K32按10个64键轮次组织。4K的补足扣除与L62额外零覆盖见 [尾轮修正](L3_attention_softmax.md#attention-softmax)，不是本图640行的额外分支。图内部分和是软件数值接口，不声称直接观察到原生内部buffer值。

## 来源、观察和边界

| 本断言 | 直接读源 / 观察 | 比较对象与范围 | 不能证明什么 |
|---|---|---|---|
| expand / contract宽度、四分片seed | [expand:267–303](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L267)、[contract:436–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L436) | CPU函数与具名冻结图；数值门见[FFN证据](APPENDIX_evidence_history.md#ffn-r04b) | 任意几何或内部[激活](APPENDIX_beginner_glossary.md#g045)唯一 |
| [QKV](APPENDIX_beginner_glossary.md#g040)、投影及half发布 | [执行器:170–239](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L170) | 当前CPU实现；[attention证据](APPENDIX_evidence_history.md#attention-evidence)分列旧门 | 保存结果不能自动关闭旧地图准入 |
| attention后乘r与零覆盖 | [attention:206–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L206)、[适配器:166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166) | 原语图、具名发布角色和[负控](APPENDIX_beginner_glossary.md#g102) | 一般同步/[别名](APPENDIX_beginner_glossary.md#g092)/生命周期仍未建立 |

往下：[FFN](L3_ffn.md#ffn)、[attention与AV](L3_attention_softmax.md#attention-softmax)、[norm](L3_norm_nonfinite.md#norm32)、[工作区写集](L3_workspace_map.md#write-sets)、[QMMA算术](L4_e4m3_and_k32.md#qmma-k32-accumulation)。各次调用集合保持单一覆盖归属：

<!-- coverage: {"launches":[58,99],"kernels":["cc_vit_1d_repack_2d_to_1d_fp8","cc_vit_1d_repack_1d_to_2d_fp8"]} -->
<!-- coverage: {"launches":[59,64,69,74,79,84,89,94],"kernels":["cc_vit_1d_ffn_expand_publish_fp8","cc_vit_1d_ffn_expand_chained_fp8"]} -->
<!-- coverage: {"launches":[60,65,70,75,80,85,90,95],"kernels":["cc_vit_1d_ffn_contract_chained_fp8"]} -->
<!-- coverage: {"launches":[61,66,71,76,81,86,91,96],"kernels":["cc_vit_1d_qkv_chained_fp8"]} -->
<!-- coverage: {"launches":[62,67,72,77,82,87,92,97],"kernels":["cc_vit_1d_attention_chained_fp8"]} -->
<!-- coverage: {"launches":[63,68,73,78,83,88,93,98],"kernels":["cc_vit_1d_projection_chained_fp8","cc_vit_1d_projection_wait_fp8"]} -->
