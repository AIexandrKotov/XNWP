from generators import Generators
from logic import XNWPProfile


def test_profile(profile: XNWPProfile) -> None:
    assert profile.saves() == XNWPProfile.loads(profile.saves()).saves()


def test_digit_generator() -> None:
    p = Generators.digit_generator.to_default_property()
    for _ in range(1000):
        assert Generators.get_value(p) in range(0, 100)
    p.generator_arguments = {"lower": 200, "upper": 300}
    for _ in range(1000):
        print(Generators.get_value(p))
        assert Generators.get_value(p) in range(200, 300)


def test_choose_generator() -> None:
    p = Generators.choose_generator.to_default_property()
    for _ in range(1000):
        assert Generators.get_value(p) in ["A", "B", "C"]
    p.generator_arguments = {"chooses": [1, 2, 3]}
    for _ in range(1000):
        assert Generators.get_value(p) in [1, 2, 3]


def test_raname_generator() -> None:
    p = Generators.raname_generator.to_default_property()
    print(Generators.get_value(p))
