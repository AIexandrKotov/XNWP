from random import *


# Генераторы генерируют случайные значения
class Generator:
    def __init__(self):
        self.Rnd = Random()
        pass

    @staticmethod
    def get_generators():
        return {
            "d": DigitGenerator(),
            "rc": RandomChooseGenerator(),
            "cc": ChanceChooseGenerator(),
        }

    def next(self, **kwargs):
        return None


class RussianNameGenerator(Generator):
    # сделать это когда-нибудь
    def next(self, **kwargs):
        return "Next name"


class DigitGenerator(Generator):
    def next(self, lower: int, upper: int):
        return self.Rnd.randint(lower, upper)


class RandomChooseGenerator(Generator):
    def next(self, chooses: list):
        return chooses[self.Rnd.randint(0, len(chooses))]


class ChanceChooseGenerator(Generator):
    @staticmethod
    def optimize(cached_items):
        overall = sum(i for i, j in cached_items)
        return [(i / overall, j) for i, j in cached_items]

    def next(self, chance_chooses: list[tuple[float, object]]):
        f = self.Rnd.random()
        items = self.optimize(chance_chooses)
        if len(items) == 0:
            return "ChanceChooses not specified"
        sum = 0.0
        for chance, o in items:
            sum += chance
            if sum >= f:
                return o
        return items[len(items) - 1][1]
