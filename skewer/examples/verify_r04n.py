"""Offline document, classification, source identity and publication checks for r04n."""
from pathlib import Path
from collections import Counter, deque
from urllib.parse import unquote, urlsplit
import argparse
import ast
import json
import re
import runpy

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
old = runpy.run_path(str(HERE / 'verify_r04k.py'))
qa = runpy.run_path(str(HERE / 'verify_r04g.py'))
safe, raw, sha, load, all_files = (old[k] for k in ('safe', 'raw', 'sha', 'load', 'all_files'))
ERRORS = []
ALLOWED = {'INDEX.md', 'APPENDIX_evidence_history.md', 'L2_04_split16_encoder.md',
           'L2_07_split16_decoder.md', 'L3_split16_window.md', 'L3_workspace_map.md'}


def require(ok, message):
    if not ok:
        ERRORS.append(message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pre-scan', action='store_true')
    args = ap.parse_args()
    files = all_files()
    docs = {p.name: raw(p).decode('utf-8').replace('\r\n', '\n') for p in files if p.parent == BASE and p.suffix == '.md'}
    baseline = load(HERE / 'r04n.baseline.json')['files']
    reference = load(HERE / 'r04k.baseline.json')
    changed = []
    for name, pin in baseline.items():
        if sha(raw(BASE / name)) != pin:
            changed.append(name)
    require(set(changed) == ALLOWED, 'only six intended existing documents changed')
    require(len(docs) == 48, '48 root Markdown pages')
    coverage = qa['coverage'](docs)
    require(coverage == Counter(reference['coverage']), 'coverage comments unchanged')
    launches, kernels = Counter(), set()
    for item, count in coverage.items():
        row = json.loads(item)
        launches.update({i: count for i in row['launches']})
        kernels.update(row['kernels'])
    require(launches == Counter(range(158)) and len(kernels) == 44, '158 launches exactly once and 44 kernel names')
    inline = Counter(qa['code_signature'](code) for text in docs.values() for _, code in qa['blocks'](text))
    require(inline == Counter(reference['inline_ast']), 'seven inline arithmetic blocks unchanged')
    ids = {name: qa['anchors'](text) for name, text in docs.items()}
    graph = {name: set() for name in docs}
    links = 0
    for name, text in docs.items():
        visible, fence = qa['without_fences'](text)
        require(fence is None, 'unclosed fence: ' + name)
        explicit = re.findall(r'<a id="([^"]+)"', text)
        require(len(explicit) == len(set(explicit)), 'duplicate anchor: ' + name)
        require(text.endswith('\n') and all(line.rstrip() == line for line in text.splitlines()), 'whitespace: ' + name)
        for table in re.findall(r'(?m)(?:^\|.*\n?)+', visible):
            require(len({len(re.split(r'(?<!\\)\|', line)) for line in table.splitlines()}) == 1, 'table arity: ' + name)
        for dest in re.findall(r'\]\(([^)\n]+)\)', visible):
            dest = dest.strip()
            dest = dest[1:dest.index('>')] if dest.startswith('<') else dest.split(' "', 1)[0]
            u = urlsplit(dest)
            if u.scheme in ('http', 'https', 'mailto', 'plugin'):
                continue
            filename, fragment = unquote(u.path), unquote(u.fragment)
            if re.match(r'^[A-Za-z]:[/\\]', dest):
                filename = unquote(dest.split('#', 1)[0])
            target = safe(BASE / name if not filename else Path(filename) if re.match(r'^[A-Za-z]:', filename) else BASE / filename)
            links += 1
            require(target.exists(), 'missing link ' + name + ': ' + dest)
            if not target.is_file():
                continue
            internal = target.parent == BASE and target.name in docs
            if internal:
                graph[name].add(target.name)
            if re.fullmatch(r'L\d+(?:-L?\d+)?', fragment):
                require(all(1 <= int(i) <= len(raw(target).splitlines()) for i in re.findall(r'\d+', fragment)), 'line anchor ' + name + ': ' + dest)
            elif fragment and target.suffix == '.md':
                anchors = ids[target.name] if internal else qa['anchors'](raw(target).decode('utf-8-sig'))
                require(fragment in anchors, 'heading ' + name + ': ' + dest)
    reached, queue = set(), deque(['L0_frame.md'])
    while queue:
        name = queue.popleft()
        if name not in reached:
            reached.add(name)
            queue.extend(graph[name] - reached)
    require(reached == set(docs), 'all pages reachable')
    classifier = runpy.run_path(str(HERE / 'classify_r04n.py'))
    classification = classifier['classification']()
    require(classification == load(HERE / 'r04n.classification.json'), 'classification receipt current')
    prior = load(HERE / 'r04l.classification.json')
    status_moves = [row['id'] for row, before in zip(classification['rows'], prior['rows']) if row['current'] != before['current']]
    require(status_moves == ['F18.02', 'F18.03', 'F18.04', 'F18.39'], 'four aggregate row moves only')
    require(classification['variant_current'] == prior['variant_current'] and classification['family_current'] == prior['family_current'], 'variant and family counts unchanged')
    for row in classification['worklist']:
        if row['evidence']:
            name, anchor = row['evidence'].split('#')
            require(anchor in ids[name], 'classification evidence: ' + row['id'])
    for name in ('INDEX.md', 'APPENDIX_evidence_history.md'):
        require('1710' in docs[name] and '108' in docs[name], 'current coverage count: ' + name)
    chapter = docs['L3_split16_window.md'].split('<a id="qkv-closed-form-r04n"></a>')[1].split('<a id="layout"></a>')[0]
    fields = classification['qkv_field_status']
    require(all(field in chapter for field in fields), 'eight closed fields plus open class named')
    require('PARTIAL_QKV_CLOSED_FORM_8/9_FIELDS_HELDOUT_EXACT' in chapter and 'closed forms verified on held-out map tables' in chapter, 'exact verdict and evidence tier')
    require(all(term in chapter for term in ('1080', '640×360', '1440', '4K', '1536/2048', 'NOT_PRESENT', '数值DAG', '动态原生血缘')), 'derivation, heldout and open proof boundaries')
    sample = load(HERE / 'r04n.qkv_samples.json')
    sample_helper = runpy.run_path(str(HERE / 'qkv_closed_form_r04n.py'))
    require(sample['status'] == 'PASS' and sample['samples'] == len(sample['rows']) == 58 and sample['mismatches'] == 0, '58 sampled address/index cells')
    require(all(row['formula'] == row['document_formula'] == row['stored'] and row['status'] == 'EXACT' for row in sample['rows']), 'three-way sample equality')
    require({row['geometry'] for row in sample['rows']} == {'1080', '4K'}, 'two sample geometries')
    require({row['stored'] for row in sample['rows'] if row['field'] == 'psel'} == {0, 1}, 'selection samples include both outputs')
    source_round = sample_helper['ROUND']
    for name, pin in sample['research_source_sha256'].items():
        require(sample_helper['sha'](source_round / name) == pin, 'research source unchanged: ' + name)
    for table in sample['source_tables']:
        require(sample_helper['sha'](table['path']) == table['sha256'], 'sample source map identity: ' + table['label'])
        matching = [row for row in sample['rows'] if row['geometry'] == table['label']]
        require(all(row['coordinate'][0] == table['a'] for row in matching), 'one window per sample geometry')
    summary = load(source_round / 'SUMMARY.json')
    require(summary['verdict'] == classification['verdict'], 'saved research verdict')
    require(all(row['mismatches'] == 0 for row in summary['per_field_geometry'] if row['field'] != 'thread_class'), 'saved eight-field map comparisons exact')
    failures = [row for row in summary['per_field_geometry'] if row['field'] == 'thread_class']
    require(len(failures) == 1 and failures[0]['mismatches'] == 1536 and failures[0]['elements'] == 2048, 'failed class hypothesis remains failed')
    worked_rows = re.findall(r'^\| (\w+)，e=(\d+)(?:,b=(\d+))? \| ([−\-\d]+) / ([−\-\d]+) \| ([−\-\d]+) / ([−\-\d]+) \|$', chapter, re.M)
    require(len(worked_rows) == 9, 'nine worked table rows')
    for field, event, byte, f1080, s1080, f4k, s4k in worked_rows:
        for label, predicted, stored in [('1080', f1080, s1080), ('4K', f4k, s4k)]:
            candidates = [row for row in sample['rows'] if row['geometry'] == label and row['field'] == field and
                          row['coordinate'][2] == 5 and row['coordinate'][3] == int(event) and
                          (not byte or row['coordinate'][4] == int(byte))]
            require(len(candidates) == 1, 'worked row sample exists: ' + field)
            if len(candidates) == 1:
                require(int(predicted.replace('−', '-')) == candidates[0]['formula'] and int(stored.replace('−', '-')) == candidates[0]['stored'], 'worked table value: ' + label + ' ' + field)
    for p in files:
        data = raw(p)
        require(not any(word.encode('utf-8') in data for word in old['OLD_WORDS']), 'avoided word: ' + p.name)
    for name in ('qkv_closed_form_r04n.py', 'classify_r04n.py', 'verify_r04n.py'):
        ast.parse(raw(HERE / name).decode('utf-8'))
    scan_path = HERE / 'r04n.leak.json'
    scan = load(scan_path)['summary'] if scan_path.exists() else None
    if not args.pre_scan:
        require(scan is not None and scan['PASS'] and scan['files_with_block'] == scan['files_with_name_violation'] == scan['missing'] == 0, 'official publication scan')
        require(scan is not None and scan['files'] == len(files), 'scan file count current')
        require(scan is not None and 'word_pc' not in scan['files_per_pattern'], 'no program-counter tokens')
    result = dict(status='PASS' if not ERRORS else 'FAIL', mode='pre-scan' if args.pre_scan else 'final',
                  markdown_pages=len(docs), reachable_pages=len(reached), local_links_checked=links,
                  coverage_comments=sum(coverage.values()), launches_exactly_once=len(launches), unique_kernel_names=len(kernels),
                  unchanged_inline_arithmetic_blocks=sum(inline.values()), changed_existing_files=changed,
                  preserved_prior_files=len(baseline) - len(changed), default_prior=classification['default_prior'], default_current=classification['default_current'],
                  moved_table_to_closed=status_moves, closed_qkv_fields=8, table_qkv_fields=['thread_class'],
                  aggregate_F18_05='TABLE; shfl_idx/psel CLOSED; thread_class TABLE',
                  variant_current=classification['variant_current'], family_current=classification['family_current'],
                  sampled_address_cells=sample['samples'], sample_mismatches=sample['mismatches'], displayed_worked_cells=2 * len(worked_rows),
                  research_sources_unchanged=True, source_map_containers_unchanged=True, avoided_word_hits=0,
                  red_line_review='Layout/index integers only; no new hardware registers, program-counter values, operand listings or model coefficient values',
                  new_GPU_runs=0, new_model_runs=0, new_chain_runs=0, new_compile_runs=0, new_full_map_runs=0,
                  network_calls=0, remote_calls=0, version_control_calls=0, external_writes=0,
                  files_in_tree=len(files), official_scan=scan, document_sha256={name: sha(raw(BASE / name)) for name in docs},
                  classification_sha256=sha(raw(HERE / 'r04n.classification.json')), sample_sha256=sha(raw(HERE / 'r04n.qkv_samples.json')), errors=ERRORS)
    (HERE / 'r04n.validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('document_sha256', 'official_scan')}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))


if __name__ == '__main__':
    main()
