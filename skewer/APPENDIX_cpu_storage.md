# 附录：CPU 函数资产的存储与无损编码

> 本页有些证据链接指向作者的私有项目档案（`../../../experiments/…`、`E:/…` 等），在公开仓库里打不开，只作出处记录保留；说明见[证据路径图例](INDEX.md#private-links)。

<!-- beginner-r04m:start expert -->
> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确[合同](APPENDIX_beginner_glossary.md#g101)与证据。
<!-- beginner-r04m:end expert -->

[整串目录](INDEX.md) · [一帧入口](L0_frame.md)

本页迁移 r04a 之前正文已有材料；文中“本轮”沿用原写作轮语境，不表示 r04a 新测。r04a 只改文档，[GPU](APPENDIX_beginner_glossary.md#g078)／模型／连续链运行均为 0。[原生行为](APPENDIX_beginner_glossary.md#g001)、CPU 表示与[验证记录](APPENDIX_beginner_glossary.md#g100)分开，旧 [NOT_RUN](APPENDIX_beginner_glossary.md#g104)、UNKNOWN、拒绝及失败均不改标。

附录脚本仍从仓库根目录运行；实算数字为原写作轮记录，本轮没有重跑。存储记号：T_f 为实测[位型](APPENDIX_beginner_glossary.md#g057)映射，b 为输入[编码](APPENDIX_beginner_glossary.md#g057)，q/j 为块号/块内索引，B=512；A/Z 为端点整数位型，P/R/I 为预测/残差/重建整数，zz 为 [zigzag](APPENDIX_beginner_glossary.md#g097) 编码。这里的数据和算法常数不列模型系数。

<a id="noise-codec"></a>
## B0 DNOISE01：完整格式、加载与资产身份

迁自 [L3_b0_input.md](L3_b0_input.md)；以下是原写作轮保存的记录。

<a id="compact"></a>
### L3.b0.compact 无损位型残差，而非函数近似

- 是什么：三份 DNOISE01 文件按 k 定位，每块端点预测加上完整整数残差，重建原 [F32](APPENDIX_beginner_glossary.md#g056) 位型。
- 输入 → 输出：已认证的三份文件、k∈[1,2²⁴] → 半径 / 三角函数的原始 U32 位型；无整帧噪声缓存。
- 怎么算：
  ~~~text
  1. 头为 24 B：magic、N、B、NB、payload 字节数；字段显式按小端读取。
  2. 实例 N=2²⁴、B=512、NB=32768；i=k−1，block=i//B，lane=i%B。
  3. 读该块端点 A、Z、残差位宽 w、payload 偏移 o。
  4. 从 bit=lane×w 处有界提取 w 位 zz；最多读取 5 个字节。
  5. residual=zz 为奇数时 −(zz>>1)−1，否则 zz>>1。
  6. I=A+floor((Z−A)×lane/511)+residual；范围检查后返回 U32 位型。
  7. 格式检查 N/B/NB、w≤33、连续偏移、精确总长；另以固定 SHA 认证内容。
  8. L2 前准备三表；b00 移交给本次调用的局部 owner，窗口全部完成后释放。
  ~~~
- 数值规则：预测在整数位型上进行，不是数值[插值](APPENDIX_beginner_glossary.md#g020)；每项残差都保存。负数除法必须 floor，不能用 C++ 截零除法代替。元数据为 A[NB]、Z[NB]、u8 位宽[NB]、u32 偏移[NB]，起点依次为 24、24+4NB、24+8NB、24+9NB，payload 从 24+13NB 起。w=0 有显式零残差路径；尾部不足五字节只在提取窗口补零，不越界读文件。
- 为什么这么算：利用相邻键位型的规律减少存储；所有不规则项由残差保留，不依赖余弦对称或库函数近似。
- 我们怎么知道：CENSUS，[compact_noise_optd.hpp:40–95](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L40)、[noise_exports_optd.inc:2–22](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L2)、[b00.hpp:61–67](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/b00.hpp#L61)；离线全量与独立重核，[D RESULT:29–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#q4-每表精确表示)。
- 往下：[MUFU 表的测量与接受域](L4_mufu.md#representation)、[本轮键查询例](L3_b0_input.md#worked-example)。

| 在线资产 | 字节 | 认证 [SHA](APPENDIX_beginner_glossary.md#g103)-256 |
|---|---:|---|
| [sqrt_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/sqrt_k_exact.dnc) | 5,675,352 | 2c42bbbabc3ad60efe6f33096539786955e2885c182422cb9c07669f88ec540e |
| [cos_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/cos_k_exact.dnc) | 8,635,352 | d95b2ad4375921cc8da901e57ef8b46bef566c14ee84fe6aad3756025b3db5b3 |
| [sin_k_exact.dnc](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/sin_k_exact.dnc) | 8,650,456 | 1ffe7b333e0155adb16ea1b8232c38013a3321bf6978ce07ddacdb6396fef1e3 |

合计 22,961,160 B，即 21.897469 MiB；不是运行进程 RSS。每表有 2²⁴ 个 k 索引，但原始 [SQRT](APPENDIX_beginner_glossary.md#g073) 唯一输入只有 16,776,341 个；重复输入的重建值也逐位一致。compact_noise_optd.hpp 中另一套 [LG2](APPENDIX_beginner_glossary.md#g072) 位平面编码不是这三表的在线入口。D 证明轮本身没有跑新噪声原语或 [launch](APPENDIX_beginner_glossary.md#g080) 门；不能把它的重建零差异称为 B00 数值验收。

<a id="raw-registry"></a>
## raw32 分块、原值注册器及内存槽

迁自 [L4_mufu.md](L4_mufu.md)；以下是原写作轮保存的记录。

一张 raw32→raw32 全表有 $2^{32}$ 项，未压缩为 16 GiB；“[全域](APPENDIX_beginner_glossary.md#g111)测量”不要求 CPU 把它全部常驻。按输入编码：

```math
q=b\mathbin{\gg}23,\qquad j=b\mathbin{\&}0x7fffff,\qquad
T_f(b)=\mathrm{LE32}(\mathrm{block}_f[q],4j).
```

q 同时包含符号和存储[指数](APPENDIX_beginner_glossary.md#g058)，共 512 块；每块 $2^{23}$ 项、33,554,432 B。当前尾部原值注册器只对注册成员查找，含两个 32 MiB 映射槽；未注册返回缺成员。注册时校验实际读取SHA；缓存未命中、换入映射前做fstat并核fd身份，所检测的变化会拒绝；缓存命中直接复用已映射页，不逐查询重新核身份。[GlassBox-NR/cpp/chain_outtail_optm/full_raw_registry.hpp:14–40、47–62](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L14)。这是存储/读取边界，不是一般网络可达性证书，也不声称已复现外部修改引发的数值变化。

<a id="mufu-storage"></a>
## LG2 E1、噪声组合表与 D03/D02 存储

迁自 [L4_mufu.md](L4_mufu.md)；以下是原写作轮保存的记录。

### lg2_decoder.hpp：544 MiB 到 67 MiB 的精确重建

[E1](APPENDIX_beginner_glossary.md#g110)重建算术见[L4.mufu](L4_mufu.md#representation)。这里保留存储事实：17张原始指数块共544 MiB；旧域表示改用两张32 MiB原值表与3 MiB等级，共67 MiB。[stage_codec.inc](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L42)绑定这些载荷，不把容量变化当作函数近似。

[原 E1 RESULT:5–19](../../../experiments/parity-cpp-opt-e1-r01-20261001-codex/RESULT_ZH.md#L5) 的证据是全部 $17\cdot2^{23}$ 项重建，不是当时已完成全 raw32 或[整链门](APPENDIX_beginner_glossary.md#g102)；旧 NOT_RUN 保留。后续固定公式外推 e=1..110 在 110 块失败，首差 0x00804a35，故这些段和其他指定正[正规](APPENDIX_beginner_glossary.md#g068)段改用原值，[全域候选 RESULT:17](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#L17)。**解码器依赖实测 base、等级和原值例外，不是闭式 lg2。**

### B0 的 sqrt_k_exact.dnc：压缩的是位型，未近似函数

令 $u=k2^{-24}$，$1\le k\le2^{24}$。本节的 $T_f$ 仍表示原始位型映射；浮点式使用 [MUFU 数值包装](L4_mufu.md#value-wrapper) $\widehat{T}_f(x)=\mathrm{value}_{32}(T_f(\mathrm{bits}_{32}(x)))$，即先取 F32 编码、查询后再解码成 F32 值，不新增舍入。$c_{\ln2}$ 为 [B0 噪声](L3_b0_input.md#noise)中 F32 编码 `0x3f317218` 表示的算法常数。预组合半径的数值为
```math
Radius(k)=\widehat{T}_{\mathrm{sqrt}}\!\left(
 \mathrm{RN}_{32}\left(
 \mathrm{RN}_{32}(\widehat{T}_{\mathrm{lg2}}(u)\cdot c_{\ln2})\cdot(-2)
 \right)\right).
```

上述两次乘法在冻结表域内没有非零 F32 次正规结果，原 FTZ 不改变这些非零值；该离线域检查不等于运行验收，也不覆盖任意 sqrt 输入。[noise_dataflow_ZH.md:24、69](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/noise_dataflow_ZH.md#L24)。sqrt_k_exact.dnc 存的就是这个结果，**不是 sqrt(u)**。sin/cos 的按 k 表值还包含原包装的角度预[缩放](APPENDIX_beginner_glossary.md#g031)/[向零](APPENDIX_beginner_glossary.md#g060)归约；在线路径不得再归约一次。[噪声证明 RESULT:9–11、25–42](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L9)。

DNOISE01 为显式 LE：24 B 头，其后是块首/块尾 uint32、每块一字节宽度、uint32 偏移和残差载荷。每 B 项形成一块；对第 j 项，
```math
P=A+\left\lfloor\frac{(Z-A)j}{B-1}\right\rfloor,\qquad
R=
\begin{cases}
\mathrm{zz}/2,&\mathrm{zz}\text{ 为偶数},\\
-(\mathrm{zz}\mathbin{\gg}1)-1,&\mathrm{zz}\text{ 为奇数},
\end{cases}
\qquad I=P+R.
```

I 是输出浮点数的**整数位型**；每项残差完整保存，预测器不承担数值近似。C++ 必须对负分子作 floor，不能直接用有符号截零除法。源码从有界至多五字节窗口提取残差，结构允许 33 位；格式校验与外部 SHA 认证分开。[compact_noise_optd.hpp:18–37、47–65、79–95](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L79)。

三份在线半径/cos/sin 载荷分别为 5,675,352、8,635,352、8,650,456 B，合计 **21.897469 MiB**；加载器把预期 SHA 编译进代码，[noise_exports_optd.inc:6–18](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L6)。运行时两次半径、三次三角表查找，再三次 F32 乘法及 [half](APPENDIX_beginner_glossary.md#g054) [发布](APPENDIX_beginner_glossary.md#g091)，[noise_online_optd.hpp:24–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_online_optd.hpp#L24)、[noise_exports_optd.inc:23–28](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/noise_exports_optd.inc#L23)。

离线报告逐项重建了全部 k 并独立核对；其中原 SQRT 唯一输入 16,776,341 个，对应 $2^{24}$ 个 k，重复输入的结果也一致。[噪声证明 RESULT:25–48](../../../experiments/parity-cpp-d-noise-proof-r01-20261001-codex/RESULT_ZH.md#L25)。该报告当时明确“未跑执行验收”，不能由压缩重建改写成当时整链已验。证明用独立 LG2 压缩表仍存在于代码后半段，但生产在线半径路径不加载它，[compact_noise_optd.hpp:99–145](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_entry_optm/compact_noise_optd.hpp#L99)。

### D03 / D02：可达块缩减与原值读取的范围

四个 L157 单 half 调用点的枚举得到 LG2 块 0、103..126（25 块），EX2 块 379..387、511（10 块）；代码先按对应站点核成员，[reach_sites.hpp:3–6](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/reach_sites.hpp#L3)、[outtail.cpp:68–69](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L68)。这些是经过当前包装后的输入块，不是函数在所有场景的完整域。

跨通道颜色分支的 lg(gray?1:S) 仍不由上述单输入枚举覆盖；不能据此删除它需要的原值段。D02 把 RCP 零指数块压成已绑定父块的一个 uint32，包装将任意 e=0 输入归到该正零字，再恢复符号。[full_raw_registry.hpp:32、51–57](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/full_raw_registry.hpp#L32)、[outtail.cpp:53、75](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/outtail.cpp#L53)。

[reach resume4 RESULT:19–24、45–49](../../../experiments/parity-cpp-mufu-reach-d03-d02-resume4-20261010-claude/RESULT_ZH.md#L19) 记录 241 个表示成员、三原语完整 raw32 的新旧软件 values+validity 门与三阳控；它不等于把 LG2/EX2 全部输入都变为接受，也不关闭跨通道域。该轮隔离未合入是历史状态；当前发布仍保留大表载荷，不能把 D03 理论裁剪当成所有载荷已消失，[ARCH 0.7:921](../../../ARCHITECTURE_V3_ZH.md#L921)。两槽映射容量也不等于整个进程峰值内存。

<a id="noise-example"></a>
## 噪声键查询与池化的完整可运行脚本

迁自 [L3_b0_input.md](L3_b0_input.md)；以下是原写作轮保存的记录。

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
## 紧凑函数表查询与边缘反例的完整脚本

迁自 [L4_mufu.md](L4_mufu.md)；以下是原写作轮保存的记录。

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
## 紧凑查询的原记录：解码中间整数与 stdout

这里人工选择一个合法键，读取的是函数资产，未读取或列出模型系数。k=43 对应块 0、块内 j=42；首尾位型 A=0x40b89456、Z=0x4091ec40，宽度 22 位。整数预测 P=1,085,630,197；提取 zz=2,493,529，逆 zigzag 得 R=−1,246,765。因此 I=P+R=0x40a260c8，F32 值约 5.07431411743，转 half 为 **0x4513**。该值是预组合 r(43)，不是直接 sqrt(43·2⁻²⁴)。

脚本先校验这份 5,675,352 B 文件的实际 SHA，与公开加载器的编译预期相同；用两种独立位提取方式核对选中残差。末项另检查负零。最后只为比较而调用一次 [libm](APPENDIX_beginner_glossary.md#g074)，并与保存的 LG2 边缘编码比对，不用它生成生产结果。

完整认证脚本见本附录前节。

本轮实际 stdout：

~~~text
k=43 block=0 lane=42 width=22
A=40b89456 Z=4091ec40 predictor=1085630197 zz=2493529 residual=-1246765
radius=40a260c8 half=4513
k=16777216 radius=80000000 half=8000
LG2_saved=c2fbffff libm_F32=c2fc0000
~~~



<a id="mufu-ex2-codec"></a>
## EX2 的基表与负轴回退工程

### ex2：基表缩放，不能向所有负参数无条件外推

EX2的正负支索引及指数位调整见[L4.mufu位级规则](L4_mufu.md#representation)。本节只保留失败段、原值回退和存储身份。

这不是直接计算数学指数。保存实验中负轴一块有 **131,071 个接受位置 codec 差异**，首差输入 0xc2fc0001；保留原有效性后用原值回退，没有把失败写成公式通过。[全域候选 RESULT:19–21、25–38](../../../experiments/parity-cpp-mufu-fulldomain-r01-20261007-codex/RESULT_ZH.md#b固定codec判定及原值回退)。B70 还可先匹配具名稀疏输入表，见 [stage_codec.inc:76–81](https://github.com/Ashley-QwQ/GlassBox-NR/blob/e4a9b4214c723015ff4a99d73f13aa9a4a8ed1ec/cpp/chain_outtail_optm/stage_codec.inc#L76)，不扩大为任意时域参数合同。


<a id="mufu-lg2-codec"></a>
## LG2 E1 的保存域与编码修正

【存储历史】LG2 E1的旧域为正号e=111..127；位级规则统一见[L4.mufu](L4_mufu.md#representation)。e=1..110的外推失败，这些及指定例外段须读认证原值或拒绝；旧整链NOT_RUN不改写。


<a id="mufu-domain-storage"></a>
## 裁剪成员与调用准入

D03 先检查输入属于对应站点准入成员，否则不放行；单 half 站点可达块不覆盖跨通道颜色分支；不能由此扩大调用准入或删除其原值段。D02 的 RCP e=0 包装归到认证正零字再恢复符号，其他边缘按 [具体包装](L4_mufu.md#edges)。[完整压缩格式、容量、可达块列表、枚举计数和工作线历史](APPENDIX_cpu_storage.md#mufu-storage)已迁移；当前发布仍保留大表载荷，裁剪理论不等于载荷已全部移除。


<a id="noise-codec-guards"></a>
## B0 噪声资产的格式拒绝与整数解码

【CPU 重建】合法 k∈[1,2²⁴] 查询经身份认证的半径/cos/sin 函数资产，重建原 F32 位型，无整帧噪声缓存；它保存的是原函数链的结果，不是函数近似，也不是原生 GPU 的文件解压步骤。N/B/NB 必须匹配固定格式、位宽须在 0..33、偏移连续、总长精确并有界读取，另核 SHA；任一格式/长度/身份失败或 k 域外即拒绝；整数预测的负分子必须 floor，不能改成截零除法。
