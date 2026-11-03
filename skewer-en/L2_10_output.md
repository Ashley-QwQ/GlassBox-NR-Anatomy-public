# L2.10 Output

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [Back to Parent L1](L1_10_output.md) · [Page Terminology](INDEX.md#shape-and-workspace-notation)

The [history](APPENDIX_beginner_glossary.md#g024) copy at L156 is uniquely defined by [L2.01.copy (id9→id6)](L2_01_prepare.md#copy); this stage follows that link and does not define a second main-text entry for the same [family](APPENDIX_beginner_glossary.md#g080).

<a id="postprocess"></a>
<!-- coverage: {"launches":[157],"kernels":["cg2r_post_process_kernel"]} -->
### L2.10.postprocess Display Postprocessing and intensity Compositing (1 Launch)

- Coverage: L157 / no B number.
- What it is: Applies color processing to the id9 [state](APPENDIX_beginner_glossary.md#g002) and composites it with the id10 [base](APPENDIX_beginner_glossary.md#g003) into the display output.
- Input → output: id9 and id10, each height H × width W × 4 [F16](APPENDIX_beginner_glossary.md#g054) values, plus the current [host](APPENDIX_beginner_glossary.md#g096) [scalars](APPENDIX_beginner_glossary.md#g076) → same-shape id2; does not overwrite id6.
- How it is computed:
  ~~~text
  1. Read id9 RGB and the current host scalars, and execute clamping / gain / nonlinear transforms in original order
  2. Compute explicit extrema, lightness-like intermediates, and hue and saturation branches
  3. Recompose RGB from the branches and captured logarithm / exponential / reciprocal results, preserving the grayscale branch
  4. Take the difference between the processed RGB and the id10 base, then composite via fused blending by intensity
  5. Clamp to the valid color range, convert RGB to half via RZ, and write alpha as 1
  ~~~
- Numeric rules: The color chain is [F32](APPENDIX_beginner_glossary.md#g056), and single-step additions/multiplications, fusions, [FTZ](APPENDIX_beginner_glossary.md#g068), and [function-table](APPENDIX_beginner_glossary.md#g074) domains are not merged; conversion to half occurs at the end, and math-library approximations do not substitute for captured function values.
- Per-instance variation: The singleton's image dimensions, [pitch](APPENDIX_beginner_glossary.md#g084), two [texture](APPENDIX_beginner_glossary.md#g027) [identities](APPENDIX_beginner_glossary.md#g103), and host scalars are bound per captured configuration; there are no network [weights](APPENDIX_beginner_glossary.md#g079) or learned [residuals](APPENDIX_beginner_glossary.md#g017), and base blending must not be conflated with neural-block residuals.
- Why it is computed this way: Separates display color adjustment from the storage of next-frame history state.
- Source adjudication: The guarded branch in current [M2](APPENDIX_beginner_glossary.md#g107) is explained as [HSL-like decomposition and recomposition](L3_b70_history_output.md#postprocess), and the legacy [Oklab](APPENDIX_beginner_glossary.md#g034) naming does not replace this implementation; the [numeric roles](L3_b70_history_output.md#post-curve) of the three scalars are written out as formulas from the code, while their host API names remain unknown.
- [Parameter branches](APPENDIX_beginner_glossary.md#g032): Five exact control fields select the admitted tuples of the same F32 color chain; [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / INFERRED (M2 explicit behavior; interpretation conflict retained); [s157, rz, and run in outtail.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp).
- Next down: [L3.postprocess (Color and Display Compositing)](L3_b70_history_output.md#postprocess), [intensity Contract](L3_b70_history_output.md#intensity); [L4.mufu (Table Functions)](L4_mufu.md#mufu); [L4.fp32-ftz (F32 / Grayscale Branch)](L4_fp32_ftz.md#fp32-ftz).
