"""Offline structure checks of the English edition (skewer-en) against the Chinese pages in skewer/.

Reuses the helpers of skewer/examples/verify_r04g.py and verify_r04k.py, so anchors, fences, coverage comments and
inline arithmetic blocks are parsed exactly as the Chinese verifier parses them. Links to the private project
archive (../../../experiments/... and similar) resolve only inside the full project layout; a missing target outside
this repository, or in a top-level folder the repository does not ship (such as ../reviews), is counted as private_archive_links_missing instead of failing, so the check also passes in a public
checkout. A missing target inside the repository is always an error.
Read-only: prints a JSON summary and exits non-zero on any error; writes nothing.
"""
from pathlib import Path
from collections import Counter, deque
from urllib.parse import unquote, urlsplit
import json
import re
import runpy

HERE = Path(__file__).resolve().parent
EN = HERE.parent
ZH = EN.parent / 'skewer'
REPO = EN.parent
qa = runpy.run_path(str(ZH / 'examples' / 'verify_r04g.py'))
old = runpy.run_path(str(ZH / 'examples' / 'verify_r04k.py'))
safe, raw = qa['safe'], qa['raw']
ERRORS = []


def require(ok, message):
    if not ok:
        ERRORS.append(message)


def pages(base):
    return {p.name: raw(p).decode('utf-8').replace('\r\n', '\n') for p in sorted(base.glob('*.md'))}


def signatures(docs):
    return Counter(qa['code_signature'](code) for text in docs.values() for _, code in qa['blocks'](text))


def main():
    zh, en = pages(ZH), pages(EN)
    require(set(en) == set(zh), 'same page names as skewer')
    coverage = qa['coverage'](en)
    require(coverage == qa['coverage'](zh), 'coverage comments identical to skewer')
    launches, kernels = Counter(), set()
    for item, count in coverage.items():
        row = json.loads(item)
        launches.update({i: count for i in row['launches']})
        kernels.update(row['kernels'])
    require(launches == Counter(range(158)) and len(kernels) == 44, '158 launches exactly once and 44 kernel names')
    inline = signatures(en)
    require(inline == signatures(zh), 'inline arithmetic blocks identical to skewer')
    ids = {name: qa['anchors'](text) for name, text in en.items()}
    graph = {name: set() for name in en}
    links = private_missing = 0
    for name, text in en.items():
        data = raw(EN / name)
        require(data.count(b'\n') == data.count(b'\r\n'), 'CRLF: ' + name)
        visible, fence = qa['without_fences'](text)
        require(fence is None, 'unclosed fence: ' + name)
        explicit = re.findall(r'<a id="([^"]+)"', text)
        require(len(explicit) == len(set(explicit)), 'duplicate anchor: ' + name)
        require(explicit == re.findall(r'<a id="([^"]+)"', zh[name]), 'explicit anchors differ from skewer: ' + name)
        require(text.endswith('\n') and all(line.rstrip() == line for line in text.splitlines()), 'whitespace: ' + name)
        for table in re.findall(r'(?m)(?:^\|.*\n?)+', visible):
            require(len({len(re.split(r'(?<!\\)\|', line)) for line in table.splitlines()}) == 1, 'table arity: ' + name)
        require(chr(36) * 2 not in text and chr(92) + 'operatorname' not in text, 'GitHub display math format: ' + name)
        require(not any(word in text for word in old['OLD_WORDS']), 'avoided word: ' + name)
        for dest in re.findall(r'\]\(([^)\n]+)\)', visible):
            dest = dest.strip()
            dest = dest[1:dest.index('>')] if dest.startswith('<') else dest.split(' "', 1)[0]
            u = urlsplit(dest)
            if u.scheme in ('http', 'https', 'mailto', 'plugin'):
                continue
            filename, fragment = unquote(u.path), unquote(u.fragment)
            if re.match(r'^[A-Za-z]:[/\\]', dest):
                filename = unquote(dest.split('#', 1)[0])
            target = safe(EN / name if not filename else Path(filename) if re.match(r'^[A-Za-z]:', filename) else EN / filename)
            links += 1
            if not target.exists():
                resolved, repo = target.resolve(), REPO.resolve()
                if not resolved.is_relative_to(repo) or not (repo / resolved.relative_to(repo).parts[0]).exists():
                    private_missing += 1   # private project archive (outside the repo or in a folder it does not ship)
                    continue
                require(False, 'missing link ' + name + ': ' + dest)
            if not target.is_file():
                continue
            internal = target.parent == EN and target.name in en
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
    require(reached == set(en), 'all pages reachable from L0_frame')
    require(not any(word in raw(Path(__file__)).decode('utf-8') for word in old['OLD_WORDS']), 'avoided word: verify_en.py')
    result = dict(status='PASS' if not ERRORS else 'FAIL', markdown_pages=len(en), reachable_pages=len(reached),
                  local_links_checked=links, private_archive_links_missing=private_missing, coverage_comments=sum(coverage.values()),
                  launches_exactly_once=len(launches), unique_kernel_names=len(kernels),
                  inline_arithmetic_blocks=sum(inline.values()), errors=ERRORS)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))


if __name__ == '__main__':
    main()
