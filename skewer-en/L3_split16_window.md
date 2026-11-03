# L3.window-attention: Complete split16 Block and Four-Kernel Handoff

<!-- beginner-r04m:start intro -->
<a id="beginner-split"></a>
[Beginner Simplification] This section passes the [512](APPENDIX_beginner_glossary.md#g007) items at each position through eight [window](APPENDIX_beginner_glossary.md#g015) blocks. Each block first processes each position individually and then exchanges content within 8×8 positions; the entry [bypass](APPENDIX_beginner_glossary.md#g016) connects to [feed-forward](APPENDIX_beginner_glossary.md#g037) contraction, and the feed-forward-result bypass connects to [attention](APPENDIX_beginner_glossary.md#g039) [post-projection](APPENDIX_beginner_glossary.md#g038). The fewer-box version is:

~~~mermaid
flowchart LR
    X["Block entry"] --> F["Per-position processing; contraction start connects to entry bypass"] --> Z["Feed-forward result"] --> A["Window comparison and content mixing"] --> P["Projection start connects to feed-forward bypass"] --> Y["Block exit"]
    X -. "First bypass" .-> F
    Z -. "Second bypass" .-> P
~~~

Position grid → window → 16 comparison heads → 32 items per head forms a single set of [logical](APPENDIX_beginner_glossary.md#g085) relationships; the eight FFN groups and device execution coordinates are accounted for separately—see [Four Types of Groupings](L1_00_one_block_primer.md#groups). Independent spatial pairing for terminal sparsification and the bridge still carries question marks, and the [DAG](APPENDIX_beginner_glossary.md#g089) [contracts](APPENDIX_beginner_glossary.md#g101) below do not erase what is unknown.
<!-- beginner-r04m:end intro -->

[Full Skewer Index](INDEX.md) · Parent level: [split16 Encoder](L2_04_split16_encoder.md), [split16 Decoder](L2_07_split16_decoder.md) · Expanded sub-items: [FFN](L3_ffn.md#channels), [window attention](L3_attention_softmax.md#window-attention), [Q/K norm](L3_norm_nonfinite.md#map-norm), [workspace / address maps](L3_workspace_map.md#address-maps)

<a id="window-attention"></a>
## What This Block Covers

- What it is: The 512-channel, [16-head](APPENDIX_beginner_glossary.md#g013) window-block [family](APPENDIX_beginner_glossary.md#g080); [encoder](APPENDIX_beginner_glossary.md#g009) B23–B30 uses L25–L57 for 33 launches in total, and decoder B40–B47 uses L101–L132 for 32 launches in total, making 65 launches overall. Ordinarily one block is four kernels, while B30 additionally includes L57 width adaptation.
- Input → output: Tier-5 X₅(512) [E4](APPENDIX_beginner_glossary.md#g055) → same-tier 512-channel E4; the encoder end additionally [publishes](APPENDIX_beginner_glossary.md#g091) X₆(512), which passes through final_head to become X₆(1024) entering [ViT](APPENDIX_beginner_glossary.md#g014); the decoder end publishes [outview](APPENDIX_beginner_glossary.md#g022) for [TIN](APPENDIX_beginner_glossary.md#g011) [upsampling](APPENDIX_beginner_glossary.md#g021) to read.
- How it is computed: **ffwd → ffwd_proj → qkv (including Q/K [normalization](APPENDIX_beginner_glossary.md#g043) and attention) → proj**. First complete FFN and its entry [residual](APPENDIX_beginner_glossary.md#g017), then perform window attention and its output projection / residual; there is no extra block-entry [LayerNorm](APPENDIX_beginner_glossary.md#g044) and no second FFN after attention.
- Numeric rules: [Matrices](APPENDIX_beginner_glossary.md#g051) publish [F16](APPENDIX_beginner_glossary.md#g054) at each [K32](APPENDIX_beginner_glossary.md#g065); G, Q/K statistics, the [denominator tree](APPENDIX_beginner_glossary.md#g050), half-[scale](APPENDIX_beginner_glossary.md#g031) multiplications, and E4 publications each preserve their respective nodes. Both residuals first undergo [H×](APPENDIX_beginner_glossary.md#g063) to become a half [seed](APPENDIX_beginner_glossary.md#g042) and are then carried step by step along the matrix chain; they cannot be moved to a single addition after the complete dot product.
- Why: A "block" is organized around a shared entry, two bypasses, and the exit to the next block; between the four launches there is an actual handoff of [workspace](APPENDIX_beginner_glossary.md#g082) [roles](APPENDIX_beginner_glossary.md#g084). Why the native binary chose these four fusion boundaries, along with its training motivation and hardware-capacity reasons, remains unknown.
- How we know: Named [params](APPENDIX_beginner_glossary.md#g083)/maps, the CPU executor, and saved segment / full-chain results are listed separately in the [evidence table](#evidence); matching exit bytes do not prove a unique network decomposition.
- Next down: [Four-Kernel Order](#order), [16 Heads and Window Partitioning](#heads), [Eight-Field Address Closed Forms for qkv](#qkv-closed-form-r04n), [1080 Layout Accounting](#layout), [Intra-Block Diagram](#wiring), [Encoder/Decoder Variants](#variants). This page retains the arithmetic of the existing sub-items; the newly added closed forms expand only addresses and indices.

E4/F16, K32, and X₅/X₆ follow the [INDEX notation](INDEX.md#shape-and-workspace-notation); for the definitions of [Q8](APPENDIX_beginner_glossary.md#g061), D8, and H×, see [FFN notation](L3_ffn.md). Throughout this page, N_out is always the **byte length** returned by a single executor call, not a new channel axis.

<a id="order"></a>
## How Four Launches Form One Block

Let X be the current block's entry E4, U the ffwd exit, Z the ffwd_proj exit, A the fused qkv exit, and Y the final projection exit:

~~~text
ffwd       : X → 512→512 pre-projection, E4 → eight groups of 64→256→G→64, E4 → U
ffwd_proj  : U + current-block X → 512→512 post-projection, using H×(D8(X),s_ff) as seed → E4 of Z
qkv        : Z → Q/K/V → norm(Q/K), E4 → 64-key attention, AV, E4 → A
proj       : A + current-block Z → output projection, using H×(D8(Z),s_att) as seed → E4 of Y
next block : takes Y as its own X, rebinding weights, bypasses, origin, and workspace intervals
~~~

For the channels and all quantization points of the first two lines, see the [split16 FFN table](L3_ffn.md#channels). The intra-kernel gate width of ffwd is 2048, while the exit U remains 512 channels; these eight per-position FFN groups are a different axis from the 16 attention heads that follow.

Inside qkv, Q/K/V are projected first, followed by the [32-channel Q/K statistics](L3_norm_nonfinite.md#map-norm), while V publishes E4 directly; subsequently, [window scores, half reduction, RCP, and AV](L3_attention_softmax.md#window-attention) are all completed within this single launch. Thus A is already the attention exit, and this kernel cannot be treated as merely generating three copies of Q/K/V to be consumed by a subsequent kernel. norm belongs to the Q/K path here, and the remaining three regular kernels do not add another norm layer as a result.

The two bypasses come from different sources: ffwd_proj reads the current block's X, whereas proj reads the current block's Z; both are exact decodings of already published E4 values, each multiplied independently by a half scale. Across the checked graphs for L28 ordinary proj, L56 dual-exit projection, and the L132 terminal view, the first seed of every matrix chain is this scaled bypass, with each subsequent K32 carrying half; each projection chain in L28 consists of 16 K32 steps. The active seed bytes in the concrete fetch maps also fall entirely within the second input role, rather than merely sharing the same shape. [Graph and provenance check](APPENDIX_evidence_history.md#split16-window-r04d)

The CPU executor runs matrix and elementwise nodes in graph order, slices the returned bytes back into named intervals according to the output list, and then executes the completion-flag [side effect](APPENDIX_beginner_glossary.md#g094) of that [binding](APPENDIX_beginner_glossary.md#g103). [split16.cpp:65–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L65); L132 actually takes the dedicated terminal-view wiring in [entry.cpp:93–94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L93). The four names describe different compute/storage boundaries; function reuse does not imply reuse of [weights](APPENDIX_beginner_glossary.md#g079), numeric values, or synchronization roles, nor is a complete native concurrency proof extrapolated from the strings wait or chained.

<a id="heads"></a>
## 16 Heads, 8×8 Windows, and Shifting

The logical channel relationship is 512=16×32. Each 8×8 window has 64 positions; per head, Q/K/V are each 64×32, scores and normalized weights are each 64×64, and [AV](APPENDIX_beginner_glossary.md#g077) returns to 64×32; the 16-head results are handed to the output projection to form the next block's 512-channel trunk. Physical interleaving and writeback for head merging follow the map, and raw exit bytes cannot be reshaped directly into an arbitrary head order.

8×5 windows of 8×8 cover a 64×40 canvas, and the [pooled](APPENDIX_beginner_glossary.md#g018) logical capacity is 32×20×512 E4. In the measured map, 327,680 B is uniquely covered by 20,480 16 B write events; bucketing by 8192 B yields 40 buckets. [Inference] Pairing each 8×8 input window with a 4×4 spatial exit is compatible with these integers, but capacity bucketing does not establish spatial wiring. Establishing the pairing additionally requires independently calibrating input window indices and the logical (x,y,c) of pooled bytes and checking source/destination coordinates per write event; recovery involving L100 further requires independent coordinate calibration of the output and skip layouts. For the detailed integer sources, see the [L100 operator](L2_06_decoder_bridge.md#operator).

At 1080, the valid tier-5 dimensions are width 60 × height 36; all four declared shifts cover 8×5 windows, with 64 keys per window in every case. This 40 is the window count, not the [CTA](APPENDIX_beginner_glossary.md#g087) count, nor does it change the position count of the primary exit to 40×64. The window count, boundary provenance, cross-lane selection, and writeback of qkv now have [this family's closed forms](#qkv-closed-form-r04n); TIN formulas cannot be applied to them, nor can the window count that happens to remain invariant at 1080 be generalized to other geometries.

In this round, reading the params of all 16 qkv launches directly shows: width/height reside in the 3rd U64 word, and the origin resides in the 4th U64 word (both 0-indexed). Encoder B23–B30 and decoder B40–B47 each follow

~~~text
(0,0), (−4,−4), (−4,0), (0,−4), (0,0), (−4,−4), (−4,0), (0,−4)
~~~

When the shift changes, the provenance graph is rebound; graphs with the same shift can be identical across named instances, which neither licenses reusing weights or numeric values nor turns identical SHAs into a proof of all dynamic provenance. Independent ordering admission for the 16-head [bias](APPENDIX_beginner_glossary.md#g052) remains [UNKNOWN](APPENDIX_beginner_glossary.md#g104), retaining the scope stated in [ARCH ordering boundary:577](../../../ARCHITECTURE_V3_ZH.md#L577) and [concrete attention graph boundaries](L3_attention_softmax.md#graph-bindings).

<a id="qkv-closed-form-r04n"></a>
## Eight-Field Address Closed Forms for qkv: Exact Validation on Held-Out Maps

The evidence tier is **closed forms verified on held-out map tables**, with original verdict **PARTIAL_QKV_CLOSED_FORM_8/9_FIELDS_HELDOUT_EXACT**. Below are CLOSED_FORMULA expressions for the CPU address/index tables, not new native numeric measurements. The [research results](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md), [frozen physical explanation](../../../experiments/mapform-split16-qkv-r01-20261027-codex/FORMULAS_ZH.md), and [frozen formula source code](../../../experiments/mapform-split16-qkv-r01-20261027-codex/formula_qkv.py) preserve the conclusions, derivations, and implementation respectively.

For the meanings of "held-out", EXACT, and TABLE, see the [label legend](APPENDIX_beginner_glossary.md#address-status).

**Coordinate card.** $H,W$ are the physically padded token height and width, not raw frame pixels, and within the validated domain they are positive multiples of 4; $(d_x,d_y)$ each take −4 or 0. The starting point of an 8×8 window is $(8w_x+d_x,8w_y+d_y)$, with coverage formulas

```math
G_X=\left\lceil\frac{W-d_x}{8}\right\rceil,\quad
G_Y=\left\lceil\frac{H-d_y}{8}\right\rceil,\quad Q=G_XG_Y,\quad A=4Q.
```

In the table coordinates $(a,y,\ell,e,b)$, $a\in[0,A)$ is flattened with window x fastest, window y next, and head group slowest; $y\in[0,4)$ is the intra-CTA [warp](APPENDIX_beginner_glossary.md#g087) index, $\ell\in[0,32)$ is the lane, $e$ is each field's own event index, and $b$ is the byte within a vector. Unpacking gives

```math
w_x=a\bmod G_X,\quad w_y=\lfloor a/G_X\rfloor\bmod G_Y,\quad
z=\lfloor a/Q\rfloor,\quad h=4z+y.
```

Notation such as F18.36 below refers to audit family / item IDs—see [ID explanation](L2_04_split16_encoder.md#audit-family-ids); do not confuse it with the F16/half number format.

$z$ is one of the four head groups, where the four warps in each group each manage one head; $h$ is the index of the 16 heads in the CPU layout, with 32 items per head. It does not independently prove the native head/query/key label ordering of bias, so F18.36 remains UNKNOWN. Each 4×4 physical block stores $4\cdot4\cdot512=8192$ B of input; one row contains $W/4$ blocks. The constants below are all layout sizes, byte strides, or event groupings, not model coefficients.

**Resource load `wload_off`, $0\le e<112$.** The first 96 events are 16 K32 baskets with 6 16 B transactions per basket, processing the Q/K/V panels for the 512 input items; the last 16 events read each head's 64×64 F16 position-bias plane:

```math
\mathrm{wload}=\begin{cases}
49152\lfloor e/6\rfloor+3072h+512(e\bmod6)+16\ell,&e<96,\\
786432+8192h+512(e-96)+16\ell,&96\le e<112.
\end{cases}
```

$49152=16\cdot3\cdot32\cdot32$ is a full-head segment for one basket, $3072=3\cdot32\cdot32$ is a single-head basket segment, and $512=32\cdot16$ is one round of lane transactions; $786432=512\cdot1536$ is the total length of the QKV panel, and $8192=64\cdot64\cdot2$ is the size of a single-head bias plane. Only intra-resource addresses are computed here.

**Shared position `sread_shared_off`, $0\le e<64$:**

```math
\mathrm{shared}=512(e\bmod16)+16\ell.
```

Every 16 events traverse the 8192 B shared region, cycling four times over 64 events; it does not vary with window, head group, or warp.

**Shared source `sread_src`, $0\le e<64,\ 0\le b<16$:**

```math
t_x=2w_x+d_x/4+(\lfloor e/2\rfloor\bmod2),\quad
t_y=2w_y+d_y/4+(\lfloor e/4\rfloor\bmod2).
```

If $0\le t_x<W/4$ and $0\le t_y<H/4$, then

```math
\mathrm{sread}=8192(t_yW/4+t_x)+1024\lfloor e/8\rfloor
+512(e\bmod2)+16\ell+b;
```

otherwise every byte is **−1**, denoting constant zero; one must not add $b$ to −1 first. The 64 events are divided into eight 64-item groups, four spatial sub-blocks, and two 32-item half-segments; 1024 is the byte count of a 64-item slice within a 4×4 block, and 512 is its 32-item half-segment. All heads read the same 512-item input, so the source does not depend on $h$.

**Two 4 B resource accesses `xsite_src` / `xsite_wsrc`, $0\le e<2,\ 0\le b<4$:**

```math
\mathrm{xsite\_src}=-3,\qquad
\mathrm{xsite\_wsrc}=917504+4h+b.
```

**−3** indicates reading from resource space rather than an input byte or constant zero. $917504=786432+16\cdot64\cdot64\cdot2$, stepping past the QKV panel and the 16 bias planes; both events fetch the same resource location and do not vary with lane, window, or event. The resource numeric value at that address is not read here.

**Writeback `gstore_off`, $0\le e<4$:**

```math
t_x=2w_x+d_x/4+(e\bmod2),\quad t_y=2w_y+d_y/4+\lfloor e/2\rfloor.
```

Using the same physical-block boundary condition as sread, when valid:

```math
\mathrm{gstore}=8192(t_yW/4+t_x)+2048z+512y+16\ell,
```

and otherwise **−1**, skipping that write transaction. 2048 is the $4\cdot4\cdot128$ B head-group slice, and 512 is the $4\cdot4\cdot32$ B single-head slice; the result is the starting point of a 16 B transaction. Window shifts land on 4×4 block boundaries, and out-of-bounds accesses use the sentinel rather than rolling modulo the image width and height. Zero-padding on −1 in sread and write-skipping on −1 in gstore are two distinct actions.

**Exchange source `shfl_idx`, $0\le e<72$.** Let $p=e\bmod36$, and for the last 32 events further let $j=p-4$:

```math
\mathrm{shfl}=\begin{cases}
4(\ell\bmod8)+(\lfloor\ell/8\rfloor\mathbin{\oplus}p),&p<4,\\
\lfloor\ell/4\rfloor+8(j\bmod2)+16\lfloor j/16\rfloor,&4\le p<36.
\end{cases}
```

$\oplus$ is integer bitwise XOR. The first four events regroup the low three bits of the lane and swap the high two bits; the last 32 events alternate fetching sources between the low and high 16-lane halves of 8-lane groups. 36 events form one round, and the two rounds are identical.

**Two-way selection `psel`, $0\le e<32$.** Let $p=e\bmod16$ and $\mathrm{bit}_k(\ell)=\lfloor\ell/2^k\rfloor\bmod2$:

```math
\mathrm{psel}=\begin{cases}
\mathrm{bit}_0(\ell),&p<4,\\
1-\mathrm{bit}_1(\ell),&4\le p<8,\\
1-\mathrm{bit}_3(\ell),&8\le p<12,\\
1-\mathrm{bit}_4(\ell),&12\le p<16.
\end{cases}
```

Two rounds of 16 events repeat four selection families, where 1/0 select the first/second source of a node respectively; they are not conditional probabilities.

**The ninth field `thread_class` remains TABLE.** None of the 1080 derivation tables contain this field (NOT_PRESENT), and the frozen single-class-0 hypothesis failed on the held-out historical table: 1536/2048 elements unequal. Although that table can be described a posteriori as four classes of 512 items each varying along the CTA axis, a post-validation description cannot be relabeled as a newly passed formula. The existing production executor still reads the original tables, and no formula backend has been integrated in this round. [Frozen failure and the sole table containing classes](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md#thread_class失败保留类别表)

**Validation and applicability boundaries.** The 1080 physical $H\times W=36\times60$ is the derivation set; reference $12\times12$, 640×360-class $12\times20$, 1440 $48\times80$, and 4K $68\times120$ are held out, covering all four existing shifts for each. Prior to freezing, only the shapes in the held-out headers were used to clarify the coverage formula, without reading held-out elements; after freezing, the formulas were not modified. The study bound container SHAs across 495 materialized NPZ paths, with all 8 fields matching element by element and array payloads matching byte for byte, without skipping negative sentinels or invalid regions. Different containers may share arrays and cannot be treated as independent native captures, nor is coverage claimed for geometries or archives outside the inventory.

What is closed here is address-map equality; it does not upgrade proofs of the numeric DAG, full chain, or dynamic native provenance/synchronization, and F18.36 ordering as well as maps of other families remain in their original states. Four full rows in the original audit—F18.02/.03/.04/.39—change from TABLE to CLOSED; in F18.05, the shfl_idx and psel sub-fields are CLOSED while the thread_class sub-field is TABLE, so the row remains TABLE when summarized by its weakest item. [Row-by-row and field-by-field classification](../skewer/examples/r04n.classification.json)

<a id="qkv-worked-r04n"></a>
### Inexpensive Spot-Check of Two Windows

The [read-only example script](../skewer/examples/qkv_closed_form_r04n.py) imports the frozen formulas, independently transcribes the expressions above, and extracts only 58 address/index cells from the NPY stream to print side by side against the stored tables, without running full maps, the model, or the chain. [This round's results and source SHAs](../skewer/examples/r04n.qkv_samples.json). In the table below, both windows take $(d_x,d_y)=(-4,-4)$ and $y=2,\ell=5,z=0$; 1080 selects $(w_x,w_y)=(0,0)$, $G_X,G_Y=8,5,a=0$; 4K selects $(1,1)$, $G_X,G_Y=16,9,a=17$. The full receipt also checks the 0 branch of psel using lane21.

| Field / local coordinates | 1080 formula / stored table | 4K formula / stored table |
|---|---:|---:|
| wload_off, e=96 | 802896 / 802896 | 802896 / 802896 |
| sread_shared_off, e=16 | 80 / 80 | 80 / 80 |
| sread_src, e=0,b=15 | −1 / −1 | 254047 / 254047 |
| sread_src, e=6,b=7 | 87 / 87 | 507991 / 507991 |
| xsite_src, e=1,b=3 | −3 / −3 | −3 / −3 |
| xsite_wsrc, e=1,b=3 | 917515 / 917515 | 917515 / 917515 |
| gstore_off, e=3 | 1104 / 1104 | 509008 / 509008 |
| shfl_idx, e=35 | 25 / 25 | 25 / 25 |
| psel, e=8 | 1 / 1 | 1 / 1 |

These are address numbers from the actual stored tables, not model coefficients or image results; the 58-cell spot-check neither replaces the full-table held-out validation saved in the study nor re-runs that validation.


<a id="rest-closed-form-r04o"></a>
## F16, F17, F19–F23: Shared Physical Block and Per-Field Closed Forms

Evidence tier: **closed forms verified on held-out map tables**, applicable only to the concrete non-empty fields marked EXACT and the bound geometries in the table below; all other entries retain FAIL, TABLE, or VACUOUS. 1080 is the derivation set, and held-out elements were read for the first time after r02 was frozen; see [results](../../../experiments/mapform-split16-rest-r02-20261027-codex/RESULT_ZH.md), [formula-by-formula explanation](../../../experiments/mapform-split16-rest-r02-20261027-codex/FORMULAS_ZH.md), and [frozen formulas](../../../experiments/mapform-split16-rest-r02-20261027-codex/formula_rest.py). r04 has bound and validated the 4K address maps for F16/F17/F19–F22; F18 follows the independent QKV results from r01. The H=36, W=60 table of F23 has been bound and compared, but r04 did not independently bind a 4K input-frame identity for that table. Array equality does not prove the numeric DAG, full chain, synchronization, or independent native dynamic provenance.

| Family and physical role | r02 verdict on non-empty fields | Empty fields / classes | Bound geometries H×W |
|---|---|---|---|
| F16: L25 ffwd_inpview | wload_off, sread_shared_off, gstore_off EXACT; sread_src FAIL | xsite_src/xsite_wsrc: only one held-out table stores empty arrays VACUOUS, 1080 NOT_PRESENT | 36×60 derivation; 12×12, 12×20, 48×80 (1440), and 68×120 (4K) held out; 4K has three paths / one container |
| F17: L26 ffwd_proj_inpview | wload_off, sread_shared_off, gstore_off, xsite_src, xsite_wsrc EXACT; sread_src FAIL | No class-field passing verdict | 36×60 derivation; 12×12, 12×20, 48×80, and 68×120 (4K) held out |
| F19: ordinary proj | sread_shared_off, sread_src, gstore_off EXACT; wload_off, xsite_src, xsite_wsrc FAIL (shape) | thread_class hypothesis FAIL, remains TABLE | 36×60 derivation; 12×12, 12×20, 48×80, and 68×120 (4K) held out |
| F20: ordinary ffwd | wload_off, sread_shared_off, sread_src, gstore_off EXACT | Both xsite fields all-empty VACUOUS; thread_class hypothesis FAIL, remains TABLE | 36×60 derivation; 12×12, 12×20, 48×80, and 68×120 (4K) held out |
| F21: ordinary ffwd_proj | wload_off, sread_shared_off, sread_src, gstore_off, xsite_src, xsite_wsrc EXACT | thread_class hypothesis FAIL, remains TABLE | 36×60 derivation; 12×12, 12×20, 48×80, and 68×120 (4K) held out |
| F22: L56 proj_pool | wload_off, sread_shared_off, sread_src, gstore_off, xsite_src, xsite_wsrc, shfl_idx, psel EXACT | thread_class candidate also EXACT against held-out tables, still remains TABLE | 36×60 derivation; 12×12, 12×20, 48×80, and 68×120 (4K) held out |
| F23: L57 final_head | wload_off, sread_shared_off, sread_src, gstore_off EXACT | Both xsite fields all-empty VACUOUS | pooled input 20×32 derivation; 8×8, 8×12, 24×40, and 36×60 held out; 4K input-frame identity not independently bound |


<a id="r04-four-k-r04p"></a>
### r04 Geometry Bindings and Per-Field Counts

r04 bound 31 of 62 candidates and compared 10 distinct "(container SHA, family, geometry)" combinations element by element and byte for byte across array payloads, with zero differences across 416,023,808 elements; the remaining 28 L132 entries and 3 B31 entries lie outside the formula domain and remain OUT_OF_SCOPE and NOT_RUN respectively. See [structured bindings](../../../experiments/mapform-split16-r04-20261027-codex/BINDINGS.json), [comparison results](../../../experiments/mapform-split16-r04-20261027-codex/COMPARISONS.json), and [identity receipts](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json); duplicate path counts are not treated as independent capture counts.

In the table below, F16/F17/F19–F22 are all 4K physical token grids with H=68, W=120 using the frozen r02 formulas; every non-empty field is EXACT/0 both element by element and across array payloads. Path counts and container SHA counts are listed separately, and element counts are per-field element counts after deduplicated comparison. W=resource offset, Sh=shared offset, S=shared source, G=writeback; X and Xw are the two xsite fields.

| Family | Paths / distinct containers | Elements per field (each EXACT/0) |
|---|---:|---|
| F16 | 3 / 1 | W 4,423,680; Sh 2,211,840; S 35,389,440; G 276,480 |
| F17 | 1 / 1 | W 2,211,840; Sh 2,211,840; S 35,389,440; G 276,480; X, Xw 13,271,040 each |
| F19 | 7 / 1 | W 4,423,680; Sh 2,211,840; S 35,389,440; G 276,480; X, Xw 13,271,040 each |
| F20 | 7 / 1 | W 8,847,360; Sh 2,211,840; S 35,389,440; G 276,480; X, Xw 0 each (empty array VACUOUS) |
| F21 | 7 / 1 | W 2,211,840; Sh 2,211,840; S 35,389,440; G 276,480; X, Xw 13,271,040 each |
| F22 | 2 / 1 | W 2,211,840; Sh 2,211,840; S 35,389,440; G 345,600; X, Xw 13,271,040 each; class 34,560; exchange 8,847,360; selection 2,211,840 |

F18 is qkv, **not an r02 formula family**, and r04 did not re-run QKV. Its 4K coverage is supported by the [existing held-out results of the r01 frozen QKV formulas](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md#每字段每几何留出结果): 12 paths, 4 distinct containers, with all 8 fields EXACT element by element and across payloads; the per-field element counts are W 31,997,952, Sh 18,284,544, S 292,552,704, X and Xw 2,285,568 each, G 1,142,784, exchange 20,570,112, and selection 9,142,272. The four containers may share arrays and do not equal four independent captures. The thread_class failures in F18/F19/F20/F21 are not overridden by the exact results on the class-free 4K fields; although the F22 class field was compared and matched, it remains table-driven.

The 1440 L25 table of F16 has H=48, W=80, one path, one container: W 1,966,080, Sh 983,040, S 15,728,640, and G 122,880 items are all EXACT/0. Parameters and map are bound via [two SHA records in the same bundle](../../../experiments/parity-cpp-geo2-l62-diagnosis-r01-20261009-codex/LINUX_1440_RESET_REUSE_PLAN_V3.json#L5397), and direct reading of the parameter bytes corresponds to 48×80.

F23 **has no table with an independently bound 4K input-frame identity**. r04 did bind an F23 H=36, W=60 physical table located under a high2160 path, whose W 2,621,440, Sh 1,310,720, S 20,971,520, and G 163,840 items are EXACT/0, with both xsite fields empty; the [binding entry](../../../experiments/mapform-split16-r04-20261027-codex/BINDINGS_ZH.md#L88) and [comparison receipt](../../../experiments/mapform-split16-r04-20261027-codex/COMPARISONS.json) give the geometry and SHAs. A path label alone is insufficient to establish frame identity, so it is neither miswritten as H=68, W=120 nor automatically upgraded to a full 4K frame numeric or chain proof.

The original Chinese Markdown reports of r04 contained numerous question marks, with parts of the body text corrupted; r04 subsequently reconstructed the reports from structured JSON using `repair_reports.py`, preserving the corrupted originals as `*.garbled-ascii`, while the pre-declaration body text could not be recovered and is documented only in `PREDECL_RECOVERED_NOTE_ZH.md`. This page relies on the structured JSON and the original records listed below, without repairing source files on its own. [This round's evidence check](../skewer/examples/r04p.evidence.json) preserves the identities and scope.

**Historical tables: retain original r02 verdicts, list r04 classifications separately.** Accepted map refers to the 12×12 map selected by the corresponding plan; existing saved r02 element-by-element and array-payload comparisons are all EXACT/0. r04 classifies the failures across the three historical variants and five fields below as NON_PRODUCTION_VARIANT without rewriting the r02 receipts.

| Field | Original r02 verdict | r04 classification | Original records and accepted map |
|---|---|---|---|
| F16 sread_src | MISMATCH 1,015,808; first diff at (0,0,0,0,4): stored −2, formula 384 | NON_PRODUCTION_VARIANT | [Calibration method and uninitialized record](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/reuse-audit.json#L42), [calibration mode](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/maps/L25-tidx-zero-calibration.json#L18), [accepted plan](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/plans/L25-r3.json#L16); corresponding field in accepted map EXACT/0 (1,048,576 items) |
| F17 sread_src | MISMATCH 3,456; first diff at (0,0,0,1,0): stored 6656, formula 512 | NON_PRODUCTION_VARIANT | [Tool bug record](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/tool-bugs.jsonl#L12), [failed map record](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/maps/L26-lane.r2-position-and-numbering-defects.json#L176), [follow-up log](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/DISCOVERY_LOG_ZH.md#L44), [accepted plan](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/plans/L26-r1.json#L16); accepted map EXACT/0 (1,048,576 items) |
| F19 wload_off | SHAPE_MISMATCH: stored (8,8,32,68), formula (8,8,32,64) | NON_PRODUCTION_VARIANT | [L28 tool bug record](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r02-l27-l28/tool-bugs.jsonl#L2), [accepted plan](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r02-l27-l28/plans/L28-r1.json#L15); accepted map EXACT/0 (131,072 items) |
| F19 xsite_src | SHAPE_MISMATCH: stored (8,8,32,32,4), formula (8,8,32,48,4) | NON_PRODUCTION_VARIANT | Same L28 historical map; accepted map EXACT/0 (393,216 items) |
| F19 xsite_wsrc | SHAPE_MISMATCH: stored (8,8,32,32,4), formula (8,8,32,48,4) | NON_PRODUCTION_VARIANT | Same L28 historical map; accepted map EXACT/0 (393,216 items) |

For the container SHAs, per-field hashes, and element counts of the three accepted maps, see the saved comparisons in [r02 L25](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L4243), [L26](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L4340), and [L28](../../../experiments/mapform-split16-rest-r02-20261027-codex/heldout_receipts.json#L5044) together with [r04 validation](../../../experiments/mapform-split16-r04-20261027-codex/VALIDATION.json). **No receipt proves that the C++ executor read these three specific 12×12 maps**; plan map selection, map-vs.-formula equality, and actual executor provenance are evaluated separately. The r02 failures on these historical variants and the thread_class failures remain preserved and cannot be retroactively changed to PASS.

In F19/F20/F21, thread_class is NOT_PRESENT at 1080, and the frozen single-class-0 hypothesis mismatches on the held-out tables at 1280/2048, 1280/2048, and 768/1024 respectively; the original class tables remain in use. In F22, the independent class candidate is elementwise EXACT against the tables in this round, but remains table-driven as required in this round, and this label agreement cannot be generalized to dynamic class provenance. Zero-byte equality on empty xsite arrays is a **vacuous check**, not evidence of non-empty resource addresses; the original executor still reads the original tables.

### Coordinates, Shapes, and Shared Blocks

Following the physical token height/width H, W and table coordinates (a,y,l,e,b) from the qkv section, the windows of these non-qkv families are unshifted: Gx=ceil(W/8), Gy=ceil(H/8), Q=Gx*Gy. a is the flattened CTA, y is the warp, l is lane 0..31, e is the event of the current field, and b is the transaction byte. Unlike qkv, the CTA flattening order for this group is as follows; for F23, H/W are the pooled input dimensions.

```math
\begin{aligned}
&\mathrm{F16,F20}: &&w_x=a\bmod G_x,\quad w_y=\lfloor a/G_x\rfloor\bmod G_y,\quad z=\lfloor a/Q\rfloor;\\
&\mathrm{F17,F19,F21,F22}: &&b_x=a\bmod(2G_x),\quad w_x=b_x\bmod G_x,\quad w_y=\lfloor a/(2G_x)\rfloor,\quad z=\lfloor b_x/G_x\rfloor;\\
&\mathrm{F23}: &&\text{same as above, replacing }2G_x\text{ with }4G_x;\qquad h=4z+(y\bmod4).
\end{aligned}
```

h is the 64-channel group index and must not be treated as an attention head; F19/F20/F23 have 8 warps, where r=floor(y/4) selects the upper or lower half of a 4×4 spatial block, while r=0 for the remaining families. The CTA count is 2Q for F16/F20 and F17/F19/F21/F22, and 4Q for F23.

Abstract the 4×4 physical block from the qkv section into a common function P_C; each block is 16C bytes, and i is the intra-block offset. V is the inpview planar position for F16/F17, where p is the 16-channel plane and i is the intra-plane byte:

```math
\begin{aligned}
P_C(t_x,t_y,i)&=\begin{cases}16C(t_y(W/4)+t_x)+i,&0\le t_x<W/4,\ 0\le t_y<H/4,\\-1,&\text{otherwise};\end{cases}\\
V(x,v,p,i)&=\begin{cases}16(HWp+vW+x)+i,&0\le x<W,\ 0\le v<H,\\-1,&\text{otherwise}.\end{cases}
\end{aligned}
```

An entire invalid element is −1, and one must not continue adding b or a bypass base address onto the sentinel; −1 in sread denotes zero, while −1 in gstore skips the write. At 512 channels, the block stride is 8192 B, sharing the same block arithmetic as qkv; F23 output uses C=1024. This reuse does not imply that CTA or event orders are identical.


Each field has shape (A,Y,32,event[,byte]); here A is the CTA count of the respective family: 2Q for F16/F17/F19/F20/F21/F22 and 4Q for F23, rather than uniformly carrying over A=4Q from qkv. The event counts in the table are the declared domains; an empty event axis is not a single zero address.

| Family | Y | wload | sread/shared | gstore | xsite (4 B per event) |
|---|---:|---:|---:|---:|---:|
| F16 | 4 | 128 | 64 | 8 | 0 (if stored) |
| F17 | 4 | 64 | 64 | 8 | 96 |
| F19 | 8 | 64 | 32 | 4 | 48 |
| F20 | 8 | 128 | 32 | 4 | 0 |
| F21 | 4 | 64 | 64 | 8 | 96 |
| F22 | 4 | 64 | 64 | 10 | 96 |
| F23 | 8 | 64 | 32 | 4 | 0 |

sread_src is 16 B per event; F22 additionally has 256 shfl_idx events, 64 psel events, and a class field. Extra events in historical tables must not be silently truncated.

### wload_off and Shared Positions

For ordinary 64-event fields, F17/F19/F21/F22 use S=16384; the first 64 events of F16/F20 also take S=16384. Because F23 has 1024 output channels, it uses S=32768:

```math
\mathrm{wload}=S\lfloor e/4\rfloor+2048h+512(e\bmod4)+16l.
```

S is the panel byte count of one K32 basket across all output channels; 2048=64×32 is a single 64-channel group, and 512=32 lanes × 16 B is one transaction round. In F16/F20, the first 64 events follow the ordinary formula, while for the last 64 events we set j=e−64, p=j mod 8, and k=floor(j/8):

```math
\mathrm{wload}=\begin{cases}
262144+16384h+1024k+8192\lfloor p/2\rfloor+512(p\bmod2)+16l,&p<4,\\
393216+16384h+2048k+512(p-4)+16l,&p\ge4.
\end{cases}
```

262144 is the end of the 512×512 panel, each expansion group occupies 131072 B, and 393216 is the start of the contraction segment. For F19, the formula above incurred a shape failure on the r02 historical variant, which r04 classified as NON_PRODUCTION_VARIANT; the accepted map and 4K map are EXACT, and the original failure remains inspectable.

For sread_shared_off, F16/F22 use 512(e mod 16)+16l, while F17/F21 have a period of 24. F19/F20/F23 take p=12/8/12:

```math
\mathrm{shared}=4096\lfloor(e\bmod p)/4\rfloor+512(e\bmod4)+2048r+16l.
```

4096 is the shared-region slice stride, and 2048r selects the upper or lower half; periodic reuse of shared positions does not replace model numeric values.

### sread_src: How Each Family Fetches Input

F17/F21/F22 use the formula below; the r02 historical variant of F17 is FAIL and classified by r04 as NON_PRODUCTION_VARIANT, while its accepted map and 4K map are EXACT; the other two families are EXACT across all bound tables:

```math
t_x=2w_x+(\lfloor e/2\rfloor\bmod2),\quad
t_y=2w_y+(\lfloor e/4\rfloor\bmod2),\quad
i=1024\lfloor e/8\rfloor+512(e\bmod2)+16l+b,\quad \mathrm{sread}=P_{512}(t_x,t_y,i).
```

F19/F20/F23 replace the event spatial bit with the warp half-region, halving the event count:

```math
t_x=2w_x+(\lfloor e/2\rfloor\bmod2),\quad t_y=2w_y+r,\quad
i=1024\lfloor e/4\rfloor+512(e\bmod2)+16l+b,\quad \mathrm{sread}=P_{512}(t_x,t_y,i).
```

F16 inpview splits the lane and byte bits across spatial coordinates and 16-channel planes; the address cannot be treated as a simple base+b. Its r02 historical variant is FAIL and classified by r04 as NON_PRODUCTION_VARIANT, while the accepted map and 4K map are EXACT:

```math
\begin{aligned}
x&=8w_x+4(\lfloor e/2\rfloor\bmod2)+(\lfloor l/4\rfloor\bmod4),\\
v&=8w_y+4(\lfloor e/4\rfloor\bmod2)+\lfloor l/16\rfloor+2(\lfloor b/4\rfloor\bmod2),\\
p&=4\lfloor e/8\rfloor+2(e\bmod2)+\lfloor b/8\rfloor,\quad
i=4(l\bmod4)+(b\bmod4),\quad \mathrm{sread}=V(x,v,p,i).
\end{aligned}
```

### gstore_off, xsite, and the F22 Second Exit

Ordinary gstore events use tx=2wx+(floor(e/2) mod 2) and i=1024h+512(e mod 2)+16l; ty is 2wy+r for 8-warp families and 2wy+floor(e/4) for the rest. The result is the 16 B transaction start in P_512(tx,ty,i); F23 uses P_1024. In F22, the first 8 events follow the ordinary formula, while events 8 and 9 write the pooled second exit in concatenated space, with Wp=4Gx and Hp=4Gy:

```math
\mathrm{pooled}=512HW+8192(w_y(W_p/4)+w_x)+1024h+512(e-8)+16l.
```

Wp/Hp include full padding; this formula closes the address indexing without deriving the pooling numeric algorithm from it.

F17/F21/F22 each have 96 4 B xsite events, of which the first n=32 fetch the bypass; F19 has 48 events in total, of which the first n=16 fetch the bypass; its r02 historical variant had a shape failure, classified by r04 as NON_PRODUCTION_VARIANT, while the accepted map and 4K map are EXACT. For e≥n, xsite_src=−3 indicates the resource and xsite_wsrc gives the resource byte offset; for e<n, xsite_wsrc=−1 and xsite_src uses the relative bypass position below, adding the concatenated base address 512HW when valid and remaining −1 when out of bounds:

```math
\mathrm{xsite\_wsrc}=\begin{cases}
-1,&e<n,\\
262144+128h+16(\lfloor((e-n)\bmod16)/2\rfloor)+4(l\bmod4)+b,&e\ge n.
\end{cases}
```

262144 is the byte length of the 512×512 panel, and 128 is 64 F16 items. The F17 bypass uses inpview: x=8wx+4(floor(e/8) mod2)+(floor(l/4) mod4), v=8wy+4floor(e/16)+2(e mod2)+floor(l/16), p=4h+(floor(e/2) mod4), i=4(l mod4)+b, taking V(x,v,p,i).

The F19/F21/F22 bypass takes P_512. Let q=floor(e/4) and t=e mod4; for the final group q=n/4−1, word=t, whereas for other odd q it takes 3−t and for other even q it takes (−t) mod4:

```math
t_x=2w_x+(\lfloor e/8\rfloor\bmod2),\quad
t_y=\begin{cases}2w_y+r,&\mathrm{F19},\\2w_y+\lfloor e/16\rfloor,&\mathrm{F21/F22},\end{cases}
\quad i=1024h+512(\lfloor e/4\rfloor\bmod2)+16l+4\,\mathrm{word}+b.
```

F16/F20/F23 have no xsite events, and non-empty addresses must not be inferred from empty arrays.

### F22 Exchange, Selection, and Class Candidate

In F22, shfl_idx has 256 events, repeating the formula below every 16 events; psel has 64 events. −2 is the invalid-class sentinel, and 0/1 are the two source-selection values:

```math
\begin{aligned}
\mathrm{shfl}&=(l\bmod4)+8(\lfloor l/4\rfloor\bmod2)+4(\lfloor e/4\rfloor\bmod2)+16(\lfloor e/8\rfloor\bmod2),\\
\mathrm{psel}&=\begin{cases}-2,&\lfloor l/8\rfloor\bmod2=0,\\1-\lfloor l/16\rfloor,&\text{otherwise}.\end{cases}
\end{aligned}
```

The thread_class candidate is EXACT on the F22 held-out tables: let laneclass be 1 when bit 3 of lane is 1, and 2floor(l/16) otherwise; with right-boundary indicator R=[8wx+4≥W] and bottom-boundary indicator B=[8wy+4≥H], the candidate is laneclass+3R+3(1+[W mod8≠0])B. It is a compared class-label formula; the production convention still retains the original tables and does not claim independent dynamic class uniqueness.

### Spot-Check of One Held-Out Window

The [read-only CPU example](../skewer/examples/split16_rest_r04o.py) samples 13 cells from the bound stored table for F22 at H=12, W=20, window (wx,wy)=(2,1), a=8, y=0; the frozen formulas, independent transcription, and stored table agree on 13/13 cells. The [receipt](../skewer/examples/r04o.example.json) contains the container and formula SHAs. In this example, sread event 2 byte 15 and gstore event 2 are both −1; gstore event 8 is 163920; psel at lanes 5/9/25 is −2/1/0 respectively. This spot-check does not replace the saved full-table held-out results.

<a id="layout"></a>
## 1080 N_out Byte Contract and Establishable Logical Axes

In this example, S=60×36=2160 and T=32×20=640. Below are the **logical shapes** supported by parameter roles, upstream/downstream wiring, and known channel widths, without claiming contiguous [HWC](APPENDIX_beginner_glossary.md#g088)/CHW; each physical arrangement still requires reading its own map.

| 1080 named exit | N_out (B) | Established logical role | Axis boundaries |
|---|---:|---|---|
| L25 ffwd | 1,105,920 | S×512 E4, i.e., 60×36×512 | Intra-kernel 2048 gate channels do not materialize as a 2048-channel exit of this kernel |
| L26 ffwd_proj | 1,105,920 | S×512 E4 | Feeds the qkv main path, and is also independently retained for the L28 bypass |
| L27 qkv | 1,105,920 | S×512 E4 exit of fused attention | Not three physical copies of Q/K/V; the eight CPU fields have [closed forms validated on held-out tables](#qkv-closed-form-r04n), while independent native head/query/key logical labels remain UNKNOWN |
| L28 proj | 1,105,920 | Next block's S×512 E4 | 16-step K32 is the arithmetic chain length, not 16 contiguous storage channel groups |
| L56 proj_pool | 1,433,600 | full is 1,105,920 B of S×512; pooled is 327,680 B of T×512 | Return value is sliced by length into two parameter pointers; one cannot divide the total length by S to invent a new channel width |
| L57 final_head | 655,360 | T×1024 E4, i.e., 32×20×1024 | Exit width is known, while internal matrix-slicing axes are not uniquely determined by width |
| L132 outview_wait | 1,105,920 | S×512 E4, read by the B48 upsampling main path | Terminal-view mapping uses dedicated wiring and cannot be replaced by an ordinary proj storage map |

In the execution tables, "outer task × subtask × 32 parallel positions × event" belongs to the fetch/writeback organization. For example, the writeback table of 1080 L25 has shape (80,4,32,8), with each active event writing 16 B; none of 80, 4, 32, or 8 can be identified as spatial, head, or channel axes from their numeric values alone, and valid writebacks/classes are additionally governed by the graph. See [address-table explanation](L3_workspace_map.md#address-maps) and [actual shapes](L3_workspace_map.md#other-maps). Any complete physical-axis decomposition of Q/K/V, AV, and projection inside qkv beyond the bound relationships above remains UNKNOWN.

[CPU Reconstruction / Tables Read Directly] In 1080 L56, pooled physical byte 0 is byte 1,105,920 in the concatenated return value; in [gstore_off](APPENDIX_beginner_glossary.md#g090), the unique event index covering it is (0,0,0,8), and the starting point of that 16 B event is 1,105,920. Those four numbers are, in order, outer task, subtask, parallel position, and write event, and are not named as spatial coordinates. The [script and integer results](../skewer/examples/map_trace_r04f.py) and [SHAs and concrete selectors](../skewer/examples/map_trace_r04f.result.json) can be inspected. The existing seed-provenance check further establishes that the bypass comes from the second input role; independent calibration from that write event to a complete logical spatial/channel rule remains UNKNOWN, so pooled byte 0 cannot be directly identified as the top-left corner. L100 can be traced further to the [established bottleneck source coordinates](L2_06_decoder_bridge.md#byte-trace).

<a id="wiring"></a>
## Intra-Block Diagram: 1080 B23, L25–L28

In the diagram, the external S×512 denotes the logical role; inside the qkv box, shapes are labeled **for one window and per head**, while the physical merging of windows and heads is still specified by the graph. Scales in the diagram indicate only their uses and do not list model coefficients.

~~~mermaid
flowchart TD
    X["L24 pool / current-block X: 60×36×512 E4"] --> F["L25 ffwd_inpview: pre-projection and grouped G / contraction"]
    F --> U["U: 2160×512 E4"]
    U --> FP["L26 ffwd_proj_inpview: 16-step K32 → E4"]
    X --> RF["D8(X) × s_ff → F16 seed"]
    RF --> FP
    FP --> Z["Z: 2160×512 E4"]
    subgraph QKERNEL["L27 qkv: fused projection, norm, and attention"]
        QKV["One window: 16 heads, Q/K/V 64×32 F16 per head"] --> NQ["Q/K norm each; only Q × query scale → E4; V undergoes Q8 directly"]
        NQ --> SC["Per-head 64×64 scores / positive-kernel weights"]
        SC --> AV["Per-head two K32 steps aggregating V → 64×32 E4"]
    end
    Z --> QKV
    AV --> A["Merge / write back A per graph: 2160×512 E4"]
    A --> P["L28 proj: 16-step K32, carrying F16 seed"]
    Z --> RA["D8(Z) × s_att → F16 seed"]
    RA --> P
    P --> Y["Y: 60×36×512 E4 → B24 / L29"]
~~~

<a id="variants"></a>
## Nine Kernel Entries Across Encoder and Decoder

| Variant | Encoder entry | Decoder entry | Differences around the same intra-block wiring |
|---|---|---|---|
| ffwd_inpview | L25 / B23, 1 launch | — | Enters from the TIN pool view; internal FFN executes according to this family's graph |
| ffwd_proj_inpview | L26 / B23, 1 launch | — | Same-block entry is still L24 pool; first-block post-projection brings the main path into the chained view |
| ffwd | L29,33,…,53, 7 launches | L101,105,…,129, 8 launches | Current-block entry → FFN front half; encoder and decoder bind weights and inputs separately |
| ffwd_proj | L30,34,…,54, 7 launches | L102,106,…,130, 8 launches | Post-projection merges in the current-block entry seed; does not take the previous block's bypass |
| qkv | L27,31,…,55, 8 launches | L103,107,…,131, 8 launches | Fused Q/K/V, Q/K norm, and window attention; origin steps through the sequence above block by block |
| proj | L28,32,…,52, 7 launches | L104,108,…,128, 7 launches | Attention output projection, merging in the current block's Z; outputs to the next block's ffwd |
| proj_pool | L56 / B30, 1 launch | — | Dual exits: full is retained as the B39 skip; pooled switches to 32×20 for L57, with spatial reduction following the frozen graph |
| final_head | L57 / B30, 1 launch | — | pooled 512→1024 channel role; output pointer connects to L58, without classification-head semantics |
| outview_wait | — | L132 / B47, 1 launch | After the final projection/residual, switches to the terminal-view graph and hands off to B48/TIN; execution entry is in entry |

The counts are 33 in the encoder and 32 in the decoder, for 65 in total. The two exits of L56 each have their own writeback map; "pool" does not by itself prove standard 2×2 average pooling, nor can pooled be reconstructed from full alone. L57 belongs to [bottleneck](APPENDIX_beginner_glossary.md#g010) width adaptation and is not counted as a ninth window-attention block. Bridge L100 connects B30.full back to the decoder entry—see [added bridge diagram](L2_06_decoder_bridge.md#wiring); for transport between the two sections and ViT, see [repack diagram and 4×4 tiles](L3_workspace_map.md#repack-diagram).

<a id="dual-dag-r04l"></a>
## L56 Dual-Exit and L57 Complete Slicing Contracts (Ranks 159, 164)

Both rows are now updated to **TABLE_DRIVEN_DESCRIBED**: arithmetic, seeds, publication points, and all dependencies are written out in full from the existing graphs, while selection from events to logical coordinates continues to depend explicitly on the tables. Inspectable safe projections are [L56 DAG](../skewer/examples/r04l.L56.dag.json) and [L57 DAG](../skewer/examples/r04l.L57.dag.json), whose generator reads only the legacy JSON and preserves source SHAs; original event address labels are removed, and stores.event is changed to the 0-based index in the original event list. nodes are graph indices rather than hardware registers, A/B/C in matrices are 16/8/4-item arrays referencing those graph nodes, and stores gives the 16 output byte nodes and class for each event with order unchanged. No coefficients were read and the network was not executed.

Each node represents a 32-lane [vector](APPENDIX_beginner_glossary.md#g076). W(site,byte) fetches `weight[wload_off[c,w,l,site]+byte]`; S(site,byte) fetches input according to sread_src, with −1 giving 0 and other negative values rejected. X/XH assemble byte/LE16 per 4 B according to xsite, where −3 selects weights, −1 selects 0, and class −7 marks invalid; E is exact E4→half, Q performs half→E4 [RN-even](APPENDIX_beginner_glossary.md#g059)/[satfinite](APPENDIX_beginner_glossary.md#g062), and K is a declared half constant. SI(site,a) fetches `a[shfl_idx[c,w,l,site]]`; PS(site,a,b) selects a/b according to psel=1/0 and rejects other values (class −2 marks invalid). F add/mul compute RN16(a+b) and RN16(a*b) respectively and cannot merge rounding; when an invalid dependency occurs, publication is forbidden, and unexecuted classes are not extrapolated as valid. [scalar_map.hpp:244–290](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L244).

For the o-th matrix event, row=0..15, col=0..7, k=0..31:

~~~text
la=4*(row%8)+(k%16)//4; ra=row//8+2*(k//16)
lb=4*col+(k%16)//4; rb=k//16
left[k]=value(A[4*ra+k%4])[la]
right[k]=value(B[4*rb+k%4])[lb]
lane=4*(row%8)+col//2; part=2*(row//8)+col%2
M[o,part][lane]=K32(left,right,value(C[part])[lane])
~~~

matrices executes in list order 0..last, and M nodes may read only completed events; each K32 outputs half, and 16 steps cannot be collapsed into a single 512-item real-number sum. Output stores writes 16 B according to class and the gstore_off event index, skipping negative write addresses; if a class write depends on an invalid node, it is rejected. [scalar_map.hpp:293–314](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L293). This formula together with the projected DAG gives the complete program for every output, while the index tables themselves remain non-closed-form.

L56 has 5857 nodes and 512 matrix events, forming 32 chains of 16 K32 steps each; the initial seed is `RN16(E4_to_half(residual)*scale)`, where the residual comes from the second input role; full applies Q8 to these half results. pooled takes four paths a/b/c/d from the final half values in the order `Q8(RN16(RN16(RN16(a+b)+RN16(c+d))*0.25))`, where 0.25 is the algorithmic constant half 0x3400, and one cannot apply Q8 to the four paths before averaging. The SI/PS selections for each path and the edge classes are specified directly by the projected nodes and stores; 78 publication event records span 12 classes. full writes 1105920 B of q2, and pooled writes 327680 B of q3. Outside the CPU graph, it does not independently prove native coordinate attribution as a "standard 2×2" pool.

[CPU Reconstruction / Integer Tables Read Directly] To implement L56, load its map, wiring and release-form contract from the manifest (see [layer index assets](REPRODUCE.md#layer-assets)). Which four final projection halves a pooled byte reads is decided by thread_class, store event, lane and byte number. Label the matrix outputs with an artificial coordinate F[c,w,event,row,col], where M(event,slot,lane) maps to row=lane//4+8·(slot//2), col=2·(lane%4)+slot%2; pooled byte 0 then reads F[0,0,450,0,0], F[0,0,450,1,0], F[0,0,450,4,0], F[0,0,450,5,0] in that order: two pairwise half sums, then their sum, times one quarter, then Q8. At 1080 all 327,680 pooled bytes read exactly four terms, with 0 mismatches. The image (y,x,c) positions of these four terms are not independently calibrated, so this must not be written as a standard 2×2 average pool; boundaries follow only the source value −1 (reads zero) and the concrete class, with no default clamp, reflection or dropping of the last window. [F04 check](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md)

L57 has 2625 nodes and 256 matrix events, forming 16 chains of 16 K32 steps each, with every initial seed equal to [+0](APPENDIX_beginner_glossary.md#g070); it contains only W/S/M/Q/K node types, with no G gate, pooling, or residual. Logical input is 32×20×512 E4 and output is 32×20×1024 E4; the 512 input dimension corresponds to 16 K32 steps, and 1024 is the output channel count. Every byte of the four 16 B publication events is given by the projected stores, and K length cannot be inferred backward from the output width. Source tables, parameter identities, and the node counts above were re-verified from the [existing bindings](../skewer/examples/split16_window_r04d.bindings.json); all provenance statuses are retained in this round.

<a id="evidence"></a>
## How We Know

| Object | Basis and supported scope (one line each) |
|---|---|
| 65 launches and bypasses | [CENSUS](APPENDIX_beginner_glossary.md#g100): actual SHAs of all 65 params in [front bindings](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json), [tail bindings](../../../experiments/parity-cpp-bindings-tail-r01-20260928-codex/s00-bindings-tail.json), and [this round's check record](../skewer/examples/split16_window_r04d.bindings.json) agree, matching the 16-block role wiring |
| Precision and intra-kernel order | CENSUS: [FFN](L3_ffn.md#channels), [norm graphs](L3_norm_nonfinite.md#map-norm), [attention graphs](L3_attention_softmax.md#graph-bindings), and this round's 26-asset SHA check support the named CPU graphs; they do not prove map semantics for arbitrary inputs/geometries |
| 1080 contiguous segment | MEASURED: [legacy B25–B30 results](../../../experiments/parity-gemini-1080-chain-r03-20260922/RESULT_ZH.md#L3) cover the 25 launches L33–L57 as well as L56 dual-exit / L57 wiring, stopping at B30 without crossing into ViT |
| Small-size intra-block gates | MEASURED: [legacy B27–B29 results](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3) are 48 single-segment / intra-block chain comparisons on two public 320×240/[reset](APPENDIX_beginner_glossary.md#g032) samples, not a cross-block continuous chain |
| Later full-frame scope | MEASURED: [M2 record](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) covers all 65 launches on 1080/1440 f0; new 4K [M2](APPENDIX_beginner_glossary.md#g107) numeric runs reach only L99, and configuration census is not used to claim its decoder was newly measured in M2 |
| qkv eight-field addresses/indices | CLOSED_FORMULA, held-out map validation: [new research results](../../../experiments/mapform-split16-qkv-r01-20261027-codex/RESULT_ZH.md); 1080 derivation, with 640×360-class / 1440 / 4K and reference geometries held out; not a new numeric gate |
| Still unknown | Independent native 16-head bias ordering, thread_class of qkv, unclosed fields of other families, general maps / synchronization / [aliasing](APPENDIX_beginner_glossary.md#g092) / lifetime, and uniqueness of internal values are not established by matching exits; legacy MAP_CHECK_FAILED entries retain their named scope |

Complete SHAs, matrix-chain checks, and the sources of the two supplementary diagrams are in the [r04d evidence appendix](APPENDIX_evidence_history.md#split16-window-r04d). [Function-table](APPENDIX_beginner_glossary.md#g074) domains and [nonfinite](APPENDIX_beginner_glossary.md#g069) boundaries continue to follow the [norm contract](L3_norm_nonfinite.md#nf-path) and named M/A1 statuses, without expanding support from this page.

For the four-path channel reduction of the bridge, see the [L100 operator](L2_06_decoder_bridge.md#operator).
