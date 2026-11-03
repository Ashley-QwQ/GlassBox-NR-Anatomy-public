# L2.01 Pre-Graph Preparation

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[CPU Reconstruction] The copy and fill functions are specified below; the design reasons for sharing a kernel and splitting launches this way are unknown.

[Full Skewer Index](INDEX.md) · [Back to Parent L1](L1_01_prepare.md) · [Page Terminology](INDEX.md#shape-and-workspace-notation)

<a id="copy"></a>
<!-- coverage: {"launches":[0,156],"kernels":["cg2r_copy_kernel"]} -->
### L2.01.copy Color / History Copy (2 Launches)

- Coverage: [L0](APPENDIX_beginner_glossary.md#g081), L156 / no B number.
- What it is: The same [family](APPENDIX_beginner_glossary.md#g080) saves the [color base](APPENDIX_beginner_glossary.md#g003) at the start of the frame and passes the [history](APPENDIX_beginner_glossary.md#g024) [state](APPENDIX_beginner_glossary.md#g002) at the end of the frame.
- Input → output: L0: id1→id10; L156: id9→id6; each is height H × width W × 4 [F16](APPENDIX_beginner_glossary.md#g054) values, with no numeric exit in the [workspace](APPENDIX_beginner_glossary.md#g082).
- How it is computed:
  ~~~text
  1. Read the current parameter block and the texture width, height, and row stride
  2. At L0, select current color and base, and verify the captured identity coordinate contract
  3. At L156, select B70 state and history, and verify the source and destination roles
  4. Row by row, copy the valid 8 × image-width bytes to the destination texture
  5. Preserve the source texture and the rest of the workspace contents for display compositing or next-frame reading
  ~~~
- Numeric rules: The identity L0 acceptance domain preserves finite half [bit patterns](APPENDIX_beginner_glossary.md#g057), while [nonfinite](APPENDIX_beginner_glossary.md#g069) conversions are still rejected; L156 copies byte for byte, including zero signs; no additions, multiplications, or [floating-point](APPENDIX_beginner_glossary.md#g056) rounding are introduced.
- Per-instance variation: The source/destination [texture](APPENDIX_beginner_glossary.md#g027) [roles](APPENDIX_beginner_glossary.md#g084) differ between the two launches, and geometry and row stride are [bound](APPENDIX_beginner_glossary.md#g103) per frame configuration; there are no [weights](APPENDIX_beginner_glossary.md#g079) and no [residuals](APPENDIX_beginner_glossary.md#g017), and one cannot assume the two copy entry contracts are identical merely because they share the same function.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) (wiring / source code); [ARCH 0.7 §1.1, §6.4](../../../ARCHITECTURE_V3_ZH.md#11-一帧从输入到输出).
- Next down: [L3.workspace-map (Resources and Write Intervals)](L3_workspace_map.md#regions); [Row-by-Row Copy and Native Seam Evidence](L3_b70_history_output.md#copy) for L156; reused on the output side by [L1.10](L1_10_output.md).

<a id="clear"></a>
<!-- coverage: {"launches":[1],"kernels":["cc_cb_clear"]} -->
### L2.01.clear Control-Region Initialization (1 Launch)

- Coverage: L1 / no B number.
- What it is: Sets the control words at the beginning of the workspace to all 1s.
- Input → output: Contiguous 4n bytes of WS (the current-frame shared workspace) starting at offset 0, where n is the 32-bit word count given by the [parameter block](APPENDIX_beginner_glossary.md#g083); 388,096 B in the 1080 instance, while the rest of the workspace is not cleared by this kernel.
- How it is computed:
  ~~~text
  1. Read the workspace base address
  2. Read the control word count from the current parameter block
  3. Verify that the target contiguous interval lies within the workspace
  4. Fill every byte in the interval with 255
  5. Preserve bytes outside the interval, leaving completion flags to be published by subsequent producers
  ~~~
- Numeric rules: All 1s is the bit pattern of the control words and is not evaluated as a floating-point NaN; no rounding is performed, old workspace values are not read, and the entire workspace is not zeroed.
- Per-instance variation: When geometry changes, the count and workspace identity change according to the parameters; no weights and no numeric residuals.
- How we know: CENSUS ([M2](APPENDIX_beginner_glossary.md#g107) explicit fill behavior); [run_launch in entry.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp).
- Next down: [L3.workspace-map (Control Words and Publication Intervals)](L3_workspace_map.md#clear).
