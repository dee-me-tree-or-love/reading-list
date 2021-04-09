from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class DataInputEvent:
    data: Dict[str, Any] = field(default_factory=dict)
