"""Read and bind existing r04/r02 receipts; no array generation or model execution."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
R04=ROOT/'experiments/mapform-split16-r04-20261027-codex'
R02=ROOT/'experiments/mapform-split16-rest-r02-20261027-codex'
R01=ROOT/'experiments/mapform-split16-qkv-r01-20261027-codex'
GUARD=''.join(map(chr,(98,108,105,110,100)))


def safe(p):
    p=Path(p).resolve()
    if any(GUARD in part.lower() for part in p.parts):raise ValueError('Excluded path')
    return p


def sha(p):
    h=hashlib.sha256()
    with safe(p).open('rb') as f:
        for data in iter(lambda:f.read(1<<20),b''):h.update(data)
    return h.hexdigest()


def load(p):return json.loads(safe(p).read_text(encoding='utf-8'))


def sealed(name):
    # r04 repair_reports.py kept the receipt-pinned originals as <name>.garbled-ascii next to the repaired reports
    old=R04/(name+'.garbled-ascii')
    return old if old.exists() else R04/name


def build():
    validation=load(R04/'VALIDATION.json')
    for name,key in [('PREDECL_ZH.md','predecl_sha256'),('RESULT_ZH.md','result_sha256'),('BINDINGS.json','bindings_sha256'),('COMPARISONS.json','comparisons_sha256')]:
        assert sha(sealed(name))==validation[key], 'Research receipt identity mismatch; stop: '+name
    bindings=load(R04/'BINDINGS.json')['bindings'];comp=load(R04/'COMPARISONS.json')
    assert sha(R02/'formula_rest.py')==comp['formula_rest_sha256']
    assert sha(R01/'formula_qkv.py')==comp['formula_qkv_sha256']
    assert Counter(r['status'] for r in bindings)==Counter({'BOUND':31,'OUT_OF_SCOPE':28,'NOT_RUN':3})
    assert validation['unique_comparisons']==len(comp['comparisons'])==10 and validation['all_compared_fields_exact']
    assert all(f['status']=='EXACT' and f['mismatches']==0 and f['source_array_sha256']==f['formula_array_sha256']
               for row in comp['comparisons'] for f in row['fields'].values())
    counts={}
    for family in ('F16','F17','F19','F20','F21','F22'):
        rows=[r for r in bindings if r['status']=='BOUND' and r.get('binding',{}).get('family')==family and r['binding']['geometry']=={'H':68,'W':120}]
        distinct={r['sha256'] for r in rows};assert len(distinct)==1
        item=next(r for r in comp['comparisons'] if r['family']==family and r['geometry']=={'H':68,'W':120})
        assert item['sha256'] in distinct
        counts[family]={'paths':len(rows),'distinct_containers':len(distinct),
                        'fields':{k:{'elements':v['elements'],'status':v['status']} for k,v in item['fields'].items()}}
    assert [counts[x]['paths'] for x in counts]==[3,1,7,7,7,2]
    f16_1440=next(r for r in comp['comparisons'] if r['family']=='F16' and r['geometry']=={'H':48,'W':80})
    f23=next(r for r in bindings if r['status']=='BOUND' and r.get('binding',{}).get('family')=='F23')
    assert f23['binding']['geometry']=={'H':36,'W':60}
    f23_compare=next(r for r in comp['comparisons'] if r['family']=='F23' and r['sha256']==f23['sha256'])
    assert sha(f23['path'])==f23['sha256'], 'F23 table identity mismatch; stop'
    for key,pin in [('descriptor','descriptor_sha256'),('map_sha_proof','map_sha_proof_sha256')]:
        assert sha(f23['binding'][key])==f23['binding'][pin], 'F23 binding evidence mismatch; stop'
    r01=load(R01/'SUMMARY.json')
    qkv=[r for r in r01['per_field_geometry'] if r['set']=='heldout' and r['H']==68 and r['W']==120]
    assert len(qkv)==8 and all(r['mismatches']==0 and r['unique_containers']==4 for r in qkv)
    r01_lock=load(R01/'FREEZE.json')
    assert sha(R01/'INVENTORY.json')==r01_lock['inventory_sha256'], 'QKV inventory identity mismatch; stop'
    qkv_paths=[r for r in load(R01/'INVENTORY.json')['tables'] if r['set']=='heldout' and r['geometry']['H']==68 and r['geometry']['W']==120]
    assert len(qkv_paths)==12 and len({r['sha256'] for r in qkv_paths})==4
    before=load(R02/'heldout_receipts.json')
    accepted=[]
    fields={'F16':['sread_src'],'F17':['sread_src'],'F19':['wload_off','xsite_src','xsite_wsrc']}
    for path,pin in validation['accepted_production_map_sha256'].items():
        assert sha(path)==pin, 'Accepted table identity mismatch; stop'
        row=next(r for r in before['unique_tables'] if r['container_sha256']==pin)
        details={}
        for name in fields[row['family']]:
            f=row['fields'][name]
            assert f['status']=='EXACT' and f['mismatches']==0 and f['source_array_sha256']==f['formula_array_sha256']
            details[name]={'elements':f['elements'],'status':'EXACT'}
        accepted.append({'family':row['family'],'path':path,'sha256':pin,'geometry':row['geometry'],'fields':details})
    assert {r['family'] for r in accepted}==set(fields)
    result_text=safe(sealed('RESULT_ZH.md')).read_text(encoding='utf-8')
    assert result_text.count('NON_PRODUCTION_VARIANT')==5
    repaired=safe(R04/'RESULT_ZH.md').read_text(encoding='utf-8')
    assert repaired.count('NON_PRODUCTION_VARIANT')==5
    return dict(status='PASS',scope='saved receipt reconciliation only; no new full-map, model, GPU or chain run',
                sources={p.relative_to(ROOT).as_posix():sha(p) for p in (R04/'RESULT_ZH.md',R04/'BINDINGS_ZH.md',sealed('RESULT_ZH.md'),sealed('BINDINGS_ZH.md'),
                                                           sealed('PREDECL_ZH.md'),R04/'PREDECL_RECOVERED_NOTE_ZH.md',R04/'repair_reports.py',R04/'BINDINGS.json',R04/'COMPARISONS.json',R04/'VALIDATION.json',R02/'heldout_receipts.json',R01/'SUMMARY.json',R01/'INVENTORY.json')},
                r04_report_chinese_corrupted=all(ord(c)<128 for c in result_text) and result_text.count('?')>100,
                r04_report_repaired=sealed('RESULT_ZH.md')!=R04/'RESULT_ZH.md' and any(ord(c)>0x4e00 for c in repaired),
                candidate_status_counts=dict(Counter(r['status'] for r in bindings)),unique_comparisons=10,elements=validation['elements'],
                r04_4k_physical_68x120=counts,f16_1440={'geometry':f16_1440['geometry'],'fields':{k:v['elements'] for k,v in f16_1440['fields'].items()},'sha256':f16_1440['sha256']},
                qkv_F18_4k={'source':'r01, not r02 or r04','paths':len(qkv_paths),'distinct_containers':len({r['sha256'] for r in qkv_paths}),'fields':{r['field']:r['elements'] for r in qkv}},
                F23={'geometry':f23['binding']['geometry'],'source_path':f23['path'],'sha256':f23['sha256'],
                     'fields':{k:{'elements':v['elements'],'status':v['status']} for k,v in f23_compare['fields'].items()},
                     'frame_identity':'4K input frame not independently bound in inspected r04 binding; path label alone is insufficient'},
                accepted_maps=accepted,historical_status='NON_PRODUCTION_VARIANT; retain r02 MISMATCH / SHAPE_MISMATCH',
                cpp_executor_12x12_map_read='NOT_ESTABLISHED',L132_candidates=28,B31_candidates=3,
                new_gpu_runs=0,new_model_runs=0,new_chain_runs=0,new_full_map_runs=0,network_calls=0,git_calls=0,external_writes=0)


if __name__=='__main__':
    data=build()
    (HERE/'r04p.evidence.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':data['status'],'counts':{k:v['paths'] for k,v in data['r04_4k_physical_68x120'].items()},
                      'f23_geometry':data['F23']['geometry'],'accepted_maps':len(data['accepted_maps']),
                      'report_chinese_corrupted':data['r04_report_chinese_corrupted']},ensure_ascii=False))
