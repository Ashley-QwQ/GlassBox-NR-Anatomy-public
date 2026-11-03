# Appendix: Storage and Lossless Encoding of CPU Function Assets

> Some evidence links on this page point into the authors' private project archive (`../../../experiments/…`, `E:/…` and similar); they do not open in the public repository and are kept as provenance records. See the [evidence path legend](INDEX.md#private-links).

<!-- beginner-r04m:start expert -->
> Beginners may skip this page and read it when needed. Finish [Full Frame](L0_frame.md#beginner-frame), [One Block](L1_00_one_block_primer.md), and [Number Points](L1_00_numbers_primer.md) first; this page retains the exact [contracts](APPENDIX_beginner_glossary.md#g101) and evidence.
<!-- beginner-r04m:end expert -->

[Full Skewer Index](INDEX.md) · [One-Frame Entry](L0_frame.md)

This page migrates existing main-text material from before r04a; "this round" in the text carries over the context of the original writing round and does not denote a new measurement in r04a. r04a modifies only documentation, with 0 [GPU](APPENDIX_beginner_glossary.md#g078) / model / continuous-chain runs. [Native behavior](APPENDIX_beginner_glossary.md#g001), CPU representations, and [verification records](APPENDIX_beginner_glossary.md#g100) are kept separate, and legacy [NOT_RUN](APPENDIX_beginner_glossary.md#g104), UNKNOWN, rejections, and failures are not relabeled.

Appendix scripts still run from the repository root; computed numeric values are records from the original writing round and were not re-run in this round. Storage notation: T_f is the measured [bit-pattern](APPENDIX_beginner_glossary.md#g057) map, b is the input [encoding](APPENDIX_beginner_glossary.md#g057), q/j are the block index / intra-block index with B=512; A/Z are endpoint integer bit patterns, P/R/I are the predicted / residual / reconstructed integers, and zz is the [zigzag](APPENDIX_beginner_glossary.md#g097) encoding. Data and algorithmic constants here do not list model coefficients.

<a id="noise-codec"></a>
## B0 DNOISE01: Complete Format, Loading, and Asset Identity

Moved from [L3_b0_input.md](L3_b0_input.md); below is the record saved from the original writing round.

<a id="compact"></a>
### L3.b0.compact Lossless Bit-Pattern Residuals, Not Function Approximation

- What it is: Three DNOISE01 files are indexed by k, adding a complete integer residual to per-block endpoint prediction to reconstruct the original [F32](APPENDIX_beginner_glossary.md#g056) bit pattern.
- Input → output: Three certified files, k∈[1,2²⁴] → raw U32 bit patterns of radius / trigonometric functions; no full-frame noise cache.
- How it is computed:
  ~~~text
  1. Header is 24 B: magic, N, B, NB, payload byte count; fields are read explicitly as little-endian.
  2. Instance N=2²⁴, B=512, NB=32768; i=k−1, block=i//B, lane=i%B.
  3. Read this block's endpoints A, Z, residual bit width w, and payload offset o.
  4. Extract a w-bit zz with bounds checking from bit=lane×w; read at most 5 bytes.
  5. residual = −(zz>>1)−1 when zz is odd, otherwise zz>>1.
  6. I=A+floor((Z−A)×lane/511)+residual; return the U32 bit pattern after range checking.
  7. Format checks on N/B/NB, w≤33, contiguous offsets, and exact total length; additionally certify contents by fixed SHA.
  8. Prepare the three tables before L2; b00 hands off to a local owner for this invocation and releases after all windows finish.
  ~~~
- Numeric rules: Prediction is performed on integer bit patterns, not numeric [interpolation](APPENDIX_beginner_glossary.md#g020); every residual is saved. Division of negative numbers must use floor and cannot be replaced by C++ truncation-toward-zero division. Metadata consists of A[NB], Z[NB], u8 bit widths[NB], and u32 offsets[NB], starting at 24, 24+4NB, 24+8NB, and 24+9NB in order, with the payload starting at 24+13NB. w=0 has an explicit zero-residual path; when fewer than five bytes remain at the tail, zeros are padded only in the extraction window without reading past the end of the file.
- Why it is computed this way: Exploits the regularity of bit patterns across adjacent keys to reduce storage; all irregular entries are preserved by the residuals without relying on cosine symmetry or library function approximations.
- How we know: CENSUS, [compact_noise_optd.hpp:40–95](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L40), [noise_exports_optd.inc:2–22](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L2), [b00.hpp:61–67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L61); offline full-table and independent re-verification, [D RESULT:29–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#q4-每表精确表示).
- Next down: [Measurement and Acceptance Domains of MUFU Tables](L4_mufu.md#representation), [Key Lookup Example in This Round](L3_b0_input.md#worked-example).

| Online asset | Bytes | Certified [SHA](APPENDIX_beginner_glossary.md#g103)-256 |
|---|---:|---|
| [sqrt_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/sqrt_k_exact.dnc) | 5,675,352 | 2c42bbbabc3ad60efe6f33096539786955e2885c182422cb9c07669f88ec540e |
| [cos_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/cos_k_exact.dnc) | 8,635,352 | d95b2ad4375921cc8da901e57ef8b46bef566c14ee84fe6aad3756025b3db5b3 |
| [sin_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/sin_k_exact.dnc) | 8,650,456 | 1ffe7b333e0155adb16ea1b8232c38013a3321bf6978ce07ddacdb6396fef1e3 |

Total 22,961,160 B, i.e., 21.897469 MiB; this is not the running process RSS. Each table has 2²⁴ k indices, whereas the raw [SQRT](APPENDIX_beginner_glossary.md#g073) has only 16,776,341 unique inputs; reconstructed values for duplicate inputs also match bit for bit. Another [LG2](APPENDIX_beginner_glossary.md#g072) bit-plane encoding in compact_noise_optd.hpp is not the online entry point for these three tables. The D proof round itself ran no new noise primitives or [launch](APPENDIX_beginner_glossary.md#g080) gates; its zero-difference reconstruction cannot be called B00 numeric acceptance.

<a id="raw-registry"></a>
## raw32 Chunking, Raw-Value Registry, and Memory Slots

Moved from [L4_mufu.md](L4_mufu.md); below is the record saved from the original writing round.

A full raw32→raw32 table has $2^{32}$ entries, or 16 GiB uncompressed; "[full-domain](APPENDIX_beginner_glossary.md#g111) measurement" does not require the CPU to keep it all resident in memory. By input encoding:

```math
q=b\mathbin{\gg}23,\qquad j=b\mathbin{\&}0x7fffff,\qquad
T_f(b)=\mathrm{LE32}(\mathrm{block}_f[q],4j).
```

q contains both the sign and the stored [exponent](APPENDIX_beginner_glossary.md#g058), giving 512 blocks in total; each block has $2^{23}$ entries, or 33,554,432 B. The current tail raw-value registry looks up only registered members and contains two 32 MiB mapping slots; unregistered queries return a missing-member result. Registration verifies the SHA actually read; on a cache miss, before swapping in a mapping, it performs fstat and checks the fd identity, rejecting detected changes; a cache hit directly reuses already-mapped pages without re-checking identity on every query. [GlassBox-NR/cpp/chain_outtail_optm/full_raw_registry.hpp:14–40, 47–62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L14). This is a storage/read boundary, not a general network reachability certificate, nor does it claim to have reproduced numeric changes induced by external modifications.

<a id="mufu-storage"></a>
## LG2 E1, Composed Noise Tables, and D03/D02 Storage

Moved from [L4_mufu.md](L4_mufu.md); below is the record saved from the original writing round.

### lg2_decoder.hpp: Exact Reconstruction from 544 MiB to 67 MiB

For [E1](APPENDIX_beginner_glossary.md#g110) reconstruction arithmetic, see [L4.mufu](L4_mufu.md#representation). Only storage facts are retained here: the 17 raw exponent blocks total 544 MiB; the legacy-domain representation instead uses two 32 MiB raw-value tables and 3 MiB of levels, totaling 67 MiB. [stage_codec.inc](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L42) binds these payloads without treating the capacity reduction as a function approximation.

The evidence in [original E1 RESULT:5–19](../../../experiments/parity-cpp-opt-e1-r01-20261001-codex/RESULT_ZH.md#L5) is the reconstruction of all $17\cdot2^{23}$ entries, not that full raw32 or a [full-chain gate](APPENDIX_beginner_glossary.md#g102) had already been completed at the time; the legacy NOT_RUN is retained. Subsequent extrapolation of the fixed formula to e=1..110 failed on block 110, with first difference at 0x00804a35, so those segments and other specified positive [normal](APPENDIX_beginner_glossary.md#g068) segments use raw values instead, [full-domain candidate RESULT:17](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#L17). **The decoder depends on measured base, levels, and raw-value exceptions; it is not a closed-form lg2.**

### B0's sqrt_k_exact.dnc: Compressing Bit Patterns, Not Approximating a Function

Let $u=k2^{-24}$, $1\le k\le2^{24}$. Here $T_f$ still denotes the raw bit-pattern map; the floating-point expression uses the [MUFU numeric wrapper](L4_mufu.md#value-wrapper) $\widehat{T}_f(x)=\mathrm{value}_{32}(T_f(\mathrm{bits}_{32}(x)))$, which takes the F32 encoding first and decodes the lookup result back to an F32 value without adding rounding. $c_{\ln2}$ is the algorithmic constant represented by the F32 encoding `0x3f317218` in [B0 noise](L3_b0_input.md#noise). The numeric value of the precomposed radius is
```math
Radius(k)=\widehat{T}_{\mathrm{sqrt}}\!\left(
 \mathrm{RN}_{32}\left(
 \mathrm{RN}_{32}(\widehat{T}_{\mathrm{lg2}}(u)\cdot c_{\ln2})\cdot(-2)
 \right)\right).
```

The two multiplications above produce no nonzero F32 subnormal results within the frozen table domain, so the underlying FTZ does not alter these nonzero values; this offline domain check does not equal runtime acceptance and does not cover arbitrary sqrt inputs. [noise_dataflow_ZH.md:24, 69](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/noise_dataflow_ZH.md#L24). What sqrt_k_exact.dnc stores is this exact result, **not sqrt(u)**. The per-k table values for sin/cos also include the angle pre-[scaling](APPENDIX_beginner_glossary.md#g031) and [toward-zero](APPENDIX_beginner_glossary.md#g060) reduction of the original wrapper; the online path must not perform reduction a second time. [noise proof RESULT:9–11, 25–42](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L9).

DNOISE01 is explicitly LE: a 24 B header followed by per-block start/end uint32 values, a one-byte width per block, uint32 offsets, and the residual payload. Every B entries form one block; for entry j,
```math
P=A+\left\lfloor\frac{(Z-A)j}{B-1}\right\rfloor,\qquad
R=
\begin{cases}
\mathrm{zz}/2,&\mathrm{zz}\text{ is even},\\
-(\mathrm{zz}\mathbin{\gg}1)-1,&\mathrm{zz}\text{ is odd},
\end{cases}
\qquad I=P+R.
```

I is the **integer bit pattern** of the output floating-point number; every residual is saved in full, and the predictor bears no numeric approximation. C++ must apply floor to negative numerators and cannot directly use signed truncation-toward-zero division. The source code extracts the residual from a bounded window of at most five bytes, with the structure permitting up to 33 bits; format validation is kept separate from external SHA certification. [compact_noise_optd.hpp:18–37, 47–65, 79–95](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L79).

The three online radius/cos/sin payloads are 5,675,352, 8,635,352, and 8,650,456 B respectively, totaling **21.897469 MiB**; the loader compiles the expected SHAs into the code, [noise_exports_optd.inc:6–18](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L6). At runtime, two radius lookups and three trigonometric table lookups are followed by three F32 multiplications and [half](APPENDIX_beginner_glossary.md#g054) [publication](APPENDIX_beginner_glossary.md#g091), [noise_online_optd.hpp:24–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L24), [noise_exports_optd.inc:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L23).

The offline report reconstructed all k entries item by item and cross-checked them independently; the raw SQRT has 16,776,341 unique inputs corresponding to $2^{24}$ values of k, and results on duplicate inputs also match. [noise proof RESULT:25–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L25). That report explicitly stated at the time that "execution acceptance was not run", which cannot be rewritten from compressed reconstruction as full-chain verification at the time. A separate compressed LG2 table used for the proof still remains in the latter half of the code, but the production online radius path does not load it, [compact_noise_optd.hpp:99–145](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L99).

### D03 / D02: Reachable-Block Reduction and the Scope of Raw-Value Reads

Enumeration across the four single-half call sites in L157 yields LG2 blocks 0, 103..126 (25 blocks) and EX2 blocks 379..387, 511 (10 blocks); the code first checks membership at the corresponding site, [reach_sites.hpp:3–6](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/reach_sites.hpp#L3), [outtail.cpp:68–69](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L68). These are the input blocks after passing through the current wrapper, not the complete domain of the functions across all scenarios.

The cross-channel color branch lg(gray?1:S) is still not covered by the single-input enumeration above; the raw-value segments it requires cannot be deleted on that basis. D02 compresses the RCP zero-exponent block into a single uint32 of a bound parent block; the wrapper maps any e=0 input to that positive-zero word and then restores the sign. [full_raw_registry.hpp:32, 51–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L32), [outtail.cpp:53, 75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53).

[reach resume4 RESULT:19–24, 45–49](../../../experiments/parity-cpp-mufu-reach-d03-d02-resume4-20261010-claude/RESULT_ZH.md#L19) records 241 representation members, old-vs.-new software values+validity gates across full raw32 for the three primitives, and three positive controls; this does not make all LG2/EX2 inputs accepted, nor does it close the cross-channel domain. That round's isolated candidate not being merged is a historical state; the current release still retains the large-table payloads, and theoretical D03 trimming cannot be treated as though all payloads have disappeared, [ARCH 0.7:921](../../../ARCHITECTURE_V3_ZH.md#L921). Nor does the two-slot mapping capacity equal the peak memory of the entire process.

<a id="noise-example"></a>
## Complete Runnable Script for Noise Key Lookup and Pooling

Moved from [L3_b0_input.md](L3_b0_input.md); below is the record saved from the original writing round.

~~~python
from pathlib import Path
import hashlib, struct
root=Path("experiments/parity-cpp-d-noise-proof-r01-20261001-codex")
pins={
 "sqrt":(5675352,"2c42bbbabc3ad60efe6f33096539786955e2885c182422cb9c07669f88ec540e"),
 "cos":(8635352,"d95b2ad4375921cc8da901e57ef8b46bef566c14ee84fe6aad3756025b3db5b3"),
 "sin":(8650456,"1ffe7b333e0155adb16ea1b8232c38013a3321bf6978ce07ddacdb6396fef1e3")}
tables={}
for name,(length,sha) in pins.items():
 d=(root/(name+"_k_exact.dnc")).read_bytes()
 assert len(d)==length and hashlib.sha256(d).hexdigest()==sha
 assert d[:8]==b"DNOISE01"
 n,b,nb,payload=struct.unpack_from("<4I",d,8)
 assert (n,b,nb)==(1<<24,512,32768) and 24+13*nb+payload==len(d)
 tables[name]=d
def at(d,k):
 n,b,nb,_=struct.unpack_from("<4I",d,8)
 assert 1<=k<=n
 block,lane=divmod(k-1,b)
 a=struct.unpack_from("<I",d,24+4*block)[0]
 z=struct.unpack_from("<I",d,24+4*nb+4*block)[0]
 width=d[24+8*nb+block]; bit=lane*width
 offset=struct.unpack_from("<I",d,24+9*nb+4*block)[0]
 pos=24+13*nb+offset+bit//8
 zz=(int.from_bytes(d[pos:pos+5],"little")>>(bit%8))&((1<<width)-1)
 residual=-(zz>>1)-1 if zz&1 else zz>>1
 return a+(z-a)*lane//(b-1)+residual
def Hash32(v):
 v &= 0xffffffff
 return (((v>>((v>>28)+4))^v)*0x108ef2d9)&0xffffffff
def keys(x,y,f):
 s=((y*0xd8163841)&0xffffffff)^((x*0x8da6b343)&0xffffffff)
 s^=((f*0x9e3779b9)&0xffffffff)^0x243f6a88
 h=Hash32(s);h^=h>>22
 m=[0xcaa5b80d,0x2c9277b5,0x83232c31,0xfa6dc5f9]
 a=[0x21dd796b,0xac564b05,0x3463e0ac,0x4712a88e]
 v=[Hash32(h*mi+ai) for mi,ai in zip(m,a)]
 return [((vi>>30)^(vi>>8))+1 for vi in v]
def float32bits(bits): return struct.unpack("<f",struct.pack("<I",bits))[0]
def RN32(v): return struct.unpack("<f",struct.pack("<f",v))[0]
def RN16(v): return struct.unpack("<e",struct.pack("<e",v))[0]
def halfbits(v): return struct.unpack("<H",struct.pack("<e",v))[0]
print("asset_SHA: 3/3 MATCH")
for frame in [0,1]:
 k=keys(0,0,frame)
 r=[float32bits(at(tables["sqrt"],k[i])) for i in [0,1]]
 tri=[float32bits(at(tables[n],k[i])) for n,i in [("cos",3),("sin",3),("cos",2)]]
 out=[RN32(r[1 if i<2 else 0]*tri[i]) for i in range(3)]
 print("frame",frame,"keys",k)
 print("products_F32",out)
 print("half",[RN16(v) for v in out],"bits",[f"0x{halfbits(v):04x}" for v in out])
Hadd=lambda a,b: RN16(a+b)
pool=RN16(Hadd(Hadd(2048,1),Hadd(-2048,1))*0.25)
print("synthetic_pool",pool,"real_mean",(2048+1-2048+1)/4)
~~~

<a id="mufu-example"></a>
## Complete Script for Compact Function-Table Lookup and Edge Counterexample

Moved from [L4_mufu.md](L4_mufu.md); below is the record saved from the original writing round.

~~~python
import pathlib,struct,hashlib,json,math

# Read measured function data only; no model coefficients or GPU calls.
root=pathlib.Path(r"E:\dlssnr-pytorch-cpu-20260909")
p=root/"experiments/parity-cpp-d-noise-proof-r01-20261001-codex/sqrt_k_exact.dnc"
d=p.read_bytes()
assert len(d)==5675352
assert hashlib.sha256(d).hexdigest()=="2c42bbbabc3ad60efe6f33096539786955e2885c182422cb9c07669f88ec540e"
assert d[:8]==b"DNOISE01"
u32=lambda at:struct.unpack_from("<I",d,at)[0]
n,B,nb,payload_bytes=struct.unpack_from("<IIII",d,8)
assert (n,B,nb)==(1<<24,512,32768)
end,widths,offsets,payload=24+4*nb,24+8*nb,24+9*nb,24+13*nb
assert payload+payload_bytes==len(d)

def entry(k):
    assert 1<=k<=n
    block,j=divmod(k-1,B)
    A,Z=u32(24+4*block),u32(end+4*block)
    w,off=d[widths+block],u32(offsets+4*block)
    bit=j*w
    start=payload+off+bit//8
    window=int.from_bytes(d[start:min(start+5,len(d))],"little")
    zz=(window>>(bit&7))&((1<<w)-1)
    independent=sum(((d[payload+off+(bit+t)//8]>>((bit+t)%8))&1)<<t for t in range(w))
    assert zz==independent
    residual=-(zz>>1)-1 if zz&1 else zz>>1
    predictor=A+((Z-A)*j)//(B-1)  # floor, including negative numerators
    raw=predictor+residual
    value=struct.unpack("<f",struct.pack("<I",raw))[0]
    half=struct.unpack("<H",struct.pack("<e",value))[0]
    return block,j,A,Z,w,zz,residual,predictor,raw,half

v=entry(43)
print(f"k=43 block={v[0]} lane={v[1]} width={v[4]}")
print(f"A={v[2]:08x} Z={v[3]:08x} predictor={v[7]} zz={v[5]} residual={v[6]}")
print(f"radius={v[8]:08x} half={v[9]:04x}")
last=entry(n)
print(f"k={n} radius={last[8]:08x} half={last[9]:04x}")
assert (v[8],v[9],last[8],last[9])==(0x40a260c8,0x4513,0x80000000,0x8000)

edge=json.loads((root/"experiments/parity-mufu-probe-20260912/edge-cases.json").read_text(encoding="utf-8"))
name=next(k for k in edge["variants"] if k.split(".")[0]=="lg2" and "ftz" in k.split("."))
saved=edge["variants"][name]["edge_inputs"]["min_normal"]
x=struct.unpack("<f",struct.pack("<I",int(saved["input_bits"],16)))[0]
ideal=struct.unpack("<I",struct.pack("<f",math.log2(x)))[0]
print(f"LG2_saved={int(saved['result_bits'],16):08x} libm_F32={ideal:08x}")
assert int(saved["result_bits"],16)==0xc2fbffff and ideal==0xc2fc0000
~~~

<a id="mufu-example-output"></a>
## Original Record of the Compact Lookup: Decoded Intermediate Integers and stdout

Here a valid key is chosen manually, reading function assets without reading or listing model coefficients. k=43 corresponds to block 0 and intra-block j=42; the start and end bit patterns are A=0x40b89456 and Z=0x4091ec40, with width 22 bits. The integer prediction is P=1,085,630,197; extracting zz=2,493,529 and inverting zigzag gives R=−1,246,765. Therefore I=P+R=0x40a260c8, which is an F32 value of approximately 5.07431411743 and converts to half as **0x4513**. This value is the precomposed r(43), not directly sqrt(43·2⁻²⁴).

The script first verifies the actual SHA of this 5,675,352 B file, matching the compiled expectation of the public loader; it cross-checks the selected residual using two independent bit-extraction methods. The final entry separately checks negative zero. Lastly, it calls [libm](APPENDIX_beginner_glossary.md#g074) once solely for comparison against the saved LG2 edge encoding, without using it to generate production results.

For the complete certification script, see the preceding section of this appendix.

Actual stdout in this round:

~~~text
k=43 block=0 lane=42 width=22
A=40b89456 Z=4091ec40 predictor=1085630197 zz=2493529 residual=-1246765
radius=40a260c8 half=4513
k=16777216 radius=80000000 half=8000
LG2_saved=c2fbffff libm_F32=c2fc0000
~~~



<a id="mufu-ex2-codec"></a>
## EX2 Base Table and Negative-Axis Fallback Engineering

### ex2: Base-Table Scaling Cannot Be Extrapolated Unconditionally to All Negative Arguments

For positive/negative branch indexing and exponent-bit adjustments of EX2, see the [bit-level rules in L4.mufu](L4_mufu.md#representation). This section retains only the failing segments, raw-value fallback, and storage identities.

This does not evaluate the mathematical exponential directly. In the saved experiments, one block on the negative axis had **131,071 accepted positions with codec differences**, with first-difference input 0xc2fc0001; original validity was retained and raw-value fallback was used instead of writing the failure as the formula passing. [full-domain candidate RESULT:19–21, 25–38](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#b固定codec判定及原值回退). B70 can also match a named sparse input table first; see [stage_codec.inc:76–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L76), without expanding this into an arbitrary temporal parameter contract.


<a id="mufu-lg2-codec"></a>
## Saved Domain and Encoding Corrections of LG2 E1

[Storage History] The legacy domain of LG2 E1 is positive sign e=111..127; for unified bit-level rules, see [L4.mufu](L4_mufu.md#representation). Extrapolation to e=1..110 failed, so those segments and specified exception segments must read certified raw values or reject; the legacy full-chain NOT_RUN is not rewritten.


<a id="mufu-domain-storage"></a>
## Trimmed Members and Call Admission

D03 first checks that the input belongs to the admitted member set of the corresponding site, and does not let it pass otherwise; reachable blocks of single-half sites do not cover the cross-channel color branch, so call admission cannot be expanded or its raw-value segments deleted on that basis. The D02 RCP e=0 wrapper maps to the certified positive-zero word and then restores the sign, with other edges following the [specific wrappers](L4_mufu.md#edges). [Complete compressed formats, capacities, reachable-block lists, enumeration counts, and workstream history](APPENDIX_cpu_storage.md#mufu-storage) have been moved; the current release still retains the large-table payloads, and trimming theory does not mean all payloads have already been removed.


<a id="noise-codec-guards"></a>
## Format Rejection and Integer Decoding of B0 Noise Assets

[CPU Reconstruction] Valid k∈[1,2²⁴] queries look up identity-certified radius/cos/sin function assets to reconstruct the original F32 bit patterns without a full-frame noise cache; what is stored is the result of the original function chain, not a function approximation and not a file-decompression step of the native GPU. N/B/NB must match the fixed format, bit widths must lie in 0..33, offsets must be contiguous, total length must be exact with bounded reads, and the SHA is verified separately; any failure in format, length, or identity, or an out-of-domain k, is rejected; negative numerators in integer prediction must use floor and cannot be changed to truncation-toward-zero division.
