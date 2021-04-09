from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class DataInput:
    data: Dict = field(default_factory=dict)
