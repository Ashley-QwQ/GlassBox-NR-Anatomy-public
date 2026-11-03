### L1.10 输出（launch L156–L157 / 无 B 编号）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L156–L157<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：无 B 编号

【入门交接】🖼 接本帧新颜色[状态](APPENDIX_beginner_glossary.md#g002)与原图备份 → 一路保存为下帧[历史](APPENDIX_beginner_glossary.md#g024)，另一路作显示调整与强度混合 → 交同输入尺寸的显示图。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：从B70状态分别保存下帧历史和生成本帧显示图。
- 输入 → 输出：L156：id9→id6；L157：id9与id10及controls→同尺寸[RGBA16F](APPENDIX_beginner_glossary.md#g028) id2。
- 计算顺序：逐有效行复制历史→对id9执行[F32](APPENDIX_beginner_glossary.md#g056)颜色链→按[intensity](APPENDIX_beginner_glossary.md#g004)与id10融合→[夹取](APPENDIX_beginner_glossary.md#g049)并[RZ](APPENDIX_beginner_glossary.md#g060)转[F16](APPENDIX_beginner_glossary.md#g054)。
- 关键例外：156路线省去[基底](APPENDIX_beginner_glossary.md#g003)备份与独立S157，尾段写id2后复制id2→id6；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED（[M2](APPENDIX_beginner_glossary.md#g107) 的复制、后处理及 RZ 出版；颜色空间名称不作为公式前提）；[chain_outtail_optm/outtail.cpp 的 s157、rz 与 run](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp)。
- 往下：[L156 共享复制片](L2_01_prepare.md#copy)、[L157 后处理/强度合成片](L2_10_output.md#postprocess)（含来源解释冲突）；跨帧回到 [L1.02 B0](L1_02_input_b0.md)，整串见 [INDEX](INDEX.md)。 · [本页术语](INDEX.md#形状与工作区记号)
