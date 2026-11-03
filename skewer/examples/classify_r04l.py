"""Reclassify the audit rows without modifying the audit or executing a model."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1] / 'reviews/FORMULA_COVERAGE_R1_codex_20261027.md'
C, T, P, M, U = ('CLOSED_FORMULA', 'TABLE_DRIVEN_DESCRIBED', 'PARTIAL',
                 'MISSING', 'UNKNOWN_IN_SOURCE')

def adjudicate(rid, description, old):
    if rid == 'V01.02':
        return U, 'L0a_object_method.md#route-scope-r04l', 'scope_only_host_generation_remains_open'
    exact = {
        'V07.01': 'L4_e4m3_and_k32.md#build-selection-r04l',
        'V01.05': 'L3_b70_history_output.md#route-owners-r04l',
        'V03.02': 'L3_b0_input.md#p5-packed-r04l',
        'V04.02': 'L3_b70_history_output.md#parent-predicate-r04l',
        'F44.02': 'L3_b70_history_output.md#parent-predicate-r04l',
        'F03.02': 'L3_b0_input.md#resource-unpack-r04l',
        'F43.02': 'L3_b70_history_output.md#resource-unpack-r04l',
        'F43.47': 'L3_b70_history_output.md#resource-unpack-r04l',
        'F43.41': 'L3_b70_history_output.md#den-uv-r04l',
        'F43.51': 'L3_b70_history_output.md#den-uv-r04l',
        'F27.18': 'L4_half_arith.md#transpose-r04l',
        'F26.03': 'L3_ffn.md#contract-class-r04l',
        'F26.04': 'L3_ffn.md#contract-class-r04l',
        'F15.54': 'L3_tin_window.md#zero-planes-r04l',
    }
    if rid in exact:
        return C, exact[rid], 'formula_completed'
    if rid in ('F22.08', 'F23.04'):
        return T, 'L3_split16_window.md#dual-dag-r04l', 'complete_DAG_table_contract'
    if old == P:
        if any(x in description for x in ('releases', 'releaseword', 'release60', 'release63', 'release完整', 'ctr/ctr2')):
            return C, 'L3_workspace_map.md#release-contract-r04l', 'formula_completed'
        if '资源矩阵' in description:
            return C, 'L3_tin_window.md#resource-layout-r04l', 'formula_completed'
        if '物理布局' in description or 'encode_layout' in description:
            return C, 'L3_tin_window.md#view-layout-r04l', 'formula_completed'
        if '部分和' in description or '投影残差' in description:
            return C, 'L3_workspace_map.md#partial-sums-r04l', 'formula_completed'
        raise AssertionError(('unreviewed partial', rid))
    if old == M:
        raise AssertionError(('unreviewed missing', rid))
    if rid in ('F03.06', 'F03.07'):
        return T, 'L4_mufu.md#noise-spec-r04l', 'table_spec_completed_value_still_table'
    if rid in ('F43.83', 'F43.90', 'F43.91', 'F44.03', 'F44.04', 'F44.05', 'F44.06', 'F44.07', 'V05.03'):
        return T, 'L4_mufu.md#tail-dispatch-r04l', 'table_spec_completed_value_still_table'
    if old == T and ('RSQ' in description or 'RCP' in description):
        return T, 'L4_mufu.md#lookup-contract-r04l', 'table_spec_completed_value_still_table'
    return old, None, 'unchanged'

def classification():
    raw = AUDIT.read_bytes()
    lines = raw.decode('utf-8').splitlines()
    ranks = {}
    for line in lines:
        if re.match(r'^\| \d+ \|', line):
            cells = [x.strip() for x in line.strip('|').split('|')]
            if re.match(r'^[FV]\d\d\.\d+', cells[1]):
                ranks[cells[1].split()[0]] = int(cells[0])
    rows = []
    for i, line in enumerate(lines, 1):
        if not re.match(r'^\| [FV]\d\d\.\d+', line):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        rid = cells[0].split()[0]
        old = cells[2]
        new, evidence, action = adjudicate(rid, cells[0], old)
        rows.append(dict(id=rid, audit_line=i, baseline=old, current=new,
                         rank=ranks.get(rid), evidence=evidence, action=action))
    assert len(rows) == len({r['id'] for r in rows}) == 1846
    default = [r for r in rows if r['id'][0] == 'F']
    variants = [r for r in rows if r['id'][0] == 'V']
    before = dict(Counter(r['baseline'] for r in default))
    assert before == {C: 1606, T: 110, P: 100, M: 2, U: 6}
    weakness = {C: 0, T: 1, P: 2, M: 3, U: 4}
    families = Counter()
    for k in range(1, 45):
        fam = [r['current'] for r in default if r['id'].startswith(f'F{k:02}.')]
        families[max(fam, key=weakness.get)] += 1
    def counts(values):
        counts=Counter(values)
        return {k:counts[k] for k in (C,T,P,M,U)}
    return dict(audit_sha256=hashlib.sha256(raw).hexdigest(),
                default_baseline=before, default_current=counts(r['current'] for r in default),
                variant_baseline=counts(r['baseline'] for r in variants),
                variant_current=counts(r['current'] for r in variants),
                family_current={k:families[k] for k in (C,T,P,M,U)},
                worklist=sorted([r for r in rows if r['rank']], key=lambda r: r['rank']),
                rows=rows)

if __name__ == '__main__':
    result = classification()
    (HERE / 'r04l.classification.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('rows', 'worklist')}, indent=2))
