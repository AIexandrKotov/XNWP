import pytest
from logic import Note, Person, Property, XNWPProfile


@pytest.fixture()
def profile() -> XNWPProfile:
    return XNWPProfile(
        notes=[("base", [Note(text="Я хочу проверить сработает ли гитхаб экшнс")])],
        persons=[
            (
                "base",
                [
                    Person(
                        properties=[
                            (
                                "base",
                                [
                                    Property(
                                        name="Имя",
                                        generator="",
                                        icon="",
                                        value="Челябинск",
                                        generator_arguments={},
                                    )
                                ],
                            )
                        ]
                    )
                ],
            )
        ],
        sample_persons=[],
        sample_properties=[],
    )
