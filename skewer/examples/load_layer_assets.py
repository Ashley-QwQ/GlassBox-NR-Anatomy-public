"""Load the frozen 1080 L56 assets into the form the public split16 executor accepts.

  python -B -X utf8 skewer/examples/load_layer_assets.py [--payload PATH] [--tables PATH] [--manifest FILE] [--source-root PATH]

The raw NPZ / JSON assets listed in REPRODUCE.md#layer-assets cannot be handed to the executor as they are. This
loader does what the public runtime does (GlassBox-NR runtime/M/g0a_runtime.py:13-29, 48-54 and
plan_runtime_merged.py:35-41):
  * keeps only the map keys the wiring needs, with their signed dtype, native byte order, C-contiguous, read-only;
  * adds a final axis to thread_class, (80,4,32) -> (80,4,32,1), because the executor indexes maps as (c,y,l,s);
  * takes the contract dictionary out of its release_form wrapper ({"contract": {...}});
  * expands the RSQ / RCP tables to dense float32 bit-pattern tables indexed by half_bits - 0x0410.
Every asset is checked against its sha256 before use. Without flags the assets are read from the local paths recorded
in split16_window_r04d.bindings.json (original project layout); --payload (payload_layout.py --out) and --tables
(payload_layout.py --tables) locate them by sha256 instead. Only 1080 L56 is supported.

LayerAssets.arguments(input_bytes, weight_bytes) returns the positional arguments of the public
dlssnr_chain_split16_optm.audit_execute (no keyword names). This proves only that the interface connects; it says
nothing about numerical correctness. audit_execute does not check that the maps are read-only; the precompiled entry
does. A self-written DAG interpreter can keep the raw three-axis thread_class and the raw half-bit table keys.
Checked on 2026-10-31 with synthetic input and weights: output 1,433,600 B, removing the class axis is refused.
"""
from pathlib import Path, PurePosixPath
from dataclasses import dataclass
import argparse
import hashlib
import io
import json
import os
import numpy as np

HERE = Path(__file__).resolve().parent
GUARD = "".join(map(chr, (98, 108, 105, 110, 100)))
# Asset rows are identical in the v2.0.1-preview (ca50ccbc...) and v2.0.2-preview (4665a4ec...) manifests.
MANIFEST_SHA = {"ca50ccbcb0516cfd72172e2400710d08edae6441ac4af4be694a0d855af26514",
                "4665a4eccef62b310cb1c61b433fa5f27b2069682b4b6616239bcfb70e893902"}
ASSETS = {   # name: (sha256, bytes)
    "map": ("f9280f62d910b66cdb728860fe27d36153da6a71367182b6cb4951667b42bb01", 17106182),
    "wiring": ("384adcbb6260db42348605a7b84532d10a02491a3fc4fb1260624227282d3686", 201381),
    "contract": ("710c38c8a76c4198d95228de787b08f12ed73bc5a4684e94c8e9440eda8adff8", 16),
    "rsq": ("06ffffcad0796e18eb51cce1166712d57b33a2138857bfa791d0e36f35210e62", 246454),
    "rcp": ("055e26f1b2324491e47b7faf02f3b82c4da71fd6d7cb4843b1275f61f95b2b59", 246446),
}
# Historical L56 contract report in the original layout (a sibling folder of the project root); its contract dict is
# projected into the release form when no --payload/--tables is given.
HISTORICAL_CONTRACT = ("18f5e0d656ab6037f7a09982c2c4e75d62f18487020cce43fc55d09a1c64733c", 1821,
                       ("dlssnr-cpp-work", "chain-split16-r01-codex", "bundle", "L56-contract.json"))
MAP_SCHEMA = {   # raw key: (raw shape, raw dtype); sread_shared_off is source-side only and not passed on
    "wload_off": ((80, 4, 32, 64), "<i8"),
    "sread_src": ((80, 4, 32, 64, 16), "<i8"),
    "gstore_off": ((80, 4, 32, 10), "<i8"),
    "xsite_src": ((80, 4, 32, 96, 4), "<i8"),
    "xsite_wsrc": ((80, 4, 32, 96, 4), "<i8"),
    "shfl_idx": ((80, 4, 32, 256), "<i8"),
    "psel": ((80, 4, 32, 64), "|i1"),
    "thread_class": ((80, 4, 32), "<i2"),
}
INPUT_ROLES = (1105920, 1105920)   # word0 input, then word1 residual
WEIGHT_BYTES = 263168
OUTPUT_ROLES = (1105920, 327680)   # word2 full, then word3 pooled
TABLE_START, TABLE_END = 0x0410, 0x7c00


