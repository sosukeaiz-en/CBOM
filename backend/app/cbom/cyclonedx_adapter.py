import uuid
from datetime import datetime, timezone
from typing import List
from app.models.db_models import CryptoAsset, Scan


class CycloneDXCBOMAdapter:
    def to_cyclonedx_json(self, scan: Scan, assets: List[CryptoAsset]) -> dict:
        bom_components = []
        for asset in assets:
            comp = {
                "type": "cryptographic-asset",
                "bom-ref": f"crypto-asset-{asset.id}",
                "name": asset.name,
                "version": "1.0",
                "cryptoProperties": {
                    "assetType": "algorithm" if asset.category.value == "SOURCE_CODE" else "certificate",
                    "algorithmProperties": {
                        "primitive": asset.purpose.value if asset.purpose else "unknown",
                        "parameterSetIdentifier": str(asset.key_length) if asset.key_length else "N/A",
                        "executionEnvironment": "software-plain",
                        "implementationPlatform": "portable-c-python",
                        "certificationLevel": ["none"],
                        "cryptoFunctions": [asset.purpose.value] if asset.purpose else ["unknown"]
                    },
                    "oid": "1.3.6.1.4.1.NIST"
                },
                "evidence": {
                    "occurrences": [
                        {
                            "location": asset.location_file,
                            "line": asset.location_line or 1
                        }
                    ]
                }
            }
            bom_components.append(comp)

        cbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "serialNumber": f"urn:uuid:{scan.id}",
            "version": 1,
            "metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "tools": [
                    {
                        "vendor": "ECDAT",
                        "name": "Enterprise Cryptographic Discovery Tool",
                        "version": scan.scanner_version
                    }
                ],
                "component": {
                    "type": "application",
                    "name": f"Project-{scan.project_id}",
                    "bom-ref": f"project-{scan.project_id}"
                }
            },
            "components": bom_components
        }

        return cbom
