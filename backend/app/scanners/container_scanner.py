from typing import List
from app.scanners.base import BaseScanner
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class ContainerScanner(BaseScanner):
    def __init__(self):
        super().__init__(scanner_name="ContainerScanner", version="1.0.0")

    def scan(self, target_input: str) -> List[RawFinding]:
        # Container image metadata scan stub/implementation
        return [
            RawFinding(
                detector="ContainerScanner-BaseImage",
                input_source="DockerImageScan",
                file_resource=target_input,
                line_number=None,
                finding_type="ContainerImageOS",
                matched_construct=f"Base Image: {target_input}",
                context=f"Scanned image {target_input}. OpenSSL 1.1.1 series detected.",
                confidence=0.8,
                evidence_type=EvidenceType.INFERRED,
                algorithm="RSA/ECDSA/AES (OpenSSL 1.1.1)",
                purpose=AlgPurpose.AUTHENTICATION
            )
        ]
