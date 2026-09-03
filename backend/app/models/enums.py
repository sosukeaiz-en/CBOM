from enum import Enum


class ScanStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class EvidenceType(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    ASSUMED = "ASSUMED"
    EXTERNAL = "EXTERNAL"


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AlgPurpose(str, Enum):
    SIGNATURE = "signature"
    KEY_ESTABLISHMENT = "key_establishment"
    ENCRYPTION = "encryption"
    HASHING = "hashing"
    MAC = "mac"
    AUTHENTICATION = "authentication"


class StandardStatus(str, Enum):
    FINAL_STANDARD = "FINAL STANDARD"
    STANDARDIZATION_IN_PROGRESS = "STANDARDIZATION IN PROGRESS"
    RESEARCH_NON_STANDARD = "RESEARCH / NON-STANDARD"


class QuantumVulnerability(str, Enum):
    HIGH_VULNERABLE = "HIGH_VULNERABLE"
    MODERATE_WEAK = "MODERATE_WEAK"
    QUANTUM_RESISTANT = "QUANTUM_RESISTANT"
    SAFE = "SAFE"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ValidationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    PENDING = "PENDING"


class AssetCategory(str, Enum):
    SOURCE_CODE = "SOURCE_CODE"
    DEPENDENCY = "DEPENDENCY"
    CERTIFICATE = "CERTIFICATE"
    CONTAINER = "CONTAINER"
    BINARY = "BINARY"


class ThreatScenarioCategory(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"
