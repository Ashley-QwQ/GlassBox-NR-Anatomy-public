### L1.03 TIN Encoder (launch L3–L24 / B1–B22)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L3–L24<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B1–B22

[Beginner Handoff] 🔢 Receive the sparser path from the input stage → pass through four tiers of sparser grids with increasing item counts per position, saving one [bypass](APPENDIX_beginner_glossary.md#g016) at each tier → hand off to the deep [window](APPENDIX_beginner_glossary.md#g015) section.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Four tiers of 8×8 window blocks progressively reduce spatial dimensions and increase [channels](APPENDIX_beginner_glossary.md#g007), retaining one [decoder](APPENDIX_beginner_glossary.md#g009) skip per tier.
- Input → output: X₁(32) [E4](APPENDIX_beginner_glossary.md#g055) of B0.[pool](APPENDIX_beginner_glossary.md#g018) → four-tier full X₁(32), X₂(64), X₃(128), X₄(256) → L24 pool X₅(512) E4.
- Computation order: At each tier, [inpview](APPENDIX_beginner_glossary.md#g022) → chained → ds_wait; the final block saves full, then pools in a fixed [half](APPENDIX_beginner_glossary.md#g054) order, [quantizes](APPENDIX_beginner_glossary.md#g061), and [projects](APPENDIX_beginner_glossary.md#g038) to the next tier.
- Key exceptions: The full exits of B4/B8/B14/B22 are handed to B66/B62/B56/B48 respectively; pool continues encoding. Zero [tokens](APPENDIX_beginner_glossary.md#g041) participate in window computation, and L6 statistical [overflow](APPENDIX_beginner_glossary.md#g071) and L24 actual [padding](APPENDIX_beginner_glossary.md#g085) zero-writes follow the lower-level [contracts](APPENDIX_beginner_glossary.md#g101).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): stages/shapes, MEASURED: single-primary-sample controlled comparisons of the four skips and named numeric chains; [ARCH 0.7 §4, current admission in §4.8](../../../ARCHITECTURE_V3_ZH.md#4-编码解码主干tin-swin).
- Next down: [L2.03 Four-Tier inpview/chained/ds_wait, 12 Slices in Total](L2_03_tin_encoder.md), where the four tiers of chained also list decoder launches; follow the skewer into [L1.04 split16 Encoder](L1_04_split16_encoder.md).
