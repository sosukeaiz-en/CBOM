import os
import re
from typing import List
from app.scanners.base import BaseScanner
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class BinaryScanner(BaseScanner):
    def __init__(self):
        super().__init__(scanner_name="BinaryScanner", version="1.0.0")
        self.strings_regex = re.compile(
            rb"\b(OpenSSL|RSA_generate_key|EVP_aes_256_cbc|EVP_sha256|EC_KEY_new|mbedtls_|libcrypto)\b"
        )

    def scan(self, target_input: str) -> List[RawFinding]:
        findings = []
        if not os.path.isfile(target_input):
            return findings

        try:
            with open(target_input, "rb") as f:
                content = f.read(10 * 1024 * 1024)  # First 10MB binary search

            matches = self.strings_regex.finditer(content)
            for m in matches:
                matched_str = m.group(0).decode("utf-8", errors="ignore")
                findings.append(RawFinding(
                    detector="BinaryScanner-Strings",
                    input_source="CompiledBinary",
                    file_resource=target_input,
                    line_number=None,
                    finding_type="BinarySymbolMatch",
                    matched_construct=matched_str,
                    context=f"Embedded symbol match in binary: {matched_str}",
                    confidence=0.85,
                    evidence_type=EvidenceType.OBSERVED,
                    algorithm="RSA" if "RSA" in matched_str else ("AES-256" if "aes" in matched_str.lower() else "OpenSSL_Crypto"),
                    purpose=AlgPurpose.AUTHENTICATION
                ))
        except Exception:
            pass

        return findings
