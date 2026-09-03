from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import declarative_base, relationship
from app.models.enums import (
    ScanStatus, EvidenceType, RiskLevel, AlgPurpose, StandardStatus,
    QuantumVulnerability, TaskStatus, ValidationStatus, AssetCategory, ThreatScenarioCategory
)

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    repository_url = Column(String(512), nullable=True)
    local_path = Column(String(512), nullable=True)
    business_criticality = Column(String(50), default="HIGH")
    data_classification = Column(String(50), default="CONFIDENTIAL")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    scans = relationship("Scan", back_populates="project", cascade="all, delete-orphan")
    assets = relationship("CryptoAsset", back_populates="project", cascade="all, delete-orphan")
    migration_plans = relationship("MigrationPlan", back_populates="project", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="project", cascade="all, delete-orphan")


class Scan(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    status = Column(SQLEnum(ScanStatus), default=ScanStatus.PENDING)
    scanner_version = Column(String(50), default="1.0.0")
    rules_version = Column(String(50), default="1.0.0")
    files_scanned = Column(Integer, default=0)
    total_findings = Column(Integer, default=0)
    unknown_findings = Column(Integer, default=0)
    source_coverage_pct = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="scans")
    assets = relationship("CryptoAsset", back_populates="scan", cascade="all, delete-orphan")
    cbom_records = relationship("CBOMRecord", back_populates="scan", cascade="all, delete-orphan")


class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    scan_id = Column(String(36), ForeignKey("scans.id"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(SQLEnum(AssetCategory), default=AssetCategory.SOURCE_CODE)
    algorithm = Column(String(100), nullable=False)
    key_length = Column(Integer, nullable=True)
    purpose = Column(SQLEnum(AlgPurpose), nullable=True)
    location_file = Column(String(512), nullable=False)
    location_line = Column(Integer, nullable=True)
    quantum_vulnerability = Column(SQLEnum(QuantumVulnerability), default=QuantumVulnerability.HIGH_VULNERABLE)
    is_unknown = Column(Boolean, default=False)
    centrality_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="assets")
    scan = relationship("Scan", back_populates="assets")
    evidences = relationship("Evidence", back_populates="asset", cascade="all, delete-orphan")
    risk_assessment = relationship("RiskAssessment", back_populates="asset", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="asset", cascade="all, delete-orphan")


class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_id = Column(String(36), ForeignKey("crypto_assets.id"), nullable=False)
    evidence_type = Column(SQLEnum(EvidenceType), default=EvidenceType.OBSERVED)
    source_file = Column(String(512), nullable=False)
    line_number = Column(Integer, nullable=True)
    detector_name = Column(String(100), nullable=False)
    detector_version = Column(String(50), default="1.0.0")
    code_excerpt = Column(Text, nullable=True)
    confidence_score = Column(Float, default=1.0)
    provenance = Column(String(255), default="Static AST Analysis")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    asset = relationship("CryptoAsset", back_populates="evidences")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_id = Column(String(36), ForeignKey("crypto_assets.id"), nullable=False, unique=True)
    risk_score = Column(Float, nullable=False)  # 0 to 100
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    quantum_vuln_score = Column(Float, default=0.0)
    sensitivity_score = Column(Float, default=0.0)
    criticality_score = Column(Float, default=0.0)
    mosca_score = Column(Float, default=0.0)
    exposure_score = Column(Float, default=0.0)
    complexity_score = Column(Float, default=0.0)
    mosca_data_lifetime_x = Column(Float, default=10.0)  # X years
    mosca_migration_time_y = Column(Float, default=3.0)   # Y years
    mosca_quantum_horizon_z = Column(Float, default=2035.0) # Z year
    urgency_flag = Column(Boolean, default=False)  # True if X + Y > Z - current_year
    explanation = Column(Text, nullable=True)
    confidence = Column(Float, default=0.9)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    asset = relationship("CryptoAsset", back_populates="risk_assessment")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_id = Column(String(36), ForeignKey("crypto_assets.id"), nullable=False)
    target_pqc_candidate = Column(String(100), nullable=False)
    standard_reference = Column(String(255), nullable=False)
    status = Column(SQLEnum(StandardStatus), default=StandardStatus.FINAL_STANDARD)
    purpose = Column(SQLEnum(AlgPurpose), nullable=False)
    migration_complexity = Column(String(50), default="MEDIUM")
    performance_impact = Column(Text, nullable=True)
    compatibility_notes = Column(Text, nullable=True)
    confidence = Column(Float, default=0.95)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    asset = relationship("CryptoAsset", back_populates="recommendations")


class MigrationPlan(Base):
    __tablename__ = "migration_plans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    strategy = Column(String(100), default="HYBRID")
    person_effort_days = Column(Float, default=0.0)
    calendar_duration_days = Column(Float, default=0.0)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    assumptions_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="migration_plans")
    tasks = relationship("MigrationTask", back_populates="plan", cascade="all, delete-orphan")
    validations = relationship("ValidationRun", back_populates="plan", cascade="all, delete-orphan")


