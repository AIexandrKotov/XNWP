import databases
import generators

databases.datas = {"names": ["Константин", "Акакий"]}

p = generators.Generators.db_choose_generator.to_default_property()
p.generator_arguments = {"db_name": "names"}

print(generators.Generators.get_value(p))

# logic.XNWPProfile(
#     notes=[("default", [])],
#     persons=[("default", [])],
#     sample_properties=[("default", [p])],
#     sample_persons=[("default", [])],
# ).savefile("abc.json")
