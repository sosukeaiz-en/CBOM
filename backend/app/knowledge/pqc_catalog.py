from app.models.enums import AlgPurpose, StandardStatus

PQC_CATALOG = {
    "FIPS 203 / ML-KEM": {
        "name": "ML-KEM",
        "standard_ref": "FIPS 203",
        "purpose": AlgPurpose.KEY_ESTABLISHMENT,
        "status": StandardStatus.FINAL_STANDARD,
        "variants": ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"],
        "description": "Module-Lattice-Based Key-Encapsulation Mechanism Standard (NIST FIPS 203).",
        "performance_notes": "Fast execution, larger public key size compared to ECC (768 bytes for ML-KEM-512)."
    },
    "FIPS 204 / ML-DSA": {
        "name": "ML-DSA",
        "standard_ref": "FIPS 204",
        "purpose": AlgPurpose.SIGNATURE,
        "status": StandardStatus.FINAL_STANDARD,
        "variants": ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"],
        "description": "Module-Lattice-Based Digital Signature Standard (NIST FIPS 204).",
        "performance_notes": "High signature creation speed, public key ~1.3KB, signature ~2.4KB."
    },
    "FIPS 205 / SLH-DSA": {
        "name": "SLH-DSA",
        "standard_ref": "FIPS 205",
        "purpose": AlgPurpose.SIGNATURE,
        "status": StandardStatus.FINAL_STANDARD,
        "variants": ["SLH-DSA-SHA2-128f", "SLH-DSA-SHAKE-128f"],
        "description": "Stateless Hash-Based Digital Signature Standard (NIST FIPS 205).",
        "performance_notes": "Conservative security baseline based purely on hash functions, larger signature sizes."
    },
    "FN-DSA / Falcon": {
        "name": "Falcon / FN-DSA",
        "standard_ref": "NIST PQC Draft",
        "purpose": AlgPurpose.SIGNATURE,
        "status": StandardStatus.STANDARDIZATION_IN_PROGRESS,
        "variants": ["Falcon-512", "Falcon-1024"],
        "description": "NTRU-lattice based signature algorithm, compact public keys and signatures.",
        "performance_notes": "Requires floating point operations during signing."
    },
    "FrodoKEM": {
        "name": "FrodoKEM",
        "standard_ref": "Academic Research",
        "purpose": AlgPurpose.KEY_ESTABLISHMENT,
        "status": StandardStatus.RESEARCH_NON_STANDARD,
        "variants": ["FrodoKEM-640", "FrodoKEM-976"],
        "description": "Unstructured lattice-based KEM, ultra-conservative security but higher overhead.",
        "performance_notes": "Large key sizes and higher bandwidth usage."
    }
}
