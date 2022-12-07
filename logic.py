import json
from generators import *


class Environment:
    default_generators = Generator.get_generators()
    default_profile = None  # из этой штуки можно будет всегда восстановить шаблоны по умолчанию

    def __init__(self):
        pass


class Profile:
    def __init__(self):
        self.persons = []
        self.notes = []
        self.sample_properties = []
        self.sample_persons = []

    def encode(self):
        return {"persons": list(map(Person.encode, self.persons)),
                "notes": list(map(Person.encode, self.notes)),
                "sample_properties": list(map(Property.encode, self.sample_properties)),
                "sample_persons": list(map(Person.encode, self.sample_persons)),
                "__profile__": True}

    @staticmethod
    def decode(dct):
        if "__profile__" in dct:
            e = Profile()
            e.persons = list(map(Person.decode, dct["persons"]))
            e.notes = list(map(Note.decode, dct["notes"]))
            return e
        return dct

    def save(self):
        return json.dumps(self, default=Profile.encode)

    def savefile(self, path):
        with open(path, 'w') as wf:
            json.dump(self, wf, default=Profile.encode)

    @staticmethod
    def load(s):
        return json.loads(s, object_hook=Profile.decode)

    @staticmethod
    def loadfile(path):
        with open(path, 'r') as rf:
            data = json.load(rf, object_hook=Profile.decode)
        return data


class Note:
    def __init__(self):
        self.text = ""
        self.tags = []

    def encode(self):
        return {"text": self.text,
                "tags": self.tags,
                "__note__": True}

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
        self.properties = []
        self.tags = []
        pass

    def add_property(self, p):
        self.properties.append(p)
        return self

    def add_tag(self, tag):
        self.tags.append(tag)
        return self

    def clone(self):
        p = Person()
        p.properties = self.properties.copy()
        p.tags = self.tags.copy()

    def encode(self):
        return {"properties": list(map(Property.encode, self.properties)),
                "tags": self.tags,
                "__person__": True}

    @staticmethod
    def decode(dct):
        if "__person__" in dct:
            p = Person()
            p.properties = list(map(Property.decode, dct["properties"]))
            p.tags = dct["tags"]
            return p
        return dct

    pass


class Property:
    def __init__(self):
        self.name = ""
        self.value = 0
        self.generator = ""
        self.genargs = {}
        self.flags = []

    def clone(self):
        p = Property()
        p.name = self.name
        p.value = self.value
        p.generator = self.generator
        p.genargs = self.genargs.copy()
        p.flags = self.flags.copy()

    def has_generator(self):
        return self.generator != ""

    def generate(self):
        return Environment.default_generators[self.generator].next(self.genargs)

    def encode(self):
        return {"name": self.name,
                "value": self.value,
                "genargs": self.genargs,
                "generator": self.generator,
                "flags": self.flags,
                "__property__": True}

    @staticmethod
    def decode(dct):
        if "__property__" in dct:
            p = Property()
            p.name = dct["name"]
            p.value = dct["value"]
            p.genargs = dct["genargs"]
            p.generator = dct["generator"]
            p.flags = dct["flags"]
            return p
        return dct

    pass
