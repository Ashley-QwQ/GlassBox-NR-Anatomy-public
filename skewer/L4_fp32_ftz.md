# L4.fp32-ftz：F32边界、FTZ与显式舍入

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · 上层：[B0重投影](L3_b0_input.md#coordinates)、[attention](L3_attention_softmax.md#window-attention)、[norm](L3_norm_nonfinite.md#affine)、[B70 / L157](L3_b70_history_output.md#postprocess) · 相邻原语：[half算术](L4_half_arith.md#f32-boundaries)、[MUFU](L4_mufu.md#edges)、[E4 / K32](L4_e4m3_and_k32.md#e4m3-format)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

<a id="fp32-ftz"></a>
## 本页覆盖什么

- 是什么：默认158次[调用](APPENDIX_beginner_glossary.md#g080)链中实际出现的[binary32](APPENDIX_beginner_glossary.md#g056)计算、格式载体和[发布](APPENDIX_beginner_glossary.md#g091)边界；F32不是全网统一的累加精度。
- 输入 → 输出：[half](APPENDIX_beginner_glossary.md#g054)展开值、参数/[资源](APPENDIX_beginner_glossary.md#g079)F32或认证[函数表](APPENDIX_beginner_glossary.md#g074)[位型](APPENDIX_beginner_glossary.md#g057)→逐站点F32操作→F16 [RN-even](APPENDIX_beginner_glossary.md#g059)、尾段[RZ16](APPENDIX_beginner_glossary.md#g060)，或继续保留F32；[E4](APPENDIX_beginner_glossary.md#g055)另由half按RN-even/[satfinite](APPENDIX_beginner_glossary.md#g062)发布。
- 怎么算：先查 [站点表](#sites) 的起止格式，再按 [FTZ表](#ftz-paths) 判断输入/输出[冲零](APPENDIX_beginner_glossary.md#g068)、保留或拒绝，最后执行指定转换；不能只给整个进程设一个统一FTZ模式。
- 数值规则：分开的F32乘/加各自RN32，显式[FMA](APPENDIX_beginner_glossary.md#g063)才融合；FTZ、RZ、half RN-even、[纹理](APPENDIX_beginner_glossary.md#g027)half中点远离零及E4 satfinite是不同合同。
- 为什么：坐标、函数参数和显示颜色保留自己的辅助精度；[矩阵](APPENDIX_beginner_glossary.md#g051)/[范数](APPENDIX_beginner_glossary.md#g043)仍按其低精度接口发布。选择这些精度与融合边界的训练或硬件动机未知。
- 我们怎么知道：当前CPU源码、保存的具名硬件/软件记录与本轮真实C++小例分别标注；源码存在、旧门通过和通用硬件语义不互相升级。
- 往下：本主题已到底；[转换格式](#formats)、[站点](#sites)、[FTZ](#ftz-paths)、[可移植实现/编译](#portable)、[真实转换例](#worked-example)、[证据范围](#evidence)。

<a id="formats"></a>
源码函数名fa/fm/ff及tn_add/tn_mul/tn_div/tn_fma是实现标识；本文数学接口统一写F32+、F32×、F32/、F32_FMA，不改变这些函数的算术或接受域。

## 三种次正规数与四种发布不能混用

F32[编码](APPENDIX_beginner_glossary.md#g057)由符号、8位[指数](APPENDIX_beginner_glossary.md#g058)、23位尾数组成。指数为0且尾数非零才是F32次正规，幅值为m·2⁻¹⁴⁹；最小正规数为2⁻¹²⁶。F16最小次正规为2⁻²⁴，展开为F32后是**F32正规数**；E4的次正规数又有自己的指数/尾数定义。[格式来源](L4_half_arith.md#format)、[E4格式](L4_e4m3_and_k32.md#e4m3-format)。

| 记号 / 转换 | 准确含义 |
|---|---|
| RN32、RN16 | 最近偶数分别发布为binary32、binary16；F32精确扩宽为binary64后再RN16，不多出一次数值舍入 |
| RZ16 | F32向零发布half；尾段先调用真实half_round，再在RN结果的幅值超过输入时向零退一个half编码 |
| FTZ | 某个F32操作的次正规输入/极小输出按其合同变成[有符号零](APPENDIX_beginner_glossary.md#g070)；不等于格式转换的RZ |
| [Q8](APPENDIX_beginner_glossary.md#g061) / satfinite | half→E4，RN-even并有限饱和；不替代前一F32/half操作的域检查或[NaN](APPENDIX_beginner_glossary.md#g069)拒绝 |
| sat / 纹理half发布 | sat夹到[0,1]并按当前尾部代码规范零；纹理过滤half为中点远离零，二者都不是E4 satfinite |

[位置偏置](APPENDIX_beginner_glossary.md#g052)直接作为half矩阵[seed](APPENDIX_beginner_glossary.md#g042)，大多数[残差](APPENDIX_beginner_glossary.md#g017)[尺度](APPENDIX_beginner_glossary.md#g031)也按half消费；查询尺度在资源中为F32，先RN16再用于half乘法。这里的Q/K路径没有额外的加性β；坐标偏移和显示控制中的F32加数按各自站点处理。不列模型系数值；参数中的[宿主](APPENDIX_beginner_glossary.md#g096)F32控制也只按具名布局读取，不把某次捕获值写成通用算法常量。

<a id="sites"></a>
## 全链F32站点：操作、起止与舍入

表内“起/止”描述数值接口；认证表可以保存F32位型而不在运行时重新求数学函数。空间布局与完整网络接线沿所链L3阅读。

| 站点 | 操作 / F32累加 | F32从哪里开始 | F32在哪里结束、如何转出 | 当前源码 / 下钻 |
|---|---|---|---|---|
| B0噪声 | 预组合半径/三角表返回值相乘，三个独立RN32乘积 | 认证表的raw32按F32解释 | 三个乘积分别RN16成输入[特征](APPENDIX_beginner_glossary.md#g008)；适配/后续E4是另外的发布 | [noise_online:12、23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L12)、[B0噪声](L3_b0_input.md#noise) |
| 噪声的原组合函数 | k·2⁻²⁴、[LG2](APPENDIX_beginner_glossary.md#g072)后乘ln2和−2、[SQRT](APPENDIX_beginner_glossary.md#g073)；角度缩放及三角参数归约含RZ到F32 | 整数键与算法常量构成F32参数 | 当前在线表已含这些步骤；不得在查表后再次归约；最终乘积才RN16 | [组合函数合同](L4_mufu.md#representation)、[噪声数据流:24–27](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/noise_dataflow_ZH.md#L24) |
| B0 [MV](APPENDIX_beginner_glossary.md#g023)/坐标/融合边界 | 宽高倒数、MV融合、floor前FMA、余数与坐标[clamp](APPENDIX_beginner_glossary.md#g049)；加/乘/除各RN32 | half MV精确展开；参数F32与整数坐标转F32 | 坐标转采样定点格，不在每个坐标节点转half | [native_temporal:5–8、28–43](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L5)、[坐标](L3_b0_input.md#coordinates) |
| B0[五tap](APPENDIX_beginner_glossary.md#g029)合并 | value为F32加权累加；[分母](APPENDIX_beginner_glossary.md#g048)为固定次序F32加法，倒数在本实现用F32除法 | 每个过滤后的half展开为F32；权重为坐标F32结果 | 归一化value RN16后才减0.5、half乘gain；gain自身也先RN16 | [native_temporal:44–48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L44)、[五tap](L3_b0_input.md#five-tap) |
| B0 / B70采样器边界 | F32坐标→定点权重；CPU以binary64转写过滤量化，不是F32纹理[累加器](APPENDIX_beginner_glossary.md#g064) | 像素中心F32坐标、half纹素 | 过滤结果按纹理half中点远离零发布，再精确展开为F32；支持域按采样合同 | [native_temporal:10–25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L10)、[B70采样:10–23](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L10) |
| B0 / [TIN](APPENDIX_beginner_glossary.md#g011)分数仿射 | 先F32乘、再F32加，各RN32，保持不融合 | [QK](APPENDIX_beginner_glossary.md#g077)矩阵返回的half分数精确展开 | RN16后执行half clamp与编码变换；之后分母树为half | [b00:48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L48)、[tin:108–109](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108)、[attention](L3_attention_softmax.md#window-attention) |
| B70分数仿射 | fm后fa，两个独立F32发布；二者使用尾部FTZ辅助函数 | half QK分数展开 | half_round RN16，之后half分数/分母路径 | [outtail:91–92](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L91) |
| B0 / TIN / B70查询尺度 | 资源F32尺度转换，无F32平方和或F32残差累加 | 四字节模型资源值 | 先RN16，再作half归一化尺度乘法，最后E4 | [b00:18](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L18)、[TIN尺度](L3_norm_nonfinite.md#affine)、[outtail:85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L85) |
| [split16](APPENDIX_beginner_glossary.md#g013) / entry图尺度与函数值 | 四字节资源尺度、RSQ/RCP表输出以F32位型传递 | 图拼出的raw32或F32表项；范数输入仍是half统计量 | 显式rne16 / rne16w处RN16；其后half运算与Q8；表索引不是通用F32求函数 | [scalar_map:252、272–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L252)、[entry_map:270–272](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp#L270) |
| [ViT](APPENDIX_beginner_glossary.md#g014) [QKV](APPENDIX_beginner_glossary.md#g040)归一化辅助 | half统计量精确转F32，验证能回转到原half后查RSQ；资源查询尺度也有F32→half接口 | half展开或原始F32尺度字节 | f16of处RN16并查非有限；Q/K后续乘法与归约不变成F32 | [qkv:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192)、[norm尺度](L3_norm_nonfinite.md#affine) |
| ViT [attention](APPENDIX_beginner_glossary.md#g039)辅助 | half→F32→RCP表；图内F32乘常量，当前包装拒绝非有限及非零次正规乘法结果 | half分母或F32表值 | f16of处RN16且非有限拒绝，再按图进入half/E4；没有F32 AV总累加器 | [attention:206–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L206) |
| B70[重投影](APPENDIX_beginner_glossary.md#g025)/[历史](APPENDIX_beginner_glossary.md#g024) | 参数变换、融合floor/clamp边界、五tap F32加权累加、F32分母；使用fm/ff/fa及RCP | 参数F32、half MV/采样结果展开 | 历史合并仍留F32，交最终RZ16；采样器half发布是前一独立边界 | [b70_temporal:27–49](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L27)、[B70历史](L3_b70_history_output.md#b70-temporal) |
| B70输出/置信混合 | half头结果转F32，当前色编码、EX2/RCP置信因子及历史差值FMA | half预测头、当前颜色half、参数F32；confidence资源为half后展开 | blended RGB用RZ16写id9；[alpha](APPENDIX_beginner_glossary.md#g026)直接half(1)，L156只复制位型 | [outtail:95–97](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L95)、[置信混合](L3_b70_history_output.md#b70-mix) |
| L157曲线/显示混合 | 曝光、三次曲线、LG2/EX2往返、与[基底](APPENDIX_beginner_glossary.md#g003)的差及显式FMA；全为尾部F32 | id9/id10 half RGB展开及[params](APPENDIX_beginner_glossary.md#g083) F32 | 中间不插half；最终clamp后RZ16写id2，alpha直接half(1) | [outtail:71、74–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L71)、[曲线/强度](L3_b70_history_output.md#post-curve) |
| L157 [HSL](APPENDIX_beginner_glossary.md#g033)型调整 | max/min、亮度/色相/饱和度、RCP、分段重组与第二次[通道](APPENDIX_beginner_glossary.md#g007)次序；fm/fa/ff保留原边界 | 曲线出口的F32 RGB | 继续F32交最终显示混合；不把两次分解之间或每个分量先转half | [outtail:72–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L72)、[HSL链](L3_b70_history_output.md#post-hsl) |
| 尾部MUFU参数与[codec](APPENDIX_beginner_glossary.md#g097) | RCP输入/输出指数处理，LG2/EX2认证映射与整数重建；LG2负和重建含向零截取及等级修正 | 上述F32参数或原始raw32 | 返回F32位型；只有调用图要求时才RN16/RZ16；整数codec不增加一个浮点累加器 | [outtail:53–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)、[lg2_decoder:17–35](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/lg2_decoder.hpp#L17)、[MUFU边界](L4_mufu.md#edges) |

B0/TIN配置期的half函数表已包含相应F32表值→RN16，运行时可能直接取half；不能据后者声称没有原F32辅助接口。split16的分数仿射是half FMA，不能并入B0/TIN的两步F32仿射。[具体差异](L3_attention_softmax.md#window-attention)。

**F32累加的实际位置**是B0/B70的历史加权值及其分母等辅助链。[QMMA](APPENDIX_beginner_glossary.md#g065)矩阵逐K32的反馈为F16，norm平方和、[窗口](APPENDIX_beginner_glossary.md#g015)分母、ViT同址部分和也依各自half树/顺序发布；不能换成F32 GEMM/求和后一次转half。软件helper使用binary64承载half参考或用整数承载矩阵规则，不等于网络有F32累加器。[矩阵合同](L3_qmma_e4m3.md#qmma-e4m3)、[half有序合并](L4_half_arith.md#atomic-add)。

<a id="ftz-paths"></a>
## FTZ按路径裁决，不按数据类型统一开关

| 路径 | 输入次正规 | 输出次正规 / 极小结果 | 证据与限定 |
|---|---|---|---|
| 尾部fm / ff / fa，含B70和L157 | 按F32指数位显式清成同号零；ff处理三个输入，fa代理ff(a,1,b) | fm按精确乘积、ff按融合和及低部残差判断舍入前tiny，零保留符号；当前非零结果幅值小于2⁻¹²⁰仍先拒绝 | [outtail:31–43](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L31)；“实现了判定”不等于该极小域已获调用准入 |
| 尾部sat | 不是独立FTZ[算子](APPENDIX_beginner_glossary.md#g035)；按调用者先完成F32运算 | 当前a≤0返回+0，a>1返回1，NaN拒绝；负零规范化与FTZ保留零符号分开 | [outtail:44](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L44) |
| B0 tn_add/tn_mul/tn_div/tn_fma | 当前CPU辅助函数没有统一按位FTZ分支 | 按显式float发布/融合执行；任意tiny参数域与硬件等价未建立，不把它命名为完整FTZ实现 | [native_temporal:5–8](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L5)；已测坐标/输入范围见 [B0证据](L3_b0_input.md#evidence) |
| B0噪声、B0/TIN分数辅助 | 有限half分数展开后是F32正规或零；噪声按合法键组合 | 保存证明排除该噪声域非零F32次正规乘积；有限half分数的固定仿射也不需要F32次正规表示；仍可在转half时[下溢](APPENDIX_beginner_glossary.md#g071) | [噪声范围](L3_b0_input.md#noise)、[TIN原式:108–109](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108)；不外推任意F32输入 |
| ViT attention的F32乘法包装 | 按具名图的half/表来源及域检查，不由函数名补成通用输入FTZ | 非零F32次正规结果直接拒绝，不能把拒绝写成“返回零并匹配” | [attention:221–228](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L221) |
| MUFU的已测FTZ包装 | RCP/RSQ/SQRT/LG2/EX2的具名探针将同号次正规按零处理；三角组合另含预缩放约定 | 各函数保持自己的raw32映射；RCP的大正规输入可生成冲零结果，不能只处理输入FTZ | [MUFU特殊值表](L4_mufu.md#edges)、[旧RCP输出修正:271–285](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L271) |
| 非FTZ MUFU包装 / half小表 | 以包装[身份](APPENDIX_beginner_glossary.md#g103)和已采域为准；非FTZ版本可能是复合函数 | 不用另一包装的结果替代；旧RSQ表与RCP表的生成包装也不同，具体调用按绑定 | [旧表包装:208–213](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L208)、[norm合同](L3_norm_nonfinite.md#affine) |
| F16 / E4发布、位型搬运 | half/E4次正规保留自己的格式语义；F16有限值展开不产生F32次正规 | RN16/RZ16可产生half次正规；E4按其量化格；copy/[repack](APPENDIX_beginner_glossary.md#g019)不计算浮点 | [真实例](#worked-example)、[half格式](L4_half_arith.md#format)、[repack](L3_workspace_map.md#repack) |

### 极小性在舍入前判断

令m=2⁻¹²⁶。人工输入a=m、b=1−2⁻²⁴时，精确积m(1−2⁻²⁴)小于m，却恰在向m舍入的中点。若先RN32再只检查结果是否次正规，会保留m；按舍入前tiny应得到零。保存的饱和F32融合乘加站点抽样5120例中，这种机制出现两例，支持该站点的舍入前判定；不证明所有非零加数、所有操作或硬件版本。[原抽样范围](../../../experiments/b1-ftz-tininess-check-r01-20261012-claude/RESULT_ZH.md#L1)。

当前代码的乘积在binary64中精确，融合和用[TwoSum](APPENDIX_beginner_glossary.md#g098)保存高/低部；高部恰为±m时还看低部方向，避免仅用已舍入F32结果判断。原2⁻¹²⁰守卫仍在，所以上述小例调用完整fm/ff会拒绝；本轮实际核对了这一点。历史修复草案的单元证据、当时未合入/未做launch门的状态继续留在 [原报告](../../../experiments/parity-cpp-defect-fix-newseal-r01-20261012-codex/RESULT_ZH.md#L1)，本页以当前已读源码为对象，不把该旧草案状态移给全部后来封存。

<a id="portable"></a>
## CPU怎样复现，哪些环境前提仍在

1. **显式位处理。** 输入FTZ检查F32指数域并只保留符号位；MUFU通过认证raw32/整数codec取得指定输出；half_round按二幂格、余数和偶尾数软件发布，RZ再按幅值退格。它们不靠开启宿主FTZ/DAZ得到结果。
2. **保持发布点。** B0的加/乘/除和噪声乘法用volatile float保留RN32边界；TIN原分数式保留两个float中间值。volatile只约束这些发布，不自行提供FTZ或任意精度的正确性证明。
3. **指定融合，禁止额外融合。** B0坐标和五tap、尾部ff用显式std::fma(float,float,float)；独立乘/加继续独立，fa通过ff(a,1,b)实现加法。half std::fma的binary64→F16两阶段属 [另一合同](L4_half_arith.md#rounding)。
4. **严格编译与环境。** 记录的GCC/Clang配方为-O2、-fno-fast-math、-ffp-contract=off；MSVC为/fp:strict及相应严格配方。[plan_format:25–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/plan_format.py#L25)。TIN unary生成器还检查FE_TONEAREST、4 B/8 B的IEEE float/double并拒绝fast-math，[unary_tables:5–6、29–33](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/unary_tables_optb2.inc#L29)。禁止重结合、隐式收缩或把表值换成libm。
5. **守卫与未知照留。** 当前尾部极小结果、非有限/溢出、ViT辅助乘法和函数表域各有独立拒绝条件。普通宿主float运算仍以IEEE最近偶数语义为前提；移植时需维持应保留路径的渐进下溢，不能让外部FTZ/DAZ破坏它们，也不能宣称任意全局标志下、任意B0 tiny参数都已等价。正确做法是按位处理或在已证正常范围执行/拒绝，不以修改全局控制字替代算子合同。

本轮没有改编译配置或任何全局舍入/FTZ/DAZ标志。上面的严格配方是源码/已有身份合同；本轮小例的实际编译器、参数与源SHA另列在 [result JSON](examples/fp32_ftz_r04e.result.json)，不把本机编译成功当成所有CPU/编译器移植已验收。

<a id="worked-example"></a>
## 真实C++边界：half次正规中点，RN与RZ不同

[可运行脚本](examples/fp32_ftz_r04e.py)逐字抽取当前outtail的rz、ftz及其原half_value/half_round等纯[标量](APPENDIX_beginner_glossary.md#g076)函数，编译后实际运行；没有导入网络、读取模型/网络输入/目标或运行[GPU](APPENDIX_beginner_glossary.md#g078)。辅助命名空间仅提供同一位拷贝接口；函数体保留原样，完整身份和stdout见 [运行记录](examples/fp32_ftz_r04e.result.json)。

中心输入raw32=0x33c00000，即3·2⁻²⁵，是**F32正规数**，恰在两个half次正规值2⁻²⁴与2⁻²³的中点。RN16取偶编码0x0002；真实rz先得到这个RN结果，发现幅值超过输入，再退为0x0001。RZ的结果仍是half次正规，并未被F32 FTZ清除。

| 人工F32编码 | 原half_round RN16 | 原rz RZ16 | RZ输出小端字节 |
|---|---|---|---|
| 33800000（2⁻²⁴） | 0001 | 0001 | 01 00 |
| 33c00000（3·2⁻²⁵） | 0002 | 0001 | 01 00 |
| b3c00000（−3·2⁻²⁵） | 8002 | 8001 | 01 80 |

负例只测试纯转换函数；实际显示RGB还有[0,1]夹取，不能由此补认负RGB的网络路径。同一小程序还核对F32最小正/负次正规经真实ftz得到+0/−0，以及上面tiny例被完整fm/ff守卫拒绝。它只检查这些人工接口，未做新的RZ全raw32硬件门或图像链。

<a id="evidence"></a>
## 证据与适用域

| 对象 | 依据及界限（各一行） |
|---|---|
| 当前F32接口/FTZ | [CENSUS](APPENDIX_beginner_glossary.md#g100)：上表源码逐站点定位；[实算源身份](examples/fp32_ftz_r04e.result.json)固定14个实际读取文件，CPU实现与硬件内部表示分开 |
| F32→half RN | MEASURED：[窄域返回验收:33–37](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L33)记录完整raw32实际调用的接受/拒绝域；不转移为RZ或任意网络调用者已放行 |
| half→F32 | MEASURED：[同报告:9、39–46](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L39)非NaN 63,490项相同，2,046个NaN载荷差异保持MISMATCH |
| FTZ时机 / MUFU | MEASURED / CENSUS：具名5120例抽样与 [MUFU包装证据](L4_mufu.md#evidence)各自保留站点、域和版本，不合成全链FTZ定理 |
| 人工转换例 | CONTROLLED：[真实C++输出](examples/fp32_ftz_r04e.result.json)检验RN/RZ、输入FTZ与拒绝分支；只约束这些人工标量输入 |
| 全链范围 | MEASURED：[M2记录](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1)的1080/1440 f0与4K [L0](APPENDIX_beginner_glossary.md#g081)–L99保持原范围；后来统一M多帧、[A1](APPENDIX_beginner_glossary.md#g107)扩域和未验分支不由本页合并 |

一般可达域、完整同步/[别名](APPENDIX_beginner_glossary.md#g092)/生命周期、任意硬件/编译器与内部值唯一仍未建立。已有[NOT_RUN](APPENDIX_beginner_glossary.md#g104)、UNKNOWN、MISMATCH、MAP_CHECK_FAILED和拒绝域继续有效。
