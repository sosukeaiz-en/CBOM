import os
from typing import List
from app.scanners.base import BaseScanner
from app.models.schemas import RawFinding
from app.discovery.detectors.certificate_detector import CertificateDetector
from app.utils.file_utils import list_files_recursive


class CertificateScanner(BaseScanner):
    def __init__(self):
        super().__init__(scanner_name="CertificateScanner", version="1.0.0")
        self.cert_detector = CertificateDetector()

    def scan(self, target_input: str) -> List[RawFinding]:
        findings = []
        if os.path.isfile(target_input):
            files = [target_input]
        elif os.path.isdir(target_input):
            files = list_files_recursive(target_input, extensions=[".pem", ".crt", ".cer", ".key", ".p12"])
        else:
            return findings

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                findings.extend(self.cert_detector.detect_in_file(file_path, content))
            except Exception:
                continue

        return findings
