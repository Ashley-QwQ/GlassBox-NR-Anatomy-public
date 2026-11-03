# L4.mufu: Measured Bit Patterns and CPU Representation of Special Functions

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · Parent level: [B0 Noise](L2_02_b0.md#noise), [ViT Normalization](L2_05_vit.md#qkv), [ViT Attention](L2_05_vit.md#attention), [B70](L2_09_b70.md), [Final Display](L2_10_output.md) · [half Publication](L4_half_arith.md#f32-boundaries)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| T_f, Domain_f | Certified [bit-pattern](APPENDIX_beginner_glossary.md#g057) map of function f, acceptance domain of the current wrapper |
| b,s,e,m | [F32](APPENDIX_beginner_glossary.md#g056) input [encoding](APPENDIX_beginner_glossary.md#g057), sign, stored [exponent](APPENDIX_beginner_glossary.md#g058), mantissa field |
| h₀, h | Starting encoding and query encoding of a small [half](APPENDIX_beginner_glossary.md#g054) table |
| k, [Radius](APPENDIX_beginner_glossary.md#g073)(k) | Noise integer key, precomposed certified radius |

<a id="mufu"></a>
### L4.mufu One Call Is Not Evaluating an Approximate Mathematical Value

- What it is: Maps an input bit pattern through a specified wrapper to a measured output bit pattern; the CPU can read raw values, decode losslessly, or execute an accepted bit-pattern transform.
- Input → output: raw32, half encoding, or noise k → raw32/half, or out-of-domain rejection. Input types and acceptance domains of different wrappers are not merged.
- How it is computed:
  ~~~text
  1. Determine the function, wrapper version, input format, rounding/FTZ, and table identity.
  2. Check domain membership for the current interface, rather than checking only whether a value is finite.
  3. Raw-value tables are indexed by raw32; compact tables reconstruct the raw integer bit pattern first.
  4. Only accepted scaling/correction branches may be computed in code; failing segments read certified raw values or reject.
  5. Convert back to half at explicit nodes prescribed by the call graph before handing off to subsequent operations.
  ~~~
- Numeric rules: The target is the encoding of $T_f(b)$, not a correctly rounded approximation of a mathematical function; a general [call](APPENDIX_beginner_glossary.md#g080) claims matching only on $Domain_f$. Captured [full domain](APPENDIX_beginner_glossary.md#g111), verified compression, and all network sites being [bound](APPENDIX_beginner_glossary.md#g103) are distinct facts.
- Why it is computed this way: Saved measurements contain bit patterns that [libm](APPENDIX_beginner_glossary.md#g074) and naive range reduction cannot reproduce; a unique internal [GPU](APPENDIX_beginner_glossary.md#g078) implementation cannot be derived from these observations.
- How we know: [V2-02-006](../../arch-v2/02.03_mufu.md#v2-02-006) is the scope entry; the text below cites current public code, original measurements, and software representation acceptances separately.
- Next down: This topic has reached the bottom; [variants and callers](#variants), [tables and encodings](#representation), [measurement scope](#evidence), [edge semantics](#edges), [executable examples](#worked-examples).

<a id="variants"></a>
## Where Each of the Seven Function Families Is Used

The L3 names in the table below are the [operator step entries in INDEX](INDEX.md). Mathematical names only indicate usage and do not define bit-for-bit results.

| Function | L2 family → L3 step | CPU path and source path:line |
|---|---|---|
| rsq | [Normalization](APPENDIX_beginner_glossary.md#g043) steps of L2.02 B0, L2.03/08 [TIN](APPENDIX_beginner_glossary.md#g011), L2.04/07 [split16](APPENDIX_beginner_glossary.md#g013), L2.05.qkv, and L2.09 B70 → reciprocal square root of query/key vector norms in L3.tin-norm | Small half table or F32 table value converted to half: [GlassBox-NR/cpp/chain_entry_optm/b00.hpp:25, 46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L46), [tin.cpp:114–117](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114), [scalar_map.hpp:272–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272), [qkv_projection_impl.hpp:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192), [outtail.cpp:58, 90](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L90) |
| rcp | B0/TIN/split16 [window](APPENDIX_beginner_glossary.md#g015) and [ViT](APPENDIX_beginner_glossary.md#g014) [attention](APPENDIX_beginner_glossary.md#g039) → [denominator](APPENDIX_beginner_glossary.md#g048) normalization in L3.attention-[softmax](APPENDIX_beginner_glossary.md#g047); B70 → L3.temporal-sampling; L157 → color-auxiliary reciprocal in L3.postprocess | half/F32 tables and tail mantissa-table [scaling](APPENDIX_beginner_glossary.md#g031): [b00.hpp:49](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L49), [tin.cpp:124–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L124), [scalar_map.hpp:272](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272), [attention_impl.hpp:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212), [b70_temporal.hpp:27–49](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L27), [outtail.cpp:53, 73](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53) |
| ex2 | Non-[reset](APPENDIX_beginner_glossary.md#g032) B70 → confidence blending in L3.output-temporal; L157 → color transform in L3.postprocess | Mantissa base table, exponent-bit transform, failing-segment raw values, and restricted-input sparse table: [b70_temporal.hpp:45–46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/b70_temporal.hpp#L45), [outtail.cpp:55–57, 71–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55), [stage_codec.inc:70–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L70) |
| lg2 | B0 → radius chain in L3.noise; L157 → color transform in L3.postprocess | The runtime path in B0 is already precomposed into the radius table; L157 uses [E1](APPENDIX_beginner_glossary.md#g110) decoding / raw-value fallback: [noise_online_optd.hpp:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L23), [lg2_decoder.hpp:17–35](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/lg2_decoder.hpp#L17), [outtail.cpp:54, 74–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L54) |
| sqrt | B0 → two radius paths in L3.noise | sqrt_k_exact.dnc saves the complete precomposed radius by k, without calling a general sqrt at runtime: [noise_exports_optd.inc:16](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L16), [noise_online_optd.hpp:26](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L26) |
| sin / cos | B0 → three angle factors in L3.noise | Two measured composed tables losslessly encoded by k: [noise_exports_optd.inc:17–18](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L17), [noise_online_optd.hpp:27–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L27) |

One cannot insert ex2 into attention merely because of the name "attention scores": the score path in public B0/TIN is an F32 [affine](APPENDIX_beginner_glossary.md#g049) transform, half clamp, and encoding transform, followed by rcp on the ordered denominator, [tin.cpp:108–109, 122–126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L108). For the completion of the native inventory to seven families, see [09-12 probe RESULT:15–22, 57–80](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L15); sin/cos in the names of [matrix](APPENDIX_beginner_glossary.md#g051) auxiliary [tensors](APPENDIX_beginner_glossary.md#g076) likewise do not signify calling trigonometric functions, and that report checked their consumers separately.

<a id="representation"></a>
## Full-Domain Maps, Small Mantissa Tables, and Acceptance Domains

[CPU Reconstruction] Complete raw32 maps may be saved in blocks without requiring the full table to stay resident; only registered and certified members are read, and unregistered queries return a missing-member error. Registration checks the SHA actually read, and on cache miss or map swap-in it checks the fd identity and rejects detected changes; a cache hit reuses already-mapped pages and is not guaranteed to re-detect external file modifications on every query. For the check order, see [full_raw_registry.hpp:28–39, 53–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L28); for chunking, two-slot map capacity, and read layout, see the [CPU Storage Appendix](APPENDIX_cpu_storage.md#raw-registry); storage capacity does not prove general network reachability.

Small tables also retain their identity: Python Sm120Tables reads measured native_half_bits, verifies the SHA, and sets the arrays read-only, with no mathematical formula fallback when a table is missing, [mlxdlss/sm120_b1.py:155–196](../../../mlxdlss/sm120_b1.py#L155). The basic formula for the half path is $T(h-h_0)$, but the specific endpoint range must be checked first; ViT converts exactly to F32 first to look up the table and applies RN to half at explicit nodes, [qkv_projection_impl.hpp:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192), [attention_impl.hpp:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212). Mathematical reciprocals and square roots for [RCP](APPENDIX_beginner_glossary.md#g072)/RSQ are not re-evaluated here.

### rcp: Measured Mantissa + Integer Exponent Adjustment

For a [normal](APPENDIX_beginner_glossary.md#g068) F32 input, take the input mantissa m to look up $r=T_{\mathrm{rcp},e=127}[m]$, subtract e−127 from its output stored exponent, and preserve the measured mantissa and input sign; when the adjusted exponent is ≤0, [publish](APPENDIX_beginner_glossary.md#g091) [signed zero](APPENDIX_beginner_glossary.md#g070), and when ≥255, publish signed [Inf](APPENDIX_beginner_glossary.md#g069). Zero/subnormal and nonfinite inputs take independent certified raw-value branches. [outtail.cpp:53](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53).

Exactness here means "a bit-pattern transform relative to the measured r and the accepted wrapper", not a claim that r equals the correctly rounded $1/x$. Historical range reduction also failed when outputs were not flushed to zero, holding on the normal input blocks only after output FTZ was added, [probe RESULT:271–285](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L271).

### lg2 / ex2: Bit-Level Reconstruction on Certified Base Tables

What is operated on here are measured output bit patterns; base, raw126, and level must all be certified, and the result is not a correctly rounded approximation from a math library.

~~~text
LG2: For positive inputs, exponent E=127 reads base[m] directly, and E=126 reads raw126[m] directly.
When E=111..125, v=RZ32(base[m]−(127−E)); align the significands using integers first, then truncate the low bits beyond the 24-bit significand.
Take the 3-bit level per mantissa; E groups 111..118 / 119..122 / 123..124 / 125 correspond to group=0/1/2/3.
Output bit pattern = bits32(v)−[level≤group]; outside this range, read only certified raw-value members or reject.
EX2 positive argument: n=floor(x), j=floor((x−n)×2^23), delta=n−1; clamp j to 0..2^23−1.
EX2 negative normal argument: form v=trunc(|x|×2^23) from significand/exponent, n=v>>23, t=v&(2^23−1).
When t=0, j=0 and delta=−n−1; otherwise j=2^23−1−t and delta=−n−2.
predicted=base_EX2[j]+delta×2^23; check input membership first, then check the 32-bit output range.
Only accepted codec branches return predicted; specified failing segments read certified raw values instead.
Zero, FTZ, and nonfinite values follow the specific wrapper branches; extrapolated formulas do not replace missing-member / NaN rejection.
~~~

For the actual bit operations, see [LG2 decoder](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/lg2_decoder.hpp#L17) and the [EX2 wrapper](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55); base-table capacities, raw-value exceptions, and legacy acceptances remain in the [CPU storage ledger](APPENDIX_cpu_storage.md#mufu-ex2-codec).

### Function Behavior, Composed Radius, and Acceptance Boundaries

<a id="value-wrapper"></a>
To connect bit-pattern lookups to floating-point multiplication, first distinguish the raw bit-pattern map $T_f$ from the numeric wrapper $\widehat{T}_f$:

```math
\widehat{T}_f(x)=\mathrm{value}_{32}\!\left(T_f(\mathrm{bits}_{32}(x))\right).
```

$\mathrm{bits}_{32}$ takes the raw encoding of an F32, and $\mathrm{value}_{32}$ interprets the encoding back as an F32 value; both only convert representations without adding rounding, and both preserve the sign of zero. $c_{\ln2}$ is the algorithmic constant represented by the F32 encoding `0x3f317218`; see [B0 noise constants](L3_b0_input.md#noise). Radius(k) in the formula below denotes the decoded F32 radius value; what the asset saves is its raw encoding.

The B0 composed radius remains
```math
Radius(k)=\widehat{T}_{\mathrm{sqrt}}\!\left(\mathrm{RN}_{32}\left(\mathrm{RN}_{32}(\widehat{T}_{\mathrm{lg2}}(k2^{-24})c_{\ln2})\cdot(-2)\right)\right),\qquad 1\le k\le2^{24}.
```
It is not sqrt(k·2⁻²⁴). The two multiplications on the frozen domain have no nonzero F32 subnormals, so the underlying FTZ does not alter these nonzero values; this is not extrapolated to arbitrary sqrt inputs. The sin/cos tables already include angle prescaling and [toward-zero](APPENDIX_beginner_glossary.md#g060) reduction, and no further reduction may be performed online; after two radius and three trigonometric lookups, only the three F32 products undergo RN to half, and the radius at u=1 preserves −0.

Member certification, table domain, and caller domain must all be satisfied simultaneously; cross-[channel](APPENDIX_beginner_glossary.md#g007) color branches do not expand their domain merely because a single-half site has been verified. Zero/subnormal and nonfinite handling still follows the [specific wrappers](#edges), and storage trimming is in the [appendix](APPENDIX_cpu_storage.md#mufu-domain-storage).

<a id="s157-reach-r2c"></a>
## Call Sites and Function Members

Each S157 site first verifies that the control tuple and input bit pattern belong to certified members before looking up the measured table or decoding; see [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate). The coverage of certified tables and the caller's reachable domain constrain the entry separately; a cross-channel color full domain cannot be derived from a single-half domain.

<a id="evidence"></a>
<a id="lookup-contract-r04l"></a>
## Per-Family Table-Lookup Contracts (Function Specification Items from Rank 7 Onward)

All steps below are **TABLE_DRIVEN_DESCRIBED**. Table identities, indices, and wrappers are written out in full, without reclassifying raw-value functions as [closed forms](APPENDIX_beginner_glossary.md#g020).

| Consumer | Function input endpoints and output wrapper | Table identity and index |
|---|---|---|
| B0 | RSQ: half encoding closed interval [0x0410,0x7c00]; RCP: denominator closed interval [0x1c00,0x60e0] | `native_half_bits[h-0x0410]` from the original [NPZ](APPENDIX_beginner_glossary.md#g097), returning half directly; RSQ length 30705, RCP length 30704 |
| TIN, including input / up- and [downsampling](APPENDIX_beginner_glossary.md#g021) / exit variants | Shared lookup requires 0x0410≤h≤0x7c00 and index less than the loaded length; RSQ may take the +Inf endpoint; before calling RCP, [0x1c00,0x60e0] is also checked | `rsq.u16` / `rcp.u16` read as LE16, directly half; lengths 30705/30704 respectively, where the latter cannot read the +Inf index |
| split16 | 0x0410≤h<0x7c00; class-invalid dependencies use 0x3c00 as a placeholder during lookup and must not let invalid values enter the matrix | `native_float_bits[:30704]` from the original NPZ, index h−0x0410, returning raw32; undergoes [RN16](APPENDIX_beginner_glossary.md#g059) only at explicit rne16 nodes in the [DAG](APPENDIX_beginner_glossary.md#g089) |
| ViT QKV | F32 must equal the converted-back half exactly, 0x0410≤h<0x7c00, and index must not be out of bounds | Same RSQ raw32 table; subsequent f16of node applies RN16 and rejects nonfinite publication |
| ViT attention | Checks half representability and the open right endpoint as above | Same RCP raw32 table; subsequent explicit f16of applies RN16, and the constant-multiply node also rejects nonzero F32 subnormals |
| B70 | RSQ closed interval [0x0410,0x7c00], raw32 table length 30705, returning RN16; denominator RCP is a raw32 function | RSQ index h−0x0410; RCP follows the mantissa-table / certified raw-value branches and cannot reuse the TIN denominator domain |

Source NPZ identities: `rsq-domain.npz` SHA-256 `06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62`; `rcp-domain.npz` SHA-256 `055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59`. The TIN exported LE16 tables are `73f5c18f6c853ce7ba071d2dca44afe4441606a046fd0d73386596b4474af874` and `0f7803de239ba07f109bead85e726cf414af35101a9d41ba58cc5c4a17a6ecfc` respectively; these are identities of different representations and are not interchangeable. [Original bindings](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/s00-bindings.json), [entry certification and field selection:15–40](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/entry_assets.py#L15), [TIN binding certification:99–105](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/backend_abi.py#L99).

Endpoint code: [B0:46, 49, 62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L46), [TIN lookup:87](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L87) and [denominator:126](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L126), [split16:272–274, 322](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272), [QKV:192–206](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L192), [attention:212–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L212), [B70:53–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53). TIN lookup itself checks only the lower bound and loaded length; the upper bound in the table is given by the named table length rather than an extra hardcoded guard. 0x7c00 is the positive Inf input endpoint; NaN and negative encodings are outside these named table domains. Special inputs must not bypass the caller's nonfinite guards.

<a id="tail-dispatch-r04l"></a>
### Sparse, Codec, and Raw-Value Selection in the Tail Stage (Ranks 84–86, 218–222, 225)

The exact dispatch order is: L155 EX2 first performs a binary search on `ex2_sparse` by unsigned raw32 key, reading raw32 directly on a hit; a miss requires L155 temporal_tables or L157 with a base-table length of 2^23. e=0 returns 1 (including positive and negative subnormals), +Inf returns +Inf, and −Inf returns +0; only the remaining inputs enter the EX2 decoding above. Positive numbers require e≤133 and expos[bits>>23]; negative numbers require admission by one of exneg, a certified codec block, or a raw-value block, with exponent shift <40 and predicted integer in [0,2^32−1]. When a negative number does not belong to exneg but has a raw-value member, the raw value takes precedence over the prediction; missing members and NaN cannot be forcibly accepted via prediction. [outtail.cpp:55–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L55).

LG2 is loaded only in L157: the E127 base table and E126 raw values each have 2^23 LE32 items, and the 3-bit level table is 3145728 B; for exponent blocks 111..127, other positive finite normal inputs can fall back only if a raw-value member is present. e=0 returns −Inf first; negative normal numbers and Inf/NaN are rejected. RCP requires a 2^23-entry mantissa table; e=0 looks up the certified positive-zero block and merges the sign, e=255 looks up the full raw32 member, and other exponents use the integer scaling above. [outtail.cpp:53–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53).

The identity contract is `(stage, function, representation, byte length, SHA-256, member set)`: the tail descriptor certifies RCP/RSQ/EX2 using extracted_sha256 and bytes from sources in the manifest; the E1 manifest's own SHA is fixed at `4255d067e6a618342182a86f44fbf2feceb92a7d148e0dcdfaabe304f8c72138`, little-endian, and the byte lengths and SHAs of the three members inherit its files fields item by item. Block members of the full raw registry must be loaded according to the [certified read rules](#representation). Substituting matching filenames for identity verification is prohibited. [tail_runtime.py:14–40](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/M/tail_runtime.py#L14). The four sites in L157 also check reach first before calling these same backing functions; the function acceptance domain does not equal the joint RGB branch reachable domain, which remains [UNKNOWN](APPENDIX_beginner_glossary.md#g104).

| Named exported representation in the tail stage | Byte length | SHA-256 |
|---|---:|---|
| RCP E127 raw32 base table | 33554432 | c408381446132e07fa5581e930dc33fb790bea7ec4276ef3621e322df2492a55 |
| EX2 block127 raw32 base table | 33554432 | cce5df10202dbfcde720ca547d147edb3e2a406a5fed189323f419177a72a1a5 |
| B70 RSQ raw32 half-domain table | 122820 | 5f50d80e6793405891045b4c8f747b46bc86551dee11b7d2cbef84f154088107 |

Identities come from the [existing tail manifest](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/dlssnr-biggeom/r01-20261006-codex/assets-chain/mirror/E/dlssnr-cpp-work/chain-outtail-r01-codex/tables/manifest.json). Actual loading first verifies the byte count, divisibility by element width, full read completion, and the SHA actually read; these tables are not regenerated in this round. [stage_codec.inc:30–56](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L30). L155 temporal also requires a non-empty 184 B parameter profile set; sparse inputs and outputs are both certified LE32 arrays of equal length with 1..65536 items, where inputs are finite, sorted by unsigned key, and reject duplicates, and outputs are read as the corresponding raw32. L156 loads no function tables; L157 loads no RSQ or half [quantization](APPENDIX_beginner_glossary.md#g061) tables. A load failure clears all tables and the raw registry rather than reusing the previous stage's cache. [stage_codec.inc:58–87](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L58).

<a id="noise-spec-r04l"></a>
### Composed Inputs of the Noise Tables (Ranks 72–73)

The explicit inputs of `NoiseAssets` are the three certified DNOISE01 members Radius/Cos/Sin, not three libm functions. With four keys each in [1,2^24], it fetches `r0=Radius(k0),r1=Radius(k1)` and `c3=Cos(k3),s3=Sin(k3),c2=Cos(k2)` in turn; the three results are `RN32(r1*c3), RN32(r1*s3), RN32(r0*c2)`, after which the caller applies RN16 item by item. Radius includes precomposed LG2/multiplication/SQRT, and Cos/Sin include angle transforms; these transforms are not performed again online. Block decoding, raw-value SHAs, and the final entry −0 follow the [existing self-contained example](APPENDIX_cpu_storage.md#mufu-example), and invalid k values are rejected. [noise_online_optd.hpp:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L23). What this round adds is the exact data contract; the two audit rows remain TABLE.

## Observed Domains and Caller Domains

[Verification Record] The saved seven-family FTZ/non-FTZ probes, cross-architecture summaries, October raw-value bank, and production member-composition checks are listed separately in the [complete measurement ledger](APPENDIX_evidence_history.md#mufu-evidence). Full-domain raw-value capture, software codec acceptance-domain agreement, and full-domain binding of network callers are distinct assertions; two device/driver receipts cannot be combined into a single measurement.

Matching saved digests for a fixed wrapper do not prove that the loaded machine code is identical; two legacy shapes were not covered, and results are not generalized to future drivers or unmeasured wrappers. The member composition of SIN/COS includes prescaling and is not an independent full-domain proof for each substep; there is no output outside the domain. Domain-extension candidates retain their original validity: LG2/EX2 match only on the acceptance domain and fall back to raw values on failing segments, which cannot be written as all formulas passing across full raw32. Legacy NOT_RUN items, unclosed cross-channel domains, and per-caller binding conditions remain in effect.

<a id="edges"></a>
## ±0, Subnormals, Inf/NaN, and FTZ

The table below shows the saved **FTZ probe wrappers**, not an acceptance commitment for every CPU interface; data comes from the complete special-exponent-block classification in [edge-cases.json](../../../experiments/parity-mufu-probe-20260912/edge-cases.json).

| Function | +0 / −0 | Same-sign subnormal input | +Inf / −Inf | NaN |
|---|---|---|---|---|
| rcp | +Inf / −Inf | Treated as the corresponding zero; tiny outputs from large normal numbers can also be flushed to signed zero | +0 / −0 | Canonicalized to 0x7fffffff |
| rsq | +Inf / −Inf | Treated as the corresponding zero; negative normal numbers output NaN | +0 / NaN | Same as above |
| sqrt | +0 / −0 | Treated as the corresponding zero; negative normal numbers output NaN | +Inf / NaN | Same as above |
| lg2 | −Inf / −Inf | Treated as the corresponding zero; negative normal numbers output NaN | +Inf / NaN | Same as above |
| ex2 | 1 / 1 | Treated as the corresponding zero, outputting 1 | +Inf / +0 | Same as above |

The public tail wrappers also explicitly encode part of the boundaries: e=0 in lg2 returns −Inf, while unadmitted inputs such as negative normal numbers and Inf/NaN are rejected; ex2 returns 1 for e=0 and returns Inf/0 for ±Inf respectively, while NaN and out-of-bounds finite numbers may still be rejected; nonfinite results of rcp come from certified raw values. [outtail.cpp:53–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53). **"Measuring NaN in a table" does not equal "the network caller permits NaN propagation."**

A half subnormal converted to F32 is still an F32 normal number, so half subnormals cannot be cleared across the board merely because a wrapper has FTZ. The common acceptance domain for small half tables is $h_0\le h<0x7c00$, [sm120_b1.py:374–378, 415–420](../../../mlxdlss/sm120_b1.py#L374). Some current C++ wrappers permit the 0x7c00 endpoint, [outtail.cpp:58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L58); r04l checked the source NPZ identities, field lengths, and final RSQ entry above: the 30705 entries of RSQ include that input and output +0 in half, whereas RCP has only 30704 entries and excludes that input. Whether each consumer can actually use it is still governed by the [per-family contracts](#lookup-contract-r04l).

Production member bindings for sin/cos target finite pre-reduction angles; the compact online interface accepts valid k values and rejects out-of-range inputs immediately, [compact_noise_optd.hpp:79–80](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L79). It provides no production contract for arbitrary NaN/Inf trigonometric inputs, which cannot be filled in via mathematical identities. The radius chain preserves −0 when u=1, which is verified by the final entry read at the end of this page; conversion to half occurs only after the three final F32 multiplications, [noise proof RESULT:9–11](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L9).

## Why libm Cannot Be Substituted

The saved LG2 result for the smallest positive normal input is not the mathematical integer −126; naive exponent scaling and trigonometric symmetry reduction also exhibit bit differences. Function wrappers must preserve certified raw values, corrections, and acceptance domains rather than merely providing a loose error bound. [Specific counterexamples, original registrations, and measurement scopes](APPENDIX_evidence_history.md#mufu-counterexample-identifiers) are collected in the appendix.

<a id="worked-examples"></a>
## Reading the Compact Table Directly: k=43 to F32/half

[Verification Record] The synthetic valid key k=43 looks up the precomposed radius raw32=0x40a260c8, which is approximately 5.07431411743 in F32 and 0x4513 after RN16; it is not directly sqrt(43·2⁻²⁴). The radius of the final entry k=2²⁴ is −0 (raw32=0x80000000, half=0x8000), preserving the sign of zero.

The same original real-computation example also reads LG2=0xc2fbffff for the smallest positive normal input, whereas libm converted to F32 gives 0xc2fc0000; measurement tables cannot be replaced by a math library. The [complete script and certified SHAs](APPENDIX_cpu_storage.md#mufu-example) and the [intermediate decoded integers and original stdout](APPENDIX_cpu_storage.md#mufu-example-output) are in the appendix. For the original run scope, see the evidence appendix.

This verifies selected table entries, decoding transcription, half publication, and a libm counterexample, without re-verifying all compressed entries or the full raw32 data.
