# L3.norm-nonfinite: 32-Channel Vector Norm, Scaling, and Nonfinite Boundaries

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start intro -->
<a id="beginner-norm"></a>
[Synthetic Concept Example, Not a Measurement] The sum of squares of (3,4) is 25 and its length is 5; multiplying both by 1/5 gives (0.6,0.8). Replacing the input with (6,8) doubles the length as well, and [scaling](APPENDIX_beginner_glossary.md#g031) the pair as a whole still yields the same direction. This uses only two items and ideal real numbers to illustrate "rescaling the magnitude of a group of numbers," without impersonating the actual 32-item and [function-table](APPENDIX_beginner_glossary.md#g074) results.

The actual step performs sum-of-squares scaling on each group of 32 items for Q and K separately only after [projection](APPENDIX_beginner_glossary.md#g038), and does not do so for V; it neither subtracts the [mean](APPENDIX_beginner_glossary.md#g044) first nor adds ε to the sum of squares, instead taking a prescribed lower bound. Another scale for the [query](APPENDIX_beginner_glossary.md#g040) is multiplied separately afterward and cannot be merged into a single knob. [Nonfinite](APPENDIX_beginner_glossary.md#g069) propagation, the exact addition tree, and the independent [A1](APPENDIX_beginner_glossary.md#g107) branch remain below.
<!-- beginner-r04m:end intro -->

[Full Skewer Index](INDEX.md) · Parent level: [TIN](L2_03_tin_encoder.md), [split16](L2_04_split16_encoder.md#qkv), [ViT QKV](L2_05_vit.md#qkv), [B70](L2_09_b70.md) · Adjacent step: [attention](L3_attention_softmax.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| x₀…x₃₁ | 32 [half](APPENDIX_beginner_glossary.md#g054) components within one position and one head |
| s, n, ε | Sum of squares, statistic after lower-bound clamping, and lower-bound constant |
| r, γ | half reciprocal square root and post-[normalization](APPENDIX_beginner_glossary.md#g043) multiplicative scale |
| i,l,u,a | Local [reduction](APPENDIX_beginner_glossary.md#g050) / fetch indices within formulas, with ranges given at each formula |

In the pseudocode on this page, `T_RSQ(x)` is shorthand for the [MUFU numeric wrapper](L4_mufu.md#value-wrapper), returning the decoded F32 numeric value of the certified result; `F32(n)` is the exact expansion of the half value. Extracting the bit pattern and decoding add no rounding and preserve the sign of zero; this does not require runtime indexing directly by raw32—the small half table of B0/TIN already pre-incorporates RN16 of that result, and the [per-family interfaces and acceptance domains](#affine) remain preserved.

<a id="norm-nonfinite"></a>
### L3.norm-nonfinite 32-Channel Sum-of-Squares Normalization per Position and per Head

- What it is: Computes the intra-head length from the half components of the QKV projection, and after [RSQ](APPENDIX_beginner_glossary.md#g072) and scaling [publishes](APPENDIX_beginner_glossary.md#g091) the [E4](APPENDIX_beginner_glossary.md#g055) bytes of Q/K.
- Input → output: 32 half values at the same t and same h → 32 normalized half values → E4; C=32/64/128/256 for [TIN](APPENDIX_beginner_glossary.md#g011), C=[512](APPENDIX_beginner_glossary.md#g007) for [split16](APPENDIX_beginner_glossary.md#g013), C=1024 for [ViT](APPENDIX_beginner_glossary.md#g014), and C=32 for B0/B70.
- How it is computed:
  ~~~text
  1. Take x[0:32] for this position and this head, once for Q and once for K.
  2. Compute s using this family's fixed half squaring / fusion / addition tree.
  3. n=max(s,ε), with ε=half(0x0410); ε is not added to s.
  4. r=RN16(T_RSQ(F32(n))).
  5. For each component, first compute H×(x_i,r), then multiply in order by the prescribed scales for that family.
  6. Publish each half multiplication separately, and finally convert to E4.
  ~~~
- Numeric rules: The statistic is the sum of squares; there is no mean subtraction, variance calculation, or division by 32. The reduction axis is the intra-head channel axis, while the 64 positions of a [window](APPENDIX_beginner_glossary.md#g015) and different heads are each independent. The statistic can [overflow](APPENDIX_beginner_glossary.md#g071) to +Inf from finite components.
- Why it is computed this way: Regulates the intra-head length of Q/K, after which the [query scale](APPENDIX_beginner_glossary.md#g052) controls the subsequent score range; training-time naming cannot substitute for the actual computation graph.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100), [tin.cpp:114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114), [b00.hpp:25, 46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L25), [outtail.cpp:83, 90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L83), and the [data-driven graphs](#map-norm). For native controlled comparisons and CPU diagnostics of nonfinite consequences, see [Evidence](#evidence).
- Next down: [norm32 Tree](#norm32), [split16 / ViT](#map-norm), [Scales and RSQ](#affine), [L6 to A1](#nf-path), [Actual Execution Example](#worked-example).

<a id="norm32"></a>
### L3.norm-nonfinite.norm32 Explicit Reduction in TIN, B0, and B70

- What it is: Splits the 32 channels into four segments of 8 items each; performs local fused sums of squares first, and then merges them in fixed pairs.
- Input → output: One Q or K head [vector](APPENDIX_beginner_glossary.md#g076) x → half statistic n.
- How it is computed:
  ~~~text
  For i=0,…,7:
    a_i = HF(x_i,x_i,H×(x_(16+i),x_(16+i)))
    b_i = HF(x_(8+i),x_(8+i),H×(x_(24+i),x_(24+i)))
    t_i = H+(a_i,b_i)
  u_i = H+(t_i,t_(i xor 4))
  v_i = H+(u_i,u_(i xor 2))
  s   = H+(v_0,v_1)
  n   = max(s,ε)
  ~~~
- Numeric rules: The squares of segments 3 and 4 publish half first and then serve as the addends of their respective fused steps; the two fused results each publish half, and every subsequent [H+](APPENDIX_beginner_glossary.md#g063) publishes half again. One can neither accumulate all 32 squares in [F32](APPENDIX_beginner_glossary.md#g056) before converting to half, nor keep both squares in high precision and round only once.
- Lower bound: ε=0.00006198883056640625, with [encoding](APPENDIX_beginner_glossary.md#g057) 0x0410, taken from a code constant. It is a lower bound on s, not an undisclosed coefficient inside the model [resource](APPENDIX_beginner_glossary.md#g079); an all-zero group uses this lower bound, and its output remains zero.
- Why it is computed this way: Fixed pairing specifies the association order of the half addition tree, and changing the pairing can change step-by-step rounding; training motivations are unknown.
- How we know: CENSUS, [tin.cpp:115–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L115), [b00.hpp:25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L25), [outtail.cpp:83](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L83); the corresponding Python tree is in [sm120_b1.py:357–371](../../../mlxdlss/sm120_b1.py#L357).
- Next down: [RSQ and Multiplicative Scales](#affine), [Overflow Instance](#nf-path); proofs and edge rules for half primitives are traced to [L4.half-arith](L4_half_arith.md).

In TIN, the [call](APPENDIX_beginner_glossary.md#g080) index for Q is t·3C+32h+i, with K adding C on top of that; V adds 2C and is [quantized](APPENDIX_beginner_glossary.md#g061) directly without passing through this tree. B0 and B70 each have only a single 32-channel head. The same tree in B70 sits after [feed-forward](APPENDIX_beginner_glossary.md#g037) and before [attention](APPENDIX_beginner_glossary.md#g039) scores; normalization of [history](APPENDIX_beginner_glossary.md#g024) [sampling](APPENDIX_beginner_glossary.md#g027) weights belongs to a separate RCP path and must not be confused with the Q/K statistic. Corresponding calls: [tin.cpp:119–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119), [b00.hpp:44–46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L44), [outtail.cpp:90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L90); for the subsequent weight path, see [L3.attention-softmax](L3_attention_softmax.md#window-attention).

<a id="map-norm"></a>
### L3.norm-nonfinite.map split16 and ViT: Interpret the Provenance Tables First, Then the Reduction

- What it is: Uses the [frozen](APPENDIX_beginner_glossary.md#g103) graph to determine the sources, fusion direction, and merge order of the 32 components; the generic C++ executor does not by itself prescribe a complete norm.
- Input → output: Internal half values of split16 fused qkv, or the merged half partial-sum results of ViT QKV → per-head Q/K statistics and E4 publication.
- How it is computed: Denote the four fetch groups in the graph by x[a,l,u] with a=0…3, l=0…3, u=0/1, giving 32 components in total. The formula below uses the fetch order of this graph:
  ~~~text
  pair(a,b) = HF(a,a,H×(b,b))
  t[l,u] = H+(pair(x[0,l,u],x[1,l,u]),
               pair(x[2,l,u],x[3,l,u]))
  v[l,u] = H+(t[l,u],t[l xor 2,u])
  w[l,u] = H+(v[l,u],v[l xor 1,u])
  s      = H+(w[0,0],w[0,1])
  n      = max(s,ε)
  r      = RN16(T_RSQ(F32(n)))
  ~~~
- Index structure: a,l,u are intra-graph provenance coordinates and do not directly equal [logical](APPENDIX_beginner_glossary.md#g085) contiguous channel indices. split16 also executes the instance's window shift and position selection; in ViT, x comes from the half merge of the final [matrix](APPENDIX_beginner_glossary.md#g051) slice result with the saved partial sums. The reduction does not cross [tokens](APPENDIX_beginner_glossary.md#g041) or heads; one cannot delete the provenance tables and retain only tensor shapes.
- Channels of the leaves: traced back from the k-th term of the score K32 that actually consumes Q/K, the leaves of x[a,l,u] are the within-head channels d. Every RSQ root and every lane has its own table: L27 node 5842/lane 0 reduces K[token0,·]; at l=0,u=0 the terms a=0..3 read d=2, 18, 0, 16, and at l=2,u=0 they read d=10, 26, 8, 24; the next root, node 5843, starts with d=3, 19, 1, 17, so the first root must not be copied. Reduce with the pair/XOR tree above; do not sort by d and substitute a library sum. The global window and head still come from the instance source tables; at 1080 the 655,360 reduction groups (including in-warp replicas) show 0 mismatches. [F04 check](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)
- Numeric rules: The frozen fusion [contract](APPENDIX_beginner_glossary.md#g101) of split16 explicitly selects the first square of pair to be fused while the second square publishes half first; at "additions of two product nodes," ViT adopts fused recomputation in the same direction. All half additions and conversions before and after RSQ remain independent boundaries.
- Why it is computed this way: Intra-tile parallel decomposition serves the matrix output arrangement; CPU loop organization can be optimized while floating-point dependencies and publication order are preserved.
- How we know: CENSUS, [scalar_map.hpp:257–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L257), [qkv_projection_impl.hpp:165–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L165). This round expanded all 32 RSQ input dependencies of L27 and L61 respectively, each containing 32 distinct scalar squares; for the concrete bindings see the [appendix](APPENDIX_evidence_history.md#norm-bindings).
- Next down: [Per-Family Scales](#affine), [Scoped Changes in A1](#a1); for matrix partial sums and primitive details, see [L3.qmma-e4m3](L3_qmma_e4m3.md) and [L4.half-arith](L4_half_arith.md).

[CPU Reconstruction / CENSUS] [Concrete graphs/contracts, sources, and SHA bindings](APPENDIX_evidence_history.md#norm-bindings) have been moved. In split16 L27, RSQ belongs to Q/K and RCP belongs to the subsequent attention [denominator](APPENDIX_beginner_glossary.md#g048); the remaining inspected prototype graphs for L25/26/28/29/30/56/57 contain no RSQ/RCP nodes. The boundary between legacy [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) entries and named admitted instances is retained, and graph/source agreement is not upgraded to a general map proof across all geometries.

<a id="affine"></a>
### L3.norm-nonfinite.affine Actual Formats of RSQ, Lower Bound, and Scales

- What it is: Looks up the native RSQ [bit pattern](APPENDIX_beginner_glossary.md#g057) for a positive statistic that is already half, then converts back to half, multiplies by scales, and converts to E4 at explicit positions.
- Input → output: half encoding of n → F32 encoding of the RSQ table entry → half r → normalized exit.
- How it is computed:
  ~~~text
  1. n=max(s,half(0x0410)); check the acceptance domain of the current wrapper.
  2. Expand F32(n) exactly, and select the RSQ table entry using the encoding of n.
  3. r=RN16(F32 value of the table entry).
  4. Compute H×(x_i,r) first, then complete the scale multiplications for Q according to the table below; K is not multiplied by the query scale.
  5. Publish half after each H×, and finally publish E4; there is no post-normalization β addition.
  ~~~
- Numeric rules: The directly verified split16 L27/L31 sites use the F32 [FTZ](APPENDIX_beginner_glossary.md#g068) wrapper of [MUFU](APPENDIX_beginner_glossary.md#g073) RSQ; other families fetch captured bit patterns from their respective bound half-domain RSQ tables without assuming a wrapper form from function names alone. Even if a finite nonzero half is subnormal, expanding it to F32 produces a normal number; one cannot flush half subnormals to zero across the board on that basis. Here the lower bound further restricts finite inputs of RSQ to ≥0x0410.
- Why it is computed this way: The source code fixes the numeric contract of reciprocal square root to the original table; approximate equality with generic sqrt/division does not constitute bit-for-bit equality.
- How we know: CENSUS / MEASURED, [half MUFU semantics:7–19](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/SEMANTICS_ZH.md#L7), [legacy table boundary JSON](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/s11-old-table-boundary.json); for representations and [full-domain](APPENDIX_beginner_glossary.md#g111) measurement scope, see [L4.mufu](L4_mufu.md#representation).
- Next down: [+Inf Acceptance Domains Across Wrappers](#a1), [Actual Example](#worked-example).

| Family | Step-by-step publication formula for Q | K / V and scale sources |
|---|---|---|
| TIN | Q_i=Q8(H×(H×(x_i,r),γ_h)) | γ_h is stored as per-head F32 in the model resource and rounded via [RN16](APPENDIX_beginner_glossary.md#g059) when loaded; K is Q8(H×(x_i,r)), and V is converted directly to E4. Source: [tin.cpp:34–51, 114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34) |
| split16 | Q_i=Q8(H×(H×(x_i,r),γ_h)) | Four-byte resource scale converted via F32→half; position/head selected by map; K has no such scale. Byte read and conversion: [scalar_map.hpp:252, 274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L252), actual order in the L27 graph |
| ViT | Q_i=Q8(H×(H×(H×(x_i,r),5.65625),γ_h)) | 5.65625 is a fixed half constant in the graph; γ_h is a per-head F32 resource scale rounded via RN16 first. K is only Q8(H×(x_i,r)); V is converted directly to E4 after a layout transform, and neither has the extra factors of Q |
| B0 / B70 | Q_i=Q8(H×(H×(x_i,r),γ)) | Single-head F32 resource scale rounded via RN16 first; K multiplies only by r. Sources: [b00.hpp:18, 46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L18), [outtail.cpp:85, 90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L85) |

Scale numeric values are not listed in this text. γ is stored as F32 and participates in multiplication as half; the QKV matrix coefficients are E4, so the matrix-coefficient format cannot be treated as the normalization-scale format. Upstream linear transformations, [bypasses](APPENDIX_beginner_glossary.md#g016), and subsequent attention biases do not act as a β here either.

5.65625=RN16(√32), with encoding 0x45a8; [real half_round evaluation](../skewer/examples/anatomy_r04i.result.json) verifies this identity. Ideally, without a lower bound or rounding, multiplying an [L2 unit vector](APPENDIX_beginner_glossary.md#g053) by √32 yields a scale with RMS equal to 1; here that factor multiplies only Q while K still follows its own formula, rather than changing both statistics into mean squares. The three half multiplications are each published separately and cannot be merged into a single combined F32 scale; the training intent behind choosing this query scale is unknown.

<a id="nf-path"></a>
## Positive-Statistic Overflow and Interface Rejection

[CPU Reconstruction] Half squaring and positive-number summation on finite inputs can overflow to +Inf. The ε lower bound does not eliminate +Inf; the original TIN table supports RSQ(+Inf)=[+0](APPENDIX_beginner_glossary.md#g070), which can absorb a finite vector into signed zero. Inf×0 is not part of this derivation, and NaN and other primitives still enforce their respective guards.

<a id="a1"></a>
[Verification Record] The finite-domain wrappers of split16/ViT in default M2 reject this statistic; the independent A1 branch admits the scoped RSQ(+Inf)=+0 and named statistic paths while still retaining the [QMMA](APPENDIX_beginner_glossary.md#g065) half overflow rejection, without updating public M2. 027/028 are image sample IDs in the diagnostic reports, not layer numbers; [propagation witnesses, branch source code, and acceptance counts](APPENDIX_evidence_history.md#norm-propagation-detail) have been moved to the appendix.

[Native Behavior / Unknown] CPU witnesses do not prove that the native network internally produces the same temporary Inf; each branch constrains only its saved compared objects and input domains.

<a id="evidence"></a>
## Evidence and Unknowns

[Verification Record] The standalone RSQ(+Inf)=+0 raw value, local CPU propagation, helper threshold controls, A1 checkpoints, and [FINAL](APPENDIX_beginner_glossary.md#g105) comparisons are distinct tiers; [named files / denominators / counts](APPENDIX_evidence_history.md#norm-evidence) have been moved. The six [C8](APPENDIX_beginner_glossary.md#g109) textures of A1 remain NOT_RUN_RAW_FILES_ABSENT; legacy per-launch finite paths do not count as new A1 gates or proofs across all inputs.

General multi-operand half combinations, NaN payload rules, nonfinite counts in unobserved intervals, and whether intermediate Inf/NaN are reachable inside the [GPU](APPENDIX_beginner_glossary.md#g078) network remain UNKNOWN; "native execution internally produces +Inf and absorbs it" remains INFERRED. Having measured a standalone function key does not mean the measured network actually reaches it internally.

<a id="worked-example"></a>
### L3.norm-nonfinite.example Directly Executing One 32-Channel Group with Repository Functions

- What it is: Executes the real reference functions rather than merely listing a theoretical sum of squares in the main text.
- Input → output: Synthetic vector [1,−2,3,−4,0,…,0] of 32 items in total, and synthetic scale γ=1; obtains the statistic, native RSQ table entry, and normalized half values.
- How it is computed: The appendix script extracts only the three original functions _norm_squared, _rsq, and normalise from the file AST; it neither imports the model or other modules nor reads weights.
- Numeric rules: The squares and fused intermediates for this group are exactly representable; RSQ and half multiplications execute according to the original functions. It verifies the numeric values for this group without claiming to cover all FMA inputs.
- Why it is computed this way: Simultaneously distinguishes the actual statistic, the length deviation of the published vector, the all-zero lower bound, and the difference between "the table contains a +Inf entry" and "the wrapper rejects it."
- How we know: The original writing round executed the appendix code directly, verifying SHAs for both the source and the RSQ asset; no new GPU, full-network, or continuous-chain runs were added.
- Next down: Bottom of this branch; for the final E4 encoding rules, see [L4.e4m3 / K32](L4_e4m3_and_k32.md#e4m3-format).

Run from the repository root; the code requires only the standard library and NumPy:

[Complete script and certified SHAs](APPENDIX_evidence_history.md#norm-example) have been moved to the appendix; the original execution output is retained below, and the original run scope is in the evidence appendix.

Actual output: s=n=30, with half encoding 0x4f80; the F32 encoding of RSQ is 0x3e3af4ba, and after RN16, r=0.1826171875 with encoding 0x31d8. The first four normalized half values:

| Synthetic x_i | Normalized half | half encoding |
|---:|---:|---|
| 1 | 0.1826171875 | 0x31d8 |
| −2 | −0.365234375 | 0xb5d8 |
| 3 | 0.5478515625 | 0x3862 |
| −4 | −0.73046875 | 0xb9d8 |

Summing the squares of the published half values in real numbers yields 1.0004711151123047; half normalization does not guarantee that the final length is exactly 1. The statistic of an all-zero group is clamped to ε. A synthetic vector of 32 entries all equal to 48 causes this tree to overflow to +Inf at the final H+(36864,36864); the unmodified reference _rsq faithfully rejects it even though the raw +Inf→+0 value on the last line of the asset is already present. The A1 admission is the new branch specified above, and the example does not silently modify legacy guards.
