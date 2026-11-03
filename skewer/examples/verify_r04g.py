"""Document/scalar QA only; the JSON receipt is the only write.

Initial use: --baseline examples/r04g_work/baseline.json (relative to skewer).
Later use reuses the saved baseline signatures in r04g.validation.json.
"""
from pathlib import Path
from collections import Counter, deque
import argparse, ast, hashlib, json, os, re, subprocess, sys, unicodedata
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
OUT = HERE / "r04g.validation.json"
GUARD = "".join(map(chr, (98, 108, 105, 110, 100)))
OLD_WORDS = ("fat" + "bin", chr(0x76f2) + chr(0x76ee))
ERRORS = []

def require(ok, message):
    if not ok:
        ERRORS.append(message)

def safe(p):
    p = Path(p)
    if any(GUARD in part.lower() for part in p.parts):
        raise ValueError("guarded path refused")
    return p

def raw(p):
    return safe(p).read_bytes()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blocks(text):
    return re.findall(r"(?ms)^([\x60~]{3})python[^\n]*\n(.*?)^\1\s*$", text)

class Canonical(ast.NodeTransformer):
    def __init__(self, aliases):
        self.aliases = aliases
    def visit_Name(self, node):
        node.id = self.aliases.get(node.id, node.id)
        return node
    def visit_FunctionDef(self, node):
        node.name = self.aliases.get(node.name, node.name)
        return self.generic_visit(node)

def code_signature(code):
    aliases = {}
    if re.search(r"def (?:E|Q8)\(", code):
        aliases.update(E="Q8", H="RN16", F="RN32", B="bits16",
                       U="decode16", A="H_add")
    if re.search(r"def (?:P|Hash32)\(", code):
        aliases["P"] = "Hash32"
    tree = Canonical(aliases).visit(ast.parse(code))
    return sha(ast.dump(tree, include_attributes=False).encode("utf-8"))

def coverage(texts):
    return Counter(json.dumps(json.loads(m), sort_keys=True, ensure_ascii=False)
                   for text in texts.values()
                   for m in re.findall(r"<!--\s*coverage:\s*(.*?)\s*-->", text))

def without_fences(text):
    result, fence = [], None
    for line in text.splitlines():
        m = re.match(r"\s*([\x60~]{3,})", line)
        if m:
            if fence is None:
                fence = m[1][0]
            elif m[1][0] == fence:
                fence = None
            result.append("")
        else:
            result.append("" if fence else line)
    return "\n".join(result), fence

def anchors(text):
    ids = set(re.findall(r'<a\s+id="([^"]+)"', text))
    seen = Counter()
    visible, _ = without_fences(text)
    for line in visible.splitlines():
        m = re.match(r"#{1,6}\s+(.+?)\s*#*$", line)
        if not m:
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", m[1])
        title = re.sub(r"<[^>]+>", "", title).replace(chr(96), "").lower()
        title = "".join(c for c in title
                        if unicodedata.category(c)[0] in "LNM"
                        or c in "_- ")
        slug = title.replace(" ", "-")
        n = seen[slug]
        seen[slug] += 1
        ids.add(slug + (f"-{n}" if n else ""))
    return ids

