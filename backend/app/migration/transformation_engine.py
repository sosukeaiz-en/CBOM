import os


class TransformationEngine:
    def apply_transformation(self, file_path: str, old_str: str, new_str: str) -> bool:
        if not os.path.exists(file_path):
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if old_str in content:
                new_content = content.replace(old_str, new_str)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return True
        except Exception:
            pass
        return False
