# L4: E4M3 Bytes and sm_120 K32 Accumulation

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Back to L3 Matrix Chain](L3_qmma_e4m3.md#qmma-e4m3) · [Full Skewer](INDEX.md)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| b,s,e,m | [E4](APPENDIX_beginner_glossary.md#g055) [encoding](APPENDIX_beginner_glossary.md#g057), sign, stored [exponent](APPENDIX_beginner_glossary.md#g058), mantissa field |
| u(b), C | E4 decoding in 2⁻⁹ integer units, [half](APPENDIX_beginner_glossary.md#g054) [seed](APPENDIX_beginner_glossary.md#g042) |
| e_f,E,g | Field exponent, common [alignment exponent](APPENDIX_beginner_glossary.md#g066), grid step, distinguished from the stored exponent by context |
| L,S_min,S_exact | Maximum term / minimum nonzero product / unplaced sum of the large-[dynamic-range](APPENDIX_beginner_glossary.md#g071) cancellation guard |
| Q_g, [RNE16](APPENDIX_beginner_glossary.md#g059) | Grid-point placement [toward zero](APPENDIX_beginner_glossary.md#g060), round-to-nearest-even half [publication](APPENDIX_beginner_glossary.md#g091) |

<a id="e4m3-format"></a>
### L4.e4m3-format What One Stored Byte Actually Represents

- What it is: 1-bit sign, 4-bit exponent, 3-bit mantissa; the highest exponent field does not follow the [Inf](APPENDIX_beginner_glossary.md#g069) encoding of small IEEE formats.
- Input → output: One byte b → finite value or NaN flag; F16 [activations](APPENDIX_beginner_glossary.md#g045) are reverse-[quantized](APPENDIX_beginner_glossary.md#g061) to E4 bytes. [Matrix](APPENDIX_beginner_glossary.md#g051) segments use this encoding, while auxiliary [scales](APPENDIX_beginner_glossary.md#g031)/biases and temporary storage are still read according to their respective types.
- How it is computed:
  ~~~text
  s = b >> 7; e = (b >> 3) & 15; m = b & 7
  If e=15 and m=7: NaN encoding, rejected as an input to this QMMA
  If e=0: u = (−1)^s × m
  Otherwise: u = (−1)^s × (8+m) × 2^(e−1)
  Actual value = u × 2^−9; the two zero encodings separately preserve the stored sign
  ~~~
- Numeric rules: Decoding is an exact integer / power-of-two transform, and finite E4 values can be converted to F16 exactly. In the reverse direction, $Q8$ selects the nearest code and breaks ties to the even code; ±Inf saturates to ±448, and NaN is rejected. E4 has no Inf encoding, and 0x78 is still a finite number.
- Why it is computed this way: The bit fields determine the representable set; the short encoding reduces storage and movement of matrices/activations, while design intent is not proven by this round.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED (conversion acceptance domain); [half-domain primitives RESULT:43–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md).
- Next down: The bit format for this topic has reached the bottom; [K32 accumulation](#qmma-k32-accumulation).

```math
\mathrm{value}(b)=
\begin{cases}
(-1)^s m\,2^{-9}, & e=0,\\
(-1)^s(8+m)\,2^{e-10}, & e>0,\ (e,m)\ne(15,7).
\end{cases}
```

| Encoding category | Value / handling | Boundary |
|---|---|---|
| 0x00 / 0x80 | [+0](APPENDIX_beginner_glossary.md#g070) / −0 | The integer u is 0 for both; the helper function that converts directly to F16 preserves the sign of zero |
| e=0, m=1..7 | [Subnormal](APPENDIX_beginner_glossary.md#g068) | Smallest positive number $2^{-9}$, largest positive subnormal $7\cdot2^{-9}$ |
| e=1, m=0 | Smallest positive normal number | $2^{-6}$ |
| e=15, m=0..6 | Still finite | 0x78 is 256, 0x7e is 448; negative numbers flip the sign bit |
| 0x7f / 0xff | NaN | Two codes, no ±Inf encoding |
| All finite codes | Including both zeros | 254 codes in total; the enumeration classification in this round's script matches this count |

Hand-calculable definition of $Q8$: take the sign, choose among the positive E4 codes 0..126 the one at minimum distance from the input magnitude, break ties by choosing the code whose least significant bit is 0, and then restore the sign; saturate when the magnitude reaches 448 or is Inf. The production table-lookup optimization saves the result of this same function and adds no new rounding.

| Format assertion | Current public source path:line | Experiment / adjudication |
|---|---|---|
| Bit fields, integer unit, NaN rejection | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:22–25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L22), [primitives.inc:61–67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L61) | [Half-domain primitives RESULT:43](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md): pairwise unpacking accepts 64,516 and excludes 1,020 NaN-containing combinations; not an independent single-byte code count |
| E4→F16 preserves ±0, whereas [QMMA](APPENDIX_beginner_glossary.md#g065) integer decoding does not preserve the sign of zero | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L67), [qmma_sm120.hpp:25, 38](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L38) | [EQUIVALENCE:5, 7, 13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md); general hardware signed-zero contract not established |
| F16→E4 [satfinite](APPENDIX_beginner_glossary.md#g062), tie-to-even | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68), [same file:85–100](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L85) | [Half-domain RESULT:44–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md): 63,490 accepted and 2,046 NaN rejected each, zero differences on the acceptance domain; [nonfinite diagnostics:103](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md) explicitly records ±Inf saturation |
| Pre-decoded table saves value / NaN flag and reports an error only upon consumption | [GlassBox-NR/cpp/chain_tin_optm/decode_reuse.inc:2–13](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/decode_reuse.inc#L2), [qmma_sm120.hpp:72–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L72) | [Port RESULT:15–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| Numeric conversion differs from bit copying | [GlassBox-NR/cpp/chain_tin_optm/portable_bits.hpp:5–8](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/portable_bits.hpp#L5) | CENSUS: copies only bytes of same-width objects; cannot be treated as [quantization](APPENDIX_beginner_glossary.md#g061), and the conversion acceptance domain follows the experiments above |

<a id="qmma-k32-accumulation"></a>
### L4.qmma-k32-accumulation Common Grid Points and Exact Sum Across the Full K32

- What it is: 32 exact E4 products and one F16 seed are each placed onto common grid points, and F16 is published only once.
- Input → output: 32 pairs of finite E4 values and finite C → one F16; the analytical model can form Inf, which the default production wrapper rejects before returning.
- How it is computed:
  ~~~text
  1. Decode/check the seed first, then check the consumed E4 values in order to form the exact products p_i.
  2. E takes the maximum over the sum of the two operands' e_f for nonzero products and e_C for nonzero C.
  3. g = 2^(E−25); compute Q_g(C) and each term Q_g(p_i) separately.
  4. Starting from Q_g(C), add Q_g(p_i) exactly for i=0..31.
  5. Perform a single final RNE16, then accept/reject according to the production guards; there is no K8/K16 grouping or per-product half publication.
  ~~~
- Numeric rules: For normal E4, $e_f=e-7$, and for subnormals it is fixed at −6; for an F16 subnormal seed, $e_C$ still takes the unbiased exponent. Placement is RZ, with RN-even only at the end; subnormal F16 outputs are supported. The current software model normalizes a zero sum to +0.
- Why it is computed this way: field, F25, C entering the alignment maximum and being truncated, and full-K32 publication are the behaviors selected from the [frozen](APPENDIX_beginner_glossary.md#g103) candidates by hardware discrimination; this cannot be used to prove a unique internal addition tree.
- How we know: MEASURED / CENSUS (scopes kept separate); [RULE:17–29](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star).
- Next down: The arithmetic for this topic has reached the bottom; [publication/guards](#publish-guards), [executable examples](#worked-examples).

```math
e_f(x)=
\begin{cases}
e(x)-7,&x\text{ is normal E4},\\
-6,&x\text{ is nonzero subnormal E4},
\end{cases}
\quad
E=\max\!\left(\{e_f(a_i)+e_f(b_i):p_i\ne0\}\cup\{e_C:C\ne0\}\right).
```

```math
g=2^{E-25},\quad
Q_g(x)=\mathrm{sgn}(x)\left\lfloor |x|/g\right\rfloor g,\quad
\mathrm{out}=\mathrm{RNE}_{16}\!\left(Q_g(C)+\sum_{i=0}^{31}Q_g(p_i)\right).
```

When all products are zero, the value of a nonzero C is preserved; when C is also zero, the current implementation returns +0. For example, E4 0x01 has unbiased exponent −9, but $e_f$ is −6; replacing this with the maximum floor-log of the actual products yields a different, excluded model.

The integer correspondence is $c=C2^{24}$, $t_i=p_i2^{24}$, and $\mathrm{shift}=\max(E-1,0)$. The source code decodes both operands into integers in units of $2^{-9}$, multiplies them, and multiplies by 64, which yields $t_i$ exactly. Shifting the absolute values of c and each $t_i$ right and then left by shift bits before restoring the sign is what implements placement toward zero for negative numbers; it cannot be replaced directly by an arithmetic right shift on negative numbers. z takes the placed c first and then adds the placed $t_i$ term by term. When the original expression for shift is negative, the grid points are finer than $2^{-24}$ and every term is already on the integer-unit grid, so taking 0 does not change the result.

| Correspondence | Current public source path:line | Experiment / software record |
|---|---|---|
| E4 unit $2^{-9}$, seed unit $2^{-24}$ | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:22–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L22) | [EQUIVALENCE:5–7](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| field, unbiased exponent of C, C entering max | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:33, 50–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L33) | [RULE:19–24](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star); batch3 excludes the [value](APPENDIX_beginner_glossary.md#g067)/renorm classes |
| Products not pre-rounded to half, integer multiplied by 64 | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:54–55](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L54) | [EQUIVALENCE:7, 11](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md), [Port RESULT:15–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| RZ placement, C first then exact sum of 32 terms, single publication at the end | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:34–46, 58–65](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L34) | [RULE:21–22](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star), [EQUIVALENCE:9–13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |

For finite inputs, the magnitude of any integer [partial sum](APPENDIX_beginner_glossary.md#g050) does not exceed
$(32\cdot448^2+65504)2^{24}=108851114278912<2^{47}$.
Truncation does not increase magnitude, so int64 addition is exact; what can be [rearranged](APPENDIX_beginner_glossary.md#g019) are these integers, not F16 across K32 steps or network [floating-point](APPENDIX_beginner_glossary.md#g056) reductions. This round's script computes this bound; the software basis is EQUIVALENCE:11 and qmma_sm120.hpp:54–60.

<a id="publish-guards"></a>
## Where the Single Publication Rounds, and Where 65520 Is Rejected

For z, take the most significant magnitude bit top, retain 11 bits of significand, and let the remainder be r. Round up when r is greater than tie, or when r equals tie and q is odd; adjust the exponent when rounding up reaches 2048; the subnormal branch returns the corresponding mantissa. The current integer model has no intermediate binary64 rounding, nor are products pre-rounded to F16.

| Stage | Behavior | Current public source path:line / evidence |
|---|---|---|
| Receiving seed | NaN/Inf with exponent field 31 is rejected first | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:27–31, 50–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L27); [Port RESULT:15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) |
| Placement / sum | Exact summation after RZ, plus a range-error check for magnitude reaching $2^{52}$ | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:34–35, 58–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L58); [EQUIVALENCE:9–13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| [D27](APPENDIX_beginner_glossary.md#g109) domain restriction | Retains the legacy cancellation / dynamic-range rejection condition; computable by the finite model does not equal accepted in production | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:61–64](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L61); [Port RESULT:9, 15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#实现与定位) |
| F16 publication | Single integer RN-even; zero becomes +0, and overflow produces a signed Inf [bit pattern](APPENDIX_beginner_glossary.md#g057) | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:37–46, 65](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L37); [EQUIVALENCE:13](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/implementation/EQUIVALENCE_ZH.md) |
| Before production return | When model=false, a result exponent field of 31 triggers QMMA half overflow rather than returning Inf | [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp:66, 69–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L66); [nonfinite diagnostics:23, 104–105](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md) |
| Subsequent E4 quantization | Applies RN-even/satfinite again, which can introduce a second-format rounding difference | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L104), [primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68); Example C in this round |

D27 can be computed in integers: $L=\max(|c|,\max_i|t_i|)$, $S_{\min}=\min_{t_i\ne0}|t_i|$, $S_{\rm exact}=c+\sum t_i$. When L and a nonzero product exist, if
$\lfloor\log_2 L\rfloor-24\ge12$,
$\lfloor\log_2 L\rfloor-\lfloor\log_2 S_{\min}\rfloor\ge20$, and
$\lfloor\log_2 L\rfloor-\lfloor\log_2|S_{\rm exact}|\rfloor\ge2$
all hold simultaneously, production rejects; when the exact sum is 0, 99 is used for the last quantity. The minimum term is taken only over the products, while the maximum term includes the seed. This is a domain guard, not a hardware boundary proven in this round.

**65520 is the F16 overflow midpoint of the sum after grid-point placement.** Above the largest positive finite value 65504, the spacing to the next step is 32 and the midpoint is 65520; ties round up to the overflow side. For nearby values with magnitude below 65520, this model can publish 65504; for values with magnitude reaching 65520, it forms Inf and then rejects. Grid-point placement must be performed first—the threshold cannot be applied directly to the untruncated mathematical dot product. See also [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:35–58](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L35), where line 42 explicitly includes equality. The software threshold does not prove a complete hardware mixed nonfinite/overflow contract.

<a id="build-selection-r04l"></a>
## Compile-Time Selection Contract (Audit V07.01, Rank 2)

Only `QMMA_TARGET_SM120 == 1` enters the field/F25 core on this page; when undefined or set to any other value, it enters the retained legacy value/D27 branch. Selection cannot be presumed from the [host](APPENDIX_beginner_glossary.md#g096) [GPU](APPENDIX_beginner_glossary.md#g078) or the mere presence of header files. Named isolated builds record both `-DQMMA_TARGET_SM120=1` and forced inclusion of the shared header, with attribution governed by that build manifest and its source identity; this does not automatically prove that an arbitrary downstream binary used the same options. [build_manifest_v3.json:13–15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/build_manifest_v3.json#L13), [selection entry:107–110](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L107).

The complete alternative formula of the legacy branch is: in units of $2^{-24}$, `c=F16(seed)*2^24`, `t[i]=u(a[i])*u(b[i])*64`, `L=max(abs(c),max(abs(t)))`, and `shift=max(floor(log2(L))+1-27,0)` (when L=0, the internal log takes −99). With `place(v)=sign(v)*((abs(v)>>shift)<<shift)`, starting from `place(c)`, add `place(t[i])` in order 0..31; this shifts the magnitude right and then restores the sign, without performing an arithmetic right shift on negative numbers. Reject if the sum magnitude is ≥2^52, then apply the three D27 conditions above; finally perform a single RN16(sum*2^-24), rejecting an all-1s exponent. This legacy branch must not be conflated with field/F25. [ffn_contract.cpp:111–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L111), [same formula in TIN:129–153](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L129).

<a id="worked-examples"></a>
## Synthetic Examples: From Input Bytes to F16 Output

Both left and right inputs are synthetically constructed, **without reading or listing model coefficients**. The bytes below list the first three items in hexadecimal, with the remaining items padded with positive zero to 32 pairs; the initial seed=0x0000 unless stated otherwise. The script executes directly and cross-checks comparable roundings using independent exact Fraction arithmetic and Python F16 conversion.

### A: Rounding Only at the End Within a Single K32

Left [38,01,01], right [38,28,01], with products $1,2^{-11},2^{-18}$. E=0 and $g=2^{-25}$, so no bits are lost.
The integer terms are 16777216, 8192, and 64, summing to 16785472, with actual value $262273/262144$.
It lies above the F16 midpoint $1+2^{-11}$, outputting **0x3c01**, i.e., $1+2^{-10}$.

If the first two pairs are placed in the first step and the third pair is placed separately in the next K32: the first step $2049/2048$ is an exact midpoint, which rounds to 0x3c00 under tie-to-even; the second step uses that as its seed, and after adding $2^{-18}$ it remains **0x3c00**. This illustrates the difference between full-K32 and grouped publication; this [operator](APPENDIX_beginner_glossary.md#g035) does not introduce extra grouping merely because only three terms are nonzero.

### B: Grid-Point Placement Cannot Be Omitted

Left [78,f8,01], right [38,38,01], with products $256,-256,2^{-18}$.
E=8 and $g=2^{-17}$, so RZ turns the last term into 0, outputting **0x0000**.
Ignoring the grid points and converting the exact sum $2^{-18}$ directly to F16 would yield **0x0040**.
The magnitudes of the first two terms do not reach the top condition of the large-dynamic-range cancellation guard, so this production example is accepted.

### C: Second-Format Rounding from F16 Followed by E4

Both left and right are [38,28,01], with exact result $1+2^{-4}+2^{-18}=278529/262144$.
Converting to F16 first yields **0x3c40**, with value $17/16$; this then lies at the E4 midpoint between 1 and $9/8$, where tie-to-even selects **0x38**.
Converting directly to E4 from the unrounded exact value lies slightly above the midpoint and selects **0x39**.
This is two publications to different target formats, not an extra binary64→F16 rounding inside K32.

### D: 65520 and Default Production Guards

| Left first three bytes | Right first three bytes | Sum after placement | Default production result |
|---|---|---:|---|
| [78,c8,b8] | [78,48,38] | 65519 | 0x7bff, i.e., 65504 |
| [78,c8,00] | [78,48,00] | 65520 | QMMA half overflow; analytical publication bit pattern 0x7c00 |
| Flip signs of left inputs in previous row | Same as previous row | −65520 | QMMA half overflow; analytical publication bit pattern 0xfc00 |

With E=16 and $g=2^{-9}$, all listed values are placed exactly. Analytical mode only displays the model bit pattern prior to rejection and does not count as a production return value or a hardware measurement.

### Actual Execution Script

The intermediate integer unit is $2^{-24}$. e4_from_units is used only for nearest-code comparison on finite values in this example; the full NaN/Inf conversion contract is listed in the format slice above. Requires no project modules, [weights](APPENDIX_beginner_glossary.md#g079), mathematical [function tables](APPENDIX_beginner_glossary.md#g074), or GPU:

See the appendix for the [complete program and raw output](APPENDIX_evidence_history.md#e4-example-source); the format and K32 arithmetic examples are retained above.
