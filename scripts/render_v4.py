#!/usr/bin/env python3
# v4 paired figures: proof-DAG (graphviz, left-to-right, examples hanging below stages) + time-band
# plot (IDL). Examples coloured by generative MAJORITY: illustrative=purple, generative=orange,
# tie/uncoded(from_question)=grey. Examples flagged essential are omitted. No titles, no legends.
#   python3 render_v4.py [key ...]      (default: all of json_v4)
import json, glob, os, sys, subprocess
ROOT="/Users/simon/Desktop/DANIEL/analysis/talk_structure"
SCRIPTS=f"{ROOT}/scripts"; V4=f"{ROOT}/json_v4"
DAG=f"{ROOT}/dag"; BANDS=f"{ROOT}/bands"
for d in (DAG,BANDS): os.makedirs(d, exist_ok=True)
PURPLE,ORANGE,GREY="#8c6bb1","#e8902a","#b8b8b8"; SF,SL="#dde6f2","#34557f"

def drawn(g):  # all examples except essential, ordered by first appearance
    ex=[e for e in g['examples'] if not e.get('essential')]
    return sorted(ex, key=lambda e: e.get('first_introduced_sec') or 0)
def color(e):                       # by generative majority (Q&A included; flagged via dashed border)
    s=e.get('generative_score',3)
    return ORANGE if s>=4 else (PURPLE if s<=2 else GREY)
def longof(h):
    h=h.lstrip('#'); return int(h[0:2],16)+int(h[2:4],16)*256+int(h[4:6],16)*65536

EXW, EXH, ROWGAP, SEP = 0.55, 0.40, 0.72, 0.78   # inches: example box w/h, row spacing, min x-sep

def _stage_coords(stages, sids):
    # Phase 1: let dot lay out the stage DAG (L->R), read back stage x,y via -Tplain.
    L=['digraph G {','  rankdir=LR; nodesep=0.30; ranksep=0.65;',
       '  node[shape=box, width=0.55, height=0.42, fixedsize=true];']
    for s in stages: L.append(f'  {s["id"]};')
    for a,b in zip([s["id"] for s in stages],[s["id"] for s in stages][1:]):
        L.append(f'  {a} -> {b} [style=invis, weight=100];')
    for s in stages:
        for d in s['depends_on']:
            if d in sids: L.append(f'  {d} -> {s["id"]};')
    L.append('}')
    out=subprocess.run(['dot','-Tplain'], input='\n'.join(L), capture_output=True, text=True).stdout
    pos={}
    for ln in out.splitlines():
        t=ln.split()
        if t and t[0]=='node': pos[t[1]]=(float(t[2]), float(t[3]))
    return pos

def build_dag(g, key):
    stages=g['proof_stages']; ex=drawn(g); sids={s['id'] for s in stages}
    pos=_stage_coords(stages, sids)
    if not pos: return
    y0=min(y for _,y in pos.values())                 # stage row baseline
    # target x for each example = mean x of its attached stages
    tx=[]
    for e in ex:
        att=[a for a in e['attaches_to'] if a in pos]
        tx.append(sum(pos[a][0] for a in att)/len(att) if att else sum(p[0] for p,_ in [(p,0) for p in pos.values()])/len(pos))
    # greedy lane packing: minimal #rows with no horizontal overlap, in x order
    order=sorted(range(len(ex)), key=lambda i: tx[i])
    rows=[]; rowof={}
    for i in order:
        placed=False
        for r,xs in enumerate(rows):
            if all(abs(tx[i]-x)>=SEP for x in xs): xs.append(tx[i]); rowof[i]=r; placed=True; break
        if not placed: rows.append([tx[i]]); rowof[i]=len(rows)-1
    # Phase 2: fixed positions (points), rendered with neato -n
    P=lambda x,y: f'pos="{x*72:.1f},{y*72:.1f}!"'
    L=['digraph G {','  graph[splines=true]; node[fontname=Helvetica, fixedsize=true]; edge[fontname=Helvetica];']
    for s in stages:
        x,y=pos[s['id']]
        L.append(f'  {s["id"]} [{P(x,y)}, shape=box, style="filled,rounded", fillcolor="{SF}", '
                 f'color="{SL}", penwidth=1.6, width=0.55, height=0.42, label=<<b>{s["code"]}</b>>];')
    for s in stages:
        for d in s['depends_on']:
            if d in sids: L.append(f'  {d} -> {s["id"]} [color="{SL}", penwidth=1.6];')
    for i,e in enumerate(ex):
        c=color(e); x=tx[i]; y=y0-(rowof[i]+1)*ROWGAP
        bcol,bpw=("#e41a1c",3.2) if e.get('from_question') else ("#555555",1.2)   # Q&A: thick red border
        L.append(f'  e{i} [{P(x,y)}, shape=box, style="filled", fillcolor="{c}", color="{bcol}", penwidth={bpw}, '
                 f'fontsize=10, width={EXW}, height={EXH}, label=<<b>E{i+1}</b>>];')
        att=[a for a in e['attaches_to'] if a in sids]
        for j,sid in enumerate(att):
            st="penwidth=1.7" if j==0 else "penwidth=0.8, style=dashed"
            L.append(f'  {sid} -> e{i} [dir=none, color="{c}", {st}];')
    L.append('}')
    open(f'{DAG}/{key}_dag.dot','w').write('\n'.join(L))

