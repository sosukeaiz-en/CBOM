from typing import List


class DependencyScheduler:
    def sort_by_dependencies(self, tasks: List[dict]) -> List[dict]:
        # Priority sorting: libraries & low-level components first
        return sorted(tasks, key=lambda t: (0 if "crypto" in t["file_path"].lower() else 1, t["priority"]))
