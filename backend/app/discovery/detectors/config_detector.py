import re
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class ConfigDetector:
    def __init__(self):
        self.ssl_ciphers_regex = re.compile(r"\b(ssl_ciphers|ssl_protocols|TLSv1\.2|TLSv1\.3|SSLv3|ECDHE-RSA-AES128-GCM-SHA256)\b", re.IGNORECASE)

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            match = self.ssl_ciphers_regex.search(line)
            if match:
                findings.append(RawFinding(
                    detector="ConfigDetector-TLS",
                    input_source="ConfigScanner",
                    file_resource=file_path,
                    line_number=idx,
                    finding_type="ConfigurationSetting",
                    matched_construct=match.group(0),
                    context=line.strip()[:200],
                    confidence=0.8,
                    evidence_type=EvidenceType.OBSERVED,
                    algorithm="TLS_PROTOCOL_CONFIG",
                    purpose=AlgPurpose.AUTHENTICATION
                ))
        return findings
