"""Run only the pinned R2 B00 scalar control functions on artificial CBs.

No model, image, weights, native target, SFU sweep or network chain is run.
Compiler sources/products/temporary files stay in this examples directory.
"""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
LANE = ROOT / "experiments/parity-cpp-param-change-r01-20261024-codex"
SNAP = LANE / "stage_d1_r2/returned/snapshot"
GUARD = "".join(map(chr, (98,108,105,110,100)))
PINS = {}

def read(path, expected=None):
    path = Path(path)
    if any(GUARD in part.lower() for part in path.parts):
        raise ValueError("guarded path refused")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if expected is not None and actual != expected:
        raise ValueError("source identity mismatch: " + str(path))
    PINS[path.as_posix()] = actual
    return data

seal = json.loads(read(SNAP / "CONTENT_SEAL_D1.json",
    "905bf2b65362cbf04d38862429be8bfc1846b1270a245dfd5447007dd73c3b6e"))

def source(relative):
    tail = "/candidate/repo/cpp/opt/M/" + relative
    pin = next(row for row in seal["pins"] if row["path"].endswith(tail))
    return read(SNAP / ("candidate/repo/cpp/opt/M/" + relative),
                pin["sha256"]).decode("utf-8")

b00 = source("entry/b00.hpp")
base = source("entry/mapexec_base.hpp")
bits = source("shared/portable_bits.hpp")

def function(text, name):
    m = re.search(r"^(?:B00Control|void|uint16_t) " + name + r"\([^\n]*\)\s*\{",
                  text, re.M)
    if not m:
        raise ValueError("function not found: " + name)
    start = text.index("{", m.start())
    depth, end = 1, start + 1
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[m.start():end]

decl = re.search(r"struct B00Control\s*\{.*?\};", b00, re.S)[0]
headers = "\n".join("#include <" + h + ">" for h in
    ("algorithm","array","cfenv","cmath","cstdint","cstring","iomanip",
     "iostream","limits","map","stdexcept","string","utility","vector"))
descriptors = """
namespace geo2 {
struct Geometry { std::map<int,std::array<uint64_t,4>> textures; };
const Geometry& g() {
 static const Geometry value{{{6,{0,0,0,0x6000}}, {3,{0,0,0,0x3000}}}};
 return value;
}
}
"""
main = r"""
uint64_t pairf(float low,float high){
 return uint64_t(optm_bit_cast<uint32_t>(low)) |
        (uint64_t(optm_bit_cast<uint32_t>(high))<<32);
}
uint64_t pairu(uint32_t low,uint32_t high){return uint64_t(low)|(uint64_t(high)<<32);}
void emit(const char* name,const std::vector<uint64_t>& q){
 b00_binding_control(q);auto c=b00_control(q);
 std::cout<<name<<" "<<c.p5<<" "<<c.reset<<" "<<c.temporal;
 for(auto h:c.constants)std::cout<<" "<<std::hex<<std::setw(4)<<std::setfill('0')<<h;
 std::cout<<std::dec<<"\n";
}
void refused(const char* name,std::vector<uint64_t> q){
 try{b00_binding_control(q);}catch(const std::exception&){std::cout<<"REFUSED "<<name<<"\n";return;}
 throw std::runtime_error("negative unexpectedly admitted");
}
int main(){
 if(std::fegetround()!=FE_TONEAREST)throw std::runtime_error("RN required");
 static_assert(std::numeric_limits<float>::is_iec559);
 static_assert(std::numeric_limits<double>::is_iec559);
 std::vector<uint64_t> reset(33);
 reset[21]=pairf(0,.25f);reset[22]=pairf(2,.5f);reset[23]=pairf(2,2);
 reset[24]=pairf(0,.5f)|1;reset[26]=pairu(1080,1920);
 reset[30]=pairu(1152,1920);reset[32]=pairu(576,960);
 emit("reset",reset);
 auto history=reset;history[1]=0x6000;history[2]=0x3000;
 history[6]=history[9]=pairf(1920,1080);
 history[7]=history[10]=pairf(1.f/1920,1.f/1080);
 history[20]=pairf(1,1);history[23]=pairf(1,2);history[25]=1;
 emit("history",history);
 auto bad=history;bad[3]=1;refused("extra_aux_handle",bad);
 bad=history;bad[25]=16;refused("counter16",bad);
 bad=history;bad[1]=0x6001;refused("wrong_history_binding",bad);
}
"""
generated = (headers + "\n" + bits.replace("#pragma once", "") + "\n" +
             function(base,"half_round") + "\n" + descriptors + decl + "\n" +
             function(b00,"b00_control") + "\n" +
             function(b00,"b00_binding_control") + "\n" + main)
compiler = shutil.which("g++")
if not compiler:
    raise RuntimeError("g++ required")
flags = ["-std=c++17","-O2","-fno-fast-math","-ffp-contract=off",
         "-frounding-math","-static"]
with tempfile.TemporaryDirectory(prefix="param-r04h-", dir=HERE) as folder:
    work = Path(folder).resolve()
    if not work.is_relative_to(HERE.resolve()):
        raise ValueError("temporary directory outside examples")
    cpp, exe = work / "control.cpp", work / "control.exe"
    cpp.write_text(generated, encoding="utf-8")
    env = dict(os.environ, TEMP=str(work), TMP=str(work), TMPDIR=str(work))
    build = subprocess.run([compiler,*flags,str(cpp),"-o",str(exe)],
                           env=env, capture_output=True, text=True)
    if build.returncode:
        raise RuntimeError(build.stderr)
    run = subprocess.run([str(exe)], env=env, check=True,
                         capture_output=True, text=True)
rows, refusals = [], []
for line in run.stdout.splitlines():
    cells = line.split()
    if cells[0] == "REFUSED":
        refusals.append(cells[1])
    else:
        rows.append(dict(case=cells[0], p5=int(cells[1]), reset=int(cells[2]),
                         temporal=int(cells[3]), feature_10_15_half=cells[4:]))
assert rows == [
    dict(case="reset",p5=1,reset=1,temporal=0,
         feature_10_15_half=["3800","3400","3c00","4000","4000","0000"]),
    dict(case="history",p5=1,reset=0,temporal=1,
         feature_10_15_half=["3800","3400","3c00","3c00","4000","0000"])]
assert refusals == ["extra_aux_handle","counter16","wrong_history_binding"]
receipt = dict(status="PASS", candidate="R2",
    candidate_content_seal="905bf2b65362cbf04d38862429be8bfc1846b1270a245dfd5447007dd73c3b6e",
    scope="artificial CB scalar controls only; not a model/geometry/native gate",
    raw_structure=2, reset_masks=[2,2], history_masks=[1,2],
    style=.5, tone=.25, rows=rows, guard_refusals=refusals,
    source_sha256=PINS, generated_scalar_sha256=hashlib.sha256(generated.encode()).hexdigest(),
    compiler=compiler, flags=flags,
    descriptors="artificial id6/id3 binding handles; real R2 binding predicate")
(HERE / "param_change_r04h.result.json").write_text(
    json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":"PASS","rows":rows,"guard_refusals":refusals}))
