import json
import re
from typing import Dict, Any, Optional


def parse_json_safely(content: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(content)
    except Exception:
        return None


def extract_regex_matches(pattern: str, text: str, flags=re.IGNORECASE) -> list[re.Match]:
    return list(re.finditer(pattern, text, flags=flags))
