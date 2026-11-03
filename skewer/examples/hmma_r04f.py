"""Run extracted scalar HMMA helpers on artificial half operands only.

python -B -X utf8 skewer/examples/hmma_r04f.py [--source-root PATH] [--out FILE]
(run from the repository root; see _roots.py for where the GlassBox-NR sources come from)
No model, weights, saved network tensors or GPU are read or executed.
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
    "half": CPP / "chain_outtail_optm/primitives.hpp",
    "entry": CPP / "chain_entry_optm/mapexec_base.hpp",
    "cached": CPP / "chain_entry_optm/decode_reuse.inc",
    "tail": CPP / "chain_outtail_optm/outtail.cpp",
}
guard = "".join(map(chr, (98, 108, 105, 110, 100)))
for path in SOURCES.values():
    if any(guard in part.lower() for part in path.parts):
        raise RuntimeError("excluded source path")
texts = {key: path.read_text(encoding="utf-8") for key, path in SOURCES.items()}


def function(text, name):
    match = re.search(r"^(?:double|void|uint16_t|uint64_t) " + name +
                      r"\([^\n]*?\)\s*\{", text, re.M)
    if not match:
        raise ValueError(name)
    start = text.index("{", match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    body = text[match.start():end]
    # Source correspondence comments are not part of the scalar arithmetic.
    return re.sub(r"^// Correspondence:.*\n", "", body, flags=re.M)


names = {
    "half": ["half_value", "half_round", "magnitude"],
    "tail": ["require", "hmma_seed"],
    "entry": ["hmma_dot"],
    "cached": ["hmma_cached"],
}
parts = [function(texts[key], name) for key, values in names.items() for name in values]
header = "\n".join("#include <" + name + ">" for name in
                   ["algorithm", "bit", "cfenv", "cmath", "cstdint", "iomanip",
                    "iostream", "limits", "stdexcept"])
header += "\nnamespace optm { using std::bit_cast; }\n"
main = r'''
int main() {
    static_assert(sizeof(double)==8 && std::numeric_limits<double>::is_iec559);
    if(std::fegetround()!=FE_TONEAREST)throw std::runtime_error("RN required");
    uint16_t a[16]={0x3c01,0xbc00}, b[16]={0x3c01,0x3c02};
    double av[16],bv[16]; double rounded_sum=0;
    for(int k=0;k<16;++k){
        av[k]=half_value(a[k]);bv[k]=half_value(b[k]);
        rounded_sum+=half_value(half_round(av[k]*bv[k]));
    }
    auto show=[](const char* name,uint16_t h){
        std::cout<<name<<" "<<std::hex<<std::setfill('0')<<std::setw(4)<<h<<std::dec<<"\n";
    };
    show("dot",hmma_dot(a,b));
    show("cached",hmma_cached(a,b,av,bv));
    show("seeded",hmma_seed(a,b,0));
    show("product_half_control",half_round(rounded_sum));
    uint16_t x[16]={half_round(1024),half_round(.5)};
    uint16_t y[16]={half_round(1),half_round(1)};
    const auto first=hmma_seed(x,y,0);
    x[0]=half_round(-1024);
    show("first_K16",first);
    show("two_K16",hmma_seed(x,y,first));
    show("single_final_round_control",half_round(1024+.5-1024+.5));
    a[0]=0x7c00;
    try { hmma_seed(a,b,0);throw std::runtime_error("missing refusal"); }
    catch(const std::invalid_argument&){std::cout<<"nonfinite_operand_refused\n";}
    std::cout<<"FP_ENV_RN_IEEE_NO_CONTROL_CHANGES\n";
}
'''
compiler = shutil.which("g++")
if not compiler:
    raise RuntimeError("g++ missing")
work = Path(tempfile.mkdtemp(prefix="anatomy-hmma-r04f-"))
source, exe = work / "scalar.cpp", work / "scalar.exe"
source.write_text(header + "\n\n".join(parts) + main, encoding="utf-8")
flags = ["-std=c++20", "-O2", "-fno-fast-math", "-ffp-contract=off",
         "-frounding-math", "-static"]
subprocess.run([compiler, *flags, str(source), "-o", str(exe)],
               capture_output=True, text=True, check=True)
run = subprocess.run([str(exe)], capture_output=True, text=True, check=True)
expected = [
    "dot 0010", "cached 0010", "seeded 0010", "product_half_control 0000",
    "first_K16 6400", "two_K16 3800", "single_final_round_control 3c00",
    "nonfinite_operand_refused", "FP_ENV_RN_IEEE_NO_CONTROL_CHANGES",
]
if run.stdout.splitlines() != expected:
    raise RuntimeError("unexpected output: " + repr(run.stdout))
result = {
    "status": "PASS",
    "scope": "artificial scalar CPU arithmetic only; zero GPU/model/chain runs",
    "compiler": compiler,
    "compiler_version": subprocess.run([compiler, "--version"], capture_output=True,
                                     text=True, check=True).stdout.splitlines()[0],
    "flags": flags,
    "extracted_functions": names,
    "source_sha256": {path.as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in SOURCES.values()},
    "generated_scalar_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "stdout": run.stdout,
    "expected": expected,
}
target = roots.out(Path(__file__).with_suffix(".result.json"))
target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(run.stdout, end="")
print("PASS", target)
