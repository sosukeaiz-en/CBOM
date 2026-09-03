from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.db_models import AuditEvent


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        action: str,
        project_id: Optional[str] = None,
        actor: str = "system",
        details: dict = None
    ) -> AuditEvent:
        event = AuditEvent(
            project_id=project_id,
            action=action,
            actor=actor,
            details_json=details or {}
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_by_project(self, project_id: str) -> List[AuditEvent]:
        return self.db.query(AuditEvent).filter(AuditEvent.project_id == project_id).order_by(AuditEvent.created_at.desc()).all()
