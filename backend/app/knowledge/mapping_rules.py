from app.models.enums import AlgPurpose, StandardStatus

MAPPING_RULES = [
    {
        "source_purpose": AlgPurpose.SIGNATURE,
        "classical_algs": ["RSA", "ECDSA", "DSA"],
        "recommended_pqc": "ML-DSA-65",
        "standard_ref": "FIPS 204",
        "status": StandardStatus.FINAL_STANDARD,
        "migration_complexity": "MEDIUM",
        "performance_impact": "Slightly larger signature size (~2.4KB). Verification is very fast.",
        "compatibility_notes": "Requires protocol payload buffer size adjustment for signatures."
    },
    {
        "source_purpose": AlgPurpose.KEY_ESTABLISHMENT,
        "classical_algs": ["RSA_ENCRYPTION", "ECDH", "DH"],
        "recommended_pqc": "ML-KEM-768",
        "standard_ref": "FIPS 203",
        "status": StandardStatus.FINAL_STANDARD,
        "migration_complexity": "MEDIUM",
        "performance_impact": "Minimal latency penalty, fast key generation.",
        "compatibility_notes": "Replace key exchange mechanism with KEM pattern (encapsulate/decapsulate)."
    },
    {
        "source_purpose": AlgPurpose.ENCRYPTION,
        "classical_algs": ["AES-128", "3DES", "DES"],
        "recommended_pqc": "AES-256-GCM",
        "standard_ref": "NIST SP 800-38D",
        "status": StandardStatus.FINAL_STANDARD,
        "migration_complexity": "LOW",
        "performance_impact": "Negligible hardware acceleration support (AES-NI).",
        "compatibility_notes": "Upgrade symmetric key size to 256 bits to achieve 128-bit quantum security."
    },
    {
        "source_purpose": AlgPurpose.HASHING,
        "classical_algs": ["SHA-1", "MD5"],
        "recommended_pqc": "SHA-256",
        "standard_ref": "FIPS 180-4",
        "status": StandardStatus.FINAL_STANDARD,
        "migration_complexity": "LOW",
        "performance_impact": "Improved performance with modern CPU instructions.",
        "compatibility_notes": "Drop broken legacy hash algorithms immediately."
    }
]


def find_recommendations_for_asset(algorithm: str, purpose: AlgPurpose = None) -> list[dict]:
    results = []
    alg_upper = algorithm.upper()

    for rule in MAPPING_RULES:
        match_purpose = (purpose is None or rule["source_purpose"] == purpose)
        match_alg = any(c_alg in alg_upper for c_alg in rule["classical_algs"])

        if match_purpose or match_alg:
            results.append(rule)

    if not results:
        results.append({
            "source_purpose": purpose or AlgPurpose.AUTHENTICATION,
            "classical_algs": [algorithm],
            "recommended_pqc": "No standardized candidate found",
            "standard_ref": "N/A",
            "status": StandardStatus.RESEARCH_NON_STANDARD,
            "migration_complexity": "HIGH",
            "performance_impact": "Unknown",
            "compatibility_notes": "No direct NIST FIPS replacement identified. Manual review required."
        })
    return results
