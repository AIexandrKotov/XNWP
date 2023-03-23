from __future__ import annotations

# import dataclasses
# import json
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Database:
    files: list[Datalist] = field(default_factory=list)


@dataclass_json
@dataclass
class Datalist:
    filename: str
    datasets: list[Dataset] = field(default_factory=list)


@dataclass_json
@dataclass
class Dataset:
    name: str
    description: str
    content: list[str] = field(default_factory=list)


default_dbfiles: Database
user_dbfiles: Database


def get_content_by_name_at(db_name: str, db: Database) -> list[str]:
    for file in db.files:
        for data in file.datasets:
            if data.name == db_name:
                return data.content
    return []


def get_content_by_name(db_name: str) -> list[str]:
    global default_dbfiles
    global user_dbfiles

    default = get_content_by_name_at(db_name, default_dbfiles)
    user = get_content_by_name_at(db_name, user_dbfiles)
    if len(user) != 0:
        return user
    elif len(default) != 0:
        return default
    else:
        return ["Data not found"]
