from typing import List
from app.migration.dependency_scheduler import DependencyScheduler


class MigrationScheduler:
    def __init__(self):
        self.dep_scheduler = DependencyScheduler()

    def schedule_tasks(self, tasks: List[dict]) -> List[dict]:
        return self.dep_scheduler.sort_by_dependencies(tasks)
