#!/usr/bin/env python3
"""Validate every graph and threshold directly from the distributed ZIP files.
Usage: python3 scripts/verify_instances.py
Python standard library only; no solver or network connection is needed.
"""
import csv
import re
from collections import Counter
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]

def read_graph(text):
    if 'NumberOfNodes' in text:
        n = int(re.search(r'NumberOfNodes\s*:\s*(\d+)', text)[1])
        body = text.replace('*', ' ')
        weights = list(map(int, body.split('WEIGHTS', 1)[1].split('CONNECTIONS', 1)[0].split()))
        matrix = [line.split() for line in body.split('CONNECTIONS', 1)[1].splitlines() if line.strip()]
        assert len(matrix) == n and all(len(row) == n for row in matrix), 'Matrix dimensions'
        assert all(x in ('0', '1') for row in matrix for x in row), 'Non-binary matrix'
        m = 0
        for u in range(n):
            for v in range(u + 1, n):
                assert matrix[u][v] == matrix[v][u], 'Asymmetric matrix'
                m += matrix[u][v] == '1'
    else:
        lines = text.splitlines()
        assert len(lines[0].split()) == 1, 'Invalid header'
        n = int(lines[0])
        weights = [None] * n
        for line in lines[1:n + 1]:
            u, w = map(int, line.split())
            assert 0 <= u < n and weights[u] is None, 'Invalid vertex identifier'
            weights[u] = w
        edges = set()
        for line in lines[n + 1:]:
            if not line.strip():
                continue
            u, v = map(int, line.split())
            assert 0 <= u < n and 0 <= v < n and u != v, 'Invalid edge'
            edges.add((min(u, v), max(u, v)))
        m = len(edges)
    assert n > 0 and len(weights) == n and all(w is not None and w >= 0 for w in weights), 'Invalid profits'
    return n, m, sum(weights), min(weights), max(weights)

def read_csv(name):
    with (ROOT / 'metadata' / name).open(encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def main():
    primary = read_csv('graphs.csv')
    supplementary = read_csv('supplementary_graphs.csv')
    assert len(primary) == 1310 and len(supplementary) == 48
    observed = {}
    archives = {}
    try:
        expected_members = {}
        for row in primary + supplementary:
            archive = row['archive']
            if archive not in archives:
                archives[archive] = ZipFile(ROOT / archive)
            expected_members.setdefault(archive, set()).add(row['file'])
            graph = row['graph']
            assert graph not in observed, f'Duplicate graph: {graph}'
            measured = read_graph(archives[archive].read(row['file']).decode('utf-8-sig'))
            n, m, total, lo, hi = measured
            assert (n, total, lo, hi) == tuple(int(row[k]) for k in ('n', 'profit_sum', 'profit_min', 'profit_max')), graph
            if row.get('m'):
                assert m == int(row['m']), graph
            observed[graph] = (n, m, total, archive, row['file'])
        for archive, names in expected_members.items():
            actual = archives[archive].namelist()
            assert len(actual) == len(names) and set(actual) == names, archive
    finally:
        for z in archives.values():
            z.close()
    cases = read_csv('cases.csv')
    assert len(cases) == 3930 and len({r['case_id'] for r in cases}) == 3930
    assert set(r['graph'] for r in cases) == {r['graph'] for r in primary}
    ratios = {}
    for row in cases + read_csv('study_instances.csv'):
        n, m, total, archive, member = observed[row['graph']]
        assert int(row['n']) == n and row['archive'] == archive and row['file'] == member
        assert int(row['K']) == int(Decimal(row['r']) * total), row
        if 'case_id' in row:
            assert (int(row['m']), int(row['profit_sum'])) == (m, total)
            ratios.setdefault(row['graph'], []).append(row['r'])
    assert all(sorted(rs) == ['0.6', '0.75', '0.9'] for rs in ratios.values())
    print('Verified: 1,310 primary graphs; 3,930 threshold cases; 48 supplementary graphs; 68 study-index entries.')
    print('Primary graph counts:', dict(sorted(Counter(r['group'] for r in primary).items())))

if __name__ == '__main__':
    main()