class MigrationTask(Base):
    __tablename__ = "migration_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    plan_id = Column(String(36), ForeignKey("migration_plans.id"), nullable=False)
    asset_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    from_algorithm = Column(String(100), nullable=False)
    to_algorithm = Column(String(100), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    estimated_person_hours = Column(Float, default=8.0)
    priority = Column(Integer, default=1)
    dependencies_json = Column(JSON, nullable=True)
    patch_diff = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    plan = relationship("MigrationPlan", back_populates="tasks")


class ValidationRun(Base):
    __tablename__ = "validation_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    plan_id = Column(String(36), ForeignKey("migration_plans.id"), nullable=False)
    overall_status = Column(SQLEnum(ValidationStatus), default=ValidationStatus.PENDING)
    build_passed = Column(Boolean, default=False)
    unit_tests_passed = Column(Boolean, default=False)
    crypto_tests_passed = Column(Boolean, default=False)
    integration_tests_passed = Column(Boolean, default=False)
    regression_passed = Column(Boolean, default=False)
    api_compatible = Column(Boolean, default=False)
    migration_confidence = Column(Float, default=0.0)
    residual_risk = Column(Float, default=0.0)
    logs_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    plan = relationship("MigrationPlan", back_populates="validations")


class ThreatScenario(Base):
    __tablename__ = "threat_scenarios"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    category = Column(SQLEnum(ThreatScenarioCategory), default=ThreatScenarioCategory.MODERATE)
    quantum_horizon_year = Column(Integer, default=2035)
    description = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    action = Column(String(100), nullable=False)
    actor = Column(String(100), default="system")
    scanner_version = Column(String(50), default="1.0.0")
    rules_version = Column(String(50), default="1.0.0")
    details_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="audit_events")


class CBOMRecord(Base):
    __tablename__ = "cbom_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scan_id = Column(String(36), ForeignKey("scans.id"), nullable=False)
    cbom_json = Column(JSON, nullable=False)
    spec_version = Column(String(50), default="1.6")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    scan = relationship("Scan", back_populates="cbom_records")


# Reference Catalogs
class AlgorithmCatalog(Base):
    __tablename__ = "algorithm_catalog"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    family = Column(String(50), nullable=False)
    purpose = Column(SQLEnum(AlgPurpose), nullable=False)
    default_quantum_vuln = Column(SQLEnum(QuantumVulnerability), default=QuantumVulnerability.HIGH_VULNERABLE)
    nist_status = Column(SQLEnum(StandardStatus), default=StandardStatus.FINAL_STANDARD)
    recommended_pqc = Column(String(100), nullable=True)


class StandardCatalog(Base):
    __tablename__ = "standard_catalog"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    standard_name = Column(String(100), nullable=False)  # e.g., FIPS 203, FIPS 204
    pqc_algorithm = Column(String(100), nullable=False) # e.g., ML-KEM, ML-DSA
    purpose = Column(SQLEnum(AlgPurpose), nullable=False)
    status = Column(SQLEnum(StandardStatus), default=StandardStatus.FINAL_STANDARD)
    reference_url = Column(String(512), nullable=True)
