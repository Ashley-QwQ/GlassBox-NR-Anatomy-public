# Two Frames and One Reset: How Old Colors Become Conditions for a New Frame

Previous stop: [Learn One Block from Scratch](L1_00_one_block_primer.md) · Next stop: [Finite Number Points and Small Baskets](L1_00_numbers_primer.md) · [Back to Index](INDEX.md)

Optional drill-down: [B0 Exact Sampling](L3_b0_input.md#coordinates) · [B70 Separate Sampling](L3_b70_history_output.md#b70-temporal)

On the default route, id names a storage slot. id9 is the color [state](APPENDIX_beginner_glossary.md#g002) freshly computed in the current frame; once copied to id6, it becomes the old state readable by the next frame. The final display output is id2, which comes from a separate display-adjustment path. The [workspace](APPENDIX_beginner_glossary.md#g082) is the storage holding intermediate numbers and management flags for computation and is not synonymous with the [history](APPENDIX_beginner_glossary.md#g024) image id6.

<a id="timeline"></a>
## Two Frames Plus One Reset: Five Tracks Viewed Separately

| Track | Frame t: normal history use | Frame t+1: continue using own result | Frame t+2: satisfies reset [contract](APPENDIX_beginner_glossary.md#g101) |
|---|---|---|---|
| New inputs | New current image id1, new motion information id3, control parameters | Refresh these external inputs again | Still requires new inputs for this frame |
| Color state | Read old id6; compute new id9 → copy to id6 | Read id6 saved at t; new id9 overwrites id6 again | Does not consume old id6; current-frame new id9 overwrites it at frame end |
| Display | New id9 separately undergoes display adjustment and blends with current-frame original image backup → id2 | Separately computes id2 in the same way; id2 is not fed back by default | Generates current-frame display in the same way; no need to zero out the old image first |
| Working storage | CPU retains the whole region, overwriting launch by [launch](APPENDIX_beginner_glossary.md#g080) on its own | Continues from t's own workspace without injecting reference intermediates | Continues overwriting according to the actual write contract, not clearing all storage to zero |
| Perturbation counter | Read counter from parameters and recompute three perturbation items with position | Read counter specified by current-frame parameters | May return to 0 under a recorded [reset](APPENDIX_beginner_glossary.md#g032); changing only the counter is not enough |

~~~mermaid
flowchart LR
    T["Frame t: new inputs + available old image"] --> N["New state id9"] --> C["Copy id9→id6"] --> T1["Frame t+1: new inputs + t's id6"]
    N --> D["Display adjustment + current-frame backup → id2"]
    T1 --> C1["Save new id6 again"] --> R["Frame t+2 reset: skip old id6"] --> C2["New state overwrites id6 at frame end"]
~~~

reset means **old history is not consumed and is replaced by the new state at the end of the frame**. Mode, history and motion resource identifiers, and other conditions must also satisfy the recorded contract; counter=0 does not automatically mean reset, nor does an arbitrary control change automatically mean reset. The [exact guards](L3_b0_input.md#guards) and [retention table](L0_frame.md#what-is-retained-between-two-frames) preserve the applicable scope.

<a id="two-samplers"></a>
## Two History Sampling Paths with Different Entry Conditions

~~~mermaid
flowchart TD
    H["Old image id6, motion information id3, current-frame controls"] --> B0G{"B0 conditions allow history?"}
    B0G -->|"Yes"| S0["B0's own coordinates and 5-tap filtered sampling"] --> C0["Old RGB after input transform → conditioning channels 7 to 9"]
    B0G -->|"No"| NOW["Conditioning channels 7 to 9 repeat current RGB"]
    H --> B70G{"B70 history path valid?"}
    B70G -->|"Yes"| CONF{"Resource confidence scale > 0? Check first"}
    CONF -->|"Yes, then sample"| S70["B70's own motion sampling, history coordinates, and raw RGB sampling"] --> MIX["Fourth predicted value gives blending share, combined with current color"]
    CONF -->|"No"| CUR["Current-color path continues; no history sample fetched"]
    B70G -->|"No"| CUR
~~~

B0 turns old colors into input conditioning for the network; B70 separately fetches raw history colors for direct blending, and the two do not share a single filtered result. The [confidence scale](APPENDIX_beginner_glossary.md#g052) turns off direct blending in B70 without automatically turning off history conditioning in B0. The fourth predicted value participates in the blending [share](APPENDIX_beginner_glossary.md#g048), while the image's [fourth channel](APPENDIX_beginner_glossary.md#g026) still writes a fixed 1; display blending strength [intensity](APPENDIX_beginner_glossary.md#g004) controls **blending between the final display and the current-frame backup**, which is a separate quantity from the history share. [Confidence check and fourth value](L3_b70_history_output.md#b70-mix)

<a id="moving-point"></a>
## A Moving Point with Explicit Parameters

**Synthetic B0 coordinate example, not a measurement and not prescribing the direction or units for all [hosts](APPENDIX_beginner_glossary.md#g096)**: Let width and height be 8×8, current index (2,3), pixel center (2.5,3.5); the two motion numbers there are (0.5,−0.5), and the [scales](APPENDIX_beginner_glossary.md#g031) on both axes are set to 1/8. By the B0 formula, the normalized history center is (0.375,0.375), which converts back to pixel-center coordinates (3,3), corresponding to continuous pixel index (2.5,2.5). With x0=y0=2.5, the fractional shares on both axes are 0.5. The direction comes from **the positive scales chosen in this example** and cannot be used to assign general semantics to actual motion fields. [Original formulas and finite domain](L3_b0_input.md#coordinates)

~~~text
Current-frame small grid (synthetic):  · · · ·     History-frame small grid (synthetic): · · · ·
                                       · ● · ·                                           · ○ · ·
                                       · · · ·                                           · · · ·
The two boxes only illustrate different frames; exact point positions follow the coordinates below, not character-cell spacing.
Current image: index (2,3) ● center (2.5,3.5)
                             │ two motion numbers (0.5,−0.5) × scales (1/8,1/8)
History image: continuous index (2.5,2.5) ○ center coordinates (3,3)
                             │ does not immediately read one pixel; proceeds to construct five filtered sampling points
~~~

<a id="nested-sampling"></a>
The outer layer consists of five **[sampling](APPENDIX_beginner_glossary.md#g027) points** (left / top / center / bottom / right), and each point filters four neighbors of its own; it does not read only five pixels in total. In this example, the five center coordinates are (1.5,3), (3,1.5), (3,3), (3,4.5), and (4.5,3). Zooming in on the center point (3,3):

~~~text
Outer synthetic position diagram:      Top (3,1.5)
                                            ○
                      Left (1.5,3) ○ ─── ○ ─── ○ Right (4.5,3)
                                      Center (3,3)
                                            ○
                                      Bottom (3,4.5)
Inner four corners after zooming in on the center point:
Pixel center (2.5,2.5) ●──────● (3.5,2.5)
                       │  ○   │   ○ is sampling point (3,3)
Pixel center (2.5,3.5) ●──────● (3.5,3.5)
~~~

The inner four corners are filtered by coordinates into a single value, and the outer five points are then combined using a separate set of weights; outer [sidelobe](APPENDIX_beginner_glossary.md#g029) weights can be negative, and the inner rule cannot substitute for the outer rule. Exact sampling also enforces specific coordinate grids and roundings, given separately in [5-tap](L3_b0_input.md#five-tap) and [4-neighborhood](L4_tex_filter.md#tex-filter). B70 has its own motion-texture and history-texture transforms and does not reuse the direct-read B0 position from this example.

<a id="workspace-memory"></a>
## Which Old Workspace Bytes Are Genuinely Required Memory?

**Undetermined.** It is known that the valid-history path consumes id6 and that the CPU own-state chain actually retains the entire workspace; however, existing evidence does not close the minimal cross-frame set of "whether each byte is numerically read before its first overwrite in the current frame". Full-workspace comparisons, declared write sets, and snapshots where before and after are both zero are all insufficient to prove which old bytes can be discarded. One can state that storage is reused, but cannot draw all old intermediate numbers as extra learned memory or promise that arbitrary zeroing leaves results unchanged. [Evidence boundaries for read/write sets](APPENDIX_evidence_history.md#workspace-checker-sets)

In engineering terms, keep conservatively what the accepted drivers keep: the whole workspace plus the six texture objects of the 158 route (with id2, id6, id9 and id10 carried across the frame boundary). This is what the existing drivers do, not a proof of the minimal required memory; details in [two-frame continuation](REPRODUCE.md#two-frames).

<a id="short-route"></a>
The small branch of the 156-launch route is: the tail end writes id2 directly and copies id2 to id6, omitting the original image backup and separate display adjustment so that display and history share the result. The runtime consumes a [frozen](APPENDIX_beginner_glossary.md#g103) route [descriptor](APPENDIX_beginner_glossary.md#g088); how the host generates that descriptor from controls has not been reconstructed, so named branch conditions are not generalized into a universal scheduling law. [156 contract](L3_b70_history_output.md#variants) · [Host scope](L0a_object_method.md#route-scope-r04l)

~~~mermaid
flowchart LR
    Route{"Given route"} -->|"Default"| State["Tail id9 → save id6; compute display id2 separately"]
    Route -->|"156 branch"| Shared["Tail writes id2 directly → save id6; display and history shared"]
~~~
