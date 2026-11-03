# L2.07 split16 Decoder

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [Back to Parent L1](L1_07_split16_decoder.md) · [Page Terminology](INDEX.md#shape-and-workspace-notation)

## Four Families Reused in the Decoder Stage

The table below serves only as navigation for this stage and does not redefine coverage; complete [launch](APPENDIX_beginner_glossary.md#g080) lists, per-instance variations, and main text are in the linked slices.

| Launches in this stage | Reused main text |
|---|---|
| L101, 105, 109, 113, 117, 121, 125, 129 | [ffwd](L2_04_split16_encoder.md#ffwd) |
| L102, 106, 110, 114, 118, 122, 126, 130 | [ffwd_proj](L2_04_split16_encoder.md#ffwd-proj) |
| L103, 107, 111, 115, 119, 123, 127, 131 | [qkv](L2_04_split16_encoder.md#qkv) |
| L104, 108, 112, 116, 120, 124, 128 | [proj](L2_04_split16_encoder.md#proj) |


This stage reuses the [field closed forms and held-out boundaries](L3_split16_window.md#rest-closed-form-r04o) of F20, F21, and F19: the non-empty wload/shared/sread/gstore of F20 and the six non-empty address fields of F21 are EXACT; shared/sread/gstore of F19 are EXACT, while the historical r02 table shape failures on its wload and two xsite fields have been classified by r04 as NON_PRODUCTION_VARIANT, with the accepted maps and 4K tables EXACT and the original failures retained. The general plane formula is `16384*(e//4)+2048*h+512*(e%4)+16*lane`, while the second half of F20 switches to expansion/contraction segments; writebacks follow 4×4 physical blocks, with −1 skipped. thread_class remains TABLE, and the 68×120 4K tables for F19/F20/F21 are EXACT field by field; no receipt proves that the C++ executor reads a specific 12×12 accepted map. This paragraph does not cover the dedicated L132 terminal view below.

<a id="outview"></a>
<!-- coverage: {"launches":[132],"kernels":["cc_split_swin_16h_proj_512_outview_wait_fp8"]} -->
### L2.07.outview split16 Terminal proj_outview_wait (Output-View Terminal Block) (1 Launch)

- Coverage: L132 / B47.
- What it is: Executes the output [projection](APPENDIX_beginner_glossary.md#g038) of the final [window](APPENDIX_beginner_glossary.md#g015) block and writes it into the view required by the [TIN](APPENDIX_beginner_glossary.md#g011) [decoder](APPENDIX_beginner_glossary.md#g009).
- Input → output: B47 [attention](APPENDIX_beginner_glossary.md#g039) exit and the current block's post-[feed-forward](APPENDIX_beginner_glossary.md#g037) [residual](APPENDIX_beginner_glossary.md#g017) → tier-5 [512](APPENDIX_beginner_glossary.md#g007)-channel [E4](APPENDIX_beginner_glossary.md#g055) [outview](APPENDIX_beginner_glossary.md#g022), located at the [workspace](APPENDIX_beginner_glossary.md#g082) exit given by the current [parameter block](APPENDIX_beginner_glossary.md#g083).
- How it is computed:
  ~~~text
  1. Read the two input roles and projection weights of B47
  2. Assemble projection and residual sources according to the gather maps
  3. Execute the frozen matrix/elementwise graph, preserving original quantization points
  4. Write out outview according to the terminal output indices
  5. Complete the handoff of this section for the B48 main path to read
  ~~~
- [Logical](APPENDIX_beginner_glossary.md#g085) handoff: B47's window attention exit and the same block's post-feed-forward residual are merged via projection and written back as outview for B48 [upsampling](APPENDIX_beginner_glossary.md#g021); the physical event axes serve only to lower this wiring to bytes.
- Index structure: [wload_off](APPENDIX_beginner_glossary.md#g090) ([weight](APPENDIX_beginner_glossary.md#g079) offsets), sread_src (input sources), and gstore_off (writeback offsets) are [bound](APPENDIX_beginner_glossary.md#g103) by block × sub-block × 32 parallel positions × event, at 16 B per write event. The eight address/index fields of qkv have [closed forms validated on held-out tables](L3_split16_window.md#qkv-closed-form-r04n), with both encoder and decoder copies included in the research inventory; thread_class remains table-driven; per-field evidence for the remaining families is given under F19/F20/F21 above and is not extrapolated to this singleton. L132 is wired by the dedicated [mapexec](APPENDIX_beginner_glossary.md#g089) in entry.
- Semantics: The output projection brings the attention result back to the block width and merges in the same-block residual; outview is its storage interface to the B48 main path.
- Numeric rules: E4 inputs [publish](APPENDIX_beginner_glossary.md#g091) [F16](APPENDIX_beginner_glossary.md#g054) at each [K32](APPENDIX_beginner_glossary.md#g065), and the output is then [quantized](APPENDIX_beginner_glossary.md#g061) to E4; view [rearrangement](APPENDIX_beginner_glossary.md#g019) adds no extra rounding, and residual/[reduction](APPENDIX_beginner_glossary.md#g050) order is not swapped arbitrarily.
- Per-instance variation: The singleton's weights, two inputs, output interval, signed window origin, and geometry are bound individually; its terminal map cannot be directly replaced by an ordinary proj.
- Why it is computed this way: This exit is the input to the stage-by-stage upsampling pathway, and the view writeback handles the handoff between the two consumption layouts.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) (wiring), INFERRED (semantics); [L132 bridge entry in ARCH 0.7 §5.1](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维).
- Next down: [L3.workspace-map (Terminal Address Mappings)](L3_workspace_map.md#address-maps); [L3.window-attention (Complete Block, Projection, and Residual)](L3_split16_window.md#window-attention).
