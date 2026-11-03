### L1.06 解码桥（launch L100 / B39）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L100<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B39

【入门交接】🔢 接全局段主路与[瓶颈](APPENDIX_beginner_glossary.md#g010)前保留[旁路](APPENDIX_beginner_glossary.md#g016) → 已知四组[通道](APPENDIX_beginner_glossary.md#g007)按序合并并接回旁路；完整空间恢复[算子](APPENDIX_beginner_glossary.md#g035)？仍未定 → 交较密网格的[窗口](APPENDIX_beginner_glossary.md#g015)[解码](APPENDIX_beginner_glossary.md#g009)段。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：把1024通道瓶颈主路与B30的512通道旁路接成解码入口。
- 输入 → 输出：L99的X₆(1024) [E4](APPENDIX_beginner_glossary.md#g055) + B30.[full](APPENDIX_beginner_glossary.md#g018)的X₅(512) E4→B39.out的X₅(512) E4。
- 计算顺序：四路各8×[K32](APPENDIX_beginner_glossary.md#g065)=256通道；按(3+1)项[half](APPENDIX_beginner_glossary.md#g054)次序[归约](APPENDIX_beginner_glossary.md#g050)全部1024通道→与[缩放](APPENDIX_beginner_glossary.md#g031)skip作[HF](APPENDIX_beginner_glossary.md#g063)→E4。
- 关键例外：保留每K32的F16[发布](APPENDIX_beginner_glossary.md#g091)、三项归约先后及HF边界；具体[插值](APPENDIX_beginner_glossary.md#g020)/卷积语义未独立确认，不能只凭核名决定。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED（[M2](APPENDIX_beginner_glossary.md#g107) 数据结构与显式算术；数值覆盖另见 INDEX）；[chain_entry_optm/entry.cpp 的 decoder](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp)。
- 往下：[L2.06 解码桥单例：投影、索引展开、三项归约、旁路合并与发布](L2_06_decoder_bridge.md#bridge)、[1080数据流图](L2_06_decoder_bridge.md#wiring)；沿串进入 [L1.07 split16 解码](L1_07_split16_decoder.md)。
