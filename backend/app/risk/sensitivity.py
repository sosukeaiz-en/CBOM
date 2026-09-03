class DataSensitivityEvaluator:
    def evaluate(self, data_classification_str: str) -> float:
        mapping = {
            "TOP_SECRET": 100.0,
            "CONFIDENTIAL": 80.0,
            "RESTRICTED": 60.0,
            "PUBLIC": 10.0
        }
        return mapping.get(data_classification_str.upper(), 75.0)
