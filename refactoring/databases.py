from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Database:
    """Представляет сериализуемый набор файлов как базу данных"""

    files: list[Datalist] = field(default_factory=list)
    """Список файлов"""

    def save(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        for file in self.files:
            with open(os.path.join(directory, file.filename), "w+") as write_file:
                json.dump(
                    dataclasses.asdict(file),
                    write_file,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )

    @staticmethod
    def get_files(path: str) -> list[str]:
        from os import listdir
        from os.path import isfile, join

        return [f for f in listdir(path) if isfile(join(path, f))]

    @staticmethod
    def load(path: str) -> Database:
        files: list[Datalist] = []
        if not os.path.exists(path):
            return Database(files)
        for file in Database.get_files(path):
            with open(os.path.join(path, file), "r") as read_file:
                files.append(Datalist.from_json(read_file.read()))  # type: ignore
        return Database(files)


@dataclass_json
@dataclass
class Datalist:
    """Представляет файл, содержащий множество именованных наборов данных"""

    filename: str
    """Имя файла"""
    datasets: list[Dataset] = field(default_factory=list)
    """Наборы данных"""


@dataclass_json
@dataclass
class Dataset:
    """Представляет набор данных, предоставляемых для генераторов"""

    name: str
    """Внутреннее имя набора данных"""
    description: str
    """Текстовое описание набора данных"""
    content: list[str] = field(default_factory=list)
    """Содержимое набора данных"""


default_dbfiles: Database
user_dbfiles: Database


def create() -> None:
    global default_dbfiles
    global user_dbfiles
    default_dbfiles = Database(
        [
            Datalist(
                "names.json",
                [
                    Dataset(
                        name="rus_male_names",
                        description="Русские имена (мужские)",
                        content=["Александр", "Алексей", "Артём", "Андрей", "Борис"],
                    )
                ],
            )
        ]
    )
    user_dbfiles = Database([])


def save() -> None:
    from kivy import platform

    if platform == "android":
        pass
    elif platform == "win":
        default_dbfiles.save(os.path.join("bin", "defaultdb"))
        user_dbfiles.save(os.path.join("bin", "userdb"))


def load() -> None:
    from kivy import platform

    if platform == "android":
        from android.storage import primary_external_storage_path

        # эту часть кода получится написать только на линуксе. увы
    elif platform == "win":
        global default_dbfiles
        global user_dbfiles
        default_dbfiles = Database.load(os.path.join("bin", "defaultdb"))
        user_dbfiles = Database.load(os.path.join("bin", "userdb"))


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


def add_list_in_default(
    filename: str, name: str, description: str, content: list[str]
) -> None:
    for file in default_dbfiles.files:
        if file == filename:
            exist: Dataset | None = next(
                (ds for ds in file.datasets if ds.name == name), None
            )
            if exist is not None:
                file.datasets.remove(exist)
            file.datasets.append(Dataset(name, description, content))
