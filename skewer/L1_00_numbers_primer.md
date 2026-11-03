# 有限数点与32项小篮

上一站：[两帧与重置](L1_00_history_primer.md) · 下一站：[L1.01图外前置](L1_01_prepare.md) · [回索引](INDEX.md)

可选下钻：[精确32项规则](L3_qmma_e4m3.md) · [数值词表](APPENDIX_beginner_glossary.md#g054)

机器保存的小数只能落在一些数点上。[F16](APPENDIX_beginner_glossary.md#g054)用16个二进制位、[E4M3](APPENDIX_beginner_glossary.md#g055)用8位保存一个数；都不是保留16或8位十进制小数。真实数点的间隔随数的大小变化，下面等距尺子只是**人工教学**。

~~~text
人工尺子：  −2  ·  −1.5  ·  −1  ·  −0.5  ·  0  ·  0.5  ·  1  ·  1.5  ·  2
待存的1.75：最近点在1.5与2中间；示意的偶末位选择2。
向零：1.75取1.5；−1.75取−1.5。向下取整会把负数推得更负，不能混用。
~~~

“最近偶数”先找最近的**可表示值**，只有正好中间才看[编码](APPENDIX_beginner_glossary.md#g057)[有效数](APPENDIX_beginner_glossary.md#g058)的最低位是否为0；不是把任何小数取成偶整数。真实F16例：1与1+2⁻¹⁰相邻，中点1+2⁻¹¹保存成1。[RZ](APPENDIX_beginner_glossary.md#g060)是向零，[RN16](APPENDIX_beginner_glossary.md#g059)/RN32/RN64是最近偶数到不同位宽。极小数可能被舍掉；某些操作还主动把[次正规](APPENDIX_beginner_glossary.md#g068)数冲成零，叫FTZ，不能一概套到所有位置。

<a id="baskets"></a>
## 一行乘一列，分两篮处理64对数

每对相乘后把乘积加起来叫[点积](APPENDIX_beginner_glossary.md#g051)。这里一篮处理32对，另带入一个已保存小计；第一篮可从0或指定[旁路](APPENDIX_beginner_glossary.md#g016)开始。

~~~mermaid
flowchart LR
    A["前32对乘积 + 起始小计"] --> G["分别朝零放到同一公共刻度"] --> S["在刻度上准确加32项与小计"] --> H["最近偶数保存F16小计"]
    H --> B["带入后32对的下一篮"] --> G2["重新选公共刻度、分别放置并相加"] --> H2["再保存F16"]
    H2 --> Q["若该出口要求：另转E4M3"]
~~~

“[公共刻度](APPENDIX_beginner_glossary.md#g066)”像统一的细尺子，让同篮的乘积与小计先落在同一格距上；放不下的尾部朝零截去。尺子由操作数编码中的指数和带入小计共同选取，具体选尺式见[专家规则](L4_e4m3_and_k32.md#qmma-k32-accumulation)。因此步末只保存一次F16，**不表示此前完全不丢精度**。它既不是每个乘积立刻转F16，也不是64对全部加完才转一次。

<a id="reuse-examples"></a>
| 沿用已有合成例，均非测量 | 看到了什么 |
|---|---|
| [A：1、2⁻¹¹、2⁻¹⁸](L4_e4m3_and_k32.md#worked-examples) | 三项在同一篮最终到1+2⁻¹⁰；前两项先存、第三项下一篮则到1。分篮改变舍入 |
| 同页B：256、−256、2⁻¹⁸ | 公共格距2⁻¹⁷把最后一项先截为0，和为0；不能先当实数[相消](APPENDIX_beginner_glossary.md#g071)再保留小尾巴 |
| 同页C：1+2⁻⁴+2⁻¹⁸ | 先存F16得到1.0625，再转E4M3得到1；直接转E4M3会得到1.125。两次转换不等于一次 |

<a id="three-cards"></a>
## 随身带三张检查卡

| 卡片 | 应问的问题 |
|---|---|
| 格式能表示什么 | 这个数是否有对应存储码？同一格式内数点也不均匀；[+0](APPENDIX_beginner_glossary.md#g070)/−0有不同编码 |
| 本操作怎样算 | 在哪里截公共格、舍入、冲零或转换？普通加乘、[融合乘加](APPENDIX_beginner_glossary.md#g063)、32项、16项和最终颜色各自有规则 |
| 当前实现允许什么 | 可表示不等于允许输入；[NaN](APPENDIX_beginner_glossary.md#g069)/Inf、上溢及其他守卫可拒绝，拒绝没有可记为匹配的输出 |

本页解释目标[sm_120](APPENDIX_beginner_glossary.md#g078)上这条E4的32项软件复现规则及已有有限域证据。它不证明设备内部一定放着篮子或尺子，不证明全部输入或未来设备，也不覆盖另外的16项步骤、[纹理](APPENDIX_beginner_glossary.md#g027)取样和最终颜色转换。[逐操作舍入表](L4_half_arith.md#beginner-rounding)保留这些差别，[完整边界](L3_qmma_e4m3.md#候选如何从-1832-收敛到一个行为类)继续有效。
