# L3.b0-noise-reprojection: B0 Noise, 16 Channels, and History Reprojection

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start intro -->
<a id="beginner-b0"></a>
[Beginner Simplification] These 16 slots are the conditioning list fed to the network, not 16 colors. The first three perturbation items are generated separately from position/counter, not grain measured from the original image; the overall visual purpose of the conditioning remains unknown. When no [history](APPENDIX_beginner_glossary.md#g024) is available, the three old-RGB slots repeat the current RGB. Next, 16 items per position become 32 items, which are then processed in small [windows](APPENDIX_beginner_glossary.md#g015).

| 0: perturbation | 1: perturbation | 2: perturbation | 3: constant 1 |
|---|---|---|---|
| 4: current R | 5: current G | 6: current B | 7: old R or current R |
| 8: old G or current G | 9: old B or current B | 10: [style](APPENDIX_beginner_glossary.md#g005) | 11: tone |
| 12: structure | 13: conditioning value | 14: conditioning value | 15: constant 0 |

Current/old RGB each undergo prescribed transforms before entering the slots; under the default non-[p5](APPENDIX_beginner_glossary.md#g032) path, 13/14 are −1, whereas the p5 branch instead reads two [scalar](APPENDIX_beginner_glossary.md#g076) conditions with structure=1 rather than sampling two separate mask images. [Existing channel contract](#channels). Read [how the current point fetches numbers from the old image](L1_00_history_primer.md#moving-point) and [five points containing a 4-neighborhood inside each](L1_00_history_primer.md#nested-sampling) first, and then read the hashing, exact coordinates, and byte unpacking below.
<!-- beginner-r04m:end intro -->

<a id="resource-unpack-r04l"></a>
## B0 Resource Unpacking (F03.02, Rank 71)

The four [E4](APPENDIX_beginner_glossary.md#g055) [matrices](APPENDIX_beginner_glossary.md#g051) use the ordinary [tile](APPENDIX_beginner_glossary.md#g087) branch of the [TIN matrix byte formula](L3_tin_window.md#resource-layout-r04l): w1=(32,128)@0, w2=(128,32)@4096, qkv=(32,96)@9312, [proj](APPENDIX_beginner_glossary.md#g038)=(32,32)@20592; offsets are relative to this block's [resource](APPENDIX_beginner_glossary.md#g079) [base address](APPENDIX_beginner_glossary.md#g084), with the last dimension contiguous. adapter is 16×32 [half](APPENDIX_beginner_glossary.md#g054): for nt=0..1 and i=0..255, `e=i%8,l=i//8,fe=e%4,k=2*(l%4)+(fe&1)+8*(fe//2),n=l//4+8*(e//4)`, and [logical](APPENDIX_beginner_glossary.md#g085) `adapter[k,16nt+n]=LE16(resource+8208+2*(256nt+i))`. The [FFN](APPENDIX_beginner_glossary.md#g037) [residual](APPENDIX_beginner_glossary.md#g017) [scale](APPENDIX_beginner_glossary.md#g031) is 32 half@9232, and the [attention](APPENDIX_beginner_glossary.md#g039) scale is 32 half@21616; the score scale [F32](APPENDIX_beginner_glossary.md#g056)@20576 undergoes [RN16](APPENDIX_beginner_glossary.md#g059) only once. bias is 4096 half@12384, where the 8×8 coordinates of query/key select the index according to the [same 12-bit arrangement as B70](L3_b70_history_output.md#resource-unpack-r04l); these are read locations, and parameter values are not listed. [b00.hpp:7–20](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L7).

<a id="p5-packed-r04l"></a>
## p5 own-history Admission Constants (V03.02, Rank 87)

Only control constants are listed here. Non-reset p5 requires history enable=1, temporal true, the low 32 bits of the frame word in 1..15, and the high 32 bits equal to 0; the corresponding q3/4/5/8/11..17 in [CB](APPENDIX_beginner_glossary.md#g083) are all 0. The following three dimension groups must match strictly bit for bit:

| CB field | packed [u64](APPENDIX_beginner_glossary.md#g057) / interpretation |
|---|---|
| CB+0x30, +0x48 (u64) | 0x4487000044f00000; low/high F32=1920, 1080 |
| CB+0x38, +0x50 (u64) | 0x3a72b9d63a088889; low/high F32=0.0005208333604969084, 0.0009259259095415473 |
| CB+0xd0, +0xf0, +0x100 (u64) | 0x0000078000000438, 0x0000078000000480, 0x000003c000000240 respectively; low/high u32=(1080,1920), (1152,1920), (576,960), must not be treated as F32 |

CB+0xa0, +0xa4 (f32) must also be finite and not nonzero [subnormals](APPENDIX_beginner_glossary.md#g068), with ±0 permitted. A failed check is rejected and cannot pass the bit-pattern equality merely because a numeric value is close to the dimension reciprocal. [R2 b00.hpp:41–50](../../../experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1_r2/returned/snapshot/candidate/repo/cpp/opt/M/entry/b00.hpp#L41).

[CPU Reconstruction / CENSUS] Default wiring and restricted parameter branches are explained separately; functions, formats, and [publication](APPENDIX_beginner_glossary.md#g091) points preserve the original [contracts](APPENDIX_beginner_glossary.md#g101). Training motivations and the design reasons for kernel splitting are unknown, and speculation is not added slice by slice.

[Full Skewer Index](INDEX.md) · Parent level: [L1.02](L1_02_input_b0.md), [Five Steps of L2.02](L2_02_b0.md#b0) · Shared arithmetic: [Matrix Multiplication](L3_qmma_e4m3.md), [half](L4_half_arith.md), [MUFU](L4_mufu.md), [attention](L3_attention_softmax.md), [norm](L3_norm_nonfinite.md)

## Local Notation on This Page

For global formats, operations, and evidence labels, see [INDEX](INDEX.md#shape-and-workspace-notation).

| Local symbol | Meaning |
|---|---|
| x,y; tx,ty | Un-[mirrored](APPENDIX_beginner_glossary.md#g030) internal coordinates; coordinates after color/[MV](APPENDIX_beginner_glossary.md#g023) mirroring |
| f, [Radius](APPENDIX_beginner_glossary.md#g073)(k) | Native frame word, certified noise radius function |
| [TEX](APPENDIX_beginner_glossary.md#g027), [tap](APPENDIX_beginner_glossary.md#g029) | Single 4-neighborhood filter fetch, one sampling point within the 5-tap filter |
| s_ff, s_att | half scales for this block's feed-forward/attention residuals |

<a id="b0-noise-reprojection"></a>
### L3.b0-noise-reprojection From Conditioning Inputs to Two Feature Exits (L2 / B0)

- What it is: Assembles conditioning inputs in each 8×8 window, executes a 32-[channel](APPENDIX_beginner_glossary.md#g007) window block, and publishes two spatial scales.
- Input → output: id1 [RGBA16F](APPENDIX_beginner_glossary.md#g028), id3 RG16F and id6 RGBA16F when valid, 264 B params, B0 weights, and [function tables](APPENDIX_beginner_glossary.md#g074) → [full](APPENDIX_beginner_glossary.md#g018) E4[Hn,Wn,32] and pool E4[Hn/2,Wn/2,32].
- How it is computed:
  ~~~text
  1. Check parameters, geometry, history handles, resource lengths, and prepared noise tables.
  2. Unmirrored (x,y,f) → four integer keys → three-channel half noise.
  3. Mirror color coordinates; current RGB and valid history RGB each complete their input transform.
  4. Noise, RGB, control values, and constants → feat[16] → half adaptation result[32].
  5. E4 feed-forward, QKV, window attention, and projection → unquantized half result.
  6. Publish full directly as E4; the other branch performs 2×2 pool from half and then publishes as E4.
  ~~~
- Numeric rules: The interfaces between front-end F32, half, and back-end E4 are each preserved; noise, texture filtering, and matrix multiplication cannot be collapsed into a single floating-point library [call](APPENDIX_beginner_glossary.md#g080).
- How we know: [CENSUS](APPENDIX_beginner_glossary.md#g100), [b00.hpp:27–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L27); for specific MEASURED gates and history limitations, see the [evidence table](#evidence).
- Next down: [Noise](#noise), [Compact Tables](#compact), [16 Channels](#channels), [Guards](#guards), [Coordinates](#coordinates), [5-tap](#five-tap), [Filtering](#texture), [Window Block](#adapter), [Dual Exits](#publish).

<a id="noise"></a>
### L3.b0.noise Coordinate / Frame Hashing and Three-Channel Noise

In the pseudocode of this section, `T_SQRT/T_LG2/T_COS/T_SIN` are shorthand for the [F32 numeric wrappers](L4_mufu.md#value-wrapper) of the corresponding certified functions: both inputs and return values are F32 numeric values. Extracting the bit pattern and decoding add no rounding and preserve the sign of zero; the lookup method for the online k pre-composed table, as well as the function and angle wrappers, still execute according to the contracts below.

- What it is: A deterministic generator with no per-pixel advancing [state](APPENDIX_beginner_glossary.md#g002); [integer hashing](APPENDIX_beginner_glossary.md#g075) produces keys, which then pass through captured special-function transforms to form Box–Muller-style noise.
- Input → output: U32 x,y,f → four k∈[1,2²⁴] → three F32 product bit patterns → three half values in feat[0:3].
- How it is computed:
  ~~~text
  1. Hash32(v)=U32(((v >> ((v>>28)+4)) xor v) × 0x108ef2d9).
  2. s=U32(y×0xd8163841) xor U32(x×0x8da6b343)
       xor U32(f×0x9e3779b9) xor 0x243f6a88.
  3. h0=Hash32(s); h=(h0>>22) xor h0.
  4. For j=0..3: v_j=Hash32(U32(h×m_j+a_j)); k_j=((v_j>>30) xor (v_j>>8))+1.
  5. u_j=k_j×2⁻²⁴; r1=Radius(k0), r2=Radius(k1); angles a1=RN32(u2×2π), a2=RN32(u3×2π).
  6. Radius(k)=T_SQRT(RN32(RN32(T_LG2(u)×ln2)×(−2))).
  7. Three F32 channels=[F32×(r2,T_COS(a2)), F32×(r2,T_SIN(a2)), F32×(r1,T_COS(a1))].
  8. Apply RN16 to each, writing channels 0, 1, 2 as [g3,g2,g1].
  ~~~
- Numeric rules: All integer multiplications / additions wrap around in U32; the algorithmic constants for the four streams are given below. The values looked up from COS/SIN already include the [RZ](APPENDIX_beginner_glossary.md#g060) reduction of the angle and must not be reduced a second time. Radius(k) pre-composes the complete radius chain; [LG2](APPENDIX_beginner_glossary.md#g072) is no longer called online. The three multiplications publish F32 first and then undergo RN16, without yet converting to E4.
- How we know: CENSUS, [noise_online_optd.hpp:12–31](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L12), [b00.hpp:29, 37–39](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L29); INFERRED / offline [full-domain](APPENDIX_beginner_glossary.md#g111) reconstruction, [noise proof RESULT:9–27](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#q2-帧几何参数).
- Next down: [Compression and Certification](#compact), [Worked Calculation Example](#worked-example), [MUFU Domains and Edges](L4_mufu.md#edges).

| j | m_j | a_j |
|---:|---|---|
| 0 | 0xcaa5b80d | 0x21dd796b |
| 1 | 0x2c9277b5 | 0xac564b05 |
| 2 | 0x83232c31 | 0x3463e0ac |
| 3 | 0xfa6dc5f9 | 0x4712a88e |

Above, ln2 and 2π denote the F32 constant bit patterns 0x3f317218 and 0x40c90fdb respectively; the reciprocal 2π used internally by the angle tables for RZ reduction is 0x3e22f983. These are algorithmic constants, [dataflow:24–27](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/noise_dataflow_ZH.md#L24). f=U32(CB+0xc8 (u32)), at byte offset 0xc8 in params. It participates in the seed and is not derived from directory frame numbers or a "reset" label. Three consecutive frames read in the noise-proof round with reset=[1,0,0] correspond to f=[0,1,2]; another sequence with per-frame reset has f=[0,0,0]. The general [host](APPENDIX_beginner_glossary.md#g096) counter, cross-instance behavior, and 32-bit wraparound contract remain [UNKNOWN](APPENDIX_beginner_glossary.md#g104). Color [mirroring](APPENDIX_beginner_glossary.md#g030) modifies only color and MV addresses; noise at padded positions still uses the raw x,y.

The noise-proof round also gives a lower bound of 2.3981766091495898×10⁻¹¹ across all composable nonzero radius / angle products, ruling out nonzero F32 subnormal products in this domain; it does not eliminate signed zero, half [underflow](APPENDIX_beginner_glossary.md#g071), or FTZ boundaries of other [operators](APPENDIX_beginner_glossary.md#g035). General special functions and [encodings](APPENDIX_beginner_glossary.md#g057) are not repeated here; see [L4.mufu](L4_mufu.md#representation).

<a id="compact"></a>
### L3.b0.compact Separating CPU Representation from Network Behavior

[CPU Reconstruction] Valid k queries look up [identity](APPENDIX_beginner_glossary.md#g103)-certified function assets to recover the original F32 bit patterns, without a full-frame noise cache. Any failure in key domain, format, length, or identity is rejected; it stores the exact results of the original function chain, not a function approximation. See the appendix for [format guards and integer decoding](APPENDIX_cpu_storage.md#noise-codec-guards).

[Complete block formats, endpoint and residual decoding, load lifetime, and the three asset SHAs](APPENDIX_cpu_storage.md#noise-codec) have been moved to the appendix; the online multiplications, F32/half roundings, and noise channels remain in the [noise steps](#noise). Offline compressed reconstruction does not equal B0 launch acceptance, and the execution gate for that proof round remains NOT_RUN.

<a id="channels"></a>
### L3.b0.channels Mirroring, Color Transform, and the 16 Channels

- What it is: Assembles a fixed-order 16-item half conditioning vector at one canvas position.
- Input → output: Noise, id1 RGB, history RGB when available, and params control words → feat[16].
- How it is computed:
  ~~~text
  1. tx=x<W ? x : 2W−2−x; ty=y<H ? y : 2H−2−y; check that both remain inside the image.
  2. gain=RN16(F32+(CB+0xc4 (f32),CB+0xc4 (f32))).
  3. cur[c]=H×(H+(upload[ty,tx,c],half(−0.5)),gain), c=0..2.
  4. feat[0:3]=three-channel noise; feat[3]=half(1).
  5. feat[4:7]=cur; feat[7:10]=temporal ? history transform result : cur.
  6. M/M2: control words each undergo RN16 and write 10..12; when p5=false, 13/14 write half(−1) and 15 writes +0.
  7. The default release entry rejects when p5=true; see the next section for selection and admission of the restricted branch.
  ~~~
- Numeric rules: Mirroring is a single reflection, not periodic wraparound for arbitrary out-of-bounds coordinates; coordinates too far out of bounds are rejected. Reading the image uses a row stride of 8W B and takes only the first three half values, with [alpha](APPENDIX_beginner_glossary.md#g026) not used as a color input. Subtracting 0.5 and multiplying by gain each perform half rounding; gain comes from params, and a fixed scale from a single capture cannot be treated as a universal constant.
- How we know: CENSUS, [b00.hpp:29–42](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L29); CONTROLLED, [independent verification of control values:15–28, 40–51](../../../experiments/parity-control-params-r03-20260922/B1_VERIFICATION_ZH.md#12-p-层偏移我自己从-zip-解包核过全对).
- Next down: [Guards and p5 Boundaries](#guards), [History Transform](#five-tap), [Adapter Matrix](#adapter).

| Channel | Implemented content when p5=false | Source |
|---|---|---|
| 0 | RN16(g3) | Product of r2 and COS of the second angle |
| 1 | RN16(g2) | Product of r2 and SIN of the second angle |
| 2 | RN16(g1) | Product of r1 and COS of the first angle |
| 3 | 1, half encoding 0x3c00 | Fixed constant |
| 4, 5, 6 | Stepwise half input transform of current R, G, B | id1[ty,tx,0..2] |
| 7, 8, 9 | Input transform of history R, G, B; repeats 4, 5, 6 when no history is present | id6 and id3, or current RGB |
| 10 | RN16(Style) | CB+0xb4 (f32), byte 0xb4; host style/128 mapping observed |
| 11 | RN16(Tone) | CB+0xac (f32), byte 0xac |
| 12 | RN16(Structure) | CB+0xb0 (f32), byte 0xb0 |
| 13 | −1 | CB+0xb8 (f32) (0xb8) participates in the p5 check; the false branch does not copy this value directly |
| 14 | −1 | CB+0xbc (f32) (0xbc) participates in the p5 check; the false branch does not copy this value directly |
| 15 | [+0](APPENDIX_beginner_glossary.md#g070), half encoding 0x0000 | Fixed constant |

The positions of Tone / Structure are distinguished by non-default controlled comparisons: the legacy mapping swapped their native outputs in both directions, 3,276,800 B each; when default values are equal, the swap is invisible. That control gate is scoped to named instances with reset, no history, and no mask texture. MV does not occupy these 16 channels—it participates in [reprojection](APPENDIX_beginner_glossary.md#g025) inside the B0 kernel; display [intensity](APPENDIX_beginner_glossary.md#g004) belongs to the tail end.

<a id="guards"></a>
### L3.b0.guards reset, History, and p5 Boundaries in Default M/M2

- What it is: The entry point restricts interpretable parameter and resource contracts up front and cannot mask missing history via a fallback path.
- Input → output: params, configured geometry / texture identities, and byte lengths of each resource → admitted execution, or exception rejection.
- How it is computed:
  ~~~text
  1. Require a 264 B parameter block; f=U32(CB+0xc8 (u32)).
  2. Nonzero-frame history handle guard (guard 4): when f>0, require U32(CB+0xc0 (u32))==1,
       CB+0x08 (u64)==configured id6 handle for this frame, CB+0x10 (u64)==configured id3 handle for this frame.
  3. temporal=(U32(CB+0xc0 (u32))!=0 && CB+0x08 (u64)!=0 && CB+0x10 (u64)!=0).
  4. temporal=false: channels 7..9 directly use the transform result of current RGB.
  5. temporal=true: both history and MV of the correct lengths must be provided simultaneously, executing native_history_pixel.
  6. p5=(min(CB+0xb8 (f32),CB+0xbc (f32))>=0); M/M2 reject when true, with child candidates listed separately.
  7. Then execute acceptance-domain checks for each arithmetic primitive; exceptions do not count as MATCH.
  ~~~
- Numeric rules: reset is a host state; the code branch is determined by actual mode / handles, and f=0 by itself does not equal no history. The nonzero-frame history handle guard ([guard 4](APPENDIX_beginner_glossary.md#g109)) prevents a nonzero frame from falling into the current-only fallback or using a wrong session handle, without proving the model's sensitivity to numeric perturbations of history. Geometry checks read W/H from CB+0xd4 (u32)/CB+0xd0 (u32) respectively and Wn/Hn from CB+0xf4 (u32)/CB+0xf0 (u32), comparing item by item against the configured geometry; residual "1080 frame0" error strings in the source code cannot be treated as current dimension limits.
- How we know: CENSUS, [b00.hpp:30–35, 53–62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L53); for the structural port of the nonzero-frame history handle guard (guard 4), see [diff (i):23–35](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/seal-port/diff_i_structural_geometry.patch#L23), with [arithmetic diff (ii)](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/seal-port/diff_ii_arithmetic.patch) empty; [RESULT:12–18](../../../experiments/parity-cpp-1440-multiframe-r01-20261017-claude/RESULT_ZH.md#结果摘要) scopes the build and execution-layer handle binding.
- Next down: [Coordinate Chain](#coordinates), [Nonfinite and Matrix Acceptance Domains](L3_norm_nonfinite.md#a1), [Evidence Scope of Gates](#evidence).

Other direct checks: upload must be 8WH B; when temporal is true, history must be 8WH B and MV must be 4WH B; the noise owner must be prepared; the RSQ / RCP half tables must have 30,705 / 30,704 entries respectively; mirrored coordinates must be valid. Deeper inside, Q/K statistics must fall within half encodings [0x0410,0x7c00], the attention [denominator](APPENDIX_beginner_glossary.md#g048) must lie in [0x1c00,0x60e0], and matrix primitive guards remain in effect; see the already expanded [norm](L3_norm_nonfinite.md#norm32), [attention](L3_attention_softmax.md#window-attention), and [QMMA publication boundaries](L4_e4m3_and_k32.md#publish-guards).

<a id="p5-candidates"></a>
### p5: Control Channels and History Selection

When p5 is true, structure is fixed at 1, and the two [masks](APPENDIX_beginner_glossary.md#g006) come from adjacent F32 fields in CB respectively; they are control values, not pixels sampled from mask images. The last six channels of the conditioning vector are:

~~~text
feat[10]=RN16(CB+0xb4 (f32))                  // style
feat[11]=RN16(CB+0xac (f32))                  // tone
feat[12]=RN16(p5 ? 1 : CB+0xb0 (f32))         // structure
feat[13]=RN16(p5 ? CB+0xb8 (f32) : -1)
feat[14]=RN16(p5 ? CB+0xbc (f32) : -1)
feat[15]=+0
~~~

At reset, the counter CB+0xc8 (u32)=0, all words from CB+0x08 (u64) through CB+0x88 (u64) with stride 8 are zero, and CB+0xc0 (u32)=1; there is no valid history, and 7..9 repeat the transformed current RGB. Relevant controls must be finite, permitting zero and rejecting nonzero subnormals.

When history is present, the previous-frame id6 of the current process and the current caller id3 are read, reusing [5-tap/FMA](#five-tap) to form 7..9; 4..6 remain current color, and structure/mask follow the formulas above. The restricted entry requires 1920×1080 color / 1920×1152 internal canvas; CB+0xc8 (u32) in 1..15, CB+0xcc (u32)=0, and CB+0xc0 (u32)=1; CB+0x08 (u64)/CB+0x10 (u64) matching id6/id3 respectively. All words at CB+0x18 (u64)/CB+0x20 (u64)/CB+0x28 (u64)/CB+0x40 (u64) and from CB+0x58 (u64) through CB+0x88 (u64) with stride 8 are zero. CB+0x30 (f32)/CB+0x34 (f32) and CB+0x48 (f32)/CB+0x4c (f32) are (W,H), and CB+0x38 (f32)/CB+0x3c (f32) and CB+0x50 (f32)/CB+0x54 (f32) are the specified F32 reciprocals; the three low/high word pairs CB+0xd0 (u32)/CB+0xd4 (u32), CB+0xf0 (u32)/CB+0xf4 (u32), and CB+0x100 (u32)/CB+0x104 (u32) are (1080,1920)/(1152,1920)/(576,960). Controls and MV scales must be finite and reject nonzero subnormals; extra aux handles or wrong bindings are still rejected.

For implementation evidence of the p5 control and own-history branches, see [parameter branch evidence](APPENDIX_evidence_history.md#param-change) (measured on child candidate); the default release entry does not automatically expand its domain as a result.

<a id="p5-example-r04h"></a>
**Synthetic substitution into the real control function.** style=0.5, tone=0.25, original structure=2; at reset the two masks=(2,2), and with history mask=(1,2), while the remaining bindings satisfy the restricted entry above:

| Case | p5/reset/temporal | half values of feat[10..15] | Corresponding half encodings |
|---|---|---|---|
| reset | true/true/false | 0.5, 0.25, 1, 2, 2, +0 | 3800 3400 3c00 4000 4000 0000 |
| history | true/false/true | 0.5, 0.25, 1, 1, 2, +0 | 3800 3400 3c00 3c00 4000 0000 |

The [real-code script](../skewer/examples/param_change_r04h.py) and [scalar result](../skewer/examples/param_change_r04h.result.json) compute only the synthetic CB and do not execute the network or sampling.

<a id="coordinates"></a>
### L3.b0.coordinates MV to History Pixel Center: Explicit F32 Fusion Boundaries

- What it is: Constructs the history sampling center and fractional offsets from the two MV half values at the current image position.
- Input → output: Mirrored tx,ty, id3[ty,tx], CB+0xa0 (f32)/CB+0xa4 (f32), W/H → x0,y0,t,v.
- How it is computed:
  ~~~text
  1. rw=F32/(1,W), rh=F32/(1,H); MV address=(ty×W+tx)×4 B.
  2. ax=F32_FMA(F32(mv_x),CB+0xa0 (f32),F32×(tx+0.5,rw)).
  3. ay=F32_FMA(F32(mv_y),CB+0xa4 (f32),F32×(ty+0.5,rh)).
  4. x0=F32+(floor(F32_FMA(W,ax,−0.5)),0.5).
  5. y0=F32+(floor(F32_FMA(H,ay,−0.5)),0.5).
  6. t=clamp(F32_FMA(W,ax,−x0),0,1).
  7. v=clamp(F32_FMA(H,ay,−y0),0,1).
  ~~~
- Numeric rules: The fusion of [FMA](APPENDIX_beginner_glossary.md#g063) must span the corresponding multiply-add and cannot perform F32× first and F32+ second; its result also affects floor and the subsequent fixed-point sampling grid. native_temporal.hpp makes these boundaries explicit using volatile F32 operations and std::fma. F32/ is the F32 division in the current C++; it is not arbitrarily replaced here by a reciprocal table or library approximation. The current implementation fetches MV directly by pixel; the evidence that this matches an explicit MV sampling chain is scoped to the verified input / coordinate domain and is not extrapolated to arbitrary [descriptors](APPENDIX_beginner_glossary.md#g088) or host coordinate transforms.
- How we know: CENSUS, [native_temporal.hpp:5–9, 27–33](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L27); MEASURED / domain-scoped verification, [native divergence RESULT:9–28](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#根因与证据), where the three audit categories fma_domain, coordinate_domain, and mv_domain respectively scope the basis for the operations and direct fetching.
- Next down: [5-tap Positions and Weights](#five-tap), [How the 25 KB Divergence Was Closed](#evidence).

<a id="five-tap"></a>
### L3.b0.five-tap Four Sidelobes Plus One Bilinear Center

- What it is: Forms five history texture sampling points from two one-dimensional cubic reconstruction coefficient sets, and then merges them in a fixed F32 order.
- Input → output: x0,y0,t,v, history id6 → three history half values, written to channels 7–9 after the input transform.
- How it is computed:
  ~~~text
  1. For s=t and s=v separately, compute s2=F32×(s,s), s3=F32×(s,s2).
  2. L=F32_FMA(F32+(s,s3),−0.5,s2); M0=F32+(F32_FMA(s3,1.5,−F32×(s2,2.5)),1).
  3. R=F32×(F32+(s3,−s2),0.5); M1=F32+(F32+(F32+(1,−L),−M0),−R).
  4. C=F32+(M0,M1); denote the results on the two axes by Lx/M1x/Rx/Cx and Ly/M1y/Ry/Cy.
  5. xc=clip(F32_FMA(M1x,F32/(1,Cx),x0),0.5,W−0.5); yc corresponds on the other axis.
  6. xl=clip(F32+(x0,−1),0.5,W−0.5), xr=clip(F32+(x0,2),0.5,W−0.5); yt/yb correspond on the other axis.
  7. wl=F32×(Lx,Cy), wt=F32×(Ly,Cx), wc=F32×(Cx,Cy), wb=F32×(Ry,Cx), wr=F32×(Rx,Cy).
  8. den=F32+(F32+(F32+(F32+(wl,wt),wc),wb),wr).
  9. value=F32×(TEX(xc,yt),wt); value=F32_FMA(TEX(xl,yc),wl,value).
  10. value=F32_FMA(TEX(xc,yc),wc,value); value=F32_FMA(TEX(xc,yb),wb,value).
  11. value=F32_FMA(TEX(xr,yc),wr,value); value=F32×(value,F32/(1,den)).
  12. history_half=RN16(value); out=H×(H+(history_half,half(−0.5)),RN16(F32×(CB+0xc4 (f32),2))).
  ~~~
- Numeric rules: Lines 9–11 are executed once for each of R, G, and B; the top→left→center→bottom→right accumulation order is distinct from the left→top→center→bottom→right denominator order. Sidelobe weights can be negative; the contract of nonnegative weights inside TEX cannot substitute for the 5-tap weights. History undergoes RN16 first, then subtracts 0.5, and then performs half multiplication; it does not chain the color transforms in F32 followed by a single RN16. CB+0xc4 (f32) interprets the same parameter bit pattern as F32, which is not equal to its U32 numeric value. Out-of-bounds history coordinates [clamp](APPENDIX_beginner_glossary.md#g049) to the boundary center and do not switch to current color on account of being out of bounds.
- How we know: CENSUS, [native_temporal.hpp:34–48](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/native_temporal.hpp#L34); MEASURED, [full / pool gates of native divergence:15–28](../../../experiments/parity-video-b00-native-divergence-r01-20261006-codex/RESULT_ZH.md#隔离原型及独立验证).
- Next down: [4-Neighborhood Filtering of Each TEX](#texture), [half Publication](L4_half_arith.md#half-arith).

<a id="texture"></a>
## Filtering Interface of Each tap

TEX receives F32 pixel-center coordinates and a finite RGBA16F 4-neighborhood, returns a half published according to the texture rules, and then expands it to F32 for 5-tap merging. The 1/256 fixed-point subpixel grid, joint 8-bit fractional weights, shared-[exponent](APPENDIX_beginner_glossary.md#g058) truncation, negative zero, and midpoints rounding away from zero are all preserved and cannot be replaced by ordinary bilinear + RN-even. Drill down to L4 for the [complete arithmetic and two single-point examples](L4_tex_filter.md#tex-filter); for the named hardware scope, still see [B0 evidence](#evidence).

<a id="adapter"></a>
### L3.b0.adapter 16→32 Adaptation and the First One-Head Window Block

- What it is: Adaptation turns the conditioning vector into [features](APPENDIX_beginner_glossary.md#g008); the 64 positions in each window then pass through feed-forward and window attention.
- Input → output: half[64,16], half adapter coefficients[16,32], E4 matrices, and half scales / biases → half[64,32].
- How it is computed:
  ~~~text
  1. At each position, a[c]=HMMA_K16(feat[0:16],adapter[:,c]), c=0..31; xc=Q8(a).
  2. h[128]=G(QMMA_K32(xc,W_expand)); the gate-function exit is E4.
  3. z[c]=H×(a[c],s_ff[c]).
  4. Contract over s=0,1,2,3: z[c]=QMMA_K32(h[s×32:s×32+32],W_contract[s,:,c],seed=z[c]).
  5. Q8(z) projects Q/K/V separately: one K32 per column; V is published directly as E4.
  6. Q and K each undergo 32-channel norm32; Q is then multiplied by the query scale, published in turn as half, and converted to E4.
  7. This window's 64×64 biased QK scores → weight transform → specified denominator tree / reciprocal → E4 weights.
  8. AV performs two K32 steps over keys 0..31 and 32..63, carrying a half accumulator; then publishes E4.
  9. Final y[c]=QMMA_K32(Q8(AV),W_proj[:,c],seed=H×(z[c],s_att[c])).
  ~~~
- Numeric rules: Adaptation uses half×half [K16](APPENDIX_beginner_glossary.md#g065), not E4 K32; its current implementation truncates products onto a common grid, sums them as integers, and applies RN16 at the end—see the source code below. The adapter residual retains the half value of a and cannot be recovered from [quantized](APPENDIX_beginner_glossary.md#g061) xc. Subsequent half publications at each K32, [activation](APPENDIX_beginner_glossary.md#g045) quantization, Q/K [normalization](APPENDIX_beginner_glossary.md#g043), and attention weight ordering each follow the already expanded topics without substituting generic BLAS / [softmax](APPENDIX_beginner_glossary.md#g047). The [exact arithmetic, 128 channels, and adapter half residual](L3_ffn.md#gate) of G are listed separately; it is a single-input clamped piecewise polynomial, not a paired-channel gate.
- How we know: CENSUS, [b00.hpp:6–26, 41–51](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L41); the uncached adapter contract [mapexec_base.hpp:157–174](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/mapexec_base.hpp#L157) and the cached version [decode_reuse.inc:71–105](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/decode_reuse.inc#L71) are listed separately; for numeric gates, see the [evidence table](#evidence).
- Next down: [QMMA Matrix Chain](L3_qmma_e4m3.md#qmma-e4m3), [norm32](L3_norm_nonfinite.md#norm32), [Window attention](L3_attention_softmax.md#window-attention), [Dual Exits](#publish).

Adapter coefficients are stored as half; matrix coefficients for feed-forward expansion / contraction, QKV, and final projection are stored as E4. Feed-forward / attention residual scales and [position biases](APPENDIX_beginner_glossary.md#g052) are half, and the query scale is converted from F32 in the resource to half. Only storage and consumption boundaries are described here; no weight numeric values are listed, and weights are not treated as algorithmic constants.

<a id="publish"></a>
### L3.b0.publish Publishing full and pool Separately from the Same half Result

- What it is: Quantizes the high-resolution exit directly, and performs a 2×2 half average along the other path.
- Input → output: Per-window y[8,8,32] half → [TIN](APPENDIX_beginner_glossary.md#g011) 4×4 tile layout for full and two-group channel-planar layout for pool, both as E4 bytes.
- How it is computed:
  ~~~text
  1. For each x,y,c: full[full_offset(x,y,c)]=Q8(Y_half[y,x,c]), where Y_half is this block's half result.
  2. For each 2×2 and channel c: even=H+(y00,y01), odd=H+(y10,y11).
  3. avg=H×(H+(even,odd),half(0.25)); finally pool=Q8(avg).
  4. full: tile=(y//4)×(Wn//4)+x//4; lane=(x%4)×4+(y%2)×16+(c%8)//2.
  5. b=((y//2)%2)×4+c%2+((c//8)%2)×2+(c//16)×8; offset=tile×512+lane×16+b.
  6. pool for physical channel p=0..31: c=(p//16)×16+((p%16)//4)×2+p%2+((p%4)//2)×8.
  7. At pooled full-image position X,Y: offset=(p//16)×(Wn//2)×(Hn//2)×16
       +(Y×(Wn//2)+X)×16+p%16.
  8. full writes the interval pointed to by CB+0xd8 (u64); pool writes the interval pointed to by CB+0xf8 (u64).
  ~~~
- Numeric rules: pool consists of three half additions and one half multiplication, quantized only at the end; it is not read from the already quantized full. full has length WnHn×32 B, and pool has length (Wn/2)(Hn/2)×32 B. The formulas give the explicit physical arrangements; contiguous logical channels do not imply contiguous bytes on disk / in the [workspace](APPENDIX_beginner_glossary.md#g082).
- How we know: CENSUS, [b00.hpp:63–68](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L63), corresponding to the [original pooling description in L1.02](L1_02_input_b0.md); this round also checks the rounding effect using a [synthetic half example](#worked-example).
- Next down: [E4 Publication](L4_e4m3_and_k32.md#e4m3-format), [half Primitives](L4_half_arith.md#half-arith); this B0 output layout bottoms out here.

### One Substitution Point for full/pool

[Real Output-Loop Computation] The [script](../skewer/examples/substitutions_r04g.py) extracts the index expressions of the output loop in b00.hpp verbatim. Taking internal canvas 1920×1152 and full point (x,y,c)=(1,2,3): tile=0, parallel position index=5, and byte selection=5, so offset=0×512+5×16+5=**85 B** (0b01010101). Its bit fields come from the spatial tile, the 16 B vector index, and the intra-vector channel/row selection respectively.

For pool, separately take logical point (X,Y,c)=(1,2,3), which reverse-maps to physical channel p=5; the first-plane offset is (2×960+1)×16+5=**30,741 B**. This pool point corresponds to the 2×2 source positions (2,4)/(3,4)/(2,5)/(3,5) in the original window and does not share coordinates with full point (1,2). The [computed output](../skewer/examples/substitutions_r04g.result.json) gives both 85 and 30741; indexing adds no numeric rounding.

<a id="evidence"></a>
## Existing Verification and Open Scope

[Verification Record] Saved microbenchmarks, fusion-boundary isolated B0, and named CPU own-state multiframe gates each compare different objects; [round-by-round results, counts, raw/frozen sources, and debug-export root causes](APPENDIX_evidence_history.md#b0-evidence) have been moved. Some legacy original-round directories are not retained on this machine, and the corresponding numbers rely only on frozen summaries without claiming to re-read raw outputs. Four-way replay agreement can still diverge jointly from native; the actual FMA fusion boundaries in the main text must be preserved, and intermediate debug exports must not be turned into extra rounding points.

Legacy R04/R06 remain DIFF, and legacy R06 f2 is NOT_RUN; isolated B0 is a [teacher-forced](APPENDIX_beginner_glossary.md#g106) single launch where f3 uses f2 id9 from another capture and f4/f5 are NOT_RUN_MISSING_NATIVE_HISTORY. Native sampler descriptors remain UNKNOWN, and legacy cross-device coordinate prefixes are not a two-dimensional full-domain proof. Legacy reset-only records are retained as of their respective dates; evidence for the restricted p5 branch is collected in the [parameter branch ledger](APPENDIX_evidence_history.md#param-change).

1080 f0–f5 / 1440 f0–f3 of 854 and 4K f0–f2 of unified M are bound to their respective builds and are not called new [M2](APPENDIX_beginner_glossary.md#g107) multiframe gates; at 1440, the six textures of f1/f2 have only five points in time, and f3 translates the input and continues across processes; 4K f3+ and independent history perturbations are not run, and the early comparison of A5 separates the written region / retained [complement](APPENDIX_beginner_glossary.md#g093). Arbitrary content, unique internal structure, or hardware equivalence are not inferred from chain gates.

<a id="worked-example"></a>
## Worked Calculation Example: One Coordinate, Two Native Frame Words

The small appendix script was actually executed in the original writing round with the repository root as the working directory; it reads only the three compact assets above and verifies their SHAs, then looks up five entries and computes the three-channel noise according to the C++ formulas. It neither imports the network nor reads prediction targets. Integer division in Python is explicitly floor, and struct f/e conversions are used to publish F32 / half.

[Complete script and certified SHAs](APPENDIX_cpu_storage.md#noise-example) have been moved to the appendix; the original execution output is retained below, and the original run scope is in the evidence appendix.

The asset SHAs of the actual output are 3/3 MATCH; fixing x=y=0:

| f | [k0,k1,k2,k3] | half values of feat[0:3] | half encodings |
|---:|---|---|---|
| 0 | [11369803,9653346,12969588,4756067] | [−0.2196044921875,1.0283203125,0.1273193359375] | [0xb307,0x3c1d,0x3013] |
| 1 | [13874273,8098557,8117985,11021557] | [−0.666015625,−1.0068359375,−0.61328125] | [0xb954,0xbc07,0xb8e8] |

For f=0, the F32 products are −0.21956901252269745, 1.0282138586044312, and 0.12729476392269135 in order; the RN16 results in the table appear only afterward. The example also shows that changing the frame word at a fixed position changes the noise while the output channel order remains fixed.

At the end, pooling is also checked using the synthetic 2×2 half input [[2048,1],[−2048,1]]: H+(2048,1)=2048, H+(−2048,1)=−2047, and final avg=0.25; direct real-number averaging gives 0.5. This tests the rounding order here without containing any model weights or native outputs, and is not a new B00 byte gate.

F16 matrix arithmetic drills down further: [L4.hmma: K16 Common Grid, seed, Publication, and Hardware Boundaries](L4_hmma.md#hmma).

### 5-tap: One Synthetic History Pixel

[Real-Code Computation] Take a 4×4 synthetic history RGB: hist[y,x,c]=(x+2y+c+1)/16; pixel (x,y)=(1,1), MV=(0.0625,−0.0625), scales of 1 on both axes, and gain parameter 0.5. The real native_history_pixel gives x0=1.5, y0=0.5, t=0.25, v=0.75, and center xc≈1.70714283, yc≈1.29285717.

The L/T/C/B/R weights are −0.07690429688, −0.02563476562, 1.196289062, −0.07690429688, and −0.02563476562 in order; the denominator is 0.9912109375. In the actual T/L/C/B/R sampling order, the R channel yields 0.1379394531, 0.1616210938, 0.2370605469, 0.3879394531, and 0.3491210938, and then still executes the original F32 fusion / division by the denominator, RN16, half subtraction of 0.5, and half multiplication by gain.

The final three half encodings are **b44e b29c b09c**. In the [complete computation / source SHAs](../skewer/examples/substitutions_r04g.result.json), the original function and the trace copy that only adds output prints are identical across all six bytes; for truncation and midpoint examples of the sampler itself, see [L4.tex-filter](L4_tex_filter.md#worked-example). This synthetic point does not represent full-launch B0 acceptance.
