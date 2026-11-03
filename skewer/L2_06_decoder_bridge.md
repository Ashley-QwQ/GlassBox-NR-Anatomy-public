# L2.06 解码桥

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_06_decoder_bridge.md) · [本页术语](INDEX.md#形状与工作区记号)

[权重组织、dtype与阶段字节账](L2_weights_layout.md)

<a id="bridge"></a>
<!-- coverage: {"launches":[100],"kernels":["cc_dec_input_upsample_1024_512_tilesync_fp8"]} -->
### L2.06.bridge 解码桥：投影、归约与 skip（1 次调用）

- 覆盖：L100 / B39。
- 是什么：把[瓶颈](APPENDIX_beginner_glossary.md#g010)出口[投影](APPENDIX_beginner_glossary.md#g038)/展开，并合入 B30 的空间[旁路](APPENDIX_beginner_glossary.md#g016)。
- 输入 → 输出：第 6 档 1024 [通道](APPENDIX_beginner_glossary.md#g007) [E4](APPENDIX_beginner_glossary.md#g055) + B30.[full](APPENDIX_beginner_glossary.md#g018)（第 5 档 512 通道完整旁路）→第 5 档 512 通道 E4；另写 [F16](APPENDIX_beginner_glossary.md#g054) [部分和](APPENDIX_beginner_glossary.md#g050)暂存与控制区，各区间由本次参数给定。
<a id="operator"></a>
## 通道归约与窗口几何

【CPU 重建／固定1080地图】每路8×[K32](APPENDIX_beginner_glossary.md#g065)覆盖256个输入通道，四路部分和（[REDMAP](APPENDIX_beginner_glossary.md#g090)前三路、OUTMAP第四路）共同归约1024=4×256通道；它们不是四个空间[插值](APPENDIX_beginner_glossary.md#g020)点。固定图的全部1,105,920个输出字节均各选四个通道组一次，并共享其余选择坐标；A来源组的空间位置相同、通道相差256。[整数核对与SHA](examples/geometry_r04g.result.json)[绑定](APPENDIX_beginner_glossary.md#g103)本实例，不能外推任意地图。

60×36的[窗口](APPENDIX_beginner_glossary.md#g015)网格为ceil(60/8)×ceil(36/8)=8×5，覆盖画布64×40；已知出口[逻辑](APPENDIX_beginner_glossary.md#g085)容量为32×20×512 E4，不是有效60×36直接减半所得的30×18。L56地图的pooled出口327,680 B由20,480个16 B写事件唯一覆盖，按8192 B人为分桶恰有40桶，每桶容量等于4×4×512 E4。[整数地图核对](examples/geometry_r04g.py)证明这些字节计数；【推断】每个8×8输入窗配对一个4×4空间出口与容量相容，但桶号尚未独立标定为空间块。要确立配对，须独立建立输入窗编号与pooled字节的逻辑(x,y,c)映射，再逐写事件核对来源/目的坐标；还需独立标定L100输出和skip的逻辑坐标才能建立桥接的空间对应。现有记录不单独证明标准四点[均值](APPENDIX_beginner_glossary.md#g044)池化、原生独立物理布局或L100采用哪种插值。

- 怎么算：
  ~~~text
  1. 按输入来源表和权重偏移表读取矩阵操作数
  2. 四路各按八步K32归约256通道，保留每步half发布
  3. 按规定先合并前三个256通道部分和
  4. 再加第四个256通道部分和完成1024通道归约，随后与缩放skip融合
  5. 量化、写输出/暂存及本实例声明的控制标记
  ~~~
- 索引结构：A_src（输入偏移）/B_off（[权重](APPENDIX_beginner_glossary.md#g079)偏移）为七轴表，前四轴乘积等于逻辑 [token](APPENDIX_beginner_glossary.md#g041) 数，尾三轴为 16×8×32；OUTMAP（输出映射）每输出字节一行 12 项；REDMAP（三项归约来源）每位置 3×4 项。
- 语义：1024 通道低密度格→512 通道高密度格有形状/接线支持；具体插值或卷积语义未独立确认，不能仅凭 upsample 名称判定[最近邻](APPENDIX_beginner_glossary.md#g021)。
- 数值规则：三项 half 加为先前两项、再第三项；与另一路加后才作[融合乘加](APPENDIX_beginner_glossary.md#g063)；最后 E4 [RN-even](APPENDIX_beginner_glossary.md#g059)，half 融合的细舍入模型留到下层。
- 实例变化：单例随几何更换来源/输出/归约图、权重与区间；[残差](APPENDIX_beginner_glossary.md#g017)始终来自当前帧 B30 完整旁路；控制计数按该实例合同写入。
- 为什么这么算：将全局瓶颈信息恢复到窗口尺度，同时接回未经过瓶颈的空间信息。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（结构/显式算术）、INFERRED（空间语义）；[entry.cpp 的 decoder](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp)。
- 往下：[L3.workspace-map（桥接映射）](L3_workspace_map.md#address-maps)；[L3.qmma-e4m3（投影矩阵）](L3_qmma_e4m3.md#qmma-e4m3)；[L4.half-arith（归约/融合舍入）](L4_half_arith.md#half-arith)。

<a id="wiring"></a>
### 1080 L100数据流：投影、三项归约与B30旁路

~~~mermaid
flowchart TD
    X["L99：X₆(1024) E4，32×20×1024"] --> P["按A_src/B_off投影：4路各256通道；各8步K32与F16发布"]
    P --> Partials["F16投影部分和Partials；执行分片轴按图"]
    Partials --> R["REDMAP选v₀/v₁/v₂：H+(H+(v₀,v₁),v₂) → r F16"]
    R --> O["OUTMAP：逐输出选r、另一路d₃、skip位置及尺度来源"]
    Partials -->|"另一路部分和d₃"| O
    O --> ADD["H+(r,d₃) → F16"]
    ADD --> HF["h_fma(D8(skip),尺度,H+(r,d₃)) → F16"]
    SK["L56 / B30.full：X₅(512) E4，60×36×512"] --> HF
    HF --> Q["Q8 → X₅(512) E4，60×36×512"]
    Q --> NEXT["B40 / L101 split16解码"]
    R -. "按RED_OFF写F16暂存" .-> TMP["暂存角色；控制标记另按本次绑定发布"]
~~~

三项归约先前两项、再第三项；OUTMAP选出的d₃还要与r作一次独立half加，之后才进入skip融合乘加和E4[发布](APPENDIX_beginner_glossary.md#g091)。图中的“分片”是CPU部分和组织，不命名为网络头，也不把该桥推定为最近邻或某种卷积。[entry.cpp:54–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L54)逐项给出顺序；本轮 [参数/地图核对](APPENDIX_evidence_history.md#split16-window-r04d)同时核对L99主路、B30.full与本[调用](APPENDIX_beginner_glossary.md#g080)的指针交接，没有执行新网络数值门。

<a id="byte-trace"></a>
### 1080 的一个实际来源例：输出物理字节0

【CPU 重建／整数表实读】[脚本](examples/map_trace_r04f.py)先核对原绑定SHA，只读整数地图。OUTMAP第0行选归约暂存偏移0和另一路部分和；前三项Partials选择器分别为(0,0,0,0)、(160,0,0,0)、(320,0,0,0)，第四项为(480,0,0,0)。每个部分和的八步K32合计读取256个不同主路字节。

经已建立的L99二维[重排](APPENDIX_beginner_glossary.md#g019)逆式解码，这四组均来自瓶颈逻辑(x,y)=(0,0)，通道分别为0–255、256–511、512–767、768–1023；skip取B30.full物理字节0。按前三项H+、再第四项H+、再HF合并skip，最后发布输出字节0。[读表结果与身份](examples/map_trace_r04f.result.json)保留完整选择器。

这里确实确定了主路源坐标；**输出字节0和skip字节0的独立逻辑坐标仍未建立**，不能把它们直接称为某个(x,y,c)。关闭剩余空间关系需独立标定两端布局并对照这些来源；当前例不宣称已解释整个32×20→60×36空间[算子](APPENDIX_beginner_glossary.md#g035)。

【CPU 重建／整数表实读】按表照着实现时，L100 的连续执行定义是：A_src/B_off 给八步 K32 的来源；REDMAP 给前三个部分和 D 的来源；OUTMAP[i] 给输出字节 i 的暂存 half 地址、第四个 D、skip 字节和尺度偏移（第 7–11 列当前不消费，不能当额外操作数）。算法是 red=H+(H+(D₀,D₁),D₂)、v=H+(red,D₃)、out[i]=Q8(HF(E4→half(skip[OUTMAP[i,5]]),尺度,v))。1080 上 1,105,920 个输出全部满足 OUTMAP[i,5]=i，也就是 skip 与当前输出按同一个物理字节下标融合；但物理下标相同，不等于两端的图像坐标已经独立标定。资产见[层索引资产](REPRODUCE.md#layer-assets)，核对见 [F04](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)。
