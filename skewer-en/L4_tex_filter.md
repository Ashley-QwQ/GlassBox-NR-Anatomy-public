# L4.tex-filter: 1/256 Fixed-Point Subpixel Grid, Joint 8-Bit Fractional Weights, and Texture half Publication

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.

<a id="beginner-sampler-fields"></a>
[CB](APPENDIX_beginner_glossary.md#g083)+0x40 is a byte position inside a launch's parameter package (from which a specific consumer may read a resource [handle](APPENDIX_beginner_glossary.md#g096)), whereas 1/256 is the coordinate/weight grid step inside filtering; the 2 are not the same name, nor is there any relationship given here where that field controls this grid step. For the beginner diagram of [sampling](APPENDIX_beginner_glossary.md#g027), see [5-Point / 4-Corner Nesting](L1_00_history_primer.md#nested-sampling).
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · Parent level: [B0 5-tap](L3_b0_input.md#five-tap) · Adjacent: [half Format](L4_half_arith.md#format), [F32 Boundaries](L4_fp32_ftz.md#sites)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

<a id="tex-filter"></a>
## Inputs and Step-by-Step Rounding

[CPU Reconstruction] This is the finite-color filtering model for B0 [history](APPENDIX_beginner_glossary.md#g024) [RGBA16F](APPENDIX_beginner_glossary.md#g028). Each TEX fetch first produces a [half](APPENDIX_beginner_glossary.md#g054), which is then expanded exactly to [F32](APPENDIX_beginner_glossary.md#g056) for [5-tap](APPENDIX_beginner_glossary.md#g029) weight merging; that half and the final [RN16](APPENDIX_beginner_glossary.md#g059) are 2 separate [publication](APPENDIX_beginner_glossary.md#g091) positions. W/H and the boundary contract are supplied by the [caller](APPENDIX_beginner_glossary.md#g080).

Local notation: a,b are integers on the 2-axis 1/256 fixed-point subpixel grid, taking values 0..255; w₀…w₃ are the integer numerators of the 4-corner joint 8-bit fractional weights, and step is the color truncation grid step. The sampler receives only the texture, dimensions, coordinates, and component, without reading CB parameters; for global formats, see [INDEX](INDEX.md#shape-and-workspace-notation).

1. Clamp the F32 pixel-center coordinate to [0.5,W−0.5]; xq=floor(double(x)×256+0.5)−128, with ix=xq//256 and a=xq%256. The y axis is handled analogously, clamping neighbors to the last valid texel.
2. br=(a*b+128)/256, taking the integer-division quotient (i.e., floor for nonnegative integers); the 4-corner weights are [256−a−b+br,a−br,b−br,br]/256. The weights are jointly [quantized](APPENDIX_beginner_glossary.md#g061) first rather than computing 4 independent high-precision bilinear products.
3. largest takes the maximum absolute value among texels with nonzero weights; when not all zero, step=2^(floor(log₂(largest))−14).
4. Each color first computes [trunc](APPENDIX_beginner_glossary.md#g060)(color/step)×step, then multiplies by its weight, and sums in binary64 in the original 4-corner order; truncation cannot be moved after the weighted multiplication.
5. Publish the nearest half, with midpoints rounding away from zero; when a single active contribution is negative zero, [−0](APPENDIX_beginner_glossary.md#g070) is preserved. An all-zero case takes the zero-value path without using log(0) to select a grid step.

Source code: [native_temporal.hpp:10–25](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L10). Its implementation calls ordinary half_round first and then adjusts to the adjacent encoding only at exact midpoints, so ordinary half RN-even cannot substitute for this step.

<a id="worked-example"></a>
## Synthetic Single Point: Truncation, Joint Weights, and Midpoint

[Real-Code Computation] The [script](../skewer/examples/substitutions_r04g.py) directly extracts and executes tn_sample on entirely synthetic texels; [output and source/function-table SHAs](../skewer/examples/substitutions_r04g.result.json) can be verified.

Take the 2×2 texels TL/TR/BL/BR=[1,2⁻²⁰,−0.5,2] and sampling point (0.5+73/256,0.5+119/256). With a=73, b=119, and br=34, the 4-corner integer weights are [98,39,85,34], summing to 256. largest=2 and step=2⁻¹³; TR is truncated toward zero to 0, while the other 3 values remain unchanged. The weighted sum is (98−42.5+68)/256=0.482421875, and the real TEX output is half **0x37b8**.

Next take the same top row with TL=1, TR=1.125, and point (0.5+1/256,0.5). The 2 weights are 255/256 and 1/256, giving a sum of 1+2⁻¹¹, which lies at an exact half midpoint. Real texture publication yields **0x3c01**, whereas ordinary RN-even gives **0x3c00**. These 2 examples separately distinguish joint 8-bit fractional weights / shared-[exponent](APPENDIX_beginner_glossary.md#g058) truncation and the final midpoint rule.

[Native Behavior / Verification Scope] [texture-align mechanism and discriminating experiments](../../../experiments/parity-b2-texture-align/TEXTURE_ARITHMETIC_ZH.md#可复核的-cpu-机制) record finite-color observations on named devices/configurations; for subsequent [sm_120](APPENDIX_beginner_glossary.md#g078) prefix verification, see [B0 evidence](L3_b0_input.md#evidence). Synthetic examples do not constitute a new GPU acceptance and do not generalize to arbitrary sampler [descriptors](APPENDIX_beginner_glossary.md#g088) or [nonfinite](APPENDIX_beginner_glossary.md#g069) texels.
