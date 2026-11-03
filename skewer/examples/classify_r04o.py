"""Update original audit rows with field-level r02 evidence, preserving failed and empty cases."""
from pathlib import Path
from collections import Counter
import json
import runpy

HERE = Path(__file__).resolve().parent
prior_module = runpy.run_path(str(HERE / 'classify_r04n.py'))
C, T, P, M, U = (prior_module[k] for k in ('C', 'T', 'P', 'M', 'U'))
MOVED = {
    'F16.02','F16.15','F17.02','F17.04','F17.09','F19.03','F19.09',
    'F20.02','F20.03','F20.15','F21.02','F21.03','F21.04','F21.09',
    'F22.02','F22.03','F22.04','F22.11','F23.02','F23.03','F23.07'}
FIELD_STATUS = {
 'F16':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'FAIL_MISMATCH','gstore_off':'EXACT','xsite_src':'VACUOUS_EMPTY','xsite_wsrc':'VACUOUS_EMPTY'},
 'F17':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'FAIL_MISMATCH','gstore_off':'EXACT','xsite_src':'EXACT','xsite_wsrc':'EXACT'},
 'F19':{'wload_off':'FAIL_SHAPE','sread_shared_off':'EXACT','sread_src':'EXACT','gstore_off':'EXACT','xsite_src':'FAIL_SHAPE','xsite_wsrc':'FAIL_SHAPE','thread_class':'FAIL_TABLE'},
 'F20':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'EXACT','gstore_off':'EXACT','xsite_src':'VACUOUS_EMPTY','xsite_wsrc':'VACUOUS_EMPTY','thread_class':'FAIL_TABLE'},
 'F21':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'EXACT','gstore_off':'EXACT','xsite_src':'EXACT','xsite_wsrc':'EXACT','thread_class':'FAIL_TABLE'},
 'F22':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'EXACT','gstore_off':'EXACT','xsite_src':'EXACT','xsite_wsrc':'EXACT','shfl_idx':'EXACT','psel':'EXACT','thread_class':'EXACT_BUT_TABLE'},
 'F23':{'wload_off':'EXACT','sread_shared_off':'EXACT','sread_src':'EXACT','gstore_off':'EXACT','xsite_src':'VACUOUS_EMPTY','xsite_wsrc':'VACUOUS_EMPTY'}}


def classification():
    prior = prior_module['classification']()
    assert prior == json.loads((HERE/'r04n.classification.json').read_text(encoding='utf-8')), 'r04n classification changed; stop'
    rows = prior['rows']
    for row in rows:
        if row['id'] in MOVED:
            assert row['current'] == T
            row['prior_r04n'] = T
            row['current'] = C
            row['evidence'] = 'L3_split16_window.md#rest-closed-form-r04o'
            row['action'] = 'r02_heldout_map_formula'
    categories = (C,T,P,M,U)
    def counts(values):
        n=Counter(values)
        return {key:n[key] for key in categories}
    default=[r for r in rows if r['id'].startswith('F')]
    def group(lo,hi):return [r for r in default if lo<=int(r['id'][1:3])<=hi]
    weakness={key:i for i,key in enumerate(categories)}
    family={f'F{k:02}':max((r['current'] for r in group(k,k)),key=weakness.get) for k in range(1,45)}
    field_aware=family.copy()
    for name in ('F20','F21'):
        assert field_aware[name]==C
        field_aware[name]=T
    result=dict(audit_sha256=prior['audit_sha256'],baseline_round='r04n',default_prior=prior['default_current'],
                default_current=counts(r['current'] for r in default),
                tin_F03_F15_prior=counts(r['current'] for r in prior['rows'] if r['id'].startswith('F') and 3<=int(r['id'][1:3])<=15),
                tin_F03_F15_current=counts(r['current'] for r in group(3,15)),
                split_F16_F23_current=counts(r['current'] for r in group(16,23)),
                moved_table_to_closed=sorted(MOVED), variant_current=prior['variant_current'],
                family_audit_rows=counts(family.values()),family_field_aware=counts(field_aware.values()),
                family_note='Original audit has no separate F20/F21 thread_class row; field-aware rollup keeps both TABLE.',
                field_status=FIELD_STATUS, thread_class_policy='All remain table-driven; F22 stored labels also matched its held-out candidate.',
                tier='closed forms verified on held-out map tables; only exact nonempty fields promoted',
                tin_tier='code-transcribed index formula; no new held-out derivation',
                worklist=sorted([r for r in rows if r['rank']],key=lambda r:r['rank']), rows=rows)
    assert len(MOVED)==21 and result['default_current']=={C:1731,T:87,P:0,M:0,U:6}
    assert result['tin_F03_F15_current']=={C:787,T:28,P:0,M:0,U:1}
    assert len(rows)==1846 and len(result['worklist'])==226
    return result


if __name__=='__main__':
    result=classification()
    (HERE/'r04o.classification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('default_prior','default_current','tin_F03_F15_current','split_F16_F23_current','family_audit_rows','family_field_aware','moved_table_to_closed')},ensure_ascii=False,indent=2))
