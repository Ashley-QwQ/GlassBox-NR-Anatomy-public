### L1.02 Input Stage B0 (launch L2 / B0)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L2<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B0

[Beginner Handoff] 🖼 Receive the current image, motion information, available old image, and controls → 🔢 assemble 16 conditioning items and turn them into 32 internal numbers → send one path to the [encoder](APPENDIX_beginner_glossary.md#g009), and keep one path for the tail end.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Within a single launch, B0 generates noise, prepares [history](APPENDIX_beginner_glossary.md#g024) conditioning, and completes [16→32](APPENDIX_beginner_glossary.md#g007) channel adaptation and the first [window](APPENDIX_beginner_glossary.md#g015) block.
- Input → output: id1, id3, valid id6, and [params](APPENDIX_beginner_glossary.md#g083) → [full](APPENDIX_beginner_glossary.md#g018) X₀(32) [E4](APPENDIX_beginner_glossary.md#g055) and pool X₁(32) E4, sent to the B70 [bypass](APPENDIX_beginner_glossary.md#g016) and the [TIN](APPENDIX_beginner_glossary.md#g011) encoder respectively.
- Computation order: Coordinates / frame word generate three-channel noise → color [mirroring](APPENDIX_beginner_glossary.md#g030) and [5-tap](APPENDIX_beginner_glossary.md#g029) history [reprojection](APPENDIX_beginner_glossary.md#g025) → 16 channels → [F16](APPENDIX_beginner_glossary.md#g054) adaptation → window block → full and 2×2 pool.
- Key exceptions: When [p5](APPENDIX_beginner_glossary.md#g032) is true, the [structure](APPENDIX_beginner_glossary.md#g005) channel is set to 1 and the two [masks](APPENDIX_beginner_glossary.md#g006) are taken from the control buffer; when history is valid, 5-tap writes 7..9, otherwise current RGB is repeated; [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): [M2](APPENDIX_beginner_glossary.md#g107) wiring and behavior, MEASURED: named temporal instances in ARCH 0.7; [ARCH 0.7 §3, including current temporal revisions](../../../ARCHITECTURE_V3_ZH.md#3-输入端).
- Next down: [L2.02 Singleton Handoff](L2_02_b0.md#b0): [noise](L2_02_b0.md#noise), [5-tap reprojection](L2_02_b0.md#temporal), [16 channels](L2_02_b0.md#channels), [adapter / window block](L2_02_b0.md#adapter), [full/pool](L2_02_b0.md#publish); follow the skewer into [L1.03](L1_03_tin_encoder.md).
