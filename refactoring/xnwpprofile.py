from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json
from note import Note
from person import Person
from property import Property


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