def bands_txt(g):
    stages=g['proof_stages']; ex=drawn(g)
    lanes=[]; blocks=[]; xmax=0.0
    for s in stages:
        li=len(lanes); lanes.append(s['code'])
        for sp in s['spans']:
            blocks.append((li,longof(SF),sp['start_sec']/60.0,sp['end_sec']/60.0,0)); xmax=max(xmax,sp['end_sec']/60.0)
    nstage=len(lanes)
    for i,e in enumerate(ex):
        li=len(lanes); lanes.append(f'E{i+1}'); c=longof(color(e)); d=1 if e.get('from_question') else 0
        for sp in e['spans']:
            blocks.append((li,c,sp['start_sec']/60.0,sp['end_sec']/60.0,d)); xmax=max(xmax,sp['end_sec']/60.0)
    out=[f"# title {g.get('title')}", f"# xmax {int(xmax)+1}", f"# nlane {len(lanes)}", f"# nstage {nstage}"]
    out+=[f"@LANE\t{i}\t{l}" for i,l in enumerate(lanes)]
    out+=[f"@BLOCK\t{li}\t{col}\t{a:.3f}\t{b:.3f}\t{d}" for li,col,a,b,d in blocks]
    return '\n'.join(out)+'\n'

keys=sys.argv[1:] or [os.path.basename(f).replace('_structure.json','') for f in sorted(glob.glob(f'{V4}/*_structure.json'))]
rlist=[]
for k in keys:
    g=json.load(open(f'{V4}/{k}_structure.json'))
    build_dag(g,k)
    open(f'{BANDS}/{k}_bands.txt','w').write(bands_txt(g))
    rlist.append(f'{BANDS}/{k}_bands.txt\t{BANDS}/{k}_bands.ps')
print(f'wrote {len(keys)} dot + band tables')
# DAGs (neato -n: use the fixed positions as-is, route edge splines)
for k in keys:
    subprocess.run(['neato','-n','-Tpdf',f'{DAG}/{k}_dag.dot','-o',f'{DAG}/{k}_dag.pdf'], stderr=subprocess.DEVNULL)
# bands via one IDL session, then ps2pdf
lf=f'{BANDS}/_render_list.txt'; open(lf,'w').write('\n'.join(rlist)+'\n')
subprocess.run(f'cd {SCRIPTS} && BANDLIST={lf} idl -quiet -e ts_render_bands_v4', shell=True)
for k in keys:
    ps=f'{BANDS}/{k}_bands.ps'
    if os.path.exists(ps): subprocess.run(['ps2pdf','-dEPSCrop',ps,f'{BANDS}/{k}_bands.pdf'], stderr=subprocess.DEVNULL)
print('done')
