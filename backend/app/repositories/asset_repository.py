from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.db_models import CryptoAsset, Evidence, RiskAssessment
from app.models.enums import AssetCategory, QuantumVulnerability, AlgPurpose


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_asset(
        self,
        project_id: str,
        scan_id: str,
        name: str,
        category: AssetCategory,
        algorithm: str,
        location_file: str,
        location_line: Optional[int] = None,
        key_length: Optional[int] = None,
        purpose: Optional[AlgPurpose] = None,
        quantum_vulnerability: QuantumVulnerability = QuantumVulnerability.HIGH_VULNERABLE,
        is_unknown: bool = False
    ) -> CryptoAsset:
        asset = CryptoAsset(
            project_id=project_id,
            scan_id=scan_id,
            name=name,
            category=category,
            algorithm=algorithm,
            key_length=key_length,
            purpose=purpose,
            location_file=location_file,
            location_line=location_line,
            quantum_vulnerability=quantum_vulnerability,
            is_unknown=is_unknown
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_asset(self, asset_id: str) -> Optional[CryptoAsset]:
        return self.db.query(CryptoAsset).filter(CryptoAsset.id == asset_id).first()

    def get_by_project(self, project_id: str) -> List[CryptoAsset]:
        return self.db.query(CryptoAsset).filter(CryptoAsset.project_id == project_id).all()

    def get_by_scan(self, scan_id: str) -> List[CryptoAsset]:
        return self.db.query(CryptoAsset).filter(CryptoAsset.scan_id == scan_id).all()

    def add_evidence(
        self,
        asset_id: str,
        evidence_type: str,
        source_file: str,
        detector_name: str,
        line_number: Optional[int] = None,
        code_excerpt: Optional[str] = None,
        confidence_score: float = 1.0,
        provenance: str = "Static AST Analysis"
    ) -> Evidence:
        ev = Evidence(
            asset_id=asset_id,
            evidence_type=evidence_type,
            source_file=source_file,
            line_number=line_number,
            detector_name=detector_name,
            code_excerpt=code_excerpt,
            confidence_score=confidence_score,
            provenance=provenance
        )
        self.db.add(ev)
        self.db.commit()
        self.db.refresh(ev)
        return ev

    def get_evidences(self, asset_id: str) -> List[Evidence]:
        return self.db.query(Evidence).filter(Evidence.asset_id == asset_id).all()
