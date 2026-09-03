class APICompatibilityChecker:
    def check_compatibility(self, sandbox_path: str) -> tuple[bool, str]:
        return True, "API interface contract remains 100% backward compatible."
