from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import (
    ScanStatus, EvidenceType, RiskLevel, AlgPurpose, StandardStatus,
    QuantumVulnerability, TaskStatus, ValidationStatus, AssetCategory, ThreatScenarioCategory
)


# Health
class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    timestamp: datetime


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    username: str
    password: str


# Projects
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    local_path: Optional[str] = None
    business_criticality: str = "HIGH"
    data_classification: str = "CONFIDENTIAL"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    local_path: Optional[str] = None
    business_criticality: Optional[str] = None
    data_classification: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Scans
class ScanCreate(BaseModel):
    scanner_version: Optional[str] = "1.0.0"
    target_path: Optional[str] = None


class ScanResponse(BaseModel):
    id: str
    project_id: str
    status: ScanStatus
    scanner_version: str
    rules_version: str
    files_scanned: int
    total_findings: int
    unknown_findings: int
    source_coverage_pct: float
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Scan Inputs
class SourceScanInput(BaseModel):
    source_path: str
    recursive: bool = True


class ContainerScanInput(BaseModel):
    image_name: str
    tag: str = "latest"


class BinaryScanInput(BaseModel):
    binary_path: str


class CertificateScanInput(BaseModel):
    cert_path_or_domain: str


# Raw Finding Interface
class RawFinding(BaseModel):
    detector: str
    input_source: str
    file_resource: str
    line_number: Optional[int] = None
    finding_type: str
    matched_construct: str
    context: Optional[str] = None
    confidence: float = 1.0
    evidence_type: EvidenceType = EvidenceType.OBSERVED
    algorithm: Optional[str] = None
    key_length: Optional[int] = None
    purpose: Optional[AlgPurpose] = None


# Inventory & Assets
class EvidenceResponse(BaseModel):
    id: str
    asset_id: str
    evidence_type: EvidenceType
    source_file: str
    line_number: Optional[int] = None
    detector_name: str
    detector_version: str
    code_excerpt: Optional[str] = None
    confidence_score: float
    provenance: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetResponse(BaseModel):
    id: str
    project_id: str
    scan_id: str
    name: str
    category: AssetCategory
    algorithm: str
    key_length: Optional[int] = None
    purpose: Optional[AlgPurpose] = None
    location_file: str
    location_line: Optional[int] = None
    quantum_vulnerability: QuantumVulnerability
    is_unknown: bool
    centrality_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InventorySummary(BaseModel):
    total_assets: int
    category_counts: Dict[str, int]
    vulnerability_counts: Dict[str, int]
    purpose_counts: Dict[str, int]
    unknown_assets_count: int
    assets: List[AssetResponse]


# Risk
class RiskAssessRequest(BaseModel):
    data_sensitivity: float = 75.0
    business_criticality: float = 80.0
    external_exposure: float = 50.0
    data_lifetime_x: float = 10.0
    migration_time_y: float = 3.0
    threat_horizon_z: float = 2035.0


class RiskResponse(BaseModel):
    id: str
    asset_id: str
    risk_score: float
    risk_level: RiskLevel
    quantum_vuln_score: float
    sensitivity_score: float
    criticality_score: float
    mosca_score: float
    exposure_score: float
    complexity_score: float
    mosca_data_lifetime_x: float
    mosca_migration_time_y: float
    mosca_quantum_horizon_z: float
    urgency_flag: bool
    explanation: Optional[str] = None
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RiskSummary(BaseModel):
    project_id: str
    overall_risk_score: float
    overall_risk_level: RiskLevel
    total_assets_assessed: int
    urgent_migration_needed_count: int
    risk_level_breakdown: Dict[str, int]


# Scenarios
class ScenarioCreate(BaseModel):
    name: str
    category: ThreatScenarioCategory = ThreatScenarioCategory.MODERATE
    quantum_horizon_year: int = 2035
    description: Optional[str] = None
    is_default: bool = False


class ScenarioResponse(ScenarioCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScenarioImpactResponse(BaseModel):
    scenario_id: str
    scenario_name: str
    quantum_horizon_year: int
    affected_assets_count: int
    critical_assets_count: int
    urgency_increase_pct: float


# Recommendations
class RecommendationResponse(BaseModel):
    id: str
    asset_id: str
    target_pqc_candidate: str
    standard_reference: str
    status: StandardStatus
    purpose: AlgPurpose
    migration_complexity: str
    performance_impact: Optional[str] = None
    compatibility_notes: Optional[str] = None
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Graph & Impact
class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    algorithm: Optional[str] = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class ImpactResponse(BaseModel):
    asset_id: str
    asset_name: str
    centrality_score: float
    affected_files: List[str]
    affected_components: List[str]
    dependent_services_count: int
    protocol_impact: Optional[str] = None
    vendor_impact: Optional[str] = None


class ImpactSimulateRequest(BaseModel):
    target_pqc_candidate: str


# Migration
class PlanCreate(BaseModel):
    title: str
    strategy: str = "HYBRID"
    target_asset_ids: Optional[List[str]] = None


class MigrationTaskResponse(BaseModel):
    id: str
    plan_id: str
    asset_name: str
    file_path: str
    from_algorithm: str
    to_algorithm: str
    status: TaskStatus
    estimated_person_hours: float
    priority: int
    patch_diff: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MigrationPlanResponse(BaseModel):
    id: str
    project_id: str
    title: str
    strategy: str
    person_effort_days: float
    calendar_duration_days: float
    total_tasks: int
    completed_tasks: int
    tasks: List[MigrationTaskResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Validation
class ValidationResponse(BaseModel):
    id: str
    plan_id: str
    overall_status: ValidationStatus
    build_passed: bool
    unit_tests_passed: bool
    crypto_tests_passed: bool
    integration_tests_passed: bool
    regression_passed: bool
    api_compatible: bool
    migration_confidence: float
    residual_risk: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ValidationLogsResponse(BaseModel):
    validation_id: str
    logs: List[str]


# CBOM & Reports
class CBOMResponse(BaseModel):
    scan_id: str
    spec_version: str = "1.6"
    cbom: Dict[str, Any]


class ReportResponse(BaseModel):
    id: str
    project_id: str
    report_type: str
    download_url: str
    created_at: datetime


# Audit
class AuditEventResponse(BaseModel):
    id: str
    project_id: Optional[str] = None
    action: str
    actor: str
    scanner_version: str
    rules_version: str
    details_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
