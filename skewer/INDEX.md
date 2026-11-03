# GLASSBOX-NR：从一帧到算术的洋葱烤串

<!-- beginner-r04m:start entry -->
<a id="beginner-entry"></a>
## 先用一张图的故事读它

送进来的是**当前图、移动信息、可使用时的上一帧保存结果，以及控制数**；出来的是与输入一样宽高、颜色经过修改的图。中间先处理一层层内部数字，末端再用它们修改颜色。**总体视觉目的仍未知**，不能仅凭名称给它指定某种画面增强功能。

一个位置旁边的“数字卡片”是内部保存的一串数：**[特征](APPENDIX_beginner_glossary.md#g008)**就是这些内部数，**[通道](APPENDIX_beginner_glossary.md#g007)**是每位置有几项；“每位置32项”不等于32种颜色或32帧。**块**是一段接收、处理、交出数字的计算；**[skip](APPENDIX_beginner_glossary.md#g016)/旁路**把较早的数保存下来，绕过中间一段再接回；**[launch](APPENDIX_beginner_glossary.md#g080)/调用**是让设备执行一段程序的一次请求，一个块可能分几次调用。

**暂无条件齐全的成对画面证据**：本串尚缺[绑定](APPENDIX_beginner_glossary.md#g103)同一对象、输入、[历史](APPENDIX_beginner_glossary.md#g024)和控制变化的完整对照组，所以这里不用零散PNG充当效果展示。下方图与人工小例只解释接线及算术，不是视觉测量。[展示边界](APPENDIX_evidence_history.md#r04f-review-resolution)

第一次可按这条短路阅读：[整帧作用图与六条旁路](L0_frame.md#beginner-frame) → [从零学一块](L1_00_one_block_primer.md) → [两帧加一次重置](L1_00_history_primer.md) → [有限数点与32项小篮](L1_00_numbers_primer.md) → [L1十阶段：从图外前置开始](L1_01_prepare.md)。精确算术可在完成十阶段后按需下钻。遇到生词点词名，或查[111组入门词义](APPENDIX_beginner_glossary.md)；构建与检查代号不是网络层。

阅读深度：本页是目录，[L0](APPENDIX_beginner_glossary.md#g081)/L1/L2/L3/L4表示逐层深入。<br>执行编号：launch L0–L157另指默认158次调用。<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B0–B70是逻辑块，不是阅读层级。先看中文作用图，再查下面的精确编号、格式和证据。
<!-- beginner-r04m:end entry -->

[公式覆盖与未闭合项](APPENDIX_evidence_history.md#formula-open-r04l)：默认[闭式](APPENDIX_beginner_glossary.md#g020)1731/1824，[TABLE](APPENDIX_beginner_glossary.md#address-status)87、UNKNOWN6；原审计行最弱项计6/44闭式族，将额外thread_class纳入后为4/44；导航覆盖与公式闭合分别计数。

【原生行为／已测范围】当前颜色与显示输出同为 W×H；显示将[处理后状态](APPENDIX_beginner_glossary.md#g002)与保存的[颜色基底](APPENDIX_beginner_glossary.md#g003)按 [intensity](APPENDIX_beginner_glossary.md#g004) 混合，[style](APPENDIX_beginner_glossary.md#g005)/tone/structure/[automask](APPENDIX_beginner_glossary.md#g006)/skin 的具名控制会改变输出（见 [控制范围与 skin 条件](../../../ARCHITECTURE_V3_ZH.md#L1792)、[B0 控制](L3_b0_input.md#channels)、[尾段](L3_b70_history_output.md#postprocess)）；这些作用尚未确定总体视觉目的，不从产品名推导“降噪／风格化”等用途。
固定身份只取四项：[DLL](APPENDIX_beginner_glossary.md#g078)为nvngx_dlssnr.dll 310.8.0.0；sm_120是目标GPU的SM 12.0架构标识；“签名样本C”是本项目核对的二进制样本身份，不是图像类别；[WEIGHTS_HT](APPENDIX_beginner_glossary.md#g079)是该DLL中的权重资源标识，不在这里列资源数值。

**【原生行为】**指[目标二进制](APPENDIX_beginner_glossary.md#g001)的可观察行为；**【CPU 重建】**指项目源码的复现规则；**【验证记录】**指绑定构建、输入和比较范围的结果。三者分别标注，读源不自动成为硬件测量。

## 这根烤串怎么读（15 行）

1. 第一次读，先看[对象与方法](L0a_object_method.md)，再从 [L0 一帧](L0_frame.md) 看输入、输出和历史回路。
2. 按下表选 L1 阶段，先确认它在默认帧中的位置。
3. L2 页列出调用家族；层级 L0/L1 与 launch L0–L157 是两套编号。
4. 沿“往下”进入 L3，看[算子](APPENDIX_beginner_glossary.md#g035)的输入、公式和[发布](APPENDIX_beginner_glossary.md#g091)顺序。
5. 需要核对数格式、累加或舍入时，再进入 L4。
6. 本串默认覆盖 158 次调用；156 路线与控制变体另列支持边界。
7. 形状和资源身份跟随实际 [params](APPENDIX_beginner_glossary.md#g083)；文件名和 kernel 名不替代内容。
8. 区分[逻辑](APPENDIX_beginner_glossary.md#g085) T、物理 P、空间补齐和真正的零写。
9. CPU计算接线以具名发布源码为主；原生结论须另有观察，数值结果绑定各自构建和输入。
10. 每片的“我们怎么知道”区分读源、实测、控制和推断。
11. 小型实算例用于核对公式，不计作新 GPU 或[整链门](APPENDIX_beginner_glossary.md#g102)。
12. 比较先看具名[角色](APPENDIX_beginner_glossary.md#g084)／[累计声明写集](APPENDIX_beginner_glossary.md#g105)／整片[工作区](APPENDIX_beginner_glossary.md#g082)／终图的范围，终图一致不补全中间观测。
13. 时域先读 [B0](L3_b0_input.md)，再读 [B70→复制→显示](L3_b70_history_output.md#b70-history-output)。
14. 【推测】、[UNKNOWN](APPENDIX_beginner_glossary.md#g104)、NOT_RUN 和[拒绝守卫](APPENDIX_beginner_glossary.md#g101)都属于正文合同。
15. 页末列出已写主题、共用步骤及仍缺的独立算术叶；页面齐全不等于证据闭合。

以下按默认158-launch路线导航；层级L0/L1与调用编号launch L0–L157分开。

横切导读：[153条权重组织](L2_weights_layout.md) · [跨GPU／CPU后端比较](L4_cross_arch.md) · [公开v2复现指南](REPRODUCE.md)。

先读[L0a 对象与方法](L0a_object_method.md)，确认固定对象与字节复现判据；再从 [L0 一帧](L0_frame.md) 进入：当前颜色、[运动矢量](APPENDIX_beginner_glossary.md#g023)、上一帧历史和控制量，经[编码](APPENDIX_beginner_glossary.md#g009)、[全局瓶颈](APPENDIX_beginner_glossary.md#g010)、解码，分成历史状态 id9→id6 与显示输出 id2 两条出口。[L0b 确定性与可复现性](L0b_determinism.md)另列驱动、设备、填充、重复及未测边界。

下表 TIN 的 1h/2h/4h/8h 分别表示 1/2/4/8 个注意力头，每头 32 通道；这里的 h 是头数，与图像高度 H 不同。

| L1 切片 | launch 区间 | B 编号 | 阶段交接 |
|---|---|---|---|
| [01 图外前置](L1_01_prepare.md) | L0–L1 | — | id1→id10；初始化工作区控制区 |
| [02 输入端 B0](L1_02_input_b0.md) | L2 | B0 | 16 通道→32 通道 [full](APPENDIX_beginner_glossary.md#g018) / pool |
| [03 TIN 编码](L1_03_tin_encoder.md) | L3–L24 | B1–B22 | 1h→2h→4h→8h；留下四档 skip |
| [04 split16 编码](L1_04_split16_encoder.md) | L25–L57 | B23–B30 | 512 通道[窗口](APPENDIX_beginner_glossary.md#g015)块→1024 通道瓶颈入口 |
| [05 ViT 瓶颈](L1_05_vit.md) | L58–L99 | B31–B38 | [repack](APPENDIX_beginner_glossary.md#g019)→8×五核→repack |
| [06 解码桥](L1_06_decoder_bridge.md) | L100 | B39 | 瓶颈主路与 B30 skip→512 通道 |
| [07 split16 解码](L1_07_split16_decoder.md) | L101–L132 | B40–B47 | 八个窗口块→[outview](APPENDIX_beginner_glossary.md#g022) |
| [08 TIN 解码](L1_08_tin_decoder.md) | L133–L154 | B48–B69 | 四级[上采样](APPENDIX_beginner_glossary.md#g021)与四条编码 skip 合并 |
| [09 B70](L1_09_b70.md) | L155 | B70 | 解码特征、B0 skip、颜色和时域输入→id9 |
| [10 输出](L1_10_output.md) | L156–L157 | — | id9→id6；后处理(id9,id10)→id2 |

## 形状与工作区记号

参数字段统一写CB+0xNN ([f32](APPENDIX_beginner_glossary.md#g057)/u32/u64)，0xNN是十六进制字节偏移；64位字下标只作括注。脚本/源码中的真实字段名保留实现拼写。

图像宽高为 $W,H$；内部画布为 $W_n,H_n$，从已准入 params 读取。以宽×高写空间尺寸，$X_r(C)$ 表示 $H_r\times W_r\times C$ 个元素，默认省略 [batch=1](APPENDIX_beginner_glossary.md#g086)。[E4](APPENDIX_beginner_glossary.md#g055) 表示 E4M3 的一字节编码，[F16](APPENDIX_beginner_glossary.md#g054)/[F32](APPENDIX_beginner_glossary.md#g056)表示binary16/binary32，binary64为双精度；[Inf](APPENDIX_beginner_glossary.md#g069)/NaN为无穷/非数，[satfinite](APPENDIX_beginner_glossary.md#g062)为有限饱和；逻辑形状不表示物理内存连续的通道顺序。

| 其他记号 / 角色名 | 本目录含义 |
|---|---|
| 1/256定点小数格 / [Q32](APPENDIX_beginner_glossary.md#g065) | 采样坐标使用1/256定点小数格，四角使用联合8位分数权重；Q32是本串sm_120 E4的一步K32，接收/发布F16 [seed](APPENDIX_beginner_glossary.md#g042) |
| [RSQ](APPENDIX_beginner_glossary.md#g072) / RCP / EX2 / LG2 | 倒数平方根 / 倒数 / 二次幂 / 二进对数的[认证函数映射](APPENDIX_beginner_glossary.md#g074)，域与位型按L4 |
| [Q8](APPENDIX_beginner_glossary.md#g061)(x) / D8(x) | F16→E4的[RN-even](APPENDIX_beginner_glossary.md#g059)/satfinite量化 / E4→F16精确解码；E只表示[指数](APPENDIX_beginner_glossary.md#g058) |
| [H+](APPENDIX_beginner_glossary.md#g063) / H× / HF | half加、乘、融合乘加；每次保留本来的发布点 |
| F32+ / F32× / F32/ / F32_FMA | F32加、乘、除、融合乘加，按站点保留舍入/[FTZ](APPENDIX_beginner_glossary.md#g068)/拒绝 |
| [Den](APPENDIX_beginner_glossary.md#g048) / [CumWrites](APPENDIX_beginner_glossary.md#g093)(L) / [Partials](APPENDIX_beginner_glossary.md#g050) | [attention](APPENDIX_beginner_glossary.md#g039)分母 / 累计声明写集 / L100的F16部分和数组 |
| RN16/RN32/RN64、bits16、[Sat01](APPENDIX_beginner_glossary.md#g049) | 最近偶数到指定格式、half原始编码、夹到[0,1]；函数表域另列 |
| [CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED / CONTROLLED / INFERRED | 读源 / 具名测量 / 对照 / 推断，均保留对象与范围 |
| launch / B | launch 是一次 kernel 调用；B 是逻辑块，两套编号分开 |
| [token](APPENDIX_beginner_glossary.md#g041) / [tile](APPENDIX_beginner_glossary.md#g087) | token 是一个特征位置；tile 是执行时分块，具体形状按该片说明 |
| $r,C$ | r 为形状档位，C 为通道数；执行索引的轴不能自动当作 C |
| $T,P$ | T 为逻辑有效 token 数；P 为 T 向上补齐到 32 倍数后的物理行数 |
| Wn/Hn、x/y、frame | 内部画布宽/高、未[镜像](APPENDIX_beginner_glossary.md#g030)坐标、原生帧计数；不是视频绝对帧号 |
| $N_{\rm out}$ / N_out | 本实例输出角色长度之和；用于尚未独立确认逻辑通道拆分的物理字节序列 |
| full / pool / pooled | 本档完整出口 / 池化出口 / 池化后的角色；不直接规定池化算术 |
| skip / [residual](APPENDIX_beginner_glossary.md#g017) / seed | 旁路 / 残差输入 / 某次累加的起始值；每片指定实际来源 |
| inpview / outview / chained | 输入视图块 / 输出视图 / 同档连续块；核名不替代布局或同步合同 |
| [ffwd](APPENDIX_beginner_glossary.md#g037) / ffwd_proj / [proj](APPENDIX_beginner_glossary.md#g038) | 前馈前段 / 前馈后段 / 注意力后投影；数据驱动片的语义另标推断 |
| RGB / MV / Q/K/V、FFN | 红绿蓝 / 运动矢量 / [查询](APPENDIX_beginner_glossary.md#g040)/键/值、前馈网络；不凭命名假定标准库算子可替代 |
| K16 / K32 / RN-even / [RZ](APPENDIX_beginner_glossary.md#g060) | 一步16 / 32项乘积、最近偶数舍入、向零舍入 |
| h_fma / FTZ / [MUFU](APPENDIX_beginner_glossary.md#g073) | half 融合乘加辅助函数 / 次正规冲零合同 / 已采的特殊数学函数 |
| [TIN](APPENDIX_beginner_glossary.md#g011) / [split16](APPENDIX_beginner_glossary.md#g013) / [ViT](APPENDIX_beginner_glossary.md#g014) | 本串窗口块家族 / 16头512通道窗口块 / 32头1024通道全局瓶颈 |
| post_block / [mapexec](APPENDIX_beginner_glossary.md#g089) | 神经网络末块 / 按绑定算术图与来源索引执行的CPU实现 |
| [alpha](APPENDIX_beginner_glossary.md#g026) / intensity / WS | 图像第四通道 / 显示混合强度 / 共享工作区 |
| params / role / release / pitch | 调用参数块 / 命名内存角色 / 完成标记 / 每行实际字节跨度 |

令 $(W_0,H_0)=(W_n,H_n)$，两轴逐级取 $n_{r+1}=4\lceil n_r/8\rceil$，即先减半、再补齐到 4 的倍数；$T=W_6H_6$，$P=32\lceil T/32\rceil$。这条 extent 链是已捕获语料的归纳，根画布依赖[宿主](APPENDIX_beginner_glossary.md#g096)合同，**不是任意 $W,H$ 的闭式公式**。

| 尺寸量（宽×高） | 1080p | 1440p | 4K |
|---|---|---|---|
| 图像 $W\times H$ | 1920×1080 | 2560×1440 | 3840×2160 |
| $X_0$ 内部画布 | 1920×1152 | 2560×1472 | 3840×2176 |
| $X_1$ / TIN 1h | 960×576 | 1280×736 | 1920×1088 |
| $X_2$ / TIN 2h | 480×288 | 640×368 | 960×544 |
| $X_3$ / TIN 4h | 240×144 | 320×184 | 480×272 |
| $X_4$ / TIN 8h | 120×72 | 160×92 | 240×136 |
| $X_5$ / split16 物理 extent | 60×36 | 80×48 | 120×68 |
| $X_6$ / ViT 二维逻辑格 | 32×20 | 40×24 | 60×36 |
| $T$ / $P$ | 640 / 640 | 960 / 960 | 2160 / 2176 |
| 整片工作区 / B | 212,519,936 | 340,722,688 | 763,062,272 |

1440 的 $X_5$ 有效高为 46、物理高为 48；4K 的 ViT 有 16 个额外 padding token。有效范围、分配范围和实际写集须分别看，不能把补齐区一概当作未用空间。CENSUS / INFERRED：[ARCH 0.7 §8.1–§8.5](../../../ARCHITECTURE_V3_ZH.md#8-几何与分辨率)。

各切片用 $Span(A)$ 表示[张量](APPENDIX_beginner_glossary.md#g076)角色 A 在工作区的区间：$[p_A-b,\ p_A-b+N_A)$，$b$ 为本次工作区基址，$p_A$ 取该 launch 的 params，$N_A$ 是物理角色字节数。E4 的 $X_r(C)$ 为 $W_rH_rC$ B，F16 再乘 2；padding 和同步写另计，不套用一个跨几何固定偏移。[纹理](APPENDIX_beginner_glossary.md#g027)按 id、格式、尺寸、pitch 与时点绑定；[RGBA16F](APPENDIX_beginner_glossary.md#g028) 有效行长 $8W$ B，MV 为 RG16F、有效行长 $4W$ B。

## 证据路径图例

下列链接在当前工作站可打开；只拿本串[镜像](APPENDIX_beginner_glossary.md#g099)时，外部源码和私有记录不一定随包附带。路径不是对象身份，具体版本仍看绑定SHA。

| 路径族 | 内容角色 | 独立读者能否打开 |
|---|---|---|
| GlassBox-NR（GitHub，固定提交 [e4a9b42](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec)） | 发布v2的独立C++重建与runtime源码；正文源码链接都指向这一提交 | 能直接在 GitHub 打开；本地运行示例仍需相邻的源码checkout |
| experiments/… | 私有项目的捕获、诊断、验收及冻结身份记录 | 需原项目证据目录；单独镜像通常不可开 |
| [mapform-split16-qkv-r01-20261027-codex](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md) | split16 qkv八字段地址闭式及留出地图验证；[公式说明](../../../experiments/mapform-split16-qkv-r01-20261027-codex/FORMULAS_ZH.md)、[冻结源码](../../../experiments/mapform-split16-qkv-r01-20261027-codex/formula_qkv.py) | 需原项目研究目录；地址等价，不是数值DAG、全链或动态血缘证明 |
| [mapform-split16-rest-r02-20261027-codex](../../../experiments/mapform-split16-rest-r02-20261027-codex/RESULT_ZH.md) | F16/F17/F19–F23逐字段闭式、留出结果和保留失败 | 需原项目研究目录；r04补充4K地址表，空数组仍非地址证据 |
| [mapform-split16-r04-20261027-codex](../../../experiments/mapform-split16-r04-20261027-codex/RESULT_ZH.md) | 绑定候选、4K地图对照及历史变体分类；[结构化回执](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json) | 需原项目研究目录；中文报告已由r04 `repair_reports.py` 从JSON重建，损坏原件保留为 `*.garbled-ascii` |
| [mapform-tin-r03-20261027-codex](../../../experiments/mapform-tin-r03-20261027-codex/RESULT_ZH.md) | TIN新地址表缺失的NOT_RUN清点 | 需原项目研究目录；源码转写不等于新留出验证 |
| F:/dlssnr-work/…、E:/dlssnr-work-e/… | 本地工作线的来源地图、wiring及参数资产 | 需相同资产副本及SHA绑定；不是公开源码目录 |
| mlxdlss/ | 早期Python CPU参考与认证函数资产接口 | 需完整项目checkout；不是当前C++发布代码本身 |
| E:/b1-relocated-10600t/… | 从10600T迁回的历史地图/配置证据副本 | 当前工作站有副本；镜像不附带，迁移路径不等于发布资产身份 |

<a id="项目与验证术语"></a>
证据表的构建代号与验证用语见[附录词表](APPENDIX_evidence_history.md#project-terms)。

## 计算口径

设计动机统一在此说明：训练目标、拆核成因及硬件资源瓶颈未由输出比较唯一确定。下文先给可读的计算/发布关系，具体系统关系只陈述可核对的输入输出；【推测】只用于训练意图。

**C++ 优化过，但不改变算术。** 浮点累加分组与顺序、显式融合边界及舍入点保留；只有精确整数和允许重排。循环组织、分块与融合实现方式不作为网络结构。行为解释以 [发布源码 cpp/](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp) 为主；Python 参考用于交叉核对 1080 f0，不代替多帧及其他几何。

**数据驱动的搬运与算术分别看。** mapexec、scalar_map 及地址映射表的索引决定从哪里取、向哪里写；算术核心决定这些值怎样相乘、相加和舍入。索引表能复现输出，不单独证明“这是某种卷积或注意力”的语义；训练意图另标【推测】，未确认的索引/算子语义直接列UNKNOWN及闭合条件。

各阶段复用的数值接口：E4 发布采用 satfinite / RN-even；sm_120 QMMA 每个 K32 按冻结规则求和并发布 F16，跨 K32 携带该 F16 [累加器](APPENDIX_beginner_glossary.md#g064)；普通 half 运算保留各自舍入，h_fma 软件参考为 binary64 融合结果 RN-even 后再 half RN-even。两次软件舍入不等于已证明 GPU 所有 half 行为；±0、次正规、Inf、FTZ 与异常按具体原语合同区分。B70 和 L157 的最终 RGB 转 half 为 RZ（向零），不能套用普通 half RN-even。INFERRED / MEASURED（限所列原语）：[ARCH 0.7 §7](../../../ARCHITECTURE_V3_ZH.md#7-算术层)。

<a id="已测实例的边界"></a>
具名构建、输入与比较范围见[附录边界](APPENDIX_evidence_history.md#index-measured-scope)。

## 往下追

L2 共 46 个覆盖/步骤入口：41 个覆盖家族/单例，加 B0 的五个核内步骤；重复正文现按共享流程与变体表组织，入口与覆盖归属不变。41 个覆盖片合并 44 个原生函数名，覆盖默认 L0–L157；重排的正/逆向、ViT 首/中段扩张及末端投影变体在对应家族内列明。跨阶段的共享片只定义一次，下表的复用导航不重复计覆盖。

| L1 → L2 | 本文件内切片数 | 跨阶段复用 |
|---|---:|---|
| [01 图外前置](L1_01_prepare.md) → [L2.01](L2_01_prepare.md) | 2 | copy 同时覆盖 L0 与 L156 |
| [02 B0](L1_02_input_b0.md) → [L2.02](L2_02_b0.md) | 6 | 一个 launch 单例与其五个核内步骤 |
| [03 TIN 编码](L1_03_tin_encoder.md) → [L2.03](L2_03_tin_encoder.md) | 12 | 四档 chained 同时列出编码、解码调用 |
| [04 split16 编码](L1_04_split16_encoder.md) → [L2.04](L2_04_split16_encoder.md) | 8 | 四个 chained 家族同时列出编码、解码调用 |
| [05 ViT](L1_05_vit.md) → [L2.05](L2_05_vit.md) | 6 | 五个算术位置各复用八次，另有双向 repack |
| [06 解码桥](L1_06_decoder_bridge.md) → [L2.06](L2_06_decoder_bridge.md) | 1 | L100 单例 |
| [07 split16 解码](L1_07_split16_decoder.md) → [L2.07](L2_07_split16_decoder.md) | 1 | 另链接 L2.04 的四家族；本地为 L132 |
| [08 TIN 解码](L1_08_tin_decoder.md) → [L2.08](L2_08_tin_decoder.md) | 8 | 另链接 L2.03 的四档 chained |
| [09 B70](L1_09_b70.md) → [L2.09](L2_09_b70.md) | 1 | L155 单例 |
| [10 输出](L1_10_output.md) → [L2.10](L2_10_output.md) | 1 | L156 链到共享 copy，本地为 L157 |

L157 的命名冲突已按当前发布版受守卫分支裁为 [HSL 型分解与重组](L3_b70_history_output.md#postprocess)；三个宿主标量的数值作用已列式，其 API 名称仍未知，局部变量名不升级为已测宿主语义。B69 的原生独立布局未知边界保留在 [1h outview 片](L2_08_tin_decoder.md#out-32)。

~~~text
L0 一帧  L0_frame.md
├─ L1.01 图外前置    → L2.01 copy / clear
├─ L1.02 B0          → L2.02 单例 → 噪声 / 重投影 / 16通道 / 适配窗口块 / 双出口
├─ L1.03 TIN 编码    → L2.03 四档 inpview / chained / ds_wait
├─ L1.04 split16 编码→ L2.04 八家族
├─ L1.05 ViT         → L2.05 repack / expand / contract / qkv / attention / projection
├─ L1.06 解码桥      → L2.06 L100
├─ L1.07 split16 解码→ L2.07 L132 + 复用 L2.04 四家族
├─ L1.08 TIN 解码    → L2.08 四档 upsample / outview + 复用 L2.03 chained
├─ L1.09 B70         → L2.09 L155
└─ L1.10 输出        → L2.10 L157 + 复用 L2.01 copy 的 L156
~~~

## 下层主题入口（全部直达正文；共用页按步骤锚点区分）

| 名称 | 将从本层继续追的对象 |
|---|---|
| <a id="l3-qmma-e4m3"></a>[L3.qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3) | 有序 K32 [矩阵](APPENDIX_beginner_glossary.md#g051)链、源码行号与当前适用边界；候选裁决移至证据附录 |
| <a id="l3-b0-noise-reprojection"></a>[L3.b0-noise-reprojection](L3_b0_input.md#b0-noise-reprojection) | B0 五步：噪声、16 通道、[五 tap](APPENDIX_beginner_glossary.md#g029)、适配窗口块与 full / pool |
| <a id="l3-input-adapter"></a>[L3.input-adapter](L3_b0_input.md#adapter) | B0 的 16 通道与 half 适配矩阵 |
| <a id="l3-ffn"></a>[L3.ffn](L3_ffn.md#ffn) | 精确单输入G、跨家族矩阵/通道账、残差seed与真实C++实算 |
| <a id="l3-tin-window"></a>[L3.tin-window](L3_tin_window.md#tin-window) | 44次完整TIN块：分窗原点、FFN先行、残差seed及四档编解码外围 |
| <a id="l3-window-attention"></a>[L3.window-attention](L3_split16_window.md#window-attention) | split16四核完整块、16头分窗、1080逻辑角色与物理字节合同、编解码末端变体 |
| <a id="l3-attention-softmax"></a>[L3.attention-softmax](L3_attention_softmax.md#attention-softmax) | 全局/窗口分数变换、half 分母、RCP、值汇合与 L62 零覆盖 |
| <a id="l3-tin-norm"></a><a id="l3-norm-nonfinite"></a>[L3.norm-nonfinite](L3_norm_nonfinite.md#norm-nonfinite) | 头内平方和、RSQ、[尺度](APPENDIX_beginner_glossary.md#g031)与 [A1](APPENDIX_beginner_glossary.md#g107) 非有限边界 |
| <a id="l3-noise"></a>[L3.noise](L3_b0_input.md#noise) | [整数散列](APPENDIX_beginner_glossary.md#g075)、三路噪声；存储编码另见 CPU 附录 |
| <a id="l3-temporal-sampling"></a>L3.temporal-sampling | 分别进入 [B0 特征重投影](L3_b0_input.md#coordinates)与 [B70 原始历史采样](L3_b70_history_output.md#b70-temporal) |
| <a id="l3-repack"></a>[L3.repack](L3_workspace_map.md#repack) | 双向闭式、接受域、逻辑 / 物理行与额外零写 |
| <a id="l3-workspace-map"></a>[L3.workspace-map](L3_workspace_map.md#workspace-map) | 角色布局、CumWrites(L)、填充、L62 零覆盖、数据驱动地址表及 WR A/B |
| <a id="l3-b70-history-output"></a>[L3.b70-history-output](L3_b70_history_output.md#b70-history-output) | B70、L156、L157、carry / [reset](APPENDIX_beginner_glossary.md#g032) 及具名多帧门 |
| <a id="l3-output-temporal"></a>[L3.output-temporal](L3_b70_history_output.md#b70-mix) | B70 预测、置信权重与历史混合 |
| <a id="l3-postprocess"></a>[L3.postprocess](L3_b70_history_output.md#postprocess) | [HSL](APPENDIX_beginner_glossary.md#g033) 型颜色链、宿主标量作用与显示合成 |
| <a id="l4-half-fma"></a><a id="l4-half-arith"></a>[L4.half-arith](L4_half_arith.md#half-arith) | F16 位格式、两阶段 FMA、整数等价证明、有序累加与 F32 转换边界 |
| <a id="l4-mufu"></a>[L4.mufu](L4_mufu.md#mufu) | 七族用途、接受域与边缘语义；测量和编码另见附录 |
| <a id="l4-fp32-ftz"></a>[L4.fp32-ftz](L4_fp32_ftz.md#fp32-ftz) | 全链F32起止、RN/RZ/satfinite、按路径FTZ与守卫、严格编译及真实C++转换例 |
| <a id="l4-e4m3"></a><a id="l4-e4m3-format"></a>[L4.e4m3-format](L4_e4m3_and_k32.md#e4m3-format) | 字节格式、次正规、特殊值与[激活](APPENDIX_beginner_glossary.md#g045)饱和量化 |
| <a id="l4-qmma-k32-accumulation"></a>[L4.qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation) | [field F25](APPENDIX_beginner_glossary.md#g066)、整 K32、65520 守卫与可执行合成例 |
| <a id="l4-hmma"></a>[L4.hmma](L4_hmma.md#hmma) | F16操作数、K16公共格、seed与逐步发布；跨架构和负零反例分列 |
| <a id="l4-tex-filter"></a>[L4.tex-filter](L4_tex_filter.md#tex-filter) | 1/256定点小数格、联合8位分数权重、共指数截断与纹理half中点 |
| <a id="l4-cross-arch"></a>[L4.cross-arch](L4_cross_arch.md#comparison) | sm_120与较早GPU的原语差异、CPU后端方案及实际字节门边界 |

## 主题清单与算术下钻边界

原计划页面均已有正文；这只表示计划页面已写，不表示每个原语都有独立算术叶。纹理过滤已补独立L4；仍缺整数坐标散列/位混合的独立L4（当前在L3 B0）、跨位置交换/来源映射的完整独立语义证明（当前在L3 workspace；它也不只是一个算术问题）。这些缺口不由页面数量关闭。

[页面与同页步骤的完整对应表](APPENDIX_evidence_history.md#topic-inventory)移到维护附录；算术导航仍在上表。

正文补齐不改变证据强度：一般maps、任意输入/几何、同步/[别名](APPENDIX_beginner_glossary.md#g092)/生命周期、内部值唯一与未测包装仍按各页保留。参数变化的156路线、p5 reset/时域已在下列独立子候选取得具名结果；M/M2不扩域，312 B post_block仍REFUSED/NOT_RUN。

<a id="param-change-r04h"></a>
## 参数分支

p5改变条件通道并在有效历史时读取上一帧状态；156路线省去基底备份与独立显示后处理，S157按精确控制元组执行同一颜色链，[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。

[证据历史与身份账](APPENDIX_evidence_history.md)保存候选裁决、证明计数、长 SHA 与回执；[CPU 存储](APPENDIX_cpu_storage.md)保存无损编码、资产布局与加载细节。算术舍入、拒绝条件和未知仍在各主题正文。
