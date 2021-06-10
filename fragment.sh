#!/bin/bash

# Executes the fragmentation algorithm
python fragment.py "$1"

# Render
name=$(basename "$1")
for file in "$name"_"{class,rel}"*.ecore
do
    python ecore2plant.py "$file" > "${file%.ecore}.plantuml"
    plantuml "${file%.ecore}.plantuml"
done