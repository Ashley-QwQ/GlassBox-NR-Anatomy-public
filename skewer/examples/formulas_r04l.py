"""Synthetic integer/layout checks only; no coefficient or model evaluation."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import runpy
import struct

HERE = Path(__file__).resolve().parent
P = (0,1,4,5,8,9,12,13,2,3,6,7,10,11,14,15)
Q = (0,1,8,9,2,3,10,11,4,5,12,13,6,7,14,15)
CHECKS = {}

def physical_to_logical(p, W, H, C, planar):
    if planar:
        j, x, y, plane = p%16, (p//16)%W, (p//(16*W))%H, p//(16*W*H)
        return (y*W+x)*C+16*plane+Q[j]
    if C == 32:
        tile, lane, b = p//512, (p%512)//16, p%16
        x, y = (lane>>2)&3, (lane>>4)+2*((b>>2)&1)
        c = 2*(lane&3)+(b&1)+8*((b>>1)&1)+16*(b>>3)
        return (((tile//(W//4))*4+y)*W+(tile%(W//4))*4+x)*C+c
    off, blk, cb, xs = p%4096, p//4096, C.bit_length()-1, 1024//C
    c=x=y=0
    for i, (kind, bit) in enumerate(zip('ccyccc xxy'.replace(' ', ''), (0,3,1,4,1,2,0,1,0))):
        v=((off>>i)&1)<<bit
        if kind=='c': c|=v
        elif kind=='x': x|=v
        else: y|=v
    pos=9
    for bit in range(5, cb): c|=((off>>pos)&1)<<bit; pos+=1
    for bit in range(2, xs.bit_length()-1): x|=((off>>pos)&1)<<bit; pos+=1
    return (((blk//(W//xs))*4+y)*W+(blk%(W//xs))*xs+x)*C+c

def logical_to_physical(i, W, H, C, planar):
    pixel,c=divmod(i,C); y,x=divmod(pixel,W)
    if planar: return 16*((c//16*H+y)*W+x)+Q.index(c%16)
    if C==32:
        lane=((c>>1)&3)+4*(x%4)+16*(y&1)
        b=(c&1)+2*((c>>3)&1)+4*((y%4)>>1)+8*(c>>4)
        return 512*((y//4)*(W//4)+x//4)+16*lane+b
    xs=1024//C; cb=C.bit_length()-1
    bits=[c&1,(c>>3)&1,(y>>1)&1,(c>>4)&1,(c>>1)&1,(c>>2)&1,x&1,(x>>1)&1,y&1]
    bits += [(c>>b)&1 for b in range(5,cb)]
    bits += [(x>>b)&1 for b in range(2,xs.bit_length()-1)]
    off=sum(v<<j for j,v in enumerate(bits))
    return 4096*((y//4)*(W//xs)+x//xs)+off

def matrix_offset(k,n,K,N,major):
    rk=16*(k//16)+P[k%16]; kt,ki=divmod(rk,32); nt,ni=divmod(n,32)
    lane=4*(ni%8)+(ki%16)//4; elem=ki%4+4*(ki//16)
    tile=4*((nt//4)*(K//32)+kt)+nt%4 if major else kt*(N//32)+nt
    return 1024*tile+512*(ni//16)+16*lane+8*((ni//8)%2)+elem

def matrix_inverse(off,K,N,major):
    tile,j=divmod(off,1024); pair=j//512; lane=(j//16)%32; frag=(j//8)%2; elem=j%8
    ki=4*(lane%4)+elem%4+16*(elem//4); ni=lane//4+8*frag+16*pair
    if major: kt=(tile//4)%(K//32); nt=4*((tile//4)//(K//32))+tile%4
    else: kt,nt=divmod(tile,N//32)
    rk=kt*32+ki
    return 16*(rk//16)+P.index(rk%16), 32*nt+ni

def run():
    layouts=[]
    for C in (32,64,128,256):
        W,H=32,8
        for planar in (False,True):
            N=W*H*C
            image=[physical_to_logical(p,W,H,C,planar) for p in range(N)]
            assert len(set(image))==N and min(image)==0 and max(image)==N-1
            assert all(logical_to_physical(i,W,H,C,planar)==p for p,i in enumerate(image))
            layouts.append([C,planar,N])
    CHECKS['layout_roundtrips']=layouts
    matrices=[]
    for K,N,major in ((32,128,False),(128,32,False),(64,384,True),(256,1152,True),(512,256,False)):
        seen=set()
        for k in range(K):
            for n in range(N):
                off=matrix_offset(k,n,K,N,major)
                assert matrix_inverse(off,K,N,major)==(k,n)
                seen.add(off)
        assert seen==set(range(K*N)); matrices.append([K,N,major,K*N])
    CHECKS['matrix_roundtrips']=matrices
    adapter=set()
    for nt in range(2):
        for i in range(256):
            e,l=i%8,i//8; fe=e%4
            k=2*(l%4)+(fe&1)+8*(fe//2); n=l//4+8*(e//4)
            adapter.add(k*32+nt*16+n)
    assert adapter==set(range(512)); CHECKS['adapter_half_slots']=512
    bias=set()
    def bit(v,b): return (v>>b)&1
    for q in range(64):
        y,x=divmod(q,8)
        for k in range(64):
            ky,kx=divmod(k,8)
            v=(bit(y,2),bit(x,2),bit(ky,2),bit(kx,2),bit(y,0),bit(x,1),bit(x,0),bit(ky,0),bit(kx,1),bit(ky,1),bit(y,1),bit(kx,0))
            bias.add(sum(b<<(11-j) for j,b in enumerate(v)))
    assert bias==set(range(4096)); CHECKS['bias_slots']=4096
    internal=lambda t:32*((t//8)//4)+16*((t%8)//4)+4*((t//8)%4)+t%4
    tin_bias=set()
    for i in range(64):
        for j in range(64):
            r,c=internal(i),internal(j)
            off=256*(4*(r//16)+c//16)+8*(4*(r%8)+(c%8)//2)+4*((c%16)//8)+2*((r%16)//8)+c%2
            tin_bias.add(off)
    assert tin_bias==set(range(4096)); CHECKS['TIN_bias_half_slots']=4096
    heads={(4*c+k//4)*16+2*(k%4) for c in range(4) for k in range(16)}
    assert len(heads)==64 and min(heads)==0 and max(heads)+2<=512
    CHECKS['B70_head_half_slots']=64
    tr=lambda i:8*(i%8)+i//8
    assert all(tr(tr(i))==i for i in range(64)); CHECKS['transpose_half_slots']=64
    half=lambda x:struct.unpack('<e',struct.pack('<e',x))[0]
    a=half(half(2048+1)-2048); b=half(half(2048-2048)+1)
    assert (a,b)==(0,1); CHECKS['half_order_control']=[a,b]
    for Qn in (1,5,8,16):
        assert {32*(x%Qn)+x//Qn for x in range(32*Qn)}==set(range(32*Qn))
    CHECKS['expand_release_permutations']=[1,5,8,16]
    release=json.loads((HERE/'r04l.release_bindings.json').read_text())
    assert Counter(tuple(map(tuple,r['releases'])) for r in release['rows'])==Counter({((6,320),):47,((6,640),):16,():1})
    CHECKS['split_release_calls']={'320':47,'640':16,'empty':1}
    for W,H,PW,PH in ((8,8,4,4),(9,9,8,8),(60,36,32,20)):
        validW,validH=(W+1)//2,(H+1)//2
        for plane in range(64):
            for y in range(PH):
                begin=validW if y<validH else 0
                if begin>=PW: continue
                off=16*((plane*PH+y)*PW+begin); length=16*(PW-begin)
                assert off+length<=16*64*PW*PH and length>=0
                assert y>=validH or begin>=validW
    CHECKS['pool_zero_span_shapes']=3
    assert struct.unpack('<ff',struct.pack('<Q',0x4487000044f00000))==(1920.,1080.)
    assert struct.unpack('<f',struct.pack('<I',0x80000000))[0]==0.0
    place=lambda v,s:(-1 if v<0 else 1)*((abs(v)>>s)<<s)
    assert place(-7,2)==-4 and ((-7>>2)<<2)==-8
    CHECKS['packed_controls_signed_zero_and_RZ']=True
    for name,pin in [('rsq','06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62'),('rcp','055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59')]:
        assert hashlib.sha256((HERE.parents[3]/f'mlxdlss/resources/{name}-domain.npz').read_bytes()).hexdigest()==pin
    CHECKS['function_source_identity_checks']=2
    import numpy as np
    endpoints={}
    for name,size in (('rsq',30705),('rcp',30704)):
        with np.load(HERE.parents[3]/f'mlxdlss/resources/{name}-domain.npz',allow_pickle=False) as table:
            assert all(table[key].shape==(size,) for key in ('input_half_bits','native_half_bits','native_float_bits'))
            assert int(table['input_half_bits'][0])==0x0410
            assert int(table['input_half_bits'][-1])==0x0410+size-1
            if name=='rsq':assert int(table['native_half_bits'][-1])==0
            endpoints[name]={'entries':size,'first_input':0x0410,'last_input':0x0410+size-1}
    CHECKS['function_table_endpoints']=endpoints
    dag=runpy.run_path(str(HERE/'dag_contract_r04l.py'))
    pins=json.loads((HERE/'split16_window_r04d.bindings.json').read_text())
    for launch in (56,57):
        d=json.loads((HERE/f'r04l.L{launch}.dag.json').read_text())
        assert d==dag['project'](launch)
        expected=next(a['sha256'] for a in pins['assets_read'] if a['path']==d['source'])
        assert d['source_sha256']==expected
        nodes=d['nodes']; depth={}; starts=[]
        for j,m in enumerate(d['matrices']):
            prev={nodes[i][1] for i in m['C'] if nodes[i][0]=='M'}
            assert all(i<j for i in prev)
            depth[j]=1+max((depth[i] for i in prev),default=0)
            if not prev: starts.append(j)
        assert max(depth.values())==16 and len(starts)==(32 if launch==56 else 16)
        CHECKS[f'L{launch}_DAG_contract']={'nodes':len(nodes),'matrix_events':len(d['matrices']),'chains':len(starts),'steps_per_chain':16}
    return {'status':'PASS','scope':'synthetic formulas and existing metadata only',
            'checks':CHECKS,'new_GPU_runs':0,'new_model_runs':0,'new_chain_runs':0}

if __name__=='__main__':
    result=run()
    (HERE/'r04l.formulas.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
