# ⛔ 自举模块路径（让 sibling import 不依赖调用方式）
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

"""把 main.py 解析出的锚点数据转录为论文用表（figures/TABLE_*.md）与图数据 JSON。
不做任何新计算；表中每个数字都来自锚点对应节。"""
import utils as u

DEF = {  # 表 2 判定规则，依据方法文档定义 D3–D6
    'value_discrepancy': ('值差异', '字段输出值与参考值不同（数值或其他值），不含以类型名代替字段值'),
    'type_name_echo': ('以类型名代替字段值', '需要布尔值的字段输出 `bool` 等类型名；同一回答单元内多个字段回显仍计 1 个'),
    'missing_field': ('缺失字段', '响应缺少请求字段名；不把未输出的值计为错误值'),
    'format_only': ('仅格式偏差', 'JSON 完整、所有请求字段存在，值经声明规则强制转换后正确，类型有偏差'),
    'value_type_consistent': ('值与类型一致', '所有请求字段存在，值与类型均符合声明规则'),
}


def write_all(res, tE, tF1, tH, tJ):
    out = []
    # 表 1 语料组成
    rows = [[f['family'], f['original'], f['main']] for f in res['corpus']['families']]
    rows.append(['合计', 500, 493])
    out.append(u.write_md('TABLE_corpus.md', '表 1 语料组成：15 个任务族的原始题数与主分析题数',
                          u.md_table(['任务族（归档标签）', '原始题数', '主分析题数'], rows, ['l', 'r', 'r']),
                          '注：任务族是归档标签，不是相互独立的应用域。Timing summaries 由 39 题变为 32 题，'
                          '原因是排除了 7 道同时要求中位数与求和的约定矛盾题（T403–T409）。'))

    # 表 2 五类互斥分类
    cats = res['partition']['categories']
    rows = [[DEF[k][0], DEF[k][1], cats[k]] for k in DEF]
    rows.append(['合计', '493 题 × 5 个路由标签 × 2 个提示条件', 4930])
    out.append(u.write_md('TABLE_partition.md', '表 2 4930 个回答单元的五类互斥分类',
                          u.md_table(['类别', '判定规则', '回答单元数'], rows, ['l', 'l', 'r']),
                          '注：存在差异的回答单元为 20 个（16 个值差异 + 4 个以类型名代替字段值），涉及 19 个任务；'
                          '2 个缺失字段均来自同一路由对 T222 的两个提示条件，不计入这 20 个。'
                          '4930 个回答单元共享问题、证据与参考，不是独立样本。'))

    # 表 3 各路由标签计数
    rows = [[r['label'], r['value_N'], r['value_E'], r['type_N'], r['type_E']] for r in res['route_counts']['rows']]
    t = res['route_counts']['total']
    rows.append(['合计', t['value_N'], t['value_E'], t['type_N'], t['type_E']])
    out.append(u.write_md('TABLE_route_counts.md', '表 3 各归档路由标签在两个提示条件下的值差异与输出类型名计数',
                          u.md_table(['归档路由标签', '值差异 N', '值差异 E', '输出类型名 N', '输出类型名 E'],
                                     rows, ['l', 'r', 'r', 'r', 'r']),
                          '注：N 为 neutral 条件，E 为 explicit 条件。标签是执行计划中请求的调用标识，计数是本语料上的描述，'
                          '不是模型排名；两个条件的顺序未随机化、每个条件一个选定回答，条件间差异不作因果解释；'
                          '零计数不代表其他任务或未来调用上无差异。'))

    # 表 4 案例
    rows = [r for r in tE['rows']]
    out.append(u.write_md('TABLE_cases.md', '表 4 分类案例',
                          u.md_table(['任务', '路由/条件', '记录', '参考/正确值', '分类'], rows),
                          '注：案例只用于说明分类规则，不推断模型内部的失败原因。'))

    # 表 5 任务排除敏感性
    rows = [r[:5] + [r[5]] for r in tF1['rows']]
    out.append(u.write_md('TABLE_sensitivity.md', '表 5 任务排除敏感性',
                          u.md_table(['分析口径', '任务/回答单元', '存在差异的回答单元', '差异任务', '输出类型名', '说明'],
                                     rows, ['l', 'r', 'r', 'r', 'r', 'l']),
                          '注：500 题口径与 484 题口径都是事后描述，不恢复随机比较，也不是独立验证。'))

    # 表 6 执行对照 + 逐一排除应用
    loo = {l['omitted']: l for l in res['exec_control']['leave_one_app_out']}
    rows = []
    for a in res['exec_control']['apps']:
        l = loo[a['app']]
        rows.append([a['app'], a['tasks'], a['direct'], a['program'], a['disc'], a['reverse'],
                     f"{l['net_gain']}/{l['kept']}", l['pp']])
    t = res['exec_control']['total']
    rows.append(['合计', t['tasks'], t['direct'], t['program'], t['disc'], t['reverse'], '—', '—'])
    out.append(u.write_md('TABLE_exec_control.md',
                          '表 6 48 题配对对照的逐应用结果与逐一排除应用的敏感性分析',
                          u.md_table(['应用证据包', '题数', '直接正确', '程序正确', '直接错/程序对', '反向',
                                      '排除该应用后净增', '描述性百分点'], rows,
                                     ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r']),
                          '注：固定集上的观察差异为 2/48 = 4.17 个百分点。末两列为排除该应用 8 题后，'
                          '其余 40 题上程序执行条件相对直接条件净增的正确题数，用于检查结果对证据包组成的依赖，'
                          '不是置信区间或总体效应。'))

    # 表 7 两个不一致任务
    out.append(u.write_md('TABLE_discordant.md', '表 7 两个不一致任务的请求量、直接答案、参考与执行程序输出',
                          u.md_table(['任务', '请求量', '直接答案', '参考', '执行程序'], tH['rows']),
                          '注：参考值在执行前由 Python 实现与独立 SQLite 查询核验；程序条件为模型生成程序后实际执行一次，'
                          '无执行反馈与迭代修复。'))

    # 表 8 测量流程失效
    out.append(u.write_md('TABLE_failure_chains.md', '表 8 7 类测量流程失效、可能导致的错误解释与修正后需要的证据',
                          u.md_table(['观察到的测量工具问题', '可能导致的错误解释', '修正后需要的证据'], tJ['rows']),
                          '注：在这些情形下，对记录的计算可以完全正确，据此得出的安全结论仍然错误。'))

    # ---------- 图数据 JSON ----------
    p = res['partition']
    u.dump_json({'figure': 'fig_partition', 'source': '锚点 C、D',
                 'panel_a': [{'category': DEF[k][0], 'cells': cats[k]} for k in DEF],
                 'panel_a_total': 4930,
                 'panel_b': [{'category': DEF[k][0], 'N': p['by_condition'][k]['N'], 'E': p['by_condition'][k]['E']}
                             for k in ['value_discrepancy', 'type_name_echo', 'missing_field']],
                 'panel_b_total': 22,
                 'note': '图中不得出现各路由的仅格式偏差/完整答案细分数（锚点未报告）'}, 'fig_partition_data.json')

    tiles = []
    for k, a in enumerate(res['exec_control']['apps']):
        for j in range(8):
            hid = f'H{8 * k + j + 1:03d}'
            disc = hid in [d['task'].split('（')[0] for d in res['exec_control']['discordant_tasks']]
            tiles.append({'app': a['app'], 'col': j + 1, 'task_id': hid,
                          'direct_correct': not disc, 'program_correct': True, 'highlight': disc})
    for a in res['exec_control']['apps']:   # 瓦片推得的计数必须回到锚点 G
        sub = [t for t in tiles if t['app'] == a['app']]
        assert sum(t['direct_correct'] for t in sub) == a['direct']
        assert sum(t['program_correct'] for t in sub) == a['program']
    u.dump_json({'figure': 'fig_exec_paired', 'source': '锚点 G、H', 'apps': res['exec_control']['apps'],
                 'tiles': tiles, 'total': res['exec_control']['total'],
                 'layout_note': '每应用 8 题、H001–H048 按表 G 的应用顺序排布（由 ID 规则推定）；锚点只给出 H007、H019 '
                                '两题的直接答案不一致，其余 46 题两条件均正确由合计 46/48、48/48 推出。'
                                '图中只标注 H007、H019，其余瓦片不对应具体任务类型。'}, 'fig_exec_paired_data.json')

    u.dump_json({'figure': 'fig_replay_conditions', 'source': '锚点 I', 'apps': res['shared_replay']['apps'],
                 'total': res['shared_replay']['total'],
                 'note': '测试示例符合不是漏洞阻断率；单一测试栈；与姊妹部署研究共享'}, 'fig_replay_conditions_data.json')
    print('  写出表格:', ', '.join(os.path.basename(x) for x in out))
