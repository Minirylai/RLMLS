# RLMLS

Benchmark instances for **Reduction-based Learning-driven Multi-Start Local Search for the Minimum General Partial Dominating Set Problem**.

The main comparison uses **1,310 weighted graphs**, each with three coverage ratios, giving **3,930 instances**. Download the grouped ZIP files below, or use **Code → Download ZIP** for the complete repository. Extract each instance archive into the repository root; it contains its own `instances/<group>/` directory.

## Benchmark instances

| Category | Type | Graphs | Instances | Number of vertices | Download |
|---|---|---:|---:|---:|---|
| MWDS | Type I | 530 | 1,590 | 50–1,000 | [TypeI.zip](instances/TypeI.zip) |
| MWDS | Type II | 530 | 1,590 | 50–1,000 | [TypeII.zip](instances/TypeII.zip) |
| MWDS | Unit disk graphs | 120 | 360 | 50–1,000 | [UDG.zip](instances/UDG.zip) |
| Network Data Repository | NDR | 30 | 90 | 501–18,470 | [NDR.zip](instances/NDR.zip) |
| Random graphs | Erdős–Rényi | 30 | 90 | 500–20,000 | [ER.zip](instances/ER.zip) |
| Random graphs | Barabási–Albert | 30 | 90 | 500–20,000 | [BA.zip](instances/BA.zip) |
| Random graphs | Stochastic block model | 30 | 90 | 500–20,000 | [SBM.zip](instances/SBM.zip) |
| Census | Population-based geographic graphs | 10 | 30 | 2,933–9,097 | [Census.zip](instances/Census.zip) |
| **Total** | | **1,310** | **3,930** | | |

For every graph, the required covered profit is

$$K=\left\lfloor r\sum_{v\in V}p_v\right\rfloor,\qquad r\in\{0.6,0.75,0.9\}.$$

A selected vertex covers itself and its adjacent vertices. Each covered vertex contributes its profit once. The objective is to minimize the **number of selected vertices**, not their total profit.

- [All 3,930 instances](metadata/cases.csv): graph name, coverage ratio, exact integer threshold `K`, archive and file path.
- [Graph information](metadata/graphs.csv): graph size, number of undirected edges, vertex profits, format and source.
- [Input formats](FORMAT.md) and [data sources](SOURCES.md).

## Supplementary experiments

[Supplementary inputs](instances/supplementary.zip) contain 48 additional graphs used in component, calibration and structural studies. These are separate from the 1,310 main-comparison graphs. In particular, supplementary `ndr_*` files use historical generated profits, whereas the main `CEE2025_*` files use the published author weight sequence; they are not interchangeable.

[Study indices](metadata/study_instances.csv) identify the learning/phase/tabu comparison (20 instances), incremental-evaluation comparison (20), initial irace calibration (24), and search-space analysis (4). Their indices refer to the corresponding study, not to a shared ordering. Additional inputs are listed in [supplementary_graphs.csv](metadata/supplementary_graphs.csv).

The learning/phase/tabu subset was selected after the 30-case pilot to examine cases with favorable RLMLS results. The incremental comparison retains its original 20-case set. These study subsets do not replace the complete main benchmark.

## Use and validation

```bash
# Extract one group (repeat for other groups as needed).
python3 -m zipfile -e instances/TypeI.zip .

# Check all distributed graph files and thresholds directly inside the ZIPs.
python3 scripts/verify_instances.py
```

Validation requires only Python 3 and its standard library. It checks all graph dimensions, profits, edges, archive membership and coverage thresholds. Data-generation information and optional regeneration commands are in [SOURCES.md](SOURCES.md).

This repository distributes experimental inputs and their documentation. Algorithm source code and experimental result tables are not included in this data release. Third-party data retain their original attribution and terms; see [NOTICE.md](NOTICE.md).
