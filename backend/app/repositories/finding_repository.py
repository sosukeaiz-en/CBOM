from typing import List
from sqlalchemy.orm import Session
from app.models.db_models import Evidence, CryptoAsset


class FindingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_findings_by_project(self, project_id: str) -> List[Evidence]:
        return (
            self.db.query(Evidence)
            .join(CryptoAsset)
            .filter(CryptoAsset.project_id == project_id)
            .all()
        )
