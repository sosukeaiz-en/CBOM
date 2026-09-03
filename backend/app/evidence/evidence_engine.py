from app.models.schemas import RawFinding
from app.models.enums import EvidenceType
from app.evidence.confidence import ConfidenceCalculator
from app.evidence.provenance import ProvenanceTracker


class EvidenceEngine:
    def __init__(self):
        self.confidence_calc = ConfidenceCalculator()
        self.provenance_tracker = ProvenanceTracker()

    def process_raw_finding(self, raw_finding: RawFinding) -> dict:
        confidence = self.confidence_calc.calculate(
            raw_finding.detector, raw_finding.matched_construct, raw_finding.evidence_type.value
        )
        provenance = self.provenance_tracker.get_provenance_info(raw_finding.detector)

        return {
            "evidence_type": raw_finding.evidence_type,
            "source_file": raw_finding.file_resource,
            "line_number": raw_finding.line_number,
            "detector_name": raw_finding.detector,
            "detector_version": "1.0.0",
            "code_excerpt": raw_finding.context,
            "confidence_score": confidence,
            "provenance": provenance
        }
