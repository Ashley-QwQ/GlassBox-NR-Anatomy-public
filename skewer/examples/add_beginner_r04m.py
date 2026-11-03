"""Insert an additive beginner layer, preserving the existing expert text."""
from pathlib import Path
import json
import re

HERE=Path(__file__).resolve().parent
BASE=HERE.parent

INTRO={
'L3_b0_input.md': '''<a id="beginner-b0"></a>
【入门简化】这16格是送给网络的条件清单，不是16种颜色。前三项扰动另由位置/计数生成，不是从原图测出的颗粒；条件的总体视觉目的仍未知。无可用历史时，旧RGB三格重复当前RGB。接着每位置16项变32项，再在小窗口处理。

| 0：扰动 | 1：扰动 | 2：扰动 | 3：常数1 |
|---|---|---|---|
| 4：当前R | 5：当前G | 6：当前B | 7：旧R或当前R |
| 8：旧G或当前G | 9：旧B或当前B | 10：style | 11：tone |
| 12：structure | 13：条件值 | 14：条件值 | 15：常数0 |

当前/旧RGB在入格前各有规定变换；默认非p5时13/14是−1，p5分支改读两个标量条件且structure=1，不是另采两张遮罩图。[现有通道合同](#channels)。先看[当前点怎样去旧图取数](L1_00_history_primer.md#moving-point)和[五点内还含四邻域](L1_00_history_primer.md#nested-sampling)，再读下面的散列、精确坐标和字节解包。''',
'L3_ffn.md': '''<a id="beginner-ffn"></a>
【入门简化】先让每个位置各自重组自己的数字串，经过逐项函数，再组合回原项数；这段不向别处取内容，随后注意力才做位置间交换。甲的2项→4项→逐项函数→2项，乙也独立走自己的线，见[人工双位置图](L1_00_one_block_primer.md#per-position)。一条旁路来自块入口，在收缩开始带入；另一条来自前馈结果，在注意力后投影开始带入，[完整两线图](L1_00_one_block_primer.md#two-residuals)先于下面的家族细表阅读。''',
'L3_tin_window.md': '''<a id="beginner-tin"></a>
【入门简化】一个小窗口内，先各位置改自己的通道，再比较位置、组合内容，两条较早的数字各在规定的起始小计处接回。先画少框版：

~~~mermaid
flowchart LR
    X["入口数字"] --> F["各位置处理 + 接回入口旁路"] --> Z["前馈结果"] --> A["窗口内交换内容"] --> P["输出投影 + 接回前馈结果旁路"] --> Y["块结果"]
    X -. "第一旁路" .-> F
    Z -. "第二旁路" .-> P
~~~

“接回”在矩阵累加起始小计处，非整段算完才加。窗口是位置范围，头是比较数字的分组，FFN组与设备工作分组又不同。[从一头块学起](L1_00_one_block_primer.md)后，下面保留多头、上下采样及格式差别。''',
'L3_split16_window.md': '''<a id="beginner-split"></a>
【入门简化】这段让每位置512项数经过八个窗口块。每块先各位置处理，再在8×8位置内交换内容；入口旁路接前馈收缩，前馈结果旁路接注意力后投影。少框版是：

~~~mermaid
flowchart LR
    X["块入口"] --> F["逐位置处理；收缩起点接入口旁路"] --> Z["前馈结果"] --> A["窗口比较与内容混合"] --> P["投影起点接前馈旁路"] --> Y["块出口"]
    X -. "第一条" .-> F
    Z -. "第二条" .-> P
~~~

位置网格→窗口→16个比较头→每头32项，是一套逻辑关系；FFN八组与设备执行坐标另算，见[四种分组](L1_00_one_block_primer.md#groups)。末端变稀与桥接的独立空间配对仍有问号，下面DAG合同不把未知抹掉。''',
'L3_attention_softmax.md': '''<a id="beginner-attention"></a>
【入门简化】当前位置用Q与候选位置的K比较，再按份额取它们的V内容；Q/K/V都由内部数生成。先用[三位置故事与并排分数表](L1_00_one_block_primer.md#qkv-story)理解谁比较、谁被取回。普通softmax先取指数再除总量；本链先按规定改编码生成正权重，训练意图未定。窗口“除总量→转粗格式→组合V”，全局“转粗格式→组合V→除总量”，[两条四格线](L1_00_one_block_primer.md#quantisation-position)把转换标出；这不是可随意交换的实数平均。''',
'L3_norm_nonfinite.md': '''<a id="beginner-norm"></a>
【人工概念例，非测量】(3,4)的平方和是25、长度是5；都乘1/5变(0.6,0.8)。把输入换成(6,8)，长度也成倍，整体缩放后仍得同一方向。这里仅用两项和理想实数说明“调一组数的大小”，不冒充实际32项与函数表的结果。

真实步骤只在投影后对Q、K各自每组32项做平方和缩放，V不做；不先减均值，也不在平方和上加ε，而是取规定下限。查询的另一尺度随后另乘，不能混成一个旋钮。非有限传播、精确加法树及独立A1分支继续留在下面。''',
'L3_qmma_e4m3.md': '''<a id="beginner-qmma"></a>
【入门简化】把一行与一列对应相乘再相加时，这条规则每次处理32对，带入一个小计，先把各项朝零放到同一刻度，再加起来、保存F16小计；下一篮用这个已保存结果继续。有些出口还要转成更粗E4。先读[有限数点与小篮](L1_00_numbers_primer.md)，再下钻下面的整数式、候选和证据范围；篮子是教学比喻，不是设备内部结构证明。''',
'L3_b70_history_output.md': '''<a id="beginner-tail"></a>
【入门简化】先区分四个对象：①三个预测数改动RGB；②有历史时的第四预测数参与混合份额；③结果图的第四存储分量固定为1；④显示强度控制最后与本帧原图备份的混合。②③④不是同一个第四数。默认先保存显示前状态，再另做显示；[两帧加reset时间线](L1_00_history_primer.md#timeline)先于坐标/颜色细式阅读。B70资源置信尺度先检查，允许才取旧图；B0条件历史是另一条路径。

<a id="beginner-colour"></a>
![人工颜色概念色样，非网络前后画面](examples/r04m.colour_cards.svg)

这些人工色样只教概念：色相是红/绿等色类，饱和度表示离灰多远，亮度式量反映明暗的一种计算约定，不等于物理照度。真实颜色链先做数值曲线，再有两轮分解/重组；临时通道次序不是最终RGB：

~~~mermaid
flowchart LR
    X["显示前颜色"] --> C["增益与曲线"] --> F["第一轮：按极值分解三量"] --> S["调整饱和度"] --> T["按临时通道顺序重组"] --> R["第二轮：按另一顺序分解"] --> S2["幂式饱和度变换"] --> RGB["重组成最终RGB"] --> I["与本帧备份按显示强度混合"]
~~~

这是下方[真实两轮接线](#post-reconstruct)的简化，不用人工色样宣称实际画面效果，也不将它替换成标准库的一次颜色空间往返。''',
'L3_workspace_map.md': '''<a id="beginner-storage"></a>
【人工存放示意】同一组(a,b,c,d)，可按两行(a,b)/(c,d)放，也可在存储中按(a,c,b,d)放；重排只换盒子，解读后仍是原来的四个数。实际规则不是随便选一种排列，需按本实例合同。读图时分三格：“从哪取数→做什么算术→往哪写数”。

~~~text
逻辑有效格：  ■ ■     实际分配格： ■ ■
              ■ ■                 ■ ■
                                  □ □  额外补齐格
~~~

□可能真被写零、被后面读取，不能自动当垃圾；内部补齐也不等于显示图变大。工作区同时放中间数和管理标记，旧字节的最小跨帧必需集合仍[未定](L1_00_history_primer.md#workspace-memory)。新手先读角色与重排含义，下面的地址表、写集、零覆盖及完成标记是专家核对层。'''
}

