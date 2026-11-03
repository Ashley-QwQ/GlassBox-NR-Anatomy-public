# L0a 对象与方法

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

[整串目录](INDEX.md) · 下一层：[L0一帧](L0_frame.md) · [确定性与可复现性](L0b_determinism.md)

[公开v2复现指南](REPRODUCE.md) · [权重组织](L2_weights_layout.md)

<a id="object"></a>
## 我们在解释哪个对象

对象固定为nvngx_dlssnr.dll **310.8.0.0、样本C、[SHA](APPENDIX_beginner_glossary.md#g103)-256前缀e16bcf15e16e13f5…**。既有只读实物核验给出完整文件SHA、版本与165,840,496 B长度，[experiments/parity-cpp-param-change-r01-20261024-codex/stage_d2_followup/RESULT_ZH.md:9](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d2_followup/RESULT_ZH.md#L9)；样本C的有效NVIDIA签名身份及[WEIGHTS_HT](APPENDIX_beginner_glossary.md#g079)资源身份见[ARCHITECTURE_V3_ZH.md:264–274](../../../ARCHITECTURE_V3_ZH.md#L264)。版本号相同不足以替代文件SHA。

这里“网络”指该固定对象在具名输入、控制与[历史](APPENDIX_beginner_glossary.md#g024)[状态](APPENDIX_beginner_glossary.md#g002)下的计算主干：B0条件输入、[编码](APPENDIX_beginner_glossary.md#g009)、[瓶颈](APPENDIX_beginner_glossary.md#g010)、解码、B70状态出口；本串还解释相邻的颜色复制、[工作区](APPENDIX_beginner_glossary.md#g082)初始化、[重排](APPENDIX_beginner_glossary.md#g019)、历史复制和显示后处理，使一帧从输入接到输出。默认路线是[launch](APPENDIX_beginner_glossary.md#g080) [L0](APPENDIX_beginner_glossary.md#g081)–L157，[B编号](APPENDIX_beginner_glossary.md#g036)与launch编号分开；它不代表[DLL](APPENDIX_beginner_glossary.md#g078)所有功能路径或唯一训练架构。[ARCHITECTURE_V3_ZH.md:147–167](../../../ARCHITECTURE_V3_ZH.md#L147)，各阶段的计算解释从[L0](L0_frame.md)进入。

因此，原生对象、[CPU重建](APPENDIX_beginner_glossary.md#g100)和结果记录需要分开阅读：前者是被观察的计算行为，CPU源码给出一个可执行的复现假说，结果记录检验该假说在明确输入与比较范围内是否成立；结果不能唯一反推原生内部结构或训练目的。[ARCHITECTURE_V3_ZH.md:63–80、1413](../../../ARCHITECTURE_V3_ZH.md#L63)。

<a id="route-scope-r04l"></a>
### 路线描述符的消费范围（审计 V01.02，排名1）

本文能解释的是冻结调用[描述符](APPENDIX_beginner_glossary.md#g088)之后的计算。[R2c](APPENDIX_beginner_glossary.md#g110) 的 `configure(d)` 取 `d.get("route_launches",158)`，仅接受156或158；它没有实现从主机 [tone](APPENDIX_beginner_glossary.md#g005)/style 选择生成路线、[常量缓冲](APPENDIX_beginner_glossary.md#g083)与[纹理](APPENDIX_beginner_glossary.md#g027)绑定的分支。因此“156/158可消费”不等于“主机如何选择156/158已重建”。该生成步骤仍为 UNKNOWN_IN_SOURCE，本轮只修订范围。[R2c geometry.hpp:31–35](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/returned/snapshot/candidate/repo/cpp/opt/M/geometry.hpp#L31)。

固定 1080 已经可以给出一份冻结 profile 的消费合同：尺寸、缓冲、跨帧保留和逐帧调用顺序，见 [两帧接续](REPRODUCE.md#two-frames)。它以已有的完整 params/profile 包为前提，不代表已经能从任意主机控制生成路线和绑定；上面的未知保持不变。

<a id="capture"></a>
## 捕获记录了什么，为什么要记录

| 记录种类 | 保存的内容 | 用来区分什么 | 既有依据 |
|---|---|---|---|
| 对象、输入与调用元数据 | DLL/资源身份，颜色/[MV](APPENDIX_beginner_glossary.md#g023)/控制与历史[角色](APPENDIX_beginner_glossary.md#g084)；逐调用序号、名称、几何、参数字节及资源描述符 | 是否在比较同一个对象、同一组输入及同一调用；同名文件或函数不替代内容身份 | [ARCHITECTURE_V3_ZH.md:147–152、294](../../../ARCHITECTURE_V3_ZH.md#L147)，[逐调用记录:294](../../../ARCHITECTURE_V3_ZH.md#L294) |
| 逐调用中间状态 | 具名角色[ROLE](APPENDIX_beginner_glossary.md#g105)、累计声明写集D、完整工作区FULL，以及具名时点的六纹理POST | 错误从哪一次交接出现；某个角色一致不能补认整工作区，缺观测点不能补成[MATCH](APPENDIX_beginner_glossary.md#g104) | [ARCHITECTURE_V3_ZH.md:118–125](../../../ARCHITECTURE_V3_ZH.md#L118)，[4K RESULT_ZH.md:23–32](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L23) |
| 最终与跨帧状态 | FINAL原始输出、帧间history/carry、[reset](APPENDIX_beginner_glossary.md#g032)前后对应状态 | 最终效果的字节是否相等，以及CPU是否真正携带自己的上一帧状态；只有终图时不推认中间点 | [4K RESULT_ZH.md:19、34–44](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19)，[scene_cut RESULT_ZH.md:4、25–35](../../../experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md#L4) |
| 原语的具名输入/输出[位型](APPENDIX_beginner_glossary.md#g057) | 小型区分样本或限定输入域的函数结果与重复结果 | 某个算术候选能否解释实测位型；原语域与整网可达域分别判断 | [QMMA移植 RESULT_ZH.md:15–19](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#L15)；适用范围见[算术层](L3_qmma_e4m3.md#qmma-e4m3) |

这些是记录的对象与用途。不同捕获的时间点和完整性不同，须随每个结果保留几何、帧、填充、构建、参照及比较范围；“采到”也不等于CPU已经复现。[ARCHITECTURE_V3_ZH.md:72、125](../../../ARCHITECTURE_V3_ZH.md#L72)。教师强制检查与CPU自有状态连续推进的区别沿用[现有词表](APPENDIX_evidence_history.md#project-terms)。

<a id="discriminator"></a>
## 用复现来判别计算假说

本串把“CPU重建在已测范围成立”的门设在实际字节上：CPU从绑定的输入/前态重新计算，逐launch按已观察的ROLE/D/FULL/纹理范围对照，同时核对FINAL；声明连续链时，还必须由CPU自己的状态推进到下一调用或下一帧。只有FINAL记录时，结论就停在FINAL；没有原生观察的点保留NOT_OBSERVED。该区分来自[ARCHITECTURE_V3_ZH.md:72、118–125](../../../ARCHITECTURE_V3_ZH.md#L72)和[具名连续链记录:19–32](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19)。

这是比视觉相近或允许容差的数值接近更强的判据：字节比较连最末位、零的符号与[发布](APPENDIX_beginner_glossary.md#g091)编码都要求一致，不能让小误差由显示或误差阈值遮住。逐launch又比单独终图多了一层判别：错的取数/写回布局、[量化](APPENDIX_beginner_glossary.md#g061)位置、累加分组、舍入/[FTZ](APPENDIX_beginner_glossary.md#g068)、纹理过滤或历史携带，只要在被测输入及已比较点造成一个字节差异，就会使该范围的假说失败；未触发差异的等价假说仍可能同时通过。具体保留的发布点见[INDEX计算口径](INDEX.md#计算口径)，实际FULL/POST/FINAL分母见[4K RESULT_ZH.md:23–46](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L23)。

例如，场景控制记录中改变所消费的历史或reset参数确实使FINAL不同，而reset隔离控制按预期保持相等；这些对照使“只是保存图像碰巧相同”或“根本没消费相应状态”的特定解释受到检验，结论仍只限已测控制。[experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md:27–36](../../../experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md#L27)。多帧结果账留在[证据附录](APPENDIX_evidence_history.md#history-evidence)。

<a id="tiers"></a>
## 怎样读证据标签

measured、census、inferred与NOT_OBSERVED的含义统一指向[现有证据词表](APPENDIX_evidence_history.md#project-terms)，不在此另立一套等级。每项还要读构建归属：M实测、M的census对应、[M2](APPENDIX_beginner_glossary.md#g107)新数值和独立child candidate不能互换，[ARCHITECTURE_V3_ZH.md:1519–1523](../../../ARCHITECTURE_V3_ZH.md#L1519)；[确定性页](L0b_determinism.md)据此逐项标注。

<a id="limits"></a>
## 字节相同的边界

测试证明的是指定版本、输入、前态、参数、填充和比较范围上的相等，不能把有限样本量换成“所有输入都相等”，也不能因出口相同就认定唯一网络分解、训练语义或一般内存/调度正确。项目现行措辞要求明确保留拒绝、未知与失败，[ARCHITECTURE_V3_ZH.md:76–80](../../../ARCHITECTURE_V3_ZH.md#L76)。

[全域](APPENDIX_beginner_glossary.md#g111)目标有单独记录，当前仍为**NOT_ESTABLISHED**：架构状态列出根0/12、完整状态转换0/92,992和37条硬件前提，[ARCHITECTURE_V3_ZH.md:7](../../../ARCHITECTURE_V3_ZH.md#L7)；条件证明骨架要求软件、布局、域、翻译、终止与硬件假设分别闭合，当前两类都有开放项，[docs/arch-v2/08_proof.md:40](../../arch-v2/08_proof.md#L40)。有限的原语一致、158次调用覆盖和具名连续链均不能代替该目标。

本页仅整理保存记录；本轮没有新增原生捕获、CPU模型或连续链运行。
