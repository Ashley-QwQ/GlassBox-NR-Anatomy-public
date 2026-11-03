### L1.10 Output (launch L156–L157 / no B number)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L156–L157<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: no B number

[Beginner Handoff] 🖼 Receive the current-frame new color [state](APPENDIX_beginner_glossary.md#g002) and the original-image backup → save one path as next-frame [history](APPENDIX_beginner_glossary.md#g024), and apply display adjustment and strength blending on the other path → deliver a display image of the same dimensions as the input.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Separately saves next-frame history and generates the current-frame display image from the B70 state.
- Input → output: L156: id9→id6; L157: id9, id10, and controls → same-size [RGBA16F](APPENDIX_beginner_glossary.md#g028) id2.
- Computation order: Copy history across valid rows → execute the [F32](APPENDIX_beginner_glossary.md#g056) color chain on id9 → blend with id10 by [intensity](APPENDIX_beginner_glossary.md#g004) → [clamp](APPENDIX_beginner_glossary.md#g049) and convert to [F16](APPENDIX_beginner_glossary.md#g054) via [RZ](APPENDIX_beginner_glossary.md#g060).
- Key exceptions: The 156-launch route omits the [base](APPENDIX_beginner_glossary.md#g003) backup and standalone S157, writing id2 at the tail end and then copying id2→id6; [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED ([M2](APPENDIX_beginner_glossary.md#g107) copy, postprocessing, and RZ publication; color-space names do not serve as formula premises); [s157, rz, and run in chain_outtail_optm/outtail.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp).
- Next down: [L156 Shared Copy Slice](L2_01_prepare.md#copy), [L157 Postprocessing / Intensity Compositing Slice](L2_10_output.md#postprocess) (including source interpretation conflict); return across frames to [L1.02 B0](L1_02_input_b0.md), or see [INDEX](INDEX.md) for the full skewer. · [Page Terminology](INDEX.md#shape-and-workspace-notation)
