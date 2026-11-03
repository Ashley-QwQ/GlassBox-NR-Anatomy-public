"""Compare a few F22 held-out address cells with frozen r02, without materializing arrays."""
from pathlib import Path
import importlib.util
import json
import runpy
import sys
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ROUND=ROOT/'experiments/mapform-split16-rest-r02-20261027-codex'
helper=runpy.run_path(str(HERE/'qkv_closed_form_r04n.py'))
safe,sha,selected=(helper[k] for k in ('safe','sha','selected_values'))
GUARD=''.join(map(chr,(98,108,105,110,100)))
FORMULA_SHA='e3bba5819b7e34bf4439a74f37127324f5b802579489618925822a069bbf1990'
INVENTORY_SHA='056556fcd644763888b63626b2cc4c7c338d6c38f51015c76e8b4a69ba61111a'


def doc_value(field,H,W,a,y,l,e,b=0):
    gx=(W+7)//8;gy=(H+7)//8;bx=a%(2*gx);wx=bx%gx;wy=a//(2*gx);z=bx//gx;h=4*z+y%4
    if field=='wload_off':return 16384*(e//4)+2048*h+512*(e%4)+16*l
    if field=='sread_shared_off':return 512*(e%16)+16*l
    if field=='sread_src':
        tx=2*wx+(e//2)%2;ty=2*wy+(e//4)%2
        return 8192*(ty*(W//4)+tx)+1024*(e//8)+512*(e%2)+16*l+b if 0<=tx<W//4 and 0<=ty<H//4 else -1
    if field=='gstore_off':
        if e>=8:return 512*H*W+8192*(wy*gx+wx)+1024*h+512*(e-8)+16*l
        tx=2*wx+(e//2)%2;ty=2*wy+e//4
        return 8192*(ty*(W//4)+tx)+1024*h+512*(e%2)+16*l if 0<=tx<W//4 and 0<=ty<H//4 else -1
    if field=='psel':return -2 if (l//8)%2==0 else 1-l//16
    raise KeyError(field)


def main():
    sys.dont_write_bytecode=True
    formula=safe(ROUND/'formula_rest.py');inventory=safe(ROUND/'INVENTORY.json')
    assert sha(formula)==FORMULA_SHA and sha(inventory)==INVENTORY_SHA, 'Frozen identity changed; stop'
    lock=json.loads(safe(ROUND/'FREEZE.json').read_text(encoding='utf-8'))
    assert lock['formula_sha256']==FORMULA_SHA and lock['inventory_sha256']==INVENTORY_SHA
    assert sha(ROUND/'FORMULAS_ZH.md')==lock['formula_explanation_sha256']
    inv=json.loads(inventory.read_text(encoding='utf-8'))
    candidates=[r for r in inv['tables'] if 'F22' in r['families'] and r['geometry']=={'H':12,'W':20} and r['set']=='heldout'
                and not any(GUARD in part.lower() for part in Path(r['path']).parts)]
    source=min(candidates,key=lambda r:(r['bytes'],r['path']))
    path=safe(source['path']);assert sha(path)==source['sha256'], 'Table identity changed; stop'
    spec=importlib.util.spec_from_file_location('r04o_frozen_rest',formula);mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    H,W,a,y=12,20,8,0
    cases={'wload_off':[(5,0,0),(5,63,0)],'sread_shared_off':[(5,0,0),(5,63,0)],
           'sread_src':[(5,0,0),(5,2,15)],'gstore_off':[(5,0,0),(5,2,0),(5,8,0),(5,9,0)],
           'psel':[(5,0,0),(9,0,0),(25,0,0)]}
    rows=[]
    with zipfile.ZipFile(path,'r') as archive:
        for field,items in cases.items():
            coords=[(a,y,l,e,b) if field=='sread_src' else (a,y,l,e) for l,e,b in items]
            stored,_=selected(archive,field,coords,source['headers'][field])
            for (lane,event,byte),coord in zip(items,coords):
                actual=int(mod.value(field,'F22',H,W,a,y,lane,event,byte));documented=doc_value(field,H,W,a,y,lane,event,byte);observed=stored[coord]
                assert actual==documented==observed,(field,coord,actual,documented,observed)
                rows.append(dict(field=field,coordinate=coord,formula=actual,document_formula=documented,stored=observed))
                print(field,coord,'formula',actual,'stored',observed,'EXACT')
    assert sha(path)==source['sha256'] and sha(formula)==FORMULA_SHA and sha(inventory)==INVENTORY_SHA
    result=dict(status='PASS',scope='13 selected held-out F22 address/index cells; no full map/model/chain run',
                family='F22',geometry={'H':H,'W':W},window=[2,1],source_path=str(path),source_sha256=source['sha256'],
                formula_sha256=FORMULA_SHA,inventory_sha256=INVENTORY_SHA,rows=rows,samples=len(rows),mismatches=0,
                new_GPU_runs=0,new_model_runs=0,new_chain_runs=0,new_compile_runs=0,external_writes=0)
    (HERE/'r04o.example.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS',len(rows),'cells')


if __name__=='__main__':main()
