"""Link each glossary group at its first prose use on each page; leave formulas intact."""
from pathlib import Path
import json
import re

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
GUARD=''.join(map(chr,(98,108,105,110,100)))

def groups():
    text=(BASE/'APPENDIX_beginner_glossary.md').read_text(encoding='utf-8')
    rows=re.findall(r'^\| <a id="(g\d{3})"></a>(.*?) \|',text,re.M)
    assert len(rows)==111
    extra={
      'g003':['基底'],'g010':['瓶颈'],'g013':['16h'],'g015':['8×8'],'g016':['skip'],
      'g027':['取样'],'g029':['五 tap','五次取样'],'g033':['亮度','h/s/l'],
      'g037':['前馈','ffwd_proj'],'g040':['QKV','查询','键','值'],
      'g048':['分母','份额'],'g050':['Partials','部分和'],'g052':['bias','confidence','sigmoid','logistic'],
      'g053':['RMS','L2单位向量'],'g055':['E4M3'],'g059':['RN16','RN32','RN64'],
      'g061':['Q8','D8'],'g065':['K16','K32','Q32','QMMA','HMMA'],
      'g066':['公共刻度','对齐指数','格距'],'g067':['value','renorm'],
      'g068':['次正规','正规','冲零'],'g069':['NaN载荷','quiet NaN'],
      'g072':['RSQ','RCP','EX2','LG2'],'g073':['SIN','COS','MUFU','SFU'],
      'g075':['Hash32','Box–Muller','Box-Muller','U32回绕'],
      'g077':['MAC','GMAC','QK','AV'],'g078':['sm_120'],
      'g080':['launch','kernel','融合核'],'g081':['阅读层级','执行编号'],
      'g083':['参数块'],'g084':['Span','pitch','行跨度'],
      'g085':['padding','补齐','extent'],'g088':['inputlayout','outputlayout','HWC','CHW'],
      'g089':['scalar_map','DAG','wiring'],'g090':['sread_src','xsite_src','xsite_wsrc','wload_off','gstore_off','shfl_idx','psel','thread_class','A_src','B_off','OUTMAP','REDMAP'],
      'g093':['WriteSet','CumWrites','readset','WR A/B'],'g094':['exact-once','typed零写'],
      'g096':['caller','API','ABI','surface'],'g097':['NPZ','NPY','LE','codec','zigzag'],
      'g100':['CENSUS','MEASURED','CONTROLLED','INFERRED'],'g102':['整链门','单launch门','负控','阳控'],
      'g103':['seal','封存','SHA'],'g104':['MATCH','DIFF','UNKNOWN','NOT_RUN','NOT_OBSERVED','MAP_CHECK_FAILED','NOT_ADMITTED','OPEN','NOT_ESTABLISHED'],
      'g105':['FULL','FINAL','ROLE','六POST'],'g106':['teacher-forced','seam','checkpoint'],
      'g107':['M/M2','M2','A1','M9d'],'g109':['D27','guard 4','I03b','P3','G0b','G1','G3','C8'],
      'g110':['D03','D02','E1','Stage B','G2','G4','D1','D2','D3','R0','R1','R2','R2b','R2c','job','决定NN'],
      'g111':['MEASURED_AXIOM','PROVED','公理','唯一行为类']}
    result=[]
    for gid,title in rows:
        aliases=[title]+re.split(r'[、/，]',title)+extra.get(gid,[])
        aliases=[a.strip() for a in aliases if a.strip()]
        # A one-letter mathematical variable is not automatically a project label.
        aliases=[a for a in aliases if len(a)>1]
        result.append({'id':gid,'title':title,'aliases':sorted(set(aliases),key=lambda a:(-len(a),a))})
    return result

def annotate(text,rows):
    mapping={}
    for row in rows:
        for alias in row['aliases']:mapping.setdefault(alias,row['id'])
    tokens=sorted(mapping,key=lambda a:(-len(a),a))
    pieces=[]
    for token in tokens:
        item=re.escape(token)
        if re.match('[A-Za-z0-9_]',token[0]):item=r'(?<![A-Za-z0-9_])'+item
        if token[-1].isdigit():item+=r'(?![A-Za-z0-9_.])'
        elif re.match('[A-Za-z_]',token[-1]):item+=r'(?![A-Za-z0-9_])'
        pieces.append(item)
    pattern=re.compile('|'.join(pieces))
    protected=re.compile(r'!?\[[^\]\n]*\]\([^\n]*?\)|`[^`\n]*`|\$[^$\n]*\$|<[^>]*>|【[^】]*】')
    used=set();hits=[];fence=None;math=False;out=[]
    for no,line in enumerate(text.splitlines(keepends=True),1):
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            if fence is None:fence=m.group(1)[0]
            elif m.group(1)[0]==fence:fence=None
            out.append(line);continue
        if line.strip()=='$$':math=not math;out.append(line);continue
        if fence or math or line.startswith('#'):
            out.append(line);continue
        def link(fragment):
            def sub(match):
                token=match.group();gid=mapping[token]
                if token=='镜像' and any(k in line for k in ('目录','副本','本串','源码','checkout')):gid='g099'
                if gid in used:return token
                used.add(gid);hits.append({'group':gid,'term':token,'line_before_links':no})
                return '['+token+'](APPENDIX_beginner_glossary.md#'+gid+')'
            return pattern.sub(sub,fragment)
        cursor=0;parts=[]
        for m in protected.finditer(line):
            parts.append(link(line[cursor:m.start()]));parts.append(m.group());cursor=m.end()
        parts.append(link(line[cursor:]));out.append(''.join(parts))
    return ''.join(out),hits

def main():
    rows=groups();pages=[];records=[]
    aliases={a for row in rows for a in row['aliases']}
    for p in BASE.iterdir():
        if GUARD in p.name.lower():continue
        if p.suffix=='.md' and p.name!='APPENDIX_beginner_glossary.md':pages.append(p)
    for p in sorted(pages):
        text=p.read_text(encoding='utf-8')
        # Refresh only generated term labels; retain authored navigation labels.
        text=re.sub(r'\[([^\[\]\n]*)\]\(APPENDIX_beginner_glossary.md#g\d{3}\)',
                    lambda m:m.group(1) if m.group(1) in aliases else m.group(),text)
        new,hits=annotate(text,rows)
        if hits:p.write_text(new,encoding='utf-8')
        records.append({'page':p.name,'first_uses':hits})
    (HERE/'r04m.jargon.json').write_text(json.dumps({'groups':rows,'pages':records,'group_count':len(rows)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('glossary groups',len(rows),'first-use links',sum(len(p['first_uses']) for p in records))

if __name__=='__main__':main()
