# 用公开GlassBox-NR v2复现哪一项结果

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

[整串目录](INDEX.md) · [对象与方法](L0a_object_method.md) · [一帧接线](L0_frame.md) · [确定性与边界](L0b_determinism.md) · [权重组织](L2_weights_layout.md)

<a id="versions"></a>
## 先选一套版本

正文解释的源码和复现入口用的不是同一个提交。动手前先按下表选定一列，不要混用：

| 项目 | 正文源码引用（读懂算法用） | 复现入口（运行用，推荐） |
|---|---|---|
| GlassBox-NR 代码 | [e4a9b42](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec)；相对 tag v2.0.0-preview（d361dca）只改了 README/CHANGELOG | tag [v2.0.3-preview](https://github.com/Ashley-QwQ/GlassBox-NR/releases/tag/v2.0.3-preview) = fa8455d（数值部分与 v2.0.1-preview = 636b321 相同，另含回执完整性检查和两帧驱动） |
| Release 资产 payload.tar.zst.001 | v2.0.0-preview：465,105,242 B，sha256 8605a10e01765870befc625c0f15a64f4e17eb27968630b936f7091f5bc1d9cd | 沿用 v2.0.1-preview 的卷（v2.0.2 没有新卷）：462,661,132 B，sha256 c86119619d0638e7bfa94b6ab84f6dd465bba132aaf9d9b4130c648082455b8c |
| devkit/data/PAYLOAD_MANIFEST.json | 文件 sha256 47f093a12bafd10b6193f9fd9a66dbc82ec6d1c2a6e1b025fed5d6a75fae69aa | 文件 sha256 2049478691d87772e044a87c01c0679a99d265e630734d5cbfc78b84abde51aa（与 v2.0.1 的 ca50ccbc… 只差 DEVKIT 驱动文件的几条 pin，资产行相同） |
| 两者差别 | — | 只有 HMMA half 零的发布改回规范 +0：四个链模块里的 7 个 C++ 源文件、三个预编译模块、runtime pins、manifest 与 payload 随之变化；说明见 [L4.hmma](L4_hmma.md#hardware)。其余正文源码引用照 e4a9b42 读即可。v2.0.2 另外只改了运行驱动：回执不完整（缺、重、乱序或为空）时以退出码 4 拒绝；跑整链前可以先用 `python devkit/test_run_1080_f0.py` 自测这项比较。v2.0.3 再加两帧驱动和帧 1 参考表，见[两帧接续](#two-frames) |
| 预期结果 | 1080 f0 终图 764e7dd0… | 同左，见 [预期输出](#expected)；v2.0.3 上用公开模块实跑了 f0 → f1：158/158 与 158/158，两帧终图 764e7dd0… / 3f1d62eb…（[门](../../../experiments/b1-glassbox-v203-gate-20261031/RESULT_ZH.md)） |
| 已核范围 | 正文各页“我们怎么知道”所列 | 本页所述的固定 1080 f0 公开参考表；其他尺寸与多帧见 README 声明表 |

代码、payload 和 manifest 三者要取同一列；混用（例如 v2.0.0 的 payload 配 v2.0.1 的代码）不对应任何已验收的组合。

<a id="quickstart"></a>
## 公开读者的起点

先 checkout tag v2.0.3-preview，再按[该 tag 下 README 的 Quickstart](https://github.com/Ashley-QwQ/GlassBox-NR/blob/v2.0.3-preview/README.md#quickstart-linux-x86-64-python-313-numpy-safetensors-zstd--14)执行；这里不重复命令。本文依据本机保存的[同一README:31–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L31)及[devkit说明:5–17](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/README.txt#L5)核对，未联网检查远端状态。

该入口复现**1920×1080、frame 0/[reset](APPENDIX_beginner_glossary.md#g032)、fill00、自有CPU状态、158次[调用](APPENDIX_beginner_glossary.md#g080)的公开参考表一致性**。公开预编译模块面向Linux x86-64／CPython 3.13；README另列numpy、safetensors和zstd依赖。其他平台的历史测量不表示发布载荷已含该平台即用后端。[README:18–24、31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L18)、[driver:58–59](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L58)。

<a id="inputs"></a>
## 需要的输入和资产

读者自行取得固定版本310.8.0.0的[DLL](APPENDIX_beginner_glossary.md#g078)，以[对象身份](L0a_object_method.md#object)与发布manifest校验；DLL及生成的[权重](APPENDIX_beginner_glossary.md#g079)不随仓库/载荷分发。公开make_weights.py从其中单一WEIGHTS_HT资源确定性派生五种所需文件，格式关系见[权重页](L2_weights_layout.md#layouts)。不能用另一个版本的DLL或把自己的任意图片当作此参考表的同一输入。[README:5–14、49–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L5)。

其余准备物是v2源码/运行时、发布[payload](APPENDIX_beginner_glossary.md#g097)、认证[函数表](APPENDIX_beginner_glossary.md#g074)和固定frame-0输入。两个输入文件为[caller](APPENDIX_beginner_glossary.md#g096)-id1.bin（当前颜色）与caller-id3.bin（[运动矢量](APPENDIX_beginner_glossary.md#g023)），从payload布局到README指定的inputs目录；参数、资源描述及参考表也必须来自相同发布集，不用私有捕获替换。[devkit/README.txt:8–17](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/README.txt#L8)、[manifest](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/manifest.json)、[资源格式](L0_frame.md#textures)。

先完成官方快速开始中的文件/重定位检查，再执行它的默认完整链入口；仅通过verify-only表示准备检查通过，尚未运行模型，不能报告数值[MATCH](APPENDIX_beginner_glossary.md#g104)。缩短stop-after的分段运行也不能领取158次调用及[FINAL](APPENDIX_beginner_glossary.md#g105)通过。[driver:36–37、42–59、83–86](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L36)。

<a id="expected"></a>
## 预期输出，以及平台表中的旧封存

固定1080 f0的最终图[SHA](APPENDIX_beginner_glossary.md#g103)-256应为：

~~~text
764e7dd0d8f440b5afeb36e72fea3d8bc137bef891e8f09dc3476b6fef8d34ef
~~~

这是[纹理](APPENDIX_beginner_glossary.md#g027)id2在L157之后的原始输出摘要；显示截图、另存的PNG或不同颜色变换后的文件不能拿来与它比较。[worker:102–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/devkit_worker.py#L102)、[公开参考表:1](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/reference_f0.json#L1)。

公开[README平台表:80–89](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L80)中的X79/[M2](APPENDIX_beginner_glossary.md#g107)、12400F/MSVC旧ea731776、1280P/MSVC/M及Pi 3B+/M，列的是各自1080 f0的同一终图锚点。**ea731776是较早优化合流封存，不是M2的[别名](APPENDIX_beginner_glossary.md#g092)**；其后才有几何/时域扩展、统一M和发布子封存M2，[ARCH:1425](../../../ARCHITECTURE_V3_ZH.md#L1425)。平台表不证明这些构建的二进制相同，也不提供每个ISA的全部原语资格；Pi只核FINAL，其他范围须看各自回执，[ARCH:1245–1246、1556](../../../ARCHITECTURE_V3_ZH.md#L1245)。

本文不复述速度数字作为验收标准。平台表的历史ea731776计时计数有更细的原报告口径：四条计时链与四条内存链分别记账，不能把它们算作八次计时[均值](APPENDIX_beginner_glossary.md#g044)，[ARCH:1563](../../../ARCHITECTURE_V3_ZH.md#L1563)。输出摘要相等与性能是否可比是两件事。

<a id="match"></a>
## 此入口的MATCH是什么意思

公开worker从自己的[工作区](APPENDIX_beginner_glossary.md#g082)与六纹理连续推进；每次调用后计算完整workspace与id1/2/3/6/9/10的SHA-256，由外层driver对照公开reference_f0.json，最后再核FINAL。158点与FINAL全部符合时，正式运行入口返回0。[worker:79–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/devkit_worker.py#L79)、[driver:70–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L70)。

这一步是**对公开参考摘要表的复现**：读者重算当前状态的摘要，未在本地重新取得原生GPU完整状态后做直接字节差分。参考表的来源说明及M2验收结果另有记录；其中1080门只有111点带原生D观测，其余对[G0b](APPENDIX_beginner_glossary.md#g109)参考FULL/六纹理，不能把公开158次表一致写成158次全新的原生FULL观察。[M2 RESULT:82、107–110](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L82)、[参考表说明:1](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/reference_f0.json#L1)。

MATCH只适用于本次绑定的输入、参数、前态、版本和比较范围；不等于视觉相近，不等于任意输入证明，也不补全NOT_OBSERVED。具体标签沿用[证据词表](APPENDIX_evidence_history.md#project-terms)，[全域](APPENDIX_beginner_glossary.md#g111)目标仍[NOT_ESTABLISHED](L0a_object_method.md#limits)。

<a id="examples"></a>
## 局部例子怎么跑

下表的例子都只用人工输入或整数地图，不跑模型、GPU 或整链。命令都从本仓库根目录执行；输入从哪里找见 [_roots.py](examples/_roots.py)：

- GlassBox-NR 源码：默认找本仓库旁边的 `GlassBox-NR` checkout，也可以用 `--source-root PATH` 指定。版本按 [上面的表](#versions) 选。
- 函数表和整数地图：用 `--tables PATH`（payload_layout.py 的 `--tables` 输出）或 `--payload PATH`（payload_layout.py 的 `--out` 输出）指定，按 sha256 查找并核对。
- `--out FILE` 把结果写到别处；不加这个参数时，会覆盖仓库里已提交的回执。

| 例子 | 验证什么 | 需要 | 命令 | 预期 |
|---|---|---|---|---|
| [ffn_r04b.py](examples/ffn_r04b.py) | B0、TIN、ViT 三族的 FFN 门函数逐位相同；half 加法顺序改变结果 | g++、源码 | `python -B -X utf8 skewer/examples/ffn_r04b.py --out ffn.json` | 首行 `finite_gate_equal 63488`，status PASS |
| [hmma_r04f.py](examples/hmma_r04f.py) | HMMA 的 half 点积与缓存路径 | g++、源码 | `python -B -X utf8 skewer/examples/hmma_r04f.py --out hmma.json` | 首行 `dot 0010`，打印 PASS |
| [fp32_ftz_r04e.py](examples/fp32_ftz_r04e.py) | F32 → half 转换与 FTZ 边界 | g++、源码 | `python -B -X utf8 skewer/examples/fp32_ftz_r04e.py --out fp32.json` | 结果 JSON 里 stdout 的首行为 `boundary 33800000 0001 0001 01 00`，status PASS（进程先打印一行 JSON 摘要） |
| [attention_av_r04f.py](examples/attention_av_r04f.py) | 同一组人工分数在 ViT 与 TIN 中的 AV 发布差别 | g++、numpy、源码、RCP 表 | `python -B -X utf8 skewer/examples/attention_av_r04f.py --tables TABLES --out av.json` | 首行以 `ViT 4d32 2a29 d448 c5` 开头 |
| [geometry_r04g.py](examples/geometry_r04g.py) | 1080 L56/L100 整数地图的几何计数 | numpy、payload | `python -B -X utf8 skewer/examples/geometry_r04g.py --payload PAYLOAD --out geometry.json` | status PASS |
| [map_trace_r04f.py](examples/map_trace_r04f.py) | 追两个物理输出字节到其源地址 | numpy、payload | `python -B -X utf8 skewer/examples/map_trace_r04f.py --payload PAYLOAD --out trace.json` | status PASS |
| [beginner_r04m.py](examples/beginner_r04m.py) | 入门页的人工教学数字 | 无 | `python -B -X utf8 skewer/examples/beginner_r04m.py` | status PASS |

在 GlassBox-NR `e4a9b42` 和 `636b321` 两个提交上，前四个例子的输出与已提交回执相同。回执里 generated 源码的哈希会随 checkout 位置变化，因为生成的 C++ 里写的是源码的绝对 include 路径；这不影响算术结果。

其余脚本（verify_*、record_*、classify_* 等作者侧审计，以及 param_change、qkv_closed_form、split16_rest、b70_rz_copy、substitutions、anatomy_r04i、weights_layout、formulas）要读私有项目档案 `experiments/…` 或原机器上的文件，公开 checkout 运行不了。

<a id="two-frames"></a>
## 固定 1080 两帧接续：已知合同与缺口

固定 1080 配置下，第二帧怎样接上第一帧，已有的自有 CPU 链给出了一份保守的工程合同（[F05 整理](../../../experiments/anatomy-f05-frame-contract-r01-20261031-codex/RESULT_ZH.md)）。它有一个前提：你已经持有同一构建、同一路线的完整逐帧 profile 包，也就是每一帧的 calls、params 和纹理描述符。v2.0.3-preview 起，公开发布包已经带齐 f0 和 f1 这一对：`devkit/run_1080_two_frames.py` 在同一进程里按下面的合同先跑 f0 再跑 f1，帧 1 的两份上传在 release 资产 `inputs-f1-1080.tar`（24,893,440 B，sha256 `f2d283262ffb7d7fdc05c3e7705f8ec11e9cac7d810c71ebff5f91596e726940`） 里，逐 launch 对照 `reference_f0.json` 和 `reference_f1.json`，命令见该 tag 下 README Quickstart 第 7 步。2026-10-31 在 v2.0.3 上实跑：158/158 与 158/158，两帧终图 764e7dd0… / 3f1d62eb…（[门](../../../experiments/b1-glassbox-v203-gate-20261031/RESULT_ZH.md)）。

- **每帧外部输入只有两项**：id1 当前颜色（1920×1080 RGBA16F，小端 half，16,588,800 B）和 id3 运动向量（1920×1080 RG16F，8,294,400 B），按原始字节上传。
- **跨帧保留**：整片工作区 212,519,936 B 原样接续。158 路线保留六张纹理对象，帧边界携带 id2、id6、id9、id10 的数据，下一帧只刷新 id1 和 id3。帧尾 L155 写 id9，L156 把 id9 复制到 id6（下一帧的历史），L157 用 id9、id10 写显示用的 id2；不能拿 id2 代替 id6（[outtail.cpp:99–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L99)）。156 路线只有 id1、id2、id3、id6 四张，B70 直接写 id2，帧尾再复制到 id6。这是已验收驱动的做法（MEASURED：1080 f0–f5 两种填充全部链-MATCH），不是最小必需状态的证明。
- **第二帧**：用同一 profile 家族里 f1 的 calls 和 params（counter=1，历史与 MV 句柄按模板），不能只把 f0 的 counter 加 1 再跑一遍；每次调用接回返回的纹理后，才调下一次。
- **reset**：换用整套 reset params。它关闭旧历史和 MV 的时域读取、counter 回 0，本帧结束时新状态覆盖 id6；它不清空工作区。切镜 f8 的冷/热启动与历史扰动对照已有终图证据。
- **必须拒绝**：分辨率或格式变化、158↔156 路线切换、任意控制插值、p5 的 counter 16 以上；版本、模块或资产身份变化时丢弃旧状态，重新初始化。
- **缺口**：公开的两帧命令和参考值只覆盖这一对固定的 f0/f1 输入、fill 00；f2 以后、fill A5、其他分辨率都还没有公开入口。也没有"抽象控制 → 完整 profile"的生成器。所以换成自己的新输入时，只能报告"在守卫内执行，并接续了自身状态"，不能报告 MATCH。

<a id="layer-assets"></a>
## 层索引资产（1080 的 L27 / L56 / L100 与 RSQ / RCP）

[L3.split16-window](L3_split16_window.md)、[L2.06](L2_06_decoder_bridge.md)、[L3.norm](L3_norm_nonfinite.md) 和 [L3.attention-softmax](L3_attention_softmax.md) 的表驱动说明用到下面这些资产，它们都在 v2.0.1-preview 的发布包里。按 sha256 在 PAYLOAD_MANIFEST.json 里查位置：PAYLOAD 类在 payload_layout.py `--out` 目录下的 canonical path，RELEASE_VOLUMES 类在 `--tables` 目录的 `tables/<sha256>.npz`。加载前先核 bytes 和 sha256，NPZ 用 `numpy.load(path, allow_pickle=False)`。

| 资产 | 发布 sha256 | manifest root | transform | bytes |
|---|---|---|---|---|
| L27 map | `6eade1fab0bdc0bcffa1a967736e4ab84c57e3d8937a538f22dca5e2205a8ed3` | PAYLOAD | none | 31,591,374 |
| L27 wiring | `e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea` | PAYLOAD | none | 304,721 |
| L27 contract | `3407a615888a4a2a11505f3dd42a45de5175f1438ce09efb1c277e5046aa5857` | PAYLOAD | release_form | 591 |
| L56 map | `f9280f62d910b66cdb728860fe27d36153da6a71367182b6cb4951667b42bb01` | PAYLOAD | none | 17,106,182 |
| L56 wiring | `384adcbb6260db42348605a7b84532d10a02491a3fc4fb1260624227282d3686` | PAYLOAD | none | 201,381 |
| L56 contract | `710c38c8a76c4198d95228de787b08f12ed73bc5a4684e94c8e9440eda8adff8` | PAYLOAD | release_form | 16 |
| L100 map | `12701da070a98f9242fa0e60e5fe767917902bdc6c1b9266109d91c161d42dd5` | PAYLOAD | none | 13,360,831 |
| L100 metadata | `a144ef00d3f4d072d2552dbeb3e9e7aea537779134287f2225510bef5e87c63c` | PAYLOAD | release_form | 3,376 |
| RSQ | `06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62` | RELEASE_VOLUMES | none | 246,454 |
| RCP | `055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59` | RELEASE_VOLUMES | none | 246,446 |

transform 为 release_form 的三项是发布时改写过的形式：两个 contract 只保留原 JSON 的 contract 字典，外包一个 contract 键；运行时读 `release_json.contract`。L100 metadata 的执行器只读 `coverage.counter_writes`；它的发布形式与历史文件在字段上是否完全一致，还没有对照归档实物核过。1440 和 4K 有各自的 map 与 wiring（4K 的 L56 wiring 与 1080 不同），不能只改 CTA 数沿用 1080 的表。完整的历史 SHA → 发布成员对照见 [F04 资产链](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)。

**交给公开执行器之前要做加载适配。** 原 NPZ 不能把全部字段直接装成字典传进去。[load_layer_assets.py](examples/load_layer_assets.py) 照公开 runtime 的做法（[g0a_runtime.py:13–29](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/g0a_runtime.py#L13-L29)、[48–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/g0a_runtime.py#L48-L54)、[plan_runtime_merged.py:35–41](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/plan_runtime_merged.py#L35-L41)）完成 L56 的适配：只留 wiring 需要的 map 字段，保持有符号 dtype、本机字节序、C 连续并设为只读；thread_class 从 (80,4,32) 补成 (80,4,32,1)，因为执行器按 (c,y,l,s) 取地图；contract 从 release_form 外壳里取出；RSQ / RCP 展开成按 half_bits−0x0410 索引的 F32 位型稠密表。不加参数时读绑定文件里记录的本机路径，加 `--payload` / `--tables` 时按 sha256 找发布资产；每项都先核 sha256。`LayerAssets.arguments(input, weights)` 给出公开 `audit_execute` 的位置参数。2026-10-31 用人工输入和人工权重跑过一次：输出 1,433,600 B；去掉 thread_class 补的那一维会被 `map index` 守卫拒绝。这只证明接口接得上，不证明数值正确；`audit_execute` 不检查只读，预编译入口才检查。自己写 DAG 解释器时，可以直接用原始三维 class 和原始 half-bit 表键。公开的预编译模块面向 Linux x86-64 / CPython 3.13，其他平台要按 GlassBox-NR 源码自行构建。核对记录见 [G03](../../../experiments/anatomy-g03-layer-loader-r01-20261031-codex/RESULT_ZH.md)。

<a id="public-private"></a>
## 公开复现与私有捕获的边界

公开读者可用自己的DLL、发布载荷与同一输入，重建权重文件、核验资产并重新执行上述1080 f0参考表门；无需访问本项目私有磁盘上的捕获目录。这个结果对应公开M2用户驱动，不自动复测M的多帧、其他输入或ea731776旧构建。[README:54–78](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L54)。

若要独立重做“CPU对原生”的原始字节差分、逐点缺口裁决、其他分辨率/历史状态/参数变化或跨GPU观察，则需要相应原始上传、原生参数/资源描述、workspace/纹理快照及固定的比较范围；只有公开摘要表不能重建这些原值。具名范围见[对象与方法](L0a_object_method.md#capture)、[确定性](L0b_determinism.md#open)与[附录结果账](APPENDIX_evidence_history.md#index-measured-scope)。

本文只提供指向现有快速开始和验收[合同](APPENDIX_beginner_glossary.md#g101)的导读；本轮没有下载、编译、运行GPU、CPU模型或连续链。

本轮的[文档与范围校验](examples/r04k.validation.json)、[发布扫描](examples/r04k.leak.json)另存为可检查回执。
