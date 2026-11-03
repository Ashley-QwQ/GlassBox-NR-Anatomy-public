# GLASSBOX-NR: The Onion Skewer from One Frame Down to Arithmetic

<!-- beginner-r04m:start entry -->
<a id="beginner-entry"></a>
## Read It First as a One-Picture Story

What goes in is **the current image, motion information, the saved result from the previous frame when available, and control numbers**; what comes out is an image of the same width and height as the input with modified colors. The middle stages process layer after layer of internal numbers, and the tail end uses them to modify the colors. **The overall visual purpose remains unknown**; one cannot assign it a specific image-enhancement function based on its name alone.

The "number card" next to a position is a sequence of numbers saved internally: **[features](APPENDIX_beginner_glossary.md#g008)** are these internal numbers, and **[channels](APPENDIX_beginner_glossary.md#g007)** are how many items each position holds; "32 items per position" does not mean 32 colors or 32 frames. A **block** is a stage of computation that receives, processes, and hands off numbers; a **[skip](APPENDIX_beginner_glossary.md#g016) / bypass** saves earlier numbers, routes around an intermediate section, and reconnects them later; a **[launch](APPENDIX_beginner_glossary.md#g080) / invocation** is a single request for the device to execute a program, and one block may be split across several launches.

**No fully controlled paired visual evidence yet**: this skewer still lacks a complete control group [binding](APPENDIX_beginner_glossary.md#g103) the same target object, input, [history](APPENDIX_beginner_glossary.md#g024), and control variations, so scattered PNGs are not used here as effect demonstrations. The diagrams and small synthetic examples below explain only wiring and arithmetic, not visual measurements. [Display boundaries](APPENDIX_evidence_history.md#r04f-review-resolution)

On a first read, follow this short path: [Full-Frame Functional Diagram and Six Bypasses](L0_frame.md#beginner-frame) → [Learn One Block from Scratch](L1_00_one_block_primer.md) → [Two Frames Plus One Reset](L1_00_history_primer.md) → [Finite Number Points and 32-Item Small Baskets](L1_00_numbers_primer.md) → [Ten L1 Stages: Starting from Pre-Graph Preparation](L1_01_prepare.md). Exact arithmetic can be drilled into on demand after finishing the ten stages. Click unfamiliar terms when you meet them, or look them up in the [111 beginner glossary entries](APPENDIX_beginner_glossary.md); build and verification codenames are not network layers.

Reading depth: this page is the index, and [L0](APPENDIX_beginner_glossary.md#g081)/L1/L2/L3/L4 denote progressive layers of depth.<br>Execution numbering: launch L0–L157 separately refers to the default 158 launches.<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B0–B70 are logical blocks, not reading levels. Read the plain-language functional diagrams first, then check the exact numbering, formats, and evidence below.
<!-- beginner-r04m:end entry -->

[Formula coverage and open items](APPENDIX_evidence_history.md#formula-open-r04l): default [closed form](APPENDIX_beginner_glossary.md#g020) 1731/1824, [TABLE](APPENDIX_beginner_glossary.md#address-status) 87, UNKNOWN 6; counting by the weakest item per original audit row gives 6/44 closed-form families, and including the extra thread_class fields gives 4/44; navigation coverage and formula closure are counted separately.

[Native Behavior / Measured Scope] Current color and display output are both W×H; display blends the [processed state](APPENDIX_beginner_glossary.md#g002) with the saved [color base](APPENDIX_beginner_glossary.md#g003) by [intensity](APPENDIX_beginner_glossary.md#g004), and the named controls [style](APPENDIX_beginner_glossary.md#g005)/tone/structure/[automask](APPENDIX_beginner_glossary.md#g006)/skin alter the output (see [Control Scope and skin Conditions](../../../ARCHITECTURE_V3_ZH.md#L1792), [B0 Controls](L3_b0_input.md#channels), and [Tail Stage](L3_b70_history_output.md#postprocess)); these effects do not yet establish an overall visual purpose, and uses such as "denoising / stylization" are not inferred from the product name.
The fixed identity takes only four items: the [DLL](APPENDIX_beginner_glossary.md#g078) is nvngx_dlssnr.dll 310.8.0.0; sm_120 is the SM 12.0 architecture identifier of the target GPU; "signed sample C" is the binary sample identity verified in this project, not an image category; [WEIGHTS_HT](APPENDIX_beginner_glossary.md#g079) is the weight resource identifier inside that DLL, and resource numeric values are not listed here.

**[Native Behavior]** refers to the observable behavior of the [target binary](APPENDIX_beginner_glossary.md#g001); **[CPU Reconstruction]** refers to the reproduction rules in the project source code; **[Verification Record]** refers to results bound to a specific build, input, and comparison scope. The three are labeled separately; reading source code does not automatically become a hardware measurement.

## How to Read This Skewer (15 Lines)

1. On a first read, start with [Object and Method](L0a_object_method.md), then view the inputs, outputs, and history loop in [L0 One Frame](L0_frame.md).
2. Pick an L1 stage from the table below and first confirm its position in the default frame.
3. L2 pages list launch families; reading levels L0/L1 and launch L0–L157 are two separate numbering systems.
4. Follow "Drilling Down" into L3 to see [operator](APPENDIX_beginner_glossary.md#g035) inputs, formulas, and [publication](APPENDIX_beginner_glossary.md#g091) order.
5. Enter L4 when you need to check number formats, accumulation, or rounding.
6. By default this skewer covers 158 launches; support boundaries for the 156-launch route and control variants are listed separately.
7. Shapes and resource identities follow actual [params](APPENDIX_beginner_glossary.md#g083); filenames and kernel names do not substitute for content.
8. Distinguish [logical](APPENDIX_beginner_glossary.md#g085) T, physical P, spatial padding, and genuine zero-writes.
9. CPU compute wiring follows the named release source code; native conclusions require separate observation, and numeric results are bound to their respective builds and inputs.
10. Each slice's "How we know" distinguishes source reading, measured results, controlled comparisons, and inference.
11. Small worked examples are used to check formulas and do not count as new GPU runs or [full-chain gates](APPENDIX_beginner_glossary.md#g102).
12. When comparing, check the scope first—named [role](APPENDIX_beginner_glossary.md#g084) / [cumulative declared write set](APPENDIX_beginner_glossary.md#g105) / full [workspace](APPENDIX_beginner_glossary.md#g082) / final image; final-image agreement does not fill in missing intermediate observations.
13. For temporal behavior, read [B0](L3_b0_input.md) first, then [B70 → Copy → Display](L3_b70_history_output.md#b70-history-output).
14. [Speculation], [UNKNOWN](APPENDIX_beginner_glossary.md#g104), NOT_RUN, and [rejection guards](APPENDIX_beginner_glossary.md#g101) are all part of the main-text contract.
15. The end of this page lists written topics, shared steps, and still-missing independent arithmetic leaves; having all planned pages written does not equal evidence closure.

The navigation below follows the default 158-launch route; reading levels L0/L1 and launch indices launch L0–L157 are kept separate.

Cross-cutting guides: [153-Entry Weight Organization](L2_weights_layout.md) · [Cross-GPU / CPU Backend Comparison](L4_cross_arch.md) · [Public v2 Reproduction Guide](REPRODUCE.md).

Read [L0a Object and Method](L0a_object_method.md) first to confirm the fixed target object and byte-reproduction criteria; then enter from [L0 One Frame](L0_frame.md): current color, [motion vectors](APPENDIX_beginner_glossary.md#g023), previous-frame history, and control values pass through the [encoder](APPENDIX_beginner_glossary.md#g009), [global bottleneck](APPENDIX_beginner_glossary.md#g010), and decoder, splitting into two exits: history state id9→id6 and display output id2. [L0b Determinism and Reproducibility](L0b_determinism.md) separately lists driver, device, fill, repeat, and unmeasured boundaries.

In the table below, 1h/2h/4h/8h for TIN denote 1/2/4/8 attention heads with 32 channels per head; here h is the head count, distinct from image height H.

| L1 slice | launch range | B numbers | Stage handoff |
|---|---|---|---|
| [01 Pre-Graph Preparation](L1_01_prepare.md) | L0–L1 | — | id1→id10; initialize workspace control region |
| [02 Input Stage B0](L1_02_input_b0.md) | L2 | B0 | 16 channels → 32-channel [full](APPENDIX_beginner_glossary.md#g018) / pool |
| [03 TIN Encoder](L1_03_tin_encoder.md) | L3–L24 | B1–B22 | 1h→2h→4h→8h; leaves four tiers of skip |
| [04 split16 Encoder](L1_04_split16_encoder.md) | L25–L57 | B23–B30 | 512-channel [window](APPENDIX_beginner_glossary.md#g015) blocks → 1024-channel bottleneck entry |
| [05 ViT Bottleneck](L1_05_vit.md) | L58–L99 | B31–B38 | [repack](APPENDIX_beginner_glossary.md#g019) → 8 × 5-kernel block → repack |
| [06 Decoder Bridge](L1_06_decoder_bridge.md) | L100 | B39 | Bottleneck main path and B30 skip → 512 channels |
| [07 split16 Decoder](L1_07_split16_decoder.md) | L101–L132 | B40–B47 | Eight window blocks → [outview](APPENDIX_beginner_glossary.md#g022) |
| [08 TIN Decoder](L1_08_tin_decoder.md) | L133–L154 | B48–B69 | Four-stage [upsampling](APPENDIX_beginner_glossary.md#g021) merged with four encoder skips |
| [09 B70](L1_09_b70.md) | L155 | B70 | Decoded features, B0 skip, color, and temporal inputs → id9 |
| [10 Output](L1_10_output.md) | L156–L157 | — | id9→id6; postprocessing(id9,id10)→id2 |

## Shape and Workspace Notation

Parameter fields are uniformly written as CB+0xNN ([f32](APPENDIX_beginner_glossary.md#g057)/u32/u64), where 0xNN is the hexadecimal byte offset; 64-bit word indices are given only in parentheses. Real field names in scripts and source code keep their implementation spelling.

Image width and height are $W,H$; the internal canvas is $W_n,H_n$, read from admitted params. Spatial dimensions are written as width × height, and $X_r(C)$ denotes $H_r\times W_r\times C$ elements with [batch=1](APPENDIX_beginner_glossary.md#g086) omitted by default. [E4](APPENDIX_beginner_glossary.md#g055) denotes the one-byte E4M3 encoding, [F16](APPENDIX_beginner_glossary.md#g054)/[F32](APPENDIX_beginner_glossary.md#g056) denote binary16/binary32, and binary64 is double precision; [Inf](APPENDIX_beginner_glossary.md#g069)/NaN are infinity and not-a-number, and [satfinite](APPENDIX_beginner_glossary.md#g062) is finite saturation; logical shape does not imply a physically contiguous channel order in memory.

| Other notation / role names | Meaning in this directory |
|---|---|
| 1/256 fixed-point subpixel grid / [Q32](APPENDIX_beginner_glossary.md#g065) | Sampling coordinates use a 1/256 fixed-point subpixel grid, and the four corners use joint 8-bit fractional weights; Q32 is a single K32 step of sm_120 E4 in this skewer, receiving and publishing an F16 [seed](APPENDIX_beginner_glossary.md#g042) |
| [RSQ](APPENDIX_beginner_glossary.md#g072) / RCP / EX2 / LG2 | [Certified function maps](APPENDIX_beginner_glossary.md#g074) for reciprocal square root / reciprocal / base-2 exponential / base-2 logarithm, with domains and bit patterns specified in L4 |
| [Q8](APPENDIX_beginner_glossary.md#g061)(x) / D8(x) | F16→E4 [RN-even](APPENDIX_beginner_glossary.md#g059)/satfinite quantization / exact E4→F16 decoding; E denotes only the [exponent](APPENDIX_beginner_glossary.md#g058) |
| [H+](APPENDIX_beginner_glossary.md#g063) / H× / HF | Half addition, multiplication, and fused multiply-add; each preserves its own publication point |
| F32+ / F32× / F32/ / F32_FMA | F32 addition, multiplication, division, and fused multiply-add, preserving per-site rounding / [FTZ](APPENDIX_beginner_glossary.md#g068) / rejection |
| [Den](APPENDIX_beginner_glossary.md#g048) / [CumWrites](APPENDIX_beginner_glossary.md#g093)(L) / [Partials](APPENDIX_beginner_glossary.md#g050) | [attention](APPENDIX_beginner_glossary.md#g039) denominator / cumulative declared write set / L100 F16 partial-sum array |
| RN16/RN32/RN64, bits16, [Sat01](APPENDIX_beginner_glossary.md#g049) | Round-to-nearest-even to the specified format, raw half encoding, clamp to [0,1]; function-table domains are listed separately |
| [CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED / CONTROLLED / INFERRED | Source reading / named measurement / controlled comparison / inference, each retaining its target object and scope |
| launch / B | launch is one kernel invocation; B is a logical block, and the two numbering systems are separate |
| [token](APPENDIX_beginner_glossary.md#g041) / [tile](APPENDIX_beginner_glossary.md#g087) | token is one feature position; tile is an execution-time block partition whose exact shape follows the slice description |
| $r,C$ | r is the resolution tier and C is the channel count; an execution-indexing axis cannot automatically be treated as C |
| $T,P$ | T is the logical valid token count; P is the physical row count after padding T up to a multiple of 32 |
| Wn/Hn, x/y, frame | Internal canvas width/height, un-[mirrored](APPENDIX_beginner_glossary.md#g030) coordinates, and native frame counter; not the absolute video frame number |
| $N_{\rm out}$ / N_out | Sum of output role lengths in this instance; used for physical byte sequences whose logical channel split has not yet been independently confirmed |
| full / pool / pooled | Full-density exit of this tier / pooled exit / role after pooling; does not directly prescribe the pooling arithmetic |
| skip / [residual](APPENDIX_beginner_glossary.md#g017) / seed | Bypass / residual input / starting value of an accumulation; each slice specifies the actual source |
| inpview / outview / chained | Input-view block / output view / same-tier consecutive block; kernel names do not substitute for layout or synchronization contracts |
| [ffwd](APPENDIX_beginner_glossary.md#g037) / ffwd_proj / [proj](APPENDIX_beginner_glossary.md#g038) | Feed-forward front half / feed-forward back half / post-attention projection; semantics on data-driven slices are separately marked as inference |
| RGB / MV / Q/K/V, FFN | Red-green-blue / motion vector / [query](APPENDIX_beginner_glossary.md#g040)/key/value, feed-forward network; standard-library operators are not assumed substitutable from naming alone |
| K16 / K32 / RN-even / [RZ](APPENDIX_beginner_glossary.md#g060) | Single-step 16- / 32-term product accumulation, round-to-nearest-even, round toward zero |
| h_fma / FTZ / [MUFU](APPENDIX_beginner_glossary.md#g073) | Half fused multiply-add helper function / subnormal flush-to-zero contract / captured special mathematical functions |
| [TIN](APPENDIX_beginner_glossary.md#g011) / [split16](APPENDIX_beginner_glossary.md#g013) / [ViT](APPENDIX_beginner_glossary.md#g014) | Window-block family in this skewer / 16-head 512-channel window blocks / 32-head 1024-channel global bottleneck |
| post_block / [mapexec](APPENDIX_beginner_glossary.md#g089) | Final block of the neural network / CPU implementation executing from bound arithmetic graphs and provenance indices |
| [alpha](APPENDIX_beginner_glossary.md#g026) / intensity / WS | Fourth image channel / display blending strength / shared workspace |
| params / role / release / pitch | Launch parameter block / named memory role / completion flag / actual byte stride per row |

Let $(W_0,H_0)=(W_n,H_n)$, and along both axes take $n_{r+1}=4\lceil n_r/8\rceil$ at each step—halving first and then rounding up to a multiple of 4; $T=W_6H_6$, $P=32\lceil T/32\rceil$. This extent chain is an induction over the captured corpus; the root canvas depends on the [host](APPENDIX_beginner_glossary.md#g096) contract and **is not a closed-form formula for arbitrary $W,H$**.

| Dimension (width × height) | 1080p | 1440p | 4K |
|---|---|---|---|
| Image $W\times H$ | 1920×1080 | 2560×1440 | 3840×2160 |
| $X_0$ internal canvas | 1920×1152 | 2560×1472 | 3840×2176 |
| $X_1$ / TIN 1h | 960×576 | 1280×736 | 1920×1088 |
| $X_2$ / TIN 2h | 480×288 | 640×368 | 960×544 |
| $X_3$ / TIN 4h | 240×144 | 320×184 | 480×272 |
| $X_4$ / TIN 8h | 120×72 | 160×92 | 240×136 |
| $X_5$ / split16 physical extent | 60×36 | 80×48 | 120×68 |
| $X_6$ / ViT 2D logical grid | 32×20 | 40×24 | 60×36 |
| $T$ / $P$ | 640 / 640 | 960 / 960 | 2160 / 2176 |
| Full workspace / B | 212,519,936 | 340,722,688 | 763,062,272 |

For 1440, $X_5$ has valid height 46 and physical height 48; for 4K, ViT has 16 extra padding tokens. Valid extent, allocated extent, and actual write sets must be examined separately; padded regions cannot be treated across the board as unused space. CENSUS / INFERRED: [ARCH 0.7 §8.1–§8.5](../../../ARCHITECTURE_V3_ZH.md#8-几何与分辨率).

Each slice uses $Span(A)$ to denote the interval of [tensor](APPENDIX_beginner_glossary.md#g076) role A in the workspace: $[p_A-b,\ p_A-b+N_A)$, where $b$ is the workspace base address for this run, $p_A$ is taken from the launch's params, and $N_A$ is the physical role size in bytes. An E4 role $X_r(C)$ is $W_rH_rC$ B, and F16 multiplies that by 2; padding and synchronization writes are counted separately rather than applying a fixed cross-geometry offset. [Textures](APPENDIX_beginner_glossary.md#g027) are bound by id, format, dimensions, pitch, and point in time; [RGBA16F](APPENDIX_beginner_glossary.md#g028) has valid row length $8W$ B, and MV is RG16F with valid row length $4W$ B.

## Evidence Path Legend

The links below can be opened on the current workstation; when taking only a [mirror](APPENDIX_beginner_glossary.md#g099) of this skewer, external source code and private records are not necessarily bundled with it. Paths are not object identities; exact versions still follow bound SHAs.

| Path family | Content role | Can an independent reader open it? |
|---|---|---|
| GlassBox-NR (GitHub, fixed commit [e4a9b42](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec)) | Standalone C++ reconstruction and runtime source code for release v2; every source link in the text points at this commit | Opens directly on GitHub; running the examples locally still needs an adjacent source checkout |
| experiments/… | Private project captures, diagnostics, acceptances, and frozen identity records | Requires the original project evidence directory; typically cannot be opened from a standalone mirror |
| [mapform-split16-qkv-r01-20261027-codex](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md) | Eight-field address closed forms and held-out map validation for split16 qkv; [formula notes](../../../experiments/mapform-split16-qkv-r01-20261027-codex/FORMULAS_ZH.md), [frozen source](../../../experiments/mapform-split16-qkv-r01-20261027-codex/formula_qkv.py) | Requires the original project research directory; address equivalence, not a proof of numeric DAG, full chain, or dynamic provenance |
| [mapform-split16-rest-r02-20261027-codex](../../../experiments/mapform-split16-rest-r02-20261027-codex/RESULT_ZH.md) | Per-field closed forms, held-out results, and retained failures for F16/F17/F19–F23 | Requires the original project research directory; r04 supplements 4K address tables, while empty arrays remain non-evidence for addresses |
| [mapform-split16-r04-20261027-codex](../../../experiments/mapform-split16-r04-20261027-codex/RESULT_ZH.md) | Bound candidates, 4K map comparisons, and historical variant classification; [structured receipt](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json) | Requires the original project research directory; Chinese reports were reconstructed from JSON by r04 `repair_reports.py`, with corrupted originals retained as `*.garbled-ascii` |
| [mapform-tin-r03-20261027-codex](../../../experiments/mapform-tin-r03-20261027-codex/RESULT_ZH.md) | NOT_RUN inventory for missing new TIN address tables | Requires the original project research directory; source transcription does not equal new held-out validation |
| F:/dlssnr-work/…, E:/dlssnr-work-e/… | Provenance maps, wiring, and parameter assets from local workstreams | Requires identical asset copies and SHA bindings; not a public source directory |
| mlxdlss/ | Early Python CPU reference and certified-function asset interface | Requires a full project checkout; not the current C++ release code itself |
| E:/b1-relocated-10600t/… | Historical map/configuration evidence copies relocated back from 10600T | Present on the current workstation; not bundled with the mirror, and a relocation path does not equal release asset identity |

<a id="项目与验证术语"></a>
For build codenames and verification terms used in evidence tables, see the [appendix glossary](APPENDIX_evidence_history.md#project-terms).

## Computation Conventions

Design motivations are stated once here: training objectives, reasons for kernel splitting, and hardware resource bottlenecks are not uniquely determined by output comparisons. The text below first gives readable computation and publication relations, while concrete system relations state only verifiable inputs and outputs; [Speculation] is used only for training intent.

**The C++ code is optimized, but does not alter the arithmetic.** Floating-point accumulation grouping and order, explicit fusion boundaries, and rounding points are preserved; only exact integer sums allow reordering. Loop organization, tiling, and fusion implementation mechanics are not treated as network structure. Behavioral explanations primarily follow the [release source cpp/](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp); the Python reference is used to cross-check 1080 f0 and does not substitute for multiframe runs or other geometries.

**Examine data-driven data movement separately from arithmetic.** Indices in mapexec, scalar_map, and address mapping tables determine where values are fetched from and written to; the arithmetic core determines how those values are multiplied, added, and rounded. An index table can reproduce the output without by itself proving the semantics that "this is a certain convolution or attention"; training intent is separately marked [Speculation], and unconfirmed index or operator semantics are listed directly as UNKNOWN along with their closure conditions.

Numeric interfaces reused across stages: E4 publication uses satfinite / RN-even; sm_120 QMMA sums each K32 according to the frozen rule and publishes F16, carrying that F16 [accumulator](APPENDIX_beginner_glossary.md#g064) across K32 steps; ordinary half operations preserve their respective roundings, and the h_fma software reference rounds the binary64 fused result via RN-even and then rounds to half via RN-even. Two-stage software rounding does not mean all GPU half behavior is proven; ±0, subnormals, Inf, FTZ, and exceptions are distinguished by each primitive's contract. Final RGB-to-half conversion in B70 and L157 uses RZ (round toward zero) and cannot use ordinary half RN-even. INFERRED / MEASURED (limited to listed primitives): [ARCH 0.7 §7](../../../ARCHITECTURE_V3_ZH.md#7-算术层).

<a id="已测实例的边界"></a>
For named builds, inputs, and comparison scopes, see [appendix boundaries](APPENDIX_evidence_history.md#index-measured-scope).

## Drilling Down

L2 has 46 coverage/step entries in total: 41 coverage families/singletons plus the five intra-kernel steps of B0; repeated prose is now organized by shared flows and variant tables while entry points and coverage attribution remain unchanged. The 41 coverage slices consolidate 44 native function names and cover the default L0–L157; forward/inverse repack, initial/middle ViT expansion, and terminal projection variants are detailed within their respective families. Cross-stage shared slices are defined only once, and the reuse navigation in the table below does not double-count coverage.

| L1 → L2 | Slices in file | Cross-stage reuse |
|---|---:|---|
| [01 Pre-Graph Preparation](L1_01_prepare.md) → [L2.01](L2_01_prepare.md) | 2 | copy covers both L0 and L156 |
| [02 B0](L1_02_input_b0.md) → [L2.02](L2_02_b0.md) | 6 | One launch singleton and its five intra-kernel steps |
| [03 TIN Encoder](L1_03_tin_encoder.md) → [L2.03](L2_03_tin_encoder.md) | 12 | Four tiers of chained list both encoder and decoder launches |
| [04 split16 Encoder](L1_04_split16_encoder.md) → [L2.04](L2_04_split16_encoder.md) | 8 | Four chained families list both encoder and decoder launches |
| [05 ViT](L1_05_vit.md) → [L2.05](L2_05_vit.md) | 6 | Five arithmetic positions each reused eight times, plus bidirectional repack |
| [06 Decoder Bridge](L1_06_decoder_bridge.md) → [L2.06](L2_06_decoder_bridge.md) | 1 | L100 singleton |
| [07 split16 Decoder](L1_07_split16_decoder.md) → [L2.07](L2_07_split16_decoder.md) | 1 | Also links the four families in L2.04; local slice is L132 |
| [08 TIN Decoder](L1_08_tin_decoder.md) → [L2.08](L2_08_tin_decoder.md) | 8 | Also links the four tiers of chained in L2.03 |
| [09 B70](L1_09_b70.md) → [L2.09](L2_09_b70.md) | 1 | L155 singleton |
| [10 Output](L1_10_output.md) → [L2.10](L2_10_output.md) | 1 | L156 links to shared copy; local slice is L157 |

The naming conflict in L157 has been adjudicated from the guarded branch in the current release as [HSL-like decomposition and recomposition](L3_b70_history_output.md#postprocess); the numeric roles of the three host scalars are written out as formulas, while their API names remain unknown and local variable names are not upgraded to measured host semantics. The unknown boundary for B69's independent native layout is retained in the [1h outview slice](L2_08_tin_decoder.md#out-32).

~~~text
L0 One Frame  L0_frame.md
├─ L1.01 Pre-Graph Preparation → L2.01 copy / clear
├─ L1.02 B0                    → L2.02 singleton → noise / reprojection / 16 channels / adapter window block / dual exits
├─ L1.03 TIN Encoder           → L2.03 four-tier inpview / chained / ds_wait
├─ L1.04 split16 Encoder       → L2.04 eight families
├─ L1.05 ViT                   → L2.05 repack / expand / contract / qkv / attention / projection
├─ L1.06 Decoder Bridge        → L2.06 L100
├─ L1.07 split16 Decoder       → L2.07 L132 + reuse four families from L2.04
├─ L1.08 TIN Decoder           → L2.08 four-tier upsample / outview + reuse chained from L2.03
├─ L1.09 B70                   → L2.09 L155
└─ L1.10 Output                → L2.10 L157 + L156 reusing copy from L2.01
~~~

## Lower-Level Topic Entries (All Direct to Main Text; Shared Pages Distinguished by Step Anchors)

| Name | What you will trace from this level |
|---|---|
| <a id="l3-qmma-e4m3"></a>[L3.qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3) | Ordered K32 [matrix](APPENDIX_beginner_glossary.md#g051) chains, source line numbers, and current applicability boundaries; candidate adjudication moved to the evidence appendix |
| <a id="l3-b0-noise-reprojection"></a>[L3.b0-noise-reprojection](L3_b0_input.md#b0-noise-reprojection) | Five steps of B0: noise, 16 channels, [5-tap](APPENDIX_beginner_glossary.md#g029), adapter window block, and full / pool |
| <a id="l3-input-adapter"></a>[L3.input-adapter](L3_b0_input.md#adapter) | B0's 16 channels and half adapter matrix |
| <a id="l3-ffn"></a>[L3.ffn](L3_ffn.md#ffn) | Exact single-input G, cross-family matrix/channel accounting, residual seed, and real C++ worked evaluation |
| <a id="l3-tin-window"></a>[L3.tin-window](L3_tin_window.md#tin-window) | 44 full TIN blocks: windowing origins, FFN-first order, residual seed, and four-tier encoder/decoder periphery |
| <a id="l3-window-attention"></a>[L3.window-attention](L3_split16_window.md#window-attention) | Four-kernel full split16 block, 16-head windowing, 1080 logical roles vs. physical byte contracts, and encoder/decoder tail variants |
| <a id="l3-attention-softmax"></a>[L3.attention-softmax](L3_attention_softmax.md#attention-softmax) | Global/window score transforms, half denominator, RCP, value aggregation, and L62 zero-overwrite |
| <a id="l3-tin-norm"></a><a id="l3-norm-nonfinite"></a>[L3.norm-nonfinite](L3_norm_nonfinite.md#norm-nonfinite) | Intra-head sum of squares, RSQ, [scale](APPENDIX_beginner_glossary.md#g031), and [A1](APPENDIX_beginner_glossary.md#g107) nonfinite boundaries |
| <a id="l3-noise"></a>[L3.noise](L3_b0_input.md#noise) | [Integer hash](APPENDIX_beginner_glossary.md#g075) and three-channel noise; storage encoding in the CPU appendix |
| <a id="l3-temporal-sampling"></a>L3.temporal-sampling | Enter [B0 feature reprojection](L3_b0_input.md#coordinates) and [B70 raw history sampling](L3_b70_history_output.md#b70-temporal) separately |
| <a id="l3-repack"></a>[L3.repack](L3_workspace_map.md#repack) | Bidirectional closed forms, acceptance domain, logical / physical rows, and extra zero-writes |
| <a id="l3-workspace-map"></a>[L3.workspace-map](L3_workspace_map.md#workspace-map) | Role layout, CumWrites(L), fills, L62 zero-overwrite, data-driven address tables, and WR A/B |
| <a id="l3-b70-history-output"></a>[L3.b70-history-output](L3_b70_history_output.md#b70-history-output) | B70, L156, L157, carry / [reset](APPENDIX_beginner_glossary.md#g032), and named multiframe gates |
| <a id="l3-output-temporal"></a>[L3.output-temporal](L3_b70_history_output.md#b70-mix) | B70 prediction, confidence weight, and history blending |
| <a id="l3-postprocess"></a>[L3.postprocess](L3_b70_history_output.md#postprocess) | [HSL](APPENDIX_beginner_glossary.md#g033)-like color chain, host scalar effects, and display compositing |
| <a id="l4-half-fma"></a><a id="l4-half-arith"></a>[L4.half-arith](L4_half_arith.md#half-arith) | F16 bit format, two-stage FMA, integer equivalence proof, ordered accumulation, and F32 conversion boundaries |
| <a id="l4-mufu"></a>[L4.mufu](L4_mufu.md#mufu) | Seven-family uses, acceptance domains, and edge semantics; measurements and encodings in the appendices |
| <a id="l4-fp32-ftz"></a>[L4.fp32-ftz](L4_fp32_ftz.md#fp32-ftz) | Full-chain F32 entry/exit points, RN/RZ/satfinite, per-path FTZ and guards, strict compilation, and real C++ conversion examples |
| <a id="l4-e4m3"></a><a id="l4-e4m3-format"></a>[L4.e4m3-format](L4_e4m3_and_k32.md#e4m3-format) | Byte format, subnormals, special values, and [activation](APPENDIX_beginner_glossary.md#g045) saturating quantization |
| <a id="l4-qmma-k32-accumulation"></a>[L4.qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation) | [field F25](APPENDIX_beginner_glossary.md#g066), full K32, 65520 guard, and executable synthetic examples |
| <a id="l4-hmma"></a>[L4.hmma](L4_hmma.md#hmma) | F16 operands, K16 common grid, seed, and step-by-step publication; cross-architecture comparison and negative-zero counterexamples listed separately |
| <a id="l4-tex-filter"></a>[L4.tex-filter](L4_tex_filter.md#tex-filter) | 1/256 fixed-point subpixel grid, joint 8-bit fractional weights, shared-exponent truncation, and texture half midpoints |
| <a id="l4-cross-arch"></a>[L4.cross-arch](L4_cross_arch.md#comparison) | Primitive differences between sm_120 and earlier GPUs, CPU backend schemes, and actual byte-gate boundaries |

## Topic Inventory and Arithmetic Drill-Down Boundaries

All originally planned pages now have main text; this means only that the planned pages have been written, not that every primitive has an independent arithmetic leaf. Texture filtering now has an independent L4 page; still missing are an independent L4 page for integer coordinate hashing / bit mixing (currently in L3 B0) and a complete independent semantic proof for cross-position exchange / provenance mapping (currently in L3 workspace; it is also more than just an arithmetic problem). These gaps are not closed by page count.

The [complete mapping table of pages and same-page steps](APPENDIX_evidence_history.md#topic-inventory) has been moved to the maintenance appendix; arithmetic navigation remains in the table above.

Completing the main text does not change evidence strength: general maps, arbitrary inputs/geometries, synchronization/[aliasing](APPENDIX_beginner_glossary.md#g092)/lifetime, uniqueness of internal values, and unmeasured wrappers remain scoped as stated on each page. The parameter-change 156-launch route and p5 reset/temporal behavior have obtained named results on independent child candidates below; M/M2 do not expand their domain, and the 312 B post_block remains REFUSED/NOT_RUN.

<a id="param-change-r04h"></a>
## Parameter Branches

p5 alters the conditioning channels and reads the previous-frame state when history is valid; the 156-launch route omits the base backup and separate display postprocessing, and S157 executes the same color chain under exact control tuples—see [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).

[Evidence History and Identity Ledger](APPENDIX_evidence_history.md) holds candidate adjudications, proof counts, full SHAs, and receipts; [CPU Storage](APPENDIX_cpu_storage.md) holds lossless encodings, asset layouts, and loading details. Arithmetic rounding, rejection conditions, and unknowns remain in each topic's main text.
