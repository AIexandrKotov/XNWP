from random import *


# Генераторы генерируют случайные значения
class Generator:
    def __init__(self):
        self.Rnd = Random()
        pass

    @staticmethod
    def get_generators():
        return {
            "NameGenerator": RussianNameGenerator(),
            "DigitGenerator": DigitGenerator()
        }

    def next(self, **kwargs):
        pass


class RussianNameGenerator(Generator):
    def next(self, **kwargs):
        return "Next name"


class DigitGenerator(Generator):
    def next(self, **kwargs):
        self.Rnd.randint(kwargs["lower"], kwargs["upper"])


class RandomChooseGenerator(Generator):
    def next(self, **kwargs):
        if "chooses" in kwargs:
            return kwargs["chooses"][self.Rnd.randint(0, len(kwargs["chooses"]))]

class ChanceChooseGenerator(Generator):
    def optimize(self, cacheditems):
        overall = sum(map(lambda x: x[1], cacheditems))
        return list(map(lambda x: (x[0], x[1] / overall), cacheditems))

    def next(self, **kwargs):
        f = self.Rnd.random()
        curl = 0.0
        curr = 0.0
        items = self.optimize(kwargs["chancechooses"])
        for x in items:
            curr += x[1]
            if curl <= f <= curr:
                return x[0]
            curr += x[1]
        return items[len(items)-1]


