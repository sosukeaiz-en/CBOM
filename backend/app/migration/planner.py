from typing import List
from app.models.db_models import CryptoAsset
from app.migration.task_generator import TaskGenerator
from app.migration.effort_estimator import PlanEffortEstimator
from app.migration.scheduler import MigrationScheduler


class MigrationPlanner:
    def __init__(self):
        self.task_gen = TaskGenerator()
        self.effort_est = PlanEffortEstimator()
        self.scheduler = MigrationScheduler()

    def build_plan(self, plan_id: str, assets: List[CryptoAsset]) -> tuple[List[dict], float, float]:
        raw_tasks = self.task_gen.generate_tasks_for_assets(assets, plan_id)
        scheduled_tasks = self.scheduler.schedule_tasks(raw_tasks)
        person_days, calendar_days = self.effort_est.estimate(scheduled_tasks)

        return scheduled_tasks, person_days, calendar_days
