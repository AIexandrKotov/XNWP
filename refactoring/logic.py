from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class XNWPProfile:
    notes: list[tuple[str, list[Note]]] = field(default_factory=list)
    persons: list[tuple[str, list[Person]]] = field(default_factory=list)
    sample_properties: list[tuple[str, list[Property]]] = field(default_factory=list)
    sample_persons: list[tuple[str, list[Person]]] = field(default_factory=list)

    def saves(self) -> str:
        return json.dumps(
            dataclasses.asdict(self),
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
        )

    def savefile(self, path: str) -> None:
        with open(path, "w") as wf:
            json.dump(
                dataclasses.asdict(self),
                wf,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    @staticmethod
    def loads(s: str) -> XNWPProfile:
        return XNWPProfile.from_json(s)  # type: ignore

    @staticmethod
    def loadfile(path: str) -> XNWPProfile:
        with open(path, "r") as rf:
            return XNWPProfile.from_json(rf.read())  # type: ignore


@dataclass_json
@dataclass
class Note:
    text: str


@dataclass_json
@dataclass
class Person:
    properties: list[tuple[str, list[Property]]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.properties = [] if self.properties is None else self.properties


@dataclass_json
@dataclass
class Property:
    name: str
    generator: str
    icon: str
    value: Any = field(default_factory=str)
    generator_arguments: dict[str, Any] = field(default_factory=dict)

    @property
    def str_arguments(self) -> str:
        return json.dumps(self.generator_arguments, ensure_ascii=False, indent=4)

    @str_arguments.setter
    def str_arguments(self, s: str) -> None:
        self.generator_arguments: dict[str, Any] = json.loads(s)
