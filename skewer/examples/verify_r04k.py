"""r04k document/header QA only; no model, compiler or remote execution."""
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
NEW_PAGES = {"L4_cross_arch.md", "L2_weights_layout.md", "REPRODUCE.md"}
NAV = {
    "INDEX.md": [
        "横切导读：[153条权重组织](L2_weights_layout.md) · [跨GPU／CPU后端比较](L4_cross_arch.md) · [公开v2复现指南](REPRODUCE.md)。",
        '| <a id="l4-cross-arch"></a>[L4.cross-arch](L4_cross_arch.md#comparison) | sm_120与较早GPU的原语差异、CPU后端方案及实际字节门边界 |',
    ],
    "L0_frame.md": [
        "[权重组织与阶段字节账](L2_weights_layout.md) · [跨架构比较](L4_cross_arch.md) · [公开v2复现](REPRODUCE.md)"
    ],
    "L0a_object_method.md": [
        "[公开v2复现指南](REPRODUCE.md) · [权重组织](L2_weights_layout.md)"
    ],
}
NAV.update({n: ["[跨架构原语与CPU后端比较](L4_cross_arch.md)"] for n in (
    "L3_qmma_e4m3.md", "L4_e4m3_and_k32.md", "L4_half_arith.md", "L4_hmma.md",
    "L4_mufu.md", "L4_fp32_ftz.md", "L4_tex_filter.md")})
NAV.update({n: ["[权重组织、dtype与阶段字节账](L2_weights_layout.md)"] for n in (
    "L2_02_b0.md", "L2_03_tin_encoder.md", "L2_04_split16_encoder.md",
    "L2_05_vit.md", "L2_06_decoder_bridge.md", "L2_09_b70.md")})
ERRORS = []


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


def all_files():
    result = []
    for root, dirs, names in os.walk(BASE):
        dirs[:] = sorted(d for d in dirs if GUARD not in d.lower())
        for name in sorted(names):
            if GUARD not in name.lower():
                result.append(safe(Path(root) / name))
    return result


