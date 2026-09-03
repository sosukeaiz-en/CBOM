class RecommendationExplainer:
    def explain(self, candidate: dict, asset_name: str) -> str:
        pqc = candidate.get("recommended_pqc")
        ref = candidate.get("standard_ref")
        notes = candidate.get("compatibility_notes")
        return (
            f"Recommended {pqc} ({ref}) for asset '{asset_name}'. "
            f"Compatibility guidance: {notes}"
        )
