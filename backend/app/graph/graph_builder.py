from typing import List
from app.models.db_models import CryptoAsset
from app.graph.dependency_graph import DependencyGraphManager
from app.models.schemas import GraphResponse, GraphNode, GraphEdge


class GraphBuilder:
    def __init__(self):
        self.graph_mgr = DependencyGraphManager()

    def get_graph_data(self, assets: List[CryptoAsset]) -> GraphResponse:
        g = self.graph_mgr.build_graph(assets)
        nodes = []
        edges = []

        for node, attrs in g.nodes(data=True):
            nodes.append(GraphNode(
                id=node,
                label=attrs.get("label", node),
                type=attrs.get("type", "unknown"),
                algorithm=attrs.get("algorithm")
            ))

        for u, v, attrs in g.edges(data=True):
            edges.append(GraphEdge(
                source=u,
                target=v,
                relation=attrs.get("relation", "depends_on")
            ))

        return GraphResponse(nodes=nodes, edges=edges)
