import os
import shutil
import tempfile
from app.core.exceptions import SandboxExecutionException


class MigrationSandbox:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or tempfile.gettempdir()

    def create_sandbox(self, project_path: str) -> str:
        sandbox_path = tempfile.mkdtemp(prefix="ecdat_sandbox_")
        if os.path.exists(project_path) and os.path.isdir(project_path):
            shutil.copytree(project_path, sandbox_path, dirs_exist_ok=True)
        return sandbox_path

    def cleanup(self, sandbox_path: str):
        if os.path.exists(sandbox_path) and "ecdat_sandbox_" in sandbox_path:
            shutil.rmtree(sandbox_path, ignore_errors=True)
