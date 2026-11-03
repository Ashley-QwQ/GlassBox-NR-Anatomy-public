# L4.half-arith: F16 Arithmetic, Two-Stage FMA, and Ordered Publication

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.

<a id="beginner-rounding"></a>
Read [Finite Number Points and Small Baskets](L1_00_numbers_primer.md) first; the table below separates "where values are saved" without extrapolating software intermediate formats into internal hardware structure.

| Operation | Rounding positions and scope to preserve |
|---|---|
| Ordinary [half](APPENDIX_beginner_glossary.md#g054) add/multiply | Current software computes in [binary64](APPENDIX_beginner_glossary.md#g056) first and then applies [RN16](APPENDIX_beginner_glossary.md#g059); these two intermediate operations on finite half values are exactly representable |
| Software half [fused multiply-add](APPENDIX_beginner_glossary.md#g063) | binary64 fused result → RN16, without saving the product as half first; this is the software contract and is not changed to another reference |
| 32-item step on this target | Each term and the [seed](APPENDIX_beginner_glossary.md#g042) are placed toward zero onto a common grid first → exact sum → RN16; the subtotal is then fed back at each step |
| 16-item step | Follows its own independent common-grid/seed rule → half; boundaries such as negative zero are still not generally closed and cannot be replaced by the 32-item rule |
| Final color | Preserves each F32 site together with rejection / [flush-to-zero](APPENDIX_beginner_glossary.md#g068), applying [RZ16](APPENDIX_beginner_glossary.md#g060) only at specified exits; not any generic terminal RN16 above |
<!-- beginner-r04m:end expert -->

<a id="transpose-r04l"></a>
## 8×8 half-Slice Transpose (F27.18, Rank 92)

The input is 32 [lanes](APPENDIX_beginner_glossary.md#g087) of 4 B each, interpreted as two LE16 slices. For output lane l=0..31 and slice b=0..1, `i=2*l+b; src=8*(i%8)+i//8`, and the two output bytes are `out[l,2*b+j]=in[src//2,2*(src%2)+j]` (j=0,1). This is an 8×8 transpose of 64 half values; applying it twice is the identity, and it performs no rounding or numeric conversion. [qkv_projection_impl.hpp:185–191](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L185). The existing L61 prototype contains 32 such nodes; the L63 prototype contains 0, so this step is not fabricated for projection. The prototype status [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) is retained, and writing out the operation semantics does not alter native provenance admission.

[Full Skewer Index](INDEX.md) · Parent level: [ViT](L2_05_vit.md), [FFN](L3_ffn.md), [attention](L3_attention_softmax.md) · [B0](L2_02_b0.md#channels), [Decoder Bridge](L2_06_decoder_bridge.md#bridge), [TIN Upsampling](L2_08_tin_decoder.md#up-256) · [E4 and K32](L4_e4m3_and_k32.md#e4m3-format) · [Full-Chain F32 / FTZ Boundaries](L4_fp32_ftz.md#fp32-ftz)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| h,s,E,m | F16 [encoding](APPENDIX_beginner_glossary.md#g057), sign, stored [exponent](APPENDIX_beginner_glossary.md#g058), mantissa field |
| v(h), RN16/RN64 | Exact decoding, round-to-nearest-even [publication](APPENDIX_beginner_glossary.md#g091) to each target format |
| g,q,rem,n | [Grid step](APPENDIX_beginner_glossary.md#g066), [scaled](APPENDIX_beginner_glossary.md#g031) quotient, discarded remainder, integer after rounding |
| T0/T1, A_j | Software floating-point reference / integer alternative, j-th same-address half publication |

<a id="half-arith"></a>
### L4.half-arith When a half Operation Actually Changes the Bit Pattern

- What it is: After decoding the raw encodings, computes at the precision prescribed by the [call](APPENDIX_beginner_glossary.md#g080) site and then publishes F16; ordinary addition/multiplication, fused multiply-add, same-address accumulation, and format conversion each have their own boundaries.
- Input → output: F16 encodings or explicit F32/binary64 values → F16 encoding or exception; producing [Inf](APPENDIX_beginner_glossary.md#g069) and whether the caller accepts Inf are two separate things.

[CPU Reconstruction] The binary64 steps below are software reproduction rules; native observable constraints come from the separately listed hardware comparisons.

- How it is computed:
  ~~~text
  1. Decode the inputs, preserving finite values, the sign of zero, and the required nonfinite classifications.
  2. Ordinary half add/multiply computes in binary64 and is then published by half_round.
  3. half FMA fuses and rounds once in binary64, and then rounds once more via half_round.
  4. The publication point of every half addition, FMA, or conversion is preserved; same-address contributions feed back term by term.
  5. Callers separately check their own acceptance domains; outer guards cannot be relaxed merely because half_round can produce Inf.
  ~~~
- Numeric rules: Ordinary half publication uses RN-even and supports subnormals; FMA preserves two rounding stages. Auxiliary F32 chains enter half only at explicit conversions; tail round-toward-zero publication and sampler publication follow their own respective contracts.
- Semantic boundary: These are the publication interfaces of the software reference; the listed native comparisons do not yet uniquely determine internal hardware precision or the physical pipeline.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100), scoped MEASURED, and the T1≡T0 software [PROVED](APPENDIX_beginner_glossary.md#g111) result are listed separately below; the synthetic examples check only the listed software arithmetic.
- Next down: This topic has reached the bottom; [bit format](#format), [rounding and add/multiply](#rounding), [integer T1](#integer-t1), [atomic-add order](#atomic-add), [F32 boundaries](#f32-boundaries), [worked examples](#worked-examples).

<a id="format"></a>
## Decoding and Special Values of One F16 Encoding

```math
s=h\mathbin{\gg}15,\quad E=(h\mathbin{\gg}10)\mathbin{\&}31,\quad m=h\mathbin{\&}1023,
\qquad
v(h)=
\begin{cases}
(-1)^s m\,2^{-24},&E=0,\\
(-1)^s(1024+m)\,2^{E-25},&1\le E\le30.
\end{cases}
```

| Encoding category | Current implementation |
|---|---|
| E=0, m=0 | ±0; decoding and half_round preserve the sign. Under RN-even, nonzero [cancellation](APPENDIX_beginner_glossary.md#g071) yields [+0](APPENDIX_beginner_glossary.md#g070), while adding two negative zeros still yields −0 |
| E=0, m≠0 | Subnormal; smallest positive number $2^{-24}$, largest positive subnormal $1023\cdot2^{-24}$, with no uniform flush to zero |
| E=1, m=0 | Smallest positive normal number $2^{-14}$ |
| E=30, m=1023 | Largest finite magnitude 65504 |
| E=31, m=0 | ±Inf; half_value decodes it, and half_round accepts it and returns the corresponding Inf encoding |
| E=31, m≠0 | NaN; half_value generates a [host](APPENDIX_beginner_glossary.md#g096) quiet NaN without preserving the original payload; half_round throws a NaN publication exception |

Basis: [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:25–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L25). The zero-sign and nonfinite branches of the integer reference can be checked line by line in [this project's T1:43–73, 81–95](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L43); [proof RESULT:9, 11, 14, 16](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L9) covers full decoding, zero exceptions, and nonfinite-domain handling.

There is no uniform rule here of "reject everything upon encountering a nonfinite value": in ordinary half addition, Inf plus a finite value can return Inf, whereas adding oppositely signed Infs, multiplying Inf by zero, or passing a NaN input causes a NaN publication rejection; invalid FMA combinations are also rejected. The nonfinite T1 branches and matching exception categories/messages with T0 belong to the software equivalence proof and cannot serve as a native NaN payload contract. min/max also each reject NaN and select the second input encoding when comparing equal, so the order of ±0 must also be preserved. [Public primitives.inc:103–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L103), [T1:55–73, 81–88, 105–111](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L55).

Callers can be narrower: for example, current public [attention](APPENDIX_beginner_glossary.md#g039) rejects half operation results containing Inf, and contract's ordinary arithmetic and same-address accumulation also have result guards. The primitive semantics above cannot be used to let them pass automatically. [attention_impl.hpp:172–186](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L172), [ffn_contract.cpp:422–429, 481–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L422). Nonfinite extensions in other [sealed](APPENDIX_beginner_glossary.md#g103) versions must be bound separately to their source code and cannot be upgraded by borrowing legacy acceptance-domain verifications.

<a id="rounding"></a>
## RN-even, 65520, and Publication Points of Add/Multiply/FMA

For finite nonzero x, the executable rule of the current half_round is:

~~~text
Take the sign and magnitude; if magnitude ≥ 65520, directly publish signed Inf.
Use frexp to obtain e such that the magnitude lies in [2^(e−1),2^e).
g = 2^max(e−11,−24); q = magnitude/g; n = floor(q); rem = q−n.
When rem>1/2, or rem=1/2 and n is odd, add 1 to n.
Encode n*g as half; when below the smallest normal number, enter the subnormal/zero encoding.
~~~

The source code scales by powers of two, and the remainder comparison includes equality; the sign is saved before taking the magnitude. [primitives.inc:35–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L35). Midpoints do not always round up: the midpoint between 1 and $1+2^{-10}$ takes 1, whereas the next midpoint takes the larger neighbor with an even mantissa. Half of the smallest positive subnormal takes +0, and the negative counterpart takes −0; between the largest subnormal and the smallest normal number, rounding up also follows the same even rule—see the run output at the end of this page.

**65520 is the overflow midpoint of RN-even to F16.** From 65504 to 65536 in the next exponent bin is a step of 32, with midpoint 65520; in this implementation, the midpoint rounds to the Inf side. 65519 is published as 65504, and ±65520 is published as ±Inf, with ordinary half_round itself no longer throwing an overflow exception; for the return guard of [matrix](APPENDIX_beginner_glossary.md#g051) multiplication, see [QMMA publication boundaries](L4_e4m3_and_k32.md#publish-guards) separately. The source is [primitives.inc:38–42, 50–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L38), and [software proof RESULT:12, 16](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L12) explicitly preserves this midpoint.

```math
\begin{aligned}
\mathrm{hadd}(a,b)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(a+b)),\\
\mathrm{hmul}(a,b)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(ab)),\\
\mathrm{hfma}(a,b,c)&=\mathrm{RN}_{16}(\mathrm{RN}_{64}(ab+c)).
\end{aligned}
```

The public source code is [primitives.inc:103–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L103). Addition of finite half values can be unified onto the $2^{-24}$ integer grid, and a product has at most 22 bits of significand, so the binary64 stage of these two operations is exact; exact composition of FMA, however, can require a wider integer, so T1 must explicitly preserve the two stages of rounding to binary64 first and then to F16. Fusion does not equal publishing the product as F16 first and then adding c, nor is it replaced here by another direct exact→F16 reference.

The evidence convention for "retaining two stages to align with native" is: this project retains the software reference that has already passed comparison on the hardware acceptance domain, and then proves that the alternative T1 is identical to it. It is neither a proof that native hardware uses binary64 internally nor a general three-input hardware full-domain equivalence proof. In [narrow-domain acceptance RESULT:22–31](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L22), addition/multiplication first determines actual validity across all raw two-input pairs and then compares outputs on the acceptance domain; the four fixed-addend FMA probes likewise each cover a $2^{32}$ input domain and **do not cover the $2^{48}$ hardware domain across an arbitrary third half**. For example, addition accepts 4,030,980,098 pairs and rejects 263,987,198 pairs; neither acceptance nor rejection means ignoring the input, and rejected items have no CPU numeric output.

<a id="integer-t1"></a>
## Alternative Implementation of the Two-Stage Reference

[CPU Reconstruction / Verification Record] Frozen T1 uses exact integers to preserve RN64 first, then RN16, together with the zero/nonfinite branches; its software equivalence proof with T0 does not prove the internal [GPU](APPENDIX_beginner_glossary.md#g078) algorithm, and std::fma remains visible in the current public modules. For the arithmetic contract, see the section above; the [two-limb implementation, proof premises, and trust boundaries](APPENDIX_evidence_history.md#half-integer-implementation) have been moved to the appendix.

<a id="atomic-add"></a>
## Why half Atomic Adds Cannot Be Reordered Arbitrarily

Each contribution at the same address reads the previous half value, performs addition, and republishes half. In the formula below, A₀ is the initial half value obtained according to the caller contract, and tᵢ are the half contributions; π(j) denotes the index of the contribution used at step j in the given execution order, with j starting from 1 until all contributions have been published. π records only the order adopted here and does not additionally prove a total order for general GPU scheduling:

```math
A_j=\mathrm{RN}_{16}\!\left(A_{j-1}+t_{\pi(j)}\right).
```

Initialization must finish before the first term, and reading the result must wait until the final term is published; changing this to summing in F32/binary64 first with a single final half, or splitting the contributions into an arbitrary [reduction](APPENDIX_beginner_glossary.md#g050) tree, alters the contract. Processing non-overlapping addresses in parallel does not grant permission to [rearrange](APPENDIX_beginner_glossary.md#g019) [same-address contributions](APPENDIX_beginner_glossary.md#g095).

Public contract runs the initialization stage first, followed by two contribution stages, and finally publishes; each two-byte unit is fed back via h_add, with a result-overflow rejection. [ffn_contract.cpp:436–442, 478–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L436). The same-address loop in projection also applies h_add term by term and checks initialization and contribution counts, [qkv_projection_impl.hpp:233–239, 290–294](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L233). On the three terms given by the map, L100 explicitly combines the first two terms first and then adds the third term, [entry.cpp:64–71](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L64).

Across the full network, this involves the 8 contract launches and 8 projection launches of [ViT](APPENDIX_beginner_glossary.md#g014), as well as L100; the generic branch in the shared [QKV](APPENDIX_beginner_glossary.md#g040) executor does not mean QKV itself also has such atomic adds. In the saved evidence, reordering in the generic harness yields DIFF, [step2a RESULT:15, 58](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L15); an early small unit test for projection also captured a reordering DIFF, though the real-input control had not yet been run at the time, [step2b RESULT:9, 16, 23](../../../experiments/parity-cpp-step2b-qkv_projection-r01-20260928-codex/RESULT_ZH.md#L9). The early L100 reordering record is explicitly NOT_RUN, [entry RESULT:23, 34](../../../experiments/parity-cpp-chain-entry-r01-20260930-codex-entry/RESULT_ZH.md#L23), and is not changed to completed.

Order and term-by-term publication are listed in the [project axiom table:33–34](../../../experiments/parity-proof-program-r02-20261007-codex/resume12-20261009/delivery/AXIOMS_ZH.md#L33) as MEASURED_AXIOM, while a **general scheduling total-order certificate remains OPEN**. Agreement across finite repeats cannot prove that arbitrary arrival orders are fixed, [rental RESULT:21](../../../experiments/parity-rental-r03-addon-20261006-codex/RESULT_ZH.md#L21). The synthetic example at the end of this page directly demonstrates the same three terms producing 0 and 1 under different orders; it is a demonstration of non-associativity, not a new GPU scheduling measurement.

<a id="f32-boundaries"></a>
## Boundaries Between F32 and half

Finite values in F16→F32 expand exactly; F32→F16 publishes at explicit conversion sites according to RN16 or the RZ16 prescribed by that call. Auxiliary F32 operations are not lowered to half early, and [texture](APPENDIX_beginner_glossary.md#g027) half publication has its own midpoint rule.
Full-chain entry/exit points, FTZ, and rejection conditions are maintained only in the [F32 site inventory](L4_fp32_ftz.md#sites); this page retains the half format, fusion, and term-by-term publication arithmetic.
NaN payload differences and the scope of legacy conversion comparisons are retained in [conversion history](APPENDIX_evidence_history.md#half-f32-history) and are not upgraded from finite-domain examples.

<a id="worked-examples"></a>
## Synthetic Calculation Examples: From Synthetically Encoded Inputs to F16 Output

All inputs are **synthetically constructed format/arithmetic examples, not model coefficients**. math.fma in Python 3.13 executes binary64 fusion, and hr transcribes the public half_round; finite_t1 uses big integers to demonstrate the two rounding stages of frozen T1 without replacing the C++ two-limb proof. Running requires no project modules, model data, or GPU.

- Fusion example: a=0x3c01, b=0x3bff, c=0xbc00, which are $1+2^{-10},1-2^{-11},-1$ respectively. The exact multiply-add is $2^{-11}-2^{-21}=1023/2097152$, and FMA outputs **0x0ffe**. If the product is converted to F16 first, it falls below the $1+2^{-11}$ midpoint and becomes 1, and adding −1 then yields **0x0000**.
- Midpoint example: 0x3c00 plus 0x1000 outputs **0x3c00**; 0x3c01 plus the same term outputs **0x3c02**. For subnormal midpoints, negative zero, and crossing the smallest-normal boundary, see stdout.
- Same-address order example: starting from +0 and adding 2048, 1, −2048 term by term in half yields **0x0000**; changing the order to 2048, −2048, 1 yields **0x3c00**. In the first order, 2048+1 is an exact midpoint and 1 is rounded off.
- Conversion example: the F32 encoding 0x3f801000 is a half midpoint and outputs **0x3c00**; the adjacent larger 0x3f801001 outputs **0x3c01**. The results for 65519 and ±65520 are also given by the script.

See the appendix for the [complete program, stdout, and independent fraction check](APPENDIX_evidence_history.md#half-example-source); the rounding positions and short results are retained above.
