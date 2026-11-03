# L3.tin-window：完整 TIN 窗口块与编解码交接

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-tin"></a>
【入门简化】一个小[窗口](APPENDIX_beginner_glossary.md#g015)内，先各位置改自己的[通道](APPENDIX_beginner_glossary.md#g007)，再比较位置、组合内容，两条较早的数字各在规定的起始小计处接回。先画少框版：

~~~mermaid
flowchart LR
    X["入口数字"] --> F["各位置处理 + 接回入口旁路"] --> Z["前馈结果"] --> A["窗口内交换内容"] --> P["输出投影 + 接回前馈结果旁路"] --> Y["块结果"]
    X -. "第一旁路" .-> F
    Z -. "第二旁路" .-> P
~~~

“接回”在[矩阵](APPENDIX_beginner_glossary.md#g051)累加起始小计处，非整段算完才加。窗口是位置范围，头是比较数字的分组，[FFN](APPENDIX_beginner_glossary.md#g037)组与设备工作分组又不同。[从一头块学起](L1_00_one_block_primer.md)后，下面保留多头、上[下采样](APPENDIX_beginner_glossary.md#g021)及格式差别。
<!-- beginner-r04m:end intro -->

[整串目录](INDEX.md) · 上层：[TIN 编码](L2_03_tin_encoder.md)、[TIN 解码](L2_08_tin_decoder.md) · 已展开分项：[FFN](L3_ffn.md#ffn)、[attention](L3_attention_softmax.md#window-attention)、[norm](L3_norm_nonfinite.md#norm32)、[工作区](L3_workspace_map.md#regions)

<a id="tin-window"></a>
## 本块覆盖什么

- 是什么：默认链的44次融合窗口[调用](APPENDIX_beginner_glossary.md#g080)，[编码](APPENDIX_beginner_glossary.md#g009)L3–L24、解码L133–L154；每次包含完整FFN、Q/K/V、Q/K[归一化](APPENDIX_beginner_glossary.md#g043)、窗口[attention](APPENDIX_beginner_glossary.md#g039)和输出[投影](APPENDIX_beginner_glossary.md#g038)。[chained](APPENDIX_beginner_glossary.md#g022)复用同一个核心，其他视图/尺度变体在核心前后增加接入或输出处理。
- 输入 → 输出：同档[逻辑](APPENDIX_beginner_glossary.md#g085)W×H×C的[E4](APPENDIX_beginner_glossary.md#g055)[特征](APPENDIX_beginner_glossary.md#g008)→8×8窗口中的64×C→同档[F16](APPENDIX_beginner_glossary.md#g054)结果，再按变体[发布](APPENDIX_beginner_glossary.md#g091)E4、[池化](APPENDIX_beginner_glossary.md#g018)出口或输出视图；upsample另读前档主路和编码[skip](APPENDIX_beginner_glossary.md#g016)。
- 怎么算：按下面11步和一张块内图追数据；先FFN，后attention。norm作用于投影后的Q/K，不在块入口，也不在FFN之前或之后再插一层通用[LayerNorm](APPENDIX_beginner_glossary.md#g044)。
- 数值规则：矩阵逐[K32](APPENDIX_beginner_glossary.md#g065)发布F16；两条[残差](APPENDIX_beginner_glossary.md#g017)的half乘法先形成矩阵[seed](APPENDIX_beginner_glossary.md#g042)，随后每步携带half；窗口越界位置补零但仍参与64键[归约](APPENDIX_beginner_glossary.md#g050)。half/E4发布及[非有限](APPENDIX_beginner_glossary.md#g069)拒绝不能由高精度库运算代替。
- 为什么：同尺度内用变化的窗口原点改变位置交互范围；降采样保留编码旁路，上采样把该旁路接回主路。训练意图、融合边界的硬件成因仍未知。
- 我们怎么知道：CPU源码、44份具名[params](APPENDIX_beginner_glossary.md#g083)核对和保存的数值门分别列在 [证据表](#evidence)；一致的出口不单独证明内部值或网络分解唯一。
- 往下：[窗口与头](#partition)、[真实顺序](#core)、[外围变体](#wrappers)、[八种尺度/方向配置](#variants)；更细数值规则沿页首四个分项链接下钻。

记号沿用 [INDEX](INDEX.md#形状与工作区记号)：空间尺寸写宽×高，[张量](APPENDIX_beginner_glossary.md#g076)局部矩阵写位置×通道；E4/F16为E4M3/binary16。[Q8](APPENDIX_beginner_glossary.md#g061)为half→E4的[RN-even](APPENDIX_beginner_glossary.md#g059)/[satfinite](APPENDIX_beginner_glossary.md#g062)，D8为精确E4→half；H+、H×、HF为half加、乘、融合乘加。K(A,W;s)是从half seed s起步、按原序逐K32发布F16的矩阵链。s_ff、s_att、s_skip和每头s_q表示模型中读取的尺度，只说明格式和用途，不列系数值。

<a id="partition"></a>

## 8×8分窗、原点与32通道头

先按本次[inputlayout](APPENDIX_beginner_glossary.md#g088)把物理字节解释为逻辑W×H×C，再分窗。设窗口编号为(bx,by)，窗内t=0,…,63：
```math
x=8b_x+(t\bmod8)+o_x,\qquad
y=8b_y+\lfloor t/8\rfloor+o_y.
```
当前接受的原点各轴为0或−4。若0≤x<W且0≤y<H，取该位置的C个E4；否则整位置填E4 [+0](APPENDIX_beginner_glossary.md#g070)。**这是平移窗口网格，不是把整张特征图循环回卷**；边缘没有按有效键数裁短attention或改成排除式[mask](APPENDIX_beginner_glossary.md#g006)。计算完仅把有效坐标写回，窗外计算结果丢弃。[取窗/散回源码:154–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L154)

窗口画布并不总等于有效图像：
```math
(C_W,C_H)=
\begin{cases}
(W-2o_x,\ H-2o_y),&C=32,\\
(8\lceil(W-o_x)/8\rceil,\ 8\lceil(H-o_y)/8\rceil),&C=64,128,256.
\end{cases}
```
窗口数为(C_W/8)×(C_H/8)；C=32路径还检查画布能被8整除。W/H必须为正、为4的倍数且不超过当前已配置内部画布，原点不满足上述集合则拒绝；这不是任意几何的支持宣称。[尺寸/原点守卫:143–155](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L143)

1080的四档有效特征分别为960×576×32、480×288×64、240×144×128、120×72×256，均E4。每窗位置数固定64，头数h=C/32，即1/2/4/8头；每头Q、K、V的通道维均32。Q/K/V从64×3C的half结果按Q区、K区、V区各自拆头；物理通道置换由布局/[权重](APPENDIX_beginner_glossary.md#g079)解包解决，不能把原始字节视图直接reshape。[头切分:119–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119)

<a id="core"></a>
## 实际顺序：FFN → QKV → norm(Q/K) → attention → 投影

以下是一个窗口的完整行为链，x₈为64×C的E4入口：

~~~text
1. 取本窗x₈；旁路x₁₆=D8(x₈)，但一头upsample改取保留的未量化merge。
2. r_ff=H×(x₁₆,s_ff)，作为FFN收缩/末投影的half seed。
3. 按L3.ffn执行扩张→G→收缩；得到包含入口残差的z：64×C F16。
4. z₈=Q8(z)：64×C E4。
5. qkv=K(z₈,W_qkv;+0)：64×3C F16；此处才投影Q/K/V。
6. 每头各自norm32(Q)、norm32(K)，Q另乘RN16(s_q)；Q/K/V发布E4。
7. 每头score_ij=Q32(Q_i,K_j,对应half位置偏置)：64×64 F16。
8. TIN分数做分开的F32乘、F32加→RN16→clamp→编码变换，得到正half权重w。
9. 固定half树求D；核对分母域，查RCP并转half；p=Q8(H×(w,r))。
10. 每头以p和V作两次K32（前32键、后32键），再Q8；拼成av：64×C E4。
11. r_att=H×(一头取z、多头取D8(z₈),s_att)；
    y=K(av,W_proj;r_att)：64×C F16。散回后按外围变体发布。
~~~

第3步一头为64×32×128扩张、逐通道G、64×128×32收缩；多头按每组C→128→32→C的实际分解和量化点执行，见 [FFN通道账](L3_ffn.md#channels)。核心 [window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130)直接给出“FFN在前”的顺序，没有额外的入口norm，也没有attention之后再接第二个FFN。

第6步对每头32个half只求平方和、max下界和[RSQ](APPENDIX_beginner_glossary.md#g072)；不减均值，ε是下界而非加到平方和的项。归约树、平方融合方向与各次RN16见 [norm32](L3_norm_nonfinite.md#norm32)。Q为Q8(H×(H×(Q,r_q),RN16(s_q)))；K使用单位尺度，V直接Q8，不经过该归一化。[norm与发布:114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)

第8–10步保留 [TIN分数与分母树](L3_attention_softmax.md#window-attention) 的原精度：先RN32(score×0.044921875)，再RN32加1.30078125，之后RN16、夹到[1.03125,1.5693359375]，按已写编码变换生成w。[分母](APPENDIX_beginner_glossary.md#g048)Den的half编码须在[0x1c00,0x60e0]，且[函数表](APPENDIX_beginner_glossary.md#g074)查找必须有相应项；不能换成half FMA或数学库[softmax](APPENDIX_beginner_glossary.md#g047)。窗口权重先归一化再量化E4，[AV](APPENDIX_beginner_glossary.md#g077)的两次K32之间携带F16。[attention:122–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L122)

<a id="residuals"></a>
### 两条残差都在矩阵seed处加入

| 接口 | 来源与发布 | 不可合并的边界 |
|---|---|---|
| FFN入口残差 | 普通块取D8(x₈)，一头upsample取未量化merge；H×到F16后进入收缩/末投影seed | 不能把缩放乘法和整个矩阵相加融合到最后；多头FFN的组间half携带保持原序 |
| attention输出残差 | C=32取未量化z；C≥64取D8(Q8(z))，再H×到F16，作为W_proj首K32的seed | z₈供[QKV](APPENDIX_beginner_glossary.md#g040)读取；一头旁路不能从z₈还原，多头也不能跳过这次E4量化 |
| 解码skip合并 | 主路低分辨率投影给F16 a；HF(D8(skip),s_skip,a)发布half merge，再Q8 | 最近邻只复制投影结果；HF的发布和其后的E4发布不同；B66保留merge供FFN seed，其他档从量化值解码 |

每个矩阵K32结束都发布F16，seed只在起点带入而后逐步携带；不存在可任意移到末端的一次通用实数“+ residual”。y同样先是half，外围出口才决定从它直接Q8或另算池化，布局变换自身不增加舍入。[矩阵接口:88–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88)

<a id="diagram"></a>
## 块内图：1080的1h/32c，B1 / L3

例取原点(0,0)：960×576×32 E4中每个8×8窗取64×32 E4，输出散回同形。其余调用更换原点和外围；核心接口不按窗口数改写。

~~~mermaid
flowchart TD
    IMG["输入视图：960×576×32 E4"] --> X["8×8分窗：64×32 E4"]
    X --> EX["扩张：64×32×128 K32链 → 64×128 F16"]
    EX --> G["逐通道G → 64×128 E4"]
    X --> RF["D8(入口) × s_ff → 64×32 F16 seed"]
    G --> FC["收缩：64×128×32，携带seed → z：64×32 F16"]
    RF --> FC
    FC --> ZQ["Q8(z)：64×32 E4"]
    ZQ --> QKV["投影：64×32×96 → 64×96 F16"]
    QKV --> QK["Q/K：各64×32 F16 → 各自 norm32；仅 Q 乘查询尺度 → E4"]
    QKV --> V["V：64×32 F16 → Q8 → E4"]
    QK --> SCORE["Q32 + half位置偏置 → 64×64 F16"]
    SCORE --> P["分数变换、half分母树、RCP、H×、Q8 → 64×64 E4"]
    P --> AV["与V作两次K32，Q8 → 64×32 E4"]
    V --> AV
    FC --> RA["未量化z × s_att → 64×32 F16 seed"]
    AV --> PROJ["输出投影64×32×32，携带seed → y：64×32 F16"]
    RA --> PROJ
    PROJ --> OUT["Q8、布局、散回 → 960×576×32 E4"]
~~~

<a id="wrappers"></a>
## 共享chained核心与四种外围

**chained**读写本档内部[TIN](APPENDIX_beginner_glossary.md#g011)布局，执行上述完整核心；每次仍[绑定](APPENDIX_beginner_glossary.md#g103)自己的权重、区间、原点和发布区，函数复用不意味着数值复用。输入视图解码、输出视图编码均为[位型](APPENDIX_beginner_glossary.md#g057)排列，不是新的归一化。

| 外围种类 | 围绕核心添加的行为 | 数值/布局约束 |
|---|---|---|
| inpview | 将上一档pool的分平面输入解到本档逻辑位置，再运行核心；结果为本档内部布局 | 入口仍是W×H×C E4；取窗之前处理输入布局，不新增池化或升采样 |
| ds_wait | 核心得到y F16；full=Q8(y)留作skip；另从同一未量化y作2×2平均，再量化、投影C→2C、量化成pool | full与pool是两条独立路径，不能从full解码重做平均；pool按分平面布局交下一档 |
| upsample | 前档2C通道主路先在低分辨率格作2C→C的K32投影；以floor(x/2),floor(y/2)最近邻×2取数；HF与本档编码full合并，再送核心 | 分窗原点不移动最近邻源坐标；输入布局为前档outview。merge是否保留未量化值见残差表 |
| outview_wait | 本档末核心照常计算，之后将Q8(y)编码成供后继读取的输出视图；不产生pool | 多头为16通道一组的分平面视图；B69按配置执行outputlayout，但其原生独立布局仍[UNKNOWN](APPENDIX_beginner_glossary.md#g104) |

下采样平均严格为
```math
p=Q8\!\left(H\times\!\left(H+\!\left(H+(y_{00},y_{01}),H+(y_{10},y_{11})\right),\tfrac14\right)\right),\qquad
\mathrm{pool}=Q8\!\left(K(p,W_{\rm ds};+0)\right).
```
三次H+和一次H×分别发布half；平均后的p先E4，再做C→2C。补齐位置按声明范围取零；pool分配extent依params而定，不总是有效W/H直接减半。L24还含名义512通道之外相关平面的显式零写，不能只发布有效值、裁掉这些写入或清空整个相邻区。[pool与补齐:162–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L162)

上采样为
```math
a=K(\mathrm{main}_8,W_{\rm up};+0),\qquad
m_{xy}=HF\!\left(D8(\mathrm{skip}_{xy}),s_{\rm skip},a_{\lfloor x/2\rfloor,\lfloor y/2\rfloor}\right),\qquad
x_8=Q8(m).
```
B66/C=32把m保留为FFN入口旁路；B48/B56/B62改用D8(x₈)。1440的B48有效高92、分窗画布可到96，额外行不作为有效输出写回。[合并与种子取值:151–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L151)

当前CPU实现为配置了releaseword的调用在数值输出之后写完成标记；44份绑定中inpview、chained、upsample有该[角色](APPENDIX_beginner_glossary.md#g084)，ds_wait、outview_wait没有同一单独角色。核名的wait字样不直接定义CPU等待动作，也不关闭原生同步/[别名](APPENDIX_beginner_glossary.md#g092)/生命周期语义；本页不从字符串补出并发证明。[发布:179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L179)

<a id="variants"></a>
## 四档、双方向与全部窗口原点

下表均为**已钉SHA的1080默认params实例**，空间边界来自 [INDEX extent表](INDEX.md#形状与工作区记号)，不推广为全部控制/几何。原点简记：0=(0,0)，xy=(−4,−4)，x=(−4,0)，y=(0,−4)；序列按B/launch递增逐项对应。各档每次恰有一个融合窗口调用。

| 方向 / 头数、C | 本档宽×高×C（E4） | B / launch，次数 | 核种类顺序 | 原点序列 | 尺度出口与skip配对 |
|---|---|---|---|---|---|
| 编码 / 1h、32 | 960×576×32 | B1–B4 / L3–L6，4 | inpview→2 chained→ds_wait | 0,xy,x,y | B4.full→B66；pool 480×288×64 |
| 编码 / 2h、64 | 480×288×64 | B5–B8 / L7–L10，4 | inpview→2 chained→ds_wait | 0,xy,x,y | B8.full→B62；pool 240×144×128 |
| 编码 / 4h、128 | 240×144×128 | B9–B14 / L11–L16，6 | inpview→4 chained→ds_wait | 0,xy,x,y,0,xy | B14.full→B56；pool 120×72×256 |
| 编码 / 8h、256 | 120×72×256 | B15–B22 / L17–L24，8 | inpview→6 chained→ds_wait | 0,xy,x,y,0,xy,x,y | B22.full→B48；pool 60×36×512 |
| 解码 / 8h、256 | 120×72×256 | B48–B55 / L133–L140，8 | upsample→6 chained→outview_wait | 0,xy,x,y,0,xy,x,y | 主路60×36×512 + B22.full；末视图交B56 |
| 解码 / 4h、128 | 240×144×128 | B56–B61 / L141–L146，6 | upsample→4 chained→outview_wait | x,y,0,xy,x,y | 主路120×72×256 + B14.full；末视图交B62 |
| 解码 / 2h、64 | 480×288×64 | B62–B65 / L147–L150，4 | upsample→2 chained→outview_wait | 0,xy,x,y | 主路240×144×128 + B8.full；末视图交B66 |
| 解码 / 1h、32 | 960×576×32 | B66–B69 / L151–L154，4 | upsample→2 chained→outview_wait | 0,xy,x,y | 主路480×288×64 + B4.full；末视图交B70 |

因此完整skip对为B4/L6↔B66/L151、B8/L10↔B62/L147、B14/L16↔B56/L141、B22/L24↔B48/L133；每条skip保留本档full E4和本档空间尺寸，并非把池化出口拿来充当旁路。C=32的attention旁路保留未量化z，B66另保留未量化merge供FFN seed；其余三档按上文量化再解码，不能因形状相同而互换。


<a id="tin-code-transcription-r04o"></a>
### TIN地址索引：源码转写层级

证据层级为 **code-transcribed index formula**：以下是字节复现执行器在源码中采用的索引，不是r03新推导或新留出验证。[r03结果](../../../experiments/mapform-tin-r03-20261027-codex/RESULT_ZH.md)的判定是NOT_RUN_MISSING_1080_ADDRESS_TABLES，未冻结公式、未读取新地址表元素。既有 `tin_map(H,W,C)` 输出布局仍沿用其【实测】闭式层级：旧TIN64/TIN128地图逐元素复现，C256预测由B15联合验证且保留原边界；[既有证据](../../../ARCHITECTURE_V3_ZH.md#L580)不因r03缺表而升降级。

下式可直接按Python整数运算执行，对应[logical_of及双向读写 tin.cpp:73–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L73)。p是物理E4字节序号，返回逻辑HWC字节序号；C=64/128/256时off位位序和xs对应4行物理块。按源码调用域提供可整除的物理宽高。

~~~text
def logical_of(p, W, H, C, layout):
    perm = (0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15)
    if layout != 0:
        j = p % 16
        x = (p // 16) % W
        y = (p // (16*W)) % H
        plane = p // (16*W*H)
        return (y*W+x)*C + 16*plane + perm[j]
    if C == 32:
        tile, lane, byte = p // 512, (p % 512) // 16, p % 16
        x = (lane >> 2) & 3
        y = (lane >> 4) + 2*((byte >> 2) & 1)
        c = 2*(lane & 3) + (byte & 1) + 8*((byte >> 1) & 1) + 16*(byte >> 3)
        return ((4*(tile // (W//4))+y)*W + 4*(tile % (W//4))+x)*32+c
    off, blk, xs = p % 4096, p // 4096, 1024 // C
    positions = (('c',0),('c',3),('y',1),('c',4),('c',1),('c',2),('x',0),('x',1),('y',0))
    c = x = y = 0
    for index, (axis, bit) in enumerate(positions):
        value = ((off >> index) & 1) << bit
        if axis == 'c': c |= value
        elif axis == 'x': x |= value
        else: y |= value
    pos = 9
    for bit in range(5, C.bit_length()-1):
        c |= ((off >> pos) & 1) << bit
        pos += 1
    for bit in range(2, xs.bit_length()-1):
        x |= ((off >> pos) & 1) << bit
        pos += 1
    return ((4*(blk // (W//xs))+y)*W + xs*(blk % (W//xs))+x)*C+c
~~~

下节给可执行的rowperm/n128矩阵面板偏移、逆向、QKV重排及bias的tokeninternal式，分别对应[tin.cpp:26](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26)、[tokeninternal:33](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L33)和[bias索引:46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L46)。它们描述位置而不读取系数。RSQ/RCP以及F03的Radius和cos/sin依然是**table-driven function values**：表中是函数结果，不是地址映射；源码索引转写不消除这些值表依赖，也不改变B69原生布局UNKNOWN。

<a id="resource-layout-r04l"></a>
### 资源矩阵、bias与头分支（排名26起）

以下为 code-transcribed index formula 层级的CPU解包[闭式](APPENDIX_beginner_glossary.md#g020)，不列任何系数值；不是r03新留出验证。`P=(0,1,4,5,8,9,12,13,2,3,6,7,10,11,14,15)`，矩阵K、N均为32的倍数；本页n128式还限定N为128的倍数，当前C>32时N=4C+128满足这个条件。对逻辑(k,n)：

~~~text
rk=16*(k//16)+P[k%16]; kt=rk//32; nt=n//32; ki=rk%32; ni=n%32
lane=4*(ni%8)+(ki%16)//4; elem=ki%4+4*(ki//16)
frag=(ni//8)%2; pair=ni//16
tile=4*((nt//4)*(K//32)+kt)+nt%4  # n128；否则 kt*(N//32)+nt
offset=1024*tile+512*pair+16*lane+8*frag+elem
W[k,n]=resource[base+offset]
~~~

逆向从offset取[tile](APPENDIX_beginner_glossary.md#g087)、pair、lane、frag、elem；`ki=4*(lane%4)+elem%4+16*(elem//4)`，`ni=lane//4+8*frag+16*pair`。普通tile逆为 `(kt,nt)=divmod(tile,N//32)`；n128逆为 `kt=(tile//4)%(K//32), nt=4*((tile//4)//(K//32))+tile%4`。再对rk的低4位应用P的逆排列，恢复k。这样也给出了打包式；无需读真实系数。[tin.cpp:26–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26)。

资源游标o初值0；`mat(K,N,major)`消费K*N字节，`half(n)`消费2n字节LE16，跳过字节不解释为系数。顺序完整为：C=32时ex(32,128)、branch(128,32)；C>32时ex(C,4C+128,n128)、out(C,C)；up时extra(2C,C)；若非up或C=32跳16；cs(C)；up时若C=32再跳16，读sin(C)，非up则跳16；qkv(C,3C)；[bias](APPENDIX_beginner_glossary.md#g052)(H*4096)，H=C/32；H个LE32 scale各RN16；o向上对齐16；proj(C,C)；ca(C)；down时extra(C,2C)。每次消费先核o+len≤资源长。[tin.cpp:34–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34)。

C≥64的QKV逻辑列 `type*C+32*h+c` 来自原解包列 `96*h+32*type+c`，type=0..2、c=0..31。`I(t)=32*((t//8)//4)+16*((t%8)//4)+4*((t//8)%4)+t%4`；令r=I(i)、c=I(j)，bias(h,i,j)从半数组索引 `4096h+256*(4*(r//16)+c//16)+8*(4*(r%8)+(c%8)//2)+4*((c%16)//8)+2*((r%16)//8)+c%2` 读取。正向/反向为同一双射的读取/散写，不增加舍入。[tin.cpp:43–50](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L43)。

C>32每头复用的三矩阵是：`ex_h[k,j]=ex[k,128h+j]` (C×128)，`branch_h[k,j]=ex[32h+k%32,4C+32*(k//32)+j]` (128×32)，`out_h[k,j]=out[32h+k,j]` (32×C)。panel只把逻辑矩阵转为列主存储 `panel[j*K+k]`，预解码不改变数值、不新增half发布。[tin.cpp:53–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L53)。

<a id="view-layout-r04l"></a>
### 输入/输出视图的双向字节式（排名27起）

以下字节置换是 code-transcribed index formula，适用于本页全部20种核族，不构成r03新留出验证。`decode[L(p)]=physical[p]`，`encode[p]=logical[L(p)]`；两方向不作数值转换。非零layout采用planar16：`j=p%16,x=(p//16)%W,y=(p//(16W))%H,plane=p//(16WH)`，`L(p)=(yW+x)C+16plane+Q[j]`，`Q=(0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15)`；反向 `p=16*((c//16*H+y)*W+x)+Q_inverse[c%16]`。

layout=0、C=32时，`tile=p//512,l=(p%512)//16,b=p%16`；`x=(l>>2)&3,y=(l>>4)+2*((b>>2)&1),c=2*(l&3)+(b&1)+8*((b>>1)&1)+16*(b>>3)`，外部tile原点为 `(4*(tile%(W//4)),4*(tile//(W//4)))`。逆式：取全局x/y的低2位为xx/yy，`l=((c>>1)&3)+4*xx+16*(yy&1)`，`b=(c&1)+2*((c>>3)&1)+4*(yy>>1)+8*(c>>4)`，`p=512*((y//4)*(W//4)+x//4)+16l+b`。

layout=0、C=64/128/256时，xs=1024/C，off=p%4096，blk=p//4096；off低9位依序送到 `(c0,c3,y1,c4,c1,c2,x0,x1,y0)`，其后先送c5..log2(C)−1，再送x2..log2(xs)−1。全局x/y分别加 `xs*(blk%(W//xs))`、`4*(blk//(W//xs))`，`L(p)=(yW+x)C+c`。逆式把这些位依相同顺序拼回off，`blk=(y//4)*(W//xs)+x//xs`，`p=4096blk+off`。要求W/H满足物理tile整除条件，不能把裁剪后的逻辑宽度拿来求tile地址。[tin.cpp:72–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L72)。这关闭CPU字节排列的说明，不关闭B69原生独立坐标标签UNKNOWN。

<a id="zero-planes-r04l"></a>
### L24额外平面的字节范围（排名145）

C=256的down输出另执行64个planar16平面（包括名义512通道以外32平面）的边界零写。`validW=(W+1)//2,validH=(H+1)//2`；对plane=0..63、y=0..PH−1，`begin=validW if y<validH else 0`；begin≥PW则为空，否则相对pooledword指针写 `off=16*((plane*PH+y)*PW+begin)`、`len=16*(PW-begin)` 个零字节。先用受检乘法、再核指针+off不溢出和整个span在[工作区](APPENDIX_beginner_glossary.md#g082)内；有效行的[0,validW)保留，不能清整个pooled分配而覆盖别名有效值。[tin.cpp:165–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L165)。独立release的qword、长度与空集合见[工作区合同](L3_workspace_map.md#release-contract-r04l)。

<a id="evidence"></a>
## 我们怎么知道

| 对象 | 依据与支持范围（各一行） |
|---|---|
| 核心接线 | [CENSUS](APPENDIX_beginner_glossary.md#g100)：[window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130)、[norm/attention:114–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)给出顺序、head与seed；CPU实现分解不单独证明原生内部唯一 |
| 44份窗口配置 | 本轮只读 [参数核对记录](examples/tin_window_r04c.bindings.json)：全部params实际SHA等于保存绑定，extent、原点和视图字段相符；这是内容核对，没有新数值运行 |
| 旧逐launch门 | MEASURED：[TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3)为L3/7/11/18/24/133/134/151三方全工作区一致；其余36个NOT_RUN保持，[teacher-forced](APPENDIX_beginner_glossary.md#g106)不等于连续链 |
| 后来的具名链 | MEASURED：[M2记录](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)含1080/1440 f0全部44个TIN调用；4K的[M2](APPENDIX_beginner_glossary.md#g107)新数值仅[L0](APPENDIX_beginner_glossary.md#g081)–L99，其TIN解码不能据配置普查改成新测，统一M的后来三帧另有 [范围](L3_b70_history_output.md#evidence) |
| 编解码旁路 | CENSUS / MEASURED：[ARCH §4.5、§4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66)与本页params/源码共同支持四对skip、最近邻和融合；不把同形地址或一次字节对照升级为任意输入结构定理 |
| 保留未知 | L133 [computed-shared](APPENDIX_beginner_glossary.md#g108)符号来源层仍NOT_ADMITTED，B69原生独立布局仍UNKNOWN；一般几何、完整同步/别名/生命周期与内部值唯一未建立，数值链通过不自动解除 |

正数范数归约可[上溢](APPENDIX_beginner_glossary.md#g071)到+Inf；是否被具体RSQ接口吸收按 [非有限合同](L3_norm_nonfinite.md#nf-path)判断，不写成“有限输入保证所有内部有限”。QMMA非有限seed/half overflow、E4 NaN、缺表/域外、参数/区间/窗口画布不满足时仍拒绝，不能用G的饱和量化替前一步放行。长SHA、逐调用配置和旧发布缺项修正记录留在 [TIN证据附录](APPENDIX_evidence_history.md#tin-window-r04c)。

半窗移位使后继窗口可把原边界两侧的位置放进同一交互域，扩大跨窗信息路径；其训练收益未独立测量。补齐到8×8整窗则是已读取窗/散回循环及其尺寸守卫的实际要求，不从此推出根画布高度的通用取整公式。
