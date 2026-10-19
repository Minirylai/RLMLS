#!/usr/bin/env python3
"""Frozen structure/weight test grid, independent of solver outcomes."""
import argparse
import csv
import json
import math
import random
import statistics
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1] / "regenerated" / "structured"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for family_index, family in enumerate(("ER", "BA", "SBM")):
        for size_index, n in enumerate((500, 2000, 5000, 10000, 20000)):
            for degree_index, degree in enumerate((6, 30)):
                for replicate in range(3):
                    # Preserve the 48 prior untested topology seeds, append 42.
                    old_sizes = {500: 0, 2000: 1, 10000: 2}
                    if n in old_sizes and replicate < 2:
                        serial = family_index * 12 + old_sizes[n] * 4 + degree_index * 2 + replicate
                    elif n == 20000 and replicate < 2:
                        serial = 36 + family_index * 4 + degree_index * 2 + replicate
                    else:
                        extras = [(size, d, seed) for size in (500,2000,5000,10000,20000)
                                  for d in (6,30) for seed in range(3)
                                  if seed == 2 or size == 5000]
                        serial = 48 + family_index * 14 + extras.index((n, degree, replicate))
                    graph_seed = 2026101100 + serial
                    weight_seed = 2026101200 + serial
                    topology = f"structured_{family}_n{n}_d{degree}_s{replicate}"
                    if family == "ER":
                        parameters = {"p": degree / (n - 1)}
                        g = nx.fast_gnp_random_graph(n, seed=graph_seed, **parameters)
                    elif family == "BA":
                        parameters = {"m": degree // 2}
                        g = nx.barabasi_albert_graph(n, seed=graph_seed, **parameters)
                    else:
                        block_size = n // 4
                        within = 0.9 * degree / (block_size - 1)
                        between = 0.1 * degree / (n - block_size)
                        parameters = {"blocks": [block_size] * 4,
                                      "mixing": 0.1, "p_within": within,
                                      "p_between": between}
                        probabilities = [[within if a == b else between for b in range(4)]
                                         for a in range(4)]
                        g = nx.stochastic_block_model([block_size] * 4, probabilities,
                                                      seed=graph_seed, selfloops=False,
                                                      sparse=True)
                    assert len(g) == n and nx.number_of_selfloops(g) == 0
                    edges = sorted((min(u, v), max(u, v)) for u, v in g.edges())
                    degrees = [g.degree[u] for u in range(n)]
                    components = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
                    attributes = dict(n=n, m=len(edges), density=nx.density(g),
                                      mean_degree=statistics.mean(degrees),
                                      max_degree=max(degrees),
                                      degree_std=statistics.pstdev(degrees),
                                      components=len(components),
                                      largest_component=components[0],
                                      average_clustering=nx.average_clustering(g))
                    attributes.update(realized_cross_edge_fraction=None,
                                      planted_partition_modularity=None)
                    if family == "SBM":
                        cross = sum(u // block_size != v // block_size for u, v in edges)
                        volumes = [sum(degrees[b * block_size:(b + 1) * block_size])
                                   for b in range(4)]
                        fraction = cross / len(edges)
                        attributes.update(realized_cross_edge_fraction=fraction,
                            planted_partition_modularity=1 - fraction -
                            sum((volume / (2 * len(edges))) ** 2 for volume in volumes))
                    rng = random.Random(weight_seed)
                    uniform = [rng.randint(20, 49) for _ in range(n)]
                    weight_versions = {'uniform20_49': uniform}
                    for scheme, weights in weight_versions.items():
                        instance = f"{topology}_{scheme}"
                        path = ROOT / f"{instance}.txt"
                        with path.open("w") as handle:
                            handle.write(f"{n}\n")
                            for u, w in enumerate(weights):
                                handle.write(f"{u} {w}\n")
                            for u, v in edges:
                                handle.write(f"{u} {v}\n")
                        mean_weight = statistics.mean(weights)
                        std_weight = statistics.pstdev(weights)
                        mean_degree = statistics.mean(degrees)
                        std_degree = statistics.pstdev(degrees)
                        correlation = (sum((d - mean_degree) * (w - mean_weight)
                                           for d, w in zip(degrees, weights))
                                       / (n * std_degree * std_weight)
                                       if std_degree and std_weight else None)
                        manifest.append(dict(id=instance, suite="structured_20261010",
                                             family=family, topology=topology, cluster=topology,
                                             file=path.name, graph_seed=graph_seed,
                                             weight_seed=weight_seed if scheme != "unit" else None,
                                             weight_scheme=scheme, parameters=parameters,
                                             generation_library=f"networkx {nx.__version__}",
                                             heterogeneous_sigma=1.2 if scheme.startswith("heterogeneous") else None,
                                             heterogeneous_seed=weight_seed+1000000 if scheme.startswith("heterogeneous") else None,
                                             degree_tie_seed=weight_seed+2000000 if "degree_" in scheme else None,
                                             profit_total_matches_uniform=scheme != "unit",
                                             source="synthetic", **attributes,
                                             profit_min=min(weights), profit_max=max(weights),
                                             profit_sum=sum(weights), profit_cv=std_weight / mean_weight,
                                             profit_degree_correlation=correlation))
                    print(topology, "nodes", n, "edges", len(edges), flush=True)
    assert len(manifest) == 90 and len({x["topology"] for x in manifest}) == 90
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    fields = ["id", "family", "topology", "weight_scheme", "graph_seed", "weight_seed",
              "n", "m", "density", "mean_degree", "max_degree", "degree_std",
              "components", "largest_component", "average_clustering", "profit_min",
              "profit_max", "profit_sum", "profit_cv", "profit_degree_correlation",
              "realized_cross_edge_fraction", "planted_partition_modularity"]
    with (ROOT / "attributes.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(manifest)
    case_fields = ["case_id", "graph", "family", "topology", "weight_scheme",
                   "n", "m", "ratio", "K", "profit_sum", "file"]
    for filename, primary in (("cases_primary.csv", True),
                              ("cases_weight_control.csv", False)):
        with (ROOT / filename).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=case_fields)
            writer.writeheader()
            for entry in manifest:
                if (entry["weight_scheme"] == "uniform20_49") != primary:
                    continue
                for ratio in (0.6, 0.75, 0.9):
                    row = {key: entry[key] for key in case_fields
                           if key not in ("case_id", "graph", "ratio", "K")}
                    row.update(case_id=f"{entry['id']}_r{ratio}", graph=entry["id"],
                               ratio=ratio, K=int(ratio * entry["profit_sum"]))
                    writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    ROOT = parser.parse_args().output_dir
    main()
