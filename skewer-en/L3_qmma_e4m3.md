# L3.qmma-e4m3: Which K32 Steps Make Up a Matrix Multiplication

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start intro -->
<a id="beginner-qmma"></a>
[Beginner Simplification] When multiplying a row and a column pair by pair and adding them up, this rule processes 32 pairs at a time, brings in a subtotal, first places each item toward zero onto the same scale, and then adds them up and saves an [F16](APPENDIX_beginner_glossary.md#g054) subtotal; the next basket continues with this saved result. Some exits must then also convert to the coarser [E4](APPENDIX_beginner_glossary.md#g055). Read [Finite Number Points and Small Baskets](L1_00_numbers_primer.md) first, and then drill down into the integer formulas, candidates, and evidence scope below; the basket is a teaching metaphor, not a proof of internal device structure.
<!-- beginner-r04m:end intro -->

[Full Skewer](INDEX.md) · Parent level: [TIN chained](L2_03_tin_encoder.md#chain-32), [ViT projection](L2_05_vit.md#projection), [Decoder Bridge](L2_06_decoder_bridge.md#bridge)

[Cross-Architecture Primitives and CPU Backend Comparison](L4_cross_arch.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| A[M,K], B[K,N] | [Logical](APPENDIX_beginner_glossary.md#g085) [matrices](APPENDIX_beginner_glossary.md#g051); physical arrangement is [bound](APPENDIX_beginner_glossary.md#g103) by the [caller](APPENDIX_beginner_glossary.md#g080) |
| C^(j), J | half [seed](APPENDIX_beginner_glossary.md#g042) before step j, and [K32](APPENDIX_beginner_glossary.md#g065) step count J=K/32 |
| Q32 | One step of [sm_120](APPENDIX_beginner_glossary.md#g078) E4 K32 and half [publication](APPENDIX_beginner_glossary.md#g091) |
| field / [value](APPENDIX_beginner_glossary.md#g067) / renorm | Candidate distinction where the [alignment exponent](APPENDIX_beginner_glossary.md#g066) is taken from fields / actual products / [normalized](APPENDIX_beginner_glossary.md#g067) operands |

<a id="qmma-e4m3"></a>
### L3.qmma-e4m3 Ordered K32 Chain for One Output Element

- What it is: Splits a matrix [reduction](APPENDIX_beginner_glossary.md#g050) into ordered 32-item steps, where each step receives and republishes an F16 [accumulator](APPENDIX_beginner_glossary.md#g064).
- Input → output: E4 [encodings](APPENDIX_beginner_glossary.md#g057) of logical $A[M,K]$ and $B[K,N]$ together with $C^{(0)}[M,N]$ → F16 matrix; only some launches subsequently publish E4 via $Q8$. Neither the entire [weight container](APPENDIX_beginner_glossary.md#g079) nor the entire [workspace](APPENDIX_beginner_glossary.md#g082) can be uniformly interpreted as E4.
- How it is computed:
  ~~~text
  1. Fetch one row of A, one column of B, and the seed for this output position according to the current layout/indexing.
  2. Initialize C^(0); when there is no explicit seed, use +0 according to the contract of that launch.
  3. For j from 0 to J−1: take the encodings of A and B at items 32j through 32j+31.
  4. C^(j+1) = Q32(these 32 encoding pairs, C^(j)); retain the original rejection conditions.
  5. Save the final F16; execute Q8 only when the caller requires an E4 exit.
  ~~~
- Numeric rules: Within each $Q_{32}$, products and the seed are first placed onto the common grid points via [RZ](APPENDIX_beginner_glossary.md#g060), then summed as exact integers, and finally rounded once at the end via [RN-even](APPENDIX_beginner_glossary.md#g059) to F16; across steps there are multiple F16 roundings. The source code places the seed first and then adds the products from 0→31; only the sum of these already-placed integers allows [rearrangement](APPENDIX_beginner_glossary.md#g019). Performing $Q8$ afterward adds one more format rounding.
- Why it is computed this way: The publication interface of tiled matrix kernels allows every 32 items to carry a same-format accumulator; the interface cannot prove hardware design motivations or a unique internal addition tree.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) / MEASURED (scoped to the candidate set and measured cases); [port RESULT:9, 15–19](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门).
- Next down: [L4.e4m3-format](L4_e4m3_and_k32.md#e4m3-format), [L4.qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation), [worked examples](L4_e4m3_and_k32.md#worked-examples).

In the formula below, r=0..M−1 is the row index of A/C, and n=0..N−1 is the column index of B/C.

```math
C^{(j+1)}_{rn}
=Q_{32}\!\left(A_{r,32j:32j+32},B_{32j:32j+32,n},C^{(j)}_{rn}\right),
\qquad j=0,\ldots,J-1.
```

### Line-Level Basis: Matrices, Storage, and Publication Interfaces

| This assertion | Direct source reading / observation | Compared object and scope | What it cannot prove |
|---|---|---|---|
| Each K32 brings in and publishes an F16 seed | [tin.cpp:88–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88) | CPU matrix interface; E4 encodings kept separate from half results | Source-code loops do not prove the physical GPU addition tree |
| Current sm_120 numeric rule | [qmma_sm120.hpp:49–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L49) and [adjudication records](APPENDIX_evidence_history.md#qmma-history) | Frozen candidates and named raw hardware bytes; bulk software comparisons listed separately | Random software comparisons are not new hardware cases |
| Formats differ from auxiliary [scales](APPENDIX_beginner_glossary.md#g031) | [tin.cpp:26–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26) | Current resource read types and respective publication points | Does not disclose coefficients; does not treat the entire container as E4 |

[Original line-level locations and experiment correspondences](APPENDIX_evidence_history.md#qmma-source-ledger) are placed in the appendix; default production guards and the current [acceptance domain](APPENDIX_beginner_glossary.md#g101) remain in effect.

The [TIN](APPENDIX_beginner_glossary.md#g011) caller is only a readable representative. Data-driven families still use their own index tables, matrix chains, and seed sources; sharing $Q_{32}$ does not mean their layouts and [residuals](APPENDIX_beginner_glossary.md#g017) are identical. Nor do retained legacy non-sm_120 branches thereby become accepted implementations for other architectures.

<a id="候选如何从-1832-收敛到一个行为类"></a>
## Applicability Boundaries of the Current Rule

[Verification Record] The current rule reaches only UNIQUE_BEHAVIOUR_CLASS_WITHIN_FROZEN_FINITE_DOMAIN_BANK: it is a unique behavior class within the frozen finite candidate bank, and does not prove candidate exhaustiveness, hardware equivalence across all finite inputs, a complete contract for [NaN](APPENDIX_beginner_glossary.md#g069)/Inf/signed zero/overflow, or network reachability. Production rejections for nonfinite values and [overflow](APPENDIX_beginner_glossary.md#g071) still follow the [publication guards](L4_e4m3_and_k32.md#publish-guards), and general conclusions remain not established.

Other architectures cannot carry over sm_120: sm_75 is field F24 / full K8, sm_86 is renorm F24 / two K8 groups, and sm_89 is field F13 / two K16 groups, each publishing F16 at the end of a group; alignment exponents, how the seed participates, and truncation also differ, and cannot be treated merely as bit-width changes.

[Candidate tables, cross-architecture receipts, source SHAs, and legacy statuses](APPENDIX_evidence_history.md#qmma-history) have been moved to the appendix. Legacy "pending C++ integration" and legacy unrun 4K entries are still retained as of their respective dates; the current source code contains the field F25 branch, does not treat legacy random software controlled comparisons as new hardware adjudications, and does not derive a general QMMA theorem from later [full-chain gates](APPENDIX_beginner_glossary.md#g102).
