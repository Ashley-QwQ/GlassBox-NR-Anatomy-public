"""Preserve the audit row denominator; update only F18 address-map evidence."""
from pathlib import Path
from collections import Counter
import json
import runpy

HERE = Path(__file__).resolve().parent
old = runpy.run_path(str(HERE / 'classify_r04l.py'))
C, T, P, M, U = (old[k] for k in ('C', 'T', 'P', 'M', 'U'))
EVIDENCE = 'L3_split16_window.md#qkv-closed-form-r04n'
FIELDS = {
    'F18.02': ['wload_off'],
    'F18.03': ['sread_shared_off', 'sread_src'],
    'F18.04': ['xsite_src', 'xsite_wsrc'],
    'F18.05': ['shfl_idx', 'psel', 'thread_class'],
    'F18.39': ['gstore_off'],
}


def classification():
    prior = old['classification']()
    saved = json.loads((HERE / 'r04l.classification.json').read_text(encoding='utf-8'))
    assert prior == saved, 'Prior classification or original audit changed; stop'
    rows = prior['rows']
    changes = []
    for row in rows:
        rid = row['id']
        if rid not in FIELDS:
            continue
        assert row['current'] == T
        row['prior_r04l'] = row['current']
        row['field_status'] = {field: T if field == 'thread_class' else C for field in FIELDS[rid]}
        row['evidence'] = EVIDENCE
        if rid == 'F18.05':
            row['action'] = 'two_closed_subfields; table_class_keeps_aggregate_row_table'
        else:
            row['current'] = C
            row['action'] = 'heldout_map_closed_form'
            changes.append(rid)
    categories = (C, T, P, M, U)
    def counts(values):
        counter = Counter(values)
        return {category: counter[category] for category in categories}
    default = [row for row in rows if row['id'].startswith('F')]
    variants = [row for row in rows if row['id'].startswith('V')]
    weakness = {category: rank for rank, category in enumerate(categories)}
    families = [max((row['current'] for row in default if row['id'].startswith(f'F{k:02}.')), key=weakness.get)
                for k in range(1, 45)]
    fields = {field: status for row in rows for field, status in row.get('field_status', {}).items()}
    assert len(fields) == 9 and list(fields.values()).count(C) == 8 and fields['thread_class'] == T
    result = dict(audit_sha256=prior['audit_sha256'], baseline_round='r04l',
                  default_prior=saved['default_current'], default_current=counts(row['current'] for row in default),
                  variant_prior=saved['variant_current'], variant_current=counts(row['current'] for row in variants),
                  family_prior=saved['family_current'], family_current=counts(families),
                  moved_table_to_closed=changes, qkv_field_status=fields,
                  aggregate_rule='Worst component per immutable original row; F18.05 retains thread_class TABLE',
                  thread_class=dict(derivation='NOT_PRESENT at 1080', frozen_hypothesis='FAIL',
                                    heldout_mismatches=1536, heldout_elements=2048, posthoc_description_is_formula=False),
                  evidence_tier='closed forms verified on held-out map tables',
                  verdict='PARTIAL_QKV_CLOSED_FORM_8/9_FIELDS_HELDOUT_EXACT',
                  worklist=sorted([row for row in rows if row['rank']], key=lambda row: row['rank']), rows=rows)
    assert result['default_current'] == {C: 1710, T: 108, P: 0, M: 0, U: 6}
    assert len(result['rows']) == 1846 and len(result['worklist']) == 226
    return result


if __name__ == '__main__':
    result = classification()
    (HERE / 'r04n.classification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('default_prior', 'default_current', 'moved_table_to_closed',
                                                'qkv_field_status', 'variant_current', 'family_current')}, indent=2))
