# L3.workspace-map: Workspace, Padding Zero-Writes, and Bidirectional repack

<!-- beginner-r04m:start intro -->
<a id="beginner-storage"></a>
[Synthetic Storage Illustration] The same group (a,b,c,d) can be placed in two rows as (a,b)/(c,d) or placed in storage as (a,c,b,d); [rearrangement](APPENDIX_beginner_glossary.md#g019) only swaps the boxes, and once interpreted they are still the same four numbers. The actual rule is not an arbitrarily chosen arrangement, and must follow the [contract](APPENDIX_beginner_glossary.md#g101) of this instance. When reading the diagrams, separate three boxes: "where to fetch numbers from → what arithmetic to perform → where to write numbers to".

~~~text
Logically valid cells:  ■ ■     Actually allocated cells: ■ ■
                        ■ ■                               ■ ■
                                                          □ □  Extra padded cells
~~~

□ may genuinely be written with zeros and read later, so it cannot automatically be treated as garbage; internal [padding](APPENDIX_beginner_glossary.md#g085) also does not mean the displayed image becomes larger. The [workspace](APPENDIX_beginner_glossary.md#g082) holds both intermediate numbers and management flags, and the minimal cross-frame required set of old bytes remains [undetermined](L1_00_history_primer.md#workspace-memory). Beginners should first read the meanings of [roles](APPENDIX_beginner_glossary.md#g084) and rearrangement; the address tables, write sets, zero-overwrites, and [completion flags](APPENDIX_beginner_glossary.md#g091) below are the expert verification layer.
<!-- beginner-r04m:end intro -->

[Full Skewer Index](INDEX.md) · Parent level: [Preparation](L2_01_prepare.md), [split16](L2_04_split16_encoder.md), [ViT](L2_05_vit.md), [Bridge](L2_06_decoder_bridge.md) · Expanded arithmetic: [Matrix Multiplication](L3_qmma_e4m3.md), [attention](L3_attention_softmax.md), [B0 Dual Exits](L3_b0_input.md#publish)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| Span(role) | Byte interval of a role relative to this workspace base address |
| [WriteSet](APPENDIX_beginner_glossary.md#g093)(L), CumWrites(L) | Single-[launch](APPENDIX_beginner_glossary.md#g080) declared write set and [cumulative declared write set](APPENDIX_beginner_glossary.md#g105); see the appendix for the checker protocol |
| Read_ws, I_decl | Read set with actual provenance evidence, and declared input-role intervals |
| π, chunk | 12-bit permutation of repack, and 4-byte transfer unit |

<a id="workspace-map"></a>
<a id="regions"></a>
### L3.workspace-map.regions Workspace Bound by Role and Point in Time (L0–L157)

- What it is: A byte allocation carried across launches, holding numeric [tensors](APPENDIX_beginner_glossary.md#g076), synchronization flags, padding, and reused intervals.
- Input → output: Current-frame configured b, N, [params](APPENDIX_beginner_glossary.md#g083), and role [descriptors](APPENDIX_beginner_glossary.md#g088) → Span(role); the same offset can serve different roles in different launches.
- How it is computed:
  ~~~text
  1. N(G)=byte count of the registered allocation; b is taken from CB+0x00 (u64) of L1 in the same instance.
  2. o(role,L)=pointer for that role in params − b + intra-descriptor offset.
  3. n(role,G)=physical element count of that role × bytes per element, or its explicit side-effect length.
  4. Span(role,L)=[o,o+n); requires 0≤o≤N and 0≤n≤N−o.
  5. Role data are read according to the layout of this run; the same logical shape does not guarantee contiguous channels in memory.
  6. The union across roles gives the declared input / output intervals; across points in time, role lengths cannot simply be summed as N.
  7. N≥max(o+n); whether it equals the union length exactly requires checking cumulative coverage separately.
  ~~~
- Numeric rules: These are byte-address and length operations with no [floating-point](APPENDIX_beginner_glossary.md#g056) rounding; numeric values inside the workspace are still interpreted according to their primitive formats. Capacity is [bound](APPENDIX_beginner_glossary.md#g103) by fixed-geometry allocation records, and the current source code gives no [closed form](APPENDIX_beginner_glossary.md#g020) for the [host](APPENDIX_beginner_glossary.md#g096) allocator over arbitrary W,H; N cannot be fitted with a fixed B/pixel ratio.
- Why it is computed this way: Allows different stages to reuse buffers and hand off data and completion [state](APPENDIX_beginner_glossary.md#g091) within the same allocation; a globally optimal reuse policy has not been independently reconstructed.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100), [entry.cpp:41–48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L41), [geometry.hpp:35–50](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/geometry.hpp#L35); for the three-tier sources / formulas, see [FIXED_GEOMETRY:36–53](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/FIXED_GEOMETRY_ZH.md#m-g004workspace-pointeroffset-与跨度) and [native_launch_facts.json](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json).
- Next down: [Geometry and Role Sizes](#geometry), [L1](#clear), [Reads, Writes, and CumWrites(L)](#write-sets), [Address Tables](#address-maps), [Side Effects](#release).

<a id="geometry"></a>
### L3.workspace-map.geometry Formulas for Three-Tier Capacities and Physical Extents

- What it is: Separates image dimensions, per-tier spatial padding, and sequence padding, scaling by actual roles.
- Input → output: Admitted Wn,Hn and per-role parameters → spatial tensor byte counts, T/P, and fixed per-tier allocation N.
- How it is computed:
  ~~~text
  1. (W0,H0)=(Wn,Hn); both axes halve and pad step by step using n_(r+1)=4×ceil(n_r/8).
  2. T=W6×H6; P=32×ceil(T/32).
  3. Byte count of a spatial E4 role=Wr×Hr×C; F16 multiplies that by 2.
  4. B0.full=32WnHn; B0.pool=32(Wn/2)(Hn/2).
  5. One 1024-channel physical role in ViT=1024P; expanded role=4096P.
  6. repack logical transfer=1024T; L58's extra zero-writes=1024(P−T).
  7. Role start still takes the params pointer; capacity N follows the registered values in the table below, not a simple sum of the sizes above.
  ~~~
- Numeric rules: Spatial valid height, physical height, and sequence P are distinct boundaries; the extent recurrence above follows the admitted geometries of this corpus and does not claim to be the host allocation formula for arbitrary images.
- Why it is computed this way: Each stage organizes storage according to its own tiling granularity; multiple alignment granularities keep N from maintaining a fixed ratio to WH.
- How we know: CENSUS / INFERRED, [INDEX shape chain](INDEX.md#shape-and-workspace-notation), [B0 source code:63](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L63), [repack.cpp:81–84, 137–150](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L137); capacities come from [GEO RESULT:11](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/RESULT_ZH.md#L11).
- Next down: [Logical Rows / padding](#padding), [repack](#repack).

| Instance | W×H | Wn×Hn | H6×W6; T / P | N (B) | B0 [full](APPENDIX_beginner_glossary.md#g018) / pool (B) | One physical 1024-[channel](APPENDIX_beginner_glossary.md#g007) role in [ViT](APPENDIX_beginner_glossary.md#g014) (B) |
|---|---|---|---|---:|---|---:|
| 1080 | 1920×1080 | 1920×1152 | 20×32; 640 / 640 | 212,519,936 | 70,778,880 / 17,694,720 | 655,360 |
| 1440 | 2560×1440 | 2560×1472 | 24×40; 960 / 960 | 340,722,688 | 120,586,240 / 30,146,560 | 983,040 |
| 4K | 3840×2160 | 3840×2176 | 36×60; 2160 / 2176 | 763,062,272 | 267,386,880 / 66,846,720 | 2,228,224 |

Taking L62 at 1080 as a concrete layout: CB+0x00 ([u64](APPENDIX_beginner_glossary.md#g057)) / CB+0x08 (u64) / CB+0x10 (u64) / CB+0x18 (u64) bind Q / K / V / output respectively; their offsets relative to b are 181,718,016 / 183,028,736 / 182,373,376 / 183,684,096 respectively, with 655,360 B each. In address order, however, they are **Q→V→K→output**, so contiguous memory order cannot be guessed from parameter arrangement. All three tiers read their own pointers via the same Span(role) formula, and 1080 offsets cannot be applied to 1440 / 4K. [ARCH 0.7 §2.4](../../../ARCHITECTURE_V3_ZH.md#24-workspace-布局).

<a id="clear"></a>
### L3.workspace-map.clear Fixed-Instance Footprint of L1

- What it is: Initializes the control region in the workspace prefix; "clear" here writes 0xFF.
- Input → output: 16 B params of L1 → contiguous interval at the start of WS set to 0xFF, with the remaining bytes preserved.
- How it is computed:
  ~~~text
  1. Require params to be exactly two qwords.
  2. b=CB+0x00 (u64); count=U32(CB+0x08 (u64)); n=4×count.
  3. For i=0..count−1: write four 0xFF bytes at b+4i.
  4. WriteSet(1)=[0,n), Read_ws(1)=∅.
  5. Register this write range; do not zero-clear the whole workspace outside n.
  ~~~
- Numeric rules: Each 32-bit slot is 0xffffffff; interpreted as a signed integer it is −1, not floating-point −1. Both 00 / A5 initial states are overwritten with FF within this prefix, while outside the prefix their respective initial values are preserved.
- Why it is computed this way: This launch resets the control prefix; specific completion-flag consumers are bound separately according to the release contract, without treating all control slots as serving the same purpose.
- How we know: CENSUS, [entry.cpp:48, 80–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L80); count is reread directly from the three-tier [native params census](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json).
- Next down: [Cumulative Write Sets](#write-sets), [Completion Flags](#release).

| Instance | count | 4×count (B) | Starting offset of L2.full |
|---|---:|---:|---:|
| 1080 | 97,024 | 388,096 | 388,096 |
| 1440 | 147,712 | 590,848 | 590,848 |
| 4K | 330,240 | 1,320,960 | 1,320,960 |

<!-- beginner-r04m:start expert-write-sets -->
> Beginners may skip this section and read it when needed. This section checks storage/execution scope and does not add a network layer.
<!-- beginner-r04m:end expert-write-sets -->

<a id="write-sets"></a>
## Declared Write Sets and Actual Reads

WriteSet(L) is the union of intervals declared as written by this launch; CumWrites(L) is the cumulative declared write set. Actual byte changes can only give a lower bound on writes, as same-value zero-writes still count as writes; nor does a role span equal an actual read of every byte. See the appendix for [merging, summary, and comparison rules](APPENDIX_evidence_history.md#workspace-checker-sets).

| Launch | Read sources and declared scope | Workspace write roles |
|---|---|---|
| [L0](APPENDIX_beginner_glossary.md#g081) | Current color [texture](APPENDIX_beginner_glossary.md#g027); this path does not read WS | ∅; output is in texture id10 |
| L1 | params; Read_ws=∅ | Control prefix |
| L2 | Current color, [MV](APPENDIX_beginner_glossary.md#g023) / history when valid, [weights](APPENDIX_beginner_glossary.md#g079), and [function tables](APPENDIX_beginner_glossary.md#g074); this path does not read WS | full, pool |
| L58 | Logical 2D input of 1024T B | Logical output plus independent padding zero-write role |
| L61, etc., [QKV](APPENDIX_beginner_glossary.md#g040) | Declared input; actual numeric addresses determined by this instance's [maps](APPENDIX_beginner_glossary.md#g089) / DAG | Q, K, V, plus two release regions |
| L62, etc., [attention](APPENDIX_beginner_glossary.md#g039) | Declared Q/K/V; provenance graph must retain dynamic [epoch](APPENDIX_beginner_glossary.md#g092) | Physical output, tail zero-overwrite, release63 |
| L63, etc., projection | attention output, [residual](APPENDIX_beginner_glossary.md#g017), weights; proven to read all 16 KiB of L62 padding | output, two release regions |
| L99 | Logical sequence input of 1024T B | Logical 2D output; does not copy the P−T rows |
| L155–L157 | Specific WS / texture sources bound by tail roles | WriteSet=∅ in this specification; write textures id9, id6, id2 respectively |

The roles in the last column are not a complete full-network lifetime proof; the read sets of non-qkv [split16](APPENDIX_beginner_glossary.md#g013), the bridge, and [TIN](APPENDIX_beginner_glossary.md#g011) can only be given per their named maps / instances and cannot be filled in as a uniform "convolution neighborhood". Each launch's WriteSet comes from frozen records, while complete parameter / aliasing / consumer / release proofs still have separate gaps.

<a id="fill"></a>
For the counts, initial states, and complement rules of the dual-fill check, see the [00/A5 protocol](APPENDIX_evidence_history.md#workspace-checker-fill); it is a falsification check on named inputs, not an independence theorem over arbitrary initial values.

<!-- beginner-r04m:start expert-padding -->
> Beginners may skip this section and read it when needed. This section checks storage/execution scope and does not add a network layer.
<!-- beginner-r04m:end expert-padding -->

<a id="padding"></a>
### L3.workspace-map.padding T and P, the L58 Zero Region, and the L62 Explicit Overwrite

- What it is: Padded rows are part of the physical role; some must be zero-overwritten again after ordinary computation writeback.
- Input → output: T=2160, P=2176 at 4K → padding write semantics for 16×1024=16,384 B.
- How it is computed:
  ~~~text
  1. L58 copies the logical 1024T B and genuinely writes zeros to the independent 1024(P−T) B role.
  2. Subsequent physical rows can participate in computation; one cannot assume L58's zeros remain preserved throughout.
  3. L62 first writes computed vectors into the physical output, including those 16 rows.
  4. Read this instance's zero-write binding, checking params, output role, zero value, 4 B width, and execution stage.
  5. After ordinary output and before release, 4096 zero-writes overwrite [2211840,2228224) relative to output.
  6. The zero-writes cover the interval exactly once and do not overlap the release region; completion state is published only at the end.
  7. The 1080 / 1440 paths with T=P do not have this tail cleanup.
  ~~~
- Numeric rules: 0x00 in [E4](APPENDIX_beginner_glossary.md#g055) is [+0](APPENDIX_beginner_glossary.md#g070), but the contract here is first and foremost byte-by-byte zero-overwrite; the writes cannot be omitted on the grounds that "the initial state is zero" or "these rows do not count as logical [tokens](APPENDIX_beginner_glossary.md#g041)". L58's padding and L62's zero-overwrite are two distinct production points in time; the fact that their lengths happen to be equal does not mean they can share a single existence check.
- Why it is computed this way: Physical tiling produces extra results while downstream still reads according to the physical layout, requiring explicit invalid-row values and completion ordering.
- How we know: CENSUS, [repack.cpp:130–174](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L130), [release adapter:95–102, 166–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L166); MEASURED / diagnostic, [diag-L062 RESULT:5–17](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/diag-L062/RESULT_ZH.md#L5).
- Next down: [Defect and Negative Controls](#padding-bug), [Padding Addresses of repack](#repack), [attention Numeric Order](L3_attention_softmax.md#vit-score).

<a id="padding-bug"></a>
### L3.workspace-map.padding-bug Final Zero-Overwrite Contract and Legacy Diagnostics

[CPU Reconstruction] Between ordinary output and release, the bound typed zero-writes must be executed; L63's readset actually consumes this region, so it cannot be called unused padding. Native before-and-after snapshots both being zero still cannot distinguish unwritten bytes from same-value zero-overwrites; zero-writes overlapping the output add no new W/CumWrites bytes, and metadata coverage cannot substitute for value and timing verification. Wrong instance, parameters, address, value, width, epoch, or stage, as well as missing writes / duplicate writes / premature release, must all be checked.

[Root cause of the omission, intervals, negative controls, and legacy build continuation records](APPENDIX_evidence_history.md#padding-bug) have been moved to the appendix. The legacy diagnostic [MAP_CHECK_FAILED](APPENDIX_beginner_glossary.md#g104) is retained, and downstream NOT_RUN entries from the diagnostic round are not rewritten on account of later named gates; results from legacy builds are not transferred to the merged seal. A global [side-effect](APPENDIX_beginner_glossary.md#g094) / aliasing / lifetime theorem remains not established; for the current binding, see the [adapter](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177).

<a id="repack"></a>
### L3.workspace-map.repack 4 B Chunk Closed Form in M2 (L58 / L99)

- What it is: Moves bit patterns for the same set of logical tokens between 2D 4×4 tiling and sequence tiling.
- Input → output: H6×W6×1024 B, with rows=H6, cols=W6 → the same logical bytes; L58 additionally publishes padding.
- How it is computed:
  ~~~text
  1. Split each token into 256 chunks; g=token×256+c, c=0..255.
  2. row=token//cols; col=token%cols.
  3. tile=(row//4)×ceil(cols/4)+col//4; slot=4(row%4)+col%4.
  4. π moves input bits 0..11 to [2,3,1,7,8,9,10,11,4,5,6,0] respectively.
  5. tiled_chunk=(tile<<12) | π((slot<<8)|c).
  6. raster_chunk=((token//16)<<12) | π(((token%16)<<8)|c).
  7. Both chunk addresses are multiplied by 4 to obtain byte offsets.
  8. L58: out[4×raster_chunk: +4]=in[4×tiled_chunk: +4].
  9. L99: reverse direction; moves only the logical T rows.
  10. L58 additionally locates g∈[256T,256P) by raster_chunk, writing one four-byte zero to each.
  ~~~
- Numeric rules: π is a permutation of integer bit indices; it does not alter [payload](APPENDIX_beginner_glossary.md#g097) bits, does not [decode](APPENDIX_beginner_glossary.md#g061) E4, and involves no addition or multiplication rounding. One block contains 16×256=4096 chunks, i.e., 16 KiB. The logical raster layout still includes π internally, so raster_chunk cannot be treated as token×256+c.
- Why it is computed this way: Converts access organization between spatial [window](APPENDIX_beginner_glossary.md#g015) kernels and global sequence kernels; the closed-form implementation only changes addresses without altering network arithmetic.
- How we know: CENSUS, [repack.cpp:26–50, 83–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26); for the boundedness, uniqueness, and complete-coverage checks on padding, see [:141–165](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L141).
- Next down: [Acceptance Domain](#repack-domain), [Denominators of Saved Verification](#repack-evidence), [Worked Index Example](#worked-example).

<a id="repack-diagram"></a>
#### L58 / L99 Permutation Diagram and One 4×4 Spatial tile

All addresses in the diagram are relative to the start of their respective roles; c=0,…,255 is the 4 B chunk index per token, and π is the 12-bit closed form above. At 1080, rows=20, cols=32, T=P=640, with 655,360 B of logical data on each side.

~~~mermaid
flowchart LR
    XY["Logical token t: row=t//cols, col=t%cols"] --> TILE["Spatial tile/slot: tile=(row//4)×ceil(cols/4)+col//4; s=4(row%4)+col%4"]
    XY --> SEQ["Sequence group/slot: g=t//16; u=t%16"]
    TILE --> A["2D byte address: 4×(4096 tile + π(256s+c))"]
    SEQ --> B["Sequence byte address: 4×(4096 g + π(256u+c))"]
    A -->|"L58: copy 4 B by same (t,c)"| B
    B -->|"L99: copy 4 B in reverse direction"| A
~~~

Drawn below is **one spatial [tile](APPENDIX_beginner_glossary.md#g087)** at the top-left corner of 1080. Each cell shows "local slot s / full-grid token t", with t=32row+col; one cell contains 1024 B and 256 chunks, and the entire tile is 16 KiB. It shows logical membership, while physical bytes within the tile are still interleaved through π.

~~~text
               local col
             0         1         2         3
        +---------+---------+---------+---------+
row  0  | s0/t0   | s1/t1   | s2/t2   | s3/t3   |
        +---------+---------+---------+---------+
     1  | s4/t32  | s5/t33  | s6/t34  | s7/t35  |
        +---------+---------+---------+---------+
     2  | s8/t64  | s9/t65  | s10/t66 | s11/t67 |
        +---------+---------+---------+---------+
     3  | s12/t96 | s13/t97 | s14/t98 | s15/t99 |
        +---------+---------+---------+---------+
~~~

Sequence group0 holds t=0…15, grouped by full-grid token index; the next row of spatial tile0 starts at t=32. For example, t=32, c=0 resides in spatial slot4, with π(4×256)=64, so the 2D offset is 256 B; the offset of sequence group2/slot0 is 32,768 B. L58 copies these 4 B, and L99 moves them back by the same logical (t,c). π only permutes address bits, with no floating-point operations on the payload.

The extra P−T rows at 4K are still accounted for separately under the [padding contract](#padding): L58 writes zeros, and L99 moves only the logical T rows; the padding role cannot be drawn as a bidirectional pair of valid tokens. The diagram and integer example come from [repack.cpp:26–50, 88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26), with [complete identities](APPENDIX_evidence_history.md#split16-window-r04d) kept in the appendix.

<a id="repack-domain"></a>
### L3.workspace-map.repack-domain Mathematical Index Domain and Resource Guards

- What it is: The closed form accepts only dimensions that satisfy the tiling and safe-length contracts.
- Input → output: rows, cols, params, input length, and workspace role pointers → bijective mapping or exception rejection.
- How it is computed:
  ~~~text
  1. rows>0, cols>0, rows×cols≤1,000,000.
  2. rows%4==0 and cols%4==0.
  3. Reject (rows==4) xor (cols==4); 4×4 is allowed, while a strip with only one side equal to 4 is not allowed.
  4. rows<16384, cols<65536; accept only launch 58 or 99 and 24 B params.
  5. Input length must equal rows×cols×1024 B; role pointers and full spans must lie within the workspace.
  6. For all logical chunks, check that source / destination are in bounds and each is unique; reject on failure.
  7. L58 additionally requires grid.x=P and checks item by item that the extra zero-writes cover padding exactly.
  ~~~
- Numeric rules: All three actual token grids 20×32, 24×40, and 36×60 lie within the domain. Larger dimensions accepted by the guards do not thereby acquire exhaustive hardware evidence; invalid inputs are neither silently clipped nor taken modulo the index range.
- Why it is computed this way: Dimension conditions maintain the tiling bijection and bound index capacity; rejecting a single side of 4 inherits the non-bijective boundary of the legacy implementation.
- How we know: CENSUS, [repack.cpp:53–63, 77–95, 113–151](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L53); [M2 RESULT §3](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#3-repack-支持域回答-b1-要求).
- Next down: [Verification Scope](#repack-evidence), [Index Example](#worked-example).

<a id="repack-evidence"></a>
## Evidence Types for repack

[Verification Record] The named three-tier, three-frame bidirectional grids have native byte comparisons; dimension scans of the legacy/new modules also include rejection results and are not all valid hardware shapes. Only zeros were observed at some positions, so it cannot be claimed that all positions are uniquely pinned by nonzero content. The mathematical acceptance domain, software equivalence domain, and hardware observation domain are kept separate; a bijection check also does not equal traversing the full domain on hardware. [Original counts, pinning rates, result files, and scopes](APPENDIX_evidence_history.md#repack-evidence) have been moved to the appendix.

<!-- beginner-r04m:start expert-address-maps -->
> Beginners may skip this section and read it when needed. This section checks storage/execution scope and does not add a network layer.
<!-- beginner-r04m:end expert-address-maps -->

<a id="address-maps"></a>
### L3.workspace-map.maps How Data-Driven Address Tables Execute

- What it is: Connects byte provenance, arithmetic DAGs, and writeback locations using signed-integer offset tables; the tables contain no predicted [activation](APPENDIX_beginner_glossary.md#g045) values.
- Input → output: This instance's bound maps, wiring, input-role bytes, and weight slices → operands and write addresses for arithmetic primitives.
- How it is computed:
  ~~~text
  1. Concatenate input roles in descriptor order to obtain the executor's inp byte space; weights form a separate weight space.
  2. wload_off[A,Y,32,S_w] gives base byte offsets for weight loads; nodes may also add fixed byte selections.
  3. sread_src[A,Y,32,S_s,B] connects each byte of a shared-source event to an inp offset.
  4. xsite_src[A,Y,32,S_x,J] has the same shape as xsite_wsrc, selecting input / weight / constant-zero sources byte by byte.
  5. Compute values according to the stages and half / QMMA primitives prescribed by the DAG; address tables do not replace arithmetic order.
  6. gstore_off[A,Y,32,S_g] gives base output offsets; currently in split16 each valid event writes 16 B.
  7. Check that every valid write span lies within the role, and check byte by byte that ownership does not conflict and coverage has no holes.
  8. Slice the returned bytes according to the outputs list and write them back to the respective parameter pointers; execute side effects such as release separately.
  ~~~
- Numeric rules: The arrays are contiguous native-endian signed integers and may use i8/i16/i32/i64; integer type width is not numeric [feature](APPENDIX_beginner_glossary.md#g008) precision. Offsets are relative to the executor's input / output / weight slices and are not all absolute WS offsets. −1 in [sread](APPENDIX_beginner_glossary.md#g090) is constant zero, and −3 in xsite selects weight in conjunction with the weight offset; other negative sentinels are handled per node / category and cannot all be treated as zero.
- Why it is computed this way: Captured and bound provenance graphs preserve complex data movement and branching where some families do not yet have independently confirmed closed forms; executing the graph where semantics are unknown is more verifiable than guessing layouts from kernel names.
- How we know: CENSUS, [scalar_map.hpp:166–189, 244–259](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L244), [output ownership:319–338](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L319), [split16.cpp:56–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L56); for the bridge's separate A_src / OUTMAP structure, see [entry.cpp:56–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L56).
- Next down: [Actual Three-Tier Shapes](#map-shapes), [Matrix Arithmetic](L3_qmma_e4m3.md#qmma-e4m3), [norm Graphs](L3_norm_nonfinite.md#map-norm), [release](#release).

The fact supported by an address table is "which bytes this bound event fetches operands from and which bytes it writes to"; it does not by itself prove "this is a 3×3 convolution" or "this execution axis is a network channel". Likewise, the existence of maps, valid array shapes, or matching output bytes does not automatically prove that all producers / consumers, dynamic epochs, aliasing, and asynchronous synchronization are correct. repack and the [eight fields of split16 qkv](L3_split16_window.md#qkv-closed-form-r04n) have obtained closed forms; the latter verifies address equality only on held-out map tables while thread_class remains table-driven, which does not mean other families have also been closed-formed. Changing geometry, window shift, input-role order, or epoch identity still requires rebinding, and the production executor still reads the original tables.

~~~mermaid
flowchart LR
    K["Execution point (a,y,lane): A/Y scheduling axes; lane=0..31; S is event axis"] --> SR["sread_src[a,y,lane,s,b]"]
    I["inp byte space concatenated by role"] --> SR
    I --> XS["xsite_src / xsite_wsrc: input, weight, or zero"]
    W["Weight byte space"] --> WL["wload_off[a,y,lane,s] + node byte selection"]
    K --> WL
    SR --> DAG["Arithmetic DAG: K32→half nodes/reductions→Q8"]
    XS --> DAG
    WL --> DAG
    DAG --> GS["gstore_off[a,y,lane,s]: 16 B per valid event"]
    GS --> O["outputs sliced by length → roles of respective CB pointers"]
~~~

16 heads × 8×8 windows is the logical attention domain, while (A,Y,32,S) are data-movement execution coordinates; the two are connected via named provenance graphs, so Y cannot be treated directly as the head count nor 32 directly as the channel count. L100 uses a separate set of A_src/B_off and REDMAP/OUTMAP; see the [bridge diagram](L2_06_decoder_bridge.md#wiring).

<a id="map-shapes"></a>
### L3.workspace-map.map-shapes Viewing Real Array Axes Through Three-Tier L57

- What it is: The shape describes execution tasks and event counts; a single array template scaling linearly with WH cannot be applied across all families.
- Input → output: Three actual NPZ headers belonging to L57 together with native grids → the shapes of the arrays below.
- How it is computed:
  ~~~text
  1. Outer axis A of L57 = grid.x×grid.y×grid.z: 48, 60, and 160 across the three tiers.
  2. In this instance Y=8, lane axis=32; S_w=64, S_s=32, B=16, S_g=4.
  3. shape of wload_off = (A,8,32,64).
  4. shape of sread_src = (A,8,32,32,16); gstore_off = (A,8,32,4).
  5. Both xsite_src and xsite_wsrc = (A,8,32,0,4): this instance has no events of this kind.
  6. Byte count per array = itemsize × product of axes; all saved formats here are little-endian i64.
  7. Switching to another family re-fetches the axes: L25 at 1080 has A=80, Y=4, S_w=128, S_s=64, S_g=8.
  ~~~
- Numeric rules: An empty event axis indicates zero items, not a missing asset. A/Y are execution dimensions, so 48 cannot be treated as the token count nor 8 as the attention head count. The generic i8/i16/i32/i64 interface acceptance described earlier also does not mean these actual files all use the narrowest integer type.
- Why it is computed this way: Different families have different vector transfers and slicing organizations, and fixed-width physical operands require these discrete event axes.
- How we know: CENSUS, reading the NPY headers of the three NPZ files in this round; [1080 L57](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c6/products/S1/L057/control1080/L57-map.npz), [1440 L57](../../../../b1-relocated-10600t/dlssnr-geo2-l24-r01-20261008-codex/runtime1440-stage-L057-binding-v2/split-work/bundle/L57-map.npz), [4K L57](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c6/products/S1/L057/high2160/L57-map.npz); grids come from [native_launch_facts](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json), and the recomputed SHA of the 1440 file matches the asset pin in [configure-L057.json](../../../../b1-relocated-10600t/dlssnr-geo2-l24-r01-20261008-codex/runtime1440-stage-L057-binding-v2/configure-L057.json).
- Next down: [Shapes Across Different Families](#other-maps), [WR](#wr).

| Field | 1080 | 1440 | 4K |
|---|---|---|---|
| wload_off | (48,8,32,64) | (60,8,32,64) | (160,8,32,64) |
| sread_src | (48,8,32,32,16) | (60,8,32,32,16) | (160,8,32,32,16) |
| gstore_off | (48,8,32,4) | (60,8,32,4) | (160,8,32,4) |
| xsite_src / xsite_wsrc | (48,8,32,0,4) | (60,8,32,0,4) | (160,8,32,0,4) |

The [full SHA](APPENDIX_evidence_history.md#map-identity) of the 1440 map has been moved to the appendix; this external local copy is a historical source for the geometry binding, and it cannot be assumed from the path name alone to be the entirety of [M2](APPENDIX_beginner_glossary.md#g107) deployment assets.

<a id="other-maps"></a>
ViT expansion uses a different axis order: src and weight_offsets are (A,4,16,8,32), and store_offsets is (A,4,8,32); see [ffn_expand-resume2.cpp:205–229](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L205). Other ViT families use provenance graphs connected per instance / epoch, and the L57 fields here cannot simply be renamed and applied to them. The actual headers of 1080 L25 also differ from L57: in [L25-map.npz](../../../../dlssnr-cpp-work/chain-split16-r01-codex/bundle/L25-map.npz), wload=(80,4,32,128), sread=(80,4,32,64,16), and gstore=(80,4,32,8).

<a id="partial-sums-r04l"></a>
## QKV and projection Partial Sums (Ranks 38, 46–47, 94–95)

QKV splits the 1024 K inputs into two 512-item segments z=0, 1; each segment runs 16 [K32](APPENDIX_beginner_glossary.md#g065) steps, where the initial [seed](APPENDIX_beginner_glossary.md#g042) is +0 and subsequent steps carry the previous [half](APPENDIX_beginner_glossary.md#g054). z0 writes the half [partial sums](APPENDIX_beginner_glossary.md#g050) of 24 16 B events to buffer (requiring each byte to be written exactly once); z1 first computes `H=RN16(buffer+p1)`, then performs Q/K reduction, [RSQ](APPENDIX_beginner_glossary.md#g072), scaling, and [Q8](APPENDIX_beginner_glossary.md#g061), while V is likewise quantized from the merged H. It has no in-place half-precision reduction stages like z1/z2. [QKV/projection leaves and seed:129–150](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L129), [matrix seed fetch:213–223](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L213).

projection computes 256 K items per segment across z=0..3 (8 K32 steps per segment): z0 has initial seed=`RN16(E4_to_half(residual)*scale)`, added prior to the first K32; z1/z2/z3 all have initial seed +0. Every K32 publishes half, so the residual cannot be moved to after the entire [dot product](APPENDIX_beginner_glossary.md#g051). Letting the four segment results be p0..p3, buffer first stores p0, z1 writes `b1=RN16(p0+p1)`, z2 writes `b2=RN16(b1+p2)`, and z3 finally computes `Q8(RN16(b2+p3))`. z1/z2 read the old half every two bytes and apply h_add, rejecting [nonfinite](APPENDIX_beginner_glossary.md#g069) values; it is required that buffer be written first and initialized only once, the two reductions occur once each, and the final output be written byte by byte exactly once. reverse_red in the source code is only a negative control that alters the order, not the default order. [Execution:227–239](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L227), [z order and coverage:271–294](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L271).

Which event each byte/half fetches is still selected by the named DAG and map; this section gives the full numeric merge order without reclassifying those indices as closed forms. The prototype labels in the [named program bindings](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/cpp-integrate-layer2-r01-20261009-codex/candidate/runtime/vit-bindings.json) continue to retain MAP_CHECK_FAILED; later instance adjudications cannot retroactively alter them.

<!-- beginner-r04m:start expert-release-contract-r04l -->
> Beginners may skip this section and read it when needed. This section checks storage/execution scope and does not add a network layer.
<!-- beginner-r04m:end expert-release-contract-r04l -->

<a id="release-contract-r04l"></a>
## Per-Family Release Regions and Empty Sets (From Rank 11)

In the table below, qN denotes the u64 role pointer at CB+8N; all writes first verify `ptr≥workspace_base`, `offset≤workspace_bytes`, and `len≤workspace_bytes−offset`. Numeric outputs complete first, followed by writes to the release regions. An empty set means there is no extra zeroing of this kind for that family.

| Family / instance | Role qword; length; value; empty set |
|---|---|
| split16 F16/F17/F19/F20/F21/F22 | q6; 320 B by default at 1080, i.e., 80 LE32(0); exceptions in the next rows |
| split16 attention F18 | L27+4j(j=0..7), L103+4j(j=0..7): q6, 640 B, i.e., 160 LE32(0) |
| split16 finalhead F23 L57 | releases=[], no memset |
| Dedicated entry F34 L132 | No memset: writes only the map execution result to q2; cannot inherit the general split16 q6 rule |
| TIN | L3–5, L151–153 use q7; L7–9, L11–15, L17–23, L133–139, L141–145, L147–149 use q8; length 4GXGY B, LE32(0); L6/10/16/24/140/146/150/154 are [] |
| ViT expand F25/F30 | q7; 4grid.x B, LE32(0); all current instances are non-empty |
| ViT contract F26 | release60=q4, release61=q7; 4grid.x B each; traverses template release records over z=0..3, with each slot of the former going 0→1→2→3 and the latter ending at 0 |
| ViT QKV F27 | release61=q5, release62=q8; 4grid.x B each; final values 1, 0 |
| ViT attention F28 | release63=q6; length taken from epoch[0].release63_size, which must be identical across all epochs; all bytes 0. 640 B at 1080; cannot apply the QKV two-region length |
| ViT projection F29/F31 | release63=q4, release64=q7; 4grid.x B each; final values 3, 0 |
| L100 F33 | ctr=q4, ctr2=q5; writes 4 B at each relative offset in counter_writes, with final values 3, 0; does not indiscriminately zero the entire segment |
| copy/repack/B0/B70/S157 | No such extra release memset; L1 separately writes FF per the [initialization contract](#clear) |

The 47 320 B launches of split16 are L25, 26, 28, 29, 30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 45, 46, 48, 49, 50, 52, 53, 54, 56, 101, 102, 104, 105, 106, 108, 109, 110, 112, 113, 114, 116, 117, 118, 120, 121, 122, 124, 125, 126, 128, 129, 130. For the safe projection of the 64 current bindings (launch/grid/release only) and source SHAs, see the [per-launch table](../skewer/examples/r04l.release_bindings.json); the 65th launch L132 is interpreted by the dedicated entry. The general executor runs `memset(span(qword,len),0,len)` for each `(qword,len)` entry without guessing the release length from the output length. [split16.cpp:79–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp#L79), [L132:93–94](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L93), [TIN:179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L179), [44 TIN bindings](../skewer/examples/tin_window_r04c.bindings.json).

The expand slot index is `32*(x%Q)+x//Q` for 0≤x<grid.x=32Q, which is a dense permutation; the four physical templates cannot multiply the length by 4. It requires release_bytes=4*release_ctas, release_ctas=nc, and live tile count ≤4nc. [expand:256–258](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp#L256). A contract record is `(z,region,offset,value,count)` with z∈[0,3], offset four-byte aligned, and offset+4≤the corresponding length; count=32 denotes the number of participants in the same slot rather than writing 32 consecutive slots; LE32(value) is written in ascending z order and original record order. Every release60 slot must appear 4 times and every release61 slot 1 time, otherwise it is rejected. [contract:348–360](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L348), [writes:518–534](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_contract/ffn_contract.cpp#L518).

attention first checks that output and release lengths are consistent across all epochs; only after numeric coverage and padding zero-overwrite complete is release63 published according to the output list. [attention:288–333](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_attention_chain_r02/attention_impl.hpp#L288), [padding order:177–189](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177). ViT role qwords are taken from the current [named bindings](../../../experiments/parity-cpp-new-seal-profile-r01-20261011-codex/wsl-projection/mnt/data/cpp-integrate-layer2-r01-20261009-codex/candidate/runtime/vit-bindings.json) without altering the legacy prototype status.

L100 selects q4 or q5 using the key `role+offset`; after sorting, the value list must strictly equal [0,1,2,3] or [0], with duplicates or missing values also rejected. Final states are published only at valid four-byte slots while preserving the remaining bytes. [entry.cpp:73–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L73).

In TIN, `CW=W−2ox,CH=H−2oy` (for C32), while other C values take `CW=8*ceil((W−ox)/8),CH=8*ceil((H−oy)/8)`; GX=CW/8, GY=CH/8. The (bx,by)-th CTA corresponds to the LE32 slot `by*GX+bx`, so the release length is exactly 4GXGY, or the empty set when releaseword<0. [tin.cpp:143–155, 179–180](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L143).

<a id="release"></a>
### L3.workspace-map.release Completion Flags Beyond Numeric Exits

- What it is: Completion flags are also output side effects; dropping them makes the full WS contract and consumer wiring incomplete.
- Input → output: QKV / projection operation type and native grid.x → U32 state slots of each release region, written back to their respective Span(role).
- How it is computed:
  ~~~text
  1. Each release region has grid.x four-byte slots, with length=4×grid.x.
  2. QKV: each slot of release61 writes U32(1), and each slot of release62 writes U32(0).
  3. projection: each slot of release63 writes U32(3), and each slot of release64 writes U32(0).
  4. The total side-effect length of both regions is 8 × this operation's grid.x.
  5. In this corpus Q=ceil(T/128), QKV grid.x=16Q, and projection grid.x=8Q.
  6. Therefore QKV additionally writes 128Q B, and projection additionally writes 64Q B.
  7. The release adapter registers these regions together with the primary numeric exits; they must not be omitted from the lengths of numeric tensors.
  ~~~
- Numeric rules: States are little-endian U32 integers, not F16 / E4. 640 B is the combined length of **both** QKV release regions at 1080; it is neither 640 B per region nor 640 B for projection as well. Logical T, physical P, and release byte counts are bound separately; the 1024 B total length for QKV at 1440 does not equal T=960.
- Why it is computed this way: Notifies subsequent work units that results are ready for consumption and initializes next-stage state; returning these bytes sequentially on the CPU does not automatically reconstruct the full intermediate wait timing on the [GPU](APPENDIX_beginner_glossary.md#g078).
- How we know: CENSUS, [release_resume1.cpp:9–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_release_resume1/release_resume1.cpp#L9), [adapter:228–234](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L228), and the [three-tier native grids](../../../experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json); the formulas induct only over these named geometries.
- Next down: [WR A/B](#wr), [Read/Write-Domain Evidence Boundaries](../../arch-v2/08.02_read_write.md#v2-08-005).

| Instance | Q | QKV grid.x; per region / both regions (B) | projection grid.x; per region / both regions (B) |
|---|---:|---|---|
| 1080 | 5 | 80; 320 / 640 | 40; 160 / 320 |
| 1440 | 8 | 128; 512 / 1024 | 64; 256 / 512 |
| 4K | 17 | 272; 1088 / 2176 | 136; 544 / 1088 |

<!-- beginner-r04m:start expert-wr -->
> Beginners may skip this section and read it when needed. This section checks storage/execution scope and does not add a network layer.
<!-- beginner-r04m:end expert-wr -->

<a id="wr"></a>
Declaration stability, natively visible changes, and CPU out-of-range invariance are three distinct checks; see the appendix for [WR adjudication and missing-observation rules](APPENDIX_evidence_history.md#workspace-checker-wr).

<a id="evidence"></a>
## Named Numeric Gates and Retained Boundaries

- [M2 RESULT §6](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#6-数值门与配置普查): 1080 / 1440 f0 and 4K L0–L99 are actual numeric gates; 4K L100–L157 in M2 has only a configuration census. Passing the segment containing repack and zero-writes does not expand into a proof across the entire acceptance domain.
- [Unified M 4K Three-Frame RESULT:19–32, 61–63](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19): Two fills, each running f0→f1→f2 in a single process, with independent receipts for 948 launches; 946 observed FULL and 2 f0 L0 NOT_OBSERVED. The A5 complement semantics, B(i) gaps, and formal checker / [computed-shared](APPENDIX_beginner_glossary.md#g108) non-admission boundaries are retained.
- Legacy diagnostics, legacy standalone builds, merged M, and release M2 are distinct identities. Matching output trajectories do not prove global ROLE lifetimes, all dynamic provenance, asynchronous hardware timing, or general correctness for arbitrary geometries.

<a id="worked-example"></a>
## Worked Index Example: row=5, col=7, chunk=37

In this round, executing the small script below reads the constants of π from the current M2 source code, computes the three-tier indices, and reads only the corresponding four bytes in the saved legacy-module labeled outputs to check the L58 and L99 directions respectively; those files are address labels, not weights or native numeric targets. The final section recomputes the capacity / CumWrites(2) figures above from the already-read metadata without running the model, GPU, or full chain.

See the appendix for the [complete verification script](APPENDIX_evidence_history.md#workspace-example-code); this page retains the actual index results.


Actual results:

| rows×cols | token | tile / slot | π((slot<<8)\|37) | tiled / raster chunk | Source / destination byte offset (L58) |
|---|---:|---|---:|---|---|
| 20×32 | 167 | 9 / 7 | 630 | 37494 / 41590 | 149976 → 166360 |
| 24×40 | 207 | 11 / 7 | 630 | 45686 / 49783 | 182744 → 199132 |
| 36×60 | 307 | 16 / 7 | 630 | 66166 / 78390 | 264664 → 313560 |

All six label reads match the formula; L99 uses the reverse offsets. Each operation copies a complete four-byte unit without rearranging the four bytes of the payload. Across the three tiers, slot is identical while tile / token and the sequence position differ, illustrating directly that addresses must be bound to cols; the complete offset table of one geometry cannot be treated as a cross-geometry closed form.

### Bit-by-Bit Substitution of π

The swizzle in the real repack.cpp sends source bit0..11 to [2,3,1,7,8,9,10,11,4,5,6,0]. For 0x725=0b011100100101, the set of 1-bits {0,2,5,8,9,10} is sent in order to {2,1,9,4,5,6}, so the output is 2²+2¹+2⁹+2⁴+2⁵+2⁶=0x276=630, i.e., 0b001001110110. [Real-function computation](../skewer/examples/anatomy_r04i.py) and [results](../skewer/examples/anatomy_r04i.result.json) verify this step at the same time without reading network values.
