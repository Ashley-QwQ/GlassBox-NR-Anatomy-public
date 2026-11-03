# L2.05 ViT: Shared Computation, Six Families, and Intra-Block Wiring

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [Parent L1](L1_05_vit.md) · [Unified Notation](INDEX.md#shape-and-workspace-notation)

[Weight Organization, dtypes, and Stage Byte Accounting](L2_weights_layout.md)

[CPU Reconstruction / CENSUS] L58 converts the 2D [role](APPENDIX_beginner_glossary.md#g084) into a sequence, each of the eight blocks executes expand→contract→qkv→[attention](APPENDIX_beginner_glossary.md#g039)→projection, and L99 converts it back to 2D. Denote each block's entry by X and the contract exit by Z; the two [residuals](APPENDIX_beginner_glossary.md#g017) come from X and Z respectively. Primary roles are [E4](APPENDIX_beginner_glossary.md#g055), [matrices](APPENDIX_beginner_glossary.md#g051) [publish](APPENDIX_beginner_glossary.md#g091) [F16](APPENDIX_beginner_glossary.md#g054) at each [K32](APPENDIX_beginner_glossary.md#g065), and [scales](APPENDIX_beginner_glossary.md#g031), [reductions](APPENDIX_beginner_glossary.md#g050), the partial half buffer, and release each have their own independent format and order. [Padded](APPENDIX_beginner_glossary.md#g085) rows, valid rows, and extra zero-writes are registered separately.

[Native Behavior / Verification Record] The widths and operation order below are supported by the current source code, [bound](APPENDIX_beginner_glossary.md#g103) graphs, and named output gates; they do not prove a [unique internal structure](APPENDIX_beginner_glossary.md#g111) in the native binary. Training motivations, why [FFN](APPENDIX_beginner_glossary.md#g037) precedes attention, and the reasons for kernel splitting are unknown.

## Shared Contract and Six Variants

Each [launch](APPENDIX_beginner_glossary.md#g080) first binds inputs/outputs, [weights](APPENDIX_beginner_glossary.md#g079), geometry, and completion flags from [params](APPENDIX_beginner_glossary.md#g083), then executes the numeric graph of its family, and finally publishes the corresponding roles. The same family reuses the computation structure; numeric values, residuals, and addresses are still bound per block. Global attention uses the logical T keys; execution is organized by physical P rows and the prescribed padding rounds, without adding valid keys from the allocated length.

| Family / coverage entry | Input → output | Computation and [quantization](APPENDIX_beginner_glossary.md#g061) in this family | Residuals, layout, and actual differences |
|---|---|---|---|
| <a id="repack"></a>[repack](APPENDIX_beginner_glossary.md#g019); L58, L99 | X₆(1024) ↔ P×1024 B | [Closed-form](APPENDIX_beginner_glossary.md#g020) permutation of 4-byte blocks, with no arithmetic rounding | L58 explicitly writes padding zeros; L99 writes only the logical T rows; reads no weights or residuals. [Mapping](L3_workspace_map.md#repack) |
| <a id="expand"></a>expand; L59,64,69,74,79,84,89,94 / B31–B38 | X: P×1024→P×4096 B | 1024→4096 matrix, 32 steps of K32 per output; elementwise G followed by E4 | No residual in this kernel. First-block publish differs from the wait/publish of the remaining [chained](APPENDIX_beginner_glossary.md#g022) launches, while G and width are identical. [FFN](L3_ffn.md#channels) |
| <a id="contract"></a>contract; L60,65,70,75,80,85,90,95 | P×4096 B→Z: P×1024 B | Four K=1024 slices of 32 K32 steps each; forms half partial sums in order first, then E4 | Only slice 0 receives the [H×](APPENDIX_beginner_glossary.md#g063)(D8(X),s_ff) [seed](APPENDIX_beginner_glossary.md#g042); slices 1/2/3 start from [+0](APPENDIX_beginner_glossary.md#g070). The buffer is 1024 F16 = 2048 B per row, not 2048 hidden [channels](APPENDIX_beginner_glossary.md#g007). [First slice and merge](L3_ffn.md#residual) |
| <a id="qkv"></a>qkv; L61,66,71,76,81,86,91,96 | Z→Q, K, V of P×1024 B each | Three-way [projection](APPENDIX_beginner_glossary.md#g038); 32 heads, 32 channels per head; intra-head sum of squares, [RSQ](APPENDIX_beginner_glossary.md#g072), and scale followed by E4 for Q/K, while V skips this [normalization](APPENDIX_beginner_glossary.md#g043) | Receives Z, with no projection residual; [F32](APPENDIX_beginner_glossary.md#g056) table return values convert back to half at explicit nodes. [norm](L3_norm_nonfinite.md#norm32) |
| <a id="attention"></a>attention; L62,67,72,77,82,87,92,97 | Q/K/V→P×1024 B | Global scores → φ → half reduction and RCP; aggregates V with E4(w) first, then multiplies by r in half and converts to E4 | No external matrix weights or residuals; padded zero keys require tail-round subtraction. 4K L62 additionally zero-overwrites 16×1024 B after computation before publishing; not replicated across all launches. [attention](L3_attention_softmax.md#attention-softmax) |
| <a id="projection"></a>projection; L63,68,73,78,83,88,93,98 | attention exit + Z → next-block P×1024 B | Output matrix and half partial sums merged according to the frozen graph, then finally E4 | [Bypass](APPENDIX_beginner_glossary.md#g016) is the current block's contract exit Z; ordered half merging cannot be replaced by real-number addition at the end. L98 is the wait variant. For the slices, seeds and merge order see [QKV and projection partial sums](L3_workspace_map.md#partial-sums-r04l); [Matrices and publication](L3_qmma_e4m3.md#qmma-e4m3), [half accumulation](L4_half_arith.md#atomic-add) |

## B31: One Complete Block at 1080 (T=P=640)

~~~mermaid
flowchart TD
    X["X: 640×1024 E4"] --> EX["L59 expand: 1024→4096; G→E4"]
    EX --> CT["L60 contract: 4 K1024 slices; slice 0 receives seed; 32 K32 steps each"]
    X --> SeedFFN["D8(X) × s_ff → half seed"]
    SeedFFN --> CT
    CT --> BUF["Slices 0/1/2 write half buffer in order: 640×1024 F16 = 640×2048 B"]
    BUF --> Z["Slice 3 performs H+ with buffer; Z: 640×1024 E4"]
    Z --> QKV["L61: Q/K/V 640×1024 E4 each; 32 heads × 32 channels; normalize Q/K only"]
    QKV --> AT["L62: 640×640 scores per head, executed in tiles; φ→Den→r"]
    AT --> AV["Q8(w)×V: 20 K32 steps; multiply by r in half → 640×1024 E4"]
    AV --> PR["L63 projection: matrix merged with prescribed half partial sums"]
    Z --> ResidualAttn["Projection residual interface of current-block Z"]
    ResidualAttn --> PR
    PR --> Y["B31 exit: 640×1024 E4 → B32"]
~~~

1080 has no padded keys; the 20 K32 steps in the diagram are organized as 10 rounds of 64 keys. For the 4K padding subtraction and L62 extra zero-overwrite, see [tail-round correction](L3_attention_softmax.md#attention-softmax); they are not an extra branch of the 640 rows in this diagram. The partial sums in the diagram are the software numeric interface and do not claim direct observation of native internal buffer values.

## Sources, Observations, and Boundaries

| This assertion | Direct source reading / observation | Compared object and scope | What it cannot prove |
|---|---|---|---|
| expand / contract widths, four-slice seed | [expand:267–303](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L267), [contract:436–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L436) | CPU functions and named frozen graphs; for numeric gates, see [FFN evidence](APPENDIX_evidence_history.md#ffn-r04b) | Arbitrary geometries or uniqueness of internal [activations](APPENDIX_beginner_glossary.md#g045) |
| [QKV](APPENDIX_beginner_glossary.md#g040), projection, and half publication | [executor:170–239](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L170) | Current CPU implementation; [attention evidence](APPENDIX_evidence_history.md#attention-evidence) lists legacy gates separately | Saved results cannot automatically close legacy map admission |
| Post-attention multiplication by r and zero-overwrite | [attention:206–238](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L206), [adapter:166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166) | Primitive graphs, named published roles, and [negative controls](APPENDIX_beginner_glossary.md#g102) | General synchronization / [aliasing](APPENDIX_beginner_glossary.md#g092) / lifetime remain not established |

Next down: [FFN](L3_ffn.md#ffn), [attention and AV](L3_attention_softmax.md#attention-softmax), [norm](L3_norm_nonfinite.md#norm32), [workspace write sets](L3_workspace_map.md#write-sets), [QMMA arithmetic](L4_e4m3_and_k32.md#qmma-k32-accumulation). Each launch set retains single-source coverage attribution:

<!-- coverage: {"launches":[58,99],"kernels":["cc_vit_1d_repack_2d_to_1d_fp8","cc_vit_1d_repack_1d_to_2d_fp8"]} -->
<!-- coverage: {"launches":[59,64,69,74,79,84,89,94],"kernels":["cc_vit_1d_ffn_expand_publish_fp8","cc_vit_1d_ffn_expand_chained_fp8"]} -->
<!-- coverage: {"launches":[60,65,70,75,80,85,90,95],"kernels":["cc_vit_1d_ffn_contract_chained_fp8"]} -->
<!-- coverage: {"launches":[61,66,71,76,81,86,91,96],"kernels":["cc_vit_1d_qkv_chained_fp8"]} -->
<!-- coverage: {"launches":[62,67,72,77,82,87,92,97],"kernels":["cc_vit_1d_attention_chained_fp8"]} -->
<!-- coverage: {"launches":[63,68,73,78,83,88,93,98],"kernels":["cc_vit_1d_projection_chained_fp8","cc_vit_1d_projection_wait_fp8"]} -->
