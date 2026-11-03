# L3.attention-softmax: Scores, Denominator Reduction, and Value Aggregation

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start intro -->
<a id="beginner-attention"></a>
[Beginner Simplification] The current position uses Q to compare against candidate positions' K, and then fetches their V content according to the resulting [shares](APPENDIX_beginner_glossary.md#g048); Q/K/V are all generated from internal numbers. First use the [3-position story and side-by-side score table](L1_00_one_block_primer.md#qkv-story) to understand what is compared and what is retrieved. Standard [softmax](APPENDIX_beginner_glossary.md#g047) takes the [exponential](APPENDIX_beginner_glossary.md#g047) first and then divides by the total; this chain first modifies the [encoding](APPENDIX_beginner_glossary.md#g057) by a prescribed rule to generate positive [weights](APPENDIX_beginner_glossary.md#g048), with undetermined training intent. [Window](APPENDIX_beginner_glossary.md#g015) attention performs "divide by total → convert to coarse format → combine V", whereas global attention performs "convert to coarse format → combine V → divide by total", with the [2 4-box lines](L1_00_one_block_primer.md#quantisation-position) marking the conversions; this is not a real-number average whose steps can be swapped at will.
<!-- beginner-r04m:end intro -->

[Full Skewer Index](INDEX.md) · Parent level: [ViT Global attention](L2_05_vit.md#attention), [split16 qkv / proj](L2_04_split16_encoder.md#qkv), [TIN Encoder](L2_03_tin_encoder.md), [TIN Decoder](L2_08_tin_decoder.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| φ, w, p | Score positive kernel, un-[normalized](APPENDIX_beginner_glossary.md#g048) [half](APPENDIX_beginner_glossary.md#g054) weight, and normalized half weight |
| Den, r, accAV | half denominator, half reciprocal, and value-aggregation half [accumulator](APPENDIX_beginner_glossary.md#g064) |
| b,l,u | Per-round column block, key pair within a block, and position within a pair |
| N,n | Number of 64-key rounds, and number of padded keys in the final round |

<a id="attention-softmax"></a>
### L3.attention-softmax Shared Interface and Different Publication Positions Across the 3 Attention Types

- What it is: Generates positive weights from Q/K scores of 32 [channels](APPENDIX_beginner_glossary.md#g007) per head, and then aggregates V in a fixed order.
- Input → output: [ViT](APPENDIX_beginner_glossary.md#g014) takes 3 P×1024 B [E4](APPENDIX_beginner_glossary.md#g055) inputs; [split16](APPENDIX_beginner_glossary.md#g013) is an internal [role](APPENDIX_beginner_glossary.md#g084) of the 16-head, 512-channel window block; [TIN](APPENDIX_beginner_glossary.md#g011) is an internal role of the 1/2/4/8-head, 32/64/128/256-channel window blocks. The latter 2 have 64 positions per window.
- How it is computed:
  ~~~text
  1. Fetch Q, K, and V from the respective address maps / window layouts, preserving upstream scaling and E4 publication.
  2. Q32(Q_i, K_j, seed) → half score; ViT seed=+0, window seed=per-head bias.
  3. Apply the specified affine transform, half clamp, and encoding transform to the score → half weight w.
  4. Compute Den using the fixed half addition tree, and obtain r via measured RCP and RN16.
  5. ViT: Q32(Q8(w), V, previous accAV) → accAV; Q8(H×(accAV,r)) → exit.
  6. TIN / split16: Q8(H×(w,r)) → weight; Q32(weight,V,previous accAV) → accAV → Q8(accAV).
  7. Publish according to this family's writeback, zero-overwrite, and completion-flag contracts.
  ~~~
- Numeric rules: None of the 3 paths can be replaced by a single [F32](APPENDIX_beginner_glossary.md#g056) [matrix](APPENDIX_beginner_glossary.md#g051) multiply-add library softmax; ViT's E4 weights are formed before dividing by the denominator, whereas window E4 weights are formed after dividing by the denominator.
- Why it is computed this way: The encoding transform maps bounded half scores to positive weights, which then [reduce](APPENDIX_beginner_glossary.md#g050) the denominator and aggregate with V; training-time naming and hardware internal implementations are not determined by these interfaces.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100), [attention_impl.hpp:172–238, 243–270](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172), [tin.cpp:108–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108), [scalar_map.hpp:261–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L261); for concrete graph [bindings](APPENDIX_beginner_glossary.md#g103) and native gates, see [Evidence](#evidence).
- Next down: [Layout](#layout), [ViT Scores and Reduction](#vit-score), [Window Path](#window-attention), [Value Aggregation and Publication](#publish), [Worked Calculation Example](#worked-example); primitives trace down to [QMMA](L3_qmma_e4m3.md#qmma-e4m3), [half](L4_half_arith.md#half-arith), and [RCP](L4_mufu.md#representation) respectively.

<a id="layout"></a>
### L3.attention-softmax.layout Logical Matrices and Physical Bytes

- What it is: First translates a [logical](APPENDIX_beginner_glossary.md#g085) "(head, position, channel)" tuple into a [byte offset](APPENDIX_beginner_glossary.md#g083) within the specified role.
- Input → output: ViT's Q/K/V are all E4, but the 3 have different intra-block arrangements; per head, logical Q/K/V are T×32 and [attention](APPENDIX_beginner_glossary.md#g039) scores are T×T. The score matrix is generated tile by tile without requiring full materialization in memory.
- How it is computed: For the verified ViT layout, the offsets below are relative to the role start at 0, all in units of B:
  ~~~text
  Q(t,h,d) =
    16384⌊t/16⌋ + 512h + 64(t mod 8) + 16⌊(d mod 16)/4⌋
    + 8⌊d/16⌋ + 4⌊(t mod 16)/8⌋ + (d mod 4)
  K(t,h,d) =
    16384⌊t/16⌋ + 512h + 64(t mod 8) + 16⌊(d mod 16)/4⌋
    + 8⌊(t mod 16)/8⌋ + 4⌊d/16⌋ + (d mod 4)
  V(t,h,d) =
    32768⌊t/32⌋ + 1024h + 512⌊d/16⌋ + 64(d mod 8)
    + 8⌊(d mod 16)/8⌋ + 16⌊(t mod 16)/4⌋
    + 4⌊(t mod 32)/16⌋ + (t mod 4)
  ~~~
- Index structure: Q/K use 16 positions × 32 channels as their intra-head block; V uses 32 positions × 32 channels as its intra-head block. Two higher-bit axes of Q and K are swapped, while V is arranged separately according to the fetch direction of the value matrix. The parameter pointer order is Q, K, V, output; the measured physical order in the [workspace](APPENDIX_beginner_glossary.md#g082) is Q, V, K, output, so the pointer order cannot be treated as the layout.
- Numeric rules: Address translation does not alter E4 encodings; negative-address sources are interpreted as 0 according to the graph. P=32⌈T/32⌉ and N=⌈T/64⌉; P, 64N, and valid T constrain the role length, tiled fetch range, and logical valid domain respectively.
- Why it is computed this way: Offsets are defined according to the fetch directions of the 2 matrix multiplications respectively; an ordinary contiguous T×1024 reshape would conflate [tokens](APPENDIX_beginner_glossary.md#g041) and channels.
- How we know: CENSUS, [attention_impl.hpp:139–156, 248–257](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L139) defines the fetches and matrix coordinates; [ARCH 0.7:347](../../../ARCHITECTURE_V3_ZH.md#L347) binds the role order; in this round, after checking SHAs against the [frozen T640 bindings](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json), the formulas above were verified item by item across the Q/K/V fetches of the 3 blocks, with 16,384,000 items passing. This is a software address-consistency review with no new native measurements.
- Next down: [Global Loop and Tail Round](#vit-score), [Zero-Overwrite](#padding); window paths are explained under their own independent [contract](APPENDIX_beginner_glossary.md#g101) below.

| Measured ViT geometry | T | P | N | n |
|---|---:|---:|---:|---:|
| 1080 | 640 | 640 | 10 | 0 |
| 1440 | 960 | 960 | 15 | 0 |
| 4K | 2160 | 2176 | 34 | 16 |

The window side cannot apply these 3 ViT formulas. TIN's temporary C++ logical layout is qkv[i,type,intra-head channel]: index i·3C+type·C+32h+d; after normalization, Q/K/V per head are each 64×32, with i=8y+x inside the 8×8 window. Out-of-bounds positions outside the input canvas are zero-padded first, with the window origin bound per instance; this is not equivalent to assigning a negative-infinity score to those keys. In split16, [QKV](APPENDIX_beginner_glossary.md#g040) and attention are fused within the qkv [family](APPENDIX_beginner_glossary.md#g080), where the 16 heads' sources, cross-position selections, shifts, and writebacks are still determined by the map, and the [proj](APPENDIX_beginner_glossary.md#g038) family consumes its exit. Sources: [tin.cpp:119–127, 143–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119), [scalar_map.hpp:250–261, 319–327](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L250); the [L27/L28 graphs](#graph-bindings) give the concrete arithmetic without simplifying fused qkv into 3 contiguous matrices.

<a id="layout-example"></a>
### Real Fetch Substitution for 1 Point

Take t=9,h=0,d=4. The Q formula gives 64×1+16×1+4×1=**84 B**, and the K formula gives 64×1+16×1+8×1=**88 B**; the difference comes from swapping bit 3 of t and bit 4 of d. The V formula gives 64×4+16×2+1=**289 B**. The nonzero terms of Q offset 84=0b01010100 are 64/16/4, those of K offset 88=0b01011000 are 64/16/8, and those of V offset 289=0b100100001 are 256/32/1.

[Real Code / Map Check] The [script](../skewer/examples/substitutions_r04g.py) selects operand bytes according to the row/col/K coordinates of actual attention matrix fetches and reads the SHA-pinned Q/K/V provenance maps, yielding 84, 88, and 289 respectively, identical to the [closed-form](APPENDIX_beginner_glossary.md#g020) substitution. [Results and source identities](../skewer/examples/substitutions_r04g.result.json) preserve the parameters. Only addresses are computed without reading network [activations](APPENDIX_beginner_glossary.md#g045); this is not a new admission for arbitrary maps.

<a id="vit-score"></a>
### L3.attention-softmax.vit-score Global Scores, half Denominator, and Tail-Round Correction (L62/67/72/77/82/87/92/97)

- What it is: All 32 heads share the same computation family, with each query scanning all 64-key rounds.
- Input → output: [Published](APPENDIX_beginner_glossary.md#g091) E4 Q/K/V from L61/66/71/76/81/86/91/96 → half scores, half weights, and per-query half reciprocals; this attention has no weight-matrix operand and no extra attention_scalar arithmetic operand (see the [weights page](L2_weights_layout.md)); do not multiply by it before or after the HF in step 2 below.
- How it is computed:
  ~~~text
  1. score_ij = Q32(Q_i, K_j, +0), head dimension K=32.
  2. c_ij = min(max(HF(score_ij, 0.08953857421875, 1.708984375),
                    1.439453125), 1.9775390625).
  3. φ(score_ij) = half(((bits(c_ij) << 4) + 0x4000) mod 65536).
  4. Reduce each round via the half tree below, with Den_0=+0 and Den_(e+1)=H+(Den_e,S_e).
  5. If n>0: pad_term = RN16(RN32(F32(φ(0)) × F32(n)));
             Den_N = H−(Den_N,pad_term).
  6. Den=max(Den_N,h₀); r=RN16(RCP32(Den)).
  ~~~
- Numeric rules: Step 2 is a half [FMA](APPENDIX_beginner_glossary.md#g063) followed by a half [clamp](APPENDIX_beginner_glossary.md#g049); step 3 is an integer transform on the encoding. The original graph transforms packed words of 2 half values; the single-half formula above holds as a simplification only within the specified clamp interval. The multiplication in step 5 is in F32, converted to half before being subtracted from the half sum; it cannot be moved into the per-item reduction.
- Value of h₀: half 0x0410 (6.198883056640625e-05). It is the constant node c16 6.198883056640625e-05 in the frozen graph (T640 graph node 6787, H2160 graph node 22590; graphs and SHAs under [bindings](#graph-bindings)); it is first packed into two halves, then enters 32 max(Den,·) nodes, and each half of every max goes through tof32 → RCP. It equals the start 0x0410 of the measured RCP table, but here it is bound from the graph node, not inferred from the table start.
- [Scaling](APPENDIX_beginner_glossary.md#g031) position: This kernel multiplies neither by 1/√32 nor by a log₂(e) scale. The norm/model scales of upstream QKV have already entered the E4 inputs; the fixed score slope visible here is the algorithmic constant in step 2. Both [QK](APPENDIX_beginner_glossary.md#g077) scores and AV pass through [QMMA](APPENDIX_beginner_glossary.md#g065) and cannot be computed via HMMA or a single exact real-number dot product.
- Why it is computed this way: Padded zero keys still yield φ(0)>0, so the tail round explicitly subtracts their contribution from the half denominator. When V is zero-padded, no corresponding value numerator is produced.
- How we know: CENSUS, [attention_impl.hpp:172–195, 206–238, 243–270](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172), [frozen reference with matching SHA:68–97, 119–152](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/external-F/src-base/kern_attention_epochfix.py#L68), and [concrete graph bindings](#graph-bindings); the tail-round F32 multiplier in the T2160 graph is actually 16.
- Next down: [Reduction Tree](#sum-order), [Value Aggregation](#publish), [RCP Bit Pattern and Domain](L4_mufu.md#representation).

[CPU Reconstruction / Bit-Field Interpretation] Both clamp intervals lie within [1,2), so the half sign is always 0, the stored exponent is always 15, and the encoding is 0x3c00+m (0≤m<1024). In both transforms on this page, the fixed exponent term and offset cancel out modulo 65536, leaving m<<4 and m<<5 respectively as the **new half encodings**; the high bits of the original mantissa enter the new exponent field, and the low bits become the new mantissa. This varies linearly within each exponent bin and scales by powers of 2 across bins, exhibiting an exponential shape; it neither multiplies the numeric value c directly by 16 or 32 nor computes an exact exp.

For example, synthetic c=1.5 has encoding 0x3e00 and m=512; the ViT transform yields 0x2000, i.e., 0.0078125, while the window transform yields 0x4000, i.e., 2. Clamping makes this bit-field simplification and positive finite range hold, and changing the interval invalidates direct reuse. This explains the [bit-pattern](APPENDIX_beginner_glossary.md#g057) mechanism without borrowing external algorithm names to infer training design; complete numeric behavior remains defined by the respective affine transforms and reductions.

<a id="sum-order"></a>
Here the 64 keys of each round are written according to the 8 consecutive 8-column blocks of QK in that round as w[b,l,u], i.e., key j=64e+8b+2l+u with 0≤b<8, 0≤l<4, u∈{0,1}. Every H+ below immediately publishes half:

~~~text
L(l,u) = H+( H+( H+( H+(w[0,l,u],w[1,l,u]),
                         H+(w[2,l,u],w[3,l,u])),
                    H+(w[4,l,u],w[5,l,u])),
               H+(w[6,l,u],w[7,l,u]))
B(u)   = H+(H+(H+(L(0,u),L(1,u)),L(2,u)),L(3,u))
S_e    = H+(B(0),B(1))
Den_0    = +0
Den_(e+1)= H+(Den_e,S_e), in order e=0,1,…,N−1
~~~

This tree accumulates the **raw half values** of φ, not E4-decoded weights. Round dependencies participate in the final denominator, and exchange sources in the address map also carry the actual round; sources from the final round cannot be copied into earlier rounds. This round verified all 64 reciprocal-input expressions of the frozen T640 graph, and the expression tree matches the formula above item by item; T2160 runs 34 rounds of the same tree and then subtracts the tail-round padding term. The original graph's [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) status is retained, as software expansion alone does not upgrade map admission; actual byte gates are listed separately in [Evidence](#evidence).

**Step-by-step differences from textbook softmax:** There is no "subtract the row maximum score", no ex2 or exp call, and no log₂(e) multiplication. The max/min on score is a fixed lower/upper-bound clamp, and the max before the reciprocal is the denominator lower bound h₀. φ is produced via a half encoding transform; it does not possess the exact shift invariance of mathematical exp. The half denominator, measured [RCP](APPENDIX_beginner_glossary.md#g072), [RN16](APPENDIX_beginner_glossary.md#g059), and E4 and AV publications continue to introduce specified roundings. The above is code behavior; "intended to approximate softmax" is only [Speculation].

<a id="window-attention"></a>
### L3.attention-softmax.window 64-Key Windows: Different Affine Precisions in TIN vs. split16

- What it is: Window blocks such as TIN [chained](APPENDIX_beginner_glossary.md#g022) indeed contain attention; split16's qkv family fuses Q/K/V generation and attention, while proj is the subsequent output projection.
- Input → output: Q/K/V are 64×32 per head; Q and K are each normalized by their own 32-channel vector norm, with Q then multiplied by the per-head scale and converted to E4; V is converted to E4 from the QKV half result. Model scale values for Q are not listed in this text.
- How it is computed:
  ~~~text
  1. Q=Q8(H×(normalized Q, RN16(per-head F32 scale))); K=Q8(normalized K).
  2. score_ij=Q32(Q_i,K_j,per-head/per-position half bias).
  3. TIN: c=RN16(RN32(RN32(F32(score)×0.044921875)+1.30078125)).
  4. split16: c=HF(score,0.044921875,1.30078125).
  5. c=min(max(c,1.03125),1.5693359375);
     w=half(((bits(c)<<5)+0x8000) mod 65536).
  6. Compute Den via each family's specified half tree; r=RN16(RCP32(Den)).
  7. p_j=H×(w_j,r); weight_byte=Q8(p_j); 2 K32 steps aggregate V.
  ~~~
- Numeric rules: TIN's F32 multiplication and F32 addition are published separately; split16's graph uses a half FMA. They cannot be interchanged on the basis of sharing the same algorithmic constants. TIN's denominator additionally checks that the half encoding lies in [0x1c00,0x60e0]; the split16 graph applies max(Den,h₀) after reduction before looking up RCP.
- Why it is computed this way: Windows restrict the interaction range, and Q's scale and [position bias](APPENDIX_beginner_glossary.md#g052) regulate the distribution of the positive kernel; boundary zero-padding, shifting, and bias indexing are interface facts that cannot be automatically replaced with a generic masked softmax.
- How we know: CENSUS, [tin.cpp:34–51, 108–127, 135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108), [sm120_b1.py:381–421](../../../mlxdlss/sm120_b1.py#L381); the half FMA / RCP semantics of split16 are in [scalar_map.hpp:261–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L261), with the call order taken from the [SHA-pinned L27 graph](#graph-bindings).
- Next down: [2 Window Reduction Coordinates](#window-sum), [Publication](#publish); for the sum of squares inside the vector norm, see [L3.norm-nonfinite (Intra-Head Sum of Squares)](L3_norm_nonfinite.md#norm32).

<a id="window-sum"></a>
In TIN under logical 8×8 window coordinates, letting w[j] have 64 items for each query, the complete tree is:

~~~text
L(b) = H+( H+( H+( H+(w[b],w[b+16]), H+(w[b+4],w[b+20])),
                   H+(w[b+32],w[b+48])),
              H+(w[b+36],w[b+52]))
Den    = H+( H+(H+(H+(L(0),L(2)),L(8)),L(10)),
           H+(H+(H+(L(1),L(3)),L(9)),L(11)))
r    = RN16(RCP32(Den))
~~~

This corresponds to [tin.cpp:124–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L124). split16 uses its own intra-tile column-block coordinates: denoting the transformed scores of the same query across the 8 QK column blocks by w[b,l,u], it computes S via [L(l,u), B(u), and S above](#sum-order), and then Den=max(S,h₀). Here the column order must first be selected according to its cross-position map, **without directly identifying b,l,u with TIN's logical grid index j**; the latter is a distinct reduction coordinate system. The L27 graph has 2 such query sub-tiles whose actual source selections are bound separately, so the exchange source of the 1st position cannot be used fixedly for both. For how the interpreter executes these selections per graph, see [scalar_map.hpp:257–259, 266–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L257). One therefore cannot simply write "sum(w)" and let a library choose the half/F32 precision and association order on its own.

[CPU Reconstruction / Integer Tables Read Directly] The frozen L27 first applies each instance's PS/SI; after that, w[b,l,u] in the tree is the local QK key j=8b+2l+u. With artificial labels W[q,j]: L(0,0) reads j=0, 8, 16, 24, 32, 40, 48, 56 and L(1,0) reads j=2, 10, 18, 26, 34, 42, 50, 58. Each query has its own binding (root 7035/lane 0 is q=0, root 8194/lane 0 is q=32). The full 1080 selection domain and all 4K SI/PS were checked with 0 mismatches. j is a QK column label and must not be taken as the image index 8y+x; the dependency on the other half of the packed word must not be dropped either. [F04 check](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)

<a id="publish"></a>
### L3.attention-softmax.publish Value Aggregation, Projection Boundary, and Writeback

- What it is: Publishes the E4 products of weights and values as half at each K32, and finally forms the E4 exit.
- Input → output: ViT's [Q8](APPENDIX_beginner_glossary.md#g061)(w) or window Q8(p), together with E4 V → half accAV → E4 attention exit; subsequent channel projection belongs to L63 etc. or split16 proj / the back half of TIN window.
- How it is computed:
  ~~~text
  ViT: accAV_0=+0
       By round and 2 K32 steps per round: accAV_(k+1)=Q32(Q8(w)[current 32 keys],V[current 32 keys],accAV_k)
       2N steps in total; out=Q8(H×(accAV_(2N),r)).
  Window: accAV_0=+0
       accAV_1=Q32(Q8(p)[first 32 keys of this graph],V[first 32 keys of this graph],accAV_0)
       accAV_2=Q32(Q8(p)[last 32 keys of this graph],V[last 32 keys of this graph],accAV_1)
       av=Q8(accAV_2), then handed to its own channel projection and residual.
  Writeback: Exclusive compute writeback table → explicit zero-overwrite for this instance (if any) → completion flag.
  ~~~
- Numeric rules: The seed of each Q32 step is the previous step's half; summing all keys in a single high-precision pass before converting to half is not permitted. ViT's r is broadcast across all output channels of the same query; r is not folded into Q8(w) ahead of time. TIN's 2 segments are logical keys 0–31 followed by 32–63; split16 uses the key arrangement bound in its graph. The current ViT wrapper rejects [nonfinite](APPENDIX_beginner_glossary.md#g069) half operation results, nonfinite publications, and out-of-domain RCP inputs; windows handle these via their respective primitive and denominator-domain guards without applying all of ViT's rejection conditions. Overflow and [subnormal](APPENDIX_beginner_glossary.md#g068) contracts follow [L3.qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3) and [L4.half-arith](L4_half_arith.md#half-arith), and do not disappear merely because the denominator is positive.
- Atomic/reduction boundaries: The denominator trees of these attentions are fixed half additions, and AV is a fixed seed chain; there is no half [atomic add](APPENDIX_beginner_glossary.md#g095) that merges attention values in arbitrary order. The split16 compute exit verifies a unique writer byte by byte; ViT's compute exit is likewise byte-by-byte [exact-once](APPENDIX_beginner_glossary.md#g094), and the subsequent zero-overwrite is a separately listed legal rewrite. C++ task-counter atomics are not network numeric atomics. Same-address half partial sums in subsequent ViT projection belong to [ordered half merging](L4_half_arith.md#half-arith) and cannot be used in reverse to reorder attention.
- Why it is computed this way: Restricts numeric accumulation to fixed low-precision interfaces; scheduling of independent output tasks may vary while the rounding order of any single dependency chain remains invariant.
- How we know: CENSUS, [attention_impl.hpp:243–270, 292–334](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L243), [tin.cpp:127, 135, 157–161](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L127), [scalar_map.hpp:303–329](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L303); the MEASURED scope is given in the table below.
- Next down: [4K L62 Zero-Write](#padding), [E4 / K32](L4_e4m3_and_k32.md), [half Publication](L4_half_arith.md), [RCP Table](L4_mufu.md#representation).

<a id="padding"></a>
### L3.attention-softmax.padding The 16×1024 B of 4K L62 Is a Publication Contract

- What it is: After all computed [vectors](APPENDIX_beginner_glossary.md#g076) have been written, explicitly overwrites the exits of the 16 physical padding tokens with 0 before publishing the completion status.
- Input → output: Complete compute exit for T=2160, P=2176 → 16,384 B at local bytes [2211840,2228224) zeroed out; other instances must check their own bindings.
- How it is computed:
  ~~~text
  1. First complete the compute writeback of the entire output.
  2. Verify params, roles, bounds, and stage identity.
  3. Execute 4096 independent 4 B zero-overwrites, covering this 16 KiB exactly once.
  4. Publish release63 only after completing the zero-overwrite.
  5. L63 consumes the published exit according to its own read table, including this padded region.
  ~~~
- Numeric rules: This is a post-computation overwrite, neither adding a [mask](APPENDIX_beginner_glossary.md#g006) to the scores nor merely pre-zeroing a newly allocated CPU buffer; ordinary computation writes to these positions again. Subtracting padded keys from the tail-round denominator and zero-overwriting the exit are 2 separate things.
- Why it is computed this way: The reconstructed exact read set of L63 reads all 16 KiB, with each byte read 16 times; retaining the computed nonzero padding values would feed them into the subsequent projection. It cannot be treated as dead space.
- How we know: MEASURED / CONTROLLED, [diag-L062/RESULT_ZH.md:5–15](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/diag-L062/RESULT_ZH.md#L5); CENSUS, [vit_adapter_geometry_padded_zstore.py:166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166) explicitly specifies compute output → zero-overwrite → completion flag; for the disabled-[negative-control](APPENDIX_beginner_glossary.md#g102) test, see [c12/RESULT_ZH.md:7](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7).
- Next down: This slice explains only the portion required for attention publication; the complete read/write [lifetime](APPENDIX_beginner_glossary.md#g092) remains in [L3.workspace-map](L3_workspace_map.md#write-sets).

For the correspondence between early event counts and current zero-overwrite items, see [padding history](APPENDIX_evidence_history.md#padding-bug).

<a id="graph-bindings"></a>
## Binding Behavioral Explanations to Frozen Graphs

[CPU Reconstruction / CENSUS] Generic executors define the primitives, while concrete [DAGs](APPENDIX_beginner_glossary.md#g089) define the order; ViT's half affine transform, encoding transform, denominator rounds / tail subtraction, and post-AV scaling, as well as split16's affine transform / reduction / RCP / weight publication and post-projection, are each verified against named graphs. [Graph and binding files, full SHAs](APPENDIX_evidence_history.md#attention-bindings) have been moved; no new all-geometry symbolic admission or complete [ROLE](APPENDIX_beginner_glossary.md#g105) lifetime proof is claimed.

<a id="evidence"></a>
## Scope of Saved Verifications

[Verification Record] Gates are listed by compared object, and legacy failures or unmeasured entries are not overwritten by later chain results:

| This assertion | Direct observation / source reading | Compared object and scope | What it cannot prove |
|---|---|---|---|
| attention execution graphs match named outputs | Per-launch native/Python/C++ comparisons and bound arithmetic graphs | ViT, split16, and TIN each per registered launches and geometries; [details](APPENDIX_evidence_history.md#attention-evidence) | Does not backfill legacy NOT_RUN entries or close general map proofs |
| L62 zero-overwrite cannot be omitted | Disabling the negative control yields workspace differences while the 6 [textures](APPENDIX_beginner_glossary.md#g027) remain identical | Registered 4K L62 and its successor read set | Six-POST cannot substitute for FULL, and a zero value in a snapshot cannot prove a zero-write occurred |
| Later chain results coexist with legacy gates | Fixed builds, own checkpoints, and native output controlled comparisons | [Legacy 1 B difference, map statuses, and build boundaries](APPENDIX_evidence_history.md#attention-scope-detail) | Does not upgrade saved-chain agreement to unique internal timing or an all-input theorem |

There is no named negative control that can be cited from the original registry as a "[libm](APPENDIX_beginner_glossary.md#g074) softmax replacement"; the synthetic example below illustrates the actual algorithm without impersonating such a hardware negative control.

<a id="worked-example"></a>
### L3.attention-softmax.example Actually Running 1 Row of 64 Scores

- What it is: Evaluates only TIN's score → denominator → half normalization → E4; inputs are entirely synthetic, without reading model weights or network targets.
- Input → output: [-8,-4,-2,-1,0,1,2,8] repeated 8 times, forming a 64-key synthetic half score row.
- How it is computed: Run the appendix Python from the repository root; uses only the standard library and NumPy to read the captured small RCP table, without importing the model.
- Numeric rules: Follows the TIN order above; the affine intermediates for this input set are exactly representable, which also verifies that its score transform produces the same result as the split16 path here; this does not prove the 2 affine paths are identical across arbitrary half inputs.
- Why it is computed this way: Simultaneously demonstrates clamping, positive weights, the half denominator, measured RCP, and E4 [underflow](APPENDIX_beginner_glossary.md#g071); the textbook comparison serves only to illustrate the difference.
- How we know: The original writing round executed the appendix code directly; asset SHAs are fixed, and the numbers below are execution outputs rather than a new [GPU](APPENDIX_beginner_glossary.md#g078) or full-attention acceptance.
- Next down: Bottom of this branch; for a runnable example of QMMA itself, see [L4.e4m3 / K32](L4_e4m3_and_k32.md).

[Complete script and certified SHAs](APPENDIX_evidence_history.md#attention-example) have been moved to the appendix; the original execution output is retained below, and the original run scope is in the evidence appendix.

This yields Den=80.375 with encoding 0x5506; the F32 encoding of RCP is 0x3c4bd830, which converts to half r=0.01244354248046875 with encoding 0x225f. Each synthetic score appears 8 times:

| Synthetic score | w | p=H×(w,r) | Q8(p) encoding |
|---:|---:|---:|---:|
| −8 | 0.00006103515625 | 0.0000007748603820800781 | 0x00 |
| −4 | 0.000457763671875 | 0.0000057220458984375 | 0x00 |
| −2 | 0.00341796875 | 0.000042557716369628906 | 0x00 |
| −1 | 0.00927734375 | 0.00011545419692993164 | 0x00 |
| 0 | 0.025390625 | 0.0003159046173095703 | 0x00 |
| 1 | 0.06640625 | 0.0008263587951660156 | 0x00 |
| 2 | 0.1875 | 0.0023326873779296875 | 0x01 |
| 8 | 9.75 | 0.121337890625 | 0x20 |

Summing the 64 published p values in ordinary real arithmetic gives 0.9998188018798828, not an exact 1; the actual code does not perform another forced renormalization either. In standard softmax on the same scores, each score=8 item is about 0.12451424958522991, differing from the half result of this path by about 0.00317636. This difference comes from the explicit algorithm and rounding, and is not used to attribute arbitrary native mismatches.

<a id="parallel-av-example"></a>
## Same Synthetic Scores and Values: ViT and Window Computed Side by Side Through AV

[CPU Reconstruction / Actual Execution] The [script](../skewer/examples/attention_av_r04f.py) uses the same 64-item score row and a value vector of [1,−1,2,−2,4,−4,8,−8] repeated 8 times, showing 1 output channel; it directly executes the source half/E4 functions and the real QMMA K32 function, while RCP reads the certified function table. Starting from synthetic scores here, it runs neither QK, the model, nor a full attention launch; the 64-key ViT pass is only a 1-round primitive demonstration, not an admitted network geometry.

| Path | F16 encodings of denominator D / reciprocal r | First 8 E4 weights actually sent to AV | F16 after 2 K32 steps | Exit E4 |
|---|---|---|---|---|
| ViT: E4(w)×V then multiply by r | 4d32 / 2a29 | 02 02 06 0f 1b 26 32 3d | d448 | c5 (−3.25); H×(AV,r) first, then Q8 |
| TIN window: H×(w,r) first, then E4×V | 5506 / 225f | 00 00 00 00 00 00 01 20 | c7e0 | d0 (−8); Q8 directly after AV |

The 2 paths each use their own φ and half reduction tree, so their denominators also differ; the final difference cannot be attributed entirely to the quantization position. This example marks every real position so readers following the ViT path can verify "E4(w) first, multiply by r afterward." [Original stdout, source/function-table SHAs, and strict compilation flags](../skewer/examples/attention_av_r04f.result.json) preserve the full identity; this does not upgrade any legacy NOT_RUN or map admission status.
