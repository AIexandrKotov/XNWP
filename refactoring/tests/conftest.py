import pytest
from note import Note
from person import Person
from property import Property
from xnwpprofile import XNWPProfile


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
