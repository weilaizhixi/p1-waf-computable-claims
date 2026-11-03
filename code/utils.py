# ⛔ 自举模块路径（让 sibling import 不依赖调用方式）
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import csv
import json
import re

ROOT = os.path.abspath(os.path.join(_HERE, '..'))
ANCHOR = os.path.join(ROOT, 'data', 'results_anchor_A-J.md')
DATA = os.path.join(ROOT, 'data')
FIG = os.environ.get('P1_OUTPUT_DIR', os.path.join(ROOT, 'outputs', 'analysis'))


def read_text(path):
    with open(path, 'r', encoding='utf-8-sig') as fh:
        return fh.read()


def clean(cell):
    """去掉 Markdown 加粗标记与首尾空白。"""
    return cell.replace('**', '').strip()


def to_num(s):
    """把锚点中的计数/百分点字符串转为 int/float；非数值返回原串。"""
    s2 = clean(s)
    if re.fullmatch(r'-?\d+', s2):
        return int(s2)
    if re.fullmatch(r'-?\d+\.\d+', s2):
        return float(s2)
    return s2


def parse_sections(text):
    """按 '## X. 标题' 切分锚点文件，返回 {字母: 段落文本}。"""
    parts = {}
    cur = None
    buf = []
    for line in text.splitlines():
        m = re.match(r'^##\s+([A-L])\.\s', line)
        if m:
            if cur:
                parts[cur] = '\n'.join(buf)
            cur, buf = m.group(1), []
        elif cur:
            buf.append(line)
    if cur:
        parts[cur] = '\n'.join(buf)
    return parts


def parse_tables(section_text):
    """返回段落内所有 Markdown 表：[{header:[...], rows:[[...]]}]。"""
    tables, cur = [], []
    for line in section_text.splitlines() + ['']:
        if line.strip().startswith('|'):
            cur.append(line.strip())
        elif cur:
            cells = [[c for c in r.strip('|').split('|')] for r in cur]
            header = [clean(c) for c in cells[0]]
            rows = [[clean(c) for c in r] for r in cells[2:]]
            tables.append({'header': header, 'rows': rows})
            cur = []
    return tables


def read_csv(name):
    with open(os.path.join(DATA, name), 'r', encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def dump_json(obj, name):
    path = os.path.join(FIG, name)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
    return path


def md_table(header, rows, align=None):
    """生成 Markdown 表；align 为每列 'l' 或 'r'。"""
    align = align or ['l'] * len(header)
    sep = ['---:' if a == 'r' else '---' for a in align]
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(sep) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(c) for c in r) + ' |')
    return '\n'.join(out) + '\n'


def write_md(name, title, table, note):
    path = os.path.join(FIG, name)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(title + '\n\n' + table + '\n' + note + '\n')
    return path