def safe(path):
    p = Path(path)
    if any(GUARD in part.lower() for part in p.parts):
        raise ValueError("excluded path")
    return p


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verified(path, expected, size):
    data = safe(path).read_bytes()
    if digest(data) != expected or (size is not None and len(data) != size):
        raise ValueError("SHA_OR_SIZE_DIFF: " + str(path))
    return data


def default_source_root():
    for base in (HERE.parents[2], HERE.parents[4] if len(HERE.parents) > 4 else None):
        if base is not None and (base / "GlassBox-NR" / "cpp").is_dir():
            return base / "GlassBox-NR"
    return None


def recorded_paths():
    rows = json.loads((HERE / "split16_window_r04d.bindings.json").read_text(encoding="utf-8"))["assets_read"]
    by_sha = {r["sha256"]: r["path"] for r in rows if r["launch"] == 56}
    out = {name: by_sha.get(sha) for name, (sha, _) in ASSETS.items()}
    private_root = HERE.parents[3] if len(HERE.parents) > 3 else None
    for name in ("rsq", "rcp"):
        if private_root is not None:
            out[name] = str(private_root / "mlxdlss/resources" / (name + "-domain.npz"))
    return out


def required_fields(wiring):
    kinds = {n[0] for n in wiring["nodes"]}
    need = {"wload_off", "sread_src", "gstore_off"}
    if kinds & {"X", "XH"}:
        need.update(("xsite_src", "xsite_wsrc"))
    if "SI" in kinds:
        need.add("shfl_idx")
    if "PS" in kinds:
        need.add("psel")
    if "classes" in wiring:
        need.add("thread_class")
    return need


def locate(name, payload, tables, manifest, source_root, recorded):
    sha, size = ASSETS[name]
    candidates = []
    if payload and name not in ("rsq", "rcp"):
        mp = Path(manifest) if manifest else Path(source_root or "") / "devkit/data/PAYLOAD_MANIFEST.json"
        raw = safe(mp).read_bytes()
        if manifest is None and digest(raw) not in MANIFEST_SHA:
            raise ValueError("PAYLOAD_MANIFEST.json is not a known v2.0.1/v2.0.2 manifest; pass --manifest")
        transform = "release_form" if name == "contract" else "none"
        for row in json.loads(raw.decode("utf-8"))["files"]:
            if row["sha256"] == sha and row["root"] == "PAYLOAD" and (row.get("transform") or "none") == transform:
                rel = PurePosixPath(row["path"].lstrip("/"))
                if ".." in rel.parts or ":" in str(rel):
                    raise ValueError("invalid manifest path")
                candidates.append(Path(payload).joinpath(*rel.parts))
    if tables:
        ext = ".npz" if name in ("map", "rsq", "rcp") else ".json"
        candidates += [Path(tables) / "tables" / (sha + ext), Path(tables) / (sha + ext)]
    if recorded.get(name) and (not (payload or tables) or (name in ("rsq", "rcp") and not tables)):
        candidates.append(Path(recorded[name]))
    for p in candidates:
        if safe(p).is_file():
            return verified(p, sha, size)
    if name == "contract" and not (payload or tables) and len(HERE.parents) > 4:
        # The original layout keeps the historical report, not the release file: project its contract dict into the
        # release form (compact JSON + LF) and require the release sha256 before using it.
        hsha, hsize, hparts = HISTORICAL_CONTRACT
        old = json.loads(verified(HERE.parents[4].joinpath(*hparts), hsha, hsize).decode("utf-8"))
        release = (json.dumps({"contract": old["contract"]}, separators=(",", ":")) + "\n").encode("utf-8")
        if digest(release) != sha or len(release) != size:
            raise ValueError("RELEASE_FORM_SHA_DIFF")
        return release
    raise FileNotFoundError("asset %s (sha256 %s) not located; pass --payload and/or --tables" % (name, sha))


