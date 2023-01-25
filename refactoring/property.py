from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Property:
    name: str
    generator: str
    icon: str
    value: Any = field(default_factory=str)
    generator_arguments: dict[str, Any] = field(default_factory=dict)
