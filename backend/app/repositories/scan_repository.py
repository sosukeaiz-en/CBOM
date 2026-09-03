from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.db_models import Scan, CBOMRecord
from app.models.enums import ScanStatus


class ScanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_id: str, scanner_version: str = "1.0.0") -> Scan:
        db_obj = Scan(
            project_id=project_id,
            scanner_version=scanner_version,
            status=ScanStatus.PENDING
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, scan_id: str) -> Optional[Scan]:
        return self.db.query(Scan).filter(Scan.id == scan_id).first()

    def get_by_project(self, project_id: str) -> List[Scan]:
        return self.db.query(Scan).filter(Scan.project_id == project_id).order_by(Scan.created_at.desc()).all()

    def update_status(self, scan_id: str, status: ScanStatus, error_message: str = None) -> Optional[Scan]:
        db_obj = self.get(scan_id)
        if not db_obj:
            return None
        db_obj.status = status
        if error_message:
            db_obj.error_message = error_message
        if status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED]:
            db_obj.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def save_cbom(self, scan_id: str, cbom_json: dict, spec_version: str = "1.6") -> CBOMRecord:
        record = CBOMRecord(
            scan_id=scan_id,
            cbom_json=cbom_json,
            spec_version=spec_version
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_cbom(self, scan_id: str) -> Optional[CBOMRecord]:
        return self.db.query(CBOMRecord).filter(CBOMRecord.scan_id == scan_id).order_by(CBOMRecord.created_at.desc()).first()
