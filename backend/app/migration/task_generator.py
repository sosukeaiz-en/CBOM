from typing import List
from app.models.db_models import CryptoAsset
from app.migration.patch_generator import PatchGenerator


class TaskGenerator:
    def __init__(self):
        self.patch_gen = PatchGenerator()

    def generate_tasks_for_assets(self, assets: List[CryptoAsset], plan_id: str) -> List[dict]:
        tasks = []
        for idx, asset in enumerate(assets, start=1):
            target_pqc = "ML-DSA-65" if "RSA" in asset.algorithm or "ECDSA" in asset.algorithm else ("ML-KEM-768" if "ECDH" in asset.algorithm else "AES-256")
            patch = self.patch_gen.generate_patch(asset.location_file, asset.algorithm, target_pqc)

            tasks.append({
                "plan_id": plan_id,
                "asset_name": asset.name,
                "file_path": asset.location_file,
                "from_algorithm": asset.algorithm,
                "to_algorithm": target_pqc,
                "estimated_person_hours": 8.0 * (1 + asset.centrality_score),
                "priority": idx,
                "patch_diff": patch
            })
        return tasks
