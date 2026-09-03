import json


class CBOMExporter:
    def export_to_json_string(self, cbom_json: dict) -> str:
        return json.dumps(cbom_json, indent=2)
