from abc import ABC, abstractmethod
from typing import List, Any
from app.models.schemas import RawFinding


class BaseScanner(ABC):
    def __init__(self, scanner_name: str, version: str = "1.0.0"):
        self.scanner_name = scanner_name
        self.version = version

    @abstractmethod
    def scan(self, target_input: Any) -> List[RawFinding]:
        """Contract: Must return a list of RawFinding objects."""
        pass
