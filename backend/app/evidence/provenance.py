class ProvenanceTracker:
    def get_provenance_info(self, detector_name: str, scanner_version: str = "1.0.0") -> str:
        return f"Detected via {detector_name} (version {scanner_version})"
