#!/bin/bash

# Edit this path to your plantuml
plantuml="~/Documents/Libs/JavaLib/plantuml.jar"

if [ $# -ne 1 ]
then
    echo "Usage: ./fragment.sh ecore-file"
    exit 1
fi

# Executes the fragmentation algorithm
python fragment.py "$1"

# Render
name=$(basename "$1")
for file in "${name%.ecore}"_*.ecore
do
    python ecore2plant.py "$file" > "${file%.ecore}.plantuml"
    java -jar $plantuml "${file%.ecore}.plantuml"
done