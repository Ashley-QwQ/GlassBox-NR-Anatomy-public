"""Render only the two teaching SVGs locally, with an explicitly selected font."""
from pathlib import Path
import hashlib,json
import resvg_py

HERE=Path(__file__).resolve().parent
FONT=Path('C:/Windows/Fonts/msyh.ttc')

if __name__=='__main__':
    assert FONT.is_file()
    rows=[]
    for name in ('score_curve','colour_cards'):
        source=HERE/f'r04m.{name}.svg';target=HERE/f'r04m.{name}.png'
        data=resvg_py.svg_to_bytes(svg_string=source.read_text(encoding='utf-8'),
            skip_system_fonts=True,font_files=[str(FONT)],sans_serif_family='Microsoft YaHei')
        target.write_bytes(data)
        rows.append({'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'png':target.name,'png_sha256':hashlib.sha256(data).hexdigest()})
    (HERE/'r04m.render.json').write_text(json.dumps({'status':'PASS','scope':'offline teaching illustrations only','rows':rows},indent=2)+'\n',encoding='utf-8')
    print('rendered',len(rows))
