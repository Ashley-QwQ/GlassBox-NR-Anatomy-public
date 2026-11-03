# L2.06 Decoder Bridge

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [Back to Parent L1](L1_06_decoder_bridge.md) · [Page Terminology](INDEX.md#shape-and-workspace-notation)

[Weight Organization, dtypes, and Stage Byte Accounting](L2_weights_layout.md)

<a id="bridge"></a>
<!-- coverage: {"launches":[100],"kernels":["cc_dec_input_upsample_1024_512_tilesync_fp8"]} -->
### L2.06.bridge Decoder Bridge: Projection, Reduction, and skip (1 Launch)

- Coverage: L100 / B39.
- What it is: [Projects](APPENDIX_beginner_glossary.md#g038)/expands the [bottleneck](APPENDIX_beginner_glossary.md#g010) exit and merges in B30's spatial [bypass](APPENDIX_beginner_glossary.md#g016).
- Input → output: Tier-6 1024-[channel](APPENDIX_beginner_glossary.md#g007) [E4](APPENDIX_beginner_glossary.md#g055) + B30.[full](APPENDIX_beginner_glossary.md#g018) (tier-5 512-channel full bypass) → tier-5 512-channel E4; also writes [F16](APPENDIX_beginner_glossary.md#g054) [partial-sum](APPENDIX_beginner_glossary.md#g050) scratch storage and the control region, with each interval given by the current parameters.
<a id="operator"></a>
## Channel Reduction and Window Geometry

[CPU Reconstruction / Fixed 1080 Map] Each path of 8×[K32](APPENDIX_beginner_glossary.md#g065) covers 256 input channels, and the four partial sums (the first three paths in [REDMAP](APPENDIX_beginner_glossary.md#g090) and the fourth path in OUTMAP) jointly reduce 1024=4×256 channels; they are not four spatial [interpolation](APPENDIX_beginner_glossary.md#g020) points. Every one of the 1,105,920 output bytes in the fixed map selects each of the four channel groups once and shares the remaining selection coordinates; the A source groups have the same spatial position and differ in channel by 256. The [integer check and SHA](../skewer/examples/geometry_r04g.result.json) are [bound](APPENDIX_beginner_glossary.md#g103) to this instance and cannot be extrapolated to arbitrary maps.

The [window](APPENDIX_beginner_glossary.md#g015) grid for 60×36 is ceil(60/8)×ceil(36/8)=8×5, covering a 64×40 canvas; the known exit [logical](APPENDIX_beginner_glossary.md#g085) capacity is 32×20×512 E4, not the 30×18 that would result from directly halving the valid 60×36 dimensions. The 327,680 B pooled exit of the L56 map is uniquely covered by 20,480 16 B write events; partitioning into 8192 B buckets yields exactly 40 buckets, each with a capacity equal to 4×4×512 E4. The [integer map check](../skewer/examples/geometry_r04g.py) proves these byte counts; [Inference] pairing each 8×8 input window with a 4×4 spatial exit is compatible with the capacity, but bucket numbers have not yet been independently calibrated as spatial blocks. Establishing that pairing requires independently establishing the logical (x,y,c) mapping between input window indices and pooled bytes and verifying source/destination coordinates per write event; it also requires independently calibrating the logical coordinates of the L100 output and skip to establish the spatial correspondence across the bridge. Existing records do not by themselves prove standard four-point [mean](APPENDIX_beginner_glossary.md#g044) pooling, an independent native physical layout, or which interpolation L100 uses.

- How it is computed:
  ~~~text
  1. Read matrix operands according to the input source table and weight offset table
  2. Reduce 256 channels across eight K32 steps along each of the four paths, preserving per-step half publication
  3. Merge the first three 256-channel partial sums in the prescribed order
  4. Add the fourth 256-channel partial sum to complete the 1024-channel reduction, then fuse with the scaled skip
  5. Quantize and write the output, scratch storage, and control flags declared for this instance
  ~~~
- Index structure: A_src (input offsets) / B_off ([weight](APPENDIX_beginner_glossary.md#g079) offsets) are seven-axis tables where the product of the first four axes equals the logical [token](APPENDIX_beginner_glossary.md#g041) count and the last three axes are 16×8×32; OUTMAP (output map) has one 12-item row per output byte; REDMAP (three-term reduction sources) has 3×4 items per position.
- Semantics: A 1024-channel low-density grid → 512-channel high-density grid is supported by shapes and wiring; specific interpolation or convolution semantics are not independently confirmed, and [nearest-neighbor](APPENDIX_beginner_glossary.md#g021) cannot be concluded from the name upsample alone.
- Numeric rules: Three-term half addition adds the first two terms first and then the third term; only after adding the fourth path is the [fused multiply-add](APPENDIX_beginner_glossary.md#g063) performed; finally E4 [RN-even](APPENDIX_beginner_glossary.md#g059) is applied, while the detailed rounding model of half fusion is deferred to the lower level.
- Per-instance variation: The singleton replaces its source/output/reduction maps, weights, and intervals as geometry changes; the [residual](APPENDIX_beginner_glossary.md#g017) always comes from the current frame's B30 full bypass; control counts are written according to the contract of that instance.
- Why it is computed this way: Restores global bottleneck information to the window scale while reconnecting spatial information that did not pass through the bottleneck.
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100) (structure / explicit arithmetic), INFERRED (spatial semantics); [decoder in entry.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp).
- Next down: [L3.workspace-map (Bridge Mappings)](L3_workspace_map.md#address-maps); [L3.qmma-e4m3 (Projection Matrices)](L3_qmma_e4m3.md#qmma-e4m3); [L4.half-arith (Reduction / Fusion Rounding)](L4_half_arith.md#half-arith).

<a id="wiring"></a>
### 1080 L100 Dataflow: Projection, Three-Term Reduction, and B30 Bypass

~~~mermaid
flowchart TD
    X["L99: X₆(1024) E4, 32×20×1024"] --> P["Project by A_src/B_off: 4 paths of 256 channels each; 8 K32 steps and F16 publication each"]
    P --> Partials["F16 projection partial sums Partials; execution slicing axes follow graph"]
    Partials --> R["REDMAP selects v₀/v₁/v₂: H+(H+(v₀,v₁),v₂) → r F16"]
    R --> O["OUTMAP: per output selects r, fourth path d₃, skip position, and scale source"]
    Partials -->|"Fourth-path partial sum d₃"| O
    O --> ADD["H+(r,d₃) → F16"]
    ADD --> HF["h_fma(D8(skip),scale,H+(r,d₃)) → F16"]
    SK["L56 / B30.full: X₅(512) E4, 60×36×512"] --> HF
    HF --> Q["Q8 → X₅(512) E4, 60×36×512"]
    Q --> NEXT["B40 / L101 split16 decoder"]
    R -. "Write F16 scratch by RED_OFF" .-> TMP["Scratch role; control flags published separately per current binding"]
~~~

Three-term reduction adds the first two terms first and then the third term; the d₃ selected by OUTMAP undergoes a separate half addition with r before entering the skip fused multiply-add and E4 [publication](APPENDIX_beginner_glossary.md#g091). "Slices" in the diagram refer to the CPU partial-sum organization; they are not named network heads, nor is the bridge presumed to be nearest-neighbor or a specific convolution. [entry.cpp:54–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L54) gives the order item by item; this round's [parameter/map check](APPENDIX_evidence_history.md#split16-window-r04d) simultaneously verifies the pointer handoff among the L99 main path, B30.full, and this [launch](APPENDIX_beginner_glossary.md#g080), without executing a new network numeric gate.

<a id="byte-trace"></a>
### A Concrete Source Example at 1080: Output Physical Byte 0

[CPU Reconstruction / Integer-Table Direct Reading] The [script](../skewer/examples/map_trace_r04f.py) first verifies the original bound SHAs and reads only the integer maps. Row 0 of OUTMAP selects reduction scratch offset 0 and the fourth-path partial sum; the first three Partials selectors are (0,0,0,0), (160,0,0,0), and (320,0,0,0), and the fourth is (480,0,0,0). The eight K32 steps of each partial sum read 256 distinct main-path bytes in total.

Decoded through the established inverse formula of the L99 2D [rearrangement](APPENDIX_beginner_glossary.md#g019), all four groups come from bottleneck logical (x,y)=(0,0), with channels 0–255, 256–511, 512–767, and 768–1023 respectively; skip takes physical byte 0 of B30.full. Merging the first three terms via H+, adding the fourth term via H+, and merging skip via HF finally publishes output byte 0. The [table-reading results and identities](../skewer/examples/map_trace_r04f.result.json) retain the complete selectors.

This indeed determines the main-path source coordinates; **independent logical coordinates for output byte 0 and skip byte 0 remain not established**, so they cannot be directly called a specific (x,y,c). Closing the remaining spatial relationship requires independently calibrating the layouts at both ends and comparing them against these sources; the current example does not claim to have explained the entire 32×20→60×36 spatial [operator](APPENDIX_beginner_glossary.md#g035).

[CPU Reconstruction / Integer Tables Read Directly] Implemented from the tables, L100 runs as follows: A_src/B_off give the sources of the eight K32 steps; REDMAP gives the sources of the first three partial sums D; OUTMAP[i] gives, for output byte i, the scratch half address, the fourth D, the skip byte and the scale offset (columns 7–11 are not consumed at present and must not be used as extra operands). The arithmetic is red=H+(H+(D₀,D₁),D₂), v=H+(red,D₃), out[i]=Q8(HF(E4→half(skip[OUTMAP[i,5]]),scale,v)). At 1080 all 1,105,920 outputs satisfy OUTMAP[i,5]=i, so skip is fused with the current output at the same physical byte index; equal physical indices do not mean the image coordinates of the two sides are independently calibrated. Assets: [layer index assets](REPRODUCE.md#layer-assets); check: [F04](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md).
