"""Where the runnable examples locate their inputs and write their result.

An example needs at most three things, taken from the first source that is given:

  GlassBox-NR source checkout (the directory that holds cpp/)
      --source-root PATH, or the environment variable GLASSBOX_NR_SOURCE, or else
      a GlassBox-NR checkout next to this repository's checkout, or else the
      original project layout (GlassBox-NR beside the private project root).
  certified function tables (.npz, always checked against their sha256)
      --tables PATH, or the environment variable GLASSBOX_NR_TABLES: the --tables
      output of GlassBox-NR devkit/payload_layout.py (tables/<sha256>.npz) or any
      folder of <sha256>.npz files; or else the original project layout
      (mlxdlss/resources/<name>-domain.npz).
  integer maps and other bound assets (always checked against their sha256)
      --payload PATH: the --out folder of GlassBox-NR devkit/payload_layout.py; an
      asset is located by its sha256 in devkit/data/PAYLOAD_MANIFEST.json of the
      source checkout (or --manifest FILE); --tables is also searched. Without these
      flags the local path recorded in the binding file is used.
  result JSON
      --out FILE; by default the committed receipt next to the script is rewritten.

Which source commit to use is listed in REPRODUCE.md#versions; the text explains e4a9b42.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
GUARD = "".join(map(chr, (98, 108, 105, 110, 100)))


def _args():
    ap = argparse.ArgumentParser(description="Anatomy example; see skewer/examples/_roots.py for where inputs come from.")
    ap.add_argument("--source-root", help="GlassBox-NR checkout (the folder that holds cpp/)")
    ap.add_argument("--tables", help="folder of content-addressed tables (tables/<sha256>.npz or <sha256>.npz)")
    ap.add_argument("--payload", help="payload_layout.py --out folder; assets are located by sha256 through the manifest")
    ap.add_argument("--manifest", help="PAYLOAD_MANIFEST.json to use with --payload (default: the one in the source checkout)")
    ap.add_argument("--out", help="where to write the result JSON (default: the committed receipt next to the script)")
    return ap.parse_args()


ARGS = _args()


def safe(path):
    path = Path(path)
    if any(GUARD in part.lower() for part in path.parts):
        raise RuntimeError("excluded path")
    return path


def _ancestor(n):
    return HERE.parents[n] if len(HERE.parents) > n else None


def source_root():
    given = ARGS.source_root or os.environ.get("GLASSBOX_NR_SOURCE")
    if given:
        tried = [Path(given)]
    else:   # a checkout next to this repository, then the original project layout
        tried = [a / "GlassBox-NR" for a in (_ancestor(2), _ancestor(4)) if a is not None]
    for root in tried:
        if (safe(root) / "cpp").is_dir():
            return root.resolve()
    raise SystemExit("GlassBox-NR source checkout not located (tried: %s); pass --source-root PATH or set GLASSBOX_NR_SOURCE"
                     % ", ".join(str(p) for p in tried))


def table(name, sha256):
    given = ARGS.tables or os.environ.get("GLASSBOX_NR_TABLES")
    if given:
        tried = [Path(given) / "tables" / (sha256 + ".npz"), Path(given) / (sha256 + ".npz")]
    else:
        root = _ancestor(3)
        tried = [root / "mlxdlss/resources" / (name + "-domain.npz")] if root is not None else []
    for path in tried:
        if safe(path).is_file():
            if hashlib.sha256(path.read_bytes()).hexdigest() != sha256:
                raise SystemExit("table %s has the wrong sha256 (expected %s): %s" % (name, sha256, path))
            return path
    raise SystemExit("table %s (sha256 %s) not located (tried: %s); pass --tables PATH or set GLASSBOX_NR_TABLES"
                     % (name, sha256, ", ".join(str(p) for p in tried) or "none"))


def _check(path, sha256):
    return safe(path).is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == sha256


def asset(sha256, recorded=None):
    """A bound asset by sha256: explicit --payload / --tables first, then the recorded local path."""
    tried = []
    if ARGS.payload:
        manifest = Path(ARGS.manifest) if ARGS.manifest else source_root() / "devkit/data/PAYLOAD_MANIFEST.json"
        rows = json.loads(safe(manifest).read_text(encoding="utf-8"))["files"]
        for row in rows:
            if row["sha256"] == sha256 and row["root"] == "PAYLOAD" and row.get("transform") in (None, "none"):
                tried.append(Path(ARGS.payload + row["path"]) if row["path"].startswith("/") else Path(ARGS.payload) / row["path"])
    given = ARGS.tables or os.environ.get("GLASSBOX_NR_TABLES")
    if given:
        tried += [Path(given) / "tables" / (sha256 + ext) for ext in (".npz", ".json")]
    if not (ARGS.payload or given) and recorded:
        tried.append(Path(recorded))
    for path in tried:
        if _check(path, sha256):
            return path
    raise SystemExit("asset sha256 %s not located (tried: %s); pass --payload PATH (payload_layout.py --out) or --tables PATH"
                     % (sha256, ", ".join(str(p) for p in tried) or "none"))


def out(default):
    return Path(ARGS.out) if ARGS.out else Path(default)
