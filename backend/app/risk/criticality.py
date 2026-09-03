class CriticalityEvaluator:
    def evaluate(self, business_criticality_str: str) -> float:
        mapping = {
            "CRITICAL": 100.0,
            "HIGH": 80.0,
            "MEDIUM": 50.0,
            "LOW": 20.0
        }
        return mapping.get(business_criticality_str.upper(), 70.0)
