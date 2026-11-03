### L1.08 TIN Decoder (launch L133–L154 / B48–B69)

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L133–L154<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B48–B69

[Beginner Handoff] 🔢 Receive the deep [decoder](APPENDIX_beginner_glossary.md#g009) exit and the four encoder [bypasses](APPENDIX_beginner_glossary.md#g016) → densify four times while reconnecting the same-tier bypasses, returning to 32 items per position → hand off to the tail end, with main-path width and height still each half of the internal canvas.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Four tiers of [projective](APPENDIX_beginner_glossary.md#g038) [upsampling](APPENDIX_beginner_glossary.md#g021) reconnect the encoder skips and restore [512](APPENDIX_beginner_glossary.md#g007)-channel deep [features](APPENDIX_beginner_glossary.md#g008) back to 32 channels.
- Input → output: B47.[outview](APPENDIX_beginner_glossary.md#g022) X₅(512) and the four encoder [full](APPENDIX_beginner_glossary.md#g018) tiers → X₄(256) → X₃(128) → X₂(64) → B69.outview X₁(32), all in [E4](APPENDIX_beginner_glossary.md#g055).
- Computation order: L133/141/147/151: main-path projection → nearest-neighbor ×2 → projected main path plus [scaled](APPENDIX_beginner_glossary.md#g031) skip → [window](APPENDIX_beginner_glossary.md#g015) block; followed by chained and outview to finish.
- Key exceptions: The [feed-forward](APPENDIX_beginner_glossary.md#g037) [seed](APPENDIX_beginner_glossary.md#g042) of 1-head upsample retains the un-[quantized](APPENDIX_beginner_glossary.md#g061) merged value, whereas multi-head quantizes to E4 first and then decodes. At 1440, the first tier has valid height 92; B69's independent layout and L133's independent provenance proof retain their boundaries as stated in L2.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED: per-tier merging, single-sample skips, and named chains; [ARCH 0.7 §4.5–§4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66); current numeric gates do not lift the symbolic-tier [NOT_ADMITTED](APPENDIX_beginner_glossary.md#g104) status of L133.
- Next down: [L2.08 Eight Four-Tier upsample/outview Slices and Shared chained Navigation](L2_08_tin_decoder.md); follow the skewer into [L1.09 B70](L1_09_b70.md).
