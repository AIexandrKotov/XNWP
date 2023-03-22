import os
import json
import copy
from typing import Optional
from old_generators import *


class Profile:
    def __init__(self):
        self.persons: list[Person] = []
        self.notes: list[Note] = []
        self.sample_properties: list[Property] = []
        self.sample_persons: list[Person] = []

    def encode(self):
        return {
            "persons": list(map(Person.encode, self.persons)),
            "notes": list(map(Note.encode, self.notes)),
            "sample_properties": list(map(Property.encode, self.sample_properties)),
            "sample_persons": list(map(Person.encode, self.sample_persons)),
            "__profile__": True,
        }

    @staticmethod
    def decode(dct):
        if "__profile__" in dct:
            e = Profile()
            e.persons = list(map(Person.decode, dct["persons"]))
            e.notes = list(map(Note.decode, dct["notes"]))
            e.sample_properties = list(map(Property.decode, dct["sample_properties"]))
            e.sample_persons = list(map(Person.decode, dct["sample_persons"]))
            return e
        return dct

    def save(self):
        return json.dumps(self, default=Profile.encode, sort_keys=True, indent=4)

    def savefile(self, path):
        with open(path, "w") as wf:
            json.dump(self, wf, default=Profile.encode, sort_keys=True, indent=4)

    @staticmethod
    def load(s):
        return json.loads(s, object_hook=Profile.decode)

    @staticmethod
    def loadfile(path):
        with open(path, "r") as rf:
            data = json.load(rf, object_hook=Profile.decode)
        return data



class Note:
    def __init__(self):
        self.text: str = ""
        self.tags: list[str] = []

    def encode(self):
        return {"text": self.text, "tags": self.tags, "__note__": True}

    @staticmethod
    def decode(dct):
        if "__note__" in dct:
            n = Note()
            n.text = dct["text"]
            n.tags = dct["tags"]
            return n
        return dct


class Person:
    def __init__(self):
        self.properties: list[Property] = []
        self.tags: list[str] = []
        pass

    def add_property(self, p):
        self.properties.append(p)
        return self

    def add_tag(self, tag):
        self.tags.append(tag)
        return self

    def encode(self):
        return {
            "properties": list(map(Property.encode, self.properties)),
            "tags": self.tags,
            "__person__": True,
        }

    @staticmethod
    def decode(dct):
        if "__person__" in dct:
            p = Person()
            p.properties = list(map(Property.decode, dct["properties"]))
            p.tags = dct["tags"]
            return p
        return dct

    pass


class Environment:
    # Пока использовать только default_profile
    def __init__(self):
        self.default_generators: dict[str, Generator] = Generator.get_generators()
        self.default_profile : Profile = Profile.loadfile(os.path.join("bin", "default.json"))
        self.current_profile: Optional[Profile] = None

    def load(self):
        self.current_profile: Profile = copy.deepcopy(self.default_profile)
        return self

    def save(self):
        self.current_profile.savefile(os.path.join("bin", "default.json"))
        return self


class Property:
    def __init__(self):
        self.name: str = ""
        self.value: object = 0
        self.generator: str = ""
        self.genargs: dict = {}

    def __str__(self):
        return f'{self.name}, {self.value}, {self.generator}, {", ".join(f"{k} = {v}" for k, v in self.genargs.items())}'

    def has_generator(self):
        return self.generator != ""

    def generate(self, e: Environment):
        self.value = e.default_generators[self.generator].next(**self.genargs)
        return self.value
    
    def agenerate(self, e: Environment, generator: str, args: dict) -> object:
        return e.default_generators[generator].next(**args)

    @property
    def js_gargs(self):
        return json.dumps(self.genargs, ensure_ascii=False)
    
    @js_gargs.setter
    def js_gargs(self, s: str):
        self.genargs = json.loads(s)

    def encode(self):
        return {
            "name": self.name,
            "value": self.value,
            "genargs": self.genargs,
            "generator": self.generator,
            "__property__": True,
        }

    @staticmethod
    def decode(dct):
        if "__property__" in dct:
            p = Property()
            p.name = dct["name"]
            p.value = dct["value"]
            p.genargs = dct["genargs"]
            p.generator = dct["generator"]
            return p
        return dct

    pass