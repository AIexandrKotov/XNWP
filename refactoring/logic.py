from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel


class Note(BaseModel):
    text: str


class Property(BaseModel):
    name: str
    generator: str
    icon: str
    value: str
    generator_arguments: dict[str, Any]

    @property
    def str_arguments(self) -> str:
        return json.dumps(self.generator_arguments, ensure_ascii=False, indent=4)

    @str_arguments.setter
    def str_arguments(self, s: str) -> None:
        self.generator_arguments: dict[str, Any] = json.loads(s)


class Person(BaseModel):
    properties: list[tuple[str, list[Property]]]

    def __post_init__(self) -> None:
        self.properties = [] if self.properties is None else self.properties


class XNWPProfile(BaseModel):
    notes: list[tuple[str, list[Note]]]
    persons: list[tuple[str, list[Person]]]
    sample_properties: list[tuple[str, list[Property]]]
    sample_persons: list[tuple[str, list[Person]]]

    def saves(self) -> str:
        return json.dumps(
            self.dict(),
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
        )

    def savefile(self, path: str) -> None:
        with open(path, "w") as wf:
            json.dump(
                self.dict(),
                wf,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    @staticmethod
    def loads(s: str) -> XNWPProfile:
        return XNWPProfile.parse_obj(json.loads(s))  # type: ignore

    @staticmethod
    def loadfile(path: str) -> XNWPProfile:
        with open(path, "r") as rf:
            return XNWPProfile.parse_obj(json.load(rf))  # type: ignore
