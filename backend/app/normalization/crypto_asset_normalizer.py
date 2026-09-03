from app.models.schemas import RawFinding
from app.models.enums import QuantumVulnerability, AssetCategory
from app.normalization.purpose_classifier import PurposeClassifier


class CryptoAssetNormalizer:
    def __init__(self):
        self.classifier = PurposeClassifier()

    def normalize(self, raw_finding: RawFinding) -> dict:
        alg = raw_finding.algorithm or "UNKNOWN_CRYPTO"
        purpose = raw_finding.purpose or self.classifier.classify(alg, raw_finding.matched_construct)

        # Determine quantum vulnerability
        alg_upper = alg.upper()
        if any(v in alg_upper for v in ["RSA", "ECDSA", "ECDH", "DSA", "DH"]):
            quantum_vuln = QuantumVulnerability.HIGH_VULNERABLE
        elif "AES-128" in alg_upper or "3DES" in alg_upper:
            quantum_vuln = QuantumVulnerability.MODERATE_WEAK
        elif any(s in alg_upper for s in ["AES-256", "SHA-256", "SHA-384", "SHA-512", "ML-KEM", "ML-DSA", "SLH-DSA"]):
            quantum_vuln = QuantumVulnerability.QUANTUM_RESISTANT
        else:
            quantum_vuln = QuantumVulnerability.HIGH_VULNERABLE

        category = AssetCategory.SOURCE_CODE
        if "Dependency" in raw_finding.detector or "Package" in raw_finding.finding_type:
            category = AssetCategory.DEPENDENCY
        elif "Certificate" in raw_finding.detector or "PEM" in raw_finding.finding_type:
            category = AssetCategory.CERTIFICATE
        elif "Container" in raw_finding.detector:
            category = AssetCategory.CONTAINER
        elif "Binary" in raw_finding.detector:
            category = AssetCategory.BINARY

        is_unknown = "UNKNOWN" in alg_upper or raw_finding.confidence < 0.6

        return {
            "name": f"{alg} ({raw_finding.matched_construct[:30]})",
            "category": category,
            "algorithm": alg,
            "key_length": raw_finding.key_length,
            "purpose": purpose,
            "location_file": raw_finding.file_resource,
            "location_line": raw_finding.line_number,
            "quantum_vulnerability": quantum_vuln,
            "is_unknown": is_unknown
        }
