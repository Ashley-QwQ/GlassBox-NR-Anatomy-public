"""Small CPU address-only comparisons; external research and tables remain read-only."""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import sys
import zipfile
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ROUND = ROOT / 'experiments/mapform-split16-qkv-r01-20261027-codex'
GUARD = ''.join(map(chr, (98, 108, 105, 110, 100)))
FORMULA_SHA = '12f4ea819859144f54ced9a45e17279de7ef49f0552156375b0024b516e502cd'
INVENTORY_SHA = '1a010315fa12b78e77c608c20cbeb27b2773bb31a9d1827462477c2c45faa4f8'
CLOSED_FIELDS = ('wload_off', 'sread_shared_off', 'sread_src', 'xsite_src',
                 'xsite_wsrc', 'gstore_off', 'shfl_idx', 'psel')


def safe(path):
    path = Path(path).resolve()
    if any(GUARD in part.lower() for part in path.parts):
        raise ValueError('Excluded path')
    return path


def sha(path):
    digest = hashlib.sha256()
    with safe(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    return json.loads(safe(path).read_text(encoding='utf-8'))


def document_value(field, g, a, y, lane, event=0, byte=0):
    """Independent scalar transcription of the displayed eight equations."""
    gx = math.ceil((g.W - g.shift_x) / 8)
    gy = math.ceil((g.H - g.shift_y) / 8)
    q = gx * gy
    wx, wy, z = a % gx, (a // gx) % gy, a // q
    head = 4 * z + y
    if field == 'wload_off':
        if event < 96:
            return 49152 * (event // 6) + 3072 * head + 512 * (event % 6) + 16 * lane
        return 786432 + 8192 * head + 512 * (event - 96) + 16 * lane
    if field == 'sread_shared_off':
        return 512 * (event % 16) + 16 * lane
    if field in ('sread_src', 'gstore_off'):
        if field == 'sread_src':
            tx = 2 * wx + g.shift_x // 4 + (event // 2) % 2
            ty = 2 * wy + g.shift_y // 4 + (event // 4) % 2
            inner = 1024 * (event // 8) + 512 * (event % 2) + 16 * lane + byte
        else:
            tx = 2 * wx + g.shift_x // 4 + event % 2
            ty = 2 * wy + g.shift_y // 4 + event // 2
            inner = 2048 * z + 512 * y + 16 * lane
        if not (0 <= tx < g.W // 4 and 0 <= ty < g.H // 4):
            return -1
        return 8192 * (ty * (g.W // 4) + tx) + inner
    if field == 'xsite_src':
        return -3
    if field == 'xsite_wsrc':
        return 917504 + 4 * head + byte
    if field == 'shfl_idx':
        phase = event % 36
        if phase < 4:
            return 4 * (lane % 8) + ((lane // 8) ^ phase)
        j = phase - 4
        return lane // 4 + 8 * (j % 2) + 16 * (j // 16)
    if field == 'psel':
        phase = event % 16
        bit = (0, 1, 3, 4)[phase // 4]
        value = (lane >> bit) & 1
        return value if phase < 4 else 1 - value
    raise KeyError(field)


def selected_values(archive, field, coordinates, header):
    """Read individual C-order NPY cells from a ZIP stream, without loading a whole array."""
    with archive.open(field + '.npy', 'r') as stream:
        version = np.lib.format.read_magic(stream)
        if version == (1, 0):
            shape, fortran, dtype = np.lib.format.read_array_header_1_0(stream)
        elif version == (2, 0):
            shape, fortran, dtype = np.lib.format.read_array_header_2_0(stream)
        else:
            raise ValueError('Unexpected NPY header version')
        assert list(shape) == header['shape'] and not fortran and not dtype.hasobject
        assert dtype == np.dtype(header['dtype'])
        start = stream.tell()
        indexed = []
        for coord in coordinates:
            flat = int(np.ravel_multi_index(coord, shape, order='C'))
            indexed.append((flat, coord))
        values = {}
        for flat, coord in sorted(indexed):
            stream.seek(start + flat * dtype.itemsize)
            data = stream.read(dtype.itemsize)
            assert len(data) == dtype.itemsize
            values[coord] = int(np.frombuffer(data, dtype=dtype, count=1)[0])
        return values, stream.tell()


def main():
    sys.dont_write_bytecode = True
    formula_path = safe(ROUND / 'formula_qkv.py')
    inventory_path = safe(ROUND / 'INVENTORY.json')
    assert sha(formula_path) == FORMULA_SHA, 'Frozen formula identity changed; stop'
    assert sha(inventory_path) == INVENTORY_SHA, 'Frozen inventory identity changed; stop'
    lock = read_json(ROUND / 'FREEZE.json')
    assert lock['formula_sha256'] == FORMULA_SHA and lock['inventory_sha256'] == INVENTORY_SHA
    assert sha(ROUND / 'FORMULAS_ZH.md') == lock['formula_explanation_sha256']
    source_pins = {name: sha(ROUND / name) for name in
                   ('RESULT_ZH.md', 'FORMULAS_ZH.md', 'formula_qkv.py', 'FREEZE.json', 'INVENTORY.json', 'SUMMARY.json')}
    spec = importlib.util.spec_from_file_location('r04n_frozen_qkv_formula', formula_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    inventory = read_json(inventory_path)
    # Base lane is 5; later psel samples also use lane 21 to check its zero result.
    # Warp/head-within-group is 2. Each geometry uses one window and head group.
    events = {
        'wload_off': [(0, 0), (95, 0), (96, 0), (111, 0)],
        'sread_shared_off': [(0, 0), (16, 0), (63, 0)],
        'sread_src': [(0, 0), (0, 15), (6, 7), (63, 15)],
        'xsite_src': [(0, 0), (1, 3)], 'xsite_wsrc': [(0, 0), (1, 3)],
        'gstore_off': [(0, 0), (3, 0)],
        'shfl_idx': [(0, 0), (3, 0), (4, 0), (35, 0), (36, 0), (71, 0)],
        'psel': [(0, 0), (4, 0), (8, 0), (12, 0), (16, 0), (31, 0)]}
    rows, tables, stream_prefix_bytes = [], [], 0
    for label, h, w, wx, wy in [('1080', 36, 60, 0, 0), ('4K', 68, 120, 1, 1)]:
        geometry = dict(H=h, W=w, shift_x=-4, shift_y=-4)
        candidates = [r for r in inventory['tables'] if r.get('geometry') == geometry and
                      not any(GUARD in part.lower() for part in Path(r['path']).parts)]
        candidate = min(candidates, key=lambda r: (r['bytes'], len(r['path']), r['path']))
        path = safe(candidate['path'])
        assert sha(path) == candidate['sha256'], 'Stored map identity changed; stop'
        g = module.Geometry(**geometry)
        a, y, lane = wy * g.GX + wx, 2, 5
        tables.append(dict(label=label, path=str(path), sha256=candidate['sha256'], set=candidate['set'],
                           geometry=geometry, window=[wx, wy], GX=g.GX, GY=g.GY, Q=g.Q, A=g.A,
                           a=a, y=y, lane=lane))
        with zipfile.ZipFile(path, 'r') as archive:
            for field in CLOSED_FIELDS:
                cases = events[field]
                coords = []
                for event, byte in cases:
                    case_lane = 21 if field == 'psel' and event >= 12 else lane
                    coord = (a, y, case_lane, event, byte) if field in ('sread_src', 'xsite_src', 'xsite_wsrc') else (a, y, case_lane, event)
                    coords.append(coord)
                values, prefix = selected_values(archive, field, coords, candidate['headers'][field])
                stream_prefix_bytes += prefix
                for (event, byte), coord in zip(cases, coords):
                    frozen = int(module.value(field, g, a, y, coord[2], event, byte))
                    transcribed = document_value(field, g, a, y, coord[2], event, byte)
                    stored = values[coord]
                    assert frozen == transcribed == stored, (label, field, coord, frozen, transcribed, stored)
                    row = dict(geometry=label, field=field, coordinate=list(coord), formula=frozen,
                               document_formula=transcribed, stored=stored, status='EXACT')
                    rows.append(row)
                    print(label, field, coord, 'formula', frozen, 'stored', stored, 'EXACT')
    for name, pin in source_pins.items():
        assert sha(ROUND / name) == pin, 'Research file changed during sample check; stop'
    for table in tables:
        assert sha(table['path']) == table['sha256'], 'Stored map changed during sample check; stop'
    result = dict(status='PASS', scope='58 selected address/index cells, not a full map/model/chain run',
                  formula_sha256=FORMULA_SHA, research_source_sha256=source_pins,
                  source_tables=tables, rows=rows, samples=len(rows), mismatches=0,
                  uncompressed_prefix_bytes_read=stream_prefix_bytes,
                  thread_class='NOT_CHECKED_HERE; frozen hypothesis failure retained from research',
                  new_GPU_runs=0, new_model_runs=0, new_chain_runs=0, new_compile_runs=0,
                  external_writes=0, network_calls=0, remote_calls=0, version_control_calls=0)
    (HERE / 'r04n.qkv_samples.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PASS', len(rows), 'selected address/index cells; full map/model/chain runs 0')


if __name__ == '__main__':
    main()
