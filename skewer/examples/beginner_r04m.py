"""Made-up teaching numbers and static SVGs only; no project numerical modules."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import struct

HERE=Path(__file__).resolve().parent

def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
def half(x):return struct.unpack('<e',struct.pack('<e',x))[0]
def hbits(x):return struct.unpack('<H',struct.pack('<e',x))[0]
def hvalue(x):return struct.unpack('<e',struct.pack('<H',x))[0]

def phi(s):
    # Existing TIN reference order; constants are algorithm constants.
    affine=f32(f32(half(s)*f32(0.044921875))+f32(1.30078125))
    c=min(max(half(affine),half(1.03125)),half(1.5693359375))
    return hvalue(((hbits(c)<<5)+0x8000)&65535)

def score_svg():
    pts=[]
    for i in range(129):
        x=-8+i/8; y=math.log2(phi(x))
        pts.append(f'{70+(x+8)*40:.2f},{270-(y+16)*10:.2f}')
    lines=['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="340" viewBox="0 0 800 340">',
           '<rect width="800" height="340" fill="#fffaf0"/>',
           '<g font-family="sans-serif" fill="#202830"><text x="28" y="28" font-size="18">人工公式示意：窗口 score → φ(score)，非画面测量</text>',
           '<text x="28" y="51" font-size="13">纵轴 log2(w)：用对数刻度看编码变换；不是把数值乘32</text>',
           '<path d="M70 70V270H730" fill="none" stroke="#333"/>']
    for x in (-8,-4,0,4,8):
        px=70+(x+8)*40;lines.append(f'<text x="{px-8}" y="294">{x}</text>')
    for y in (-16,-12,-8,-4,0,4):
        py=270-(y+16)*10;lines.append(f'<text x="28" y="{py+4}">{y}</text>')
    lines+=['<text x="680" y="320">score</text></g>',
            '<polyline fill="none" stroke="#b04d19" stroke-width="3" points="'+' '.join(pts)+'"/>',
            '</svg>']
    (HERE/'r04m.score_curve.svg').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def colour_svg():
    rows=[('色相：不同色类',['#ff0000','#00ff00','#0000ff']),
          ('饱和度：向灰靠近',['#ff0000','#bf4040','#808080']),
          ('亮度式量：暗至亮',['#800000','#ff0000','#ff8080'])]
    lines=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="260" viewBox="0 0 720 260">',
           '<rect width="720" height="260" fill="#fffaf0"/>',
           '<g font-family="sans-serif" fill="#202830"><text x="20" y="27" font-size="18">人工颜色概念卡：不是网络前后画面</text>']
    for i,(label,colours) in enumerate(rows):
        y=48+i*62;lines.append(f'<text x="20" y="{y+23}">{label}</text>')
        for j,c in enumerate(colours):lines.append(f'<rect x="{245+j*145}" y="{y}" width="115" height="42" fill="{c}" stroke="#333"/>')
    lines+=['<text x="20" y="245" font-size="12">只教颜色坐标直觉；这里的明暗不是物理照度，也没有展示控制效果。</text></g></svg>']
    (HERE/'r04m.colour_cards.svg').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def run():
    scores=(-1,0,1);values=(2,4,8)
    ordinary=[math.exp(s-max(scores)) for s in scores]
    ordinary=[w/sum(ordinary) for w in ordinary]
    weights=[phi(s) for s in scores]
    ideal=[w/sum(weights) for w in weights]
    assert weights==[0.00927734375,0.025390625,0.06640625]
    assert [f'{w:.6f}' for w in ideal]==['0.091787','0.251208','0.657005']
    content=[sum(w*v for w,v in zip(row,values)) for row in (ordinary,ideal)]
    assert [f'{v:.4f}' for v in content]==['6.4809','6.4444']
    assert hbits(1.5)==0x3e00 and hvalue(((hbits(1.5)<<5)+0x8000)&65535)==2
    assert half(1+2**-11)==1
    assert half(1+2**-11+2**-18)==1+2**-10
    assert half(half(1+2**-11)+2**-18)==1
    assert int(Fraction(2**-18)/Fraction(2**-17))==0
    W=H=8;tx,ty=2,3;mx,my=.5,-.5;sx=sy=1/8
    ax=mx*sx+(tx+.5)/W;ay=my*sy+(ty+.5)/H
    x0=math.floor(W*ax-.5)+.5;y0=math.floor(H*ay-.5)+.5
    t=W*ax-x0;v=H*ay-y0
    assert (ax,ay,x0,y0,t,v)==(.375,.375,2.5,2.5,.5,.5)
    score_svg();colour_svg()
    result={'status':'PASS','scope':'made-up pedagogy, not a measurement or model run',
            'scores':scores,'contents':values,'ordinary_fractions':ordinary,'window_phi':weights,
            'window_ideal_fractions_before_real_rounding':ideal,'ideal_content_outputs':content,
            'B0_coordinate_example':{'size':[8,8],'current_index':[2,3],'motion':[mx,my],'scale':[sx,sy],
              'history_normalized':[ax,ay],'history_centre':[8*ax,8*ay],'history_continuous_index':[8*ax-.5,8*ay-.5],
              'base_centre':[x0,y0],'fraction':[t,v]},
            'new_GPU_runs':0,'new_model_runs':0,'new_chain_runs':0,'new_compile_runs':0}
    result['svg_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'r04m.score_curve.svg',HERE/'r04m.colour_cards.svg')}
    (HERE/'r04m.beginner_examples.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'ideal_content_outputs':content,'new_model_runs':0}))

if __name__=='__main__':run()
