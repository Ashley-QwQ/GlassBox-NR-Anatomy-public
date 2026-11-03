"""Run extracted scalar C++ functions on artificial FFN inputs only.

Run from the repository root: python -B -X utf8 skewer/examples/ffn_r04b.py [--source-root PATH] [--out FILE]
(see _roots.py for where the GlassBox-NR sources come from)
Requires g++ in PATH. No model, GPU, saved network input, or target is read.
Generated C++ and the executable stay in a new temporary directory.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _roots as roots

CPP = roots.source_root() / "cpp"
SOURCES = {
    "b0": CPP / "chain_entry_optm/b00.hpp",
    "tin": CPP / "chain_tin_optm/tin.cpp",
    "vit": CPP / "fam_ffn_expand_resume2_chain_r02/ffn_expand-resume2.cpp",
    "qmma": CPP / "chain_tin_optm/qmma_sm120.hpp",
    "b0_helpers": CPP / "chain_entry_optm/mapexec_base.hpp",
    "tin_helpers": CPP / "chain_tin_optm/primitives.inc",
}


def function(text, name):
    match = re.search(r"^(?:double|int|uint8_t|uint16_t) " + name + r"\([^\n]*?\)\s*\{", text, re.M)
    if not match:
        raise ValueError(name)
    start = text.index("{", match.start())
    depth = 1
    end = start + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[match.start():end]


texts = {k: p.read_text(encoding="utf-8") for k, p in SOURCES.items()}
helpers = ["half_value", "half_round", "e4_units", "e4_half", "sat_e4",
           "h_add", "h_mul", "h_fma", "h_min", "h_max"]


def normalized_body(code):
    # The two names implement a raw bit copy; do not alter any arithmetic.
    body = code[code.index("{"):].replace("optm_bit_cast", "std::bit_cast")
    return re.sub(r"\s+", "", re.sub(r"//[^\n]*", "", body))


for source_name in ["b0_helpers", "tin_helpers"]:
    for name in helpers:
        source_function = "sat_e4_reference" if name == "sat_e4" else name
        assert normalized_body(function(texts[source_name], source_function)) == normalized_body(function(texts["vit"], name)), (source_name, name)

parts = [function(texts["vit"], n) for n in helpers]
for family, original, renamed in [("b0", "gate", "gate_b0"),
                                   ("tin", "gate_reference", "gate_tin"),
                                   ("vit", "gate", "gate_vit")]:
    parts.append(function(texts[family], original).replace(original + "(", renamed + "(", 1))
header = "\n".join("#include <" + n + ">" for n in
                   ["algorithm", "bit", "cmath", "cstdint", "iomanip", "iostream", "limits", "stdexcept"])
header += '\n#include "' + SOURCES["qmma"].as_posix() + '"\n'
main = r'''
int main() {
    size_t count=0;
    for(unsigned i=0;i<65536;++i) {
        if((i&0x7c00)==0x7c00)continue;
        auto a=gate_b0(uint16_t(i)),b=gate_tin(uint16_t(i)),c=gate_vit(uint16_t(i));
        if(a!=b||a!=c)throw std::runtime_error("finite scalar gate mismatch");
        ++count;
    }
    std::cout<<"finite_gate_equal "<<count<<"\n";
    const uint16_t inputs[]={0xc500,0xc400,0xbc00,0x8000,0x0000,0x3800,0x3c00,0x4000,0x4400,0x4500};
    const uint16_t seed=h_mul(e4_half(0x28),0x4000); // artificial 0.25 * 2
    for(auto x:inputs) {
        auto g=gate_b0(x);
        uint8_t a[32]{},b[32]{};a[0]=g;b[0]=0x38; // one artificial unit matrix coefficient
        auto y=qmma_sm120_r01::raw(a,b,seed);
        std::cout<<std::hex<<std::setfill('0')<<std::setw(4)<<x<<" "
                 <<std::setw(2)<<unsigned(g)<<" "<<std::setw(4)<<seed<<" "
                 <<std::setw(4)<<y<<" "<<std::setw(2)<<unsigned(sat_e4(y))<<std::dec<<"\n";
    }
    // A tiny analogue of the fixed four-part ViT residual reduction.
    uint16_t terms[]={half_round(2048),half_round(1),half_round(-2048),half_round(1)};
    auto ordered=h_add(h_add(h_add(terms[0],terms[1]),terms[2]),terms[3]);
    auto changed=h_add(h_add(h_add(terms[0],terms[2]),terms[1]),terms[3]);
    std::cout<<"ordered_half "<<std::hex<<ordered<<" reordered_half "<<changed<<std::dec<<"\n";
    for(auto x:{0x7c00,0xfc00,0x7e00}) {
        try { gate_vit(uint16_t(x));throw std::logic_error("missing nonfinite refusal"); }
        catch(const std::domain_error&) { std::cout<<"vit_nonfinite_refused "<<std::hex<<x<<std::dec<<"\n"; }
    }
}
'''
work = Path(tempfile.mkdtemp(prefix="anatomy-ffn-r04b-"))
source = work / "scalar.cpp"
source.write_text(header + "\n\n".join(parts) + main, encoding="utf-8")
compiler = shutil.which("g++")
if not compiler:
    raise RuntimeError("g++ missing")
exe = work / "scalar.exe"
flags = ["-std=c++20", "-O2", "-fno-fast-math", "-ffp-contract=off", "-static"]
command = [compiler, *flags, str(source), "-o", str(exe)]
build = subprocess.run(command, capture_output=True, text=True, check=True)
run = subprocess.run([str(exe)], capture_output=True, text=True, check=True)
lines = run.stdout.splitlines()
assert lines[0] == "finite_gate_equal 63488"
assert "ordered_half 3c00 reordered_half 4000" in lines
result = {
    "scope": "artificial scalar CPU example; zero GPU/model/chain runs",
    "compiler": compiler,
    "compiler_version": subprocess.run([compiler, "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0],
    "flags": flags,
    "source_sha256": {str(v): hashlib.sha256(v.read_bytes()).hexdigest() for v in SOURCES.values()},
    "extracted_functions": helpers + ["b0 gate", "tin gate_reference", "vit gate"],
    "helper_source_check": "all helper bodies equal after bit-copy wrapper name normalization; cached E4 publication compared through its unchanged reference",
    "temporary_build": str(work),
    "generated_cpp_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "stdout": lines,
    "status": "PASS",
}
destination = roots.out(Path(__file__).with_suffix(".result.json"))
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(run.stdout, end="")
print("result:", destination)
