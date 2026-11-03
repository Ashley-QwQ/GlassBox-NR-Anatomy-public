# L4.tex-filter：1/256定点小数格、联合8位分数权重与纹理half发布

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。

<a id="beginner-sampler-fields"></a>
[CB](APPENDIX_beginner_glossary.md#g083)+0x40是某次参数包内的字节位置（具体消费者可读资源[句柄](APPENDIX_beginner_glossary.md#g096)），1/256是过滤内部的坐标/权重刻度；两者不是同一名字，也没有这里给出的字段控制该刻度的关系。[取样](APPENDIX_beginner_glossary.md#g027)的新手图见[五点/四角嵌套](L1_00_history_primer.md#nested-sampling)。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · 上层：[B0五tap](L3_b0_input.md#five-tap) · 相邻：[half格式](L4_half_arith.md#format)、[F32边界](L4_fp32_ftz.md#sites)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

<a id="tex-filter"></a>
## 输入与逐次舍入

【CPU 重建】这是B0[历史](APPENDIX_beginner_glossary.md#g024)[RGBA16F](APPENDIX_beginner_glossary.md#g028)的有限颜色过滤模型。每次TEX先产生一个[half](APPENDIX_beginner_glossary.md#g054)，再精确展开为[F32](APPENDIX_beginner_glossary.md#g056)供[五tap](APPENDIX_beginner_glossary.md#g029)权重合并；它与最后的[RN16](APPENDIX_beginner_glossary.md#g059)是两个[发布](APPENDIX_beginner_glossary.md#g091)位置。W/H与边界合同由[调用](APPENDIX_beginner_glossary.md#g080)者给定。

局部记号：a,b为两轴1/256定点小数格上的整数，取值0..255；w₀…w₃为四角联合8位分数权重的整数分子，step为颜色截断格。采样器只接收纹理、尺寸、坐标与分量，不读取CB参数；全局格式见[INDEX](INDEX.md#形状与工作区记号)。

1. F32像素中心坐标夹到[0.5,W−0.5]；xq=floor(double(x)×256+0.5)−128，ix=xq//256、a=xq%256。y轴同理，邻居夹到最后一个有效纹素。
2. br=(a*b+128)/256，按整数除法取商（即非负整数的floor）；四角权重为[256−a−b+br,a−br,b−br,br]/256。先联合[量化](APPENDIX_beginner_glossary.md#g061)权重，不做四个独立高精度双线性乘积。
3. largest取非零权重纹素的最大绝对值；非全零时step=2^(floor(log₂(largest))−14)。
4. 各颜色先[trunc](APPENDIX_beginner_glossary.md#g060)(color/step)×step，再乘权重，按四角原序在binary64求和；不能把截断移到加权乘积之后。
5. 发布最近half，中点取离零较远者；单有效贡献为负零时保留[−0](APPENDIX_beginner_glossary.md#g070)。全零走零值路径，不用log(0)选格。

源代码：[native_temporal.hpp:10–25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L10)。其实现先调用普通half_round，再仅在恰好中点时按邻码校正，普通half RN-even不能代替这步。

<a id="worked-example"></a>
## 人工单点：截断、联合权重与中点

【真实代码实算】[脚本](examples/substitutions_r04g.py)直接抽取并执行tn_sample，输入全为人工纹素；[输出、源码/函数表SHA](examples/substitutions_r04g.result.json)可核对。

取2×2纹素TL/TR/BL/BR=[1,2⁻²⁰,−0.5,2]，采样点(0.5+73/256,0.5+119/256)。a=73、b=119、br=34，四角整数权重为[98,39,85,34]，和256。largest=2，step=2⁻¹³；TR被向零截成0，其余三值不变。加权和为(98−42.5+68)/256=0.482421875，真实TEX输出half **0x37b8**。

再取同一顶行TL=1、TR=1.125，点(0.5+1/256,0.5)。两项权重255/256与1/256，和为1+2⁻¹¹，恰在half中点。真实纹理发布为 **0x3c01**；普通RN-even给 **0x3c00**。这两个例子分别区分联合8位分数权重/共[指数](APPENDIX_beginner_glossary.md#g058)截断与末端中点规则。

【原生行为／验证范围】[texture-align机制与区分实验](../../../experiments/parity-b2-texture-align/TEXTURE_ARITHMETIC_ZH.md#可复核的-cpu-机制)记录具名设备/配置的有限颜色观察；后续[sm_120](APPENDIX_beginner_glossary.md#g078)前缀核对见[B0证据](L3_b0_input.md#evidence)。人工例不构成新GPU验收，不扩大到任意采样[描述符](APPENDIX_beginner_glossary.md#g088)或[非有限](APPENDIX_beginner_glossary.md#g069)纹素。
