"""Read integer maps only; no model tensors, coefficients or network runs.

Run from the repository root: python -B -X utf8 skewer/examples/geometry_r04g.py
[--payload PATH] [--out FILE]; maps are located by sha256, see _roots.py.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _roots as roots
HERE=Path(__file__).resolve().parent
records=json.loads((HERE/"split16_window_r04d.bindings.json").read_text(encoding="utf-8"))
guard="".join(map(chr,(98,108,105,110,100)))
pins={}
def asset(launch,suffix):
    r=next(x for x in records["assets_read"] if x["launch"]==launch and x["path"].endswith(suffix))
    p=roots.asset(r["sha256"],r["path"])
    assert not any(guard in x.lower() for x in p.parts)
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==r["sha256"],"map identity mismatch"
    pins[p.as_posix()]=actual
    return p
with np.load(asset(100,".npz"),allow_pickle=False) as z:
    av=z["A_src"].reshape(4,160,16,8,32)
    def decode_byte(offset):
        chunk=offset//4
        low=chunk%4096
        order=[2,3,1,7,8,9,10,11,4,5,6,0]
        original=sum(((low>>dst)&1)<<src for src,dst in enumerate(order))
        tile=chunk//4096;slot=original//256
        return ((tile%8)*4+slot%4,(tile//8)*4+slot//4,
                4*(original%256)+offset%4)
    x0,y0,c0=decode_byte(av[0])
    # A_src contains packed-word bases, not one channel per entry. Apply
    # decoder()'s actual A operand selection before checking a matrix row.
    k=np.arange(32)
    for matrix_row in range(16):
        lanes=(matrix_row%8)*4+(k%16)//4
        parts=matrix_row//8+2*(k//16)
        addresses=av[0][...,lanes]+4*parts+k%4
        xx,yy,cc=decode_byte(addresses)
        assert np.all(xx==xx[...,:1,:1]) and np.all(yy==yy[...,:1,:1])
        assert np.all(np.sort(cc.reshape(160,16,256),axis=-1)==np.arange(256))
    for group in range(1,4):
        xx,yy,cc=decode_byte(av[group])
        assert np.array_equal(xx,x0) and np.array_equal(yy,y0)
        assert np.array_equal(cc,c0+256*group)
    out=z["OUTMAP"];ro=z["RED_OFF"];red=z["REDMAP"]
    ix=np.searchsorted(ro,out[:,0])
    assert np.array_equal(ro[ix],out[:,0])
    parts=np.concatenate((red[ix],out[:,None,1:5]),axis=1)
    groups=np.sort(parts[:,:,0]//160,axis=1)
    assert np.all(groups==np.arange(4))
    # The four selectors share the non-channel coordinates.
    canonical=parts.copy();canonical[:,:,0]%=160
    same=np.all(canonical==canonical[:,0:1,:])
    assert same
    count=len(out)
with np.load(asset(56,".npz"),allow_pickle=False) as z:
    stores=z["gstore_off"]
    start=60*36*512
    live=stores[stores>=start]-start
    assert len(live)*16==32*20*512
    assert np.array_equal(np.sort(live),np.arange(0,32*20*512,16))
    # Each 4x4x512-byte output tile has exactly 8192 bytes.
    tile_counts=np.bincount(live//8192,minlength=40)
    assert np.all(tile_counts==512)
    per_task=[]
    for row in stores:
        offsets=row[row>=start]-start
        per_task.append({"bytes":int(len(offsets)*16),
                         "tile_ids":list(map(int,np.unique(offsets//8192)))})
result={
    "status":"PASS","scope":"fixed 1080 integer maps only, not native independent spatial-layout proof",
    "L100_output_bytes":count,
    "L100_all_four_channel_group_ids_once":True,
    "L100_shared_non_channel_selector":bool(same),
    "L100_A_source_groups_same_position_channels_shift_256":True,
    "L100_single_trace_channel_ranges":[[0,255],[256,511],[512,767],[768,1023]],
    "L100_each_partial_K":8*32,
    "L100_all_matrix_rows_each_partial_256_distinct_channels":True,
    "L56_extent_relation":{"input_wh":[60,36],"window_counts":[8,5],
                           "window_canvas_wh":[64,40],"per_window_output_wh":[4,4],
                           "output_wh":[32,20]},
    "L56_pooled_unique_16B_events":len(live),
    "L56_4x4x512_tiles":len(tile_counts),
    "L56_bytes_per_tile":8192,
    "L56_task_output_summary":per_task,
    "limits":"window counts and output tile capacity support the geometry; not proof of standard average pooling or a unique native interpolation kernel",
    "source_sha256":pins,
}
roots.out(HERE/"geometry_r04g.result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k not in ("source_sha256","L56_task_output_summary")},ensure_ascii=False))
