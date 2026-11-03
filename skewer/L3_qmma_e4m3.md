# L3.qmma-e4m3：矩阵乘由哪些 K32 步组成

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start intro -->
<a id="beginner-qmma"></a>
【入门简化】把一行与一列对应相乘再相加时，这条规则每次处理32对，带入一个小计，先把各项朝零放到同一刻度，再加起来、保存[F16](APPENDIX_beginner_glossary.md#g054)小计；下一篮用这个已保存结果继续。有些出口还要转成更粗[E4](APPENDIX_beginner_glossary.md#g055)。先读[有限数点与小篮](L1_00_numbers_primer.md)，再下钻下面的整数式、候选和证据范围；篮子是教学比喻，不是设备内部结构证明。
<!-- beginner-r04m:end intro -->

[整串](INDEX.md) · 上层：[TIN chained](L2_03_tin_encoder.md#chain-32)、[ViT projection](L2_05_vit.md#projection)、[解码桥](L2_06_decoder_bridge.md#bridge)

[跨架构原语与CPU后端比较](L4_cross_arch.md)

## 本页局部记号

全局格式、运算与证据标签见[INDEX](INDEX.md#形状与工作区记号)。

| 局部符号 | 含义 |
|---|---|
| A[M,K]、B[K,N] | [逻辑](APPENDIX_beginner_glossary.md#g085)[矩阵](APPENDIX_beginner_glossary.md#g051)；物理排列由[调用](APPENDIX_beginner_glossary.md#g080)者[绑定](APPENDIX_beginner_glossary.md#g103) |
| C^(j)、J | 第j步之前的half [seed](APPENDIX_beginner_glossary.md#g042)、[K32](APPENDIX_beginner_glossary.md#g065)步数J=K/32 |
| Q32 | 一步[sm_120](APPENDIX_beginner_glossary.md#g078) E4 K32及half[发布](APPENDIX_beginner_glossary.md#g091) |
| field / [value](APPENDIX_beginner_glossary.md#g067) / renorm | [对齐指数](APPENDIX_beginner_glossary.md#g066)取字段/实际乘积/[归一化](APPENDIX_beginner_glossary.md#g067)操作数的候选区别 |

<a id="qmma-e4m3"></a>
### L3.qmma-e4m3 一个输出元素的有序 K32 链

- 是什么：把矩阵[归约](APPENDIX_beginner_glossary.md#g050)拆成有序的 32 项步，每步接收并重新发布一个 F16 [累加器](APPENDIX_beginner_glossary.md#g064)。
- 输入 → 输出：逻辑 $A[M,K]$、$B[K,N]$ 的 E4 [编码](APPENDIX_beginner_glossary.md#g057)及 $C^{(0)}[M,N]$ → F16 矩阵；部分调用随后才用 $Q8$ 发布 E4。不能把整个[权重容器](APPENDIX_beginner_glossary.md#g079)或[工作区](APPENDIX_beginner_glossary.md#g082)统一解释为 E4。
- 怎么算：
  ~~~text
  1. 按本次布局/索引取得 A 的一行、B 的一列及该输出位置的 seed。
  2. 初始化 C^(0)；没有显式 seed 时按该调用合同使用 +0。
  3. j 从 0 到 J−1：取 A、B 在第 32j 到 32j+31 项的编码。
  4. C^(j+1) = Q32(这 32 对编码, C^(j))；保留原拒绝条件。
  5. 保存最后一个 F16；只有调用者要求 E4 出口时再执行 Q8。
  ~~~
- 数值规则：每个 $Q_{32}$ 内先按公共格点 [RZ](APPENDIX_beginner_glossary.md#g060) 放置乘积和 seed，再精确整数求和，末端一次 [RN-even](APPENDIX_beginner_glossary.md#g059) 到 F16；跨步存在多次 F16 舍入。源码先放置 seed，再按 0→31 加乘积；只有这些已放置整数的和允许[重排](APPENDIX_beginner_glossary.md#g019)。另作 $Q8$ 时再多一次格式舍入。
- 为什么这么算：分块矩阵核的发布接口使每 32 项都能携带同格式累加器；接口不能证明硬件设计动机或唯一内部加法树。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED（限定候选和已测例）；[移植 RESULT:9、15–19](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门)。
- 往下：[L4.e4m3-format](L4_e4m3_and_k32.md#e4m3-format)、[L4.qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation)、[可执行例子](L4_e4m3_and_k32.md#worked-examples)。

下式中，r=0..M−1 是 A/C 的行索引，n=0..N−1 是 B/C 的列索引。

```math
C^{(j+1)}_{rn}
=Q_{32}\!\left(A_{r,32j:32j+32},B_{32j:32j+32,n},C^{(j)}_{rn}\right),
\qquad j=0,\ldots,J-1.
```

### 行级依据：矩阵、存储与发布接口

| 本断言 | 直接读源 / 观察 | 比较对象与范围 | 不能证明什么 |
|---|---|---|---|
| 每K32带入并发布F16 seed | [tin.cpp:88–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88) | CPU矩阵接口；E4编码与half结果分开 | 源码循环不证明物理GPU加法树 |
| 当前sm_120数值规则 | [qmma_sm120.hpp:49–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L49)及[裁决记录](APPENDIX_evidence_history.md#qmma-history) | 冻结候选、具名硬件原字节；大量软件比较另列 | 软件随机比较不是新增硬件案例 |
| 格式与辅助[尺度](APPENDIX_beginner_glossary.md#g031)不同 | [tin.cpp:26–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26) | 当前资源读取类型及各发布点 | 不披露系数，不把整个容器当E4 |

[原行级定位与各实验对应](APPENDIX_evidence_history.md#qmma-source-ledger)放在附录；默认生产守卫和当前[接受域](APPENDIX_beginner_glossary.md#g101)继续有效。

[TIN](APPENDIX_beginner_glossary.md#g011) 调用者只是可读代表。数据驱动家族仍使用各自的索引表、矩阵链和 seed 来源；共用 $Q_{32}$ 不表示布局和[残差](APPENDIX_beginner_glossary.md#g017)相同。保留的非 sm_120 旧分支也不因此成为其他架构的已验收实现。

<a id="候选如何从-1832-收敛到一个行为类"></a>
## 当前规则的适用边界

【验证记录】当前规则只达到 UNIQUE_BEHAVIOUR_CLASS_WITHIN_FROZEN_FINITE_DOMAIN_BANK：在冻结有限候选库内为一个行为类，不证明候选穷尽、全部有限输入硬件等价、[NaN](APPENDIX_beginner_glossary.md#g069)/Inf/符号零/溢出完整合同或网络可达性。非有限与 [overflow](APPENDIX_beginner_glossary.md#g071) 的生产拒绝仍见 [发布守卫](L4_e4m3_and_k32.md#publish-guards)，一般结论仍未建立。

其他架构不能沿用 sm_120：sm_75 为 field F24/整 K8，sm_86 为 renorm F24/两组 K8，sm_89 为 field F13/两组 K16，各自在组末 F16 发布；对齐指数、seed 参与方式及截断也有差别，不能只当作位数变化。

[候选表、跨架构收据、源码 SHA 与旧状态](APPENDIX_evidence_history.md#qmma-history)已迁到附录。旧“待 C++ 接入”和旧 4K 未运行仍按其年代保留；当前源码存在 field F25 分支，不把旧软件随机对照当成新硬件裁决，也不由后来[整链门](APPENDIX_beginner_glossary.md#g102)推出一般 QMMA 定理。
