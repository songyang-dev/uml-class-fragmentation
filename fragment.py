
# Ecore file format IO
from typing import Iterator, List
from pyecore.resources import ResourceSet, URI, global_registry
import pyecore.ecore as Ecore  # We get a reference to the Ecore metamodle implem.
from pyecore.resources.json import JsonResource

global_registry[Ecore.nsURI] = Ecore  # We load the Ecore metamodel first
rset = ResourceSet()

def load(name: str) -> Ecore.EPackage:
    """Load the root of the ecore xmi file

    Args:
        name (str): Name of the .ecore

    Returns:
        Ecore.EPackage: Root of the model
    """
    resource = rset.get_resource(URI(name))
    graphMMRoot : Ecore.EPackage = resource.contents[0]  # We get the root (an EPackage here)
    return graphMMRoot

def save(root: Ecore.EPackage, name: str):
    """Saves the ecore into a file

    Args:
        root (Ecore.EPackage): Ecore root
        name (str): Name of the file
    """
    new_resource = rset.create_resource(URI(name))
    new_resource.append(root)
    new_resource.save()
    return

"""
Fragmentation algorithm:
The fragmentation algorithm is supposed to divide the UML class diagram into pieces.
Each piece can be a class or an interface with all of its attributes.
A piece can also be a relationship between classes and/or interfaces. In this case,
each class and interface have no attributes.

The goal of fragments is to focus a human's attention on a part of the UML diagram,
in order to get a natural language description of the part.

Estimated fragment count per model is the sum of the number of classes/interfaces and
the number of relations.
"""    

def parse_args():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fragment ecore-file")
        sys.exit(1)
    else:
        return sys.argv[1]

def main():

    ecoreFile = parse_args()

    root = load(ecoreFile)
    classes : List[Ecore.EClass] = []
    enums: List[Ecore.EEnum] = []

    for content in root.eContents:
        if type(content) is Ecore.EClass:
            classes.append(content)
        elif type(content) is Ecore.EEnum:
            enums.append(content)
        else:
            raise Exception(str(content))

    # stats
    print(len(classes), "Classes")
    print(len(enums), "Enums")

    import os

    for index, c in enumerate(classes):
        name = f"{os.path.splitext(ecoreFile)[0]}"

        new_package = Ecore.EPackage(name=name, nsURI=root.nsURI, nsPrefix=root.nsPrefix)
        new_package.eClassifiers.extend([c])

        save(new_package, f"{name}_class{index}.ecore")

if __name__ == "__main__":
    main()