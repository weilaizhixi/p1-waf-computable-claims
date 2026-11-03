# ⛔ 自举模块路径（让 sibling import 不依赖调用方式）
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

"""paper-analysis 主程序。

只做三件事，不新增任何锚点之外的数据：
1. 解析唯一数据锚点（交接包 05_实验结果数据全量版.md）的 A–J 节表格；
2. 用 data/ 下 3 个 CSV 对锚点数字做全量核对（CSV 只核对，不改写）；
3. 把锚点表格转录为论文用表 figures/TABLE_*.md，并为 3 张数据图输出 JSON。
"""
import datetime
import hashlib

import utils as u

CHECKS = []          # 每条硬约束/核对：(名称, 是否通过, 说明)


def check(name, ok, detail=''):
    CHECKS.append({'name': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  ✅ ' if ok else '  ❌ ') + name + (f'  [{detail}]' if detail else ''))


def main():
    print('=== 读取数据锚点 ===')
    text = u.read_text(u.ANCHOR)
    anchor_sha = hashlib.sha256(open(u.ANCHOR, 'rb').read()).hexdigest()
    sec = u.parse_sections(text)
    print('  节:', ''.join(sorted(sec)), ' SHA-256 前缀', anchor_sha[:16])
    os.makedirs(u.FIG, exist_ok=True)

    res = {'source_anchor': 'data/results_anchor_A-J.md',
           'anchor_sha256': anchor_sha,
           'generated_at': datetime.datetime.now().isoformat(timespec='seconds'),
           'policy': '全部数值逐字取自锚点；CSV 只用于核对；不计算置信区间、显著性、准确率或阻断率'}

    # ---------------- A. 语料组成 ----------------
    print('=== A 语料组成 ===')
    tA = u.parse_tables(sec['A'])[0]
    fam = [{'family': r[0], 'original': u.to_num(r[1]), 'main': u.to_num(r[2])}
           for r in tA['rows'] if r[0] != 'Total']
    totA = [r for r in tA['rows'] if r[0] == 'Total'][0]
    check('A 任务族数 = 15', len(fam) == 15, len(fam))
    check('A 原始题数列和 = Total 500', sum(f['original'] for f in fam) == u.to_num(totA[1]) == 500)
    check('A 主分析题数列和 = Total 493', sum(f['main'] for f in fam) == u.to_num(totA[2]) == 493)
    changed = [f['family'] for f in fam if f['original'] != f['main']]
    check('A 仅 Timing summaries 发生变化（39→32）', changed == ['Timing summaries'], changed)
    res['corpus'] = {'families': fam, 'total_original': 500, 'total_main': 493,
                     'excluded_contradictory': 'T403–T409（7 题）'}

    # ---------------- B. 唯一性与来源 ----------------
    tB = u.parse_tables(sec['B'])[0]
    res['uniqueness'] = {r[0]: {'value': u.to_num(r[1]), 'note': r[2]} for r in tB['rows']}

    # ---------------- C/D. 分路由计数与五类分区 ----------------
    print('=== C/D 回答单元分区 ===')
    tC = u.parse_tables(sec['C'])[0]
    routes = []
    for r in tC['rows']:
        if r[0] == 'Total':
            totC = [u.to_num(x) for x in r[1:]]
            continue
        routes.append({'label': r[0], 'value_N': u.to_num(r[1]), 'value_E': u.to_num(r[2]),
                       'type_N': u.to_num(r[3]), 'type_E': u.to_num(r[4])})
    for j, k in enumerate(['value_N', 'value_E', 'type_N', 'type_E']):
        check(f'C 列 {k} 之和 = Total {totC[j]}', sum(x[k] for x in routes) == totC[j])

    tD = u.parse_tables(sec['D'])[0]
    dvals = [u.to_num(r[1]) for r in tD['rows']]
    cats = dict(zip(['value_discrepancy', 'type_name_echo', 'missing_field',
                     'format_only', 'value_type_consistent'], dvals[:5]))
    check('D 五类之和 = 4930', sum(dvals[:5]) == dvals[5] == 4930, dvals)
    check('存在差异的回答单元 20 = 16 + 4', cats['value_discrepancy'] + cats['type_name_echo'] == 20)
    check('C 值差异 N+E = D 值差异 16', totC[0] + totC[1] == cats['value_discrepancy'])
    check('C 输出类型名 N+E = D 输出类型名 4', totC[2] + totC[3] == cats['type_name_echo'])

    # CSV 核对（10 行，每行 493）
    rows = u.read_csv('p1_cell_partition.csv')
    csv_cols = ['value_discrepancies', 'type_name_echoes', 'missing_field_cells',
                'format_only_complete_answers', 'complete_value_and_type_consistent']
    check('CSV 分区共 10 行', len(rows) == 10)
    for r in rows:
        s = sum(int(r[c]) for c in csv_cols)
        check(f"CSV {r['model']}/{r['condition']} 五类之和 = 493", s == int(r['cells']) == 493, s)
    for c, v in zip(csv_cols, dvals[:5]):
        check(f'CSV 列和 {c} = 锚点 {v}', sum(int(r[c]) for r in rows) == v)
    cmap = {'neutral': 'N', 'explicit': 'E'}
    for x in routes:
        for cond in ('neutral', 'explicit'):
            rr = [r for r in rows if r['model'] == x['label'] and r['condition'] == cond][0]
            ok = (int(rr['value_discrepancies']) == x['value_' + cmap[cond]] and
                  int(rr['type_name_echoes']) == x['type_' + cmap[cond]])
            check(f"CSV {x['label']}/{cond} 值差异与输出类型名 = 锚点 C", ok)
    miss = {cond: sum(int(r['missing_field_cells']) for r in rows if r['condition'] == cond)
            for cond in ('neutral', 'explicit')}
    miss_models = sorted({r['model'] for r in rows if int(r['missing_field_cells']) > 0})
    check('缺失字段只来自 gpt6luna、两条件各 1（锚点 D：T222 两个条件）',
          miss == {'neutral': 1, 'explicit': 1} and miss_models == ['gpt6luna'], (miss, miss_models))

    res['partition'] = {
        'total_cells': 4930, 'categories': cats, 'discrepancy_cells': 20, 'discrepancy_tasks': 19,
        'by_condition': {'value_discrepancy': {'N': totC[0], 'E': totC[1]},
                         'type_name_echo': {'N': totC[2], 'E': totC[3]},
                         'missing_field': {'N': 1, 'E': 1}},
        'missing_field_source': 'gpt6luna × T222，两个提示条件各 1 个回答单元（锚点 D）',
        'note': '各路由的仅格式偏差与完整答案计数只在 CSV 中出现，锚点未报告，不输出（ASSETS_CONFLICTS M1）'}
    res['route_counts'] = {'rows': routes, 'total': dict(zip(['value_N', 'value_E', 'type_N', 'type_E'], totC)),
                           'note': '归档路由标签计数，是本语料上的描述，不是模型排名；条件差异不作因果解释'}

    # ---------------- E. 案例 ----------------
    tE = u.parse_tables(sec['E'])[0]
    res['cases'] = [dict(zip(['task', 'route_condition', 'record', 'reference', 'category'], r))
                    for r in tE['rows']]

    # ---------------- F. 敏感性 ----------------
    print('=== F 敏感性 ===')
    tF1, tF2 = u.parse_tables(sec['F'])[:2]
    sens = [dict(zip(['analysis', 'tasks_cells', 'disc_cells', 'disc_tasks', 'type_echo', 'note'], r))
            for r in tF1['rows']]
    check('F 三种口径的输出类型名均为 4', all(s['type_echo'] == '4' for s in sens))
    loo = [{'omitted': r[0], 'kept': u.to_num(r[1]), 'net_gain': u.to_num(r[2]), 'pp': u.to_num(r[3])}
           for r in tF2['rows']]

    # ---------------- G. 执行对照 ----------------
    print('=== G 执行对照 ===')
    tG = u.parse_tables(sec['G'])[0]
    apps = []
    for r in tG['rows']:
        if r[0] == 'Total':
            totG = [u.to_num(x) for x in r[1:]]
            continue
        apps.append(dict(zip(['app', 'tasks', 'direct', 'program', 'disc', 'reverse'],
                             [r[0]] + [u.to_num(x) for x in r[1:]])))
    for j, k in enumerate(['tasks', 'direct', 'program', 'disc', 'reverse']):
        check(f'G 列 {k} 之和 = Total {totG[j]}', sum(a[k] for a in apps) == totG[j])
    check('G 合计 48/46/48/2/0', totG == [48, 46, 48, 2, 0], totG)
    for a in apps:
        check(f"G {a['app']}: 程序正确 − 直接正确 = 不一致对 − 反向",
              a['program'] - a['direct'] == a['disc'] - a['reverse'])
    pp = round(totG[3] / totG[0] * 100, 2)
    check('固定集差异 2/48 = 4.17 pp（锚点 G）', pp == 4.17, pp)
    # 逐一排除应用：由 G 逐行复算后与 F 下表比对（只核对，正文用 F 的数字）
    for l in loo:
        a = [x for x in apps if x['app'] == l['omitted']][0]
        kept = totG[0] - a['tasks']
        gain = (totG[2] - a['program']) - (totG[1] - a['direct'])
        check(f"F 逐一排除 {l['omitted']}: {gain}/{kept} = {l['net_gain']}/{l['kept']}，{l['pp']} pp",
              kept == l['kept'] and gain == l['net_gain'] and round(gain / kept * 100, 1) == l['pp'])
    erows = u.read_csv('p1_execution_control.csv')
    name_map = {a['app'].lower().replace(' ', '_'): a for a in apps}
    for r in erows:
        a = name_map.get(r['app'])
        ok = a is not None and [int(r[k]) for k in ['tasks', 'direct_correct', 'program_correct',
                                                    'direct_wrong_program_correct', 'reverse_pairs']] == \
            [a['tasks'], a['direct'], a['program'], a['disc'], a['reverse']]
        check(f"CSV 执行对照 {r['app']} = 锚点 G", ok)

    # ---------------- H. 两个不一致任务 ----------------
    tH = u.parse_tables(sec['H'])[0]
    disc_tasks = [dict(zip(['task', 'quantity', 'direct', 'reference', 'program'], r)) for r in tH['rows']]
    for d in disc_tasks:
        check(f"H {d['task']}: 程序输出 = 参考，直接答案 ≠ 参考",
              d['program'] == d['reference'] and d['direct'] != d['reference'])
    res['exec_control'] = {'apps': apps, 'total': dict(zip(['tasks', 'direct', 'program', 'disc', 'reverse'], totG)),
                           'fixed_set_pp': '2/48 = 4.17', 'leave_one_app_out': loo,
                           'discordant_tasks': disc_tasks, 'changed_input_check': '48/48（事后测量工具检查）'}
    res['task_exclusion_sensitivity'] = sens

    # ---------------- I. 213 格回放 ----------------
    print('=== I 共享回放 ===')
    tI = u.parse_tables(sec['I'])[0]
    rep = []
    for r in tI['rows']:
        if r[0] == 'Total':
            totI = [u.to_num(x) for x in r[1:]]
            continue
        rep.append(dict(zip(['app', 'candidates', 'valid', 'benign', 'example'],
                            [r[0]] + [u.to_num(x) for x in r[1:]])))
    check('I 应用数 = 12', len(rep) == 12)
    for j, k in enumerate(['candidates', 'valid', 'benign', 'example']):
        check(f'I 列 {k} 之和 = Total {totI[j]}', sum(x[k] for x in rep) == totI[j])
    check('I 合计 213/213/211/141', totI == [213, 213, 211, 141], totI)
    for x in rep:
        check(f"I {x['app']}: 候选 ≥ 测量有效 ≥ 良性 ≥ 示例符合 ≥ 0",
              x['candidates'] >= x['valid'] >= x['benign'] >= x['example'] >= 0)
    srows = u.read_csv('p1_shared_replay.csv')
    rmap = {x['app'].lower().replace(' ', '_'): x for x in rep}
    for r in srows:
        x = rmap.get(r['app'])
        ok = x is not None and [int(r[k]) for k in ['candidates', 'measurement_valid',
                                                    'benign_response_contracts', 'example_conformance']] == \
            [x['candidates'], x['valid'], x['benign'], x['example']]
        check(f"CSV 回放 {r['app']} = 锚点 I", ok)
    res['shared_replay'] = {'apps': rep, 'total': dict(zip(['candidates', 'valid', 'benign', 'example'], totI)),
                            'note': '单一测试栈上的计数；141 是测试示例符合，不是漏洞阻断率；与姊妹部署研究共享',
                            'historical': '240 候选 / 205 联合可筛选格 / 101 旧标准通过（较弱中断标准，不作因果修复比较）'}

    # ---------------- J. 失效链 ----------------
    tJ = u.parse_tables(sec['J'])[0]
    res['failure_chains'] = [dict(zip(['problem', 'wrong_interpretation', 'evidence_needed'], r))
                             for r in tJ['rows']]
    check('J 测量流程失效类别 = 7', len(res['failure_chains']) == 7)

    # Internal historical audit metadata (section K) is outside this public release.

    import tables_and_figdata as tf
    tf.write_all(res, tE, tF1, tH, tJ)

    res['checks'] = {'n_total': len(CHECKS), 'n_pass': sum(c['pass'] for c in CHECKS), 'items': CHECKS}
    u.dump_json(res, 'all_results.json')
    n_fail = len(CHECKS) - res['checks']['n_pass']
    print(f'=== 完成：{len(CHECKS)} 项核对，{n_fail} 项失败 ===')
    return 1 if n_fail else 0


if __name__ == '__main__':
    sys.exit(main())
