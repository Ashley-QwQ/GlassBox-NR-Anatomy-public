# L3.tin-window: Complete TIN Window Block and Encoder/Decoder Handoff

<!-- beginner-r04m:start intro -->
<a id="beginner-tin"></a>
[Beginner Simplification] Within a small [window](APPENDIX_beginner_glossary.md#g015), each position first modifies its own [channels](APPENDIX_beginner_glossary.md#g007), then positions are compared and content is combined, while 2 sets of earlier numbers each reconnect at their prescribed starting subtotals. First, a fewer-box version:

~~~mermaid
flowchart LR
    X["Entry numbers"] --> F["Per-position processing + reconnect entry bypass"] --> Z["Feed-forward result"] --> A["Exchange content within window"] --> P["Output projection + reconnect feed-forward result bypass"] --> Y["Block result"]
    X -. "1st bypass" .-> F
    Z -. "2nd bypass" .-> P
~~~

"Reconnecting" happens at the starting subtotal of [matrix](APPENDIX_beginner_glossary.md#g051) accumulation, not by adding only after the entire stage finishes computing. A window is a range of positions, a head is a grouping of comparison numbers, and [FFN](APPENDIX_beginner_glossary.md#g037) groups and device work groupings are different again. After [learning from a 1-head block](L1_00_one_block_primer.md), the text below retains the multi-head, up/[downsampling](APPENDIX_beginner_glossary.md#g021), and format differences.
<!-- beginner-r04m:end intro -->

[Full Skewer Index](INDEX.md) · Parent level: [TIN Encoder](L2_03_tin_encoder.md), [TIN Decoder](L2_08_tin_decoder.md) · Expanded sub-items: [FFN](L3_ffn.md#ffn), [attention](L3_attention_softmax.md#window-attention), [norm](L3_norm_nonfinite.md#norm32), [Workspace](L3_workspace_map.md#regions)

<a id="tin-window"></a>
## What This Block Covers

- What it is: The 44 fused window [launches](APPENDIX_beginner_glossary.md#g080) of the default chain, [encoder](APPENDIX_beginner_glossary.md#g009) L3–L24 and decoder L133–L154; each contains a complete FFN, Q/K/V, Q/K [normalization](APPENDIX_beginner_glossary.md#g043), window [attention](APPENDIX_beginner_glossary.md#g039), and output [projection](APPENDIX_beginner_glossary.md#g038). [chained](APPENDIX_beginner_glossary.md#g022) reuses the same core, while other view/scale variants add input or output processing before or after the core.
- Input → output: Same-tier [logical](APPENDIX_beginner_glossary.md#g085) W×H×C [E4](APPENDIX_beginner_glossary.md#g055) [features](APPENDIX_beginner_glossary.md#g008) → 64×C in 8×8 windows → same-tier [F16](APPENDIX_beginner_glossary.md#g054) result, which then [publishes](APPENDIX_beginner_glossary.md#g091) E4, a [pooled](APPENDIX_beginner_glossary.md#g018) exit, or an output view according to the variant; upsample additionally reads the previous tier's main path and the encoder [skip](APPENDIX_beginner_glossary.md#g016).
- How it is computed: Trace the data through the 11 steps and 1 intra-block diagram below; FFN first, then attention. norm acts on the projected Q/K, neither at the block entry nor by inserting another generic [LayerNorm](APPENDIX_beginner_glossary.md#g044) layer before or after FFN.
- Numeric rules: Matrices publish F16 at each [K32](APPENDIX_beginner_glossary.md#g065); the half multiplications of the 2 [residuals](APPENDIX_beginner_glossary.md#g017) first form the matrix [seed](APPENDIX_beginner_glossary.md#g042), and each subsequent step carries half; out-of-bounds window positions are zero-padded but still participate in the 64-key [reduction](APPENDIX_beginner_glossary.md#g050). Half/E4 publications and [nonfinite](APPENDIX_beginner_glossary.md#g069) rejections cannot be replaced by high-precision library operations.
- Why: Within the same scale, varying the window origin changes the positional interaction range; downsampling retains the encoder bypass, and upsampling reconnects that bypass to the main path. Training intent and the hardware causes of fusion boundaries remain unknown.
- How we know: CPU source code, verification of the 44 named [params](APPENDIX_beginner_glossary.md#g083), and saved numeric gates are listed separately in the [evidence table](#evidence); matching exits do not by themselves prove that internal values or the network decomposition are unique.
- Next down: [Windows and Heads](#partition), [Actual Order](#core), [Peripheral Variants](#wrappers), [8 Scale/Direction Configurations](#variants); for finer numeric rules, drill down along the 4 sub-item links at the top of the page.

Notation follows [INDEX](INDEX.md#shape-and-workspace-notation): spatial dimensions are written as width × height, and local [tensor](APPENDIX_beginner_glossary.md#g076) matrices are written as positions × channels; E4/F16 denote E4M3/binary16. [Q8](APPENDIX_beginner_glossary.md#g061) is half→E4 [RN-even](APPENDIX_beginner_glossary.md#g059)/[satfinite](APPENDIX_beginner_glossary.md#g062), and D8 is exact E4→half; H+, H×, and HF are half addition, multiplication, and fused multiply-add. K(A,W;s) is a matrix chain starting from half seed s that publishes F16 at each K32 in original order. s_ff, s_att, s_skip, and per-head s_q denote scales read from the model, with only their formats and uses described here and no coefficient values listed.

<a id="partition"></a>

## 8×8 Window Partitioning, Origins, and 32-Channel Heads

First interpret the physical bytes as logical W×H×C according to the current [inputlayout](APPENDIX_beginner_glossary.md#g088), and then partition into windows. Let the window index be (bx,by), with intra-window index t=0,…,63:
```math
x=8b_x+(t\bmod8)+o_x,\qquad
y=8b_y+\lfloor t/8\rfloor+o_y.
```
Currently accepted origins are 0 or −4 on each axis. If 0≤x<W and 0≤y<H, fetch the C E4 values at that position; otherwise fill the entire position with E4 [+0](APPENDIX_beginner_glossary.md#g070). **This shifts the window grid rather than cyclically wrapping the entire feature map**; at the edges, attention is neither truncated to the valid key count nor changed to an exclusionary [mask](APPENDIX_beginner_glossary.md#g006). After computation, only valid coordinates are written back, and out-of-window computation results are discarded. [Window fetch/scatter source:154–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L154)

The window canvas does not always equal the valid image:
```math
(C_W,C_H)=
\begin{cases}
(W-2o_x,\ H-2o_y),&C=32,\\
(8\lceil(W-o_x)/8\rceil,\ 8\lceil(H-o_y)/8\rceil),&C=64,128,256.
\end{cases}
```
The window count is (C_W/8)×(C_H/8); the C=32 path additionally checks that the canvas is divisible by 8. W/H must be positive, multiples of 4, and no larger than the currently configured internal canvas, and origins outside the set above are rejected; this is not a claim of support for arbitrary geometries. [Dimension/origin guards:143–155](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L143)

At 1080, the 4 tiers of valid features are 960×576×32, 480×288×64, 240×144×128, and 120×72×256 respectively, all in E4. The position count per window is fixed at 64, and the head count is h=C/32, i.e., 1/2/4/8 heads; the channel dimension of Q, K, and V per head is 32 in every case. Q/K/V are split into heads from the 64×3C half result within the Q region, K region, and V region respectively; physical channel permutations are handled by layout/[weight](APPENDIX_beginner_glossary.md#g079) unpacking, and the raw byte view cannot be reshaped directly. [Head splitting:119–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L119)

<a id="core"></a>
## Actual Order: FFN → QKV → norm(Q/K) → attention → Projection

Below is the complete behavioral chain for 1 window, where x₈ is the 64×C E4 entry:

~~~text
1. Fetch this window's x₈; bypass x₁₆=D8(x₈), except 1-head upsample takes the retained unquantized merge instead.
2. r_ff=H×(x₁₆,s_ff), serving as the half seed for FFN contraction / final projection.
3. Execute expansion→G→contraction according to L3.ffn; obtain z containing the entry residual: 64×C F16.
4. z₈=Q8(z): 64×C E4.
5. qkv=K(z₈,W_qkv;+0): 64×3C F16; Q/K/V are projected only at this point.
6. Per head, apply norm32(Q) and norm32(K) separately, and multiply Q additionally by RN16(s_q); publish Q/K/V as E4.
7. Per head, score_ij=Q32(Q_i,K_j,corresponding half position bias): 64×64 F16.
8. TIN scores undergo separate F32 multiplication and F32 addition → RN16 → clamp → encoding transform, yielding positive half weights w.
9. Compute D via the fixed half tree; check the denominator domain, look up RCP, and convert to half; p=Q8(H×(w,r)).
10. Per head, perform 2 K32 steps with p and V (first 32 keys, last 32 keys), then Q8; concatenate into av: 64×C E4.
11. r_att=H×(1-head takes z, multi-head takes D8(z₈),s_att);
    y=K(av,W_proj;r_att): 64×C F16. After scattering back, publish according to the peripheral variant.
~~~

In step 3, 1-head performs a 64×32×128 expansion, per-channel G, and 64×128×32 contraction; multi-head executes according to the actual C→128→32→C decomposition and quantization points per group—see [FFN channel accounting](L3_ffn.md#channels). The core [window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130) directly gives the "FFN first" order, with no extra entry norm and no 2nd FFN appended after attention.

In step 6, over the 32 half values of each head, only the sum of squares, max lower bound, and [RSQ](APPENDIX_beginner_glossary.md#g072) are computed; the mean is not subtracted, and ε is a lower bound rather than a term added to the sum of squares. For the reduction tree, squaring fusion direction, and each RN16, see [norm32](L3_norm_nonfinite.md#norm32). Q is Q8(H×(H×(Q,r_q),RN16(s_q))); K uses unit scale, and V undergoes Q8 directly without passing through this normalization. [norm and publication:114–121](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114)

Steps 8–10 preserve the original precision of [TIN scores and denominator tree](L3_attention_softmax.md#window-attention): first RN32(score×0.044921875), then RN32 addition of 1.30078125, followed by RN16, clamping to [1.03125,1.5693359375], and generating w via the documented encoding transform. The half encoding of the [denominator](APPENDIX_beginner_glossary.md#g048) Den must lie in [0x1c00,0x60e0], and the [function-table](APPENDIX_beginner_glossary.md#g074) lookup must have a corresponding entry; it cannot be replaced with a half FMA or a math-library [softmax](APPENDIX_beginner_glossary.md#g047). Window weights are normalized first and then quantized to E4, and the 2 K32 steps of [AV](APPENDIX_beginner_glossary.md#g077) carry F16 between them. [attention:122–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L122)

<a id="residuals"></a>
### Both Residuals Enter at the Matrix seed

| Interface | Source and publication | Non-mergeable boundaries |
|---|---|---|
| FFN entry residual | Ordinary blocks take D8(x₈), while 1-head upsample takes the unquantized merge; after H× to F16, it enters the contraction / final-projection seed | Cannot fuse the scaling multiplication and addition across the entire matrix into a single final step; inter-group half carry in multi-head FFN preserves original order |
| attention output residual | C=32 takes unquantized z; C≥64 takes D8(Q8(z)), then applies H× to F16 as the seed of the 1st K32 of W_proj | z₈ is read by [QKV](APPENDIX_beginner_glossary.md#g040); the 1-head bypass cannot be recovered from z₈, nor can multi-head skip this E4 quantization |
| Decoder skip merge | Low-resolution projection of the main path yields F16 a; HF(D8(skip),s_skip,a) publishes half merge, followed by Q8 | Nearest-neighbor only duplicates the projected result; the HF publication and subsequent E4 publication are distinct; B66 retains merge for the FFN seed, while other tiers decode from the quantized value |

Every matrix K32 step publishes F16 at its end, with seed brought in only at the starting point and carried step by step thereafter; there is no generic single real-number "+ residual" that can be moved arbitrarily to the end. Likewise, y is first half, and only the peripheral exit decides whether to apply Q8 directly to it or compute pooling separately; layout transformations themselves add no rounding. [Matrix interface:88–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88)

<a id="diagram"></a>
## Intra-Block Diagram: 1h/32c at 1080, B1 / L3

Taking origin (0,0) as the example: from 960×576×32 E4, each 8×8 window fetches 64×32 E4, and the output scatters back to the same shape. Other launches change the origin and periphery; the core interface is not rewritten by window count.

~~~mermaid
flowchart TD
    IMG["Input view: 960×576×32 E4"] --> X["8×8 windowing: 64×32 E4"]
    X --> EX["Expansion: 64×32×128 K32 chain → 64×128 F16"]
    EX --> G["Per-channel G → 64×128 E4"]
    X --> RF["D8(entry) × s_ff → 64×32 F16 seed"]
    G --> FC["Contraction: 64×128×32, carrying seed → z: 64×32 F16"]
    RF --> FC
    FC --> ZQ["Q8(z): 64×32 E4"]
    ZQ --> QKV["Projection: 64×32×96 → 64×96 F16"]
    QKV --> QK["Q/K: 64×32 F16 each → norm32 each; only Q × query scale → E4"]
    QKV --> V["V: 64×32 F16 → Q8 → E4"]
    QK --> SCORE["Q32 + half position bias → 64×64 F16"]
    SCORE --> P["Score transform, half denominator tree, RCP, H×, Q8 → 64×64 E4"]
    P --> AV["2 K32 steps with V, Q8 → 64×32 E4"]
    V --> AV
    FC --> RA["Unquantized z × s_att → 64×32 F16 seed"]
    AV --> PROJ["Output projection 64×32×32, carrying seed → y: 64×32 F16"]
    RA --> PROJ
    PROJ --> OUT["Q8, layout, scatter back → 960×576×32 E4"]
~~~

<a id="wrappers"></a>
## Shared chained Core and 4 Peripheral Wrappers

**chained** reads and writes this tier's internal [TIN](APPENDIX_beginner_glossary.md#g011) layout and executes the complete core above; each launch still [binds](APPENDIX_beginner_glossary.md#g103) its own weights, intervals, origin, and publication region, so function reuse does not mean numeric reuse. Input-view decoding and output-view encoding are both [bit-pattern](APPENDIX_beginner_glossary.md#g057) permutations, not new normalizations.

| Peripheral type | Behavior added around the core | Numeric / layout constraints |
|---|---|---|
| inpview | Unpacks the planar-split input from the previous tier's pool into this tier's logical positions, then runs the core; result is in this tier's internal layout | Entry remains W×H×C E4; processes input layout before window fetching, adding no pooling or upsampling |
| ds_wait | Core produces y F16; full=Q8(y) is retained as skip; separately performs a 2×2 average from the same unquantized y, then quantizes, projects C→2C, and quantizes into pool | full and pool are 2 independent paths, and the average cannot be redone by decoding from full; pool is handed to the next tier in planar-split layout |
| upsample | Previous tier's 2C-channel main path first undergoes a 2C→C K32 projection on the low-resolution grid; fetches with nearest-neighbor ×2 at floor(x/2),floor(y/2); merges via HF with this tier's encoder full, then feeds the core | Window-partition origin does not shift the nearest-neighbor source coordinates; input layout is the previous tier's outview. See the residual table for whether merge retains its unquantized value |
| outview_wait | Core at the end of this tier computes as usual, and then encodes Q8(y) into the output view read by the successor; produces no pool | Multi-head is a planar-split view in groups of 16 channels; B69 executes outputlayout per configuration, while its independent native layout remains [UNKNOWN](APPENDIX_beginner_glossary.md#g104) |

Downsampling averaging is strictly
```math
p=Q8\!\left(H\times\!\left(H+\!\left(H+(y_{00},y_{01}),H+(y_{10},y_{11})\right),\tfrac14\right)\right),\qquad
\mathrm{pool}=Q8\!\left(K(p,W_{\rm ds};+0)\right).
```
The 3 H+ operations and 1 H× operation each publish half separately; the averaged p is converted to E4 first, and then undergoes C→2C. Padded positions take zero according to the declared range; the allocated extent of pool depends on params and is not always a direct halving of valid W/H. L24 additionally includes explicit zero-writes to related planes outside the nominal 512 channels; one cannot publish only the valid values, strip away these writes, or zero out the entire adjacent region. [pool and padding:162–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L162)

Upsampling is
```math
a=K(\mathrm{main}_8,W_{\rm up};+0),\qquad
m_{xy}=HF\!\left(D8(\mathrm{skip}_{xy}),s_{\rm skip},a_{\lfloor x/2\rfloor,\lfloor y/2\rfloor}\right),\qquad
x_8=Q8(m).
```
B66/C=32 retains m as the FFN entry bypass; B48/B56/B62 use D8(x₈) instead. At 1440, B48 has valid height 92 while the window-partition canvas can reach 96, and the extra rows are not written back as valid output. [Merge and seed fetching:151–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L151)

The current CPU implementation writes a completion flag after numeric output for launches configured with releaseword; among the 44 bindings, inpview, chained, and upsample have that [role](APPENDIX_beginner_glossary.md#g084), whereas ds_wait and outview_wait do not have the same standalone role. The word wait in a kernel name neither directly defines a CPU wait action nor closes native synchronization/[aliasing](APPENDIX_beginner_glossary.md#g092)/lifetime semantics; this page does not extrapolate concurrency proofs from strings. [Publication:179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L179)

<a id="variants"></a>
## 4 Tiers, 2 Directions, and All Window Origins

All entries in the table below are **SHA-pinned 1080 default params instances**, with spatial boundaries taken from the [INDEX extent table](INDEX.md#shape-and-workspace-notation), and are not generalized to all controls/geometries. Origin shorthand: 0=(0,0), xy=(−4,−4), x=(−4,0), y=(0,−4); sequences correspond item by item in ascending B/launch order. Each step in each tier is a single fused window launch.

| Direction / heads, C | Tier width×height×C (E4) | B / launch, count | Kernel-type sequence | Origin sequence | Scale exits and skip pairing |
|---|---|---|---|---|---|
| Encoder / 1h, 32 | 960×576×32 | B1–B4 / L3–L6, 4 | inpview→2 chained→ds_wait | 0,xy,x,y | B4.full→B66; pool 480×288×64 |
| Encoder / 2h, 64 | 480×288×64 | B5–B8 / L7–L10, 4 | inpview→2 chained→ds_wait | 0,xy,x,y | B8.full→B62; pool 240×144×128 |
| Encoder / 4h, 128 | 240×144×128 | B9–B14 / L11–L16, 6 | inpview→4 chained→ds_wait | 0,xy,x,y,0,xy | B14.full→B56; pool 120×72×256 |
| Encoder / 8h, 256 | 120×72×256 | B15–B22 / L17–L24, 8 | inpview→6 chained→ds_wait | 0,xy,x,y,0,xy,x,y | B22.full→B48; pool 60×36×512 |
| Decoder / 8h, 256 | 120×72×256 | B48–B55 / L133–L140, 8 | upsample→6 chained→outview_wait | 0,xy,x,y,0,xy,x,y | Main path 60×36×512 + B22.full; final view to B56 |
| Decoder / 4h, 128 | 240×144×128 | B56–B61 / L141–L146, 6 | upsample→4 chained→outview_wait | x,y,0,xy,x,y | Main path 120×72×256 + B14.full; final view to B62 |
| Decoder / 2h, 64 | 480×288×64 | B62–B65 / L147–L150, 4 | upsample→2 chained→outview_wait | 0,xy,x,y | Main path 240×144×128 + B8.full; final view to B66 |
| Decoder / 1h, 32 | 960×576×32 | B66–B69 / L151–L154, 4 | upsample→2 chained→outview_wait | 0,xy,x,y | Main path 480×288×64 + B4.full; final view to B70 |

Thus the complete skip pairs are B4/L6↔B66/L151, B8/L10↔B62/L147, B14/L16↔B56/L141, and B22/L24↔B48/L133; each skip retains this tier's full E4 and this tier's spatial dimensions rather than using the pooled exit as the bypass. The C=32 attention bypass retains unquantized z, and B66 additionally retains unquantized merge for the FFN seed; the other 3 tiers quantize and then decode as described above and cannot be interchanged on the basis of matching shapes.


<a id="tin-code-transcription-r04o"></a>
### TIN Address Indexing: Source-Transcribed Tier

The evidence tier is **code-transcribed index formula**: the following are the indices adopted in the source code by the byte-reproducing executor, not new derivations or new held-out validations from r03. The verdict in [r03 result](../../../experiments/mapform-tin-r03-20261027-codex/RESULT_ZH.md) is NOT_RUN_MISSING_1080_ADDRESS_TABLES, with no frozen formulas and no new address-table elements read. The existing `tin_map(H,W,C)` output layout still retains its [Measured] closed-form tier: the legacy TIN64/TIN128 maps are reproduced element by element, and the C256 prediction is jointly verified by B15 while retaining its original boundary; [existing evidence](../../../ARCHITECTURE_V3_ZH.md#L580) is neither upgraded nor downgraded due to the missing tables in r03.

The formula below can be executed directly with Python integer arithmetic, corresponding to [logical_of and bidirectional read/write tin.cpp:73–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L73). p is the physical E4 byte index and the function returns the logical HWC byte index; for C=64/128/256, the bit order of off and xs correspond to a 4-row physical block. Divisible physical width and height are provided according to the source-code call domain.

~~~text
def logical_of(p, W, H, C, layout):
    perm = (0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15)
    if layout != 0:
        j = p % 16
        x = (p // 16) % W
        y = (p // (16*W)) % H
        plane = p // (16*W*H)
        return (y*W+x)*C + 16*plane + perm[j]
    if C == 32:
        tile, lane, byte = p // 512, (p % 512) // 16, p % 16
        x = (lane >> 2) & 3
        y = (lane >> 4) + 2*((byte >> 2) & 1)
        c = 2*(lane & 3) + (byte & 1) + 8*((byte >> 1) & 1) + 16*(byte >> 3)
        return ((4*(tile // (W//4))+y)*W + 4*(tile % (W//4))+x)*32+c
    off, blk, xs = p % 4096, p // 4096, 1024 // C
    positions = (('c',0),('c',3),('y',1),('c',4),('c',1),('c',2),('x',0),('x',1),('y',0))
    c = x = y = 0
    for index, (axis, bit) in enumerate(positions):
        value = ((off >> index) & 1) << bit
        if axis == 'c': c |= value
        elif axis == 'x': x |= value
        else: y |= value
    pos = 9
    for bit in range(5, C.bit_length()-1):
        c |= ((off >> pos) & 1) << bit
        pos += 1
    for bit in range(2, xs.bit_length()-1):
        x |= ((off >> pos) & 1) << bit
        pos += 1
    return ((4*(blk // (W//xs))+y)*W + xs*(blk % (W//xs))+x)*C+c
~~~

The next section gives the executable rowperm/n128 matrix panel offsets, their inverses, QKV rearrangement, and the tokeninternal formula for bias, corresponding to [tin.cpp:26](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26), [tokeninternal:33](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L33), and [bias indexing:46](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L46) respectively. They describe positions without reading coefficients. RSQ/RCP as well as Radius and cos/sin in F03 remain **table-driven function values**: the tables hold function results rather than address mappings; source-code index transcription neither eliminates these value-table dependencies nor changes B69's native layout status of UNKNOWN.

<a id="resource-layout-r04l"></a>
### Resource Matrices, bias, and Head Branches (from Rank 26)

Below are the CPU unpacking [closed forms](APPENDIX_beginner_glossary.md#g020) at the code-transcribed index formula tier, listing no coefficient values; they are not new held-out validations from r03. `P=(0,1,4,5,8,9,12,13,2,3,6,7,10,11,14,15)`, and matrix dimensions K and N are both multiples of 32; the n128 formula on this page additionally requires N to be a multiple of 128, which N=4C+128 satisfies when C>32. For logical (k,n):

~~~text
rk=16*(k//16)+P[k%16]; kt=rk//32; nt=n//32; ki=rk%32; ni=n%32
lane=4*(ni%8)+(ki%16)//4; elem=ki%4+4*(ki//16)
frag=(ni//8)%2; pair=ni//16
tile=4*((nt//4)*(K//32)+kt)+nt%4  # n128; otherwise kt*(N//32)+nt
offset=1024*tile+512*pair+16*lane+8*frag+elem
W[k,n]=resource[base+offset]
~~~

The inverse extracts [tile](APPENDIX_beginner_glossary.md#g087), pair, lane, frag, and elem from offset; `ki=4*(lane%4)+elem%4+16*(elem//4)`, `ni=lane//4+8*frag+16*pair`. The ordinary tile inverse is `(kt,nt)=divmod(tile,N//32)`; the n128 inverse is `kt=(tile//4)%(K//32), nt=4*((tile//4)//(K//32))+tile%4`. Applying the inverse permutation of P to the low 4 bits of rk then recovers k. This also gives the packing formula without reading real coefficients. [tin.cpp:26–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26).

The resource cursor o starts at 0; `mat(K,N,major)` consumes K*N bytes, `half(n)` consumes 2n bytes of LE16, and skipped bytes are not interpreted as coefficients. The complete sequence is: for C=32, ex(32,128), branch(128,32); for C>32, ex(C,4C+128,n128), out(C,C); when up, extra(2C,C); if not up or C=32, skip 16; cs(C); when up, if C=32 skip 16 again, then read sin(C), and if not up skip 16; qkv(C,3C); [bias](APPENDIX_beginner_glossary.md#g052)(H*4096) with H=C/32; H LE32 scale values each rounded via RN16; align o upward to 16; proj(C,C); ca(C); when down, extra(C,2C). Before each consumption, check o+len≤resource length. [tin.cpp:34–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34).

For C≥64, the QKV logical column `type*C+32*h+c` comes from the raw unpacked column `96*h+32*type+c`, with type=0..2 and c=0..31. Let `I(t)=32*((t//8)//4)+16*((t%8)//4)+4*((t//8)%4)+t%4`; setting r=I(i) and c=I(j), bias(h,i,j) is read from half-array index `4096h+256*(4*(r//16)+c//16)+8*(4*(r%8)+(c%8)//2)+4*((c%16)//8)+2*((r%16)//8)+c%2`. Forward and inverse are read/scatter under the same bijection and add no rounding. [tin.cpp:43–50](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L43).

For C>32, the 3 matrices reused per head are: `ex_h[k,j]=ex[k,128h+j]` (C×128), `branch_h[k,j]=ex[32h+k%32,4C+32*(k//32)+j]` (128×32), and `out_h[k,j]=out[32h+k,j]` (32×C). panel merely converts a logical matrix into column-major storage `panel[j*K+k]`; pre-decoding neither alters numeric values nor adds new half publications. [tin.cpp:53–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L53).

<a id="view-layout-r04l"></a>
### Bidirectional Byte Formulas for Input/Output Views (from Rank 27)

The following byte permutations are code-transcribed index formulas applicable to all 20 kernel families on this page, and do not constitute new held-out validations from r03. `decode[L(p)]=physical[p]` and `encode[p]=logical[L(p)]`; neither direction performs numeric conversion. A nonzero layout uses planar16: `j=p%16,x=(p//16)%W,y=(p//(16W))%H,plane=p//(16WH)`, `L(p)=(yW+x)C+16plane+Q[j]`, with `Q=(0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15)`; the inverse is `p=16*((c//16*H+y)*W+x)+Q_inverse[c%16]`.

When layout=0 and C=32, `tile=p//512,l=(p%512)//16,b=p%16`; `x=(l>>2)&3,y=(l>>4)+2*((b>>2)&1),c=2*(l&3)+(b&1)+8*((b>>1)&1)+16*(b>>3)`, and the outer tile origin is `(4*(tile%(W//4)),4*(tile//(W//4)))`. Inverse formula: taking the low 2 bits of global x/y as xx/yy, `l=((c>>1)&3)+4*xx+16*(yy&1)`, `b=(c&1)+2*((c>>3)&1)+4*(yy>>1)+8*(c>>4)`, and `p=512*((y//4)*(W//4)+x//4)+16l+b`.

When layout=0 and C=64/128/256, xs=1024/C, off=p%4096, and blk=p//4096; the low 9 bits of off are routed in order to `(c0,c3,y1,c4,c1,c2,x0,x1,y0)`, followed first by c5..log2(C)−1 and then by x2..log2(xs)−1. Global x/y add `xs*(blk%(W//xs))` and `4*(blk//(W//xs))` respectively, giving `L(p)=(yW+x)C+c`. The inverse reassembles these bits back into off in the same order, with `blk=(y//4)*(W//xs)+x//xs` and `p=4096blk+off`. W/H must satisfy the physical tile divisibility conditions, and a cropped logical width cannot be used to compute tile addresses. [tin.cpp:72–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L72). This closes the specification of the CPU byte arrangement without closing the independent native coordinate label UNKNOWN for B69.

<a id="zero-planes-r04l"></a>
### Byte Range of L24 Extra Planes (Rank 145)

The C=256 down output additionally performs boundary zero-writes across 64 planar16 planes (including 32 planes outside the nominal 512 channels). Let `validW=(W+1)//2,validH=(H+1)//2`; for plane=0..63 and y=0..PH−1, `begin=validW if y<validH else 0`; if begin≥PW the span is empty, and otherwise write `len=16*(PW-begin)` zero bytes at `off=16*((plane*PH+y)*PW+begin)` relative to the pooledword pointer. Checked multiplication is used first, followed by verifying that pointer+off does not overflow and that the entire span lies within the [workspace](APPENDIX_beginner_glossary.md#g082); `[0,validW)` of valid rows is preserved, and one cannot zero the entire pooled allocation and overwrite aliased valid values. [tin.cpp:165–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L165). For the qword, length, and empty set of standalone release, see the [workspace contract](L3_workspace_map.md#release-contract-r04l).

<a id="evidence"></a>
## How We Know

| Object | Basis and supported scope (1 line each) |
|---|---|
| Core wiring | [CENSUS](APPENDIX_beginner_glossary.md#g100): [window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130) and [norm/attention:114–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114) give the order, head, and seed; the CPU implementation decomposition does not by itself prove native internal uniqueness |
| 44 window configurations | Read-only [parameter verification record](../skewer/examples/tin_window_r04c.bindings.json) in this round: actual SHAs of all params match the saved bindings, and extent, origin, and view fields agree; this is a content check with no new numeric runs |
| Legacy per-launch gates | MEASURED: [TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3) shows 3-way full-workspace agreement for L3/7/11/18/24/133/134/151; the remaining 36 NOT_RUN entries remain, and [teacher-forced](APPENDIX_beginner_glossary.md#g106) does not equal a continuous chain |
| Later named chains | MEASURED: [M2 record](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) covers all 44 TIN launches for 1080/1440 f0; new 4K [M2](APPENDIX_beginner_glossary.md#g107) numeric runs cover only [L0](APPENDIX_beginner_glossary.md#g081)–L99, so its TIN decoder cannot be relabeled as newly measured on the basis of a configuration census, while the later 3 frames of unified M have their own separate [scope](L3_b70_history_output.md#evidence) |
| Encoder/decoder bypasses | CENSUS / MEASURED: [ARCH §4.5, §4.8](../../../ARCHITECTURE_V3_ZH.md#45-上采样过渡块b48--b56--b62--b66) together with this page's params/source code jointly support the 4 skip pairs, nearest-neighbor, and fusion; same-shape addresses or a single byte comparison are not upgraded to a structural theorem over arbitrary inputs |
| Retained unknowns | The symbolic provenance tier of L133 [computed-shared](APPENDIX_beginner_glossary.md#g108) remains NOT_ADMITTED, and B69's independent native layout remains UNKNOWN; general geometries, complete synchronization/aliasing/lifetime, and uniqueness of internal values are not established, and passing the numeric chain does not automatically lift them |

Positive vector-norm reduction can [overflow](APPENDIX_beginner_glossary.md#g071) to +Inf; whether it is absorbed by a specific RSQ interface is determined by the [nonfinite contract](L3_norm_nonfinite.md#nf-path), and is not written as "finite inputs guarantee all internal values are finite." Nonfinite QMMA seeds / half overflow, E4 NaN, missing-table / out-of-domain inputs, and unsatisfied parameter/interval/window-canvas guards are still rejected, and the saturating quantization of G cannot be used to let a preceding step pass. Full SHAs, per-launch configurations, and correction records for legacy publication omissions remain in the [TIN evidence appendix](APPENDIX_evidence_history.md#tin-window-r04c).

Half-window shifting allows subsequent windows to place positions from both sides of a previous boundary into the same interaction domain, expanding cross-window information paths; its training benefit has not been independently measured. Padding to full 8×8 windows is the actual requirement of the read window-fetch/scatter loops and their dimension guards, and no general rounding formula for the root canvas height is derived from it.
