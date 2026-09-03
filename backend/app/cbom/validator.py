class CBOMValidator:
    def validate(self, cbom_json: dict) -> tuple[bool, str]:
        if not isinstance(cbom_json, dict):
            return False, "CBOM root must be a JSON object"
        if cbom_json.get("bomFormat") != "CycloneDX":
            return False, "bomFormat must be 'CycloneDX'"
        if cbom_json.get("specVersion") not in ["1.5", "1.6"]:
            return False, "specVersion must be '1.5' or '1.6'"
        if "components" not in cbom_json:
            return False, "CBOM must contain 'components' array"
        return True, "CBOM is valid CycloneDX format"
