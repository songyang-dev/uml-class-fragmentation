"""
Fragment the plantuml file instead, using the plantuml-parser
"""
import os
import subprocess
from sys import argv

import inquire
import uml


def generate_json_from_plantuml(filename: str):

    return_code = subprocess.call(['node', 'plantuml-parser.js', filename])

    if return_code != 0:

        raise Warning("JSON generation failed, {}".format(filename))


def fragment(uml_model_path: str):

    json_file = uml_model_path.removesuffix(".plantuml") + ".json"
    if not os.path.isfile(json_file):
        generate_json_from_plantuml(uml_model_path)

    uml_model = inquire.get_json_uml(json_file)

    rel_index = 0

    # classes
    for index, uml_class in enumerate(uml_model.classes):

        class_fragment = "@startuml\n!theme plain"

        class_fragment += "\nclass {}".format(uml_class.name)

        class_fragment += "\n{"

        # associations

        for class_association in uml_class.associations:
            destination, multiplicity, name = class_association

            if multiplicity == "1..1":
                association = f'{uml_class.name} "1" --> "1" {destination}'
            elif multiplicity == "0..1":
                association = f'{uml_class.name} "0" --> "1" {destination}'
            elif multiplicity == "0..*":
                association = f'{uml_class.name} "0" --> "*" {destination}'
            elif multiplicity == "1..*":
                association = f'{uml_class.name} "1" --> "*" {destination}'
            else:
                association = f"{uml_class.name} --> {destination}"

            if name != "":
                association += f" : {name}"

            relation_fragment = "@startuml\n!theme plain\n{}\n@enduml".format(
                association)

            with open(os.path.join(OUT_LOCATION, f"{uml_model.package_name}_rel{rel_index}.plantuml"), "w") as out_file:
                out_file.write(relation_fragment)
                rel_index += 1

        # attribute
        for class_attribute in uml_class.attributes:
            attribute_name = class_attribute[0]
            attribute_type = class_attribute[1]

            if attribute_type == None:
                class_fragment += f"\n{attribute_name}"
            else:
                class_fragment += f"\n{attribute_name} : {attribute_type}"

        class_fragment += "\n}\n@enduml"

        with open(os.path.join(OUT_LOCATION, f"{uml_model.package_name}_class{index}.plantuml"), "w") as out_file:
            out_file.write(class_fragment)


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python fragment_plantuml.py plantuml-file out-location")
        exit(1)

    OUT_LOCATION = argv[2]
    fragment(argv[1])
