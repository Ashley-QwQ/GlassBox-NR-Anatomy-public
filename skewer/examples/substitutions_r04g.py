"""Real scalar/layout source substitutions on artificial data, no model runs.

Build products and compiler temporary files stay below this examples directory.
The certified function assets are opened read-only; no mathematical fallback.
"""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,tempfile
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CPP=ROOT.parent/"GlassBox-NR/cpp"
guard="".join(map(chr,(98,108,105,110,100)))
pins={}
def read(p,expected=None):
    p=Path(p)
    assert not any(guard in x.lower() for x in p.parts)
    raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest()
    if expected is not None:assert h==expected,"identity mismatch: "+str(p)
    pins[p.as_posix()]=h
    return raw
sources={
    "tail":CPP/"chain_outtail_optm/outtail.cpp",
    "half":CPP/"chain_outtail_optm/primitives.hpp",
    "temporal":CPP/"chain_entry_optm/native_temporal.hpp",
    "b0":CPP/"chain_entry_optm/b00.hpp",
    "entry":CPP/"chain_entry_optm/entry.cpp",
    "attention":CPP/"fam_attention_chain_r02/attention_impl.hpp",
}
texts={k:read(p).decode("utf-8") for k,p in sources.items()}
def function(text,name):
    m=re.search(r"^(?:inline )?(?:double|float|bool|void|uint16_t|uint64_t) "+name+r"\([^\n]*?\)\s*\{",text,re.M)
    if not m:raise ValueError(name)
    start=text.index("{",m.start());depth=1;end=start+1
    while depth:
        depth+=(text[end]=="{")-(text[end]=="}");end+=1
    return text[m.start():end]

