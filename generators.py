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
            "date": DateGenerator(),
        }
    
    @staticmethod
    def get_generators_help():
        return '''Реализованные генераторы:
        d - Числовой генератор, аргументы l, u: int
        rc - Генератор случайного выбора, аргумент c: list
        cc - Генератор шансового выбора, аргумент c_c: list[tuple[float, object]]
        date - генератор даты, необяз. аргумент year: tuple[int, int]
        '''

    def next(self, **kwargs):
        return None


class RussianNameGenerator(Generator):
    # сделать это когда-нибудь
    def next(self, **kwargs):
        return "Next name"


class DateGenerator(Generator):
    def next(self, year=None):
        if year == None:
            return f'{str(self.Rnd.randint(1, 31)).zfill(2)}.{str(self.Rnd.randint(1, 12)).zfill(2)}'
        else:
            return f'{str(self.Rnd.randint(1, 31)).zfill(2)}.{str(self.Rnd.randint(1, 12)).zfill(2)}.{str(self.Rnd.randint(year[0], year[1]))}'


class DigitGenerator(Generator):
    def next(self, l: int, u: int):
        return self.Rnd.randint(l, u)


class RandomChooseGenerator(Generator):
    def next(self, c: list):
        return c[self.Rnd.randint(0, len(c) - 1)]


class ChanceChooseGenerator(Generator):
    @staticmethod
    def optimize(cached_items):
        overall = sum(i for i, j in cached_items)
        return [(i / overall, j) for i, j in cached_items]

    def next(self, c_c: list[tuple[float, object]]):
        f = self.Rnd.random()
        items = self.optimize(c_c)
        if len(items) == 0:
            return "ChanceChooses not specified"
        sum = 0.0
        for chance, o in items:
            sum += chance
            if sum >= f:
                return o
        return items[len(items) - 1][1]
