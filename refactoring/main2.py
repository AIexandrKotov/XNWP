import databases
import generators

databases.default_dbfiles = databases.Database(
    files=[
        databases.Datalist(
            filename="default",
            datasets=[
                databases.Dataset(
                    name="names",
                    description="default",
                    content=[
                        "Константин",
                        "Акакий",
                    ],
                )
            ],
        )
    ]
)
databases.user_dbfiles = databases.default_dbfiles

p = generators.Generators.db_choose_generator.to_default_property()
p.generator_arguments = {"db_name": "names"}

print(generators.Generators.get_value(p))

# logic.XNWPProfile(
#     notes=[("default", [])],
#     persons=[("default", [])],
#     sample_properties=[("default", [p])],
#     sample_persons=[("default", [])],
# ).savefile("abc.json")
