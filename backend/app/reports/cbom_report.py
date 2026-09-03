import json


class CBOMReportGenerator:
    def format_cbom_summary(self, cbom_json: dict) -> str:
        components = cbom_json.get("components", [])
        return (
            f"CBOM AUDIT REPORT (CycloneDX v{cbom_json.get('specVersion', '1.6')})\n"
            f"Serial Number: {cbom_json.get('serialNumber')}\n"
            f"Total BOM Components: {len(components)}\n"
        )
