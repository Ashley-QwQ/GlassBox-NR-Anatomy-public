# L3.window-attention：split16完整块与四核交接

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-split"></a>
【入门简化】这段让每位置[512](APPENDIX_beginner_glossary.md#g007)项数经过八个[窗口](APPENDIX_beginner_glossary.md#g015)块。每块先各位置处理，再在8×8位置内交换内容；入口[旁路](APPENDIX_beginner_glossary.md#g016)接[前馈](APPENDIX_beginner_glossary.md#g037)收缩，前馈结果旁路接[注意力](APPENDIX_beginner_glossary.md#g039)[后投影](APPENDIX_beginner_glossary.md#g038)。少框版是：

~~~mermaid
flowchart LR
    X["块入口"] --> F["逐位置处理；收缩起点接入口旁路"] --> Z["前馈结果"] --> A["窗口比较与内容混合"] --> P["投影起点接前馈旁路"] --> Y["块出口"]
    X -. "第一条" .-> F
    Z -. "第二条" .-> P
~~~

位置网格→窗口→16个比较头→每头32项，是一套[逻辑](APPENDIX_beginner_glossary.md#g085)关系；FFN八组与设备执行坐标另算，见[四种分组](L1_00_one_block_primer.md#groups)。末端变稀与桥接的独立空间配对仍有问号，下面[DAG](APPENDIX_beginner_glossary.md#g089)[合同](APPENDIX_beginner_glossary.md#g101)不把未知抹掉。
<!-- beginner-r04m:end intro -->

[整串目录](INDEX.md) · 上层：[split16编码](L2_04_split16_encoder.md)、[split16解码](L2_07_split16_decoder.md) · 已展开分项：[FFN](L3_ffn.md#channels)、[窗口attention](L3_attention_softmax.md#window-attention)、[Q/K norm](L3_norm_nonfinite.md#map-norm)、[工作区/地址图](L3_workspace_map.md#address-maps)

<a id="window-attention"></a>
## 本块覆盖什么

- 是什么：512通道、[16头](APPENDIX_beginner_glossary.md#g013)的窗口块[家族](APPENDIX_beginner_glossary.md#g080)；[编码](APPENDIX_beginner_glossary.md#g009)B23–B30用L25–L57共33次调用，解码B40–B47用L101–L132共32次，共65次。通常一块四核，B30另含L57宽度适配。
- 输入 → 输出：第5档X₅(512) [E4](APPENDIX_beginner_glossary.md#g055)→同档512通道E4；编码末端另[发布](APPENDIX_beginner_glossary.md#g091)X₆(512)，经final_head成X₆(1024)进入[ViT](APPENDIX_beginner_glossary.md#g014)；解码末端发布供[TIN](APPENDIX_beginner_glossary.md#g011)[上采样](APPENDIX_beginner_glossary.md#g021)读取的[outview](APPENDIX_beginner_glossary.md#g022)。
- 怎么算：**ffwd → ffwd_proj → qkv（含Q/K[归一化](APPENDIX_beginner_glossary.md#g043)与attention）→ proj**。先完成FFN及其入口[残差](APPENDIX_beginner_glossary.md#g017)，再做窗口attention及其输出投影/残差；没有额外的块入口[LayerNorm](APPENDIX_beginner_glossary.md#g044)或attention之后的第二套FFN。
- 数值规则：[矩阵](APPENDIX_beginner_glossary.md#g051)逐[K32](APPENDIX_beginner_glossary.md#g065)发布[F16](APPENDIX_beginner_glossary.md#g054)；G、Q/K统计量、[分母树](APPENDIX_beginner_glossary.md#g050)、half[尺度](APPENDIX_beginner_glossary.md#g031)乘法和E4发布均保留各自节点。两条残差先[H×](APPENDIX_beginner_glossary.md#g063)到half [seed](APPENDIX_beginner_glossary.md#g042)，再随矩阵链逐步携带，不能移到完整点积之后一次相加。
- 为什么：“块”按同一入口、两条旁路和下一块出口组织；四次launch之间有实际[工作区](APPENDIX_beginner_glossary.md#g082)[角色](APPENDIX_beginner_glossary.md#g084)交接。为何原生选择这四个融合边界、其训练动机和硬件容量原因仍未知。
- 我们怎么知道：具名[params](APPENDIX_beginner_glossary.md#g083)/地图、CPU执行器和保存的分段/整链结果分别列在 [证据表](#evidence)；出口字节一致不证明唯一的网络分解。
- 往下：[四核顺序](#order)、[16头与分窗](#heads)、[qkv八字段地址闭式](#qkv-closed-form-r04n)、[1080布局账](#layout)、[块内图](#wiring)、[编解码变体](#variants)。本页保留已有分项的算术；新增闭式只展开地址与索引。

E4/F16、K32与X₅/X₆沿用 [INDEX记号](INDEX.md#形状与工作区记号)；[Q8](APPENDIX_beginner_glossary.md#g061)、D8、H×的定义见 [FFN记号](L3_ffn.md)。N_out在本页始终是单次执行器返回的**字节长度**，并非新的通道轴。

<a id="order"></a>
## 四次launch怎样构成一块

设X为本块入口E4，U为ffwd出口，Z为ffwd_proj出口，A为融合qkv出口，Y为最终投影出口：

~~~text
ffwd       : X → 512→512预投影、E4 → 八组64→256→G→64、E4 → U
ffwd_proj  : U + 本块X → 512→512后投影，以H×(D8(X),s_ff)作seed → Z的E4
qkv        : Z → Q/K/V → norm(Q/K)、E4 → 64键attention、AV、E4 → A
proj       : A + 本块Z → 输出投影，以H×(D8(Z),s_att)作seed → Y的E4
下一块     : 以Y为自己的X，重新绑定权重、旁路、原点及工作区区间
~~~

前两行的通道与全部量化点见 [split16 FFN表](L3_ffn.md#channels)。ffwd的核内门宽为2048，出口U仍为512通道；这八组逐位置FFN分组与后面的16个attention头是不同的轴。

qkv内部先投影Q/K/V，再执行 [32通道Q/K统计量](L3_norm_nonfinite.md#map-norm)，V直接发布E4；随后 [窗口分数、half归约、RCP、AV](L3_attention_softmax.md#window-attention)全部在这一次launch内完成。因此A已是attention出口，不能把该核当成只生成三份待后核消费的Q/K/V。norm属于这里的Q/K路径，其余三个常规核没有由此新增一层norm。

两条旁路来源不同：ffwd_proj读本块X，proj读本块Z；二者均是已发布E4的精确解码，再独立half乘尺度。已核对的L28普通proj、L56双出口投影、L132末视图图，其矩阵链首seed均为这种缩放后的旁路，后续各K32携带half；L28的每条投影链为16步K32。具体取数图的活动seed字节也全部落在第二个输入角色，不只是形状相同。[图与来源核对](APPENDIX_evidence_history.md#split16-window-r04d)

CPU执行器依图顺序运行矩阵/逐元素节点，按输出列表把返回字节切回具名区间，再执行该[绑定](APPENDIX_beginner_glossary.md#g103)的完成标记[副作用](APPENDIX_beginner_glossary.md#g094)。[split16.cpp:65–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L65)；L132实际走 [entry.cpp:93–94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L93) 的专用末视图接线。四个名字描述的是不同的计算/存储边界，函数复用不意味着[权重](APPENDIX_beginner_glossary.md#g079)、数值或同步角色复用；也不从wait/chained字样补出完整的原生并发证明。

<a id="heads"></a>
## 16头、8×8窗口与移位

逻辑通道关系是512=16×32。每个8×8窗口有64个位置；每头Q/K/V各64×32，分数及归一化权重各64×64，[AV](APPENDIX_beginner_glossary.md#g077)回到64×32；16头结果交给输出投影，形成下一块的512通道主干。头合并的物理交错与写回按map，不能把原始出口字节直接reshape成任意头序。

8×5个8×8窗覆盖64×40画布，[pooled](APPENDIX_beginner_glossary.md#g018)逻辑容量为32×20×512 E4。已测地图中，327,680 B由20,480个16 B写事件唯一覆盖；按8192 B分桶得到40桶。【推断】把每个8×8输入窗配对到一个4×4空间出口与这些整数相容，但容量分桶不建立空间接线。确立配对还需独立标定输入窗编号及pooled字节的逻辑(x,y,c)，逐写事件核对其来源/目的坐标；涉及L100的恢复则还需输出与skip布局的独立坐标标定。详细整数来源见[L100算子](L2_06_decoder_bridge.md#operator)。

1080有效第5档为宽60×高36；四种已声明位移的覆盖均为8×5个窗口，每窗仍有64键。这个40是窗口计数，不是[CTA](APPENDIX_beginner_glossary.md#g087)数，也不把主出口的位置数改为40×64。qkv的窗口数、边界来源、跨lane选择和写回现有[本家族闭式](#qkv-closed-form-r04n)，不能套用TIN公式，也不能把1080恰好不变的窗口数推广到其他几何。

本轮实际读取16次qkv的params：宽/高位于第3个U64字，原点位于第4个U64字（均从0计）。编码B23–B30与解码B40–B47各自都是

~~~text
(0,0), (−4,−4), (−4,0), (0,−4), (0,0), (−4,−4), (−4,0), (0,−4)
~~~

位移改变时重绑来源图；同位移的图在具名实例中可相同，不能据此复用权重或数值，也不能把相同SHA当作全部动态来源已证明。16头[bias](APPENDIX_beginner_glossary.md#g052)的独立排序准入仍[UNKNOWN](APPENDIX_beginner_glossary.md#g104)，沿用 [ARCH排序边界:577](../../../ARCHITECTURE_V3_ZH.md#L577)与 [具体attention图边界](L3_attention_softmax.md#graph-bindings) 的保留口径。

<a id="qkv-closed-form-r04n"></a>
## qkv八字段地址闭式：留出地图精确验证

证据层级为 **closed forms verified on held-out map tables（闭式，已在留出地图表验证）**，原判定 **PARTIAL_QKV_CLOSED_FORM_8/9_FIELDS_HELDOUT_EXACT**。以下是CPU地址/索引表的CLOSED_FORMULA，不是新增原生数值测量。[研究结果](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md)、[冻结物理说明](../../../experiments/mapform-split16-qkv-r01-20261027-codex/FORMULAS_ZH.md)与[冻结公式源码](../../../experiments/mapform-split16-qkv-r01-20261027-codex/formula_qkv.py)分别保存结论、推导和实现。

“留出”、EXACT与TABLE的含义见[标签图例](APPENDIX_beginner_glossary.md#address-status)。

**坐标卡。** $H,W$是物理补齐后的token高宽，不是原始帧像素，已验域内为正的4倍数；$(d_x,d_y)$各取−4或0。8×8窗口起点为$(8w_x+d_x,8w_y+d_y)$，覆盖式为

```math
G_X=\left\lceil\frac{W-d_x}{8}\right\rceil,\quad
G_Y=\left\lceil\frac{H-d_y}{8}\right\rceil,\quad Q=G_XG_Y,\quad A=4Q.
```

表坐标$(a,y,\ell,e,b)$中，$a\in[0,A)$按窗口x最快、窗口y其次、head组最慢展平；$y\in[0,4)$为CTA内[warp](APPENDIX_beginner_glossary.md#g087)编号，$\ell\in[0,32)$为lane，$e$是各字段自己的事件编号，$b$是向量内字节。解开为

```math
w_x=a\bmod G_X,\quad w_y=\lfloor a/G_X\rfloor\bmod G_Y,\quad
z=\lfloor a/Q\rfloor,\quad h=4z+y.
```

下文F18.36这类写法是审计家族/条目编号，见[编号说明](L2_04_split16_encoder.md#audit-family-ids)；不要与F16/half数格式混读。

$z$是四个head组之一，每组四个warp各管一个head；$h$为CPU布局中的16个head编号，每头32项。它没有独立证明原生bias的head/query/key标签排序，F18.36继续UNKNOWN。每个4×4物理块保存$4\cdot4\cdot512=8192$ B输入；一行有$W/4$块。下列常数均是布局大小、字节步长或事件分组，不是模型系数。

**资源加载 `wload_off`，$0\le e<112$。** 前96事件为16个K32篮、每篮6次16 B事务，处理512输入项的Q/K/V面板；后16事件读每head的64×64 F16位置偏置平面：

```math
\mathrm{wload}=\begin{cases}
49152\lfloor e/6\rfloor+3072h+512(e\bmod6)+16\ell,&e<96,\\
786432+8192h+512(e-96)+16\ell,&96\le e<112.
\end{cases}
```

$49152=16\cdot3\cdot32\cdot32$是一篮全head段，$3072=3\cdot32\cdot32$是单head篮段，$512=32\cdot16$是一轮lane事务；$786432=512\cdot1536$是QKV面板总长，$8192=64\cdot64\cdot2$是单head偏置平面大小。这里只计算资源内地址。

**共享位置 `sread_shared_off`，$0\le e<64$：**

```math
\mathrm{shared}=512(e\bmod16)+16\ell.
```

每16事件走完8192 B共享区，64事件循环四次；不随窗口、head组或warp变化。

**共享来源 `sread_src`，$0\le e<64,\ 0\le b<16$：**

```math
t_x=2w_x+d_x/4+(\lfloor e/2\rfloor\bmod2),\quad
t_y=2w_y+d_y/4+(\lfloor e/4\rfloor\bmod2).
```

若$0\le t_x<W/4$且$0\le t_y<H/4$，则

```math
\mathrm{sread}=8192(t_yW/4+t_x)+1024\lfloor e/8\rfloor
+512(e\bmod2)+16\ell+b;
```

否则每个字节都为**−1**，表示常量零；不能先把−1加上$b$。64事件分八个64项组、四个空间子块和两个32项半段；1024是4×4块内64项片段的字节数，512是其32项半段。各head读取相同的512项输入，因此来源不依赖$h$。

**两次4 B资源访问 `xsite_src` / `xsite_wsrc`，$0\le e<2,\ 0\le b<4$：**

```math
\mathrm{xsite\_src}=-3,\qquad
\mathrm{xsite\_wsrc}=917504+4h+b.
```

**−3**表示从资源空间读取，不是输入字节或常量零。$917504=786432+16\cdot64\cdot64\cdot2$，跨过QKV面板和16个偏置平面；两个事件取相同资源位置，不随lane、窗口或事件变化。不读取该地址的资源数值。

**写回 `gstore_off`，$0\le e<4$：**

```math
t_x=2w_x+d_x/4+(e\bmod2),\quad t_y=2w_y+d_y/4+\lfloor e/2\rfloor.
```

使用与sread相同的物理块边界条件；有效时

```math
\mathrm{gstore}=8192(t_yW/4+t_x)+2048z+512y+16\ell,
```

否则为**−1**，该写事务跳过。2048是$4\cdot4\cdot128$ B的head组片段，512是$4\cdot4\cdot32$ B的单head片段；结果是16 B事务起点。窗口位移落在4×4块界，越界用哨兵，不对图像宽高取模roll。sread的−1补零与gstore的−1跳写是两个动作。

**交换来源 `shfl_idx`，$0\le e<72$。** 令$p=e\bmod36$，后32事件再令$j=p-4$：

```math
\mathrm{shfl}=\begin{cases}
4(\ell\bmod8)+(\lfloor\ell/8\rfloor\mathbin{\oplus}p),&p<4,\\
\lfloor\ell/4\rfloor+8(j\bmod2)+16\lfloor j/16\rfloor,&4\le p<36.
\end{cases}
```

$\oplus$是整数按位异或。前四事件重组lane低三位，并交换高两位；后32事件在8-lane分组的低/高16-lane部分交替取来源。36事件为一轮，两轮相同。

**二选一 `psel`，$0\le e<32$。** 令$p=e\bmod16$，$\mathrm{bit}_k(\ell)=\lfloor\ell/2^k\rfloor\bmod2$：

```math
\mathrm{psel}=\begin{cases}
\mathrm{bit}_0(\ell),&p<4,\\
1-\mathrm{bit}_1(\ell),&4\le p<8,\\
1-\mathrm{bit}_3(\ell),&8\le p<12,\\
1-\mathrm{bit}_4(\ell),&12\le p<16.
\end{cases}
```

两轮16事件重复四个选择族，1/0分别选择节点的第一/第二来源；不是条件概率。

**第九字段 `thread_class`仍TABLE。** 1080全部推导表均无该字段（NOT_PRESENT），冻结的单类别0假说在留出历史表上失败：1536/2048元素不等。该表虽事后可描述为四类各512项、随CTA轴变化，不能把验证后描述改记为新通过公式。现有生产执行器仍读取原表，本轮没有集成公式后端。[冻结失败及唯一含类别的表](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md#thread_class失败保留类别表)

**验证与适用边界。** 1080物理$H\times W=36\times60$是推导集；参考$12\times12$、640×360类$12\times20$、1440的$48\times80$和4K的$68\times120$为留出，覆盖各自已有四种位移。冻结前用过留出header的shape来明确覆盖式，未读留出元素；冻结后没有改公式。研究对495条物化NPZ路径绑定容器SHA，8字段逐元素/数组payload逐字节一致，负哨兵及无效区未跳过。不同容器可能共享数组，不能视作独立原生采集，也不宣称清单外几何或归档已覆盖。

这里闭合的是地址图相等；不升级数值DAG、完整链或动态原生血缘/同步证明，F18.36排序与其他家族地图仍保持原状态。原审计F18.02/.03/.04/.39四整行由TABLE改CLOSED；F18.05的shfl_idx、psel子字段CLOSED，thread_class子字段TABLE，按最弱项汇总仍TABLE。[逐行与逐字段分类](examples/r04n.classification.json)

<a id="qkv-worked-r04n"></a>
### 两个窗口的便宜复查

[只读示例脚本](examples/qkv_closed_form_r04n.py)导入冻结公式，独立转写上式，只从NPY流中取58个地址/索引单元，与存表并排打印，不运行完整地图、模型或链。[本轮结果与源SHA](examples/r04n.qkv_samples.json)。下表两窗均取$(d_x,d_y)=(-4,-4)$、$y=2,\ell=5,z=0$；1080选$(w_x,w_y)=(0,0)$，$G_X,G_Y=8,5,a=0$；4K选$(1,1)$，$G_X,G_Y=16,9,a=17$。完整回执还用lane21检查psel的0分支。

| 字段/局部坐标 | 1080公式 / 存表 | 4K公式 / 存表 |
|---|---:|---:|
| wload_off，e=96 | 802896 / 802896 | 802896 / 802896 |
| sread_shared_off，e=16 | 80 / 80 | 80 / 80 |
| sread_src，e=0,b=15 | −1 / −1 | 254047 / 254047 |
| sread_src，e=6,b=7 | 87 / 87 | 507991 / 507991 |
| xsite_src，e=1,b=3 | −3 / −3 | −3 / −3 |
| xsite_wsrc，e=1,b=3 | 917515 / 917515 | 917515 / 917515 |
| gstore_off，e=3 | 1104 / 1104 | 509008 / 509008 |
| shfl_idx，e=35 | 25 / 25 | 25 / 25 |
| psel，e=8 | 1 / 1 | 1 / 1 |

这些是真实存表的地址数，不是模型系数或图像结果；58格复查不替代研究已保存的全表留出验证，也没有重跑该验证。


<a id="rest-closed-form-r04o"></a>
## F16、F17、F19–F23：共享物理块与各字段闭式

证据层级：**closed forms verified on held-out map tables**，仅适用于下表标为EXACT的具体非空字段和已绑定几何；其余行保留FAIL、TABLE或VACUOUS。1080为推导集，r02冻结后首次读取留出元素；[结果](../../../experiments/mapform-split16-rest-r02-20261027-codex/RESULT_ZH.md)、[逐式说明](../../../experiments/mapform-split16-rest-r02-20261027-codex/FORMULAS_ZH.md)、[冻结公式](../../../experiments/mapform-split16-rest-r02-20261027-codex/formula_rest.py)。r04已绑定并验证F16/F17/F19–F22的4K地址图；F18沿用r01的独立QKV结果。F23的H=36、W=60表已绑定并比对，但r04没有独立绑定该表的4K输入帧身份。数组相等不证明数值DAG、全链、同步或独立原生动态血缘。

| 族与物理角色 | 非空字段的r02判定 | 空字段 / 类别 | 已绑定几何 H×W |
|---|---|---|---|
| F16：L25 ffwd_inpview | wload_off、sread_shared_off、gstore_off EXACT；sread_src FAIL | xsite_src/xsite_wsrc：仅一张留出表存空数组VACUOUS，1080 NOT_PRESENT | 36×60推导；12×12、12×20、48×80（1440）及68×120（4K）留出；4K三路径/一容器 |
| F17：L26 ffwd_proj_inpview | wload_off、sread_shared_off、gstore_off、xsite_src、xsite_wsrc EXACT；sread_src FAIL | 无类别字段通过结论 | 36×60推导；12×12、12×20、48×80及68×120（4K）留出 |
| F19：普通proj | sread_shared_off、sread_src、gstore_off EXACT；wload_off、xsite_src、xsite_wsrc FAIL（shape） | thread_class假说FAIL，保持TABLE | 36×60推导；12×12、12×20、48×80及68×120（4K）留出 |
| F20：普通ffwd | wload_off、sread_shared_off、sread_src、gstore_off EXACT | 两个xsite全空VACUOUS；thread_class假说FAIL，保持TABLE | 36×60推导；12×12、12×20、48×80及68×120（4K）留出 |
| F21：普通ffwd_proj | wload_off、sread_shared_off、sread_src、gstore_off、xsite_src、xsite_wsrc EXACT | thread_class假说FAIL，保持TABLE | 36×60推导；12×12、12×20、48×80及68×120（4K）留出 |
| F22：L56 proj_pool | wload_off、sread_shared_off、sread_src、gstore_off、xsite_src、xsite_wsrc、shfl_idx、psel EXACT | thread_class候选也与留出表EXACT，仍保持TABLE | 36×60推导；12×12、12×20、48×80及68×120（4K）留出 |
| F23：L57 final_head | wload_off、sread_shared_off、sread_src、gstore_off EXACT | 两个xsite全空VACUOUS | pooled输入20×32推导；8×8、8×12、24×40和36×60留出；4K输入帧身份未独立绑定 |


<a id="r04-four-k-r04p"></a>
### r04几何绑定与逐字段计数

r04将62条候选中31条绑定并对10个不同的“容器SHA、家族、几何”组合逐元素、数组payload逐字节对照，416,023,808个元素无差；另外28条L132和3条B31不在公式域，分别保持OUT_OF_SCOPE和NOT_RUN。[结构化绑定](../../../experiments/mapform-split16-r04-20261027-codex/BINDINGS.json)、[比较结果](../../../experiments/mapform-split16-r04-20261027-codex/COMPARISONS.json)、[身份回执](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json)；不将副本路径数当独立采集数。

下表F16/F17/F19–F22均为H=68、W=120的4K物理token网格，使用冻结r02式；每个非空字段逐元素及数组payload EXACT/0。路径数与容器SHA数分列，元素数为去重比较后的字段元素数。W=资源偏移、Sh=共享偏移、S=共享来源、G=写回；X和Xw是两个xsite字段。

| 家族 | 路径 / 不同容器 | 每字段元素数（各EXACT/0） |
|---|---:|---|
| F16 | 3 / 1 | W 4,423,680；Sh 2,211,840；S 35,389,440；G 276,480 |
| F17 | 1 / 1 | W 2,211,840；Sh 2,211,840；S 35,389,440；G 276,480；X、Xw各13,271,040 |
| F19 | 7 / 1 | W 4,423,680；Sh 2,211,840；S 35,389,440；G 276,480；X、Xw各13,271,040 |
| F20 | 7 / 1 | W 8,847,360；Sh 2,211,840；S 35,389,440；G 276,480；X、Xw各0（空数组VACUOUS） |
| F21 | 7 / 1 | W 2,211,840；Sh 2,211,840；S 35,389,440；G 276,480；X、Xw各13,271,040 |
| F22 | 2 / 1 | W 2,211,840；Sh 2,211,840；S 35,389,440；G 345,600；X、Xw各13,271,040；类别34,560；交换8,847,360；选择2,211,840 |

F18是qkv，**不是r02公式族**，r04没有新跑QKV。其4K由[r01冻结QKV公式的既有留出结果](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md#每字段每几何留出结果)支持：12路径、4个不同容器，8字段逐元素及payload EXACT；每字段分别为W 31,997,952、Sh 18,284,544、S 292,552,704、X和Xw各2,285,568、G 1,142,784、交换20,570,112、选择9,142,272个元素。四个容器可能共享数组，不等于四次独立采集。F18/F19/F20/F21的thread_class失败不被4K无类别字段的精确结果覆盖；F22类别虽已对照，仍保留表驱动。

F16的1440 L25是H=48、W=80，一路径、一容器：W 1,966,080、Sh 983,040、S 15,728,640、G 122,880项均EXACT/0。参数和map通过[同一bundle的两个SHA记录](../../../experiments/parity-cpp-geo2-l62-diagnosis-r01-20261009-codex/LINUX_1440_RESET_REUSE_PLAN_V3.json#L5397)绑定，参数字节实读对应48×80。

F23**没有独立绑定4K输入帧身份的表**。r04确实绑定一份位于high2160路径的F23 H=36、W=60物理表，其W 2,621,440、Sh 1,310,720、S 20,971,520、G 163,840项EXACT/0，两个xsite为空；[绑定条目](../../../experiments/mapform-split16-r04-20261027-codex/BINDINGS_ZH.md#L88)及[比较回执](../../../experiments/mapform-split16-r04-20261027-codex/COMPARISONS.json)给出几何和SHA。路径标签不足以单独建立帧身份，因此不把它误写成H=68、W=120，也不把它自动升级为完整4K帧数值或链证明。

r04的中文Markdown报告原件含大量问号，部分正文已损坏；r04随后用 `repair_reports.py` 从结构化JSON重建了报告，损坏原件保留为 `*.garbled-ascii`，预声明正文无法恢复，只有 `PREDECL_RECOVERED_NOTE_ZH.md` 说明。本页以结构化JSON和下列原始记录为准，不自行修复源文件。[本轮证据核对](examples/r04p.evidence.json)保存身份与范围。

**历史表：保留r02原判定，r04分类另列。** 接受图指对应计划所选的12×12图；已有保存的r02逐元素与数组payload比较均EXACT/0。r04把下列三张历史变体、五个字段的失败分别标为NON_PRODUCTION_VARIANT，不改写r02回执。

| 字段 | r02原判定 | r04分类 | 原始记录与接受图 |
|---|---|---|---|
| F16 sread_src | MISMATCH 1,015,808；首差(0,0,0,0,4)：存表−2、公式384 | NON_PRODUCTION_VARIANT | [校准方式及未初始化记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/reuse-audit.json#L42)、[校准模式](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/maps/L25-tidx-zero-calibration.json#L18)、[接受计划](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/plans/L25-r3.json#L16)；接受图对应字段EXACT/0（1,048,576项） |
| F17 sread_src | MISMATCH 3,456；首差(0,0,0,1,0)：存表6656、公式512 | NON_PRODUCTION_VARIANT | [工具缺陷记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/tool-bugs.jsonl#L12)、[失败图记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/maps/L26-lane.r2-position-and-numbering-defects.json#L176)、[后续记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/DISCOVERY_LOG_ZH.md#L44)、[接受计划](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/plans/L26-r1.json#L16)；接受图EXACT/0（1,048,576项） |
| F19 wload_off | SHAPE_MISMATCH：存表(8,8,32,68)，公式(8,8,32,64) | NON_PRODUCTION_VARIANT | [L28工具缺陷记录](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r02-l27-l28/tool-bugs.jsonl#L2)、[接受计划](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r02-l27-l28/plans/L28-r1.json#L15)；接受图EXACT/0（131,072项） |
| F19 xsite_src | SHAPE_MISMATCH：存表(8,8,32,32,4)，公式(8,8,32,48,4) | NON_PRODUCTION_VARIANT | 同一L28历史图；接受图EXACT/0（393,216项） |
| F19 xsite_wsrc | SHAPE_MISMATCH：存表(8,8,32,32,4)，公式(8,8,32,48,4) | NON_PRODUCTION_VARIANT | 同一L28历史图；接受图EXACT/0（393,216项） |

三份接受图的容器SHA、逐字段哈希和元素数分别见[r02 L25](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L4243)、[L26](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L4340)、[L28](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L5044)保存比较与[r04校验](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json)。**没有回执证明C++执行器读取了这三份具体12×12图**；计划选图、图与公式相等、实际执行器血缘分别看。r02在这些历史变体上的失败及thread_class失败仍保留，不能追改为PASS。

F19/F20/F21的thread_class在1080 NOT_PRESENT，冻结的单类别0假说分别在留出表失配1280/2048、1280/2048、768/1024；原类别表继续使用。F22的独立类别候选在本轮表逐项EXACT，但仍按本轮要求保留表驱动，且不能将此标签一致推广为动态类别血缘。空xsite数组的零字节相等是**真空检查**，不是非空资源地址证据；原执行器仍读原表。

### 坐标、形状和共享块

沿用qkv节的物理token宽高H、W和表坐标(a,y,l,e,b)，但本组非qkv的窗口无位移：Gx=ceil(W/8)、Gy=ceil(H/8)、Q=Gx*Gy。a为展平CTA，y为warp，l为lane 0..31，e为本字段事件，b为事务字节。与qkv不同，本组的CTA展平次序如下；F23的H/W是pooled输入尺寸。

```math
\begin{aligned}
&\mathrm{F16,F20}: &&w_x=a\bmod G_x,\quad w_y=\lfloor a/G_x\rfloor\bmod G_y,\quad z=\lfloor a/Q\rfloor;\\
&\mathrm{F17,F19,F21,F22}: &&b_x=a\bmod(2G_x),\quad w_x=b_x\bmod G_x,\quad w_y=\lfloor a/(2G_x)\rfloor,\quad z=\lfloor b_x/G_x\rfloor;\\
&\mathrm{F23}: &&\text{同上，将 }2G_x\text{ 换成 }4G_x;\qquad h=4z+(y\bmod4).
\end{aligned}
```

h是64通道组编号，不能当作注意力的head；F19/F20/F23有8个warp，令r=floor(y/4)选择4×4空间块的上下半区，其余族r=0。F16/F20和F17/F19/F21/F22的CTA数为2Q，F23为4Q。

把qkv节的4×4物理块抽为公共函数P_C；每块为16C字节，i是块内偏移。V是F16/F17的inpview平面位置，p为16通道平面，i为平面内字节：

```math
\begin{aligned}
P_C(t_x,t_y,i)&=\begin{cases}16C(t_y(W/4)+t_x)+i,&0\le t_x<W/4,\ 0\le t_y<H/4,\\-1,&\text{其他};\end{cases}\\
V(x,v,p,i)&=\begin{cases}16(HWp+vW+x)+i,&0\le x<W,\ 0\le v<H,\\-1,&\text{其他}.\end{cases}
\end{aligned}
```

整个无效元素为−1，不能在哨兵上继续加b或旁路基址；sread的−1表示零，gstore的−1跳写。512通道时块步长8192 B，与qkv共用同一块算术；F23输出用C=1024。该复用不表示CTA或事件顺序相同。


各字段形状为(A,Y,32,事件[,字节])；这里A是本家族的CTA数：F16/F17/F19/F20/F21/F22为2Q，F23为4Q，不统一沿用qkv的A=4Q。表中事件数是声明域，空事件轴不是一条零地址。

| 家族 | Y | wload | sread/shared | gstore | xsite（每事件4 B） |
|---|---:|---:|---:|---:|---:|
| F16 | 4 | 128 | 64 | 8 | 0（若存储） |
| F17 | 4 | 64 | 64 | 8 | 96 |
| F19 | 8 | 64 | 32 | 4 | 48 |
| F20 | 8 | 128 | 32 | 4 | 0 |
| F21 | 4 | 64 | 64 | 8 | 96 |
| F22 | 4 | 64 | 64 | 10 | 96 |
| F23 | 8 | 64 | 32 | 4 | 0 |

sread_src每事件16 B；F22另有shfl_idx 256事件、psel 64事件及类别字段。历史表额外事件不能被静默截掉。

### wload_off 与共享位置

普通64事件，F17/F19/F21/F22采用S=16384；F16/F20的前64事件也取S=16384。F23因1024输出通道采用S=32768：

```math
\mathrm{wload}=S\lfloor e/4\rfloor+2048h+512(e\bmod4)+16l.
```

S是一个K32篮跨全部输出通道的面板字节数；2048=64×32是单64通道组，512=32 lane×16 B是一轮事务。F16/F20前64事件同普通式，后64事件令j=e−64、p=j mod 8、k=floor(j/8)：

```math
\mathrm{wload}=\begin{cases}
262144+16384h+1024k+8192\lfloor p/2\rfloor+512(p\bmod2)+16l,&p<4,\\
393216+16384h+2048k+512(p-4)+16l,&p\ge4.
\end{cases}
```

262144是512×512面板末尾，扩张组占131072 B，393216为收缩段起点。F19上述式在r02历史变体发生shape失败，r04分类为NON_PRODUCTION_VARIANT；接受图和4K图EXACT，原失败保持可查。

sread_shared_off的F16/F22为512(e mod 16)+16l，F17/F21周期为24。F19/F20/F23取p=12/8/12：

```math
\mathrm{shared}=4096\lfloor(e\bmod p)/4\rfloor+512(e\bmod4)+2048r+16l.
```

4096为共享片区步长，2048r选择上下半区；周期复用共享位置，并非更换模型数值。

### sread_src：各家族如何取输入

F17/F21/F22采用下式；F17的r02历史变体FAIL、r04分类为NON_PRODUCTION_VARIANT，其接受图及4K图EXACT；其它两个族在已绑定表内EXACT：

```math
t_x=2w_x+(\lfloor e/2\rfloor\bmod2),\quad
t_y=2w_y+(\lfloor e/4\rfloor\bmod2),\quad
i=1024\lfloor e/8\rfloor+512(e\bmod2)+16l+b,\quad \mathrm{sread}=P_{512}(t_x,t_y,i).
```

F19/F20/F23以warp半区替换事件空间位，因而事件数减半：

```math
t_x=2w_x+(\lfloor e/2\rfloor\bmod2),\quad t_y=2w_y+r,\quad
i=1024\lfloor e/4\rfloor+512(e\bmod2)+16l+b,\quad \mathrm{sread}=P_{512}(t_x,t_y,i).
```

F16 inpview将lane与byte位拆到空间坐标和16通道平面；不能把地址当作简单base+b。其r02历史变体FAIL，r04分类为NON_PRODUCTION_VARIANT，接受图及4K图EXACT：

```math
\begin{aligned}
x&=8w_x+4(\lfloor e/2\rfloor\bmod2)+(\lfloor l/4\rfloor\bmod4),\\
v&=8w_y+4(\lfloor e/4\rfloor\bmod2)+\lfloor l/16\rfloor+2(\lfloor b/4\rfloor\bmod2),\\
p&=4\lfloor e/8\rfloor+2(e\bmod2)+\lfloor b/8\rfloor,\quad
i=4(l\bmod4)+(b\bmod4),\quad \mathrm{sread}=V(x,v,p,i).
\end{aligned}
```

### gstore_off、xsite与F22第二出口

gstore的普通事件用tx=2wx+(floor(e/2) mod 2)、i=1024h+512(e mod 2)+16l；ty在8-warp族为2wy+r，其余为2wy+floor(e/4)。结果是P_512(tx,ty,i)的16 B事务起点；F23用P_1024。F22前8事件同普通式，事件8、9写拼接空间的pooled第二出口，Wp=4Gx、Hp=4Gy：

```math
\mathrm{pooled}=512HW+8192(w_y(W_p/4)+w_x)+1024h+512(e-8)+16l.
```

Wp/Hp包括完整补齐；此式关闭地址索引，不由它推出pool数值算法。

F17/F21/F22各96次4 B xsite事件，前n=32取旁路；F19共48次，前n=16取旁路；r02历史变体有shape失败，r04分类为NON_PRODUCTION_VARIANT，接受图和4K图EXACT。e≥n时xsite_src=−3表示资源，xsite_wsrc给资源字节偏移；e<n时xsite_wsrc=−1，xsite_src用下列旁路相对位置，合法时加拼接基址512HW，越界仍为−1：

```math
\mathrm{xsite\_wsrc}=\begin{cases}
-1,&e<n,\\
262144+128h+16(\lfloor((e-n)\bmod16)/2\rfloor)+4(l\bmod4)+b,&e\ge n.
\end{cases}
```

262144是512×512面板字节长，128是64个F16项。F17旁路用inpview：x=8wx+4(floor(e/8) mod2)+(floor(l/4) mod4)，v=8wy+4floor(e/16)+2(e mod2)+floor(l/16)，p=4h+(floor(e/2) mod4)，i=4(l mod4)+b，取V(x,v,p,i)。

F19/F21/F22旁路取P_512。令q=floor(e/4)、t=e mod4；最后一组q=n/4−1时word=t，其余奇数q取3−t，其余偶数q取(−t) mod4：

```math
t_x=2w_x+(\lfloor e/8\rfloor\bmod2),\quad
t_y=\begin{cases}2w_y+r,&\mathrm{F19},\\2w_y+\lfloor e/16\rfloor,&\mathrm{F21/F22},\end{cases}
\quad i=1024h+512(\lfloor e/4\rfloor\bmod2)+16l+4\,\mathrm{word}+b.
```

F16/F20/F23无xsite事件，不应以空数组推断非空地址。

### F22交换、选择与类别候选

F22的shfl_idx有256事件，以下式每16事件重复；psel有64事件。−2是无效类别哨兵，0/1为两个来源选择值：

```math
\begin{aligned}
\mathrm{shfl}&=(l\bmod4)+8(\lfloor l/4\rfloor\bmod2)+4(\lfloor e/4\rfloor\bmod2)+16(\lfloor e/8\rfloor\bmod2),\\
\mathrm{psel}&=\begin{cases}-2,&\lfloor l/8\rfloor\bmod2=0,\\1-\lfloor l/16\rfloor,&\text{其他}.\end{cases}
\end{aligned}
```

thread_class候选在F22留出表EXACT：令laneclass在lane第3位为1时为1，否则为2floor(l/16)；右界R=[8wx+4≥W]、下界B=[8wy+4≥H]，则候选为laneclass+3R+3(1+[W mod8≠0])B。它是已比对的类别标签式，生产口径仍保留原表，不声称独立动态类别唯一性。

### 一个留出窗口的复查

[只读CPU例](examples/split16_rest_r04o.py)对F22的H=12、W=20，窗口(wx,wy)=(2,1)、a=8、y=0，从绑定存表抽13格，冻结公式、独立转写和存表13/13一致。[回执](examples/r04o.example.json)包含容器及公式SHA。例中sread事件2字节15与gstore事件2均为−1；gstore事件8为163920；psel在lane 5/9/25分别为−2/1/0。该抽样不替代已保存的全表留出结果。

<a id="layout"></a>
## 1080的N_out字节合同与可建立的逻辑轴

本例S=60×36=2160，T=32×20=640。以下是参数角色、前后接线和已知通道宽支持的**逻辑形状**，不声明连续[HWC](APPENDIX_beginner_glossary.md#g088)/CHW；各物理排列仍需读取自己的map。

| 1080具名出口 | N_out（B） | 已建立的逻辑角色 | 轴的边界 |
|---|---:|---|---|
| L25 ffwd | 1,105,920 | S×512 E4，即60×36×512 | 核内2048门通道不落成2048通道的本核出口 |
| L26 ffwd_proj | 1,105,920 | S×512 E4 | 供qkv主路，也独立保留给L28旁路 |
| L27 qkv | 1,105,920 | 融合attention的S×512 E4出口 | 不是三份物理Q/K/V；CPU八字段已有[留出表验证闭式](#qkv-closed-form-r04n)，原生head/query/key独立逻辑标签仍UNKNOWN |
| L28 proj | 1,105,920 | 下一块S×512 E4 | 16步K32是算术链长，不是16个连续存储通道组 |
| L56 proj_pool | 1,433,600 | full为1,105,920 B的S×512；pooled为327,680 B的T×512 | 返回值按长度切到两个参数指针，不能把总长除以S发明新通道宽 |
| L57 final_head | 655,360 | T×1024 E4，即32×20×1024 | 出口宽已知，内部矩阵分片轴未由宽度唯一确定 |
| L132 outview_wait | 1,105,920 | S×512 E4，供B48上采样主路读取 | 末视图映射为专用接线，不能替换成普通proj的存储图 |

执行表中的“外层任务×子任务×32并行位置×事件”属于取数/写回组织。比如1080 L25的写回表是(80,4,32,8)，每个活动事件写16 B；80、4、32、8均不能仅凭数值认作空间、头或通道轴，有效写回/类别还由图控制。[地址表解释](L3_workspace_map.md#address-maps)、[实际shape](L3_workspace_map.md#other-maps)。qkv内部Q/K/V、AV及投影的每个完整物理轴分解，超出上述已绑定关系的部分继续UNKNOWN。

【CPU 重建／实际读表】1080 L56的pooled物理字节0在拼接返回值中是字节1,105,920；[gstore_off](APPENDIX_beginner_glossary.md#g090)中唯一覆盖它的事件索引为(0,0,0,8)，该16 B事件起点正是1,105,920。这四个数依次是外层任务、子任务、并行位置、写事件，不命名为空间坐标。[脚本与整数结果](examples/map_trace_r04f.py)、[SHA与具体选择器](examples/map_trace_r04f.result.json)可查。已有seed来源核对还确定旁路来自第二输入角色；从该写事件到完整逻辑空间/通道规律的独立标定仍UNKNOWN，不能把pooled字节0直接认作左上角。L100可继续追到[已确定的瓶颈源坐标](L2_06_decoder_bridge.md#byte-trace)。

<a id="wiring"></a>
## 块内图：1080 B23，L25–L28

图中外部S×512为逻辑角色；qkv框内标出**一窗、每头**的形状，窗口与头的物理合并仍由图指定。图里的尺度只表示用途，不列模型系数。

~~~mermaid
flowchart TD
    X["L24 pool / 本块X：60×36×512 E4"] --> F["L25 ffwd_inpview：预投影与分组G/收缩"]
    F --> U["U：2160×512 E4"]
    U --> FP["L26 ffwd_proj_inpview：16步K32 → E4"]
    X --> RF["D8(X) × s_ff → F16 seed"]
    RF --> FP
    FP --> Z["Z：2160×512 E4"]
    subgraph QKERNEL["L27 qkv：投影、norm与attention融合"]
        QKV["一窗：16头，Q/K/V每头64×32 F16"] --> NQ["Q/K 各自 norm；仅 Q 乘查询尺度 → E4；V直接Q8"]
        NQ --> SC["每头64×64分数/正核权重"]
        SC --> AV["每头两次K32汇合V → 64×32 E4"]
    end
    Z --> QKV
    AV --> A["按图合并/写回A：2160×512 E4"]
    A --> P["L28 proj：16步K32，携带F16 seed"]
    Z --> RA["D8(Z) × s_att → F16 seed"]
    RA --> P
    P --> Y["Y：60×36×512 E4 → B24 / L29"]
~~~

<a id="variants"></a>
## 编码与解码的九种核入口

| 变体 | 编码入口 | 解码入口 | 围绕同一块接线的差异 |
|---|---|---|---|
| ffwd_inpview | L25 / B23，1次 | — | 从TIN pool视图接入；内部FFN照本家族图执行 |
| ffwd_proj_inpview | L26 / B23，1次 | — | 同块入口仍是L24 pool；首块后投影把主路带入chained视图 |
| ffwd | L29,33,…,53，7次 | L101,105,…,129，8次 | 本块入口→FFN前段；编码/解码分别绑定权重和输入 |
| ffwd_proj | L30,34,…,54，7次 | L102,106,…,130，8次 | 后投影合入当前块入口seed；不取前一块旁路 |
| qkv | L27,31,…,55，8次 | L103,107,…,131，8次 | Q/K/V、Q/K norm、窗口attention融合；原点逐块取上列序列 |
| proj | L28,32,…,52，7次 | L104,108,…,128，7次 | attention输出投影，合入当前块Z；输出给下一块ffwd |
| proj_pool | L56 / B30，1次 | — | 双出口：full留作B39 skip；pooled换到32×20供L57，空间归约按冻结图 |
| final_head | L57 / B30，1次 | — | pooled 512→1024通道角色；输出指针接L58，非分类头语义 |
| outview_wait | — | L132 / B47，1次 | 最后投影/残差后改用末视图图，交B48/TIN；执行入口为entry |

计数为编码33、解码32，共65。L56的两个出口各自有写回图；“pool”不单独证明标准2×2平均池化，也不能只从full重建pooled。L57属于[瓶颈](APPENDIX_beginner_glossary.md#g010)宽度适配，不把它算成第九个窗口attention块。桥接L100把B30.full接回解码入口，见 [新增桥接图](L2_06_decoder_bridge.md#wiring)；两段与ViT之间的搬运见 [repack图与4×4 tile](L3_workspace_map.md#repack-diagram)。

<a id="dual-dag-r04l"></a>
## L56双出口与L57完整分片合同（排名159、164）

两行现改为 **TABLE_DRIVEN_DESCRIBED**：算术、seed、发布点和全部依赖已由现图写全，事件到逻辑坐标的选择继续显式依赖表。可检查的安全投影为[L56 DAG](examples/r04l.L56.dag.json)、[L57 DAG](examples/r04l.L57.dag.json)，生成器只读旧JSON，保留源SHA；删除原事件地址标签，stores.event改为原事件列表的0基序号。nodes是图序号而非硬件寄存器，matrices中A/B/C是引用这些图节点的16/8/4项数组；stores给每事件16个输出字节节点及类别，顺序不改。没有读取系数或执行网络。

每节点代表32个lane的[向量](APPENDIX_beginner_glossary.md#g076)。W(site,byte)取 `weight[wload_off[c,w,l,site]+byte]`；S(site,byte)按sread_src取输入，−1为0、其他负数拒绝。X/XH按xsite逐4 B组装byte/LE16，−3选权重、−1选0、类别−7标无效；E精确E4→half、Q作half→E4 [RN-even](APPENDIX_beginner_glossary.md#g059)/[satfinite](APPENDIX_beginner_glossary.md#g062)，K是声明的half常量。SI(site,a)取 `a[shfl_idx[c,w,l,site]]`；PS(site,a,b)按psel=1/0选a/b，其他值拒绝（类别−2标无效）。F add/mul分别RN16(a+b)、RN16(a*b)，不能合并舍入；出现无效依赖时不得发布，未执行的类不外推为有效。[scalar_map.hpp:244–290](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L244)。

第o个矩阵事件，row=0..15、col=0..7、k=0..31：

~~~text
la=4*(row%8)+(k%16)//4; ra=row//8+2*(k//16)
lb=4*col+(k%16)//4; rb=k//16
left[k]=value(A[4*ra+k%4])[la]
right[k]=value(B[4*rb+k%4])[lb]
lane=4*(row%8)+col//2; part=2*(row//8)+col%2
M[o,part][lane]=K32(left,right,value(C[part])[lane])
~~~

matrices按列表0..末项执行，M节点只能读已完成事件；每次K32输出half，不能把16次折成一次512项实数和。输出stores按类别与gstore_off事件序号写16 B，负写地址跳过；类别写入依赖无效节点则拒绝。[scalar_map.hpp:293–314](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L293)。该式加投影DAG给出每输出的完整程序，索引表本身仍不闭式。

L56有5857节点、512矩阵事件，32条各16次K32的链；首seed为 `RN16(E4_to_half(residual)*scale)`，残差来自第二输入角色；full为这些half结果经Q8。pooled从最终half取四路a/b/c/d，顺序为 `Q8(RN16(RN16(RN16(a+b)+RN16(c+d))*0.25))`，0.25是算法常量half 0x3400，不能先把四路Q8再平均。各路的SI/PS选择及边缘类别直接由投影nodes、stores指定；12类别共78个发布事件记录。full写q2的1105920 B，pooled写q3的327680 B。它没有在CPU图之外独立证明“标准2×2”的原生坐标归属。

【CPU 重建／整数表实读】照着实现 L56 时，按 manifest 加载 L56 的 map、wiring 和发布形式的 contract（见[层索引资产](REPRODUCE.md#layer-assets)）。每个 pooled 字节由 thread_class、store 事件、lane 和字节号决定它读哪四个最终投影 half。用人工坐标 F[c,w,event,row,col] 标记矩阵输出，M(event,slot,lane) 对应 row=lane//4+8·(slot//2)、col=2·(lane%4)+slot%2；pooled 字节 0 依次取 F[0,0,450,0,0]、F[0,0,450,1,0]、F[0,0,450,4,0]、F[0,0,450,5,0]，先两两 half 相加，再合并、乘四分之一、Q8。1080 上 327,680 个 pooled 字节都恰好读四项、0 不一致。这四项在图像上的 (y,x,c) 位置没有独立标定，所以不能写成标准 2×2 平均池化；边界只按来源 −1（读零）和具体 class 处理，不默认 clamp、反射或裁掉最后一个窗口。[F04 核对](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)

L57有2625节点、256矩阵事件，16条各16次K32的链，首seed均[+0](APPENDIX_beginner_glossary.md#g070)；只有W/S/M/Q/K类型，没有G门、池化或残差。逻辑输入32×20×512 E4，输出32×20×1024 E4；512输入维对应16个K32，1024是输出通道数。四个16 B发布事件的每一字节由投影stores给出，不能由输出宽度反推K长度。源表、参数身份与上述节点数均从[既有绑定](examples/split16_window_r04d.bindings.json)重核；本轮保留所有来源状态。

<a id="evidence"></a>
## 我们怎么知道

| 对象 | 依据与支持范围（各一行） |
|---|---|
| 65次调用与旁路 | [CENSUS](APPENDIX_beginner_glossary.md#g100)：[front绑定](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json)、[tail绑定](../../../experiments/parity-cpp-bindings-tail-r01-20260928-codex/s00-bindings-tail.json)与 [本轮核对记录](examples/split16_window_r04d.bindings.json)的65份params实际SHA一致，16块角色接线相符 |
| 精度与核内顺序 | CENSUS：[FFN](L3_ffn.md#channels)、[norm图](L3_norm_nonfinite.md#map-norm)、[attention图](L3_attention_softmax.md#graph-bindings)及本轮26个资产SHA核对，支持具名CPU图；不证明任意输入/几何的地图语义 |
| 1080连续段 | MEASURED：[B25–B30旧结果](../../../experiments/parity-gemini-1080-chain-r03-20260922/RESULT_ZH.md#L3)覆盖L33–L57共25次及L56双出口/L57接线，只到B30，不越入ViT |
| 小尺寸块内门 | MEASURED：[B27–B29旧结果](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3)为两公开320×240/[reset](APPENDIX_beginner_glossary.md#g032)样本的48项单段/块内链比较，不是跨块连续链 |
| 后来整帧范围 | MEASURED：[M2记录](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)含1080/1440 f0全部65次；4K的[M2](APPENDIX_beginner_glossary.md#g107)新数值只到L99，不借配置普查宣称其解码已在M2新测 |
| qkv八字段地址/索引 | CLOSED_FORMULA，留出地图验证：[新研究结果](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md)；1080推导，640×360类/1440/4K及参考几何留出；不是新的数值门 |
| 仍未知 | 原16头bias独立排序、qkv的thread_class与其他家族未闭合字段、一般地图/同步/[别名](APPENDIX_beginner_glossary.md#g092)/生命周期与内部值唯一均未由出口相同建立；旧MAP_CHECK_FAILED保持具名范围 |

完整SHA、矩阵链核对和两张补图的来源在 [r04d证据附录](APPENDIX_evidence_history.md#split16-window-r04d)。[函数表](APPENDIX_beginner_glossary.md#g074)域与[非有限](APPENDIX_beginner_glossary.md#g069)边界继续沿用 [norm合同](L3_norm_nonfinite.md#nf-path)及具名M/A1状态，不由本页扩大支持。

桥接的四路通道归约见[L100算子](L2_06_decoder_bridge.md#operator)。
