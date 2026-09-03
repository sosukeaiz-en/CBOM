from typing import List
from app.models.db_models import CryptoAsset, Recommendation
from app.models.enums import AlgPurpose
from app.recommend.candidate_selector import CandidateSelector
from app.recommend.ranking import RecommendationRanker
from app.recommend.explanation import RecommendationExplainer


class RecommendationEngine:
    def __init__(self):
        self.selector = CandidateSelector()
        self.ranker = RecommendationRanker()
        self.explainer = RecommendationExplainer()

    def generate_recommendations(self, asset: CryptoAsset) -> List[dict]:
        candidates = self.selector.select_candidates(asset)
        ranked = self.ranker.rank_candidates(candidates)

        results = []
        for cand in ranked:
            explanation = self.explainer.explain(cand, asset.name)
            results.append({
                "target_pqc_candidate": cand["recommended_pqc"],
                "standard_reference": cand["standard_ref"],
                "status": cand["status"],
                "purpose": asset.purpose or AlgPurpose.SIGNATURE,
                "migration_complexity": cand["migration_complexity"],
                "performance_impact": cand["performance_impact"],
                "compatibility_notes": f"{cand['compatibility_notes']} | {explanation}",
                "confidence": 0.95
            })
        return results
