# L0b 确定性与可复现性

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

[整串目录](INDEX.md) · [对象与方法](L0a_object_method.md) · [一帧接线](L0_frame.md) · [证据词表](APPENDIX_evidence_history.md#project-terms)

本页收集既有记录对“固定输入、控制、[资源](APPENDIX_beginner_glossary.md#g079)与前态产生可复现字节”的支持，结论逐项受观察范围限制。统一M、发布子[封存](APPENDIX_beginner_glossary.md#g103)[M2](APPENDIX_beginner_glossary.md#g107)和后续child candidate分别记账；M的实测不能自动转成M2的新测，census也不能代替数值运行。[ARCHITECTURE_V3_ZH.md:1519–1523](../../../ARCHITECTURE_V3_ZH.md#L1519)。

<a id="driver"></a>
## 驱动与租机身份

**【measured，历史摘要；未绑定M／M2／child candidate数值门】** 旧记录报告：616.92与591.86下同标签的原生输出逐字节相同，[README_ZH.md:20](../../../README_ZH.md#L20)；[架构](APPENDIX_beginner_glossary.md#g078)文档将它限定为“陈旧、单项”的驱动维度记录，[ARCHITECTURE_V3_ZH.md:1391](../../../ARCHITECTURE_V3_ZH.md#L1391)。在本轮指定来源及其明确引用中，**这两版驱动对应的原始捕获配对表、完整输入/参数同一性门及M/M2复测未见记录**。因此只保留该历史观察，不能据此宣布所有驱动、全部中间[状态](APPENDIX_beginner_glossary.md#g002)或任意输入均相等。

**【census，租机规则；原生参照层，非M／M2／child candidate数值门】** RTX 5090 D V2确实出现在租机记录中，现场名称、UUID、驱动580.97与sm_120均有登记；用户的租机身份规则是名称、UUID、驱动只记录，不凭其字符串拦截，真正[准入](APPENDIX_beginner_glossary.md#g101)看冻结正对照的结果字节。[LATEST_ZH.md:130](../../../LATEST_ZH.md#L130)。

**【measured，原生参照层；非M／M2／child candidate新验收】** 后续归档复核记载，5090 D V2／580.97有七次运行完成七项门控，均与5090／591.86基准在[FINAL](APPENDIX_beginner_glossary.md#g105)层逐字节一致；报告同时保留“仅一块卡、冻结期望出处未在该轮回到原始采集核对”的限制。[experiments/kb-r04-register-r01-20261011-claude/RESULT_ZH.md:7–14、65](../../../experiments/kb-r04-register-r01-20261011-claude/RESULT_ZH.md#L7)。另一个具名兑现记录也将该设备的正控与预测兑现明确限定为帧0、终图层，[experiments/b1-preregistered-bright-scene-redeem-20261018/RESULT_ZH.md:26–30](../../../experiments/b1-preregistered-bright-scene-redeem-20261018/RESULT_ZH.md#L26)。这些记录支持该次设备配置的正控，不能推广到所有SKU或未来驱动。

<a id="workspace-fill"></a>
## 00与A5填充究竟检验了什么

**【measured on M】** 4K自有CPU连续链对每种填充各从[reset](APPENDIX_beginner_glossary.md#g032)运行f0→f1→f2；两种填充的三张终图分别与同一原生参照相等，每张66,355,200 B。该轮绑定M=9d0a4593…，没有注入原生中间状态。[experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md:19、34–40](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19)。

比较对象必须分清：00一侧按报告比较FULL；A5一侧在早期比较累计已写区与原生相等、未写[补集](APPENDIX_beginner_glossary.md#g093)仍为A5。两种填充从f0 L99起才累计覆盖整个763,062,272 B[工作区](APPENDIX_beginner_glossary.md#g082)，f1/f2从[L0](APPENDIX_beginner_glossary.md#g081)起已全覆盖；两个f0 L0 FULL均为[NOT_OBSERVED](APPENDIX_beginner_glossary.md#g104)。[experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md:32](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L32)。较早1080记录也明确：两填充累计声明写集的digest在158/158点相同，FULL只在L99–L157的59点相同，[ARCHITECTURE_V3_ZH.md:118–125](../../../ARCHITECTURE_V3_ZH.md#L118)；该旧数值不在此改记为M2双填充实测。

**【inferred from measured on M及旧捕获】** 这些对照排除了“在所测轨迹上，把00换成A5会改变已比较输出”的假说，支持所测结果不依赖这两种初值的偶然选择；它们不证明从未读取未初始化区域，也不排除读取后被覆盖、被屏蔽或恰好不影响结果，更不证明对任意初值、输入、[别名](APPENDIX_beginner_glossary.md#g092)或调度都独立。项目原定义已将两填充明确限定为有限证伪检验，[ARCHITECTURE_V3_ZH.md:121–125](../../../ARCHITECTURE_V3_ZH.md#L121)；读写/同步证明边界另见[附录](APPENDIX_evidence_history.md#project-terms)。

<a id="repeat"></a>
## 重复运行与同捕获复现

**【measured，历史原生捕获；非M／M2／child candidate门】** REDG双运行检查取得787个检查点配对零差，包括帧0的157点及帧1/2各158点；但原报告为INCONCLUSIVE_INPUT_PARAMS_GATE，原始P1/P2上传缺失、部分参数差异超出预声明例外，所以它没有建立“同输入、同参数”的原生可复现结论。[experiments/parity-redg-double-run-1080-r01-20260929-codex/RESULT_ZH.md:7–22](../../../experiments/parity-redg-double-run-1080-r01-20260929-codex/RESULT_ZH.md#L7)。后来的census将四份帧0可比捕获、换序[负控](APPENDIX_beginner_glossary.md#g102)与事后重定位更正并列，仍保留原上传只到catalog SHA的缺口，[experiments/parity-proof-structure-census-r01-20261006-codex/RESULT_ZH.md:15](../../../experiments/parity-proof-structure-census-r01-20261006-codex/RESULT_ZH.md#L15)。

**【inferred，原生顺序义务；不是M／M2／child candidate全域定理】** 有限重复相同不证明所有到达顺序、同步或可见性都相同；独立的顺序证书仍是另一项义务。[docs/arch-v2/08.01_redg.md:32](../../arch-v2/08.01_redg.md#L32)。

**【measured on M】** 4K f0/f1在同一已固定捕获上的n=2自有CPU复现，共632/632个[launch](APPENDIX_beginner_glossary.md#g080)对、1264/1264个非易变回执投影、7584/7584个状态SHA相同。比较保留所有数值SHA、路由与写集，仅按预先冻结的schema排除运行标识、计时等易变元数据；f2是新测量，不在n=2分母内，也没有声称原始JSON整文件相同。[experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md:44–46](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L44)。这是CPU对同一参照的复现，不能充当第二次原生GPU捕获。

<a id="scene-parameters"></a>
## 场景与控制变化

【measured，M记录／854a8724数值，非M2】scene_cut自有状态f0→f15的16张FINAL全部相等，f8切镜的reset隔离和历史敏感控制符合预登记结果，但逐launch原生FULL/[纹理](APPENDIX_beginner_glossary.md#g027)未观测；见[experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md:1–35](../../../experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md#L1)，结果账留在[附录](APPENDIX_evidence_history.md#history-evidence)。

【measured on child candidate，非M／M2】参数扰动在分别冻结的子候选上已有具名FULL与FINAL相等结果，原生history及部分中间点仍NOT_OBSERVED，不能合成同一最终seal的完整回归；见[experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md:5–22](../../../experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md#L5)，QA账全部留在[附录](APPENDIX_evidence_history.md#param-change)。

<a id="open"></a>
## 还没有建立的确定性范围

| 层级与构建归属 | 尚缺什么 | 已有记录与边界 |
|---|---|---|
| census／M2 | M上的4K三帧、双填充、n=2不自动属于M2；同等级M2复测未见记录 | M2新数值范围为1080/1440 f0及4K L0–L99；其余普查单列，[experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md:82–95](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L82) |
| census／child candidate | 实例切换/feature rebuild、312 B后处理、剩余独立S157、320×240及同一最终seal全回归尚未建立；原生history与缺失FULL不计MATCH | [experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md:22](../../../experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md#L22)；实例切换后续只读定位仍以[payload](APPENDIX_beginner_glossary.md#g097)未找到而STOP，[stage_d2_followup/RESULT_ZH.md:1–5](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d2_followup/RESULT_ZH.md#L1) |
| census／M及其数值前代 | 1440 f4/f5、4K f3+、300帧CPU及其他改参流尚无同等级链门；任意新分辨率不在已测三档准入内 | [ARCHITECTURE_V3_ZH.md:1415–1416](../../../ARCHITECTURE_V3_ZH.md#L1415)；4K其他输入/几何/平台与f3+仍NOT_RUN，[4K RESULT_ZH.md:61–63](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L61) |
| inferred／跨M、M2与child candidate的宣称边界 | 所有驱动/SKU、任意初值、任意调度与全部输入的确定性未由这些有限结果确立 | [ARCHITECTURE_V3_ZH.md:1409–1416](../../../ARCHITECTURE_V3_ZH.md#L1409)；条件[全域](APPENDIX_beginner_glossary.md#g111)证明仍[NOT_ESTABLISHED](L0a_object_method.md#limits) |

本页是保存记录的整理，没有新增GPU、CPU模型或连续链运行。
