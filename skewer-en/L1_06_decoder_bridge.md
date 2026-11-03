### L1.06 Decoder Bridge (launch L100 / B39)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L100<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B39

[Beginner Handoff] 🔢 Receive the global-section main path and the pre-[bottleneck](APPENDIX_beginner_glossary.md#g010) retained [bypass](APPENDIX_beginner_glossary.md#g016) → known: four [channel](APPENDIX_beginner_glossary.md#g007) groups are merged in order and reconnected with the bypass; full spatial restoration [operator](APPENDIX_beginner_glossary.md#g035)? still undetermined → hand off to the denser-grid [window](APPENDIX_beginner_glossary.md#g015) [decoder](APPENDIX_beginner_glossary.md#g009) section.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Joins the 1024-channel bottleneck main path with B30's 512-channel bypass into the decoder entry.
- Input → output: X₆(1024) [E4](APPENDIX_beginner_glossary.md#g055) of L99 + X₅(512) E4 of B30.[full](APPENDIX_beginner_glossary.md#g018) → X₅(512) E4 of B39.out.
- Computation order: Four paths of 8×[K32](APPENDIX_beginner_glossary.md#g065)=256 channels each; [reduce](APPENDIX_beginner_glossary.md#g050) all 1024 channels in (3+1)-term [half](APPENDIX_beginner_glossary.md#g054) order → perform [HF](APPENDIX_beginner_glossary.md#g063) with the [scaled](APPENDIX_beginner_glossary.md#g031) skip → E4.
- Key exceptions: Preserves per-K32 F16 [publication](APPENDIX_beginner_glossary.md#g091), three-term reduction order, and HF boundaries; specific [interpolation](APPENDIX_beginner_glossary.md#g020)/convolution semantics are not independently confirmed and cannot be determined from the kernel name alone.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED ([M2](APPENDIX_beginner_glossary.md#g107) data structures and explicit arithmetic; see INDEX separately for numeric coverage); [decoder in chain_entry_optm/entry.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp).
- Next down: [L2.06 Decoder Bridge Singleton: Projection, Index Expansion, Three-Term Reduction, Bypass Merge, and Publication](L2_06_decoder_bridge.md#bridge), [1080 Dataflow Diagram](L2_06_decoder_bridge.md#wiring); follow the skewer into [L1.07 split16 Decoder](L1_07_split16_decoder.md).
