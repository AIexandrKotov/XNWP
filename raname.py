from dataclasses import dataclass, field
from random import Random


@dataclass
class Raname:
    random: Random = field(default_factory=Random, init=False)

    def random_element(self, lst: list[str]) -> str:
        return lst[self.random.randrange(0, len(lst))]

    def left_random(self, lst: list[str]) -> str:
        name: str = self.random_element(lst)
        right: int = self.random.randrange(0, len(name))
        return name[:right]

    def right_random(self, lst: list[str]) -> str:
        name: str = self.random_element(lst)
        left: int = self.random.randrange(0, len(name))
        return name[left:]

    def center_random(self, lst: list[str]) -> str:
        name: str = self.random_element(lst)
        left: int = self.random.randrange(0, len(name))
        right: int = self.random.randrange(left, len(name))
        return name[left:right]

    def random_random(self, lst: list[str]) -> str:
        choosed = self.random.randint(0, 2)
        if choosed == 0:
            return self.left_random(lst)
        elif choosed == 1:
            return self.center_random(lst)
        elif choosed == 2:
            return self.right_random(lst)
        return self.center_random(lst)

    def level1(self, lst: list[str], push_depth: bool = True) -> str:
        depth: str = "-1-> " if push_depth else ""
        return f"{depth}{self.random_element(lst)}"

    def level2(self, lst: list[str], push_depth: bool = True) -> str:
        depth: str = "-2-> " if push_depth else ""
        return f"{depth}{self.left_random(lst)}{self.right_random(lst)}"

    def level3(self, lst: list[str], push_depth: bool = True) -> str:
        depth: str = "-3-> " if push_depth else ""
        return f"{depth}{self.left_random(lst)}{self.center_random(lst)}{self.right_random(lst)}"

    def level_i(
        self,
        lst: list[str],
        depth: int,
        push_depth: bool = True,
        only_center: bool = True,
    ) -> str:
        if depth == 1:
            return self.level1(lst, push_depth)
        elif depth == 2:
            return self.level2(lst, push_depth)
        elif depth == 3:
            return self.level3(lst, push_depth)
        elif depth > 3:
            s = f"-{depth}-> " if push_depth else ""
            s += self.left_random(lst)
            for _ in range(depth - 2):
                s += self.center_random(lst) if only_center else self.random_random(lst)
            s += self.right_random(lst)
            return s
        else:
            raise ValueError("depth below zero")
