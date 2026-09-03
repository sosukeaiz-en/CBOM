from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.db_models import MigrationPlan, MigrationTask, ValidationRun
from app.models.enums import TaskStatus, ValidationStatus


class MigrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(
        self,
        project_id: str,
        title: str,
        strategy: str = "HYBRID",
        person_effort_days: float = 0.0,
        calendar_duration_days: float = 0.0
    ) -> MigrationPlan:
        plan = MigrationPlan(
            project_id=project_id,
            title=title,
            strategy=strategy,
            person_effort_days=person_effort_days,
            calendar_duration_days=calendar_duration_days
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_plan(self, plan_id: str) -> Optional[MigrationPlan]:
        return self.db.query(MigrationPlan).filter(MigrationPlan.id == plan_id).first()

    def get_plans_by_project(self, project_id: str) -> List[MigrationPlan]:
        return self.db.query(MigrationPlan).filter(MigrationPlan.project_id == project_id).all()

    def add_task(
        self,
        plan_id: str,
        asset_name: str,
        file_path: str,
        from_algorithm: str,
        to_algorithm: str,
        estimated_person_hours: float = 8.0,
        priority: int = 1,
        patch_diff: Optional[str] = None
    ) -> MigrationTask:
        task = MigrationTask(
            plan_id=plan_id,
            asset_name=asset_name,
            file_path=file_path,
            from_algorithm=from_algorithm,
            to_algorithm=to_algorithm,
            estimated_person_hours=estimated_person_hours,
            priority=priority,
            patch_diff=patch_diff
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def save_validation_run(
        self,
        plan_id: str,
        overall_status: ValidationStatus,
        build_passed: bool = True,
        unit_tests_passed: bool = True,
        crypto_tests_passed: bool = True,
        integration_tests_passed: bool = True,
        regression_passed: bool = True,
        api_compatible: bool = True,
        migration_confidence: float = 0.95,
        residual_risk: float = 10.0,
        logs: list = None
    ) -> ValidationRun:
        run = ValidationRun(
            plan_id=plan_id,
            overall_status=overall_status,
            build_passed=build_passed,
            unit_tests_passed=unit_tests_passed,
            crypto_tests_passed=crypto_tests_passed,
            integration_tests_passed=integration_tests_passed,
            regression_passed=regression_passed,
            api_compatible=api_compatible,
            migration_confidence=migration_confidence,
            residual_risk=residual_risk,
            logs_json=logs or []
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def get_validation_run(self, validation_id: str) -> Optional[ValidationRun]:
        return self.db.query(ValidationRun).filter(ValidationRun.id == validation_id).first()
