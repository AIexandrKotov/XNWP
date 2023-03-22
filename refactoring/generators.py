from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Any

import databases
from logic import Property
from raname import Raname


@dataclass
class AbstractGenerator:
    random: Random = field(default_factory=Random, init=False)

    def get_next(self, /, *args: tuple, **kwargs: dict[str, Any]) -> Any:
        raise NotImplementedError()

    def get_default(self) -> dict[str, Any]:
        raise NotImplementedError()

    def get_help(self) -> str:
        return "AbstractGenerator has not a specification"

    def __str__(self) -> str:
        return type(self).__name__

    def allow_arguments(self, d: dict[str, Any]) -> bool:
        for k, v in self.get_default().items():
            if k not in d or not isinstance(d[k], type(v)):
                return False
        return True

    def include_in_property(self, p: Property) -> None:
        p.generator = type(self).__name__
        p.generator_arguments = self.get_default()

    def to_default_property(
        self, name: str = "", value: Any = "", icon: str = ""
    ) -> Property:
        return Property(name, str(self), icon, value, self.get_default())


@dataclass
class DigitGenerator(AbstractGenerator):
    def get_next(  # type: ignore
        self,
        /,
        *args: tuple,
        lower: int,
        upper: int,
        **kwargs: dict[str, Any],
    ) -> int:
        return self.random.randrange(lower, upper)

    def get_default(self) -> dict[str, Any]:
        return {"lower": 0, "upper": 100}

    def get_help(self) -> str:
        return """
            DigitGenerator(lower: int, upper: int) -> int
            '''Returns random digit in range [lower, upper)'''
        """


@dataclass
class ChooseGenerator(AbstractGenerator):
    def get_next(  # type: ignore
        self, /, *args: tuple, chooses: list[Any], **kwargs: dict[str, Any]
    ) -> Any:
        return self.random.choice(chooses)

    def get_default(self) -> dict[str, Any]:
        return {"chooses": ["A", "B", "C"]}

    def get_help(self) -> str:
        return """
            ChooseGenerator(chooses: list[Any]) -> Any
            '''Returns random element from non-empty list'''
        """


@dataclass
class DBChooseGenerator(AbstractGenerator):
    def get_next(  # type: ignore
        self, /, *args: tuple, db_name: str, **kwargs: dict[str, Any]
    ) -> Any:
        return self.random.choice(databases.get_by_name(db_name))

    def get_default(self) -> dict[str, Any]:
        return {"db_name": "default"}

    def get_help(self) -> str:
        return """
            DBChooseGenerator(db_name: str) -> str
            '''Returns random str from data base'''
        """


@dataclass
class RanameGenerator(AbstractGenerator, Raname):
    def get_next(  # type: ignore
        self,
        /,
        *args: tuple,
        chooses: list[str],
        min_depth: int,
        max_depth: int,
        push_depth: bool,
        only_center: bool,
        **kwargs: dict[str, Any],
    ) -> str:
        return self.level_i(
            chooses, self.random.randint(min_depth, max_depth), push_depth, only_center
        )

    def get_default(self) -> dict[str, Any]:
        return {
            "chooses": ["left", "center", "right"],
            "min_depth": 1,
            "max_depth": 5,
            "push_depth": False,
            "only_center": True,
        }

    def get_help(self) -> str:
        return """
            RanameGenerator(
                chooses: list[str],
                min_depth: int,
                max_depth: int,
                push_depth: bool,
                only_center: bool
            ) -> str
            '''Returns random generated string based on depth strings from list'''
        """


@dataclass
class RanameDatabaseGenerator(AbstractGenerator, Raname):
    def get_next(  # type: ignore
        self,
        /,
        *args: tuple,
        db_name: str,
        min_depth: int,
        max_depth: int,
        push_depth: bool,
        only_center: bool,
        **kwargs: dict[str, Any],
    ) -> str:
        return self.level_i(
            databases.get_by_name(db_name),
            self.random.randint(min_depth, max_depth),
            push_depth,
            only_center,
        )

    def get_default(self) -> dict[str, Any]:
        return {
            "db_name": "default",
            "min_depth": 1,
            "max_depth": 5,
            "push_depth": False,
            "only_center": True,
        }

    def get_help(self) -> str:
        return """
            RanameDatabaseGenerator(
                db_name: str,
                min_depth: int,
                max_depth: int,
                push_depth: bool,
                only_center: bool
            ) -> str
            '''Returns random generated string based on depth strings from database'''
        """


class Generators:
    digit_generator: AbstractGenerator = DigitGenerator()
    choose_generator: AbstractGenerator = ChooseGenerator()
    db_choose_generator: AbstractGenerator = DBChooseGenerator()
    raname_generator: AbstractGenerator = RanameGenerator()
    db_raname_generator: AbstractGenerator = RanameDatabaseGenerator()

    # !! include all generators in list:
    __generators: list[AbstractGenerator] = [
        digit_generator,
        choose_generator,
        raname_generator,
        db_choose_generator,
        db_raname_generator,
    ]

    @staticmethod
    def __mapper(generator: AbstractGenerator) -> tuple[str, AbstractGenerator]:
        return (str(generator), generator)

    __named_generators: dict[str, AbstractGenerator] = dict(map(__mapper, __generators))

    @staticmethod
    def generator_exists(generator_name: str) -> bool:
        """Return True if that generator exists"""
        return generator_name in Generators.__named_generators.keys()

    @staticmethod
    def get_generator_from_name(generator_name: str) -> AbstractGenerator:
        """Return generator by generator_name"""
        if Generators.generator_exists(generator_name):
            return Generators.__named_generators[generator_name]
        raise ValueError(f'Generator "{generator_name}" not exists')

    @staticmethod
    def allow_arguments_for_name(generator_name: str, args: dict[str, Any]) -> bool:
        """Return True if args is correct for this generator"""
        if Generators.generator_exists(generator_name):
            return Generators.get_generator_from_name(generator_name).allow_arguments(
                args
            )
        raise ValueError(f'Generator "{generator_name}" not exists')

    @staticmethod
    def get_value_direct(generator_name: str, args: dict[str, Any]) -> Any:
        return Generators.__named_generators[generator_name].get_next(**args)

    @staticmethod
    def get_value(p: Property) -> Any:
        return Generators.__named_generators[p.generator].get_next(
            **p.generator_arguments
        )

    @staticmethod
    def generate(p: Property) -> None:
        p.value = Generators.get_value(p)
