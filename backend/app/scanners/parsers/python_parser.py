import ast
from typing import List
from app.models.schemas import RawFinding
from app.models.enums import EvidenceType, AlgPurpose


class PythonASTParser:
    def parse_code(self, file_path: str, code: str) -> List[RawFinding]:
        findings = []
        try:
            tree = ast.parse(code, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if any(lib in alias.name for lib in ["cryptography", "Crypto", "ssl", "hashlib"]):
                            findings.append(RawFinding(
                                detector="PythonASTParser",
                                input_source="SourceCodeScanner",
                                file_resource=file_path,
                                line_number=node.lineno,
                                finding_type="ImportStatement",
                                matched_construct=f"import {alias.name}",
                                context=f"Line {node.lineno}: import {alias.name}",
                                confidence=0.95,
                                evidence_type=EvidenceType.OBSERVED,
                                algorithm="CRYPTO_IMPORT",
                                purpose=AlgPurpose.AUTHENTICATION
                            ))
                elif isinstance(node, ast.ImportFrom):
                    if node.module and any(lib in node.module for lib in ["cryptography", "Crypto", "ssl", "hashlib"]):
                        findings.append(RawFinding(
                            detector="PythonASTParser",
                            input_source="SourceCodeScanner",
                            file_resource=file_path,
                            line_number=node.lineno,
                            finding_type="ImportFromStatement",
                            matched_construct=f"from {node.module} import ...",
                            context=f"Line {node.lineno}: from {node.module}",
                            confidence=0.95,
                            evidence_type=EvidenceType.OBSERVED,
                            algorithm="CRYPTO_IMPORT",
                            purpose=AlgPurpose.AUTHENTICATION
                        ))
        except SyntaxError:
            pass  # Non-python code or syntax error silently handled
        return findings
