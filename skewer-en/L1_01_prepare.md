### L1.01 Pre-Graph Preparation (launch L0–L1 / no B number)

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L0–L1<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: no B number

[Beginner Handoff] 🖼 Receive the current-frame image → keep an original-image backup; 🗃 set only the specified management region → hand off to input computation, and keep the backup for display.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Pre-Graph Preparation retains the display compositing [base](APPENDIX_beginner_glossary.md#g003) and initializes the control region for subsequent blocks.
- Input → output: W×H×4 [F16](APPENDIX_beginner_glossary.md#g054) of id1 → identically shaped id10; L1 separately fills the declared 4n B control region with 0xFF.
- Computation order: Copy across valid [texels](APPENDIX_beginner_glossary.md#g027) → read clear length → fill control region → hand off to subsequent launches.
- Key exceptions: [Nonfinite](APPENDIX_beginner_glossary.md#g069) conversions during copy remain subject to guards; the initialized range is not the entire [workspace](APPENDIX_beginner_glossary.md#g082), nor does it zero-fill.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): id10 wiring, fill value, and range in [M2](APPENDIX_beginner_glossary.md#g107) source code; [run_launch in chain_entry_optm/entry.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp); ARCH §1.1 labels the id10 wiring as inference, and the distinction from source-code verification is retained here.
- Next down: [L2.01.copy Color/History Copy](L2_01_prepare.md#copy), [L2.01.clear Control-Region Initialization](L2_01_prepare.md#clear); follow the skewer into [L1.02 B0](L1_02_input_b0.md).
