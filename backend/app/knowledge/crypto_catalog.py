from app.models.enums import AlgPurpose, QuantumVulnerability, StandardStatus

CLASSICAL_CRYPTO_CATALOG = {
    "RSA": {
        "family": "Asymmetric",
        "purpose": AlgPurpose.SIGNATURE,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "Shor's algorithm breaks RSA key factorisation completely in polynomial time."
    },
    "RSA_ENCRYPTION": {
        "family": "Asymmetric",
        "purpose": AlgPurpose.KEY_ESTABLISHMENT,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "RSA key transport is vulnerable to quantum key retrieval."
    },
    "ECDSA": {
        "family": "ECC",
        "purpose": AlgPurpose.SIGNATURE,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "Elliptic Curve discrete logarithm problem broken by Shor's algorithm."
    },
    "ECDH": {
        "family": "ECC",
        "purpose": AlgPurpose.KEY_ESTABLISHMENT,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "ECDH key exchange completely broken by quantum computers."
    },
    "AES-128": {
        "family": "Symmetric",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_vulnerability": QuantumVulnerability.MODERATE_WEAK,
        "notes": "Grover's algorithm reduces effective security from 128 to 64 bits."
    },
    "AES-256": {
        "family": "Symmetric",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_vulnerability": QuantumVulnerability.QUANTUM_RESISTANT,
        "notes": "Grover's algorithm leaves 128 bits of security, considered quantum resistant."
    },
    "SHA-256": {
        "family": "Hash",
        "purpose": AlgPurpose.HASHING,
        "default_vulnerability": QuantumVulnerability.QUANTUM_RESISTANT,
        "notes": "Collision resistance reduced to 128 bits under Grover, safe for standard use."
    },
    "SHA-1": {
        "family": "Hash",
        "purpose": AlgPurpose.HASHING,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "Classically weak and broken, quantum impact accelerates deprecation."
    },
    "MD5": {
        "family": "Hash",
        "purpose": AlgPurpose.HASHING,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "Classically broken."
    },
    "3DES": {
        "family": "Symmetric",
        "purpose": AlgPurpose.ENCRYPTION,
        "default_vulnerability": QuantumVulnerability.HIGH_VULNERABLE,
        "notes": "Deprecated symmetric cipher with small block size."
    }
}
