### L1.05 ViT 瓶颈（launch L58–L99 / B31–B38）

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L58–L99<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B31–B38

【入门交接】🔢 接最小网格的数字 → 换成按位置排列的序列，让每位置与全部有效位置交换内容，再换回二维组织 → 交[解码](APPENDIX_beginner_glossary.md#g009)桥。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：把低分辨率二维[特征](APPENDIX_beginner_glossary.md#g008)[重排](APPENDIX_beginner_glossary.md#g019)为序列，执行八个全局块，再重排回二维。
- 输入 → 输出：X₆(1024) [E4](APPENDIX_beginner_glossary.md#g055)→P×1024 B序列→X₆(1024) E4；T/P分别是有效与[物理](APPENDIX_beginner_glossary.md#g085)行数。
- 计算顺序：L58 repack→八组expand→contract→qkv→[attention](APPENDIX_beginner_glossary.md#g039)→projection→L99逆repack。
- 关键例外：contract[残差](APPENDIX_beginner_glossary.md#g017)来自块入口，projection残差来自contract出口。L58补齐真写零；4K L62另在计算后覆零16×1024 B，不能省略。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：八块与残差接线、MEASURED：具名链及 padding 修复；[ARCH 0.7 §5.2–§5.3，关联 §7.13](../../../ARCHITECTURE_V3_ZH.md#52-一维-vitl58l99)。
- 往下：[L2.05 六家族](L2_05_vit.md)：[repack](L2_05_vit.md#repack)、[expand](L2_05_vit.md#expand)、[contract](L2_05_vit.md#contract)、[qkv](L2_05_vit.md#qkv)、[attention](L2_05_vit.md#attention)、[projection](L2_05_vit.md#projection)；沿串进入 [L1.06](L1_06_decoder_bridge.md)。
