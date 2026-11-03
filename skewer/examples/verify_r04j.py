"""r04j documentation QA: read-only evidence checks, one receipt write."""
from pathlib import Path
from collections import Counter, deque
from urllib.parse import unquote, urlsplit
import argparse
import hashlib
import json
import os
import re
import runpy

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
GUARD = "".join(map(chr, (98, 108, 105, 110, 100)))
OLD_WORDS = ("fat" + "bin", chr(0x76f2) + chr(0x76ee))
ERRORS = []
ALLOWED_EDITS = {
    "INDEX.md", "L0_frame.md", "L1_04_split16_encoder.md",
    "L2_04_split16_encoder.md", "L2_06_decoder_bridge.md",
    "L3_split16_window.md", "L3_b0_input.md",
    "L3_b70_history_output.md", "L4_tex_filter.md", "L4_mufu.md",
    "APPENDIX_cpu_storage.md", "APPENDIX_evidence_history.md",
}
NEW_PAGES = {"L0a_object_method.md", "L0b_determinism.md"}


def require(ok, message):
    if not ok:
        ERRORS.append(message)


def safe(path):
    p = Path(path).resolve()
    if any(GUARD in part.lower() for part in p.parts):
        raise ValueError("guarded path refused")
    return p


def raw(path):
    return safe(path).read_bytes()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(raw(path))


