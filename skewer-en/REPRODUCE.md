# Which Result Can Be Reproduced with Public GlassBox-NR v2

[Full Skewer Index](INDEX.md) · [Object and Method](L0a_object_method.md) · [One-Frame Wiring](L0_frame.md) · [Determinism and Boundaries](L0b_determinism.md) · [Weight Organization](L2_weights_layout.md)

<a id="versions"></a>
## Pick One Version Set First

The source the text explains and the reproduction entry are not the same commit. Before starting, pick one column of this table and do not mix them:

| Item | Source references in the text (for understanding the algorithm) | Reproduction entry (for running; recommended) |
|---|---|---|
| GlassBox-NR code | [e4a9b42](https://github.com/Ashley-QwQ/GlassBox-NR/tree/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec); relative to tag v2.0.0-preview (d361dca) only README/CHANGELOG changed | tag [v2.0.3-preview](https://github.com/Ashley-QwQ/GlassBox-NR/releases/tag/v2.0.3-preview) = fa8455d (numerically identical to v2.0.1-preview = 636b321, plus the receipt-completeness check and the two-frame driver) |
| Release asset payload.tar.zst.001 | v2.0.0-preview: 465,105,242 B, sha256 8605a10e01765870befc625c0f15a64f4e17eb27968630b936f7091f5bc1d9cd | the v2.0.1-preview volume, used unchanged (v2.0.2 has no new volume): 462,661,132 B, sha256 c86119619d0638e7bfa94b6ab84f6dd465bba132aaf9d9b4130c648082455b8c |
| devkit/data/PAYLOAD_MANIFEST.json | file sha256 47f093a12bafd10b6193f9fd9a66dbc82ec6d1c2a6e1b025fed5d6a75fae69aa | file sha256 2049478691d87772e044a87c01c0679a99d265e630734d5cbfc78b84abde51aa (differs from v2.0.1's ca50ccbc… only in a few DEVKIT pins of the driver files; the asset rows are the same) |
| Difference between the two | — | Only the HMMA half-zero publication restored to canonical +0: 7 C++ source files across four chain modules, three prebuilt modules, the runtime pins, the manifest and the payload change with it; see [L4.hmma](L4_hmma.md#hardware). All other source references in the text can be read at e4a9b42. v2.0.2 additionally changes only the run driver: an incomplete receipt (missing, repeated, reordered or empty) is refused with exit code 4; before a full run, `python devkit/test_run_1080_f0.py` self-tests this comparison. v2.0.3 adds the two-frame driver and the frame-1 reference table, see [two-frame continuation](#two-frames) |
| Expected result | 1080 f0 final image 764e7dd0… | Same, see [expected output](#expected); on v2.0.3 the f0 → f1 chain was run on the public modules: 158/158 and 158/158, finals 764e7dd0… / 3f1d62eb… ([gate](../../../experiments/b1-glassbox-v203-gate-20261031/RESULT_ZH.md)) |
| Verified scope | As listed under "How we know" on each page | The fixed 1080 f0 public reference table described on this page; other sizes and multi-frame runs are in the README claims table |

Take code, payload and manifest from the same column; a mixed set (for example the v2.0.0 payload with v2.0.1 code) matches no accepted combination.

<a id="quickstart"></a>
## Starting Point for Public Readers

Check out tag v2.0.3-preview, then follow the [Quickstart in the README at that tag](https://github.com/Ashley-QwQ/GlassBox-NR/blob/v2.0.3-preview/README.md#quickstart-linux-x86-64-python-313-numpy-safetensors-zstd--14); commands are not repeated here. This page is verified against the locally saved [same README:31–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L31) and [devkit notes:5–17](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/README.txt#L5), without network access to check remote status.

This entry point reproduces **agreement with the public reference table for 1920×1080, frame 0/[reset](APPENDIX_beginner_glossary.md#g032), fill00, own CPU state, across 158 [launches](APPENDIX_beginner_glossary.md#g080)**. The public precompiled modules target Linux x86-64 / CPython 3.13; the README additionally lists numpy, safetensors, and zstd dependencies. Historical measurements on other platforms do not mean the release payload includes a ready-to-use backend for those platforms. [README:18–24, 31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L18), [driver:58–59](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L58).

<a id="inputs"></a>
## Required Inputs and Assets

The reader obtains the fixed version 310.8.0.0 [DLL](APPENDIX_beginner_glossary.md#g078) independently and verifies it against the [object identity](L0a_object_method.md#object) and the release manifest; the DLL and generated [weights](APPENDIX_beginner_glossary.md#g079) are not distributed with the repository/payload. Public make_weights.py deterministically derives the five required files from the single WEIGHTS_HT resource inside it; for the format relationships, see the [weights page](L2_weights_layout.md#layouts). One cannot use another version of the DLL or treat an arbitrary image of one's own as the same input for this reference table. [README:5–14, 49–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L5).

The remaining prerequisites are the v2 source/runtime, the release [payload](APPENDIX_beginner_glossary.md#g097), the certified [function tables](APPENDIX_beginner_glossary.md#g074), and the fixed frame-0 inputs. The two input files are [caller](APPENDIX_beginner_glossary.md#g096)-id1.bin (current color) and caller-id3.bin ([motion vectors](APPENDIX_beginner_glossary.md#g023)), laid out from the payload into the inputs directory specified by the README; parameters, resource descriptors, and the reference table must also come from the same release set without being replaced by private captures. [devkit/README.txt:8–17](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/README.txt#L8), [manifest](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/manifest.json), [resource formats](L0_frame.md#textures).

Complete the file/relocation checks in the official quickstart first, and then execute its default full-chain entry point; passing verify-only alone means the preparation checks passed without yet running the model, and cannot be reported as a numeric [MATCH](APPENDIX_beginner_glossary.md#g104). Nor can a partial run with a shortened stop-after claim passing across all 158 launches and [FINAL](APPENDIX_beginner_glossary.md#g105). [driver:36–37, 42–59, 83–86](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L36).

<a id="expected"></a>
## Expected Output, and Legacy Seals in the Platform Table

The final-image [SHA](APPENDIX_beginner_glossary.md#g103)-256 for fixed 1080 f0 should be:

~~~text
764e7dd0d8f440b5afeb36e72fea3d8bc137bef891e8f09dc3476b6fef8d34ef
~~~

This is the raw output digest of [texture](APPENDIX_beginner_glossary.md#g027) id2 after L157; display screenshots, re-saved PNGs, or files after a different color transform cannot be compared against it. [worker:102–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/devkit_worker.py#L102), [public reference table:1](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/reference_f0.json#L1).

X79/[M2](APPENDIX_beginner_glossary.md#g107), 12400F/MSVC legacy ea731776, 1280P/MSVC/M, and Pi 3B+/M in the public [README platform table:80–89](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L80) list the same final-image anchor for their respective 1080 f0 runs. **ea731776 is an earlier optimization-convergence seal, not an [alias](APPENDIX_beginner_glossary.md#g092) of M2**; geometric/temporal extensions, unified M, and the release sub-seal M2 came only afterward, [ARCH:1425](../../../ARCHITECTURE_V3_ZH.md#L1425). The platform table neither proves that the binaries of these builds are identical nor provides full primitive qualification for every ISA; Pi checks only FINAL, and other scopes must be checked in their respective receipts, [ARCH:1245–1246, 1556](../../../ARCHITECTURE_V3_ZH.md#L1245).

This page does not repeat speed numbers as acceptance criteria. The historical ea731776 timing counts in the platform table have a finer accounting convention in the original report: four timing chains and four memory chains are accounted for separately and cannot be treated as an eight-run timing [mean](APPENDIX_beginner_glossary.md#g044), [ARCH:1563](../../../ARCHITECTURE_V3_ZH.md#L1563). Output digest equality and whether performance is comparable are two separate matters.

<a id="match"></a>
## What MATCH Means at This Entry Point

The public worker advances continuously from its own [workspace](APPENDIX_beginner_glossary.md#g082) and six textures; after each launch it computes the SHA-256 of the full workspace and of id1/2/3/6/9/10, which the outer driver compares against public reference_f0.json before finally checking FINAL. When all 158 points and FINAL match, the formal run entry point returns 0. [worker:79–107](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/devkit_worker.py#L79), [driver:70–85](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/run_1080_f0.py#L70).

This step is **a reproduction against the public reference digest table**: the reader recomputes the digests of the current states without locally re-acquiring the full native GPU states and performing direct byte diffs. The provenance notes of the reference table and the M2 acceptance results are recorded separately; within the 1080 gate, only 111 points carry native D observations while the remaining points compare FULL / six textures against the [G0b](APPENDIX_beginner_glossary.md#g109) reference, so agreement across the 158-point public table cannot be written as 158 brand-new native FULL observations. [M2 RESULT:82, 107–110](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L82), [reference table notes:1](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/devkit/data/reference_f0.json#L1).

MATCH applies only to the inputs, parameters, pre-states, version, and comparison scope bound to this run; it does not equal visual similarity, does not equal a proof for arbitrary inputs, and does not fill in NOT_OBSERVED. Specific labels follow the [evidence glossary](APPENDIX_evidence_history.md#project-terms), and the [full-domain](APPENDIX_beginner_glossary.md#g111) goal remains [NOT_ESTABLISHED](L0a_object_method.md#limits).

<a id="examples"></a>
## Running the Local Examples

The examples below use only artificial inputs or integer maps; no model, GPU or full chain runs. Run every command from this repository's root. Where the inputs come from is defined in [_roots.py](../skewer/examples/_roots.py):

- GlassBox-NR sources: by default a `GlassBox-NR` checkout next to this repository, or `--source-root PATH`. Pick the version from [the table above](#versions).
- Function tables and integer maps: `--tables PATH` (the `--tables` output of payload_layout.py) or `--payload PATH` (its `--out` output); they are looked up and checked by sha256.
- `--out FILE` writes the result elsewhere; without it the committed receipt in the repository is overwritten.

| Example | What it checks | Needs | Command | Expected |
|---|---|---|---|---|
| [ffn_r04b.py](../skewer/examples/ffn_r04b.py) | the FFN gate functions of B0, TIN and ViT are bit-identical; half addition order changes the result | g++, sources | `python -B -X utf8 skewer/examples/ffn_r04b.py --out ffn.json` | first line `finite_gate_equal 63488`, status PASS |
| [hmma_r04f.py](../skewer/examples/hmma_r04f.py) | HMMA half dot product and the cached path | g++, sources | `python -B -X utf8 skewer/examples/hmma_r04f.py --out hmma.json` | first line `dot 0010`, prints PASS |
| [fp32_ftz_r04e.py](../skewer/examples/fp32_ftz_r04e.py) | F32 → half conversion and FTZ boundaries | g++, sources | `python -B -X utf8 skewer/examples/fp32_ftz_r04e.py --out fp32.json` | the first stdout line in the result JSON is `boundary 33800000 0001 0001 01 00`, status PASS (the process first prints a one-line JSON summary) |
| [attention_av_r04f.py](../skewer/examples/attention_av_r04f.py) | the same artificial scores published through ViT and TIN AV | g++, numpy, sources, RCP table | `python -B -X utf8 skewer/examples/attention_av_r04f.py --tables TABLES --out av.json` | first line starts `ViT 4d32 2a29 d448 c5` |
| [geometry_r04g.py](../skewer/examples/geometry_r04g.py) | geometry counts of the 1080 L56/L100 integer maps | numpy, payload | `python -B -X utf8 skewer/examples/geometry_r04g.py --payload PAYLOAD --out geometry.json` | status PASS |
| [map_trace_r04f.py](../skewer/examples/map_trace_r04f.py) | traces two physical output bytes to their source addresses | numpy, payload | `python -B -X utf8 skewer/examples/map_trace_r04f.py --payload PAYLOAD --out trace.json` | status PASS |
| [beginner_r04m.py](../skewer/examples/beginner_r04m.py) | the made-up teaching numbers of the primer pages | nothing | `python -B -X utf8 skewer/examples/beginner_r04m.py` | status PASS |

At both GlassBox-NR commits `e4a9b42` and `636b321`, the first four examples produce the same output as their committed receipts. The generated-source hash in a receipt changes with the checkout location, because the generated C++ includes the sources by absolute path; the arithmetic is unaffected.

The other scripts (the author-side audits verify_*, record_*, classify_*, and param_change, qkv_closed_form, split16_rest, b70_rz_copy, substitutions, anatomy_r04i, weights_layout, formulas) read the private project archive `experiments/…` or files on the original machine and cannot run from a public checkout.

<a id="two-frames"></a>
## Fixed-1080 Two-Frame Continuation: Known Contract and Gaps

For the fixed 1080 configuration, the existing own-state CPU chains give a conservative engineering contract for continuing frame 0 into frame 1 ([F05 summary](../../../experiments/anatomy-f05-frame-contract-r01-20261031-codex/RESULT_ZH.md)). It assumes one thing: you already hold the complete per-frame profile package of the same build and route, i.e. the calls, params and texture descriptors of every frame. Since v2.0.3-preview the public release ships this pair for f0 and f1: `devkit/run_1080_two_frames.py` runs f0 and then f1 in one process under the contract below, the two frame-1 uploads are in the release asset `inputs-f1-1080.tar` (24,893,440 B, sha256 `f2d283262ffb7d7fdc05c3e7705f8ec11e9cac7d810c71ebff5f91596e726940`), and every launch is compared with `reference_f0.json` and `reference_f1.json`; the command is step 7 of the README Quickstart at that tag. Run on v2.0.3 on 2026-10-31: 158/158 and 158/158, finals 764e7dd0… / 3f1d62eb… ([gate](../../../experiments/b1-glassbox-v203-gate-20261031/RESULT_ZH.md)).

- **Only two external inputs per frame**: id1, the current colour (1920×1080 RGBA16F, little-endian half, 16,588,800 B), and id3, the motion vectors (1920×1080 RG16F, 8,294,400 B), uploaded as raw bytes.
- **Kept across frames**: the whole 212,519,936 B workspace, carried over unchanged. The 158 route keeps six texture objects and carries the data of id2, id6, id9 and id10 across the frame boundary; the next frame refreshes only id1 and id3. At frame end L155 writes id9, L156 copies id9 to id6 (the next frame's history), and L157 writes the display texture id2 from id9 and id10; id2 must not stand in for id6 ([outtail.cpp:99–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L99)). The 156 route has only id1, id2, id3 and id6; B70 writes id2 directly, which is then copied to id6 at frame end. This is what the accepted drivers do (MEASURED: 1080 f0–f5 chain-MATCH in both fills), not a proof of the minimal required state.
- **Second frame**: use the f1 calls and params of the same profile family (counter=1, history and MV handles as in the template); do not just add 1 to the f0 counter and run again. Take back the returned textures after every call before making the next one.
- **Reset**: switch to the full set of reset params. It turns off the temporal reads of the old history and MV, sets the counter back to 0, and the new state overwrites id6 at the end of the frame; it does not clear the workspace. The warm/cold start and history-perturbation controls of the scene cut at f8 have final-image evidence.
- **Must be refused**: a change of resolution or format, switching between the 158 and 156 routes, interpolating arbitrary controls, and p5 counters of 16 and above; on any change of version, module or asset identity, discard the old state and initialise again.
- **Gaps**: the public two-frame command and reference cover only this fixed f0/f1 input pair at fill 00; f2 onwards, fill A5 and other resolutions have no public entry yet, and there is no generator from abstract controls to a complete profile. With your own new inputs you can therefore report only "executed within the guards and carried its own state", never MATCH.

<a id="layer-assets"></a>
## Layer Index Assets (1080 L27 / L56 / L100 and RSQ / RCP)

The table-driven descriptions in [L3.split16-window](L3_split16_window.md), [L2.06](L2_06_decoder_bridge.md), [L3.norm](L3_norm_nonfinite.md) and [L3.attention-softmax](L3_attention_softmax.md) use the assets below, all of which are in the v2.0.1-preview release package. Locate each one by sha256 in PAYLOAD_MANIFEST.json: PAYLOAD entries sit at their canonical path under the payload_layout.py `--out` folder, RELEASE_VOLUMES entries at `tables/<sha256>.npz` under the `--tables` folder. Check bytes and sha256 before loading; load NPZ files with `numpy.load(path, allow_pickle=False)`.

| Asset | Release sha256 | manifest root | transform | bytes |
|---|---|---|---|---|
| L27 map | `6eade1fab0bdc0bcffa1a967736e4ab84c57e3d8937a538f22dca5e2205a8ed3` | PAYLOAD | none | 31,591,374 |
| L27 wiring | `e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea` | PAYLOAD | none | 304,721 |
| L27 contract | `3407a615888a4a2a11505f3dd42a45de5175f1438ce09efb1c277e5046aa5857` | PAYLOAD | release_form | 591 |
| L56 map | `f9280f62d910b66cdb728860fe27d36153da6a71367182b6cb4951667b42bb01` | PAYLOAD | none | 17,106,182 |
| L56 wiring | `384adcbb6260db42348605a7b84532d10a02491a3fc4fb1260624227282d3686` | PAYLOAD | none | 201,381 |
| L56 contract | `710c38c8a76c4198d95228de787b08f12ed73bc5a4684e94c8e9440eda8adff8` | PAYLOAD | release_form | 16 |
| L100 map | `12701da070a98f9242fa0e60e5fe767917902bdc6c1b9266109d91c161d42dd5` | PAYLOAD | none | 13,360,831 |
| L100 metadata | `a144ef00d3f4d072d2552dbeb3e9e7aea537779134287f2225510bef5e87c63c` | PAYLOAD | release_form | 3,376 |
| RSQ | `06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62` | RELEASE_VOLUMES | none | 246,454 |
| RCP | `055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59` | RELEASE_VOLUMES | none | 246,446 |

The three release_form entries were rewritten for the release: the two contracts keep only the contract dictionary of the original JSON, wrapped in a contract key, so read `release_json.contract` at run time. The executor reads only `coverage.counter_writes` from the L100 metadata; whether its release form matches the historical file field for field has not yet been checked against the archived object. 1440 and 4K have their own maps and wirings (the 4K L56 wiring differs from 1080), so the 1080 tables must not be reused with only the CTA count changed. The full historical-SHA → release-member chain is in the [F04 asset chain](../../../experiments/anatomy-f04-layer-index-r01-20261031-codex/RESULT_ZH.md).

**Adapt the assets before handing them to the public executor.** The raw NPZ cannot be passed in as a dictionary of all its fields. [load_layer_assets.py](../skewer/examples/load_layer_assets.py) does for L56 what the public runtime does ([g0a_runtime.py:13–29](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/g0a_runtime.py#L13-L29), [48–54](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/g0a_runtime.py#L48-L54), [plan_runtime_merged.py:35–41](https://github.com/Ashley-QwQ/GlassBox-NR/blob/658b7228f242643c14f752e7f19efa4043263c21/runtime/M/plan_runtime_merged.py#L35-L41)): it keeps only the map keys the wiring needs, with their signed dtype, native byte order, C-contiguous and read-only; it pads thread_class from (80,4,32) to (80,4,32,1), because the executor indexes maps as (c,y,l,s); it takes the contract out of its release_form wrapper; and it expands RSQ / RCP to dense F32 bit-pattern tables indexed by half_bits−0x0410. Without flags it reads the local paths recorded in the bindings file; with `--payload` / `--tables` it locates the release assets by sha256; every asset is checked against its sha256 first. `LayerAssets.arguments(input, weights)` returns the positional arguments of the public `audit_execute`. Run once on 2026-10-31 with synthetic input and weights: output 1,433,600 B; dropping the thread_class axis is refused by the `map index` guard. This shows only that the interface connects, not that the numbers are right; `audit_execute` does not check read-only, the precompiled entry does. A self-written DAG interpreter can use the raw three-axis class and the raw half-bit table keys directly. The public prebuilt modules target Linux x86-64 / CPython 3.13; other platforms build from the GlassBox-NR sources. Check record: [G03](../../../experiments/anatomy-g03-layer-loader-r01-20261031-codex/RESULT_ZH.md).

<a id="public-private"></a>
## Boundary Between Public Reproduction and Private Captures

A public reader can use their own DLL, the release payload, and the same inputs to rebuild the weight files, verify the assets, and re-run the 1080 f0 reference-table gate above, without needing access to the capture directories on this project's private disks. This result corresponds to the public M2 user driver and does not automatically re-test multiframe runs on M, other inputs, or the legacy ea731776 build. [README:54–78](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/README.md#L54).

Independently redoing raw "CPU vs. native" byte diffs, point-by-point gap adjudications, other resolutions / history states / parameter variations, or cross-GPU observations requires the corresponding raw uploads, native parameter/resource descriptors, workspace/texture snapshots, and fixed comparison scopes; the public digest table alone cannot reconstruct those raw values. For the named scopes, see [Object and Method](L0a_object_method.md#capture), [Determinism](L0b_determinism.md#open), and the [appendix result ledger](APPENDIX_evidence_history.md#index-measured-scope).

This page provides only a guide to the existing quickstart and acceptance [contracts](APPENDIX_beginner_glossary.md#g101); this round performed no downloads, compilations, or GPU, CPU-model, or continuous-chain runs.

The [documentation and scope validation](../skewer/examples/r04k.validation.json) and [release scan](../skewer/examples/r04k.leak.json) for this round are saved separately as inspectable receipts.
