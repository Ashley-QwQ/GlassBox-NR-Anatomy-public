"""Verify r04h documentation without rereading unrelated experiment sources.

Old external anchors retain their r04g verification; every target still exists.
New anchors are read only from the declared r04h reports/diagnostics/R2 source.
This runs no scalar example, model, GPU, network chain or SFU sweep.
"""
from pathlib import Path
from collections import Counter,deque
from urllib.parse import unquote,urlsplit
import argparse,hashlib,json,os,re,runpy,subprocess

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
OUT=HERE/"r04h.validation.json"
GUARD="".join(map(chr,(98,108,105,110,100)))
OLD_WORDS=("fat"+"bin",chr(0x76f2)+chr(0x76ee))
ERRORS=[]

def require(ok,message):
    if not ok:ERRORS.append(message)
def read(path):
    p=Path(path)
    if any(GUARD in s.lower() for s in p.parts):
        raise ValueError("guarded path refused")
    return p.read_bytes()
def digest(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(read(path))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--pre-scan",action="store_true")
    args=ap.parse_args()
    qa=runpy.run_path(str(HERE/"verify_r04g.py"))
    baseline=load(HERE/"r04h.baseline.json")
    projection=load(HERE/"param_change_r04h.evidence.json")
    scalar=load(HERE/"param_change_r04h.result.json")
    allowed={Path(p).resolve() for obj in (projection,scalar)
             for p in obj["source_sha256"]}
    source_checks=0
    for obj in (projection,scalar):
        for path,expected in obj["source_sha256"].items():
            require(digest(read(path))==expected,"source identity mismatch: "+path)
            source_checks+=1
    require(scalar["status"]=="PASS","R2 scalar example failed")
    require([r["feature_10_15_half"] for r in scalar["rows"]]==[
        ["3800","3400","3c00","4000","4000","0000"],
        ["3800","3400","3c00","3c00","4000","0000"]],"R2 scalar result changed")
    require(len(scalar["guard_refusals"])==3,"R2 guard examples missing")
    d1=projection["stage_D1"]
    require(d1["FULL_MATCH"]+d1["FULL_NOT_OBSERVED"]==d1["calls"]==3476,
            "D1 call census")
    require((d1["FULL_MATCH"],d1["FULL_NOT_OBSERVED"],d1["FINAL_MATCH"],
             d1["distinct_logical_frames"],d1["DIFF"])==(473,3003,22,19,0),
            "D1 observed/unobserved/frame census")
    require(len(projection["S157_new_control_tuples"])==15,"tuple count")
    lane=ROOT/"experiments/parity-cpp-param-change-r01-20261024-codex"
    census=load(lane/"stage_d1b_r2c/REACH_CENSUS.json")
    expected_tuples=[dict(index=r["tuple_index"],
        u32=[f"{n:08x}" for n in r["u32"]],floats=r["floats"]) for r in census["rows"]]
    require(projection["S157_new_control_tuples"]==expected_tuples,
            "control tuple projection differs from accepted census")
    require(projection["SFU_union_blocks"]==census["union_blocks"],
            "SFU union projection differs from accepted census")
    docs={p.name:read(p).decode("utf-8") for p in sorted(BASE.glob("*.md"))}
    require(len(docs)==39,"expected 39 Markdown pages")
    for path,expected in baseline["files"].items():
        if not path.endswith(".md"):
            require(digest(read(BASE/path))==expected,"prior artifact changed: "+path)
    changed=[name for name in docs if digest(read(BASE/name))!=baseline["files"][name]]
    expected_changed={
        "INDEX.md","L0_frame.md","L1_02_input_b0.md","L1_10_output.md",
        "L2_02_b0.md","L2_10_output.md","L3_b0_input.md",
        "L3_b70_history_output.md","L3_ffn.md","L4_mufu.md","APPENDIX_evidence_history.md"}
    require(set(changed)==expected_changed,"unexpected changed Markdown set")
    cov=qa["coverage"](docs)
    require(cov==Counter(baseline["coverage_comments"]),"coverage comments changed")
    launches=Counter();kernels=set()
    for value,n in cov.items():
        c=json.loads(value);launches.update({i:n for i in c["launches"]})
        kernels.update(c["kernels"])
    require(launches==Counter(range(158)),"158/158 exactly-once coverage")
    signatures=Counter(qa["code_signature"](c)
        for text in docs.values() for _,c in qa["blocks"](text))
    require(signatures==Counter(baseline["inline_ast"]),"old inline arithmetic changed")
    for name,text in docs.items():
        visible,fence=qa["without_fences"](text)
        require(fence is None,"unclosed fence: "+name)
        for table in re.findall(r"(?m)(?:^\|.*\n?)+",visible):
            arities=[len(re.split(r"(?<!\\)\|",line)) for line in table.splitlines()]
            require(len(set(arities))==1,"table arity: "+name)
    require(len(docs["L2_02_b0.md"].splitlines())<=45,"B0 L2 too long")
    ids={name:qa["anchors"](text) for name,text in docs.items()}
    old_links={tuple(row) for row in baseline["links"]}
    graph={name:set() for name in docs}
    links=0;new_external_anchors=0;retained_external_anchors=0
    for name,text in docs.items():
        visible,_=qa["without_fences"](text)
        for dest in re.findall(r"\]\(([^)\n]+)\)",visible):
            dest=dest.strip()
            if dest.startswith("<"):dest=dest[1:dest.index(">")]
            else:dest=dest.split(' "',1)[0]
            u=urlsplit(dest)
            if u.scheme in ("http","https","mailto","plugin"):continue
            fragment=unquote(u.fragment);filename=unquote(u.path)
            if re.match(r"^[A-Za-z]:[/\\]",dest):
                filename=unquote(dest.split("#",1)[0])
            elif u.scheme=="file":filename=filename.lstrip("/")
            target=(BASE/name if not filename else Path(filename)
                    if re.match(r"^[A-Za-z]:",filename) else BASE/filename).resolve()
            if any(GUARD in part.lower() for part in target.parts):
                raise ValueError("guarded link target refused")
            links+=1;require(target.exists(),"missing link "+name+": "+dest)
            if not target.is_file():continue
            internal=target.parent==BASE and target.name in docs
            if internal:graph[name].add(target.name)
            if not fragment:continue
            if not internal and (name,dest) in old_links:
                retained_external_anchors+=1
                continue
            if not internal:
                require(target.is_relative_to(BASE) or target in allowed,
                        "new anchor outside declared sources: "+dest)
                if not target.is_relative_to(BASE) and target not in allowed:continue
                new_external_anchors+=1
            if re.fullmatch(r"L\d+(?:-L?\d+)?",fragment):
                values=list(map(int,re.findall(r"\d+",fragment)))
                require(all(1<=i<=len(read(target).splitlines()) for i in values),
                        "line anchor "+name+": "+dest)
            elif target.suffix==".md":
                target_ids=ids[target.name] if internal else qa["anchors"](read(target).decode("utf-8-sig"))
                require(fragment in target_ids,"heading anchor "+name+": "+dest)
    reached=set();queue=deque(["L0_frame.md"])
    while queue:
        name=queue.popleft()
        if name not in reached:reached.add(name);queue.extend(graph[name]-reached)
    require(reached==set(docs),"unreachable pages: "+str(set(docs)-reached))
    # Verify the newly copied seal strings against the accepted reports.
    lane=ROOT/"experiments/parity-cpp-param-change-r01-20261024-codex"
    reports=(read(lane/"STAGE_D1_ZH.md")+read(lane/"STAGE_B_ZH.md")).decode("utf-8")
    new_appendix=docs["APPENDIX_evidence_history.md"].split('<a id="param-change-r04h">')[1]
    for seal in re.findall(r"(?<![0-9a-f])[0-9a-f]{60,70}(?![0-9a-f])",new_appendix):
        require(len(seal)==64 and seal in reports,"copied seal mismatch")
    for row in expected_tuples:
        require("| "+str(row["index"])+" | "+" ".join(row["u32"])+" |" in new_appendix,
                "exact control tuple missing from appendix")
    file_count=0
    for root,dirs,files in os.walk(BASE):
        dirs[:]=sorted(d for d in dirs if GUARD not in d.lower())
        for name in sorted(files):
            if GUARD in name.lower():
                require(False,"guarded filename skipped");continue
            p=Path(root)/name
            if p.suffix not in (".md",".py",".json"):continue
            text=read(p).decode("utf-8")
            require(not any(w in text for w in OLD_WORDS),"protected old wording: "+p.name)
            file_count+=1
    diff=subprocess.run(["git","diff","--check","--","docs/anatomy/skewer"],
                        cwd=ROOT,text=True,capture_output=True)
    require(diff.returncode==0,"git diff --check: "+diff.stdout+diff.stderr)
    scan_path=HERE/"r04h.leak.json"
    scan=load(scan_path)["summary"] if scan_path.exists() else None
    if not args.pre_scan:
        require(scan is not None and scan["PASS"] and scan["files_with_block"]==0
                and scan["files_with_name_violation"]==0 and scan["missing"]==0,
                "leak scan not passing")
    result=dict(status="PASS" if not ERRORS else "FAIL",
        scope="r04h document/source-identity QA; no model/GPU/chain/SFU sweep",
        markdown_pages=len(docs),changed_markdown=sorted(changed),
        local_links_checked=links,reachable_pages=len(reached),
        new_external_anchors_checked=new_external_anchors,
        unchanged_external_anchors_retained_from_r04g=retained_external_anchors,
        coverage_comments=sum(cov.values()),launches_exactly_once=len(launches),
        unique_kernel_names=len(kernels),old_inline_examples_unchanged=sum(signatures.values()),
        old_examples_rerun_in_r04h=False,R2_scalar_example="2 cases PASS; 3 guard refusals",
        source_identities_checked=source_checks,publish_text_files_checked=file_count,
        b0_l2_lines=len(docs["L2_02_b0.md"].splitlines()),
        baseline_sha256=digest(read(HERE/"r04h.baseline.json")),
        document_sha256={name:digest(read(BASE/name)) for name in docs},
        new_artifact_sha256={name:digest(read(HERE/name)) for name in
            ("param_change_r04h.py","param_change_r04h.result.json",
             "param_change_r04h.evidence.json","verify_r04h.py")},
        leak_scan=scan,git_diff_check_exit=diff.returncode,errors=ERRORS)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({k:v for k,v in result.items() if k not in
        ("document_sha256","new_artifact_sha256","leak_scan")},ensure_ascii=False,indent=2))
    raise SystemExit(bool(ERRORS))

if __name__=="__main__":main()
