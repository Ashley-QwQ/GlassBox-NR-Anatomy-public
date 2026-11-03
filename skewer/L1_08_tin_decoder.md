### L1.08 TIN 解码（launch L133–L154 / B48–B69）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L133–L154<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B48–B69

【入门交接】🔢 接深层[解码](APPENDIX_beginner_glossary.md#g009)出口与四条编码[旁路](APPENDIX_beginner_glossary.md#g016) → 四次变密并接回同档旁路、每位置项数回到32 → 交末端，主路宽高仍各为内部画布一半。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：四级[投影](APPENDIX_beginner_glossary.md#g038)[上采样](APPENDIX_beginner_glossary.md#g021)接回编码skip，把[512](APPENDIX_beginner_glossary.md#g007)通道深层[特征](APPENDIX_beginner_glossary.md#g008)恢复到32通道。
- 输入 → 输出：B47.[outview](APPENDIX_beginner_glossary.md#g022) X₅(512)与四档编码[full](APPENDIX_beginner_glossary.md#g018)→X₄(256)→X₃(128)→X₂(64)→B69.outview X₁(32)，均为[E4](APPENDIX_beginner_glossary.md#g055)。
- 计算顺序：L133/141/147/151：主路投影→最近邻×2→投影主路加[缩放](APPENDIX_beginner_glossary.md#g031)skip→[窗口](APPENDIX_beginner_glossary.md#g015)块；随后chained和outview收尾。
- 关键例外：一头upsample的[前馈](APPENDIX_beginner_glossary.md#g037)[seed](APPENDIX_beginner_glossary.md#g042)保留未[量化](APPENDIX_beginner_glossary.md#g061)合并值，多头先E4再解码。1440首档有效高92；B69独立布局和L133独立来源证明仍按L2保留边界。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED：分档合并、单样本 skip 及具名链；[ARCH 0.7 §4.5–§4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66)；当前数值门不解除 L133 符号层 [NOT_ADMITTED](APPENDIX_beginner_glossary.md#g104)。
- 往下：[L2.08 四档 upsample/outview 八片及共享 chained 导航](L2_08_tin_decoder.md)；沿串进入 [L1.09 B70](L1_09_b70.md)。
