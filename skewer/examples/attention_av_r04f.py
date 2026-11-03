"""Compare ViT and TIN AV publication using identical artificial scores/values.

Only certified RCP function data and scalar C++ helpers are read.
Run from the repository root: python -B -X utf8 skewer/examples/attention_av_r04f.py
[--source-root PATH] [--tables PATH] [--out FILE]; see _roots.py for where the inputs come from. No model,
saved network input/target, GPU or network chain is run.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import struct
import subprocess
import tempfile
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _roots as roots

CPP = roots.source_root() / "cpp"
helper = CPP / "fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp"
qmma = CPP / "chain_tin_optm/qmma_sm120.hpp"
asset = roots.table("rcp", "055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59")
guard = "".join(map(chr, (98, 108, 105, 110, 100)))
for path in (helper, qmma, asset):
    if any(guard in part.lower() for part in path.parts):
        raise RuntimeError("excluded path")
assert hashlib.sha256(asset.read_bytes()).hexdigest() == (
    "055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59")
with np.load(asset, allow_pickle=False) as z:
    rcp = z["native_half_bits"].copy()
    keys = z["input_half_bits"].copy()
assert np.array_equal(keys, np.arange(0x0410, 0x7c00, dtype=np.uint16))
text = helper.read_text(encoding="utf-8")


def function(name):
    match = re.search(r"^(?:double|int|uint8_t|uint16_t) " + name +
                      r"\([^\n]*?\)\s*\{", text, re.M)
    if not match:
        raise ValueError(name)
    start = text.index("{", match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[match.start():end]


parts = [function(name) for name in
         ("half_value", "half_round", "e4_units", "e4_half", "sat_e4",
          "h_add", "h_mul", "h_fma", "h_min", "h_max")]
header = "\n".join("#include <" + n + ">" for n in
                   ("algorithm", "bit", "cfenv", "cmath", "cstdint", "iomanip",
                    "iostream", "limits", "stdexcept", "string"))
header += '\n#include "' + qmma.as_posix() + '"\n'
main = r'''
uint16_t phi(uint16_t s,bool vit) {
    if(vit) {
        auto c=h_fma(s,half_round(.08953857421875),half_round(1.708984375));
        c=h_min(h_max(c,half_round(1.439453125)),half_round(1.9775390625));
        return uint16_t((unsigned(c)<<4)+0x4000);
    }
    float t=float(half_value(s))*.044921875f;
    t=t+1.30078125f;
    auto c=half_round(double(t));
    c=h_min(h_max(c,half_round(1.03125)),half_round(1.5693359375));
    return uint16_t((unsigned(c)<<5)+0x8000);
}
uint16_t den(const uint16_t* w,bool vit) {
    if(vit) {
        uint16_t b[2]{};
        for(int u=0;u<2;++u)
            for(int l=0;l<4;++l) {
                auto at=[&](int i){return w[8*i+2*l+u];};
                auto x=h_add(h_add(at(0),at(1)),h_add(at(2),at(3)));
                x=h_add(x,h_add(at(4),at(5)));x=h_add(x,h_add(at(6),at(7)));
                b[u]= l ? h_add(b[u],x) : x;
            }
        return h_add(b[0],b[1]);
    }
    auto leg=[&](int i){
        auto x=h_add(h_add(w[i],w[i+16]),h_add(w[i+4],w[i+20]));
        return h_add(h_add(x,h_add(w[i+32],w[i+48])),h_add(w[i+36],w[i+52]));
    };
    return h_add(h_add(h_add(h_add(leg(0),leg(2)),leg(8)),leg(10)),
                 h_add(h_add(h_add(leg(1),leg(3)),leg(9)),leg(11)));
}
int main(int argc,char** argv) {
    if(std::fegetround()!=FE_TONEAREST)throw std::runtime_error("RN required");
    static_assert(std::numeric_limits<double>::is_iec559);
    const double scores[8]={-8,-4,-2,-1,0,1,2,8};
    // Artificial values for one output channel, already representable in E4.
    const double values[8]={1,-1,2,-2,4,-4,8,-8};
    std::cout<<std::hex<<std::setfill('0');
    for(int family=0;family<2;++family) {
        bool vit=family==0;uint16_t w[64];uint8_t a[64],v[64];
        for(int i=0;i<64;++i){w[i]=phi(half_round(scores[i%8]),vit);
                            v[i]=sat_e4(half_round(values[i%8]));}
        auto d=den(w,vit);
        std::cout<<(vit?"ViT":"TIN")<<" "<<std::setw(4)<<d;
        if(argc==1){std::cout<<"\n";continue;}
        auto r=uint16_t(std::stoul(argv[family+1],nullptr,16));
        for(int i=0;i<64;++i)a[i]=sat_e4(vit?w[i]:h_mul(w[i],r));
        uint16_t sum=0;
        for(int i=0;i<64;i+=32)sum=qmma_sm120_r01::raw(a+i,v+i,sum);
        auto out=sat_e4(vit?h_mul(sum,r):sum);
        std::cout<<" "<<std::setw(4)<<r<<" "<<std::setw(4)<<sum<<" "
                 <<std::setw(2)<<unsigned(out)<<" weights";
        for(int i=0;i<8;++i)std::cout<<" "<<std::setw(2)<<unsigned(a[i]);
        std::cout<<"\n";
    }
}
'''
compiler = shutil.which("g++")
if not compiler:
    raise RuntimeError("g++ missing")
work = Path(tempfile.mkdtemp(prefix="anatomy-attention-av-r04f-"))
source, exe = work / "scalar.cpp", work / "scalar.exe"
source.write_text(header + "\n\n".join(parts) + main, encoding="utf-8")
flags = ["-std=c++20", "-O2", "-fno-fast-math", "-ffp-contract=off",
         "-frounding-math", "-static"]
subprocess.run([compiler, *flags, str(source), "-o", str(exe)],
               capture_output=True, text=True, check=True)
den_lines = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout.splitlines()
den_bits = [int(line.split()[1], 16) for line in den_lines]
assert all(0x0410 <= h < 0x7c00 for h in den_bits)
r_bits = [int(rcp[h-0x0410]) for h in den_bits]
output = subprocess.run([str(exe), *[f"{h:x}" for h in r_bits]],
                        capture_output=True, text=True, check=True).stdout
assert output.splitlines() == [
    "ViT 4d32 2a29 d448 c5 weights 02 02 06 0f 1b 26 32 3d",
    "TIN 5506 225f c7e0 d0 weights 00 00 00 00 00 00 01 20",
]
receipt = {
    "status": "PASS",
    "scope": "artificial 64-key one-channel scalar illustration, no GPU/model/chain",
    "scores_period": [-8,-4,-2,-1,0,1,2,8],
    "values_period": [1,-1,2,-2,4,-4,8,-8],
    "repeats": 8,
    "columns": "family denominator_F16 reciprocal_F16 AV_F16 output_E4 first_8_weight_E4",
    "stdout": output,
    "denominator_values": [struct.unpack("<e", struct.pack("<H", h))[0] for h in den_bits],
    "source_sha256": {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (helper, qmma, asset)},
    "generated_scalar_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "compiler": compiler, "flags": flags,
}
roots.out(Path(__file__).with_suffix(".result.json")).write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(output, end="")