L1=[
('L1_01_prepare.md','🖼 接本帧当前图 → 留一份原图备份；🗃 只设置指定管理区 → 交输入计算，并把备份留给显示。'),
('L1_02_input_b0.md','🖼 接当前图、移动信息、可用旧图与控制 → 🔢 凑16项条件并变成32项内部数 → 一路交编码，一路留到末端。'),
('L1_03_tin_encoder.md','🔢 接输入端较稀的一路 → 经过四档更稀网格、每位置项数增加，并各存一条旁路 → 交深层窗口段。'),
('L1_04_split16_encoder.md','🔢 接四档编码的出口 → 在小窗口内连续处理八块，再分出较稀主路与一份保留旁路 → 主路交全局段、旁路交桥。'),
('L1_05_vit.md','🔢 接最小网格的数字 → 换成按位置排列的序列，让每位置与全部有效位置交换内容，再换回二维组织 → 交解码桥。'),
('L1_06_decoder_bridge.md','🔢 接全局段主路与瓶颈前保留旁路 → 已知四组通道按序合并并接回旁路；完整空间恢复算子？仍未定 → 交较密网格的窗口解码段。'),
('L1_07_split16_decoder.md','🔢 接桥输出的每位置512项数 → 连续八块窗口处理并交出后续需要的存放组织 → 交四档变密阶段。'),
('L1_08_tin_decoder.md','🔢 接深层解码出口与四条编码旁路 → 四次变密并接回同档旁路、每位置项数回到32 → 交末端，主路宽高仍各为内部画布一半。'),
('L1_09_b70.md','🔢 接半密主路、入口保存的一路及🖼 当前/可用历史颜色 → 预测颜色修正、按条件另取旧色混合 → 交本帧新颜色状态。'),
('L1_10_output.md','🖼 接本帧新颜色状态与原图备份 → 一路保存为下帧历史，另一路作显示调整与强度混合 → 交同输入尺寸的显示图。'),
]
EXPERT=[f'L2_{n:02}_'+s+'.md' for n,s in enumerate((
    'prepare','b0','tin_encoder','split16_encoder','vit','decoder_bridge',
    'split16_decoder','tin_decoder','b70','output'),1)] + [
    'L4_e4m3_and_k32.md','L4_half_arith.md','L4_hmma.md','L4_fp32_ftz.md','L4_mufu.md','L4_tex_filter.md',
    'APPENDIX_evidence_history.md','APPENDIX_cpu_storage.md']

