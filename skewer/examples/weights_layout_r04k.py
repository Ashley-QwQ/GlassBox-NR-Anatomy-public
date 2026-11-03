"""Project only an existing container's JSON header; never read its payload."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import math
import re
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GUARD = "".join(map(chr, (98, 108, 105, 110, 100)))
STAGES = (
    (0, 0, "B0"), (1, 22, "TIN_encoder"), (23, 30, "split16_encoder"),
    (31, 38, "ViT"), (39, 39, "bridge"),
    (40, 47, "split16_decoder"), (48, 69, "TIN_decoder"), (70, 70, "B70"),
)


def safe(p):
    p = Path(p).resolve()
    if any(GUARD in x.lower() for x in p.parts):
        raise ValueError("guarded path refused")
    return p


def stage_for(block):
    return next(name for lo, hi, name in STAGES if lo <= block <= hi)


def main():
    source = safe(ROOT / "experiments/parity-v1/weights-packed.safetensors")
    # A bounded read of 8 + header_length bytes. No tensor data or full-file hash.
    with source.open("rb") as f:
        length = struct.unpack("<Q", f.read(8))[0]
        if not 0 < length < (1 << 20):
            raise ValueError("header bound")
        header = json.loads(f.read(length))
        assert f.tell() == 8 + length
    metadata = header["__metadata__"]
    records = json.loads(metadata["source_tensor_records"])
    assert len(records) == int(metadata["tensor_count"]) == 153
    rows = []
    groups = defaultdict(lambda: defaultdict(list))
    for name, record in sorted(records.items()):
        match = re.fullmatch(r"block(\d+)\.layer(\d+)\.(layer|blend_scale)", name)
        if not match:
            raise ValueError("unexpected tensor name")
        block, layer = int(match[1]), int(match[2])
        dims = record["dimensions"]
        nbytes = record["byteCount"]
        assert record["dtypeCode"] == 1 and nbytes == 2 * math.prod(dims)
        assert header[name]["dtype"] == "U8" and header[name]["shape"] == [nbytes]
        assert header[name]["data_offsets"][1] - header[name]["data_offsets"][0] == nbytes
        stage = stage_for(block)
        row = dict(name=name, block=block, layer=layer, stage=stage,
                   serialized_dimensions=dims, serialized_dtype_code=1,
                   container_dtype="U8", container_shape=[nbytes],
                   payload_bytes=nbytes, aligned_slot_bytes=(nbytes + 511) // 512 * 512)
        rows.append(row)
        groups[stage][tuple(dims)].append(name)
    stages = {}
    for lo, hi, stage in STAGES:
        members = [r for r in rows if r["stage"] == stage]
        variants = [dict(serialized_dimensions=list(dims), count=len(names),
                         names=names) for dims, names in sorted(groups[stage].items())]
        stages[stage] = dict(block_range=[lo, hi], tensor_count=len(members),
                             payload_bytes=sum(r["payload_bytes"] for r in members),
                             aligned_slot_bytes=sum(r["aligned_slot_bytes"] for r in members),
                             shape_variants=variants)
    payload = sum(r["payload_bytes"] for r in rows)
    aligned = sum(r["aligned_slot_bytes"] for r in rows)
    assert payload == int(metadata["payload_byte_count"]) == 147683778
    assert aligned == 147719680
    assert sum(s["tensor_count"] for s in stages.values()) == 153
    # Source-code identities only; no per-tensor hash or coefficient is published.
    rules = [
        Path("E:/GlassBox-NR/devkit/make_weights.py"),
        Path("E:/GlassBox-NR/third_party/mlxdlss/tools/extract_dlssnr_weights.py"),
    ]
    result = dict(
        status="PASS", scope="header metadata and integer size arithmetic only",
        source=str(source), source_file_bytes=source.stat().st_size,
        bytes_read=8 + length, payload_bytes_read=0,
        source_code_sha256={str(p): hashlib.sha256(safe(p).read_bytes()).hexdigest() for p in rules},
        tensor_count=len(rows), payload_bytes=payload,
        alignment=512, aligned_upload_bytes=aligned,
        padding_bytes=aligned-payload, resource_bytes=147695410,
        resource_record_framing_bytes=147695410-payload,
        order_note="sum of padded slots is order-independent; source resource order is not inferred from the sorted header",
        stages=stages, tensors=rows,
    )
    (HERE / "r04k.weights_layout.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ("source_code_sha256", "tensors", "stages")}, ensure_ascii=False, indent=2))
    for stage, data in stages.items():
        print(stage, data["tensor_count"], data["payload_bytes"], data["aligned_slot_bytes"])


if __name__ == "__main__":
    main()
