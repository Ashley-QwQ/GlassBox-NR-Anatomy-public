"""Read only integer map sources for two physical output-byte examples.

No numeric tensor, weights, network input/target or model execution is used.
Logical output coordinates are intentionally not inferred from byte offsets.
Run from the repository root: python -B -X utf8 skewer/examples/map_trace_r04f.py
[--payload PATH] [--out FILE]; maps are located by sha256, see _roots.py.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _roots as roots

HERE = Path(__file__).resolve().parent
binding = HERE / "split16_window_r04d.bindings.json"
records = json.loads(binding.read_text(encoding="utf-8"))
guard = "".join(map(chr, (98, 108, 105, 110, 100)))


def asset(launch, suffix):
    row = next(r for r in records["assets_read"]
               if r["launch"] == launch and r["path"].endswith(suffix))
    path = roots.asset(row["sha256"], row["path"])
    if any(guard in part.lower() for part in path.parts):
        raise RuntimeError("excluded path")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == row["sha256"], "source identity mismatch"
    return path, digest


p100, h100 = asset(100, ".npz")
p56, h56 = asset(56, ".npz")
with np.load(p100, allow_pickle=False) as z:
    # Do not load B_off: the example needs no coefficient source.
    a = z["A_src"]
    out = z["OUTMAP"][0].copy()
    ro = z["RED_OFF"]
    red_index = int(np.searchsorted(ro, out[0]))
    assert int(ro[red_index]) == int(out[0])
    reductions = z["REDMAP"][red_index].copy()
    selectors = [tuple(map(int, row)) for row in reductions]
    selectors.append(tuple(map(int, out[1:5])))
    aflat = a.reshape(640, 16, 8, 32)

bit_dest = [2,3,1,7,8,9,10,11,4,5,6,0]


def logical_main_byte(offset):
    chunk, byte = divmod(offset, 4)
    tile, sw = divmod(chunk, 4096)
    original = sum(((sw >> dst) & 1) << src for src, dst in enumerate(bit_dest))
    slot, channel_chunk = divmod(original, 256)
    y = (tile // 8)*4 + slot//4
    x = (tile % 8)*4 + slot%4
    assert 0 <= x < 32 and 0 <= y < 20
    return x, y, 4*channel_chunk+byte


sources = []
for t, chain, lane_d, slot in selectors:
    row = lane_d//4 + (slot//2)*8
    addresses = []
    for step in range(8):
        for k in range(32):
            lane_a = (row % 8)*4 + (k % 16)//4
            part = row//8 + 2*(k//16)
            addresses.append(int(aflat[t, chain, step, lane_a]) + 4*part + k%4)
    logical = [logical_main_byte(offset) for offset in addresses]
    sources.append({
        "D_selector": [t, chain, lane_d, slot],
        "source_spatial_xy": [list(xy) for xy in sorted({(x,y) for x,y,c in logical})],
        "channel_min_max": [min(c for x,y,c in logical), max(c for x,y,c in logical)],
        "read_events": len(addresses),
        "unique_input_bytes": len(set(addresses)),
    })
with np.load(p56, allow_pickle=False) as z:
    stores = z["gstore_off"]
    # Concatenated CPU result: full first, pooled second.
    pooled_start = 60*36*512
    owners = np.argwhere((stores >= 0) & (stores <= pooled_start) &
                         (pooled_start < stores+16))
    assert len(owners) == 1
    owner = owners[0]
    start = int(stores[tuple(owner)])
result = {
    "status": "PASS",
    "scope": "integer maps only; source coordinates use the independent L99 repack formula; no logical output/skip coordinate claim",
    "source_sha256": {p100.as_posix(): h100, p56.as_posix(): h56},
    "L100_output_byte": 0,
    "L100_reduction_half_byte_offset": int(out[0]),
    "L100_reduction_index": red_index,
    "L100_skip_byte_offset": int(out[5]),
    "L100_four_partial_sources": sources,
    "L56_pooled_byte": 0,
    "L56_concatenated_output_byte": pooled_start,
    "L56_writer_index": list(map(int, owner)),
    "L56_writer_start": start,
    "L56_byte_within_16B_event": pooled_start-start,
    "unknown": "native independent logical output and skip labeling; full logical spatial relation of L56/L100",
}
roots.out(HERE / "map_trace_r04f.result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k != "source_sha256"},
                 ensure_ascii=False))
