# L2.01 图外前置

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

【CPU 重建】复制与填充的功能按下文列明；共用核及拆分方式的设计原因未知。

[整串目录](INDEX.md) · [返回所属 L1](L1_01_prepare.md) · [本页术语](INDEX.md#形状与工作区记号)

<a id="copy"></a>
<!-- coverage: {"launches":[0,156],"kernels":["cg2r_copy_kernel"]} -->
### L2.01.copy 颜色 / 历史复制（2 次调用）

- 覆盖：[L0](APPENDIX_beginner_glossary.md#g081)、L156 / 无 B 编号。
- 是什么：同一[家族](APPENDIX_beginner_glossary.md#g080)在帧首保存[颜色基底](APPENDIX_beginner_glossary.md#g003)，在帧尾传递[历史](APPENDIX_beginner_glossary.md#g024)[状态](APPENDIX_beginner_glossary.md#g002)。
- 输入 → 输出：L0：id1→id10；L156：id9→id6；各为高 H×宽 W×4 个 [F16](APPENDIX_beginner_glossary.md#g054)，[工作区](APPENDIX_beginner_glossary.md#g082)无数值出口。
- 怎么算：
  ~~~text
  1. 读取本次参数块与纹理的宽、高、行跨度
  2. L0 选当前颜色与基底，核对已捕获的恒等坐标合同
  3. L156 选 B70 状态与历史，核对源和目标角色
  4. 逐行把有效的 8×图像宽度个字节交给目标纹理
  5. 保持源纹理与其余工作区内容，供显示合成或下一帧读取
  ~~~
- 数值规则：恒等 L0 准入域保留有限 half [位型](APPENDIX_beginner_glossary.md#g057)，[非有限](APPENDIX_beginner_glossary.md#g069)转换仍拒绝；L156 按字节复制，包括零符号；不引入加乘或[浮点](APPENDIX_beginner_glossary.md#g056)舍入。
- 实例变化：两次调用的源/目标[纹理](APPENDIX_beginner_glossary.md#g027)[角色](APPENDIX_beginner_glossary.md#g084)不同，几何与行跨度随帧配置[绑定](APPENDIX_beginner_glossary.md#g103)；无[权重](APPENDIX_beginner_glossary.md#g079)、无[残差](APPENDIX_beginner_glossary.md#g017)，不能仅凭函数相同认为两套复制入口合同相同。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100)（接线/源码）；[ARCH 0.7 §1.1、§6.4](../../../ARCHITECTURE_V3_ZH.md#11-一帧从输入到输出)。
- 往下：[L3.workspace-map（资源与写区间）](L3_workspace_map.md#regions)；L156 的 [逐行复制及原生 seam 证据](L3_b70_history_output.md#copy)；输出侧由 [L1.10](L1_10_output.md) 复用本片。

<a id="clear"></a>
<!-- coverage: {"launches":[1],"kernels":["cc_cb_clear"]} -->
### L2.01.clear 控制区初始化（1 次调用）

- 覆盖：L1 / 无 B 编号。
- 是什么：把工作区开头的控制字置为全 1。
- 输入 → 输出：WS（本帧共享工作区）从偏移 0 开始的连续 4n 字节，n（[参数块](APPENDIX_beginner_glossary.md#g083)给出的 32 位字数）；1080 实例长 388,096 B，工作区其余部分不由本核清理。
- 怎么算：
  ~~~text
  1. 读取工作区基址
  2. 从本次参数块读取控制字数
  3. 检查目标连续区间处于工作区内
  4. 把区间内每个字节填为 255
  5. 保留区间外字节，交给后续生产者发布标记
  ~~~
- 数值规则：全 1 是控制字的位型，不作为浮点 NaN 运算；不舍入、不读取工作区旧值，也不把整片工作区置零。
- 实例变化：几何改变时计数与工作区身份按参数变化；无权重、无数值残差。
- 我们怎么知道：CENSUS（[M2](APPENDIX_beginner_glossary.md#g107) 明确填充行为）；[entry.cpp 的 run_launch](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp)。
- 往下：[L3.workspace-map（控制字与发布区间）](L3_workspace_map.md#clear)。
