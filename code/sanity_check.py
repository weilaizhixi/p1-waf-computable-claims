# ⛔ 自举模块路径（让 sibling import 不依赖调用方式）
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

"""检测 JSON 结果中的 NaN/Inf 与“太完美”指标；并从落盘 JSON 重新复核硬约束。"""
import json
import math

FIG = os.environ.get('P1_OUTPUT_DIR', os.path.join(_HERE, '..', 'outputs', 'analysis'))
errors, suspicious = [], []


def walk(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f'{path}[{i}]')
    elif obj is None:
        errors.append(f'❌ {path} 为 null')
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        errors.append(f'❌ {path} 为 NaN/Inf')
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        key = path.lower()
        if any(w in key for w in ['accuracy', 'r2', 'auc', 'f1', 'p_value']):
            suspicious.append(f'🚩 {path} = {obj}')


for f in sorted(os.listdir(FIG)):
    if f.endswith('.json'):
        walk(json.load(open(os.path.join(FIG, f), encoding='utf-8')), f)

# 从落盘 JSON 重新复核硬约束（不信任进程内变量）
r = json.load(open(os.path.join(FIG, 'all_results.json'), encoding='utf-8'))
c = r['partition']['categories']
cons = [
    ('五类之和 = 4930', sum(c.values()) == 4930),
    ('20 = 值差异 + 输出类型名', c['value_discrepancy'] + c['type_name_echo'] == 20),
    ('执行对照 48/46/48/2/0', list(r['exec_control']['total'].values()) == [48, 46, 48, 2, 0]),
    ('程序正确 − 直接正确 = 不一致对 − 反向', 48 - 46 == 2 - 0),
    ('回放 213/213/211/141', list(r['shared_replay']['total'].values()) == [213, 213, 211, 141]),
    ('回放逐应用单调', all(a['candidates'] >= a['valid'] >= a['benign'] >= a['example'] >= 0
                         for a in r['shared_replay']['apps'])),
    ('语料 500 → 493', r['corpus']['total_original'] == 500 and r['corpus']['total_main'] == 493),
    ('核对项全部通过', r['checks']['n_pass'] == r['checks']['n_total']),
]
for name, ok in cons:
    (print if ok else errors.append)(('  ✅ ' if ok else '❌ ') + name)

for e in errors:
    print(e)
for s in suspicious:
    print(s)
print(f'N_CONSTRAINTS={sum(ok for _, ok in cons)} N_CHECKS={r["checks"]["n_total"]}')
if errors:
    sys.exit(1)
print('✅ 所有数值通过 sanity check')
