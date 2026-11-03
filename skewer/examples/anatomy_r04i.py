"""Real scalar functions and shape-derived matrix costs; no model/GPU runs."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CPP=ROOT.parent/"GlassBox-NR/cpp"
GUARD="".join(map(chr,(98,108,105,110,100)))
pins={}
def read(path,expected=None):
    path=Path(path)
    if any(GUARD in p.lower() for p in path.parts):raise ValueError("guarded path refused")
    raw=path.read_bytes();h=hashlib.sha256(raw).hexdigest()
    if expected is not None and h!=expected:raise ValueError("identity mismatch: "+str(path))
    pins[path.as_posix()]=h
    return raw
tail=read(CPP/"chain_outtail_optm/outtail.cpp").decode()
half=read(CPP/"chain_outtail_optm/primitives.hpp").decode()
temporal=read(CPP/"chain_outtail_optm/b70_temporal.hpp").decode()
repack=read(CPP/"fam_repack/repack.cpp").decode()
tin=read(CPP/"chain_tin_optm/tin.cpp").decode()
read(CPP/"chain_entry_optm/b00.hpp")
read(CPP/"chain_entry_optm/entry.cpp")
identity=json.loads(read(ROOT/"WEIGHTS_IDENTITY.json"))["canonical_weights"]
assert identity["size_bytes"]==147695410
def fn(text,name):
    m=re.search(r"^(?:inline )?(?:float|bool|void|double|uint16_t|uint32_t) "+name+r"\([^\n]*?\)\s*\{",text,re.M)
    if not m:raise ValueError(name)
    start=text.index("{",m.start());end=start+1;depth=1
    while depth:depth+=(text[end]=="{")-(text[end]=="}");end+=1
    return text[m.start():end]
manifest_path=ROOT.parent/"dlssnr-cpp-work/chain-outtail-r01-codex/tables/manifest.json"
manifest=json.loads(read(manifest_path))
assets=[]
for name,h in (
    ("ex2","cce5df10202dbfcde720ca547d147edb3e2a406a5fed189323f419177a72a1a5"),
    ("rcp","c408381446132e07fa5581e930dc33fb790bea7ec4276ef3621e322df2492a55")):
    path=manifest_path.parent/(name+".bin")
    assert manifest["sources"][name]["extracted_sha256"]==h
    read(path,h);assets.append(path)
headers="\n".join("#include <"+x+">" for x in
    ("algorithm","array","bit","cfenv","cmath","cstdint","cstring","fstream",
     "iomanip","iostream","limits","stdexcept","string","utility","vector"))
setup=r"""
namespace optm {using std::bit_cast;}
template<class T> T load(const uint8_t* p,size_t at){T x;std::memcpy(&x,p+at,sizeof(x));return x;}
std::vector<uint32_t> ex2tab,rcptab;
std::vector<std::pair<uint32_t,uint32_t>> ex2_sparse;
std::array<bool,512> exneg{},expos{};
int configured_launch=155;bool temporal_tables=true;
namespace mufu_full_r01 {
std::array<bool,512> ex_codec_admitted{};
bool has(unsigned,unsigned){return false;}
bool lookup(unsigned,uint32_t,uint32_t&){throw std::runtime_error("unexpected raw fallback");}
}
"""
parts=[fn(half,n) for n in ("half_value","half_round")]
parts += [fn(tail,n) for n in
    ("require","fb","ftz","ftz_tiny_before_fma","fm","ff","fa","sat","rz","rcp","ex")]
parts += [re.search(r"constexpr uint32_t kBitDest\[12\].*?;",repack)[0],fn(repack,"swizzle")]
color=re.search(r"float tex=float\(half_value\(load<uint16_t>\(color.p,at\+c\*2\)\)\).*?blended\[c\]=encoded\[c\];",tail,re.S)[0]
gate=re.search(r"float argument=.*?float factor=sat\(ff\(sigmoid,confidence,0.f\)\);",temporal,re.S)[0]
blend=re.search(r"float delta=ff\(inv,weighted,-encoded\[c\]\);out\[c\]=ff\(factor,delta,encoded\[c\]\);",temporal)[0]
main=r"""
template<class T>void table(std::vector<T>&v,const char* p){
 std::ifstream f(p,std::ios::binary|std::ios::ate);if(!f)throw std::runtime_error("table");
 auto n=f.tellg();v.resize(size_t(n)/sizeof(T));f.seekg(0);f.read((char*)v.data(),n);
}
int main(int argc,char** argv){
 if(argc!=3||std::fegetround()!=FE_TONEAREST)throw std::runtime_error("args/RN");
 table(ex2tab,argv[1]);table(rcptab,argv[2]);
 NEGATIVE_BLOCKS
 POSITIVE_BLOCKS
 uint8_t p[184]{},pixels[8]{};
 float scale=.03125f;std::memcpy(p+0x30,&scale,4);
 uint16_t h=half_round(.5);for(int c=0;c<3;c++)std::memcpy(pixels+2*c,&h,2);
 struct Texture{uint8_t* p;} color{pixels};
 size_t at=0;uint16_t dh[4]={half_round(.01),0,half_round(-.01),half_round(1)};
 const uint16_t* head=dh;float encoded[3],blended[3],out[3]{};
 std::cout<<std::setprecision(10);
 for(int c=0;c<3;c++){COLOR_FRAGMENT
  std::cout<<"color "<<c<<" "<<half_value(dh[c])<<" "<<base<<" "<<val<<" "<<encoded[c]<<"\n";}
 float confidence=float(half_value(half_round(.5))),inv=rcp(1);
 GATE_FRAGMENT
 std::cout<<"gate "<<argument<<" "<<ex(argument)<<" "<<sigmoid<<" "<<factor<<" "<<inv<<"\n";
 float weighted_history[3]={.75f,.25f,.5f};
 for(int c=0;c<3;c++){float weighted=weighted_history[c];BLEND_FRAGMENT
  std::cout<<"blend "<<c<<" "<<delta<<" "<<out[c]<<" "<<std::hex<<rz(out[c])<<std::dec<<"\n";}
 std::cout<<"pi "<<std::hex<<0x725<<" "<<swizzle(0x725)<<std::dec<<"\n";
 for(unsigned b=0;b<12;b++)if((0x725>>b)&1)std::cout<<"bit "<<b<<" "<<kBitDest[b]<<"\n";
 std::cout<<"sqrt32 "<<half_value(half_round(std::sqrt(32.)))<<" "<<std::hex<<half_round(std::sqrt(32.))<<"\n";
}
"""
for a,b in [("COLOR_FRAGMENT",color),("GATE_FRAGMENT",gate),("BLEND_FRAGMENT",blend),
    ("NEGATIVE_BLOCKS","\n".join(f"exneg[{n}]=true;" for n in manifest["runtime"]["ex2_negative_blocks"])),
    ("POSITIVE_BLOCKS","\n".join(f"expos[{n}]=true;" for n in manifest["runtime"]["ex2_positive_blocks"]))]:
    main=main.replace(a,b)
source=headers+setup+"\n".join(parts)+main
compiler=shutil.which("g++");assert compiler
flags=["-std=c++20","-O2","-fno-fast-math","-ffp-contract=off","-frounding-math","-static"]
with tempfile.TemporaryDirectory(prefix="anatomy-r04i-",dir=HERE) as folder:
    work=Path(folder).resolve();assert work.is_relative_to(HERE.resolve())
    cpp=work/"scalar.cpp";exe=work/"scalar.exe";cpp.write_text(source,encoding="utf-8")
    env=dict(os.environ,TEMP=str(work),TMP=str(work),TMPDIR=str(work))
    r=subprocess.run([compiler,*flags,str(cpp),"-o",str(exe)],env=env,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr)
    r=subprocess.run([str(exe),*map(str,assets)],env=env,capture_output=True,text=True,check=True)
assert "pi 725 276" in r.stdout and "sqrt32 5.65625 45a8" in r.stdout

# Logical coefficient slots and MACs from the documented matrix dimensions.
# This is not an executed-lane census. split16 totals remain open where MKN
# (notably final_head and the pooled projection) has not been established.
assert "w.ex=mat(C,4*C+128,true);w.out=mat(C,C)" in tin
def tin_main(c):return 12*c*c if c==32 else 9*c*c+128*c
def tin_stage(decode):
    weight=linear=attention=0
    for c,n in [(32,4),(64,4),(128,6),(256,8)]:
        positions=(1920*1152)//(4*(c//32)**2)
        extra=2*c*c
        weight+=n*tin_main(c)+extra
        linear+=n*positions*tin_main(c)+(positions//4)*extra
        attention+=n*2*positions*64*c
    return dict(matrix_bytes=weight,linear_MAC=linear,attention_MAC=attention,complete=True)
positions=1920*1152
stages={
 "B0":dict(matrix_bytes=32*16*2+12*32*32,
           linear_MAC=positions*(32*16+12*32*32),
           attention_MAC=2*positions*64*32,complete=True),
 "TIN_encoder":tin_stage(False),
 "split16_encoder":dict(matrix_bytes=8*(3*512*512+512*512),
           linear_MAC=2160*8*(3*512*512+512*512),
           attention_MAC=8*2*2160*64*512,complete=False,
           omitted="QKV projection, pooled extra projection and L57 internal MKN"),
 "ViT":dict(matrix_bytes=8*12*1024*1024,
           linear_MAC=640*8*12*1024*1024,attention_MAC=8*2*640*640*1024,complete=True),
 "L100":dict(matrix_bytes=1024*512,linear_MAC=2160*1024*512,
           attention_MAC=0,complete=True),
 "split16_decoder":dict(matrix_bytes=8*(3*512*512+512*512),
           linear_MAC=2160*8*(3*512*512+512*512),
           attention_MAC=8*2*2160*64*512,complete=False,omitted="QKV projection"),
 "TIN_decoder":tin_stage(True),
 "B70":dict(matrix_bytes=12*32*32+32*4*2,
           linear_MAC_reset=positions*(12*32*32+32*3),
           linear_MAC_history=positions*(12*32*32+32*4),
           attention_MAC=2*positions*64*32,complete=True)
}
receipt=dict(status="PASS",scope="artificial B70 arithmetic and repack; logical shape costs, no network/GPU",
    source_sha256=pins,generated_scalar_sha256=hashlib.sha256(source.encode()).hexdigest(),
    flags=flags,compiler=compiler,stdout_tokens=[s.split() for s in r.stdout.splitlines()],
    B70_inputs=dict(color=[.5,.5,.5],dh_before_half=[.01,0,-.01,1],
                    host_scale=.03125,artificial_confidence=.5,
                    supplied_weighted_history=[.75,.25,.5],denominator=1),
    canonical_resource=dict(bytes=identity["size_bytes"],sha256=identity["sha256"]),
    cost_scope="1080/internal1920x1152; logical valid positions; matrix slots only, excluding biases/scales/alignment, no executed-lane or FLOP claim",
    stages=stages,complete_network_total="NOT_ESTABLISHED: split16 entries are explicit known subtotals")
(HERE/"anatomy_r04i.result.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(r.stdout)
print(json.dumps(stages,indent=2))
