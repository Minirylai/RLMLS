# Benchmark sources and construction

## Type I, Type II and unit disk graphs

The 1,180 MWDS-derived inputs follow the public benchmark archive accompanying:

M. D. Rasheed and A. Singh, *Solution of minimum general partial dominating set problem through heuristic approaches*, Computers and Electrical Engineering 125 (2025), 110427. [Article](https://doi.org/10.1016/j.compeleceng.2025.110427) · [Author benchmark archive](https://scis.uohyd.ac.in/~alokcs/MinGPDS.zip).

Type I and Type II each contain 530 graphs; UDG contains 120. The distributed contents preserve the experimental input files. Type I profits in these files range from 20 to 49; Type II profits were generated using degree-dependent bounds, and UDG profits range from 1 to 100. These are vertex profits for coverage, not selection costs. The earlier MWDS benchmark source is [Jovanović's benchmark page](https://mail.ipb.ac.rs/~rakaj/home/BenchmarkMWDSP.htm).

## Network Data Repository

The 30 main NDR inputs use topologies and the published weight sequence from the same author archive. The missing `bio-grid-plant` topology was obtained from [Network Repository](https://nrvis.com/download/data/bio/bio-grid-plant.zip). See also [Network Repository](https://networkrepository.com/) and its [AAAI 2015 paper](https://networkrepository.com/pubs/aaai15-nr.pdf).

Normalization retains numeric vertex identifiers `0..max_id`, including identifiers with no incident edge, and assigns `p_i = W[i]` from the published sequence. Self-loops are removed and repeated undirected edges are merged. Duplicate `rt-pol` / `ia-retweet-pol` topology files are represented once. The authors' exact ID-to-weight mapping was not published; these files define the explicit normalized inputs used in our experiments, rather than claiming an exact reconstruction of every unpublished original mapping.

[NDR_sources.zip](provenance/NDR_sources.zip) includes the original topologies, weight list, author format description and normalization metadata. Main `CEE2025_*` inputs and supplementary `ndr_*` inputs must be kept separate because their profits differ.

## Random graphs

The 90 generated graphs comprise three families, each with five vertex counts `{500, 2000, 5000, 10000, 20000}`, two connection scales `d ∈ {6, 30}`, and three replicates per combination:

- **Erdős–Rényi:** independent edge probability `d/(n−1)` ([Gilbert, 1959](https://doi.org/10.1214/aoms/1177706098)).
- **Barabási–Albert:** attachment parameter `d/2` ([Barabási and Albert, 1999](https://doi.org/10.1126/science.286.5439.509)).
- **Stochastic block model:** four equal blocks; within-block probability `0.9d/(n/4−1)` and between-block probability `0.1d/(3n/4)` ([Holland et al., 1983](https://doi.org/10.1016/0378-8733(83)90021-7)).

Profits are independent integers sampled from `{20, …, 49}`. [structured_manifest.json](provenance/structured_manifest.json) gives graph/profit seeds, model parameters and realized attributes. The graph names encode family, size, connection scale, replicate and profit scheme.

Optional regeneration, using the recorded library versions:

```bash
python3 -m pip install -r scripts/generation_requirements.txt
python3 scripts/generate_structured.py --output-dir regenerated/structured
```

The supplied ZIPs remain the reference experimental inputs; regeneration writes to a separate directory.

## Census geographic graphs

Ten graphs are constructed from the 2020 Census population-weighted tract centers for Michigan, Florida, New York, Texas and California. Each state retains all positive-population tracts, with population as vertex profit. Two connection scales, 6 and 30, give two graphs per state. Great-circle distance determines adjacency; the resulting service radii are rounded upward to 0.1 km and range from 1.1 to 6.8 km.

- [U.S. Census Bureau population-center data](https://www.census.gov/geographies/reference-files/time-series/geo/centers-population.html)
- [Population-center methodology](https://www2.census.gov/geo/pdfs/reference/cenpop2020/COP2020_documentation.pdf)
- [Census2020_sources.zip](provenance/Census2020_sources.zip): original public files, GEOID mappings, graph specifications and regeneration script.

To verify the construction against the distributed graphs:

```bash
python3 -m zipfile -e instances/Census.zip .
python3 -m zipfile -e provenance/Census2020_sources.zip .
python3 -m pip install -r scripts/generation_requirements.txt
python3 Census2020_sources/prepare.py
```

The provenance filenames retain the original Chinese labels. `冻结Census30.json` contains the graph specifications and all 30 graph–threshold cases; `*_节点对应.csv` maps numeric graph identifiers to geographic identifiers. Other candidate radii in the provenance files describe construction checks, not additional main-benchmark instances.

## Supplementary inputs

The supplementary archive contains generated repeated-pattern graphs, independent ER/BA/SBM graphs, and historical-profit NDR inputs used outside the main comparison. Their file names and roles are indexed separately. The study index lists the exact graph–threshold pairs used in the current manuscript's component and search-space figures and in the initial 24-instance calibration. The original 20-instance incremental study and the subsequently selected 20-instance learning/phase/tabu study have separate indices.
