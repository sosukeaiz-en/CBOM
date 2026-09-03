from typing import List
from app.models.db_models import Project, CryptoAsset, RiskAssessment


class ExecutiveSummaryGenerator:
    def generate_summary_text(self, project: Project, assets: List[CryptoAsset], risks: List[RiskAssessment]) -> str:
        total_assets = len(assets)
        critical_risks = sum(1 for r in risks if r.risk_level.value == "CRITICAL")
        high_risks = sum(1 for r in risks if r.risk_level.value == "HIGH")

        return (
            f"EXECUTIVE CRYPTOGRAPHIC RISK SUMMARY FOR {project.name.upper()}\n"
            f"===========================================================\n"
            f"Business Criticality: {project.business_criticality}\n"
            f"Data Classification: {project.data_classification}\n"
            f"Total Discovered Cryptographic Assets: {total_assets}\n"
            f"Critical Quantum Vulnerabilities: {critical_risks}\n"
            f"High Quantum Vulnerabilities: {high_risks}\n"
            f"Recommended Next Action: Initiate PQC Migration Planning for legacy RSA/ECDSA/ECDH algorithms.\n"
        )
