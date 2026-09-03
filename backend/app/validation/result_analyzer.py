from app.models.enums import ValidationStatus


class ValidationResultAnalyzer:
    def analyze_results(self, test_results: dict) -> tuple[ValidationStatus, float, float]:
        all_passed = all(r[0] for r in test_results.values())
        if all_passed:
            status = ValidationStatus.PASSED
            confidence = 0.95
            residual_risk = 5.0
        else:
            status = ValidationStatus.FAILED
            confidence = 0.40
            residual_risk = 60.0
        return status, confidence, residual_risk
