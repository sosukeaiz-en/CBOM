import networkx as nx
from typing import List
from app.models.db_models import CryptoAsset


class DependencyGraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, assets: List[CryptoAsset]) -> nx.DiGraph:
        self.graph.clear()
        file_nodes = set()

        for asset in assets:
            asset_node = f"asset:{asset.id}"
            file_node = f"file:{asset.location_file}"

            self.graph.add_node(asset_node, label=asset.name, type="asset", algorithm=asset.algorithm)
            self.graph.add_node(file_node, label=asset.location_file, type="file")

            file_nodes.add(file_node)
            self.graph.add_edge(file_node, asset_node, relation="contains")

        # Connect files that share imports / paths
        file_list = list(file_nodes)
        for i in range(len(file_list)):
            for j in range(i + 1, len(file_list)):
                # If they share directory or module name
                dir1 = file_list[i].rsplit("/", 1)[0]
                dir2 = file_list[j].rsplit("/", 1)[0]
                if dir1 == dir2:
                    self.graph.add_edge(file_list[i], file_list[j], relation="depends_on")

        return self.graph
