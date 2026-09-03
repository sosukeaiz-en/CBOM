from app.models.db_models import CryptoAsset
from app.models.enums import QuantumVulnerability
from app.risk.mosca import MoscaCalculator
from app.risk.scoring import RiskScoreCalculator
from app.risk.criticality import CriticalityEvaluator
from app.risk.sensitivity import DataSensitivityEvaluator


class RiskEngine:
    def __init__(self):
        self.mosca_calc = MoscaCalculator()
        self.score_calc = RiskScoreCalculator()
        self.crit_eval = CriticalityEvaluator()
        self.sens_eval = DataSensitivityEvaluator()

    def assess_asset_risk(
        self,
        asset: CryptoAsset,
        data_sensitivity_str: str = "CONFIDENTIAL",
        business_criticality_str: str = "HIGH",
        external_exposure_score: float = 50.0,
        x_lifetime_years: float = 10.0,
        y_migration_years: float = 3.0,
        z_horizon_year: float = 2035.0
    ) -> dict:
        # Quantum vuln score
        if asset.quantum_vulnerability == QuantumVulnerability.HIGH_VULNERABLE:
            q_score = 100.0
        elif asset.quantum_vulnerability == QuantumVulnerability.MODERATE_WEAK:
            q_score = 65.0
        elif asset.quantum_vulnerability == QuantumVulnerability.QUANTUM_RESISTANT:
            q_score = 10.0
        else:
            q_score = 0.0

        sens_score = self.sens_eval.evaluate(data_sensitivity_str)
        crit_score = self.crit_eval.evaluate(business_criticality_str)
        mosca_score, urgency_flag, mosca_explanation = self.mosca_calc.calculate_urgency(
            x_lifetime_years, y_migration_years, z_horizon_year
        )
        complexity_score = 50.0 + (asset.centrality_score * 40.0)

        final_score, level = self.score_calc.compute_score(
            q_score, sens_score, crit_score, mosca_score, external_exposure_score, complexity_score
        )

        explanation = (
            f"Risk Level {level.value} ({final_score}/100) for asset '{asset.name}' using {asset.algorithm}. "
            f"{mosca_explanation}"
        )

        return {
            "risk_score": final_score,
            "risk_level": level,
            "quantum_vuln_score": q_score,
            "sensitivity_score": sens_score,
            "criticality_score": crit_score,
            "mosca_score": mosca_score,
            "exposure_score": external_exposure_score,
            "complexity_score": complexity_score,
            "mosca_data_lifetime_x": x_lifetime_years,
            "mosca_migration_time_y": y_migration_years,
            "mosca_quantum_horizon_z": z_horizon_year,
            "urgency_flag": urgency_flag,
            "explanation": explanation,
            "confidence": 0.90
        }
