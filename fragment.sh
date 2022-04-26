#!/bin/bash

shopt -s expand_aliases

# Edit this path to your plantuml
alias plantuml="java -jar \"C:\Users\songy\Documents\My Documents\Scripts\Libs\plantuml\plantuml-1.2021.16.jar\""

if [ $# -ne 3 ] && [ $# -ne 1 ]; then
  echo "Usage: ./fragment.sh ecore-file [--parallelize number-of-cores]"
  exit 1
fi

# Paths where this script is
DIR="${BASH_SOURCE%/*}"

# Parallelization controls
parallelize=False
max_jobs=0
if [ $# -eq 3 ]; then
  parallelize=True
  max_jobs=$3
fi

# Executes the fragmentation algorithm
python "$DIR"/fragment.py "$1"

# Render
name=$(basename "$1")
folder=$(dirname "$1")
function render(){
  python "$DIR"/ecore2plant.py "$folder/$1" >"$folder/${1%.ecore}.plantuml"
  plantuml "$folder/${1%.ecore}.plantuml"
}

# Sequential
if [ "$parallelize" == "False" ]; then
  for file in "$folder/${name%.ecore}"_*.ecore; do
    render "$file"
  done
  
  # Parallelized
  # https://unix.stackexchange.com/questions/103920/parallelize-a-bash-for-loop#216475
else
  N=$max_jobs
  (
    for file in "$folder/${name%.ecore}"_*.ecore; do
      ((i = i % N))
      ((i++ == 0)) && wait
      render "$file" &
    done
  )
fi

# Render original file
python "$DIR"/ecore2plant.py "$1" >"${1%.ecore}.plantuml"
plantuml "$folder/${1%.ecore}.plantuml"
