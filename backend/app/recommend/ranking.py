from typing import List


class RecommendationRanker:
    def rank_candidates(self, candidates: List[dict]) -> List[dict]:
        # Rank final NIST standards higher than research candidates
        def score_candidate(cand):
            status = cand.get("status", "")
            if status == "FINAL STANDARD":
                return 100
            elif status == "STANDARDIZATION IN PROGRESS":
                return 70
            return 30

        return sorted(candidates, key=score_candidate, reverse=True)
