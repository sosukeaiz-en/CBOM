import os


class LocationMapper:
    def sanitize_path(self, raw_path: str, base_dir: str = None) -> str:
        if base_dir and raw_path.startswith(base_dir):
            return os.path.relpath(raw_path, base_dir)
        return raw_path
