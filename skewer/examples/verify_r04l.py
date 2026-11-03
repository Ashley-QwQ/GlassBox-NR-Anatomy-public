"""Offline document, classification and publication checks; no version control."""
from pathlib import Path
from collections import Counter, deque
from urllib.parse import unquote, urlsplit
import argparse
import hashlib
import json
import re
import runpy

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
old=runpy.run_path(str(HERE/'verify_r04k.py'))
qa=runpy.run_path(str(HERE/'verify_r04g.py'))
safe,raw,sha,load,all_files=(old[k] for k in ('safe','raw','sha','load','all_files'))
ERRORS=[]

def require(ok,message):
    if not ok: ERRORS.append(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pre-scan',action='store_true');args=ap.parse_args()
    files=all_files();docs={p.name:raw(p).decode('utf-8') for p in files if p.parent==BASE and p.suffix=='.md'}
    baseline=load(HERE/'r04l.baseline.json')
    reference=load(HERE/'r04k.baseline.json')
    require(len(docs)==44,'44 pages')
    changed=[]
    for name,pin in baseline['files'].items():
        data=raw(BASE/name)
        if sha(data)!=pin:
            changed.append(name)
            require('/' not in name and name.endswith('.md'),'prior non-document artifact changed: '+name)
    coverage=qa['coverage'](docs)
    require(coverage==Counter(reference['coverage']),'coverage comments preserved')
    launches,kernels=Counter(),set()
    for item,count in coverage.items():
        row=json.loads(item);launches.update({i:count for i in row['launches']});kernels.update(row['kernels'])
    require(launches==Counter(range(158)) and len(kernels)==44,'158 launches and 44 kernels')
    inline=Counter(qa['code_signature'](c) for t in docs.values() for _,c in qa['blocks'](t))
    require(inline==Counter(reference['inline_ast']),'seven old Python blocks unchanged')
    ids={n:qa['anchors'](t) for n,t in docs.items()}
    graph={n:set() for n in docs};links=0;sources={}
    for name,t in docs.items():
        visible,fence=qa['without_fences'](t)
        require(fence is None,'unclosed fence: '+name)
        explicit=re.findall(r'<a id="([^"]+)"',t)
        require(len(explicit)==len(set(explicit)),'duplicate anchor: '+name)
        require(t.endswith('\n'),'newline: '+name)
        require(all(s.rstrip()==s for s in t.splitlines()),'whitespace: '+name)
        for table in re.findall(r'(?m)(?:^\|.*\n?)+',visible):
            require(len({len(re.split(r'(?<!\\)\|',s)) for s in table.splitlines()})==1,'table arity: '+name)
        for dest in re.findall(r'\]\(([^)\n]+)\)',visible):
            dest=dest.strip();dest=dest[1:dest.index('>')] if dest.startswith('<') else dest.split(' "',1)[0]
            u=urlsplit(dest)
            if u.scheme in ('http','https','mailto','plugin'):continue
            filename,fragment=unquote(u.path),unquote(u.fragment)
            if re.match(r'^[A-Za-z]:[/\\]',dest):filename=unquote(dest.split('#',1)[0])
            target=safe(BASE/name if not filename else Path(filename) if re.match(r'^[A-Za-z]:',filename) else BASE/filename)
            links+=1;require(target.exists(),'missing link '+name+': '+dest)
            if not target.is_file():continue
            internal=target.parent==BASE and target.name in docs
            if internal:graph[name].add(target.name)
            if name in changed and not target.is_relative_to(BASE) and target.suffix in ('.cpp','.hpp','.inc','.py','.json'):
                sources[str(target)]=sha(raw(target))
            if re.fullmatch(r'L\d+(?:-L?\d+)?',fragment):
                require(all(1<=int(i)<=len(raw(target).splitlines()) for i in re.findall(r'\d+',fragment)),'line anchor '+name+': '+dest)
            elif fragment and target.suffix=='.md':
                anchors=ids[target.name] if internal else qa['anchors'](raw(target).decode('utf-8-sig'))
                require(fragment in anchors,'heading '+name+': '+dest)
    reached=set();q=deque(['L0_frame.md'])
    while q:
        n=q.popleft()
        if n not in reached:reached.add(n);q.extend(graph[n]-reached)
    require(reached==set(docs),'all pages reachable')
    classification=runpy.run_path(str(HERE/'classify_r04l.py'))['classification']()
    require(classification==load(HERE/'r04l.classification.json'),'classification receipt current')
    C,T,P,M,U=(runpy.run_path(str(HERE/'classify_r04l.py'))[k] for k in ('C','T','P','M','U'))
    require(classification['default_current']=={C:1706,T:112,P:0,M:0,U:6},'default classification')
    require(classification['family_current']=={C:4,T:34,P:0,M:0,U:6},'family classification')
    require(classification['variant_current']=={C:18,T:1,P:0,M:0,U:3},'variant classification')
    for row in classification['worklist']:
        if row['evidence']:
            page,anchor=row['evidence'].split('#');require(anchor in ids[page],'classification evidence '+row['id'])
    audit=(HERE.parents[1]/'reviews/FORMULA_COVERAGE_R1_codex_20261027.md')
    require(sha(raw(audit))==classification['audit_sha256'],'audit unchanged')
    aliases={
        'PUB':Path('E:/GlassBox-NR'),
        'EXT61':Path('F:/dlssnr-work/vit-t640-numeric-r07-codex/maps/t640'),
        'R1':HERE.parents[3]/'experiments/parity-cpp-param-change-r01-20261024-codex/stage_c_r1/handoff-resume5/candidate',
        'R2':HERE.parents[3]/'experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1_r2/returned/snapshot/candidate',
        'R2b':HERE.parents[3]/'experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1a_r2b/returned/snapshot/candidate',
        'R2c':HERE.parents[3]/'experiments/parity-cpp-param-change-r01-20261024-codex/stage_d1b_r2c/returned/snapshot/candidate',
    }
    pins=0
    for label,pin in re.findall(r'^\| `((?:PUB|EXT61|R1|R2|R2b|R2c)/[^`]+)` \| \d+ \| `([0-9a-f]{64})` \|',raw(audit).decode('utf-8'),re.M):
        alias,rel=label.split('/',1);p=safe(aliases[alias]/rel)
        # Stop immediately on first mismatch; never rewrite source evidence.
        actual=sha(raw(p))
        if actual!=pin:raise RuntimeError('audit source identity mismatch: '+label)
        pins+=1
    require(pins==38,'38 audited source/map identities')
    formula=load(HERE/'r04l.formulas.json');require(formula['status']=='PASS','formula examples')
    for p in files:
        if p.suffix in ('.md','.py','.json'):
            text=raw(p).decode('utf-8')
            require(not any(w in text for w in old['OLD_WORDS']),'protected word: '+p.name)
    scan_path=HERE/'r04l.leak.json';scan=load(scan_path).get('summary') if scan_path.exists() else None
    if not args.pre_scan:
        require(scan is not None and scan['PASS'] and scan['files_with_block']==0 and scan['files_with_name_violation']==0 and scan['missing']==0,'official scan')
        require(scan is not None and scan['files']==len(files),'scan file count current')
    result=dict(status='PASS' if not ERRORS else 'FAIL',markdown_pages=len(docs),reachable_pages=len(reached),local_links_checked=links,
                coverage_comments=sum(coverage.values()),launches_exactly_once=len(launches),unique_kernel_names=len(kernels),
                inline_arithmetic_blocks=sum(inline.values()),old_non_document_artifacts_preserved=True,
                audited_source_pins=pins,changed_pages=changed,classification={k:classification[k] for k in ('default_baseline','default_current','variant_current','family_current')},
                files_in_tree=len(files),new_GPU_runs=0,new_model_runs=0,new_chain_runs=0,new_compile_runs=0,network_calls=0,remote_calls=0,version_control_calls=0,
                source_sha256=sources,document_sha256={n:sha(raw(BASE/n)) for n in docs},official_scan=scan,errors=ERRORS)
    (HERE/'r04l.validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('document_sha256','source_sha256','official_scan')},ensure_ascii=False,indent=2))
    raise SystemExit(bool(ERRORS))

if __name__=='__main__':main()
