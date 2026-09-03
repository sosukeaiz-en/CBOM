from typing import List
from app.models.db_models import CryptoAsset
from app.graph.dependency_graph import DependencyGraphManager
from app.graph.centrality import CentralityCalculator
from app.models.schemas import ImpactResponse


class ImpactAnalyzer:
    def __init__(self):
        self.graph_mgr = DependencyGraphManager()
        self.centrality_calc = CentralityCalculator()

    def analyze_asset_impact(self, target_asset: CryptoAsset, all_assets: List[CryptoAsset]) -> ImpactResponse:
        g = self.graph_mgr.build_graph(all_assets)
        node_id = f"asset:{target_asset.id}"
        centrality = self.centrality_calc.compute_centrality(g, node_id)

        affected_files = [target_asset.location_file]
        affected_components = [target_asset.name]

        for a in all_assets:
            if a.id != target_asset.id and a.location_file == target_asset.location_file:
                affected_components.append(a.name)

        return ImpactResponse(
            asset_id=target_asset.id,
            asset_name=target_asset.name,
            centrality_score=centrality,
            affected_files=list(set(affected_files)),
            affected_components=list(set(affected_components)),
            dependent_services_count=len(affected_files) * 2,
            protocol_impact=f"Impacts protocol handling in {target_asset.location_file}",
            vendor_impact="Requires vendor PQC compatibility check"
        )
