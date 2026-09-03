import networkx as nx


class CentralityCalculator:
    def compute_centrality(self, graph: nx.DiGraph, asset_node_id: str) -> float:
        if asset_node_id not in graph:
            return 0.1
        try:
            centrality_map = nx.degree_centrality(graph)
            return round(centrality_map.get(asset_node_id, 0.1), 3)
        except Exception:
            return 0.1
