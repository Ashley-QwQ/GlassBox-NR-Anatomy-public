"""Compile real scalar conversion helpers and run artificial boundary inputs.

Run from the repository root:
python -B -X utf8 skewer/examples/fp32_ftz_r04e.py [--source-root PATH] [--out FILE]
(see _roots.py for where the GlassBox-NR sources come from)

No model, network input, target, GPU or network chain is opened or executed.
Compilation stays in a fresh temporary directory. Floating-point flags are
checked, not changed; no host FTZ/DAZ control is used.
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
    "tail": CPP / "chain_outtail_optm/outtail.cpp",
    "half": CPP / "chain_outtail_optm/primitives.hpp",
    "b70_temporal": CPP / "chain_outtail_optm/b70_temporal.hpp",
    "b0_temporal": CPP / "chain_entry_optm/native_temporal.hpp",
    "noise": CPP / "chain_entry_optm/noise_online_optd.hpp",
    "b0": CPP / "chain_entry_optm/b00.hpp",
    "tin": CPP / "chain_tin_optm/tin.cpp",
    "tin_unary": CPP / "chain_tin_optm/unary_tables_optb2.inc",
    "split16": CPP / "chain_split16_optm/scalar_map.hpp",
    "entry_map": CPP / "chain_entry_optm/mapexec_base.hpp",
    "attention": CPP / "fam_attention_chain_r02/attention_impl.hpp",
    "qkv": CPP / "fam_qkv_projection_chain_r02/qkv_projection_impl.hpp",
    "lg2": CPP / "chain_outtail_optm/lg2_decoder.hpp",
    "plan_rules": CPP.parent / "devkit/plan_format.py",
}
guard = "".join(map(chr, (98, 108, 105, 110, 100)))
for path in SOURCES.values():
    if any(guard in part.lower() for part in path.parts):
        raise RuntimeError("excluded source path")
texts = {key: path.read_text(encoding="utf-8") for key, path in SOURCES.items()}


def function(text, name):
    match = re.search(r"^(?:double|float|bool|void|uint16_t) " + name + r"\([^\n]*?\)\s*\{",
                      text, re.M)
    if not match:
        raise ValueError(name)
    start = text.index("{", match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[match.start():end]


names = {
    "half": ["half_value", "half_round"],
    "tail": ["fb", "ftz", "rz", "require", "ftz_tiny_before_fma", "fm", "ff"],
}
parts = [function(texts[key], name) for key, values in names.items() for name in values]
header = "\n".join("#include <" + name + ">" for name in
                   ["algorithm", "bit", "cfenv", "cmath", "cstdint", "iomanip",
                    "iostream", "limits", "stdexcept"])
header += "\nnamespace optm { using std::bit_cast; }\n"
main = r'''
int main() {
    static_assert(sizeof(float)==4 && sizeof(double)==8);
    static_assert(std::numeric_limits<float>::is_iec559 &&
                  std::numeric_limits<double>::is_iec559);
    if(std::fegetround()!=FE_TONEAREST)throw std::runtime_error("RN environment required");
    for(uint32_t raw:{0x33800000u,0x33c00000u,0xb3c00000u}) {
        const float x=fb(raw);
        const uint16_t rn=half_round(double(x)),toward=rz(x);
        std::cout<<"boundary "<<std::hex<<std::setfill('0')<<std::setw(8)<<raw
                 <<" "<<std::setw(4)<<rn<<" "<<std::setw(4)<<toward
                 <<" "<<std::setw(2)<<unsigned(toward&255)
                 <<" "<<std::setw(2)<<unsigned(toward>>8)<<std::dec<<"\n";
    }
    for(uint32_t raw:{0x00000001u,0x80000001u})
        std::cout<<"ftz_bits "<<std::hex<<std::setw(8)<<std::setfill('0')<<raw
                 <<" "<<std::setw(8)<<std::bit_cast<uint32_t>(ftz(fb(raw)))<<std::dec<<"\n";
    const float a=fb(0x00800000u),b=fb(0x3f7fffffu);
    if(!ftz_tiny_before_fma(a,b,0.f) || ftz_tiny_before_fma(a,1.f,0.f))
        throw std::runtime_error("tiny predicate boundary");
    try {fm(a,b);throw std::runtime_error("missing multiply refusal");}
    catch(const std::invalid_argument& e){std::cout<<"fm_refused "<<e.what()<<"\n";}
    try {ff(a,b,0.f);throw std::runtime_error("missing fused refusal");}
    catch(const std::invalid_argument& e){std::cout<<"ff_refused "<<e.what()<<"\n";}
    std::cout<<"FP_ENV_RN_IEEE_NO_CONTROL_CHANGES\n";
}
'''
compiler = shutil.which("g++")
if not compiler:
    raise RuntimeError("g++ missing")
work = Path(tempfile.mkdtemp(prefix="anatomy-fp32-r04e-"))
source, exe = work / "scalar.cpp", work / "scalar.exe"
source.write_text(header + "\n\n".join(parts) + main, encoding="utf-8")
flags = ["-std=c++20", "-O2", "-fno-fast-math", "-ffp-contract=off",
         "-frounding-math", "-static"]
build = subprocess.run([compiler, *flags, str(source), "-o", str(exe)],
                       capture_output=True, text=True, check=True)
run = subprocess.run([str(exe)], capture_output=True, text=True, check=True)
lines = run.stdout.splitlines()
expected = [
    "boundary 33800000 0001 0001 01 00",
    "boundary 33c00000 0002 0001 01 00",
    "boundary b3c00000 8002 8001 01 80",
    "ftz_bits 00000001 00000000",
    "ftz_bits 80000001 80000000",
    "fm_refused fp32 underflow boundary",
    "ff_refused fp32 FMA underflow boundary",
    "FP_ENV_RN_IEEE_NO_CONTROL_CHANGES",
]
if lines != expected:
    raise RuntimeError("unexpected scalar output: " + repr(lines))
result = {
    "status": "PASS",
    "scope": "artificial scalar CPU boundaries only; zero GPU/model/chain runs",
    "compiler": compiler,
    "compiler_version": subprocess.run([compiler, "--version"], capture_output=True,
                                     text=True, check=True).stdout.splitlines()[0],
    "flags": flags,
    "floating_environment": "IEEE binary32/binary64 and FE_TONEAREST checked; no mode or FTZ/DAZ changes",
    "extracted_functions": names,
    "source_sha256": {path.as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in SOURCES.values()},
    "generated_cpp_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "temporary_build": str(work),
    "compile_stderr": build.stderr,
    "stdout": lines,
}
out = roots.out(Path(__file__).with_suffix(".result.json"))
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": result["status"], "stdout": lines, "result": str(out)},
                 ensure_ascii=False))
