### L1.01 图外前置（launch L0–L1 / 无 B 编号）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L0–L1<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：无 B 编号

【入门交接】🖼 接本帧当前图 → 留一份原图备份；🗃 只设置指定管理区 → 交输入计算，并把备份留给显示。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：图外前置保留显示合成[基底](APPENDIX_beginner_glossary.md#g003)，并初始化后续块的控制区。
- 输入 → 输出：id1的W×H×4 [F16](APPENDIX_beginner_glossary.md#g054)→同形id10；L1另把声明的4n B控制区填成0xFF。
- 计算顺序：按有效[纹素](APPENDIX_beginner_glossary.md#g027)复制→读取清理长度→填控制区→交给后续调用。
- 关键例外：复制的[非有限](APPENDIX_beginner_glossary.md#g069)转换仍受守卫限制；初始化范围不是整片[工作区](APPENDIX_beginner_glossary.md#g082)，也不表示置零。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：[M2](APPENDIX_beginner_glossary.md#g107) 源码的 id10 接线、填充值与范围；[chain_entry_optm/entry.cpp 的 run_launch](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp)；ARCH §1.1 将 id10 接线标为推断，这里保留其与源码核对的区别。
- 往下：[L2.01.copy 颜色/历史复制](L2_01_prepare.md#copy)、[L2.01.clear 控制区初始化](L2_01_prepare.md#clear)；沿串进入 [L1.02 B0](L1_02_input_b0.md)。
