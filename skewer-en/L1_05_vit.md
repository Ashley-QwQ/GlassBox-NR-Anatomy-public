### L1.05 ViT Bottleneck (launch L58–L99 / B31–B38)

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L58–L99<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B31–B38

[Beginner Handoff] 🔢 Receive the numbers on the smallest grid → rearrange into a sequence ordered by position, let every position exchange content with all valid positions, then rearrange back into a 2D organization → hand off to the [decoder](APPENDIX_beginner_glossary.md#g009) bridge.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: [Rearranges](APPENDIX_beginner_glossary.md#g019) low-resolution 2D [features](APPENDIX_beginner_glossary.md#g008) into a sequence, executes eight global blocks, and rearranges back to 2D.
- Input → output: X₆(1024) [E4](APPENDIX_beginner_glossary.md#g055) → P×1024 B sequence → X₆(1024) E4; T/P are the valid and [physical](APPENDIX_beginner_glossary.md#g085) row counts respectively.
- Computation order: L58 repack → eight groups of expand → contract → qkv → [attention](APPENDIX_beginner_glossary.md#g039) → projection → L99 inverse repack.
- Key exceptions: The contract [residual](APPENDIX_beginner_glossary.md#g017) comes from the block entry, and the projection residual comes from the contract exit. L58 padding performs genuine zero-writes; 4K L62 additionally zero-overwrites 16×1024 B after computation and cannot be omitted.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): eight blocks and residual wiring, MEASURED: named chains and padding fix; [ARCH 0.7 §5.2–§5.3, related §7.13](../../../ARCHITECTURE_V3_ZH.md#52-一维-vitl58l99).
- Next down: [L2.05 Six Families](L2_05_vit.md): [repack](L2_05_vit.md#repack), [expand](L2_05_vit.md#expand), [contract](L2_05_vit.md#contract), [qkv](L2_05_vit.md#qkv), [attention](L2_05_vit.md#attention), [projection](L2_05_vit.md#projection); follow the skewer into [L1.06](L1_06_decoder_bridge.md).
