from typing import List
from app.models.schemas import RawFinding


def deduplicate_findings(findings: List[RawFinding]) -> List[RawFinding]:
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f.file_resource, f.line_number, f.algorithm, f.matched_construct)
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)
    return unique_findings
