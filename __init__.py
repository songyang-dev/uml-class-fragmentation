from . import fragment_plantuml


def fragment(file, out_location):
    fragment_plantuml.OUT_LOCATION = out_location
    return fragment_plantuml.fragment(file)
