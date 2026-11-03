# L2.08 TIN Decoder: upsample and outview

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [Back to Parent L1](L1_08_tin_decoder.md)

[TIN](APPENDIX_beginner_glossary.md#g011) is a [window](APPENDIX_beginner_glossary.md#g015)-block [family](APPENDIX_beginner_glossary.md#g080), upsample is the [upsampling](APPENDIX_beginner_glossary.md#g021) transition block, and [outview](APPENDIX_beginner_glossary.md#g022) is the output [physical](APPENDIX_beginner_glossary.md#g085) view; for [E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054), [K32](APPENDIX_beginner_glossary.md#g065), [RN-even](APPENDIX_beginner_glossary.md#g059), [seed](APPENDIX_beginner_glossary.md#g042), [skip](APPENDIX_beginner_glossary.md#g016), and X_r(C), see the [notation table](INDEX.md#shape-and-workspace-notation). Logical shapes in the table default to E4, with extents following actual [params](APPENDIX_beginner_glossary.md#g083). Upsampling first performs a 2C→C [projection](APPENDIX_beginner_glossary.md#g038); for the single-head / multi-head [matrix](APPENDIX_beginner_glossary.md#g051) decomposition of window [FFN](APPENDIX_beginner_glossary.md#g037), see [L3.ffn](L3_ffn.md#channels), keeping known matrix widths separate from independent physical layouts that remain unknown.

## chained Reused in the Decoder

This table serves only for navigation; coverage remains uniquely attributed to the shared families on the [encoder](APPENDIX_beginner_glossary.md#g009) side.

| Launches in this stage | Shared main text |
|---|---|
| L134–L139 | [8h / 256 channels](L2_03_tin_encoder.md#chain-256) |
| L142–L145 | [4h / 128 channels](L2_03_tin_encoder.md#chain-128) |
| L148–L149 | [2h / 64 channels](L2_03_tin_encoder.md#chain-64) |
| L152–L153 | [1h / 32 channels](L2_03_tin_encoder.md#chain-32) |

## Shared Computation of the Two Families

- **What upsample is / input → output / how it is computed:** Decodes the main path according to the previous tier's outview and projects to the target [channel](APPENDIX_beginner_glossary.md#g007) count; takes floor(x/2),floor(y/2) of the previous tier at the target coordinates for a nearest-neighbor ×2 expansion; merges via [HF](APPENDIX_beginner_glossary.md#g063)([D8](APPENDIX_beginner_glossary.md#g061)(skip),s_skip,projected_main), i.e., the projected main path plus this tier's [scaled](APPENDIX_beginner_glossary.md#g031) encoder [full](APPENDIX_beginner_glossary.md#g018) skip; executes the first window block according to this tier's seed rule, writing only the declared valid range and [publishing](APPENDIX_beginner_glossary.md#g091) control words. The window origin shifts only the window-partition grid, not the nearest-neighbor source coordinates.
- **What outview is / input → output / how it is computed:** Reads this tier's internal [features](APPENDIX_beginner_glossary.md#g008), [weights](APPENDIX_beginner_glossary.md#g079), and window origin, partitions into 8×8 windows, and zero-pads out-of-bounds positions; executes feed-forward, [normalization](APPENDIX_beginner_glossary.md#g043), [attention](APPENDIX_beginner_glossary.md#g039), and [residual](APPENDIX_beginner_glossary.md#g017) projection; writes a same-shape E4 view at the original quantization point and completes the terminal handoff. It includes a full window computation and cannot be treated as a pure copy, nor does it have an extra pool.
- **Numeric rules:** Publishes F16 at each K32; half fused rounding and E4 RN-even points are preserved. Multi-head quantizes the merged value first and then decodes it as the feed-forward seed, and its tail seed likewise takes the quantized-then-decoded feed-forward result; 1-head upsample retains the unquantized merged value as the feed-forward seed; the tail projection of each 1-head block retains the unquantized feed-forward value. Exit layout [rearrangement](APPENDIX_beginner_glossary.md#g019) performs no further rounding. For function domains / [nonfinite](APPENDIX_beginner_glossary.md#g069) values and QMMA [overflow](APPENDIX_beginner_glossary.md#g071) guards, see the [nonfinite contract](L3_norm_nonfinite.md#norm-nonfinite).
- **Why:** upsample reconnects this tier's encoder bypass and restores the spatial density of the main path; outview hands this tier's result off to the next tier's reading layout, and at the finest tier hands it off to B70. Training and fusion design motivations are unknown; generic rationales are not repeated for each scale.

## Variant Table

| Family / entry | launches / B | Logical shape | Residual sources | seed quantization | layout | Actual differences |
|---|---|---|---|---|---|---|
| <a id="up-256"></a>upsample 8h/256 | L133 / B48 | X₅(512) + X₄(256) skip→X₄(256) | B22/L24.full, then current-window input / feed-forward | Both merged value and tail feed-forward value E4-quantized then decoded | Previous tier's outview → this tier's internal | First-window origin (0,0); weights/skip/valid range [bound](APPENDIX_beginner_glossary.md#g103) per configuration; 1440 valid height 92, window canvas can be 96, writes only valid output; publishes only without waiting |
| <a id="out-256"></a>outview 8h/256 | L140 / B55 | X₄(256)→same shape | Current-window input and feed-forward result | Tail seed E4-quantized then decoded | 16 channels/plane, 16 B per spatial position per plane, channel permutation per configuration | Read by subsequent upsampling, no extra pooling |
| <a id="up-128"></a>upsample 4h/128 | L141 / B56 | X₄(256) + X₃(128) skip→X₃(128) | B14/L16.full, then current-window input / feed-forward | Both merged value and tail feed-forward value E4-quantized then decoded | Previous tier's outview → this tier's internal | First-window origin (−4,0); weights/skip/valid range bound per configuration |
| <a id="out-128"></a>outview 4h/128 | L146 / B61 | X₃(128)→same shape | Current-window input and feed-forward result | Tail seed E4-quantized then decoded | 16 channels/plane, 16 B per spatial position per plane, channel permutation per configuration | Read by subsequent upsampling, no extra pooling |
| <a id="up-64"></a>upsample 2h/64 | L147 / B62 | X₃(128) + X₂(64) skip→X₂(64) | B8/L10.full, then current-window input / feed-forward | Both merged value and tail feed-forward value E4-quantized then decoded | Previous tier's outview → this tier's internal | First-window origin (0,0); weights/skip/valid range bound per configuration |
| <a id="out-64"></a>outview 2h/64 | L150 / B65 | X₂(64)→same shape | Current-window input and feed-forward result | Tail seed E4-quantized then decoded | 16 channels/plane, 16 B per spatial position per plane, channel permutation per configuration | Read by subsequent upsampling, no extra pooling |
| <a id="up-32"></a>upsample 1h/32 | L151 / B66 | X₂(64) + X₁(32) skip→X₁(32) | B4/L6.full, then current-window input / feed-forward | Both merged value and tail feed-forward value retained unquantized | Previous tier's outview → this tier's internal | First-window origin (0,0); weights/skip/valid range bound per configuration |
| <a id="out-32"></a>outview 1h/32 | L154 / B69 | X₁(32)→same shape | Current-window input and feed-forward result | Tail seed unquantized | [M2](APPENDIX_beginner_glossary.md#g107) configured per [outputlayout](APPENDIX_beginner_glossary.md#g088); independent native verification [UNKNOWN](APPENDIX_beginner_glossary.md#g104) | Reused by subsequent B70 at half-resolution coordinates; layout conclusion not upgraded merely from sharing an executor |

Each launch binds its weights, residual addresses, window origin, source physical width and height, output layout, and valid range according to the current configuration, without generalizing from small square samples. The planar layout of multi-head outview does not automatically constitute independent evidence for B69.

**Retained unknowns:** [computed-shared](APPENDIX_beginner_glossary.md#g108) refers to the write→read provenance proof for computed shared-memory intermediates ([terminology](INDEX.md#项目与验证术语)), not an additional network layer. The symbolic provenance tier of L133 computed-shared remains NOT_ADMITTED; passing the numeric chain does not lift that status. B69's independent native layout remains UNKNOWN (ARCH §4.4); the minimum closure condition is to independently determine the logical position/channel labels of native L154 output bytes, compare them item by item against the current outputlayout, and then verify the source fetched by L155 at half-resolution coordinates—it can be closed only after both mappings agree and pass identity, scope, and counterexample controls. That witness is currently absent and cannot be derived solely from sharing the same CPU executor.

- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) (families/layouts/wiring), MEASURED (named merges and exits); [ARCH §4.5, §4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66), [outview §4.4](../../../ARCHITECTURE_V3_ZH.md#44-outview-核b55--b61--b65同属-tinlayout_fused_-家族但输出不是-tin-布局).
- Next down: [L3.tin-window: Complete Block Handoff](L3_tin_window.md#tin-window), [documented window attention](L3_attention_softmax.md#window-attention), [half fused rounding](L4_half_arith.md#half-arith), [write sets and layouts](L3_workspace_map.md#write-sets).

<!-- coverage: {"launches":[133],"kernels":["cc_tinlayout_fused_swin_8h_256_8_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[140],"kernels":["cc_tinlayout_fused_swin_8h_256_8_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[141],"kernels":["cc_tinlayout_fused_swin_4h_128_4_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[146],"kernels":["cc_tinlayout_fused_swin_4h_128_4_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[147],"kernels":["cc_tinlayout_fused_swin_2h_64_2_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[150],"kernels":["cc_tinlayout_fused_swin_2h_64_2_outview_wait_fp8"]} -->
<!-- coverage: {"launches":[151],"kernels":["cc_tinlayout_fused_swin_1h_32_1_upsample_tilesync_fp8"]} -->
<!-- coverage: {"launches":[154],"kernels":["cc_tinlayout_fused_swin_1h_32_1_outview_wait_fp8"]} -->
