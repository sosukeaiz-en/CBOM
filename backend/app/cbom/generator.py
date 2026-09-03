from typing import List
from app.models.db_models import Scan, CryptoAsset
from app.cbom.cyclonedx_adapter import CycloneDXCBOMAdapter
from app.cbom.validator import CBOMValidator


class CBOMGenerator:
    def __init__(self):
        self.adapter = CycloneDXCBOMAdapter()
        self.validator = CBOMValidator()

    def generate(self, scan: Scan, assets: List[CryptoAsset]) -> dict:
        cbom_json = self.adapter.to_cyclonedx_json(scan, assets)
        is_valid, msg = self.validator.validate(cbom_json)
        if not is_valid:
            raise ValueError(f"Generated CBOM is invalid: {msg}")
        return cbom_json
