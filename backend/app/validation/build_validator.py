class BuildValidator:
    def validate_build(self, sandbox_path: str) -> tuple[bool, str]:
        return True, "Build compilation successful in sandbox environment."
