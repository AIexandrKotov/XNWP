import typing

from logic import *
import copy

profile = Profile()

note1 = Note()
note1.tags.append("важное")
note1.text = "Вот у этих вот людей будут вот такие вот судьбы"

note2 = Note()
note2.tags.append("важное")
note2.tags.append("не забыть")
note2.text = "Этот персонаж выиграет в казино миллион даларов"

for x in [note1, note2]:
    profile.notes.append(x)

prop_name = Property()
prop_name.name = "Имя персонажа"
prop_name.value = "Безымянный"

prop_age = Property()
prop_age.name = "Возраст"
prop_age.generator = "Digit"
prop_age.genargs = {"lower": 10, "upper": 99}
next(prop_age)

prop_status = Property()
prop_status.name = "Статус в обществе"
prop_status.generator = "ChanceChoose"
prop_status.genargs = {
    "chance_chooses": [(0.1, "Нищий"), (0.2, "Средний класс"), (0.1, "Программист-работяга")]
} # dict[str, list[tuple[float, str]]]
next(prop_status)

print(prop_status)

for x in [prop_name, prop_age]:
    profile.sample_properties.append(x)

person1 = Person()
person1.properties.append(prop_name)
person1.properties.append(prop_age)
person1.tags = "Главные"

profile.sample_persons.append(person1)

Alex: Person = copy.deepcopy(profile.sample_persons[0])
Alex.properties[0].value = "Саня"
next(Alex.properties[1])

Kate: Person = copy.deepcopy(profile.sample_persons[0])
Kate.properties[0].value = "Катя"
next(Kate.properties[1])

profile.persons.append(Alex)
profile.persons.append(Kate)

s = profile.save()
profile.savefile("test.json")
# print(s)
# e = Profile.load(s)
# print(e.save())
# e = Profile.loadfile("test.json")
# print(e.persons)