ROUNDING='''<a id="beginner-rounding"></a>
先读[有限数点与小篮](L1_00_numbers_primer.md)；下表把“保存在哪里”分开，不把软件中间格式推为硬件内部结构。

| 操作 | 应保留的舍入位置与范围 |
|---|---|
| 普通half加/乘 | 当前软件先binary64运算再RN16；有限half的这两类中间运算可精确表示 |
| 软件half融合乘加 | binary64融合结果→RN16，乘积不先单独存half；软件合同，不改成另一参考 |
| 本目标32项步 | 各项与seed先朝零放公共格→精确和→RN16；每步再反馈小计 |
| 16项步 | 按其独立公共格/seed规则→half；负零等边界仍未普遍关闭，不能借32项规则代替 |
| 最终颜色 | 保留各F32站点与拒绝/冲零，指定出口才RZ16；不是上面任一通用末端RN16 |
'''

def block(tag,text):
    return '<!-- beginner-r04m:start '+tag+' -->\n'+text.strip()+'\n<!-- beginner-r04m:end '+tag+' -->'

def add_top(name,tag,text):
    p=BASE/name;t=p.read_text(encoding='utf-8')
    assert 'beginner-r04m:start '+tag not in t
    head,rest=t.split('\n',1)
    p.write_text(head+'\n\n'+block(tag,text)+'\n'+rest,encoding='utf-8')

def main():
    edits=[]
    for name,text in INTRO.items():
        add_top(name,'intro',text);edits.append({'page':name,'kind':'beginner_paragraph'})
    for name,text in L1:
        title=(BASE/name).read_text(encoding='utf-8').splitlines()[0]
        match=re.search(r'（launch (.*?) / (.*?)）',title)
        assert match,name
        launch,logical=match.groups()
        caption='阅读深度：L1（阶段）<br>执行编号：launch '+launch+'<br>逻辑块编号：'+logical
        add_top(name,'stage',caption+'\n\n【入门交接】'+text+'\n\n固定图标：🖼 图像；🔢 内部数字；🗃 管理存储。这里只讲接谁、改什么、交给谁；精确形式在下方。')
        edits.append({'page':name,'kind':'beginner_stage'})
    for name in EXPERT:
        extra=''
        if name=='L4_half_arith.md':extra='\n\n'+ROUNDING
        if name=='L4_tex_filter.md':extra='\n\nCB+0x40是某次参数包内的字节位置（具体消费者可读资源句柄），1/256是过滤内部的坐标/权重刻度；两者不是同一名字，也没有这里给出的字段控制该刻度的关系。取样的新手图见[五点/四角嵌套](L1_00_history_primer.md#nested-sampling)。'
        add_top(name,'expert','> 新手可跳过；需要时再读。先完成[整帧](L0_frame.md#beginner-frame)、[一块](L1_00_one_block_primer.md)和[数点](L1_00_numbers_primer.md)，本页保留精确合同与证据。'+extra)
        edits.append({'page':name,'kind':'expert_banner'})
    p=BASE/'L3_workspace_map.md';t=p.read_text(encoding='utf-8')
    for anchor in ('write-sets','padding','address-maps','release-contract-r04l','wr'):
        marker='<a id="'+anchor+'"></a>'
        assert t.count(marker)==1
        t=t.replace(marker,block('expert-'+anchor,'> 新手可跳过；需要时再读。这一段核对存储/执行范围，不增加一层网络。')+'\n\n'+marker)
    p.write_text(t,encoding='utf-8');edits.append({'page':p.name,'kind':'expert_sections','anchors':['write-sets','padding','address-maps','release-contract-r04l','wr']})
    (HERE/'r04m.layers.json').write_text(json.dumps({'beginner_pages':['INDEX.md','L0_frame.md']+list(INTRO)+[n for n,_ in L1], 'banner_pages':EXPERT,'edits':edits},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('beginner pages',2+len(INTRO)+len(L1),'banner pages',len(EXPERT),'expert sections',5)

if __name__=='__main__':main()