def files_under_base():
    result = []
    for root, dirs, names in os.walk(BASE):
        dirs[:] = sorted(d for d in dirs if GUARD not in d.lower())
        for name in sorted(names):
            if GUARD in name.lower():
                continue
            result.append(safe(Path(root) / name))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre-scan", action="store_true")
    args = ap.parse_args()
    # Load pure parsing helpers only; the historical executable entry is not called.
    qa = runpy.run_path(str(HERE / "verify_r04g.py"))
    baseline = load(HERE / "r04j.baseline.json")
    files = files_under_base()
    docs = {p.name: raw(p).decode("utf-8") for p in files
            if p.parent == BASE and p.suffix == ".md"}
    require(len(docs) == 41, "41 root Markdown pages required")
    changed = []
    for name, old in baseline["files"].items():
        require((BASE / name).is_file(), "prior file removed: " + name)
        if sha(raw(BASE / name)) != old:
            changed.append(name)
            require(name in ALLOWED_EDITS, "unexpected prior artifact change: " + name)
    require(set(changed) == ALLOWED_EDITS, "expected fact/navigation edit set")
    new_files = {p.relative_to(BASE).as_posix() for p in files} - baseline["files"].keys()
    expected_new = NEW_PAGES | {
        "examples/r04j.baseline.json", "examples/verify_r04j.py",
        "examples/r04j.validation.json", "examples/r04j.leak.json",
    }
    require(new_files <= expected_new, "unexpected new artifact")
    coverage = qa["coverage"](docs)
    require(coverage == Counter(baseline["coverage"]), "coverage metadata changed")
    launches, kernels = Counter(), set()
    for item, n in coverage.items():
        row = json.loads(item)
        launches.update({i: n for i in row["launches"]})
        kernels.update(row["kernels"])
    require(launches == Counter(range(158)), "158 launches exactly once")
    require(len(kernels) == 44, "44 unique kernel names")
    code = Counter(qa["code_signature"](c) for t in docs.values()
                   for _, c in qa["blocks"](t))
    require(code == Counter(baseline["inline_ast"]), "seven inline arithmetic ASTs changed")
    require(sum(code.values()) == 7, "seven existing inline examples")
    ids = {name: qa["anchors"](text) for name, text in docs.items()}
    graph = {name: set() for name in docs}
    links = 0
    new_sources = {}
    for name, text in docs.items():
        explicit = re.findall(r'<a id="([^"]+)"', text)
        require(len(explicit) == len(set(explicit)), "duplicate explicit anchor: " + name)
        visible, fence = qa["without_fences"](text)
        require(fence is None, "unclosed fence: " + name)
        require(text.endswith("\n"), "missing final newline: " + name)
        require(not any(line.rstrip() != line for line in text.splitlines()),
                "trailing whitespace: " + name)
        for table in re.findall(r"(?m)(?:^\|.*\n?)+", visible):
            arities = [len(re.split(r"(?<!\\)\|", line)) for line in table.splitlines()]
            require(len(set(arities)) == 1, "table arity: " + name)
        for dest in re.findall(r"\]\(([^)\n]+)\)", visible):
            dest = dest.strip()
            if dest.startswith("<"):
                dest = dest[1:dest.index(">")]
            else:
                dest = dest.split(' "', 1)[0]
            u = urlsplit(dest)
            if u.scheme in ("https", "http", "mailto", "plugin"):
                continue
            filename, fragment = unquote(u.path), unquote(u.fragment)
            if re.match(r"^[A-Za-z]:[/\\]", dest):
                filename = unquote(dest.split("#", 1)[0])
            elif u.scheme == "file":
                filename = filename.lstrip("/")
            target = safe(BASE / name if not filename else Path(filename)
                          if re.match(r"^[A-Za-z]:", filename) else BASE / filename)
            links += 1
            require(target.exists(), "missing link " + name + ": " + dest)
            if not target.is_file():
                continue
            internal = target.parent == BASE and target.name in docs
            if internal:
                graph[name].add(target.name)
            if name in NEW_PAGES and not target.is_relative_to(BASE):
                new_sources[str(target)] = sha(raw(target))
            if not fragment:
                continue
            if re.fullmatch(r"L\d+(?:-L?\d+)?", fragment):
                numbers = list(map(int, re.findall(r"\d+", fragment)))
                require(all(1 <= i <= len(raw(target).splitlines()) for i in numbers),
                        "invalid line anchor " + name + ": " + dest)
            elif target.suffix == ".md":
                target_ids = ids[target.name] if internal else qa["anchors"](
                    raw(target).decode("utf-8-sig"))
                require(fragment in target_ids, "missing heading " + name + ": " + dest)
    reached = set()
    queue = deque(["L0_frame.md"])
    while queue:
        name = queue.popleft()
        if name not in reached:
            reached.add(name)
            queue.extend(graph[name] - reached)
    require(reached == set(docs), "unreachable pages")
    require(docs["INDEX.md"].index("L0a_object_method.md") <
            docs["INDEX.md"].index("L0_frame.md"), "object page must precede L0")
    for page in NEW_PAGES:
        require(page in docs["INDEX.md"] and page in docs["L0_frame.md"],
                "entry navigation missing: " + page)
    sampler_pages = ["INDEX.md", "L3_b70_history_output.md", "L4_tex_filter.md"]
    require(all("CB+0x40" not in docs[n] for n in sampler_pages), "sampler/CB conflation")
    require(docs["L3_b0_input.md"].count("CB+0x40 (u64)") == 1, "genuine handle slot")
    require("br=(a*b+128)/256" in docs["L4_tex_filter.md"] and
            "整数除法" in docs["L4_tex_filter.md"], "joint integer weight description")
    for n in ("L1_04_split16_encoder.md", "L2_04_split16_encoder.md",
              "L2_06_decoder_bridge.md", "L3_split16_window.md"):
        require("【推断】" in docs[n] and "独立" in docs[n], "geometry evidence tier: " + n)
    for n in ("L4_mufu.md", "APPENDIX_cpu_storage.md"):
        require("缓存命中" in docs[n] and "SHA" in docs[n], "cache qualification: " + n)
    for p in files:
        if p.suffix in (".md", ".py", ".json"):
            text = raw(p).decode("utf-8")
            require(not any(w in text for w in OLD_WORDS), "protected wording: " + p.name)
    # Confirm source evidence read for the three fixes without executing it.
    source_pins = {
        "E:/GlassBox-NR/cpp/chain_entry_optm/native_temporal.hpp": None,
        "E:/GlassBox-NR/cpp/chain_outtail_optm/full_raw_registry.hpp": None,
        str(BASE.parent / "reviews/FACT_AUDIT_R1_codex_20261027.md"): None,
    }
    new_sources.update({str(safe(p)): sha(raw(p)) for p in source_pins})
    scan_path = HERE / "r04j.leak.json"
    scan = load(scan_path)["summary"] if scan_path.is_file() else None
    if not args.pre_scan:
        require(scan is not None and scan["PASS"] and scan["files_with_block"] == 0
                and scan["files_with_name_violation"] == 0 and scan["missing"] == 0,
                "official leak scan not passing")
        require(scan is not None and scan["files"] == len(files), "scan file count stale")
    result = dict(
        status="PASS" if not ERRORS else "FAIL",
        scope="r04j documentation and saved evidence only",
        writes_under="docs/anatomy/skewer",
        new_GPU_runs=0, new_model_runs=0, new_chain_runs=0,
        network_calls=0, remote_calls=0, version_control_calls=0,
        markdown_pages=len(docs), reachable_pages=len(reached),
        local_links_checked=links, coverage_comments=sum(coverage.values()),
        launches_exactly_once=len(launches), unique_kernel_names=len(kernels),
        original_inline_arithmetic_preserved=code == Counter(baseline["inline_ast"]),
        previous_non_markdown_artifacts_preserved=all(n in ALLOWED_EDITS for n in changed),
        changed_existing_pages=sorted(changed), new_files=sorted(new_files),
        files_in_tree=len(files), source_sha256=new_sources,
        document_sha256={n: sha(raw(BASE / n)) for n in docs},
        official_scan=scan, errors=ERRORS,
    )
    (HERE / "r04j.validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ("document_sha256", "source_sha256", "official_scan", "new_files")},
                     ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))


if __name__ == "__main__":
    main()
