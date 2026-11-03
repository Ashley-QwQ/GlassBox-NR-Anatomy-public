# L2.04 split16 编码与共享家族

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_04_split16_encoder.md)

[权重组织、dtype与阶段字节账](L2_weights_layout.md)

[split16](APPENDIX_beginner_glossary.md#g013) 指 16 头、[512](APPENDIX_beginner_glossary.md#g007) 通道的[窗口](APPENDIX_beginner_glossary.md#g015)块[家族](APPENDIX_beginner_glossary.md#g080)。[ffwd](APPENDIX_beginner_glossary.md#g037) / ffwd_proj / qkv / [proj](APPENDIX_beginner_glossary.md#g038) 是前馈前段／后段、[查询](APPENDIX_beginner_glossary.md#g040)键值及融合[注意力](APPENDIX_beginner_glossary.md#g039)／输出投影的[角色](APPENDIX_beginner_glossary.md#g084)解释；[full](APPENDIX_beginner_glossary.md#g018)、pooled、N_out、[E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054)、[K32](APPENDIX_beginner_glossary.md#g065) 和 [seed](APPENDIX_beginner_glossary.md#g042) 见 [记号表](INDEX.md#形状与工作区记号)。X₅=60×36、X₆=32×20 是本页 1080 例，宽×高；主角色为 E4，附属角色类型逐[描述符](APPENDIX_beginner_glossary.md#g088)读取。

## 共享实现合同与家族特定计算

【CPU 重建／CENSUS】各家族从当前 [params](APPENDIX_beginner_glossary.md#g083) 和描述符取得角色，按当前[冻结](APPENDIX_beginner_glossary.md#g103)图完成[矩阵](APPENDIX_beginner_glossary.md#g051)、[归约](APPENDIX_beginner_glossary.md#g050)与[发布](APPENDIX_beginner_glossary.md#g091)；具体取数/写回索引见下层。可选类别、交换来源、分支表按实例绑定。写回者唯一，出口依各角色长度切到独立指针，再发布完成标记。这是共同执行方法，不代替下表的[算子](APPENDIX_beginner_glossary.md#g035)差异。

- **ffwd / ffwd_inpview 怎么算：** 接收512通道输入，先512→512预投影并[量化](APPENDIX_beginner_glossary.md#g061)，再按具名图的八组64→256→64执行G及收缩，发布512通道E4；首块按[TIN](APPENDIX_beginner_glossary.md#g011) pool输入视图取数，后续用[chained](APPENDIX_beginner_glossary.md#g022)视图。核内全门宽2048，不等于[物理](APPENDIX_beginner_glossary.md#g085)N_out；分组依据与矩阵账见 [FFN表](L3_ffn.md#channels)。
- **ffwd_proj / inpview 变体怎么算：** 消费本块ffwd的512通道E4，作512→512后投影；同块入口[解码](APPENDIX_beginner_glossary.md#g061)后与half[尺度](APPENDIX_beginner_glossary.md#g031)相乘，作为首K32的half seed，经过16步后E4发布。不能换成相邻块同形[残差](APPENDIX_beginner_glossary.md#g017)；详见 [残差接口](L3_ffn.md#residual)。
- **qkv 怎么算：** 消费前馈后[特征](APPENDIX_beginner_glossary.md#g008)，在当前移位窗口完成 Q/K/V 及融合 attention；窗口位移改变必须重绑索引，重复位移才可能复用地址图。wload_off、sread_shared_off、sread_src、xsite_src、xsite_wsrc、gstore_off、shfl_idx、psel已有[留出地图验证的八字段闭式](L3_split16_window.md#qkv-closed-form-r04n)；thread_class因1080缺字段、冻结假说在留出失败而仍表驱动。生产执行器仍读原表，地址等价不扩张为数值DAG、全链或动态血缘证明。它不是单独一次 512→1536 线性变换，内部角色长度不能一律当成三份 Q/K/V；已写的分数、归约、[RCP](APPENDIX_beginner_glossary.md#g072) 与 [AV](APPENDIX_beginner_glossary.md#g077) 见 [attention 分项](L3_attention_softmax.md#window-attention)。
- **proj / proj_pool 怎么算：** 消费当前块 qkv 出口与前馈后[旁路](APPENDIX_beginner_glossary.md#g016)，按投影/合并图形成下一块主干；L56 按两套写回索引分别形成空间 full 和池化换格出口，不能只算一份 skip 后以未经核对的库池化代替另一份。pooled 名称不证明标准平均池化公式。
- **final_head 怎么算：** 消费 L56 pooled，按当前二维格、[权重](APPENDIX_beginner_glossary.md#g079)和采集索引执行独立图，发布 1024 通道角色；其输出指针正是 L58 输入指针，无后续 [ViT](APPENDIX_beginner_glossary.md#g014) 残差输入，也没有分类头语义。
- **数值规则：** 矩阵逐 K32 发布 F16；归约、[门函数](APPENDIX_beginner_glossary.md#g045)、half/E4 量化、融合与残差 seed 的节点保持冻结图原序；RSQ/RCP 表外拒绝，QMMA [overflow](APPENDIX_beginner_glossary.md#g071) 守卫不删除。已确认的seed见下表及L3；物理布局未知不放宽算术次序。
- **为什么：** ffwd 增加逐位置处理的隐藏角色，ffwd_proj 将其带回主干并保留入口；qkv 在窗口内交换位置内容，proj 形成下一块特征；proj_pool 保留[瓶颈](APPENDIX_beginner_glossary.md#g010)前空间旁路并减少 [token](APPENDIX_beginner_glossary.md#g041)，final_head 适配瓶颈宽度。这些是投影、分组、残差与换格的算子作用；选择这些宽度和融合边界的训练意图仍未知。


### 其余家族的地址闭式及留出边界

<a id="audit-family-ids"></a>
下面F16–F23是审计家族编号；F16作为家族号时，不表示同名的F16/half浮点格式。F18.36中F18指家族，36指该家族内的审计条目。

F16（inpview ffwd）、F17（inpview ffwd_proj）、F19（proj）、F20（ffwd）、F21（ffwd_proj）、F22（proj_pool）、F23（final_head）的[各字段可执行公式与证据表](L3_split16_window.md#rest-closed-form-r04o)共用4×4物理块 P_C；越界来源−1补零，越界写回−1跳过，xsite的−3选择资源。普通64事件资源面板偏移为 `16384*(e//4)+2048*h+512*(e%4)+16*lane`；F23的篮步长改32768，F16/F20后64事件另分扩张/收缩。F22另有pooled第二出口索引及交换/选择式，F23按1024通道输出块写回。

阅读下面的英文标签前，可先看[地址公式与对照标签图例](APPENDIX_beginner_glossary.md#address-status)。

每个字段按EXACT、r02历史FAIL或VACUOUS分别读：F16/F17的sread_src与F19的wload/xsite历史变体已由r04分类为NON_PRODUCTION_VARIANT，对应接受图EXACT，r02失败不改写；没有回执证明C++实际读取这些12×12图。F16/F20/F23空xsite不构成非空地址证据，thread_class仍TABLE。F16/F17/F19–F22的68×120 4K表EXACT，F18的4K来自独立r01 QKV式；F23另有36×60绑定表，但没有独立绑定4K帧身份。详见[逐族计数](L3_split16_window.md#r04-four-k-r04p)；地址相等不证明数值DAG/全链/动态血缘。

## 变体表

| 家族／入口 | launches / B | 逻辑形状 / M×K×N | 残差来源 | seed 量化 | layout | 真正差异 |
|---|---|---|---|---|---|---|
| <a id="ffwd-inpview"></a>ffwd_inpview | L25 / B23 | S×512×512预投影；8组S×64×256→S×256×64；拼回S×512 | 块入口保留给后段 | 本核无外部残差；内部点按图 | TIN pool→512通道E4首块出口 | 单例；首块输入索引不等于 chained |
| <a id="ffwd-proj-inpview"></a>ffwd_proj_inpview | L26 / B23 | ffwd X₅(512) + 块入口→X₅(512)；S×512×512 | B23 入口 | 入口E4解码后half乘尺度，首K32 seed | 首块隐藏/入口→chained | 单例；首次接入 16 头主干 |
| <a id="ffwd"></a>ffwd | L29,33,37,41,45,49,53；L101,105,109,113,117,121,125,129 / B24–B30,B40–B47 | S×512×512预投影；8组S×64×256→S×256×64；拼回S×512 | 本块输入保留给后段 | 本核无外部残差；内部点按图 | chained→512通道E4 | 15 次，编码/解码共用家族 |
| <a id="ffwd-proj"></a>ffwd_proj | L30,34,38,42,46,50,54；L102,106,110,114,118,122,126,130 / 同上 | ffwd X₅(512) + 块入口→X₅(512)；S×512×512 | 当前块入口 | 入口E4解码后half乘尺度，首K32 seed | 隐藏/入口→主干 | 15 次；不复用前块数值或残差 |
| <a id="qkv"></a>qkv | L27,31,35,39,43,47,51,55；L103,107,111,115,119,123,127,131 / B23–B30,B40–B47 | X₅(512)→融合注意力 N_out B；16头、每头32通道；物理索引轴不等同逻辑轴 | 前馈后主角色由 proj 合并 | 权重和中间量按图量化，不能简化为线性 QKV | 移位窗口索引→融合出口 | 16 次；位移、动态[状态](APPENDIX_beginner_glossary.md#g002)/发布域逐实例绑定 |
| <a id="proj"></a>proj | L28,32,36,40,44,48,52；L104,108,112,116,120,124,128 / B23–B29,B40–B46 | 注意力出口 + X₅(512)→X₅(512)；已核L28为16步K32，物理分片轴另按图 | 当前块前馈后主角色 | 本块前馈后Z的E4解码后half乘尺度，作投影首K32 seed | 融合出口→chained | 14 次；输出给下一块 ffwd |
| <a id="proj-pool"></a>proj_pool | L56 / B30 | →full X₅(512) + pooled X₆(512)；已核链各16步K32，双出口分片按图 | B30 前馈后旁路 | 本块Z的E4解码后half乘尺度；双出口按冻结图带入seed | 两份输出按长度切分为独立指针 | B39 skip 与瓶颈入口分流，均 E4 |
| <a id="final-head"></a>final_head | L57 / B30 | X₆(512)→X₆(1024)；已知 K=512，16 条各 16 步 K32 链、首 seed 为 +0（见 [L3 的 L57 一段](L3_split16_window.md#evidence)，紧挨证据节之前）；逻辑 M/N 与空间/分片对应未确认 | 无后续 ViT 残差 | 不引入额外 seed；图内节点保持 | 二维池化角色→L58 同指针输入 | 单例；1024 为出口宽度，不推断内部矩阵 |

每次调用的权重、输入/旁路、[工作区](APPENDIX_beginner_glossary.md#g082)区间、几何和控制状态独立绑定；同一家族在具名样本可复用地址图，不能据此复用数值。L56 两份宽高、补齐 extent、偏移和 L57 二维格同样逐配置读取。

- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（精确调用集合、执行器、角色接线）、MEASURED（具名双出口/1024 接线）、INFERRED（算子语义）；[ARCH §5.1–§5.1.2](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维)。
- 往下：[L3.ffn：门函数、通道与残差](L3_ffn.md#ffn)、[L3.window-attention：完整融合块](L3_split16_window.md#window-attention)、[已写 attention 分项](L3_attention_softmax.md#window-attention)、[QMMA](L3_qmma_e4m3.md#qmma-e4m3)、[数据驱动地址表](L3_workspace_map.md#address-maps)。解码端 [L2.07](L2_07_split16_decoder.md)复用四个 chained 家族；L132 在该页独立说明。

<!-- coverage: {"launches":[25],"kernels":["cc_split_swin_16h_ffwd_inpview_512_tilesync_fp8"]} -->
<!-- coverage: {"launches":[26],"kernels":["cc_split_swin_16h_ffwd_proj_inpview_512_chained_fp8"]} -->
<!-- coverage: {"launches":[29,33,37,41,45,49,53,101,105,109,113,117,121,125,129],"kernels":["cc_split_swin_16h_ffwd_512_chained_fp8"]} -->
<!-- coverage: {"launches":[30,34,38,42,46,50,54,102,106,110,114,118,122,126,130],"kernels":["cc_split_swin_16h_ffwd_proj_512_chained_fp8"]} -->
<!-- coverage: {"launches":[27,31,35,39,43,47,51,55,103,107,111,115,119,123,127,131],"kernels":["cc_split_swin_16h_qkv_512_chained_fp8"]} -->
<!-- coverage: {"launches":[28,32,36,40,44,48,52,104,108,112,116,120,124,128],"kernels":["cc_split_swin_16h_proj_512_chained_fp8"]} -->
<!-- coverage: {"launches":[56],"kernels":["cc_split_swin_16h_proj_pool_512_chained_fp8"]} -->
<!-- coverage: {"launches":[57],"kernels":["cc_split_swin_16h_final_head_512_wait_fp8"]} -->

L56逻辑几何：8×5个8×8窗覆盖60×36有效区，窗口画布64×40；出口容量为32×20×512 E4。【推断】每窗配对4×4空间出口与这些容量相容，尚未由独立坐标证据确立；它不是已证明的逐窗接线，也不是把有效尺寸直接减半。[已测字节与配对所需证据](L3_split16_window.md#heads)分列。
