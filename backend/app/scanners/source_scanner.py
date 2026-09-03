import os
from typing import List
from app.scanners.base import BaseScanner
from app.models.schemas import RawFinding
from app.discovery.detectors.algorithm_detector import AlgorithmDetector
from app.discovery.detectors.api_detector import APIDetector
from app.discovery.detectors.config_detector import ConfigDetector
from app.discovery.detectors.library_detector import LibraryDetector
from app.discovery.detectors.protocol_detector import ProtocolDetector
from app.discovery.detectors.certificate_detector import CertificateDetector
from app.scanners.parsers.python_parser import PythonASTParser
from app.discovery.deduplication import deduplicate_findings
from app.utils.file_utils import list_files_recursive

SUPPORTED_EXTENSIONS = [
    ".py", ".c", ".h", ".cpp", ".hpp", ".cc", ".java", ".go", ".rs", ".js", ".ts",
    ".pem", ".crt", ".key", ".conf", ".yaml", ".yml", ".json", ".txt"
]


class SourceScanner(BaseScanner):
    def __init__(self):
        super().__init__(scanner_name="SourceScanner", version="1.0.0")
        self.alg_detector = AlgorithmDetector()
        self.api_detector = APIDetector()
        self.config_detector = ConfigDetector()
        self.lib_detector = LibraryDetector()
        self.proto_detector = ProtocolDetector()
        self.cert_detector = CertificateDetector()
        self.py_parser = PythonASTParser()

    def scan(self, target_input: str) -> List[RawFinding]:
        findings: List[RawFinding] = []

        if os.path.isfile(target_input):
            files_to_scan = [target_input]
        elif os.path.isdir(target_input):
            files_to_scan = list_files_recursive(target_input, extensions=SUPPORTED_EXTENSIONS)
        else:
            return []

        for file_path in files_to_scan:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Run detectors
                findings.extend(self.alg_detector.detect_in_file(file_path, content))
                findings.extend(self.api_detector.detect_in_file(file_path, content))
                findings.extend(self.config_detector.detect_in_file(file_path, content))
                findings.extend(self.lib_detector.detect_in_file(file_path, content))
                findings.extend(self.proto_detector.detect_in_file(file_path, content))
                findings.extend(self.cert_detector.detect_in_file(file_path, content))

                if file_path.endswith(".py"):
                    findings.extend(self.py_parser.parse_code(file_path, content))

            except Exception:
                continue

        return deduplicate_findings(findings)
