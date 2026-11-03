### L1.03 TIN 编码（launch L3–L24 / B1–B22）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L3–L24<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B1–B22

【入门交接】🔢 接输入端较稀的一路 → 经过四档更稀网格、每位置项数增加，并各存一条[旁路](APPENDIX_beginner_glossary.md#g016) → 交深层[窗口](APPENDIX_beginner_glossary.md#g015)段。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：四档8×8窗口块逐级缩小空间、增加[通道](APPENDIX_beginner_glossary.md#g007)，每档保留一条[解码](APPENDIX_beginner_glossary.md#g009)skip。
- 输入 → 输出：B0.[pool](APPENDIX_beginner_glossary.md#g018)的X₁(32) [E4](APPENDIX_beginner_glossary.md#g055)→四档full X₁(32)、X₂(64)、X₃(128)、X₄(256)→L24 pool X₅(512) E4。
- 计算顺序：每档[inpview](APPENDIX_beginner_glossary.md#g022)→chained→ds_wait；末块保存full，再按固定[half](APPENDIX_beginner_glossary.md#g054)次序池化、[量化](APPENDIX_beginner_glossary.md#g061)并[投影](APPENDIX_beginner_glossary.md#g038)到下一档。
- 关键例外：B4/B8/B14/B22的full分别交B66/B62/B56/B48；pool继续编码。零[token](APPENDIX_beginner_glossary.md#g041)参与窗口计算，L6统计[上溢](APPENDIX_beginner_glossary.md#g071)及L24实际[补齐](APPENDIX_beginner_glossary.md#g085)零写按下层[合同](APPENDIX_beginner_glossary.md#g101)。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：阶段/形状、MEASURED：四条 skip 的单主样本对照及具名数值链；[ARCH 0.7 §4，当前准入见 §4.8](../../../ARCHITECTURE_V3_ZH.md#4-编码解码主干tin-swin)。
- 往下：[L2.03 四档 inpview/chained/ds_wait，共 12 片](L2_03_tin_encoder.md)，四档 chained 同时列出解码调用；沿串进入 [L1.04 split16 编码](L1_04_split16_encoder.md)。
