from __future__ import annotations

import json
import os

from logic import XNWPProfile
from pydantic import BaseModel


class Dataset(BaseModel):
    """Представляет набор данных, предоставляемых для генераторов"""

    name: str
    """Внутреннее имя набора данных"""
    description: str
    """Текстовое описание набора данных"""
    content: list[str]
    """Содержимое набора данных"""


class Datalist(BaseModel):
    """Представляет файл, содержащий множество именованных наборов данных"""

    filename: str
    """Имя файла"""
    name: str
    """Имя списка данных"""
    description: str
    """Описание списка данных"""
    datasets: list[Dataset]
    """Наборы данных"""


class Database(BaseModel):
    """Представляет сериализуемый набор файлов как базу данных"""

    files: list[Datalist]
    """Список файлов"""

    def save(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        for file in self.files:
            with open(
                os.path.join(directory, file.filename), "w+", encoding="utf_8"
            ) as write_file:
                json.dump(
                    file.dict(),
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
            return Database(files=files)
        for file in Database.get_files(path):
            with open(os.path.join(path, file), "r", encoding="utf_8") as read_file:
                files.append(Datalist.parse_obj(json.load(read_file)))
        return Database(files=files)


default_dbfiles: Database
user_dbfiles: Database
user_profiles: dict[str, XNWPProfile]
last_profile: str


def create() -> None:
    global default_dbfiles
    global user_dbfiles
    default_dbfiles = Database(
        files=[
            Datalist(
                filename="names.json",
                name="Имена",
                description="Содержит наборы данных с именами",
                datasets=[
                    Dataset(
                        name="rus_male_names",
                        description="Русские имена (мужские)",
                        content=["Александр", "Алексей", "Артём", "Андрей", "Борис"],
                    )
                ],
            )
        ]
    )
    user_dbfiles = Database(files=[])


def get_all_datalists() -> list[Datalist]:
    """Скомпоновывает базы данных по умолчанию и пользовательские
    в единый комплекс данных.
    """
    global default_dbfiles
    global user_dbfiles
    ret: list[Datalist] = []
    ret.extend(default_dbfiles.files)
    ret.extend(user_dbfiles.files)
    return ret


def save() -> None:
    from kivy import platform

    if platform == "android":
        pass
    elif platform == "win":
        default_dbfiles.save(os.path.join("bin", "defaultdb"))
        user_dbfiles.save(os.path.join("bin", "userdb"))


def load_profiles(path: str) -> dict[str, XNWPProfile]:
    dct: dict[str, XNWPProfile] = {}
    for file in Database.get_files(path):
        dct[os.path.basename(file)] = XNWPProfile.loadfile(file)
    return dct


def load() -> None:
    from kivy import platform

    global default_dbfiles
    global user_dbfiles
    global user_profiles

    if platform == "android":
        user_dbfiles = Database(files=[])
        default_dbfiles = Database.load(os.path.join("bin", "defaultdb"))
        if os.path.exists(os.path.join("bin", "profiles")):
            user_profiles = load_profiles(os.path.join("bin", "profiles"))
        else:
            user_profiles = {
                "last.json": XNWPProfile(
                    notes=[], persons=[], sample_persons=[], sample_properties=[]
                )
            }
        # from android.storage import primary_external_storage_path

        # эту часть кода получится написать только на линуксе. увы
    elif platform == "win" or platform == "linux":
        default_dbfiles = Database.load(os.path.join("bin", "defaultdb"))
        user_dbfiles = Database.load(os.path.join("bin", "userdb"))
        if os.path.exists(os.path.join("bin", "profiles")):
            user_profiles = load_profiles(os.path.join("bin", "profiles"))
        else:
            user_profiles = {
                "last.json": XNWPProfile(
                    notes=[], persons=[], sample_persons=[], sample_properties=[]
                )
            }


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
            file.datasets.append(
                Dataset(name=name, description=description, content=content)
            )
