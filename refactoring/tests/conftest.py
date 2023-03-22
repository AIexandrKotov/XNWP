import pytest
from logic import Note, Person, Property, XNWPProfile


@pytest.fixture()
def profile() -> XNWPProfile:
    return XNWPProfile(
        notes=[("base", [Note("Я хочу проверить сработает ли гитхаб экшнс")])],
        persons=[
            ("base", [Person([("base", [Property("Имя", "", "", "Челябинск", {})])])])
        ],
        sample_persons=[],
        sample_properties=[],
    )
