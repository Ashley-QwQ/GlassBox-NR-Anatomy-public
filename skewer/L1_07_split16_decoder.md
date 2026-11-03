### L1.07 split16解码（launch L101–L132 / B40–B47）

<!-- beginner-r04m:start stage -->
阅读深度：L1（阶段）<br>[执行编号](APPENDIX_beginner_glossary.md#g081)：[launch](APPENDIX_beginner_glossary.md#g080) L101–L132<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B40–B47

【入门交接】🔢 接桥输出的每位置[512](APPENDIX_beginner_glossary.md#g007)项数 → 连续八块[窗口](APPENDIX_beginner_glossary.md#g015)处理并交出后续需要的存放组织 → 交四档变密阶段。

固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。
<!-- beginner-r04m:end stage -->

上一层：[L0 一帧](L0_frame.md) · [回索引](INDEX.md)

【CPU 重建】阶段接线如下；[统一记号](INDEX.md#形状与工作区记号)与[解释口径](INDEX.md#计算口径)集中在目录。

- 作用：在512通道尺度再执行八个[16头](APPENDIX_beginner_glossary.md#g013)窗口块，末端转成[TIN](APPENDIX_beginner_glossary.md#g011)[上采样](APPENDIX_beginner_glossary.md#g021)所需视图。
- 输入 → 输出：B39.out的X₅(512) [E4](APPENDIX_beginner_glossary.md#g055)→八块内部[角色](APPENDIX_beginner_glossary.md#g084)→B47.[outview](APPENDIX_beginner_glossary.md#g022)的同形E4，交L133。
- 计算顺序：八组[ffwd](APPENDIX_beginner_glossary.md#g037)→ffwd_proj→qkv→[proj](APPENDIX_beginner_glossary.md#g038)；末次换成L132 proj_outview_wait。
- 关键例外：L132仍包含投影与E4[发布](APPENDIX_beginner_glossary.md#g091)，后面的视图[重排](APPENDIX_beginner_glossary.md#g019)本身不增加[量化](APPENDIX_beginner_glossary.md#g061)；每块的输入、[权重](APPENDIX_beginner_glossary.md#g079)、[残差](APPENDIX_beginner_glossary.md#g017)及窗口位移独立[绑定](APPENDIX_beginner_glossary.md#g103)。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)：逐块接线与 L132 出口、MEASURED：具名数值链；[ARCH 0.7 §5.1，L132 桥接入口](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维)。
- 往下：[L2.07 四个共享家族的解码导航](L2_07_split16_decoder.md)与 [L132 outview 单例](L2_07_split16_decoder.md#outview)；沿串进入 [L1.08 TIN 解码](L1_08_tin_decoder.md)。