def expand_table(data):
    with np.load(io.BytesIO(data), allow_pickle=False) as z:
        bits, vals = z["input_half_bits"], z["native_float_bits"]
        if bits.ndim != 1 or vals.shape != bits.shape or bits.dtype != np.dtype("<u2") or vals.dtype != np.dtype("<u4"):
            raise ValueError("function table schema")
        ix = bits.astype(np.int64) - TABLE_START
        live = (ix >= 0) & (ix < TABLE_END - TABLE_START)
        dense = np.zeros(TABLE_END - TABLE_START, dtype=np.uint32)
        dense[ix[live]] = vals[live]
        if np.unique(ix[live]).size != dense.size:
            raise ValueError("function table domain coverage")
        table = dense.view(np.float32)   # bit reinterpretation, not a numeric cast
        table.flags.writeable = False
        return table


@dataclass
class LayerAssets:
    wiring: dict
    maps: dict
    contract: dict
    tables: dict
    receipt: dict

    def arguments(self, input_bytes, weight_bytes, threads=4, queue_seed=0):
        """Positional arguments of the public audit_execute (it has no keyword names)."""
        if not isinstance(input_bytes, bytes) or len(input_bytes) != sum(INPUT_ROLES):
            raise ValueError("L56 input byte length/type")
        if not isinstance(weight_bytes, bytes) or len(weight_bytes) != WEIGHT_BYTES:
            raise ValueError("L56 weight byte length/type")
        return (self.wiring, self.maps, input_bytes, weight_bytes, self.contract,
                self.tables["rsq"], self.tables["rcp"], sum(OUTPUT_ROLES), threads, queue_seed)


def load_layer_assets(layer, payload=None, tables=None, manifest=None, source_root=None):
    if layer != 56:
        raise ValueError("only the frozen 1080 L56 is supported")
    tables = tables or os.environ.get("GLASSBOX_NR_TABLES")
    source_root = source_root or os.environ.get("GLASSBOX_NR_SOURCE") or default_source_root()
    recorded = recorded_paths()
    blobs = {name: locate(name, payload, tables, manifest, source_root, recorded) for name in ASSETS}
    wiring = json.loads(blobs["wiring"].decode("utf-8"))
    contract = json.loads(blobs["contract"].decode("utf-8"))["contract"]   # never pass the outer wrapper
    if not isinstance(contract, dict):
        raise ValueError("contract must be a dict")
    maps = {}
    with np.load(io.BytesIO(blobs["map"]), allow_pickle=False) as z:
        if not required_fields(wiring).issubset(z.files):
            raise ValueError("missing required map fields")
        for key, (shape, dtype) in MAP_SCHEMA.items():
            a = z[key]
            if a.shape != shape or a.dtype != np.dtype(dtype):
                raise ValueError("map shape/dtype: " + key)
            if key == "thread_class":
                a = a[..., None]   # (80,4,32) -> (80,4,32,1)
            a = np.ascontiguousarray(a, dtype=a.dtype.newbyteorder("="))
            a.flags.writeable = False
            maps[key] = a
        excluded = sorted(set(z.files) - set(maps))
    expanded = {name: expand_table(blobs[name]) for name in ("rsq", "rcp")}
    receipt = {"layer": 56, "assets": {n: {"sha256": ASSETS[n][0], "bytes": len(b)} for n, b in blobs.items()},
               "maps": {k: {"shape": list(a.shape), "dtype": a.dtype.str, "c_contiguous": a.flags.c_contiguous,
                            "writeable": a.flags.writeable, "bytes": a.nbytes} for k, a in maps.items()},
               "excluded_keys": excluded, "required_by_wiring": sorted(required_fields(wiring)),
               "input_bytes": sum(INPUT_ROLES), "weight_bytes": WEIGHT_BYTES, "output_bytes": sum(OUTPUT_ROLES),
               "tables": {k: {"shape": list(v.shape), "dtype": v.dtype.str, "sha256": digest(v.tobytes())}
                          for k, v in expanded.items()},
               "contract_entries": len(contract), "numerical_correctness": "NOT_ESTABLISHED"}
    return LayerAssets(wiring, maps, contract, expanded, receipt)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Check and adapt the 1080 L56 assets; prints a receipt, runs nothing.")
    ap.add_argument("--payload")
    ap.add_argument("--tables")
    ap.add_argument("--manifest")
    ap.add_argument("--source-root")
    args = ap.parse_args()
    print(json.dumps(load_layer_assets(56, **vars(args)).receipt, ensure_ascii=False, indent=2))
