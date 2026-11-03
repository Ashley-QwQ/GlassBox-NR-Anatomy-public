### L1.07 split16 Decoder (launch L101–L132 / B40–B47)

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start stage -->
Reading depth: L1 (stage)<br>[Execution numbering](APPENDIX_beginner_glossary.md#g081): [launch](APPENDIX_beginner_glossary.md#g080) L101–L132<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B40–B47

[Beginner Handoff] 🔢 Receive the [512](APPENDIX_beginner_glossary.md#g007) items per position output by the bridge → process eight consecutive [window](APPENDIX_beginner_glossary.md#g015) blocks and deliver the storage organization needed next → hand off to the four-tier densifying stage.

Fixed icons: 🖼 image; 🔢 internal numbers; 🗃 management storage. This summary states only what is received, what is modified, and whom it is handed off to; exact forms follow below.
<!-- beginner-r04m:end stage -->

One level up: [L0 One Frame](L0_frame.md) · [Back to Index](INDEX.md)

[CPU Reconstruction] Stage wiring is given below; [unified notation](INDEX.md#shape-and-workspace-notation) and [computation conventions](INDEX.md#computation-conventions) are collected in the index.

- Function: Executes eight more [16-head](APPENDIX_beginner_glossary.md#g013) window blocks at the 512-channel scale and converts at the tail into the view required for [TIN](APPENDIX_beginner_glossary.md#g011) [upsampling](APPENDIX_beginner_glossary.md#g021).
- Input → output: X₅(512) [E4](APPENDIX_beginner_glossary.md#g055) of B39.out → internal [roles](APPENDIX_beginner_glossary.md#g084) of the eight blocks → identically shaped E4 of B47.[outview](APPENDIX_beginner_glossary.md#g022), handed to L133.
- Computation order: Eight groups of [ffwd](APPENDIX_beginner_glossary.md#g037) → ffwd_proj → qkv → [proj](APPENDIX_beginner_glossary.md#g038); the final step is replaced by L132 proj_outview_wait.
- Key exceptions: L132 still includes projection and E4 [publication](APPENDIX_beginner_glossary.md#g091), while the subsequent view [rearrangement](APPENDIX_beginner_glossary.md#g019) itself adds no extra [quantization](APPENDIX_beginner_glossary.md#g061); inputs, [weights](APPENDIX_beginner_glossary.md#g079), [residuals](APPENDIX_beginner_glossary.md#g017), and window shifts for each block are [bound](APPENDIX_beginner_glossary.md#g103) independently.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100): per-block wiring and L132 exit, MEASURED: named numeric chains; [ARCH 0.7 §5.1, L132 bridge entry](../../../ARCHITECTURE_V3_ZH.md#51-split-swin-16h512-维).
- Next down: [L2.07 Decoder Navigation for the Four Shared Families](L2_07_split16_decoder.md) and [L132 outview Singleton](L2_07_split16_decoder.md#outview); follow the skewer into [L1.08 TIN Decoder](L1_08_tin_decoder.md).