def run_inline(texts):
    results = []
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for key in ("TEMP", "TMP", "TMPDIR"):
        env[key] = str(HERE)
    for name, text in sorted(texts.items()):
        for i, (_, code) in enumerate(blocks(text)):
            r = subprocess.run([sys.executable, "-B", "-X", "utf8", "-c", code],
                               cwd=ROOT, env=env, text=True, encoding="utf-8",
                               capture_output=True, timeout=120)
            results.append(dict(file=name, block=i, exit_code=r.returncode,
                                code_sha256=sha(code.encode("utf-8")),
                                stdout_sha256=sha(r.stdout.encode("utf-8")),
                                stdout_tokens=[line.split() for line in r.stdout.splitlines()],
                                stderr=r.stderr))
            require(r.returncode == 0, f"inline failed: {name} block {i}: {r.stderr[-500:]}")
    require(len(results) == 8, "expected eight inline Python examples")
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline")
    args = parser.parse_args()
    docs = {p.name: raw(p).decode("utf-8") for p in sorted(BASE.glob("*.md"))}
    require(len(docs) == 39, "expected 39 Markdown pages")
    current_coverage = coverage(docs)
    current_signatures = Counter(code_signature(code)
                                 for t in docs.values() for _, code in blocks(t))
    if args.baseline:
        baseline = json.loads(raw(BASE / args.baseline))
        old_docs = {k: v["text"] for k, v in baseline.items() if k.endswith(".md")}
        old_coverage = coverage(old_docs)
        old_signatures = Counter(code_signature(code)
                                 for t in old_docs.values() for _, code in blocks(t))
        baseline_info = dict(
            sha256=sha(raw(BASE / args.baseline)),
            files={k: v["sha256"] for k, v in baseline.items()},
            coverage_comments=dict(old_coverage),
            inline_canonical_ast=dict(old_signatures))
    else:
        baseline_info = json.loads(raw(OUT))["baseline"]
        old_coverage = Counter(baseline_info["coverage_comments"])
        old_signatures = Counter(baseline_info["inline_canonical_ast"])
    require(current_coverage == old_coverage, "coverage comments changed")
    require(current_signatures == old_signatures, "inline arithmetic AST changed")
    launches, kernels = Counter(), set()
    for item, n in current_coverage.items():
        item = json.loads(item)
        launches.update({i: n for i in item["launches"]})
        kernels.update(item["kernels"])
    require(launches == Counter(range(158)), "launch coverage must be exactly 0..157 once")
    require(len(kernels) == 44 and sum(current_coverage.values()) == 41,
            "kernel/comment census changed")

    local_rows = {}
    table_pages = ("L3_attention_softmax.md", "L3_b0_input.md",
                   "L3_norm_nonfinite.md", "L3_workspace_map.md",
                   "L3_b70_history_output.md", "L3_qmma_e4m3.md",
                   "L4_mufu.md", "L4_half_arith.md", "L4_e4m3_and_k32.md")
    for name in table_pages:
        lines = docs[name].splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith("|"))
        count = 0
        for line in lines[start:]:
            if not line.startswith("|"):
                break
            count += 1
        local_rows[name] = count - 2
        require(3 <= count - 2 <= 5, f"local notation rows: {name} {count-2}")
    require(len(docs["L2_02_b0.md"].splitlines()) <= 45, "B0 L2 exceeds 45 lines")
    for name, text in docs.items():
        visible, fence = without_fences(text)
        require(fence is None, f"unclosed fence {name}")
        for line_no, line in enumerate(visible.splitlines(), 1):
            require(not any(w in line for w in ("Q₈", "D₈", "Q_8", "D_8")),
                    f"old notation {name}:{line_no}")
        for table in re.findall(r"(?m)(?:^\|.*\n?)+", visible):
            arities = [len(re.split(r"(?<!\\)\|", line)) for line in table.splitlines()]
            require(len(set(arities)) == 1, f"table arity {name}: {arities}")
        if name.startswith("L1_"):
            require("动机未知" not in text and "架构动机" not in text,
                    f"repeated motive note {name}")

    ids = {name: anchors(t) for name, t in docs.items()}
    graph = {name: set() for name in docs}
    link_count = 0
    for name, text in docs.items():
        visible, _ = without_fences(text)
        for dest in re.findall(r"\]\(([^)\n]+)\)", visible):
            dest = dest.strip()
            if dest.startswith("<"):
                dest = dest[1:dest.index(">")]
            else:
                dest = dest.split(' "', 1)[0]
            u = urlsplit(dest)
            if u.scheme in ("https", "http", "mailto", "plugin"):
                continue
            fragment = unquote(u.fragment)
            filename = unquote(u.path)
            if re.match(r"^[A-Za-z]:[/\\]", dest):
                filename = unquote(dest.split("#", 1)[0])
            if u.scheme == "file":
                filename = filename.lstrip("/")
            if not filename:
                target = BASE / name
            elif re.match(r"^[A-Za-z]:", filename):
                target = Path(filename)
            else:
                target = (BASE / filename).resolve()
            safe(target)
            link_count += 1
            require(target.exists(), f"missing link {name}: {dest}")
            if not target.is_file():
                continue
            if target.parent == BASE and target.name in docs:
                graph[name].add(target.name)
            if fragment:
                if re.fullmatch(r"L\d+(?:-L?\d+)?", fragment):
                    numbers = list(map(int, re.findall(r"\d+", fragment)))
                    require(all(1 <= i <= len(raw(target).splitlines()) for i in numbers),
                            f"line anchor {name}: {dest}")
                elif target.suffix == ".md":
                    target_ids = ids.get(target.name) if target.parent == BASE else anchors(raw(target).decode("utf-8-sig"))
                    require(fragment in target_ids, f"heading anchor {name}: {dest}")
    reached, queue = set(), deque(["L0_frame.md"])
    while queue:
        name = queue.popleft()
        if name not in reached:
            reached.add(name)
            queue.extend(graph[name] - reached)
    require(reached == set(docs), "unreachable Markdown pages: " + str(set(docs) - reached))

    file_count = 0
    for root, directories, files in os.walk(BASE):
        directories[:] = sorted(d for d in directories
                                if GUARD not in d.lower() and d != "r04g_work")
        for filename in sorted(files):
            if GUARD in filename.lower():
                require(False, "guarded filename skipped")
                continue
            path = safe(Path(root) / filename)
            if path.suffix not in (".md", ".py", ".json"):
                continue
            data = raw(path).decode("utf-8")
            require(not any(word in data for word in OLD_WORDS),
                    "protected old wording: " + path.relative_to(BASE).as_posix())
            file_count += 1
    source_checks = 0
    for filename, expected in baseline_info["files"].items():
        if not filename.endswith(".md"):
            require(sha(raw(BASE / filename)) == expected,
                    "pre-existing example changed: " + filename)
    for filename in ("geometry_r04g.result.json", "substitutions_r04g.result.json"):
        receipt = json.loads(raw(HERE / filename))
        require(receipt["status"] == "PASS", "example receipt status " + filename)
        for path, expected in receipt["source_sha256"].items():
            require(sha(raw(path)) == expected, "source identity mismatch " + path)
            source_checks += 1
    inline = run_inline(docs)
    diff = subprocess.run(["git", "diff", "--check", "--", "docs/anatomy/skewer"],
                          cwd=ROOT, text=True, capture_output=True)
    require(diff.returncode == 0, "git diff --check: " + diff.stdout + diff.stderr)
    scan = HERE / "r04g.leak.json"
    scanner = json.loads(raw(scan)) if scan.exists() else None
    require(scanner is not None or args.baseline is not None, "leak scan receipt missing")
    if scanner:
        summary = scanner["summary"]
        require(summary["PASS"] and summary["files_with_block"] == 0
                and summary["files_with_name_violation"] == 0
                and summary["missing"] == 0, "leak scan failed")
    result = dict(
        status="PASS" if not ERRORS else "FAIL",
        scope="document/renamed scalar examples; no GPU, model or full chain",
        markdown_pages=len(docs), local_links_checked=link_count,
        reachable_pages=len(reached), coverage_comments=sum(current_coverage.values()),
        launches_exactly_once=len(launches), unique_kernel_names=len(kernels),
        notation_table_rows=local_rows, b0_l2_lines=len(docs["L2_02_b0.md"].splitlines()),
        publish_text_files_checked=file_count, source_identities_checked=source_checks,
        inline_arithmetic_ast_preserved=current_signatures == old_signatures,
        inline_examples=inline, baseline=baseline_info,
        git_diff_check_exit=diff.returncode,
        leak_scan=scanner["summary"] if scanner else None,
        document_sha256={k: sha(v.encode("utf-8")) for k, v in docs.items()},
        errors=ERRORS)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("baseline", "inline_examples", "document_sha256", "leak_scan")},
                     ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))

if __name__ == "__main__":
    main()
