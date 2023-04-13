import databases
import generators
import logic

databases.default_dbfiles = databases.Database(files=[])
databases.user_dbfiles = databases.Database(files=[])

p = generators.Generators.db_choose_generator.to_default_property()
p.generator_arguments = {"db_name": "rus_male_names"}


logic.XNWPProfile(
    notes=[("default", [])],
    persons=[("default", [])],
    sample_properties=[("default", [p])],
    sample_persons=[("default", [])],
).savefile("abc.json")

databases.load()
print(generators.Generators.get_value(p))
databases.save()
