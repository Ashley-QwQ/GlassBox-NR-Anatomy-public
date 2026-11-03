# L3.b0-noise-reprojection：B0 的噪声、16 通道与历史重投影

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-b0"></a>
【入门简化】这16格是送给网络的条件清单，不是16种颜色。前三项扰动另由位置/计数生成，不是从原图测出的颗粒；条件的总体视觉目的仍未知。无可用[历史](APPENDIX_beginner_glossary.md#g024)时，旧RGB三格重复当前RGB。接着每位置16项变32项，再在小[窗口](APPENDIX_beginner_glossary.md#g015)处理。

| 0：扰动 | 1：扰动 | 2：扰动 | 3：常数1 |
|---|---|---|---|
| 4：当前R | 5：当前G | 6：当前B | 7：旧R或当前R |
| 8：旧G或当前G | 9：旧B或当前B | 10：[style](APPENDIX_beginner_glossary.md#g005) | 11：tone |
| 12：structure | 13：条件值 | 14：条件值 | 15：常数0 |

当前/旧RGB在入格前各有规定变换；默认非[p5](APPENDIX_beginner_glossary.md#g032)时13/14是−1，p5分支改读两个[标量](APPENDIX_beginner_glossary.md#g076)条件且structure=1，不是另采两张遮罩图。[现有通道合同](#channels)。先看[当前点怎样去旧图取数](L1_00_history_primer.md#moving-point)和[五点内还含四邻域](L1_00_history_primer.md#nested-sampling)，再读下面的散列、精确坐标和字节解包。
<!-- beginner-r04m:end intro -->

<a id="resource-unpack-r04l"></a>
## B0资源解包（F03.02，排名71）

四个[E4](APPENDIX_beginner_glossary.md#g055)[矩阵](APPENDIX_beginner_glossary.md#g051)使用[TIN矩阵字节式](L3_tin_window.md#resource-layout-r04l)的普通[tile](APPENDIX_beginner_glossary.md#g087)分支：w1=(32,128)@0、w2=(128,32)@4096、qkv=(32,96)@9312、[proj](APPENDIX_beginner_glossary.md#g038)=(32,32)@20592；偏移相对本块[资源](APPENDIX_beginner_glossary.md#g079)[基址](APPENDIX_beginner_glossary.md#g084)，最后一个维度连续。adapter为16×32 [half](APPENDIX_beginner_glossary.md#g054)：nt=0..1、i=0..255，`e=i%8,l=i//8,fe=e%4,k=2*(l%4)+(fe&1)+8*(fe//2),n=l//4+8*(e//4)`，[逻辑](APPENDIX_beginner_glossary.md#g085) `adapter[k,16nt+n]=LE16(resource+8208+2*(256nt+i))`。[FFN](APPENDIX_beginner_glossary.md#g037)[残差](APPENDIX_beginner_glossary.md#g017)[尺度](APPENDIX_beginner_glossary.md#g031)32half@9232，[attention](APPENDIX_beginner_glossary.md#g039)尺度32half@21616；score尺度[F32](APPENDIX_beginner_glossary.md#g056)@20576仅[RN16](APPENDIX_beginner_glossary.md#g059)一次。bias4096half@12384，query/key的8×8坐标按[B70同一12-bit排列](L3_b70_history_output.md#resource-unpack-r04l)选索引；这是读取位置，不列参数值。[b00.hpp:7–20](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L7)。

<a id="p5-packed-r04l"></a>
## p5 own-history准入常数（V03.02，排名87）

这里只列控制常数。非reset的p5需history使能=1、temporal真、帧字低32位在1..15且高32位0；[CB](APPENDIX_beginner_glossary.md#g083)对应q3/4/5/8/11..17均0。以下三个尺寸组严格逐位相等：

| CB字段 | packed [u64](APPENDIX_beginner_glossary.md#g057) / 解释 |
|---|---|
| CB+0x30、+0x48 (u64) | 0x4487000044f00000；低/高F32=1920、1080 |
| CB+0x38、+0x50 (u64) | 0x3a72b9d63a088889；低/高F32=0.0005208333604969084、0.0009259259095415473 |
| CB+0xd0、+0xf0、+0x100 (u64) | 分别0x0000078000000438、0x0000078000000480、0x000003c000000240；低/高u32=(1080,1920)、(1152,1920)、(576,960)，不得当作F32 |

CB+0xa0、+0xa4 (f32)还须有限，且不为非零[次正规](APPENDIX_beginner_glossary.md#g068)，±0允许。判定失败拒绝，不能因数值接近尺寸倒数而通过位型等式。[R2 b00.hpp:41–50](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1_r2/returned/snapshot/candidate/repo/cpp/opt/M/entry/b00.hpp#L41)。

【CPU 重建／CENSUS】默认接线与受限参数分支分别说明；函数、格式与[发布](APPENDIX_beginner_glossary.md#g091)点保持原[合同](APPENDIX_beginner_glossary.md#g101)。训练动机及拆核设计原因未知，不逐片补推测。

[整串目录](INDEX.md) · 上层：[L1.02](L1_02_input_b0.md)、[L2.02 的五步](L2_02_b0.md#b0) · 共用算术：[矩阵乘](L3_qmma_e4m3.md)、[half](L4_half_arith.md)、[MUFU](L4_mufu.md)、[attention](L3_attention_softmax.md)、[norm](L3_norm_nonfinite.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| x,y；tx,ty | 未[镜像](APPENDIX_beginner_glossary.md#g030)内部坐标；颜色/[MV](APPENDIX_beginner_glossary.md#g023)镜像后的坐标 |
| f、[Radius](APPENDIX_beginner_glossary.md#g073)(k) | 原生帧字、认证噪声半径函数 |
| [TEX](APPENDIX_beginner_glossary.md#g027)、[tap](APPENDIX_beginner_glossary.md#g029) | 单次四邻域过滤、五tap中的一个采样点 |
| s_ff、s_att | 本块前馈/注意力残差的half尺度 |

<a id="b0-noise-reprojection"></a>
### L3.b0-noise-reprojection 从条件输入到两个特征出口（L2 / B0）

- 是什么：在每个 8×8 窗口中组装条件输入，执行一个 32 [通道](APPENDIX_beginner_glossary.md#g007)窗口块，并发布两种空间尺度。
- 输入 → 输出：id1 [RGBA16F](APPENDIX_beginner_glossary.md#g028)、有效时的 id3 RG16F 与 id6 RGBA16F、264 B params、B0 权重及[函数表](APPENDIX_beginner_glossary.md#g074) → [full](APPENDIX_beginner_glossary.md#g018) E4[Hn,Wn,32] 与 pool E4[Hn/2,Wn/2,32]。
- 怎么算：
  ~~~text
  1. 检查参数、几何、历史句柄、资源长度和已准备的噪声表。
  2. 未镜像 (x,y,f) → 四个整数键 → 三路 half 噪声。
  3. 镜像颜色坐标；当前 RGB 与有效历史 RGB 各完成输入变换。
  4. 噪声、RGB、控制量及常数 → feat[16] → half 适配结果[32]。
  5. E4 前馈、QKV、窗口 attention 与投影 → 未量化 half 结果。
  6. 直接 E4 发布 full；另一支从 half 做 2×2 pool 后 E4 发布。
  ~~~
- 数值规则：前端 F32、half 与后段 E4 的界面各自保留；噪声、纹理过滤和矩阵乘不能合成一个浮点库[调用](APPENDIX_beginner_glossary.md#g080)。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)，[b00.hpp:27–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L27)；MEASURED 的具体门及历史限制见[证据表](#evidence)。
- 往下：[噪声](#noise)、[紧凑表](#compact)、[16 通道](#channels)、[守卫](#guards)、[坐标](#coordinates)、[五 tap](#five-tap)、[过滤](#texture)、[窗口块](#adapter)、[双出口](#publish)。

<a id="noise"></a>
### L3.b0.noise 坐标 / 帧散列与三路噪声

本节伪代码的 `T_SQRT/T_LG2/T_COS/T_SIN` 是对应认证函数的 [F32 数值包装](L4_mufu.md#value-wrapper) 的短写：输入和返回值都是 F32 数值。取位型与解码不新增舍入并保留零的符号；在线 k 预组合表的查询方式、函数与角度包装仍按下文合同执行。

- 是什么：无逐像素推进[状态](APPENDIX_beginner_glossary.md#g002)的确定性生成器；[整数散列](APPENDIX_beginner_glossary.md#g075)产生键，再通过已采特殊函数变换形成 Box–Muller 型噪声。
- 输入 → 输出：U32 的 x,y,f → 四个 k∈[1,2²⁴] → 三个 F32 乘积位型 → feat[0:3] 的三个 half。
- 怎么算：
  ~~~text
  1. Hash32(v)=U32(((v >> ((v>>28)+4)) xor v) × 0x108ef2d9)。
  2. s=U32(y×0xd8163841) xor U32(x×0x8da6b343)
       xor U32(f×0x9e3779b9) xor 0x243f6a88。
  3. h0=Hash32(s)；h=(h0>>22) xor h0。
  4. j=0..3：v_j=Hash32(U32(h×m_j+a_j))；k_j=((v_j>>30) xor (v_j>>8))+1。
  5. u_j=k_j×2⁻²⁴；r1=Radius(k0)，r2=Radius(k1)；角度 a1=RN32(u2×2π)，a2=RN32(u3×2π)。
  6. Radius(k)=T_SQRT(RN32(RN32(T_LG2(u)×ln2)×(−2)))。
  7. F32 三路=[F32×(r2,T_COS(a2)), F32×(r2,T_SIN(a2)), F32×(r1,T_COS(a1))]。
  8. 分别 RN16，按 [g3,g2,g1] 写通道 0、1、2。
  ~~~
- 数值规则：所有整数乘 / 加按 U32 回绕；四条流的算法常量如下。COS/SIN 查得的值已包含角度的 [RZ](APPENDIX_beginner_glossary.md#g060) 归约，不能再归约一次。Radius(k) 预组合了完整半径链；在线不再调用 [LG2](APPENDIX_beginner_glossary.md#g072)。三路乘法先发布 F32，再 RN16，尚未转 E4。
- 我们怎么知道：CENSUS，[noise_online_optd.hpp:12–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L12)、[b00.hpp:29、37–39](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L29)；INFERRED / 离线[全域](APPENDIX_beginner_glossary.md#g111)重建，[噪声证明 RESULT:9–27](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#q2-帧几何参数)。
- 往下：[压缩及认证](#compact)、[实际计算例](#worked-example)、[MUFU 的域及边缘](L4_mufu.md#edges)。

| j | m_j | a_j |
|---:|---|---|
| 0 | 0xcaa5b80d | 0x21dd796b |
| 1 | 0x2c9277b5 | 0xac564b05 |
| 2 | 0x83232c31 | 0x3463e0ac |
| 3 | 0xfa6dc5f9 | 0x4712a88e |

上述 ln2、2π 分别指 F32 常量位型 0x3f317218、0x40c90fdb；角度表内部用于 RZ 归约的逆 2π 为 0x3e22f983。它们是算法常量，[数据流:24–27](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/noise_dataflow_ZH.md#L24)。f=U32(CB+0xc8 (u32))，在 params 的字节偏移0xc8。它参与种子，不由目录帧号或“reset”标签推导。噪声证明轮读到的连续三帧 reset=[1,0,0] 对应 f=[0,1,2]；另一组逐帧 reset 的 f=[0,0,0]。一般[宿主](APPENDIX_beginner_glossary.md#g096)计数、跨实例及 32 位回绕合同仍 [UNKNOWN](APPENDIX_beginner_glossary.md#g104)。颜色[镜像](APPENDIX_beginner_glossary.md#g030)只改颜色和 MV 地址，补齐位置的噪声仍用原始 x,y。

噪声证明轮还给出所有可组合非零半径 / 角度乘积的下界 2.3981766091495898×10⁻¹¹，排除了这个域中的非零 F32 次正规乘积；它不消除符号零、half [下溢](APPENDIX_beginner_glossary.md#g071)或其他[算子](APPENDIX_beginner_glossary.md#g035)的 FTZ 边界。通用特殊函数及[编码](APPENDIX_beginner_glossary.md#g057)不在这里重复，见 [L4.mufu](L4_mufu.md#representation)。

<a id="compact"></a>
### L3.b0.compact CPU 表示与网络行为分开

【CPU 重建】合法k查询经[身份](APPENDIX_beginner_glossary.md#g103)认证的函数资产，恢复原F32位型，无整帧噪声缓存。键域、格式、长度或身份失败即拒绝；它保存原函数链结果，不是函数近似。[格式守卫与整数解码](APPENDIX_cpu_storage.md#noise-codec-guards)见附录。

[完整块格式、端点与残差解码、加载寿命和三份资产 SHA](APPENDIX_cpu_storage.md#noise-codec)移至附录；在线运算的乘法、F32/half 舍入与噪声通道仍在 [噪声步骤](#noise)。离线压缩重建不等于 B0 launch 验收，该证明轮的执行门仍 NOT_RUN。

<a id="channels"></a>
### L3.b0.channels 镜像、颜色变换与 16 个通道

- 是什么：在一个画布位置拼出固定顺序的 16 项 half 条件向量。
- 输入 → 输出：噪声、id1 的 RGB、可用时的历史 RGB、params 控制字 → feat[16]。
- 怎么算：
  ~~~text
  1. tx=x<W ? x : 2W−2−x；ty=y<H ? y : 2H−2−y；检查二者仍在图像内。
  2. gain=RN16(F32+(CB+0xc4 (f32),CB+0xc4 (f32)))。
  3. cur[c]=H×(H+(upload[ty,tx,c],half(−0.5)),gain)，c=0..2。
  4. feat[0:3]=三路噪声；feat[3]=half(1)。
  5. feat[4:7]=cur；feat[7:10]=temporal ? 历史变换结果 : cur。
  6. M/M2：控制字分别RN16后写10..12；p5=false时13/14写half(−1)，15写+0。
  7. 默认发布入口在p5=true时拒绝；受限分支的选择与准入另见下节。
  ~~~
- 数值规则：镜像是一轮反射，不是任意越界坐标的周期折返；越界过远被拒绝。读图像行跨度为 8W B，只取前三个 half，[alpha](APPENDIX_beginner_glossary.md#g026) 不作颜色输入。减 0.5 与乘 gain 分别 half 舍入；gain 来自 params，不能把某次捕获的固定缩放当通用常量。
- 我们怎么知道：CENSUS，[b00.hpp:29–42](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L29)；CONTROLLED，[控制量独立核验:15–28、40–51](../../../experiments/parity-control-params-r03-20260922/B1_VERIFICATION_ZH.md#12-p-层偏移我自己从-zip-解包核过全对)。
- 往下：[守卫与 p5 边界](#guards)、[历史变换](#five-tap)、[适配矩阵](#adapter)。

| 通道 | p5=false 的已实现内容 | 来源 |
|---|---|---|
| 0 | RN16(g3) | r2 与第二角度的 COS 乘积 |
| 1 | RN16(g2) | r2 与第二角度的 SIN 乘积 |
| 2 | RN16(g1) | r1 与第一角度的 COS 乘积 |
| 3 | 1，half 编码 0x3c00 | 固定常量 |
| 4、5、6 | 当前 R、G、B 的分步 half 输入变换 | id1[ty,tx,0..2] |
| 7、8、9 | 历史 R、G、B 的输入变换；无历史则重复 4、5、6 | id6 与 id3，或当前 RGB |
| 10 | RN16(Style) | CB+0xb4 (f32)，字节 0xb4；已观察宿主 style/128 映射 |
| 11 | RN16(Tone) | CB+0xac (f32)，字节 0xac |
| 12 | RN16(Structure) | CB+0xb0 (f32)，字节 0xb0 |
| 13 | −1 | CB+0xb8 (f32)（0xb8）参与 p5 判定；假分支不直接复制该值 |
| 14 | −1 | CB+0xbc (f32)（0xbc）参与 p5 判定；假分支不直接复制该值 |
| 15 | [+0](APPENDIX_beginner_glossary.md#g070)，half 编码 0x0000 | 固定常量 |

Tone / Structure 的位置由非默认控制对照区分：旧映射曾双向输出对方的原生结果，各 3,276,800 B；默认值相等时看不出交换。该控制门限 reset、无历史、无遮罩纹理的具名实例。MV 不占这 16 通道，它在 B0 核内参与[重投影](APPENDIX_beginner_glossary.md#g025)；显示 [intensity](APPENDIX_beginner_glossary.md#g004) 属于尾部。

<a id="guards"></a>
### L3.b0.guards 默认M/M2的reset、历史与p5边界

- 是什么：入口先限定可解释的参数与资源合同，不能靠回退路径掩盖缺失历史。
- 输入 → 输出：params、已配置几何 / 纹理身份、各资源字节长度 → 准入执行，或异常拒绝。
- 怎么算：
  ~~~text
  1. 要求264 B参数块；f=U32(CB+0xc8 (u32))。
  2. 非零帧历史句柄守卫（guard 4）：f>0 时，要求 U32(CB+0xc0 (u32))==1，
       CB+0x08 (u64)==本帧已配置 id6 句柄，CB+0x10 (u64)==本帧已配置 id3 句柄。
  3. temporal=(U32(CB+0xc0 (u32))!=0 && CB+0x08 (u64)!=0 && CB+0x10 (u64)!=0)。
  4. temporal=false：通道 7..9 直接使用当前 RGB 的变换结果。
  5. temporal=true：必须同时提供长度正确的 history 与 MV，执行 native_history_pixel。
  6. p5=(min(CB+0xb8 (f32),CB+0xbc (f32))>=0)；M/M2在真时拒绝，子候选另列。
  7. 再执行各算术原语的接受域检查；异常不计 MATCH。
  ~~~
- 数值规则：reset 是宿主状态；代码分支由实际 mode / 句柄判定，f=0 本身不等于无历史。非零帧历史句柄守卫（[guard 4](APPENDIX_beginner_glossary.md#g109)） 防止非零帧落入 current-only 回退或使用错误会话句柄，没有证明模型对历史数值扰动的敏感性。几何检查读 W/H分别取CB+0xd4 (u32)/CB+0xd0 (u32)，Wn/Hn取CB+0xf4 (u32)/CB+0xf0 (u32)，与已配置几何逐项比较；源码中残留的“1080 frame0”错误文本不能当现行尺寸限制。
- 我们怎么知道：CENSUS，[b00.hpp:30–35、53–62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L53)；非零帧历史句柄守卫（guard 4） 的结构移植见 [diff (i):23–35](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/seal-port/diff_i_structural_geometry.patch#L23)，[算术 diff (ii)](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/seal-port/diff_ii_arithmetic.patch)为空；[RESULT:12–18](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要)限定该构建和执行层句柄绑定。
- 往下：[坐标链](#coordinates)、[非有限与矩阵接受域](L3_norm_nonfinite.md#a1)、[门的证据范围](#evidence)。

其他直接检查：upload 必须为 8WH B；temporal 的 history 为 8WH B、MV 为 4WH B；噪声 owner 必须已准备；RSQ / RCP half 表分别为 30,705 / 30,704 项；镜像后坐标必须有效。更深处 Q/K 的统计量须落入 half 编码 [0x0410,0x7c00]，attention [分母](APPENDIX_beginner_glossary.md#g048)须在 [0x1c00,0x60e0]，矩阵原语守卫仍保留；见已展开的 [norm](L3_norm_nonfinite.md#norm32)、[attention](L3_attention_softmax.md#window-attention) 和 [QMMA 发布边界](L4_e4m3_and_k32.md#publish-guards)。

<a id="p5-candidates"></a>
### p5：控制通道与历史选择

p5真时，structure固定为1，两个[mask](APPENDIX_beginner_glossary.md#g006)分别来自CB的相邻F32字段；它们是控制量，不是从遮罩图像采样的像素。条件向量最后六通道为：

~~~text
feat[10]=RN16(CB+0xb4 (f32))                  // style
feat[11]=RN16(CB+0xac (f32))                  // tone
feat[12]=RN16(p5 ? 1 : CB+0xb0 (f32))         // structure
feat[13]=RN16(p5 ? CB+0xb8 (f32) : -1)
feat[14]=RN16(p5 ? CB+0xbc (f32) : -1)
feat[15]=+0
~~~

reset时计数CB+0xc8 (u32)=0，CB+0x08 (u64)至CB+0x88 (u64)、步长8的各字全零，CB+0xc0 (u32)=1；没有有效历史，7..9重复当前变换后的RGB。相关控制须有限，允许零、拒绝非零次正规。

有历史时，读本进程上一帧id6与当前caller id3，沿用[五tap/FMA](#five-tap)形成7..9；4..6仍为当前颜色，structure/mask沿用上式。受限入口要求1920×1080颜色/1920×1152内部画布；CB+0xc8 (u32)为1..15、CB+0xcc (u32)=0、CB+0xc0 (u32)=1；CB+0x08 (u64)/CB+0x10 (u64)分别匹配id6/id3。CB+0x18 (u64)/CB+0x20 (u64)/CB+0x28 (u64)/CB+0x40 (u64)及CB+0x58 (u64)至CB+0x88 (u64)、步长8的各字为零。CB+0x30 (f32)/CB+0x34 (f32)及CB+0x48 (f32)/CB+0x4c (f32)为(W,H)，CB+0x38 (f32)/CB+0x3c (f32)及CB+0x50 (f32)/CB+0x54 (f32)为指定F32倒数；CB+0xd0 (u32)/CB+0xd4 (u32)、CB+0xf0 (u32)/CB+0xf4 (u32)、CB+0x100 (u32)/CB+0x104 (u32)三对低/高字为(1080,1920)/(1152,1920)/(576,960)。控制及MV尺度须有限且拒绝非零次正规；额外aux句柄或错误绑定仍拒绝。

p5控制与自身历史分支的实现证据见[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）；默认发布入口不因此自动扩域。

<a id="p5-example-r04h"></a>
**真实控制函数的人工代入。** style=0.5、tone=0.25、原structure=2；reset两个mask=(2,2)，有历史时mask=(1,2)，其余绑定满足上面的受限入口：

| 情形 | p5/reset/temporal | feat[10..15]的half值 | 对应half编码 |
|---|---|---|---|
| reset | true/true/false | 0.5, 0.25, 1, 2, 2, +0 | 3800 3400 3c00 4000 4000 0000 |
| history | true/false/true | 0.5, 0.25, 1, 1, 2, +0 | 3800 3400 3c00 3c00 4000 0000 |

[真实代码脚本](examples/param_change_r04h.py)与[标量结果](examples/param_change_r04h.result.json)只计算人工CB，不执行网络或采样。

<a id="coordinates"></a>
### L3.b0.coordinates MV 到历史像素中心：显式 F32 融合边界

- 是什么：从当前图像位置的两个 MV half 构造历史采样的中心与小数偏移。
- 输入 → 输出：镜像后的 tx,ty、id3[ty,tx]、CB+0xa0 (f32)/CB+0xa4 (f32)、W/H → x0,y0,t,v。
- 怎么算：
  ~~~text
  1. rw=F32/(1,W)，rh=F32/(1,H)；MV 地址=(ty×W+tx)×4 B。
  2. ax=F32_FMA(F32(mv_x),CB+0xa0 (f32),F32×(tx+0.5,rw))。
  3. ay=F32_FMA(F32(mv_y),CB+0xa4 (f32),F32×(ty+0.5,rh))。
  4. x0=F32+(floor(F32_FMA(W,ax,−0.5)),0.5)。
  5. y0=F32+(floor(F32_FMA(H,ay,−0.5)),0.5)。
  6. t=clamp(F32_FMA(W,ax,−x0),0,1)。
  7. v=clamp(F32_FMA(H,ay,−y0),0,1)。
  ~~~
- 数值规则：[FMA](APPENDIX_beginner_glossary.md#g063) 的融合必须跨过相应乘加，不能先F32×再F32+；其结果还影响 floor 与后续定点采样格。native_temporal.hpp 以 volatile F32 运算和 std::fma 写清边界。F32/是当前C++的F32除法；这里不把它擅改为任意倒数表或库近似。当前实现对 MV 直接按像素取值，其与显式 MV 采样链相同的证据限已核输入 / 坐标域，不外推任意[描述符](APPENDIX_beginner_glossary.md#g088)或宿主坐标变换。
- 我们怎么知道：CENSUS，[native_temporal.hpp:5–9、27–33](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L27)；MEASURED / 限域核验，[原生分歧 RESULT:9–28](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据)，其中 fma_domain、coordinate_domain、mv_domain 三类审计分别限定运算与直接取值的依据。
- 往下：[五 tap 位置与权重](#five-tap)、[25 KB 的闭合经过](#evidence)。

<a id="five-tap"></a>
### L3.b0.five-tap 四条侧瓣加一个双线性中心

- 是什么：由两个一维三次重建系数组成五个历史纹理采样点，再按固定 F32 次序合并。
- 输入 → 输出：x0,y0,t,v、历史 id6 → 三个历史 half，经输入变换写通道 7–9。
- 怎么算：
  ~~~text
  1. 对 s=t 与 s=v 分别算 s2=F32×(s,s)，s3=F32×(s,s2)。
  2. L=F32_FMA(F32+(s,s3),−0.5,s2)；M0=F32+(F32_FMA(s3,1.5,−F32×(s2,2.5)),1)。
  3. R=F32×(F32+(s3,−s2),0.5)；M1=F32+(F32+(F32+(1,−L),−M0),−R)。
  4. C=F32+(M0,M1)；两轴结果记 Lx/M1x/Rx/Cx 与 Ly/M1y/Ry/Cy。
  5. xc=clip(F32_FMA(M1x,F32/(1,Cx),x0),0.5,W−0.5)；yc 两轴对应。
  6. xl=clip(F32+(x0,−1),0.5,W−0.5)，xr=clip(F32+(x0,2),0.5,W−0.5)；yt/yb 两轴对应。
  7. wl=F32×(Lx,Cy)，wt=F32×(Ly,Cx)，wc=F32×(Cx,Cy)，wb=F32×(Ry,Cx)，wr=F32×(Rx,Cy)。
  8. den=F32+(F32+(F32+(F32+(wl,wt),wc),wb),wr)。
  9. value=F32×(TEX(xc,yt),wt)；value=F32_FMA(TEX(xl,yc),wl,value)。
  10. value=F32_FMA(TEX(xc,yc),wc,value)；value=F32_FMA(TEX(xc,yb),wb,value)。
  11. value=F32_FMA(TEX(xr,yc),wr,value)；value=F32×(value,F32/(1,den))。
  12. history_half=RN16(value)；out=H×(H+(history_half,half(−0.5)),RN16(F32×(CB+0xc4 (f32),2)))。
  ~~~
- 数值规则：第 9–11 行对 RGB 各做一次；上→左→中→下→右的累加与左→上→中→下→右的分母次序分开。侧瓣权重可为负；不能拿 TEX 内部非负权重的合同代替五 tap 权重。历史先 RN16，再减 0.5，再 half 乘；不是在 F32 连做颜色变换后一次 RN16。CB+0xc4 (f32)按F32解释同一参数位型，不与其U32数值相等。越界历史坐标 [clamp](APPENDIX_beginner_glossary.md#g049) 到边界中心，不因越界改用当前颜色。
- 我们怎么知道：CENSUS，[native_temporal.hpp:34–48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L34)；MEASURED，[原生分歧的 full / pool 门:15–28](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证)。
- 往下：[每个 TEX 的四邻域过滤](#texture)、[half 发布](L4_half_arith.md#half-arith)。

<a id="texture"></a>
## 每个tap的过滤接口

TEX接收F32像素中心坐标与有限RGBA16F四邻域，返回按纹理规则发布的half，再展开为F32供五tap合并。1/256定点小数格、联合8位分数权重、共[指数](APPENDIX_beginner_glossary.md#g058)截断、负零和中点远离零均保留，不能以普通双线性+RN-even替换。[完整算术及两个单点例](L4_tex_filter.md#tex-filter)下钻到L4，具名硬件范围仍见[B0证据](#evidence)。

<a id="adapter"></a>
### L3.b0.adapter 16→32 适配与首个一头窗口块

- 是什么：适配把条件向量变成[特征](APPENDIX_beginner_glossary.md#g008)；每窗 64 个位置再经过前馈与窗口 attention。
- 输入 → 输出：half[64,16]、half 适配系数[16,32]、E4 矩阵与 half 尺度 / 偏置 → half[64,32]。
- 怎么算：
  ~~~text
  1. 每个位置 a[c]=HMMA_K16(feat[0:16],adapter[:,c])，c=0..31；xc=Q8(a)。
  2. h[128]=G(QMMA_K32(xc,W_expand))；门函数出口为 E4。
  3. z[c]=H×(a[c],s_ff[c])。
  4. 按 s=0,1,2,3 做收缩：z[c]=QMMA_K32(h[s×32:s×32+32],W_contract[s,:,c],seed=z[c])。
  5. Q8(z) 分别投影 Q/K/V：每列一个 K32；V 直接 E4 发布。
  6. Q、K 各按 32 通道 norm32；Q 再乘查询尺度，依次 half 发布后转 E4。
  7. 本窗 64×64 的带偏置 QK 分数 → 权重变换 → 指定分母树 / 倒数 → E4 权重。
  8. AV 按键 0..31、32..63 做两个 K32，携带 half 累加器；再发布 E4。
  9. 最终 y[c]=QMMA_K32(Q8(AV),W_proj[:,c],seed=H×(z[c],s_att[c]))。
  ~~~
- 数值规则：适配用 half×half 的 [K16](APPENDIX_beginner_glossary.md#g065)，不是 E4 的 K32；其当前实现按共同格截断乘积、整数求和，末端 RN16，见下面源码。适配残差保存 a 的 half，不能从[量化](APPENDIX_beginner_glossary.md#g061)后的 xc 还原。后续各 K32 的 half 发布、[激活](APPENDIX_beginner_glossary.md#g045)量化、Q/K [归一化](APPENDIX_beginner_glossary.md#g043)和 attention 权重顺序分别沿用已展开主题，不换成通用 BLAS / [softmax](APPENDIX_beginner_glossary.md#g047)。G 的[精确算术、128通道与适配half残差](L3_ffn.md#gate)已单列；它是单输入裁剪分段多项式，不是成对通道门。
- 我们怎么知道：CENSUS，[b00.hpp:6–26、41–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L41)；适配的未缓存合同 [mapexec_base.hpp:157–174](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp#L157) 与缓存版本 [decode_reuse.inc:71–105](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/decode_reuse.inc#L71)分列；数值门见[证据表](#evidence)。
- 往下：[QMMA矩阵链](L3_qmma_e4m3.md#qmma-e4m3)、[norm32](L3_norm_nonfinite.md#norm32)、[窗口attention](L3_attention_softmax.md#window-attention)、[双出口](#publish)。

适配系数存为 half；前馈扩张 / 收缩、QKV、最终投影的矩阵系数存为 E4。前馈 / attention 残差尺度和[位置偏置](APPENDIX_beginner_glossary.md#g052)为 half，查询尺度从资源中的 F32 转为 half。这里只描述存储与消费边界，不列任何权重数值或把权重当算法常量。

<a id="publish"></a>
### L3.b0.publish 从同一份 half 分别发布 full 与 pool

- 是什么：直接量化高分辨率出口，并在另一条路径上做 2×2 half 平均。
- 输入 → 输出：每窗 y[8,8,32] half → full 的 [TIN](APPENDIX_beginner_glossary.md#g011) 4×4 tile 布局与 pool 的两组通道平面布局，均为 E4 字节。
- 怎么算：
  ~~~text
  1. 每个 x,y,c：full[full_offset(x,y,c)]=Q8(Y_half[y,x,c])，Y_half 为本次 half 结果。
  2. 对每个 2×2 与通道 c：even=H+(y00,y01)，odd=H+(y10,y11)。
  3. avg=H×(H+(even,odd),half(0.25))；最后 pool=Q8(avg)。
  4. full：tile=(y//4)×(Wn//4)+x//4；lane=(x%4)×4+(y%2)×16+(c%8)//2。
  5. b=((y//2)%2)×4+c%2+((c//8)%2)×2+(c//16)×8；offset=tile×512+lane×16+b。
  6. pool 对物理通道 p=0..31：c=(p//16)×16+((p%16)//4)×2+p%2+((p%4)//2)×8。
  7. 以池化后的全图位置 X,Y：offset=(p//16)×(Wn//2)×(Hn//2)×16
       +(Y×(Wn//2)+X)×16+p%16。
  8. full 写 CB+0xd8 (u64) 指向的区间；pool 写 CB+0xf8 (u64) 指向的区间。
  ~~~
- 数值规则：pool 是三次 half 加、一次 half 乘，最后才量化；不从已量化 full 读取。full 长 WnHn×32 B，pool 长 (Wn/2)(Hn/2)×32 B。公式是显式物理排列；逻辑通道连续不代表磁盘 / [工作区](APPENDIX_beginner_glossary.md#g082)字节连续。
- 我们怎么知道：CENSUS，[b00.hpp:63–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L63)，与 [L1.02 的原池化说明](L1_02_input_b0.md)对应；本轮还用[人工 half 例](#worked-example)核对舍入影响。
- 往下：[E4 发布](L4_e4m3_and_k32.md#e4m3-format)、[half 原语](L4_half_arith.md#half-arith)；该 B0 输出布局到底了。

### full/pool的一个代入点

【真实输出循环实算】[脚本](examples/substitutions_r04g.py)逐字抽取b00.hpp输出循环的索引表达式。取内部画布1920×1152，full点(x,y,c)=(1,2,3)：tile=0、并行位置索引=5、字节选择=5，所以offset=0×512+5×16+5=**85 B**（0b01010101）。其位段分别来自空间tile、16 B向量编号与向量内通道/行选择。

pool另取逻辑点(X,Y,c)=(1,2,3)，反查物理通道p=5；第一平面偏移为(2×960+1)×16+5=**30,741 B**。该pool点对应原窗口的2×2来源位置(2,4)/(3,4)/(2,5)/(3,5)，不是与full点(1,2)共用坐标。[实算输出](examples/substitutions_r04g.result.json)同时给出85和30741，索引不增加数值舍入。

<a id="evidence"></a>
## 已有验证与未决范围

【验证记录】保存微基准、融合边界隔离 B0，以及具名 CPU 自有多帧门各比较不同对象，[逐轮结果、计数、原始/冻结来源及调试导出根因](APPENDIX_evidence_history.md#b0-evidence)已迁移。部分旧原轮目录未在本机保留，相关数字仅据冻结摘要，不称重读原始输出。四方回放共同一致仍可能共同偏离原生；必须保留正文的实际 FMA 融合边界，不能把中间调试导出变成额外舍入点。

旧 R04/R06 仍 DIFF，旧 R06 f2 NOT_RUN；隔离 B0 为 [teacher-forced](APPENDIX_beginner_glossary.md#g106) 单 launch，f3 用另一捕获 f2 id9，f4/f5 NOT_RUN_MISSING_NATIVE_HISTORY。原生采样描述符仍 UNKNOWN，跨设备的旧坐标前缀不是二维全域证明。旧reset-only记录按日期保留；受限p5分支的证据统一见[参数分支账](APPENDIX_evidence_history.md#param-change)。

854 的 1080 f0–f5/1440 f0–f3 和统一 M 的 4K f0–f2 是各自构建范围，不称 [M2](APPENDIX_beginner_glossary.md#g107) 新多帧门；1440 f1/f2 六纹理仅五时点、f3 输入平移并跨进程续接；4K f3+ 与独立历史扰动未运行，A5 早期比较已写区/保留[补集](APPENDIX_beginner_glossary.md#g093)。不由链门推出任意内容、内部结构唯一或硬件等价。

<a id="worked-example"></a>
## 实际计算例：一个坐标、两个原生帧字

附录小脚本在原写作轮实际执行，工作目录为仓库根；只读三份上述紧凑资产并验证 SHA，再按 C++ 公式查询五项、计算三路噪声。没有导入网络或读取预测目标。Python 的整除明确为 floor，struct 的 f/e 转换用于发布 F32 / half。

[完整脚本与认证 SHA](APPENDIX_cpu_storage.md#noise-example)移至附录；下方保留原执行输出，原运行范围见证据附录。

实际输出的资产 SHA 为 3/3 MATCH；固定 x=y=0：

| f | [k0,k1,k2,k3] | feat[0:3] 的 half 值 | half 编码 |
|---:|---|---|---|
| 0 | [11369803,9653346,12969588,4756067] | [−0.2196044921875,1.0283203125,0.1273193359375] | [0xb307,0x3c1d,0x3013] |
| 1 | [13874273,8098557,8117985,11021557] | [−0.666015625,−1.0068359375,−0.61328125] | [0xb954,0xbc07,0xb8e8] |

f=0 的 F32 乘积依次为 −0.21956901252269745、1.0282138586044312、0.12729476392269135；其后才出现表中 RN16 的结果。例子同时展示：固定位置改变帧字就改变噪声，输出通道次序仍固定。

末尾还用人工 2×2 half 输入 [[2048,1],[−2048,1]] 验证池化：H+(2048,1)=2048，H+(−2048,1)=−2047，最终 avg=0.25；实数直接平均为 0.5。它检验的是这里的舍入顺序，不含任何模型权重或原生输出，不是新增 B00 字节门。

F16矩阵算术继续下钻：[L4.hmma：K16公共格、seed、发布与硬件边界](L4_hmma.md#hmma)。

### 五tap：一个人工历史像素

【真实代码实算】取4×4人工历史RGB：hist[y,x,c]=(x+2y+c+1)/16；像素(x,y)=(1,1)，MV=(0.0625,−0.0625)，两轴尺度1，gain参数0.5。真实native_history_pixel给x0=1.5、y0=0.5、t=0.25、v=0.75，中心xc≈1.70714283、yc≈1.29285717。

L/T/C/B/R权重依次为−0.07690429688、−0.02563476562、1.196289062、−0.07690429688、−0.02563476562；分母0.9912109375。R通道按实际T/L/C/B/R取样顺序得到0.1379394531、0.1616210938、0.2370605469、0.3879394531、0.3491210938，随后仍按原F32融合/除分母、RN16、half减0.5及half乘gain执行。

最终三个half编码为 **b44e b29c b09c**。[完整实算/源SHA](examples/substitutions_r04g.result.json)中，原函数与只增加输出的trace副本六字节相同；采样器本身的截断与中点例见[L4.tex-filter](L4_tex_filter.md#worked-example)。该人工点不代表B0整调用验收。
