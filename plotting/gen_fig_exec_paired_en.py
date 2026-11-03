# 图 4：48 题配对瓦片矩阵 (6 个应用 × 8 题；每格左半直接回答、右半程序执行)
# 数据：figures/fig_exec_paired_data.json (转录自 RESULTS.md G、H)
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _figcommon import *
from matplotlib.patches import Rectangle, Patch

d = load('fig_exec_paired_data.json')
apps = [a['app'] for a in d['apps']]
summ = {a['app']: a for a in d['apps']}
assert sum(a['direct'] for a in d['apps']) == 46
assert sum(a['program'] for a in d['apps']) == 48
assert sum(a['reverse'] for a in d['apps']) == 0

col_ok_direct = C['blue_main']
col_ok_prog = C['teal']
col_wrong = C['red_strong']

fig, ax = plt.subplots(figsize=(6.3, 3.5), layout='constrained')
set_paper_placement(fig, width_fraction=0.95)
gap = 0.08
th = 0.62  # 瓦片高度 (行距 1，留出上方标签空间)
for t in d['tiles']:
    r = apps.index(t['app'])
    y = len(apps) - 1 - r
    x = t['col'] - 1
    w = (1 - gap) / 2
    ax.add_patch(Rectangle((x + gap / 2, y), w, th,
                           facecolor=col_ok_direct if t['direct_correct'] else col_wrong,
                           edgecolor='none'))
    ax.add_patch(Rectangle((x + gap / 2 + w, y), w, th,
                           facecolor=col_ok_prog if t['program_correct'] else col_wrong,
                           edgecolor='none'))
    if t['highlight']:
        ax.add_patch(Rectangle((x + gap / 2, y), 1 - gap, th,
                               facecolor='none', edgecolor=C['neutral_black'], linewidth=1.6))
        ax.text(x + 0.5, y + th + 0.04, t['task_id'], ha='center', va='bottom')

for r, a in enumerate(apps):
    y = len(apps) - 1 - r + th / 2
    ax.text(8.25, y, f"{summ[a]['direct']}/8  {summ[a]['program']}/8", ha='left', va='center')
ax.text(8.25, len(apps) - 1 + th + 0.04, 'Direct  Program', ha='left', va='bottom')

ax.set_xlim(0, 10.2)
ax.set_ylim(-0.12, len(apps))
ax.set_xticks(np.arange(8) + 0.5, [str(i) for i in range(1, 9)])
ax.set_yticks(np.arange(len(apps)) + th / 2, apps[::-1])
ax.minorticks_off()
ax.set_xlabel('Task order within application evidence package')
ax.tick_params(length=0)
for s in ('top', 'right', 'left', 'bottom'):
    ax.spines[s].set_visible(False)
ax.set_aspect('equal')
handles = [Patch(color=col_ok_direct, label='Direct answer correct'),
           Patch(color=col_wrong, label='Direct answer incorrect'),
           Patch(color=col_ok_prog, label='Program execution correct')]
fig.legend(handles=handles, loc='outside lower center', ncol=3, frameon=False,
           handlelength=1.0)

finish(fig, 'fig_exec_paired')
