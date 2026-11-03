### L1.02 输入端 B0（launch L2 / B0）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L2<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B0

【入门交接】🖼 接当前图、移动信息、可用旧图与控制 → 🔢 凑16项条件并变成32项内部数 → 一路交[编码](APPENDIX_beginner_glossary.md#g009)，一路留到末端。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：B0在一次调用内生成噪声、准备[历史](APPENDIX_beginner_glossary.md#g024)条件，完成[16→32](APPENDIX_beginner_glossary.md#g007)通道适配和首个[窗口](APPENDIX_beginner_glossary.md#g015)块。
- 输入 → 输出：id1、id3、有效id6及[params](APPENDIX_beginner_glossary.md#g083)→[full](APPENDIX_beginner_glossary.md#g018) X₀(32) [E4](APPENDIX_beginner_glossary.md#g055)与pool X₁(32) E4，分别送B70[旁路](APPENDIX_beginner_glossary.md#g016)与[TIN](APPENDIX_beginner_glossary.md#g011)编码。
- 计算顺序：坐标/帧字生成三路噪声→颜色[镜像](APPENDIX_beginner_glossary.md#g030)与[五tap](APPENDIX_beginner_glossary.md#g029)历史[重投影](APPENDIX_beginner_glossary.md#g025)→16通道→[F16](APPENDIX_beginner_glossary.md#g054)适配→窗口块→full与2×2 pool。
- 关键例外：[p5](APPENDIX_beginner_glossary.md#g032)真时[structure](APPENDIX_beginner_glossary.md#g005)通道置1、两个[mask](APPENDIX_beginner_glossary.md#g006)取控制缓冲；有历史则五tap写7..9，否则重复当前RGB；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：[M2](APPENDIX_beginner_glossary.md#g107) 接线与行为、MEASURED：ARCH 0.7 的具名时域实例；[ARCH 0.7 §3，含当前时域修订](../../../ARCHITECTURE_V3_ZH.md#3-输入端)。
- 往下：[L2.02 单例交接](L2_02_b0.md#b0)：[噪声](L2_02_b0.md#noise)、[五 tap 重投影](L2_02_b0.md#temporal)、[16 通道](L2_02_b0.md#channels)、[适配/窗口块](L2_02_b0.md#adapter)、[full/pool](L2_02_b0.md#publish)；沿串进入 [L1.03](L1_03_tin_encoder.md)。
