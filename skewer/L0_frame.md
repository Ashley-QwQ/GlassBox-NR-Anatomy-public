### L0 一帧（launch L0–L157 / B0–B70）

<!-- beginner-r04m:start frame -->
<a id="beginner-frame"></a>
## 先画作用，再读精确接线

【入门简化，证据沿用下方正文】当前图、移动的两个数、可用旧图和控制数进来，显示仍与输入同尺寸。移动数的通用方向和单位未定。图中数字卡片统一只写“每位置几项”；RGB是可见颜色三项，内部32/[512](APPENDIX_beginner_glossary.md#g007)/1024项没有逐通道的已知画面含义。[编码](APPENDIX_beginner_glossary.md#g009)逐步变稀，解码逐步变密；它们是计算阶段，不是文件压缩的正逆过程。

~~~mermaid
flowchart TD
    I["当前图：宽×高；每像素RGB"] --> P["准备：保留本帧原图备份、设置管理标记"]
    M["移动信息：每位置两个数；方向/单位？"] --> IN["输入处理：凑16项条件 → 每位置32项"]
    H["可使用的旧图"] --> IN
    C["控制数"] --> IN
    P --> IN
    IN --> E1["编码第一档：每位置32项"] --> E2["编码第二档：每位置64项"] --> E3["编码第三档：每位置128项"] --> E4["编码第四档：每位置256项"]
    E4 --> S["八个窗口块：每位置512项"] --> SHR["换到更稀网格？空间配对未定；每位置1024项"]
    SHR --> G["八个全位置块：每位置1024项"] --> BR["接回旁路、恢复较密网格？完整空间算子未定；每位置512项"]
    BR --> SD["八个窗口块：每位置512项"] --> D4["变密第一档：每位置256项"] --> D3["变密第二档：每位置128项"] --> D2["变密第三档：每位置64项"] --> D1["变密第四档：每位置32项；宽高仍各为内部画布一半"]
    D1 --> T["末端：接回入口数字，预测颜色修正；按条件另取旧颜色混合"]
    IN -->|"①入口完整密度数字，32项"| T
    E1 -->|"②同档数字，32项"| D1
    E2 -->|"③同档数字，64项"| D2
    E3 -->|"④同档数字，128项"| D3
    E4 -->|"⑤同档数字，256项"| D4
    S -->|"⑥瓶颈前数字，512项"| BR
    I --> T
    M --> T
    H --> T
    C --> T
    T --> N["本帧新颜色状态"] --> SAVE["保存为下帧旧图"]
    N --> SHOW["显示颜色调整，再与本帧备份按强度混合"] --> O["显示图：仍为输入的宽×高"]
    P -->|"原图备份：另一路，不计六条内部旁路"| SHOW
    C --> SHOW
    SAVE -. "下一帧" .-> H
~~~

六条内部[旁路](APPENDIX_beginner_glossary.md#g016)按①入口→末端、②至⑤四档编码→对应变密档、⑥[瓶颈](APPENDIX_beginner_glossary.md#g010)前→桥接来记；原图备份单算第七条保存连接。内部变稀/[补齐](APPENDIX_beginner_glossary.md#g085)不改变最终显示宽高。先把每个位置的数字卡片记住，再展开[一个小块的两条局部残差](L1_00_one_block_primer.md#two-residuals)；局部[残差](APPENDIX_beginner_glossary.md#g017)与这里的跨阶段旁路是两种尺度的接线。

桥接可先画两层：**已知**四组通道的[部分和](APPENDIX_beginner_glossary.md#g050)按固定次序相加、再接旁路；**未定？**完整空间恢复关系，不能画成已证明的[最近邻](APPENDIX_beginner_glossary.md#g021)[插值](APPENDIX_beginner_glossary.md#g020)或四点[均值](APPENDIX_beginner_glossary.md#g044)。[精确桥图](L2_06_decoder_bridge.md#wiring)

阅读深度：[L0](APPENDIX_beginner_glossary.md#g081)（整帧）。<br>执行编号：默认[launch](APPENDIX_beginner_glossary.md#g080) L0–L157。<br>[逻辑块](APPENDIX_beginner_glossary.md#g036)编号：B0–B70。下面保留原有精确图、数值域、参数与比较范围；已有基础后再读“教科书差异”框。[历史](APPENDIX_beginner_glossary.md#g024)的三帧时间线另见[入门页](L1_00_history_primer.md#timeline)，[工作区](APPENDIX_beginner_glossary.md#g082)最小必需记忆范围仍[未定](L1_00_history_primer.md#workspace-memory)。
<!-- beginner-r04m:end frame -->

[对象与方法](L0a_object_method.md) · [确定性与可复现性](L0b_determinism.md) · [整串目录](INDEX.md)

[权重组织与阶段字节账](L2_weights_layout.md) · [跨架构比较](L4_cross_arch.md) · [公开v2复现](REPRODUCE.md)

> **它不是什么／与教科书模型的差异（当前重建与已见接线）**
>
> - 同尺寸W×H输出；已测三档只补内部画布高度，1080→1152后[镜像](APPENDIX_beginner_glossary.md#g030)取颜色。[边界取样](L3_b0_input.md#channels)
> - 含[attention](APPENDIX_beginner_glossary.md#g039)的主干块先[FFN](APPENDIX_beginner_glossary.md#g037)、后attention。[各家族前馈接线](L3_ffn.md#channels)
> - 没有块入口LayerNorm；只对[投影](APPENDIX_beginner_glossary.md#g038)后Q/K逐头做无均值平方和与[RSQ](APPENDIX_beginner_glossary.md#g072)，V不做。[Q/K归一化](L3_norm_nonfinite.md#norm32)
> - G是单输入裁剪分段多项式，不按[GELU](APPENDIX_beginner_glossary.md#g046)/SiLU或双分支门替换。[门函数](L3_ffn.md#gate)
> - attention不求[exp](APPENDIX_beginner_glossary.md#g047)或行最大值；[ViT](APPENDIX_beginner_glossary.md#g014)先[Q8](APPENDIX_beginner_glossary.md#g061)(w)汇合V、再乘倒数。[分数与发布](L3_attention_softmax.md#attention-softmax)
> - 残差保留[矩阵](APPENDIX_beginner_glossary.md#g051)[seed](APPENDIX_beginner_glossary.md#g042)／首分片及有序[half](APPENDIX_beginner_glossary.md#g054)合并的真实接口，不统一挪成点积后实数加法。[残差舍入](L3_ffn.md#residual)

当前颜色 id1、[运动矢量](APPENDIX_beginner_glossary.md#g023) MV id3、有效历史 id6 和控制量，经编码→瓶颈→解码生成[状态](APPENDIX_beginner_glossary.md#g002) id9；L156 将其保存成下帧历史，L157 按 [intensity](APPENDIX_beginner_glossary.md#g004) 与[颜色基底](APPENDIX_beginner_glossary.md#g003) id10 合成同尺寸显示 id2。总体视觉目的仍未知，见 [入口的对象与项目术语](INDEX.md)。

【验证记录／展示边界】具名控制会改变输出，但这里尚无[绑定](APPENDIX_beginner_glossary.md#g103)当前对象身份、同一输入/历史状态及两个控制变化的完整图像/差分组；不能从零散PNG推定视觉目的。已知数值作用见[B0控制通道](L3_b0_input.md#channels)及[显示混合](L3_b70_history_output.md#postprocess)，图像展示所缺的身份与对照条件见[证据附录](APPENDIX_evidence_history.md#r04f-review-resolution)。

图中空间轴统一为 **宽×高×通道**，[batch=1](APPENDIX_beginner_glossary.md#g086)；[E4](APPENDIX_beginner_glossary.md#g055)/F16 是 E4M3/binary16。尺寸直接取 [INDEX extent 表](INDEX.md#形状与工作区记号) 的 1080 实例；只表示阶段边界的逻辑形状，内部隐藏轴及物理排列不从图推导。

~~~mermaid
flowchart TD
    Input["输入：id1 1920×1080×4 F16；id3 1920×1080×2 F16；有效 id6 1920×1080×4 F16；controls 各 params 标量，无空间轴"]
    Prepare["图外前置 L0–L1：id10 1920×1080×4 F16；控制区 uint32，逻辑张量轴不适用"]
    B0["L2 / B0：1920×1152×16 F16 条件→full 1920×1152×32 E4；pool 960×576×32 E4"]
    C1["TIN 1h L3–L6：full 960×576×32 E4；pool 480×288×64 E4"]
    C2["TIN 2h L7–L10：full 480×288×64 E4；pool 240×144×128 E4"]
    C3["TIN 4h L11–L16：full 240×144×128 E4；pool 120×72×256 E4"]
    C4["TIN 8h L17–L24：full 120×72×256 E4；pool 60×36×512 E4"]
    SplitEnc["split16 编码 L25–L57：B30.full 60×36×512 E4；pooled 32×20×512 E4；L57 32×20×1024 E4；核内隐藏轴未独立确认"]
    ViT["ViT L58–L99：32×20×1024 E4→640 token×1024 E4→32×20×1024 E4；T=P=640"]
    Bridge["桥 L100 / B39：60×36×512 E4"]
    SplitDec["split16 解码 L101–L132：60×36×512 E4 outview；核内隐藏轴未独立确认"]
    H4["TIN L133–L140：120×72×256 E4 outview"]
    H3["TIN L141–L146：240×144×128 E4 outview"]
    H2["TIN L147–L150：480×288×64 E4 outview"]
    H1["TIN L151–L154：960×576×32 E4 outview"]
    B70["B70 L155：main 按 floor(x/2),floor(y/2) 复用，与 B0.full 合并；id9 1920×1080×4 F16"]
    History["L156：id9→id6 1920×1080×4 F16"]
    Display["L157：处理 id9，再按 intensity 与 id10 混合→id2 1920×1080×4 F16"]
    Input --> Prepare --> B0 --> C1 --> C2 --> C3 --> C4 --> SplitEnc --> ViT --> Bridge --> SplitDec --> H4 --> H3 --> H2 --> H1 --> B70
    Input --> B0
    Input --> B70
    SplitEnc -- "B30.full 60×36×512 E4 skip" --> Bridge
    C4 -- "B22.full 120×72×256 E4 skip" --> H4
    C3 -- "B14.full 240×144×128 E4 skip" --> H3
    C2 -- "B8.full 480×288×64 E4 skip" --> H2
    C1 -- "B4.full 960×576×32 E4 skip" --> H1
    B0 -- "B0.full 1920×1152×32 E4 skip" --> B70
    B70 --> History
    B70 --> Display
    Prepare -- "id10 1920×1080×4 F16" --> Display
    History -. "下一帧历史" .-> Input
~~~

1080→1152是本次[params](APPENDIX_beginner_glossary.md#g083)给定的内部画布高度，多出的72行用于内部计算；输出仍裁到1920×1080。不是把画面按比例拉伸，也不能由一个ceil(H/8)公式推出根画布高度。B0按ty=y<H?y:2H−2−y反射颜色/MV：y=1080读1078行，y=1151读1007行；噪声仍用未镜像的内部坐标。[B0镜像合同](L3_b0_input.md#channels)规定该有限范围，后续各档补齐另按[窗口](APPENDIX_beginner_glossary.md#g015)[合同](APPENDIX_beginner_glossary.md#g101)。

B70 的半分辨率主路按坐标复用，并非因字节数相等就 reshape 为全分辨率；内部画布到图像有效区的裁取见 [B70](L3_b70_history_output.md#b70-network)。图外工作区还含 F16/[F32](APPENDIX_beginner_glossary.md#g056) 暂存及控制字，不将它们画成虚构的通道。旧单样本直接 skip 对照只覆盖四条 [TIN](APPENDIX_beginner_glossary.md#g011) 编解码连接；B0→B70 另按当前源码接线。

## 像素数值域与表示变换

| 位置 | 表示与数值域 | 变换 |
|---|---|---|
| id1 / id10 | F16颜色；本例按[0,1]理解，入口没有据此统一[夹取](APPENDIX_beginner_glossary.md#g049) | 当前色与基底按位读取；[alpha](APPENDIX_beginner_glossary.md#g026)不参与网络颜色输入 |
| B0条件 | F16；噪声、颜色、固定常量及控制分量[分别定义](L3_b0_input.md#channels) | 当前颜色先减0.5、再乘gain，两步各half[发布](APPENDIX_beginner_glossary.md#g091)。仅忽略舍入时，color∈[0,1]且gain≥0给出±gain/2的理想界；实际F16结果须按两次舍入计算 |
| 主干/skip | E4M3有限码在[−448,448]，[非有限](APPENDIX_beginner_glossary.md#g069)路径另有守卫 | 每[K32](APPENDIX_beginner_glossary.md#g065)先发布F16，出口Q8；这不是说所有中间half也在该区间 |
| B70当前色 | F32 encoded∈[0,1] | 实数理想形式color+8×scale×dh，实际按三次[FMA](APPENDIX_beginner_glossary.md#g063)及夹取 |
| B70历史与id9 | F32融合→[RZ16](APPENDIX_beginner_glossary.md#g060)；factor∈[0,1] | [五tap](APPENDIX_beginner_glossary.md#g029)可有负侧瓣；融合后未统一夹[0,1]，不能给id9虚构固定颜色范围 |
| L157→id2 | F32颜色链与基底合成→夹[0,1]→RZ16，alpha=1 | 增益/曲线、两轮[HSL](APPENDIX_beginner_glossary.md#g033)与intensity各保留原运算边界 |

具体数值见[B70代入](L3_b70_history_output.md#b70-mix)，格式边界见[F32叶](L4_fp32_ftz.md#sites)。

<a id="textures"></a>
## 六个纹理与控制速查

【原生行为／CPU重建接线】默认路线记录六个[纹理](APPENDIX_beginner_glossary.md#g027)槽位，编号不连续；其余编号未在这条路线作为已登记纹理绑定，不能据空号猜成遮罩。[六POST](APPENDIX_beginner_glossary.md#g105)指下列六纹理在指定调用后的有效区；不是六张不同图像任务。

| ID | [角色](APPENDIX_beginner_glossary.md#g084) | 格式 / 尺寸 | 写入 | 读取 |
|---|---|---|---|---|
| id1 | 当前颜色 | [RGBA16F](APPENDIX_beginner_glossary.md#g028) / W×H | [caller](APPENDIX_beginner_glossary.md#g096) | L0、L2、L155 |
| id2 | 显示结果 | RGBA16F / W×H | L157 | caller |
| id3 | 运动矢量 | RG16F / W×H | caller | 有历史时L2、L155 |
| id6 | 上帧历史 | RGBA16F / W×H | 上帧/本帧L156 | 有历史时L2、L155 |
| id9 | 当前时域状态 | RGBA16F / W×H | L155 | L156、L157 |
| id10 | 显示基底 | RGBA16F / W×H | L0 | L157 |

| params角色 | 消费位置与已知作用 |
|---|---|
| [style](APPENDIX_beginner_glossary.md#g005) / tone / structure | B0通道10/11/12；由half适配接入网络 |
| [p5](APPENDIX_beginner_glossary.md#g032) | p5真时structure=1、两个[mask](APPENDIX_beginner_glossary.md#g006)取控制缓冲；有历史时读自身id6，见[B0](L3_b0_input.md#p5-candidates) |
| 原生帧计数、模式、历史/MV句柄 | 噪声散列及历史有效合同；reset不能仅改帧计数 |
| intensity | L157显示混合，不增加B0输入通道 |
| 坐标尺度与偏移 | B0/B70采样变换；值和格式按实际params，不以屏幕分辨率代替 |

字段的十六进制字节偏移见[B0](L3_b0_input.md#channels)及[B70](L3_b70_history_output.md#postprocess)；这些数值作用不等于全部宿主API字段名称已知。

<a id="params"></a>
## params常量缓冲：已知偏移子集

偏移均为**十六进制字节偏移**，每行只适用于所列调用；这不是完整宿主ABI。表只汇总现有正文/绑定中已给出的字段，没有按名字推断其他偏移。

| 调用家族 / 已知长度 | 偏移、类型与含义 | 现有依据 |
|---|---|---|
| L1 clear / 16 B | CB+0x00 ([u64](APPENDIX_beginner_glossary.md#g057))工作区基址；CB+0x08 (u32)待填字数 | [工作区clear](L3_workspace_map.md#clear) |
| B0 / 264 B | CB+0xac (f32)/CB+0xb0 (f32)/CB+0xb4 (f32)为tone/structure/style；CB+0xb8 (f32)/CB+0xbc (f32)用于p5判定 | [16通道](L3_b0_input.md#channels) |
| B0 / 同上 | CB+0xa0 (f32)/CB+0xa4 (f32)为MV尺度；CB+0xc4 (f32)生成输入gain；CB+0xc8 (u32)帧字 | [坐标](L3_b0_input.md#coordinates) |
| B0 / 同上 | CB+0xc0 (u32)历史模式；CB+0x08 (u64)/CB+0x10 (u64)为历史/MV句柄；CB+0xd8 (u64)/CB+0xf8 (u64)为[full](APPENDIX_beginner_glossary.md#g018)/pool指针 | [守卫](L3_b0_input.md#guards)、[发布](L3_b0_input.md#publish) |
| [split16](APPENDIX_beginner_glossary.md#g013) ffwd / qkv / final_head | CB+0x00 (u64)输入、CB+0x08 (u64)输出；不把其他字段从同形核外推 | [逐调用绑定](examples/split16_window_r04d.bindings.json) |
| split16 ffwd_proj / proj / L132 | CB+0x00 (u64)主路、CB+0x08 (u64)本块残差、CB+0x10 (u64)输出；L56另有CB+0x18 (u64)pooled输出 | [角色绑定](examples/split16_window_r04d.bindings.json) |
| L58/L99 [repack](APPENDIX_beginner_glossary.md#g019) / 24 B | CB+0x00 (u64)/CB+0x08 (u64)输入/输出；CB+0x10 (u32)/CB+0x14 (u32)二维rows/cols | [重排接受域](L3_workspace_map.md#repack-domain) |
| ViT attention | CB+0x00 (u64)/CB+0x08 (u64)/CB+0x10 (u64)/CB+0x18 (u64)分别为Q/K/V/output；不按指针顺序猜实际布局 | [角色偏移](L3_workspace_map.md#regions) |
| L100 bridge | CB+0x00 (u64)/CB+0x08 (u64)/CB+0x10 (u64)主路/skip/输出 | [已有参数绑定](examples/split16_window_r04d.bindings.json) |
| B70 / 184 B | CB+0x30 (f32)预测颜色修正尺度；CB+0x94 (f32)/CB+0x8c (f32)/CB+0x9c (f32)及另轴CB+0x98 (f32)/CB+0x90 (f32)/CB+0xa0 (f32)构造MV坐标 | [颜色](L3_b70_history_output.md#b70-current)、[历史坐标](L3_b70_history_output.md#b70-temporal) |
| B70 / 同上 | CB+0xa4 (f32)/CB+0xa8 (f32)历史中心变换；历史点再用CB+0x7c (f32)/CB+0x74 (f32)/CB+0x84 (f32)及另轴CB+0x80 (f32)/CB+0x78 (f32)/CB+0x88 (f32)变换 | [时域公式](L3_b70_history_output.md#b70-temporal) |
| L157 / 376 B | CB+0x120 (f32)显示强度I；CB+0x144 (f32)/CB+0x14c (f32)/CB+0x150 (f32)/CB+0x154 (f32)为a/b/c/δ | [曲线与标量](L3_b70_history_output.md#post-curve)、[显示混合](L3_b70_history_output.md#intensity) |

## 两帧之间保留什么

| 对象 | 帧 t 的行为 | 帧 t+1 的来源 | reset 的作用 |
|---|---|---|---|
| id1 / id3 / params | caller 刷新当前颜色、MV、控制及原生帧字 | 再由 caller 刷新，不能注入原生网络中间结果作 CPU 预测输入 | API reset 由原生宿主发起；CPU 消费对应参数合同，不调用该 API |
| API 显式 reset | 原生宿主通过 API 发起重置，CPU 读对应 reset params | 新 id9 替换历史后，正常帧依 profile 恢复 carry | 不调用 API 来代替 CPU 预测，也不将 API reset 等同于清空整个 workspace |
| 参数变化触发 reset | 不读旧历史，条件通道7..9重复当前变换后的RGB | 计数及句柄按reset合同更新 | 本帧生成的新状态在帧尾覆盖id6 |
| p5历史条件 | 自身id6由当前id3[重投影](APPENDIX_beginner_glossary.md#g025)，进入7..9；structure=1、mask取CB | 下一帧继续从自身状态读取 | reset关闭历史消费 |
| id9→id6 | B70 写 id9，L156 按有效行复制 id6 | 本次保存的 id6 由下一帧 B0/B70 读取 | 已捕获 reset profile 使本帧跳过旧历史；无需先清空 id6，末尾新 id9 替换它 |
| id10 / id2 | 当前基底／当前显示结果 | 默认路线重写基底和显示；id2 不作为时域历史 | 156 路线使用自己的尾段合同，见下表 |
| workspace / 纹理缓冲 | CPU 自有链保留整片状态，逐调用覆写；[CumWrites](APPENDIX_beginner_glossary.md#g093)(L) 是声明累计写集 | 接续前一帧 CPU 状态，读取集合另按调用审计 | 不把 reset 描述成整片清零；任意初值[全域](APPENDIX_beginner_glossary.md#g111)独立尚未证明 |
| 噪声与函数资产 | 由坐标和实际 params 帧字重新散列；资产不可变 | 无递推 [RNG](APPENDIX_beginner_glossary.md#g075) 状态；表按调用加载，不携带像素随机状态 | 原生帧字可回到 0；视频绝对帧号与噪声计数不同 |

p5改变条件通道和历史读取，S157按精确元组执行颜色链；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。

## 158 与 156 路线

156分支省去基底备份与独立显示处理；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。

| 路线 | 已知触发 | 调用与尾段 | 当前解释边界 |
|---|---|---|---|
| 默认 158 | 本串默认具名 params | L0–L157；L0 保存 id10；L155 为默认 post_block，L156 复制，L157 后处理混合 | 158 是调用数，逻辑块为 B0–B70；各阶段计数见 INDEX |
| 156 | tone=0或style=0的具名分支 | 省去默认L0与L157；尾部写id2后复制id2→id6，只绑定1/2/3/6 | 显示与历史共用同一尾部结果 |

- 数值规则：图像状态/显示 RGB 最后 RZ 转 F16，alpha=1；内部矩阵、half 运算、量化及域外拒绝仍逐调用保留，见 [计算口径](INDEX.md#计算口径)。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（阶段、形状、源码接线）、MEASURED / CONTROLLED（具名链和 reset 控制）、INFERRED（块级语义）；[ARCH §1](../../../ARCHITECTURE_V3_ZH.md#1-全景)、[尾段变体](L3_b70_history_output.md#variants)、[历史合同](L3_b70_history_output.md#loop)。
- 往下：[L1 全部十片](INDEX.md) → 各 L1 的 L2 家族链接。

## 1080逻辑矩阵规模

这里[MAC](APPENDIX_beginner_glossary.md#g077)指一次[标量](APPENDIX_beginner_glossary.md#g076)乘加，GMAC=10⁹ MAC；只按已写矩阵维度及有效[查询](APPENDIX_beginner_glossary.md#g040)位置计数，使用内部画布1920×1152，不是[GPU](APPENDIX_beginner_glossary.md#g078)指令/CPU重复执行量、计时或带宽测量。[权重](APPENDIX_beginner_glossary.md#g079)列是矩阵系数槽位字节（E4每项1 B，B0适配/B70末端F16每项2 B），不含偏置、尺度、对齐，也不声称是唯一实物权重跨度。

| 阶段 | 矩阵槽位净字节 | 线性GMAC | QK＋AV GMAC |
|---|---:|---:|---:|
| B0 | 13,312 | 28.311552 | 9.059697 |
| TIN编码 | 6,367,232 | 130.233139 | 19.251855 |
| split16编码（已知小计） | 8,388,608 | 18.119393 | 1.132462 |
| ViT | 100,663,296 | 64.424509 | 6.710886 |
| L100 | 524,288 | 1.132462 | 0.000000 |
| split16解码（已知小计） | 8,388,608 | 18.119393 | 1.132462 |
| TIN解码 | 6,367,232 | 130.233139 | 19.251855 |
| B70 | 12,544 | 27.391427 / 27.462205 | 9.059697 |

B0含16→32适配；TIN按实际单头/分组FFN及编解码投影；ViT按8块的1024→4096→1024、QKV及投影；B70线性列分别为reset三预测量/有历史四预测量。每个有效窗口query使用64个key；不把移位窗被丢弃的query或数据驱动执行重复计算混入该逻辑口径。小数仅为显示舍入，整数原值在[真实代码与维度计算](examples/anatomy_r04i.py)及[结果](examples/anatomy_r04i.result.json)。

split16两行仅列8块FFN及512→512输出投影的已知小计；QKV投影的完整MKN、编码双出口额外投影及L57内部矩阵尚未全部闭式确认，因此不补全整网MAC或权重分摊。该表不把[UNKNOWN](APPENDIX_beginner_glossary.md#g104)补成标准dense [Transformer](APPENDIX_beginner_glossary.md#g012)。WEIGHTS_HT资源元数据为147,695,410 B，见[身份元数据](../../../WEIGHTS_IDENTITY.json)；资源容器与这里的运行时矩阵槽位不是同一口径，不能相加。
