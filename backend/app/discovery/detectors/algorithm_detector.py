import re
from typing import List, Optional
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose

PATTERNS = [
    # RSA patterns
    {
        "regex": r"\b(RSA_generate_key|EVP_PKEY_RSA|EVP_rsa|RSA_public_encrypt|RSA_private_decrypt|rsa\.generate_private_key|RSAPrivateKey|RSA_new|RSA_PKCS1_PADDING)\b",
        "algorithm": "RSA",
        "purpose": AlgPurpose.SIGNATURE,
        "default_key_length": 2048,
        "detector": "AlgorithmDetector-RSA"
    },
    # ECC / ECDSA / ECDH patterns
    {
        "regex": r"\b(EC_KEY_new|EC_KEY_new_by_curve_name|EVP_PKEY_EC|EVP_ecdsa|ECDSA_sign|ECDSA_verify|ec\.generate_private_key|SECP256R1|prime256v1|ECDH_compute_key)\b",
        "algorithm": "ECDSA",
        "purpose": AlgPurpose.SIGNATURE,
        "default_key_length": 256,
        "detector": "AlgorithmDetector-ECC"
    },
    # AES patterns
    {
        "regex": r"\b(EVP_aes_256_cbc|EVP_aes_128_gcm|EVP_aes_256_gcm|AES_encrypt|AES_cbc_encrypt|Cipher\(algorithms\.AES|AES\.new)\b",
        "algorithm": "AES-256" if "256" else "AES-128",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_key_length": 256,
        "detector": "AlgorithmDetector-AES"
    },
    # SHA-2 patterns
    {
        "regex": r"\b(SHA256_Init|EVP_sha256|hashes\.SHA256|hashlib\.sha256|SHA384_Init|SHA512_Init)\b",
        "algorithm": "SHA-256",
        "purpose": AlgPurpose.HASHING,
        "default_key_length": None,
        "detector": "AlgorithmDetector-SHA2"
    },
    # Legacy / Weak Hash MD5 & SHA-1
    {
        "regex": r"\b(MD5_Init|EVP_md5|hashlib\.md5|SHA1_Init|EVP_sha1|hashlib\.sha1)\b",
        "algorithm": "MD5" if "md5" else "SHA-1",
        "purpose": AlgPurpose.HASHING,
        "default_key_length": None,
        "detector": "AlgorithmDetector-WeakHash"
    },
    # DES / 3DES patterns
    {
        "regex": r"\b(DES_ecb_encrypt|DES_ncbc_encrypt|EVP_des_ede3_cbc|TripleDES|DES\.new)\b",
        "algorithm": "3DES",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_key_length": 168,
        "detector": "AlgorithmDetector-DES"
    },
    # ChaCha20
    {
        "regex": r"\b(EVP_chacha20|ChaCha20Poly1305|ChaCha20)\b",
        "algorithm": "ChaCha20",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_key_length": 256,
        "detector": "AlgorithmDetector-ChaCha"
    }
]


class AlgorithmDetector:
    def __init__(self):
        self.compiled_patterns = [
            (p, re.compile(p["regex"], re.IGNORECASE)) for p in PATTERNS
        ]

    def detect_in_file(self, file_path: str, content: str) -> List[RawFinding]:
        findings = []
        lines = content.splitlines()

        for line_idx, line in enumerate(lines, start=1):
            for pattern_info, regex in self.compiled_patterns:
                match = regex.search(line)
                if match:
                    matched_str = match.group(0)

                    # Determine specific algorithm from matched string if possible
                    alg_name = pattern_info["algorithm"]
                    if "md5" in matched_str.lower():
                        alg_name = "MD5"
                    elif "sha1" in matched_str.lower():
                        alg_name = "SHA-1"
                    elif "256" in matched_str:
                        alg_name = "AES-256" if "aes" in matched_str.lower() else "SHA-256"
                    elif "128" in matched_str:
                        alg_name = "AES-128"

                    finding = RawFinding(
                        detector=pattern_info["detector"],
                        input_source="SourceCodeScanner",
                        file_resource=file_path,
                        line_number=line_idx,
                        finding_type="AlgorithmUsage",
                        matched_construct=matched_str,
                        context=line.strip()[:200],
                        confidence=0.9,
                        evidence_type=EvidenceType.OBSERVED,
                        algorithm=alg_name,
                        key_length=pattern_info["default_key_length"],
                        purpose=pattern_info["purpose"]
                    )
                    findings.append(finding)
        return findings
