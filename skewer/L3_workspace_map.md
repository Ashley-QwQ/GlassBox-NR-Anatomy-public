# L3.workspace-map：工作区、padding 零写与双向 repack

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-storage"></a>
【人工存放示意】同一组(a,b,c,d)，可按两行(a,b)/(c,d)放，也可在存储中按(a,c,b,d)放；[重排](APPENDIX_beginner_glossary.md#g019)只换盒子，解读后仍是原来的四个数。实际规则不是随便选一种排列，需按本实例[合同](APPENDIX_beginner_glossary.md#g101)。读图时分三格：“从哪取数→做什么算术→往哪写数”。

~~~text
逻辑有效格：  ■ ■     实际分配格： ■ ■
              ■ ■                 ■ ■
                                  □ □  额外补齐格
~~~

□可能真被写零、被后面读取，不能自动当垃圾；内部[补齐](APPENDIX_beginner_glossary.md#g085)也不等于显示图变大。[工作区](APPENDIX_beginner_glossary.md#g082)同时放中间数和管理标记，旧字节的最小跨帧必需集合仍[未定](L1_00_history_primer.md#workspace-memory)。新手先读[角色](APPENDIX_beginner_glossary.md#g084)与重排含义，下面的地址表、写集、零覆盖及[完成标记](APPENDIX_beginner_glossary.md#g091)是专家核对层。
<!-- beginner-r04m:end intro -->

[整串目录](INDEX.md) · 上层：[准备](L2_01_prepare.md)、[split16](L2_04_split16_encoder.md)、[ViT](L2_05_vit.md)、[桥接](L2_06_decoder_bridge.md) · 已展开算术：[矩阵乘](L3_qmma_e4m3.md)、[attention](L3_attention_softmax.md)、[B0 双出口](L3_b0_input.md#publish)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| Span(role) | 角色相对本次工作区基址的字节区间 |
| [WriteSet](APPENDIX_beginner_glossary.md#g093)(L)、CumWrites(L) | 单[调用](APPENDIX_beginner_glossary.md#g080)声明写集、[累计声明写集](APPENDIX_beginner_glossary.md#g105)；检查协议见附录 |
| Read_ws、I_decl | 实际有来源证据的读取集、声明输入角色区间 |
| π、chunk | repack的12位置换、4字节搬运单位 |

<a id="workspace-map"></a>
<a id="regions"></a>
### L3.workspace-map.regions 按角色与时点绑定的工作区（L0–L157）

- 是什么：一块跨调用接续的字节分配，容纳数值[张量](APPENDIX_beginner_glossary.md#g076)、同步标记、补齐及复用区间。
- 输入 → 输出：本帧配置的 b、N、[params](APPENDIX_beginner_glossary.md#g083) 和角色[描述符](APPENDIX_beginner_glossary.md#g088) → Span(role)；同一偏移在不同调用可以承担不同角色。
- 怎么算：
  ~~~text
  1. N(G)=已登记 allocation 的字节数；b 取同实例 L1 的 CB+0x00 (u64)。
  2. o(role,L)=params 中该角色指针−b+描述符内偏移。
  3. n(role,G)=该角色物理元素数×每元素字节数，或其显式副作用长度。
  4. Span(role,L)=[o,o+n)；要求 0≤o≤N 且 0≤n≤N−o。
  5. 角色数据按本次布局读取；同一逻辑形状不保证通道在内存中连续。
  6. 各角色之并给出声明的输入 / 输出区间；跨时点不能把角色长度直接相加作 N。
  7. N≥max(o+n)；是否恰等于并集长度，要另查累计覆盖。
  ~~~
- 数值规则：这些是字节地址与长度运算，没有[浮点](APPENDIX_beginner_glossary.md#g056)舍入；工作区里的数值仍按其原语格式解释。容量由固定几何分配记录[绑定](APPENDIX_beginner_glossary.md#g103)，当前源码没有给出任意 W,H 的[宿主](APPENDIX_beginner_glossary.md#g096) allocator [闭式](APPENDIX_beginner_glossary.md#g020)；不能用固定 B/像素拟合 N。
- 为什么这么算：让不同阶段复用缓冲，并在同一分配中交接数据与完成[状态](APPENDIX_beginner_glossary.md#g091)；全局最优复用策略未独立重建。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)，[entry.cpp:41–48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L41)、[geometry.hpp:35–50](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/geometry.hpp#L35)；三档来源 / 公式见 [FIXED_GEOMETRY:36–53](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/FIXED_GEOMETRY_ZH.md#m-g004workspace-pointeroffset-与跨度)及[native_launch_facts.json](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json)。
- 往下：[几何及角色大小](#geometry)、[L1](#clear)、[读写与 CumWrites(L)](#write-sets)、[地址表](#address-maps)、[副作用](#release)。

<a id="geometry"></a>
### L3.workspace-map.geometry 三档容量与物理 extent 的公式

- 是什么：把图像尺寸、各层空间补齐与序列补齐分开，按实际角色缩放。
- 输入 → 输出：已准入的 Wn,Hn 及各角色参数 → 空间张量字节数、T/P、各档固定分配 N。
- 怎么算：
  ~~~text
  1. (W0,H0)=(Wn,Hn)；两轴各用 n_(r+1)=4×ceil(n_r/8) 逐级减半并补齐。
  2. T=W6×H6；P=32×ceil(T/32)。
  3. 空间 E4 角色的字节数=Wr×Hr×C；F16 再乘 2。
  4. B0.full=32WnHn；B0.pool=32(Wn/2)(Hn/2)。
  5. ViT 的一份 1024 通道物理角色=1024P；扩张角色=4096P。
  6. repack 逻辑搬运=1024T；L58 的额外零写=1024(P−T)。
  7. 角色起点仍取 params 指针；容量 N 按下表登记值，而非以上大小的简单总和。
  ~~~
- 数值规则：空间有效高、物理高和序列 P 是不同边界；上述 extent 递推沿用本语料的已准入几何，不声称是任意图像的宿主分配公式。
- 为什么这么算：各阶段按自己的分块粒度组织存储；多个对齐粒度使 N 不与 WH 保持固定比例。
- 我们怎么知道：CENSUS / INFERRED，[INDEX 的形状链](INDEX.md#形状与工作区记号)、[B0 源码:63](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L63)、[repack.cpp:81–84、137–150](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L137)；容量来自 [GEO RESULT:11](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/RESULT_ZH.md#L11)。
- 往下：[逻辑行 / padding](#padding)、[repack](#repack)。

| 实例 | W×H | Wn×Hn | H6×W6；T / P | N（B） | B0 [full](APPENDIX_beginner_glossary.md#g018) / pool（B） | [ViT](APPENDIX_beginner_glossary.md#g014) 一份物理 1024 [通道](APPENDIX_beginner_glossary.md#g007)角色（B） |
|---|---|---|---|---:|---|---:|
| 1080 | 1920×1080 | 1920×1152 | 20×32；640 / 640 | 212,519,936 | 70,778,880 / 17,694,720 | 655,360 |
| 1440 | 2560×1440 | 2560×1472 | 24×40；960 / 960 | 340,722,688 | 120,586,240 / 30,146,560 | 983,040 |
| 4K | 3840×2160 | 3840×2176 | 36×60；2160 / 2176 | 763,062,272 | 267,386,880 / 66,846,720 | 2,228,224 |

以 1080 的 L62 为具体布局：CB+0x00 ([u64](APPENDIX_beginner_glossary.md#g057)) / CB+0x08 (u64) / CB+0x10 (u64) / CB+0x18 (u64) 分别绑定 Q / K / V / output；相对 b 的偏移分别为 181,718,016 / 183,028,736 / 182,373,376 / 183,684,096，每份 655,360 B。按地址顺序却是 **Q→V→K→output**，不能按参数排列猜连续内存顺序。三档都按同一 Span(role) 公式读取各自指针，不能给 1440 / 4K 套 1080 偏移。[ARCH 0.7 §2.4](../../../ARCHITECTURE_V3_ZH.md#24-workspace-布局)。

<a id="clear"></a>
### L3.workspace-map.clear L1 的固定实例 footprint

- 是什么：初始化工作区前缀中的控制区；“clear”在这里写 0xFF。
- 输入 → 输出：L1 的 16 B params → WS 起始连续区间置 0xFF，其余字节保留。
- 怎么算：
  ~~~text
  1. 要求 params 恰为两个 qword。
  2. b=CB+0x00 (u64)；count=U32(CB+0x08 (u64))；n=4×count。
  3. 对 i=0..count−1：在 b+4i 写四个 0xFF 字节。
  4. WriteSet(1)=[0,n)，Read_ws(1)=∅。
  5. 登记此写范围；n 之外不作整片清零。
  ~~~
- 数值规则：每个 32 位槽为 0xffffffff；按有符号整数解释是 −1，不是浮点数 −1。00 / A5 初态在该前缀都被覆盖成 FF，前缀之外仍保留各自初值。
- 为什么这么算：该调用重置控制前缀；具体完成标记消费者另按release合同绑定，不把所有控制槽视为同一用途。
- 我们怎么知道：CENSUS，[entry.cpp:48、80–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L80)；count 直接重读三档 [native params 普查](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json)。
- 往下：[累计写集](#write-sets)、[完成标记](#release)。

| 实例 | count | 4×count（B） | L2.full 的起始偏移 |
|---|---:|---:|---:|
| 1080 | 97,024 | 388,096 | 388,096 |
| 1440 | 147,712 | 590,848 | 590,848 |
| 4K | 330,240 | 1,320,960 | 1,320,960 |

<!-- beginner-r04m:start expert-write-sets -->
> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。
<!-- beginner-r04m:end expert-write-sets -->

<a id="write-sets"></a>
## 声明写集与实际读取

WriteSet(L)是本调用声明写入的区间并；CumWrites(L)是累计声明写集。实际字节变化只能给出写入下界，同值零写仍属于写入；角色跨度也不等于每字节实际读取。[合并、摘要与比较规则](APPENDIX_evidence_history.md#workspace-checker-sets)见附录。

| 调用 | 读来源与声明范围 | 工作区写角色 |
|---|---|---|
| [L0](APPENDIX_beginner_glossary.md#g081) | 当前颜色[纹理](APPENDIX_beginner_glossary.md#g027)；本路径不读 WS | ∅；输出在纹理 id10 |
| L1 | params；Read_ws=∅ | 控制前缀 |
| L2 | 当前颜色、有效时的 [MV](APPENDIX_beginner_glossary.md#g023) / history、[权重](APPENDIX_beginner_glossary.md#g079)及[函数表](APPENDIX_beginner_glossary.md#g074)；本路径不读 WS | full、pool |
| L58 | 1024T B 的逻辑二维输入 | 逻辑 output 加独立 padding 零写角色 |
| L61 等 [QKV](APPENDIX_beginner_glossary.md#g040) | 声明 input；实际数值地址由本实例 [maps](APPENDIX_beginner_glossary.md#g089) / DAG 决定 | Q、K、V，以及两个 release 区 |
| L62 等 [attention](APPENDIX_beginner_glossary.md#g039) | 声明 Q/K/V；来源图需保留动态 [epoch](APPENDIX_beginner_glossary.md#g092) | 物理 output、尾部覆零、release63 |
| L63 等 projection | attention output、[residual](APPENDIX_beginner_glossary.md#g017)、权重；已证明读取 L62 的全部 16 KiB padding | output、两个 release 区 |
| L99 | 逻辑 1024T B 的序列输入 | 逻辑二维 output；不复制 P−T 行 |
| L155–L157 | 具体 WS / 纹理来源按尾部角色绑定 | 此规范中的 WriteSet=∅；分别写纹理 id9、id6、id2 |

最后一列的角色不是完整的全网生命周期证明；非 qkv [split16](APPENDIX_beginner_glossary.md#g013)、桥接及 [TIN](APPENDIX_beginner_glossary.md#g011) 的读集只能按其具名 map / 实例给出，不能填成统一的“卷积邻域”。每个 launch 的 WriteSet 来自冻结记录，完整参数 / 别名 / consumer / release 证明仍另有缺口。

<a id="fill"></a>
双填充检查的数目、初态与补集规则见[00/A5协议](APPENDIX_evidence_history.md#workspace-checker-fill)；它是具名输入的证伪检查，不是任意初值独立性定理。

<!-- beginner-r04m:start expert-padding -->
> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。
<!-- beginner-r04m:end expert-padding -->

<a id="padding"></a>
### L3.workspace-map.padding T 与 P、L58 零区和 L62 显式覆盖

- 是什么：补齐行是物理角色的一部分；有些必须在普通计算写回之后再次覆零。
- 输入 → 输出：4K 的 T=2160、P=2176 → 16×1024=16,384 B 的 padding 写语义。
- 怎么算：
  ~~~text
  1. L58 拷贝逻辑 1024T B，并对独立的 1024(P−T) B 角色真正写零。
  2. 后续物理行可以参与计算，不能假定 L58 的零会一直保留。
  3. L62 先把 computed 向量写入物理 output，包括那 16 行。
  4. 读取本实例的零写绑定，核 params、输出角色、零值、4 B 宽度和执行阶段。
  5. 在普通输出之后、release 之前，4096 个零写覆盖相对 output [2211840,2228224)。
  6. 零写覆盖恰一次且 release 区不重叠；最后才发布完成状态。
  7. T=P 的 1080 / 1440 路径没有这组尾部清理。
  ~~~
- 数值规则：[E4](APPENDIX_beginner_glossary.md#g055) 的 0x00 为 [+0](APPENDIX_beginner_glossary.md#g070)，但这里的合同首先是逐字节覆零；不能用“初态是零”或“这些行不算逻辑 [token](APPENDIX_beginner_glossary.md#g041)”省略写入。L58 的补齐与 L62 的覆零是两个不同生产时点；二者长度碰巧相同，不表示可以共用一个存在性判断。
- 为什么这么算：物理分块会产生额外结果，而下游仍按物理布局读入，因此需要明确的无效行值与完成次序。
- 我们怎么知道：CENSUS，[repack.cpp:130–174](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L130)、[发布适配器:95–102、166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166)；MEASURED / 诊断，[diag-L062 RESULT:5–17](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/diag-L062/RESULT_ZH.md#L5)。
- 往下：[缺陷与负控](#padding-bug)、[repack 的 padding 地址](#repack)、[attention 数值顺序](L3_attention_softmax.md#vit-score)。

<a id="padding-bug"></a>
### L3.workspace-map.padding-bug 零覆盖的最终合同与旧诊断

【CPU 重建】普通输出之后、release 之前必须执行绑定的 typed 零写；L63 的 readset 实际消费该区，不能称无用 padding。原生前后快照同为零仍不能区分未写与同值覆零；与输出重叠的零写不新增 W/CumWrites 字节，元数据覆盖不能代替值与时序验证。错实例、参数、地址、值、宽度、epoch、阶段，漏写/重复写/提前 release 都必须被检查。

[漏项根因、区间、负控与旧构建续接记录](APPENDIX_evidence_history.md#padding-bug)移至附录。旧诊断 [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) 保留，诊断轮下游 NOT_RUN 不因后来具名门改写；旧构建结果不转移给合流 seal。全局[副作用](APPENDIX_beginner_glossary.md#g094)/别名/生命周期定理仍未建立，当前绑定见 [适配器](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177)。

<a id="repack"></a>
### L3.workspace-map.repack M2 的 4 B chunk 闭式（L58 / L99）

- 是什么：同一组逻辑 token 在二维 4×4 分块与序列分块之间搬运位型。
- 输入 → 输出：H6×W6×1024 B，rows=H6、cols=W6 → 同样的逻辑字节；L58 另发布 padding。
- 怎么算：
  ~~~text
  1. 每 token 切成 256 个 chunk；g=token×256+c，c=0..255。
  2. row=token//cols；col=token%cols。
  3. tile=(row//4)×ceil(cols/4)+col//4；slot=4(row%4)+col%4。
  4. π 将输入位 0..11 分别移到 [2,3,1,7,8,9,10,11,4,5,6,0]。
  5. tiled_chunk=(tile<<12) | π((slot<<8)|c)。
  6. raster_chunk=((token//16)<<12) | π(((token%16)<<8)|c)。
  7. 两个 chunk 地址均乘 4 才是字节偏移。
  8. L58：out[4×raster_chunk: +4]=in[4×tiled_chunk: +4]。
  9. L99：方向反过来；只搬逻辑 T 行。
  10. L58 额外 g∈[256T,256P) 按 raster_chunk 定位，各写一个四字节零。
  ~~~
- 数值规则：π 是整数位索引的置换，不改变 [payload](APPENDIX_beginner_glossary.md#g097) 的位，不[解码](APPENDIX_beginner_glossary.md#g061) E4，也没有加乘舍入。一块含 16×256=4096 个 chunk，即 16 KiB。逻辑 raster 布局内部仍有 π，不能把 raster_chunk 当 token×256+c。
- 为什么这么算：在空间[窗口](APPENDIX_beginner_glossary.md#g015)核与全局序列核之间转换访问组织；闭式实现只是换地址，不改变网络算术。
- 我们怎么知道：CENSUS，[repack.cpp:26–50、83–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26)，padding 的有界、唯一及完整覆盖检查见 [:141–165](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L141)。
- 往下：[接受域](#repack-domain)、[保存验证的分母](#repack-evidence)、[实际索引例](#worked-example)。

<a id="repack-diagram"></a>
#### L58 / L99置换图与一个4×4空间tile

图中地址均相对各自角色起点；c=0,…,255是每token的4 B chunk编号，π为上面的12位闭式。1080的rows=20、cols=32、T=P=640，两边各655,360 B逻辑数据。

~~~mermaid
flowchart LR
    XY["逻辑token t：row=t//cols，col=t%cols"] --> TILE["空间tile/slot：tile=(row//4)×ceil(cols/4)+col//4；s=4(row%4)+col%4"]
    XY --> SEQ["序列group/slot：g=t//16；u=t%16"]
    TILE --> A["二维字节地址：4×(4096 tile + π(256s+c))"]
    SEQ --> B["序列字节地址：4×(4096 g + π(256u+c))"]
    A -->|"L58：按同一(t,c)复制4 B"| B
    B -->|"L99：反方向复制4 B"| A
~~~

下面画的是1080左上角**一个空间[tile](APPENDIX_beginner_glossary.md#g087)**。每格为“局部slot s / 全图token t”，t=32row+col；一格含1024 B、256个chunk，整tile为16 KiB。它展示逻辑归属，格内的物理字节仍经π交错。

~~~text
               local col
             0         1         2         3
        +---------+---------+---------+---------+
row  0  | s0/t0   | s1/t1   | s2/t2   | s3/t3   |
        +---------+---------+---------+---------+
     1  | s4/t32  | s5/t33  | s6/t34  | s7/t35  |
        +---------+---------+---------+---------+
     2  | s8/t64  | s9/t65  | s10/t66 | s11/t67 |
        +---------+---------+---------+---------+
     3  | s12/t96 | s13/t97 | s14/t98 | s15/t99 |
        +---------+---------+---------+---------+
~~~

序列group0容纳t=0…15，按全图token号分组；空间tile0的下一行则从t=32开始。例如t=32、c=0位于空间slot4，π(4×256)=64，因此二维偏移为256 B；序列group2/slot0的偏移为32,768 B。L58复制这一4 B，L99按同一逻辑(t,c)搬回。π仅置换地址位，payload无浮点运算。

4K额外的P−T行仍按 [padding合同](#padding)单列：L58写零，L99只搬逻辑T行；不能把补齐角色画成一对双向有效token。图和整数例来自 [repack.cpp:26–50、88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26)，[完整身份](APPENDIX_evidence_history.md#split16-window-r04d)留在附录。

<a id="repack-domain"></a>
### L3.workspace-map.repack-domain 数学索引域与资源守卫

- 是什么：闭式只接受满足分块和安全长度合同的维度。
- 输入 → 输出：rows、cols、params、输入长度及工作区角色指针 → 双射映射或异常拒绝。
- 怎么算：
  ~~~text
  1. rows>0、cols>0，rows×cols≤1,000,000。
  2. rows%4==0 且 cols%4==0。
  3. 拒绝 (rows==4) xor (cols==4)；4×4 允许，单边为 4 的长条不允许。
  4. rows<16384、cols<65536；只接受 launch 58 或 99、24 B params。
  5. 输入长度必须等于 rows×cols×1024 B；角色指针与完整跨度在工作区内。
  6. 对全部逻辑 chunk 检查源 / 目标不越界、各自唯一；失败就拒绝。
  7. L58 还要求 grid.x=P，并逐项核对额外零写恰覆盖 padding。
  ~~~
- 数值规则：三个实际 token 网格 20×32、24×40、36×60 均在域内。守卫可接受的更大尺寸没有因此获得硬件穷举证据；错误输入不静默裁切，也不对索引取模。
- 为什么这么算：维度条件维持分块双射并限制索引容量；单边为 4 的拒绝继承了旧实现的非双射边界。
- 我们怎么知道：CENSUS，[repack.cpp:53–63、77–95、113–151](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L53)；[M2 RESULT §3](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#3-repack-支持域回答-b1-要求)。
- 往下：[验证范围](#repack-evidence)、[索引例](#worked-example)。

<a id="repack-evidence"></a>
## repack 的证据类型

【验证记录】具名三档三帧双向格有原生字节对照；旧/新模块维度扫描还包含拒绝结果，不是全部有效硬件形状。部分位置仅观察到零，不能称所有位置都被非零内容唯一钉死。数学接受域、软件等价域和硬件观测域分别保留；双射检查也不等于硬件遍历完整域。[原计数、钉住率、结果文件及范围](APPENDIX_evidence_history.md#repack-evidence)移至附录。

<!-- beginner-r04m:start expert-address-maps -->
> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。
<!-- beginner-r04m:end expert-address-maps -->

<a id="address-maps"></a>
### L3.workspace-map.maps 数据驱动地址表怎样执行

- 是什么：以有符号整数偏移表连接字节来源、算术 DAG 和写回位置，表中没有[激活](APPENDIX_beginner_glossary.md#g045)预测值。
- 输入 → 输出：本实例绑定的 maps、wiring、输入角色字节和权重切片 → 算术原语的操作数及写地址。
- 怎么算：
  ~~~text
  1. 按描述符顺序拼接输入角色，得到 executor 的 inp 字节空间；权重另作 weight 空间。
  2. wload_off[A,Y,32,S_w] 给权重加载的基础字节偏移；节点还可加固定字节选择。
  3. sread_src[A,Y,32,S_s,B] 把一次共享来源事件的各字节连到 inp 偏移。
  4. xsite_src[A,Y,32,S_x,J] 与 xsite_wsrc 同形，逐字节选择输入 / 权重 / 常量零来源。
  5. 按 DAG 规定的阶段和 half / QMMA 原语算值；地址表不替代算术顺序。
  6. gstore_off[A,Y,32,S_g] 给输出基础偏移，当前 split16 每个有效事件写 16 B。
  7. 检查每个有效写跨度在角色内，并逐字节检查所有权不冲突、覆盖无洞。
  8. 按 outputs 列表切分返回字节，分别回写各参数指针；另执行 release 等副作用。
  ~~~
- 数值规则：数组为连续的本机端序有符号整数，可用 i8/i16/i32/i64；类型宽度不是数值[特征](APPENDIX_beginner_glossary.md#g008)精度。偏移相对 executor 的输入 / 输出 / 权重切片，不都是绝对 WS 偏移。[sread](APPENDIX_beginner_glossary.md#g090) 的 −1 为常量零，xsite 的 −3 配合权重偏移选择 weight；其他负哨兵按节点 / 类别分别处理，不能全当零。
- 为什么这么算：已采且绑定的来源图能保留复杂搬运和分支，而部分家族尚没有独立确认的闭式；在语义未知处执行图比根据核名猜布局更可检验。
- 我们怎么知道：CENSUS，[scalar_map.hpp:166–189、244–259](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L244)、[输出所有权:319–338](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L319)、[split16.cpp:56–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L56)；桥接的另一套 A_src / OUTMAP 结构见 [entry.cpp:56–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L56)。
- 往下：[三档实际 shape](#map-shapes)、[矩阵算术](L3_qmma_e4m3.md#qmma-e4m3)、[norm 图](L3_norm_nonfinite.md#map-norm)、[release](#release)。

地址表支持的事实是“这个绑定的事件从哪些字节取操作数、写哪些字节”，不单独证明“这是 3×3 卷积”或“这个执行轴就是网络通道”。同样，maps 存在、数组 shape 合法或输出字节匹配，不自动证明全部生产者 / 消费者、动态 epoch、别名和异步同步正确。repack及[split16 qkv八字段](L3_split16_window.md#qkv-closed-form-r04n)已得到闭式；后者只在留出地图表验证地址相等，thread_class继续表驱动，不代表其他家族也已闭式化。更换几何、窗口位移、输入角色顺序或 epoch 身份仍必须重新绑定，生产执行器也仍读取原表。

~~~mermaid
flowchart LR
    K["执行点(a,y,lane)：A/Y调度轴；lane=0..31；S为事件轴"] --> SR["sread_src[a,y,lane,s,b]"]
    I["按角色拼接的inp字节空间"] --> SR
    I --> XS["xsite_src / xsite_wsrc：输入、权重或零"]
    W["权重字节空间"] --> WL["wload_off[a,y,lane,s] + 节点字节选择"]
    K --> WL
    SR --> DAG["算术DAG：K32→half节点/归约→Q8"]
    XS --> DAG
    WL --> DAG
    DAG --> GS["gstore_off[a,y,lane,s]：每有效事件16 B"]
    GS --> O["outputs按长度切分→各CB指针的角色"]
~~~

16头×8×8窗是逻辑注意力域，(A,Y,32,S)是搬运执行坐标；两者经具名来源图连接，不能把Y直接当头数或把32直接当通道数。L100用另一套A_src/B_off及REDMAP/OUTMAP，见[桥接图](L2_06_decoder_bridge.md#wiring)。

<a id="map-shapes"></a>
### L3.workspace-map.map-shapes 用三档 L57 看真实数组轴

- 是什么：shape 描述执行任务与事件数；不能给所有家族套一个随 WH 线性缩放的数组模板。
- 输入 → 输出：同属 L57 的三份实际 NPZ 头及原生 grid → 下列各数组的形状。
- 怎么算：
  ~~~text
  1. L57 的外层 A=grid.x×grid.y×grid.z：三档为 48、60、160。
  2. 该实例 Y=8、lane 轴=32；S_w=64、S_s=32、B=16、S_g=4。
  3. wload_off 的 shape=(A,8,32,64)。
  4. sread_src 的 shape=(A,8,32,32,16)；gstore_off=(A,8,32,4)。
  5. xsite_src 与 xsite_wsrc 均=(A,8,32,0,4)：该实例没有这类事件。
  6. 每数组字节数=itemsize×各轴乘积；此处保存格式全部为小端 i64。
  7. 换一个家族重新取轴：1080 的 L25 为 A=80、Y=4、S_w=128、S_s=64、S_g=8。
  ~~~
- 数值规则：空事件轴表示零项，不是缺失资产。A/Y 是执行维度，不能把 48 当 token 数或把 8 当 attention 头数。前面通用的 i8/i16/i32/i64 接口接受能力，也不代表这些实际文件都使用最窄整数。
- 为什么这么算：不同家族有不同向量搬运与分片组织，固定宽度的物理操作数需要这些离散事件轴。
- 我们怎么知道：CENSUS，本轮读取三份 NPZ 的 NPY 头；[1080 L57](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c6/products/S1/L057/control1080/L57-map.npz)、[1440 L57](../../../../b1-relocated-10600t/dlssnr-geo2-l24-r01-20261008-codex/runtime1440-stage-L057-binding-v2/split-work/bundle/L57-map.npz)、[4K L57](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c6/products/S1/L057/high2160/L57-map.npz)；grid 来自 [native_launch_facts](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json)，1440 文件重算 SHA 与 [configure-L057.json](../../../../b1-relocated-10600t/dlssnr-geo2-l24-r01-20261008-codex/runtime1440-stage-L057-binding-v2/configure-L057.json) 的资产 pin 相同。
- 往下：[不同家族的 shape](#other-maps)、[WR](#wr)。

| 字段 | 1080 | 1440 | 4K |
|---|---|---|---|
| wload_off | (48,8,32,64) | (60,8,32,64) | (160,8,32,64) |
| sread_src | (48,8,32,32,16) | (60,8,32,32,16) | (160,8,32,32,16) |
| gstore_off | (48,8,32,4) | (60,8,32,4) | (160,8,32,4) |
| xsite_src / xsite_wsrc | (48,8,32,0,4) | (60,8,32,0,4) | (160,8,32,0,4) |

1440 地图的 [完整 SHA](APPENDIX_evidence_history.md#map-identity)移至附录；该外部本地副本是几何绑定的历史来源，不能仅凭路径名认定它就是全部 [M2](APPENDIX_beginner_glossary.md#g107) 部署资产。

<a id="other-maps"></a>
ViT 扩张使用另一套 axis 次序：src 与 weight_offsets 为 (A,4,16,8,32)，store_offsets 为 (A,4,8,32)，见 [ffn_expand-resume2.cpp:205–229](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L205)。其他 ViT 家族用按实例 / epoch 连接的来源图，不能把这里的 L57 字段直接改名套入。1080 L25 的实际头也与 L57 不同：[L25-map.npz](../../../../dlssnr-cpp-work/chain-split16-r01-codex/bundle/L25-map.npz)中的 wload=(80,4,32,128)、sread=(80,4,32,64,16)、gstore=(80,4,32,8)。

<a id="partial-sums-r04l"></a>
## QKV与projection部分和（排名38、46–47、94–95）

QKV将1024个K输入分成z=0、1两个512段；每段16次[K32](APPENDIX_beginner_glossary.md#g065)，首[seed](APPENDIX_beginner_glossary.md#g042)为+0、其后继承前次[half](APPENDIX_beginner_glossary.md#g054)。z0把24个16 B事件的half[部分和](APPENDIX_beginner_glossary.md#g050)写buffer（要求每字节恰一次）；z1先做 `H=RN16(buffer+p1)`，再做Q/K归约、[RSQ](APPENDIX_beginner_glossary.md#g072)、尺度和[Q8](APPENDIX_beginner_glossary.md#g061)，V同样从合并的H量化。它没有z1/z2的原地半精度规约阶段。[QKV/projection叶与seed:129–150](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L129)、[矩阵取seed:213–223](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L213)。

projection按z=0..3各算256个K（每段8次K32）：z0首seed=`RN16(E4_to_half(residual)*scale)`，先于第一K32加入；z1/z2/z3首seed均+0。每个K32都发布half，不能把残差挪到全部[点积](APPENDIX_beginner_glossary.md#g051)之后。令四段结果为p0..p3，buffer先存p0，z1写 `b1=RN16(p0+p1)`，z2写 `b2=RN16(b1+p2)`，z3最终 `Q8(RN16(b2+p3))`。z1/z2每两字节读旧half再h_add，[非有限](APPENDIX_beginner_glossary.md#g069)拒绝；要求buffer先写、只初写一次，两个规约恰各一次，最终输出逐字节恰一次。源码的reverse_red仅为改变顺序的反控，不是默认顺序。[执行:227–239](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L227)、[z序与覆盖:271–294](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L271)。

每个字节/half取哪个事件仍由具名DAG与map选择；本节给全数值合并次序，未把这些索引改判为闭式。[具名程序绑定](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/cpp-integrate-layer2-r01-20261009-codex/candidate/runtime/vit-bindings.json)的原型标签继续保留MAP_CHECK_FAILED；后来的实例裁决不能倒改它。

<!-- beginner-r04m:start expert-release-contract-r04l -->
> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。
<!-- beginner-r04m:end expert-release-contract-r04l -->

<a id="release-contract-r04l"></a>
## 各族发布区与空集合（排名11起）

下表qN指CB+8N的u64角色指针；所有写入先验证 `ptr≥workspace_base`、`offset≤workspace_bytes`、`len≤workspace_bytes−offset`。数值输出先完成，再写发布区。空集合指没有该族的额外清零。

| 家族/实例 | 角色qword；长度；值；空集合 |
|---|---|
| split16 F16/F17/F19/F20/F21/F22 | q6；1080默认320 B，即80个LE32(0)；例外见下一行 |
| split16 attention F18 | L27+4j(j=0..7)、L103+4j(j=0..7)：q6、640 B，即160个LE32(0) |
| split16 finalhead F23 L57 | releases=[]，无memset |
| 专用entry F34 L132 | 无memset：只把map执行结果写q2；不能继承一般split16的q6规则 |
| TIN | L3–5、L151–153用q7；L7–9、L11–15、L17–23、L133–139、L141–145、L147–149用q8；长4GXGY B，LE32(0)；L6/10/16/24/140/146/150/154为[] |
| ViT expand F25/F30 | q7；4grid.x B，LE32(0)；当前实例均非空 |
| ViT contract F26 | release60=q4、release61=q7；各4grid.x B；按z=0..3遍历模板发布记录，前者每槽0→1→2→3，后者最终0 |
| ViT QKV F27 | release61=q5、release62=q8；各4grid.x B；终值1、0 |
| ViT attention F28 | release63=q6；长度取epoch[0].release63_size，所有epoch必须相同；全字节0。1080为640 B，不能套QKV双区长度 |
| ViT projection F29/F31 | release63=q4、release64=q7；各4grid.x B；终值3、0 |
| L100 F33 | ctr=q4、ctr2=q5；按counter_writes中的每个相对偏移写4 B，终值3、0；不是无差别清整段 |
| copy/repack/B0/B70/S157 | 无此额外release memset；L1另按[初始化合同](#clear)写FF |

split16 的47个320 B调用为L25、26、28、29、30、32、33、34、36、37、38、40、41、42、44、45、46、48、49、50、52、53、54、56、101、102、104、105、106、108、109、110、112、113、114、116、117、118、120、121、122、124、125、126、128、129、130。64份现绑定的安全投影（仅launch/grid/release）和源SHA见[逐调用表](examples/r04l.release_bindings.json)；第65个L132由专用entry解释。一般executor逐条 `(qword,len)` 执行 `memset(span(qword,len),0,len)`，不从输出长度猜release长度。[split16.cpp:79–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L79)，[L132:93–94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L93)，[TIN:179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L179)、[44份TIN绑定](examples/tin_window_r04c.bindings.json)。

expand槽索引为 `32*(x%Q)+x//Q`，0≤x<grid.x=32Q，是稠密置换；四个物理模板不能把长度乘4。要求release_bytes=4*release_ctas、release_ctas=nc，活tile数≤4nc。[expand:256–258](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L256)。contract记录为 `(z,region,offset,value,count)`，z∈[0,3]、offset四字节对齐且offset+4≤对应长度，count=32表示同槽参与者数，不是连续写32个槽；按z升序、记录原序写LE32(value)。每个release60槽必须出现4次、release61槽1次，否则拒绝。[contract:348–360](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L348)、[写入:518–534](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L518)。

attention先检查所有epoch输出和发布长度一致；数值覆盖与padding覆零完成后，才按输出列表发布release63。[attention:288–333](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L288)，[padding顺序:177–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177)。ViT角色qword取现[具名绑定](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/cpp-integrate-layer2-r01-20261009-codex/candidate/runtime/vit-bindings.json)，不改变旧原型状态。

L100用键 `role+offset` 选择q4或q5；值列表排序后必须严格等于[0,1,2,3]或[0]，重复/缺少也拒绝。仅在合法四字节槽发布终态，保留其余字节。[entry.cpp:73–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L73)。

TIN中 `CW=W−2ox,CH=H−2oy`（C32），其他C取 `CW=8*ceil((W−ox)/8),CH=8*ceil((H−oy)/8)`；GX=CW/8、GY=CH/8。第(bx,by)个CTA对应LE32槽 `by*GX+bx`，所以发布长恰为4GXGY，releaseword<0时空集合。[tin.cpp:143–155、179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L143)。

<a id="release"></a>
### L3.workspace-map.release 数值出口以外的完成标记

- 是什么：完成标记也是输出副作用；丢掉它们会使完整 WS 合同与 consumer 接线不完整。
- 输入 → 输出：QKV / projection 操作类型与 native grid.x → 每个发布区的 U32 状态槽，再回写各自 Span(role)。
- 怎么算：
  ~~~text
  1. 每个发布区有 grid.x 个四字节槽，长度=4×grid.x。
  2. QKV：release61 每槽写 U32(1)，release62 每槽写 U32(0)。
  3. projection：release63 每槽写 U32(3)，release64 每槽写 U32(0)。
  4. 两区总副作用长度均为 8×本操作 grid.x。
  5. 本语料 Q=ceil(T/128)，QKV grid.x=16Q，projection grid.x=8Q。
  6. 所以 QKV 额外写 128Q B，projection 额外写 64Q B。
  7. 发布适配器把这些区与主要数值出口一同登记；不得从数值 tensor 的长度中省略。
  ~~~
- 数值规则：状态为小端 U32 整数，不是 F16 / E4。640 B 是 1080 的 QKV **两个**发布区总长；不是每个区 640 B，也不是 projection 同样 640 B。逻辑 T、物理 P 与 release 字节数分别绑定，1440 的 QKV 总长 1024 B 不等于 T=960。
- 为什么这么算：通知后续工作单元结果可消费，并初始化下一阶段状态；CPU 顺序返回这些字节不自动重建 [GPU](APPENDIX_beginner_glossary.md#g078) 的完整中间等待时序。
- 我们怎么知道：CENSUS，[release_resume1.cpp:9–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_release_resume1/release_resume1.cpp#L9)、[适配器:228–234](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L228)及[三档 native grid](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json)；公式只归纳这些具名几何。
- 往下：[WR A/B](#wr)、[读写域证据边界](../../arch-v2/08.02_read_write.md#v2-08-005)。

| 实例 | Q | QKV grid.x；每区 / 两区（B） | projection grid.x；每区 / 两区（B） |
|---|---:|---|---|
| 1080 | 5 | 80；320 / 640 | 40；160 / 320 |
| 1440 | 8 | 128；512 / 1024 | 64；256 / 512 |
| 4K | 17 | 272；1088 / 2176 | 136；544 / 1088 |

<!-- beginner-r04m:start expert-wr -->
> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。
<!-- beginner-r04m:end expert-wr -->

<a id="wr"></a>
声明稳定、原生可见变化、CPU范围外不变是三项不同检查；[WR判定与缺观测规则](APPENDIX_evidence_history.md#workspace-checker-wr)见附录。

<a id="evidence"></a>
## 具名数值门与保留边界

- [M2 RESULT §6](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#6-数值门与配置普查)：1080 / 1440 f0 以及 4K L0–L99 是实际数值门；M2 的 4K L100–L157 只有配置普查。repack 与零写所在段的通过不扩成整个接受域证明。
- [统一 M 的 4K 三帧 RESULT:19–32、61–63](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19)：两填充各单进程 f0→f1→f2，948 个调用有独立回执；946 个已观察 FULL、2 个 f0 L0 NOT_OBSERVED。A5 补集语义、B(i) 缺口、形式 checker / [computed-shared](APPENDIX_beginner_glossary.md#g108) 未准入边界保留。
- 老诊断、旧独立构建、合流 M 与发布 M2 是不同身份。输出轨迹匹配不证明全局 ROLE 生命周期、所有动态来源、异步硬件时序或任意几何的通用正确性。

<a id="worked-example"></a>
## 实际索引例：row=5、col=7、chunk=37

本轮执行下面的小脚本：从当前 M2 源码读取 π 的常量，计算三档索引，并在保存的旧模块标号输出中只读对应四字节，分别核对 L58 与 L99 的方向；这些文件是地址标签，不是权重或原生数值目标。末段从已读元数据复算上文的容量 / CumWrites(2) 数目，不运行模型、GPU 或整链。

[完整验证脚本](APPENDIX_evidence_history.md#workspace-example-code)见附录；本页保留实际索引结果。


实际结果：

| rows×cols | token | tile / slot | π((slot<<8)\|37) | tiled / raster chunk | 源 / 目标字节偏移（L58） |
|---|---:|---|---:|---|---|
| 20×32 | 167 | 9 / 7 | 630 | 37494 / 41590 | 149976 → 166360 |
| 24×40 | 207 | 11 / 7 | 630 | 45686 / 49783 | 182744 → 199132 |
| 36×60 | 307 | 16 / 7 | 630 | 66166 / 78390 | 264664 → 313560 |

六次标号读取全部符合公式；L99 使用反向偏移。每次复制完整四字节，payload 的四个字节不重排。三档的 slot 相同，tile / token 及序列位置不同，正说明地址必须绑定 cols；不能把某个几何的完整偏移表当成全几何闭式。

### π的逐位代入

真实repack.cpp的swizzle将源bit0..11送到[2,3,1,7,8,9,10,11,4,5,6,0]。0x725=0b011100100101的置位集合{0,2,5,8,9,10}依次送到{2,1,9,4,5,6}，所以输出为2²+2¹+2⁹+2⁴+2⁵+2⁶=0x276=630，即0b001001110110。[真实函数实算](examples/anatomy_r04i.py)及[结果](examples/anatomy_r04i.result.json)同时验证这一步，未读网络值。
