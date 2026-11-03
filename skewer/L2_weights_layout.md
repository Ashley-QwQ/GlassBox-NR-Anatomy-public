# L2 权重组织：153个打包条目与各阶段的字节账

[整串目录](INDEX.md) · [一帧与成本口径](L0_frame.md) · [B0](L2_02_b0.md) · [TIN](L2_03_tin_encoder.md) · [split16](L2_04_split16_encoder.md) · [ViT](L2_05_vit.md) · [解码桥](L2_06_decoder_bridge.md) · [B70](L2_09_b70.md)

本页横切各[调用](APPENDIX_beginner_glossary.md#g080)家族，只增加资产组织说明，不新增launch或覆盖归属。

<a id="resource"></a>
## 一个资源，三种形状口径

固定样本C只有一份weight-like PE[资源](APPENDIX_beginner_glossary.md#g079)WEIGHTS_HT，长147,695,410 B；资源表没有按preset/feature分开的第二份权重资源。这个结论不证明每次运行时上传都相同。[资源只读核查RESULT:9–22](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d2_followup/RESULT_ZH.md#L9)。

**153是序列化的打包条目数，不是153个普通稠密参数[矩阵](APPENDIX_beginner_glossary.md#g051)。** 发布提取器保留每条名称、形状元数据与载荷，把载荷存成一维U8；明确不猜稠密FP16形状或混合精度分段。[公开extract_dlssnr_weights.py:1–9、29–31、85–98](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/third_party/mlxdlss/tools/extract_dlssnr_weights.py#L1)。因此须区分：

- 资源记录的dimensions=[N]、dtypeCode=1以及byteCount=2N；这里只是序列化结构关系，不能据code=1把整条载荷认作普通[F16](APPENDIX_beginner_glossary.md#g054)矩阵。[make_weights.py:11–19、216–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/make_weights.py#L11)。
- 容器的U8[2N]保存相同载荷字节；一个条目可同时包含[E4](APPENDIX_beginner_glossary.md#g055)矩阵、F16[向量](APPENDIX_beginner_glossary.md#g076)/偏置、[F32](APPENDIX_beginner_glossary.md#g056)[尺度](APPENDIX_beginner_glossary.md#g031)和内部对齐。[make_weights.py:263–286](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/make_weights.py#L263)、[TIN typed loader:34–52](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34)。
- CPU算术看到的是[解码](APPENDIX_beginner_glossary.md#g057)后的矩阵/向量及其具体布局。E4可展开为F16参与重建，不能据展开后的类型把存储量乘二；也不能把打包的一维N当作网络[通道](APPENDIX_beginner_glossary.md#g007)数。[B0 loader:7–20](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L7)、[权重格式边界](L3_qmma_e4m3.md)。

本轮仅读取既有容器的8 B长度和32,528 B JSON头；**载荷读取0 B**。153条名称/维度/大小的白名单投影与整数汇总见[元数据回执](examples/r04k.weights_layout.json)，读取边界见[脚本:29–61](examples/weights_layout_r04k.py#L29)。未重核载荷[SHA](APPENDIX_beginner_glossary.md#g103)，数值身份沿用既有[五文件派生验收](../../../experiments/parity-cpp-v2-weights-derive-r01-20261021-claude/RESULT_ZH.md#L18)；未输出系数、逐条哈希或字节转储。

<a id="families"></a>
## 条目如何归到阶段与调用家族

名称规则为blockB.layerJ.layer，B70另有block70.layer0.blend_scale。B是[逻辑块](APPENDIX_beginner_glossary.md#g036)，J是该块的参数包序号；一个[TIN](APPENDIX_beginner_glossary.md#g011)包由同一次融合调用消费，多包的[split16](APPENDIX_beginner_glossary.md#g013)/[ViT](APPENDIX_beginner_glossary.md#g014)则分别供多个调用使用。对应的默认调用表见[L0](L0_frame.md)，实际取数仍以参数绑定及CPU[来源图](APPENDIX_beginner_glossary.md#g089)为准，名称本身不是原生布局证明。

| 阶段／块 | 条目组织与消费家族 | 算术矩阵和附属项的形状／dtype（[CPU重建](APPENDIX_beginner_glossary.md#g100)口径） |
|---|---|---|
| B0 | B0.J0一包，供L2输入融合核 | E4的32×128、128×32、32×96、32×32；另有F16的16×32适配、32通道[残差](APPENDIX_beginner_glossary.md#g017)尺度和64×64偏置，F32[查询尺度](APPENDIX_beginner_glossary.md#g052)加载后转half。[b00.hpp:7–20、46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L7) |
| TIN编码B1–B22／解码B48–B69 | 每块J0一包；[inpview](APPENDIX_beginner_glossary.md#g022)/chained/ds_wait/upsample/outview按阶段消费 | C=32的E4[前馈](APPENDIX_beginner_glossary.md#g037)32×128→128×32；C≥64的打包矩阵槽C×(4C+128)与C×C；另有[QKV](APPENDIX_beginner_glossary.md#g040) C×3C、输出投影C×C，上/[下采样](APPENDIX_beginner_glossary.md#g021)附加2C×C／C×2C。F16偏置为(C/32)×64×64、残差向量C，查询尺度F32[C/32]转half。内部前馈分组见[FFN变体](L3_ffn.md#channels)，不能把所有槽当作一个稠密层。[tin.cpp:34–52、119–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34) |
| split16编码B23–B30／解码B40–B47 | 每块J0 ffwd、J1 ffwd_proj、J2融合qkv/[attention](APPENDIX_beginner_glossary.md#g039)、J3 proj；B30另有J4 final_head | 主干512通道：前投影512×512、八组64×256与256×64、后投影512×512；QKV[逻辑](APPENDIX_beginner_glossary.md#g085)512×1536、16×64×64 F16偏置、16个F32查询尺度；J1/J3另含F16[512]残差尺度。B30.J4逻辑512→1024。E4矩阵与F16发布位置分开，[split16完整块](L3_split16_window.md#order)、[FFN形状](L3_ffn.md#channels)、[norm尺度](L3_norm_nonfinite.md#affine)。 |
| ViT B31–B38 | 每块五包：J0 expand、J1 contract、J2 qkv_projection、J3 attention、J4 projection | E4矩阵1024×4096、4096×1024、1024×3072、1024×1024；J1/J4的F16[1024]残差尺度、J2的F32[32]查询尺度，J3仅F16[1] attention_scalar（序列化条目为U8[2]；所查公开 attention 路径不把它作为算术输入，见下文）。逻辑形状与dtype注记见[weight_spec.json](../../../mlxdlss/weight_spec.json)，实际算术/图绑定见[ViT步骤](L2_05_vit.md)。 |
| B39 | J0，供L100解码桥 | E4逻辑1024×512投影和F16[512] [skip](APPENDIX_beginner_glossary.md#g016)融合尺度；四路256通道[部分和](APPENDIX_beginner_glossary.md#g050)的顺序与实际权重索引由图确定。[entry.cpp:54–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L54)、[桥接图](L2_06_decoder_bridge.md#operator)。 |
| B70 | J0主包＋独立blend_scale，供L155；L156/L157不另增加本资源条目 | E4的32×128、128×32、32×96、32×32，F16的两份16×4末端头、32通道合并/残差向量和64×64偏置；F32查询尺度加载后转half，另有F16[1] blend_scale。[outtail.cpp:85–97](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L85)。 |

split16与ViT的逻辑shape注记不替代完整物理轴、bias顺序或任意地图[准入](APPENDIX_beginner_glossary.md#g101)；仍保留各主题的[UNKNOWN](APPENDIX_beginner_glossary.md#g104)边界。上表矩阵形状不是[L0](APPENDIX_beginner_glossary.md#g081)成本表中“已知矩阵槽小计”以外的全网[GMAC](APPENDIX_beginner_glossary.md#g077)补算。

<a id="stage-bytes"></a>
## 从记录形状推得每阶段字节数

以下N均为资源dimensions=[N]的元素数。记A(N)=512×ceil(2N/512)，则每条[payload](APPENDIX_beginner_glossary.md#g097)为2N B、上传槽为A(N) B；公式按全部153条元数据计算，不读载荷。分组明细见[脚本:14–19、45–78](examples/weights_layout_r04k.py#L14)和[完整元数据](examples/r04k.weights_layout.json)。

| 阶段 | 条目数 | ΣN的形状公式 | payload B（2ΣN） | 512 B槽合计 |
|---|---:|---|---:|---:|
| B0 | 1 | 10848 | 21,696 | 22,016 |
| TIN编码 | 22 | 3×10336+11360+3×30880+34968+5×98592+114968+7×344616+410144 | 7,200,720 | 7,208,960 |
| split16编码 | 33 | 8×262144+16×131584+8×458784+262152 | 16,269,840 | 16,273,920 |
| ViT | 40 | 8×(2097160+2098176+1572928+1+525312) | 100,697,232 | 100,708,352 |
| B39桥 | 1 | 262656 | 525,312 | 525,312 |
| split16解码 | 32 | 8×262144+16×131584+8×458784 | 15,745,536 | 15,749,120 |
| TIN解码 | 22 | 410392+7×344616+115088+5×98592+35024+3×30880+11392+3×10336 | 7,201,632 | 7,209,472 |
| B70 | 2 | 10904+1 | 21,810 | 22,528 |
| 合计 | 153 | 73,841,889 | 147,683,778 | **147,719,680** |

ΣA(N)=147,719,680 B，其中槽间/尾部补齐共35,902 B；原始资源147,695,410 B另含11,632 B记录框架。**阶段槽合计是按条目归属求和，不声称每个阶段在原始资源里必然是一个连续区间。** 读取的容器头按名字排序，也不能由它反推资源原顺序。

<a id="layouts"></a>
## 512 B上传布局与其他容器

device_weights.bin按资源出现顺序拼接，每条payload后补到512 B倍数，最后一条也补齐；这正是147,719,680 B布局。[make_weights.py:245–252](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/make_weights.py#L245)。weights-device.bin与weights_gpu.bin按名称排序、每条前对齐且不补最后尾部，长度147,719,232 B；两者与device_weights.bin布局不同，不能只凭总量接到同一指针。原资源weights.bin和U8容器又是不同格式。[make_weights.py:21–31、255–261](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/make_weights.py#L21)，[五文件派生RESULT:8–22](../../../experiments/parity-cpp-v2-weights-derive-r01-20261021-claude/RESULT_ZH.md#L8)。

<a id="scales"></a>
## 尺度因子在哪些节点起作用

这里仅说明位置与类型，不列任何系数值。FFN与attention的逐通道F16尺度先乘旁路，再作为矩阵[seed](APPENDIX_beginner_glossary.md#g042)或有序合并的输入；不能挪成最后一次高精度相加。[残差接口](L3_ffn.md#residual)。TIN上采样的sin向量作用在skip合并，B39的向量也用于skip融合，B70的sin/cos向量作用于解码[特征](APPENDIX_beginner_glossary.md#g008)与B0特征合并；这些名称不表示调用三角函数。[tin.cpp:151–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L151)、[entry.cpp:71](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L71)、[outtail.cpp:86–90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L86)。

查询尺度为每头的F32资源字段，按具体图/loader转到half并作用于[归一化](APPENDIX_beginner_glossary.md#g043)后的Q；K的对应归一化不新增同样的学习尺度。[TIN loader:50、norm:114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L50)、[split16/ViT的图约束](L3_norm_nonfinite.md#affine)。ViT attention_scalar是参数清单里的命名项：B31–B38 的 attention 参数指向各自条目，但在所查公开 runtime 与保存的 attention 图里，找不到它到分数[仿射](APPENDIX_beginner_glossary.md#g049)的消费边；分数仿射的 slope/addend 是图内常量，可追溯的来源是内核里的 F32 字面量常量转 half，没有证据表明它们由 attention_scalar 折叠而来，实现时不要再乘这个标量（[F06 追踪](../../../experiments/anatomy-f06-attention-scalar-r01-20261031-codex/RESULT_ZH.md)，8/8 块一致；专有训练/导出历史不在此结论内）。blend_scale属于B70[时域](APPENDIX_beginner_glossary.md#g024)置信混合；两者都不是通用输出gain。[ViT分数](L3_attention_softmax.md#attention-softmax)、[B70混合](L3_b70_history_output.md#b70-temporal)。

[宿主](APPENDIX_beginner_glossary.md#g096)[CB](APPENDIX_beginner_glossary.md#g083)中的gain、[intensity](APPENDIX_beginner_glossary.md#g004)、帧与控制量，以及认证噪声/[MUFU](APPENDIX_beginner_glossary.md#g073)函数资产，分别属于参数或函数资产；它们不因此变成第154个权重条目。[输入与宿主控制](L3_b0_input.md#channels)、[显示](L3_b70_history_output.md#postprocess)、[CPU资产附录](APPENDIX_cpu_storage.md)。
