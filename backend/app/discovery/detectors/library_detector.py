import re
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class LibraryDetector:
    def __init__(self):
        self.import_regex = re.compile(
            r"\b(import cryptography|from cryptography|import PyCryptodome|import paramiko|#include <openssl/|import ssl)\b",
            re.IGNORECASE
        )

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            match = self.import_regex.search(line)
            if match:
                findings.append(RawFinding(
                    detector="LibraryDetector-Import",
                    input_source="DependencyScanner",
                    file_resource=file_path,
                    line_number=idx,
                    finding_type="LibraryDependency",
                    matched_construct=match.group(0),
                    context=line.strip()[:200],
                    confidence=0.9,
                    evidence_type=EvidenceType.OBSERVED,
                    algorithm="CRYPTO_LIBRARY_IMPORT",
                    purpose=AlgPurpose.AUTHENTICATION
                ))
        return findings
