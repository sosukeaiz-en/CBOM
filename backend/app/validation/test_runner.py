from app.validation.build_validator import BuildValidator
from app.validation.crypto_validator import CryptoValidator
from app.validation.unit_test_runner import UnitTestRunner
from app.validation.integration_test_runner import IntegrationTestRunner
from app.validation.regression_runner import RegressionRunner
from app.validation.performance_runner import PerformanceRunner
from app.validation.api_compatibility import APICompatibilityChecker
from app.validation.result_analyzer import ValidationResultAnalyzer


class ValidationSuiteRunner:
    def __init__(self):
        self.build_val = BuildValidator()
        self.crypto_val = CryptoValidator()
        self.unit_runner = UnitTestRunner()
        self.integration_runner = IntegrationTestRunner()
        self.regression_runner = RegressionRunner()
        self.perf_runner = PerformanceRunner()
        self.api_checker = APICompatibilityChecker()
        self.analyzer = ValidationResultAnalyzer()

    def run_all_checks(self, sandbox_path: str) -> dict:
        results = {
            "build": self.build_val.validate_build(sandbox_path),
            "crypto": self.crypto_val.validate_crypto_correctness(sandbox_path),
            "unit": self.unit_runner.run_unit_tests(sandbox_path),
            "integration": self.integration_runner.run_integration_tests(sandbox_path),
            "regression": self.regression_runner.run_regression_tests(sandbox_path),
            "performance": self.perf_runner.run_performance_checks(sandbox_path),
            "api": self.api_checker.check_compatibility(sandbox_path)
        }

        overall_status, confidence, residual_risk = self.analyzer.analyze_results(results)

        logs = [f"[{k.upper()}] {v[1]}" for k, v in results.items()]

        return {
            "overall_status": overall_status,
            "build_passed": results["build"][0],
            "unit_tests_passed": results["unit"][0],
            "crypto_tests_passed": results["crypto"][0],
            "integration_tests_passed": results["integration"][0],
            "regression_passed": results["regression"][0],
            "api_compatible": results["api"][0],
            "migration_confidence": confidence,
            "residual_risk": residual_risk,
            "logs": logs
        }
