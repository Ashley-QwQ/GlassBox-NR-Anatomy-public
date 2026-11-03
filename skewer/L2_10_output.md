# L2.10 输出

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [返回所属 L1](L1_10_output.md) · [本页术语](INDEX.md#形状与工作区记号)

L156 的[历史](APPENDIX_beginner_glossary.md#g024)复制由 [L2.01.copy（id9→id6）](L2_01_prepare.md#copy) 唯一定义；本阶段沿该链接读取，不另定义一份同[家族](APPENDIX_beginner_glossary.md#g080)正文。

<a id="postprocess"></a>
<!-- coverage: {"launches":[157],"kernels":["cg2r_post_process_kernel"]} -->
### L2.10.postprocess 显示后处理与 intensity 合成（1 次调用）

- 覆盖：L157 / 无 B 编号。
- 是什么：把 id9 [状态](APPENDIX_beginner_glossary.md#g002)作颜色处理，再与 id10 [基底](APPENDIX_beginner_glossary.md#g003)合成为显示输出。
- 输入 → 输出：id9与 id10各为高 H×宽 W×4 个 [F16](APPENDIX_beginner_glossary.md#g054)，加本次[宿主](APPENDIX_beginner_glossary.md#g096)[标量](APPENDIX_beginner_glossary.md#g076) → 同形 id2；不改写 id6。
- 怎么算：
  ~~~text
  1. 读取 id9 RGB 和本次宿主标量，按原序执行夹取/增益/非线性变换
  2. 作显式的极值、亮度式中间量、色相与饱和度分支计算
  3. 按各分支及已采对数/指数/倒数结果重组 RGB，保留灰度分支
  4. 对处理后 RGB 与 id10 基底求差，再按 intensity作融合合成
  5. 夹到有效颜色范围，RGB 以 RZ转 half，alpha写 1
  ~~~
- 数值规则：颜色链为 [F32](APPENDIX_beginner_glossary.md#g056)，单步加乘、融合、[FTZ](APPENDIX_beginner_glossary.md#g068)和[函数表](APPENDIX_beginner_glossary.md#g074)域不合并；最后转 half，不用数学库近似替代已采函数值。
- 实例变化：单例的图像尺寸、[pitch](APPENDIX_beginner_glossary.md#g084)、两份[纹理](APPENDIX_beginner_glossary.md#g027)[身份](APPENDIX_beginner_glossary.md#g103)和宿主标量按捕获配置绑定；无网络[权重](APPENDIX_beginner_glossary.md#g079)/学习[残差](APPENDIX_beginner_glossary.md#g017)，基底混合不能与神经块残差混为一谈。
- 为什么这么算：把显示颜色调整与下一帧历史状态的存储分开。
- 来源裁决：当前 [M2](APPENDIX_beginner_glossary.md#g107) 受守卫分支按 [HSL 型分解与重组](L3_b70_history_output.md#postprocess)解释，旧 [Oklab](APPENDIX_beginner_glossary.md#g034) 命名不替代这条实现；三个标量的 [数值作用](L3_b70_history_output.md#post-curve)已从代码列式，其宿主 API 名称仍未知。
- [参数分支](APPENDIX_beginner_glossary.md#g032)：五个精确控制字段选择同一F32颜色链的准入元组；[参数分支证据](APPENDIX_evidence_history.md#param-change)（measured on child candidate）。
- 我们怎么知道：[CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED（M2 明确行为；解释冲突保留）；[outtail.cpp 的 s157、rz 与 run](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp)。
- 往下：[L3.postprocess（颜色与显示合成）](L3_b70_history_output.md#postprocess)、[intensity 合同](L3_b70_history_output.md#intensity)；[L4.mufu（表函数）](L4_mufu.md#mufu)；[L4.fp32-ftz（F32/灰度分支）](L4_fp32_ftz.md#fp32-ftz)。
