from logic import *

prop1 = Property()
prop1.name = "Name"
prop1.value = "Viktor Kisly"
prop2 = Property()
prop2.name = "Age"
prop2.value = 29
p1 = Person().add_property(prop1).add_property(prop2)
e = Profile()
e.persons = [p1]
s = e.save()
e.savefile("test.json")
print(s)
e = Profile.load(s)
print(e.save())
e = Profile.loadfile("test.json")
print(e.persons)