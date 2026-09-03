from app.knowledge.crypto_catalog import CLASSICAL_CRYPTO_CATALOG
from app.knowledge.pqc_catalog import PQC_CATALOG
from app.knowledge.standard_registry import NIST_STANDARDS
from app.knowledge.mapping_rules import MAPPING_RULES
from app.knowledge.compatibility_matrix import COMPATIBILITY_MATRIX


class KnowledgeBaseManager:
    def __init__(self):
        self.classical_catalog = CLASSICAL_CRYPTO_CATALOG
        self.pqc_catalog = PQC_CATALOG
        self.standards = NIST_STANDARDS
        self.rules = MAPPING_RULES
        self.compatibility = COMPATIBILITY_MATRIX
        self.version = "1.0.0"

    def get_version(self) -> str:
        return self.version

    def get_pqc_catalog(self) -> dict:
        return self.pqc_catalog

    def get_standards(self) -> list:
        return self.standards


knowledge_manager = KnowledgeBaseManager()
