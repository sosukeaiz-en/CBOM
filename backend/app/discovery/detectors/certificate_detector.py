import re
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class CertificateDetector:
    def __init__(self):
        self.cert_regex = re.compile(
            r"-----BEGIN (CERTIFICATE|RSA PRIVATE KEY|EC PRIVATE KEY|PRIVATE KEY|X509 CERTIFICATE)-----",
            re.IGNORECASE
        )

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            match = self.cert_regex.search(line)
            if match:
                block_type = match.group(1)
                is_private_key = "PRIVATE KEY" in block_type.upper()
                alg = "RSA" if "RSA" in block_type.upper() else ("ECC" if "EC" in block_type.upper() else "X509_CERT")
                
                findings.append(RawFinding(
                    detector="CertificateDetector-PEM",
                    input_source="CertificateScanner",
                    file_resource=file_path,
                    line_number=idx,
                    finding_type="PEM_Block_Found",
                    matched_construct=f"PEM Header: {match.group(0)} (Metadata logged only, NO key stored)",
                    context=f"PEM block marker found at line {idx}",
                    confidence=0.98,
                    evidence_type=EvidenceType.OBSERVED,
                    algorithm=alg,
                    purpose=AlgPurpose.SIGNATURE if is_private_key else AlgPurpose.AUTHENTICATION
                ))
        return findings
