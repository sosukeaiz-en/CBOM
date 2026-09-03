import concurrent.futures
from typing import Callable, Any

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class JobManager:
    def submit_job(self, fn: Callable, *args, **kwargs) -> concurrent.futures.Future:
        return executor.submit(fn, *args, **kwargs)


job_manager = JobManager()
