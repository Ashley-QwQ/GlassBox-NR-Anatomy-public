### L1.04 split16 Encoder (launch L25–L57 / B23–B30)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L25–L57<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B23–B30

[Beginner Handoff] 🔢 Receive the exit of the four [encoding](APPENDIX_beginner_glossary.md#g009) tiers → process eight consecutive blocks inside small [windows](APPENDIX_beginner_glossary.md#g015), then split into a sparser main path and a retained [bypass](APPENDIX_beginner_glossary.md#g016) → hand the main path to the global section and the bypass to the bridge.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Eight [16-head](APPENDIX_beginner_glossary.md#g013), [512](APPENDIX_beginner_glossary.md#g007)-channel window blocks feed the [TIN](APPENDIX_beginner_glossary.md#g011) encoder exit into the [global bottleneck](APPENDIX_beginner_glossary.md#g010).
- Input → output: X₅(60×36×512) covers 64×40 with 8×5 windows of 8×8, and the exit [logical](APPENDIX_beginner_glossary.md#g085) capacity is X₆(32×20×512); [Inference] each window corresponding to a 4×4 spatial exit is an interpretation compatible with the layout, while independent window-to-exit coordinate pairing is not yet established—for the required evidence, see [geometry boundaries](L3_split16_window.md#heads). Also retains the B30.[full](APPENDIX_beginner_glossary.md#g018) skip, and L57 adapts to 1024 channels.
- Computation order: Eight groups of [ffwd](APPENDIX_beginner_glossary.md#g037) → ffwd_proj → qkv → [proj](APPENDIX_beginner_glossary.md#g038); the first group receives [inpview](APPENDIX_beginner_glossary.md#g022), and the final group splits via L56 proj_pool before feeding into L57 final_head.
- Key exceptions: full and pooled each have their own writeback provenance and cannot be replaced by unverified library pooling. Physical execution axes do not equal logical spatial/channel axes; exact mappings are deferred to L3.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): topology, MEASURED: named segments / full chains; [ARCH 0.7 §5.1](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维).
- Next down: [L2.04 Eight Family Slices](L2_04_split16_encoder.md), where the four chained families also list decoder launches; follow the skewer into [L1.05 ViT](L1_05_vit.md).
