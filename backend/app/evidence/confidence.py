class ConfidenceCalculator:
    def calculate(self, detector_name: str, matched_construct: str, evidence_type: str) -> float:
        base_confidence = 0.8
        if "AST" in detector_name:
            base_confidence = 0.95
        elif "Certificate" in detector_name:
            base_confidence = 0.98
        elif "Algorithm" in detector_name:
            base_confidence = 0.90
        elif "Inferred" in evidence_type:
            base_confidence = 0.70
        elif "Assumed" in evidence_type:
            base_confidence = 0.50

        return min(1.0, max(0.0, base_confidence))
