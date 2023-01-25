from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import dataclass_json
from property import Property


@dataclass_json
@dataclass
class Person:
    properties: list[tuple[str, list[Property]]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.properties = [] if self.properties is None else self.properties
