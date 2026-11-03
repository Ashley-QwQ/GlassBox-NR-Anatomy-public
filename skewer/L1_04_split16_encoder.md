### L1.04 split16编码（launch L25–L57 / B23–B30）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L25–L57<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B23–B30

【入门交接】🔢 接四档[编码](APPENDIX_beginner_glossary.md#g009)的出口 → 在小[窗口](APPENDIX_beginner_glossary.md#g015)内连续处理八块，再分出较稀主路与一份保留[旁路](APPENDIX_beginner_glossary.md#g016) → 主路交全局段、旁路交桥。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：八个[16头](APPENDIX_beginner_glossary.md#g013)、[512](APPENDIX_beginner_glossary.md#g007)通道窗口块把[TIN](APPENDIX_beginner_glossary.md#g011)编码出口送到[全局瓶颈](APPENDIX_beginner_glossary.md#g010)。
- 输入 → 输出：X₅(60×36×512)按8×5个8×8窗覆盖64×40，出口[逻辑](APPENDIX_beginner_glossary.md#g085)容量为X₆(32×20×512)；【推断】每窗对应4×4空间出口是与布局相容的解释，独立窗→出口坐标配对尚未建立，所需证据见[几何边界](L3_split16_window.md#heads)。另留B30.[full](APPENDIX_beginner_glossary.md#g018) skip，L57适配至1024通道。
- 计算顺序：八组[ffwd](APPENDIX_beginner_glossary.md#g037)→ffwd_proj→qkv→[proj](APPENDIX_beginner_glossary.md#g038)；首组接[inpview](APPENDIX_beginner_glossary.md#g022)，末组用L56 proj_pool分流，再接L57 final_head。
- 关键例外：full与pooled各有自己的写回来源，不能用未经核对的库池化替代。物理执行轴不等于逻辑空间/通道轴，具体映射留到L3。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：拓扑、MEASURED：具名分段/整链；[ARCH 0.7 §5.1](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维)。
- 往下：[L2.04 八个家族片](L2_04_split16_encoder.md)，其中四个 chained 家族同时列出解码调用；沿串进入 [L1.05 ViT](L1_05_vit.md)。
