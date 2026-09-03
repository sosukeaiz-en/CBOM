from typing import List
from app.models.db_models import CryptoAsset
from app.models.enums import AlgPurpose
from app.knowledge.mapping_rules import find_recommendations_for_asset


class CandidateSelector:
    def select_candidates(self, asset: CryptoAsset) -> List[dict]:
        return find_recommendations_for_asset(asset.algorithm, asset.purpose)
