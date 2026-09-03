import re
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class ProtocolDetector:
    def __init__(self):
        self.protocol_regex = re.compile(r"\b(TLSv1_2_client_method|TLSv1_3_client_method|ssh-rsa|ecdsa-sha2-nistp256)\b", re.IGNORECASE)

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            match = self.protocol_regex.search(line)
            if match:
                findings.append(RawFinding(
                    detector="ProtocolDetector",
                    input_source="ProtocolScanner",
                    file_resource=file_path,
                    line_number=idx,
                    finding_type="ProtocolUsage",
                    matched_construct=match.group(0),
                    context=line.strip()[:200],
                    confidence=0.88,
                    evidence_type=EvidenceType.OBSERVED,
                    algorithm="TLS_SSH_PROTOCOL",
                    purpose=AlgPurpose.KEY_ESTABLISHMENT
                ))
        return findings
