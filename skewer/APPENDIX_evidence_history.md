# 附录：证据历史、构建身份与保存回执

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

<a id="formula-open-r04l"></a>
## 公式覆盖：未闭合项

r04l按审计原行ID复核，[1846行分类及226项排名账](examples/r04l.classification.json)固定原审计[SHA](APPENDIX_beginner_glossary.md#g103)：默认1824行从 CLOSED/TABLE/PARTIAL/MISSING/[UNKNOWN](APPENDIX_beginner_glossary.md#g104)=1606/110/100/2/6变为 **1706/112/0/0/6**；变体22行为18/1/0/0/3。默认100行新增[闭式](APPENDIX_beginner_glossary.md#g020)、两行补全[DAG](APPENDIX_beginner_glossary.md#g089)合同后转TABLE，59行补表规格仍TABLE；V01.02仅修范围，[宿主](APPENDIX_beginner_glossary.md#g096)生成继续UNKNOWN。family最弱项为4/34/0/0/6，仍**4/44闭式族**（覆盖5/158位置），不能把158/158导航覆盖叫公式全闭合。

r04n当时增量：[qkv八字段闭式及留出表证据](L3_split16_window.md#qkv-closed-form-r04n)使F18.02/.03/.04/.39四整行TABLE→CLOSED，当时为 **1710/108/0/0/6**，变体与family计数不变。[当时分类账](examples/r04n.classification.json)保持1846行和226项排名的原分母：F18.05合并行内shfl_idx、psel已CLOSED，thread_class因1080缺字段、冻结假说在留出失败而仍TABLE，按最弱子项汇总该行继续TABLE。8/9是字段计数，不能当作8个审计整行或闭合整个F18族；F18.36独立bias排序继续UNKNOWN。


r04o分类记录：[逐行和逐字段账](examples/r04o.classification.json)维持原1846行分母；F16–F23共178行由146 CLOSED / 31 TABLE / 1 UNKNOWN变为 **167 / 10 / 1**，21个完整地址行由TABLE转CLOSED。默认1824行当前为 **1731/87/0/0/6**；变体22行仍18/1/0/0/3。原审计行最弱项得到6/44 CLOSED族，但F20/F21的可选thread_class没有独立审计行，将类别字段纳入后仍为 **4/44**；这些额外字段继续TABLE。F03–F15共816行保持 **787 CLOSED / 28 TABLE / 1 UNKNOWN**：28行是RSQ/RCP与F03噪声的函数值依赖，不是地址表；TIN源码索引为[code-transcribed index formula](L3_tin_window.md#tin-code-transcription-r04o)，r03的新地址留出验证NOT_RUN。

| 剩余类型与ID组 | 闭合路线与原审计工作量 |
|---|---|
| split16地址与未覆盖项：F16.03、F17.03、F19.02/.04的r02历史失败；F34、L132与B31候选 | r04将历史失败分别分类为NON_PRODUCTION_VARIANT，接受图EXACT且原FAIL保留；具体12×12图无C++实际读取回执。[逐项及4K计数](L3_split16_window.md#r04-four-k-r04p)。L132的28候选为OUT_OF_SCOPE，B31的3个一维候选为NOT_RUN；不套r02公式。F23有36×60绑定表，4K输入帧身份未独立绑定。ViT F25–31与L100 F33.01–03仍需各自的坐标/动态来源证据。 |
| F18.05类别、F19/F20/F21类别及F22.05类别；完整DAG F22.08/F23.04 | qkv及F22的交换/选择子项已闭式；F19/F20/F21单类别假说FAIL，F22类别候选留出EXACT但仍表驱动。F22/F23的DAG与L56独立空间来源仍按表及原证据边界，不由地址等价升级。 |
| [RSQ](APPENDIX_beginner_glossary.md#g072)/RCP、[Radius](APPENDIX_beginner_glossary.md#g073)/Cos/Sin、LG2/EX2及V05.03函数值（所有函数TABLE行） | 端点/包装/身份规格已补；无表[位型](APPENDIX_beginner_glossary.md#g057)规则至少5–20人日，需结构证据/探针，闭合时间未知 |
| F18.36 [bias](APPENDIX_beginner_glossary.md#g052)、F42.50 B69坐标、F35.56 L133共享来源 | 独立head/query/key标签1–3日；B69独立坐标1–3日及设备数据；L133 epoch写→读血缘2–5日及数据，仍NOT_ADMITTED |
| F03.54/F43.50 [HMMA](APPENDIX_beginner_glossary.md#g065)零符号 | 保留480个反例；新零乘积/[seed](APPENDIX_beginner_glossary.md#g042)/[相消](APPENDIX_beginner_glossary.md#g071)/K16内部子段判别1–3日及采集窗口，不由CPU候选消除UNKNOWN |
| F44.47/V05.04 RGB联合域 | [饱和度](APPENDIX_beginner_glossary.md#g033)跨[通道](APPENDIX_beginner_glossary.md#g007)分支3–10日，完整闭合时间未知 |
| V01.02宿主生成；V06.01 312B ABI | 前者1–3日及数据；后者证据盘点1日、实现/验收3–10日及数据；312B继续拒绝/NOT_RUN |

r04l工作记录为现代码/绑定转写与小型Python检查；零新增[GPU](APPENDIX_beginner_glossary.md#g078)、模型、连续链、编译、远程或网络运行。[当时分类账](examples/r04l.classification.json)、[验证回执](examples/r04l.validation.json)、[扫描回执](examples/r04l.leak.json)保留历史身份。r04n仅新增[58个地址/索引单元复查](examples/r04n.qkv_samples.json)，只读导入冻结公式及两份存表；未重跑研究的全地图留出验证，数值DAG、全链及动态血缘证明均不升级。[当时检查](examples/r04n.validation.json)与[当时发布扫描](examples/r04n.leak.json)保留历史身份。r04o新增[13格地址例](examples/r04o.example.json)及源码索引转写；[当时检查](examples/r04o.validation.json)和[当时发布扫描](examples/r04o.leak.json)保留历史身份。r04p只整理已保存的地图结果与变体分类，不修改原审计行计数；[本轮验证](examples/r04p.validation.json)、[扫描](examples/r04p.leak.json)记录当前文档状态。

[整串目录](INDEX.md) · [一帧入口](L0_frame.md)

本页迁移 r04a 之前正文已有材料；文中“本轮”沿用原写作轮语境，不表示 r04a 新测。r04a 只改文档，GPU／模型／连续链运行均为 0。[原生行为](APPENDIX_beginner_glossary.md#g001)、CPU 表示与[验证记录](APPENDIX_beginner_glossary.md#g100)分开，旧 NOT_RUN、UNKNOWN、拒绝及失败均不改标。

附录脚本仍从仓库根目录运行；实算数字为原写作轮记录，本轮没有重跑。

<a id="qmma-history"></a>
## QMMA 候选裁决、跨架构对照与源码身份

迁自 [L3_qmma_e4m3.md](L3_qmma_e4m3.md)；以下是原写作轮保存的记录。

## 候选如何从 1,832 收敛到一个行为类

冻结候选名单与预测 → 采集硬件回答 → 独立比较器淘汰任一用例首差的候选 → 在存活名单中设计下一批判别。不能见到答案后再修改候选公式。

| 阶段 | 读到的用例与判别 | 剩余 | 证据及强度 |
|---|---|---:|---|
| 建银行，09-18 | 8 个命名模型 + 1,824 个参数组合，QMMA/HMMA 分开评估；24 个扫描例分出 291 类 | 1,832 | CENSUS：[核心探针 RESULT:23–54](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#第-2-项候选清单与离线评估) |
| sm_120 首轮，09-20 | 历史记载：24 扫描 + 5 实例用例进入预测，命中 1,206 成员类，收尾再淘汰 32 | 1,174 | INFERRED／历史转述：[旧 ARCH:548–550](../../../ARCHITECTURE_ZH.md)、[当时 Ada 验收回顾:62](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#4-对既有结论的影响)；首轮硬件复核/结案目录在本机当前路径缺失，本轮未重读原始收据 |
| 首批裁决，96 新例 | 冻结分区 61 / 168 / 945，实测选中第一类；EXACT 与旧 CORE 被淘汰 | 61 | MEASURED（保存记录）：[本轮 RESULT:3](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/RESULT_ZH.md)、[裁决:5–7](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/ADJUDICATION_ZH.md#裁决) |
| batch2，4 例 | 双遍为 0x5c02、0x5c02、0x5c02、0x5c00；剩 field、[value](APPENDIX_beginner_glossary.md#g067)、renorm 三类 | 8 | MEASURED：[resume2 RESULT:8–9](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume2-20261007/RESULT_ZH.md#正式裁决与规则) |
| batch3，2 例 | 双遍为 0x0001、0x0000，淘汰 value 与 renorm 类 | 3 个名字、1 个行为类 | MEASURED：[resume3 RESULT:8–16](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RESULT_ZH.md#正式裁决)、[RULE:5–29](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#正式结果) |

三个名字为 LOONG_HMMA、P_F25_opsum-field_cmax1_ctr1_zero_none_gfnone、P_F25_opsum-field_cmax1_ctr1_zero_none_gf-24。名称里的 HMMA 不改变本次输入格式。RULE:28–29 的代数理由是：有限 [E4](APPENDIX_beginner_glossary.md#g055) 乘积均在 $2^{-18}$ 格上，有限 F16 seed 在 $2^{-24}$ 格上；额外格点下限只在原本已能精确放置各项的细格区域起作用。三个名字在冻结有限模型域内相同，不是仅因样本未分开才归为一类。

状态为 UNIQUE_BEHAVIOUR_CLASS_WITHIN_FROZEN_FINITE_DOMAIN_BANK。它没有证明候选族穷尽、硬件对所有有限输入都相同、[NaN](APPENDIX_beginner_glossary.md#g069)/Inf/符号零/溢出完整合同或网络可达性；网络链一致也不能取代算术判别。

## sm_120 与其他架构

公式口径沿用 [V2-02-004](../../arch-v2/02.02_architectures.md#v2-02-004) 与 [RULE:31–40](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#跨架构比较)。本轮没有在 GPU 上重测；历史硬件记录与本轮沿用旧规则分别列出。

| 架构 / 输入路径 | 对齐、分组与发布 | 历史硬件记录 | 本轮范围 |
|---|---|---|---|
| sm_75：E4 [解码](APPENDIX_beginner_glossary.md#g061)成 F16，再用 HMMA | field F24；整 K8 一次 F16 [RN-even](APPENDIX_beginner_glossary.md#g059)；F16 [次正规](APPENDIX_beginner_glossary.md#g068)[字段指数](APPENDIX_beginner_glossary.md#g058) −14 | MEASURED：RTX 2060，79 个扫描例一名存活；[09-18 RESULT:56–71](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#第-4-项本机-hmma1688sm_75rtx-2060的结果) | 沿用旧规则；没有原生 E4 QMMA 门 |
| sm_86：E4 解码成 F16，再用 HMMA | renorm F24；K16 分两组 K8，各组 F16 发布后作下一组 seed | MEASURED：RTX A2000 Laptop，65/65 扫描、3,748/3,748 实例支持 GGGZ_HMMA；[Ampere RESULT:3–19](../../../experiments/parity-claude-ampere-probe-r01-20260921/RESULT_ZH.md#1-结果) | 公式沿用 RULE 对冻结 GGGZ 参数的解释，不是本轮新硬件裁决 |
| sm_89：E4 QMMA | field F13；K32 分两组 K16，各自 F16 发布 | MEASURED：RTX 4090 D 回传，GGGZ_QMMA 唯一；FP8 单一来源、未交叉验证；[Ada RESULT:25–35、64–67](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#2-判读用冻结比较器不另写) | 沿用旧公式/验收，不能扩大成跨卡[全域](APPENDIX_beginner_glossary.md#g111)证明 |
| sm_120：E4 QMMA | [field F25](APPENDIX_beginner_glossary.md#g066)；整 K32 末端一次 F16 发布 | MEASURED：96+4+2 个保存硬件例，最终一类；[移植 RESULT:15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) | 当前源码逐项对齐 RULE；本轮仅合成软件例 |

F13/F24/F25 不能只理解为有效位数差别：指数来源、分组、seed 是否参与最大指数、是否截断都影响输出，不能用 sm_89 的两组 K16 或普通精确[点积](APPENDIX_beginner_glossary.md#g051)替换 sm_120。

## 当前源码与历史记录的边界

- 本轮读取的代表头文件 10 份副本 SHA-256 相同：2b85ddfaeb37eb5d16560224def629ff29a043c4421b5b571749103b398e5452；这是源码身份，不是运行时构建身份。
- 10-07 RULE/RESULT 当时的“待 C++ 接入”针对旧树；当前头文件已有 field F25 分支。旧实验不因此改标。
- 移植的 1 亿随机例是对独立软件参考的比较，与 102 硬件例分开；旧移植轮当时的 4K 未运行不覆盖 ARCH 0.7 后来的具名结果。本主题不把后来整链一致推广成一般 QMMA 定理。

<a id="half-proof"></a>
## 整数 T1 与 T0 的组合证明、计数及身份

迁自 [L4_half_arith.md](L4_half_arith.md)；以下是原写作轮保存的记录。

[项目 RESULT_resume2_v1_ZH.md:3、9–28](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L3) 的 PROVED 覆盖全部 $2^{48}=281,474,976,710,656$ 个原始三元组，含异常类别和消息。证明连接是：

1. 完整 65,536 解码域，精确两肢合成、零号和 81 个最高位区间；T1 第一阶段证书 272/272 实际 UNSAT，独立 IEEE [binary64](APPENDIX_beginner_glossary.md#g056) 舍入连接到 T0。
2. T0 非 NaN binary64→half 转换与 IEEE RN-even 的连接；第二阶段 1,704 个真实 UNSAT 叶子，区间覆盖导出 5,002,132 个双符号编译代表。
3. 25,572,235,280,384 个非有限原始三元组另作类别证明与 448 个代表比较；与有限域互补。连同 253,952 个有限运行核对及解码代表，实际编译比较总数 5,322,068；该数量不是枚举了 $2^{48}$。

两个故意破坏实现的控制均被捕获：漏进位与 ties-away，见 [RESULT:32–35](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L32)。信任边界仍含 IEEE 正确舍入的 std::fma、最近偶数环境、double/整数 ABI、编译器、求解器和源码到模型对应；[RESULT:39–43](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L39)。历史 UNKNOWN 没有直接升级成 UNSAT。

本轮重读并核对 [composition-result-v1.json](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/composition-result-v1.json) 绑定的计划、7 个证据成员及两份冻结源码 SHA，均一致；未重跑求解器或完整证明驱动。T1 源码 SHA-256 为 78d251701c70818c5f67e14f380f1794a13e58cd8b3e98000bf6f668293cf557，T0 为 4acb7aecc4144713a569d139aa9a209d8b14848a7615ec02c7ca7fa87563fdf7。

<a id="attention-bindings"></a>
## attention 冻结图、解释器与 SHA 绑定

迁自 [L3_attention_softmax.md](L3_attention_softmax.md)；以下是原写作轮保存的记录。

<a id="graph-bindings"></a>
## 行为解释与冻结图的绑定

通用执行器定义原语，具体 DAG 定义[调用](APPENDIX_beginner_glossary.md#g080)顺序。以下只列本片实际读取的图与 SHA，不抄底层指令信息或模型系数。单行 JSON 的源码位置为 :1。

| 来源 path:line | SHA-256 | 本片用来核对什么 |
|---|---|---|
| [dlssnr-work/l62-epoch-fix-r02-claude/maps-base/t640/cy0/l62-templates-and-checks.json:1](F:/dlssnr-work/l62-epoch-fix-r02-claude/maps-base/t640/cy0/l62-templates-and-checks.json) | 8037735246b6c41c95a85191eb785bfd1d42043cca087ffe485c02f935a49205 | ViT half [仿射](APPENDIX_beginner_glossary.md#g049)、编码变换、10 轮[分母](APPENDIX_beginner_glossary.md#g048)和 [AV](APPENDIX_beginner_glossary.md#g077) 后[缩放](APPENDIX_beginner_glossary.md#g031)；另核对 cy1/cy2 绑定及三份 map SHA |
| [dlssnr-cpp-work/fam-attention-r01-codex/resume1/maps/H2160/cy0/l62-templates-and-checks.json:1](../../../../dlssnr-cpp-work/fam-attention-r01-codex/resume1/maps/H2160/cy0/l62-templates-and-checks.json) | 0f5d63fe9bb92f554b077731857780ca4b5e086622fb74118d148f3265145035 | 34 轮，尾轮补足 16 项的 F32 乘法→half 扣除；保留旧地图状态 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json) | e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea | split16 两组[查询](APPENDIX_beginner_glossary.md#g040)子片的 half 仿射、[归约](APPENDIX_beginner_glossary.md#g050)、RCP、[权重](APPENDIX_beginner_glossary.md#g048)发布及 AV |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L28-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L28-lane.wiring.json) | e9c276cfeb85801e701539aece1b008ef6d06f3ff8b4f4e45d1fd59a2d3940bd | [proj](APPENDIX_beginner_glossary.md#g038) 的通道投影/[残差](APPENDIX_beginner_glossary.md#g017)边界；没有另一次分数[归一化](APPENDIX_beginner_glossary.md#g048) |

T640 图 SHA 与 [s00-bindings.json 的 L62.epoch_wiring](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json)相符；split16 两图与 [s00-bindings-front.json 的 L27/L28 maps](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json)相符。参考解释器的 E 盘冻结副本与 F 盘源本轮 SHA 均为 f906820b2786a3ace14f5b65ed435e144301aa38e88a4d761d82a0e533bd961c。这些读取不声称新的全几何符号准入或完整 [ROLE](APPENDIX_beginner_glossary.md#g105) 生命周期证明。

<a id="norm-bindings"></a>
## norm 的冻结图、融合合同与身份

迁自 [L3_norm_nonfinite.md](L3_norm_nonfinite.md)；以下是原写作轮保存的记录。

| 本轮实际读取的图 / 合同 path:line | SHA-256 | 使用范围 |
|---|---|---|
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json) | e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea | split16 32 个 RSQ 统计依赖、尺度与发布 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/C27-contraction.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/C27-contraction.json) | a2f128a46633274bbc12977677512ab9c217572a6067da40440d57b0f7429610 | 64 个平方对融合合同项均选择第一项融合 |
| [dlssnr-work/vit-t640-numeric-r07-codex/maps/t640/l61-t640-map.json:1](F:/dlssnr-work/vit-t640-numeric-r07-codex/maps/t640/l61-t640-map.json) | 2421b94d7a1790b7deaab7fdaaa4136b3ebb3058050d8f6347558d9e9d23ea82 | ViT 32 个 RSQ 依赖、Q/K/V 各 32 个发布节点及不同尺度 |

L61 地址图 SHA 为 325b9666d3a868a3a0e37c87a1c10b9056aba87fb8681d1b0ed565dce57f44cc，与 [T640 绑定的 L61 行](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json)相符。split16 图/合同对应 [front bindings 的 L27 行](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json)。这些是结构与软件一致性检查；旧 MAP_CHECK_FAILED 和具名实例放行的边界保留，不升级为全几何的通用地图证明。 本轮另读 split16 的 L25/26/28/29/30/56/57 七个家族原型图，均没有 RSQ/RCP 节点；L27 的 32 个 RSQ 属于 Q/K，两个 RCP 属于后续[注意力](APPENDIX_beginner_glossary.md#g039)分母，后者见 [L3.attention-softmax](L3_attention_softmax.md#window-attention)。

<a id="norm-witness"></a>
## 027/028 的 CPU 统计首源与吸收见证

迁自 [L3_norm_nonfinite.md](L3_norm_nonfinite.md)；以下是原写作轮保存的记录。

| 已保存的 CPU 见证 | 能确定什么 | 限制 |
|---|---|---|
| 027 L6：37824+30464=68288→+Inf；028 L6：35552+30784=66336→+Inf | 两图最早被观察到的非有限 launch 均为 L6 的 norm32 正数求和 | 这些是统计中间值，不是模型系数；不是 GPU 最早时钟或唯一源头 |
| 027 L31 与 028 L27 的 norm 分支 | +Inf 经 RSQ(+Inf)=[+0](APPENDIX_beginner_glossary.md#g070)、有限分量乘零、E4 零在本分支内吸收 | 没有证明 L6 的同一个 Inf 字节一路存储并传播到 L27/L31 |
| 两图继续到 L61 | 分别出现新的有限 half 加法上溢、有限 half 平方上溢 | 旧 QKV 包装拒绝；不能用旧诊断给后续 L62–L157 编造结果 |

两图的输入各 8,294,400 个 half 字，非有限输入数为零；[L0](APPENDIX_beginner_glossary.md#g081)–L6 的被观察前缀[工作区](APPENDIX_beginner_glossary.md#g082)与六[纹理](APPENDIX_beginner_glossary.md#g027) SHA 均与接受参考相同。[诊断 RESULT:7–25](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7) 证明 CPU 观察路径保持这些输出，不能据此宣称 GPU 的内部位型已经测到。旧 45 张全在 L27/L31 守卫停止，也不证明每张的首源都已经追到同一 L6 节点。

<a id="a1-ledger"></a>
## A1 的分组计数、拒绝清单及构建身份

迁自 [L3_norm_nonfinite.md](L3_norm_nonfinite.md)；以下是原写作轮保存的记录。

| 旧判定 | 图数 | [A1](APPENDIX_beginner_glossary.md#g107) FINAL MATCH | A1 拒绝 |
|---|---:|---:|---:|
| MATCH | 99 | 99 | 0 |
| INVALID | 45 | 42 | 3 |
| UNCOMPARED | 3 | 3 | 0 |
| 合计 | 147 | 144 | 3 |

旧 45 个 INVALID 的保护版停止点为 L27 共 33、L31 共 12，见 [ARCH 0.7:989、1008–1014](../../../ARCHITECTURE_V3_ZH.md#L989)。本轮只读核对 [image_verdicts_final.json](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/image_verdicts_final.json) 的 147 个唯一键及 prior→status 计数，得到上表；没有重新打开图像目标或运行链。

剩余三张都是 ViT attention 的 QMMA half 上溢拒绝：

| 图像登记名 | 拒绝 launch | 判定 |
|---|---:|---|
| heldout-091-saturation_blocks-02 | L77 | INVALID_REFUSED，QMMA half overflow，无终图 |
| heldout-093-saturation_blocks-04 | L97 | 同上 |
| batch3-052-saturation_patches-1920x1080 | L72 | 同上 |

守卫位于 [qmma_sm120.hpp:65–70](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L65)，生产调用默认执行；详见 [A1 RESULT:46–56](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L46)。这三张不算 MATCH，也不能因为其他同类别图可通过而统一豁免。

**源码身份须分开。** A1 构建为 14267c09ecef6a7a34068a42b8674da105c70370d199886d83183c50753fdcb3，父统一 M 为 9d0a4593…，范围为 1080 单帧 f0。公开 M2 的 [split16:272](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272) 与 [ViT:180、200](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L180) 仍可读到原有限域守卫；A1 结果使用上面的独立替换源与二进制。不能把 144 图结论写成 M2、1440、4K 或多帧的新验收。[ARCH 0.7:1425](../../../ARCHITECTURE_V3_ZH.md#L1425) 同样区分这两个身份。

<a id="padding-bug"></a>

不能混淆两种事件计数：早期解释器图报告 131,072 次同值零写，覆盖 4096 个不同 4 B 地址、每处 32 次；后来的具类型发布合同把同值重复写归并成 4096 个零覆盖项。地址并集与发布顺序相同，不能把前一个数字称作不同的字节数。早期计数与地址[负控](APPENDIX_beginner_glossary.md#g102)：[attention 移植 RESULT:143–146](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L143)。原生快照里的零值本身不能证明零写确实执行过；这需要读写事件、顺序绑定和关闭负控共同支持。
## L62 零覆盖收集器漏项与修复历史

迁自 [L3_workspace_map.md](L3_workspace_map.md)；以下是原写作轮保存的记录。


### L3.workspace-map.padding-bug 为什么向量覆盖通过仍会漏掉 16 KiB

- 是什么：生成器已发出零写事件，收集器与执行器却只保留普通输出事件，导致[副作用](APPENDIX_beginner_glossary.md#g094)缺失。
- 输入 → 输出：原先看似完整的普通[向量](APPENDIX_beginner_glossary.md#g076) maps → 带值、地址、实例与阶段的零写绑定。
- 怎么算：
  ~~~text
  1. 原生普通输出已经覆盖物理 P 行；尾 tile 另有 4096 个四字节零写。
  2. 缺陷收集器只把普通输出纳入 templates/maps；保留零写“计数”却没有可执行项。
  3. CPU 因而发布了 computed padding；4K L62 首差仅为 WS [665036800,665053184)。
  4. 修复将零写作为独立 typed 操作接入，在 output 发布后、release 前执行。
  5. 验证器检查全部地址、值、宽度、尾 tile、epoch、实例与先后次序。
  6. 独立关闭 zstore 的 L62 负控，再次得到同一 16,384 B 差异；六纹理仍 MATCH。
  7. 保持开启的旧独立构建从自有 own61 续跑 L62–L91，共 30 次调用 MATCH。
  ~~~
- 数值规则：原生前态和后态该区都是零，单看快照无法区分“未写”与“同值覆零”。L63 的 typed [readset](APPENDIX_beginner_glossary.md#g093) 证明该区全部 16 KiB 真被读取，不能称无人消费的废 [padding](APPENDIX_beginner_glossary.md#g085)。零写位于普通输出[角色](APPENDIX_beginner_glossary.md#g084)内部，区间并不会新增字节，所以 WriteSet / CumWrites 元数据不变也不能代替数值与阶段验证。
- 为什么这么算：先前只验证主要向量出口，遗漏了与输出重叠的标量副作用；这说明覆盖检查需要同时约束值和时序。
- 我们怎么知道：MEASURED，[c12 RESULT:7–9](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7)；CONTROLLED，[verify_zstore_p.py:3–49](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/a07/verify_zstore_p.py#L3)覆盖错实例 / 参数 / 地址 / 值 / 宽度 / epoch / 阶段、漏写、重复写、提前 release 等负控。
- 往下：[现行发布接线](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177)、[WR 的边界](L3_workspace_map.md#wr)。

上述旧诊断保留 MAP_CHECK_FAILED，诊断轮本身未修复或运行下游；旧独立构建的 L62–91 门也不自动转移给后来的合流 seal。后来 M2 的 4K L60–99 门及统一 M 三帧链另有[具名记录](L3_workspace_map.md#evidence)，并未把旧轮的 NOT_RUN 改为通过。全局副作用 / 别名 / 生命周期定理仍未建立。

<a id="repack-evidence"></a>
## repack 原生格、软件维度扫描及非零钉住率

迁自 [L3_workspace_map.md](L3_workspace_map.md)；以下是原写作轮保存的记录。


## repack 怎样验证：18 格与 8,082 项分别是什么

| 证据 | 核对对象 | 范围 |
|---|---|---|
| [native_validate_new_formula.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/native_validate_new_formula.json) | 18/18 原生输入 / 输出格匹配，4K L58 padding 另比 | L58/L99×1080/1440/4K×f0/f1/f2 |
| [M2 RESULT:9、28–32](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#3-repack-支持域回答-b1-要求)及[测试程序](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/tools/repack_equiv_test.py) | 旧 / 新模块在 8,082 个维度×方向记录上结果一致 | rows、cols=1..64，略过 rows×cols×256>900000 的格；包含拒绝结果 |
| [equiv_old_maps.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/equiv_old_maps.json) | 本轮只读计数：8,082 项中 **440 个有效映射哈希、7,642 个拒绝结果** | 文件另有 4 项线程 / 队列调度对照、3 项参数负控，共 8,089 条；不是 8,082 个有效硬件形状 |
| [native_pinning_coverage.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/native_pinning_coverage.json) | 原生非零内容独立钉住映射位置；与公式冲突为 0 | 1080 84.375%、1440 100%、4K 94.4444%；其余为全零区，不能称所有位置都由非零内容唯一钉死 |

原报告把 8,082/8,082 简称“映射哈希”；按保存测试的实际类型拆分如上。18 格是原生字节对照，维度扫描是旧 / 新软件模块结果对照，数学接受域又更大；三者不互换。新源码还逐项检查映射双射，这约束索引本身，不等于硬件遍历完整接受域。

<a id="map-identity"></a>
## L57 的 1440 地址图身份

迁自 [L3_workspace_map.md](L3_workspace_map.md)；以下是原写作轮保存的记录。

1440 地图 SHA-256 为 cce87defbdde26cb2a0a4d4cf76c0ece8dbb07cf7ac2140354456c080f89570c；这份外部本地副本是几何绑定的历史来源，不能仅凭路径名认定它就是全部 M2 部署资产。

<a id="b0-evidence"></a>
## B0 采样实验、融合诊断与历次验收

迁自 [L3_b0_input.md](L3_b0_input.md)；以下是原写作轮保存的记录。

<a id="evidence"></a>
## 我们怎么知道：微基准、失败轮次与 B00 门分列

| 实际实验轮次 | 保存结果能支持什么 | 限制 |
|---|---|---|
| parity-video-tex-filter-r04-20260928-codex；[冻结来源 STATUS:723](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/STATUS_ZH.md#L723) | sm_75 / sm_86 的联合8位分数权重（1/256定点小数格）微基准 10,436 分量零差；接入后 320 q25x 从 27,573→203 B，1080 f1 从 765,813→73,119 B | 仍 DIFF；本机未保留该原轮目录，数字据冻结摘要，不伪称重读原始微基准输出 |
| [parity-video-sm120-tex-filter-r06-20260928-codex](../../../experiments/parity-video-sm120-tex-filter-r06-20260928-codex/RESULT_ZH.md#3-冻结假设族训练拟合) | 180 个预登记假设无训练集全 MATCH，四个 S2 留出件仍 DIFF；1080 f1 为 25,390 / 7,629 B | 该轮不能唯一归因纹理；其 f2 因资源锁 NOT_RUN 的原记录保留，后来的另轮结果不改写它 |
| parity-video-d3d12-tex-r07-20260929-codex；[冻结来源 STATUS:737](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/STATUS_ZH.md#L737) | 本机 2060 的 D3D12 / CUDA 56 组、603,232 分量；[RGBA16F](APPENDIX_beginner_glossary.md#g028) 48 组相同，差异限 RG16F 缺失 W 分量 | B0 [MV](APPENDIX_beginner_glossary.md#g023) 只读 x/y；不能从 Turing 外推 sm_120；该原轮目录本机未保留，依据为冻结摘要 |
| [parity-proof-gpu-sweeps-r01-20261007-codex / Item C](../../../experiments/parity-proof-gpu-sweeps-r01-20261007-codex/ADJUDICATION_ITEMC_FULL_ZH.md) | 后续 sm_120 的 112 CUDA+63 D3D12 配置共 175/175 的旧坐标前缀匹配 sm_75 | 通常每配置 2,693 坐标，load 控制为 32；新增坐标没有同坐标参照，不是任意 raw32 / 二维全域证明，原生运行时[描述符](APPENDIX_beginner_glossary.md#g088)仍 UNKNOWN |
| [parity-video-b00-native-divergence-r01-20261006-codex](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证) | 修正原生 [FMA](APPENDIX_beginner_glossary.md#g063) 边界的隔离 B00，1080 f0、f1、f2、f3 的 [full](APPENDIX_beginner_glossary.md#g018) / pool 各 0 B 差 | [teacher-forced](APPENDIX_beginner_glossary.md#g106) 单 launch；该轮 f4/f5 为 NOT_RUN_MISSING_NATIVE_HISTORY，f3 历史由另一捕获的 f2 id9 提供，不是同捕获 id6 实测 |
| [parity-cpp-1440-multiframe-r01-20261017-claude](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | 854 构建两填充的 1080 f0–f5 与 1440 f0–f3 自有链，包含各帧 B00 launch 门 | 1440 f1/f2 六纹理只在 5 个原生时点比较；f3 有输入平移和自有 f2 检查点跨进程接缝；不是 M2 全部多帧新测 |
| [parity-cpp-4k-multiframe-r01-20261022-codex](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19) | 统一 M 两填充，各单进程 f0→f1→f2，包含各帧 B00；f2 实际使用本 fill 自有 f1 历史 | A5 的早期门为已写区等于原生 / 补集保留 A5；4K f3+、独立历史扰动研究未运行；不由链门推出任意内容或硬件等价 |

**25 KB 残差的根因。** 119 项调试导出把中间乘法变成必须保留的舍入点，阻止原生坐标链的 FMA 融合。关闭运行时 debug 开关仍使用同一编译产物，所以 sm_75 / sm_86 / sm_120 回放与 CPU 可以四方相同，同时共同偏离原生。删去调试导出后的静态重编译恢复融合，隔离原型 full / pool 才在 f0–f3 归零；该轮没有新增 GPU 执行。结论来自[原生分歧 RESULT:9、24–28、39](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据)，不是从 R06 的过滤拟合失败单独推出来的。

旧的 [reset](APPENDIX_beginner_glossary.md#g032)-only / 固定 1080 说明按其原轮日期保留；当前 b00.hpp 的 [guard 4](APPENDIX_beginner_glossary.md#g109) 与具名多帧门另有直接来源。上述门约束输出轨迹，不证明内部结构唯一，也不使尚拒绝的 p5 自动通过。

<a id="attention-evidence"></a>
## attention 保存的门、负控与旧失败

迁自 [L3_attention_softmax.md](L3_attention_softmax.md)；以下是原写作轮保存的记录。


## 保存的原生门、负控与未决范围

| 对象 | 已读记录与判定 | 能说明的范围 |
|---|---|---|
| ViT 八次 attention | [RESULT:115](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L115)、[s02-validate-resume5.json](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/s02-validate-resume5.json)：1080 f0 的 L62/67/72/77/82/87/92/97，output 与 release63 都 MATCH | MEASURED，逐 launch 输入和参数绑定的原生 / Python / C++ 三方对照；不是连续链 |
| 跨几何历史门 | [同 RESULT:275–282](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L275)：72 格中 71 格 THREE_WAY_MATCH；旧 4K f0 L92 为 1 B 差异、NOT_ESTABLISHED | 保留旧结果；旧 QMMA 候选下的敏感边界不作为现规则的全域证明，原语裁决见 [L3.qmma-e4m3](L3_qmma_e4m3.md#候选如何从-1832-收敛到一个行为类) |
| 4K L62 零覆盖 | [c12 RESULT:7](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7)：关闭 zstore 的独立 L62 负控复现工作区 [665036800,665053184) 的 16,384 B 差异，六 POST 仍 MATCH；开启后从自有 L61 接续 L62–L91，末端 MATCH | CONTROLLED，确实区分“无零覆盖”和“有零覆盖”；POST 相同不足以宣称完整工作区相同 |
| 后来的固定 4K f0 链 | [continuation6_RESULT_ZH.md:1–10、范围段](../../../experiments/b1-arch-v3-refresh-r01-20261023-codex/continuation6_RESULT_ZH.md#L1)：L0–L157 每 launch 全工作区和六 POST 相同，包含这八次 attention | MEASURED，按 SHA 自有检查点分段、新进程接续的特定构建；不能拿来改写上面旧 L92 记录，亦不推出异步中间时序唯一 |
| split16 qkv | [Step2a RESULT:5–23](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L5)、[s03-qkv.json](../../../experiments/parity-cpp-step2a-r01-20260928-codex/s03-qkv.json)：L103/107/111/115/119/123/127/131，1080 f0 八格、1440/4K 各三帧 24 格，共 56/56 MATCH | MEASURED，包含融合 attention 的整 launch 对照；原 MAP_CHECK_FAILED 与限域放行原样保留，不称 56 份通用地图证明 |
| [TIN](APPENDIX_beginner_glossary.md#g011) 窗口实现 | [TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3)：1080 f0 L3/7/11/18/24/133/134/151，8/44 三方全工作区相同；该轮其余 36 个 NOT_RUN | MEASURED，八个具名整 launch；后续固定 4K f0 链证据另列，不能倒灌改成此轮 44/44 |
| 偏置索引负控 | [RULEDOUT-ATTENTION-FRAGBIAS:23–31](../../../knowledge/RULED_OUT_ZH.md#ruledout-attention-fragbias)：2/4/8 头、具名 B9/B15 的片内序假设分别约 71% / 74% 失配，逻辑序同时零差 | CONTROLLED，原登记范围为 sm75 / branched_window；不外推到 1 头、16 头或当前全部家族 |

没有找到可按原登记引用的“[libm](APPENDIX_beginner_glossary.md#g074) [softmax](APPENDIX_beginner_glossary.md#g047) 替代”专名 RULED_OUT 条目，因此不虚构已跑的原生负控。本片用实际运算图和下面的合成例说明标准 softmax 的运算与结果不同；RCP 不能随意换 libm 的位型理由见 [L4.mufu](L4_mufu.md#edges)。优化 C++ 可改变独立任务的循环组织；上述 half 和 QMMA 依赖次序保持，只有精确整数部分满足对应规则时才允许[重排](APPENDIX_beginner_glossary.md#g019)。

<a id="norm-evidence"></a>
## norm 分层证据：原值、软件控制、检查点与终图

迁自 [L3_norm_nonfinite.md](L3_norm_nonfinite.md)；以下是原写作轮保存的记录。


## 证据支持到哪一层

| 层级 | 已读证据 | 能支持的结论与界限 |
|---|---|---|
| CPU 首源与局部依赖 | [传播诊断 RESULT:7–47](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7) | 027/028 的 L6 首源和 L27/L31 局部吸收；实际 NaN 可达、未观察区间的非有限次数仍 UNKNOWN |
| RSQ 特定输入原值 | [原表边界](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/s11-old-table-boundary.json)、[A1 RESULT:39–44](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L39) | RSQ(+Inf)=+0 的已有双遍硬件事实；不推出一般多操作数非有限组合全域相同 |
| 软件 helper 与阈值负控 | [A1 RESULT:44](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L44) | 对独立 _Float16 参照 8,593,757 项零失败；阈值改错负控 2698 项失败。属于软件门 |
| A1 逐检查点 | [A1 RESULT:25–30](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L25) | G1 两图各八点，共 16 个 FULL 工作区；G3 五图各八个 C8 窗口，共 40 个 FULL 工作区相同；输入来自 R04/C8 会话平移，属于 relocated byte-identical |
| A1 终图 | [A1 RESULT:18、32–36](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L18) | 144/147 终图相同、3 拒绝；C8 六纹理仍 NOT_RUN_RAW_FILES_ABSENT；终图相同不证明原生内部也形成 +Inf |
| norm 调用者的原逐 launch 门 | [TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3)、[split16 RESULT:5–23](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L5)、[ViT R09 RESULT:5–27](../../../experiments/parity-vit-t640-numeric-r09-20260925-codex/RESULT_ZH.md#L5) | 具名实例的整体输出对照支撑这些有限路径；不能把旧逐 launch 门升格为 A1 新门或所有输入证明 |

A1 的后果字节支持限定语义，但一般 half 多操作数组合、NaN 载荷规则、GPU 中间 Inf/NaN 是否可达仍按原报告留 UNKNOWN。特别是“原生内部也产生 +Inf 并被 RSQ 吸收”属于 INFERRED；独立 RSQ(+Inf) 原值已测与网络内部是否实际达到该键是两个断言。

<a id="history-evidence"></a>
## 尾段三档多帧、sceneA 与切镜的结果账

迁自 [L3_b70_history_output.md](L3_b70_history_output.md)；以下是原写作轮保存的记录。


## 多帧证据：比较对象与边界

| 具名记录 | 已测结果 | 保留边界 |
|---|---|---|
| [1080 门 2 / 854](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | f0–f5，两填充，各 948 条事件全 MATCH；含每帧 B70 / 复制 / 显示 | 对 G0b FULL / 六纹理与原生累计声明写集/roles 的比较分列；不是所有点都有原生 FULL |
| [sceneA 演练 Stage R，10-24](../../../experiments/parity-cpp-exam1080-r01-20261023-codex/STAGE_R_ZH.md#实测结果与时间) | 1080 f0–f31，32/32 FINAL SHA 与获准 R02 catalog 相同；fill00、12 线程，单 predictor、自有状态，5056 次调用 | FINAL_SHA256_ONLY；不是逐 launch 原生状态观测；f16–f31 [params](APPENDIX_beginner_glossary.md#g083) 按冻结模板仅改 B0 帧字合成，非原生捕获参数 |
| [1440 多帧](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | f0–f3 两填充自有链；f0–f2 单进程，f3 从自有 f2 检查点续接 | f1/f2 六纹理只有五个原生时点；f3 输入经过会话平移、有跨进程接缝；f4/f5 NOT_RUN |
| [4K 三帧，10-22](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19) | 统一 M 两填充，各单进程 f0→f1→f2；948 个调用、946 个已观察 FULL、5688 个六纹理 POST | 两个 f0 L0 FULL 未观测；A5 早期比较已写区 / 保留补集；f3+ NOT_RUN，M2 身份不与 M 新测混写 |
| [scene_cut 数值轮](../../../experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md#r1-结果2026-10-20决定-35) | 16 帧自有链 FINAL 逐字节相同，f8 reset；C1–C5 如上 | FINAL only，无逐 launch 原生 FULL / 纹理；不是 midstream f4+ 或 p5 通过 |

sceneA 的 32 帧结论绑定 M9d / 854 数值及所列输入、参数合成规则、初态与构建；不称 M2 上新跑 32 帧，也不由终图 SHA 匹配反推出所有隐藏状态唯一。原 Stage R 的冻结 Stage P 状态不在本文重新启动。本轮新增的只是正文与下面的合成例，没有新 GPU、网络或连续链运行。

<a id="mufu-evidence"></a>
## MUFU 原生全域、跨架构摘要与生产成员验收

迁自 [L4_mufu.md](L4_mufu.md)；以下是原写作轮保存的记录。


## 全域测量到底证明了什么

| 记录 | 已有证据 | 边界 |
|---|---|---|
| 09-12 本机七族 × FTZ/非 FTZ，共 14 变体 | 每变体完整 raw32，512 块，每块双遍；旧 half 小表由独立形状与全扫取值两臂核对，[探针 RESULT:182–211、233–251](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L182) | 非 FTZ 包装可能是复合行为，不能统称为同一个裸函数；三角包装还涉及归约 |
| 同日 sm_75 对 sm_120 | **7,168/7,168 块哈希相同、14/14 对冻结 GPU 程序包 SHA 相同**，[租机 RESULT:15–38](../../../experiments/parity-blackwell-rental-20260912/RESULT_ZH.md#L15)、[逐变体比较 JSON](../../../experiments/parity-blackwell-rental-20260912/a1-mufu-arch-compare.json) | 固定已测配置；包身份不等于两架构所载内核机器码相同；两项旧形状未覆盖；不能推广到未测包装、未来驱动或网络所有站点 |
| 10 月七个 raw32 原值 bank | 七族各 512 块；SQRT/SIN/COS/RSQ 四项再验 24 容器、2,048 块，[narrow resume4 RESULT:12–22](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume4-20261008/RESULT_ZH.md#L12) | 原值采集与 CPU/调用者绑定分开；不能把 09 月与 10 月设备/驱动收据合成一次测量 |
| 10 月实际生产成员绑定 | SQRT 16,776,341 项，SIN/COS 各 15,468,894 项；RSQ 接受 half 像 30,705 项，组合比较零差，[同报告:5–22](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume4-20261008/RESULT_ZH.md#L5) | 域外拒绝无数值输出；SIN/COS 是正确预缩放后的组合，不是每子步骤各自全域证明 |
| 扩域候选 rcp/lg2/ex2 | rcp 全 raw32 接受且匹配；lg2 接受 $2^{31}$；ex2 接受 2,248,015,875；后两项仅接受域匹配，[候选 RESULT:25–38](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#L25) | 保留原有效性和失败段原值回退，不能写成所有公式在全 raw32 通过 |

本轮实际重读了 [原 sm_120 元数据](../../../rental-transfer/probe-suite.json) 和 14 份保存的 sm_75 块摘要，重新计算 7,168 对哈希比较及 14 对 GPU 程序包身份，全部一致。比较算法的原路径和字段见 [a1_mufu_arch_compare.py:13–40](../../../experiments/parity-blackwell-rental-20260912/a1_mufu_arch_compare.py#L13)。这是保存摘要复核，**没有重新计算原始全域 GPU 输出或新增 GPU 执行**。

硬件报告与 wrapper/[codec](APPENDIX_beginner_glossary.md#g097)/调用点全域连接仍需分开。[V2-02-006](../../arch-v2/02.03_mufu.md#v2-02-006) 的限定继续有效；原硬件前提表保留逐调用者绑定条件，[项目公理表:39–45](../../../experiments/parity-proof-program-r02-20261007-codex/resume12-20261009/delivery/AXIOMS_ZH.md#L39)。

<a id="index-scope"></a>
## 入口原具名构建与已测实例范围

迁自 [INDEX.md](INDEX.md)；以下是原写作轮保存的记录。

ARCH 0.7 的 T1080 为 854 构建上的 f0–f5；T1440 为 854 上 f0–f3，f3 从 CPU 自有 f2 检查点跨进程续接且输入经过会话平移；T4K 为统一 M 上每填充单进程 f0→f1→f2。M2 新数值门覆盖 1080/1440 f0 与 4K L0–L99，其余对应不能改写成 M2 上新测；1440 f0–f2 原生六纹理仅五个时点，不能补成逐 launch 全观测。MEASURED / CENSUS：[ARCH 0.7 §9.5.1、§12.7](../../../ARCHITECTURE_V3_ZH.md#951-07-当前结果及完整scope-tokens)。

10-24 sceneA 演练新增 1080 f0–f31 的 32/32 FINAL SHA 匹配：单进程、自有状态、fill00，f16–f31 参数由冻结模板合成；这是 M9d / 854 数值上的 FINAL-only 证据，不是 M2 的逐 launch 原生状态新门。scene_cut 的历史消费 / reset 控制与三档多帧范围见 [尾段证据表](L3_b70_history_output.md#evidence)。

<a id="attention-example"></a>
## TIN 分数与 RCP 实算的完整认证脚本

迁自 [L3_attention_softmax.md](L3_attention_softmax.md)；以下是原写作轮保存的记录。

~~~python
from pathlib import Path
import hashlib, struct, math
import numpy as np

RN16 = lambda x: struct.unpack("<e", struct.pack("<e", x))[0]
RN32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
bits16 = lambda x: struct.unpack("<H", struct.pack("<e", x))[0]
decode16 = lambda b: struct.unpack("<e", struct.pack("<H", b))[0]
H_add = lambda x,y: RN16(x+y)
asset = Path("mlxdlss/resources/rcp-domain.npz")
assert hashlib.sha256(asset.read_bytes()).hexdigest() == (
    "055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59")
with np.load(asset, allow_pickle=False) as z:
    ins = z["input_half_bits"].copy()
    rcp_half = z["native_half_bits"].copy()
    rcp_f32 = z["native_float_bits"].copy()
assert np.array_equal(ins, np.arange(0x0410, 0x7c00, dtype=np.uint16))

def Q8(x):
    # Finite nonnegative synthetic inputs only; nearest, ties to even code.
    def decode(c):
        e,m = c >> 3, c & 7
        return m*2.0**-9 if e == 0 else (1+m/8)*2.0**(e-7)
    return min(range(127), key=lambda c: (abs(decode(c)-x), c & 1))

def score(s, kind):
    if kind == "TIN":
        t = RN16(RN32(RN32(s*0.044921875)+1.30078125))
    else:
        # Chosen synthetic inputs have exact affine intermediates.
        t = RN16(s*0.044921875+1.30078125)
    t = min(max(t,1.03125),1.5693359375)
    return decode16(((bits16(t) << 5)+0x8000) & 0xffff)

def den(w):
    def leg(b):
        x = H_add(H_add(w[b],w[b+16]), H_add(w[b+4],w[b+20]))
        x = H_add(x,H_add(w[b+32],w[b+48]))
        return H_add(x,H_add(w[b+36],w[b+52]))
    return H_add(H_add(H_add(H_add(leg(0),leg(2)),leg(8)),leg(10)),
             H_add(H_add(H_add(leg(1),leg(3)),leg(9)),leg(11)))

s = [RN16(x) for x in (-8,-4,-2,-1,0,1,2,8)]*8
w = [score(x,"TIN") for x in s]
d = den(w)
ix = bits16(d)-0x0410
r = decode16(int(rcp_half[ix]))
raw = int(rcp_f32[ix])
assert bits16(RN16(struct.unpack("<f",struct.pack("<I",raw))[0])) == bits16(r)
p = [RN16(x*r) for x in w]
q = [Q8(x) for x in p]
textbook = [math.exp(x-max(s)) for x in s]
textbook = [x/sum(textbook) for x in textbook]
print("d",d,"d_half",hex(bits16(d)),"RCP_raw32",hex(raw),"r",r,"r_half",hex(bits16(r)))
for i in range(8):
    print(s[i],w[i],p[i],hex(q[i]),textbook[i])
print("sum_half_weights_in_real_arithmetic",sum(p))
print("max_difference_from_textbook",max(abs(x-y) for x,y in zip(p,textbook)))
assert w == [score(x,"split16") for x in s]
~~~

<a id="norm-example"></a>
## 人工 32 通道归一化的原函数实算脚本

迁自 [L3_norm_nonfinite.md](L3_norm_nonfinite.md)；以下是原写作轮保存的记录。

~~~python
from pathlib import Path
import ast, hashlib
from types import SimpleNamespace
import numpy as np

source = Path("mlxdlss/sm120_b1.py")
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "f4ada69da4ec60be36f09b05560a0fd0240a147721a20a0b51d7001518089d31")
tree = ast.parse(raw.decode("utf-8-sig"))
names = {"_norm_squared", "_rsq", "normalise"}
chosen = [n for n in tree.body
          if isinstance(n, ast.FunctionDef) and n.name in names]
assert {n.name for n in chosen} == names
module = ast.Module(
    body=[ast.ImportFrom(module="__future__",
                         names=[ast.alias(name="annotations")], level=0), *chosen],
    type_ignores=[])
env = {"np": np, "_RSQ_FIRST_CODE": 0x0410,
       "UnsupportedByBackend": RuntimeError}
exec(compile(ast.fix_missing_locations(module), str(source), "exec"), env)

asset = Path("mlxdlss/resources/rsq-domain.npz")
assert hashlib.sha256(asset.read_bytes()).hexdigest() == (
    "06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62")
with np.load(asset, allow_pickle=False) as z:
    keys = z["input_half_bits"].copy()
    floats = z["native_float_bits"].copy()
    table = SimpleNamespace(rsq_half_bits=z["native_half_bits"].copy())
assert np.array_equal(keys, np.arange(0x0410,0x7c01,dtype=np.uint16))

# Artificial vector and gain, not model values.
x = np.array([[1,-2,3,-4]+[0]*28], dtype=np.float16)
out,n = env["normalise"](x,table,scale=np.float16(1))
r = env["_rsq"](n,table)
ix = int(n.view(np.uint16)[0])-0x0410
print("source_sha256",hashlib.sha256(raw).hexdigest())
print("n",n.tolist(),"n_bits",[hex(int(b)) for b in n.view(np.uint16)])
print("rsq_f32_bits",hex(int(floats[ix])),"r",r.tolist(),
      "r_bits",[hex(int(b)) for b in r.view(np.uint16)])
print("first4_half",out[0,:4].tolist(),
      "bits",[hex(int(b)) for b in out[0,:4].view(np.uint16)])
print("real_sum_of_published_half_squares",float(np.sum(out.astype(np.float64)**2)))

with np.errstate(over="ignore",invalid="ignore"):
    zero = np.zeros((1,32),dtype=np.float16)
    high = np.full((1,32),48,dtype=np.float16)
    z = env["_norm_squared"](zero)
    h = env["_norm_squared"](high)
print("zero_floor",float(z[0]),hex(int(z.view(np.uint16)[0])))
print("synthetic_48_group_stat",hex(int(h.view(np.uint16)[0])))
try:
    env["_rsq"](h,table)
    raise AssertionError("unchanged reference unexpectedly accepted +Inf")
except RuntimeError as e:
    print("unchanged_reference",str(e))
print("saved_RSQ_Inf_row",hex(int(floats[-1])),
      hex(int(table.rsq_half_bits[-1])))
~~~

<a id="ffn-r04b"></a>
## r04b FFN：具体图、通道推导与实算身份

本节是r04b新增的只读核对与人工CPU标量例；GPU、模型、连续链新运行均为0。其他历史节的“本轮”语境不改变。主文见 [L3.ffn](L3_ffn.md#ffn)。

### split16 FFN的通道依据

L25与L29图分别按矩阵A来源分为原输入S、Q(预投影矩阵结果)、Q(G结果)三段；取B来源的wload_off索引并并上字节位移，统计的是权重地址集合，不读取权重值。得到每组预投影32768 B、扩张16384 B、收缩16384 B；全组分别262144/131072/131072 B。原序K32链给K=512/64/256，结合出口每位置512 E4和取数分组，得到512→512预投影、八组64→256→64。逻辑分组是这些具体图的解释，不等于16个attention头，也不构成通用几何定理。

L25/L29的每条门均为同一half min/max→abs→两次fma→mul→Q，且末乘保留未裁输入。L26/L30图没有另一个G，首矩阵C来源为mul([D8](APPENDIX_beginner_glossary.md#g061)(同块入口),half尺度)，16个K32携带该seed，末端Q。首块/连续块的布局和角色来源分别由front bindings中的L25/26/29/30钉住。本轮四份wiring与四份地址图实际SHA均与该绑定相符；任一不符会停止，不修补证据。

### ViT contract的分片依据

T640原型0/1/2/3四个live模板的矩阵链各为32步K32。第0段seed含dq(块入口)与half尺度的mul，写half buffer；第1/2段从零起、依次half加到buffer；第3段从零起，与buffer作half加再sat到E4。物理buffer为P×2048 B，主输出为P×1024 E4；不能从“2048”推导成门控通道劈半。

### 已有数值记录的读取边界

- expand：[resume4正式结果:289](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L289)聚合72个独立P3；[完整release与Python边界:137](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L137)、[padding:220–224](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L220)保留各角色。没有把其“正式整链结果”标题解释成72条连续网络链。
- contract：[旧L60四角色门:3–8](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L3)、[resume7格式迁移:404](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L404)是不同快照；旧71格NOT_RUN和MAP_CHECK_FAILED不由当前M2整帧结果改写。
- split16：两公开320×240/reset样本的 [B27–B29记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3)包含三块共48项单段/块内链比较；只取其中[FFN](APPENDIX_beginner_glossary.md#g037) launch引用，不把qkv单独门混入FFN分母。
- M2：[发布数值记录](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)为1080/1440 f0及4K L0–L99；按INDEX口径区分参考FULL/六纹理、原生具名比较点与FINAL，不冒充直接观察每个G内部[激活](APPENDIX_beginner_glossary.md#g045)。

### 本轮人工例与完整身份

[源码抽取/编译脚本](examples/ffn_r04b.py)、[实际stdout/编译器/函数列表](examples/ffn_r04b.result.json)、[图与通道账](examples/ffn_r04b.wiring.json)可复用。程序只抽取原C++的纯标量函数，调用原QMMA头；临时构建不写入发布源码。初次动态链接程序启动失败，最终静态链接版本实际运行PASS；启动失败不计为算术结果。最终63488个有限half的B0/TIN/ViT G相同，另列人工门+K32残差字节表、half换序例和ViT非有限拒绝；均非新增原生门。

| 实际读取的源/图 | SHA-256 |
|---|---|
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.npz) | fc4cc52f301b72a67ba7667372bff51127607512d87846091f1187b61342f7a0 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json) | 4a19d31ece96b382228c0a3c20fbebbe1dd55b144ac9addd58a73db8544d4910 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.npz) | d7a30db1b0a6de967aec37873544965eeedaa828a6ac7dd090dbc9f2a957be74 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json) | 998f5e5729490cf269385a3f1fdcbf2b8bdf6b5b0d370cb8b05a1cd315755e66 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.npz) | 209764facb72c75f27760465eb9075fc7829765b2cb30ae8b2b12405748ad6f5 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json) | 3b03345e3c9b1969e4992fc2cfd7ef4c140ffee389e4a62f867cb6f040223639 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.npz) | c8979c9ab482d4f166b8af8c735aba5a662075f4e0219d063e5049880de470d7 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json) | 3364fc7bfa55fef2d1b482e20076294c4c2c766182d7ec034ddf890eebd2f530 |
| [dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json](F:/dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json) | c7ebf67032c860ece07fe64ac0a8d5f849913f441cb42fea16c4ac5ad9e0b62a |
| [experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json) | 65c4120d1bf9b136508ef0a3154b67c0c0d1906bd13e8f0a391e83248140c541 |
| [experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json) | f81dc2374c601d0432d8e7488fa7a6086b1551caa592adbcf4d9eb68e25c16dc |
| [GlassBox-NR/cpp/chain_entry_optm/b00.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp) | 932e0c805f020420f0e6fad9543d3e1710d0561b6afa14a30263d6f9bd939392 |
| [GlassBox-NR/cpp/chain_tin_optm/tin.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp) | 371d33d205655f75c809f0f9990a8054edf8e930a31733f72dbf916f87b4f1f8 |
| [GlassBox-NR/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp) | fe67bb0dc7c878e69291798425c77a3c3f013863e11f36a48e533323ede40287 |
| [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp) | 2b85ddfaeb37eb5d16560224def629ff29a043c4421b5b571749103b398e5452 |
| [GlassBox-NR/cpp/chain_entry_optm/mapexec_base.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp) | 0ac19678e7b4a31857434ffda3b250f508c98e76970485b3c70f7948b65eeb60 |
| [GlassBox-NR/cpp/chain_tin_optm/primitives.inc](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc) | 5e5519dbbe41145146487512337401631ac8342c74f7357ba7ab781219a4c48e |

共享half/E4 helper的函数体也逐项核对：忽略空白/注释并统一等价的位拷贝封装名称后，B0、TIN与ViT一致；缓存量化路径使用未改的reference构造，未将存储优化当成另一种算术。

生成C++的SHA、编译器完整身份和原stdout见上述result JSON；本轮没有重跑旧证明、GPU原语或网络链。

<a id="tin-window-r04c"></a>
## r04c TIN完整窗口块：44份配置与证据边界

主文为 [L3.tin-window](L3_tin_window.md#tin-window)。本节仅新增CPU源码阅读、44份1080默认params的实际内容/SHA核对，以及已有记录的整理；没有读取模型系数或目标工作区，没有运行GPU、模型、原生调用或CPU网络链，也没有把旧测量重新计为本轮结果。

### 本轮实际读取的身份

| 源或绑定 | SHA-256 |
|---|---|
| [TIN实现](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp) | 371d33d205655f75c809f0f9990a8054edf8e930a31733f72dbf916f87b4f1f8 |
| [旧44调用绑定](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/s00-bindings.json) | 55bdba63b3324c410c3983b90fffb51d176bcd39fe9daff3e1f3ac963e103fbc |

[逐调用核对记录](examples/tin_window_r04c.bindings.json)保留全部44份实际params路径、SHA、B/launch、C、外围种类、W/H、带符号原点、输入/输出布局、前档尺寸和pool/[skip](APPENDIX_beginner_glossary.md#g016)/完成标记字段；结果为ALL_44_PARAMS_SHA_AND_FIELDS_MATCH。实际读取的每份params SHA均等于上述旧绑定的预期值，extent/原点与保存字段也逐项一致，没有通过修改绑定消除差异。源文件与绑定的完整SHA同列在该JSON中。

这44项恰为L3–L24及L133–L154，包含4 [inpview](APPENDIX_beginner_glossary.md#g022)、28 chained、4 ds_wait、4 upsample、4 outview_wait。八行尺度/方向表由这些具名配置整理；特别是B56/L141原点为(−4,0)，不能按每档重新开始四相循环来猜。该核对只关闭这些1080参数身份和字段的一致性，不建立任意几何、任意控制或未知参数版本的支持。

### 接线依据与实现层

[window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130)明确先构造入口残差seed、做FFN，再量化FFN结果、投影Q/K/V、归一化Q/K、做attention，最后以缩放后的FFN旁路为seed执行输出投影。一头的attention旁路取未量化half，多头取E4发布后的解码值；[upsample与取窗:151–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L151)另使B66保留未量化merge作FFN seed。这里描述CPU实现的数值分解，不能由出口相同推断原生内部表示唯一。

[norm/attention:114–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)钉住32通道头、Q/K平方和下界、V直接发布、分数的独立F32乘/加、half分母树、RCP与AV的两次K32。[pool:162–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L162)从未量化核心结果做三次half加和一次quarter乘，先E4再C→2C；C=256另保留相关平面的零写范围。布局解码/编码、补零和完成标记属于实际外围行为，核名自身不是同步语义证明。

### 旧数值门不能与配置普查相加

[TIN R01结果:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3)的8/44是L3、L7、L11、L18、L24、L133、L134、L151逐调用teacher-forced比较；每次覆盖212,519,936 B整片工作区，C++、Python与具名原生参考一致。其余36项在该旧记录中继续是NOT_RUN，不因本轮读到44份params而升级。380项静态/布局检查、5个合成窗口测试和3个非法输入拒绝，也不是新增原生门。

旧L134曾出现C++等于Python而两者与原生相差640 B；缺失的是160个完成位置的显式零写。适配层补齐后才取得保存的三方一致结果；[旧失败及修正:25–27](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L25)仍保留，不把“两个重建相同”当成该旧版已对原生通过。本轮没有重跑它。

[M2发布数值记录:1–3](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)后来覆盖1080/1440 f0完整158调用，故包含各自的44个TIN调用；4K的M2新数值范围仅L0–L99，L100–L157只做配置普查。比较对象继续按INDEX区分CPU参考FULL/六纹理、具名原生观测与FINAL；另有统一M的后来多帧结果，见 [尾段证据范围](L3_b70_history_output.md#evidence)，不移名为M2本轮新测。

L133的[computed-shared](APPENDIX_beginner_glossary.md#g108)符号来源层仍NOT_ADMITTED，B69原生独立布局仍UNKNOWN。完整同步、别名、生命周期、一般几何以及内部值唯一没有由上述数值门建立；这几项未知随正文保留。

<a id="split16-window-r04d"></a>
## r04d split16完整块与两张补图：身份和读取边界

主文见 [split16完整块](L3_split16_window.md#window-attention)；补图分别在 [L100数据流](L2_06_decoder_bridge.md#wiring)与 [repack置换/4×4 tile](L3_workspace_map.md#repack-diagram)。本轮仅阅读源码、具名params、图/索引和保存结果，并计算小型整数示意；没有读取模型系数、网络输入或目标工作区，没有新GPU、模型、原生调用或CPU整链运行。

### 当前实际读取的源身份

| 源或绑定 | SHA-256 |
|---|---|
| [front绑定](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json) | 65c4120d1bf9b136508ef0a3154b67c0c0d1906bd13e8f0a391e83248140c541 |
| [tail绑定](../../../experiments/parity-cpp-bindings-tail-r01-20260928-codex/s00-bindings-tail.json) | 5939bc86c36559800d06d9496b992b13f1d3c5f98fa46e387480f9abe2a3fa2e |
| [split16角色执行器](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp) | 284d2629e3282d7f759453f8c99bd158552da36f19913a869001b7899bc3417f |
| [split16标量图执行器](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp) | 20610eaa92c3bada615647abd5d2ce5989f7186374b83d1aaeb7c4d4dff3a50a |
| [L100/L132执行入口](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp) | c9f1977d816c5e65757625a59859f6673578920ab7b69127efdc92e5870d313e |
| [repack闭式](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp) | 8d721e2dc8d4a2530a92548c0e19a4f4854dc9ef6652e75472a269bf2480663b |

[本轮核对记录](examples/split16_window_r04d.bindings.json)保留L25–L57、L101–L132全部65份实际params的路径/SHA、角色字节长度与生产者，另列16次qkv的有效60×36和带符号原点。全部65份SHA均等于front/tail保存绑定；16块内的主路、原块入口旁路、前馈后旁路指针均逐项相符，没有修改绑定以消除差异。

同一记录保留13个代表调用的26个实际地图/图资产SHA和NPZ数组头：L25/26/27/28/29/30/31/35/39/56/57/132/100。每个实际SHA均与对应保存绑定相符；这不是对65个调用全图的新增符号准入。L100、L133的参数另按tail核SHA；L58、L99只作为交接端点实际读取并记录当前SHA，未在本轮另核其旧参考pin。五条额外交接是L56.pool→L57、L57→L58、L99→L100主路、L56.full→L100 skip、L132→L133主路，均核了实际参数指针。

### 输出投影与图内子链

本轮检查图中矩阵seed依赖，再读取L28/L56/L132各自地图的整数来源，未读取这些来源指向的数值payload。三份图的所有链首seed均为E4来源解码后与half尺度相乘；活动seed字节引用各1,105,920项，每项都落在拼接输入的第二角色，即保存绑定中的本块前馈后旁路。这个来源检查不替代全部Read_ws/权重读集、别名和生命周期证明。

| 具体图 | 按前一矩阵seed依赖拆出的K32子链长度：条数 | 能支持什么 |
|---|---|---|
| L27 / L31 / L35 / L39 | 16步：48条；1步：32条；2步：16条 | 与Q/K/V投影、QK及AV的已写顺序接合；四种原点各自核图SHA |
| L28 | 16步：16条 | 每条输出投影从缩放旁路half起步，随后逐K32携带 |
| L56 / L132 | 16步：32条 | 双出口/末视图各有自己的图与源选择，不据“32”发明新网络轴 |

这些是具体图里的符号片段库存，不是逻辑矩阵的行数、头数或独立数值证据次数；完整物理轴闭式仍未建立。FFN的通道依据继续见 [r04b](#ffn-r04b)，Q/K归约与分数/AV见 [norm绑定](#norm-bindings)、[attention绑定](#attention-bindings)，不把这些分项在本轮重新计门。

### 两张图各自支持的范围

[entry.cpp:58–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L58)从A_src/B_off生成8步K32部分和；REDMAP每项选三个F16，按先前两项再第三项相加。OUTMAP再选另一路部分和、skip位置和尺度来源，先half加，再与B30.full作h_fma，最后E4发布；F16暂存和控制区另写。图只画已确认的投影/归约/合并，不为L100补认[最近邻](APPENDIX_beginner_glossary.md#g021)、卷积或新的网络头轴。

[repack.cpp:26–50、88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26)给出二维[tile](APPENDIX_beginner_glossary.md#g087)与序列group各自的闭式、相同π及双向4 B搬运。本轮整数示意核对π在4096个索引上为置换，并保存1080左上4×4 tile的16个c=0对应地址；t=32的256 B→32,768 B来自该闭式，未执行payload。已保存原生/映射门的分母继续见 [repack证据](L3_workspace_map.md#repack-evidence)，整数双射不升级为新原生对照。

### 具名数值记录与保留未知

[1080 B25–B30旧结果](../../../experiments/parity-gemini-1080-chain-r03-20260922/RESULT_ZH.md#L3)是L33–L57的25调用连续段，含L56的full/pooled及L57；它止于B30，不包含ViT。另一个 [B27–B29旧结果](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3)是两公开320×240/reset样本的48项单段/块内链比较，没有跨块连续链结论。二者的输入、分辨率与分母分别保留。

[M2数值范围](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)后来包含1080/1440 f0完整65个split16调用；其4K新数值只到L99，解码与L100/L132在该M2轮仅配置普查。统一M后来多帧、具名原生观察、参考FULL/六纹理和FINAL继续按 [INDEX](INDEX.md)、[尾段证据](L3_b70_history_output.md#evidence)分列，不更名为本轮新测。

16头bias的独立排序、完整物理轴、一般maps/同步/别名/生命周期及内部值唯一仍UNKNOWN；原MAP_CHECK_FAILED按具名图/几何保留。非有限合同和M/A1版本界限沿用原文，本轮没有扩大接受域。


<a id="ffn-gate-history"></a>
## FFN 逐调用门的历史明细

| FFN位置 | 保存的数值门（各一行） |
|---|---|
| ViT expand八次 | [正式resume4:289–291](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L289)：72个具名逐调用P3（逐调用数值对照阶段）均MATCH；output/padding与完整release分列，Python完整release仍NOT_COVERED_BY_PYTHON，不是72条自有连续链 |
| ViT contract八次 | [旧独立门:3–8](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L3)：L60 1080 f0四角色三方一致，旧其余71格NOT_RUN保留；八次调用在 [M2具名f0门](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)另有逐launch比较，不倒灌旧轮，MAP_CHECK_FAILED仍按具名准入 |
| split16 ffwd/ffwd_proj | [B27–B29旧门](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3)：L41/42、45/46、49/50有两样本单段/块内链MATCH；[M2](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)覆盖具名f0的全部本家族调用，不能借用qkv的56格门充当前馈门 |
| TIN融合调用内FFN | [TIN门:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3)：原轮8/44个具名整launch三方一致、其余36个NOT_RUN；其中含L18/134 chained；未独立测每个内部G，后来M2门另列 |
| B0 / B70内FFN | [B0隔离门](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证)为f0–f3 full/pool teacher-forced零差，[尾段具名门](L3_b70_history_output.md#evidence)含L155；两者验证整调用出口，不把小例子或内部trace当独立GPU激活观测 |


<a id="half-integer-implementation"></a>
## half T1 的整数实现与证明工程

## 可移植整数 T1 如何保留两个舍入阶段

这里引用本项目的冻结实现与实验记录；不把外部讲解文档当事实来源，也不把实验 T1 当成当前公开模块默认实现。后者仍可直接看到 std::fma 分支。

有限输入解码为带符号 $m_a2^{e_a}$：次正规取尾数域与单位 −24，正规取 1024+m 与单位 E−25。[T1 source:52–54](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L52)。

```math
P=(m_a m_b)\,2^{e_a+e_b+48},\qquad
Q=m_c\,2^{e_c+48},\qquad
N=\left|\,\pm P\pm Q\,\right|.
```

P、Q 是整数；源码用两个 uint64 肢完成移位、带进位加法、借位减法与比较，$P<2^{80},Q<2^{64},N<2^{81}$。零和单独处理：非零抵消给 +0，两项均为负零才保留 −0。[T1 source:75–95](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L75)、[证明 RESULT:9–11](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L9)。

~~~text
若 N=0：走准确零符号分支。
top=floor(log2 N)。
top≤52：把 N*2^−48 直接送整数 half 发布器。
top>52：
    shift=top−52；sig=N>>shift；rem=N−(sig<<shift)；tie=2^(shift−1)。
    sig 按 rem/tie 与 sig 奇偶做一次 RN-even。
    把 sig*2^(shift−48) 送整数 half 发布器，保留 sig=2^53 的进位。
发布器按目标 half 格距再次 RN-even，处理次正规、跨正规边界与溢出。
~~~

第一阶段对应 [T1 source:96–103](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L96)，第二阶段为 [source:14–41](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L14)。整数加/乘也在 [source:55–73](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L55) 中有直接单位格/有效数乘积实现；本节的全域证明结论专指 h_fma 组合。

【验证记录】保存的证明将整数 T1 与软件 T0 在全部原始 F16 三元组（含异常类别和消息）上的行为连接，结论为 PROVED；不是对 GPU 内部实现的证明。完整解码、精确两肢合成、两次 RN-even、零符号、非有限分类与故意破坏控制均是证明前提。

信任边界仍含 IEEE 正确舍入的 std::fma、最近偶数环境、double/整数 ABI、编译器、求解器及源码到模型对应；历史 UNKNOWN 不直接升级为 UNSAT。当前公开默认模块仍可见 std::fma 分支，实验 T1 不冒充默认实现。[证明叶子/代表计数、控制、源码 SHA 及原复核记录](APPENDIX_evidence_history.md#half-proof)移至附录；本轮未重跑证明驱动或求解器。


<a id="half-example-source"></a>
## half 人工例的完整程序与原输出

~~~python
import math
import struct

# Artificial inputs only. No project imports, model files, or GPU calls.
def hv(h):
    s = -1 if h & 0x8000 else 1
    e, m = (h >> 10) & 31, h & 1023
    if e == 31:
        return math.nan if m else s * math.inf
    return s * math.ldexp(m if e == 0 else 1024 + m, -24 if e == 0 else e - 25)

def hr(x):
    sign = (struct.unpack("<Q", struct.pack("<d", x))[0] >> 48) & 0x8000
    if math.isnan(x):
        raise ValueError("NaN half publication outside measured domain")
    if math.isinf(x) or abs(x) >= 65520:
        return sign | 0x7c00
    a = abs(x)
    if not a:
        return sign
    _, e = math.frexp(a)
    step = max(e - 11, -24)
    q = math.ldexp(a, -step)
    n = math.floor(q)
    rem = q - n
    n += rem > .5 or (rem == .5 and n & 1)
    rounded = math.ldexp(n, step)
    if rounded >= 65536:
        return sign | 0x7c00
    if rounded < 2**-14:
        return sign | n
    _, out_e = math.frexp(rounded)
    mant = int(math.ldexp(rounded, 11 - out_e))
    if mant == 2048:
        out_e, mant = out_e + 1, 1024
    return sign | ((out_e + 14) << 10) | (mant - 1024)

def add(a, b):
    return hr(hv(a) + hv(b))

def mul(a, b):
    return hr(hv(a) * hv(b))

def fma(a, b, c):
    return hr(math.fma(hv(a), hv(b), hv(c)))

def rshift(v, sh):
    if sh <= 0:
        return v << -sh
    q, r = divmod(v, 1 << sh)
    tie = 1 << (sh - 1)
    return q + (r > tie or (r == tie and q & 1))

def ipack(v, exponent, sign):
    if not v:
        return sign
    e = v.bit_length() - 1 + exponent
    if e > 15:
        return sign | 0x7c00
    q = rshift(v, max(e - 10, -24) - exponent)
    if not q:
        return sign
    if e < -14:
        return sign | q
    if q == 2048:
        q, e = 1024, e + 1
    return sign | 0x7c00 if e > 15 else sign | ((e + 15) << 10) | (q - 1024)

def finite_t1(a, b, c):
    def dec(h):
        e = (h >> 10) & 31
        assert e != 31
        return (h & 1023) + (1024 if e else 0), e - 25 if e else -24
    ma, ea = dec(a)
    mb, eb = dec(b)
    mc, ec = dec(c)
    ps, cs = (a ^ b) & 0x8000, c & 0x8000
    p, q = (ma * mb) << (ea + eb + 48), mc << (ec + 48)
    net = (-p if ps else p) + (-q if cs else q)
    if not net:
        return ps & cs
    sign, v = (0x8000 if net < 0 else 0), abs(net)
    sh = max(v.bit_length() - 1 - 52, 0)
    return ipack(rshift(v, sh), sh - 48, sign)

a, b, c = 0x3c01, 0x3bff, 0xbc00
fused, separated = fma(a, b, c), add(mul(a, b), c)
print(f"FMA={fused:04x} MUL_ADD={separated:04x} T1={finite_t1(a,b,c):04x}")
print(f"ties={add(0x3c00,0x1000):04x},{add(0x3c01,0x1000):04x}")
print(f"subnormal_ties={hr(2**-25):04x},{hr(3*2**-25):04x},{hr(-2**-25):04x}")
print(f"subnormal_to_normal={hr(1023.5*2**-24):04x} negative_zero={add(0x8000,0x8000):04x}")
print(f"overflow={hr(65519):04x},{hr(65520):04x},{hr(-65520):04x}")
x, y, z = 0x6800, 0x3c00, 0xe800
print(f"atomic_orders={add(add(x,y),z):04x},{add(add(x,z),y):04x}")
f32 = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
print(f"F32_to_F16={hr(f32(0x3f801000)):04x},{hr(f32(0x3f801001)):04x}")
for triple in [(a,b,c), (0x0400,0x7400,0x1000), (0x3c00,0x7bff,0x5000),
               (0x8000,0x3c00,0x8000), (0x7bff,0x7bff,1)]:
    assert fma(*triple) == finite_t1(*triple)
assert (fused, separated) == (0x0ffe, 0x0000)
~~~

本轮实际 stdout：

~~~text
FMA=0ffe MUL_ADD=0000 T1=0ffe
ties=3c00,3c02
subnormal_ties=0000,0002,8000
subnormal_to_normal=0400 negative_zero=8000
overflow=7bff,7c00,fc00
atomic_orders=0000,3c00
F32_to_F16=3c00,3c01
~~~

另用独立 Fraction 检查融合例的精确分数，并以 Python struct 的 F16 转换核对上述有限发布/中点/溢出；全部一致。T0 与有限 T1 演示在五个具名人工/控制三元组相同。本轮没有新 GPU、模型或整链运行，也没有重做完整软件证明。


<a id="e4-example-source"></a>
## E4 / K32 人工例的完整程序与原输出

~~~python
# Synthetic operands only; no model files, imports, or GPU calls.
def lg(n):
    return n.bit_length() - 1 if n else -99

def dec(b):
    if b & 127 == 127:
        raise ValueError("E4M3 NaN code")
    e, m = (b >> 3) & 15, b & 7
    u = (8 + m) << (e - 1) if e else m
    return -u if b & 128 else u

def seed(h):
    e, m = (h >> 10) & 31, h & 1023
    if e == 31:
        raise ValueError("nonfinite QMMA seed")
    u = (1024 + m) << (e - 1) if e else m
    return -u if h & 32768 else u

def pub(z):
    if not z:
        return 0
    sign, a = (32768 if z < 0 else 0), abs(z)
    top = lg(a)
    sh = max(top - 10, 0)
    q, r = a >> sh, a - ((a >> sh) << sh)
    if sh and (r > 1 << (sh - 1) or
               (r == 1 << (sh - 1) and q & 1)):
        q += 1
    if q >= 2048:
        q >>= 1
        top += 1
    if top < 10:
        return sign | q
    E = top - 9
    return sign | 31744 if E >= 31 else sign | (E << 10) | (q - 1024)

def dot(A, B, C=0, model=False):
    assert len(A) == len(B) == 32
    c = seed(C)
    E, exact, largest, least = (lg(abs(c)) - 24 if c else -99), c, abs(c), None
    terms = []
    for a, b in zip(A, B):
        x, y = dec(a), dec(b)
        t = x * y * 64
        terms.append(t)
        exact += t
        largest = max(largest, abs(t))
        if t:
            least = abs(t) if least is None else min(least, abs(t))
            E = max(E, max(lg(abs(x)) - 9, -6) + max(lg(abs(y)) - 9, -6))
    sh = max(E - 1, 0)
    def place(x):
        return (-1 if x < 0 else 1) * ((abs(x) >> sh) << sh)
    z = place(c)
    for t in terms:
        z += place(t)
    if abs(z) >= 1 << 52:
        raise ValueError("QMMA accumulator outside exact range")
    if not model and largest and least is not None:
        top = lg(largest) - 24
        span = lg(largest) - lg(least)
        cancel = lg(largest) - lg(abs(exact)) if exact else 99
        if top >= 12 and span >= 20 and cancel >= 2:
            raise ValueError("D27 QMMA counterexample domain")
    h = pub(z)
    if not model and h & 31744 == 31744:
        raise ValueError("QMMA half overflow")
    return h

def pad(xs):
    return xs + [0] * (32 - len(xs))

def e4_from_units(z, sign=0):
    a = abs(z)
    c = min(range(127), key=lambda c: (abs(a - (dec(c) << 15)), c & 1))
    return (128 if z < 0 or sign else 0) | c

a, b = pad([0x38, 0x01, 0x01]), pad([0x38, 0x28, 0x01])
whole = dot(a, b)
first = dot(pad([0x38, 0x01]), pad([0x38, 0x28]))
split = dot(pad([0x01]), pad([0x01]), first)
print(f"same_K32={whole:04x} split_K32={split:04x}")

cancelled = dot(pad([0x78, 0xf8, 0x01]), pad([0x38, 0x38, 0x01]))
print(f"grid_cancel={cancelled:04x} exact_sum_RN={pub(64):04x}")

a, b = pad([0x38, 0x28, 0x01]), pad([0x38, 0x28, 0x01])
h = dot(a, b)
exact_units = sum(dec(x) * dec(y) * 64 for x, y in zip(a, b))
print(f"F16_then_E4={h:04x}->{e4_from_units(seed(h)):02x} direct_E4={e4_from_units(exact_units):02x}")

lo_a, lo_b = pad([0x78, 0xc8, 0xb8]), pad([0x78, 0x48, 0x38])
hi_a, hi_b = pad([0x78, 0xc8]), pad([0x78, 0x48])
print(f"65519_RN={dot(lo_a, lo_b):04x}")
for label, aa in [("65520", hi_a), ("minus65520", [x ^ 128 for x in hi_a])]:
    try:
        dot(aa, hi_b)
    except ValueError as err:
        print(f"{label}={err}; model_bits={dot(aa, hi_b, model=True):04x}")
assert (whole, first, split, cancelled, h) == (0x3c01, 0x3c00, 0x3c00, 0, 0x3c40)
~~~

本轮实际 stdout：

~~~text
same_K32=3c01 split_K32=3c00
grid_cancel=0000 exact_sum_RN=0040
F16_then_E4=3c40->38 direct_E4=39
65519_RN=7bff
65520=QMMA half overflow; model_bits=7c00
minus65520=QMMA half overflow; model_bits=fc00
~~~

独立分数/转换核对另确认 A 为 262273/262144→0x3c01，第一半为 2049/2048→0x3c00，C 为 278529/262144→0x3c40，65519→0x7bff；例 B 的未放置和转 F16 为 0x0040，直接 E4 与两步 E4 差异也用精确距离重算。它们核对本例和源码转写，不建立新硬件全域结论。


<a id="norm-propagation-detail"></a>
## 027/028 与 A1 非有限传播历史

### L3.norm-nonfinite.path L6 首源与 L27/L31 的拒绝点

- 是什么：有限输入可以在平方/half 正数求和中得到 +Inf，随后被原 RSQ 表吸收，或被另一个包装的域守卫拒绝。
- 输入 → 输出：已追踪的 027/028 有限 half 输入 → L6 的 +Inf 统计临时量；之后是否拒绝取决于实际路由和接口。
- 怎么算：
  ~~~text
  有限 x → half 平方/和上溢 → n=+Inf
  支持该键的 RSQ：+Inf → F32 +0 → half +0
  若 x_i 与 γ 有限：x_i × +0 → 带符号零 → 缩放 → E4 零
  旧 split16 / ViT 有限域包装：+Inf → 守卫拒绝，没有后继可比输出
  ~~~
- 数值规则：ε 的 max 下界保留 +Inf。有限 x 乘零的吸收不能推广成允许 Inf×0；后者可能产生 NaN，仍需单独的原语域和实际可达证据。
- 为什么这么算：原 TIN RSQ 表已包含输入 +Inf、输出 +0 的末项；旧 split16 的 loader/guard 排除了这个键。相同统计量因此有不同的接受结果。
- 我们怎么知道：MEASURED（CPU 旁路），[非有限传播诊断 RESULT:7–15、29–47](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7)；原生内部是否也产生同样的临时值仍为 UNKNOWN。
- 往下：[A1 的新语义与计数](L3_norm_nonfinite.md#a1)、[half 上溢界](L4_half_arith.md#half-arith)。

【验证记录】保存的 027/028 见证追到 CPU L6 统计上溢，后续局部范数可将 +Inf 吸收为零；后来 L61 又有新的上溢并被旧包装拒绝。它没有证明同一个 Inf 字节一路传播，也未测到 GPU 内部同样的临时值（UNKNOWN）。[原数值、前缀一致性及限制](APPENDIX_evidence_history.md#norm-witness)移至附录；不为旧拒绝后的未观察区间编造结果。

### L3.norm-nonfinite.a1 45 INVALID 中恢复 42，三张继续拒绝

- 是什么：A1 在独立子封存中补齐限定的 +Inf 统计语义，重新执行原 147 图验证，保留 QMMA 的拒绝边界。
- 输入 → 输出：旧 99 MATCH / 45 INVALID / 3 UNCOMPARED → 144 FINAL MATCH / 3 INVALID_REFUSED / 0 DIFF。
- 怎么算：
  ~~~text
  1. entry / split16 的 RSQ 特判 half +Inf：返回 F32 +0。
  2. ViT QKV 允许 add/mul/max 及其规定融合形态的 +Inf 结果继续流动。
  3. ViT RSQ 特判 F32 +Inf：返回 F32 +0；原半精度发布点保留。
  4. −Inf、NaN、其他表外键与未放行操作继续拒绝；RCP 不扩域。
  5. 每图重新推进到终图或第一次守卫拒绝，分别登记。
  6. QMMA 的 half 输出若为非有限，生产路径仍拒绝，不交出终图。
  ~~~
- 数值规则：RN-even 的 half 上溢界是绝对值 ≥65520；65504 是最大有限 half，不是精确实数输入的上溢阈值。A1 没有把 half 归约改成 F32，也没有删掉失败图或调整期待字节。
- 为什么这么算：RSQ(+Inf)=+0 已有独立原值证据；它允许“有限向量的统计量上溢后被吸收”的路径继续。QMMA 的一般非有限结果及混合拓扑需要另一套证据，不能顺带放行。
- 我们怎么知道：MEASURED / CONTROLLED，[A1 RESULT:5–54](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L5)、[A1 修改清单](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/NF_A1_SOURCE.diff)；限定分支源码：[A1 scalar_map.hpp:272](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/src-M/new/scalar_map.hpp#L272)、[A1 qkv_projection_impl.hpp:165–205](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/src-M/new/qkv_projection_impl.hpp#L165)。
- 往下：[证据与边界](L3_norm_nonfinite.md#evidence)、[QMMA 发布守卫](L4_e4m3_and_k32.md#publish-guards)。

【验证记录】A1 的恢复与三张拒绝见 [完整计数与身份账](APPENDIX_evidence_history.md#a1-ledger)。三张均因 ViT attention QMMA half overflow 拒绝，分别在 L77/L97/L72，没有终图，不能算 MATCH 或按类别豁免；默认生产守卫见 [qmma_sm120.hpp:65–70](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L65)。

A1 使用独立替换源/构建，范围为 1080 单帧 f0；公开 M2 的有限域守卫不因此更新，不能转移为 M2、1440、4K 或多帧的新验收。

RCP 的原值与调用准入也要分开：旧 [SEMANTICS:17](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/SEMANTICS_ZH.md#L17) 已记录潜在 RCP(+Inf) 的双遍 +0 原值；A1 报告仍选择不为 RCP 建模扩域。本文按实际 A1 分支记录其拒绝，不把报告中“无证据”的概括扩成“从未采过 RCP 原值”。


<a id="r04f-scope"></a>
## 文档修订与例子运行范围

r04f只改本目录文档与人工标量示例；新增GPU、模型和连续链运行均为0，没有重跑旧实验或软件证明。此前各页相同的运行范围声明集中于此。保留具体观测、拒绝及未知的适用域。

- L3_attention_softmax.md：本轮只有文档、地址/图一致性检查和以上合成算术；新增 GPU / 模型 / 连续链运行均为 0。
- L3_ffn.md：x=5 的输出不同于x=4，直接检验“只裁因子、不裁末端x”。同一程序另以人工half分片[2048,1,−2048,1]调用真实H+：原序得到0x3c00（1），交换中间分片得到0x4000（2）；它展示逐次half舍入的顺序敏感，不是新原生负控。ViT gate 对人工+Inf/−Inf/NaN均实际拒绝。完整程序还覆盖x=−5与全部有限half三种G写法；本轮只有小型CPU算术，GPU/模型/整链新运行均为0。
- L3_split16_window.md：完整SHA、矩阵链核对和两张补图的来源在 [r04d证据附录](APPENDIX_evidence_history.md#split16-window-r04d)。函数表域与非有限边界继续沿用 [norm合同](L3_norm_nonfinite.md#nf-path)及具名M/A1状态，不由本页扩大支持。本轮GPU、模型、整链新运行均为0。
- L3_tin_window.md：正数范数归约可上溢到+Inf；是否被具体RSQ接口吸收按 [非有限合同](L3_norm_nonfinite.md#nf-path)判断，不写成“有限输入保证所有内部有限”。QMMA非有限seed/half overflow、E4 NaN、缺表/域外、参数/区间/窗口画布不满足时仍拒绝，不能用G的饱和量化替前一步放行。长SHA、逐调用配置和旧发布缺项修正记录留在 [TIN证据附录](APPENDIX_evidence_history.md#tin-window-r04c)。本轮GPU、模型、整链新运行均为0。
- L3_workspace_map.md：4K额外的P−T行仍按 [padding合同](L3_workspace_map.md#padding)单列：L58写零，L99只搬逻辑T行；不能把补齐角色画成一对双向有效[token](APPENDIX_beginner_glossary.md#g041)。图和整数例来自 [repack.cpp:26–50、88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26)，本轮只核对闭式/整数例，未运行新payload或GPU门；[完整身份](APPENDIX_evidence_history.md#split16-window-r04d)留在附录。
- L4_fp32_ftz.md：| 本轮小例 | CONTROLLED：[真实C++输出](examples/fp32_ftz_r04e.result.json)为人工RN/[RZ](APPENDIX_beginner_glossary.md#g060)、输入FTZ与守卫检查；新增GPU、模型、整链运行均为0 |
- L4_mufu.md：这核对了选定表项、解码转写、half 发布及一个 libm 反例，没有重新验全部压缩项或全 raw32 数据。本轮新 GPU / 模型 / 整链运行均为 0。


<a id="attention-scope-detail"></a>
## attention 各旧门的范围补充

【验证记录】ViT 与 split16 有具名逐 launch 原生/Python/C++ 对照；TIN 原轮仅部分具名调用实测，其余仍 NOT_RUN。旧跨几何 ViT 的 4K f0 L92 仍保留 1 B DIFF / NOT_ESTABLISHED；split16 的原 MAP_CHECK_FAILED 不升级为通用地图证明。后来固定 4K 自有检查点分段、新进程续接的全链门不改写这些旧记录，也不证明异步中间时序唯一。[原门/分母/负控与范围](APPENDIX_evidence_history.md#attention-evidence)移至附录。

关闭 L62 零覆盖可检出工作区差异而六 POST 相同，故 POST 不能代替 FULL；偏置索引旧负控只限登记的多头/旧路径，不外推到全部家族。没有可按原登记引用的“libm softmax 替代”专名负控，不能虚构已跑；实际图与下方合成例说明算法不同。浮点依赖次序保留，仅满足规则的精确整数部分可重排。


<a id="qmma-source-ledger"></a>
## QMMA 行级源码与旧实验对应表

| 断言 | 当前公开源码 path:line | 实验/裁决记录 |
|---|---|---|
| 矩阵段按字节取值；打包布局与数值解码分开 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:12](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L12)、[同文件:26–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26) | CENSUS；[ARCH 0.7 §7.1](../../../ARCHITECTURE_V3_ZH.md#71-数字格式与转换) |
| seed 可来自调用者；K 每次增加 32，前步 F16 反馈下一步 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:88–100](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88) | [移植 RESULT:15–19](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门)、[RULE:17–22](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star) |
| 目标宏为 sm_120 时，raw / decoded 明确委托同一规则 | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:125–128](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L125)、[decode_reuse.inc:11–13](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/decode_reuse.inc#L11)、[qmma_sm120.hpp:69–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L69) | [移植 RESULT:7–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#实现与定位)；源码分支不代替实际构建身份 |
| F16 矩阵结果与后续 E4 发布为两步 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:98–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L98)、[primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68) | [半域原语 RESULT:43–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md)；二次格式舍入见下层合成例 C |
| 矩阵编码为 E4，辅助缩放/偏置还按 F16 或 F32 读取 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:34–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34) | CENSUS；[ARCH 0.7 §7.1](../../../ARCHITECTURE_V3_ZH.md#71-数字格式与转换) 的存储/计算概括须按字段限定；不列系数值 |


<a id="topic-inventory"></a>
## 页面与同页步骤对应

r04f后为38个Markdown页面：INDEX 1、L0 1、L1 10、L2 10、L3 9、L4 5、附录2。页面数量不是原语全解释或证据全闭合证明。

| 层级 | 独立页面 | 同页覆盖的导航主题 |
|---|---|---|
| L3 | [qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3) | QMMA与有序K32矩阵链 |
| L3 | [b0-noise-reprojection](L3_b0_input.md#b0-noise-reprojection) | B0输入、input-adapter、noise；temporal-sampling的B0[重投影](APPENDIX_beginner_glossary.md#g025) |
| L3 | [ffn](L3_ffn.md#ffn) | 单输入G、通道/矩阵账与前馈残差 |
| L3 | [tin-window](L3_tin_window.md#tin-window) | 四档TIN完整窗口块与编解码外围 |
| L3 | [window-attention / split16](L3_split16_window.md#window-attention) | split16四核完整块、16头、布局与末端变体 |
| L3 | [attention-softmax](L3_attention_softmax.md#attention-softmax) | ViT/窗口分数、half归约、RCP及AV |
| L3 | [norm-nonfinite](L3_norm_nonfinite.md#norm-nonfinite) | tin-norm别名；Q/K范数、尺度与非有限合同 |
| L3 | [workspace-map](L3_workspace_map.md#workspace-map) | repack、角色布局、读写/补齐与发布 |
| L3 | [b70-history-output](L3_b70_history_output.md#b70-history-output) | temporal-sampling的B70采样、output-temporal、postprocess、历史保存与显示 |
| L4 | [hmma](L4_hmma.md#hmma) | F16适配/末端头、K16格点与硬件边界 |
| L4 | [half-arith](L4_half_arith.md#half-arith) | half-fma别名；F16算术、两阶段融合与有序发布 |
| L4 | [mufu](L4_mufu.md#mufu) | 七族函数的包装、认证映射与接受域 |
| L4 | [fp32-ftz](L4_fp32_ftz.md#fp32-ftz) | F32起止、FTZ、舍入、编译与转换例 |
| L4 | [e4m3-format](L4_e4m3_and_k32.md#e4m3-format) / [qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation) | e4m3别名；格式与K32累加共用一页 |


<a id="r04f-review-resolution"></a>
## R2 两份审阅的逐项处理（r04f）

以下C/G编号分别对应[Codex R2](../reviews/REVIEW_OUTSIDER_R2_codex_20261024.md)和[Gemini R2](../reviews/REVIEW_OUTSIDER_R2_gemini_20261024.md)的“十个问题”，不是新实验编号。文档中的当前CPU规则、旧硬件观察及开放问题保持分列。Stage R/P等旧任务标签已从架构正文移除；这里仅为审阅对照保留原称。

| 审阅项 | 处理 | 具体落点与边界 |
|---|---|---|
| C1 跨层矛盾 | 已修 | L1/L2跟随L3；TIN共享seed、split16投影首seed、B0控制10–12及p5=false固定13/14同步；物理布局未知仍保留 |
| C2 可观察图像与两个控制 | 保留缺口，未制作图组 | 见下方图像证据条件；L0列明数值作用与展示边界，不猜视觉任务 |
| C3 对象归属 | 已修 | INDEX仅四个身份起步；原生行为/CPU重建/验证记录标签显式分开，half的binary64块起首标CPU规则 |
| C4 HMMA算术叶 | 已补 | [L4.hmma](L4_hmma.md#hmma)：F16/K16、seed、公共格、发布、拒绝、跨架构、真实C++例；480负零反例不改标 |
| C5 上采样缩放对象 | 已修 | L1.08、L2.08统一为投影主路加缩放skip，即HF(D8(skip),s_skip,projected_main) |
| C6 L1过密 | 已修 | 十篇改为作用/阶段形状/顺序/例外卡；表轴、binary64与重复基础释义移出 |
| C7 入口身份/工程史 | 已修 | DLL、sm_120、样本C、WEIGHTS_HT首屏解释；工程词表移至INDEX后段独立表，详细构建及页面统计留附录 |
| C8 ViT与窗口AV例 | 已补 | [并排例](L3_attention_softmax.md#parallel-av-example)同一人工score/V，经各自φ、分母、两步真实K32算到出口；不把差异全部归给量化位置 |
| C9 证据难读 | 已修 | ViT、FFN、QMMA、attention正文采用断言/直接依据/比较范围/局限四列；旧轮计数和地图状态保留在附录 |
| C10 存储/证明拥挤 | 已移 | half双肢T1及完整程序、E4完整程序、MUFU负轴/LG2/成员裁剪、B0格式/解码守卫移现有附录；舍入、拒绝和未知保留正文 |
| G1 首页工程代码 | 已修 | 与C7相同；遵照r04f明确要求，完整项目词表留INDEX后段的独立标题，不再先于架构入口 |
| [G2](APPENDIX_beginner_glossary.md#g110) L56/L100空间对应 | 部分补充，独立坐标未补造 | [L100实读](L2_06_decoder_bridge.md#byte-trace)给出物理输出0的四个源通道组及已知主路(0,0)；L56给出pooled字节0唯一写事件。两端独立逻辑坐标仍UNKNOWN |
| G3 行内释义重复 | 已修 | L1全系、L2.05及其余点名L2的基础释义集中到INDEX/L0，保留实例形状和调用次数 |
| G4 未定义行话 | 已修 | computed-shared/I03b/027/028/P3在后段词表定义或移附录；六POST在L0资源表明确为id1/2/3/6/9/10；Stage R/P移出正文 |
| G5 φ位域机制 | 已补 | [分数变换](L3_attention_softmax.md#vit-score)说明E=15、固定项模消去、m<<4/5进入新指数/尾数域，含c=1.5人工例；不假定训练设计名 |
| G6 六纹理与控制速查 | 已补 | [L0资源表](L0_frame.md#textures)给ID/角色/格式/尺寸/写入/读取及params作用，空号不猜遮罩 |
| G7 params记号混用 | 已修 | B0/B70正文统一param_f32/u32/u64[十六进制字节偏移]；F32与整数解释分开，不改被引源码 |
| G8 旧章节/占位 | 已修 | 旧3a/3b/3d/3e导航名更新；MUFU过期占位句删除；INDEX区分页面写完与原语算术/证明仍缺 |
| G9 日记与失效链接判断 | 日记下沉；未采纳删除有效链接 | 运行次数/修订回执集中附录，当前边界留正文。examples实际存在，所有本地/跨盘链接与片段核验通过，故保留可用证据链接 |
| G10 ViT模板与块内图 | 已修 | [L2.05](L2_05_vit.md)改共享合同+六行变体表+B31五核图，含640×2048 B half buffer和两条残差 |
| 两审阅的旧项复查/结构建议 | 已合并落实 | 保留完整FFN/TIN/split16中间层与已有图，不另建架构；FFN总图的seed直接进入收缩矩阵/首分片框；泛化“为什么”改页级未知说明，仅保留具体推测 |

**图像展示未采纳的理由与关闭条件。** 本次只对安全路径下的既有PNG文件名作索引，并抽查[旧native-sample回执](../../../experiments/results/native-sample/run.json)，该回执为terminated/native timeout，不能用同目录output.png证明当前固定对象的有效终图。没有据此声称整个磁盘不存在其他图；当前读取材料没有可直接复用且身份完整的同一输入、同一历史及两个控制变化的图像/差分组。应先绑定DLL/资源、输入色彩/MV约定、params、历史状态、原生输出与显示变换，再展示这些保存图像。此文档轮不生成新模型/原生/连续链结果，也不以任意旧PNG填补该缺口。

**坐标示例的边界。** 新例确实执行了整数地图查找和L99已建立重排的逆索引，没有读取权重或张量数值。它补齐“具体哪个字节从哪里来”的可核查实例；把L56或L100输出物理字节直接命名成逻辑(x,y,c)，仍缺独立端点布局标定。应将独立原生标记/来源见证与CPU两端布局逐项核对，不能只从同一地图自证。B69独立布局的最小关闭条件也已写入L2.08，computed-shared一般来源/同步证明仍NOT_ADMITTED。

**执行范围。** 新增[HMMA](examples/hmma_r04f.py)和[attention AV](examples/attention_av_r04f.py)只编译抽取的标量函数并执行人工数据；[地图例](examples/map_trace_r04f.py)只读整数地址资产，先核原绑定SHA。旧实验、模型、系数、数值实现及保护材料没有修改；新增GPU/模型/连续链运行均为0，无暂存、提交或推送。

**验收。** 38个Markdown页面从L0全部可达，1,356条本地链接及片段核验通过；41个原覆盖注释保持，L0–L157共158次调用各覆盖一次，44个核名不变；原8个Python代码块内容保持。三个新增例实际执行通过，9份源/函数表/地图身份复核一致。官方发布扫描覆盖51文件，PASS、BLOCK 0、名称违规0、缺文件0；两项受保护旧措辞未回流。暂存区无本目录改动。


<a id="project-terms"></a>
## 项目与验证术语

这些是证据身份和工程用语，遇到结果表时再查；不属于张量轴或网络层。

| 术语 | 本项目含义 |
|---|---|
| M / M2 | 统一 CPU 封存／其发布子封存；读者须用具名构建绑定结果，代码存在不等于该版本已有所有数值门。 |
| unified seal（统一封存） | 把构建、源和资产身份绑定的冻结交付；不是原生模型名称，也不自动包含后续工作线。 |
| 854… / M9d | 旧构建摘要前缀／数值工作线简称；用来限定已测结果，不表示逻辑层或新M2验收。 |
| A1 | 独立的非有限统计量语义补充分支；其放行与拒绝不能当成公开 M2 已更新。 |
| D03/D02（另有 E1、D） | CPU 函数资产裁剪／原值存储（LG2／噪声编码）工作线；帮助区分函数行为与保存它的办法。 |
| G0b / G1 / G3 / C8 | 地图索引缩窄的旧 CPU 参考／A1 检查点门／A1 检查点门／采集窗口；均非网络层，须按报告核对输入与分母。 |
| “决定 NN” | 项目决策编号；说明规则或授权来源，不是额外硬件观测。 |
| teacher-forced | 每调用注入保存的参考前态；能检验该调用，不能替代 CPU 自有状态连续推进。 |
| WR A/B | A 查自报 written_ranges 稳定；B(i) 查原生变化字节落在自报区间、B(ii) 查 CPU 区间外不变；不替代完整读写集/别名/同步证明。 |
| FULL / FINAL / ROLE（另有 D） | 整片工作区／终图／具名角色比较（D 是累计声明写集）；看范围才能解释 MATCH。 |
| NOT_OBSERVED | 该比较点没有原生观测；不能补写为 MATCH、DIFF 或“没有执行”。 |
| CENSUS / MEASURED / CONTROLLED / INFERRED / PROVED | 读源、具名测量、对照、推断、具名软件证明；最后一项不表示GPU实现已证明。 |
| computed-shared | 计算所得共享中间值的写→读来源及合法读取证明；L133旧证明器尚缺一般操作数血缘、同步和独立仿真语义准入，NOT_ADMITTED不由数值MATCH解除。须补这些独立检查及负控，不能仅重跑终图比较。 |
| I03b | 2026-09-19的B70历史采样阻塞裁决编号；后续输出门已推进，但阻塞解除过程没有完整文字证据，见[B70范围](L3_b70_history_output.md#evidence)。 |
| 027/028 | 非有限诊断所用的两个图像样本编号，非网络层/launch；见[历史见证](APPENDIX_evidence_history.md#norm-propagation-detail)。 |
| P3 | 旧执行器验收的逐调用数值对照阶段；不是网络层级。 |
| Stage B / E4 | 参数变化工作线的156调用路线；E4为tone0/style0捕获，不是E4数格式的别名 |
| G2 | 1080面部/[skin-mask](APPENDIX_beginner_glossary.md#g006)的reset两帧捕获，分片是原生观测拆分 |
| G4 | 1080面部序列16帧的终图捕获；中间workspace未采 |
| L1_1of2 / L1_2of2 | 同一1080三帧控制序列的两个捕获分片；预测进程各自独立，不能拼接CPU状态 |
| D1 | p5时域/无额外aux纹理实现与其控制/SFU准入工作阶段 |
| D2 | 实例切换/feature rebuild工作阶段；不是网络层编号 |
| D3 | 312 B post_block参数布局工作阶段；不是156路线的别名 |
| R0 | 已在CPU数值前撤回的reset控制解释；不是矩阵残差r或指数E |
| R1 | 有限reset子候选：p5时[structure](APPENDIX_beginner_glossary.md#g005)=1、mask取CB两个F32 |
| R2 | 无额外aux句柄的p5时域实现子候选 |
| R2b | 精确S157控制元组谓词扩展；reach STOP后未创建正式seal |
| R2c | 在R2实现上再认证四个S157站点的子候选；终态按其执行seal绑定 |
| job AM-S2 | 源记录的旧任务标签为Q8；320×240 automask/structure=2样本。本串job名统一为AM-S2，Q8(x)只指量化 |
| job S1 | 320×240 skin-face八帧样本；不要与其他章节同名地图产品编号混用 |
| job G1-320 | 源参数变化记录中的G1：320×240 face/skin-mask九帧样本；区别于旧A1检查点门G1 |
| 六POST | 调用后六张纹理id1、2、3、6、9、10的有效区比较；与整片workspace的FULL不同，见[L0资源表](L0_frame.md#textures)。 |


<a id="index-measured-scope"></a>
## 已测实例的边界

1080/1440 的旧多帧门绑定 854，4K 三帧绑定统一 M；M2 的具名新门限于 1080/1440 f0 与 4K L0–L99，不把其余范围改为 M2 新测。sceneA 只比较 FINAL；1440 部分时点缺逐 launch 原生六纹理观测。[原范围、帧数、构建与回执](APPENDIX_evidence_history.md#index-scope)移至附录，跨帧状态详见 [L0](L0_frame.md#两帧之间保留什么)。

本目录按 ARCH 0.7 当前补充及 LATEST 解释旧材料：旧的“1440 停 L133、4K 全链未运行、B0 仅 reset”已被具名实例取代；整网定理仍为 NOT_ESTABLISHED，L133 computed-shared 符号层仍为 NOT_ADMITTED。字节一致不自动证明一般几何、内部值唯一、全部 maps 语义或未测控制分支。


<a id="half-f32-history"></a>
## half/F32旧转换记录与适用范围

全链F32↔F16边界逐站点清单只维护于[L4.fp32-ftz](L4_fp32_ftz.md#sites)。本节只保留历史转换验收与调试回执的适用范围。

保存实验曾定位到调试导出固定乘法舍入点、破坏原生坐标融合；恢复融合后的具名帧结果与输入限制在 [B00 分歧 RESULT:7–33](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据)。该报告当时的帧4/5未运行是历史范围，不能据此否定后续具名多帧验收；这里仅用它确认融合边界及五个采样贡献的次序。

F32→F16 时，先精确扩宽至 binary64，再 half_round；扩宽不增加数值舍入。F16→F32 的有限值与 ±Inf 也可精确表示，但 NaN 载荷另论。项目保存验收的完整 raw32 转换接受 4,278,190,082、拒绝 16,777,214 个输入；half→F32 非 NaN 63,490 项相同，**2,046 个 NaN 仍为正式差异**：CPU 规范化成 0x7fc00000，GPU 为 0x7fffffff。[窄域 RESULT:9、35–46](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L35)。F16↔E4 已在 [E4格式片](L4_e4m3_and_k32.md#e4m3-format) 列出，本片沿用该转换合同。


<a id="workspace-checker-sets"></a>
## 累计写集与比较器规则

### L3.workspace-map.sets 逐调用读写、累计 CumWrites(L) 与未比较区

- 是什么：用声明写范围定义可比较的累计状态；实际变化集合不能替代写入集合。
- 输入 → 输出：每个调用的 roles / written_ranges、前后状态及逐项来源图 → WriteSet(L)、CumWrites(L)、Unwritten(L) 与比较范围。
- 怎么算：
  ~~~text
  1. I_decl(L)=声明输入角色区间之并；Read_ws(L)=有 typed 来源证据的实际读取字节之并。
  2. WriteSet(L)=本调用 written_ranges 的区间并；先排序，再合并重叠或相邻区间。
  3. 首帧从 CumWrites(−1)=∅ 开始；CumWrites(L)=CumWrites(L−1)∪WriteSet(L)。
  4. Unwritten(L)=[0,N) \ CumWrites(L)；UNINIT_NOT_COMPARED=N−|CumWrites(L)|。
  5. Δ(L)={a : PRE(L)[a]≠POST(L)[a]}；它只能给出写入下界。
  6. CumWrites digest=SHA256，依次输入每个合并区间的小端 U64 偏移、U64 长度及区间字节。
  7. 对 CPU 检查 WriteSet(L) 之外 PRE/POST 不变；比较原生时明确实际可见范围。
  ~~~
- 数值规则：同值写零不会进入 Δ，却仍是写入；两次覆盖同一地址的执行次序也不会保存在区间并中。I_decl 是分配跨度，不等于每字节都被数值消费；输入角色只限制读地址，不能单独证明完整 Read_ws。纹理与权重读集另列，不混入 WS 集合。
- 为什么这么算：把数值出口、同步副作用和未触及的初值区别开，使单 launch 与连续链比较使用明确对象。
- 我们怎么知道：CENSUS，[DefinedBytes:5–33](../../../cpp/opt/M/phase2_support/defined_bytes.py#L5)；CONTROLLED / MEASURED，[规范定义:11–28、48](../../../experiments/b1-dl-canonical-definition-20261010/DL_CANONICAL_ZH.md#1-规范定义)，旧 write-once / 无条件“读≤写”说法的边界见 [V2-08-005](../../arch-v2/08.02_read_write.md#v2-08-005)。
- 往下：[双填充](L3_workspace_map.md#fill)、[padding 同值零写](L3_workspace_map.md#padding)、[WR 检查](L3_workspace_map.md#wr)。


<a id="workspace-checker-fill"></a>
## 累计状态计数与00/A5比较协议

**CumWrites 与未初始化区的具体数目。** 本轮重读原生普查中的三档 params 字数组，核对 L1、L2 两出口相邻，得到 CumWrites(2)=[0,clear+full+pool)；本轮未重新解包原捕获：

| 实例 | CumWrites(2) 长度（B） | UNINIT_NOT_COMPARED（B） |
|---|---:|---:|
| 1080 | 88,861,696 | 123,658,240 |
| 1440 | 151,323,648 | 189,399,040 |
| 4K | 335,554,560 | 427,507,712 |

1080 冻结记录还给出 |CumWrites(6)|=168,487,936 B，从 L99 起 CumWrites=N；它是累计**声明**写集经指定原生范围核对零差，不是从 GPU 数据变化直接推得“原生实际写过的全部字节”。多帧保留前帧工作区时，累计定义状态也保留；不能在每帧重新把它误记成全部未知。

### L3.workspace-map.fill 00 / A5：已写字节与保留字节

- 是什么：在相同有效输入下改变初态填充，检查已定义结果是否依赖未写区。
- 输入 → 输出：F=00 与 F=A5 两次具名运行 → CumWrites 内的结果对照，以及补集保留规则。
- 怎么算：
  ~~~text
  1. 首帧 WS 用 F 填满；单 launch 教师强制另把指定前态的 CumWrites(L−1) 贴回。
  2. 执行调用，累加声明 W 得到 CumWrites；不以两次填充的差异反推 CumWrites。
  3. 比较 CumWrites 内候选与具名参照；另查声明外无写。
  4. U 内 CPU 字节继续保持 F；原生 U 未观察时记 UNINIT_NOT_COMPARED。
  5. A5 对照 fill00 原生时：已写区逐字节等于参照，补集逐字节仍为 A5。
  6. 仅当 CumWrites=N，或双方初值相同且声明外无写均有证据时，才可按相应范围合并成 FULL。
  ~~~
- 数值规则：同 fill 的 CPU FULL 匹配可包含尚未写过的相同初值，不自动是 GPU FULL 匹配。早期 1080 两 fill 的 CumWrites digest 158/158 相同，而 FULL SHA 只有 L99–L157 的 59/158 相同；两种填充是有限证伪检验，不能证明对任意初值都独立。
- 为什么这么算：让误读未写字节更容易暴露，并区分算法结果与缓冲残留。
- 我们怎么知道：MEASURED / CENSUS，[CumWrites 规范:77–88](../../../experiments/b1-dl-canonical-definition-20261010/DL_CANONICAL_ZH.md#4-调和规则)；后来 T4K 的实际 A5 / FULL 范围见 [多帧 RESULT:23–32](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L23)，其 f0 L0 FULL 为 NOT_OBSERVED。
- 往下：[WR A/B 的不同保证](L3_workspace_map.md#wr)、[padding](L3_workspace_map.md#padding)。


<a id="workspace-checker-wr"></a>
## WR A/B独立判定

### L3.workspace-map.wr WR A/B 分别查什么

- 是什么：对声明范围的稳定性、原生可见变化和 CPU 范围外修改分别检查。
- 输入 → 输出：冻结 written_ranges、CPU PRE/POST、原生可用 PRE/POST → A、B(i)、B(ii) 的独立判定。
- 怎么算：
  ~~~text
  1. A：本次 CPU 自报 written_ranges 必须等于冻结期望元数据。
  2. B(i)：原生前后快照可用时，检查其变化字节 Δ_native(L)⊆WriteSet(L)。
  3. B(ii)：调用 DefinedBytes.check_unreported，要求 CPU 在 WriteSet(L) 外逐字节不变。
  4. 缺原生快照的项记 NOT_EVALUATED，不用同 fill 初态替代观测。
  5. 越界写、漏段、范围平移等负控必须被相应检查拒绝。
  6. 字节比较、A、B 及符号准入分别报告；其中一项通过不能替换其余项。
  ~~~
- 数值规则：A 的期望来自同 seal 的 native-MATCH 回执中 CPU 自报范围，证明的是运行间元数据稳定；B(i) 只检查可见变化，捕捉不到所有同值写；B(ii) 是这次 CPU 执行的范围外不变，不是全输入的硬件无别名定理。
- 为什么这么算：把“声明一致”与“执行未越界”分别检查，防止只比较主要张量而漏掉发布标记或 padding。
- 我们怎么知道：CONTROLLED / MEASURED，[continuation6 WR4K:60–79](../../../experiments/b1-arch-v3-refresh-r01-20261023-codex/continuation6_RESULT_ZH.md#wr4k决定-232026-10-17)：A 158/158，B(i) 156 PASS、L0/L1 NOT_EVALUATED，B(ii) 158 PASS；负控与实际首尾状态均具名记录。
- 往下：[三帧链的最新范围](L3_workspace_map.md#evidence)、[区间算法](../../../cpp/opt/M/phase2_support/defined_bytes.py#L3)。


<a id="workspace-example-code"></a>
## repack索引例与检查器元数据的完整脚本

~~~python
from pathlib import Path
import re,struct,json
src=Path("E:/GlassBox-NR/cpp/fam_repack/repack.cpp").read_text(encoding="utf-8-sig")
dest=list(map(int,re.search(r"kBitDest\[12\]\s*=\s*\{([^}]+)\}",src)[1].split(",")))
assert sorted(dest)==list(range(12))
def pi(x): return sum(((x>>b)&1)<<d for b,d in enumerate(dest))
old=Path("experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/oldmap")
for rows,cols in [(20,32),(24,40),(36,60)]:
 row,col,c=5,7,37
 token=row*cols+col
 tile=(row//4)*((cols+3)//4)+col//4
 slot=4*(row%4)+col%4
 tiled=(tile<<12)|pi((slot<<8)|c)
 raster=((token//16)<<12)|pi(((token%16)<<8)|c)
 for launch,at,expected in [(58,raster,tiled),(99,tiled,raster)]:
  with (old/f"old_L{launch}_{rows}x{cols}.u32").open("rb") as f:
   f.seek(at*4);assert struct.unpack("<I",f.read(4))[0]==expected
 print(rows,cols,"token",token,"tile",tile,"slot",slot,"pi",pi((slot<<8)|c),
       "tiled_chunk",tiled,"raster_chunk",raster,"byte_offsets",4*tiled,4*raster)
root=Path("experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence")
j=json.loads((root/"equiv_old_maps.json").read_text(encoding="utf-8"))
dim={k:v for k,v in j.items() if re.fullmatch(r"\d+,\d+,\d+",k)}
print("saved_dimension_direction_results",len(dim),
      "valid_hashes",sum(not v.startswith("ERR") for v in dim.values()),
      "rejections",sum(v.startswith("ERR") for v in dim.values()),
      "other_controls",len(j)-len(dim))
data=json.loads(Path("experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json").read_text(encoding="utf-8"))
N={"1080":212519936,"1440":340722688,"2160":763062272}
def q(L,g):
 u=next(r for r in data["launches"] if r["launch"]==L)["resolutions"][g]["params_u32_le"]
 return [u[i]+(u[i+1]<<32) for i in range(0,len(u),2)]
for geo,n in N.items():
 a=q(1,geo);b=q(2,geo);base=a[0];clear=4*(a[1]&0xffffffff)
 nw,nh=b[30]>>32,b[30]&0xffffffff
 full=nw*nh*32;pool=(nw//2)*(nh//2)*32
 assert b[27]-base==clear and b[31]-base==clear+full
 print("geometry",geo,"N",n,"clear",clear,"full",full,"pool",pool,
       "D2",clear+full+pool,"U2",n-clear-full-pool)
~~~


<a id="mufu-counterexample-identifiers"></a>
## 特殊函数反例的原登记编号

## 为什么不能改用 libm 或朴素闭式

- [RULEDOUT-MUFU-LG2-LAW](../../../knowledge/RULED_OUT_ZH.md#ruledout-mufu-lg2-law) 记录：最小正正规数的实测 lg2 不等于精确整数 −126，254 个二幂输入中 126 个不精确。文末实际读取保存编码 0xc2fbffff，而当前 libm 转 F32 是 0xc2fc0000。
- [RULEDOUT-c7b4080777](../../../knowledge/RULED_OUT_ZH.md#ruledout-c7b4080777) 记录相邻指数缩放仍有失败段；E1 用实测三位等级修正，不是把失败的 lg2 约简律重新宣称成立。
- [RULEDOUT-f1623cdd85](../../../knowledge/RULED_OUT_ZH.md#ruledout-f1623cdd85) 保留错误误差界导致半径域估计错误的反例；先取数学值再给宽松容差，不足以支持逐字节一致。
- [噪声证明 RESULT:46–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L46) 实测朴素三角反射、半周期与四分之一移位互推均有大量位差；完整残差保留了这些不规则值。
- [RULEDOUT-MUFU-71BLOCK-SCOPE](../../../knowledge/RULED_OUT_ZH.md#ruledout-mufu-71block-scope) 还说明仅按 71 个[逻辑块](APPENDIX_beginner_glossary.md#g036)会漏最终显示核；本片按完整 L2 路径定位，不静默沿用旧 154 次调用范围。

这些条目有各自年代与范围；例如旧条目“sm_120 尚未测”已被后来具名 14 变体记录推进，原有失败与限定不删。可精确计算的是认证数据的索引、整数解码、位型修正和已验收缩放；超越函数映射的未记录值不由这些公式自动产生。


<a id="r04g-review-resolution"></a>
## R3逐项修订与例子范围（r04g）

对应[Gemini R3完整审阅](../reviews/REVIEW_OUTSIDER_R3_gemini_20261026.md)。仅写本目录；读取源码、整数地址和认证函数资产，不改运行时、旧实验或外部文件，不运行GPU/模型/整链，不暂存或提交。

| R3 Top-10项 | 处理与正文落点 |
|---|---|
| 1 L100/L56[算子](APPENDIX_beginner_glossary.md#g035)直觉 | L1.06/L2.06/L3.split16前置4×256归约；固定1080地图全输出的四组来源/非通道坐标已核，L56按8192 B分桶的40桶与64×40→32×20容量相容；每窗4×4空间配对仅为【推断】，尚缺独立坐标标定。没有补认标准[均值](APPENDIX_beginner_glossary.md#g044)池化或唯一插值 |
| 2 INDEX工程术语/旧边界 | 两个整节移至本附录project-terms/index-measured-scope，INDEX各留一行链接，保留对象标签和架构导航 |
| 3 九页重复记号表 | 每页只留3–5个局部条目，格式、运算及证据标签集中INDEX |
| 4 多义数学记号 | 全文Q8/D8；指数E；Den分母、CumWrites累计写集、Partials部分和、Radius半径、[Hash32](APPENDIX_beginner_glossary.md#g075)整数散列、HSL_Fwd/HSL_Rev分解分别命名；F32运算用F32+/×/除与F32_FMA。真实源码函数名保留为实现标识 |
| 5 重复未知/系统解释 | L1十处重复动机说明归口INDEX；窗口尺寸守卫与角色/发布交接是读源事实；跨窗收益及资源压力因果另标推测 |
| 6 偏移代入 | t=9,h=0,d=4的Q/K/V=84/88/289 B，与真实取数坐标及绑定map相同；B0真实输出循环full=85、pool=30741 B，分别说明坐标和位段 |
| 7 跨页重复 | B0 L2压为五行步骤表+图；F32站点只在L4.fp32维护；half留转换规则并补ViT/FFN/attention回链 |
| 8 悬空编号/残句 | D27和guard 4用功能名称解释；MUFU反例编号移本附录；尾段残句补全，L1.09采用当前简卡文本 |
| 9 复杂数值例 | 人工TEX联合8位分数权重/截断/中点、[五tap](APPENDIX_beginner_glossary.md#g029)像素、L157两轮HSL真实代码体全部实算，记录中间值和输出编码 |
| 10 workspace测试协议 | 累计集/00-A5/WR判定及Python检查脚本移本附录；正文留角色、实际读写边界、repack/补齐/索引与结果表 |

**Missing/cut/结构建议对应。** L0增加六项“它不是什么”框，每项链到既有算术/接线页；图旁说明1080→1152来自实际内部画布合同并给镜像行代入。L0另汇总各调用已知params字节偏移子集，不声称完整ABI。新增[L4.tex-filter](L4_tex_filter.md#tex-filter)，把已存在的采样器位级规则从B0 L3下钻，保留L3过滤接口。已有五层骨架、六纹理表、完整块及形状图不重建。

**未按字面采纳的范围。** “所有残差均在第一矩阵seed加入”不适合作为未经限定的全家族定理：本串ViT contract含首分片与有序half合并，projection按其具名图保留接口；L0框只说实际seed/部分和接线不可移为末端实数加法。R3将HMMA概括成与QMMA同理的17项，也不能解除原有负零反例、B0全零早退或B70守卫；L4.hmma原证据状态不变。资源预算造成拆核的说法没有本轮独立测量，因此只列为推测。

**受控视觉图组仍未补入。** 现有阅读材料没有绑定同一输入、历史、参数及控制变化的完整可复用图组；旧超时回执不能作终图证据，详见[r04f缺口](#r04f-review-resolution)。本轮新增例是人工标量/像素，不冒充网络输出或视觉对照；未为补图另跑模型。

**实算与复跑。** [geometry_r04g.py](examples/geometry_r04g.py)只查已钉SHA的整数地图；[substitutions_r04g.py](examples/substitutions_r04g.py)抽取真实half/纹理/时域/s157与布局表达式，用人工数据运行。所有编译中间件在本目录内部创建和清理；原函数与仅增加日志的副本逐输出字节相同，认证函数原值缺失会抛错，不以libm回退。原八个Python工作例改名后逐个复跑，算术AST在名称归一后保持；数值结果与验收记录由[校验报告](examples/r04g.validation.json)保存。


<a id="param-change"></a>
<a id="param-change-r04h"></a>
## 参数变化r01：B/C/D1接受证据回填（r04h）

【子候选／保存测量，非M/M2】权威范围取[总报告](../../../experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md)、[B](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_B_ZH.md)、[C](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_C_ZH.md)、[G2终态](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c_r1/G2_RESULT_ZH.md)、[D1终态](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1_ZH.md)及[D1A认证细节](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1A_ZH.md)。D1A/诊断中的RUNNING与STOP是历史，不能覆盖D1最终终态；各阶段不同seal也不合并为一次回归。M/M2及旧证据保持。

| 候选身份 | content seal SHA-256 | execution seal SHA-256 |
|---|---|---|
| Stage B | 8d84018cc8e3297c78b9c841ae215680a0c3751bb27d8ac6937113804c6f4db8 | e65a7eaead43d9b3dd8a4384a42e109bea0d932b04430ac5eb6d3cd721c54662 |
| R1 / G2 | f7335470fed0810740b27d33c48f53b44f00572c0af63035f04ee9b2de62de93 | e985763908112f63c8720bc33a6b3fce085d78816cf158cbf46baf68353c0f1a |
| R2（原STOP保留） | 905bf2b65362cbf04d38862429be8bfc1846b1270a245dfd5447007dd73c3b6e | a69cacce8e2bc4bd1ccb5ea1332b4ef3342bfadfc89895bf03ccea9b8449e748 |
| R2b（reach STOP） | 未创建正式candidate seal | 未创建正式execution seal |
| 最终R2c / L1 | fed491ba117f2d3b24b815d2f2d401471e3570edcd67f106fed3abd9cb577d0a | 699d97f81439171b69319e54d9458804ff61b0a17fae4c93fe045c423bc1f1fe |
| 最终R2c / G4 | 同一R2c content | 690a3256b6d7f8a66aa6eb5eb0d9747fd02cb700c601330b138773bc6ed23d13 |

Stage B接受范围是E4两模式tone0/style0，每模式单进程自有状态f0→f1、fill00、1080：四帧624完整workspace MATCH、4 FINAL及4 copy6 MATCH、624 WR B(ii) PASS，分片并集FULL无缺口。四纹理1/2/3/6与默认158路六纹理不同；六POST、WR B(i)仍NOT_RUN。

R1 G2为315 FULL MATCH、1 FULL NOT_OBSERVED、2 FINAL MATCH、316 WR B(ii) PASS；原生history缺失。R0忽略CB+0xb8 (u64)（含两个F32字段）解释因[同上传reset原生判别](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/NATIVE_B00_DISCRIMINANT_C.json)被否定并[撤回](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/WITHDRAW_R0.json)，数值模型调用0。旧copy6诊断错误把显示id2当history，不能把该错误比较记录当已成立的history数值DIFF；[诊断](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c_r1/DIAG_COPY6_ZH.md)只纠正身份，原生id6/id9仍NOT_OBSERVED。

| 最终R2c job | 调用 | FULL MATCH / NOT_OBSERVED | WR B(ii) PASS | FINAL MATCH |
|---|---:|---:|---:|---:|
| L1_1of2，各自f0→f2 | 474 | 236 / 238 | 474 | 3 |
| L1_2of2，各自f0→f2 | 474 | 237 / 237 | 474 | 3 |
| G4，f0→f15 | 2528 | 0 / 2528 | 2528 | 16 |
| 合计 | 3476 | 473 / 3003 | 3476 | 22 |

两L1预测轨迹独立，不拼接CPU状态；观测并集为f0 L1..157、f1/f2 L0..157。重复的三个L1 FINAL只代表三个逻辑帧，22份FINAL合计19个不同逻辑帧。L1_1of2的f1/f2 L2全workspace及B00_FULL/POOL均零差，2of2该点未采。G4全部中间FULL未采；3003个缺口不计MATCH，所有原生history另为NOT_OBSERVED。WR B(i)/六POST NOT_RUN。

R2的固定控制STOP与R2b的reach STOP分别见[S157控制诊断](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1_r2/DIAG_S157_GUARD_ZH.md)、[SFU站点诊断](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1a_r2b/DIAG_REACH_GUARD_ZH.md)。最终R2c独立S157为4/4：1份新元组R2 CPU-own输入、3份父元组原生函数输入；不是四条连续链。R2b无正式seal，不能虚构其独立完整回归。R2c只扩reach并重编outtail，保留原颜色算术/codec/资产；单half域认证也不关闭跨通道lg(gray?1:S)的全域绑定，后者仍OPEN。

<a id="param-change-tuples-r04h"></a>
### R2b→R2c的精确控制元组

父入口另按浮点数值比较，δ=+0/−0均可通过；下表15项才是精确u32匹配，完整准入为两者OR，见[父谓词修订](L3_b70_history_output.md#parent-predicate-r04l)。

【子候选谓词，非M/M2】列顺序为字节偏移0x120/0x144/0x14c/0x150/0x154的I/a/b/c/δ，表项是五个u32位型，不是模型权重。原父元组为3f800000 bdcccccd be800000 bdcccccd 00000000；另加下列15个调查元组，不插值。它们来自[四站点枚举表](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/REACH_CENSUS.json)，元组谓词准入及SFU有限half域认证不等于每组已有原生图像输出或连续链验证。

| 调查序号 | I / a / b / c / δ 的精确u32 |
|---|---|
| 0 | 3f800000 00000000 00000000 be19999a 00000000 |
| 1 | 00000000 bdcccccd be800000 bdcccccd 00000000 |
| 2 | 3e800000 bdcccccd be800000 bdcccccd 00000000 |
| 3 | 3f000000 bdcccccd be800000 bdcccccd 00000000 |
| 4 | 3f400000 bdcccccd be800000 bdcccccd 00000000 |
| 5 | 3fc00000 bdcccccd be800000 bdcccccd 00000000 |
| 6 | 3f800000 bcf5c290 bd99999a bcf5c290 00000000 |
| 7 | 3f800000 bd4ccccd be000000 bd4ccccd 00000000 |
| 8 | 3f800000 bd8f5c29 be333333 bd8f5c29 00000000 |
| 9 | 3dcccccd bdcccccd be800000 bdcccccd 00000000 |
| 10 | 3ea8f5c3 bdcccccd be800000 bdcccccd 00000000 |
| 11 | 3f666666 bdcccccd be800000 bdcccccd 00000000 |
| 12 | 3f7fbe77 bdcccccd be800000 bdcccccd 00000000 |
| 13 | 3f800000 bccccccd bd800000 bccccccd 00000000 |
| 14 | 3f800000 bd75c290 be19999a bd75c290 00000000 |

**未覆盖范围。** D2 instance switch/feature rebuild五帧、D3 312 B post_block八帧均REFUSED/NOT_RUN，另一工作线in progress；两类重叠2帧，共11个唯一帧。独立S157余75条为NOT_RUN_STATE_UNAVAILABLE，不以L1/G4补填。320×240 job AM-S2 / job S1 / job G1-320为NOT_RUN_GEOMETRY_UNSUPPORTED_T64_FFN_CONTRACT，原job AM-S2 f0 L60的模板合同拒绝不绕过；不是一般320算法已验收。最终同一seal的Stage E/F全回归NOT_RUN。

**本次文档工作。** 新增模型/GPU/整链/SFU全域扫描均为0；仅运行[人工CB标量控制](examples/param_change_r04h.py)，其[R2源码SHA/半精度结果](examples/param_change_r04h.result.json)与[接受报告身份及计数投影](examples/param_change_r04h.evidence.json)可检查。只写本目录，不提交；链接、默认158/158覆盖与发布扫描见[本轮校验](examples/r04h.validation.json)。


### 撤回判别与函数站点认证的完整账

**R0撤回。** R0曾把该reset解释为“保留原structure、忽略CB+0xb8 (u64)（含两个F32字段）并令两个mask为−1”。在CPU数值前，同上传SHA、counter0、其余B00参数相同而仅CB+0xb8 (u64)改变的原生两帧，B00 FULL有43,177,878 B、POOL有10,627,432 B不同，否定忽略mask的解释；不唯一确定内部实现。见[原生判别](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/NATIVE_B00_DISCRIMINANT_C.json)与[撤回记录](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/WITHDRAW_R0.json)。R0数值调用0，不计作数值DIFF或失败修复。


## S157：R2c子候选的四站点reach再认证

【子候选保存测量复核，非M/M2】R2b的原父＋15个精确控制元组不改变颜色算术；最终R2c对15个新元组各枚举全部65,536 half，63,488有限码完成、2,048非有限码仍拒绝。id9 RGB进入四站点，id10只作末端混合[基底](APPENDIX_beginner_glossary.md#g003)。site0/site2新增LG2块127，联合域{0,103..127}；site1/site3新增EX2块0及372..378，联合域{0,372..387,511}；块号是raw32>>23，不是程序地址。保留原validity与其他guard，控制元组枚举不等于任意float或任意跨通道颜色的准入。

| 表成员 / 站点 | R2c沿用的实测backing及运行表示 |
|---|---|
| LG2 127 / site0、2 | 完整实测base_E127.bin，33,554,432 B，原值直接读取；其余LG2块按既有E1认证表示 |
| EX2 372/373 / site1、3 | 保存的完整原始块作硬件SHA参照，运行仍用未修改ex2.bin整数codec；非libm替代 |
| EX2 374..378新增、379..387既有 | 未改ex2.bin基表及已对完整硬件块SHA验收的整数codec |
| EX2 0/511 | 保存FTZ常量或−Inf单点的认证表示；NaN仍拒绝，不能把整个特殊值块写成全域准入 |

[SITE_TUPLE_BACKINGS](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/SITE_TUPLE_BACKINGS.json)逐元组/站点/块绑定测量文件、硬件全块SHA及运行表示，44个成员无缺失；[REACH_CENSUS](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/REACH_CENSUS.json)给出实际half计数。旧35块293,601,280输入的R2/R2c values/validity SHA完全相同；新增9块75,497,472输入的编译lookup与保存硬件全块SHA相同。保存sm_75/sm_120的14变体7,168对摘要重读一致；属于旧测量复核，本轮新增GPU=0。[D1A证书说明](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1A_ZH.md)的运行中状态由[D1最终报告](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1_ZH.md)取代。

最终R2c独立S157 4/4 FINAL MATCH：1份新控制的R2 CPU-own输入＋3份父元组函数输入；后者非连续链。75条缺状态记录仍NOT_RUN_STATE_UNAVAILABLE；跨通道lg(gray?1:S)全域调用绑定仍OPEN。测量全域、codec有效域、site reach、独立函数结果与连续链逐层记账；M/M2不变，也不扩大到未测设备/驱动、旧ELF或任意参数。



<a id="r04i-review-resolution"></a>
### R4逐项处理（r04i）

1. 参数变化账：INDEX/L0–L4只留分支的输入、公式与接线，标记measured on child candidate并单链到本节；分片、计数、撤回、STOP、未运行范围统一保留于param-change。
2. 代号：project-terms补齐Stage B、G2/G4、D1–D3、R0–R2c、两个L1分片及320任务；job AM-S2取代与Q8(x)冲突的旧job标签，源标签映射只在词表。
3. CB记号：叙述、伪代码、图及速查表统一CB+0xNN (f32/u32/u64)；实现脚本的真实字段名和数组访问不改名。
4. 地址图：workspace-map增加inp/sread/xsite/wload→算术DAG→16 B gstore→角色切分图，明确A/Y是执行轴，不冒充逻辑头/窗闭式。
5. 实算：原B70颜色片段、置信FMA及认证EX2/RCP包装计算人工像素；真实repack swizzle展开0x725→0x276；原half_round计算RN16(√32)=5.65625。
6. 算子直觉：解释当前色加预测残差及Q的[RMS](APPENDIX_beginner_glossary.md#g053)尺度；数学事实不标训练推测，保留各发布点和未知硬件成因。
7. L4：LG2 E1与EX2正/负支位级规则回正文，原值表/等级容量留CPU附录，函数站点认证账归本节。
8. 排版：去掉L100整段重复，补L1.04窗口几何、L2.04实际已知MKN、L2.07逻辑交接；修重复标题/锚点、残句和中文词内空格。
9. 脚本：B70内联Python原样移至examples/b70_rz_copy_r04i.py，正文只保留输入输出。
10. 路径：INDEX给出v2源码、私有records、工作线地图、早期Python和10600T迁回副本的角色及可打开条件；链接文字去机器盘符。

Missing/cut：L0新增六行数值域表与阶段矩阵字节/逻辑MAC表，保留图层骨架；早期零写事件计数移padding-bug。未补完整split16/整网MAC及物理权重分摊：现有文档未闭合全部QKV、编码双出口和L57内部MKN，只给已证矩阵的小计；不把输出宽度猜成一层dense。表排除bias/scale/对齐，资源容器字节数不与运行时矩阵槽位相加。没有受控新视觉素材，未另跑图像/模型来补图。HMMA零符号及宿主字段命名增加NOT_RUN闭合方案，不将计划冒充新测量。

本轮只读源码、函数表与身份元数据，新增模型/GPU/整链运行0；[计算脚本](examples/anatomy_r04i.py)、[真实输出及形状整数](examples/anatomy_r04i.result.json)、[文档校验](examples/r04i.validation.json)保存范围。所有编译临时文件在本目录内部建立和清理；旧验收、M/M2及子候选均未改动，不提交。

<a id="r04j-fact-resolution"></a>
## r04j：事实审计修订与两篇导读

只处理[事实审计R1](../reviews/FACT_AUDIT_R1_codex_20261027.md)；另外两份审阅未读、未执行。三组非CORRECT项及跨页冲突统一如下：

| 项目 | 修订结果 | 直接依据 |
|---|---|---|
| C281／WRONG | INDEX、B0、B70、纹理L4及本附录全部恢复为1/256定点小数格／联合8位分数权重；br=(a*b+128)/256为整数除法。保留B0真正的CB+0x40 u64句柄槽；采样函数不读CB | [native_temporal.hpp:10–19](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L10)，[真实句柄合同](L3_b0_input.md#p5-candidates) |
| C282／OVERCLAIM | L1.04、L2.04、L2.06、L3.split16统一将每8×8窗配4×4空间出口标为【推断】；保留8×5、64×40、32×20和20,480×16 B的整数事实，区分40个8192 B容量桶与空间坐标。补出输入窗及pooled字节的独立(x,y,c)映射、逐事件来源/目的配对，以及L100输出/skip坐标的闭合条件 | [geometry_r04g.py:48–61、77–84](examples/geometry_r04g.py#L48)，[统一几何边界](L3_split16_window.md#heads) |
| C283／CORRECT_BUT_IMPRECISE | L4.mufu与CPU存储附录明确：注册核实际SHA，换入映射前核fd身份，缓存命中复用已映射页；无逐查询检测外部变化保证 | [full_raw_registry.hpp:28–39、53–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L28) |

其余跨页重复计数与M/M2/child归属按审计已有通过范围保留，没有新增数值验收。[对象与方法](L0a_object_method.md)解释固定DLL、捕获种类、复现判据与证明边界；[确定性](L0b_determinism.md)逐项绑定历史原生、M、M2或child的证据，明确两版旧驱动只有摘要、原始配对记录未见。场景与参数QA继续链接本附录，未合并成新的统一seal。

本轮只写skewer，新增GPU、CPU模型、连续链及原语扫描均为0；没有网络、SSH或版本控制操作。旧脚本、输出、收据及内联算术不改；[变更前身份](examples/r04j.baseline.json)、[纯文档校验器](examples/verify_r04j.py)、[校验回执](examples/r04j.validation.json)、[发布扫描](examples/r04j.leak.json)保留检查范围。

<!-- beginner-r04m:start novice-resolution -->
<a id="beginner-review-r04m"></a>
## 本轮入门教学层与验收范围

针对[新手审阅](../reviews/REVIEW_NOVICE_R5_codex_20261027.md)，新增整帧作用图、完整小块、历史时间线、有限数点小篮和111组词义；[25处逐项处理账](examples/r04m.review_resolution.json)记录落点及未定项。原44页专家正文可完整还原，旧证据状态不升级。本轮未重新进行新手复述/绘图验收，该项仍为NOT_RUN。

两组PNG/SVG只用人工分数和概念色块，图内均有人工教学标签；未使用模型系数、激活或真实前后画面对照。[最终文档检查](examples/r04m.validation.json)与[发布扫描](examples/r04m.leak.json)保存本轮结果；新增GPU、模型、整链和编译运行均为0。
<!-- beginner-r04m:end novice-resolution -->
