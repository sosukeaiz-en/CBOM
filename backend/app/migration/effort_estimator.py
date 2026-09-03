from typing import List


class PlanEffortEstimator:
    def estimate(self, tasks: List[dict]) -> tuple[float, float]:
        total_hours = sum(t.get("estimated_person_hours", 8.0) for t in tasks)
        person_days = round(total_hours / 8.0, 1)
        calendar_days = round(person_days / 2.0, 1)  # assuming 2 FTEs
        return person_days, calendar_days
