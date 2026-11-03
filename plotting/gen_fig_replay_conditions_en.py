# 图 5：213 格共享回放的逐级计数 (Candidate-rule cells ⊇ Measurement valid ⊇ Benign-response contract ⊇ Example conformance)
# 数据：figures/fig_replay_conditions_data.json (转录自 RESULTS.md I)
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _figcommon import *

d = load('fig_replay_conditions_data.json')
apps = d['apps']
keys = ['candidates', 'valid', 'benign', 'example']
for k in keys:
    assert sum(a[k] for a in apps) == d['total'][k]
assert [d['total'][k] for k in keys] == [213, 213, 211, 141]

names = {'candidates': 'Candidate-rule cells', 'valid': 'Measurement valid',
         'benign': 'Benign-response contract', 'example': 'Example conformance'}
style = {'candidates': dict(height=0.86, facecolor='white', edgecolor=C['neutral_black'], linewidth=0.8),
         'valid': dict(height=0.70, facecolor=C['neutral_light'], edgecolor='none'),
         'benign': dict(height=0.50, facecolor=C['blue_secondary'], edgecolor='none'),
         'example': dict(height=0.28, facecolor=C['red_strong'], edgecolor='none')}

fig = plt.figure(figsize=(6.3, 5.3), layout='constrained')
set_paper_placement(fig, width_fraction=0.95)
gs = fig.add_gridspec(2, 1, height_ratios=[12, 1.6])


def draw(ax, rows, labels, xmax):
    n = len(rows)
    for i, row in enumerate(rows):
        y = n - 1 - i
        for k in keys:
            ax.barh(y, row[k], label=names[k] if i == 0 else '_nolegend_', **style[k])
        ax.text(xmax * 1.04, y, f"{row['valid']}/{row['benign']}/{row['example']}",
                ha='left', va='center')
    ax.set_yticks(range(n), labels[::-1])
    ax.set_xlim(0, xmax * 1.28)
    ax.spines['bottom'].set_bounds(0, xmax)
    ax.minorticks_off()
    ax.set_ylim(-0.6, n - 0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


ax = fig.add_subplot(gs[0, 0])
draw(ax, apps, [a['app'] for a in apps], 20)
ax.set_xticks([0, 5, 10, 15, 20])
ax.set_title('a', loc='left', fontweight='bold')


bx = fig.add_subplot(gs[1, 0])
draw(bx, [d['total']], ['Total'], 213)
bx.set_xticks([0, 50, 100, 150, 200, 213], ['0', '50', '100', '150', '', '213'])
bx.set_xlabel('Number of rule cells')
bx.set_title('b', loc='left', fontweight='bold')

h, l = ax.get_legend_handles_labels()
fig.legend(h, l, loc='outside lower center', ncol=2, frameon=False, handlelength=1.2)

finish(fig, 'fig_replay_conditions')
