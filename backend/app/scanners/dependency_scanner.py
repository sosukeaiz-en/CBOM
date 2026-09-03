import os
import json
from typing import List
from app.scanners.base import BaseScanner
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class DependencyScanner(BaseScanner):
    def __init__(self):
        super().__init__(scanner_name="DependencyScanner", version="1.0.0")

    def scan(self, target_input: str) -> List[RawFinding]:
        findings = []
        if not os.path.exists(target_input):
            return findings

        # Scan requirements.txt
        req_path = os.path.join(target_input, "requirements.txt") if os.path.isdir(target_input) else (target_input if "requirements.txt" in target_input else None)
        if req_path and os.path.exists(req_path):
            with open(req_path, "r", encoding="utf-8", errors="ignore") as f:
                for idx, line in enumerate(f, 1):
                    line_str = line.strip()
                    if any(pkg in line_str.lower() for pkg in ["cryptography", "pycryptodome", "paramiko", "pynacl", "pyopenssl"]):
                        findings.append(RawFinding(
                            detector="DependencyScanner-Pip",
                            input_source="Requirements.txt",
                            file_resource=req_path,
                            line_number=idx,
                            finding_type="DependencyPackage",
                            matched_construct=line_str,
                            context=line_str,
                            confidence=0.95,
                            evidence_type=EvidenceType.OBSERVED,
                            algorithm="DEPENDENCY_CRYPTO_LIBRARY",
                            purpose=AlgPurpose.AUTHENTICATION
                        ))

        # Scan package.json
        pkg_path = os.path.join(target_input, "package.json") if os.path.isdir(target_input) else (target_input if "package.json" in target_input else None)
        if pkg_path and os.path.exists(pkg_path):
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    for dep_name, version in deps.items():
                        if any(crypto_dep in dep_name.lower() for crypto_dep in ["crypto", "jose", "jsonwebtoken", "node-forge", "bcrypt", "webcrypto"]):
                            findings.append(RawFinding(
                                detector="DependencyScanner-Npm",
                                input_source="Package.json",
                                file_resource=pkg_path,
                                line_number=None,
                                finding_type="NpmDependency",
                                matched_construct=f"{dep_name}: {version}",
                                context=f"NPM package {dep_name} version {version}",
                                confidence=0.95,
                                evidence_type=EvidenceType.OBSERVED,
                                algorithm="NPM_CRYPTO_PACKAGE",
                                purpose=AlgPurpose.AUTHENTICATION
                            ))
            except Exception:
                pass

        return findings