# Actual source operand coordinates plus pinned byte-source maps.
bind=json.loads(read(ROOT/"experiments/parity-cpp-step2b-vit-r02-20260928-codex/s00-bindings.json"))
binding=next(x for x in bind["rows"] if x["launch"]==62)["map"]
mr,wr=binding["epoch_maps"][0],binding["epoch_wiring"][0]
rawmap=Path(mr["path"]);read(rawmap,mr["sha256"])
wiring=json.loads(read(wr["path"],wr["sha256"]))
nodes=wiring["nodes"];wires=wiring["templates"]["0|0"]["wiring"]
with np.load(rawmap,allow_pickle=False) as z:
    def leaf_address(node_id,lane,byte):
        n=nodes[node_id]
        assert n[0]=="leaf" and n[1] in ("qload","kread","vread")
        key=f"{n[1]}|{n[2]}|{n[3]}"
        return int(z[key][0,0,lane])+4*n[4]+byte
    # row=9,k=4: actual A-coordinate expression in attention_impl.hpp.
    qnode=wires[0][3][1]
    qaddr=leaf_address(qnode,(9%8)*4+(4%16)//4,4%4)
    # Key row9 is col1 of its 8-column block; value channel4 is col4.
    kaddresses=[];vaddresses=[]
    for w in wires:
        n=nodes[w[4][0]]
        if n[0]=="leaf" and n[1]=="kread":
            kaddresses.append(leaf_address(w[4][0],1*4+(4%16)//4,4%4))
        if n[0]=="leaf" and n[1]=="vread":
            vaddresses.append(leaf_address(w[4][0],4*4+(9%16)//4,9%4))
    assert qaddr==84 and 88 in kaddresses and 289 in vaddresses
layout={"logical_t_h_d":[9,0,4],"Q_byte":qaddr,"K_byte":88,"V_byte":289,
        "scope":"actual source operand selection and pinned maps; artificial address example"}

manifest_path=Path("E:/dlssnr-cpp-work/chain-outtail-r01-codex/tables/manifest.json")
manifest=json.loads(read(manifest_path))
assets={}
expected_tables={"ex2":"cce5df10202dbfcde720ca547d147edb3e2a406a5fed189323f419177a72a1a5",
                 "rcp":"c408381446132e07fa5581e930dc33fb790bea7ec4276ef3621e322df2492a55"}
for key in ("ex2","rcp"):
    p=manifest_path.parent/(key+".bin")
    assert manifest["sources"][key]["extracted_sha256"]==expected_tables[key]
    read(p,expected_tables[key]);assets[key]=p
encoded=ROOT/"experiments/parity-cpp-opt-e1-r01-20261001-codex/encoded"
codec=json.loads(read(encoded/"manifest.json","4255d067e6a618342182a86f44fbf2feceb92a7d148e0dcdfaabe304f8c72138"))
for name in ("base_E127.bin","raw_E126.bin","level_3bit.bin"):
    read(encoded/name,codec["files"][name]["sha256"]);assets[name]=encoded/name
read(CPP/"chain_outtail_optm/lg2_decoder.hpp")
read(CPP/"chain_outtail_optm/reach_sites.hpp")

headers="\n".join("#include <"+n+">" for n in
 ("algorithm","array","bit","cfenv","cmath","cstdint","cstring","exception","fstream",
  "iomanip","iostream","limits","mutex","stdexcept","string","thread","vector"))
headers+='\n#include "'+(CPP/"chain_outtail_optm/lg2_decoder.hpp").as_posix()+'"\n'
headers+='\n#include "'+(CPP/"chain_outtail_optm/reach_sites.hpp").as_posix()+'"\n'
headers+="""
namespace optm {using std::bit_cast;}
template<class T> T optm_bit_cast(auto x){return std::bit_cast<T>(x);}
template<class T> T load(const uint8_t* p,size_t at){T v;std::memcpy(&v,p+at,sizeof(v));return v;}
struct Ws {std::vector<uint64_t> q;};
namespace geo2 {struct Geo{int cw=1,ch=1;};Geo& g(){static Geo v;return v;}
size_t product(size_t a,size_t b){return a*b;}}
struct Texture {uint8_t* p;int pitch;uint64_t surf,tex;};
struct Mem {size_t pool_bytes=0;};
int configured_launch=157;bool temporal_tables=false,ready=true;
std::vector<std::pair<uint32_t,uint32_t>> ex2_sparse;
std::vector<uint32_t> ex2tab,rcptab;opte1::Decoder lg2codec;
std::array<int,512> lg2idx;std::array<bool,512> exneg{},expos{};
namespace mufu_full_r01 {
std::array<bool,512> ex_codec_admitted{};
bool has(unsigned,unsigned){return false;}
bool lookup(unsigned,uint32_t,uint32_t&){throw std::runtime_error("unexpected raw fallback");}
}
"""
parts=[function(texts["half"],n) for n in ("half_value","half_round","h_add","h_mul")]
parts+=[function(texts["entry"],"le16")]
parts+=[function(texts["tail"],n) for n in
 ("require","fb","ftz","ftz_tiny_before_fma","fm","ff","fa","sat","rz","rcp","lg","ex","reach_lg","reach_ex")]
# Preserve the real scheduler and the entire real one-pixel color body.
parallel_start=texts["tail"].index("template<class Fn> void parallel")
parallel_end=texts["tail"].index("\nstruct Texture",parallel_start)
parts.append(texts["tail"][parallel_start:parallel_end])
parts+=[function(texts["temporal"],n) for n in
 ("tn_add","tn_mul","tn_div","tn_fma","tn_clip","tn_sample","native_history_pixel")]
history=function(texts["temporal"],"native_history_pixel")
history=history.replace("void native_history_pixel(","void history_traced(",1)
history=history.replace("for(int c=0;c<3;++c){float value=",
 '''std::cout<<"five_coords "<<x0<<" "<<y0<<" "<<t<<" "<<v<<" "<<xc<<" "<<yc<<"\\n";
 std::cout<<"five_weights_LTCBR "<<wl<<" "<<wt<<" "<<wc<<" "<<wb<<" "<<wr<<" "<<den<<"\\n";
 std::cout<<"five_samples_TLCBR "<<tn_sample(hist,w,h,xc,yt,0)<<" "<<tn_sample(hist,w,h,xl,yc,0)<<" "<<tn_sample(hist,w,h,xc,yc,0)<<" "<<tn_sample(hist,w,h,xc,yb,0)<<" "<<tn_sample(hist,w,h,xr,yc,0)<<"\\n";
 for(int c=0;c<3;++c){float value=''')
parts.append(history)
s157=function(texts["tail"],"s157")
parts.append(s157)
traced=s157.replace("void s157(","void s157_traced(",1)
traced=traced.replace("rgb[c]=reach_ex(3,fm(reach_lg(2,std::max(0.f,a)),eb));",
    'rgb[c]=reach_ex(3,fm(reach_lg(2,std::max(0.f,a)),eb));std::cout<<"curve "<<c<<" "<<rawv<<" "<<x<<" "<<pre<<" "<<rgb[c]<<"\\n";')
traced=traced.replace("decompose(rgb[0],rgb[1],rgb[2],false,H,S,L);",
    'decompose(rgb[0],rgb[1],rgb[2],false,H,S,L);std::cout<<"HSL_Fwd "<<H<<" "<<S<<" "<<L<<"\\n";')
traced=traced.replace("decompose(h,q1,p1,true,H,S,L);",
    'std::cout<<"temporary "<<h<<" "<<q1<<" "<<p1<<"\\n";decompose(h,q1,p1,true,H,S,L);std::cout<<"HSL_Rev "<<H<<" "<<S<<" "<<L<<"\\n";')
assert traced!=s157
parts.append(traced)

# B0 layout expressions taken verbatim from the actual output loops.
full=re.search(r"int lane=\(lx%4\).*?size_t tile=.*?;",texts["b0"])[0]
pool_c=re.search(r"int c=\(physical/16\).*?;",texts["b0"])[0]
pool_o=re.search(r"size_t o=size_t\(physical/16\).*?;",texts["b0"])[0]
parts.append("size_t full_offset(int wx,int wy,int lx,int ly,int c,int nw){"+full+"return tile*512+lane*16+b;}")
parts.append("size_t pool_offset(int wx,int wy,int lx,int ly,int physical,int nw,int nh){"+pool_c+pool_o+"return o;}")
main=r'''
template<class T> void filevec(std::vector<T>& v,const char* path){
 std::ifstream f(path,std::ios::binary|std::ios::ate);if(!f)throw std::runtime_error("asset");
 auto n=f.tellg();v.resize(size_t(n)/sizeof(T));f.seekg(0);f.read((char*)v.data(),n);
}
void put16(uint8_t* p,uint16_t v){std::memcpy(p,&v,2);}
void sample_example(){
 uint8_t tex[32]{};double values[4]={1,0x1p-20,-.5,2};
 for(int k=0;k<4;k++)put16(tex+8*k,half_round(values[k]));
 float x=.5f+73.f/256,y=.5f+119.f/256;
 auto v=tn_sample(tex,2,2,x,y,0);
 std::cout<<"TEX_joint "<<v<<" "<<std::hex<<half_round(v)<<std::dec<<"\n";
 put16(tex,half_round(1));put16(tex+8,half_round(1.125));
 auto mid=tn_sample(tex,2,2,.5f+1.f/256,.5f,0);
 std::cout<<"TEX_midpoint "<<std::hex<<half_round(mid)<<" "<<half_round(1+0x1p-11)<<std::dec<<"\n";
 uint8_t hist[4*4*8]{},mv[4*4*4]{};Ws ws;ws.q.resize(33);
 auto setp=[&](int word,float value){auto b=std::bit_cast<uint32_t>(value);
  ws.q[word/2]|=uint64_t(b)<<((word%2)*32);};
 setp(40,1);setp(41,1);setp(49,.5);
 for(int yy=0;yy<4;yy++)for(int xx=0;xx<4;xx++)for(int c=0;c<3;c++)
   put16(hist+(yy*4+xx)*8+c*2,half_round((xx+2*yy+c+1)/16.));
 put16(mv+(1*4+1)*4,half_round(.0625));put16(mv+(1*4+1)*4+2,half_round(-.0625));
 uint16_t out[3],traced[3];native_history_pixel(hist,mv,ws,1,1,4,4,out);
 history_traced(hist,mv,ws,1,1,4,4,traced);
 if(std::memcmp(out,traced,6))throw std::runtime_error("history trace changed arithmetic");
 std::cout<<"five_tap_RGB";
 for(auto h:out)std::cout<<" "<<std::hex<<std::setw(4)<<std::setfill('0')<<h;
 std::cout<<std::dec<<"\n";
}
int main(int argc,char** argv){
 if(argc!=6||std::fegetround()!=FE_TONEAREST)throw std::runtime_error("args/RN");
 static_assert(std::numeric_limits<float>::is_iec559&&std::numeric_limits<double>::is_iec559);
 filevec(ex2tab,argv[1]);filevec(rcptab,argv[2]);filevec(lg2codec.base,argv[3]);
 filevec(lg2codec.e126,argv[4]);filevec(lg2codec.levels,argv[5]);
 lg2idx.fill(-1);for(int i=111;i<=127;i++)lg2idx[i]=i-111;
 NEGATIVE_BLOCKS
 POSITIVE_BLOCKS
 std::cout<<std::setprecision(10);
 std::cout<<"B0_full_pool "<<full_offset(0,0,1,2,3,1920)<<" "
          <<pool_offset(0,0,1,2,5,1920,1152)<<"\n";
 sample_example();
 uint8_t p[376]{},raw[8]{},base[8]{},out[8]{},other[8]{};
 auto pf=[&](int at,float v){std::memcpy(p+at,&v,4);};
 auto pu=[&](int at,uint64_t v){std::memcpy(p+at,&v,8);};
 pf(0x144,-.1f);pf(0x14c,-.25f);pf(0x150,-.1f);pf(0x154,0);pf(0x120,1);
 uint32_t one=1;std::memcpy(p+0x124,&one,4);std::memcpy(p+0x128,&one,4);
 pu(0,3);pu(32,1);pu(64,2);
 for(int c=0;c<3;c++){put16(raw+c*2,half_round((c+1)*.25));put16(base+c*2,half_round((c+1)*.125));}
 Texture tr{raw,8,0,1},tb{base,8,0,2},to{out,8,3,0},tt{other,8,3,0};
 s157(p,tr,tb,to,1);s157_traced(p,tr,tb,tt,1);
 if(std::memcmp(out,other,8))throw std::runtime_error("trace changed arithmetic");
 std::cout<<"L157_RGBA";
 for(int c=0;c<4;c++)std::cout<<" "<<std::hex<<std::setw(4)<<std::setfill('0')<<le16(out+2*c);
 std::cout<<std::dec<<"\n";
}
'''
main=main.replace("NEGATIVE_BLOCKS","\n".join(f"exneg[{b}]=true;" for b in manifest["runtime"]["ex2_negative_blocks"]))
main=main.replace("POSITIVE_BLOCKS","\n".join(f"expos[{b}]=true;" for b in manifest["runtime"]["ex2_positive_blocks"]))
compiler=shutil.which("g++")
assert compiler,"g++ required"
with tempfile.TemporaryDirectory(prefix="scalar-r04g-",dir=HERE) as folder:
    work=Path(folder).resolve()
    assert work.is_relative_to(HERE.resolve()) # Bound compiler writes and eventual recursive cleanup.
    source=work/"scalar.cpp";exe=work/"scalar.exe"
    source.write_text(headers+"\n\n".join(parts)+main,encoding="utf-8")
    flags=["-std=c++20","-O2","-fno-fast-math","-ffp-contract=off","-frounding-math","-static"]
    env=dict(os.environ,TEMP=str(work),TMP=str(work),TMPDIR=str(work))
    build=subprocess.run([compiler,*flags,str(source),"-o",str(exe)],capture_output=True,text=True,env=env)
    if build.returncode:raise RuntimeError(build.stderr)
    args=[str(assets[n]) for n in ("ex2","rcp","base_E127.bin","raw_E126.bin","level_3bit.bin")]
    run=subprocess.run([str(exe),*args],capture_output=True,text=True,check=True,env=env)
    generated_sha=hashlib.sha256(source.read_bytes()).hexdigest()
receipt={"status":"PASS","scope":"artificial one-point scalar/layout examples; no GPU/model/network chain",
 "QKV_layout":layout,"stdout":run.stdout,"source_sha256":pins,
 "generated_scalar_sha256":generated_sha,"flags":flags,
 "compiler":compiler,"raw_fallback":"throws if invoked; chosen pixel required none",
 "tracing":"entire original s157 executed; trace copy adds output only and must match final 8 bytes"}
HERE.joinpath("substitutions_r04g.result.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(layout));print(run.stdout,end="")