def restored_without_navigation(name, text):
    for nav in NAV[name]:
        require(text.count(nav) == 1, "navigation missing/duplicated: " + name)
        if nav.startswith("|"):
            text = text.replace(nav + "\n", "")
        else:
            text = text.replace("\n" + nav + "\n", "")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre-scan", action="store_true")
    args = ap.parse_args()
    qa = runpy.run_path(str(HERE / "verify_r04g.py"))  # pure helper definitions only
    baseline = load(HERE / "r04k.baseline.json")
    files = all_files()
    docs = {p.name: raw(p).decode("utf-8") for p in files
            if p.parent == BASE and p.suffix == ".md"}
    require(len(docs) == 44, "44 Markdown pages required")
    changed = []
    for name, old_sha in baseline["files"].items():
        data = raw(BASE / name)
        if sha(data) == old_sha:
            continue
        changed.append(name)
        require(name in NAV, "prior artifact changed beyond navigation: " + name)
        if name in NAV:
            old_text = restored_without_navigation(name, docs[name])
            variants = (old_text.encode("utf-8"), old_text.replace("\n", "\r\n").encode("utf-8"))
            require(any(sha(v) == old_sha for v in variants), "non-navigation content changed: " + name)
    require(set(changed) == set(NAV), "expected navigation edit set")
    expected_new = NEW_PAGES | {
        "examples/r04k.baseline.json", "examples/weights_layout_r04k.py",
        "examples/r04k.weights_layout.json", "examples/verify_r04k.py",
        "examples/r04k.validation.json", "examples/r04k.leak.json",
    }
    new_files = {p.relative_to(BASE).as_posix() for p in files} - baseline["files"].keys()
    require(new_files <= expected_new, "unexpected new artifact")
    coverage = qa["coverage"](docs)
    require(coverage == Counter(baseline["coverage"]), "coverage comments changed")
    launches, kernels = Counter(), set()
    for item, count in coverage.items():
        row = json.loads(item)
        launches.update({i: count for i in row["launches"]})
        kernels.update(row["kernels"])
    require(launches == Counter(range(158)) and len(kernels) == 44, "158/158 and 44 kernel names")
    code = Counter(qa["code_signature"](c) for text in docs.values()
                   for _, c in qa["blocks"](text))
    require(code == Counter(baseline["inline_ast"]), "existing inline arithmetic changed")
    ids = {n: qa["anchors"](t) for n, t in docs.items()}
    graph, links, sources = {n: set() for n in docs}, 0, {}
    for name, text in docs.items():
        visible, fence = qa["without_fences"](text)
        require(fence is None, "unclosed fence: " + name)
        explicit = re.findall(r'<a id="([^"]+)"', text)
        require(len(explicit) == len(set(explicit)), "duplicate explicit anchor: " + name)
        require(text.endswith("\n"), "final newline: " + name)
        require(not any(s.rstrip() != s for s in text.splitlines()), "trailing whitespace: " + name)
        for table in re.findall(r"(?m)(?:^\|.*\n?)+", visible):
            counts = [len(re.split(r"(?<!\\)\|", line)) for line in table.splitlines()]
            require(len(set(counts)) == 1, "table arity: " + name)
        for dest in re.findall(r"\]\(([^)\n]+)\)", visible):
            dest = dest.strip()
            if dest.startswith("<"):
                dest = dest[1:dest.index(">")]
            else:
                dest = dest.split(' "', 1)[0]
            u = urlsplit(dest)
            if u.scheme in ("http", "https", "mailto", "plugin"):
                continue  # offline task: external URLs are not fetched
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
                sources[str(target)] = sha(raw(target))
            if re.fullmatch(r"L\d+(?:-L?\d+)?", fragment):
                numbers = map(int, re.findall(r"\d+", fragment))
                require(all(1 <= i <= len(raw(target).splitlines()) for i in numbers),
                        "invalid line anchor " + name + ": " + dest)
            elif fragment and target.suffix == ".md":
                anchors = ids[target.name] if internal else qa["anchors"](
                    raw(target).decode("utf-8-sig"))
                require(fragment in anchors, "missing heading " + name + ": " + dest)
    reached, queue = set(), deque(["L0_frame.md"])
    while queue:
        name = queue.popleft()
        if name not in reached:
            reached.add(name)
            queue.extend(graph[name] - reached)
    require(reached == set(docs), "unreachable page")
    for name in NEW_PAGES:
        require(name in docs["INDEX.md"], "INDEX entry missing: " + name)
        require(any(name in docs[n] for n in NAV if n != "INDEX.md"), "L-layer entry missing: " + name)
    comparison = re.findall(r"(?m)(?:^\|.*\n?)+", docs["L4_cross_arch.md"])
    require(len(comparison) == 1, "one consolidated architecture table")
    if comparison:
        for row in comparison[0].splitlines()[2:]:
            cells = row.split("|")[2:-1]
            require(len(cells) == 3 and all("【" in c and "](" in c for c in cells),
                    "every comparison cell needs tier and evidence")
    weights = load(HERE / "r04k.weights_layout.json")
    require(weights["status"] == "PASS" and weights["payload_bytes_read"] == 0,
            "metadata-only weight projection")
    require(weights["tensor_count"] == len(weights["tensors"]) == 153, "153 packed entries")
    require(weights["aligned_upload_bytes"] == 147719680 and
            weights["payload_bytes"] == 147683778, "weight layout totals")
    for path, expected in weights["source_code_sha256"].items():
        require(sha(raw(path)) == expected, "weight rule source changed")
    labels = {"B0": "B0", "TIN_encoder": "TIN编码", "split16_encoder": "split16编码",
              "ViT": "ViT", "bridge": "B39桥", "split16_decoder": "split16解码",
              "TIN_decoder": "TIN解码", "B70": "B70"}
    for stage, row in weights["stages"].items():
        line = next((s for s in docs["L2_weights_layout.md"].split('<a id="stage-bytes">', 1)[1].splitlines()
                     if s.startswith("| " + labels[stage] + " |") and "Σ" not in s), "")
        require(str(row["tensor_count"]) in line and
                f'{row["payload_bytes"]:,}' in line and f'{row["aligned_slot_bytes"]:,}' in line,
                "stage byte table: " + stage)
    for row in weights["tensors"]:
        require(set(row) == {"name", "block", "layer", "stage", "serialized_dimensions",
                            "serialized_dtype_code", "container_dtype", "container_shape",
                            "payload_bytes", "aligned_slot_bytes"}, "metadata whitelist")
    ref_path = Path("E:/GlassBox-NR/devkit/data/reference_f0.json")
    ref = load(ref_path)
    require(len(ref["launches"]) == 158 and ref["final_sha256"] in docs["REPRODUCE.md"],
            "public final reference")
    require("ea731776" in docs["REPRODUCE.md"] and "摘要表" in docs["REPRODUCE.md"],
            "public reproduction identity/scope")
    for p in files:
        if p.suffix in (".md", ".py", ".json"):
            require(not any(w in raw(p).decode("utf-8") for w in OLD_WORDS),
                    "protected wording: " + p.name)
    scan_path = HERE / "r04k.leak.json"
    scan = load(scan_path)["summary"] if scan_path.is_file() else None
    if not args.pre_scan:
        require(scan is not None and scan["PASS"] and scan["files_with_block"] == 0
                and scan["files_with_name_violation"] == 0 and scan["missing"] == 0,
                "official publish scan")
        require(scan is not None and scan["files"] == len(files), "scan count stale")
    result = dict(
        status="PASS" if not ERRORS else "FAIL", scope="three new pages and navigation only",
        markdown_pages=len(docs), reachable_pages=len(reached), local_links_checked=links,
        coverage_comments=sum(coverage.values()), launches_exactly_once=len(launches),
        unique_kernel_names=len(kernels), inline_arithmetic_preserved=code == Counter(baseline["inline_ast"]),
        previous_artifacts_preserved=not any(n not in NAV for n in changed),
        changed_navigation_pages=sorted(changed), new_files=sorted(new_files),
        weight_entries=153, weight_payload_bytes_read=weights["payload_bytes_read"],
        aligned_weight_layout_bytes=weights["aligned_upload_bytes"],
        new_GPU_runs=0, new_model_runs=0, new_chain_runs=0,
        network_calls=0, remote_calls=0, version_control_calls=0,
        files_in_tree=len(files), source_sha256=sources,
        document_sha256={n: sha(raw(BASE / n)) for n in docs},
        official_scan=scan, errors=ERRORS,
    )
    (HERE / "r04k.validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ("source_sha256", "document_sha256", "official_scan", "new_files")},
                     ensure_ascii=False, indent=2))
    raise SystemExit(bool(ERRORS))


if __name__ == "__main__":
    main()
