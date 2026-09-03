from app.models.enums import RiskLevel


class RiskScoreCalculator:
    def __init__(self, weights: dict = None):
        self.weights = weights or {
            "quantum_vuln": 0.25,
            "data_sensitivity": 0.20,
            "business_criticality": 0.20,
            "mosca_factor": 0.20,
            "exposure": 0.10,
            "complexity": 0.05
        }

    def compute_score(
        self,
        quantum_score: float,
        sensitivity_score: float,
        criticality_score: float,
        mosca_score: float,
        exposure_score: float,
        complexity_score: float
    ) -> tuple[float, RiskLevel]:
        w = self.weights
        total_score = (
            (quantum_score * w["quantum_vuln"]) +
            (sensitivity_score * w["data_sensitivity"]) +
            (criticality_score * w["business_criticality"]) +
            (mosca_score * w["mosca_factor"]) +
            (exposure_score * w["exposure"]) +
            (complexity_score * w["complexity"])
        )

        final_score = round(min(100.0, max(0.0, total_score)), 2)

        if final_score >= 80.0:
            level = RiskLevel.CRITICAL
        elif final_score >= 60.0:
            level = RiskLevel.HIGH
        elif final_score >= 40.0:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return final_score, level
