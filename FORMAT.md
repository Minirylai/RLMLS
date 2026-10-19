# Input formats

The files preserve the inputs used in the experiments. Vertex identifiers are zero-based. `metadata/cases.csv` provides the required covered profit `K`; `K` is not stored in the graph file.

## Weighted edge list

Used by UDG, NDR, ER, BA, SBM, Census and the supplementary inputs:

```text
n
0 p_0
1 p_1
...
n-1 p_(n-1)
u v
...
```

The first line gives the number of vertices. The following `n` lines give a vertex identifier and its nonnegative integer profit. Each subsequent line gives an undirected edge. Isolated vertices remain in the profit block. An edge is counted once, irrespective of endpoint order.

## Labeled matrix

Type I and Type II retain the original author format:

```text
NumberOfNodes:
n
Positions
x_0 y_0
...
x_(n-1) y_(n-1)
******************WEIGHTS*****************************
p_0
...
p_(n-1)
*****************CONNECTIONS****************
a_00 a_01 ... a_0(n-1)
...
a_(n-1)0 ... a_(n-1)(n-1)
```

There are `n` coordinate rows, `n` profit entries and an `n × n` symmetric binary matrix. Ignore the matrix diagonal when counting edges. Self-coverage is included by the MinGPDS definition, not counted as a graph edge. The marker lengths vary; identify the words `NumberOfNodes`, `WEIGHTS` and `CONNECTIONS` rather than assuming a fixed number of asterisks.

## CSV indices

- `graphs.csv`: one row per main weighted graph. `m` counts distinct undirected edges, excluding self-loops. `profit_sum`, `profit_min` and `profit_max` describe the actual supplied profits.
- `cases.csv`: one row per graph–ratio pair. `case_id` appends `__r<ratio>` to the graph name. `K` is the exact integer threshold used for that pair.
- `supplementary_graphs.csv`: additional inputs, separate from the main graph count.
- `study_instances.csv`: selected study membership, with the study-specific index and threshold.

The `archive` column locates the ZIP relative to the repository root. The `file` column gives both its member path and its path after extraction at the repository root. Use integer `K` from the index to avoid floating-point rounding differences when reconstructing thresholds.
