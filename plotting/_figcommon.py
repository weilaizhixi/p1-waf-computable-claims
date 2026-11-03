import os, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
CODE_DIR=Path(__file__).resolve().parent
FIG_DIR=Path(os.environ.get('P1_OUTPUT_DIR', str(CODE_DIR.parent/'outputs'/'analysis')))
MAP=json.loads((CODE_DIR/'chart_translation_map.json').read_text(encoding='utf-8'))
C={'blue_main':'#0A2C83','blue_secondary':'#2D51A4','red_strong':'#C25F4B','gold':'#D3BE00','neutral_dark':'#454545','neutral_black':'#272727','neutral_light':'#C5C5C5','teal':'#448393'}
COLORS={'text':'#000000','dark':'#000000'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.labelsize':9,'axes.titlesize':10,'xtick.labelsize':8.5,'ytick.labelsize':8.5,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.8,'svg.fonttype':'none','svg.hashsalt':'p1-v1.0.0','pdf.fonttype':42,'savefig.facecolor':'white'})
def convert(v):
 if isinstance(v,str):return MAP.get(v,v)
 if isinstance(v,list):return [convert(x) for x in v]
 if isinstance(v,dict):return {k:convert(x) for k,x in v.items()}
 return v
def load(name):return convert(json.loads((FIG_DIR/name).read_text(encoding='utf-8')))
def set_paper_placement(fig,**kwargs):pass
def finish(fig,name):
 for ext in ['png','svg','pdf']:
  metadata = {'Date': None} if ext == 'svg' else ({'CreationDate': None, 'ModDate': None} if ext == 'pdf' else {})
  fig.savefig(FIG_DIR/(name+'.'+ext),dpi=350,bbox_inches='tight',pad_inches=0.04,metadata=metadata)
 plt.close(fig)
