# Appendix: Evidence History, Build Identities, and Saved Receipts

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

<a id="formula-open-r04l"></a>
## Formula Coverage: Open Items

r04l reviewed against the original audit row IDs, and the [1846-row classification and 226-item ranking ledger](../skewer/examples/r04l.classification.json) pins the original audit [SHA](APPENDIX_beginner_glossary.md#g103): the default 1824 rows change from CLOSED/TABLE/PARTIAL/MISSING/[UNKNOWN](APPENDIX_beginner_glossary.md#g104)=1606/110/100/2/6 to **1706/112/0/0/6**; the 22 variant rows are 18/1/0/0/3. In the default set, 100 rows add [closed forms](APPENDIX_beginner_glossary.md#g020), two rows turn into TABLE after completing the [DAG](APPENDIX_beginner_glossary.md#g089) contract, and 59 rows with supplemented table specifications remain TABLE; V01.02 only fixes the scope while [host](APPENDIX_beginner_glossary.md#g096) generation remains UNKNOWN. Summarizing by the weakest item per family gives 4/34/0/0/6, still **4/44 closed-form families** (covering 5/158 positions); 158/158 navigation coverage cannot be called full formula closure.

Incremental update at r04n: the [eight-field closed forms and held-out table evidence for qkv](L3_split16_window.md#qkv-closed-form-r04n) move the four full rows F18.02/.03/.04/.39 from TABLE→CLOSED, bringing the counts at the time to **1710/108/0/0/6**, with variant and family counts unchanged. The [classification ledger at the time](../skewer/examples/r04n.classification.json) retains the original denominators of 1846 rows and 226 ranked items: within the merged row F18.05, shfl_idx and psel are CLOSED, while thread_class remains TABLE because the field is absent at 1080 and the frozen hypothesis failed on the held-out set, so the row continues as TABLE when summarized by its weakest sub-item. 8/9 is a field count and cannot be treated as 8 full audit rows or as closing the entire F18 family; independent bias ordering in F18.36 remains UNKNOWN.


r04o classification record: the [row-by-row and field-by-field ledger](../skewer/examples/r04o.classification.json) maintains the original 1846-row denominator; the 178 rows across F16–F23 change from 146 CLOSED / 31 TABLE / 1 UNKNOWN to **167 / 10 / 1**, with 21 complete address rows moving from TABLE to CLOSED. The default 1824 rows currently stand at **1731/87/0/0/6**; the 22 variant rows remain 18/1/0/0/3. Taking the weakest item per original audit row gives 6/44 CLOSED families, but the optional thread_class of F20/F21 has no standalone audit row, and including the class fields keeps the count at **4/44**; these extra fields remain TABLE. The 816 rows across F03–F15 remain **787 CLOSED / 28 TABLE / 1 UNKNOWN**: the 28 rows are function-value dependencies on RSQ/RCP and F03 noise rather than address tables; TIN source-code indexing is a [code-transcribed index formula](L3_tin_window.md#tin-code-transcription-r04o), and new address held-out validation in r03 is NOT_RUN.

| Remaining category and ID group | Closure path and original audit effort |
|---|---|
| split16 addresses and uncovered items: r02 historical failures on F16.03, F17.03, and F19.02/.04; F34, L132, and B31 candidates | r04 classifies the historical failures as NON_PRODUCTION_VARIANT, with the accepted maps EXACT and the original FAIL verdicts retained; there is no C++ actual-read receipt for the specific 12×12 maps. [Per-item and 4K counts](L3_split16_window.md#r04-four-k-r04p). The 28 L132 candidates are OUT_OF_SCOPE and the 3 one-dimensional B31 candidates are NOT_RUN; r02 formulas are not applied to them. F23 has a bound 36×60 table, while its 4K input-frame identity is not independently bound. ViT F25–31 and L100 F33.01–03 still require their own coordinate / dynamic-provenance evidence. |
| F18.05 class, F19/F20/F21 classes, and F22.05 class; complete DAGs F22.08/F23.04 | The exchange/selection sub-items of qkv and F22 are in closed form; the single-class hypothesis for F19/F20/F21 is FAIL, and the F22 class candidate is held-out EXACT but remains table-driven. The DAGs of F22/F23 and the independent spatial provenance of L56 still follow the tables and original evidence boundaries, without being upgraded from address equivalence. |
| [RSQ](APPENDIX_beginner_glossary.md#g072)/RCP, [Radius](APPENDIX_beginner_glossary.md#g073)/Cos/Sin, LG2/EX2, and V05.03 function values (all function TABLE rows) | Endpoint / wrapper / identity specifications have been supplemented; table-free [bit-pattern](APPENDIX_beginner_glossary.md#g057) rules require at least 5–20 person-days and structural evidence/probes, with closure time unknown |
| F18.36 [bias](APPENDIX_beginner_glossary.md#g052), F42.50 B69 coordinates, F35.56 L133 shared provenance | Independent head/query/key labels: 1–3 days; B69 independent coordinates: 1–3 days plus device data; L133 epoch write→read lineage: 2–5 days plus data, still NOT_ADMITTED |
| F03.54/F43.50 [HMMA](APPENDIX_beginner_glossary.md#g065) zero sign | Retains 480 counterexamples; new zero-product / [seed](APPENDIX_beginner_glossary.md#g042) / [cancellation](APPENDIX_beginner_glossary.md#g071) / K16 internal sub-segment adjudication requires 1–3 days plus a capture window, and UNKNOWN is not eliminated by CPU candidates |
| F44.47/V05.04 joint RGB domain | Cross-[channel](APPENDIX_beginner_glossary.md#g007) [saturation](APPENDIX_beginner_glossary.md#g033) branch: 3–10 days, with full closure time unknown |
| V01.02 host generation; V06.01 312B ABI | Former: 1–3 days plus data; latter: 1 day for evidence inventory and 3–10 days plus data for implementation/acceptance; 312B remains rejected/NOT_RUN |

The r04l work record consists of current-code/binding transcription and small Python checks, with zero new [GPU](APPENDIX_beginner_glossary.md#g078), model, continuous-chain, compilation, remote, or network runs. The [classification ledger at the time](../skewer/examples/r04l.classification.json), [verification receipt](../skewer/examples/r04l.validation.json), and [scan receipt](../skewer/examples/r04l.leak.json) preserve their historical identities. r04n adds only a [58-cell address/index spot-check](../skewer/examples/r04n.qkv_samples.json), importing the frozen formulas and two stored tables read-only without re-running the study's full-map held-out validation, and does not upgrade proofs of the numeric DAG, full chain, or dynamic lineage. The [check at the time](../skewer/examples/r04n.validation.json) and [release scan at the time](../skewer/examples/r04n.leak.json) preserve their historical identities. r04o adds a [13-cell address example](../skewer/examples/r04o.example.json) and source-code index transcription; the [check at the time](../skewer/examples/r04o.validation.json) and [release scan at the time](../skewer/examples/r04o.leak.json) preserve their historical identities. r04p only organizes saved map results and variant classifications without modifying the original audit row counts; [this round's validation](../skewer/examples/r04p.validation.json) and [scan](../skewer/examples/r04p.leak.json) record the current documentation state.

[Full Skewer Index](INDEX.md) · [One-Frame Entry](L0_frame.md)

This page migrates existing main-text material from before r04a; "this round" in the text carries over the context of the original writing round and does not denote a new measurement in r04a. r04a modifies only documentation, with GPU / model / continuous-chain runs all equal to 0. [Native behavior](APPENDIX_beginner_glossary.md#g001), CPU representations, and [verification records](APPENDIX_beginner_glossary.md#g100) are kept separate, and legacy NOT_RUN, UNKNOWN, rejections, and failures are not relabeled.

Appendix scripts still run from the repository root; computed numeric values are records from the original writing round and were not re-run in this round.

<a id="qmma-history"></a>
## QMMA Candidate Adjudication, Cross-Architecture Comparison, and Source Identity

Moved from [L3_qmma_e4m3.md](L3_qmma_e4m3.md); below is the record saved from the original writing round.

## How Candidates Converged from 1,832 to One Behavior Class

Freeze the candidate list and predictions → collect hardware answers → use an independent comparator to eliminate any candidate with a first difference on any case → design the next batch of discriminators within the surviving list. Candidate formulas must not be modified after seeing the answers.

| Stage | Cases read and discrimination | Remaining | Evidence and tier |
|---|---|---:|---|
| Bank construction, 09-18 | 8 named models + 1,824 parameter combinations, QMMA/HMMA evaluated separately; 24 sweep cases partition into 291 classes | 1,832 | CENSUS: [core probe RESULT:23–54](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#第-2-项候选清单与离线评估) |
| sm_120 first round, 09-20 | Historical record: 24 sweep + 5 instance cases entered prediction, hitting a 1,206-member class, with 32 more eliminated at wrap-up | 1,174 | INFERRED / historical recounting: [legacy ARCH:548–550](../../../ARCHITECTURE_ZH.md), [Ada acceptance review at the time:62](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#4-对既有结论的影响); the first-round hardware review/closure directory is absent from the current local path, and raw receipts were not re-read in this round |
| First batch adjudication, 96 new cases | Frozen partition 61 / 168 / 945, measured results select the first class; EXACT and legacy CORE eliminated | 61 | MEASURED (saved record): [this round's RESULT:3](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/RESULT_ZH.md), [adjudication:5–7](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/ADJUDICATION_ZH.md#裁决) |
| batch2, 4 cases | Two passes give 0x5c02, 0x5c02, 0x5c02, 0x5c00; leaving the three classes field, [value](APPENDIX_beginner_glossary.md#g067), and renorm | 8 | MEASURED: [resume2 RESULT:8–9](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume2-20261007/RESULT_ZH.md#正式裁决与规则) |
| batch3, 2 cases | Two passes give 0x0001, 0x0000, eliminating the value and renorm classes | 3 names, 1 behavior class | MEASURED: [resume3 RESULT:8–16](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RESULT_ZH.md#正式裁决), [RULE:5–29](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#正式结果) |

The three names are LOONG_HMMA, P_F25_opsum-field_cmax1_ctr1_zero_none_gfnone, and P_F25_opsum-field_cmax1_ctr1_zero_none_gf-24. HMMA in the name does not alter the input format here. The algebraic reason in RULE:28–29 is: finite [E4](APPENDIX_beginner_glossary.md#g055) products all lie on the $2^{-18}$ grid, and finite F16 seeds lie on the $2^{-24}$ grid; the extra grid-point lower bound takes effect only in fine-grid regions where every term can already be placed exactly. The three names are identical across the frozen finite model domain, rather than being grouped into one class merely because samples failed to separate them.

The status is UNIQUE_BEHAVIOUR_CLASS_WITHIN_FROZEN_FINITE_DOMAIN_BANK. It does not prove candidate-family exhaustiveness, hardware equivalence across all finite inputs, a complete contract for [NaN](APPENDIX_beginner_glossary.md#g069)/Inf/signed zero/overflow, or network reachability; nor can network-chain agreement substitute for arithmetic discrimination.

## sm_120 vs. Other Architectures

Formula conventions follow [V2-02-004](../../arch-v2/02.02_architectures.md#v2-02-004) and [RULE:31–40](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#跨架构比较). No GPU re-measurements were run in this round; historical hardware records and legacy rules carried over in this round are listed separately.

| Architecture / input path | Alignment, grouping, and publication | Historical hardware record | Scope in this round |
|---|---|---|---|
| sm_75: [decode](APPENDIX_beginner_glossary.md#g061) E4 to F16, then use HMMA | field F24; single F16 [RN-even](APPENDIX_beginner_glossary.md#g059) across full K8; F16 [subnormal](APPENDIX_beginner_glossary.md#g068) [field exponent](APPENDIX_beginner_glossary.md#g058) −14 | MEASURED: RTX 2060, one survivor across 79 sweep cases; [09-18 RESULT:56–71](../../../experiments/parity-core-accum-probe-r01-20260918/RESULT_ZH.md#第-4-项本机-hmma1688sm_75rtx-2060的结果) | Carries over legacy rule; no native E4 QMMA gate |
| sm_86: decode E4 to F16, then use HMMA | renorm F24; K16 split into two K8 groups, each publishing F16 to serve as the next group's seed | MEASURED: RTX A2000 Laptop, 65/65 sweep and 3,748/3,748 instance cases support GGGZ_HMMA; [Ampere RESULT:3–19](../../../experiments/parity-claude-ampere-probe-r01-20260921/RESULT_ZH.md#1-结果) | Formula carries over RULE's interpretation of the frozen GGGZ parameters, not a new hardware adjudication in this round |
| sm_89: E4 QMMA | field F13; K32 split into two K16 groups, each publishing F16 | MEASURED: returned from RTX 4090 D, GGGZ_QMMA unique; single FP8 source, not cross-validated; [Ada RESULT:25–35, 64–67](../../../experiments/parity-claude-ada-bounty-accept-r01-20260921/RESULT_ZH.md#2-判读用冻结比较器不另写) | Carries over legacy formula/acceptance; cannot be expanded into a cross-card [full-domain](APPENDIX_beginner_glossary.md#g111) proof |
| sm_120: E4 QMMA | [field F25](APPENDIX_beginner_glossary.md#g066); single F16 publication at the end of full K32 | MEASURED: 96+4+2 saved hardware cases, one final class; [port RESULT:15](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门) | Current source code aligns item by item with RULE; only synthetic software examples in this round |

F13/F24/F25 cannot be understood merely as differences in significand bit width: exponent source, grouping, whether the seed participates in the maximum exponent, and truncation all affect the output, so sm_120 cannot be replaced by the two K16 groups of sm_89 or an ordinary exact [dot product](APPENDIX_beginner_glossary.md#g051).

## Boundaries Between Current Source Code and Historical Records

- All 10 copies of the representative header file read in this round share the same SHA-256: 2b85ddfaeb37eb5d16560224def629ff29a043c4421b5b571749103b398e5452; this is a source identity, not a runtime build identity.
- "Pending C++ integration" in the 10-07 RULE/RESULT referred to the legacy tree; the current header file already contains the field F25 branch. Legacy experiments are not relabeled as a result.
- The 1 hundred million random cases in the port are comparisons against an independent software reference, kept separate from the 102 hardware cases; the unrun 4K status in the legacy port round at the time does not override the later named results in ARCH 0.7. This topic does not generalize later full-chain agreement into a general QMMA theorem.

<a id="half-proof"></a>
## Composed Proof, Counts, and Identities for Integer T1 and T0

Moved from [L4_half_arith.md](L4_half_arith.md); below is the record saved from the original writing round.

PROVED in [project RESULT_resume2_v1_ZH.md:3, 9–28](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L3) covers all $2^{48}=281,474,976,710,656$ raw triples, including exception categories and messages. The proof chain is:

1. Complete 65,536 decode domain, exact two-limb composition, zero sign, and 81 top-bit intervals; 272/272 first-stage T1 certificates are genuinely UNSAT, connecting independent IEEE [binary64](APPENDIX_beginner_glossary.md#g056) rounding to T0.
2. Connection between T0 non-NaN binary64→half conversion and IEEE RN-even; 1,704 genuine UNSAT leaves in the second stage, with interval coverage exporting 5,002,132 dual-sign compiled representatives.
3. 25,572,235,280,384 nonfinite raw triples proved separately by category and compared across 448 representatives, complementing the finite domain. Together with 253,952 finite runtime checks and decode representatives, the total number of actual compiled comparisons is 5,322,068; this count is not a brute-force enumeration of $2^{48}$.

Both controls that intentionally break the implementation were caught: missing carry and ties-away, see [RESULT:32–35](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L32). The trust boundary still includes IEEE correctly rounded std::fma, the round-to-nearest-even environment, the double/integer ABI, the compiler, the solver, and the source-to-model correspondence; [RESULT:39–43](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L39). Historical UNKNOWN entries were not directly upgraded to UNSAT.

This round re-read and checked the plan, 7 evidence members, and two frozen source SHAs bound in [composition-result-v1.json](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/composition-result-v1.json), and all match; neither the solver nor the full proof driver was re-run. The T1 source SHA-256 is 78d251701c70818c5f67e14f380f1794a13e58cd8b3e98000bf6f668293cf557, and T0 is 4acb7aecc4144713a569d139aa9a209d8b14848a7615ec02c7ca7fa87563fdf7.

<a id="attention-bindings"></a>
## attention Frozen Graphs, Interpreter, and SHA Bindings

Moved from [L3_attention_softmax.md](L3_attention_softmax.md); below is the record saved from the original writing round.

<a id="graph-bindings"></a>
## Binding Behavioral Explanations to Frozen Graphs

Generic executors define the primitives, while concrete DAGs define the [call](APPENDIX_beginner_glossary.md#g080) order. Below we list only the graphs and SHAs actually read by this slice, without copying low-level instruction details or model coefficients. The source location for single-line JSON files is :1.

| Source path:line | SHA-256 | What this slice checks with it |
|---|---|---|
| [dlssnr-work/l62-epoch-fix-r02-claude/maps-base/t640/cy0/l62-templates-and-checks.json:1](F:/dlssnr-work/l62-epoch-fix-r02-claude/maps-base/t640/cy0/l62-templates-and-checks.json) | 8037735246b6c41c95a85191eb785bfd1d42043cca087ffe485c02f935a49205 | ViT half [affine](APPENDIX_beginner_glossary.md#g049) transform, encoding transform, 10-round [denominator](APPENDIX_beginner_glossary.md#g048), and post-[AV](APPENDIX_beginner_glossary.md#g077) [scaling](APPENDIX_beginner_glossary.md#g031); also checks cy1/cy2 bindings and the three map SHAs |
| [dlssnr-cpp-work/fam-attention-r01-codex/resume1/maps/H2160/cy0/l62-templates-and-checks.json:1](../../../../dlssnr-cpp-work/fam-attention-r01-codex/resume1/maps/H2160/cy0/l62-templates-and-checks.json) | 0f5d63fe9bb92f554b077731857780ca4b5e086622fb74118d148f3265145035 | 34 rounds, F32 multiplication→half subtraction for the 16 padded items in the tail round; retains legacy map status |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json) | e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea | half affine transform, [reduction](APPENDIX_beginner_glossary.md#g050), RCP, [weight](APPENDIX_beginner_glossary.md#g048) publication, and AV across the two [query](APPENDIX_beginner_glossary.md#g040) sub-tiles of split16 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L28-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L28-lane.wiring.json) | e9c276cfeb85801e701539aece1b008ef6d06f3ff8b4f4e45d1fd59a2d3940bd | Channel projection / [residual](APPENDIX_beginner_glossary.md#g017) boundary of [proj](APPENDIX_beginner_glossary.md#g038); no second score [normalization](APPENDIX_beginner_glossary.md#g048) |

The T640 graph SHA matches [L62.epoch_wiring in s00-bindings.json](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json); the two split16 graphs match [the L27/L28 maps in s00-bindings-front.json](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json). In this round, both the frozen E-drive copy and the F-drive source of the reference interpreter have SHA f906820b2786a3ace14f5b65ed435e144301aa38e88a4d761d82a0e533bd961c. These reads claim neither new all-geometry symbolic admission nor a complete [ROLE](APPENDIX_beginner_glossary.md#g105) lifetime proof.

<a id="norm-bindings"></a>
## norm Frozen Graphs, Fusion Contract, and Identities

Moved from [L3_norm_nonfinite.md](L3_norm_nonfinite.md); below is the record saved from the original writing round.

| Graph / contract actually read in this round path:line | SHA-256 | Scope of use |
|---|---|---|
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L27-lane.wiring.json) | e9f851e2df2ecbaf01cabf635ddf0d72b8713b5ac4fa3e4eeda140ad2ac07dea | 32 RSQ statistic dependencies, scales, and publications in split16 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/C27-contraction.json:1](../../../../dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/C27-contraction.json) | a2f128a46633274bbc12977677512ab9c217572a6067da40440d57b0f7429610 | All 64 square-pair fusion contract items select the first square for fusion |
| [dlssnr-work/vit-t640-numeric-r07-codex/maps/t640/l61-t640-map.json:1](F:/dlssnr-work/vit-t640-numeric-r07-codex/maps/t640/l61-t640-map.json) | 2421b94d7a1790b7deaab7fdaaa4136b3ebb3058050d8f6347558d9e9d23ea82 | 32 RSQ dependencies, 32 publication nodes each for Q/K/V, and distinct scales in ViT |

The L61 address-map SHA is 325b9666d3a868a3a0e37c87a1c10b9056aba87fb8681d1b0ed565dce57f44cc, matching [the L61 row of the T640 bindings](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json). The split16 graph/contract corresponds to [the L27 row of front bindings](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json). These are structural and software consistency checks; the boundary between legacy MAP_CHECK_FAILED entries and named admitted instances is retained and not upgraded to a general map proof across all geometries. This round also read the seven split16 family prototype graphs for L25/26/28/29/30/56/57, none of which contain RSQ/RCP nodes; in L27, the 32 RSQ nodes belong to Q/K and the two RCP nodes belong to the subsequent [attention](APPENDIX_beginner_glossary.md#g039) denominator, with the latter covered in [L3.attention-softmax](L3_attention_softmax.md#window-attention).

<a id="norm-witness"></a>
## CPU Statistic First Sources and Absorption Witnesses for 027/028

Moved from [L3_norm_nonfinite.md](L3_norm_nonfinite.md); below is the record saved from the original writing round.

| Saved CPU witness | What it establishes | Limitation |
|---|---|---|
| 027 L6: 37824+30464=68288→+Inf; 028 L6: 35552+30784=66336→+Inf | The earliest observed nonfinite launch in both images is the positive summation in norm32 at L6 | These are intermediate statistics, not model coefficients; neither the earliest GPU cycle nor the sole source |
| norm branch of 027 L31 and 028 L27 | +Inf is absorbed within this branch via RSQ(+Inf)=[+0](APPENDIX_beginner_glossary.md#g070), finite components multiplied by zero, and E4 zero | Does not prove that the same Inf byte from L6 was stored and propagated all the way to L27/L31 |
| Both images continuing to L61 | Incur new finite half addition overflow and finite half squaring overflow respectively | Rejected by the legacy QKV wrapper; legacy diagnostics cannot be used to fabricate results for subsequent L62–L157 |

Each of the two images has 8,294,400 half input words with zero nonfinite inputs; across the observed prefix [L0](APPENDIX_beginner_glossary.md#g081)–L6, both the [workspace](APPENDIX_beginner_glossary.md#g082) and the six-[texture](APPENDIX_beginner_glossary.md#g027) SHAs match the accepted reference. [Diagnostic RESULT:7–25](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7) proves that the CPU observation path preserves these outputs, which cannot be used to claim that internal GPU bit patterns have been measured. Nor does the fact that all 45 legacy images stopped at the L27/L31 guards prove that the first source of every image has been traced to the same L6 node.

<a id="a1-ledger"></a>
## A1 Group Counts, Rejection List, and Build Identities

Moved from [L3_norm_nonfinite.md](L3_norm_nonfinite.md); below is the record saved from the original writing round.

| Legacy verdict | Image count | [A1](APPENDIX_beginner_glossary.md#g107) FINAL MATCH | A1 rejected |
|---|---:|---:|---:|
| MATCH | 99 | 99 | 0 |
| INVALID | 45 | 42 | 3 |
| UNCOMPARED | 3 | 3 | 0 |
| Total | 147 | 144 | 3 |

The guarded stopping points for the 45 legacy INVALID images are 33 at L27 and 12 at L31; see [ARCH 0.7:989, 1008–1014](../../../ARCHITECTURE_V3_ZH.md#L989). This round checked the 147 unique keys and prior→status counts in [image_verdicts_final.json](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/image_verdicts_final.json) read-only to obtain the table above, without reopening image targets or running the chain.

The remaining three images are all QMMA half overflow rejections in ViT attention:

| Registered image name | Rejection launch | Verdict |
|---|---:|---|
| heldout-091-saturation_blocks-02 | L77 | INVALID_REFUSED, QMMA half overflow, no final image |
| heldout-093-saturation_blocks-04 | L97 | Same as above |
| batch3-052-saturation_patches-1920x1080 | L72 | Same as above |

The guard resides at [qmma_sm120.hpp:65–70](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L65) and executes by default in production calls; see [A1 RESULT:46–56](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L46) for details. These three images do not count as MATCH, nor can they be uniformly exempted merely because other images in the same category pass.

**Source identities must be kept separate.** The A1 build is 14267c09ecef6a7a34068a42b8674da105c70370d199886d83183c50753fdcb3, the parent unified M is 9d0a4593…, and the scope is 1080 single-frame f0. The original finite-domain guards remain readable in public M2 at [split16:272](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp#L272) and [ViT:180, 200](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_qkv_projection_chain_r02/qkv_projection_impl.hpp#L180); the A1 results use the independent replacement source and binary above. The 144-image conclusion cannot be written as a new acceptance for M2, 1440, 4K, or multiframe runs. [ARCH 0.7:1425](../../../ARCHITECTURE_V3_ZH.md#L1425) likewise distinguishes these two identities.

<a id="padding-bug"></a>

The two event counts must not be conflated: early interpreter graphs reported 131,072 same-value zero-writes covering 4096 distinct 4 B addresses 32 times each, whereas the later typed publication contract merges repeated same-value writes into 4096 zero-overwrite items. Their address union and publication order are identical, and the earlier number cannot be called a different byte count. Early count and address [negative control](APPENDIX_beginner_glossary.md#g102): [attention port RESULT:143–146](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L143). Zero values in a native snapshot do not by themselves prove that zero-writes actually executed; that requires joint support from read/write events, ordering bindings, and disabled-write negative controls.
## L62 Zero-Overwrite Collector Omission and Repair History

Moved from [L3_workspace_map.md](L3_workspace_map.md); below is the record saved from the original writing round.


### L3.workspace-map.padding-bug Why 16 KiB Could Still Be Missed When Vector Coverage Passed

- What it is: The generator had already emitted zero-write events, but the collector and executor retained only ordinary output events, causing the [side effect](APPENDIX_beginner_glossary.md#g094) to go missing.
- Input → output: Ordinary [vector](APPENDIX_beginner_glossary.md#g076) maps that previously appeared complete → zero-write bindings carrying values, addresses, instances, and stages.
- How it is computed:
  ~~~text
  1. Native ordinary output already covers the physical P rows; the tail tile additionally has 4096 four-byte zero-writes.
  2. The defective collector included only ordinary outputs in templates/maps, retaining the zero-write "count" without executable items.
  3. The CPU consequently published computed padding; the first difference at 4K L62 was solely WS [665036800,665053184).
  4. The fix integrates the zero-writes as an independent typed operation executed after output publication and before release.
  5. The verifier checks all addresses, values, widths, tail tiles, epochs, instances, and ordering.
  6. The L62 negative control that independently disables zstore reproduces the exact same 16,384 B difference while the six textures still MATCH.
  7. With zstore enabled, the legacy standalone build continued from its own own61 across L62–L91, with all 30 launches MATCH.
  ~~~
- Numeric rules: Native before-and-after states in this region are both zero, so snapshots alone cannot distinguish "unwritten" from "same-value zero-overwrite". The typed [readset](APPENDIX_beginner_glossary.md#g093) of L63 proves that all 16 KiB of this region are genuinely read and cannot be called unconsumed dead [padding](APPENDIX_beginner_glossary.md#g085). Because the zero-writes lie inside the ordinary output [role](APPENDIX_beginner_glossary.md#g084) and add no new byte intervals, unchanged WriteSet / CumWrites metadata cannot substitute for value and stage verification.
- Why it is computed this way: Previously only the primary vector exits were verified, omitting scalar side effects that overlap the output; this shows that coverage checks must constrain both values and timing.
- How we know: MEASURED, [c12 RESULT:7–9](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7); CONTROLLED, [verify_zstore_p.py:3–49](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c11/a07/verify_zstore_p.py#L3) covers negative controls for wrong instance / parameters / address / value / width / epoch / stage, missing writes, duplicate writes, premature release, and so on.
- Next down: [Current Publication Wiring](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/runtime/vit_adapter_geometry_padded_zstore.py#L177), [Boundaries of WR](L3_workspace_map.md#wr).

The legacy diagnostics above retain MAP_CHECK_FAILED, and the diagnostic round itself neither repaired nor ran downstream launches; nor does the L62–91 gate of the legacy standalone build automatically transfer to the later merged seal. The later 4K L60–99 gate in M2 and the unified M three-frame chain have separate [named records](L3_workspace_map.md#evidence) and do not rewrite the legacy round's NOT_RUN entries as passed. A global side-effect / aliasing / lifetime theorem remains not established.

<a id="repack-evidence"></a>
## repack Native Grids, Software Dimension Scans, and Nonzero Pinning Rates

Moved from [L3_workspace_map.md](L3_workspace_map.md); below is the record saved from the original writing round.


## How repack Is Verified: What the 18 Grids and 8,082 Items Each Are

| Evidence | Checked object | Scope |
|---|---|---|
| [native_validate_new_formula.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/native_validate_new_formula.json) | 18/18 native input / output grids match, with 4K L58 padding compared separately | L58/L99×1080/1440/4K×f0/f1/f2 |
| [M2 RESULT:9, 28–32](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#3-repack-支持域回答-b1-要求) and [test program](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/tools/repack_equiv_test.py) | Legacy / new modules agree across 8,082 dimension×direction records | rows, cols=1..64, skipping grids where rows×cols×256>900000; includes rejection results |
| [equiv_old_maps.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/equiv_old_maps.json) | Read-only count in this round: out of 8,082 items, **440 valid mapping hashes and 7,642 rejection results** | The file also contains 4 thread / queue scheduling controlled comparisons and 3 parameter negative controls, for 8,089 entries in total; not 8,082 valid hardware shapes |
| [native_pinning_coverage.json](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/native_pinning_coverage.json) | Native nonzero content independently pins mapping positions, with 0 conflicts against the formula | 1080 84.375%, 1440 100%, 4K 94.4444%; the remainder is all-zero regions, so it cannot be claimed that every position is uniquely pinned by nonzero content |

The original report referred to 8,082/8,082 in shorthand as "mapping hashes"; the breakdown by actual saved test type is given above. The 18 grids are native byte comparisons, the dimension scan is a result comparison between the legacy and new software modules, and the mathematical acceptance domain is larger still; the three are not interchangeable. The new source code also checks the mapping bijection item by item, which constrains the indices themselves without equaling a hardware traversal of the full acceptance domain.

<a id="map-identity"></a>
## 1440 Address-Map Identity for L57

Moved from [L3_workspace_map.md](L3_workspace_map.md); below is the record saved from the original writing round.

The 1440 map SHA-256 is cce87defbdde26cb2a0a4d4cf76c0ece8dbb07cf7ac2140354456c080f89570c; this external local copy is a historical source for the geometry binding, and it cannot be assumed from the path name alone to be the entirety of M2 deployment assets.

<a id="b0-evidence"></a>
## B0 Sampling Experiments, Fusion Diagnostics, and Historical Acceptances

Moved from [L3_b0_input.md](L3_b0_input.md); below is the record saved from the original writing round.

<a id="evidence"></a>
## How We Know: Microbenchmarks, Failed Rounds, and B00 Gates Listed Separately

| Actual experiment round | What the saved results support | Limitation |
|---|---|---|
| parity-video-tex-filter-r04-20260928-codex; [frozen source STATUS:723](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/STATUS_ZH.md#L723) | Joint 8-bit fractional weights (1/256 fixed-point subpixel grid) microbenchmark on sm_75 / sm_86 has zero differences across 10,436 components; after integration, 320 q25x drops from 27,573→203 B and 1080 f1 from 765,813→73,119 B | Still DIFF; the original-round directory is not retained on this machine, so the numbers rely on the frozen summary without claiming to have re-read the raw microbenchmark output |
| [parity-video-sm120-tex-filter-r06-20260928-codex](../../../experiments/parity-video-sm120-tex-filter-r06-20260928-codex/RESULT_ZH.md#3-冻结假设族训练拟合) | Out of 180 pre-registered hypotheses, none achieves full MATCH on the training set, and the four S2 held-out items remain DIFF; 1080 f1 is 25,390 / 7,629 B | This round cannot uniquely attribute the difference to texture filtering; its original record of f2 being NOT_RUN due to a resource lock is retained and not overwritten by later rounds |
| parity-video-d3d12-tex-r07-20260929-codex; [frozen source STATUS:737](../../../experiments/parity-arch-doc-v2-r01-20261007-codex/sources/STATUS_ZH.md#L737) | 56 D3D12 / CUDA groups and 603,232 components on the local 2060; 48 [RGBA16F](APPENDIX_beginner_glossary.md#g028) groups are identical, with differences confined to the missing W component of RG16F | B0 [MV](APPENDIX_beginner_glossary.md#g023) reads only x/y; cannot extrapolate from Turing to sm_120; the original-round directory is not retained on this machine, so the basis is the frozen summary |
| [parity-proof-gpu-sweeps-r01-20261007-codex / Item C](../../../experiments/parity-proof-gpu-sweeps-r01-20261007-codex/ADJUDICATION_ITEMC_FULL_ZH.md) | Across 112 CUDA+63 D3D12 configurations on subsequent sm_120, 175/175 legacy coordinate prefixes match sm_75 | Typically 2,693 coordinates per configuration, with 32 for load controls; newly added coordinates lack a same-coordinate reference, so this is not an arbitrary raw32 / two-dimensional full-domain proof, and native runtime [descriptors](APPENDIX_beginner_glossary.md#g088) remain UNKNOWN |
| [parity-video-b00-native-divergence-r01-20261006-codex](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证) | Isolated B00 with corrected native [FMA](APPENDIX_beginner_glossary.md#g063) boundaries has 0 B difference on both [full](APPENDIX_beginner_glossary.md#g018) and pool across 1080 f0, f1, f2, and f3 | [teacher-forced](APPENDIX_beginner_glossary.md#g106) single launch; f4/f5 in that round are NOT_RUN_MISSING_NATIVE_HISTORY, and f3 history is supplied by f2 id9 from another capture rather than measured id6 from the same capture |
| [parity-cpp-1440-multiframe-r01-20261017-claude](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | Dual-fill 1080 f0–f5 and 1440 f0–f3 own-state chains on the 854 build, including per-frame B00 launch gates | At 1440, the six textures of f1/f2 are compared at only 5 native points in time; f3 has input translation and a cross-process seam from its own f2 checkpoint; not a full multiframe new measurement on M2 |
| [parity-cpp-4k-multiframe-r01-20261022-codex](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19) | Dual-fill unified M, each running f0→f1→f2 in a single process, including per-frame B00; f2 actually uses that fill's own f1 history | Early gates for A5 check that the written region equals native while the complement retains A5; 4K f3+ and independent history-perturbation studies are not run; arbitrary content or hardware equivalence is not inferred from chain gates |

**Root cause of the 25 KB residual.** 119 debug exports turned intermediate multiplications into mandatory rounding points, preventing FMA fusion in the native coordinate chain. Turning off the runtime debug switch still used the same compiled artifact, so sm_75 / sm_86 / sm_120 replays and the CPU could agree four ways while jointly diverging from native. Static recompilation after removing the debug exports restored fusion, bringing the isolated prototype's full / pool differences to zero across f0–f3, with no new GPU executions in that round. This conclusion comes from [native divergence RESULT:9, 24–28, 39](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据), and is not inferred from the filter-fitting failure of R06 alone.

Legacy [reset](APPENDIX_beginner_glossary.md#g032)-only / fixed-1080 notes are retained as of their original round dates; [guard 4](APPENDIX_beginner_glossary.md#g109) in current b00.hpp and the named multiframe gates have separate direct sources. The gates above constrain output trajectories without proving unique internal structure or automatically admitting the still-rejected p5 branch.

<a id="attention-evidence"></a>
## attention Saved Gates, Negative Controls, and Legacy Failures

Moved from [L3_attention_softmax.md](L3_attention_softmax.md); below is the record saved from the original writing round.


## Saved Native Gates, Negative Controls, and Open Scope

| Object | Records read and verdict | Supported scope |
|---|---|---|
| Eight ViT attention launches | [RESULT:115](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L115), [s02-validate-resume5.json](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/s02-validate-resume5.json): L62/67/72/77/82/87/92/97 on 1080 f0, both output and release63 MATCH | MEASURED, three-way native / Python / C++ comparison with bound per-launch inputs and parameters; not a continuous chain |
| Cross-geometry historical gate | [Same RESULT:275–282](../../../experiments/parity-cpp-step2b-attention-r01-20260928-codex/RESULT_ZH.md#L275): 71 of 72 grids THREE_WAY_MATCH; legacy 4K f0 L92 has a 1 B difference, NOT_ESTABLISHED | Legacy result retained; a sensitive boundary under a legacy QMMA candidate does not serve as a full-domain proof of the current rule; for primitive adjudication, see [L3.qmma-e4m3](L3_qmma_e4m3.md#候选如何从-1832-收敛到一个行为类) |
| 4K L62 zero-overwrite | [c12 RESULT:7](../../../experiments/parity-cpp-geo2-tin-diagnostic-r01-20261011-codex/resume16/resume16b/c12/RESULT_ZH.md#L7): standalone L62 negative control with zstore disabled reproduces the 16,384 B difference in workspace [665036800,665053184) while six-POST still MATCH; with zstore enabled, continuing L62–L91 from its own L61 yields an end MATCH | CONTROLLED, genuinely distinguishes "without zero-overwrite" from "with zero-overwrite"; matching POST is insufficient to claim the full workspace is identical |
| Later fixed 4K f0 chain | [continuation6_RESULT_ZH.md:1–10, scope section](../../../experiments/b1-arch-v3-refresh-r01-20261023-codex/continuation6_RESULT_ZH.md#L1): full workspace and six-POST match at every launch across L0–L157, including these eight attention launches | MEASURED, specific build segmented by SHA-verified own checkpoints and continued in new processes; cannot be used to overwrite the legacy L92 record above, nor does it imply unique asynchronous intermediate timing |
| split16 qkv | [Step2a RESULT:5–23](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L5), [s03-qkv.json](../../../experiments/parity-cpp-step2a-r01-20260928-codex/s03-qkv.json): L103/107/111/115/119/123/127/131, eight grids on 1080 f0 and 24 grids across three frames each on 1440/4K, totaling 56/56 MATCH | MEASURED, full-launch comparisons including fused attention; original MAP_CHECK_FAILED and scoped admission are retained as is, without calling this 56 general map proofs |
| [TIN](APPENDIX_beginner_glossary.md#g011) window implementation | [TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3): L3/7/11/18/24/133/134/151 on 1080 f0, 8/44 three-way full workspace identical; the remaining 36 in that round are NOT_RUN | MEASURED, eight named full launches; later fixed 4K f0 chain evidence is listed separately and cannot be backfilled to turn this round into 44/44 |
| Bias-indexing negative control | [RULEDOUT-ATTENTION-FRAGBIAS:23–31](../../../knowledge/RULED_OUT_ZH.md#ruledout-attention-fragbias): intra-tile ordering hypotheses on 2/4/8 heads and named B9/B15 mismatch by about 71% / 74% respectively, while logical ordering simultaneously has zero difference | CONTROLLED, originally registered scope is sm75 / branched_window; not extrapolated to 1 head, 16 heads, or all current families |

No dedicated RULED_OUT entry for "[libm](APPENDIX_beginner_glossary.md#g074) [softmax](APPENDIX_beginner_glossary.md#g047) replacement" was found that could be cited from the original registry, so no executed native negative control is fabricated. This slice uses the actual computation graphs and the synthetic example below to show that standard softmax differs in both operations and results; for the bit-pattern reasons why RCP cannot be casually replaced by libm, see [L4.mufu](L4_mufu.md#edges). Optimized C++ may alter loop organization across independent tasks; the half and QMMA dependency orders above are preserved, and [rearrangement](APPENDIX_beginner_glossary.md#g019) is permitted only where exact integer parts satisfy the corresponding rules.

<a id="norm-evidence"></a>
## norm Layered Evidence: Raw Values, Software Controls, Checkpoints, and Final Images

Moved from [L3_norm_nonfinite.md](L3_norm_nonfinite.md); below is the record saved from the original writing round.


## Which Layer Each Piece of Evidence Supports

| Layer | Evidence read | Supported conclusions and boundaries |
|---|---|---|
| CPU first source and local dependencies | [Propagation diagnostic RESULT:7–47](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7) | L6 first source and L27/L31 local absorption for 027/028; actual NaN reachability and nonfinite counts in unobserved intervals remain UNKNOWN |
| RSQ raw value at specific input | [Original table boundary](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/s11-old-table-boundary.json), [A1 RESULT:39–44](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L39) | Existing two-pass hardware fact of RSQ(+Inf)=+0; does not imply full-domain equivalence for general multi-operand nonfinite combinations |
| Software helper and threshold negative control | [A1 RESULT:44](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L44) | Zero failures across 8,593,757 items against an independent _Float16 reference; 2698 failures under the threshold-perturbation negative control. Belongs to software gates |
| A1 per-checkpoint | [A1 RESULT:25–30](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L25) | Two G1 images at eight points each, totaling 16 FULL workspaces; five G3 images across eight C8 windows each, totaling 40 identical FULL workspaces; inputs come from R04/C8 session translation and are relocated byte-identical |
| A1 final images | [A1 RESULT:18, 32–36](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L18) | 144/147 final images identical and 3 rejected; C8 six textures remain NOT_RUN_RAW_FILES_ABSENT; identical final images do not prove that +Inf also forms internally in native execution |
| Original per-launch gates of norm callers | [TIN RESULT:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3), [split16 RESULT:5–23](../../../experiments/parity-cpp-step2a-r01-20260928-codex/RESULT_ZH.md#L5), [ViT R09 RESULT:5–27](../../../experiments/parity-vit-t640-numeric-r09-20260925-codex/RESULT_ZH.md#L5) | Overall output comparisons on named instances support these finite paths; legacy per-launch gates cannot be upgraded into new A1 gates or proofs across all inputs |

The consequence bytes in A1 support the scoped semantics, while general multi-operand half combinations, NaN payload rules, and whether intermediate Inf/NaN are reachable on the GPU remain UNKNOWN per the original reports. In particular, "native execution also produces +Inf internally and absorbs it via RSQ" is INFERRED; having measured the standalone RSQ(+Inf) raw value and whether the network actually reaches that key internally are two distinct assertions.

<a id="history-evidence"></a>
## Result Ledger for Tail-Stage Three-Tier Multiframe, sceneA, and Scene Cuts

Moved from [L3_b70_history_output.md](L3_b70_history_output.md); below is the record saved from the original writing round.


## Multiframe Evidence: Compared Objects and Boundaries

| Named record | Measured result | Retained boundaries |
|---|---|---|
| [1080 Gate 2 / 854](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | f0–f5, dual-fill, all 948 events each MATCH; includes per-frame B70 / copy / display | Comparisons against G0b FULL / six textures and native cumulative declared write sets / roles are listed separately; not every point has a native FULL |
| [sceneA drill Stage R, 10-24](../../../experiments/parity-cpp-exam1080-r01-20261023-codex/STAGE_R_ZH.md#实测结果与时间) | 1080 f0–f31, 32/32 FINAL SHAs match the approved R02 catalog; fill00, 12 threads, single predictor, own state, 5056 launches | FINAL_SHA256_ONLY; not per-launch native state observations; f16–f31 [params](APPENDIX_beginner_glossary.md#g083) are synthesized from a frozen template by changing only the B0 frame word, not native captured parameters |
| [1440 multiframe](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) | f0–f3 dual-fill own-state chain; f0–f2 in a single process, f3 continued from its own f2 checkpoint | At f1/f2, the six textures have only five native points in time; f3 inputs undergo session translation and have a cross-process seam; f4/f5 NOT_RUN |
| [4K three-frame, 10-22](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L19) | Dual-fill unified M, each running f0→f1→f2 in a single process; 948 launches, 946 observed FULL points, 5688 six-texture POST points | Two f0 L0 FULL points unobserved; early A5 comparisons separate written regions / retained complements; f3+ NOT_RUN, and M2 identity is not conflated with new measurements on M |
| [scene_cut numeric round](../../../experiments/parity-cpp-1080-multiparam-r03-20261018-claude/RESULT_ZH.md#r1-结果2026-10-20决定-35) | 16-frame own-state chain FINAL identical byte for byte, with reset at f8; C1–C5 as above | FINAL only, with no per-launch native FULL / textures; does not constitute a pass for midstream f4+ or p5 |

The 32-frame conclusion for sceneA is bound to M9d / 854 numeric values and the listed inputs, parameter synthesis rule, initial state, and build; it neither claims a new 32-frame run on M2 nor infers unique hidden states across the board from matching final-image SHAs. The frozen Stage P status of original Stage R is not reopened here. What this round adds is only main text and the synthetic example below, with no new GPU, network, or continuous-chain runs.

<a id="mufu-evidence"></a>
## MUFU Native Full Domain, Cross-Architecture Summary, and Production Member Acceptance

Moved from [L4_mufu.md](L4_mufu.md); below is the record saved from the original writing round.


## What Full-Domain Measurements Actually Prove

| Record | Existing evidence | Boundary |
|---|---|---|
| 09-12 local seven families × FTZ/non-FTZ, 14 variants in total | Complete raw32 per variant, 512 blocks, two passes per block; legacy small half tables cross-checked via two arms (independent shape and full-sweep lookup), [probe RESULT:182–211, 233–251](../../../experiments/parity-mufu-probe-20260912/RESULT_ZH.md#L182) | Non-FTZ wrappers may reflect composite behavior and cannot be uniformly called the same bare function; trigonometric wrappers also involve range reduction |
| Same-day sm_75 vs. sm_120 | **7,168/7,168 block hashes identical and 14/14 pairs of frozen GPU program package SHAs identical**, [rental RESULT:15–38](../../../experiments/parity-blackwell-rental-20260912/RESULT_ZH.md#L15), [per-variant comparison JSON](../../../experiments/parity-blackwell-rental-20260912/a1-mufu-arch-compare.json) | Fixed measured configuration; package identity does not mean the kernel machine code loaded on the two architectures is identical; two legacy shapes were not covered; cannot be generalized to unmeasured wrappers, future drivers, or all network sites |
| Month 10 seven raw32 raw-value banks | 512 blocks for each of the seven families; SQRT/SIN/COS/RSQ re-verified across 24 containers and 2,048 blocks, [narrow resume4 RESULT:12–22](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume4-20261008/RESULT_ZH.md#L12) | Raw-value capture is kept separate from CPU/caller bindings; receipts from months 09 and 10 across devices/drivers cannot be combined into a single measurement |
| Month 10 actual production member bindings | 16,776,341 SQRT items, 15,468,894 items each for SIN/COS; RSQ accepts 30,705 half images, with zero differences in composed comparisons, [same report:5–22](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume4-20261008/RESULT_ZH.md#L5) | Out-of-domain rejections produce no numeric output; SIN/COS are compositions after proper prescaling, not independent full-domain proofs for each substep |
| Domain-extension candidates rcp/lg2/ex2 | rcp accepted and matched across all raw32; lg2 accepts $2^{31}$; ex2 accepts 2,248,015,875; the latter two match only on their acceptance domains, [candidate RESULT:25–38](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#L25) | Retains original validity and raw-value fallback on failing segments; cannot be written as all formulas passing across full raw32 |

This round actually re-read the [original sm_120 metadata](../../../rental-transfer/probe-suite.json) and the 14 saved sm_75 block summaries, recomputing the 7,168 hash-pair comparisons and 14 GPU program package identities, all of which matched. For the original paths and fields of the comparison algorithm, see [a1_mufu_arch_compare.py:13–40](../../../experiments/parity-blackwell-rental-20260912/a1_mufu_arch_compare.py#L13). This is a review of saved summaries, **without recomputing raw full-domain GPU outputs or adding new GPU executions**.

Hardware reports and full-domain connections across wrappers / [codecs](APPENDIX_beginner_glossary.md#g097) / call sites must still be kept separate. The qualifications in [V2-02-006](../../arch-v2/02.03_mufu.md#v2-02-006) remain in effect; the original hardware premise table retains per-caller binding conditions, [project axiom table:39–45](../../../experiments/parity-proof-program-r02-20261007-codex/resume12-20261009/delivery/AXIOMS_ZH.md#L39).

<a id="index-scope"></a>
## Original Named Builds and Measured Instance Scope from the Index

Moved from [INDEX.md](INDEX.md); below is the record saved from the original writing round.

In ARCH 0.7, T1080 is f0–f5 on the 854 build; T1440 is f0–f3 on 854, where f3 continues across processes from the CPU's own f2 checkpoint with session-translated inputs; T4K is single-process f0→f1→f2 per fill on unified M. New M2 numeric gates cover 1080/1440 f0 and 4K L0–L99, while the remaining correspondences cannot be rewritten as new measurements on M2; at 1440 f0–f2, the six native textures are observed at only five points in time and cannot be filled in as full per-launch observations. MEASURED / CENSUS: [ARCH 0.7 §9.5.1, §12.7](../../../ARCHITECTURE_V3_ZH.md#951-07-当前结果及完整scope-tokens).

The 10-24 sceneA drill adds a 32/32 FINAL SHA match across 1080 f0–f31: single process, own state, fill00, with f16–f31 parameters synthesized from a frozen template; this is FINAL-only evidence on M9d / 854 numeric values, not a new per-launch native-state gate on M2. For the history-consumption / reset controls of scene_cut and the three-tier multiframe scope, see the [tail-stage evidence table](L3_b70_history_output.md#evidence).

<a id="attention-example"></a>
## Complete Certification Script for TIN Score and RCP Computation

Moved from [L3_attention_softmax.md](L3_attention_softmax.md); below is the record saved from the original writing round.

~~~python
from pathlib import Path
import hashlib, struct, math
import numpy as np

RN16 = lambda x: struct.unpack("<e", struct.pack("<e", x))[0]
RN32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
bits16 = lambda x: struct.unpack("<H", struct.pack("<e", x))[0]
decode16 = lambda b: struct.unpack("<e", struct.pack("<H", b))[0]
H_add = lambda x,y: RN16(x+y)
asset = Path("mlxdlss/resources/rcp-domain.npz")
assert hashlib.sha256(asset.read_bytes()).hexdigest() == (
    "055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59")
with np.load(asset, allow_pickle=False) as z:
    ins = z["input_half_bits"].copy()
    rcp_half = z["native_half_bits"].copy()
    rcp_f32 = z["native_float_bits"].copy()
assert np.array_equal(ins, np.arange(0x0410, 0x7c00, dtype=np.uint16))

def Q8(x):
    # Finite nonnegative synthetic inputs only; nearest, ties to even code.
    def decode(c):
        e,m = c >> 3, c & 7
        return m*2.0**-9 if e == 0 else (1+m/8)*2.0**(e-7)
    return min(range(127), key=lambda c: (abs(decode(c)-x), c & 1))

def score(s, kind):
    if kind == "TIN":
        t = RN16(RN32(RN32(s*0.044921875)+1.30078125))
    else:
        # Chosen synthetic inputs have exact affine intermediates.
        t = RN16(s*0.044921875+1.30078125)
    t = min(max(t,1.03125),1.5693359375)
    return decode16(((bits16(t) << 5)+0x8000) & 0xffff)

def den(w):
    def leg(b):
        x = H_add(H_add(w[b],w[b+16]), H_add(w[b+4],w[b+20]))
        x = H_add(x,H_add(w[b+32],w[b+48]))
        return H_add(x,H_add(w[b+36],w[b+52]))
    return H_add(H_add(H_add(H_add(leg(0),leg(2)),leg(8)),leg(10)),
             H_add(H_add(H_add(leg(1),leg(3)),leg(9)),leg(11)))

s = [RN16(x) for x in (-8,-4,-2,-1,0,1,2,8)]*8
w = [score(x,"TIN") for x in s]
d = den(w)
ix = bits16(d)-0x0410
r = decode16(int(rcp_half[ix]))
raw = int(rcp_f32[ix])
assert bits16(RN16(struct.unpack("<f",struct.pack("<I",raw))[0])) == bits16(r)
p = [RN16(x*r) for x in w]
q = [Q8(x) for x in p]
textbook = [math.exp(x-max(s)) for x in s]
textbook = [x/sum(textbook) for x in textbook]
print("d",d,"d_half",hex(bits16(d)),"RCP_raw32",hex(raw),"r",r,"r_half",hex(bits16(r)))
for i in range(8):
    print(s[i],w[i],p[i],hex(q[i]),textbook[i])
print("sum_half_weights_in_real_arithmetic",sum(p))
print("max_difference_from_textbook",max(abs(x-y) for x,y in zip(p,textbook)))
assert w == [score(x,"split16") for x in s]
~~~

<a id="norm-example"></a>
## Original-Function Computation Script for Synthetic 32-Channel Normalization

Moved from [L3_norm_nonfinite.md](L3_norm_nonfinite.md); below is the record saved from the original writing round.

~~~python
from pathlib import Path
import ast, hashlib
from types import SimpleNamespace
import numpy as np

source = Path("mlxdlss/sm120_b1.py")
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "f4ada69da4ec60be36f09b05560a0fd0240a147721a20a0b51d7001518089d31")
tree = ast.parse(raw.decode("utf-8-sig"))
names = {"_norm_squared", "_rsq", "normalise"}
chosen = [n for n in tree.body
          if isinstance(n, ast.FunctionDef) and n.name in names]
assert {n.name for n in chosen} == names
module = ast.Module(
    body=[ast.ImportFrom(module="__future__",
                         names=[ast.alias(name="annotations")], level=0), *chosen],
    type_ignores=[])
env = {"np": np, "_RSQ_FIRST_CODE": 0x0410,
       "UnsupportedByBackend": RuntimeError}
exec(compile(ast.fix_missing_locations(module), str(source), "exec"), env)

asset = Path("mlxdlss/resources/rsq-domain.npz")
assert hashlib.sha256(asset.read_bytes()).hexdigest() == (
    "06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62")
with np.load(asset, allow_pickle=False) as z:
    keys = z["input_half_bits"].copy()
    floats = z["native_float_bits"].copy()
    table = SimpleNamespace(rsq_half_bits=z["native_half_bits"].copy())
assert np.array_equal(keys, np.arange(0x0410,0x7c01,dtype=np.uint16))

# Artificial vector and gain, not model values.
x = np.array([[1,-2,3,-4]+[0]*28], dtype=np.float16)
out,n = env["normalise"](x,table,scale=np.float16(1))
r = env["_rsq"](n,table)
ix = int(n.view(np.uint16)[0])-0x0410
print("source_sha256",hashlib.sha256(raw).hexdigest())
print("n",n.tolist(),"n_bits",[hex(int(b)) for b in n.view(np.uint16)])
print("rsq_f32_bits",hex(int(floats[ix])),"r",r.tolist(),
      "r_bits",[hex(int(b)) for b in r.view(np.uint16)])
print("first4_half",out[0,:4].tolist(),
      "bits",[hex(int(b)) for b in out[0,:4].view(np.uint16)])
print("real_sum_of_published_half_squares",float(np.sum(out.astype(np.float64)**2)))

with np.errstate(over="ignore",invalid="ignore"):
    zero = np.zeros((1,32),dtype=np.float16)
    high = np.full((1,32),48,dtype=np.float16)
    z = env["_norm_squared"](zero)
    h = env["_norm_squared"](high)
print("zero_floor",float(z[0]),hex(int(z.view(np.uint16)[0])))
print("synthetic_48_group_stat",hex(int(h.view(np.uint16)[0])))
try:
    env["_rsq"](h,table)
    raise AssertionError("unchanged reference unexpectedly accepted +Inf")
except RuntimeError as e:
    print("unchanged_reference",str(e))
print("saved_RSQ_Inf_row",hex(int(floats[-1])),
      hex(int(table.rsq_half_bits[-1])))
~~~

<a id="ffn-r04b"></a>
## r04b FFN: Concrete Graphs, Channel Derivation, and Real-Computation Identities

This section presents the read-only checks and synthetic CPU scalar examples newly added in r04b; new GPU, model, and continuous-chain runs are all 0. The "this round" context of other historical sections remains unchanged. For the main text, see [L3.ffn](L3_ffn.md#ffn).

### Channel Basis for split16 FFN

The L25 and L29 graphs each split into three stages by matrix A source: original input S, Q(pre-projection matrix result), and Q(G result); taking the wload_off indices of the B sources together with their byte offsets counts the set of weight addresses without reading weight values. This gives 32768 B for pre-projection, 16384 B for expansion, and 16384 B for contraction per group, and 262144/131072/131072 B respectively across all groups. The original-order K32 chains give K=512/64/256; combined with 512 E4 per position at the exit and the fetch grouping, this yields a 512→512 pre-projection and eight groups of 64→256→64. Logical grouping is an interpretation of these concrete graphs; it does not equal the 16 attention heads and does not constitute a general geometric theorem.

Every gate in L25/L29 is the same half min/max→abs→two fma→mul→Q sequence, and the final multiplication retains the unclamped input. The L26/L30 graphs do not have another G; the first matrix C source is mul([D8](APPENDIX_beginner_glossary.md#g061)(same-block entry), half scale), with 16 K32 steps carrying that seed and Q at the end. The layouts and role sources of the first block and consecutive blocks are pinned by L25/26/29/30 in front bindings respectively. In this round, the actual SHAs of all four wiring files and four address maps match those bindings; any mismatch would halt execution without patching the evidence.

### Slicing Basis for ViT contract

In the T640 prototype, the matrix chains of the four live templates 0/1/2/3 are 32 K32 steps each. The slice 0 seed contains mul of dq(block entry) and the half scale, writing the half buffer; slices 1/2 start from zero and add to the buffer in half in order; slice 3 starts from zero, adds to the buffer in half, and then applies sat to E4. The physical buffer is P×2048 B and the primary output is P×1024 E4; "2048" cannot be used to infer a halving of gated channels.

### Reading Boundaries of Existing Numeric Records

- expand: [formal resume4 result:289](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L289) aggregates 72 independent P3 runs; [full release and Python boundary:137](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L137) and [padding:220–224](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L220) preserve each role. Its "formal full-chain result" heading is not interpreted as 72 continuous network chains.
- contract: [legacy L60 four-role gate:3–8](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L3) and [resume7 format migration:404](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L404) are distinct snapshots; the legacy 71 NOT_RUN cells and MAP_CHECK_FAILED are not rewritten by the current M2 full-frame results.
- split16: the [B27–B29 record](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3) on two public 320×240/reset samples contains 48 single-segment / intra-block chain comparisons across three blocks; only the [FFN](APPENDIX_beginner_glossary.md#g037) launch citations are taken from it, without mixing standalone qkv gates into the FFN denominator.
- M2: the [release numeric record](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) covers 1080/1440 f0 and 4K L0–L99; following the INDEX convention, it distinguishes reference FULL / six textures, named native comparison points, and FINAL, without claiming to directly observe the internal [activations](APPENDIX_beginner_glossary.md#g045) of every G.

### Synthetic Examples and Complete Identities in This Round

The [source-extraction / compilation script](../skewer/examples/ffn_r04b.py), [actual stdout / compiler / function list](../skewer/examples/ffn_r04b.result.json), and [graph and channel accounting](../skewer/examples/ffn_r04b.wiring.json) are reusable. The program extracts only pure scalar functions from the original C++ and calls the original QMMA header; temporary builds are not written into the release source tree. An initial dynamically linked binary failed to launch, while the final statically linked binary ran and returned PASS; the launch failure does not count as an arithmetic result. Across all 63488 finite half encodings, B0/TIN/ViT G produce identical outputs; the synthetic gate + K32 residual byte table, the half reordering example, and the ViT nonfinite rejections are also listed, none of which are new native gates.

| Actually read source / graph | SHA-256 |
|---|---|
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.npz) | fc4cc52f301b72a67ba7667372bff51127607512d87846091f1187b61342f7a0 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L25-lane.wiring.json) | 4a19d31ece96b382228c0a3c20fbebbe1dd55b144ac9addd58a73db8544d4910 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.npz) | d7a30db1b0a6de967aec37873544965eeedaa828a6ac7dd090dbc9f2a957be74 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L26-lane.wiring.json) | 998f5e5729490cf269385a3f1fdcbf2b8bdf6b5b0d370cb8b05a1cd315755e66 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.npz) | 209764facb72c75f27760465eb9075fc7829765b2cb30ae8b2b12405748ad6f5 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L29-lane.wiring.json) | 3b03345e3c9b1969e4992fc2cfd7ef4c140ffee389e4a62f867cb6f040223639 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.npz](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.npz) | c8979c9ab482d4f166b8af8c735aba5a662075f4e0219d063e5049880de470d7 |
| [dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json](E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L30-lane.wiring.json) | 3364fc7bfa55fef2d1b482e20076294c4c2c766182d7ec034ddf890eebd2f530 |
| [dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json](F:/dlssnr-work/l60-generalize-t640-r01-claude/pred/maps/l60-templates-and-checks.json) | c7ebf67032c860ece07fe64ac0a8d5f849913f441cb42fea16c4ac5ad9e0b62a |
| [experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json) | 65c4120d1bf9b136508ef0a3154b67c0c0d1906bd13e8f0a391e83248140c541 |
| [experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json](../../../experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json) | f81dc2374c601d0432d8e7488fa7a6086b1551caa592adbcf4d9eb68e25c16dc |
| [GlassBox-NR/cpp/chain_entry_optm/b00.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp) | 932e0c805f020420f0e6fad9543d3e1710d0561b6afa14a30263d6f9bd939392 |
| [GlassBox-NR/cpp/chain_tin_optm/tin.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp) | 371d33d205655f75c809f0f9990a8054edf8e930a31733f72dbf916f87b4f1f8 |
| [GlassBox-NR/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp) | fe67bb0dc7c878e69291798425c77a3c3f013863e11f36a48e533323ede40287 |
| [GlassBox-NR/cpp/chain_tin_optm/qmma_sm120.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp) | 2b85ddfaeb37eb5d16560224def629ff29a043c4421b5b571749103b398e5452 |
| [GlassBox-NR/cpp/chain_entry_optm/mapexec_base.hpp](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp) | 0ac19678e7b4a31857434ffda3b250f508c98e76970485b3c70f7948b65eeb60 |
| [GlassBox-NR/cpp/chain_tin_optm/primitives.inc](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc) | 5e5519dbbe41145146487512337401631ac8342c74f7357ba7ab781219a4c48e |

The function bodies of the shared half/E4 helpers were also checked item by item: after ignoring whitespace/comments and unifying equivalent bit-copy wrapper names, B0, TIN, and ViT are identical; the cached quantization path uses the unmodified reference construction, without treating a storage optimization as a different arithmetic.

For the SHA of the generated C++, full compiler identity, and raw stdout, see the result JSON above; this round did not re-run legacy proofs, GPU primitives, or network chains.

<a id="tin-window-r04c"></a>
## r04c Complete TIN Window Block: 44 Configurations and Evidence Boundaries

The main text is [L3.tin-window](L3_tin_window.md#tin-window). This section adds only CPU source reading, actual content/SHA checks across the 44 1080 default params files, and organization of existing records; it did not read model coefficients or target workspaces, did not run any GPU, model, native invocation, or CPU network chain, and did not recount legacy measurements as results of this round.

### Identities Actually Read in This Round

| Source or binding | SHA-256 |
|---|---|
| [TIN implementation](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp) | 371d33d205655f75c809f0f9990a8054edf8e930a31733f72dbf916f87b4f1f8 |
| [Legacy 44-launch bindings](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/s00-bindings.json) | 55bdba63b3324c410c3983b90fffb51d176bcd39fe9daff3e1f3ac963e103fbc |

The [per-launch check record](../skewer/examples/tin_window_r04c.bindings.json) preserves all 44 actual params paths, SHAs, B/launch numbers, C, peripheral types, W/H, signed origins, input/output layouts, previous-tier dimensions, and pool/[skip](APPENDIX_beginner_glossary.md#g016)/completion-flag fields, with verdict ALL_44_PARAMS_SHA_AND_FIELDS_MATCH. Every actually read params SHA equals the expected value in the legacy bindings above, and the extents/origins and saved fields also match item by item, without modifying the bindings to eliminate differences. The full SHAs of the source file and bindings are listed in that same JSON.

These 44 items are exactly L3–L24 and L133–L154, consisting of 4 [inpview](APPENDIX_beginner_glossary.md#g022), 28 chained, 4 ds_wait, 4 upsample, and 4 outview_wait launches. The eight-row scale/direction table is compiled from these named configurations; in particular, B56/L141 has origin (−4,0) and cannot be guessed by restarting the four-phase cycle at each tier. This check closes only the consistency of these 1080 parameter identities and fields, and does not establish support for arbitrary geometries, arbitrary controls, or unknown parameter versions.

### Wiring Basis and Implementation Tier

[window:130–135](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L130) explicitly constructs the entry residual seed first and runs FFN, then quantizes the FFN result, projects Q/K/V, normalizes Q/K, runs attention, and finally executes the output projection using the scaled FFN bypass as seed. The 1-head attention bypass takes the unquantized half value, whereas multi-head takes the decoded value after E4 publication; [upsample and window fetching:151–159](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L151) additionally causes B66 to retain the unquantized merge as the FFN seed. This describes the numeric decomposition of the CPU implementation; native internal representation uniqueness cannot be inferred from matching exits.

[norm/attention:114–127](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L114) pins the 32-channel heads, the Q/K sum-of-squares lower bound, direct V publication, separate F32 multiplication/addition for scores, the half denominator tree, RCP, and the two K32 steps of AV. [pool:162–175](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L162) performs three half additions and one quarter multiplication from the unquantized core result, converting to E4 first and then projecting C→2C; C=256 additionally preserves the zero-write range on related planes. Layout decoding/encoding, zero-padding, and completion flags belong to actual peripheral behavior; kernel names by themselves are not proofs of synchronization semantics.

### Legacy Numeric Gates Cannot Be Added to a Configuration Census

The 8/44 in [TIN R01 result:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3) are per-launch teacher-forced comparisons on L3, L7, L11, L18, L24, L133, L134, and L151; each covers the entire 212,519,936 B workspace, with C++, Python, and the named native reference in agreement. The remaining 36 items stay NOT_RUN in that legacy record and are not upgraded because 44 params files were read in this round. Nor are the 380 static/layout checks, 5 synthetic window tests, and 3 invalid-input rejections new native gates.

In legacy L134, C++ once equaled Python while both differed from native by 640 B; what was missing was the explicit zero-write across 160 completion slots. Only after the adapter layer supplied it was the saved three-way agreement obtained; [legacy failure and fix:25–27](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L25) is retained, without treating "two reconstructions agree" as that legacy version having passed against native. It was not re-run in this round.

[M2 release numeric record:1–3](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) subsequently covered all 158 launches of 1080/1440 f0, and thus includes all 44 TIN launches of each; the new M2 numeric scope for 4K covers only L0–L99, while L100–L157 underwent only a configuration census. Compared objects continue to follow the INDEX convention in distinguishing CPU reference FULL / six textures, named native observations, and FINAL; later multiframe results for unified M are listed separately—see [tail evidence scope](L3_b70_history_output.md#evidence)—and are not relabeled as new M2 measurements in this round.

The [computed-shared](APPENDIX_beginner_glossary.md#g108) symbolic provenance tier of L133 remains NOT_ADMITTED, and B69's independent native layout remains UNKNOWN. Complete synchronization, aliasing, lifetime, general geometries, and uniqueness of internal values are not established by the numeric gates above; these unknowns remain preserved along with the main text.

<a id="split16-window-r04d"></a>
## r04d Complete split16 Block and Two Supplementary Diagrams: Identities and Reading Boundaries

For the main text, see [complete split16 block](L3_split16_window.md#window-attention); the supplementary diagrams are in [L100 dataflow](L2_06_decoder_bridge.md#wiring) and [repack permutation / 4×4 tile](L3_workspace_map.md#repack-diagram) respectively. This round read only source code, named params, graphs/indices, and saved results, and evaluated small integer illustrations; it did not read model coefficients, network inputs, or target workspaces, and performed no new GPU, model, native invocation, or CPU full-chain runs.

### Source Identities Actually Read in This Round

| Source or binding | SHA-256 |
|---|---|
| [front bindings](../../../experiments/parity-cpp-bindings-front-r01-20260928-codex/s00-bindings-front.json) | 65c4120d1bf9b136508ef0a3154b67c0c0d1906bd13e8f0a391e83248140c541 |
| [tail bindings](../../../experiments/parity-cpp-bindings-tail-r01-20260928-codex/s00-bindings-tail.json) | 5939bc86c36559800d06d9496b992b13f1d3c5f98fa46e387480f9abe2a3fa2e |
| [split16 role executor](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/split16.cpp) | 284d2629e3282d7f759453f8c99bd158552da36f19913a869001b7899bc3417f |
| [split16 scalar-graph executor](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_split16_optm/scalar_map.hpp) | 20610eaa92c3bada615647abd5d2ce5989f7186374b83d1aaeb7c4d4dff3a50a |
| [L100/L132 execution entry](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp) | c9f1977d816c5e65757625a59859f6673578920ab7b69127efdc92e5870d313e |
| [repack closed form](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp) | 8d721e2dc8d4a2530a92548c0e19a4f4854dc9ef6652e75472a269bf2480663b |

The [check record for this round](../skewer/examples/split16_window_r04d.bindings.json) preserves the paths/SHAs, role byte lengths, and producers for all 65 actual params files across L25–L57 and L101–L132, and additionally lists the valid 60×36 dimensions and signed origins for the 16 qkv launches. All 65 SHAs equal the saved front/tail bindings; the main-path, original block-entry bypass, and post-feed-forward bypass pointers within the 16 blocks all match item by item, without modifying the bindings to eliminate differences.

The same record preserves the 26 actual map/graph asset SHAs and NPZ array headers for 13 representative launches: L25/26/27/28/29/30/31/35/39/56/57/132/100. Every actual SHA matches the corresponding saved binding; this is not a new symbolic admission across the full graphs of all 65 launches. The parameters of L100 and L133 were additionally checked by SHA against tail; L58 and L99 were read directly only as handoff endpoints with their current SHAs recorded, without separately checking their legacy reference pins in this round. The five additional handoffs are L56.pool→L57, L57→L58, L99→L100 main path, L56.full→L100 skip, and L132→L133 main path, all of which had their actual parameter pointers checked.

### Output Projection and Intra-Graph Subchains

This round checked the matrix seed dependencies in the graphs and then read the integer sources in the respective maps of L28/L56/L132, without reading the numeric payloads pointed to by those sources. Across all three graphs, the initial seed of every chain is an E4 source decoded and multiplied by a half scale; there are 1,105,920 active seed byte references in each, and every item falls within the second role of the concatenated input, i.e., the current block's post-feed-forward bypass in the saved bindings. This provenance check does not replace complete proofs for Read_ws / weight read sets, aliasing, or lifetime.

| Concrete graph | K32 subchain lengths split by preceding matrix seed dependency: count | What it supports |
|---|---|---|
| L27 / L31 / L35 / L39 | 16 steps: 48 chains; 1 step: 32 chains; 2 steps: 16 chains | Connects with the documented order of Q/K/V projection, QK, and AV; graph SHAs checked for each of the four origins |
| L28 | 16 steps: 16 chains | Every output projection starts from the scaled bypass half and is then carried at each K32 step |
| L56 / L132 | 16 steps: 32 chains | Dual-exit and terminal-view launches each have their own graph and source selections; no new network axis is invented from "32" |

These are inventories of symbolic fragments inside the concrete graphs, not logical matrix row counts, head counts, or counts of independent numeric evidence; a complete closed form for the physical axes remains not established. For the FFN channel basis, continue to see [r04b](#ffn-r04b); for Q/K reduction and scores/AV, see [norm bindings](#norm-bindings) and [attention bindings](#attention-bindings), without recounting these sub-items as new gates in this round.

### Scope Supported by Each of the Two Diagrams

[entry.cpp:58–75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/entry.cpp#L58) generates 8-step K32 partial sums from A_src/B_off; each item of REDMAP selects three F16 values and adds the first two terms first and then the third term. OUTMAP then selects the other partial-sum path, the skip position, and the scale source, performs a half addition first, then applies h_fma with B30.full, and finally publishes E4; F16 scratch storage and the control region are written separately. The diagram draws only the confirmed projection/reduction/merge steps, without attributing [nearest-neighbor](APPENDIX_beginner_glossary.md#g021), convolution, or a new network head axis to L100.

[repack.cpp:26–50, 88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26) gives the respective closed forms for the 2D [tile](APPENDIX_beginner_glossary.md#g087) and sequence group, the shared π, and the bidirectional 4 B transfer. This round's integer illustration verified that π is a permutation across all 4096 indices and saved the 16 corresponding addresses at c=0 for the top-left 4×4 tile at 1080; 256 B→32,768 B at t=32 comes from this closed form without executing on payload data. For the denominators of saved native/mapping gates, continue to see [repack evidence](L3_workspace_map.md#repack-evidence); an integer bijection is not upgraded to a new native controlled comparison.

### Named Numeric Records and Retained Unknowns

The [legacy 1080 B25–B30 result](../../../experiments/parity-gemini-1080-chain-r03-20260922/RESULT_ZH.md#L3) is a 25-launch continuous segment across L33–L57, including full/pooled of L56 and L57; it stops at B30 and does not include ViT. Another [legacy B27–B29 result](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3) consists of 48 single-segment / intra-block chain comparisons on two public 320×240/reset samples, with no cross-block continuous-chain conclusion. The inputs, resolutions, and denominators of both are preserved separately.

The [M2 numeric scope](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) subsequently covered all 65 split16 launches of 1080/1440 f0; its new 4K numeric runs reached only L99, while the decoder and L100/L132 underwent only a configuration census in that M2 round. Later multiframe runs for unified M, named native observations, reference FULL / six textures, and FINAL continue to be listed separately per [INDEX](INDEX.md) and [tail evidence](L3_b70_history_output.md#evidence), and are not relabeled as new measurements in this round.

Independent ordering of the 16-head bias, complete physical axes, general maps/synchronization/aliasing/lifetime, and uniqueness of internal values remain UNKNOWN; original MAP_CHECK_FAILED statuses are preserved per named graph/geometry. The nonfinite contract and M/A1 version boundaries follow the original text, and this round did not expand the acceptance domain.


<a id="ffn-gate-history"></a>
## Historical Breakdown of Per-Launch FFN Gates

| FFN site | Saved numeric gates (one line each) |
|---|---|
| Eight ViT expand launches | [Formal resume4:289–291](../../../experiments/parity-cpp-step2b-ffn_expand-r01-20260928-codex/RESULT_ZH.md#L289): all 72 named per-launch P3 (per-launch numeric comparison stage) runs MATCH; output/padding and full release are listed separately, and Python full release remains NOT_COVERED_BY_PYTHON; not 72 own-state continuous chains |
| Eight ViT contract launches | [Legacy standalone gate:3–8](../../../experiments/parity-cpp-step2b-ffn_contract-r01-20260928-codex/RESULT_ZH.md#L3): three-way agreement across four roles on L60 1080 f0, with the remaining 71 legacy NOT_RUN cells retained; the eight launches have separate per-launch comparisons in the [named M2 f0 gate](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) without backfilling the legacy round, and MAP_CHECK_FAILED remains governed by named admission |
| split16 ffwd/ffwd_proj | [Legacy B27–B29 gate](../../../experiments/parity-astra-opus-split16-b23-b30-20260913/revisions/r04-b27-b29/RESULT_ZH.md#L3): two-sample single-segment / intra-block chain MATCH on L41/42, 45/46, and 49/50; [M2](../../../experiments/parity-cpp-m2-release-clean-r01-20261020-claude/RESULT_ZH.md#L1) covers all launches of these families on named f0, and the 56-cell gate of qkv cannot be borrowed to serve as a feed-forward gate |
| FFN inside TIN fused launches | [TIN gate:3–23](../../../experiments/parity-cpp-chain-tin-r01-20260930-codex/RESULT_ZH.md#L3): three-way full-launch agreement on 8/44 named launches in the original round, with the remaining 36 NOT_RUN, including L18/134 chained; each internal G was not measured independently, and later M2 gates are listed separately |
| FFN inside B0 / B70 | [B0 isolated gate](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证) shows zero teacher-forced differences on f0–f3 full/pool, and the [named tail gates](L3_b70_history_output.md#evidence) include L155; both verify full-launch exits without treating small examples or internal traces as independent GPU activation observations |


<a id="half-integer-implementation"></a>
## Integer Implementation and Proof Engineering of half T1

## How Portable Integer T1 Preserves Both Rounding Stages

Here we cite this project's frozen implementation and experiment records; external explanatory documents are not treated as sources of fact, nor is experimental T1 treated as the default implementation in the current public modules. The std::fma branch remains directly visible in the latter.

A finite input decodes to signed $m_a2^{e_a}$: subnormals take the mantissa field with unit −24, and normals take 1024+m with unit E−25. [T1 source:52–54](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L52).

```math
P=(m_a m_b)\,2^{e_a+e_b+48},\qquad
Q=m_c\,2^{e_c+48},\qquad
N=\left|\,\pm P\pm Q\,\right|.
```

P and Q are integers; the source code uses two uint64 limbs to perform shifts, addition with carry, subtraction with borrow, and comparisons, with $P<2^{80},Q<2^{64},N<2^{81}$. Zero sums are handled separately: nonzero cancellation yields +0, and −0 is preserved only when both terms are negative zero. [T1 source:75–95](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L75), [proof RESULT:9–11](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/RESULT_resume2_v1_ZH.md#L9).

~~~text
If N=0: take the exact zero-sign branch.
top=floor(log2 N).
top≤52: send N*2^−48 directly to the integer half publisher.
top>52:
    shift=top−52; sig=N>>shift; rem=N−(sig<<shift); tie=2^(shift−1).
    Apply RN-even once to sig according to rem/tie and the parity of sig.
    Send sig*2^(shift−48) to the integer half publisher, preserving the carry when sig=2^53.
The publisher applies RN-even again according to the target half grid step, handling subnormals, normal-boundary crossings, and overflow.
~~~

The first stage corresponds to [T1 source:96–103](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L96), and the second stage is [source:14–41](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L14). Integer addition and multiplication also have direct unit-grid / significand-product implementations in [source:55–73](../../../experiments/parity-cpp-hfma-proof-r01-20261002-codex/resume2/source/integer_half_recon.hpp#L55); the full-domain proof conclusion in this section refers specifically to the h_fma composition.

[Verification Record] The saved proof connects the behavior of integer T1 and software T0 across all raw F16 triples (including exception categories and messages), with verdict PROVED; it is not a proof of the internal GPU implementation. Full decoding, exact two-limb composition, two RN-even stages, zero sign, nonfinite classification, and deliberate-corruption controls are all premises of the proof.

The trust boundary still includes IEEE correctly rounded std::fma, a round-to-nearest-even environment, double/integer ABI, the compiler, the solver, and source-to-model correspondence; historical UNKNOWN statuses are not directly upgraded to UNSAT. The std::fma branch remains visible in the current public default modules, and experimental T1 does not impersonate the default implementation. [Proof leaf/representative counts, controls, source SHAs, and original review records](APPENDIX_evidence_history.md#half-proof) have been moved to the appendix; this round did not re-run the proof driver or solver.


<a id="half-example-source"></a>
## Complete Program and Raw Output of the half Synthetic Example

~~~python
import math
import struct

# Artificial inputs only. No project imports, model files, or GPU calls.
def hv(h):
    s = -1 if h & 0x8000 else 1
    e, m = (h >> 10) & 31, h & 1023
    if e == 31:
        return math.nan if m else s * math.inf
    return s * math.ldexp(m if e == 0 else 1024 + m, -24 if e == 0 else e - 25)

def hr(x):
    sign = (struct.unpack("<Q", struct.pack("<d", x))[0] >> 48) & 0x8000
    if math.isnan(x):
        raise ValueError("NaN half publication outside measured domain")
    if math.isinf(x) or abs(x) >= 65520:
        return sign | 0x7c00
    a = abs(x)
    if not a:
        return sign
    _, e = math.frexp(a)
    step = max(e - 11, -24)
    q = math.ldexp(a, -step)
    n = math.floor(q)
    rem = q - n
    n += rem > .5 or (rem == .5 and n & 1)
    rounded = math.ldexp(n, step)
    if rounded >= 65536:
        return sign | 0x7c00
    if rounded < 2**-14:
        return sign | n
    _, out_e = math.frexp(rounded)
    mant = int(math.ldexp(rounded, 11 - out_e))
    if mant == 2048:
        out_e, mant = out_e + 1, 1024
    return sign | ((out_e + 14) << 10) | (mant - 1024)

def add(a, b):
    return hr(hv(a) + hv(b))

def mul(a, b):
    return hr(hv(a) * hv(b))

def fma(a, b, c):
    return hr(math.fma(hv(a), hv(b), hv(c)))

def rshift(v, sh):
    if sh <= 0:
        return v << -sh
    q, r = divmod(v, 1 << sh)
    tie = 1 << (sh - 1)
    return q + (r > tie or (r == tie and q & 1))

def ipack(v, exponent, sign):
    if not v:
        return sign
    e = v.bit_length() - 1 + exponent
    if e > 15:
        return sign | 0x7c00
    q = rshift(v, max(e - 10, -24) - exponent)
    if not q:
        return sign
    if e < -14:
        return sign | q
    if q == 2048:
        q, e = 1024, e + 1
    return sign | 0x7c00 if e > 15 else sign | ((e + 15) << 10) | (q - 1024)

def finite_t1(a, b, c):
    def dec(h):
        e = (h >> 10) & 31
        assert e != 31
        return (h & 1023) + (1024 if e else 0), e - 25 if e else -24
    ma, ea = dec(a)
    mb, eb = dec(b)
    mc, ec = dec(c)
    ps, cs = (a ^ b) & 0x8000, c & 0x8000
    p, q = (ma * mb) << (ea + eb + 48), mc << (ec + 48)
    net = (-p if ps else p) + (-q if cs else q)
    if not net:
        return ps & cs
    sign, v = (0x8000 if net < 0 else 0), abs(net)
    sh = max(v.bit_length() - 1 - 52, 0)
    return ipack(rshift(v, sh), sh - 48, sign)

a, b, c = 0x3c01, 0x3bff, 0xbc00
fused, separated = fma(a, b, c), add(mul(a, b), c)
print(f"FMA={fused:04x} MUL_ADD={separated:04x} T1={finite_t1(a,b,c):04x}")
print(f"ties={add(0x3c00,0x1000):04x},{add(0x3c01,0x1000):04x}")
print(f"subnormal_ties={hr(2**-25):04x},{hr(3*2**-25):04x},{hr(-2**-25):04x}")
print(f"subnormal_to_normal={hr(1023.5*2**-24):04x} negative_zero={add(0x8000,0x8000):04x}")
print(f"overflow={hr(65519):04x},{hr(65520):04x},{hr(-65520):04x}")
x, y, z = 0x6800, 0x3c00, 0xe800
print(f"atomic_orders={add(add(x,y),z):04x},{add(add(x,z),y):04x}")
f32 = lambda u: struct.unpack("<f", struct.pack("<I", u))[0]
print(f"F32_to_F16={hr(f32(0x3f801000)):04x},{hr(f32(0x3f801001)):04x}")
for triple in [(a,b,c), (0x0400,0x7400,0x1000), (0x3c00,0x7bff,0x5000),
               (0x8000,0x3c00,0x8000), (0x7bff,0x7bff,1)]:
    assert fma(*triple) == finite_t1(*triple)
assert (fused, separated) == (0x0ffe, 0x0000)
~~~

Actual stdout in this round:

~~~text
FMA=0ffe MUL_ADD=0000 T1=0ffe
ties=3c00,3c02
subnormal_ties=0000,0002,8000
subnormal_to_normal=0400 negative_zero=8000
overflow=7bff,7c00,fc00
atomic_orders=0000,3c00
F32_to_F16=3c00,3c01
~~~

An independent Fraction check also verified the exact fraction for the fusion example, and Python struct F16 conversions checked the finite publications, midpoints, and overflows above; all matched. T0 and the finite T1 demonstration agree across the five named synthetic/control triples. This round performed no new GPU, model, or full-chain runs, and did not redo the complete software proof.


<a id="e4-example-source"></a>
## Complete Program and Raw Output of the E4 / K32 Synthetic Example

~~~python
# Synthetic operands only; no model files, imports, or GPU calls.
def lg(n):
    return n.bit_length() - 1 if n else -99

def dec(b):
    if b & 127 == 127:
        raise ValueError("E4M3 NaN code")
    e, m = (b >> 3) & 15, b & 7
    u = (8 + m) << (e - 1) if e else m
    return -u if b & 128 else u

def seed(h):
    e, m = (h >> 10) & 31, h & 1023
    if e == 31:
        raise ValueError("nonfinite QMMA seed")
    u = (1024 + m) << (e - 1) if e else m
    return -u if h & 32768 else u

def pub(z):
    if not z:
        return 0
    sign, a = (32768 if z < 0 else 0), abs(z)
    top = lg(a)
    sh = max(top - 10, 0)
    q, r = a >> sh, a - ((a >> sh) << sh)
    if sh and (r > 1 << (sh - 1) or
               (r == 1 << (sh - 1) and q & 1)):
        q += 1
    if q >= 2048:
        q >>= 1
        top += 1
    if top < 10:
        return sign | q
    E = top - 9
    return sign | 31744 if E >= 31 else sign | (E << 10) | (q - 1024)

def dot(A, B, C=0, model=False):
    assert len(A) == len(B) == 32
    c = seed(C)
    E, exact, largest, least = (lg(abs(c)) - 24 if c else -99), c, abs(c), None
    terms = []
    for a, b in zip(A, B):
        x, y = dec(a), dec(b)
        t = x * y * 64
        terms.append(t)
        exact += t
        largest = max(largest, abs(t))
        if t:
            least = abs(t) if least is None else min(least, abs(t))
            E = max(E, max(lg(abs(x)) - 9, -6) + max(lg(abs(y)) - 9, -6))
    sh = max(E - 1, 0)
    def place(x):
        return (-1 if x < 0 else 1) * ((abs(x) >> sh) << sh)
    z = place(c)
    for t in terms:
        z += place(t)
    if abs(z) >= 1 << 52:
        raise ValueError("QMMA accumulator outside exact range")
    if not model and largest and least is not None:
        top = lg(largest) - 24
        span = lg(largest) - lg(least)
        cancel = lg(largest) - lg(abs(exact)) if exact else 99
        if top >= 12 and span >= 20 and cancel >= 2:
            raise ValueError("D27 QMMA counterexample domain")
    h = pub(z)
    if not model and h & 31744 == 31744:
        raise ValueError("QMMA half overflow")
    return h

def pad(xs):
    return xs + [0] * (32 - len(xs))

def e4_from_units(z, sign=0):
    a = abs(z)
    c = min(range(127), key=lambda c: (abs(a - (dec(c) << 15)), c & 1))
    return (128 if z < 0 or sign else 0) | c

a, b = pad([0x38, 0x01, 0x01]), pad([0x38, 0x28, 0x01])
whole = dot(a, b)
first = dot(pad([0x38, 0x01]), pad([0x38, 0x28]))
split = dot(pad([0x01]), pad([0x01]), first)
print(f"same_K32={whole:04x} split_K32={split:04x}")

cancelled = dot(pad([0x78, 0xf8, 0x01]), pad([0x38, 0x38, 0x01]))
print(f"grid_cancel={cancelled:04x} exact_sum_RN={pub(64):04x}")

a, b = pad([0x38, 0x28, 0x01]), pad([0x38, 0x28, 0x01])
h = dot(a, b)
exact_units = sum(dec(x) * dec(y) * 64 for x, y in zip(a, b))
print(f"F16_then_E4={h:04x}->{e4_from_units(seed(h)):02x} direct_E4={e4_from_units(exact_units):02x}")

lo_a, lo_b = pad([0x78, 0xc8, 0xb8]), pad([0x78, 0x48, 0x38])
hi_a, hi_b = pad([0x78, 0xc8]), pad([0x78, 0x48])
print(f"65519_RN={dot(lo_a, lo_b):04x}")
for label, aa in [("65520", hi_a), ("minus65520", [x ^ 128 for x in hi_a])]:
    try:
        dot(aa, hi_b)
    except ValueError as err:
        print(f"{label}={err}; model_bits={dot(aa, hi_b, model=True):04x}")
assert (whole, first, split, cancelled, h) == (0x3c01, 0x3c00, 0x3c00, 0, 0x3c40)
~~~

Actual stdout in this round:

~~~text
same_K32=3c01 split_K32=3c00
grid_cancel=0000 exact_sum_RN=0040
F16_then_E4=3c40->38 direct_E4=39
65519_RN=7bff
65520=QMMA half overflow; model_bits=7c00
minus65520=QMMA half overflow; model_bits=fc00
~~~

Independent fraction/conversion checks additionally confirmed that A is 262273/262144→0x3c01, the first half is 2049/2048→0x3c00, C is 278529/262144→0x3c40, and 65519→0x7bff; the unplaced sum of Example B converts to F16 as 0x0040, and the difference between direct E4 and two-step E4 was also recomputed using exact distances. These verify this example and the source transcription, without establishing new full-domain hardware conclusions.


<a id="norm-propagation-detail"></a>
## 027/028 and A1 Nonfinite Propagation History

### L3.norm-nonfinite.path Initial Source at L6 and Rejection Points at L27/L31

- What it is: Finite inputs can produce +Inf during squaring / positive half summation, and subsequently be absorbed by the original RSQ table or rejected by the domain guard of another wrapper.
- Input → output: Traced finite half inputs of 027/028 → +Inf temporary statistic in L6; whether it is rejected afterward depends on the actual route and interface.
- How it is computed:
  ~~~text
  Finite x → half squaring/sum overflow → n=+Inf
  RSQ supporting this key: +Inf → F32 +0 → half +0
  If x_i and γ are finite: x_i × +0 → signed zero → scaling → E4 zero
  Legacy split16 / ViT finite-domain wrappers: +Inf → guard rejection, with no comparable downstream output
  ~~~
- Numeric rules: The ε max lower bound preserves +Inf. Absorption of finite x multiplied by zero cannot be generalized to permit Inf×0; the latter can produce NaN and still requires separate primitive-domain and actual reachability evidence.
- Why it is computed this way: The original TIN RSQ table already includes the final entry mapping input +Inf to output +0; the legacy split16 loader/guard excluded this key. The same statistic therefore yields different acceptance outcomes.
- How we know: MEASURED (CPU side-channel), [nonfinite propagation diagnostics RESULT:7–15, 29–47](../../../experiments/parity-cpp-nonfinite-propagation-diag-r01-20261009-codex/RESULT_ZH.md#L7); whether native execution internally produces the same temporary values remains UNKNOWN.
- Next down: [New Semantics and Counts of A1](L3_norm_nonfinite.md#a1), [half Overflow Threshold](L4_half_arith.md#half-arith).

[Verification Record] The saved 027/028 witnesses trace to a CPU L6 statistic overflow, where subsequent local vector norms can absorb +Inf into zero; later at L61 a new overflow occurs and is rejected by the legacy wrapper. This neither proves that the same Inf byte propagates all the way through nor measures the same temporary values inside the GPU (UNKNOWN). [Raw numeric values, prefix agreement, and limitations](APPENDIX_evidence_history.md#norm-witness) have been moved to the appendix; no results are fabricated for unobserved intervals after legacy rejections.

### L3.norm-nonfinite.a1 42 of 45 INVALID Recovered, Three Remain Rejected

- What it is: In an independent child seal, A1 supplies the scoped +Inf statistic semantics, re-executes the original 147-image verification, and retains the QMMA rejection boundary.
- Input → output: Legacy 99 MATCH / 45 INVALID / 3 UNCOMPARED → 144 FINAL MATCH / 3 INVALID_REFUSED / 0 DIFF.
- How it is computed:
  ~~~text
  1. entry / split16 RSQ special-cases half +Inf: returns F32 +0.
  2. ViT QKV allows +Inf results from add/mul/max and their prescribed fused forms to continue flowing.
  3. ViT RSQ special-cases F32 +Inf: returns F32 +0, preserving the original half-precision publication points.
  4. −Inf, NaN, other out-of-table keys, and unadmitted operations continue to be rejected; RCP does not expand its domain.
  5. Advance each image again to the final image or the first guard rejection, recording each separately.
  6. If the half output of QMMA is nonfinite, the production path still rejects without producing a final image.
  ~~~
- Numeric rules: The half overflow threshold under RN-even is magnitude ≥65520; 65504 is the largest finite half, not the overflow threshold for exact real inputs. A1 neither changed the half reduction to F32 nor deleted failing images or adjusted expected bytes.
- Why it is computed this way: RSQ(+Inf)=+0 already has independent raw-value evidence; it allows the path where "a finite vector's statistic overflows and is absorbed" to continue. General nonfinite results and mixed topologies in QMMA require a separate body of evidence and cannot be admitted alongside it.
- How we know: MEASURED / CONTROLLED, [A1 RESULT:5–54](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/RESULT_ZH.md#L5), [A1 modification diff](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/NF_A1_SOURCE.diff); scoped branch source code: [A1 scalar_map.hpp:272](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/src-M/new/scalar_map.hpp#L272), [A1 qkv_projection_impl.hpp:165–205](../../../experiments/parity-cpp-nonfinite-a1-r01-20261018-claude/src-M/new/qkv_projection_impl.hpp#L165).
- Next down: [Evidence and Boundaries](L3_norm_nonfinite.md#evidence), [QMMA Publication Guards](L4_e4m3_and_k32.md#publish-guards).

[Verification Record] For the recovered images and three rejections in A1, see the [complete counts and identity ledger](APPENDIX_evidence_history.md#a1-ledger). All three were rejected due to ViT attention QMMA half overflow at L77/L97/L72 respectively, producing no final image, and cannot be counted as MATCH or exempted by category; for the default production guard, see [qmma_sm120.hpp:65–70](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L65).

A1 uses an independent replacement source/build scoped to 1080 single-frame f0; the finite-domain guards of public M2 are not updated as a result, and this cannot be transferred as a new acceptance for M2, 1440, 4K, or multiframe runs.

Raw values of RCP and caller admission must also be kept separate: legacy [SEMANTICS:17](../../../experiments/parity-cpp-half-rsq-rcp-domain-diag-r01-20261008-codex/SEMANTICS_ZH.md#L17) already recorded the two-pass +0 raw value for prospective RCP(+Inf), whereas the A1 report still chose not to model a domain extension for RCP. This text records its rejection according to the actual A1 branch, without expanding the report's summary of "no evidence" into "no RCP raw value was ever captured."


<a id="r04f-scope"></a>
## Documentation Revisions and Example Run Scope

r04f modifies only the documentation in this directory and synthetic scalar examples; new GPU, model, and continuous-chain runs are all 0, and no legacy experiments or software proofs were re-run. Identical run-scope declarations previously placed on individual pages are consolidated here. The domains of applicability for specific observations, rejections, and unknowns are retained.

- L3_attention_softmax.md: This round consists only of documentation, address/graph consistency checks, and the synthetic arithmetic above; new GPU / model / continuous-chain runs are all 0.
- L3_ffn.md: The output for x=5 differs from that for x=4, directly verifying that "only the factor is clamped, not the final x." The same program also calls the real H+ on synthetic half slices [2048,1,−2048,1]: the original order yields 0x3c00 (1), whereas swapping the middle slices yields 0x4000 (2); this illustrates the order sensitivity of step-by-step half rounding and is not a new native negative control. The ViT gate actually rejects synthetic +Inf/−Inf/NaN. The full program also covers x=−5 and all three G implementations across all finite half inputs; this round involves only small CPU arithmetic, with new GPU/model/full-chain runs all equal to 0.
- L3_split16_window.md: Full SHAs, matrix-chain checks, and the sources of the two supplementary diagrams are in the [r04d evidence appendix](APPENDIX_evidence_history.md#split16-window-r04d). Function-table domains and nonfinite boundaries continue to follow the [norm contract](L3_norm_nonfinite.md#nf-path) and named M/A1 statuses, without expanding support from this page. New GPU, model, and full-chain runs in this round are all 0.
- L3_tin_window.md: Positive vector-norm reduction can overflow to +Inf; whether it is absorbed by a specific RSQ interface is determined by the [nonfinite contract](L3_norm_nonfinite.md#nf-path), and is not written as "finite inputs guarantee all internal values are finite." Nonfinite QMMA seeds / half overflow, E4 NaN, missing-table / out-of-domain inputs, and unsatisfied parameter/interval/window-canvas guards are still rejected, and the saturating quantization of G cannot be used to let a preceding step pass. Full SHAs, per-launch configurations, and correction records for legacy publication omissions remain in the [TIN evidence appendix](APPENDIX_evidence_history.md#tin-window-r04c). New GPU, model, and full-chain runs in this round are all 0.
- L3_workspace_map.md: The extra P−T rows at 4K are still accounted for separately under the [padding contract](L3_workspace_map.md#padding): L58 writes zeros, and L99 moves only the logical T rows; the padding role cannot be drawn as a bidirectional pair of valid [tokens](APPENDIX_beginner_glossary.md#g041). The diagram and integer example come from [repack.cpp:26–50, 88–102](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/fam_repack/repack.cpp#L26); this round checked only the closed form and integer example without running new payloads or GPU gates, and [complete identities](APPENDIX_evidence_history.md#split16-window-r04d) remain in the appendix.
- L4_fp32_ftz.md: | Small example in this round | CONTROLLED: [real C++ output](../skewer/examples/fp32_ftz_r04e.result.json) checks synthetic RN/[RZ](APPENDIX_beginner_glossary.md#g060), input FTZ, and guards; new GPU, model, and full-chain runs are all 0 |
- L4_mufu.md: This verifies selected table entries, decoding transcription, half publication, and a libm counterexample, without re-verifying all compressed entries or the full raw32 data. New GPU / model / full-chain runs in this round are all 0.


<a id="attention-scope-detail"></a>
## Scope Supplements for Legacy attention Gates

[Verification Record] ViT and split16 have named per-launch native/Python/C++ comparisons; in the original TIN round only a subset of named launches were measured, while the rest remain NOT_RUN. In legacy cross-geometry ViT, 4K f0 L92 still retains 1 B DIFF / NOT_ESTABLISHED; the original MAP_CHECK_FAILED statuses of split16 are not upgraded to a general map proof. Later full-chain gates for fixed 4K segmented at own-state checkpoints and resumed in a new process neither rewrite these legacy records nor prove that asynchronous intermediate timing is unique. [Original gates/denominators/negative controls and scopes](APPENDIX_evidence_history.md#attention-evidence) have been moved to the appendix.

Disabling the L62 zero-overwrite detects a workspace difference while the six-POST textures remain identical, so POST cannot substitute for FULL; legacy negative controls for bias indexing are restricted to the registered multi-head / legacy paths and are not extrapolated to all families. There is no named negative control that can be cited from the original registry as a "libm softmax replacement," so none may be fabricated as having been run; the actual graphs and the synthetic examples below show that the algorithms differ. Floating-point dependency order is preserved, and only exact integer parts satisfying the rules may be rearranged.


<a id="qmma-source-ledger"></a>
## Line-Level Source Code and Legacy Experiment Correspondence Table for QMMA

| Assertion | Current public source path:line | Experiment / adjudication record |
|---|---|---|
| Matrix segments are fetched by byte; packing layout is kept separate from numeric decoding | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:12](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L12), [same file:26–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L26) | CENSUS; [ARCH 0.7 §7.1](../../../ARCHITECTURE_V3_ZH.md#71-数字格式与转换) |
| seed may come from the caller; K advances by 32 each time, with the previous step's F16 fed back to the next step | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:88–100](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L88) | [Port RESULT:15–19](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#单元门), [RULE:17–22](../../../experiments/parity-qmma-sm120-adjudication-r01-20261006-codex/resume3-20261007/RULE_ZH.md#可读规范-q_star) |
| When the target macro is sm_120, raw / decoded explicitly delegate to the same rule | [GlassBox-NR/cpp/chain_tin_optm/primitives.inc:125–128](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L125), [decode_reuse.inc:11–13](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/decode_reuse.inc#L11), [qmma_sm120.hpp:69–74](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/qmma_sm120.hpp#L69) | [Port RESULT:7–17](../../../experiments/parity-cpp-qmma-sm120-port-r01-20261007-codex/RESULT_ZH.md#实现与定位); source branches do not substitute for actual build identity |
| F16 matrix result and subsequent E4 publication are two separate steps | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:98–104](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L98), [primitives.inc:68–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/primitives.inc#L68) | [Half-domain primitives RESULT:43–45](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md); for second-format rounding, see lower-level synthetic Example C |
| Matrix encodings are E4, while auxiliary scales/biases are still read as F16 or F32 | [GlassBox-NR/cpp/chain_tin_optm/tin.cpp:34–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_tin_optm/tin.cpp#L34) | CENSUS; the storage/computation summary in [ARCH 0.7 §7.1](../../../ARCHITECTURE_V3_ZH.md#71-数字格式与转换) must be qualified per field; coefficient values are not listed |


<a id="topic-inventory"></a>
## Mapping Between Pages and Same-Page Steps

After r04f there are 38 Markdown pages: INDEX 1, L0 1, L1 10, L2 10, L3 9, L4 5, and Appendices 2. Page count is not a proof that all primitives are fully explained or that all evidence is closed.

| Level | Standalone page | Navigation topics covered on the same page |
|---|---|---|
| L3 | [qmma-e4m3](L3_qmma_e4m3.md#qmma-e4m3) | QMMA and ordered K32 matrix chains |
| L3 | [b0-noise-reprojection](L3_b0_input.md#b0-noise-reprojection) | B0 input, input-adapter, and noise; B0 [reprojection](APPENDIX_beginner_glossary.md#g025) of temporal-sampling |
| L3 | [ffn](L3_ffn.md#ffn) | Single-input G, channel/matrix accounting, and feed-forward residuals |
| L3 | [tin-window](L3_tin_window.md#tin-window) | Four-tier complete TIN window block and encoder/decoder periphery |
| L3 | [window-attention / split16](L3_split16_window.md#window-attention) | Four-kernel complete split16 block, 16 heads, layouts, and terminal variants |
| L3 | [attention-softmax](L3_attention_softmax.md#attention-softmax) | ViT/window scores, half reduction, RCP, and AV |
| L3 | [norm-nonfinite](L3_norm_nonfinite.md#norm-nonfinite) | tin-norm alias; Q/K vector norms, scales, and nonfinite contract |
| L3 | [workspace-map](L3_workspace_map.md#workspace-map) | repack, role layouts, read/write and padding, and publication |
| L3 | [b70-history-output](L3_b70_history_output.md#b70-history-output) | B70 sampling of temporal-sampling, output-temporal, postprocess, history saving, and display |
| L4 | [hmma](L4_hmma.md#hmma) | F16 adapter / terminal head, K16 grid points, and hardware boundaries |
| L4 | [half-arith](L4_half_arith.md#half-arith) | half-fma alias; F16 arithmetic, two-stage fusion, and ordered publication |
| L4 | [mufu](L4_mufu.md#mufu) | Wrappers, certified maps, and acceptance domains of the seven function families |
| L4 | [fp32-ftz](L4_fp32_ftz.md#fp32-ftz) | F32 entry/exit points, FTZ, rounding, compilation, and conversion examples |
| L4 | [e4m3-format](L4_e4m3_and_k32.md#e4m3-format) / [qmma-k32-accumulation](L4_e4m3_and_k32.md#qmma-k32-accumulation) | e4m3 alias; format and K32 accumulation share a single page |


<a id="r04f-review-resolution"></a>
## Item-by-Item Handling of the Two R2 Reviews (r04f)

The C/G numbers below correspond to the "ten questions" in [Codex R2](../reviews/REVIEW_OUTSIDER_R2_codex_20261024.md) and [Gemini R2](../reviews/REVIEW_OUTSIDER_R2_gemini_20261024.md), respectively. They are not new experiment numbers. The document continues to separate current CPU rules, prior hardware observations, and open questions. Old task labels such as Stage R/P have been removed from the architecture text; their original names are retained here only for comparison with the reviews.

| Review item | Handling | Specific location and boundary |
|---|---|---|
| C1 Cross-layer contradictions | Fixed | L1/L2 follow L3; TIN shared seed, split16 projection first seed, B0 controls 10–12, and fixed 13/14 for p5=false are synchronized; unknown physical layout remains unknown |
| C2 Observable images and two controls | Gap retained; image set not made | See the image evidence conditions below; L0 states the numerical effects and display boundary without guessing the visual task |
| C3 Attribution to object | Fixed | INDEX starts with only four identities; native behavior / CPU reconstruction / verification record labels are explicitly separated, and the binary64 block for half starts by identifying it as a CPU rule |
| C4 HMMA arithmetic leaf | Added | [L4.hmma](L4_hmma.md#hmma): F16/K16, seed, common grid, publication, rejection, cross-architecture, real C++ example; the 480 negative-zero counterexamples retain their original label |
| C5 Object of upsampling scaling | Fixed | L1.08 and L2.08 consistently use the projection main path plus scaled skip, namely HF(D8(skip),s_skip,projected_main) |
| C6 L1 too dense | Fixed | The ten pages now use function / stage shape / order / exception cards; table axes, binary64, and repeated basic definitions were moved out |
| C7 Entry identity / engineering history | Fixed | DLL, sm_120, sample C, and WEIGHTS_HT are explained on the first screen; the engineering glossary was moved to a separate table later in INDEX, while detailed builds and page statistics remain in the appendix |
| C8 ViT and window AV example | Added | [Side-by-side example](L3_attention_softmax.md#parallel-av-example): the same synthetic score/V is computed through each φ, denominator, and two real K32 steps to the exit; the difference is not attributed entirely to quantization position |
| C9 Evidence hard to read | Fixed | ViT, FFN, QMMA, and attention text uses four columns: assertion / direct evidence / comparison scope / limitations; prior-round counts and map status remain in the appendix |
| C10 Storage / proof overcrowding | Moved | The half two-limb T1 and full program, E4 full program, MUFU negative axis / LG2 / member pruning, and B0 format / decoding guards were moved to the existing appendix; rounding, rejection, and unknowns remain in the main text |
| G1 Engineering code on the front page | Fixed | Same as C7; following the explicit r04f requirement, the full project glossary remains under a separate heading later in INDEX, no longer preceding the architecture entry point |
| [G2](APPENDIX_beginner_glossary.md#g110) L56/L100 spatial correspondence | Partially supplemented; independent coordinates not fabricated | [L100 actual reads](L2_06_decoder_bridge.md#byte-trace) give the four source channel groups for physical output 0 and the known main-path (0,0); L56 gives the unique write event for pooled byte 0. Independent logical coordinates at both ends remain UNKNOWN |
| G3 Repeated inline definitions | Fixed | Basic definitions across L1, L2.05, and the other named L2 pages were consolidated in INDEX/L0; example shapes and launch counts remain |
| G4 Undefined jargon | Fixed | computed-shared/I03b/027/028/P3 are defined in the glossary later or moved to the appendix; six-POST is explicitly identified as id1/2/3/6/9/10 in the L0 resource table; Stage R/P was moved out of the main text |
| G5 φ bit-field mechanism | Added | [Score transform](L3_attention_softmax.md#vit-score) explains E=15, cancellation of fixed terms modulo, and m<<4/5 entering the new exponent/mantissa fields, with a synthetic c=1.5 example; no training-design name is assumed |
| G6 Six-texture and control quick reference | Added | The [L0 resource table](L0_frame.md#textures) gives ID / role / format / size / writes / reads and params effects; no mask is guessed for unused IDs |
| G7 Mixed params notation | Fixed | B0/B70 text consistently uses param_f32/u32/u64[hexadecimal byte offset]; F32 and integer interpretations are separated without changing the cited source |
| G8 Old sections / placeholders | Fixed | Old 3a/3b/3d/3e navigation names were updated; the obsolete MUFU placeholder sentence was deleted; INDEX distinguishes completed pages from missing primitive arithmetic / proofs |
| G9 Diary and invalid-link assessment | Diary moved down; deletion of valid links not adopted | Run counts and revision receipts were consolidated in the appendix; current boundaries remain in the main text. The examples exist, and all local / cross-drive links and fragments passed checks, so usable evidence links were retained |
| G10 ViT template and intra-block diagram | Fixed | [L2.05](L2_05_vit.md) now has a shared contract + six-row variant table + B31 five-kernel diagram, including the 640×2048 B half buffer and two residuals |
| Recheck of older items from both reviews / structural suggestions | Merged and implemented | Complete FFN/TIN/split16 intermediate layers and existing diagrams are retained without creating another architecture; in the overall FFN diagram, seed enters the contraction matrix / first shard box directly; generalized "why" claims were changed to page-level explanations of unknowns, retaining only specific speculation |

**Why the image display was not adopted and what would close the gap.** This round indexed only existing PNG filenames under safe paths and spot-checked the [old native-sample receipt](../../../experiments/results/native-sample/run.json). That receipt is terminated/native timeout; output.png in the same directory cannot prove a valid final image for the current fixed object. This does not claim that no other images exist anywhere on the disk. The materials read do not contain a directly reusable image / difference set with complete identity binding for the same input, same history, and two control changes. The DLL/resources, input color/MV conventions, params, history state, native output, and display transform should be bound before displaying those saved images. This documentation round generates no new model / native / continuous-chain results and does not fill the gap with arbitrary old PNGs.

**Boundary of the coordinate example.** The new example did perform integer map lookups and inverse indexing of the established L99 rearrangement. It did not read weights or tensor values. It adds a checkable example of "which byte came from where"; directly naming an L56 or L100 output physical byte as logical (x,y,c) still requires independent endpoint layout calibration. Independent native markers / provenance witnesses should be checked item by item against CPU layouts at both ends; the same map cannot prove itself. The minimum closure conditions for the independent B69 layout are also in L2.08. A general provenance / synchronization proof for computed-shared remains NOT_ADMITTED.

**Execution scope.** The new [HMMA](../skewer/examples/hmma_r04f.py) and [attention AV](../skewer/examples/attention_av_r04f.py) examples compile only extracted scalar functions and execute synthetic data; the [map example](../skewer/examples/map_trace_r04f.py) reads only integer address assets and first checks the bound SHA. Old experiments, models, coefficients, numeric implementations, and protected materials were not modified; new GPU / model / continuous-chain runs were all 0, with no staging, commit, or push.

**Acceptance.** All 38 Markdown pages are reachable from L0; 1,356 local links and fragments passed checks. All 41 original coverage comments remain, each of the 158 launches L0–L157 is covered once, and the 44 kernel names are unchanged; the contents of the original 8 Python code blocks remain unchanged. The three new examples actually ran and passed, and 9 source / function-table / map identities matched on recheck. The official release scan covered 51 files: PASS, BLOCK 0, 0 naming violations, and 0 missing files; two protected old wordings did not return. No changes from this directory were staged.


<a id="project-terms"></a>
## Project and Verification Terms

These are evidence-identity and engineering terms. Consult them when reading result tables; they are not tensor axes or network layers.

| Term | Meaning in this project |
|---|---|
| M / M2 | Unified CPU seal / its release sub-seal; readers must bind results to named builds. The existence of code does not mean that version has passed every numeric gate. |
| unified seal | A frozen delivery binding build, source, and asset identities; not a native model name, and it does not automatically include later workstreams. |
| 854… / M9d | An old build digest prefix / a shorthand for a numeric workstream; used to bound measured results, not a logical layer or new M2 acceptance. |
| A1 | A separate supplementary branch for nonfinite statistic semantics; its admissions and rejections cannot be taken to mean that the public M2 has been updated. |
| D03/D02 (also E1, D) | CPU function asset pruning / raw-value storage (LG2 / noise encoding) workstreams; they help distinguish function behavior from how it is saved. |
| G0b / G1 / G3 / C8 | An old CPU reference with narrowed map indices / A1 checkpoint gate / A1 checkpoint gate / capture window; none is a network layer. Check inputs and denominators against the reports. |
| "Decision NN" | A project decision number; identifies the source of a rule or authorization, not an additional hardware observation. |
| teacher-forced | Injects a saved reference prior state at each launch; it can check that launch but cannot replace continuous advancement of CPU own state. |
| WR A/B | A checks stability of self-reported written_ranges; B(i) checks that native changed bytes fall within the self-reported ranges, and B(ii) checks that CPU bytes outside the ranges remain unchanged; these do not replace a complete read/write set, aliasing, or synchronization proof. |
| FULL / FINAL / ROLE (also D) | Entire workspace / final image / named role comparison (D is the cumulative declared write set); the scope is needed to interpret MATCH. |
| NOT_OBSERVED | No native observation exists at that comparison point; it cannot be filled in as MATCH, DIFF, or "not executed." |
| CENSUS / MEASURED / CONTROLLED / INFERRED / PROVED | Source reading, named measurement, controlled comparison, inference, named software proof; the last does not mean the GPU implementation has been proven. |
| computed-shared | Proof of write→read provenance and valid reads for computed shared intermediate values; the old L133 prover still lacks general operand lineage, synchronization, and independent simulation semantics admission. Numeric MATCH does not lift NOT_ADMITTED. These independent checks and negative controls must be added; rerunning only the final-image comparison is insufficient. |
| I03b | The 2026-09-19 adjudication number for the B70 history-sampling blocker; later output gates advanced, but there is no complete written evidence of how the blocker was lifted. See [B70 scope](L3_b70_history_output.md#evidence). |
| 027/028 | Two image sample numbers used for nonfinite diagnostics, not network layers / launches; see the [historical witness](APPENDIX_evidence_history.md#norm-propagation-detail). |
| P3 | The per-launch numeric controlled-comparison stage in old executor acceptance; not a network level. |
| Stage B / E4 | The 156-launch route in the parameter-change workstream; E4 is a tone0/style0 capture, not an alias for the E4 number format |
| G2 | A 1080 face/[skin-mask](APPENDIX_beginner_glossary.md#g006) reset 2-frame capture; shards divide native observations |
| G4 | A final-image capture of a 1080 face sequence of 16 frames; intermediate workspaces were not captured |
| L1_1of2 / L1_2of2 | Two capture shards of the same 1080 3-frame control sequence; prediction processes are independent and CPU state cannot be stitched together |
| D1 | Work stage for the p5 temporal implementation without an additional aux texture and its control / SFU admission |
| D2 | Instance switch / feature rebuild work stage; not a network layer number |
| D3 | 312 B post_block parameter-layout work stage; not an alias for the 156 route |
| R0 | Reset control interpretation withdrawn before CPU numeric execution; not matrix residual r or exponent E |
| R1 | Finite reset child candidate: when p5, [structure](APPENDIX_beginner_glossary.md#g005)=1 and mask takes the two F32 values in CB |
| R2 | Child candidate for the p5 temporal implementation without an additional aux handle |
| R2b | Exact S157 control-tuple predicate extension; no formal seal was created after reach STOP |
| R2c | Child candidate that recertifies four S157 sites on the R2 implementation; its final state is bound to its execution seal |
| job AM-S2 | The old job label in the source record was Q8; a 320×240 automask/structure=2 sample. This skewer consistently uses job name AM-S2; Q8(x) refers only to quantization |
| job S1 | A 320×240 skin-face 8-frame sample; do not confuse it with the identically named map product number in another section |
| job G1-320 | G1 in the source parameter-change record: a 320×240 face/skin-mask 9-frame sample; distinct from the old A1 checkpoint gate G1 |
| six-POST | Comparison of the valid regions of the six textures id1, 2, 3, 6, 9, and 10 after a launch; distinct from FULL for the entire workspace. See the [L0 resource table](L0_frame.md#textures). |


<a id="index-measured-scope"></a>
## Boundaries of Measured Instances

The old 1080/1440 multi-frame gates are bound to 854, and the 4K 3-frame gate to unified M. M2's named new gates are limited to 1080/1440 f0 and 4K L0–L99; the remaining scope is not relabeled as newly measured on M2. sceneA compares only FINAL; some 1440 points lack per-launch native six-texture observations. The [original scope, frame counts, builds, and receipts](APPENDIX_evidence_history.md#index-scope) were moved to the appendix; for state across frames, see [L0](L0_frame.md#what-is-retained-between-two-frames).

This directory interprets old material according to the current ARCH 0.7 supplements and LATEST: the old statements "1440 stops at L133, the 4K full chain was not run, B0 is reset only" have been superseded by named instances. A whole-network theorem remains NOT_ESTABLISHED, and the L133 computed-shared symbolic layer remains NOT_ADMITTED. Byte agreement does not automatically prove general geometry, unique internal values, all maps semantics, or unmeasured control branches.


<a id="half-f32-history"></a>
## Old half/F32 Conversion Records and Their Scope

The per-site inventory of F32↔F16 boundaries across the full chain is maintained only in [L4.fp32-ftz](L4_fp32_ftz.md#sites). This section retains only the scope of historical conversion acceptance and debugging receipts.

A saved experiment traced a divergence to a fixed multiplication rounding point in a debug export that broke native coordinate fusion. Named frame results and input limits after restoring fusion are in [B00 divergence RESULT:7–33](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据). That report's unrun frames 4/5 are historical scope and cannot negate later named multi-frame acceptance; here it is used only to confirm the fusion boundary and the order of the five sampling contributions.

For F32→F16, first widen exactly to binary64, then apply half_round; widening adds no numeric rounding. Finite F16→F32 values and ±Inf are also exactly representable, but NaN payloads are a separate matter. The project's saved acceptance of the complete raw32 conversion accepts 4,278,190,082 inputs and rejects 16,777,214; 63,490 non-NaN half→F32 entries agree, while **2,046 NaNs remain formal differences**: the CPU canonicalizes them to 0x7fc00000 and the GPU to 0x7fffffff. [Narrow-domain RESULT:9, 35–46](../../../experiments/parity-gpu-narrow-exhaustive-r01-20261007-codex/resume2-20261007/RESULT_ZH.md#L35). F16↔E4 is listed in the [E4 format slice](L4_e4m3_and_k32.md#e4m3-format); this slice uses the same conversion contract.


<a id="workspace-checker-sets"></a>
## Cumulative Write Sets and Comparator Rules

### L3.workspace-map.sets Per-Launch Reads and Writes, Cumulative CumWrites(L), and Uncompared Region

- What it is: Define comparable cumulative state using declared write ranges; the actual changed set cannot substitute for the write set.
- Input → output: Each launch's roles / written_ranges, pre- and post-state, and item-by-item provenance graph → WriteSet(L), CumWrites(L), Unwritten(L), and comparison scope.
- How it is computed:
  ~~~text
  1. I_decl(L)=union of declared input-role intervals; Read_ws(L)=union of actual bytes read with typed provenance evidence.
  2. WriteSet(L)=union of this launch's written_ranges intervals; sort first, then merge overlapping or adjacent intervals.
  3. Start the first frame with CumWrites(−1)=∅; CumWrites(L)=CumWrites(L−1)∪WriteSet(L).
  4. Unwritten(L)=[0,N) \ CumWrites(L); UNINIT_NOT_COMPARED=N−|CumWrites(L)|.
  5. Δ(L)={a : PRE(L)[a]≠POST(L)[a]}; it gives only a lower bound on writes.
  6. CumWrites digest=SHA256, fed each merged interval's little-endian U64 offset, U64 length, and interval bytes in order.
  7. Check CPU PRE/POST invariance outside WriteSet(L); state the actually visible scope when comparing native execution.
  ~~~
- Numeric rule: A same-value zero-write does not enter Δ but is still a write; the execution order of two overwrites of the same address is not preserved in the interval union either. I_decl is an allocation span, not a claim that every byte is numerically consumed; an input role only restricts read addresses and cannot alone prove the complete Read_ws. Texture and weight read sets are listed separately, not mixed into the WS set.
- Why it is computed this way: To distinguish numeric exits, synchronization side effects, and untouched initial values, so single-launch and continuous-chain comparisons use explicit objects.
- How we know: CENSUS, [DefinedBytes:5–33](../../../cpp/opt/M/phase2_support/defined_bytes.py#L5); CONTROLLED / MEASURED, [canonical definition:11–28, 48](../../../experiments/b1-dl-canonical-definition-20261010/DL_CANONICAL_ZH.md#1-规范定义). For the boundary of the old write-once / unconditional "read≤write" claim, see [V2-08-005](../../arch-v2/08.02_read_write.md#v2-08-005).
- Next: [Double fill](L3_workspace_map.md#fill), [padding same-value zero-writes](L3_workspace_map.md#padding), [WR checks](L3_workspace_map.md#wr).


<a id="workspace-checker-fill"></a>
## Cumulative State Counts and the 00/A5 Comparison Protocol

**Specific counts for CumWrites and the uninitialized region.** This round reread the params word arrays for the three resolution tiers in the native census and checked that the L1 and L2 exits are adjacent, yielding CumWrites(2)=[0,clear+full+pool); the original captures were not unpacked again this round:

| Instance | CumWrites(2) length (B) | UNINIT_NOT_COMPARED (B) |
|---|---:|---:|
| 1080 | 88,861,696 | 123,658,240 |
| 1440 | 151,323,648 | 189,399,040 |
| 4K | 335,554,560 | 427,507,712 |

The 1080 frozen record also gives |CumWrites(6)|=168,487,936 B, with CumWrites=N starting at L99. This is the cumulative **declared** write set checked with zero differences against the specified native scope, not "all bytes actually written by native execution" inferred directly from GPU data changes. When the previous frame's workspace is retained across frames, cumulative defined state is retained too; it must not be mistakenly recorded as entirely unknown again at every frame.

### L3.workspace-map.fill 00 / A5: Written and Retained Bytes

- What it is: Change the initial fill with the same valid inputs to check whether defined results depend on the unwritten region.
- Input → output: Named runs with F=00 and F=A5 → comparison of results inside CumWrites and the retention rule for its complement.
- How it is computed:
  ~~~text
  1. Fill the first frame's WS with F; for a teacher-forced single launch, also restore CumWrites(L−1) from the specified prior state.
  2. Execute the launch and accumulate declared W to obtain CumWrites; do not infer CumWrites from differences between the two fills.
  3. Compare the candidate with the named reference inside CumWrites; separately check for no writes outside the declaration.
  4. CPU bytes in U continue to retain F; when native U is not observed, record UNINIT_NOT_COMPARED.
  5. When comparing A5 against native fill00: the written region equals the reference byte by byte, and the complement remains A5 byte by byte.
  6. Combine into FULL over the corresponding scope only when CumWrites=N, or when there is evidence that both initial values are the same and neither writes outside the declaration.
  ~~~
- Numeric rule: A CPU FULL match with the same fill can include identical initial values that have not yet been written; it is not automatically a GPU FULL match. In the early 1080 runs, CumWrites digests matched for 158/158 across the two fills, but FULL SHA matched for only 59/158, L99–L157. The two fills are a finite falsification test and cannot prove independence from arbitrary initial values.
- Why it is computed this way: To make accidental reads of unwritten bytes easier to expose and distinguish algorithm results from buffer residue.
- How we know: MEASURED / CENSUS, [CumWrites specification:77–88](../../../experiments/b1-dl-canonical-definition-20261010/DL_CANONICAL_ZH.md#4-调和规则); for the later actual T4K A5 / FULL scope, see [multi-frame RESULT:23–32](../../../experiments/parity-cpp-4k-multiframe-r01-20261022-codex/RESULT_ZH.md#L23), where f0 L0 FULL is NOT_OBSERVED.
- Next: [Different guarantees of WR A/B](L3_workspace_map.md#wr), [padding](L3_workspace_map.md#padding).


<a id="workspace-checker-wr"></a>
## Independent WR A/B Determinations

### L3.workspace-map.wr What WR A/B Check Separately

- What it is: Separate checks of declared-range stability, native visible changes, and CPU modifications outside the range.
- Input → output: Frozen written_ranges, CPU PRE/POST, available native PRE/POST → independent A, B(i), and B(ii) determinations.
- How it is computed:
  ~~~text
  1. A: This CPU run's self-reported written_ranges must equal the frozen expected metadata.
  2. B(i): When native before-and-after snapshots are available, check that their changed bytes Δ_native(L)⊆WriteSet(L).
  3. B(ii): Call DefinedBytes.check_unreported and require the CPU to remain unchanged byte by byte outside WriteSet(L).
  4. Record entries without native snapshots as NOT_EVALUATED; do not substitute a same-fill initial state for observation.
  5. Negative controls such as out-of-range writes, omitted segments, and shifted ranges must be rejected by the corresponding checks.
  6. Report byte comparison, A, B, and symbolic admission separately; a pass in one cannot replace the others.
  ~~~
- Numeric rule: A's expected values come from CPU self-reported ranges in native-MATCH receipts under the same seal; it proves metadata stability across runs. B(i) checks only visible changes and cannot capture every same-value write. B(ii) is outside-range invariance for this CPU execution, not a hardware no-aliasing theorem for all inputs.
- Why it is computed this way: Check "declaration agreement" and "execution stayed in range" separately, preventing a comparison of only the main tensor from missing publication markers or padding.
- How we know: CONTROLLED / MEASURED, [continuation6 WR4K:60–79](../../../experiments/b1-arch-v3-refresh-r01-20261023-codex/continuation6_RESULT_ZH.md#wr4k决定-232026-10-17): A 158/158, B(i) 156 PASS with L0/L1 NOT_EVALUATED, B(ii) 158 PASS; negative controls and actual initial and final states are recorded by name.
- Next: [Latest scope of the 3-frame chain](L3_workspace_map.md#evidence), [interval algorithm](../../../cpp/opt/M/phase2_support/defined_bytes.py#L3).


<a id="workspace-example-code"></a>
## Full Script for the repack Index Example and Checker Metadata

~~~python
from pathlib import Path
import re,struct,json
src=Path("E:/GlassBox-NR/cpp/fam_repack/repack.cpp").read_text(encoding="utf-8-sig")
dest=list(map(int,re.search(r"kBitDest\[12\]\s*=\s*\{([^}]+)\}",src)[1].split(",")))
assert sorted(dest)==list(range(12))
def pi(x): return sum(((x>>b)&1)<<d for b,d in enumerate(dest))
old=Path("experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence/oldmap")
for rows,cols in [(20,32),(24,40),(36,60)]:
 row,col,c=5,7,37
 token=row*cols+col
 tile=(row//4)*((cols+3)//4)+col//4
 slot=4*(row%4)+col%4
 tiled=(tile<<12)|pi((slot<<8)|c)
 raster=((token//16)<<12)|pi(((token%16)<<8)|c)
 for launch,at,expected in [(58,raster,tiled),(99,tiled,raster)]:
  with (old/f"old_L{launch}_{rows}x{cols}.u32").open("rb") as f:
   f.seek(at*4);assert struct.unpack("<I",f.read(4))[0]==expected
 print(rows,cols,"token",token,"tile",tile,"slot",slot,"pi",pi((slot<<8)|c),
       "tiled_chunk",tiled,"raster_chunk",raster,"byte_offsets",4*tiled,4*raster)
root=Path("experiments/parity-cpp-m2-release-clean-r01-20261020-claude/evidence")
j=json.loads((root/"equiv_old_maps.json").read_text(encoding="utf-8"))
dim={k:v for k,v in j.items() if re.fullmatch(r"\d+,\d+,\d+",k)}
print("saved_dimension_direction_results",len(dim),
      "valid_hashes",sum(not v.startswith("ERR") for v in dim.values()),
      "rejections",sum(v.startswith("ERR") for v in dim.values()),
      "other_controls",len(j)-len(dim))
data=json.loads(Path("experiments/parity-cpp-geom-census-r01-20261006-codex/native_launch_facts.json").read_text(encoding="utf-8"))
N={"1080":212519936,"1440":340722688,"2160":763062272}
def q(L,g):
 u=next(r for r in data["launches"] if r["launch"]==L)["resolutions"][g]["params_u32_le"]
 return [u[i]+(u[i+1]<<32) for i in range(0,len(u),2)]
for geo,n in N.items():
 a=q(1,geo);b=q(2,geo);base=a[0];clear=4*(a[1]&0xffffffff)
 nw,nh=b[30]>>32,b[30]&0xffffffff
 full=nw*nh*32;pool=(nw//2)*(nh//2)*32
 assert b[27]-base==clear and b[31]-base==clear+full
 print("geometry",geo,"N",n,"clear",clear,"full",full,"pool",pool,
       "D2",clear+full+pool,"U2",n-clear-full-pool)
~~~


<a id="mufu-counterexample-identifiers"></a>
## Original Registry IDs of Special-Function Counterexamples

## Why libm or a Naive Closed Form Cannot Be Substituted

- [RULEDOUT-MUFU-LG2-LAW](../../../knowledge/RULED_OUT_ZH.md#ruledout-mufu-lg2-law) records that the measured lg2 of the smallest positive normal number is not the exact integer −126; 126 of 254 power-of-2 inputs are inexact. The end of this page reads the saved encoding 0xc2fbffff, whereas current libm converted to F32 is 0xc2fc0000.
- [RULEDOUT-c7b4080777](../../../knowledge/RULED_OUT_ZH.md#ruledout-c7b4080777) records failure intervals even under adjacent exponent scaling; E1 uses measured 3-bit rank corrections rather than reasserting the failed lg2 reduction law.
- [RULEDOUT-f1623cdd85](../../../knowledge/RULED_OUT_ZH.md#ruledout-f1623cdd85) retains a counterexample in which an incorrect error bound caused an incorrect radius-domain estimate; computing a mathematical value and then applying a loose tolerance cannot support byte-for-byte agreement.
- [Noise proof RESULT:46–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L46) measured many bit differences for naive trigonometric reflection and derivations using half-period and quarter shifts; the full residual preserves these irregular values.
- [RULEDOUT-MUFU-71BLOCK-SCOPE](../../../knowledge/RULED_OUT_ZH.md#ruledout-mufu-71block-scope) also explains that counting only 71 [logical blocks](APPENDIX_beginner_glossary.md#g036) misses the final display kernel; this slice locates sites along the complete L2 path and does not silently retain the old 154-launch scope.

These entries have their own dates and scopes. For example, the old statement "sm_120 has not yet been measured" was advanced by the later named 14-variant record; the original failures and limitations are not deleted. What can be computed exactly is the index of certified data, integer decoding, bit-pattern correction, and accepted scaling; unrecorded values in transcendental function maps do not follow automatically from these formulas.


<a id="r04g-review-resolution"></a>
## R3 Item-by-Item Revisions and Example Scope (r04g)

Corresponds to the [complete Gemini R3 review](../reviews/REVIEW_OUTSIDER_R3_gemini_20261026.md). Writes only in this directory; reads source, integer addresses, and certified function assets; does not modify runtime, old experiments, or external files; does not run GPU / model / full chain; does not stage or commit.

| R3 Top-10 item | Handling and location in main text |
|---|---|
| 1 L100/L56 [operator](APPENDIX_beginner_glossary.md#g035) intuition | L1.06/L2.06/L3.split16 put the 4×256 reduction first; the four source groups / non-channel coordinates of all outputs in the fixed 1080 map were checked. L56's 40 buckets of 8192 B each are compatible with the 64×40→32×20 capacity; 4×4 spatial pairing per window is only [Inference], still lacking independent coordinate calibration. Standard [mean](APPENDIX_beginner_glossary.md#g044) pooling or unique interpolation was not additionally asserted |
| 2 INDEX engineering terms / old boundaries | Two complete sections moved to this appendix at project-terms/index-measured-scope, with a one-line link to each left in INDEX; object labels and architecture navigation retained |
| 3 Repeated notation tables on nine pages | Only 3–5 local entries remain per page; formats, operations, and evidence labels are consolidated in INDEX |
| 4 Ambiguous mathematical notation | Q8/D8 throughout; exponent E; Den denominator, CumWrites cumulative write set, Partials partial sums, Radius radius, [Hash32](APPENDIX_beginner_glossary.md#g075) integer hash, and HSL_Fwd/HSL_Rev decomposition named separately; F32 operations use F32+/×/division and F32_FMA. Actual source function names remain as implementation identifiers |
| 5 Repeated unknowns / system explanations | Ten repeated L1 motivation explanations consolidated in INDEX; window-size guards and role / release handoffs are source-reading facts; cross-window benefits and resource-pressure causation are separately marked as speculation |
| 6 Offset substitutions | Q/K/V=84/88/289 B for t=9,h=0,d=4, matching actual fetch coordinates and the bound map; the actual B0 output loop gives full=85, pool=30741 B, explaining coordinates and bit fields respectively |
| 7 Cross-page repetition | B0 L2 condensed to a five-row step table + diagram; F32 sites maintained only in L4.fp32; half retains conversion rules and adds links back to ViT/FFN/attention |
| 8 Dangling numbers / sentence fragments | D27 and guard 4 explained by function names; MUFU counterexample IDs moved to this appendix; trailing sentence fragments completed; L1.09 uses the current short-card text |
| 9 Complex numeric examples | Synthetic TEX joint 8-bit fractional weights / truncation / midpoint, [5-tap](APPENDIX_beginner_glossary.md#g029) pixel, and two rounds of L157 HSL real code bodies all computed, with intermediate values and output encodings recorded |
| 10 Workspace test protocol | Cumulative sets / 00-A5 / WR determinations and Python checker script moved to this appendix; roles, actual read/write boundaries, repack / padding / indexing, and result tables remain in the main text |

**Handling of missing/cut/structural suggestions.** L0 adds a six-item "what it is not" box, each item linking to an existing arithmetic / wiring page; text beside the diagram explains that 1080→1152 comes from the actual internal-canvas contract and gives a mirror-row substitution. L0 also summarizes the known subset of params byte offsets for each launch without claiming a complete ABI. The new [L4.tex-filter](L4_tex_filter.md#tex-filter) moves existing bit-level sampler rules down from B0 L3 while retaining the L3 filtering interface. The existing five-layer skeleton, six-texture table, complete blocks, and shape diagrams are not rebuilt.

**Scope not adopted literally.** "All residuals are added at the first matrix seed" is unsuitable as an unqualified all-family theorem: this skewer's ViT contract includes a first shard and ordered half merging, while projection retains its interface according to its named diagram. The L0 box says only that actual seed / partial-sum wiring cannot be moved to real-number addition at the end. R3 also summarizes HMMA as 17 terms analogous to QMMA, but this cannot remove the existing negative-zero counterexamples, B0 all-zero early return, or B70 guard; L4.hmma's original evidence status is unchanged. The claim that resource budgets caused kernel splitting has no independent measurement this round and is therefore listed only as speculation.

**A controlled visual image set is still missing.** The available reading material contains no complete reusable image set binding the same input, history, parameters, and control changes; the old timeout receipt cannot serve as final-image evidence. See the [r04f gap](#r04f-review-resolution). New examples this round use synthetic scalars / pixels and do not pass as network output or visual controlled comparisons; no model was run separately to fill the image gap.

**Computations and reruns.** [geometry_r04g.py](../skewer/examples/geometry_r04g.py) looks up only integer maps with pinned SHA; [substitutions_r04g.py](../skewer/examples/substitutions_r04g.py) extracts real half / texture / temporal / s157 and layout expressions and runs them on synthetic data. All compilation intermediates were created and cleaned within this directory; the original functions and copies with only logging added have identical output bytes, and missing certified function raw values raise errors rather than falling back to libm. The original eight Python working examples were rerun individually after renaming, with arithmetic ASTs preserved after name normalization; numeric results and acceptance records are saved in the [validation report](../skewer/examples/r04g.validation.json).


<a id="param-change"></a>
<a id="param-change-r04h"></a>
## Parameter Change r01: Backfilling B/C/D1 Acceptance Evidence (r04h)

[Child Candidate / Saved Measurement, Non-M/M2] The authoritative scope is the [overall report](../../../experiments/parity-cpp-param-change-r01-20261024-codex/RESULT_ZH.md), [B](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_B_ZH.md), [C](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_C_ZH.md), [G2 final state](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c_r1/G2_RESULT_ZH.md), [D1 final state](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1_ZH.md), and [D1A certification details](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1A_ZH.md). RUNNING and STOP in D1A / diagnostics are historical and cannot override D1's final state; different seals for different stages are not combined into one regression. M/M2 and old evidence remain unchanged.

| Candidate identity | content seal SHA-256 | execution seal SHA-256 |
|---|---|---|
| Stage B | 8d84018cc8e3297c78b9c841ae215680a0c3751bb27d8ac6937113804c6f4db8 | e65a7eaead43d9b3dd8a4384a42e109bea0d932b04430ac5eb6d3cd721c54662 |
| R1 / G2 | f7335470fed0810740b27d33c48f53b44f00572c0af63035f04ee9b2de62de93 | e985763908112f63c8720bc33a6b3fce085d78816cf158cbf46baf68353c0f1a |
| R2 (original STOP retained) | 905bf2b65362cbf04d38862429be8bfc1846b1270a245dfd5447007dd73c3b6e | a69cacce8e2bc4bd1ccb5ea1332b4ef3342bfadfc89895bf03ccea9b8449e748 |
| R2b (reach STOP) | No formal candidate seal created | No formal execution seal created |
| Final R2c / L1 | fed491ba117f2d3b24b815d2f2d401471e3570edcd67f106fed3abd9cb577d0a | 699d97f81439171b69319e54d9458804ff61b0a17fae4c93fe045c423bc1f1fe |
| Final R2c / G4 | Same R2c content | 690a3256b6d7f8a66aa6eb5eb0d9747fd02cb700c601330b138773bc6ed23d13 |

Stage B's acceptance scope is E4's two modes tone0/style0, with a single process per mode advancing its own state f0→f1, fill00, 1080: across four frames, 624 complete workspace MATCH, 4 FINAL and 4 copy6 MATCH, and 624 WR B(ii) PASS; the union of shards has no FULL gaps. The four textures 1/2/3/6 differ from the six textures on the default 158 route; six-POST and WR B(i) remain NOT_RUN.

R1 G2 has 315 FULL MATCH, 1 FULL NOT_OBSERVED, 2 FINAL MATCH, and 316 WR B(ii) PASS; native history is missing. The R0 interpretation that ignored CB+0xb8 (u64) (containing two F32 fields) was disproved by the [native discriminant for reset with the same upload](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/NATIVE_B00_DISCRIMINANT_C.json) and [withdrawn](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/WITHDRAW_R0.json); numeric model calls were 0. The old copy6 diagnostic mistakenly treated display id2 as history; that erroneous comparison record cannot be treated as an established history numeric DIFF. The [diagnostic](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c_r1/DIAG_COPY6_ZH.md) corrects identity only; native id6/id9 remain NOT_OBSERVED.

| Final R2c job | Launches | FULL MATCH / NOT_OBSERVED | WR B(ii) PASS | FINAL MATCH |
|---|---:|---:|---:|---:|
| L1_1of2, each f0→f2 | 474 | 236 / 238 | 474 | 3 |
| L1_2of2, each f0→f2 | 474 | 237 / 237 | 474 | 3 |
| G4, f0→f15 | 2528 | 0 / 2528 | 2528 | 16 |
| Total | 3476 | 473 / 3003 | 3476 | 22 |

The two L1 prediction trajectories are independent; CPU state is not stitched together. The observation union is f0 L1..157, f1/f2 L0..157. The three repeated L1 FINALs represent only three logical frames, so the 22 FINALs total 19 distinct logical frames. L1_1of2 has zero differences for the full workspace and B00_FULL/POOL at f1/f2 L2; 2of2 did not capture that point. G4 captured no intermediate FULL; the 3003 gaps are not counted as MATCH, and all native history is separately NOT_OBSERVED. WR B(i) / six-POST are NOT_RUN.

For R2's fixed-control STOP and R2b's reach STOP, see the [S157 control diagnostic](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1_r2/DIAG_S157_GUARD_ZH.md) and [SFU site diagnostic](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1a_r2b/DIAG_REACH_GUARD_ZH.md), respectively. Final R2c standalone S157 is 4/4: 1 R2 CPU-own input for a new tuple and 3 native function inputs for the parent tuple; these are not four continuous chains. R2b has no formal seal, so an independent full regression for it cannot be invented. R2c only extends reach and rebuilds outtail, retaining the original color arithmetic / codec / assets; single-half-domain certification also does not close the full-domain binding of cross-channel lg(gray?1:S), which remains OPEN.

<a id="param-change-tuples-r04h"></a>
### Exact Control Tuples from R2b→R2c

The parent entry is separately compared by floating-point value, so both δ=+0/−0 pass; only the 15 entries below are exact u32 matches. Full admission is the OR of the two; see the [parent predicate revision](L3_b70_history_output.md#parent-predicate-r04l).

[Child Candidate Predicate, Non-M/M2] Column order is I/a/b/c/δ at byte offsets 0x120/0x144/0x14c/0x150/0x154. Entries are five u32 bit patterns, not model weights. The original parent tuple is 3f800000 bdcccccd be800000 bdcccccd 00000000; the following 15 investigation tuples are added without interpolation. They come from the [four-site enumeration table](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/REACH_CENSUS.json). Tuple-predicate admission and SFU finite-half-domain certification do not mean that native image output or continuous-chain validation already exists for every tuple.

| Investigation index | Exact u32 for I / a / b / c / δ |
|---|---|
| 0 | 3f800000 00000000 00000000 be19999a 00000000 |
| 1 | 00000000 bdcccccd be800000 bdcccccd 00000000 |
| 2 | 3e800000 bdcccccd be800000 bdcccccd 00000000 |
| 3 | 3f000000 bdcccccd be800000 bdcccccd 00000000 |
| 4 | 3f400000 bdcccccd be800000 bdcccccd 00000000 |
| 5 | 3fc00000 bdcccccd be800000 bdcccccd 00000000 |
| 6 | 3f800000 bcf5c290 bd99999a bcf5c290 00000000 |
| 7 | 3f800000 bd4ccccd be000000 bd4ccccd 00000000 |
| 8 | 3f800000 bd8f5c29 be333333 bd8f5c29 00000000 |
| 9 | 3dcccccd bdcccccd be800000 bdcccccd 00000000 |
| 10 | 3ea8f5c3 bdcccccd be800000 bdcccccd 00000000 |
| 11 | 3f666666 bdcccccd be800000 bdcccccd 00000000 |
| 12 | 3f7fbe77 bdcccccd be800000 bdcccccd 00000000 |
| 13 | 3f800000 bccccccd bd800000 bccccccd 00000000 |
| 14 | 3f800000 bd75c290 be19999a bd75c290 00000000 |

**Uncovered scope.** The five frames for D2 instance switch/feature rebuild and eight frames for D3 312 B post_block are all REFUSED/NOT_RUN, with another workstream in progress; the two groups overlap by 2 frames, for 11 unique frames total. The remaining 75 standalone S157 records are NOT_RUN_STATE_UNAVAILABLE and are not filled in from L1/G4. The 320×240 job AM-S2 / job S1 / job G1-320 are NOT_RUN_GEOMETRY_UNSUPPORTED_T64_FFN_CONTRACT; the original template-contract rejection at job AM-S2 f0 L60 is not bypassed. This is not acceptance of a general 320 algorithm. The final Stage E/F full regression under the same seal is NOT_RUN.

**This documentation work.** New model / GPU / full-chain / SFU full-domain scans were all 0; only the [synthetic CB scalar control](../skewer/examples/param_change_r04h.py) was run. Its [R2 source SHA / half-precision results](../skewer/examples/param_change_r04h.result.json) and [acceptance-report identities and count projection](../skewer/examples/param_change_r04h.evidence.json) can be inspected. Writes only in this directory, no commit; links, default 158/158 coverage, and release scan are in [this round's validation](../skewer/examples/r04h.validation.json).


### Complete Account of the Withdrawal Discriminant and Function-Site Certification

**R0 withdrawal.** R0 interpreted this reset as "retain the original structure, ignore CB+0xb8 (u64) (containing two F32 fields), and set both masks to −1." Before CPU numeric execution, two native frames with the same upload SHA, counter0, and remaining B00 parameters, differing only in CB+0xb8 (u64), had 43,177,878 B different in B00 FULL and 10,627,432 B in POOL. This disproves the interpretation that masks are ignored; it does not uniquely determine the internal implementation. See the [native discriminant](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/NATIVE_B00_DISCRIMINANT_C.json) and [withdrawal record](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_c/WITHDRAW_R0.json). R0 had 0 numeric calls and is not counted as a numeric DIFF or a failed repair.


## S157: Four-Site Reach Recertification for the R2c Child Candidate

[Child Candidate Saved Measurement Review, Non-M/M2] R2b's original parent + 15 exact control tuples do not change color arithmetic; final R2c enumerates all 65,536 half values for each of the 15 new tuples, completing 63,488 finite codes while still rejecting 2,048 nonfinite codes. id9 RGB enters the four sites; id10 serves only as the final blending [base](APPENDIX_beginner_glossary.md#g003). site0/site2 add LG2 block 127, with union domain {0,103..127}; site1/site3 add EX2 blocks 0 and 372..378, with union domain {0,372..387,511}. Block numbers are raw32>>23, not program addresses. Original validity and other guards are retained; enumeration of control tuples is not admission of arbitrary float values or arbitrary cross-channel colors.

| Table member / site | Measured backing and runtime representation retained by R2c |
|---|---|
| LG2 127 / site0, 2 | Complete measured base_E127.bin, 33,554,432 B, with raw values read directly; remaining LG2 blocks use the existing E1-certified representation |
| EX2 372/373 / site1, 3 | Saved complete raw blocks serve as hardware SHA references; runtime still uses the unmodified ex2.bin integer codec, not a libm substitute |
| EX2 374..378 new, 379..387 existing | Unmodified ex2.bin base table and integer codec accepted against complete hardware-block SHA |
| EX2 0/511 | Certified representation of saved FTZ constants or the single −Inf point; NaN is still rejected, so the entire special-value block cannot be described as full-domain admission |

[SITE_TUPLE_BACKINGS](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/SITE_TUPLE_BACKINGS.json) binds measurement files, hardware full-block SHA, and runtime representations by tuple / site / block, with no missing members among 44; [REACH_CENSUS](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/REACH_CENSUS.json) gives actual half counts. R2/R2c values/validity SHA are identical for the old 35 blocks and 293,601,280 inputs; the compiled lookup for the new 9 blocks and 75,497,472 inputs has the same SHA as the saved full hardware blocks. Saved sm_75/sm_120 summaries for 7,168 pairs across 14 variants matched on reread; this is a review of old measurements, with new GPU runs=0 this round. The running status in the [D1A certification notes](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1A_ZH.md) is superseded by the [D1 final report](../../../experiments/parity-cpp-param-change-r01-20261024-codex/STAGE_D1_ZH.md).

Final R2c standalone S157 has 4/4 FINAL MATCH: 1 R2 CPU-own input with new controls + 3 parent-tuple function inputs; the latter are not a continuous chain. The 75 records lacking state remain NOT_RUN_STATE_UNAVAILABLE; full-domain call binding for cross-channel lg(gray?1:S) remains OPEN. The measured full domain, codec validity domain, site reach, standalone function results, and continuous chain are accounted for separately at each layer; M/M2 are unchanged, and the scope is not extended to unmeasured devices / drivers, old ELF, or arbitrary parameters.



<a id="r04i-review-resolution"></a>
### Item-by-Item Handling of R4 (r04i)

1. Parameter-change account: INDEX/L0–L4 retain only branch inputs, formulas, and wiring, marked measured on child candidate and linked solely to this section; shards, counts, withdrawals, STOP, and unrun scope are consolidated under param-change.
2. Code names: project-terms adds Stage B, G2/G4, D1–D3, R0–R2c, the two L1 shards, and 320 jobs; job AM-S2 replaces the old job label that conflicted with Q8(x), and the source-label mapping appears only in the glossary.
3. CB notation: prose, pseudocode, diagrams, and quick-reference tables consistently use CB+0xNN (f32/u32/u64); actual field names and array accesses in implementation scripts are not renamed.
4. Address map: workspace-map adds an inp/sread/xsite/wload→arithmetic DAG→16 B gstore→role split diagram, making clear that A/Y are execution axes and not presenting them as a closed form for logical heads / windows.
5. Computation: the original B70 color fragment, confidence FMA, and certified EX2/RCP wrappers compute synthetic pixels; the real repack swizzle expands 0x725→0x276; the original half_round computes RN16(√32)=5.65625.
6. Operator intuition: explains current color plus predicted residual and the [RMS](APPENDIX_beginner_glossary.md#g053) scale of Q; mathematical facts are not labeled as training speculation, and publication points and unknown hardware causes are retained.
7. L4: bit-level rules for LG2 E1 and EX2 positive / negative branches return to the main text; raw-value tables / rank capacities remain in the CPU appendix, and the function-site certification account is consolidated in this section.
8. Layout: removes the complete duplicated L100 passage, adds L1.04 window geometry, actually known L2.04 MKN, and L2.07 logical handoff; fixes duplicate headings / anchors, sentence fragments, and spaces inside Chinese words.
9. Script: B70 inline Python moved unchanged to examples/b70_rz_copy_r04i.py; only input and output remain in the main text.
10. Paths: INDEX gives the roles and conditions for opening v2 source, private records, workstream maps, early Python, and the copy migrated back to 10600T; machine drive letters removed from link text.

Missing/cut: L0 adds a six-row numeric-domain table and stage matrix-byte / logical-MAC table, retaining the layer skeleton; early zero-write event counts move to padding-bug. Complete split16 / whole-network MAC and physical weight allocation were not added: existing documents do not close all QKV, encoder dual-exit, and internal L57 MKN, so only subtotals for proven matrices are given; output width is not guessed to be a dense layer. The table excludes bias/scale/alignment, and resource-container bytes are not added to runtime matrix-slot bytes. There is no new controlled visual material, and no image / model run was added to fill the gap. NOT_RUN closure plans were added for HMMA zero sign and host field naming; plans are not presented as new measurements.

This round read only source, function tables, and identity metadata, with 0 new model / GPU / full-chain runs; the [calculation script](../skewer/examples/anatomy_r04i.py), [actual outputs and shape integers](../skewer/examples/anatomy_r04i.result.json), and [document validation](../skewer/examples/r04i.validation.json) preserve the scope. All compilation temporary files were created and cleaned within this directory; old acceptance, M/M2, and child candidates were not changed, and nothing was committed.

<a id="r04j-fact-resolution"></a>
## r04j: Fact-Audit Revisions and Two Guides

Only [fact audit R1](../reviews/FACT_AUDIT_R1_codex_20261027.md) was handled; the other two reviews were neither read nor executed. The three groups of non-CORRECT items and cross-page conflicts were reconciled as follows:

| Item | Revision result | Direct evidence |
|---|---|---|
| C281/WRONG | INDEX, B0, B70, texture L4, and this appendix all restored to 1/256 fixed-point subpixel grid / joint 8-bit fractional weights; br=(a*b+128)/256 is integer division. B0's actual CB+0x40 u64 handle slot is retained; the sampling function does not read CB | [native_temporal.hpp:10–19](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L10), [actual handle contract](L3_b0_input.md#p5-candidates) |
| C282/OVERCLAIM | L1.04, L2.04, L2.06, and L3.split16 consistently mark pairing each 8×8 window with a 4×4 spatial exit as [Inference]; retain the integer facts 8×5, 64×40, 32×20, and 20,480×16 B, distinguishing 40 capacity buckets of 8192 B from spatial coordinates. Add independent (x,y,c) mappings for input-window and pooled bytes, per-event source / destination pairing, and closure conditions for L100 output / skip coordinates | [geometry_r04g.py:48–61, 77–84](../skewer/examples/geometry_r04g.py#L48), [unified geometry boundary](L3_split16_window.md#heads) |
| C283/CORRECT_BUT_IMPRECISE | L4.mufu and the CPU storage appendix clarify: check actual SHA at registration, check fd identity before mapping a replacement, and reuse mapped pages on cache hits; no guarantee of detecting external changes on every query | [full_raw_registry.hpp:28–39, 53–60](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L28) |

Other repeated cross-page counts and M/M2/child attribution are retained within the scope already passed by the audit; no new numeric acceptance was added. [Object and method](L0a_object_method.md) explains the fixed DLL, capture types, reproduction criteria, and proof boundaries; [determinism](L0b_determinism.md) binds evidence item by item to historical native, M, M2, or child, clarifying that only summaries exist for the two old driver versions and raw paired records were not found. Scenario and parameter QA continue to link to this appendix and are not merged into a new unified seal.

This round wrote only to skewer, with 0 new GPU, CPU model, continuous-chain, or primitive scans; there were no network, SSH, or version-control operations. Old scripts, outputs, receipts, and inline arithmetic were unchanged; [pre-change identity](../skewer/examples/r04j.baseline.json), [documentation-only validator](../skewer/examples/verify_r04j.py), [validation receipt](../skewer/examples/r04j.validation.json), and [release scan](../skewer/examples/r04j.leak.json) preserve the inspection scope.

<!-- beginner-r04m:start novice-resolution -->
<a id="beginner-review-r04m"></a>
## This Round's Beginner Teaching Layer and Acceptance Scope

In response to the [novice review](../reviews/REVIEW_NOVICE_R5_codex_20261027.md), a whole-frame function diagram, complete small block, history timeline, finite-number-point small basket, and 111 groups of meanings were added; the [25-item handling account](../skewer/examples/r04m.review_resolution.json) records locations and undetermined items. The original 44 pages of expert text can be fully restored, and old evidence status is not upgraded. Novice retelling / drawing acceptance was not repeated this round and remains NOT_RUN.

The two PNG/SVG sets use only synthetic scores and conceptual color blocks, with synthetic teaching labels in the figures; no model coefficients, activations, or real before-and-after frame comparisons were used. The [final document check](../skewer/examples/r04m.validation.json) and [release scan](../skewer/examples/r04m.leak.json) preserve this round's results; new GPU, model, full-chain, and compilation runs were all 0.
<!-- beginner-r04m:end novice-resolution -->
