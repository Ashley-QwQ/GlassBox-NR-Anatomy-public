"""r04i document, source-identity and moved-code QA; no model/GPU runs."""
from pathlib import Path
from collections import Counter,deque
from urllib.parse import unquote,urlsplit
import argparse,hashlib,json,os,re,runpy,subprocess

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
OUT=HERE/"r04i.validation.json"
GUARD="".join(map(chr,(98,108,105,110,100)))
OLD_WORDS=("fat"+"bin",chr(0x76f2)+chr(0x76ee))
ERRORS=[]
def require(ok,message):
    if not ok:ERRORS.append(message)
def raw(path):
    p=Path(path)
    if any(GUARD in s.lower() for s in p.parts):raise ValueError("guarded path refused")
    return p.read_bytes()
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(raw(path))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--pre-scan",action="store_true")
    args=ap.parse_args()
    qa=runpy.run_path(str(HERE/"verify_r04g.py"))
    baseline=load(HERE/"r04i.baseline.json")
    docs={p.name:raw(p).decode("utf-8") for p in sorted(BASE.glob("*.md"))}
    require(len(docs)==39,"39 Markdown pages required")
    for path,expected in baseline["files"].items():
        if not path.endswith(".md"):
            require(sha(raw(BASE/path))==expected,"prior artifact changed: "+path)
    coverage=qa["coverage"](docs)
    require(coverage==Counter(baseline["coverage"]),"coverage comment drift")
    launches=Counter();kernels=set()
    for text,n in coverage.items():
        item=json.loads(text);launches.update({i:n for i in item["launches"]});kernels.update(item["kernels"])
    require(launches==Counter(range(158)),"158/158 exactly once")
    code=Counter(qa["code_signature"](c) for t in docs.values() for _,c in qa["blocks"](t))
    require(sum(code.values())==7,"expected seven remaining appendix Python blocks")
    code.update([qa["code_signature"](raw(HERE/"b70_rz_copy_r04i.py").decode("utf-8"))])
    require(code==Counter(baseline["inline_ast"]),"moved/existing arithmetic AST changed")
    require(not qa["blocks"](docs["L3_b70_history_output.md"]),"B70 Python still inline")
    ids={name:qa["anchors"](text) for name,text in docs.items()}
    for name,text in docs.items():
        explicit=re.findall(r'<a id="([^"]+)">',text)
        require(len(explicit)==len(set(explicit)),"duplicate anchor: "+name)
        visible,fence=qa["without_fences"](text)
        require(fence is None,"unclosed fence: "+name)
        require(not re.search(r"(?m)^(#{1,6} .+)\n\s*\n\1$",text),
                "consecutive duplicate heading: "+name)
        for table in re.findall(r"(?m)(?:^\|.*\n?)+",visible):
            arities=[len(re.split(r"(?<!\\)\|",line)) for line in table.splitlines()]
            require(len(set(arities))==1,"table arity: "+name)
        if name=="INDEX.md" or name.startswith("L"):
            require(not re.search(r"\b(?:Stage B|R[012](?:b|c)?|G[24]|D[123])\b|3003|3,003|1of2|2of2",visible),
                    "parameter QA bookkeeping in main text: "+name)
            require(not re.search(r"param_(?:f32|u32|u64)\[",text),
                    "legacy CB notation: "+name)
            require(not re.search(r"\bQ8\s*(?:job|f0|/S1)",text),
                    "job/quantisation collision: "+name)
    require("param-change" in ids["APPENDIX_evidence_history.md"],"canonical ledger anchor missing")
    require(len(docs["L2_02_b0.md"].splitlines())<=45,"B0 L2 over 45 lines")
    # The duplicated bridge paragraphs must no longer be copied into split16.
    paragraphs={p for p in docs["L2_06_decoder_bridge.md"].split("\n\n") if len(p)>120}
    require(not any(p in docs["L3_split16_window.md"] for p in paragraphs),
            "bridge/split16 duplicate paragraph")
    graph={name:set() for name in docs};links=0
    for name,text in docs.items():
        visible,_=qa["without_fences"](text)
        for dest in re.findall(r"\]\(([^)\n]+)\)",visible):
            dest=dest.strip()
            if dest.startswith("<"):dest=dest[1:dest.index(">")]
            else:dest=dest.split(' "',1)[0]
            u=urlsplit(dest)
            if u.scheme in ("https","http","mailto","plugin"):continue
            fragment=unquote(u.fragment);filename=unquote(u.path)
            if re.match(r"^[A-Za-z]:[/\\]",dest):filename=unquote(dest.split("#",1)[0])
            elif u.scheme=="file":filename=filename.lstrip("/")
            target=(BASE/name if not filename else Path(filename) if re.match(r"^[A-Za-z]:",filename) else BASE/filename).resolve()
            if any(GUARD in part.lower() for part in target.parts):raise ValueError("guarded link refused")
            links+=1;require(target.exists(),"missing link "+name+": "+dest)
            if not target.is_file():continue
            internal=target.parent==BASE and target.name in docs
            if internal:graph[name].add(target.name)
            if fragment:
                if re.fullmatch(r"L\d+(?:-L?\d+)?",fragment):
                    numbers=list(map(int,re.findall(r"\d+",fragment)))
                    require(all(1<=i<=len(raw(target).splitlines()) for i in numbers),
                            "line anchor "+name+": "+dest)
                elif target.suffix==".md":
                    target_ids=ids[target.name] if internal else qa["anchors"](raw(target).decode("utf-8-sig"))
                    require(fragment in target_ids,"heading anchor "+name+": "+dest)
    reached=set();queue=deque(["L0_frame.md"])
    while queue:
        name=queue.popleft()
        if name not in reached:reached.add(name);queue.extend(graph[name]-reached)
    require(reached==set(docs),"unreachable: "+str(set(docs)-reached))
    computed=load(HERE/"anatomy_r04i.result.json");require(computed["status"]=="PASS","real code example status")
    for path,h in computed["source_sha256"].items():require(sha(raw(path))==h,"source identity mismatch: "+path)
    scalar_text=docs["L3_b70_history_output.md"].replace("−","-")
    for tokens in computed["stdout_tokens"]:
        if tokens[0] in ("color","gate","blend"):
            for number in tokens[2:]:
                if len(number)>=7:
                    require(number in scalar_text,"scalar table differs from real output: "+number)
    require(computed["stages"]["TIN_encoder"]==computed["stages"]["TIN_decoder"],
            "symmetric logical TIN budget")
    require(not computed["stages"]["split16_encoder"]["complete"] and
            not computed["stages"]["split16_decoder"]["complete"],"unclosed split16 total promoted")
    for key,row in computed["stages"].items():
        label={"B0":"B0","TIN_encoder":"TIN编码","split16_encoder":"split16编码（已知小计）",
               "ViT":"ViT","L100":"L100","split16_decoder":"split16解码（已知小计）",
               "TIN_decoder":"TIN解码","B70":"B70"}[key]
        linear=f'{row["linear_MAC"]/1e9:.6f}' if "linear_MAC" in row else f'{row["linear_MAC_reset"]/1e9:.6f} / {row["linear_MAC_history"]/1e9:.6f}'
        line=f'| {label} | {row["matrix_bytes"]:,} | {linear} | {row["attention_MAC"]/1e9:.6f} |'
        require(line in docs["L0_frame.md"],"cost table differs from real calculation: "+key)
    file_count=0
    for root,dirs,files in os.walk(BASE):
        dirs[:]=sorted(d for d in dirs if GUARD not in d.lower())
        for filename in sorted(files):
            if GUARD in filename.lower():require(False,"guarded filename skipped");continue
            p=Path(root)/filename
            if p.suffix not in (".md",".py",".json"):continue
            text=raw(p).decode("utf-8")
            require(not any(s in text for s in OLD_WORDS),"protected old wording: "+p.name)
            file_count+=1
    diff=subprocess.run(["git","diff","--check","--","docs/anatomy/skewer"],cwd=ROOT,text=True,capture_output=True)
    require(diff.returncode==0,"git diff --check: "+diff.stdout+diff.stderr)
    scan_path=HERE/"r04i.leak.json";scan=load(scan_path)["summary"] if scan_path.exists() else None
    if not args.pre_scan:
        require(scan is not None and scan["PASS"] and scan["files_with_block"]==0
                and scan["files_with_name_violation"]==0 and scan["missing"]==0,"leak scan failed/missing")
    result=dict(status="PASS" if not ERRORS else "FAIL",
        scope="document/source identity QA; new real scalar examples only, no GPU/model/chain",
        markdown_pages=len(docs),reachable_pages=len(reached),local_links_checked=links,
        coverage_comments=sum(coverage.values()),launches_exactly_once=len(launches),
        unique_kernel_names=len(kernels),arithmetic_AST_preserved_with_moved_example=code==Counter(baseline["inline_ast"]),
        remaining_inline_Python=7,moved_example="b70_rz_copy_r04i.py",
        new_scalar_examples="B70 color/confidence + real swizzle + half sqrt32",
        scalar_table_matches_real_output=True,
        source_identities_checked=len(computed["source_sha256"]),
        complete_network_MAC="NOT_ESTABLISHED; explicit split16 subtotals",
        publish_text_files_checked=file_count,git_diff_check_exit=diff.returncode,
        document_sha256={n:sha(raw(BASE/n)) for n in docs},
        new_artifact_sha256={n:sha(raw(HERE/n)) for n in
            ("anatomy_r04i.py","anatomy_r04i.result.json","b70_rz_copy_r04i.py","verify_r04i.py","r04i.baseline.json")},
        leak_scan=scan,errors=ERRORS)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({k:v for k,v in result.items() if k not in
        ("document_sha256","new_artifact_sha256","leak_scan")},ensure_ascii=False,indent=2))
    raise SystemExit(bool(ERRORS))
if __name__=="__main__":main()
