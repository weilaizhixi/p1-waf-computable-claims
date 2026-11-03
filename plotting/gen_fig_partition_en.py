# 图 3：4930 个回答单元的五类互斥分区 (a 总体构成；b 22 个非完整/差异单元放大)
# 数据：figures/fig_partition_data.json (转录自 RESULTS.md C、D)
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _figcommon import *
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

d = load('fig_partition_data.json')
cells = {r['category']: r['cells'] for r in d['panel_a']}
assert sum(cells.values()) == d['panel_a_total'] == 4930

fig = plt.figure(figsize=(6.3, 4.3), layout='constrained')
set_paper_placement(fig, width_fraction=0.95)
gs = fig.add_gridspec(2, 1, height_ratios=[0.8, 1.25])

# ---- a：单条水平堆叠条 (绝对计数，0–4930)----
ax = fig.add_subplot(gs[0, 0])
order = ['Value and type consistency', 'Format-only deviation', 'Value discrepancy', 'Type-name substitution', 'Missing fields']
cols = {'Value and type consistency': C['blue_main'], 'Format-only deviation': C['blue_secondary'],
        'Value discrepancy': C['red_strong'], 'Type-name substitution': C['gold'], 'Missing fields': C['neutral_dark']}
left = 0
for k in order:
    ax.barh(0, cells[k], left=left, height=0.55, color=cols[k],
            edgecolor='white', linewidth=0.4, label=f'{k} ({cells[k]})')
    left += cells[k]
ax.text(cells['Value and type consistency'] / 2, 0, '4161', ha='center', va='center', color='white')
ax.text(cells['Value and type consistency'] + cells['Format-only deviation'] / 2, 0, '747',
        ha='center', va='center', color='white')
ax.annotate('22', xy=(4930 - 11, 0.28), xytext=(4930 - 11, 0.62),
            ha='center', va='bottom',
            arrowprops=dict(arrowstyle='-', lw=0.6, color=C['neutral_black']))
ax.set_xlim(0, 4930)
ax.set_ylim(-0.45, 0.95)
ax.set_xticks([0, 1000, 2000, 3000, 4000, 4930])
ax.set_yticks([])
ax.minorticks_off()
ax.set_xlabel('Number of response cells')
ax.spines['left'].set_visible(False)
ax.set_title('a', loc='left', fontweight='bold')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.65), ncol=2,
          frameon=False, handlelength=1.0, columnspacing=1.0)

# ---- b：22 个单元放大，每点一个回答单元，按提示条件着色 ----
bx = fig.add_subplot(gs[1, 0])
rows = d['panel_b']
cN, cE = C['blue_main'], C['red_strong']
for i, r in enumerate(rows):
    y = len(rows) - 1 - i
    xs_n = np.arange(r['N'])
    xs_e = np.arange(r['N'], r['N'] + r['E'])
    bx.scatter(xs_n, [y] * len(xs_n), s=46, marker='o', color=cN, zorder=3)
    bx.scatter(xs_e, [y] * len(xs_e), s=46, marker='s', facecolor='white',
               edgecolor=cE, linewidth=1.2, zorder=3)
    bx.text(16.4, y, f"{r['N'] + r['E']}", ha='left', va='center')
short = {'Type-name substitution': 'Type-name substitution'}
bx.set_yticks(range(len(rows)), [short.get(r['category'], r['category']) for r in rows][::-1])
bx.minorticks_off()
bx.set_xticks([0, 4, 9, 14], ['1', '5', '10', '15'])
bx.set_xlim(-0.8, 17.6)
bx.set_ylim(-0.6, len(rows) - 0.4)
bx.set_xlabel('Response cells (one per point)')
bx.set_title('b', loc='left', fontweight='bold')
handles = [Line2D([], [], marker='o', ls='', color=cN, markersize=6, label='neutral'),
           Line2D([], [], marker='s', ls='', markerfacecolor='white', markeredgecolor=cE,
                  markeredgewidth=1.2, markersize=6, label='explicit')]
bx.legend(handles=handles, loc='lower right', frameon=False, ncol=2)

finish(fig, 'fig_partition')
