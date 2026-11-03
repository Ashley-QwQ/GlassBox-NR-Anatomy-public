### L0 One Frame (launch L0–L157 / B0–B70)

<!-- beginner-r04m:start frame -->
<a id="beginner-frame"></a>
## Draw the Function First, Then Read the Exact Wiring

[Beginner Simplification; Evidence Follows Main Text Below] The current image, the two motion numbers, the available old image, and the control numbers come in, and the display output remains the same size as the input. The general direction and units of the motion numbers are undetermined. In the diagram, the number cards uniformly write only "how many items per position"; RGB is the three visible color items, while the internal 32 / [512](APPENDIX_beginner_glossary.md#g007) / 1024 items have no known per-channel visual meaning. [Encoding](APPENDIX_beginner_glossary.md#g009) progressively reduces grid density, and decoding progressively restores density; they are computation stages, not the forward and inverse operations of file compression.

~~~mermaid
flowchart TD
    I["Current image: width × height; RGB per pixel"] --> P["Preparation: keep current-frame original image backup, set management flags"]
    M["Motion information: two numbers per position; direction/units?"] --> IN["Input processing: assemble 16 conditioning items → 32 items per position"]
    H["Available old image"] --> IN
    C["Control numbers"] --> IN
    P --> IN
    IN --> E1["Encoding tier 1: 32 items per position"] --> E2["Encoding tier 2: 64 items per position"] --> E3["Encoding tier 3: 128 items per position"] --> E4["Encoding tier 4: 256 items per position"]
    E4 --> S["Eight window blocks: 512 items per position"] --> SHR["Switch to sparser grid? Spatial pairing undetermined; 1024 items per position"]
    SHR --> G["Eight all-position blocks: 1024 items per position"] --> BR["Reconnect bypass, restore denser grid? Full spatial operator undetermined; 512 items per position"]
    BR --> SD["Eight window blocks: 512 items per position"] --> D4["Densifying tier 1: 256 items per position"] --> D3["Densifying tier 2: 128 items per position"] --> D2["Densifying tier 3: 64 items per position"] --> D1["Densifying tier 4: 32 items per position; width and height still each half of internal canvas"]
    D1 --> T["Tail end: reconnect entry numbers, predict color correction; conditionally fetch old color separately for blending"]
    IN -->|"① Entry full-density numbers, 32 items"| T
    E1 -->|"② Same-tier numbers, 32 items"| D1
    E2 -->|"③ Same-tier numbers, 64 items"| D2
    E3 -->|"④ Same-tier numbers, 128 items"| D3
    E4 -->|"⑤ Same-tier numbers, 256 items"| D4
    S -->|"⑥ Pre-bottleneck numbers, 512 items"| BR
    I --> T
    M --> T
    H --> T
    C --> T
    T --> N["Current-frame new color state"] --> SAVE["Save as old image for next frame"]
    N --> SHOW["Display color adjustment, then blend with current-frame backup by strength"] --> O["Display image: still input width × height"]
    P -->|"Original image backup: separate path, not counted among the six internal bypasses"| SHOW
    C --> SHOW
    SAVE -. "Next frame" .-> H
~~~

The six internal [bypasses](APPENDIX_beginner_glossary.md#g016) are remembered as ① entry → tail end, ②–⑤ the four encoding tiers → their corresponding densifying tiers, and ⑥ pre-[bottleneck](APPENDIX_beginner_glossary.md#g010) → bridge; the original image backup is counted separately as a seventh saved connection. Internal grid thinning and [padding](APPENDIX_beginner_glossary.md#g085) do not change the final display width and height. Keep each position's number card in mind first, then expand [the two local residuals of a single block](L1_00_one_block_primer.md#two-residuals); local [residuals](APPENDIX_beginner_glossary.md#g017) and the cross-stage bypasses here are wiring at two different scales.

The bridge can first be drawn in two layers: **known** is that the [partial sums](APPENDIX_beginner_glossary.md#g050) of four channel groups are added in a fixed order before reconnecting the bypass; **undetermined?** is the full spatial restoration relationship, which cannot be drawn as proven [nearest-neighbor](APPENDIX_beginner_glossary.md#g021) [interpolation](APPENDIX_beginner_glossary.md#g020) or a four-point [mean](APPENDIX_beginner_glossary.md#g044). [Exact bridge diagram](L2_06_decoder_bridge.md#wiring)

Reading depth: [L0](APPENDIX_beginner_glossary.md#g081) (full frame).<br>Execution numbering: default [launch](APPENDIX_beginner_glossary.md#g080) L0–L157.<br>[Logical block](APPENDIX_beginner_glossary.md#g036) numbering: B0–B70. The original exact diagram, value domains, parameters, and comparison scopes are retained below; read the "differences from textbook models" box once you have the basics. For the three-frame [history](APPENDIX_beginner_glossary.md#g024) timeline, see the [primer page](L1_00_history_primer.md#timeline); the minimum required memory scope of the [workspace](APPENDIX_beginner_glossary.md#g082) remains [undetermined](L1_00_history_primer.md#workspace-memory).
<!-- beginner-r04m:end frame -->

[Object and Method](L0a_object_method.md) · [Determinism and Reproducibility](L0b_determinism.md) · [Full Skewer Index](INDEX.md)

[Weight Organization and Stage Byte Accounting](L2_weights_layout.md) · [Cross-Architecture Comparison](L4_cross_arch.md) · [Public v2 Reproduction](REPRODUCE.md)

> **What It Is Not / Differences from Textbook Models (Current Reconstruction and Observed Wiring)**
>
> - Same-size W×H output; the three measured tiers pad only the internal canvas height, [mirroring](APPENDIX_beginner_glossary.md#g030) to fetch colors after 1080→1152. [Boundary sampling](L3_b0_input.md#channels)
> - Trunk blocks containing [attention](APPENDIX_beginner_glossary.md#g039) run [FFN](APPENDIX_beginner_glossary.md#g037) first and attention second. [Feed-forward wiring across families](L3_ffn.md#channels)
> - No block-entry LayerNorm; only post-[projection](APPENDIX_beginner_glossary.md#g038) Q/K undergo per-head uncentered sum of squares and [RSQ](APPENDIX_beginner_glossary.md#g072), while V does not. [Q/K normalization](L3_norm_nonfinite.md#norm32)
> - G is a single-input clamped piecewise polynomial, not replaced by [GELU](APPENDIX_beginner_glossary.md#g046)/SiLU or a two-branch gate. [Gate function](L3_ffn.md#gate)
> - attention does not compute [exp](APPENDIX_beginner_glossary.md#g047) or row maxima; [ViT](APPENDIX_beginner_glossary.md#g014) aggregates V with [Q8](APPENDIX_beginner_glossary.md#g061)(w) first and multiplies by the reciprocal afterward. [Scores and publication](L3_attention_softmax.md#attention-softmax)
> - Residuals preserve the actual interfaces of [matrix](APPENDIX_beginner_glossary.md#g051) [seed](APPENDIX_beginner_glossary.md#g042) / first slice and ordered [half](APPENDIX_beginner_glossary.md#g054) merging, rather than being uniformly moved to real-number addition after the dot product. [Residual rounding](L3_ffn.md#residual)

Current color id1, [motion vector](APPENDIX_beginner_glossary.md#g023) MV id3, valid history id6, and control values pass through encoder → bottleneck → decoder to generate [state](APPENDIX_beginner_glossary.md#g002) id9; L156 saves it as next-frame history, and L157 composites it with the [color base](APPENDIX_beginner_glossary.md#g003) id10 by [intensity](APPENDIX_beginner_glossary.md#g004) into the same-size display output id2. The overall visual purpose remains unknown; see [Object and Project Terms in the Index](INDEX.md).

[Verification Record / Display Boundary] Named controls alter the output, but there is not yet a complete image/difference set here that [binds](APPENDIX_beginner_glossary.md#g103) the current object identity, the same input/history state, and variations of the two controls; a visual purpose cannot be inferred from scattered PNGs. For known numeric effects, see [B0 Conditioning Channels](L3_b0_input.md#channels) and [Display Blending](L3_b70_history_output.md#postprocess); for the identity and control conditions still missing for visual display, see the [evidence appendix](APPENDIX_evidence_history.md#r04f-review-resolution).

In the diagram, spatial axes are written uniformly as **width × height × channels** with [batch=1](APPENDIX_beginner_glossary.md#g086); [E4](APPENDIX_beginner_glossary.md#g055)/F16 are E4M3/binary16. Dimensions are taken directly from the 1080 instance in the [INDEX extent table](INDEX.md#shape-and-workspace-notation); they represent only logical shapes at stage boundaries, and internal hidden axes and physical layouts are not derived from the diagram.

~~~mermaid
flowchart TD
    Input["Inputs: id1 1920×1080×4 F16; id3 1920×1080×2 F16; valid id6 1920×1080×4 F16; controls as params scalars, no spatial axes"]
    Prepare["Pre-Graph Preparation L0–L1: id10 1920×1080×4 F16; control region uint32, logical tensor axes not applicable"]
    B0["L2 / B0: 1920×1152×16 F16 conditioning → full 1920×1152×32 E4; pool 960×576×32 E4"]
    C1["TIN 1h L3–L6: full 960×576×32 E4; pool 480×288×64 E4"]
    C2["TIN 2h L7–L10: full 480×288×64 E4; pool 240×144×128 E4"]
    C3["TIN 4h L11–L16: full 240×144×128 E4; pool 120×72×256 E4"]
    C4["TIN 8h L17–L24: full 120×72×256 E4; pool 60×36×512 E4"]
    SplitEnc["split16 Encoder L25–L57: B30.full 60×36×512 E4; pooled 32×20×512 E4; L57 32×20×1024 E4; intra-kernel hidden axes not independently confirmed"]
    ViT["ViT L58–L99: 32×20×1024 E4→640 token×1024 E4→32×20×1024 E4; T=P=640"]
    Bridge["Bridge L100 / B39: 60×36×512 E4"]
    SplitDec["split16 Decoder L101–L132: 60×36×512 E4 outview; intra-kernel hidden axes not independently confirmed"]
    H4["TIN L133–L140: 120×72×256 E4 outview"]
    H3["TIN L141–L146: 240×144×128 E4 outview"]
    H2["TIN L147–L150: 480×288×64 E4 outview"]
    H1["TIN L151–L154: 960×576×32 E4 outview"]
    B70["B70 L155: main reused by floor(x/2),floor(y/2), merged with B0.full; id9 1920×1080×4 F16"]
    History["L156: id9→id6 1920×1080×4 F16"]
    Display["L157: process id9, then blend with id10 by intensity → id2 1920×1080×4 F16"]
    Input --> Prepare --> B0 --> C1 --> C2 --> C3 --> C4 --> SplitEnc --> ViT --> Bridge --> SplitDec --> H4 --> H3 --> H2 --> H1 --> B70
    Input --> B0
    Input --> B70
    SplitEnc -- "B30.full 60×36×512 E4 skip" --> Bridge
    C4 -- "B22.full 120×72×256 E4 skip" --> H4
    C3 -- "B14.full 240×144×128 E4 skip" --> H3
    C2 -- "B8.full 480×288×64 E4 skip" --> H2
    C1 -- "B4.full 960×576×32 E4 skip" --> H1
    B0 -- "B0.full 1920×1152×32 E4 skip" --> B70
    B70 --> History
    B70 --> Display
    Prepare -- "id10 1920×1080×4 F16" --> Display
    History -. "Next-frame history" .-> Input
~~~

1080→1152 is the internal canvas height given by [params](APPENDIX_beginner_glossary.md#g083) in this instance, with the extra 72 rows used for internal computation; the output is still cropped to 1920×1080. It does not stretch the image proportionally, nor can the root canvas height be derived from a single ceil(H/8) formula. B0 reflects color/MV by ty=y<H?y:2H−2−y: y=1080 reads row 1078, and y=1151 reads row 1007; noise still uses unmirrored internal coordinates. The [B0 mirroring contract](L3_b0_input.md#channels) specifies this finite scope, and padding at subsequent tiers follows the respective [window](APPENDIX_beginner_glossary.md#g015) [contracts](APPENDIX_beginner_glossary.md#g101).

The half-resolution main path in B70 is reused by coordinates rather than reshaped into full resolution merely because the byte counts match; for cropping from the internal canvas to the valid image region, see [B70](L3_b70_history_output.md#b70-network). The off-graph workspace also holds F16/[F32](APPENDIX_beginner_glossary.md#g056) scratch buffers and control words, which are not drawn as fictitious channels. Earlier single-sample direct skip controlled comparisons cover only the four [TIN](APPENDIX_beginner_glossary.md#g011) encoder-decoder connections; B0→B70 follows the current source wiring separately.

## Pixel Value Domains and Representation Transforms

| Location | Representation and value domain | Transform |
|---|---|---|
| id1 / id10 | F16 color; understood as [0,1] in this instance, with no uniform [clamping](APPENDIX_beginner_glossary.md#g049) at the entry | Current color and base are read bitwise; [alpha](APPENDIX_beginner_glossary.md#g026) does not participate in network color input |
| B0 conditioning | F16; noise, color, fixed constants, and control components are [defined separately](L3_b0_input.md#channels) | Current color first subtracts 0.5 and then multiplies by gain, with each step [published](APPENDIX_beginner_glossary.md#g091) in half. Only when ignoring rounding do color∈[0,1] and gain≥0 give the ideal bound ±gain/2; the actual F16 result must be computed with two roundings |
| Trunk / skip | E4M3 finite codes lie in [−448,448], with separate guards on [nonfinite](APPENDIX_beginner_glossary.md#g069) paths | Each [K32](APPENDIX_beginner_glossary.md#g065) first publishes F16 and applies Q8 at the exit; this does not mean all intermediate half values also lie in that interval |
| B70 current color | F32 encoded∈[0,1] | Ideal real-number form color+8×scale×dh; actually computed via three [FMAs](APPENDIX_beginner_glossary.md#g063) and clamping |
| B70 history and id9 | F32 blending → [RZ16](APPENDIX_beginner_glossary.md#g060); factor∈[0,1] | The [5-tap](APPENDIX_beginner_glossary.md#g029) filter can have negative sidelobes; there is no uniform [0,1] clamp after blending, so a fixed color range cannot be fabricated for id9 |
| L157→id2 | F32 color chain composited with base → clamp to [0,1] → RZ16, alpha=1 | Gain/curve, two rounds of [HSL](APPENDIX_beginner_glossary.md#g033), and intensity each preserve their original operation boundaries |

For concrete numeric values, see [B70 worked substitution](L3_b70_history_output.md#b70-mix); for format boundaries, see the [F32 leaf](L4_fp32_ftz.md#sites).

<a id="textures"></a>
## Quick Reference: Six Textures and Controls

[Native Behavior / CPU Reconstruction Wiring] The default route records six [texture](APPENDIX_beginner_glossary.md#g027) slots with non-contiguous numbering; the remaining numbers are not bound as registered textures on this route and cannot be guessed to be masks from the unused numbers. [Six-POST](APPENDIX_beginner_glossary.md#g105) refers to the valid regions of the six textures below after a specified launch, not six different image tasks.

| ID | [Role](APPENDIX_beginner_glossary.md#g084) | Format / size | Written by | Read by |
|---|---|---|---|---|
| id1 | Current color | [RGBA16F](APPENDIX_beginner_glossary.md#g028) / W×H | [caller](APPENDIX_beginner_glossary.md#g096) | L0, L2, L155 |
| id2 | Display result | RGBA16F / W×H | L157 | caller |
| id3 | Motion vector | RG16F / W×H | caller | L2, L155 when history is valid |
| id6 | Previous-frame history | RGBA16F / W×H | Previous-frame / current-frame L156 | L2, L155 when history is valid |
| id9 | Current temporal state | RGBA16F / W×H | L155 | L156, L157 |
| id10 | Display base | RGBA16F / W×H | L0 | L157 |

| params role | Consumption site and known effect |
|---|---|
| [style](APPENDIX_beginner_glossary.md#g005) / tone / structure | B0 channels 10/11/12; fed into the network via the half adapter |
| [p5](APPENDIX_beginner_glossary.md#g032) | When p5 is true, structure=1 and the two [masks](APPENDIX_beginner_glossary.md#g006) are taken from the control buffer; reads its own id6 when history is valid—see [B0](L3_b0_input.md#p5-candidates) |
| Native frame counter, mode, history/MV handles | Noise hashing and valid-history contract; reset cannot merely change the frame counter |
| intensity | L157 display blending; does not add a B0 input channel |
| Coordinate scales and offsets | B0/B70 sampling transforms; values and formats follow actual params and are not replaced by screen resolution |

For hexadecimal byte offsets of the fields, see [B0](L3_b0_input.md#channels) and [B70](L3_b70_history_output.md#postprocess); knowing these numeric effects does not mean all host API field names are known.

<a id="params"></a>
## params Constant Buffer: Known Offset Subset

All offsets are **hexadecimal byte offsets**, and each row applies only to the listed launches; this is not a complete host ABI. The table summarizes only fields already given in the existing main text and bindings, without inferring other offsets from names.

| Launch family / known length | Offset, type, and meaning | Existing basis |
|---|---|---|
| L1 clear / 16 B | CB+0x00 ([u64](APPENDIX_beginner_glossary.md#g057)) workspace base address; CB+0x08 (u32) word count to fill | [Workspace clear](L3_workspace_map.md#clear) |
| B0 / 264 B | CB+0xac (f32)/CB+0xb0 (f32)/CB+0xb4 (f32) are tone/structure/style; CB+0xb8 (f32)/CB+0xbc (f32) are used for p5 determination | [16 channels](L3_b0_input.md#channels) |
| B0 / same as above | CB+0xa0 (f32)/CB+0xa4 (f32) are MV scales; CB+0xc4 (f32) generates input gain; CB+0xc8 (u32) frame word | [Coordinates](L3_b0_input.md#coordinates) |
| B0 / same as above | CB+0xc0 (u32) history mode; CB+0x08 (u64)/CB+0x10 (u64) are history/MV handles; CB+0xd8 (u64)/CB+0xf8 (u64) are [full](APPENDIX_beginner_glossary.md#g018)/pool pointers | [Guards](L3_b0_input.md#guards), [publication](L3_b0_input.md#publish) |
| [split16](APPENDIX_beginner_glossary.md#g013) ffwd / qkv / final_head | CB+0x00 (u64) input, CB+0x08 (u64) output; other fields are not extrapolated from identically shaped kernels | [Per-launch bindings](../skewer/examples/split16_window_r04d.bindings.json) |
| split16 ffwd_proj / proj / L132 | CB+0x00 (u64) main path, CB+0x08 (u64) intra-block residual, CB+0x10 (u64) output; L56 additionally has CB+0x18 (u64) pooled output | [Role bindings](../skewer/examples/split16_window_r04d.bindings.json) |
| L58/L99 [repack](APPENDIX_beginner_glossary.md#g019) / 24 B | CB+0x00 (u64)/CB+0x08 (u64) input/output; CB+0x10 (u32)/CB+0x14 (u32) 2D rows/cols | [Repack acceptance domain](L3_workspace_map.md#repack-domain) |
| ViT attention | CB+0x00 (u64)/CB+0x08 (u64)/CB+0x10 (u64)/CB+0x18 (u64) are Q/K/V/output respectively; actual layout is not guessed from pointer order | [Role offsets](L3_workspace_map.md#regions) |
| L100 bridge | CB+0x00 (u64)/CB+0x08 (u64)/CB+0x10 (u64) main path / skip / output | [Existing parameter bindings](../skewer/examples/split16_window_r04d.bindings.json) |
| B70 / 184 B | CB+0x30 (f32) predicted color correction scale; CB+0x94 (f32)/CB+0x8c (f32)/CB+0x9c (f32) and other-axis CB+0x98 (f32)/CB+0x90 (f32)/CB+0xa0 (f32) construct MV coordinates | [Color](L3_b70_history_output.md#b70-current), [history coordinates](L3_b70_history_output.md#b70-temporal) |
| B70 / same as above | CB+0xa4 (f32)/CB+0xa8 (f32) history center transform; the history point is then transformed by CB+0x7c (f32)/CB+0x74 (f32)/CB+0x84 (f32) and other-axis CB+0x80 (f32)/CB+0x78 (f32)/CB+0x88 (f32) | [Temporal formulas](L3_b70_history_output.md#b70-temporal) |
| L157 / 376 B | CB+0x120 (f32) display strength I; CB+0x144 (f32)/CB+0x14c (f32)/CB+0x150 (f32)/CB+0x154 (f32) are a/b/c/δ | [Curve and scalars](L3_b70_history_output.md#post-curve), [display blending](L3_b70_history_output.md#intensity) |

## What Is Retained Between Two Frames

| Object | Behavior on frame t | Source on frame t+1 | Effect of reset |
|---|---|---|---|
| id1 / id3 / params | caller refreshes current color, MV, controls, and native frame word | Refreshed again by caller; native network intermediates cannot be injected as CPU prediction inputs | API reset is initiated by the native host; the CPU consumes the corresponding parameter contract without calling that API |
| Explicit API reset | Native host initiates reset via API; CPU reads the corresponding reset params | After new id9 replaces history, normal frames resume carry according to the profile | Does not call the API in place of CPU prediction, nor equate API reset with clearing the entire workspace |
| Parameter-change-triggered reset | Old history is not read; conditioning channels 7..9 repeat the current transformed RGB | Counter and handles update according to the reset contract | The new state generated in this frame overwrites id6 at the end of the frame |
| p5 history conditioning | Own id6 is [reprojected](APPENDIX_beginner_glossary.md#g025) by current id3 into 7..9; structure=1, masks taken from CB | Next frame continues reading from its own state | reset turns off history consumption |
| id9→id6 | B70 writes id9, and L156 copies id6 across valid rows | The id6 saved this time is read by next-frame B0/B70 | Captured reset profile makes this frame skip old history; no need to clear id6 first, as the new id9 at the end replaces it |
| id10 / id2 | Current base / current display result | Default route rewrites base and display; id2 does not serve as temporal history | The 156-launch route uses its own tail contract; see table below |
| workspace / texture buffers | CPU own-state chain retains the full buffer state, overwriting launch by launch; [CumWrites](APPENDIX_beginner_glossary.md#g093)(L) is the cumulative declared write set | Continues from the previous frame's CPU state; read sets are audited separately per launch | Do not describe reset as zeroing the entire workspace; [full-domain](APPENDIX_beginner_glossary.md#g111) independence from arbitrary initial values is not yet proven |
| Noise and function assets | Re-hashed from coordinates and the actual params frame word; assets are immutable | No recurrent [RNG](APPENDIX_beginner_glossary.md#g075) state; tables are loaded per launch and carry no per-pixel random state | Native frame word can return to 0; absolute video frame number and noise counter are distinct |

p5 alters the conditioning channels and history reading, and S157 executes the color chain under exact tuples; see [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).

## The 158 and 156 Routes

The 156-launch branch omits the base backup and separate display processing; see [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate).

| Route | Known trigger | Launches and tail stage | Current interpretation boundary |
|---|---|---|---|
| Default 158 | Default named params in this skewer | L0–L157; L0 saves id10; L155 is default post_block, L156 copies, L157 postprocesses and blends | 158 is the launch count, while logical blocks are B0–B70; see INDEX for per-stage counts |
| 156 | Named branch with tone=0 or style=0 | Omits default L0 and L157; tail writes id2 and then copies id2→id6, binding only 1/2/3/6 | Display and history share the same tail result |

- Numeric rules: image state / display RGB is finally converted to F16 via RZ with alpha=1; internal matrices, half operations, quantization, and out-of-domain rejections are still preserved per launch—see [Computation Conventions](INDEX.md#computation-conventions).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) (stages, shapes, source wiring), MEASURED / CONTROLLED (named chains and reset controls), INFERRED (block-level semantics); [ARCH §1](../../../ARCHITECTURE_V3_ZH.md#1-全景), [tail variants](L3_b70_history_output.md#variants), [history contract](L3_b70_history_output.md#loop).
- Next down: [All Ten L1 Slices](INDEX.md) → L2 family links on each L1 page.

## 1080 Logical Matrix Scale

Here [MAC](APPENDIX_beginner_glossary.md#g077) denotes one [scalar](APPENDIX_beginner_glossary.md#g076) multiply-add and GMAC=10⁹ MAC; counts follow only the written matrix dimensions and valid [query](APPENDIX_beginner_glossary.md#g040) positions using the 1920×1152 internal canvas, not [GPU](APPENDIX_beginner_glossary.md#g078) instructions, repeated CPU execution work, timing, or bandwidth measurements. The [weights](APPENDIX_beginner_glossary.md#g079) column gives net matrix-slot bytes (1 B per E4 item, 2 B per F16 item in the B0 adapter and B70 tail), excluding biases, scales, and alignment, and does not claim to be a unique physical weight span.

| Stage | Net matrix-slot bytes | Linear GMAC | QK+AV GMAC |
|---|---:|---:|---:|
| B0 | 13,312 | 28.311552 | 9.059697 |
| TIN Encoder | 6,367,232 | 130.233139 | 19.251855 |
| split16 Encoder (known subtotal) | 8,388,608 | 18.119393 | 1.132462 |
| ViT | 100,663,296 | 64.424509 | 6.710886 |
| L100 | 524,288 | 1.132462 | 0.000000 |
| split16 Decoder (known subtotal) | 8,388,608 | 18.119393 | 1.132462 |
| TIN Decoder | 6,367,232 | 130.233139 | 19.251855 |
| B70 | 12,544 | 27.391427 / 27.462205 | 9.059697 |

B0 includes the 16→32 adapter; TIN follows the actual single-head / grouped FFN and encoder/decoder projections; ViT follows the 8 blocks of 1024→4096→1024, QKV, and projection; the two values in the B70 linear column are for the three reset predicted values and the four predicted values when history is valid, respectively. Each valid window query uses 64 keys; discarded shifted-window queries and repeated computations in data-driven execution are not mixed into this logical accounting. Decimals are rounded for display only; exact integer values are in the [actual code and dimension calculation](../skewer/examples/anatomy_r04i.py) and [results](../skewer/examples/anatomy_r04i.result.json).

The two split16 rows list only the known subtotals for the 8-block FFN and 512→512 output projection; the full MKN of QKV projections, the extra dual-exit projections in the encoder, and the internal matrices of L57 have not all been confirmed in closed form, so full-network MACs and weight allocations are not filled in. This table does not fill in [UNKNOWN](APPENDIX_beginner_glossary.md#g104) items as a standard dense [Transformer](APPENDIX_beginner_glossary.md#g012). The WEIGHTS_HT resource metadata is 147,695,410 B (see [identity metadata](../../../WEIGHTS_IDENTITY.json)); the resource container and the runtime matrix slots here follow different accounting conventions and cannot be added together.
