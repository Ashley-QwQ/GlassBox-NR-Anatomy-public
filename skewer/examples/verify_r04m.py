"""Offline beginner-layer review, preservation, navigation and publication checks."""
from pathlib import Path
from collections import Counter, deque
from urllib.parse import unquote, urlsplit
import argparse
import ast
import json
import re
import runpy
import struct
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
old = runpy.run_path(str(HERE / 'verify_r04k.py'))
qa = runpy.run_path(str(HERE / 'verify_r04g.py'))
safe, raw, sha, load, all_files = (old[k] for k in ('safe', 'raw', 'sha', 'load', 'all_files'))
ERRORS = []


def require(ok, message):
    if not ok:
        ERRORS.append(message)


def unlinked(text):
    return re.sub(r'\[([^\[\]\n]*)\]\(APPENDIX_beginner_glossary.md#g\d{3}\)', r'\1', text)


def restored(text):
    text = re.sub(r'\n<!-- beginner-r04m:start [^>]+-->.*?<!-- beginner-r04m:end [^>]+-->\n', '', text, flags=re.S)
    return unlinked(text)


def section(text, tag):
    return re.search(r'<!-- beginner-r04m:start ' + re.escape(tag) + r' -->(.*?)<!-- beginner-r04m:end ' + re.escape(tag) + r' -->', text, re.S).group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pre-scan', action='store_true')
    args = ap.parse_args()
    files = all_files()
    docs = {p.name: raw(p).decode('utf-8').replace('\r\n', '\n') for p in files if p.parent == BASE and p.suffix == '.md'}
    baseline = load(HERE / 'r04m.baseline.json')['files']
    reference = load(HERE / 'r04k.baseline.json')
    require(len(docs) == 48, '48 root Markdown pages')
    preserved_docs, preserved_other = [], []
    for name, pin in baseline.items():
        p = safe(BASE / name)
        require(p.is_file(), 'baseline file missing: ' + name)
        if not p.is_file():
            continue
        data = raw(p)
        if '/' not in name and name.endswith('.md'):
            prior = restored(data.decode('utf-8').replace('\r\n', '\n'))
            candidates = (prior.encode('utf-8'), prior.replace('\n', '\r\n').encode('utf-8'))
            ok = any(sha(value) == pin for value in candidates)
            require(ok, 'expert text preservation: ' + name)
            if ok:
                preserved_docs.append(name)
        else:
            ok = sha(data) == pin
            require(ok, 'old artifact preservation: ' + name)
            if ok:
                preserved_other.append(name)
    require(len(preserved_docs) == 44 and len(preserved_other) == 56, '100 baseline files preserved')
    register_like = re.compile(r'(?<![A-Za-z0-9_])(?:U?R|U?P|SR)\d{1,3}(?![A-Za-z0-9_])')
    reviewed_project_labels = 0
    for name, text in docs.items():
        additions = '\n'.join(re.findall(r'<!-- beginner-r04m:start [^>]+-->(.*?)<!-- beginner-r04m:end [^>]+-->', text, re.S)) if name in baseline else text
        for line in additions.splitlines():
            candidates = register_like.findall(line)
            if candidates:
                ok = name == 'APPENDIX_beginner_glossary.md' and (('id="g109"' in line and candidates == ['P3']) or ('id="g110"' in line and candidates == ['R0']))
                require(ok, 'unclassified register-like teaching token: ' + name)
                reviewed_project_labels += len(candidates)
    require(reviewed_project_labels == 2, 'two glossary project labels reviewed as non-register names')
    coverage = qa['coverage'](docs)
    require(coverage == Counter(reference['coverage']), 'coverage comments preserved')
    launches, kernels = Counter(), set()
    for item, count in coverage.items():
        row = json.loads(item)
        launches.update({i: count for i in row['launches']})
        kernels.update(row['kernels'])
    require(launches == Counter(range(158)) and len(kernels) == 44, '158 launches exactly once and 44 kernel names')
    inline = Counter(qa['code_signature'](c) for t in docs.values() for _, c in qa['blocks'](t))
    require(inline == Counter(reference['inline_ast']), 'seven old arithmetic blocks unchanged')
    ids = {name: qa['anchors'](text) for name, text in docs.items()}
    graph = {name: set() for name in docs}
    links = 0
    for name, text in docs.items():
        visible, fence = qa['without_fences'](text)
        require(fence is None, 'unclosed fence: ' + name)
        explicit = re.findall(r'<a id="([^"]+)"', text)
        require(len(explicit) == len(set(explicit)), 'duplicate anchor: ' + name)
        require(text.endswith('\n') and all(line.rstrip() == line for line in text.splitlines()), 'text whitespace: ' + name)
        starts = re.findall(r'<!-- beginner-r04m:start ([^>]+) -->', text)
        ends = re.findall(r'<!-- beginner-r04m:end ([^>]+) -->', text)
        require(starts == ends, 'insertion markers: ' + name)
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
    require(reached == set(docs), 'all pages reachable from frame page')
    layers = load(HERE / 'r04m.layers.json')
    require(len(set(layers['beginner_pages'])) == 21, '21 beginner page introductions')
    for name in layers['beginner_pages']:
        require('<!-- beginner-r04m:start ' in docs[name] and docs[name].index('<!-- beginner-r04m:start ') < 180, 'top introduction: ' + name)
    require(len(set(layers['banner_pages'])) == 18, '18 expert banner pages')
    for name in layers['banner_pages']:
        require('新手可跳过；需要时再读' in section(docs[name], 'expert'), 'expert banner: ' + name)
    workspace_parts = ['write-sets', 'padding', 'address-maps', 'release-contract-r04l', 'wr']
    for part in workspace_parts:
        require('新手可跳过；需要时再读' in section(docs['L3_workspace_map.md'], 'expert-' + part), 'workspace banner: ' + part)
    caption_pages = ['INDEX.md', 'L0_frame.md'] + [name for name in layers['beginner_pages'] if re.match(r'L1_\d', name)]
    for name in caption_pages:
        tag = 'entry' if name == 'INDEX.md' else 'frame' if name == 'L0_frame.md' else 'stage'
        caption = unlinked(section(docs[name], tag))
        require(all(term in caption for term in ('阅读深度', '执行编号', '逻辑块')) and caption.count('<br>') >= 2, 'three-line caption: ' + name)
    role = re.search(r'~~~mermaid\n(.*?)\n~~~', section(docs['L0_frame.md'], 'frame'), re.S).group(1)
    require(all(role.count(char) == 1 for char in '①②③④⑤⑥'), 'six numbered internal skips')
    require('原图备份：另一路，不计六条内部旁路' in role and '仍为输入的宽×高' in role and role.count('？') >= 3, 'role diagram backup, same size and unknown spatial operators')
    require(not re.search(r'launch|0x|\bL\d|\bB\d|F16|F32|E4M3', role), 'role diagram has no execution IDs, formats or offsets')
    primer = docs['L1_00_one_block_primer.md']
    require('linkStyle 2,3 stroke:#aa2222' in primer and 'linkStyle 11,12 stroke:#2255aa' in primer, 'two residual edge colours')
    review_path = BASE.parent / 'reviews' / 'REVIEW_NOVICE_R5_codex_20261027.md'
    review = raw(review_path).decode('utf-8')
    resolution = load(HERE / 'r04m.review_resolution.json')
    require(resolution['review_sha256'] == sha(raw(review_path)), 'novice review identity')
    require([row['rank'] for row in resolution['lost_rows']] == list(range(1, 26)), '25 ranked lost rows')
    review_lost = review[review.index('## 3.'):review.index('## 4.')]
    reviewed_terms = {int(line.split('|')[1].strip().split('；')[0]): line.split('|')[2].strip() for line in review_lost.splitlines() if re.match(r'^\| \d+；', line)}
    require(all(reviewed_terms[row['rank']] == row['review_term'] for row in resolution['lost_rows']), 'lost-row labels match review')
    for row in resolution['lost_rows'] + resolution['top_five']:
        page, _, fragment = row['evidence'].partition('#')
        require(page in docs and (not fragment or fragment in ids[page]), 'review response target: ' + row['evidence'])
    jargon = load(HERE / 'r04m.jargon.json')
    review_terms = review[review.index('## 4.'):review.index('## 5.')]
    titles = [line.split('|')[1].strip() for line in review_terms.splitlines() if line.startswith('|') and not line.startswith('|---') and line.split('|')[1].strip() != '术语或写法']
    require(titles == [g['title'] for g in jargon['groups']] and len(titles) == 111, 'all 111 review term groups in order')
    used = {row['group'] for page in jargon['pages'] for row in page['first_uses']}
    require(used == {f'g{i:03}' for i in range(1, 112)}, 'all 111 groups linked')
    linker = runpy.run_path(str(HERE / 'link_glossary_r04m.py'))
    aliases = {a for group in jargon['groups'] for a in group['aliases']}
    for page in jargon['pages']:
        current = docs[page['page']]
        clean = re.sub(r'\[([^\[\]\n]*)\]\(APPENDIX_beginner_glossary.md#g\d{3}\)', lambda m: m.group(1) if m.group(1) in aliases else m.group(), current)
        linked, hits = linker['annotate'](clean, jargon['groups'])
        require(linked == current and hits == page['first_uses'], 'first-use links current: ' + page['page'])
    examples = load(HERE / 'r04m.beginner_examples.json')
    render = load(HERE / 'r04m.render.json')
    require(examples['status'] == render['status'] == 'PASS', 'saved teaching example and render receipts')
    require(examples['scores'] == [-1, 0, 1] and examples['contents'] == [2, 4, 8], 'synthetic example inputs')
    illustrations = []
    for row in render['rows']:
        svg, png = raw(HERE / row['source']), raw(HERE / row['png'])
        require(sha(svg) == row['source_sha256'] == examples['svg_sha256'][row['source']], 'teaching SVG identity: ' + row['source'])
        require(sha(png) == row['png_sha256'], 'render identity: ' + row['png'])
        root = ET.fromstring(svg)
        words = ''.join(root.itertext())
        require('人工' in words and ('非画面测量' in words or '不是网络前后画面' in words), 'teaching label: ' + row['source'])
        require(not any(node.tag.rsplit('}', 1)[-1] in ('image', 'script', 'foreignObject') for node in root.iter()), 'no source raster or executable content in SVG')
        require(png[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10)), 'PNG signature')
        dims = struct.unpack('>II', png[16:24])
        require(dims == (int(root.attrib['width']), int(root.attrib['height'])), 'PNG matches SVG dimensions')
        illustrations.append(dict(svg=row['source'], png=row['png'], width=dims[0], height=dims[1], labelled_synthetic=True))
    require(len(illustrations) == 2, 'two completed illustration pairs')
    source = ast.parse(raw(HERE / 'beginner_r04m.py').decode('utf-8'))
    imports = {node.module if isinstance(node, ast.ImportFrom) else alias.name for node in ast.walk(source) if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    require(imports <= {'pathlib', 'fractions', 'hashlib', 'json', 'math', 'struct'}, 'teaching generator uses only standard scalar/SVG modules')
    for p in files:
        data = raw(p)
        require(not any(word.encode('utf-8') in data for word in old['OLD_WORDS']), 'avoided word: ' + p.name)
    scan_path = HERE / 'r04m.leak.json'
    scan = load(scan_path)['summary'] if scan_path.exists() else None
    if not args.pre_scan:
        require(scan is not None and scan['PASS'] and scan['files_with_block'] == scan['files_with_name_violation'] == scan['missing'] == 0, 'official publication scan')
        require(scan is not None and scan['files'] == len(files), 'official scan file count current')
        require(scan is not None and 'word_pc' not in scan['files_per_pattern'], 'no program-counter tokens')
    result = dict(status='PASS' if not ERRORS else 'FAIL', mode='pre-scan' if args.pre_scan else 'final',
                  markdown_pages=len(docs), reachable_pages=len(reached), local_links_checked=links,
                  coverage_comments=sum(coverage.values()), launches_exactly_once=len(launches), unique_kernel_names=len(kernels),
                  preserved_expert_pages=len(preserved_docs), preserved_old_other_files=len(preserved_other), inline_arithmetic_blocks=sum(inline.values()),
                  top_five_responses=len(resolution['top_five']), lost_rows=len(resolution['lost_rows']), jargon_groups=len(titles),
                  first_use_links=sum(len(p['first_uses']) for p in jargon['pages']), beginner_page_introductions=len(layers['beginner_pages']),
                  expert_banner_pages=layers['banner_pages'], workspace_expert_sections=workspace_parts,
                  avoided_word_hits=0 if not any('avoided word:' in error for error in ERRORS) else None,
                  red_line=dict(new_hardware_register_names=0, reviewed_project_label_tokens=reviewed_project_labels,
                                new_program_counter_values=0, new_model_coefficient_values=0,
                                instruction_forms='checked by official scanner', ambiguous_hex='format bits, masks and parameter byte locations'),
                  illustrations=illustrations, visual_review='Completed during initial local rendering; render hashes unchanged',
                  teaching_source_review='Synthetic scalar inputs and colour chips; formula constants are not model coefficients; no activation/image imports',
                  new_GPU_runs=0, new_model_runs=0, new_chain_runs=0, new_compile_runs=0, network_calls=0, remote_calls=0, version_control_calls=0,
                  novice_acceptance_retest='NOT_RUN', mermaid_render='NOT_RUN; local fence and role structure checks only',
                  files_in_tree=len(files), official_scan=scan,
                  document_sha256={name: sha(raw(BASE / name)) for name in docs},
                  review_resolution_sha256=sha(raw(HERE / 'r04m.review_resolution.json')), errors=ERRORS)
    (HERE / 'r04m.validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('document_sha256', 'official_scan', 'expert_banner_pages')}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))


if __name__ == '__main__':
    main()
