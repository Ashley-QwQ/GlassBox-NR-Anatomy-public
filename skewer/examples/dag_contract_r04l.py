"""Project existing L56/L57 arithmetic wiring; never load coefficients or run it."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
GUARD = ''.join(map(chr, (98, 108, 105, 110, 100)))

def safe(p):
    p = Path(p)
    assert all(GUARD not in x.lower() for x in p.parts)
    return p

def project(launch):
    p = safe(f'E:/dlssnr-work-e/1080-close-r04-codex/maps/s1080-v1/L{launch}-lane.wiring.json')
    raw = p.read_bytes()
    source = json.loads(raw)
    # Keep only semantic DAG indices, never original event address labels.
    events = source['gstore_pcs']
    if 'classes' in source:
        stores = [{'class': c['cls'], 'event': events.index(e),
                   'atoms': c['gstore_atoms'][str(e)]}
                  for c in source['classes'] for e in c['gstore_pcs']]
    else:
        stores = [{'class': None, 'event': j,
                   'atoms': source['gstore_atoms'][str(e)]}
                  for j, e in enumerate(events)]
    constants = [n[1] for n in source['nodes'] if n[0] == 'K']
    assert constants == ([13312] if launch == 56 else [0])
    return {'launch': launch, 'source': p.as_posix(),
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'scope': 'CPU table contract; no native provenance upgrade',
            'nodes': source['nodes'], 'matrices': source['mmas'],
            'stores': stores, 'event_count': len(events)}

if __name__ == '__main__':
    for launch in (56, 57):
        d = project(launch)
        (HERE / f'r04l.L{launch}.dag.json').write_text(
            json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        print(launch, len(d['nodes']), len(d['matrices']), len(d['stores']))
