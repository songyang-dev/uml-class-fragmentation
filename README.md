# UML Class Diagram Fragmentation
A UML class diagram contains classes and other types to convey code architecture. The fragmentation of a UML class diagram means separating one UML into many UMLs. Each smaller UML is either a class or a relationship between classes.

This fragmentation is meant to redirect the attention of human readers to important parts of the UML diagram. The goal of fragmentation is to allow easier labelling of UML with English prose, to eventually develop a machine learning model that can translate English to UML.

## Installation
Required packages and software are
* [pyecore](https://github.com/pyecore/pyecore), a Python library for manipulating Ecore's XMI files
* [plantuml](https://plantuml.com/), a Java JAR used for rendering UML into images
* Python 3+
* Java
* Bash

## Getting started
This repo is meant to be run using the `./fragment.sh ecore-file` command. Inside this script, you **must** edit the variable `plantuml` to a path pointing to the location of the plantuml jar. The fragmentation are stored in the folder of the ecore files.

After the fragmentation is complete, you may use `python create_sqlite3.py directory-of-fragments` to generate a SQLite3 database of the models and its fragments. Here are the schema.

```sql
CREATE TABLE models (
        name TEXT PRIMARY KEY,
        classes INTEGER,
        relations INTEGER
    );

CREATE TABLE fragments (
        kind TEXT,
        number INTEGER,
        model TEXT,
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY(model) REFERENCES models(name)
    );
```
