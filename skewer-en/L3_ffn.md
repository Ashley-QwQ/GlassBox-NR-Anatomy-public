# L3.ffn: Per-Channel Gate Function, Expansion, and Residual Wiring

<!-- beginner-r04m:start intro -->
<a id="beginner-ffn"></a>
[Beginner Simplification] First let each position independently recombine its own number sequence, pass through an item-by-item function, and combine back to the original item count; this sub-stage does not fetch content from elsewhere, and only afterward does [attention](APPENDIX_beginner_glossary.md#g039) perform cross-position exchange. Position A goes 2 items → 4 items → item-by-item function → 2 items, and Position B independently follows its own path; see the [synthetic two-position diagram](L1_00_one_block_primer.md#per-position). One [bypass](APPENDIX_beginner_glossary.md#g016) comes from the block entry and is brought in at the start of contraction; the other comes from the [feed-forward](APPENDIX_beginner_glossary.md#g037) result and is brought in at the start of attention [post-projection](APPENDIX_beginner_glossary.md#g038); read the [complete two-bypass diagram](L1_00_one_block_primer.md#two-residuals) before the detailed per-[family](APPENDIX_beginner_glossary.md#g080) table below.
<!-- beginner-r04m:end intro -->

<a id="contract-class-r04l"></a>
## contract Templates and Zero Sources (F26.03/F26.04, Ranks 33–34)

Let P = input byte length / 4096 and bands=ceil(P/128), requiring P>0 and P%32=0; the [CTA](APPENDIX_beginner_glossary.md#g087) count is 8bands, and all four [warps](APPENDIX_beginner_glossary.md#g087) execute. For CTA c and warp w: `class=0 if w<2 else (2 if 128*(c%bands)+64>=P else 1)`. Selection names: class0→live, class1→dead, and class2→dead_edge when `128bands−P≥64`, otherwise →live; the name dead does not mean it is not executed. [ffn_contract.cpp:224–231](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L224), [geometry and selection:301–324](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L301).

The source-zero predicate is `8*(c%bands)+4*(w//2)+slot//2 >= 2*ceil(P/32)`; the source map must be −1 at those positions, and other negative values are not [admitted](APPENDIX_beginner_glossary.md#g101). At z=0, a genuine edge class2 replaces the exact subtree `dq(part(cg(...),part_index))` with `dq(sat(cat(c16(+0),c16(+0))))`, recursively keeping all other subtrees unchanged. Only this class/stage permits this replacement, and edge template stores must be empty; other template [wiring](APPENDIX_beginner_glossary.md#g089)/stores must equal the corresponding live graphs, and templates cannot be guessed from map signs. [source-zero check:248–263](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L248), [subtree replacement:267–281](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L267), [application:315–324](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L315). This closes the template / zero-value rule; the address map remains independently labeled TABLE. For the [release](APPENDIX_beginner_glossary.md#g091) contract, see [per-family release regions](L3_workspace_map.md#release-contract-r04l).

[Full Skewer Index](INDEX.md) · Parent level: [B0](L2_02_b0.md#adapter), [TIN](L2_03_tin_encoder.md), [split16](L2_04_split16_encoder.md#ffwd), [ViT expand](L2_05_vit.md#expand) / [contract](L2_05_vit.md#contract), [B70](L2_09_b70.md#b70)

## Notation and Objects in This File

[E4](APPENDIX_beginner_glossary.md#g055)/[F16](APPENDIX_beginner_glossary.md#g054), [K32](APPENDIX_beginner_glossary.md#g065), [RN-even](APPENDIX_beginner_glossary.md#g059), and [seed](APPENDIX_beginner_glossary.md#g042) follow the [unified notation](INDEX.md#shape-and-workspace-notation). [Q8](APPENDIX_beginner_glossary.md#g061) is F16→E4 RN-even/[satfinite](APPENDIX_beginner_glossary.md#g062), and D8 is exact E4→F16 [decoding](APPENDIX_beginner_glossary.md#g061); [H+](APPENDIX_beginner_glossary.md#g063), H×, and HF are half addition, multiplication, and fused multiply-add respectively. The software reference for HF retains the boundary of rounding the [binary64](APPENDIX_beginner_glossary.md#g056) fused result followed by RN16; see the [half contract](L4_half_arith.md#rounding). Denote by K(A,W;s) a [matrix](APPENDIX_beginner_glossary.md#g051) chain starting from half seed s that publishes F16 at each K32 in actual order, rather than a real-number multiplication rounded only once across the full K.

M×K×N refers to a left matrix of M×K and a right matrix of K×N. For [TIN](APPENDIX_beginner_glossary.md#g011), M=64 [window](APPENDIX_beginner_glossary.md#g015) positions; for [split16](APPENDIX_beginner_glossary.md#g013), S is the position count of the current X₅ [role](APPENDIX_beginner_glossary.md#g084) (60×36=2160 at 1080), while execution-time [padding](APPENDIX_beginner_glossary.md#g085)/masking follows the maps separately; [ViT](APPENDIX_beginner_glossary.md#g014) uses the physical row count P (640 at 1080). Below, [CENSUS](APPENDIX_beginner_glossary.md#g100) describes CPU source code / concrete graphs, and MEASURED/CONTROLLED refer to named saved records; they constrain the native outputs within their respective scopes and cannot prove that the internal [architecture](APPENDIX_beginner_glossary.md#g078) is unique. Design and training motivations remain unknown.

<a id="ffn"></a>
## What One Complete FFN Sub-Block Does

- What it is: First transforms [channels](APPENDIX_beginner_glossary.md#g007) at each position, then applies the single-input [gate function](APPENDIX_beginner_glossary.md#g045), and finally passes through contraction / output projection to reconnect the [scaled](APPENDIX_beginner_glossary.md#g031) [residual](APPENDIX_beginner_glossary.md#g017) from the same block's entry back to the main path.
- Input → output: Block-entry E4 (B0/B70 additionally retain an unquantized F16 entry) → expanded F16 → post-gate E4 → contraction-path F16 → feed-forward exit E4; whether the unquantized F16 is also read by subsequent sub-layers is handled per family in the table below.
- How it is computed: Determine the positions and channels for this run; take the original block entry as the residual; execute this family's pre-projection/expansion; apply G below elementwise; complete contraction and seed merging according to the variant table; publish F16/E4 at the original nodes. The gate function neither mixes two independent hidden [vectors](APPENDIX_beginner_glossary.md#g076) nor performs spatial attention.
- Numeric rules: F16 publication at each K32, the two HF operations and one H× inside the gate, intermediate E4 publications, residual H×, and [partial-sum](APPENDIX_beginner_glossary.md#g050) H+ are all independent boundaries and cannot be collapsed into an ordinary GEMM + activation + single final addition.
- Why: Expansion provides more per-position intermediate channels, and the output path brings them back to the block width; the same-block entry is the exact bypass source. Why these widths, gate shape, or kernel-splitting schemes were adopted is unknown; no training explanation is supplied on this basis.
- How we know: The line-level source code, concrete DAGs, and [five categories of numeric records](#evidence) below are listed separately; a native output gate for a complete FFN does not equal directly observing every internal activation.
- Next down: [Arithmetic of G](#gate), [Channel and Variant Table](#channels), [Small Worked Example from Real C++](#worked-example), [QMMA](L3_qmma_e4m3.md#qmma-e4m3), and [E4 Publication](L4_e4m3_and_k32.md#e4m3-format).

<a id="gate"></a>
## G Is a Single-Input Clamped Piecewise Polynomial

For an input half x, the exact node-by-node interface is:

```math
\begin{aligned}
c&=\mathrm{clamp}_{16}(x,-4,4),\\
\ell&=HF(|c|,-0.055908203125,\ 0.447265625),\\
f&=HF(c,\ell,\ 0.89453125),\\
t&=H\times(x,f),\\
G(x)&=Q8(t).
\end{aligned}
```

Here the three decimal numbers are fixed **algorithmic constants** in the function code and do not read or disclose model coefficients. [clamp](APPENDIX_beginner_glossary.md#g049) is used only for the factor f, while the final multiplication uses the original x; permanently clamping x to ±4 as well would change the result. Absolute value clears the sign bit without adding floating-point rounding. Both HF operations apply RN16 after the fused result; H× applies RN16 again; finally there is a separate RN-even/satfinite conversion to E4. This gate does not call [MUFU](APPENDIX_beginner_glossary.md#g073), [exp](APPENDIX_beginner_glossary.md#g047), tanh, erf, [RSQ](APPENDIX_beginner_glossary.md#g072), or RCP.

**It is neither textbook [GELU](APPENDIX_beginner_glossary.md#g046)/SiLU nor a paired-channel gate.** Ignoring publication rounding, its real-number expression is
```math
g_*(x)=x\left[0.89453125+c\left(0.447265625-0.055908203125|c|\right)\right].
```
Within the clamped interval it is a piecewise cubic; for x≤−4 the factor is 0, and for x≥4 the factor is 1.7890625. An actual finite half x=4 yields t=7.15625 and E4 output 7; both GELU(4) and SiLU(4) are less than 4 and do not equal 7 even if published in this page's format, so G cannot be treated as a same-domain equivalent implementation of either. Each output depends only on its own x, and the factor is constructed from that same x; there is no SwiGLU-style "two independent projections → elementwise product" and no channel halving caused by G. Training names regarding "which activation it approximates" remain [Speculation]; this text uses only G.

| Family G site | Current code/graph and precision differences |
|---|---|
| B0 | [b00.hpp:24](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L24): half clamp/abs → two h_fma → h_mul → sat_e4 |
| TIN | [tin.cpp:105–112](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L105): reference formula computes the two stages in binary64 followed by half_round each; production may use an exact unary table generated from this function, which is not a conclusion that native hardware uses a lookup table |
| ViT expand | [ffn_expand-resume2.cpp:149–154](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L149): two std::fma → half_round; entry explicitly rejects [Inf](APPENDIX_beginner_glossary.md#g069)/NaN |
| split16 ffwd | [L25 graph](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json) / [L29 graph](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json): each G is min/max, abs, fma, fma, mul, Q; [executor:254–274](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L254) executes half arithmetic node by node |
| B70 | [outtail.cpp:88](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L88): same clamp / two half FMAs / half multiplication, with qc publishing E4 |

[This Round: CPU Computation] Extracting the original C++ functions, all three implementations for B0/TIN/ViT produce identical E4 outputs across **all 63488 finite F16 encodings**, including ±0; this is an exhaustive equivalence of these software functions on that domain, not a new GPU measurement, and does not cover arbitrary nonfinite inputs. The concrete G graph of split16 has the same structure as the formula above; this software check is not upgraded to full-graph / full-geometry admission. Rejections for nonfinite seeds, E4 NaN, and half [overflow](APPENDIX_beginner_glossary.md#g071) in QMMA along the chain are still enforced according to the [primitive guards](L4_e4m3_and_k32.md#publish-guards); the satfinite of G cannot be used to bypass a rejection from the preceding matrix.

<a id="wiring"></a>
## One Complete Residual Wiring Diagram

The "contraction path" in the diagram contains one or more matrix layers according to the table below; the entry point of seed is the actual accumulation interface, not a real-number addition appended at the very end.

~~~mermaid
flowchart LR
    X["Current-block entry: E4; B0/B70 additionally retain half"] --> PRE["Pre-projection: present in split16; others per variant"]
    PRE --> EX["Expansion K32 chain → F16"]
    EX --> G["Single-input G: two HF, one H× → E4"]
    G --> DOWN["Contraction matrix / first slice: receives seed; each K32, intermediate E4, and partial-sum H+ per variant"]
    X --> R["Original block entry decoded or retained in half × residual scale → half seed"]
    R --> DOWN
    DOWN --> Z["Feed-forward result F16 merged per variant"]
    Z --> Q["Q8 → feed-forward exit E4"]
    Z -. "Unquantized value retained only on named 1-head paths" .-> L["Independent bypass for subsequent sub-layers"]
~~~

<a id="channels"></a>
## Cross-Family Channel and Variant Table

All matrix [weights](APPENDIX_beginner_glossary.md#g079) are E4; bypass scales are consumed as F16, and their values are not listed here. The logical grouping of split16 is inferred from the data dependencies, K32 chains, and weight-index coverage of the named graphs (CENSUS / INFERRED), without equating this group axis to the 16 attention heads; [detailed bindings and counts](APPENDIX_evidence_history.md#ffn-r04b) are in the appendix.

| Family / launches | M×K×N and expansion width | Whether G splits channels / staging | Residual source, precision, and injection point | Actual differences and locations |
|---|---|---|---|---|
| B0 / L2 | Per window 64×32×128, then 64×128×32; expansion 128 | Not split; post-gate 128 E4 | Unquantized F16 of adapter output a, with H×(a,s_ff) as the first-K32 contraction seed; still F16 after 4 K32 steps, then published as E4 | Expansion input is xc=Q8(a), so the residual cannot be recovered from xc; [b00.hpp:42–44](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L42) |
| TIN 1-head [chained](APPENDIX_beginner_glossary.md#g022) / C=32 | 64×32×128→64×128×32 | Not split; 128 E4 | H×(D8(current-block entry),s_ff) as contraction seed; 4 contraction steps | 1-head upsample entry is an exception that takes the unquantized merged value sx; does not expand the full [upsampling](APPENDIX_beginner_glossary.md#g021) topic; [tin.cpp:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130) |
| TIN multi-head chained / C=64/128/256 | H=C/32; per group 64×C×128, post-gate per group 64×128×32, then 64×32×C; total gate width 4C | Not split; 128 E4 per group, then contracted to 32 and Q8 | Initializes z=H×(D8(entry),s_ff), accumulating the half result of each 32→C matrix into z in original h order; each group's final projection is a single K32 | Intermediate 32 channels must be E4; not a single ordinary 4C→C. Packed C×(4C+128) includes the grouped branch parameter region, and the extra 128 is not a second gate vector; [tin.cpp:38, 63–68, 133–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L63) |
| split16 ffwd / L25 and L29,33,…,53; L101,105,…,129 | Pre-projection S×512×512→Q8; eight groups of S×64×256→G→S×256×64→Q8; concatenated back to S×512; total gate width 2048 | Not split; total gate 2048 E4 is an intra-kernel quantity, while the actual ffwd exit remains 512 E4/position | ffwd does not merge the entry residual; original block entry is handed independently to the next kernel | First-block inpview and chained have different fetch layouts; the three stages inside the graph do not treat physical N_out directly as the expansion width; [L25/L29 graphs and bindings](APPENDIX_evidence_history.md#ffn-r04b) |
| split16 ffwd_proj / L26 and L30,34,…,54; L102,106,…,130 | S×512×512; receives the 512 E4 from ffwd above | This kernel does not execute G again | H×(D8(original block entry),s_ff) as F16 seed of the first K32; 16 steps follow, with Q8 at the end | Bypass is the same-block entry, not the ffwd exit itself; [L26 graph](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json) / [L30 graph](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json) |
| ViT expand / L59,64,69,74,79,84,89,94 | P×1024×4096, 32 K32 steps per output; total gate width 4096 | Not split; 4096 E4/row after elementwise G | This kernel does not add the block-entry residual | Publish/wait differs between publish and chained without changing G or width; [expand:267–303](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L267) |
| ViT contract / L60,65,70,75,80,85,90,95 | Logical P×4096×1024, but actually four K=1024 slices of 32 K32 steps each, followed by fixed half merging | No G; 2048 B/position = 1024 F16 partial sums, not 2048 hidden channels or half of the gate | H×(D8(block entry),s_ff) serves as the seed of slice 0; slices 1/2/3 start from [+0](APPENDIX_beginner_glossary.md#g070); H+ according to the formula below, with Q8 at the end | buffer/output/release are each independent roles; [contract:302–312, 436–488](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L302) |
| B70 1-head FFN / L155 | Active window positions ×32×128→×128×32 | Not split; 128 E4 | Unquantized half merge from two-way [feature](APPENDIX_beginner_glossary.md#g008) merging, with H×(merge,s_ff) as contraction seed | Expansion reads Q8(merge), while bypass retains merge; covers only FFN without expanding the terminal head / [temporal](APPENDIX_beginner_glossary.md#g024) stage; [outtail.cpp:85–88](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L88) |

<a id="residual"></a>
### Why "Add the Residual After Contraction Finishes" Is Not Accurate Enough

In B0 / 1-head TIN / split16 post-projection / B70, the residual is first multiplied via H× to half and then used as the seed of the **first matrix step**; each subsequent K32 carries the previous step's F16, and the residual must not be moved to a single addition after the entire dot product. In multi-head TIN, each group's 32→C projection also carries the previous group's half result, so the group order cannot be permuted arbitrarily.

The actual software interface of ViT contract can be written as:
```math
\begin{aligned}
r&=H\times(D8(X),s_{\rm ff}),\\
p_0&=K(H_0,W_0;r),\qquad
p_i=K(H_i,W_i;+0)\quad(i=1,2,3),\\
b_0&=p_0,\quad b_1=H+(b_0,p_1),\quad b_2=H+(b_1,p_2),\\
Y&=Q8\!\left(H+(b_2,p_3)\right).
\end{aligned}
```
H_i/W_i denote the 1024 items assigned to that slice by the [frozen](APPENDIX_beginner_glossary.md#g103) graph, without assuming that memory is laid out as four contiguous segments. Slice 0 writes the half buffer, slices 1/2 accumulate into the buffer in half in order, and slice 3 adds to the buffer and outputs E4; the [concrete templates](F:/dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json) and the [executor](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L477) jointly determine this order. Sensitivity to reordering does not mean a unique native concurrent arrival order has been proven.

This page ends at the FFN exit. In 1-head TIN the subsequent bypass retains unquantized z, whereas multi-head TIN uses D8(Q8(z)); for complete wiring, see [TIN Block](L3_tin_window.md#tin-window) and [split16 Fused Block](L3_split16_window.md#window-attention), which each retain their attention, projection, and residual interfaces.

<a id="worked-example"></a>
## Small Example from Real C++ Functions: Bytes In, Bytes Out

The [script](../skewer/examples/ffn_r04b.py) extracts the B0 gate, TIN gate_reference, ViT gate, and half/E4 functions verbatim from the current source code, compiles them, and executes them directly; K32 calls the original qmma_sm120.hpp. It does not import the network, read weights or saved network inputs/targets, or use a GPU. [Raw outputs and source identities](../skewer/examples/ffn_r04b.result.json) and [compilation records](APPENDIX_evidence_history.md#ffn-r04b) can be inspected.

Send a synthetic half expansion result x to G, take a synthetic bypass E4=0x28 (0.25) and half scale 0x4000 (2), and apply the real H× to obtain seed=0x3800 (0.5). Then use a **synthetic K32 contraction** whose first item is 1 and remaining items are 0 to merge G(x) with the seed, followed by Q8 at the end. This is a small primitive path and does not impersonate a real 128- or 4096-channel FFN or any model coefficients. F16 encodings are shown as four-digit hexadecimal; [little-endian](APPENDIX_beginner_glossary.md#g097) input bytes are ordered low byte then high byte, for example 0xbc00 is 00 bc.

| F16 encoding of x (value) | G(x) E4 byte | seed F16 | Contraction result F16 | Final E4 byte |
|---|---|---|---|---|
| c400 (−4) | 80 (−0) | 3800 | 3800 | 30 |
| bc00 (−1) | b0 (−0.5) | 3800 | 0000 | 00 |
| 8000 (−0) | 80 | 3800 | 3800 | 30 |
| 0000 (+0) | 00 | 3800 | 3800 | 30 |
| 3800 (0.5) | 31 (0.5625) | 3800 | 3c40 | 38 |
| 3c00 (1) | 3a (1.25) | 3800 | 3f00 | 3e |
| 4000 (2) | 45 (3.25) | 3800 | 4380 | 47 |
| 4400 (4) | 4e (7) | 3800 | 4780 | 4f |
| 4500 (5) | 51 (9) | 3800 | 48c0 | 52 |

The output for x=5 differs from that for x=4, directly verifying that "only the factor is clamped, not the final x." The same program also calls the real H+ on synthetic half slices [2048,1,−2048,1]: the original order yields 0x3c00 (1), whereas swapping the middle slices yields 0x4000 (2); this illustrates the order sensitivity of step-by-step half rounding and is not a new native [negative control](APPENDIX_beginner_glossary.md#g102). The ViT gate actually rejects synthetic +Inf/−Inf/NaN. The full program also covers x=−5 and compares the outputs of the three G implementations across all finite half inputs.

<a id="evidence"></a>
## How We Know: Per-Launch Records and Boundaries

| This assertion | Direct source reading / observation | Compared object and scope | What it cannot prove |
|---|---|---|---|
| Expansion, gate, and contraction nodes | Line-level source code and bound graphs of each family above | Current CPU functions / concrete graphs; native output gates listed separately in the [appendix](APPENDIX_evidence_history.md#ffn-gate-history) | Does not treat internal CPU values as native activation observations |
| ViT two-stage feed-forward | Saved per-launch native/Python/C++ comparisons | Named inputs, with output/padding/release roles each following the original reports | Legacy [NOT_RUN](APPENDIX_beginner_glossary.md#g104) and MAP_CHECK_FAILED entries are not overwritten by later gates |
| TIN, split16, and B0/B70 feed-forward | Saved full-launch or named intra-block chain comparisons | Complete exits include FFN; not a separate hardware measurement of each individual G | Does not prove uniqueness across all geometries, all inputs, or all internal matrix decompositions |

[Native behavior](APPENDIX_beginner_glossary.md#g001), CPU matrix decompositions, and finite-domain equivalence of software G each retain their respective evidence strength; complete maps semantics, arbitrary geometries/inputs, nonfinite combinations, and uniqueness of internal values remain not established. Complete graph identities, K32-chain / weight-index counts, and evaluated source SHAs are placed only in the [FFN evidence appendix](APPENDIX_evidence_history.md#ffn-r04b); legacy experiments are neither re-run nor modified.
