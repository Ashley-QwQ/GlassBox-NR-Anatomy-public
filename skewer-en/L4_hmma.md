# L4.hmma: F16 Products, K16 Common Grid, and Step-by-Step Publication

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · Parent level: [B0 Adaptation](L3_b0_input.md#adapter), [B70 Terminal Head](L3_b70_history_output.md#b70-network) · Comparison: [E4 QMMA](L4_e4m3_and_k32.md#qmma-k32-accumulation), [F16 Format and Rounding](L4_half_arith.md#format)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

<a id="hmma"></a>
## Objects, Notation, and Domain of Applicability

[CPU Reconstruction] This page first explains the [scalar](APPENDIX_beginner_glossary.md#g076) [K16](APPENDIX_beginner_glossary.md#g065) reproduction rule in the current source code; it is not a hardware [full-domain](APPENDIX_beginner_glossary.md#g111) theorem. A and B are 16 [F16](APPENDIX_beginner_glossary.md#g054) [encodings](APPENDIX_beginner_glossary.md#g057) each, C is an F16 [seed](APPENDIX_beginner_glossary.md#g042), and the output is also F16. In B0, hmma_cached / hmma_dot imply C=[+0](APPENDIX_beginner_glossary.md#g070); in B70, hmma_seed explicitly receives C. Caching exact decoded values adds no rounding.

F16 has a 1-bit sign, a 5-bit [exponent](APPENDIX_beginner_glossary.md#g058), and a 10-bit mantissa field; the finite range reaches ±65504, and the smallest positive [subnormal](APPENDIX_beginner_glossary.md#g068) is 2⁻²⁴. Operand [Inf](APPENDIX_beginner_glossary.md#g069)/NaN are outside the acceptance domain of these functions, whereas ±0 and nonzero subnormals cannot be uniformly flushed; for the complete encoding, see the link above.

[Native Behavior / Verification Record] Saved probes on [sm_120](APPENDIX_beginner_glossary.md#g078) support the common-grid candidate below across a large number of finite cases, while also uncovering counterexamples to its negative-zero predictions; the negative-zero revision remains pending adjudication. For cross-architecture and candidate status, see [Hardware Boundaries](#hardware); the current CPU source-code description cannot be upgraded to a rule for all native inputs.

| Symbol | Meaning on this page |
|---|---|
| v(h), E_h | Exact F16 value, and 5-bit stored exponent in the encoding; for the format, see the link above |
| η(h) | E_h−15 for normal numbers; fixed at −14 for nonzero subnormals, which is the field exponent rather than the actual log₂ magnitude |
| e_C | ⌊log₂\|v(C)\|⌋ for nonzero seed; does not participate in the maximum when C=0 |
| E, g, RZ_g | Common exponent for this step, power-of-two [grid step](APPENDIX_beginner_glossary.md#g066), and truncation [toward zero](APPENDIX_beginner_glossary.md#g060) onto that grid |
| [RN16](APPENDIX_beginner_glossary.md#g059) / K16 | Round-to-nearest-even [publication](APPENDIX_beginner_glossary.md#g091) to F16 / 16 products per step; not an execution thread shape |

<a id="grid"></a>
## Common Grid, Precision, and Order of One Step

For finite inputs, the current software rule is:

```math
\begin{aligned}
E&=\max\bigl(-21,\ e_C,\ \{\eta(a_k)+\eta(b_k):v(a_k)v(b_k)\ne0\}\bigr),\\
g&=2^{E-25},\qquad RZ_g(x)=\mathrm{trunc}(x/g)\,g,\\
Y&=\mathrm{RN}_{16}\!\left(RZ_g(v(C))+
             \sum_{k=0}^{15}RZ_g(v(a_k)v(b_k))\right).
\end{aligned}
```

1. Select the common grid using the original F16 exponent field; terms whose product is zero do not participate in E. In B0, all-zero products directly return +0.
2. A finite F16 product has at most 22 bits of significand and can be represented exactly in [binary64](APPENDIX_beginner_glossary.md#g056); here **products are not converted to F16 first**.
3. The seed and each product are divided by g and truncated toward zero to integers; the signed integers are summed from k=0 to 15. Within the acceptance domain, these integers and their sum are exact, and per-term F16 rounding cannot be inserted.
4. The integer sum is multiplied back by g, and half_round then performs a single RN16. F16 subnormals are preserved without applying F32 FTZ.
5. If a subsequent K16 step exists, it carries this published F16; across steps, one cannot compute the real-number sum first and round only once. The integer loop in software does not prove the physical GPU addition tree.

"25" refers to the position of the common grid relative to the field exponent; it cannot be understood as a floating-point [accumulator](APPENDIX_beginner_glossary.md#g064) uniformly having a 25-bit mantissa, nor can products and the seed be summed with full precision first and truncated only afterward.

Source code: [mapexec_base.hpp:157–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp#L157), [decode_reuse.inc:71–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/decode_reuse.inc#L71), [outtail.cpp:60–61](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L60). For the terminal RN16, see [primitives.hpp:12–36](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/primitives.hpp#L12).

<a id="callers"></a>
## Where B0 and B70 Each Connect

| [Call](APPENDIX_beginner_glossary.md#g080) | Inputs and K grouping | seed / publication / rejection |
|---|---|---|
| B0 [16→32](APPENDIX_beginner_glossary.md#g007) adaptation | feat[16] at each position and 16 F16 [resource](APPENDIX_beginner_glossary.md#g079) items per output channel; one K16 per output | C=+0; first obtains 32 F16 values, then applies [Q8](APPENDIX_beginner_glossary.md#g061) for the [feed-forward](APPENDIX_beginner_glossary.md#g037) main path; the adapter F16 is also retained as the feed-forward [residual](APPENDIX_beginner_glossary.md#g017). The source rejects nonfinite operands and single-term [scaling](APPENDIX_beginner_glossary.md#g031) out-of-range; this function does not have the same terminal finite guard as B70 |
| B70 terminal head | The 32 F16 values at the [window](APPENDIX_beginner_glossary.md#g015) exit are split into two groups of 16 according to a fixed channel permutation; the two groups each use their own F16 head parameters | First step C=+0, second step C=first-step F16. Without [history](APPENDIX_beginner_glossary.md#g024), 3 RGB heads are computed, and with history, the confidence head is computed in addition; rejects nonfinite inputs/seed, integer sum range ≥2⁵², and terminal half [overflow](APPENDIX_beginner_glossary.md#g071) |

Call sites: [b00.hpp:16, 42–44](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L42), [outtail.cpp:94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L94). Resource coefficients are not disclosed; for subsequent color/history blending, see [B70](L3_b70_history_output.md#b70-mix). Whether the function can publish Inf and whether the caller accepts it must be examined separately.

<a id="qmma-difference"></a>
## Differences from sm_120 E4 QMMA

| Item | HMMA CPU rule on this page | [E4](APPENDIX_beginner_glossary.md#g055) QMMA rule in this skewer |
|---|---|---|
| A/B, items per step | F16, 16 items | E4, 32 items |
| Nonzero subnormal field exponent | −14 | −6 |
| seed / exit | F16; implicit zero in B0, explicitly carried in B70 | F16 seed, republishing F16 at each K32 |
| Common grid | Includes −21 lower bound and E−25 on this page; uses F16 fields | Sets the grid from E4 fields and half seed; see the independent arithmetic leaf |
| Evidence | Legacy candidate has 480 valid signed-zero counterexamples | A separate set of independent candidates, controls, and saved cases; cannot be borrowed to close the HMMA zero rule |

Operand formats, groupings, guards, and evidence are each [bound](APPENDIX_beginner_glossary.md#g103) separately. The appearance of E−25 on both pages does not make them interchangeable; nor can the legacy sm_75/sm_86 execution of F16 after E4 decoding be treated as native E4 QMMA.

<a id="hardware"></a>
## Cross-Architecture: What Is Legacy Hardware Observation, and What Remains Open

[Verification Record] The table below relays only named saved records with no new device runs; candidate survival is scoped strictly to those experimental test cases.

| Architecture | Candidate supported by saved observations | Scope and limitations |
|---|---|---|
| sm_75 / RTX 2060 | K8 field F24, full-K8 publication candidate | [Original report:56–71](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#L56); K8 results cannot be extrapolated to K16 on this page |
| sm_86 / RTX A2000 Laptop | K16 split into two K8 groups, truncating/publishing per group by F24 candidate; 65/65 discriminating cases and 3748/3748 real fragments | [Ampere report:9–24](../../../experiments/parity-claude-ampere-probe-r01-20260921/RESULT_ZH.md#L9); the full-K16 F25 candidate fails here |
| sm_89 / RTX 4090 D | HMMA candidate in the returned acceptance matches sm_86 | [Ada reading](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#L24); device, payload identity, and two-pass conditions are bound to the original return, not measured in this round |
| sm_120 | Legacy full-K16 F25 candidate; in the subsequent 1,380,992 cases, 1,380,512 match and 480 cases have CPU −0 / GPU +0 | [Follow-up sweep:25–31](../../../experiments/parity-proof-gpu-sweeps-r01-20261007-codex/RESULT_ZH.md#L25) formally falsifies the legacy combined rule; the sign of zero cannot be ignored |

[Native Behavior / Unknown] The 480-case discrepancy cannot be attributed in isolation to product truncation, internal accumulation, or final publication. Although the candidate that changes legacy output −0 to +0 matches that batch of saved cases, it remains [OPEN](APPENDIX_beginner_glossary.md#g104). This normalization was implemented in isolated candidate `63ff1ff6` and merged into historical seal `49a98a0b`, but the release line M/M2 did not carry it, so hmma_seed/hmma_dot/hmma_cached in the public v2.0.0-preview source code (GlassBox-NR `e4a9b42`) still publish −0; v2.0.1-preview (`636b321`) restored +0 normalization at the end of those three functions (0 mismatches on the sm_120 saved-sweep unit gate, 158/158 end-to-end on 1080p f0), while all other code references and line numbers in this document still follow the v2.0.0 source code; it is an implementation choice aligning with that batch of saved cases and does not upgrade the candidate to a proven rule. Arithmetic is not altered during documentation revisions. Nor does the passing record across all 63,488 finite half values with only the C input cover general A/B/C combinations: [narrow-domain acceptance:22–31](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L22). For the overall architecture adjudication, see [ARCH §7.2.2–7.2.3](../../../ARCHITECTURE_V3_ZH.md#L865).

Closure path (NOT_RUN): Fix a finite acceptance domain and first scan three separate groups—signed-zero products only, ±0 seed only, and exact cancellation of nonzero products; then keep the operand multiset unchanged while swapping only K8 grouping / term order, recording the native output [bit pattern](APPENDIX_beginner_glossary.md#g057) at each step. These controlled comparisons can rule out candidate rules for product zero signs, grouped cancellation, or terminal zero normalization, though a single exit still cannot uniquely prove the internal pipeline; no new hardware probes are run in this round, and legacy counterexamples are not normalized away.

<a id="worked-example"></a>
## Small Real C++ Example: Product Rounding and Cross-K16 Rounding

[CPU Reconstruction / Actual Execution] The [script](../skewer/examples/hmma_r04f.py) extracts the three original functions above together with the original half helper functions and executes synthetic inputs under [strict floating-point compilation](APPENDIX_beginner_glossary.md#g098) flags, without compiling network modules. The [source SHAs, compiler, flags, and output](../skewer/examples/hmma_r04f.result.json) can be verified, and the complete program is placed in examples.

First example: With the remaining 14 terms set to zero, A=[0x3c01,0xbc00], B=[0x3c01,0x3c02], C=0. The exact sum of products is
$(1+2^{-10})^2-(1+2^{-9})=2^{-20}$; with E=0 and g=2⁻²⁵, the result is published as F16 **0x0010**. If each product were converted to F16 first, the small term of the first product would be rounded off, and the cancellation result would be **0x0000**.

Second example: The first K16 has only two nonzero products, 1024 and 0.5, and RN16 tie-to-even yields 1024; the second K16 has only −1024 and 0.5, and carrying 1024 from the previous step yields 0.5. If intermediate F16 publication were removed, the real-number sum of the four terms would be 1.

~~~text
dot 0010
cached 0010
seeded 0010
product_half_control 0000
first_K16 6400
two_K16 3800
single_final_round_control 3c00
nonfinite_operand_refused
~~~

These two examples test the format, rounding positions, and a rejection branch of the current software, and are not model coefficients, new native measurements, or a complete acceptance-domain proof; hardware negative zero and the general finite K16 rule remain open as stated in the section above.
