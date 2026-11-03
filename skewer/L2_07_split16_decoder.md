# L2.07 split16 解码

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_07_split16_decoder.md) · [本页术语](INDEX.md#形状与工作区记号)

## 解码阶段复用的四个家族

下表只作本阶段导航，不重复定义覆盖；完整[调用](APPENDIX_beginner_glossary.md#g080)列表、逐实例变化与正文均在所链片中。

| 本阶段调用 | 复用正文 |
|---|---|
| L101、105、109、113、117、121、125、129 | [ffwd](L2_04_split16_encoder.md#ffwd) |
| L102、106、110、114、118、122、126、130 | [ffwd_proj](L2_04_split16_encoder.md#ffwd-proj) |
| L103、107、111、115、119、123、127、131 | [qkv](L2_04_split16_encoder.md#qkv) |
| L104、108、112、116、120、124、128 | [proj](L2_04_split16_encoder.md#proj) |


本阶段复用F20、F21、F19的[字段闭式与留出边界](L3_split16_window.md#rest-closed-form-r04o)：F20的非空wload/shared/sread/gstore及F21六个非空地址字段EXACT；F19的shared/sread/gstore EXACT，其wload和两项xsite的r02历史表shape失败由r04分类为NON_PRODUCTION_VARIANT，接受图与4K表EXACT，原失败保留。一般面板式为 `16384*(e//4)+2048*h+512*(e%4)+16*lane`，F20后半需改用扩张/收缩分段；写回按4×4物理块，−1跳过。thread_class仍TABLE，F19/F20/F21的68×120 4K表已逐字段EXACT；没有回执证明C++执行器读取具体12×12接受图。本段不覆盖下方L132专用末视图。

<a id="outview"></a>
<!-- coverage: {"launches":[132],"kernels":["cc_split_swin_16h_proj_512_outview_wait_fp8"]} -->
### L2.07.outview split16 末端 proj_outview_wait（输出视图末块）（1 次调用）

- 覆盖：L132 / B47。
- 是什么：执行最后一个[窗口](APPENDIX_beginner_glossary.md#g015)块的输出[投影](APPENDIX_beginner_glossary.md#g038)并写成 [TIN](APPENDIX_beginner_glossary.md#g011) [解码](APPENDIX_beginner_glossary.md#g009)需要的视图。
- 输入 → 输出：B47 [注意力](APPENDIX_beginner_glossary.md#g039)出口及本块[前馈](APPENDIX_beginner_glossary.md#g037)后[残差](APPENDIX_beginner_glossary.md#g017) → 第 5 档 [512](APPENDIX_beginner_glossary.md#g007) 通道 [E4](APPENDIX_beginner_glossary.md#g055) [outview](APPENDIX_beginner_glossary.md#g022)，位于本次[参数块](APPENDIX_beginner_glossary.md#g083)给出的[工作区](APPENDIX_beginner_glossary.md#g082)出口。
- 怎么算：
  ~~~text
  1. 读取 B47 的两份输入角色和投影权重
  2. 按采集映射组装投影与残差来源
  3. 执行冻结矩阵/逐元素图，保留原量化点
  4. 按末端输出索引写出 outview
  5. 完成本段交接，供 B48 主路读取
  ~~~
- [逻辑](APPENDIX_beginner_glossary.md#g085)交接：B47的窗口attention出口与同块前馈后残差经投影合并，再按outview写回供B48[上采样](APPENDIX_beginner_glossary.md#g021)；物理事件轴只负责把这条接线落到字节。
- 索引结构：[wload_off](APPENDIX_beginner_glossary.md#g090)（[权重](APPENDIX_beginner_glossary.md#g079)偏移）、sread_src（输入来源）、gstore_off（写回偏移）按块×子块×32 个并行位置×事件[绑定](APPENDIX_beginner_glossary.md#g103)，每写事件 16 B。qkv的八个地址/索引字段已有[留出表验证闭式](L3_split16_window.md#qkv-closed-form-r04n)，编码/解码副本均在研究清单内；thread_class仍表驱动；其余家族各字段证据见上方F19/F20/F21，不外推到本单例。L132 由 entry 的专用 [mapexec](APPENDIX_beginner_glossary.md#g089)接线。
- 语义：输出投影把注意力结果带回块宽，并合入同块残差；outview是它与B48主路的存储接口。
- 数值规则：E4 输入逐 [K32](APPENDIX_beginner_glossary.md#g065)[发布](APPENDIX_beginner_glossary.md#g091) [F16](APPENDIX_beginner_glossary.md#g054)，输出再[量化](APPENDIX_beginner_glossary.md#g061)为 E4；视图[重排](APPENDIX_beginner_glossary.md#g019)不增加舍入，不任意交换残差/[归约](APPENDIX_beginner_glossary.md#g050)顺序。
- 实例变化：单例的权重、两份输入、输出区间、带符号窗口原点和几何各自绑定；它的末端映射不能直接换成普通 proj。
- 为什么这么算：这个出口是逐级上采样通路的输入，视图写回负责两种消费布局之间的交接。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（接线）、INFERRED（语义）；[ARCH 0.7 §5.1 的 L132 桥接入口](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维)。
- 往下：[L3.workspace-map（末端地址映射）](L3_workspace_map.md#address-maps)；[L3.window-attention（完整块、投影与残差）](L3_split16_window.md#window-attention)。
