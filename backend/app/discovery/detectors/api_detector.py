import re
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose

API_PATTERNS = [
    {
        "regex": r"\b(EVP_DigestInit_ex|EVP_EncryptInit_ex|EVP_DecryptInit_ex|SSL_CTX_new|SSL_connect|SSL_accept)\b",
        "detector": "APIDetector-OpenSSL-EVP",
        "purpose": AlgPurpose.AUTHENTICATION
    },
    {
        "regex": r"\b(cipher\.encrypt|cipher\.decrypt|signer\.sign|verifier\.verify)\b",
        "detector": "APIDetector-PyCA-Cryptography",
        "purpose": AlgPurpose.SIGNATURE
    }
]


class APIDetector:
    def __init__(self):
        self.compiled = [(p, re.compile(p["regex"])) for p in API_PATTERNS]

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            for info, regex in self.compiled:
                match = regex.search(line)
                if match:
                    findings.append(RawFinding(
                        detector=info["detector"],
                        input_source="APIScanner",
                        file_resource=file_path,
                        line_number=idx,
                        finding_type="CryptoAPICall",
                        matched_construct=match.group(0),
                        context=line.strip()[:200],
                        confidence=0.85,
                        evidence_type=EvidenceType.OBSERVED,
                        algorithm="API_WRAPPED_CRYPTO",
                        purpose=info["purpose"]
                    ))
        return findings
